# HeyHi Design Bridge — Reference

*Load-on-demand knowledge for `heyhi-design-bridge`. The procedure lives in `SKILL.md`; the rationale lives in the approved build plan (a local plan file, not shipped).*

---

## 1. The Scene-Graph IR

One IR per breakpoint. Canonical schema: `schema/scene-graph.schema.json` (JSON Schema Draft 2020-12). Golden example: `examples/atlas-hero.lg.ir.json`. The IR is the reviewed contract: it is validated and diffed without opening Figma, and it is what the human reviewer approves before any write.

**Top level**
- `$schema` — const `heyhi-scene-graph/v0.4`.
- `meta` — `source` (prototype path), `breakpoint` (`sm`/`md`/`lg`), `brand_config`, `generated_by`.
- `tokens_used[]` — every CSS-custom-property to token resolution, with provenance.
- `root` — the node tree.

**`tokens_used[]` item**
- `css_var`, `token_path` (dotted brand-config path), `figma_variable` (Figma Variable name), `resolved` (computed literal), `source` (`declared` | `computed` | `matched`), `match_confidence` (0..1).
- `source` is the honesty field: `declared` = a bare `var()` read from the stylesheet (a true lookup); `matched` = a nearest-token confidence match (flag when low); `computed` = read from `getComputedStyle` with no token recoverable.

**Node** (`root` and every child)
- `type` — `FRAME` | `TEXT` | `VECTOR` | `IMAGE` | `GROUP`.
- `name` — Figma layer name.
- `layout` — `mode` (`HORIZONTAL`/`VERTICAL`/`NONE`), `primaryAxisAlignItems`, `counterAxisAlignItems`, `itemSpacing`, `padding {t,r,b,l}`. `NONE` means absolute positioning; flag it. (v0.4, ADR-014) `layoutWrap` (`NO_WRAP`/`WRAP`, valid only when `mode === HORIZONTAL`), `counterAxisSpacing` (number — the row-gap between wrapped rows), and `counterAxisAlignContent` (`AUTO`/`SPACE_BETWEEN`) model a wrapping flex line / multi-row grid as a real Figma wrapping auto-layout; all three are optional and set directly.
- `size` — `w`, `h` (number or null), `sizing {h,v}` with `FILL`/`HUG`/`FIXED`.
- `fills[]` — a list of paints. A solid fill is `{type: "SOLID", bind, resolved}` (`bind` is the token path that becomes a Figma Variable binding; `resolved` is the literal fallback). A `GRADIENT_LINEAR` / `GRADIENT_RADIAL` fill carries `stops[]` (`{pos, color}`, `pos` canonical) and, for linear, an `angle`. An `IMAGE` fill (v0.3, ADR-013) carries `imageRef`, `scaleMode` (`FILL`/`FIT`/`CROP`/`TILE`), and an optional `imagePosition` (0..1 focal point); the byte embed lands via the Figma MCP `upload_assets` tool (raw bytes → cover fill on the node; v0.8 retires the inline `figma.createImage(base64)` path for rasters).
- `children[]` — nested nodes (FRAME/GROUP).
- `characters` — TEXT only (required for TEXT).
- `type_style` — TEXT typography, set directly (see Binding reality). Carries `token_ref` for traceability.
- `svgRef` — VECTOR only (required): the SVG to import via `createNodeFromSvg`.
- `imageRef` — IMAGE only (required): the raster to place.
- `cornerRadius` — (v0.2, ADR-010) a number (uniform) or `{tl,tr,br,bl}` (mixed). Set directly.
- `strokes[]` — (v0.2) `{weight, align?, color}`. Border `weight` set directly; `color` binds like a fill.
- `effects[]` — (v0.2) `{type, x, y, blur, spread, color}`. Box-shadows; one entry per shadow (stacked shadows map to several).
- `opacity` — (v0.2) a number 0..1, present only below 1. Set directly.
- `position` — (v0.3, ADR-013) `{x, y}` offset from the parent frame's top-left, used when the parent is a `NONE`-layout (absolute) container; a full-bleed `inset:0` child is modelled as fill-parent. Set directly.
- `runs[]` — (v0.3, ADR-013) TEXT only: inline styled ranges `{start, end, fill?, style?}` over `characters` (end exclusive), applied via `setRangeFills` / `setRangeFontName`. A run's `fill` binds like any fill; `style` carries a partial type style plus `italic`.
- `flags[]` — `{feature, node, action, needs_human}`: does-not-map features, surfaced and never dropped.

---

## 2. Binding reality (confirmed, Phase-T2 spike 2026-06-11)

Confirmed empirically against `use_figma` (see `spike-T2-findings.md`). Figma binds **color fills/strokes** and the full **float-field set** (itemSpacing, all four paddings, width/height, all four radii, strokeWeight, opacity) to Variables; `rotation` does not bind. Typography **also binds** (fontFamily, fontStyle, fontSize, lineHeight, letterSpacing, and text `characters`), reversing the earlier premise that it could not. So:

- Color: emit a `bind` and write a Variable binding (the v1 default).
- Typography: **v1 sets the value directly** on the text node and carries `token_ref` for traceability (surfaced in the documentation frame), by design choice rather than necessity. Binding type is possible and is implemented as the `--type-mode bind` flag (`set-direct` is the default); it would require the client's Figma to model typography as string and float variables and would couple writes to font-load.

**Shared named Text Styles via `--type-mode style` (v0.4, WS3).** A third type mode writes type **set-direct on first paint** (no `bindRefs` on text ops — correct first render), then points the operator at the proven post-build finish in `compose_type.py` (`extract → review → emit → create.js + apply.js`), which creates one `figma.createTextStyle()` per role and applies it with `setTextStyleIdAsync()`. The finish binds **family / style / size** to Variables but sets **lineHeight / letterSpacing / textCase direct**, because a Variable-bound `lineHeight` **coerces to pixels** in Figma (proven live 2026-06-17) — so the `--type-mode bind` path's `lineHeight`/`letterSpacing` binds are subtly wrong, and `style` mode avoids the coercion entirely. **token_ref-aware role naming:** a `type_style.token_ref` (e.g. `tokens.typography.scale.body-lg`) is the design's own name for the role, so it now beats the size-rank heuristic (`body-lg → Body/Large`), with a Title-cased `Category/Variant` fallback for unknown tails. Default stays `set-direct` for the first promotion; flip to `style` after one live pass proves the finish end-to-end.

Builder notes from the spike: weight is a Figma **style-name string** ('Bold'), not a number, so the numeric IR `weight` maps to a style name; load fonts per call and route a missing font to `flags` (it throws detectably); DM Mono has no Bold. The IR and the verification do not depend on type binding.

The v0.2 decoration floats (`cornerRadius`, stroke `weight`, `opacity`) follow the same rule as `itemSpacing` and `padding`: set directly, not Variable-bound. Only color binds, so stroke `color` and a solid fill behave identically. Whether those floats can additionally Variable-bind is the open Phase-T2 question (ADR-010). The v0.3 fields follow the same set-direct stance: `position` x/y and run styling are set directly on the node, while a run's `fill` color binds like any other fill (ADR-013).

**Font preflight (real-engagement finding).** Before authoring brand typography, run `figma.listAvailableFontsAsync()` filtered to the brand families to confirm they exist and to capture the **exact** Figma style-name spellings — they differ per family: Work Sans is `SemiBold`/`ExtraBold` (no space); Inter is `Semi Bold`/`Extra Bold` (with a space). Use a `loadFont(family, style)` helper that try/catches to an Inter fallback so a missing weight degrades gracefully rather than throwing. This is the read-side complement to the existing rule that the numeric IR `weight` maps to a Figma style-name string and that a missing font routes to `flags`.

**The line-height-to-pixels coercion, in full (Compose, real-engagement finding, 2026-06-17).** The coercion named above is the short form; the exact API mechanics matter when authoring against the Text Style API directly (the surgical-finish path, §5b). `figma.createTextStyle()` plus `textStyle.setBoundVariable(field, variable)` bind `fontFamily`, `fontStyle`, `fontSize`, `lineHeight`, and `letterSpacing`. But a `lineHeight` bound to a FLOAT Variable is coerced to **PIXELS**: a style set to `{unit:'PERCENT', value:160}` with a bound FLOAT `160` renders as `{unit:'PIXELS', value:160}` (160px leading, not 1.6×). So a Variable-backed type system binds **fontFamily + fontStyle + fontSize** and sets **lineHeight + letterSpacing (PERCENT) + textCase directly**. `node.setTextStyleIdAsync(style.id)` applies a style (async); Text Styles are **type-only**, so applying one preserves the node's existing color fills — color stays bound to its own Variables, giving the clean *color = Variables, type = Styles* split.

---

## 3. CSS to Figma mapping

This table reports three honesty states, not two. **Captured + built** is extracted *and* constructed by the Builder, so it renders when the `use_figma` op-plan is written. **Captured, not yet built** is read into the IR (on the reviewed contract, so it does not silently vanish) but the Builder does not yet construct it, so it would render empty or as a placeholder. **Flagged only** has no Figma equivalent: it is recorded in `IR.flags`, never dropped, and handed to a human. Read the state before promising a render; do not read "captured" as "renders."

**(a) Captured + built (renders on the `use_figma` write).**

| CSS | Figma |
|-----|-------|
| flexbox direction / align / justify | auto-layout `mode` / counter / primary align |
| wrapping flex (`flex-wrap: wrap`) / multi-row grid (`children > tracks`) | `layoutWrap:WRAP` + `counterAxisSpacing` (row-gap) + `counterAxisAlignContent`; FIXED width, HUG height (v0.4, ADR-014) |
| interactive control (`<a>` / `<button>` / `role=button` / `.btn` / `.cta`) with a visible box | a HORIZONTAL control FRAME: non-transparent bg → `fills`, transparent bg + border → the border as a real `strokes` outline (a ghost button is an outline, never bare text); the label is tagged `token_ref → tokens.typography.scale.button` so `--type-mode style` binds the shared `UI/Button` text style. A bare link (no box) stays TEXT; nav links never become pills (v0.4, WS4) |
| `gap` | `itemSpacing` |
| padding | frame padding |
| `var(--token)` color (declared) | Variable-bound fill |
| font size / weight / line-height / letter-spacing | text values; `--type-mode set-direct` (default, token-annotated) / `bind` (Variable-bound) / `style` (set-direct first paint, then shared named Text Styles via the `compose_type.py` finish — WS3) |
| width / height, fixed spacing | frame size |
| `box-shadow` (single or stacked) | `effects[]`, one entry per shadow (v0.2) |
| `border-radius` | `cornerRadius`, number or per-corner (v0.2) |
| border | `strokes[]`, weight direct, color bound (v0.2) |
| `opacity` < 1 | `opacity` (v0.2) |
| SVG referenced by `<img src="*.svg">` | editable VECTOR via `createNodeFromSvg` (P1) |
| linear / radial gradient | `GradientPaint` (`gradientStops` + `gradientTransform` from the CSS angle) (P2, v0.3) |
| raster `background-image: url()` and raster `<img>` | `IMAGE` paint; bytes embedded via the Figma MCP `upload_assets` tool after the write (v0.8: raw bytes → cover fill; retires inline `figma.createImage`) |
| `position: absolute` / `inset` offset | `node.x` / `node.y` in a `NONE`-layout frame; `inset:0` modelled as fill-parent (P3, v0.3) |
| inline styled runs (`<span>` accent, `<em>`) | per-range `setRangeFills` / `setRangeFontName` over `runs[]` (P4, v0.3) |
| `.sr-only` screen-reader-only text (clipped ~1px + `overflow:hidden` + absolute) | dropped from the IR by computed-shape match (not class name) and recorded as an informational `screen-reader-only` flag — assistive-only text never renders as a visible layer, and never drops silently (D3, v0.14.0) |
| visible `::before` / `::after` (background, border, or content) | emitted as a `needs-human` **placeholder** (feature `pseudo-placeholder`) so the build ships and a human confirms it, in three shapes by fidelity. **(1)** a resolvable box on a **leaf** frame host flips the host to `NONE`-layout with the placeholder at the captured box (the coverage-bar / progress-fill pattern). **(2)** a resolvable box on a **non-leaf or non-frame** host wraps it in a `NONE`-layout container `[host, placeholder]` so the host keeps its own layout (the interpreter honours a positioned child only under a `NONE` parent, ADR-013). **(3)** an in-flow `position:static` **content-text marker** (`content:"▸ "`, box resolves to `auto`) wraps the host in a `HORIZONTAL` row `[placeholder, host]` so the marker ships inline (a nominal ~1em square from the host font). Only a box-less pseudo with **no content** (an empty `static` pseudo), or an incoherent box+inline mix, keeps the `pseudo-element` flag, which **BLOCKS** the build: refuse rather than silent-drop (R-1=D + the non-leaf / box-null follow-up, v0.15.0) |

Stacked box-shadows are no longer flagged: a Figma node carries multiple effects, so they map to several `effects[]` entries (ADR-010, v0.2). The gradient, raster, absolute-position, and inline-run rows landed in the v0.3 visual-fidelity pass (ADR-013, packets P1 to P6). The one live step inside this bucket is the raster byte embed, which now lands via the Figma MCP `upload_assets` tool (raw bytes → cover fill, full-res; v0.8 retires inline `figma.createImage` for rasters) into the client's own Figma file (see the Data handling note in `SKILL.md`); the `--summary` forecast names it and `run_build.py assets` lists each raster's node id + local path for the embed.

**(b) Captured, not yet built.** Empty as of the v0.3 visual-fidelity pass: every CSS feature the extractor captures now also builds. The bucket stays in the model as the honest home for a future capture-without-build gap, where the IR would hold the data but the Builder would not yet render it.

**(c) Flagged only (no Figma equivalent; recorded in `IR.flags`, never silent, handed to a human).**

**Non-uniform** CSS grid only (`2fr 1fr`, `minmax`, `auto` tracks — Figma wrap columns are equal-width, so a reduced `css-grid` flag remains; a uniform `repeat(N, 1fr)` grid now maps to `layoutWrap:WRAP` and is no longer flagged — ADR-014), a wrapping **column** flex (`flex-direction: column; flex-wrap: wrap` — no Figma equivalent, raised as `flex-wrap-vertical`), `position: sticky` / `fixed`, complex or 3D transforms, `overflow: scroll`, animations / transitions, `clamp()` / `calc()`-derived values (token link is best-effort), and fonts absent from the Figma workspace.

**Token recovery caveat.** `getComputedStyle` returns resolved literals (`rgb(255,59,48)`), not `var(--token)`. Recover the token from the **declared** stylesheet values (`document.styleSheets` cssRules). `clamp()`/`calc()`, shorthand-expanded properties, nested vars, and JS-set values break the bare-var case; those become confidence-scored matches and are flagged when low.

**Control-affordance flags (v0.4, WS4) on the approval surface.** Two control flags ride into `IR.flags` so a button or link defect is reviewed, not shipped. `link-color-unsnapped` — a TEXT colour that resolves only via the **matched** path and is nearest a **background**-family token is kept literal and UNBOUND rather than snapped to that token (the anti-snap guard, §5); the literal stays visible and the flag asks a human to pick the right token. `near-invisible-label` — a control label whose colour ≈ its own control fill (low contrast) is flagged as likely unreadable. Both are `needs_human` and surface in the `--summary` flag ledger.

---

## 4. Vectorize parameters

**Ceilings (Phase V.0): the slot is generic, the numbers are per instance.** Pre-polish anchor ceilings per **(class, tier)**, selected with `--tier`:

| class · tier | ceiling | notes |
|---|---|---|
| mark · flat | instance-ratified | geometric glyph/symbol |
| mark · organic | instance-ratified | animal/figure silhouette; structurally higher anchor floor than a geometric outline |
| illustration · flat | instance-ratified | vector-friendly limited palette |
| illustration · detailed | **human-judged** | woodcut/engraving texture caps `ssim·target` and runs into the thousands of anchors; **generate flat instead**, else the human judges recognizability (anchors + fidelity reported, not gated) |

**Fidelity bar:** an instance-ratified minimum on `ssim·target` (re-rasterized trace vs the quantized flat target) at hero + icon scale for the flat + organic tiers (the detailed tier is exempt, human judgment). `scripts/vectorize/presets.py` `CEILINGS` is the slot and ships unratified; `calibrate.py` proposes values against the instance's own art and writes `examples/vectorize/calibration-report.{md,json}` (an instance's report is instance data; HeyHi's is not shipped in a scaffold export), and the instance owner ratifies them into `scripts/vectorize/instance_calibration.py` (instance-only, not shipped in a scaffold export). HeyHi's ratified values and evidence trail live in that file. **Generation guidance:** prompt for flat color, hard edges, and *no woodcut/engraving texture* so a detailed subject lands in the gated flat tier rather than the human-judged detailed bucket (SKILL.md Mode 2 step 1).

**Calibrated defaults** (`presets.py`; the recommended values from the sweep):

- **Quantize:** **dithering off** (dithering adds noise the tracer turns into extra anchors), despeckle. *Marks:* light pre-blur (`blur_radius 1.0`) softens stairstepped edges, then Otsu threshold to mono. *Illustration:* **palette-LOCK** the quantize to the brand color tokens (`--palette`; default: the instance palette) — plain mediancut averages small brand accents (red, blue) into a muddy merge that SSIM does not catch because the background dominates the metric.
- **Color-SNAP (illustration):** after tracing, snap every fill back to the nearest brand token. vtracer re-clusters and introduces boundary-blend shades (e.g. a saturated blue drifts a step or two per channel) even from a palette-locked input; snapping guarantees the output carries exactly the brand palette. Color only — anchor count is unaffected.
- **potrace (mono mark):** `turdsize 2`, `alphamax 1.0` (above ~1.33 all corners are suppressed and marks lose crispness), `opttolerance 0.3`.
- **vtracer (color illustration):** `mode spline`, `hierarchical stacked`, `color_precision 4`, `filter_speckle 8`, `corner_threshold 45`, `path_precision 3`, `splice_threshold 45`. (`color_precision 4` keeps the full brand palette and high icon fidelity; lower values merge a tint and drop small-scale fidelity.)
- **SVGO:** conservative `convertPathData {floatPrecision: 2}` (reduces bytes, not anchor count; viewBox and per-color layers kept for editability).
- **Curve-fit (Schneider / `fit_curve.py`, never raw RDP):** **on for illustration** — it roughly halved the golden's over-segmented curves with no measured fidelity loss; **off for marks** — refitting rounds the corners that make a mark intentional. `path_ops.py` flattens M/L/H/V/C/S/Q/T and arcs (A, vtracer's space-separated form) before refitting.

There is a real tension between few anchors and crisp corners: the most aggressive reduction rounds off the corners that make a mark look intentional. The pipeline gets most of the way; the human polish wins the craft. **Golden results** for an instance are recorded with its calibration (`scripts/vectorize/instance_calibration.py`), not here.

**Knockout via render-then-potrace (dense / detailed two-tone subjects).** A direct vtracer 2-color palette-lock on a *dense* subject can bake an unstable figure/ground: the heavily-inked region becomes a full-canvas base-colour layer with the lighter colour stacked on top, so stripping the background exposes a solid block, not a silhouette. To get a clean single-colour **knockout** that keeps vtracer's bold stipple-collapse: render the full (correct) vtracer trace to a bold ink-on-paper bitmap, then `potrace` that bitmap (dark = foreground) → ink shapes on transparent with the lighter detail carried as interior **holes**. Notes: sample the actual ink + paper colours from the source raster when the art isn't brand-originated (don't default to the brand palette); drop crop-bleed strays by despeckling the rendered bitmap *before* potrace — keep only components whose bbox **touches the largest body's bbox** (this preserves intentional attached marks like a ground line and drops far edge slivers), because a bbox-max-dimension despeckle keeps tall-thin slivers; avoid a morphological *close* to solidify stipple — it over-fills and destroys interior detail (e.g. tyre hubs). The single-colour knockout (one editable `fill`) is the recommended primary brand-icon deliverable; offer two-tone (explicit cream highlights, better contrast on dark) as a variant. **Verify** by rendering on a contrasting colour (magenta confirms the background + holes are transparent) and on dark (confirms single-colour contrast). An instance keeps its worked sets and their measurements with its own records, not here.

**Post-processing geometry — use `path_ops`, not naive parsing.** When computing a path bbox, tightening a viewBox, or dropping stray paths from trace output, use `path_ops.parse_subpaths` + `flatten_subpath` for absolute geometry. Pairing every number in a `d` attribute as `x,y` silently breaks on relative commands (lowercase `c`/`l`/`v`/`h`) and arc parameters, producing out-of-range bboxes that blow up the viewBox.

**Landing marks as inline SVG — the per-call cap (real-engagement finding; primary lever is now dedup, v0.8).** Landing brand marks as editable vectors via `createNodeFromSvg` requires the SVG inline, which collides with the 50,000-character per-call `use_figma` cap. The **primary lever (v0.8) is SVG dedup**: the Builder imports each *unique* svg once as a Figma component (`createComponentFromNode`) and reuses it by instance, so a mark used many times costs its bytes once. That is what makes an SVG-heavy page buildable — a logo-heavy real page went from unbuildable-at-any-`--max-nodes` to a handful of chunks. **SVGO at precision 2 is the complementary per-mark shrink**, now wired as `build_figma.py --svgo` (`npx --yes svgo -p 2 --multipass`, opt-in and a hermetic no-op without `npx`): it roughly halves a detailed mark (≈27KB → ≈10KB observed) with no visible loss, packing the few unique masters into fewer chunks and clearing the cap for a single oversized master. Demonstrate colorway variants (reverse, one-ink) by **cloning a placed vector and recoloring its fills/strokes**, not by inlining a separately-recolored SVG per variant — fewer characters, and the variants stay tied to one source. The driver here is the per-call character budget, not anchor count; `build_figma.py` chunks by projected char length so it never emits an over-cap chunk (`examples/logo-wall.lg.ir.json` is the regression golden).

---

## 4a. Object-aware compositing (primitive refinement + managed keyline)

A refined emblem is **objects composited over frame primitives**, not one flat silhouette. A frame primitive (ring, badge, banner) sits *behind* the subject; where they overlap, the design needs a **keyline** — the negative-space (or positive-stroke) separation that makes the object read as on top. Two halves, one idea.

**Geometric-primitive refinement** (`scripts/vectorize/refine_primitive.py`). When a frame is traced as a wobbly path fused into the subject silhouette (one connected ink component, no separable circular subpath), it cannot be cleaned by dropping a subpath. Reconstruct it in raster space: `fit_circle` (Kåsa + MAD-reject robust fit → centre, outer/inner radius, gap) → `erase_band` (remove the thin frame band at pure-frame angles only; object crossings read thick and are kept) → re-trace the object alone → `arc_path_d` (replace the primitive with a true filled annular arc). The primitive is now a parameter, not a trace: smoother, fewer anchors (a worked emblem's ring went 114 → 108). Circle first; rounded-rect / capsule are future fitters behind the same `fit → arc` contract.

**Managed keyline** (`scripts/vectorize/composite_keyline.py`). The rule: a frame primitive is **knocked out around every object that crosses it**, by a uniform keyline — one operation, correct at every junction at once. Two kinds: **occlusion** (default) `frame − dilate(object, w)`, a background-coloured gap; **stroke** `dilate(object, w) − object`, a positive outline in a keyline colour. `w` (`keyline_width`) is the single parameter; default **≈ 1.8% of frame diameter** (`default_keyline_width`), calibrated on a worked organic emblem and generalised unchanged to two further marks from the same set. A designed open arc (the primitive's arc span) and figure-occlusion keylines stay independent and composable.

**Easily managed.** Emit object / frame / keyline as separate elements, never flattened. In Figma the managed form is a live **Boolean Subtract** (`ring − expanded-figure`); `figma_boolean_landing_js()` generates the `use_figma` op. Editing the figure or the offset reflows the keyline with no re-import.

**DEF-5 — the transform trap (read before touching trace output).** potrace's SVG backend wraps every path in `<g transform="translate(0,H) scale(0.1,-0.1)">`; embedding the raw `d` without it renders the path off-canvas — the mask/art silently does nothing, **yet a thumbnail still looks fixed**. It recurred at four assembly sites before the root cause was removed: `potrace_path(bake=True)` (the default) folds the transform into viewBox coordinates via `bake_transform`. Always decide from a render *and* a geometric assert (`assert_keyline_opens`, an A/B pixel-diff vs the continuous frame) — the thumbnail is the proxy that lied (§7). Worked set: an organic emblem from a client engagement (organic mark, ring + figure keyline), reproduced end-to-end by `refine_primitive.refine()` to ≤ 0.2%.

---

## 5. Re-run / idempotency contract

The Builder is not create-only. On re-run it must either **replace-by-key** or write a **new versioned page** (the human reviewer chooses):

- Tag built frames with a stable key via a name/description convention (`pluginData` is not reliably available through `use_figma`, so identity rides on names/descriptions).
- Branch on Variable/collection already exists (reuse) vs. missing (create), and on font missing at write time (flag, do not silently fall back).
- A multi-chunk page build is atomic per call but not per page, so detect a half-written page from returned node IDs and offer to clean or resume (partial-build recovery).

**Implemented (v0.3.0):** `scripts/build_figma.py --rerun replace|version` realises this as a dedicated Figma page per build, named with the IR's stable key (`HeyHi Bridge · <source>`, with a ` · <breakpoint>` suffix only for a single-breakpoint build). `replace` clears that page and rebuilds it; `version` writes `<page> vN`. The token collection and its Variables **find-or-create** by name on re-run (the reuse branch), so re-running reuses them rather than duplicating Variables — verified live (0 duplicate collection or Variables). Values are set on **create only**: a reused Variable is not overwritten (see the Canonical-collection reuse hazard below). The font-missing branch runs at write time (flag plus Inter fallback, never silent). The chunk runner `scripts/run_build.py` drives the chunked write, threading the returned id map across calls. Remaining follow-ups: partial-build recovery (resume from the returned node-id map), and setting the current page at the start of every chunk (a cross-chunk write currently lands the node on the build page via `appendChild`, but momentarily creates it on the default page).

**Canonical-collection reuse hazard (real-engagement finding, fixed v0.6.0).** When the Translate binds to a **pre-existing canonical Variable collection** — e.g. one authored on a Color foundations page in the same file — an earlier build overwrote the canonical values: `doVariable` called `setValueForMode` on the reuse branch as well as on create, so the extractor's low-confidence `matched` literals (observed: white CTA text matched to `backgrounds/surface` at 94%, a tinted eyebrow matched to `structural/border-default` at 92%) were written over the canonical token values. **Fixed in v0.6.0:** `doVariable` sets the value only when it *creates* a Variable; a found (reused) Variable is left untouched. Trade-off by design — a re-run no longer auto-updates a reused Variable's value, so a deliberate change to an existing Variable is now an explicit action (re-author it in Figma, or point the Translate at a separate collection).

**Anti-snap guard at the extractor (v0.4, WS4) — the upstream half.** The v0.6.0 fix stops a low-confidence `matched` literal from *overwriting* a reused Variable; the WS4 anti-snap guard stops the worst such literal from being *produced* in the first place. In `resolveColor`, a `text`-role colour that resolves only via the **matched** path whose nearest token is a **background**-family token (the "white CTA text matched to `backgrounds/surface` at 94%" case — a near-white label snapping to a near-white surface and vanishing) is kept literal and UNBOUND, with a `link-color-unsnapped` flag, instead of binding to that background token. The two defenses compose: the guard keeps the wrong bind from forming, and even where a bind does form the reuse branch never writes it back. The contrast complement is `near-invisible-label`, raised when a control label colour ≈ its own control fill (§3 control-affordance flags).

**Chat-driven chunk reissue (real-engagement finding).** When issuing `run_build` chunks manually via `use_figma`, the interpreter body (everything after the `OPS` array) is byte-identical across chunks — read only line 1 (`IDMAP`) and line 2 (`OPS`) of each `chunk_N.ready.js` and append a known compact interpreter, rather than re-reading the whole file each time. The `run_build` state persists on disk (`record`/`prep` accumulate the id map), so a chat-driven build survives context summarization: resume from `prep` at any point.

**Live-write pre-flight and context budget (multi-chunk pages; 2026-06-18, first full live acceptance).** Three steps make a real live write land instead of stalling. (1) *Cap triage.* Run `build_figma.py <IR> --summary` first and read the Build-plan line. If the max projected payload is over the 50,000-char `use_figma` cap and the warning names SVG masters that exceed the cap alone, re-run the build with `--svgo` (§4) — that shrinks the masters; lowering `--max-nodes` does **not** fix a single over-cap master. Confirm `GEOMETRY CHECK: PASS` after `--svgo`, then issue. (A logo-heavy home page went 51,106 → 44,895 chars this way; without it the write is transport-blocked.) (2) *New-page safety.* List the document's pages with `get_metadata` (no `nodeId`) and use a NEW, unique `--page-name`; the builder finds-or-creates by name and `--rerun replace` clears only that page, so a fresh name creates a new page and leaves every existing build untouched (new-page-not-replace by construction). (3) *Context budget.* Do NOT issue all chunks from the main session — each chunk's read + re-emit into `use_figma` is ~40–45K chars (~24K tokens), so a 10+-chunk page exhausts one context. Delegate the `prep → use_figma → record` loop to **sequential sub-agents handling ~3 chunks each** (4 approaches the per-agent limit). The on-disk `run-state.json` threads the id map across agents, so each sub-agent resumes at the recorded cursor — including after a sub-agent dies mid-run (read `run-state.json` for the cursor, then continue). The main session keeps the screenshot verification and the `compose_type` text-styles finish; load `use_figma` in each sub-agent via `ToolSearch`. The general form of this delegation pattern is in `CLAUDE-SESSION-RULES.md § In-session sub-agent delegation`.

---

## 5a. use_figma write-runtime gotchas (hand-authored pages and chunked builds)

These bite any `use_figma` write — the chunked Builder and a hand-authored page alike. They recurred on every page of a real-engagement build.

1. **`resize()` flips an auto-layout frame's sized axis to `FIXED`,** collapsing the hug axis (a vertical container drops to ~10px). Set or restore `primaryAxisSizingMode='AUTO'` (and `counterAxisSizingMode='AUTO'` for hug-height wrap rows) as the **last** operation on every authored frame, via a post-build `fix()` traversal of the tree. Do not trust the sizing modes set before `resize()` — the resize silently overrides them. **Implemented (v0.4, ADR-014):** `build_figma.py doFrame` now resizes only the FIXED axis and re-asserts `AUTO` on a HUG axis as the last op. This removes over-height white space on every vertical auto-layout section, not just wrap frames; NONE-layout (absolute) frames keep the literal captured box.
2. **Replication lag between back-to-back `use_figma` calls.** A cross-call read of a just-created page's `children` can return empty: the write has not yet propagated to the replica the next call hits. Before reading another call's nodes, `await figma.setCurrentPageAsync(page)` first (forces the page to load), then read, and **guard** — return an error sentinel and retry if the expected node is not yet visible. Prefer self-contained calls (each call builds a complete unit) over append-across-calls where feasible.
3. **`figma.loadAllPagesAsync` is not exposed** in the `use_figma` runtime — calling it throws. Use `setCurrentPageAsync` to force a single page's content to load instead.
4. **The executor wraps your `code` in an async function, so you must `return` a value** to get any output back. A trailing expression returns nothing ("Code executed with no return value"); end the script with `return JSON.stringify({...})`.
5. **Strip the `<style>@import …</style>` block from web-authored SVG before `createNodeFromSvg`.** Figma does not process `@import`; remove the block and let font resolution work by family name (preflight with `listAvailableFontsAsync`, per §2 / F4). With the brand families present in the file, text imports as editable text nodes with correct fonts.
6. **Wrap each `createNodeFromSvg` in try/catch inside a batch** so one malformed asset reports in the result array instead of failing the whole call.
7. **Landing a set of finished SVGs as a contact sheet:** create one labelled container frame placed clear of existing canvas (map top-level bounding boxes with `get_metadata` first), probe-land one asset and screenshot-verify, then thread the container id across calls with `getNodeByIdAsync`. Worked example: the True Once set (11 assets) landed into the HeyHi-Assets file, container node 76:2.

---

## 5b. Surgical finish (upgrade an already-built page)

To finish or upgrade a page that already has a structural build, work surgically rather than a from-scratch chunked rebuild — the monolithic chunked-write wall (§5a) does not apply, because a surgical finish issues a handful of small, targeted `use_figma` calls instead of the ten dense ~44k payloads of inline SVG a from-scratch rebuild requires.

- **Type system.** Apply `compose_type.py` (`extract → review → emit → create.js + apply.js`, §2) as the SKILL.md Type mode note describes — its `apply.js` classifies each **existing** TEXT node by its current resolved (family, weight-class, fontSize, letter-spacing-px, line-height-ratio) rather than reading a fresh IR, finds the nearest defined style, and calls `setTextStyleIdAsync`. Robust against repeated layer names (e.g. ten "Card Icon" / "Btn" nodes). Proven: 116 nodes classified, 0 mixed / 0 unmatched / 0 errors on a real page; letter-spacing/case disambiguate a tight label tier (an eyebrow vs. a nav label vs. a bold footer heading, all near the same font size).
- **Rasters via `upload_assets`** (raw bytes POST, zero agent transcription) carry the hero photo and any **dense SVG rasterized first** (`rsvg-convert -h 256 in.svg -o out.png`): a 26.8k screenprint logo or an 11–13k illustration becomes a crisp PNG with no transcription risk. Editable vectors stay on the brand's logo/illustration pages.
- **`imageHash` reuse:** `upload_assets(nodeId)` returns an `imageHash`; set that same hash as an IMAGE fill on every repeat slot via one small `use_figma` call (`node.fills=[{type:'IMAGE',scaleMode:'FIT',imageHash}]`) — on a real page, 14 unique uploads covered 24 icon slots and 6 covered a 40-item carousel.
- **Small clean SVGs** stay vectors via `createNodeFromSvg` (≤~1k Phosphor-scale icons transcribe reliably) when editability matters.
- **Asset→slot correlation:** the prototype's `<img src>` DOM order aligns 1:1 with the build's image-placeholder tree order — extract both, map by index.
- **Faithful gradients** reproduce IR `GRADIENT_LINEAR` scrims with `cssAngleToGradientTransform(deg)` (`dx=sin θ, dy=−cos θ`, §1) plus rgba stops; stack an image fill and a gradient fill on one node.
- **Resize raster nodes to the asset's true aspect** before FILL — a square placeholder distorts a wide wordmark.
- The general `use_figma` write-runtime gotchas (§5a) still apply: `return JSON.stringify(...)`, preload fonts before any text edit, wrap risky calls in try/catch, self-clean probe artifacts.

Net effect: a real client mockup was finished in place (type system + hero photo/scrim + 3 logos + 68 icon/illustration slots + text-wrap + CTA contrast) with no chunk runner and nothing transcribed that could not be reproduced faithfully. Live-proven 2026-06-17.

---

## 6. Golden sets

- **Translate:** three prototypes spanning the brand-config preferred patterns (Single Column Reader, Editorial Split, Case Study Scroll), each at `sm`/`md`/`lg`, plus one deliberately adversarial page (CSS grid + sticky nav + pseudo-element badges) to exercise the flag path.
- **Vectorize:** one mono mark and one limited-palette illustration.
- **Keyline (§4a):** an organic emblem from a client engagement (organic mark, ring + figure keyline) and one ringed object, reproduced end-to-end by `refine_primitive.refine()` to ≤ 0.2%.

---

## 7. Verification

- **IR (unit/trajectory):** golden prototypes have expected IRs; the extractor is diffed against them; every declared-token bind resolves; every does-not-map feature appears in `flags` (zero silent drops); low-confidence matches are flagged, not asserted. Schema validity is enforced by `schema/validate_ir.py`.
- **Translate (outcome):** build each golden IR into a scratch Figma file; compare per-breakpoint against the rendered HTML; assert color fills are Variable-bound (not hardcoded) and type values match their `token_ref` and cite it in the doc frame; confirm the doc frame lists tokens, type specimen, and flags; confirm the large-page build completes across chunks without orphaned parents.
- **Translate geometric gate (v0.4, ADR-014 / WS2):** `build_figma.assert_geometry(root)` walks the IR before any write and flags two defect classes geometrically (no Figma): **overflow** (a non-wrap `HORIZONTAL` frame whose children's summed width exceeds its fixed width — the lost-wrap signature) and **whitespace** (an auto-layout frame whose fixed, non-HUG height runs far taller than predicted content, tuned conservative so fixed-height controls do not trip it). Wired into the `--summary` approval surface as a `GEOMETRY CHECK` section and into `run_build.py self-test` as a hard failure. This catches the lost-wrap / dead-space class with a geometric assert, not an eyeballed thumbnail (corrections lesson `recurring-defect-needs-root-cause-not-per-site-patch`).
- **Translate instruments — make each able to fail, and read a PASS for what it proves (v0.14.0, geometry-defects arc).** `GEOMETRY CHECK` (`assert_geometry`) reasons about *emitted* geometry (a `frameAxisAuto` port) and flags `circular` (a `v:FILL` child inside a `v:HUG` primary axis — the D-09 143-vs-2664 root collapse) and `fallback` (a frame taking Figma's createFrame 100px default); it runs the css-grid pre-pass first, so a css-grid page is judged as emitted, not as the raw IR. New `scripts/figma_readback.py` is the live stage: `emit <ir> --out-dir D` writes one `use_figma` payload; run it on a scratch file via `use_figma(fileKey, <contents>)`; pipe the return to `verdict D`. It rebuilds the IR with real auto-layout, reads the root + token leaves back against the captured values, self-cleans on success and failure, and refuses a payload over the 50k cap (a full page goes through the plugin transport). New `scripts/preflight_fonts.py` is the font gate (Mode 1 preflight step). Every check is proven able to fail before it is trusted green (a pre-fix fixture shows the FAIL).

  | Instrument | Computes layout? | Sees the fallback / circular collapse | Judges fonts | Gate for |
  |---|---|---|---|---|
  | `GEOMETRY CHECK` (`assert_geometry`) | predicts emitted axes | yes, static prediction | no | plan-time geometry gate |
  | `mock-run.mjs` | no | no | only with a real `--fonts` dump | plumbing (ops execute, ids thread) |
  | `figma_readback.py` | yes, the real Figma engine | yes, measured not predicted | no | live geometry gate |
  | `preflight_fonts.py` | no | no | yes, inline runs included | the font gate |

  Over-trust warning: a `mock-run` PASS proves the ops run, not that the geometry is right or the fonts exist; a `GEOMETRY CHECK` PASS is a prediction, confirmed only by `figma_readback`.
- **Vectorize (outcome):** anchor count under the Phase-V.0 ratified ceiling for the asset class, palette matches the requested brand colors, visual fidelity acceptable at icon and hero scale. Record before/after anchor counts. Human-polish time is reported, not gated. For a knockout, also confirm transparency + interior holes on a contrasting background (magenta) and single-color contrast on dark (§4).
- **Keyline / object-aware compositing (§4a):** decide from a render *and* a geometric assert — `assert_keyline_opens()` proves the frame opened where the figure crosses (an A/B pixel-diff vs the continuous frame), the check a thumbnail cannot fake. A dropped potrace transform is silent and thumbnail-deceptive; `potrace_path(bake=True)` removes it at the source (DEF-5).
- **System:** one full dry run per mode in a scratch Figma file and a throwaway output dir before any real engagement. Promotion is gated on all three passing.

---

## 8. v1 success definition

v1 succeeds when (a) a real HeyHi identity proposal (a `ui-studio` prototype) is translated end to end through the four touchpoints into a Figma file with responsive mockups plus the documentation frame, color fills Variable-bound, and every unmapped feature surfaced as a flag, with no manual JSON authoring; and (b) a Nano Banana mark is vectorized to within the Phase-V.0 anchor ceiling and landed in the `logo.marks` slot, with the human polish step the only hand-work. Both run from a single chat invocation.

---

*HeyHi Confidential*
