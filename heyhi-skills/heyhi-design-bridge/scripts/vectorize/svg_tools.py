"""Shared SVG utilities for the HeyHi Design Bridge vectorizer.

Pure helpers, no side effects beyond the explicit rasterize call:
  - anchor counting (the craft metric: on-curve points per path)
  - palette extraction
  - rasterize-for-fidelity (via rsvg-convert) + dependency-free fidelity metrics

Anchor count is the headline number Vectorize reports. An "anchor" here is an
on-curve node (the point a designer drags in Figma), not a Bezier control handle.
Tracers emit only M/L/H/V/C/S/Q/T/Z; A is counted (1 per arc) but never emitted by
vtracer/potrace, so flattening (fit_curve) does not need arc support.

HeyHi Confidential.
"""
from __future__ import annotations

import os
import re
import subprocess
import xml.etree.ElementTree as ET

import numpy as np
from PIL import Image

# --------------------------------------------------------------------------- #
# Path tokenizing + anchor counting
# --------------------------------------------------------------------------- #

_TOKEN_RE = re.compile(
    r"([MmLlHhVvCcSsQqTtAaZz])|([-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?)"
)
# on-curve args consumed per command (the trailing point is the anchor)
_ARGS = {"M": 2, "L": 2, "H": 1, "V": 1, "C": 6, "S": 4, "Q": 4, "T": 2, "A": 7, "Z": 0}


def _tokenize_path(d: str):
    out = []
    for m in _TOKEN_RE.finditer(d):
        if m.group(1):
            out.append(("cmd", m.group(1)))
        else:
            out.append(("num", float(m.group(2))))
    return out


def count_anchors_in_path(d: str) -> int:
    """Count on-curve anchor points in one path `d` string.

    Handles implicit command repetition (e.g. `L 1 2 3 4` = two anchors) and the
    M->L implicit-lineto rule. Z adds no anchor.
    """
    toks = _tokenize_path(d)
    n_anchor = 0
    i, N = 0, len(toks)
    cmd = None
    while i < N:
        kind, val = toks[i]
        if kind == "cmd":
            cmd = val
            i += 1
            if cmd.upper() == "Z":
                cmd = None
                continue
            if i >= N:
                break
        if cmd is None:
            i += 1
            continue
        base = cmd.upper()
        nargs = _ARGS[base]
        if nargs == 0:
            cmd = None
            continue
        if i + nargs <= N and all(toks[j][0] == "num" for j in range(i, i + nargs)):
            n_anchor += 1
            i += nargs
            if base == "M":  # subsequent coordinate pairs are implicit linetos
                cmd = "l" if cmd == "m" else "L"
        else:
            i += 1  # malformed run; step past to avoid a stall
    return n_anchor


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def count_anchors_svg(svg: str) -> int:
    """Total anchors across every drawable element in an SVG (string or path)."""
    svg_text = _read(svg)
    total = 0
    try:
        root = ET.fromstring(svg_text)
    except ET.ParseError:
        # fall back to a raw scan of path data
        for m in re.finditer(r'\bd\s*=\s*"([^"]*)"', svg_text):
            total += count_anchors_in_path(m.group(1))
        return total
    for el in root.iter():
        tag = _local(el.tag)
        if tag == "path" and el.get("d"):
            total += count_anchors_in_path(el.get("d"))
        elif tag in ("rect",):
            total += 4
        elif tag in ("circle", "ellipse"):
            total += 4  # conventional 4-anchor representation
        elif tag == "line":
            total += 2
        elif tag in ("polygon", "polyline"):
            pts = re.findall(r"[-+0-9.eE]+", el.get("points", ""))
            total += len(pts) // 2
    return total


def path_anchor_breakdown(svg: str):
    """Return [(path_index, anchor_count)] for every <path> — used to target curve-fit."""
    svg_text = _read(svg)
    out = []
    for idx, m in enumerate(re.finditer(r'\bd\s*=\s*"([^"]*)"', svg_text)):
        out.append((idx, count_anchors_in_path(m.group(1))))
    return out


# --------------------------------------------------------------------------- #
# Palette
# --------------------------------------------------------------------------- #

def _norm_hex(c: str):
    c = c.strip().lower()
    if c == "none":
        return None
    m = re.match(r"rgb\(\s*([0-9.]+)[, ]+([0-9.]+)[, ]+([0-9.]+)", c)
    if m:
        r, g, b = (int(round(float(x))) for x in m.groups())
        return f"#{r:02x}{g:02x}{b:02x}"
    if c.startswith("#"):
        h = c[1:]
        if len(h) == 3:
            h = "".join(ch * 2 for ch in h)
        if len(h) >= 6:
            return "#" + h[:6]
    return None


def palette_svg(svg: str):
    """Distinct fill/stroke colors in an SVG, normalized to #rrggbb (sorted)."""
    svg_text = _read(svg)
    colors = set()
    for m in re.finditer(r"(?:fill|stroke)\s*[:=]\s*[\"']?\s*(#[0-9a-fA-F]{3,8}|rgb\([^)]*\)|none)", svg_text):
        h = _norm_hex(m.group(1))
        if h:
            colors.add(h)
    return sorted(colors)


def _hex_to_rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def snap_fills_to_palette(svg_text: str, palette_hexes):
    """Rewrite every fill/stroke color to the nearest brand-palette color.

    Tracers (vtracer) re-cluster and introduce boundary-blend shades even from a
    palette-locked input — e.g. a saturated blue drifts a step or two per channel, ink
    splits into two near-blacks. Snapping guarantees the output carries exactly the brand palette and
    that brand-critical accents survive. It changes only color values, never geometry,
    so anchor count is unaffected.
    """
    pal = [_hex_to_rgb(h) for h in palette_hexes]
    pal_hex = ["#%02x%02x%02x" % _hex_to_rgb(h) for h in palette_hexes]

    def nearest(col_hex):
        rgb = _hex_to_rgb(col_hex)
        k = min(range(len(pal)), key=lambda j: sum((a - b) ** 2 for a, b in zip(rgb, pal[j])))
        return pal_hex[k]

    def repl(m):
        attr, col = m.group(1), m.group(2)
        if col.lower() == "none":
            return m.group(0)
        return f'{attr}="{nearest(col)}"'

    return re.sub(r'(fill|stroke)="(#[0-9a-fA-F]{3,8}|none)"', repl, svg_text)


def palette_raster(img: Image.Image, max_colors: int = 64):
    """Distinct colors actually present in a raster, most-common first."""
    rgb = img.convert("RGB")
    counts = rgb.getcolors(maxcolors=1_000_000) or []
    counts.sort(key=lambda c: -c[0])
    return ["#%02x%02x%02x" % col for _, col in counts[:max_colors]]


# --------------------------------------------------------------------------- #
# Rasterize + fidelity (rsvg-convert; dependency-free metrics)
# --------------------------------------------------------------------------- #

def rasterize_svg(svg_path: str, w: int, h: int, out_png: str, background: str = "white"):
    cmd = ["rsvg-convert", svg_path, "-w", str(w), "-h", str(h), "-o", out_png]
    if background:
        cmd += ["--background-color", background]
    subprocess.run(cmd, check=True, capture_output=True)
    return out_png


def _to_array(path_or_img, size):
    im = path_or_img if isinstance(path_or_img, Image.Image) else Image.open(path_or_img)
    im = im.convert("RGB").resize(size, Image.LANCZOS)
    return np.asarray(im, dtype=np.float64)


def pixel_agreement(a: np.ndarray, b: np.ndarray, tol: int = 16) -> float:
    """Fraction of pixels whose worst channel differs by <= tol."""
    return float((np.abs(a - b).max(axis=2) <= tol).mean())


def psnr(a: np.ndarray, b: np.ndarray) -> float:
    mse = float(np.mean((a - b) ** 2))
    return 99.0 if mse == 0 else float(10 * np.log10(255.0 ** 2 / mse))


def block_ssim(a: np.ndarray, b: np.ndarray, block: int = 8) -> float:
    """Mean SSIM over non-overlapping luma blocks. Pure numpy, no scikit-image."""
    ga, gb = a.mean(axis=2), b.mean(axis=2)
    H, W = ga.shape
    H2, W2 = (H // block) * block, (W // block) * block
    if H2 == 0 or W2 == 0:
        return float("nan")
    def blocks(g):
        g = g[:H2, :W2]
        return (g.reshape(H2 // block, block, W2 // block, block)
                 .transpose(0, 2, 1, 3).reshape(-1, block * block))
    ba, bb = blocks(ga), blocks(gb)
    C1, C2 = (0.01 * 255) ** 2, (0.03 * 255) ** 2
    ma, mb = ba.mean(1), bb.mean(1)
    va, vb = ba.var(1), bb.var(1)
    cov = ((ba - ma[:, None]) * (bb - mb[:, None])).mean(1)
    ssim = ((2 * ma * mb + C1) * (2 * cov + C2)) / ((ma ** 2 + mb ** 2 + C1) * (va + vb + C2))
    return float(ssim.mean())


def fidelity(svg_path: str, reference, scales=(64, 768), background="white", tmp="/tmp"):
    """Re-rasterize the traced SVG at each scale and compare to a reference raster.

    `reference` is a PNG path or PIL.Image (the quantized target or the original
    source). Returns {scale: {agreement, psnr, ssim}} — a proxy. Final visual
    judgment stays human (icon + hero scale), per the plan.
    """
    ref_img = reference if isinstance(reference, Image.Image) else Image.open(reference)
    out = {}
    for s in scales:
        png = os.path.join(tmp, f"_fidelity_{s}.png")
        rasterize_svg(svg_path, s, s, png, background=background)
        a = _to_array(png, (s, s))
        b = _to_array(ref_img, (s, s))
        out[s] = {
            "agreement": round(pixel_agreement(a, b), 4),
            "psnr": round(psnr(a, b), 2),
            "ssim": round(block_ssim(a, b), 4),
        }
    return out


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #

def _read(svg: str) -> str:
    if "<" in svg and ">" in svg:  # looks like markup, not a path
        return svg
    if os.path.exists(svg):
        with open(svg, "r", encoding="utf-8") as f:
            return f.read()
    return svg  # treat as a bare path-data string


if __name__ == "__main__":
    import sys
    for p in sys.argv[1:]:
        print(f"{p}: anchors={count_anchors_svg(p)} palette={palette_svg(p)}")
