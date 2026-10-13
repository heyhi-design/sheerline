---
classification: confidential
title: "Module 2.4 — The two-axis conflict order and the fundamentals layer"
track: 2
module: "2.4"
level: intermediate
prereqs: ["2.3"]
est_minutes: 30
teaches: sheerline
opens_files:
  - sheerline/os/operating-principles.md
  - sheerline/os/foundations/visual-design/FOUNDATION.md
---

# Module 2.4 — The two-axis conflict order and the fundamentals layer

## You are here

Foundations reference a corpus and a reasoning layer, but they do not settle disputes. This module opens the rule that does: what happens when accessibility, the brand design system, and the universal fundamentals disagree about a value. It closes Track 2. Previous: [`module-2-3.md`](module-2-3.md). Next: Track 3, which opens the Design-Systems quality loop (authored in the seminar's dispatch batch).

## Learning objectives

After this you can:

- Name the two axes of the conflict order and what each one decides.
- Say where the brand design system ranks on each axis, and why that is not a contradiction.
- Explain how an accessibility conflict resolves against a brand value.
- Place the universal fundamentals as a referenced layer, not one re-authored per skill.

## Concept

Three sources can disagree about a single value. The accessibility standard wants one thing (a minimum contrast, say), the brand design system wants another (its exact token), and the universal design fundamentals want a third. Sheerline resolves this with one rule, authored once as **A.1**, ratified. The instruction that comes with it matters as much as the rule: point at it, do not re-derive a second canonical hierarchy. HeyHi's order had been duplicated and divergent across skills, and two centers is exactly the anti-pattern the ratification exists to end.

A.1 is a **two-axis** rule, and holding the two axes apart is the whole module.

The **value-source axis** decides which source supplies the emitted value, in four steps. First, accessibility is a hard gate: when a value fails conformance, move to the nearest conformant value at the token source and record it, with safety-critical usability contracts folded inside the gate. Second, inside that gate the brand design system is authoritative for everything it specifies, on a specified-beats-silent test. Third, where the design system is silent, the universal fundamentals fill the gap. Fourth, a stated brand-versus-fundamentals conflict resolves to the brand rule and is flagged.

The **severity axis** decides something different: which failure to grade first. Its order is Accessibility → Interaction → Visual → Brand → Code. A brand deviation is a real defect, but it is graded after an accessibility or interaction failure, because it hurts less.

Now the payoff, and the line to remember: **author on brand, grade on severity.** The rule "use the design system's tokens, never a raw value" ranks brand *high*, because on the value-source axis the brand system supplies what gets emitted. The severity order ranks brand *low*, because a brand slip is less severe than an accessibility or interaction failure. Both are true at once, and they only look contradictory if you collapse them onto one axis. One asks "which source supplies this value" (answer: the brand system, inside the accessibility gate). The other asks "which failure do I fix first" (answer: accessibility, well before brand). Sheerline's evaluation and corrections layer grades on the severity axis, which is why the same brand system can rank high for what to emit and low for what to grade first.

The fundamentals themselves, the binding UX laws, the control-state contract, and the type and spacing constraints, are a *referenced reasoning layer*, not authored inside the operating principles. This is the same reference-not-copy discipline from module 2.3, applied one level up: the fundamentals are ratified once as Increment A (A.1 the conflict order, A.2 the laws, A.3 the control-state contract), the operating principles point at A.1, and the deep-area foundations point at the set. Nobody re-authors a second copy. The conflict order lives in one file; the fundamentals live in one place; everything else references both.

Two quick design terms. *WCAG* is the web accessibility conformance standard, and its AA level is the hard gate here, not a preference to weigh. A *token* is the design system's named value (a specific color or spacing step) that output uses instead of a raw literal, which is why "author on brand" means "reach for the brand token."

## Walkthrough

Open `sheerline/os/operating-principles.md` and find "The cross-quality conflict-resolution order". Read the "point at it, do not re-derive" instruction, then the two axes: the value-source axis (rules 1 through 4) and the severity axis. Read the paragraph that reconciles them, where `tokens, not raw values` ranks brand high for authoring while the severity order ranks brand low for grading, both true because they are different axes.

Now open `sheerline/os/foundations/visual-design/FOUNDATION.md` and find "the fundamentals reasoning layer (referenced, not authored here)". Notice the foundation points at the ratified spec and the reasoning of record rather than restating the hierarchy: the same reference discipline you traced for the style corpus in module 2.3.

## Lab

From `sheerline/os/operating-principles.md`, answer the axis question directly. Read the conflict-order section and state where the brand design system ranks on each axis: high or low on the value-source axis, and high or low on the severity axis. Then write the one sentence that reconciles them.

**Success looks like:** brand named as high on the value-source axis (it supplies the emitted token) and low on the severity axis (a brand defect is graded after accessibility, interaction, and visual), plus a single sentence, "author on brand, grade on severity," explaining why two different rankings do not conflict.

## Common misreads

- *"The conflict order ranks brand once."* No. It is two-axis: brand ranks high for authoring a value and low for grading a defect. A single number would hide the split.
- *"Author-on-brand and grade-on-severity contradict."* No. Different axes. One asks which source supplies the value; the other asks which failure to fix first.
- *"Accessibility is a preference to weigh against brand."* No. WCAG AA is a hard gate: resolve to the nearest conformant value at the token source and record it. It is not traded off.
- *"The fundamentals are authored in the operating principles."* No. They are a referenced layer, ratified once as Increment A; the operating principles point at A.1, and re-deriving a second hierarchy is the anti-pattern the ratification ends.

## Self-check

1. What does the value-source axis decide, and what does the severity axis decide?
2. Where does brand rank on each axis, and why is that not a contradiction?
3. How does an accessibility conflict resolve against a brand value?
4. From the Lab: brand's rank on each axis, and the one-sentence reconciliation.

## Go deeper

- `sheerline/os/operating-principles.md`, the conflict-order section: the two axes and the point-at-it rule in full.
- `sheerline/os/foundations/visual-design/FOUNDATION.md`: how a foundation references the fundamentals layer instead of re-authoring it.
- Architecture figure 5, [`../../docs/architecture.md`](../../docs/architecture.md), draws the boundary, the moat, and the two-axis conflict order.
- Grading on the severity axis is the evaluator's work, which Track 3 opens; the retained moat is Track 4.

---

*HeyHi Confidential*
