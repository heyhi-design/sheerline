#!/usr/bin/env python3
"""HeyHi Design Bridge — Vectorize (Nano Banana raster -> craft SVG).

Pipeline (plan s5, reference.md s4):
  1. quantize   Pillow, dithering OFF, despeckle (+ light pre-blur for marks)
  2. trace      potrace (mono) / vtracer (color), tuned for few points
  3. cleanup    SVGO, conservative (precision only; viewBox + color layers kept)
  4. curve-fit  optional Schneider refit of any path over an anchor budget (never RDP)
  5. report     one-line craft report: anchors, palette, before/after reduction
  6. land       separate step (use_figma / logo.marks) — see SKILL.md Mode 2 step 6

Human polish is the primary craft surface and the only hand-work; this tool gets
the path most of the way and says so — it never pretends the craft is finished.

Trace + simplify is fully local. Generation (upstream) is the only step that would
touch an external provider; this script does not generate.

Usage:
  python3 vectorize.py INPUT.png --class mark|illustration [--out OUT.svg]
      [--engine auto|potrace|vtracer] [--colors N] [--mono] [--invert]
      [--curve-fit] [--curve-fit-threshold N] [--curve-fit-error PX]
      [--fidelity] [--json REPORT.json] [--quiet]

HeyHi Confidential.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image, ImageFilter

import presets as P
import svg_tools as st

HERE = os.path.dirname(os.path.abspath(__file__))
SVGO_CONFIG = os.path.join(HERE, "svgo.config.mjs")


# --------------------------------------------------------------------------- #
# 1. quantize
# --------------------------------------------------------------------------- #

def _otsu(gray: np.ndarray) -> int:
    hist, _ = np.histogram(gray, bins=256, range=(0, 256))
    total = gray.size
    sum_all = np.dot(np.arange(256), hist)
    w_b = s_b = 0.0
    best_t, best_var = 127, -1.0
    for t in range(256):
        w_b += hist[t]
        if w_b == 0:
            continue
        w_f = total - w_b
        if w_f == 0:
            break
        s_b += t * hist[t]
        m_b = s_b / w_b
        m_f = (sum_all - s_b) / w_f
        var = w_b * w_f * (m_b - m_f) ** 2
        if var > best_var:
            best_var, best_t = var, t
    return best_t


def _palette_image(hexes):
    pal = []
    for h in hexes:
        h = h.lstrip("#")
        pal += [int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)]
    pal += [0, 0, 0] * (256 - len(hexes))  # pad to a full 256-entry palette
    pi = Image.new("P", (1, 1))
    pi.putpalette(pal)
    return pi


def quantize(img: Image.Image, colors: int, blur: float, despeckle: int,
             mono: bool, invert: bool, palette=None):
    """Return (raster_for_trace, palette_list, mode_str). dithering OFF always.

    If `palette` (a list of brand hex colors) is given, snap to it — guaranteeing the
    brand colors survive. Otherwise mediancut to `colors`.
    """
    img = img.convert("RGBA")
    bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
    img = Image.alpha_composite(bg, img).convert("RGB")  # flatten transparency on white

    if blur and blur > 0:
        img = img.filter(ImageFilter.GaussianBlur(radius=blur))
    if despeckle and despeckle > 0:
        size = 2 * despeckle + 1
        img = img.filter(ImageFilter.MedianFilter(size=size))

    if mono:
        gray = np.asarray(img.convert("L"))
        t = _otsu(gray)
        bw = img.convert("L").point(lambda x, t=t: (255 if x >= t else 0)).convert("1")
        if invert:
            bw = bw.point(lambda x: 255 - x).convert("1")
        return bw, ["#000000"], "mono"

    if palette:
        q = img.quantize(palette=_palette_image(palette), dither=Image.Dither.NONE)
    else:
        q = img.quantize(colors=colors, method=Image.Quantize.MEDIANCUT,
                         dither=Image.Dither.NONE)
    rgb = q.convert("RGB")
    return rgb, st.palette_raster(rgb, max_colors=max(colors, len(palette or []))), "color"


# --------------------------------------------------------------------------- #
# 2. trace
# --------------------------------------------------------------------------- #

def trace_potrace(bw: Image.Image, params: dict, out_svg: str, tmp: str):
    pbm = os.path.join(tmp, "_trace.pbm")
    bw.save(pbm)
    cmd = ["potrace", "-s", "-o", out_svg,
           "--turdsize", str(params.get("turdsize", 2)),
           "--alphamax", str(params.get("alphamax", 1.0)),
           "--opttolerance", str(params.get("opttolerance", 0.2)),
           pbm]
    subprocess.run(cmd, check=True, capture_output=True)
    return out_svg


def trace_vtracer(rgb: Image.Image, params: dict, out_svg: str, tmp: str):
    import vtracer
    png = os.path.join(tmp, "_trace.png")
    rgb.save(png)
    vtracer.convert_image_to_svg_py(
        png, out_svg,
        colormode=params.get("colormode", "color"),
        hierarchical=params.get("hierarchical", "stacked"),
        mode=params.get("mode", "spline"),
        filter_speckle=int(params.get("filter_speckle", 4)),
        color_precision=int(params.get("color_precision", 6)),
        corner_threshold=int(params.get("corner_threshold", 60)),
        splice_threshold=int(params.get("splice_threshold", 45)),
        path_precision=int(params.get("path_precision", 3)),
    )
    return out_svg


# --------------------------------------------------------------------------- #
# 3. cleanup (svgo)
# --------------------------------------------------------------------------- #

def svgo_cleanup(in_svg: str, out_svg: str):
    try:
        r = subprocess.run(
            ["npx", "--yes", "svgo", "--config", SVGO_CONFIG, "-i", in_svg, "-o", out_svg],
            check=True, capture_output=True, text=True, timeout=180,
        )
        return out_svg, True, ""
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError) as e:
        msg = getattr(e, "stderr", "") or str(e)
        # graceful degradation: keep the traced SVG, flag it
        with open(in_svg) as f, open(out_svg, "w") as g:
            g.write(f.read())
        return out_svg, False, msg.strip()[:200]


# --------------------------------------------------------------------------- #
# orchestrate
# --------------------------------------------------------------------------- #

def run(input_path, asset_class, out_svg=None, engine="auto", colors=None,
        mono=False, invert=False, curve_fit=None, cf_threshold=40, cf_error=None,
        do_fidelity=False, tmp=None, preset_override=None, palette=None, tier="flat"):
    preset = preset_override or P.preset_for(asset_class)
    colors = colors if colors is not None else preset["quantize_colors"]
    palette = palette if palette is not None else preset.get("palette")
    # curve-fit: explicit caller value wins; otherwise the preset decides (off for marks,
    # on for illustrations) — corners are human polish, smooth over-segmentation is not.
    if curve_fit is None:
        curve_fit = preset.get("curve_fit", False)
    if cf_error is None:
        cf_error = preset.get("curve_fit_error", 1.5)
    if engine == "auto":
        engine = preset["engine"]
    if engine == "potrace":
        mono = True  # potrace is a black/white tracer
    if out_svg is None:
        out_svg = os.path.splitext(input_path)[0] + ".svg"
    tmp = tmp or tempfile.mkdtemp(prefix="vectorize_")

    flags = []
    img = Image.open(input_path)
    src_size = img.size

    raster, out_palette, mode = quantize(
        img, colors=(2 if mono else colors),
        blur=preset.get("blur_radius", 0.0), despeckle=preset.get("despeckle", 0),
        mono=mono, invert=invert, palette=(None if mono else palette),
    )

    traced = os.path.join(tmp, "_traced.svg")
    if engine == "potrace":
        trace_potrace(raster, preset["potrace"], traced, tmp)
    else:
        trace_vtracer(raster, preset["vtracer"], traced, tmp)
    anchors_trace = st.count_anchors_svg(traced)

    cleaned, ok, msg = svgo_cleanup(traced, out_svg)
    if not ok:
        flags.append({"stage": "svgo", "issue": "cleanup failed; using raw trace", "detail": msg})
    anchors_svgo = st.count_anchors_svg(cleaned)

    cf_stats = None
    if curve_fit:
        import path_ops
        with open(cleaned) as f:
            svg_text = f.read()
        new_svg, cf_stats = path_ops.curve_fit_svg(svg_text, cf_threshold, cf_error)
        with open(out_svg, "w") as f:
            f.write(new_svg)
        if cf_stats["skipped_arc"]:
            flags.append({"stage": "curve-fit", "issue": f"{cf_stats['skipped_arc']} path(s) left untouched (unsupported command)"})

    # palette-lock snap: map traced fills back to exact brand tokens (color only, not
    # geometry), so the tracer's boundary-blend shades cannot drift the brand palette.
    if palette and not mono:
        with open(out_svg) as f:
            snapped = st.snap_fills_to_palette(f.read(), palette)
        with open(out_svg, "w") as f:
            f.write(snapped)

    anchors_final = st.count_anchors_svg(out_svg)
    final_palette = ["#000000"] if mode == "mono" else st.palette_svg(out_svg)

    ceiling = P.ceiling_for(asset_class, tier)
    human_judged = P.is_human_judged(asset_class, tier)
    fidelity = None
    if do_fidelity:
        # Compare the final vector against the QUANTIZED flat target — the image the
        # tracer actually consumed. Comparing to the raw source would penalize the
        # trace for correctly rejecting input noise; quantize already removed it. This
        # reference is also production-available (no clean original is assumed).
        quant_ref = raster.convert("RGB") if mode == "mono" else raster
        fidelity = st.fidelity(out_svg, quant_ref, scales=P.FIDELITY_SCALES, tmp=tmp)

    reduction_pct = (round(100 * (anchors_trace - anchors_final) / anchors_trace, 1)
                     if anchors_trace else 0.0)

    report = {
        "input": input_path,
        "asset_class": asset_class,
        "engine": engine,
        "src_size": list(src_size),
        "quantize_colors": (2 if mono else colors),
        "palette_locked": bool(palette) and not mono,
        "palette": final_palette,
        "palette_count": len(final_palette),
        "anchors": {
            "trace": anchors_trace,
            "after_svgo": anchors_svgo,
            "final": anchors_final,
        },
        "reduction_vs_trace_pct": reduction_pct,
        "curve_fit": cf_stats,
        "ceiling": {
            "ratified": P.CEILINGS.get("ratified", False),
            "tier": tier,
            "anchors_max": ceiling,
            "human_judged": human_judged,
            "within": (None if ceiling is None else anchors_final <= ceiling),
        },
        "fidelity": fidelity,
        "output_svg": out_svg,
        "flags": flags,
        "craft_note": ("Pipeline got it most of the way. Human polish is the primary "
                       "craft surface: reposition anchors, restore intentional corners "
                       "the tracer rounded, lock the brand palette, test at icon + hero "
                       "scale. The tool does not pretend the craft is finished."),
    }
    return report


def one_line(r: dict) -> str:
    a = r["anchors"]
    parts = [
        f"vectorize: {r['asset_class']} · {r['engine']} · {r['palette_count']} colors",
        f"{a['final']} anchors (trace {a['trace']} → final {a['final']}, -{r['reduction_vs_trace_pct']}%)",
    ]
    if r.get("fidelity"):
        scs = sorted(r["fidelity"])
        ic, he = scs[0], scs[-1]
        parts.append(f"fidelity ssim {r['fidelity'][ic]['ssim']:.2f}/{r['fidelity'][he]['ssim']:.2f} (icon/hero vs target)")
    c = r["ceiling"]
    if not c["ratified"]:
        parts.append("ceiling: not yet ratified (Phase V.0)")
    elif c.get("human_judged"):
        parts.append(f"ceiling[{c['tier']}]: human-judged (anchors reported, not gated)")
    elif c["anchors_max"] is None:
        parts.append(f"ceiling[{c['tier']}]: n/a")
    else:
        parts.append(f"ceiling[{c['tier']}] {c['anchors_max']}: {'WITHIN' if c['within'] else 'OVER'}")
    parts.append("→ your turn: polish corners, lock palette, test at scale")
    return "  ·  ".join(parts)


def main(argv=None):
    ap = argparse.ArgumentParser(description="HeyHi Design Bridge — Vectorize")
    ap.add_argument("input")
    ap.add_argument("--class", dest="asset_class", required=True, choices=["mark", "illustration"])
    ap.add_argument("--tier", default="flat",
                    help="flat (default) | organic (mark: animal/figure silhouettes) | "
                         "detailed (illustration: woodcut/engraving — human-judged, not gated)")
    ap.add_argument("--out", default=None)
    ap.add_argument("--engine", default="auto", choices=["auto", "potrace", "vtracer"])
    ap.add_argument("--colors", type=int, default=None)
    ap.add_argument("--palette", default=None,
                    help="comma-separated brand hex colors to snap to (palette-lock); "
                         "overrides the preset palette")
    ap.add_argument("--mono", action="store_true")
    ap.add_argument("--invert", action="store_true")
    ap.add_argument("--curve-fit", dest="curve_fit", action=argparse.BooleanOptionalAction,
                    default=None, help="force curve-fit on/off; default = the class preset")
    ap.add_argument("--curve-fit-threshold", dest="cf_threshold", type=int, default=40)
    ap.add_argument("--curve-fit-error", dest="cf_error", type=float, default=None)
    ap.add_argument("--fidelity", action="store_true")
    ap.add_argument("--json", dest="json_out", default=None)
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)

    palette = [c.strip() for c in args.palette.split(",")] if args.palette else None
    report = run(
        args.input, args.asset_class, out_svg=args.out, engine=args.engine,
        colors=args.colors, mono=args.mono, invert=args.invert,
        curve_fit=args.curve_fit, cf_threshold=args.cf_threshold, cf_error=args.cf_error,
        do_fidelity=args.fidelity, palette=palette, tier=args.tier,
    )
    if args.json_out:
        with open(args.json_out, "w") as f:
            json.dump(report, f, indent=2)
    if not args.quiet:
        print(one_line(report))
    return report


if __name__ == "__main__":
    main()
