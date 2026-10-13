---
classification: confidential
title: "Foundation: Collaboration, Communication & Facilitation (area 11, PARTIAL / governance-manifest)"
area: 11
nature: operating
coverage: partial
phase: P1
kind: governance
status: manifest
---

# Foundation: Collaboration, Communication & Facilitation (area 11)

**Coverage: PARTIAL (covered for general facilitation, partial for client design work). This is a governance manifest, not new capability.** Most of the value in this area is governance over a strong existing facilitation family plus a strict behavioral boundary, not new generation skills. It authors **zero net-new methods** and **copies nothing**. Manifest grade: pointers plus loading rules (the area-5/6/7 shape), not deep prose.

*Authored to close the gap the P1.5 operating-area skills surfaced: `design-rationale-decision-record` and `heyhi-figjam-mapper` register into area 11, and until now they registered into context that did not exist. Paths below are repo-root-relative.*

---

## The spine: three behavioral guardrails (referenced, never restated)

This area's spine is three behavioral guardrails. They are authored **once**, as first-class invariants in [`os/operating-principles.md`](../../operating-principles.md) (the "zero-cost operating invariants" section), because their failure modes are cross-cutting — the temptation to auto-generate critique, to present simulated cognitive inference as real empathy, or to let model-assisted ideation collapse a set's diversity, can surface in a proposal, an email, a workshop design, or a client summary, not only when a task routes into this area. A guardrail that only loaded when someone routed here would be reliably absent in exactly the mis-routed cases where it is most needed. So they live in always-loaded governance, and **this foundation names each and points at its canonical statement; the one-line gists in the table below are pointers, not the governing text** (the reference-not-copy rule applies to the behavioral boundary exactly as it applies to the corpus, and two centers is the anti-pattern the placement exists to avoid):

| Guardrail | Where it lives (canonical) |
|---|---|
| Critique and facilitation governance (critique is never a generation target; assemble the pre-read and capture decisions, render no verdicts) | `os/operating-principles.md` — zero-cost operating invariants |
| The empathy boundary (a model simulates cognitive empathy; it has no experiential or compassionate empathy; simulated empathy is never presented as the real thing) | `os/operating-principles.md` — zero-cost operating invariants |
| The ideation-diversity guard (model-assisted ideation is stimulus, never selection; widen the field, measure overlap, warn on premature convergence; the human chooses) | `os/operating-principles.md` — zero-cost operating invariants |

## Registered skills (area 11)

| Skill | Verb | What it does | Judgment that stays human |
|---|---|---|---|
| `design-rationale-decision-record` | validate | Scaffolds a decision record (ADR / DACI), checks DACI completeness, sweeps docs and threads for unrecorded or contradicted decisions | The rationale content and the decision itself ship empty |
| `heyhi-figjam-mapper` | generate | Renders flows / journey maps / service blueprints / IA maps live in FigJam from structured inputs; routes each type to the right Figma mechanism | Pain points, opportunities, IA-correctness stay the human's (empty judgment slots) |
| `heyhi-workshop` | consult / facilitate | Runs or preps a workshop (Human-in-the-Loop, Anti-Slop, Craft at Scale) — covers general facilitation | Reading the room, safety, who-holds-the-decision |
| `heyhi-deck` | generate | Builds decks and teaching material — the articulation/communication surface | The argument being made |
| `crit-prep-and-capture` (deployed) | prepare / capture | Assembles the crit pre-read from the presenter's stated goals (stops when none are stated) and captures the room's items, dispositions (default `undecided`), and follow-ups; emits each decided item into the decision-record shape `design-rationale-decision-record` consumes | The critique itself, the verdict, the read of the room, who holds the decision — the artifact has no field for any of them |

`heyhi-learning-series` serves this area from the HeyHi/keel layer but is not in Sheerline's governed subset (a watch-item, not under-coverage). The net-new here is deliberately thin: the class-N net-new, `crit-prep-and-capture` (assemble a pre-read, capture decisions, render no verdicts), is built and deployed (2026-09-05); the exec-translation / articulation extensions stay P3, gated on real pull.

## The canon this area references (as reference, never generated)

| Reference | What it supplies | State |
|---|---|---|
| `ai-services/design-intelligence/research/sheerline-skill-buildout-research-2026-08-09.md` § 6.3 | The facilitation canon of record: the critique boundary (critique evaluates work against *stated goals* through dialogue; crit formats held as reference for humans to run; model critique is an always-available first reviewer, never a final gate); the articulation canon (Greever; Minto / SCQA; BLUF — with the caveat that the *struggle* of articulating is the mechanism); the decision-record canon (ADR; DACI for the choice vs RACI for the work) | Authored, landed |
| `heyhi-skills/heyhi-workshop/`, `heyhi-skills/heyhi-deck/` | The deployed facilitation and articulation methods | Deployed |
| `heyhi-skills/design-rationale-decision-record/`, `heyhi-skills/heyhi-figjam-mapper/` | The two P1.5 area-11 skills carry their own method in their references | Deployed |

Design critique is a don't-automate boundary: it is a facilitation and behavioral-corrections surface, never a generation target. That rule is the first guardrail above, referenced not restated.

---

*Area map: `os/foundations/registry.yaml` · The three behavioral guardrails: `os/operating-principles.md` · Skill routing: `sheerline/skills/registry/skill-registry.py`*

*HeyHi Confidential*
