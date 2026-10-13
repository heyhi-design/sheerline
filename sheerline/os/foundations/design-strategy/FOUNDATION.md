---
classification: confidential
title: "Foundation: Design Strategy & Product Thinking (area 9, PARTIAL / governance-manifest)"
area: 9
nature: operating
coverage: partial
phase: P1.5
kind: governance
status: manifest
---

# Foundation: Design Strategy & Product Thinking (area 9)

**Coverage: PARTIAL. This is a governance manifest, not new capability.** It brings the strategy area under governance at manifest grade: register its skills, point at the canon as reference, and name where the human judgment stays. It authors **zero net-new methods** and **copies nothing**. Manifest grade means pointers plus loading rules, not the deep prose of a Visual or Design-Systems foundation (the area-5/6/7 shape).

*Authored to close the gap the four P1.5 operating-area skills surfaced: two of them (`design-measurability-mapper`, `strategy-integrity-warden`) register into area 9, and until now they registered into context that did not exist. Paths below are repo-root-relative.*

---

## What this area governs

Design strategy and product thinking is the operating layer where a designer decides *what* to build and *whether it worked* — opportunity framing, measurability, prioritization — as distinct from the craft of building it. The dominant build-class here is governance, not generation: this area breeds plausible-but-hollow skills (a "product-sense generator" is the archetype), so the canon is carried as **reference for a human to reason with**, never as a thing the agent produces.

## Registered skills (area 9)

| Skill | Verb | What it does | Judgment that stays human |
|---|---|---|---|
| `design-measurability-mapper` | validate | Answers "is this design goal measurable at all?" and builds the Goals→Signals→Metrics scaffold; audits whether events are instrumented; stress-tests for gaming | **Metric selection** (a values decision) ships empty; target-setting |
| `strategy-integrity-warden` | validate | Audits an opportunity-solution tree / JTBD / prioritization artifact for reasoning integrity — evidence-linkage-or-assumption-flag, solutions-dressed-as-opportunities, back-solved scores, evidence staleness | **Which opportunity, the what-to-build call** — the warden never selects |
| `futurecasting` | consult | Org foresight, preferred-future design, the Decision Register (adjacent — org direction, not product-opportunity selection; `strategy-integrity-warden` is its X on the Decision Register) | The strategic direction itself |

Both P1.5 skills are warden/validator-shaped by construction: they structure and audit, they do not select. A capability in this area that scores, ranks, or selects an opportunity or a metric has exceeded its charter (see the boundary below).

## The canon this area references (as reference, never generated)

| Reference | What it supplies | State |
|---|---|---|
| `ai-services/design-intelligence/research/sheerline-skill-buildout-research-2026-08-09.md` § 6.1 | The strategy canon of record: product-sense as reference-only; the Opportunity Solution Tree carried *with its 2026 failure modes* (the dominant critique is starving the tree, not drawing it wrong); JTBD's two lineages disambiguated (Ulwick ODI vs Christensen); the measurement canon (HEART / Goals-Signals-Metrics with the no-validation caveat; North Star with its gaming critiques); the prioritization canon (RICE as read-and-challenge; back-solved scores are the anti-pattern) | Authored, landed |
| `heyhi-skills/futurecasting/` (SKILL.md + references) | The org-foresight method: the seven generative tools, the Working Canvas, the Decision Register, the pre-mortem | Deployed |

HeyHi's product/design-strategy corpus is otherwise **thin** (the honest state — most existing strategy material is org-foresight via `futurecasting`, not product-opportunity or measurement work). The P1.5 skills carry their own method in their references; this manifest does not restate it. Deep product-strategy canon is a P3 build if an engagement pulls it, not a Phase-1.5 task.

## The human-judgment boundary (referenced, not restated)

The rules that keep this area's skills warden-shaped are the standing boundary in [`os/operating-principles.md`](../../operating-principles.md): the taste-and-critique boundary, the "what stays human" list (which names **metric selection** and **the positioning stance**), and the grades-inform-never-gate line carried in that same taste-and-critique boundary. **Point at that boundary; this foundation does not restate it.** The reference-not-copy rule applies to the behavioral boundary exactly as it applies to the corpus.

---

*Area map: `os/foundations/registry.yaml` · Human-judgment boundary + the grades-never-gates line: `os/operating-principles.md` · Skill routing: `sheerline/skills/registry/skill-registry.py`*

*HeyHi Confidential*
