# extract_scene_graph — HeyHi Design Bridge, Phase T1

The Translate extractor. It loads a `ui-studio` HTML prototype in a headless
Chromium (Playwright) and emits one schema-valid scene-graph IR per breakpoint
(`sm` 375 / `md` 768 / `lg` 1440). The IR is the reviewed contract the `use_figma`
Builder (Phase T2) reads; it is validated and diffed without opening Figma.

Frozen schema: `../../schema/scene-graph.schema.json` (v0.1). This extractor does
not modify it. Where a CSS feature has no v0.1 node slot, the feature is surfaced
in `IR.flags`, never dropped silently.

## Install

```bash
npm install
npx playwright install chromium
```

`node_modules/` and the browser binary are not tracked (see `.gitignore`).

## Run

```bash
# defaults to the bundled golden prototype + its fixture brand-config
# (examples/brand-config/example.json, a neutral example palette)
node extract.mjs

# explicit
node extract.mjs \
  --prototype ../../examples/prototypes/atlas-reader.html \
  --config    ../../examples/brand-config/example.json \
  --out       ../../examples \
  --name      atlas-reader \
  --root      body \
  --breakpoints sm,md,lg
```

Outputs, for `--name atlas-reader`:

- `examples/atlas-reader.{sm,md,lg}.ir.json`: one IR per breakpoint
- `examples/prototypes/assets/vec-*.svg`: any inline `<svg>` extracted as a VECTOR asset

Validate the result against the frozen schema:

```bash
python3 ../../schema/validate_ir.py ../../examples/atlas-reader.*.ir.json
```

## What it does (per `reference.md` §1–3)

1. **Settle before measuring.** Loads at `networkidle`, awaits `document.fonts.ready`,
   then freezes animations/transitions so computed values are read at a stable base
   frame. The freeze stylesheet is marked and skipped during declared-value reads, so
   the animation flag still fires.
2. **Walks the DOM** from `--root`, capturing computed styles, `getBoundingClientRect`,
   and text runs (`lib/browser-capture.mjs`).
3. **Probes `::before` / `::after`** explicitly with `getComputedStyle(el, '::before')`.
   A plain DOM walk cannot see them; each is raised as a `pseudo-element` flag.
4. **Recovers tokens from declared stylesheet values** (`document.styleSheets` cssRules),
   not `getComputedStyle`. A declared bare `var(--token)` is a direct lookup
   (`source: "declared"`); a literal, `clamp()`/`calc()`, shorthand-expanded, nested, or
   inherited value becomes a confidence-scored nearest-token match (`source: "matched"`),
   flagged when low. The token map is built forward from the brand-config, mirroring
   `ui-studio/scripts/cursor-export.py`, so the `cssVar → token_path → figma_variable`
   convention is exact (hyphenated segments and all).
5. **Maps flexbox to auto-layout** and flags every does-not-map feature: CSS grid,
   `position: sticky` / `fixed`, pseudo-elements, transforms, stacked shadows,
   `overflow: scroll`, `flex-wrap`, animations, `clamp()`/`calc()`-derived values, and
   non-brand (missing) fonts.

## Architecture

| File | Role |
|------|------|
| `extract.mjs` | CLI: launch browser, loop breakpoints, write IRs + assets |
| `lib/brand-map.mjs` | brand-config → token maps (color / spacing / type), nearest-token matchers |
| `lib/browser-capture.mjs` | in-page capture (DOM walk, CSSOM cascade, pseudo probe) |
| `lib/build-ir.mjs` | rich capture → strict v0.1 IR (node mapping, fills, flags, `tokens_used`) |
| `lib/color.mjs` | color parsing + redmean distance for nearest-token |

Capture stays rich and loss-tolerant; the strict mapping happens Node-side. That
split is what lets the extractor honour "no silent drops" against a frozen,
`additionalProperties:false` schema: everything the page declares leaves the
browser, and `build-ir` decides what maps to a node slot and what is flagged.

## Known limits (v0.1)

- The v0.1 IR node has no slot for corner-radius, box-shadow, stroke, or opacity.
  These are aggregated into one `schema-gap:*` flag per property and reported in
  `../../SCHEMA-GAPS.md` for the human reviewer, rather than changing the frozen schema.
- `FILL` / `HUG` sizing is heuristic (cross-axis stretch and block flow → `FILL`,
  text → `HUG`). The T2 spike and human review refine sizing in Figma.
- Mixed inline-and-block content inside one element is not split into separate runs;
  text-bearing elements flatten to `textContent`. `ui-studio` output is structured
  cleanly enough that this has not bitten, but it is the next hardening target.

---

*HeyHi Confidential*
