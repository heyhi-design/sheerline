"""Per-class vectorize presets + the anchor-ceiling slot (the mechanism, generic defaults).

Scaffold vs instance. This file ships the mechanism and generic starting values: no palette
lock, and UNRATIFIED ceilings with `None` targets, so Vectorize asserts no numeric target
until an instance calibrates and ratifies its own. calibrate.py proposes numbers against the
instance's own art; only the instance owner's ratification records them.

An instance records its calibration in `instance_calibration.py` beside this file
(optional; see `_apply_instance` below): `PALETTE` (brand hex colors for palette-locked
quantization), `CEILINGS` (same shape as the generic block here, `ratified: True`), and
optionally `GOLDENS` (the mark and palette make_goldens.py calibrates against). The
instance file is instance-only: it never ships in a scaffold export.

HeyHi Confidential.
"""
from __future__ import annotations

import importlib.util
import os

# Palette for palette-locked quantization (the plan's "brand-config color tokens" quantize
# target). Snapping to a fixed brand palette keeps brand-critical accents from being averaged
# into a muddy merge; SSIM alone does not protect them because they are small relative to the
# background. Generic default: none. A client engagement passes its own via --palette; an
# instance sets its default in instance_calibration.PALETTE.
DEFAULT_PALETTE = None
# Brand accents calibrate.py requires to survive an illustration trace. Generic: none.
ACCENTS = ()

# The synthetic golden inputs make_goldens.py generates for calibrate.py: a mono mark
# (rasterized from a hand-authored SVG, whose anchor count is the polish target) and a
# limited-palette emblem drawn in six roles. Generic: a neutral example mark and a neutral
# palette. An instance calibrating against its own mark and brand colors overrides any of
# these keys in instance_calibration.GOLDENS. Paths are relative to the skill folder.
GOLDENS = {
    "mark_svg": "examples/assets/example-mark.svg",
    "mark_name": "example-mark-mono",
    "emblem_name": "example-emblem",
    "palette": {
        "paper": "#F8F8F8", "ink": "#1C1C1C", "accent": "#E4572E",
        "accent2": "#2B59C3", "gray": "#6B6B6B", "tint": "#E6E6E6",
    },
}

# Trace-time parameters (the primary lever for low anchor count). reference.md s4.
PRESETS = {
    "mark": {
        # Mono marks trace cleanest through potrace; few-color marks fall back to vtracer.
        # Starting values from the reference sweep (reference.md section 4). Curve-fit OFF:
        # a mark is corners, and refitting rounds them; corner work is the human polish.
        "engine": "potrace",
        "quantize_colors": 4,        # ceiling for a few-color mark; mono collapses to 2
        "blur_radius": 1.0,          # light pre-quantize blur softens stairstepped edges
        "despeckle": 2,
        "curve_fit": False,
        "potrace": {
            "turdsize": 2,           # drop specks below N px
            "alphamax": 1.0,         # >~1.33 suppresses all corners; keep crisp
            "opttolerance": 0.3,
        },
        "vtracer": {                 # used only if a mark is genuinely multi-color
            "colormode": "color", "mode": "spline", "hierarchical": "stacked",
            "color_precision": 6, "filter_speckle": 6, "corner_threshold": 70,
            "path_precision": 3, "splice_threshold": 45,
        },
        "svgo_precision": 2,
    },
    "illustration": {
        # Starting values from the reference sweep (reference.md section 4): palette-lock +
        # color_precision 4 + filter_speckle 8 + curve-fit. Curve-fit ON: it halves
        # over-segmented smooth boundaries with no measured fidelity loss.
        "engine": "vtracer",
        "quantize_colors": 14,       # 12-16 band; ignored when palette is set
        "palette": DEFAULT_PALETTE,  # palette-lock target (instance or --palette); never average brand colors
        "blur_radius": 0.0,
        "despeckle": 1,
        "curve_fit": True,
        "curve_fit_error": 1.5,
        "vtracer": {
            "colormode": "color", "mode": "spline", "hierarchical": "stacked",
            "color_precision": 4, "filter_speckle": 8, "corner_threshold": 45,
            "path_precision": 3, "splice_threshold": 45,
        },
        "svgo_precision": 2,
    },
}

# The ceiling slot. Pre-polish ceilings per (class, tier): a traced asset must come in under
# its tier ceiling before the human polish step. The TIER STRUCTURE is the method: flat vs
# organic marks, flat vs detailed illustrations, with detailed woodcut/engraving art judged by
# a human on recognizability (texture caps the fidelity proxy, so no anchor gate is honest
# there). The NUMBERS are per instance: None here, set by the instance's ratified calibration.
CEILINGS = {
    "ratified": False,
    "ratified_on": None,
    "ratified_by": None,
    "fidelity_bar": {
        # proxy on ssim·target (re-rasterized trace vs the quantized flat target), checked at
        # BOTH hero and icon scale. Final accept/reject is human.
        "ssim_target_hero_min": None,
        "ssim_target_icon_min": None,
        "note": "Pre-polish proxy on ssim·target at hero+icon, set by the instance's "
                "ratified calibration. Human accepts/rejects at icon + hero scale; polish "
                "time is reported, not gated. The detailed-illustration tier is human-judged.",
    },
    "mark": {
        "flat": {"anchors_max": None},       # geometric glyph / symbol
        "organic": {"anchors_max": None},    # animal / figure silhouette (higher anchor floor)
    },
    "illustration": {
        "flat": {"anchors_max": None},       # vector-friendly, limited palette
        "detailed": {"anchors_max": None, "gate": "human-judged"},  # woodcut / engraving
    },
}


def _apply_instance() -> None:
    """Overlay the instance's ratified calibration, if this checkout carries one."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "instance_calibration.py")
    if not os.path.isfile(path):
        return
    spec = importlib.util.spec_from_file_location("vectorize_instance_calibration", path)
    inst = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(inst)
    global CEILINGS, ACCENTS, GOLDENS
    if getattr(inst, "GOLDENS", None):
        GOLDENS = {**GOLDENS, **inst.GOLDENS}
    if getattr(inst, "ACCENTS", None):
        ACCENTS = tuple(inst.ACCENTS)
    if getattr(inst, "PALETTE", None):
        PRESETS["illustration"]["palette"] = list(inst.PALETTE)
    if getattr(inst, "CEILINGS", None):
        CEILINGS = inst.CEILINGS


_apply_instance()

# Fidelity proxy is sampled at these scales (icon + hero), per the plan's wording.
FIDELITY_SCALES = (48, 768)


def preset_for(asset_class: str) -> dict:
    if asset_class not in PRESETS:
        raise ValueError(f"unknown asset class {asset_class!r}; expected one of {list(PRESETS)}")
    return PRESETS[asset_class]


def ceiling_for(asset_class: str, tier: str = "flat"):
    """Ratified anchor ceiling for a (class, tier). None if unratified OR human-judged."""
    if not CEILINGS.get("ratified"):
        return None
    return CEILINGS.get(asset_class, {}).get(tier, {}).get("anchors_max")


def is_human_judged(asset_class: str, tier: str = "flat") -> bool:
    """True when a tier is gated on human recognizability, not an anchor ceiling."""
    return CEILINGS.get(asset_class, {}).get(tier, {}).get("gate") == "human-judged"


def tiers_for(asset_class: str):
    return [k for k in CEILINGS.get(asset_class, {}) if isinstance(CEILINGS[asset_class][k], dict)]
