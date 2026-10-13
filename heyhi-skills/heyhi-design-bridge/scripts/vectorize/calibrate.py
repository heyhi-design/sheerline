#!/usr/bin/env python3
"""Phase V.0 calibration harness for Vectorize.

Sweeps a modest per-class parameter grid over the golden inputs and, per combo,
measures final anchor count, palette (the actual colors), and two fidelity proxies:
  - ssim·target = traced vector re-rasterized vs the quantized flat target. This is
    trace faithfulness and is PRODUCTION-AVAILABLE (no clean original is assumed).
    The fidelity BAR is set on this.
  - ssim·source = vs the clean noise-free source (whole-pipeline). A synthetic-golden
    luxury; reported as context. It is harsh on edge-dominated marks (deliberate blur
    shifts edges a pixel), so it is NOT a hard gate.

Recommendation: lowest anchors among combos that clear the ssim·target floor and (for
illustration) preserve the instance's brand accents, when it names any (SSIM alone does
not protect small accents). Curve-fit is evaluated as a post-step on the best
illustration combo. It PROPOSES ceilings with headroom; it asserts nothing as final —
the proposals go into a report for the instance owner to ratify (Phase V.0 gate) into
instance_calibration.py.

  python3 calibrate.py            # regenerate goldens, sweep, write the report
  python3 calibrate.py --no-regen # reuse existing goldens

Writes examples/vectorize/calibration-report.{md,json} (the instance's calibration evidence).

HeyHi Confidential.
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import tempfile

import make_goldens
import presets as P
import svg_tools as st
import vectorize as V

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.normpath(os.path.join(HERE, "..", ".."))
GOLD = os.path.join(SKILL, "examples", "vectorize")
SOURCES = os.path.join(GOLD, "sources")

# ssim·target floor for the sweep (the production-available bar) and the brand accents that
# must survive an illustration: both come from the instance calibration (presets.py overlays
# instance_calibration.py). A generic copy has neither, so --ssim-floor is required there and
# the accent check is skipped (no instance accents to protect).
SSIM_FLOOR = P.CEILINGS.get("fidelity_bar", {}).get("ssim_target_hero_min")
BRAND_ACCENTS = {c.lower() for c in P.ACCENTS}
# The plan's bar is "acceptable at icon AND hero scale", so the floor applies at both.
HERO, ICON = max(P.FIDELITY_SCALES), min(P.FIDELITY_SCALES)


def _mark_grid():
    base = copy.deepcopy(P.PRESETS["mark"])
    out = []
    for blur in (0.6, 1.0, 1.4):
        for turd in (2, 8):
            for alpha in (0.8, 1.0, 1.2):
                pr = copy.deepcopy(base)
                pr["blur_radius"] = blur
                pr["potrace"] = {"turdsize": turd, "alphamax": alpha, "opttolerance": 0.3}
                out.append((f"blur{blur}_turd{turd}_a{alpha}", pr))
    return out


def _illo_grid():
    # palette-locked via preset + snapped post-trace, so color_precision now only drives
    # anchor economy (fewer pre-snap boundary shades -> fewer paths). corner_threshold
    # barely moved the count in the prior sweep, so it stays fixed.
    base = copy.deepcopy(P.PRESETS["illustration"])
    out = []
    for cp in (2, 4, 6):
        for spk in (8, 16):
            pr = copy.deepcopy(base)
            pr["vtracer"] = dict(base["vtracer"], color_precision=cp, filter_speckle=spk,
                                 corner_threshold=45)
            out.append((f"cp{cp}_spk{spk}", pr))
    return out


def _run_combo(src, clean, cls, combo_id, preset, tmp, curve_fit=False, cf_error=1.5):
    out = os.path.join(tmp, f"{cls}_{combo_id}{'_cf' if curve_fit else ''}.svg")
    rep = V.run(src, cls, out_svg=out, engine=preset["engine"],
                colors=preset.get("quantize_colors"), do_fidelity=True, tmp=tmp,
                preset_override=preset, curve_fit=curve_fit, cf_threshold=15, cf_error=cf_error)
    src_fid = st.fidelity(out, clean, scales=P.FIDELITY_SCALES, tmp=tmp)
    return {
        "combo": combo_id + ("+cf" if curve_fit else ""),
        "anchors": rep["anchors"]["final"],
        "palette": rep["palette"],
        "palette_count": rep["palette_count"],
        "ssim_target_hero": rep["fidelity"][HERO]["ssim"],
        "ssim_target_icon": rep["fidelity"][ICON]["ssim"],
        "ssim_source_hero": src_fid[HERO]["ssim"],
        "ssim_source_icon": src_fid[ICON]["ssim"],
        "preset": preset,
        "svg": out,
    }


def _clears(r, cls):
    # bar applies at BOTH hero and icon scale (plan: "acceptable at icon and hero scale")
    if r["ssim_target_hero"] < SSIM_FLOOR or r["ssim_target_icon"] < SSIM_FLOOR:
        return False
    if cls == "illustration":
        pal = {c.lower() for c in r["palette"]}
        if not BRAND_ACCENTS <= pal:
            return False
    return True


def calibrate(regen=True):
    if regen:
        make_goldens.main()
    tmp = tempfile.mkdtemp(prefix="calib_")

    cfg = {
        "mark": dict(src=os.path.join(SOURCES, make_goldens.MARK_NAME + ".png"),
                     clean=os.path.join(SOURCES, make_goldens.MARK_NAME + ".clean.png"),
                     grid=_mark_grid(), headroom=1.5,
                     reference_anchors=st.count_anchors_svg(make_goldens.MARK_SVG)),
        "illustration": dict(src=os.path.join(SOURCES, make_goldens.EMBLEM_NAME + ".png"),
                             clean=os.path.join(SOURCES, make_goldens.EMBLEM_NAME + ".clean.png"),
                             grid=_illo_grid(), headroom=1.35, reference_anchors=None),
    }

    results = {}
    for cls, c in cfg.items():
        rows = []
        for combo_id, preset in c["grid"]:
            try:
                rows.append(_run_combo(c["src"], c["clean"], cls, combo_id, preset, tmp))
            except Exception as e:
                rows.append({"combo": combo_id, "anchors": -1, "palette": [], "palette_count": -1,
                             "ssim_target_hero": 0, "ssim_target_icon": 0,
                             "ssim_source_hero": 0, "ssim_source_icon": 0,
                             "error": str(e)[:120], "preset": preset, "svg": None})
        rows = [r for r in rows if r["anchors"] >= 0]
        passing = [r for r in rows if _clears(r, cls)]
        pool = passing or rows
        best = min(pool, key=lambda r: r["anchors"])

        curve_fit_row = None
        if cls == "illustration" and best.get("svg"):
            # evaluate curve-fit on the best trace-param combo
            base_id = best["combo"]
            cf = _run_combo(c["src"], c["clean"], cls, base_id.replace("+cf", ""),
                            best["preset"], tmp, curve_fit=True, cf_error=1.5)
            curve_fit_row = cf
            if cf["anchors"] < best["anchors"] and _clears(cf, cls):
                best = cf  # adopt curve-fit when it reduces anchors and still clears

        results[cls] = {
            "rows": sorted(rows, key=lambda r: r["anchors"]),
            "recommended": best,
            "curve_fit_row": curve_fit_row,
            "floors_cleared": bool(passing),
            "reference_anchors": c["reference_anchors"],
            "proposed_ceiling": int(round(best["anchors"] * c["headroom"])),
        }
    return results


# --------------------------------------------------------------------------- #
# report
# --------------------------------------------------------------------------- #

def _table(rows, top=9):
    head = ("| combo | anchors | palette | ssim·target h/i | ssim·source h/i |\n"
            "|---|---|---|---|---|\n")
    body = ""
    for r in rows[:top]:
        body += (f"| {r['combo']} | {r['anchors']} | {r['palette_count']} | "
                 f"{r['ssim_target_hero']:.3f}/{r['ssim_target_icon']:.3f} | "
                 f"{r['ssim_source_hero']:.3f}/{r['ssim_source_icon']:.3f} |\n")
    return head + body


def write_report(results):
    L = ["# Vectorize — Phase V.0 Calibration Report",
         "",
         "*Proposals only. No numeric ceiling is asserted as final until the instance owner ratifies "
         "(Phase V.0 gate). Trace + simplify is fully local; no external service was touched.*",
         "",
         "**Inputs (synthetic goldens from `make_goldens.py`, `examples/vectorize/sources/`).** "
         "The mono mark is the hand-authored reference mark rasterized + softened (a stand-in "
         "for a generated mark). The illustration is a flat-color, curved-boundary emblem. "
         "Both carry light blur + noise to mimic generated-raster edges. "
         "**They are stand-ins** — re-check the ratified ceilings against real generated "
         "output before the first real engagement.",
         "",
         f"**Fidelity.** `ssim·target` = traced vector re-rasterized vs the quantized flat "
         f"target (trace faithfulness; production-available — the BAR sits here, ≥ {SSIM_FLOOR} "
         f"at BOTH hero and icon). `ssim·source` = vs the clean noise-free source (whole-pipeline; "
         f"context only — harsh on blurred marks, so not a gate). h/i = hero({HERO}px)/icon({ICON}px). "
         f"Final visual judgment is human, at icon + hero scale.",
         ""]
    for cls, res in results.items():
        rec = res["recommended"]
        L += [f"## {cls}", ""]
        if res["reference_anchors"]:
            L.append(f"- Hand-authored reference mark: **{res['reference_anchors']} "
                     f"anchors** — the target the polish step works back toward.")
        L += [f"- Recommended: `{rec['combo']}` → **{rec['anchors']} anchors**, "
              f"palette {rec['palette']} ({rec['palette_count']}), "
              f"ssim·target(hero) {rec['ssim_target_hero']:.3f}.",
              f"- ssim·target floor cleared by ≥1 combo: **{res['floors_cleared']}**.",
              f"- **Proposed anchor ceiling: {res['proposed_ceiling']}** "
              f"(recommended {rec['anchors']} × headroom for input variance).", ""]
        if res["curve_fit_row"]:
            cf = res["curve_fit_row"]
            L.append(f"- Curve-fit on the best combo: {cf['anchors']} anchors "
                     f"(ssim·target hero {cf['ssim_target_hero']:.3f}) — "
                     f"{'adopted' if rec['combo'].endswith('+cf') else 'not adopted'}.")
            L.append("")
        L += [_table(res["rows"]), ""]

    m, i = results["mark"], results["illustration"]
    L += ["## Proposed for ratification", "",
          "| Class | Proposed anchor ceiling (pre-polish) | Fidelity bar (proxy) | Palette |",
          "|---|---|---|---|",
          f"| mark | **{m['proposed_ceiling']}** | ssim·target ≥ {SSIM_FLOOR} (hero+icon) | mono (1 ink) |",
          f"| illustration | **{i['proposed_ceiling']}** | ssim·target ≥ {SSIM_FLOOR} (hero+icon) | "
          + (f"palette-locked to the instance palette; accents {', '.join(sorted(BRAND_ACCENTS))} must survive |"
             if P.PRESETS["illustration"].get("palette")
             else "no palette lock (no instance palette); no accent check |"),
          "",
          f"Mark polish works back toward ~{m['reference_anchors']} anchors (the hand-authored "
          "mark). Human-polish time is reported, not gated. The bar is a pre-polish proxy; the "
          "human accepts or rejects at icon + hero scale.",
          "",
          "*HeyHi Confidential*"]
    text = "\n".join(L)
    with open(os.path.join(GOLD, "calibration-report.md"), "w") as f:
        f.write(text)

    def slim(r):
        return {k: v for k, v in r.items() if k not in ("preset", "svg")}
    serial = {cls: {"recommended": slim(res["recommended"]),
                    "recommended_preset": res["recommended"]["preset"],
                    "proposed_ceiling": res["proposed_ceiling"],
                    "floors_cleared": res["floors_cleared"],
                    "reference_anchors": res["reference_anchors"],
                    "ssim_target_floor": SSIM_FLOOR,
                    "rows": [slim(r) for r in res["rows"]]}
              for cls, res in results.items()}
    with open(os.path.join(GOLD, "calibration-report.json"), "w") as f:
        json.dump(serial, f, indent=2, default=str)
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-regen", action="store_true")
    ap.add_argument("--ssim-floor", type=float, default=None,
                    help="ssim·target floor for the sweep (default: the instance's ratified bar)")
    args = ap.parse_args()
    global SSIM_FLOOR
    if args.ssim_floor is not None:
        SSIM_FLOOR = args.ssim_floor
    if SSIM_FLOOR is None:
        ap.error("no ratified instance fidelity bar; pass --ssim-floor (e.g. a starting value "
                 "to propose against, which the instance owner then ratifies)")
    print(write_report(calibrate(regen=not args.no_regen)))


if __name__ == "__main__":
    main()
