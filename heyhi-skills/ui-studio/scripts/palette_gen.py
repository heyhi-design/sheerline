#!/usr/bin/env python3
"""
palette_gen.py - seed colour -> structured, accessible-by-construction brand palette.

ui-styles deep-research, moment 2 Item 7 (build). Staged in skill-updates/ for review;
NOT wired into the deployed ui-studio skill yet.

WHY
  The style subsystem currently extracts colour once and freezes it (a single
  warm/cool/neutral tag). Research (Material HCT seed->tonal-palette, the open-source
  material-color-utilities) shows colour can be reasoned generatively from ONE seed and made
  accessible by construction. This is a self-contained implementation of that idea.

COLOUR SPACE
  Production should use HCT (CAM16 x L*) via material-color-utilities. That library is not
  vendored here, so this build uses OKLCH (Bjorn Ottosson) as a self-contained perceptual
  space for hue/chroma identity, and computes WCAG contrast EMPIRICALLY from sRGB luminance,
  so the accessibility guarantee holds regardless of the perceptual space. Swap the oklch_*
  helpers for an HCT backend to upgrade; role-solving and the contrast guarantee are
  backend-agnostic (Provider-Agnostic invariant).

HUMAN-IN-THE-LOOP
  The designer supplies the seed and direction. The system extends it into a coherent,
  accessible palette. It does not choose the brand colour. Output is a proposal a human reads.

USAGE
  python3 palette_gen.py --seed "#2D5BFF"                 # light-scheme palette (JSON)
  python3 palette_gen.py --seed "#2D5BFF" --scheme dark   # dark-native palette
  python3 palette_gen.py --selftest                       # assert every pair meets WCAG AA
"""
import math
import json
import argparse
import sys

# ---------- sRGB <-> linear ----------
def _decode(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def _encode(c):
    c = 0.0 if c < 0 else (1.0 if c > 1 else c)
    return 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055

def hex_to_lin(h):
    h = h.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return _decode(r), _decode(g), _decode(b)

def lin_to_hex(r, g, b):
    return "#" + "".join("%02X" % round(_encode(x) * 255) for x in (r, g, b))

# ---------- linear sRGB <-> OKLab / OKLCH ----------
def _cbrt(x):
    return math.copysign(abs(x) ** (1 / 3), x)

def lin_to_oklab(r, g, b):
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = _cbrt(l), _cbrt(m), _cbrt(s)
    return (
        0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
        1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
        0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_,
    )

def oklab_to_lin(L, a, b):
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    return (
        4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
        -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
        -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s,
    )

def hex_to_oklch(h):
    L, a, b = lin_to_oklab(*hex_to_lin(h))
    return L, math.hypot(a, b), math.atan2(b, a)

def _in_gamut(r, g, b, eps=1e-4):
    return all(-eps <= x <= 1 + eps for x in (r, g, b))

def oklch_to_hex(L, C, h):
    """OKLCH -> hex, reducing chroma until the colour fits the sRGB gamut (keeps L exact)."""
    c = C
    r, g, b = oklab_to_lin(L, c * math.cos(h), c * math.sin(h))
    for _ in range(48):
        if _in_gamut(r, g, b):
            break
        c *= 0.92
        r, g, b = oklab_to_lin(L, c * math.cos(h), c * math.sin(h))
    return lin_to_hex(r, g, b)

# ---------- WCAG ----------
def luminance(hexc):
    r, g, b = hex_to_lin(hexc)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast(h1, h2):
    a, b = luminance(h1), luminance(h2)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)

def solve_L_for_contrast(C, h, ref_hex, target):
    """Tone at (C, h) nearest the reference's lightness whose WCAG contrast vs ref meets `target`.

    Contrast is monotone in L on either side of the reference: against a LIGHT reference a
    darker tone (lower L) raises contrast; against a DARK reference a lighter tone (higher L)
    raises contrast. We return the minimum-sufficient tone on the correct side, preserving the
    most chroma/softness while guaranteeing the ratio. Works for light- and dark-scheme roles.
    """
    ref_light = luminance(ref_hex) >= 0.5
    lo, hi = 0.0, 1.0
    for _ in range(34):
        mid = (lo + hi) / 2
        passes = contrast(oklch_to_hex(mid, C, h), ref_hex) >= target
        if ref_light:
            lo, hi = (mid, hi) if passes else (lo, mid)   # lightest sufficient (darker) tone
        else:
            lo, hi = (lo, mid) if passes else (mid, hi)    # darkest sufficient (lighter) tone
    return oklch_to_hex(lo if ref_light else hi, C, h)

# ---------- palette ----------
TONES = [12, 20, 30, 40, 50, 60, 70, 80, 90, 95]
# tone anchors per scheme: (background, surface, border)
_SCHEME_TONES = {"light": (0.985, 0.965, 0.880), "dark": (0.160, 0.210, 0.320)}

def _solve_accent(sL, sC, sh, bg):
    """Accent near the seed's own lightness, guaranteeing accent-on-bg >= 3.0 and text >= 4.5.

    Stays at the seed's natural tone when it already separates from the background and carries
    a text colour; only nudges when it must. Fixes the earlier always-darken behaviour that
    flattened high-lightness brand hues (e.g. yellow).
    """
    accent = oklch_to_hex(sL, sC, sh)
    if contrast(accent, bg) < 3.0:
        accent = solve_L_for_contrast(sC, sh, bg, 3.0)
    accent_text = "#FFFFFF" if contrast("#FFFFFF", accent) >= contrast("#111111", accent) else "#111111"
    if contrast(accent_text, accent) < 4.5:
        accent = solve_L_for_contrast(sC, sh, accent_text, 4.5)
        if contrast(accent, bg) < 3.0:  # re-establish bg separation if the text nudge collapsed it
            accent = solve_L_for_contrast(sC, sh, bg, 3.0)
        accent_text = "#FFFFFF" if contrast("#FFFFFF", accent) >= contrast("#111111", accent) else "#111111"
    return accent, accent_text

_SEMANTIC_HUES = {"success": 145, "warning": 75, "error": 29}  # OKLCH hue degrees (green / amber / red)

def _semantic_roles(bg, base_C):
    """Conventional success/warning/error hues, harmonized to the palette's chroma and made
    accessible by construction (fill-on-bg >= 3.0, text-on-fill >= 4.5). Hue is convention,
    not brand choice; the generator only makes them legible and on-key with the palette."""
    C = max(0.10, min(base_C, 0.16))
    out = {}
    for name, deg in _SEMANTIC_HUES.items():
        fill, txt = _solve_accent(0.60, C, math.radians(deg), bg)
        out[name], out[name + "_text"] = fill, txt
    return out

def build_palette(seed_hex, scheme="light", body_target=7.0, muted_target=4.5):
    sL, sC, sh = hex_to_oklch(seed_hex)
    neutral_c = min(sC * 0.15, 0.018)  # faint seed temperature carried into neutrals
    t_bg, t_surface, t_border = _SCHEME_TONES[scheme]

    bg = oklch_to_hex(t_bg, neutral_c, sh)
    surface = oklch_to_hex(t_surface, neutral_c * 1.3, sh)
    border = oklch_to_hex(t_border, neutral_c * 1.6, sh)
    text = solve_L_for_contrast(neutral_c * 1.6, sh, bg, body_target)
    text_muted = solve_L_for_contrast(neutral_c * 1.3, sh, bg, muted_target)
    accent, accent_text = _solve_accent(sL, sC, sh, bg)
    semantics = _semantic_roles(bg, sC)

    def ramp(C):
        return {str(t): oklch_to_hex(t / 100, C, sh) for t in TONES}

    report = [
        ("text on bg", text, bg, body_target),
        ("muted text on bg", text_muted, bg, 4.5),
        ("text on surface", text, surface, 4.5),
        ("accent text on accent", accent_text, accent, 4.5),
        ("accent on bg (UI, 3:1)", accent, bg, 3.0),
        ("success text", semantics["success_text"], semantics["success"], 4.5),
        ("success on bg (3:1)", semantics["success"], bg, 3.0),
        ("warning text", semantics["warning_text"], semantics["warning"], 4.5),
        ("warning on bg (3:1)", semantics["warning"], bg, 3.0),
        ("error text", semantics["error_text"], semantics["error"], 4.5),
        ("error on bg (3:1)", semantics["error"], bg, 3.0),
    ]
    contrast_report = [
        {"pair": name, "ratio": round(contrast(a, b), 2), "target": tgt,
         "pass": contrast(a, b) >= tgt}
        for (name, a, b, tgt) in report
    ]
    return {
        "meta": {
            "seed": seed_hex.upper(),
            "scheme": scheme,
            "colour_space": "OKLCH (self-contained); HCT backend is the production upgrade",
            "guarantee": "WCAG AA computed empirically from sRGB luminance",
            "note": "Designer supplies the seed; the system extends it. Human-in-the-loop.",
        },
        "roles": {
            "background": bg, "surface": surface, "border": border,
            "text": text, "text_muted": text_muted,
            "accent": accent, "accent_text": accent_text,
            **semantics,
        },
        "ramps": {"primary": ramp(sC), "neutral": ramp(neutral_c * 1.6)},
        "contrast_report": contrast_report,
        "all_pass": all(r["pass"] for r in contrast_report),
    }

# ---------- CLI / smoke test ----------
def selftest():
    seeds = ["#2D5BFF", "#C8503A", "#1C7C54", "#7A4DBE", "#E8B400", "#0A0A0A", "#0F4C5C"]
    failures = []
    for scheme in ("light", "dark"):
        for s in seeds:
            p = build_palette(s, scheme=scheme)
            for r in p["contrast_report"]:
                if not r["pass"]:
                    failures.append((scheme, s, r))
            tag = "ok  " if p["all_pass"] else "FAIL"
            print(f"  [{tag}] {scheme:<5} {s}  accent={p['roles']['accent']} on {p['roles']['background']}")
        print()
    if failures:
        print(f"SELFTEST FAILED: {len(failures)} pair(s) below target")
        for scheme, s, r in failures[:12]:
            print(f"   {scheme} {s} {r['pair']} ratio={r['ratio']} target={r['target']}")
        return 1
    print(f"SELFTEST PASSED: {len(seeds)} seeds x 2 schemes x 11 documented pairs (5 core + 6 semantic) all meet WCAG AA")
    return 0

def main():
    ap = argparse.ArgumentParser(description="Seed colour -> accessible brand palette (ui-styles Item 7 build).")
    ap.add_argument("--seed", help="seed colour, e.g. '#2D5BFF'")
    ap.add_argument("--scheme", choices=["light", "dark"], default="light", help="colour scheme")
    ap.add_argument("--selftest", action="store_true", help="assert every documented pair meets WCAG AA")
    args = ap.parse_args()
    if args.selftest:
        sys.exit(selftest())
    if not args.seed:
        ap.error("provide --seed or --selftest")
    print(json.dumps(build_palette(args.seed, scheme=args.scheme), indent=2))

if __name__ == "__main__":
    main()
