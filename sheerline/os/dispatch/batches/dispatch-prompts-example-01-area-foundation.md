---
classification: confidential
title: "Worked example: fill one practice-area foundation and build its first skill"
status: done
example: true
---

# Worked example batch 01: one area, foundation then skill

**A worked example of the dispatch convention, not a real batch.** It shows the shape an instance's own batch files take: a dated (here, numbered) file, waves that run in order, lanes that each OWN a disjoint set of files, and one convergence lane that folds the work together and carries the status flips. Replace `<area>` with a practice-area key from `os/foundations/registry.yaml`.

**Waves.** Wave 1: DISPATCH-01 and DISPATCH-02 run in parallel (disjoint OWNS). Wave 2: DISPATCH-03 runs after both merge, and is the only lane that edits the shared anchors.

---

## DISPATCH-01: Fill the practice-area foundation

**OWNS:** `os/foundations/<area>/FOUNDATION.md` only.

```
─── ENV CHECK (complete before anything else) ────────────────────────────────
Read the instance's root agent guide (the file its operating principles name as
the session entry point). IF it loads: proceed to MISSION. IF any error: STOP and
report "ENV ERROR: cannot read the agent guide." Do not proceed.
──────────────────────────────────────────────────────────────────────────────
```

**MISSION.** Write the governance manifest for `<area>`: what the practice covers, what stays human, which existing corpus documents it references in place, and the skills that will serve it.

**CONTEXT LOAD.** (1) `os/foundations/registry.yaml`: the area's nature, coverage, and build gate. (2) `os/operating-principles.md`: the constraints, the conflict order, the IP boundary. (3) One filled foundation as the shape to match. Before declaring any cited path missing, glob it.

**OUTPUT SPEC.** One file, `os/foundations/<area>/FOUNDATION.md`, with frontmatter and a classification mark.

**CRITICAL CONSTRAINTS.** Foundations reference the corpus in place, never byte-copy it. Grades inform, never gate. The taste boundary holds: judgment calls ship as labeled empty slots. The retained moat is not built here.

**SMOKE TESTS.** Every cited path resolves. No byte-copied corpus. The what-stays-human section names at least one empty slot. Day-0 adversarial re-read, every MISS fixed.

**QUALITY GATE.** The manifest reads as governance, not content; every reference resolves; nothing outside OWNS changed.

---

## DISPATCH-02: Build the area's first skill

**OWNS:** the new skill's folder, staged for review (not deployed).

**MISSION.** Build the one skill the foundation names as the area's first verb, with its eval cases.

**CONTEXT LOAD.** (1) The batch plan's section for this area, the same source DISPATCH-01 writes from (the lanes run in parallel, so never wait on DISPATCH-01's output). (2) `skills/registry/skill-registry.yaml`: neighbouring skills, so the new triggers do not collide. (3) `skills/evals/README.md`: the eval-case shape.

**OUTPUT SPEC.** `SKILL.md` plus `evals/cases.yaml` (four cases: invariant, empty slot, restraint, routing).

**CRITICAL CONSTRAINTS.** The skill proposes and steps back: the human verdict ships empty behind a named gate. No trigger may collide with an existing skill; prove it with the router.

**SMOKE TESTS.** The router returns the new skill for its own trigger phrases and not for its neighbours'. All four eval cases are present. Day-0 re-read.

**QUALITY GATE.** Staged, reviewable, collision-free, with evals.

---

## DISPATCH-03: Convergence

**OWNS:** the shared anchors: the subset registry, `os/foundations/registry.yaml` coverage, `os/project-state.yaml`, `os/decision-log.md`, and this file's `status:`.

**MISSION.** After the human promotes the skill, fold both lanes into the shared anchors, re-derive every count from the files (never trust a lane's number), and flip this batch's status.

**SMOKE TESTS.** `skills/evals/measure_coverage.py` reports the new skill with an eval home. The routing battery passes. The coverage tag moves only if the foundation and the skill both landed.

**QUALITY GATE.** Anchors agree with the tree; status flipped; one decision-log entry.

*HeyHi Confidential*
