#!/usr/bin/env python3
"""Generate the Vectorize golden raster inputs — synthetic, fully local.

No external generative service is touched (the data-handling default). Two goldens, named
and colored by presets.GOLDENS (generic: a neutral example mark and palette; an instance
overrides them in instance_calibration.GOLDENS to calibrate against its own mark and brand):
  - <mark_name>.png       the hand-authored mark SVG, rasterized + softened to mimic a
                          generated raster (a stand-in for a Nano Banana mark)
  - <emblem_name>.png     a flat-color, limited-palette illustration with curved
                          boundaries (the real test of curve anchor economy)

Both get light Gaussian softening + mild noise so the tracer faces a realistic edge,
not a razor-clean synthetic one. Seeded, so the set regenerates byte-stably. These
are SYNTHETIC stand-ins; ratified ceilings must be re-checked against true Nano Banana
output before a real engagement (flagged in the calibration report).

HeyHi Confidential.
"""
from __future__ import annotations

import os
import subprocess

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import presets as P

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.normpath(os.path.join(HERE, "..", ".."))  # scripts/vectorize -> skill root
MARK_SVG = os.path.join(SKILL, P.GOLDENS["mark_svg"])
MARK_NAME = P.GOLDENS["mark_name"]
EMBLEM_NAME = P.GOLDENS["emblem_name"]
OUT_DIR = os.path.join(SKILL, "examples", "vectorize", "sources")

SIZE = 1024
SEED = 611  # 2026-06-11


def _rgb(hex_color):
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


# The emblem palette, by role (presets.GOLDENS["palette"]).
_PAL = P.GOLDENS["palette"]
PAPER = _rgb(_PAL["paper"])
INK = _rgb(_PAL["ink"])
ACCENT = _rgb(_PAL["accent"])    # the flow band
ACCENT2 = _rgb(_PAL["accent2"])  # the central ring
GRAY = _rgb(_PAL["gray"])
TINT = _rgb(_PAL["tint"])


def _soften(img, blur=0.8, noise_sigma=3.0, rng=None):
    img = img.filter(ImageFilter.GaussianBlur(radius=blur))
    if noise_sigma > 0:
        rng = rng or np.random.default_rng(SEED)
        arr = np.asarray(img.convert("RGB"), dtype=np.float64)
        arr += rng.normal(0, noise_sigma, arr.shape)
        img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    return img


def _clean_path(path):
    base, ext = os.path.splitext(path)
    return base + ".clean" + ext


def make_mark_mono(path):
    """Rasterize the hand-authored mark to a softened mono-ish raster."""
    png = path + ".raw.png"
    subprocess.run(["rsvg-convert", MARK_SVG, "-w", str(SIZE), "-h", str(SIZE),
                    "-o", png, "--background-color", "white"], check=True)
    clean = Image.open(png).convert("RGB")
    clean.save(_clean_path(path))  # noise-free reference (whole-pipeline fidelity)
    img = _soften(clean, blur=1.2, noise_sigma=2.5, rng=np.random.default_rng(SEED))
    img.save(path)
    os.remove(png)
    return path


def _wave_band(draw, y0, amp, thickness, color, phase=0.0, n=200):
    """A curved horizontal band — gives vtracer real curves to economize."""
    xs = np.linspace(0, SIZE, n)
    top = [(x, y0 + amp * np.sin(2 * np.pi * (x / SIZE) + phase)) for x in xs]
    bot = [(x, y0 + thickness + amp * np.sin(2 * np.pi * (x / SIZE) + phase)) for x in xs]
    draw.polygon(top + bot[::-1], fill=color)


def make_illustration(path):
    """Flat-color, limited-palette emblem: 'work flowing through a system'."""
    rng = np.random.default_rng(SEED + 1)
    S = SIZE * 2  # supersample for clean anti-aliased edges, then downscale
    img = Image.new("RGB", (S, S), PAPER)
    d = ImageDraw.Draw(img)

    # soft tint backdrop ellipse
    d.ellipse([S * 0.08, S * 0.18, S * 0.92, S * 0.82], fill=TINT)
    # curved flow band (accent)
    _wave_band(ImageDraw.Draw(img), y0=S * 0.46, amp=S * 0.05, thickness=S * 0.06,
               color=ACCENT, phase=0.3)
    # two rounded-square nodes (ink outline feel via filled gray + paper inset)
    for cx in (S * 0.24, S * 0.76):
        d.rounded_rectangle([cx - S * 0.13, S * 0.34, cx + S * 0.13, S * 0.60],
                            radius=S * 0.04, fill=GRAY)
        d.rounded_rectangle([cx - S * 0.10, S * 0.37, cx + S * 0.10, S * 0.57],
                            radius=S * 0.03, fill=PAPER)
    # central loop (accent2 ring) + ink core
    cx, cy, r = S * 0.5, S * 0.47, S * 0.11
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ACCENT2)
    d.ellipse([cx - r * 0.55, cy - r * 0.55, cx + r * 0.55, cy + r * 0.55], fill=PAPER)
    d.ellipse([cx - r * 0.22, cy - r * 0.22, cx + r * 0.22, cy + r * 0.22], fill=INK)
    # three accent dots (ink)
    for fx in (0.34, 0.5, 0.66):
        d.ellipse([S * fx - S * 0.012, S * 0.70, S * fx + S * 0.012, S * 0.70 + S * 0.024], fill=INK)

    clean = img.resize((SIZE, SIZE), Image.LANCZOS)
    clean.save(_clean_path(path))  # noise-free reference (whole-pipeline fidelity)
    img = _soften(clean, blur=0.7, noise_sigma=2.0, rng=rng)
    img.save(path)
    return path


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    m = make_mark_mono(os.path.join(OUT_DIR, MARK_NAME + ".png"))
    i = make_illustration(os.path.join(OUT_DIR, EMBLEM_NAME + ".png"))
    print("wrote:", m)
    print("wrote:", i)


if __name__ == "__main__":
    main()
