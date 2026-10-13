#!/usr/bin/env python3
"""HeyHi Design Bridge — Mode 2 geometric-primitive refinement (Phase 2, PRO-24).

When a frame primitive (a ring/badge) is traced as a wobbly path fused into the
subject silhouette — one connected ink component, no separable circular subpath —
the trace cannot be cleaned by dropping a subpath. Reconstruct it in raster space:

  1. fit_circle      robust circle fit to per-angle outer-edge points (Kasa + MAD
                     reject) -> centre, outer/inner radius, stroke, gap.
  2. erase_band      remove the THIN frame band at pure-frame angles only (object
                     crossings read thick and are kept).
  3. (re-trace)      the object alone -> clean object paths (delegated to the trace
                     pipeline; trace_object() is a convenience wrapper).
  4. arc_path_d      replace the primitive with TRUE geometry (a filled annular arc)
                     — mathematically perfect, the primitive is now a parameter.
  5. keyline         composite the arc UNDER the object with a managed keyline
                     (composite_keyline.py), so the object reads on top.

Generalises an earlier one-off ring fitter. Circle first; rounded-rect / capsule
are future fitters behind the same (fit -> arc) contract.

DRAFT in skill-updates/. Promotion is human-gated and happens with the Phase 5 docs.
Reuses composite_keyline.py (same dir). HeyHi Confidential.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import tempfile
from collections import deque

import numpy as np
from PIL import Image, ImageFilter

import composite_keyline as ck


# --------------------------------------------------------------------------- #
# colour sampling
# --------------------------------------------------------------------------- #

def sample_colors(rgb: np.ndarray):
    """Median ink (dark) and paper (bright) colours. Art is often not brand-originated
    (reference.md §4) — sample, do not assume the brand palette."""
    a = rgb.reshape(-1, 3).astype(float)
    lum = 0.299 * a[:, 0] + 0.587 * a[:, 1] + 0.114 * a[:, 2]
    ink = a[lum < 90]
    paper = a[lum > 180]
    med = lambda x: tuple(int(v) for v in np.median(x, axis=0))
    return med(ink), med(paper)


# --------------------------------------------------------------------------- #
# 1. fit (circle)
# --------------------------------------------------------------------------- #

def _kasa(P):
    x, y = P[:, 0], P[:, 1]
    M = np.c_[2 * x, 2 * y, np.ones(len(x))]
    b = x * x + y * y
    s, *_ = np.linalg.lstsq(M, b, rcond=None)
    a, bb, c = s
    return a, bb, math.sqrt(c + a * a + bb * bb)


def fit_circle(ink: np.ndarray, nbins: int = 720, ink_thresh: int = 110) -> dict:
    """Robust circle fit + inner edge + gap. Returns the frame descriptor dict."""
    H, W = ink.shape
    ys, xs = np.where(ink)
    c0 = np.array([xs.mean(), ys.mean()])
    ang = (np.degrees(np.arctan2(ys - c0[1], xs - c0[0])) + 360) % 360
    rad = np.hypot(xs - c0[0], ys - c0[1])
    b = (ang / 360 * nbins).astype(int) % nbins
    edge = []
    for k in range(nbins):
        m = b == k
        if m.any():
            r = rad[m].max()
            th = (k + 0.5) / nbins * 2 * math.pi
            edge.append((c0[0] + r * math.cos(th), c0[1] + r * math.sin(th)))
    P = np.array(edge, float)
    for _ in range(8):  # robust: reject non-circular outliers (object pokes)
        cx, cy, R_out = _kasa(P)
        res = np.hypot(P[:, 0] - cx, P[:, 1] - cy) - R_out
        mad = np.median(np.abs(res - np.median(res))) + 1e-6
        keep = np.abs(res - np.median(res)) < 3 * mad
        if keep.all():
            break
        P = P[keep]
    # inner edge + per-angle classification
    strokes, presence, inner_cream = [], np.zeros(nbins), np.zeros(nbins, bool)
    for k in range(nbins):
        th = (k + 0.5) / nbins * 2 * math.pi
        dx, dy = math.cos(th), math.sin(th)
        tinner, cnt = None, 0
        for rr in np.arange(R_out + 3, R_out - 40, -1):
            x, y = int(round(cx + rr * dx)), int(round(cy + rr * dy))
            if 0 <= x < W and 0 <= y < H and ink[y, x]:
                cnt += 1
                tinner = rr
            elif tinner is not None:
                break
        presence[k] = cnt
        if tinner is not None:
            xi, yi = int(round(cx + (tinner - 6) * dx)), int(round(cy + (tinner - 6) * dy))
            cream = not (0 <= xi < W and 0 <= yi < H and ink[yi, xi])
            inner_cream[k] = cream
            t = R_out - tinner + 1
            if cream and t < 40:
                strokes.append(t)
    stroke = float(np.median(strokes))
    R_in = R_out - stroke
    # gap = longest contiguous run where there is no thin ring band (presence>0 & cream inside)
    ring_here = ((presence > 0) & inner_cream).astype(int)
    ext = np.concatenate([ring_here, ring_here])
    runs, run, start = [], 0, 0
    for j in range(nbins * 2):
        if ext[j] == 0:
            if run == 0:
                start = j
            run += 1
        else:
            if run > 0:
                runs.append((run, start % nbins))
            run = 0
    runs.sort(reverse=True)
    gap_len, gs = runs[0]
    return {"cx": float(cx), "cy": float(cy), "R_out": float(R_out), "R_in": float(R_in),
            "stroke": stroke, "R_mid": (R_out + R_in) / 2, "nbins": nbins,
            "gap_start_deg": gs / nbins * 360, "gap_end_deg": (gs + gap_len) / nbins * 360,
            "gap_len_deg": gap_len / nbins * 360}


# --------------------------------------------------------------------------- #
# 2. erase the frame band (object crossings kept)
# --------------------------------------------------------------------------- #

def erase_band(rgb: np.ndarray, fit: dict, paper_rgb, ink_thresh: int = 110) -> np.ndarray:
    """Paint the thin frame band to `paper_rgb` at pure-frame angles only, leaving a
    clean object-only raster. Pure-frame = cream just inside R_in (no object behind)."""
    out = rgb.copy()
    L = np.asarray(Image.fromarray(rgb).convert("L"))
    H, W = L.shape
    ink = L < ink_thresh
    cx, cy, R_in, R_out, nb = fit["cx"], fit["cy"], fit["R_in"], fit["R_out"], fit["nbins"]
    inner_cream = np.zeros(nb, bool)
    for k in range(nb):
        th = (k + 0.5) / nb * 2 * math.pi
        xi = int(round(cx + (R_in - 8) * math.cos(th)))
        yi = int(round(cy + (R_in - 8) * math.sin(th)))
        inner_cream[k] = not (0 <= xi < W and 0 <= yi < H and ink[yi, xi])
    yy, xx = np.mgrid[0:H, 0:W]
    r = np.hypot(xx - cx, yy - cy)
    th = (np.degrees(np.arctan2(yy - cy, xx - cx)) + 360) % 360
    pure = inner_cream[(th / 360 * nb).astype(int) % nb]
    band = (r >= R_in - 2) & (r <= R_out + 3)
    out[band & pure & ink] = list(paper_rgb)
    return out


# --------------------------------------------------------------------------- #
# 4. true-geometry arc
# --------------------------------------------------------------------------- #

def arc_path_d(fit: dict, full_circle: bool = False) -> str:
    """Filled annular arc (M A L A Z) for the fitted circle, honouring the gap.
    full_circle=True ignores the gap (let a §4 keyline knockout open it instead)."""
    cx, cy, Ro, Ri = fit["cx"], fit["cy"], fit["R_out"], fit["R_in"]
    pt = lambda R, deg: (cx + R * math.cos(math.radians(deg)), cy + R * math.sin(math.radians(deg)))
    if full_circle:
        # two semicircle arcs out, two back
        o0, o1 = pt(Ro, 0), pt(Ro, 180)
        i1, i0 = pt(Ri, 180), pt(Ri, 0)
        return (f"M {o0[0]:.2f} {o0[1]:.2f} A {Ro:.2f} {Ro:.2f} 0 1 1 {o1[0]:.2f} {o1[1]:.2f} "
                f"A {Ro:.2f} {Ro:.2f} 0 1 1 {o0[0]:.2f} {o0[1]:.2f} Z "
                f"M {i0[0]:.2f} {i0[1]:.2f} A {Ri:.2f} {Ri:.2f} 0 1 0 {i1[0]:.2f} {i1[1]:.2f} "
                f"A {Ri:.2f} {Ri:.2f} 0 1 0 {i0[0]:.2f} {i0[1]:.2f} Z")
    a0, a1 = fit["gap_end_deg"], fit["gap_start_deg"]
    span = (a1 + 360) - a0
    large = 1 if span > 180 else 0
    Ox0, Oy0 = pt(Ro, a0); Ox1, Oy1 = pt(Ro, a1)
    Ix1, Iy1 = pt(Ri, a1); Ix0, Iy0 = pt(Ri, a0)
    return (f"M {Ox0:.2f} {Oy0:.2f} A {Ro:.2f} {Ro:.2f} 0 {large} 1 {Ox1:.2f} {Oy1:.2f} "
            f"L {Ix1:.2f} {Iy1:.2f} A {Ri:.2f} {Ri:.2f} 0 {large} 0 {Ix0:.2f} {Iy0:.2f} Z")


# --------------------------------------------------------------------------- #
# 3. object trace (convenience — the trace pipeline already exists)
# --------------------------------------------------------------------------- #

def _otsu(gray: np.ndarray) -> int:
    hist, _ = np.histogram(gray, bins=256, range=(0, 256))
    total = gray.size
    sum_all = np.dot(np.arange(256), hist)
    wB = sB = 0.0
    best_t, best_v = 127, -1.0
    for t in range(256):
        wB += hist[t]
        if wB == 0:
            continue
        wF = total - wB
        if wF == 0:
            break
        sB += t * hist[t]
        mB = sB / wB
        mF = (sum_all - sB) / wF
        v = wB * wF * (mB - mF) ** 2
        if v > best_v:
            best_v, best_t = v, t
    return best_t


def trace_object(object_rgb: np.ndarray, blur=3.5, despeckle=2,
                 turdsize=8, alphamax=1.1, opttol=1.6):
    """Blur+despeckle+Otsu (the mark preset) then potrace -> (path_ds, mono_mask)."""
    img = Image.fromarray(object_rgb).convert("RGB")
    if blur:
        img = img.filter(ImageFilter.GaussianBlur(blur))
    if despeckle:
        img = img.filter(ImageFilter.MedianFilter(2 * despeckle + 1))
    gray = np.asarray(img.convert("L"))
    mask = gray < _otsu(gray)
    d, transform = ck.potrace_path(mask, turdsize=turdsize, alphamax=alphamax, opttol=opttol)
    return d, transform, mask


# --------------------------------------------------------------------------- #
# orchestrate
# --------------------------------------------------------------------------- #

def refine(input_png: str, out_dir: str, keyline_width: int = 11, paper=None, ink=None):
    os.makedirs(out_dir, exist_ok=True)
    rgb = np.asarray(Image.open(input_png).convert("RGB"))
    if paper is None or ink is None:
        ink_rgb, paper_rgb = sample_colors(rgb)
    else:
        ink_rgb, paper_rgb = ink, paper
    fit = fit_circle(np.asarray(Image.fromarray(rgb).convert("L")) < 110)
    arc_d = arc_path_d(fit)
    object_rgb = erase_band(rgb, fit, paper_rgb)
    Image.fromarray(object_rgb).save(os.path.join(out_dir, "object_only.png"))
    obj_d, obj_tf, obj_mask = trace_object(object_rgb)
    ink_hex = "#%02X%02X%02X" % tuple(ink_rgb)
    paper_hex = "#%02X%02X%02X" % tuple(paper_rgb)
    # keyline: knock the dilated object out of the arc (reuse Phase 1)
    sub_d, sub_tf = ck.keyline_occlusion(obj_mask, keyline_width)
    # obj_d / sub_d are baked to viewBox coords at trace time (DEF-5 fixed at source),
    # so obj_tf / sub_tf are "" and art_transform is a defensive no-op (still correct
    # under bake=False). The reproduce assertion is what made this safe to simplify.
    svg = ck.knockout_svg(arc_d, [obj_d], sub_d, sub_tf, ink_hex,
                          title="refined emblem", art_transform=obj_tf)
    open(os.path.join(out_dir, "refined.svg"), "w").write(svg)
    json.dump(fit, open(os.path.join(out_dir, "fit.json"), "w"), indent=2)
    return {"fit": fit, "arc_d": arc_d, "object_d": obj_d, "svg": svg,
            "ink": ink_hex, "paper": paper_hex, "out_dir": out_dir}


def main(argv=None):
    ap = argparse.ArgumentParser(description="HeyHi Design Bridge — geometric-primitive refinement")
    ap.add_argument("--input", required=True, help="raster with the fused frame + object")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--keyline-width", type=int, default=11)
    ap.add_argument("--assert-fit", default=None, help="golden fit.json to match (cx/R_out/R_in)")
    ap.add_argument("--assert-erase", default=None, help="golden object-only PNG to match")
    a = ap.parse_args(argv)
    r = refine(a.input, a.out_dir, a.keyline_width)
    fit = r["fit"]
    print({"cx": round(fit["cx"], 1), "cy": round(fit["cy"], 1), "R_out": round(fit["R_out"], 1),
           "R_in": round(fit["R_in"], 1), "gap": (round(fit["gap_start_deg"], 1), round(fit["gap_end_deg"], 1)),
           "out": r["out_dir"]})
    if a.assert_fit:
        g = json.load(open(a.assert_fit))
        for k in ("cx", "cy", "R_out", "R_in"):
            assert abs(fit[k] - g[k]) < 1.0, f"fit.{k} {fit[k]:.2f} != golden {g[k]:.2f}"
        print("ASSERT fit: PASS (matches golden within 1px)")
    if a.assert_erase:
        gold = np.asarray(Image.open(a.assert_erase).convert("L")) < 110
        mine = np.asarray(Image.open(os.path.join(a.out_dir, "object_only.png")).convert("L")) < 110
        agree = (gold == mine).mean() * 100
        assert agree > 99.0, f"erase agreement {agree:.2f}% < 99%"
        print(f"ASSERT erase: PASS ({agree:.2f}% pixel agreement with the golden object-only raster)")
    return r


if __name__ == "__main__":
    main()
