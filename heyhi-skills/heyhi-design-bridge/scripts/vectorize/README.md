# scripts/vectorize — HeyHi Design Bridge, Mode 2 (Vectorize)

Raster (Nano Banana / any PNG) → craft-quality SVG. Fully local; no external service.
Procedure lives in `../../SKILL.md` (Mode 2); rationale in `../../reference.md` §4 and
the plan. The pipeline gets the path most of the way; **human polish is the primary
craft surface and the only hand-work.**

## Pipeline
quantize (Pillow, dithering off; palette-lock for illustration) → trace (potrace mono
/ vtracer color) → SVGO cleanup → optional Schneider curve-fit (illustration default
on; marks off) → color-snap to brand tokens → one-line craft report → land
(`use_figma` `createNodeFromSvg` / `logo.marks[].asset`).

## Dependencies
| Tool | Install | Used for |
|------|---------|----------|
| Python 3.9+, Pillow, numpy | `pip install --user -r requirements.txt` | quantize, metrics |
| vtracer | `pip install --user vtracer` (in requirements) | color trace |
| potrace + mkbitmap | `brew install potrace` | mono trace |
| librsvg (`rsvg-convert`) | `brew install librsvg` | fidelity rasterize |
| SVGO | `npx --yes svgo` (auto, no install) | path cleanup |

## Files
- `vectorize.py` — CLI orchestrator (steps 2–5 + craft report).
- `presets.py` — per-class trace params + the `CEILINGS` slot (ships unratified; overlays `instance_calibration.py` when present).
- `svg_tools.py` — anchor counting, palette, rsvg-convert fidelity (SSIM/agreement, pure numpy).
- `fit_curve.py` — vendored Schneider least-squares Bézier fit (the curve-fit; **not** RDP).
- `path_ops.py` — SVG path parse / flatten (incl. arcs) / Schneider re-emit.
- `make_goldens.py` — regenerates the golden raster inputs (seeded) from `presets.GOLDENS`: a neutral example mark (`examples/assets/example-mark.svg`) and palette by default, or the instance's own mark and palette when its calibration sets `GOLDENS`.
- `calibrate.py` — the Phase V.0 sweep → `../../examples/vectorize/calibration-report.{md,json}`.
- `svgo.config.mjs` — conservative SVGO config (precision only; viewBox + color layers kept).

## Usage
```bash
python3 vectorize.py INPUT.png --class mark|illustration --out OUT.svg --fidelity --json OUT.report.json
# brand colors: --palette "#RRGGBB,#RRGGBB,..."  (default: the instance palette, if set)
# force curve-fit on/off: --curve-fit / --no-curve-fit  (default = the class preset)

python3 calibrate.py            # regenerate goldens, sweep, write the calibration report
                                # (no instance bar? add --ssim-floor <starting value>)
python3 make_goldens.py         # just regenerate the golden inputs
```

## Ceilings (Phase V.0): generic slot, instance numbers
`presets.py` ships the per-(class, tier) ceiling slot unratified, with no palette and no
accents. An instance ratifies its own ceilings, fidelity bar, palette, and accents into
`instance_calibration.py` beside it (instance-only; never shipped in a scaffold export), along
with the golden mark and palette it calibrated against (`GOLDENS`), and
`presets.py` overlays that file when present. `calibrate.py` proposes the numbers; without an
instance bar it needs `--ssim-floor`. The human makes the final call. Re-validate against real
generated output before a paid engagement.

*HeyHi Confidential*
