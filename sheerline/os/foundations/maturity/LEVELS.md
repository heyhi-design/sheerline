---
classification: confidential
title: "Sheerline practice-capability levels: the 5-rung scale (LEVELS.md)"
created: "2026-09-13"
source: plans/plan-sheerline-maturity-instrument-2026-09-12.md   # DF-01 W1, Phase B (B2)
---

# The Sheerline practice-capability scale

**HeyHi Confidential.** The generic 5-rung scale for the Sheerline maturity instrument. This
file ships the **scale** (rung names, generic meanings, one synthetic worked example). It
carries **no real per-area rung text and no real level/target/evidence value** for any of the
13 areas. Those live in the private `sheerline/` tree (each area's `maturity` block in
`os/foundations/registry.yaml`, plus its evidence refs), exactly as the `coverage:` tags do
today, and they never travel out of it. Because this file is the mechanism only, it is the
**keel-upstream-eligible artifact** (plan § 1 B4): a keel adopter could uncomment a
`# maturity: <level>` line the same way the template already ships the optional coverage-state
fields, without ever seeing HeyHi's real per-area content.

## What this instrument is (and is not)

It grades **Sheerline itself** (HeyHi's own 13-area practice-delivery capability) on how good
and mature each area's practice is. It is a **sibling of `coverage`, not a replacement**:
`coverage` answers "does at least one skill plus a foundation exist" (a coarse existence tag);
this scale answers "how well does the practice actually run" (a finer judgment ladder). The two
are orthogonal and never conflict. `coverage` stays the canonical existence tag; a
practice-capability read never moves a `coverage` value.

**Naming discipline (required).** In any client-facing text this is the
**"practice-capability level"**, never a bare "maturity level" and never "the maturity model."
"The maturity model" is a different, client-facing instrument
(`ai-services/design-intelligence/design-system-maturity-model.md`) that grades a **client's**
design system on a 5-level by 6-to-8-axis automation ladder. The two share a 1-to-5 numeral and
nothing else. The deliberate divergence in rung names below is the collision guard.

## The scale (Dreyfus-shaped)

A **judgment** ladder (rule-following to intuitive expertise), not an infrastructure-automation
ladder. Sheerline's areas are graded on practice judgment (is a ship-empty slot really
exercised, is a correction a real incident or a seeded one, has a human signed a gate in the
room), which is Dreyfus's domain. The automation-ladder shape belongs to the separate
client-facing model named above.

| Level | Rung | What the practice looks like at this rung (generic) |
|---|---|---|
| 1 | **Scaffolded** | The practice exists as structure and rules, and is followed literally, context-blind. A foundation plus at least one skill exist; the ship-empty slots are present but applied by rote. |
| 2 | **Situated** | The practice adapts to the situation. Whoever runs it reads context and chooses among the rules; the slots are exercised with real judgment on real inputs, case by case. |
| 3 | **Governed** | The practice pauses and asks by rule where its own contract is silent, and names deliberate absences instead of defaulting them. A governance `FOUNDATION.md` section states the pause-and-ask rules. |
| 4 | **Calibrated** | The practice's judgment has been checked against evidence and a human gate has signed it in the room. The rule is tuned by real incidents, not by assertion. Requires at least one affirmation (a signed gate). |
| 5 | **Exemplary** | The practice sets the pattern others adopt, and its incidents become the anchors that teach the rung below. Requires sustained affirmations plus the practice being reused or cited beyond its origin. |

A level reads `null` (ungraded) when no rung has been authored for that area yet. This is
deliberate (SFIA: not every level is meaningful for every skill), not a forced floor of 1.

**Monotonic-by-agent.** An agent may raise a stored level when the evidence supports it; only a
**human** lowers one. This is the "practice capability can regress" property (a leadership
change or a lost practice can move an area down), and the down-move is a human judgment, never
an automatic recompute. `measure_maturity.py` surfaces a `POSSIBLE-REGRESSION` flag for review;
it never lowers a stored level itself.

## How a rung gets authored: BARS from the corrections registry

Each rung, once authored for a real area, is anchored by a concrete **behavioral incident**:
a good-or-poor example of the practice in action, drawn from Sheerline's corrections registry.
That registry is a **critical-incident log** already (`trigger_context` plus `correction`, one
incident per entry), which is exactly the raw material a behaviorally anchored rating scale
(BARS; Flanagan's critical-incident technique, 1954) is built from. Authoring rungs is
therefore near-free once real incidents exist, rather than a new research program.

**The activation rule.** A real rung is authored from a **promoted correction** (a real fire),
or, only if the instance owner explicitly approves, **provisionally** from the seed layer plus evaluator
findings, marked provisional until a real fire supersedes it. As of Phase B the corrections
registry holds zero real-engagement fires (method 0, seed 13, all generic or demo), so **no
real rung is authored in this file**. The one example below is synthetic.

## The one worked example (synthetic)

Not a real area, not a real correction id, not a HeyHi finding. It shows the shape a real rung
takes; it grades nothing.

> **Area 0, "Widget Practice"** *(fictional; not in the 13-area map)*, **Level 3, Governed.**
> Behavioral anchor: *"When a widget spec omits a stated failure mode, the practice pauses and
> asks rather than inventing a default."* Anchored to synthetic incident `WP-014`: an invented
> default shipped and was later retracted. Evidence: `direct` is a governed `FOUNDATION.md`
> section stating the pause-and-ask rule; `indirect` is a corrections entry recording the
> `WP-014` pattern; `affirmation` is none yet. That last point is load-bearing: this is a
> **proof** (the mechanism ran), not yet a **fire** (no human gate has signed it in the room),
> so Level 4 is out of reach until one does.

## The proof-versus-fire wall

A **proof** means the mechanism ran. A **fire** means a human gate signed it in the room. Levels
1 through 3 can be substantiated by `direct` and `indirect` evidence. **Levels 4 and 5 require
at least one `affirmation`** (a signed gate). No quantity of `direct` or `indirect` artifacts
reaches Level 4 without a fire. This is why the instrument cannot inflate itself: an agent can
produce direct and indirect evidence, but it cannot manufacture an affirmation.

## The moat boundary

This file is generic and publishable: rung names, generic meanings, one synthetic example, and
the field shape. Every real per-area rung descriptor, and every real `level` / `target` /
`evidence` value, stay retained in the private `sheerline/` tree exactly as `coverage:` tags do
today. They are the practice-capability equivalent of a trade secret and never travel to keel.
See `EVIDENCE-CLASSES.md` for the three evidence classes and how `indirect` evidence is derived.

*HeyHi Confidential*
