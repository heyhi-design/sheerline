---
classification: confidential
title: "Module 3.3 — GRADE: the evaluator"
track: 3
module: "3.3"
level: advanced
prereqs: ["3.2"]
est_minutes: 35
teaches: sheerline
opens_files:
  - ai-services/agentic-infrastructure/benchmark/eval_harness_i1.py
  - ai-services/agentic-infrastructure/benchmark/eval_harness_i2.py
  - ai-services/agentic-infrastructure/benchmark/eval_harness_i3.py
  - ai-services/agentic-infrastructure/benchmark/eval-harness-i1-preregistration.md
---

# Module 3.3 — GRADE: the evaluator

## You are here

VALIDATE returns a deterministic finding on one artifact at one moment. GRADE asks the two questions a single validation cannot: is the system getting better or worse across releases, and how good is the output on the axes no deterministic check can see? This is the verb where the moat lives, so it is taught as architecture and never reproduced. Previous: [`module-3-2.md`](module-3-2.md). Next: [`module-3-4.md`](module-3-4.md).

## Learning objectives

After this you can:

- State the one-line difference between a linter and an evaluator.
- Name the four evaluator layers and the single thing each one adds.
- Explain why a pre-registration is committed before the scorer exists.
- Explain "grades inform, never gate" as the don't-automate line made structural, and say where that rule began.

## Concept

The validator in 3.2 answers one artifact at one instant with a deterministic finding. GRADE asks two things that a single validation cannot. Is my system's conformance getting better or worse across releases? And how good is output on the axes no deterministic check reaches, whether it reads as this brand rather than generic-on-token, whether the layout is intentional rather than merely arranged? The one-line difference names the whole shift: a linter emits a boolean, an evaluator emits a series.

The evaluator is built in four layers, each adding exactly one thing the layer before it lacks.

**I1 is the discriminating scorer, the deterministic floor** over dimensions 1, 2, 3, and 6. Its job is not to grade production output; it is to prove the score can tell seeded drift from a clean version at all, by the located catch rule. A defect counts as caught only when a finding lands on the specific seeded target, scored as a paired comparison of a seeded artifact against its own unmodified twin. Because twin and seeded differ by exactly one mutation, the organic noise present in both cancels, and the separation survives contamination. I1's whole output is a kill decision: a floor that cannot separate stops the build.

**I1.5 is the mutation engine**, which asks the harder question by importing I1 and composing on top of it without editing it: does the floor catch a near-miss as readily as an obvious defect? It generalizes each operator from one value into a tiered space, a flagrant value nothing real would use, a realistic wrong choice, the subtlest non-conforming literal, and a structure-preserving control that stays valid. The boundary it locates is the finding: the deterministic layer keys on literalness, not magnitude. It catches drift that changes code structure, a literal where a token belongs or an unknown token name, and it is blind to drift that preserves valid structure, a real token used in the wrong role. Naming that boundary is worth more than pretending the floor has none.

**I2 is the series**: storage and trend, keyed by model, model version, system version, and date. It grades the golden set of known-good components and the correction pairs from the registry, and it carries the discipline that keeps a trend honest, which is to measure variance before reporting any delta. The deterministic floor has no model in the loop, so its run-to-run variance is zero by construction, and the comparison refuses to call any release-over-release change material unless it clears that measured floor. A line drawn through noise is a defect, so I2 enumerates every pair it cannot score rather than quietly dropping it.

**I3 is the judge panel** for the two irreducibly semantic dimensions, intent fidelity and compositional coherence, that no deterministic check reaches. Its shape is deliberate: a panel of distinct named lenses, not many identical raters, because identical raters only average a shared bias instead of removing it. The judge is blind to whether an artifact was seeded, and it is injected behind a provider-agnostic adapter rather than wired to one model. Two validity gates guard the instrument before anyone trusts it. The panel must sit at chance when asked to tell seeded from organic, because a panel that spots the injection seam is scoring the seam, not the quality. And it must return no fabricated findings on a genuinely clean set. Absent both, it ships the floor and reports the semantic ceiling only once a human has calibrated the panel and judged inter-rater agreement good enough.

That last clause is the rule the whole verb turns on. Across all four layers the pre-registration is committed before the scorer exists, fixing the separation statistic, the predicted ordering, and the kill criterion in advance, so no one can choose the passing criterion after seeing the numbers. And the output is always scores and located findings, never a verdict: the evaluator ships no default threshold. Which score blocks a merge, at what severity, for which team, is authored judgment the client owns. **Grades inform, never gate.** This is module [0.3](../track-0-orientation/module-0-3.md)'s don't-automate line made structural: the machine measures, and a person decides.

## Walkthrough

Open `ai-services/agentic-infrastructure/benchmark/eval_harness_i1.py` and read the docstring: the deterministic floor, the located catch rule, and the line that its output is a kill decision whose criterion lives in the pre-registration and the findings note, "never as a threshold constant here." Open `ai-services/agentic-infrastructure/benchmark/eval_harness_i2.py` for the linter-boolean-versus-evaluator-series line and the measure-variance-before-any-delta discipline. Open `ai-services/agentic-infrastructure/benchmark/eval_harness_i3.py` for the panel of distinct lenses, the blind injected judge, the two validity gates, and the ship-the-floor fallback. In each file, find the "grades, never gates; ship no default threshold" statement and notice it is load-bearing, not a footnote.

## Lab

Open `ai-services/agentic-infrastructure/benchmark/eval-harness-i1-preregistration.md`. Read section 5 (the kill criterion) and section 7 (no default threshold). State the kill rule in one sentence and the materiality rule in another, in your own words, from the pre-registration, not guessed.

**Success looks like:** the kill fires only for a reason internal to the scorer, a detector that misses its own seeded target or fires on the clean twin, and never for a substrate mismatch or a defect kind that had no seeder; and the scorer ships no default threshold, because which finding count blocks a merge is authored client judgment on the don't-automate line. Bonus: name the mutation pre-registration's materiality bar as the same kind of pre-registered validity margin, not an output-quality threshold.

## Common misreads

- *"The evaluator gates the merge."* No. It emits scores and located findings and ships no default threshold. Which score blocks a release is the client's authored call. Grades inform, never gate.
- *"A linter and an evaluator do the same job."* No. A linter emits a boolean at one instant; an evaluator emits a series across releases, plus a judged ceiling the linter cannot see.
- *"The pre-registration is written up after the run."* No. It is committed before the scorer exists, so the passing criterion cannot be chosen once the numbers land.
- *"The judge panel is many copies of one rater."* No. It is distinct named lenses, blind and injected, gated to sit at chance on the seam before its scores are trusted.

## Self-check

1. State the one-line difference between a linter and an evaluator.
2. Name the four layers and the one thing each adds.
3. Why is the pre-registration committed before the scorer exists?
4. From the Lab: the kill rule and the no-threshold rule, and how "grades inform, never gate" traces back to module 0.3.

## Go deeper

- `ai-services/agentic-infrastructure/benchmark/eval_harness_i1.py` and `ai-services/agentic-infrastructure/benchmark/eval_harness_mutation.py`: the floor and the mutation engine.
- `ai-services/agentic-infrastructure/benchmark/eval_harness_i2.py` and `ai-services/agentic-infrastructure/benchmark/eval_harness_i3.py`: the series and the judge panel.
- `ai-services/agentic-infrastructure/benchmark/eval-harness-i1-preregistration.md`: the separation statistic, the kill criterion, and no default threshold.
- Architecture figure 4, [`../../docs/architecture.md`](../../docs/architecture.md), draws GRADE as the third verb, with the grades-inform-never-gate rule on its face.
- Evaluation is the one invariant a firm does not give away (module [0.3](../track-0-orientation/module-0-3.md)); the retained moat returns in Track 4.1.

---

*HeyHi Confidential*
