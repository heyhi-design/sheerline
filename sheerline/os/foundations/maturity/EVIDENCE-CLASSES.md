---
classification: confidential
title: "Sheerline maturity evidence classes: direct / indirect / affirmation (EVIDENCE-CLASSES.md)"
created: "2026-09-13"
source: plans/plan-sheerline-maturity-instrument-2026-09-12.md   # DF-01 W1, Phase B (B2)
---

# Evidence classes

**HeyHi Confidential.** The three evidence classes that **substantiate** a practice-capability
level rather than assert it. Modeled on SCAMPI's evidence taxonomy: a rating is never made on
work products alone, so an affirmation is required before the top rungs. Read this alongside
`LEVELS.md` (the 5-rung scale) and the per-area `maturity.evidence` blocks in
`os/foundations/registry.yaml`.

## The three classes

| Class | What it is | Examples |
|---|---|---|
| **direct** | The work product itself, directly attributable to the practice. | A merged PR, a `FOUNDATION.md` section, a `measure_maturity.py` structural check id. |
| **indirect** | Supporting or resultant artifacts: evidence that the practice produced something, not the thing itself. | A corrections or intake candidate id classified to this area (**derived**, see below). |
| **affirmation** | A dated human-gate signature: a **fire**, per the empirical-moat vocabulary. The in-the-room confirmation, not an empty slot. | A signed gate row with a date and the gate name. |

## How `indirect` evidence is derived

This is the load-bearing mechanism, and the place the instrument is easiest to get wrong.

`measure_maturity.py` classifies a corrections or intake entry to an area by keyword-matching
its `category` / `trigger_context` / `correction` text against the area's `key` and `name`. It
**reuses the corrections `search.py` field-weighted scoring** (`correction` 1.0,
`trigger_context` 0.8, `pattern` 0.6, `id` 0.6, `category` 0.5) rather than inventing a second
matcher, so the classification uses the same relevance mechanism the corrections CLI already
trusts.

The area's `FOUNDATION.md` vocabulary was considered as an additional query source (and named as
one in the plan's B2) but **deliberately dropped**: its headers are broad enough that nearly
every corrections/intake entry token-overlaps them (30-37 of 43 per area, versus 0-6 for
`key` + `name`, in the Phase-B probe), which turns `indirect` into noise. `key` + `name` is the
discriminating vocabulary, and a human confirms every hit regardless, so precision wins.

Three properties keep this honest:

1. **Derived, best-effort, never a stored foreign key.** An `indirect` hit is recomputed from
   text every run. Nothing writes a Sheerline-area id back onto a correction entry.
2. **The corrections `dimension` field is not a Sheerline area id.** The corrections schema
   carries an optional `dimension: 1-6` field. That routes to the **eval-harness scoring
   dimension** (the grading axes), a wholly different axis from Sheerline's 13 practice areas.
   It must never be read as a Sheerline area id, and this instrument never does.
3. **Low-confidence and multi-area matches are surfaced, not filed.** When a match is weak or a
   correction plausibly belongs to more than one area, `measure_maturity.py` surfaces it for a
   human check instead of silently attaching it. The script never gates on its own
   classification: grades inform, they do not gate.

## How evidence maps to a level

- **Levels 1 through 3** can be substantiated by `direct` plus `indirect` evidence: the
  mechanism ran and produced artifacts.
- **Levels 4 and 5 require at least one `affirmation`.** No quantity of `direct` or `indirect`
  artifacts reaches Level 4 without a signed gate. This is the proof-versus-fire wall stated in
  `LEVELS.md`: a proof means the mechanism ran; a fire means a human signed it in the room.

An agent can assemble `direct` and `indirect` evidence on its own. It cannot manufacture an
`affirmation`. That asymmetry is the reason the instrument cannot inflate itself.

*HeyHi Confidential*
