---
title: "heyhi-logo-system — Scale-Degradation Matrix"
classification: HeyHi Confidential
module: D
loads_in: [Spec, Critique]
version: "0.1.0"
created: "2026-06-10"
grounding: ["schema.json:280 (logo.scale_degradation, frozen)", "gate0-facilitation-guide.md (16px test)", "reference.md (Scalability axis)"]
---

# Scale-Degradation Matrix

**HeyHi Confidential**

*On-demand reference module for `heyhi-logo-system`. Loads in **Spec** (to fill `logo.scale_degradation`) and **Critique** (to score the Scalability axis against a defined path rather than a vibe). Its output keys match the frozen `logo.scale_degradation` schema (`schema.json:280`); it adds no new field.*

---

## The principle: degradation is typology-dependent

The external `ckm:logo-design` skill ships one flat size matrix (512 / 128 / 32 / 1200×630 / monochrome) applied to every mark. That is the right instinct — a written ladder of checkpoints — but a wordmark and a combination mark do not degrade the same way. A wordmark sheds *characters*; a combination mark sheds its *wordmark*; an emblem often cannot shed anything and must be redrawn. This module makes ckm's flat matrix **typology-aware**, so the reduction path in the spec is the one this construction type actually needs.

A mark without a defined reduction path "just shrinks until it fails." That is a **High** severity finding in the severity rubric, and it is what this matrix exists to prevent.

---

## The standard checkpoint ladder (surfaces every mark must pass)

These are the recurring real surfaces. Treat the pixel thresholds as **defaults the spec author tunes per mark**, not absolutes — the schema's `below_px` is per-mark for exactly this reason.

| Checkpoint | ~Size | What must hold | Common reduction action |
|---|---|---|---|
| Full lockup | ≥ 96 px / print | Everything: mark + wordmark + any tagline | none (home size) |
| App icon | ~128 px | The mark in a square; internal detail simplified if needed | simplify internal detail |
| Sub-lockup floor | < ~64 px | Wordmark legibility starts to fail | switch to **icon**-only (ckm's <64px rule) |
| Favicon | ~32 px | Icon recognizable, high contrast | **icon**, often **monochrome** |
| Legibility floor | 16 px | The mark is still *recognizable as the brand* | the 16px test (Legibility axis) — see below |

The 16px row is HeyHi's existing **16px test** from `gate0-facilitation-guide.md`: render the mark at 16×16 and ask, for a wordmark, which letters survive; for a symbol, whether it is still recognizable. The matrix below states *what each typology becomes* on the way down this ladder.

`use_mark` values must come from the frozen schema enum: **`icon` | `monochrome` | `simplified`**.

---

## Per-typology reduction paths

| Typology | Reduction path (full → smallest) | Default threshold(s) | Terminal `use_mark` |
|---|---|---|---|
| **Wordmark** | full wordmark → tighter tracking / drop tagline → single-glyph or initial lockup | below ~48 px → `simplified`; below ~24 px → `icon` (the glyph) | `icon` |
| **Lettermark** | full initials → (already compact) → high-contrast initials | below ~24 px → `monochrome` | `monochrome` |
| **Pictorial** | lockup → symbol only → simplified symbol | below ~64 px → `icon`; below ~24 px → `simplified` | `simplified` |
| **Abstract** | lockup → symbol only → (already minimal) | below ~64 px → `icon` | `icon` |
| **Combination** | full lockup → drop wordmark, icon only → simplified icon | below ~64 px → `icon`; below ~24 px → `simplified` | `simplified` |
| **Emblem** | full emblem → **redrawn** simplified emblem → monochrome glyph/initial | below ~96 px → `simplified` (a *separately drawn* small form, not a scaled-down emblem); below ~32 px → `monochrome` | `monochrome` |
| **Dynamic** | active system → the stable anchor form → monochrome anchor | below ~64 px → `icon` (anchor); below ~24 px → `monochrome` | `monochrome` |

**The emblem caveat (the one that bites).** Emblems are detail-dense and inseparable, so a scaled-down emblem turns to mud. The reduction step for an emblem is not "shrink it" — it is "switch to a *separately drawn* simplified form below the detail-survival threshold." If a spec leaves an emblem with no redrawn small form, Scalability is **Not ready** (1) regardless of how good the full mark is. Flag it; do not average it away.

---

## What this produces in the config (exact `logo.scale_degradation` shape)

Module D writes directly into the frozen field. A combination mark, worked:

```json
"scale_degradation": {
  "thresholds": [
    { "below_px": 64, "use_mark": "icon",       "$description": "Below 64px the wordmark is unreliable; drop to the icon-only lockup." },
    { "below_px": 24, "use_mark": "simplified", "$description": "Below 24px (favicon and smaller) use the simplified icon with reduced internal detail." }
  ],
  "reduction_path": "Full lockup (mark + wordmark) down to ~64px; icon-only from 64px to 24px; simplified icon below 24px. The wordmark is never set below 16px.",
  "$description": "Ordered reduction path for a combination mark; thresholds are tokenizable, the 'degraded but still recognizable' judgment lives in the design-intent document."
}
```

Keys used — `thresholds[]` with `below_px` (integer), `use_mark` (one of `icon`/`monochrome`/`simplified`), per-threshold `$description`; plus `reduction_path` (string) and a field-level `$description` — are exactly the frozen schema's keys (`schema.json:280`). No new key is introduced.

---

## Coordination notes (how this composes with the other streams)

- **Critique Scalability axis.** The axis is scored against *whether a path like the above exists and is stated*, not against an impression. A mark with a typology-correct reduction path is at least **Ready** (3) on Scalability; a mark with no path is **Not ready** (1).
- **R2 (projected vs measured).** When critiquing an *unrendered* concept, this matrix gives the **projected** reduction path from the typology. Mark Scalability "projected from structure, not measured," cap go/no-go at medium confidence, and confirm the path at the mandatory render-and-verify second critique (render at 16/32 px and look). The matrix is the projection; the render is the measurement.
- **F5 (raster input).** If only a raster is available, the small-size render shows resampling blur, not the true reduction behavior. Mark Scalability "estimated (raster)" and prefer vector via the Figma MCP before certifying.
- **Module E.** "No reduction path" and "emblem with no redrawn small form" are catalogued Scalability failures in [`mark-failure-modes.md`](mark-failure-modes.md); this module is the fix-side, that module is the find-side.

---

*Companion module to `heyhi-logo-system`. Cross-references: [`logo-typology.md`](logo-typology.md), [`mark-failure-modes.md`](mark-failure-modes.md). Grounding: `heyhi-skills/ui-studio/brand-config/schema.json` (frozen `logo.scale_degradation`), `ai-services/design-intelligence/gate0-facilitation-guide.md` (16px test).*

*HeyHi Confidential*
