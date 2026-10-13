---
classification: confidential
title: "Module 4.3 — Extending the system"
track: 4
module: "4.3"
level: expert
prereqs: ["4.2"]
est_minutes: 35
teaches: sheerline
opens_files:
  - sheerline/os/foundations/registry.yaml
  - sheerline/os/corrections/LIFECYCLE.md
  - heyhi-mcp/heyhi_mcp/corrections/schema.yaml
---

# Module 4.3 — Extending the system

## You are here

You can run a loop. Now grow the harness: add a practice-area foundation, add a correction, add an eval case, and know exactly where judgment stays human. The question this module answers: how do you extend the system without eroding the boundary that protects it? Previous: [`module-4-2.md`](module-4-2.md). Next: [`module-4-4.md`](module-4-4.md).

## Learning objectives

After this you can:

- Add a practice-area foundation through the registry, referencing the corpus rather than copying it.
- Author a correction with the right severity and say why it is or is not promotable.
- Add an eval case as a known-bad and expected pair without setting a gate.
- Name the human judgment that sits at each of these three extensions.

## Concept

Extending the harness is three moves, and each one has a human at the gate.

**Add a foundation.** A practice area is a row in the registry carrying a coverage state and a phase. Deepening it means registering its skills, seeding its corrections, and pointing the foundation manifest at the corpus in place, never byte-copying it, the reference-not-copy discipline from module 2.3 applied one level up. The judgment that stays human is which area to deepen next and whether a gap is worth filling now, which is what the coverage-and-phase map exists to make visible rather than decide.

**Add a correction.** A correction is factual or behavioral, and the difference decides what it may do. A factual correction is a deterministic, structural fact, a hardcoded hex where a token exists, an off-scale spacing value; it can be injected, and once it keeps firing, five or more times or across three or more separate sessions, it can be promoted to a hard rule. A behavioral correction is a taste read or a critique tendency; it surfaces to a human as a reminder to decide, and it is never promotable to an auto-enforced rule. A taste correction hardening into an enforced check is the boundary collapsing, which is why the severity vocabulary is exactly two values and the design taxonomy lives in a separate category field. The registry is curated, not generated: an agent may propose a pattern, but a human decides what enters and what promotes.

**Add an eval case.** A recurring drift, captured as a known-bad and expected pair, joins the graded known-bad set from Track 3.3 and 3.4. The judgment that stays human is which score blocks a merge, because the evaluator ships no default threshold, and that decision is authored client policy sitting on the don't-automate line.

The through-line is one idea: every extension has a person at the gate. The don't-automate line from module [0.3](../track-0-orientation/module-0-3.md) is not a limit bolted on afterward; it is the thing the whole system is built to protect. The harness compounds the mechanical work so the team keeps more room for the judgment that was never a generation target.

## Walkthrough

Open `sheerline/os/foundations/registry.yaml` and read how an area carries a nature, a coverage state, and a phase, so deepening one is a tracked, scheduled act. Open `sheerline/os/corrections/LIFECYCLE.md` and read "The factual / behavioral boundary", "Promotion thresholds", and "The human standard": only factual corrections are injected or promoted, a behavioral one is never promotable, and the registry is curated. Then open `heyhi-mcp/heyhi_mcp/corrections/schema.yaml` and read the design-extension section for the fields a new correction carries, the severity, the category taxonomy, the predicate, and the known-bad and expected pair.

## Lab

Sketch a new correction entry. Pick a real design drift, decide its severity, factual or behavioral, and say in one line why it is or is not promotable.

**Success looks like:** two entries that show you own the line. A hardcoded-hex-where-a-token-exists correction is `factual` and becomes promotable once it keeps firing, because it is a deterministic structural fact. A "this secondary button reads too heavy" correction is `behavioral` and never promotable, because it is a taste read a human has to weigh, and auto-enforcing it would collapse the boundary.

## Common misreads

- *"Any recurring correction can be promoted."* No. Only factual ones. A behavioral correction stays a reminder however often it recurs.
- *"Adding a foundation means copying the corpus in."* No. Reference it in place; byte-copying is the trap named in module 2.3.
- *"The agent curates the registry."* No. An agent proposes a pattern; a human decides what enters and what promotes.
- *"Adding an eval case sets a threshold."* No. It adds a known-bad and expected pair. Which score gates a merge is authored client judgment, not shipped.

## Self-check

1. What does deepening a foundation involve, and what judgment stays human in it?
2. What may a factual correction do that a behavioral one may not, and why?
3. How does a new eval case enter the system without setting a gate?
4. From the Lab: your two correction sketches, and the promotability call for each.

## Go deeper

- `sheerline/os/foundations/registry.yaml`: the 13-area map, with coverage and phase per area.
- `sheerline/os/corrections/LIFECYCLE.md`: statuses, the factual/behavioral boundary, promotion, and the human standard.
- `heyhi-mcp/heyhi_mcp/corrections/schema.yaml`: the design-extension fields a correction carries.
- The factual/behavioral line is Track 3.4; grades-inform-never-gate is 3.3; the don't-automate line is module [0.3](../track-0-orientation/module-0-3.md). The capstone is 4.4.

---

*HeyHi Confidential*
