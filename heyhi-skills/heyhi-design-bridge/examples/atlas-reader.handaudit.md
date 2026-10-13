---
classification: HeyHi Confidential
---

# atlas-reader — hand audit (zero silent drops)

The T1 golden prototype `prototypes/atlas-reader.html` is a Single Column Reader
page built on its fixture brand-config (`brand-config/example.json`, a neutral
example palette in the `ui-studio` token structure). It is deliberately adversarial:
every does-not-map feature from `reference.md` §3 is embedded so the extractor's
flag path is exercised end to end. Each such element carries a `data-audit="…"`
attribute naming the flag it must raise.

This audit is the ground truth for the smoke-test criterion "every does-not-map
feature appears in `IR.flags`." The flag set is identical across `sm` / `md` / `lg`
(features are viewport-independent), so the audit is stated once.

## Does-not-map features → flags (`needs_human: true`)

| # | Prototype element | `data-audit` | Expected flag | Emitted |
|---|-------------------|--------------|---------------|:------:|
| 1 | `header.site-header` (`position: sticky`) | `position-sticky` | `position-sticky` | ✓ |
| 2 | `button.back-to-top` (`position: fixed`) | `position-fixed` | `position-fixed` | ✓ |
| 3 | `.eyebrow::before` (pseudo content) | `pseudo-element` | `pseudo-element` | ✓ |
| 4 | `h1.title` (`font-size: clamp(...)` direct) | `clamp-calc-derived` | `clamp-calc-derived` | ✓ |
| 5 | `.reader` (`padding: calc(...)` direct) | (on `.reader`) | `clamp-calc-derived` | ✓ |
| 6 | `blockquote.pull-quote` (`transform: perspective/rotateX`) | `transform` | `transform` | ✓ |
| 7 | `.stat-row` (`display: grid`) | `css-grid` | `css-grid` | ✓ |
| 8 | `ul.tag-list` (`flex-wrap: wrap`) | `flex-wrap` | `flex-wrap` | ✓ |
| 9 | `pre.code` (`overflow-x: scroll`) | `overflow-scroll` | `overflow-scroll` | ✓ |
| 10 | `.pulse-dot` (`animation: pulse`) | `animation` | `animation` | ✓ |
| 11 | `.overlay-card` (relative box, absolute child) | `absolute-positioning` | `absolute-positioning` | ✓ |
| 12 | `p.phantom` (`font-family: "Phantom Sans Display"`) | `missing-font` | `missing-font` | ✓ |

12 flags, 11 distinct features (`clamp-calc-derived` fires twice: the title's
direct `clamp()` font-size and the reader's direct `calc()` padding). The
`pulse-dot` is **not** transform-flagged: with animations frozen its computed
transform is identity, and the mapper treats identity matrices as "none."
`aside.callout`'s stacked `box-shadow` (still marked `data-audit="multi-shadow"` in
the prototype) is **no longer flagged**: in v0.2 it maps to two `effects[]` entries
(ADR-010).

## v0.2 decoration fields (ADR-010 — real node slots, not schema-gap flags)

What T1 carried as aggregated `schema-gap:*` flags are now real node fields, emitted
by the extractor's `decorations()` pass. No flag.

| Field | Nodes (lg) | Example |
|-------|-----------:|---------|
| `cornerRadius` | 15 | `.pulse-dot` 8 (`50%` resolved against the box), `.cta` 4, `.tag` 2 |
| `strokes[]` | 1 | `figure img` 1px, color bound to `tokens.color.structural.border` |
| `effects[]` | 2 nodes / 3 entries | `.callout` two stacked DROP_SHADOW (spread + alpha preserved), `.cta` one |
| `opacity` | 1 | `.figcaption` 0.85 |

## Token recovery cases

| Case | Element | `source` | `match_confidence` | token_path |
|------|---------|----------|-------------------:|------------|
| Declared bare var (color) | `body` background | `declared` | 1.0 | `tokens.color.backgrounds.page` |
| Declared bare var (color) | `.cta` background | `declared` | 1.0 | `tokens.color.accent.primary` |
| Declared bare var (spacing) | `.stat-row` gap | `declared` | 1.0 | `tokens.spacing.grid_gap` |
| Declared bare var (type) | `.lede` font-size | `declared` | 1.0 | `tokens.typography.scale.h3` |
| Matched literal (near) | `.near-accent` `#E4572F` | `matched` | 0.998 | `tokens.color.accent.primary` |
| Matched clamp (type) | `.title` `clamp(...)` | `matched` | 0.5 | `tokens.typography.scale.h1` |
| Matched calc (spacing) | `.reader` `calc(...)` | `matched` | 0.595 | `tokens.spacing.tiers.2xl` |
| Matched inherited (color) | nav links, byline | `matched` | 1.0 | `tokens.color.text.muted` |

Declared bare-var colors resolve to the correct `token_path` (smoke criterion 3a).
At least one `clamp()`/`calc()` value is `source: "matched"` at low confidence and
carries a `clamp-calc-derived` flag (smoke criterion 3b): two do.

## Node-type coverage

All five IR node types are produced: `FRAME` (containers, chips), `TEXT`,
`VECTOR` (the inline `<svg>` wordmark, written to `prototypes/assets/vec-*.svg`),
`IMAGE` (the `<img>` figure), and `GROUP` (the overlay-card, whose absolute child
forces `layout.mode: NONE`).

## Reproduce

```bash
cd ../scripts/extract_scene_graph && node extract.mjs
python3 ../../schema/validate_ir.py ../../examples/atlas-reader.sm.ir.json \
  ../../examples/atlas-reader.md.ir.json ../../examples/atlas-reader.lg.ir.json
```

Re-runs are byte-identical (animations frozen, no clock or network dependence in
the measured values).

---

*HeyHi Confidential*
