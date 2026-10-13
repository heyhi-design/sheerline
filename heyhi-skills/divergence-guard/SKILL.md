---
name: divergence-guard
description: >-
  Read a session's design artifacts for premature convergence and for fidelity
  that has outrun the question, and inform the humans without gating anything.
  Runs the mechanical work: counts the structurally distinct options present
  (on the divergence axes; hifi variants of one structure count as one), reports
  their overlap, offers unordered widening stimulus for the unexplored axes,
  classifies the artifact's fidelity against the stated test question on the
  fidelity ladder, and notes whether a lofi phase is in evidence. Triggers:
  "are we converging too early", "are we converging too early on this design", "is
  this too high fidelity for the question", "is this prototype too high
  fidelity for what we're testing", "do we have enough alternatives", "divergence read",
  "how many structural options do we have". Produces a Divergence Read that
  carries no pass / fail / status / severity / score field, echoes N as context
  and never enforces it, and leaves whether to diverge further and the fidelity
  call EMPTY behind a named human gate. NOT for Audit this prototype / what
  interactions are missing (use heyhi-prototype-audit). NOT for Wireframe /
  draft the skeletons (use flow-and-lofi-author). NOT for Generate the
  alternatives / generate lofi options (use flow-and-lofi-author; this reads
  existing artifacts, that generates). NOT for Workshop: run or facilitate the
  ideation session (use heyhi-workshop). NOT for Audit the opportunity tree /
  prioritization reasoning (use strategy-integrity-warden). NOT for Visual
  exploration boards / visual direction options (area 6).
version: "0.1.0"
updated: "2026-09-05"
status: "deployed 2026-09-07 — heyhi-skills/divergence-guard/ (buildable-now, internal-first, self-application-first); registered in the main registry and the Sheerline area-5 subset registry, promoted in the Bucket B convergence third run (staged #788, cleared by the instance owner 2026-09-07). On demand in v1 (spec § 10 D2: no Exit-Gate hook; never a required header). Sheerline area 5 (Wireframing & Prototyping), P3 deepen, build class N; coverage unchanged (area 5 stays covered). Spec: plans/plan-sheerline-p3-prototyping-lofi-2026-09-05.md § 3 / § 5 / § 6 / § 9. Foundation: sheerline/os/foundations/prototyping/FOUNDATION.md."
review_by: "2026-09-19"
classification: HeyHi Confidential
---

# Divergence Guard

**Sheerline area 5 (Wireframing & Prototyping) · P3 deepen · buildable-now, self-application-first · build class N.** The ideation-diversity guard made operable. `sheerline/os/operating-principles.md` § The zero-cost operating invariants states that guard once, and this skill points at it rather than restating it; it runs the three verbs that bullet names, **widen, measure, warn**, on a session's artifacts. It **measures** how many structurally distinct options exist and how much they overlap, **widens** by offering stimulus, and **warns** when fidelity has outrun the question being asked. It renders no verdict and blocks nothing, by construction.

**The boundary this skill obeys (Sheerline, absolute).** A structured artifact with explicit empty judgment slots, a named human gate, and provenance labels on anything inferred. *Whether to diverge further and the fidelity call are the empty slots.* Counting options, naming overlap, listing unexplored axes, and placing an artifact on the ladder are mechanical; deciding that the room has diverged enough, or that this fidelity is right for this question, is the human's. A version of this skill that ranks its stimulus, scores the session, sets a threshold, or can be keyed on by a gate has exceeded its charter.

> **This skill closes through the Exit Gate (`CLAUDE-SESSION-RULES.md § Exit Gate`).** See the bottom-of-skill bracket. Its own read is never an Exit-Gate required header (§ What is explicitly out of scope).

---

## Routing — disambiguation with sibling skills

| If the task is… | Use |
|---|---|
| "Are we converging too early / is this too hi-fi for what we're testing / how many real options do we have" on existing artifacts | **this skill** |
| Generate the alternatives, wireframe, draft the skeletons | `flow-and-lofi-author` (that generates; this reads) |
| Audit a built prototype for interaction completeness or readiness | `heyhi-prototype-audit` (an audit has a system to measure against; this has only the question) |
| Run or facilitate the ideation session itself | `heyhi-workshop` (the room stays human) |
| Audit an opportunity tree or prioritization artifact's reasoning | `strategy-integrity-warden` |
| Divergent visual boards, visual direction options | area 6 (`heyhi-visual-exploration`, candidate): visual divergence is not structural divergence; three visual treatments of one flow are one structural option here |
| Whether to diverge further; the fidelity call | **the human** (this skill's named gate) |

---

## Step 0: Improvement hook check

Retrieve any recurring corrections for convergence / fidelity work (`retrieve_design_corrections`, or the Sheerline `os/corrections/` registry). Fold a match into the pass. None exist yet; skip silently.

## Step 1: Load context

1. **The session's artifacts:** a Lo-fi Pack, a set of prototypes or comps, a brief, a folder. Any fidelity; the guard reads structure, not polish.
2. **The stated purpose / test question.** If absent, the first finding is "no test question stated"; the guard proceeds on the artifacts and asks. It never invents the question.
3. **Mode:** on-demand (the default and the only v1 mode). Same output either way.
4. `sheerline/os/foundations/prototyping/FOUNDATION.md` — the area-5 governed context. Register under it; do not author it.
5. `references/fidelity-ladder.md` — the question-class → sufficient-fidelity ladder. THE method spine for the warn verb. The divergence axes it compares on are **authored once** in `heyhi-skills/flow-and-lofi-author/references/lofi-method.md` § 2 (at staging: `skill-updates/flow-and-lofi-author/references/lofi-method.md`) and pointed at, never copied.
6. `references/worked-example.md` — a filled Divergence Read on invented artifacts. Calibration only.
7. The engagement-intake resolution (`sheerline/profile/engagement-intake.yaml`), when one exists: `deliverable.root`, `hermetic_seal_confirmed`, `brand_voice_source` for the prose register. Absent a profile, the instance's own defaults.

## Step 2: Read, mechanically

Each step is mechanical. None of it decides whether to diverge, ranks a stimulus, or calls the fidelity right.

1. **Convergence read (measure).** Count the structurally distinct options in the artifacts, comparing on the divergence axes. Report the count and the shared-axis overlap between options. **One option** is reported as "1 structural option present," never as a failure. Multiple hi-fi variants of one structure (three color treatments of one flow) count as **one** structural option, with the visual-vs-structural distinction named. N, if the human stated one, is echoed as context and never enforced.
2. **Widening stimulus (widen).** For each unexplored axis value, one short prompt of the form "an alternative that starts from X / decomposes by Y / discloses Z on demand." Each labeled `[stimulus — not a recommendation]`. The list is **unordered**: no ranking, no preference words, no "best." The guard never drafts the alternative (that is `flow-and-lofi-author`'s, on the human's request).
3. **Fidelity-vs-question flag (warn).** Classify the stated question against the fidelity ladder and the artifact's fidelity as read (lo-fi · mid · hi-fi visual · hi-fi coded; the classification is `[inferred]`). Where the artifact sits above the rung the question needs, say so **in prose** and name what the extra fidelity costs (time, attachment, reviewers reacting to color instead of structure). Where it sits below, say that too. Where no question was stated, the flag is that fidelity cannot be right-sized to an unstated question.
4. **Skipped-phase note.** If the artifacts are hi-fi and no lo-fi or flow artifact is visible in the session, note in one prose sentence that the operating principle's lo-fi phase is not in evidence. A note, never a block.
5. **Self-report.** State the read's limits: it counted structure from what it could see; hidden alternatives (a sketchbook, the room's reasons) are invisible to it.

## Step 3: Produce the Divergence Read

Output this exact structure. There is no `pass`, `fail`, `status`, `severity`, or `score` key anywhere in it; the fidelity reading and the phase note are prose sentences on purpose, so no enumerated value exists for a gate to match.

```
# Divergence Read — [session / artifact set]
Read: [date]     Mode: on-demand     Test question: [as stated | NOT STATED]
This read informs; it gates nothing. It carries no verdict, score, threshold, or blocking field.

## Structural options present
Count: [k]   (N requested, if any: [n] — echoed as context, not enforced)
| Option | Where | axes: nav · decomposition · hierarchy · entry · disclosure · input |
|--------|-------|---------------------------------------------------------------------|
Overlap: [pairs and the axes they share]. Hi-fi variants of one structure counted as one: [note].

## Widening stimulus  [stimulus — not recommendations; unordered]
- an alternative that starts from … (entry axis unexplored)
- an alternative that decomposes by … (decomposition axis unexplored)

## Fidelity vs the question
Artifact fidelity as read: [lo-fi | mid | hi-fi visual | hi-fi coded]  [inferred — the guard classified it]
Sufficient for the stated question class: [rung, per the ladder]
[One or two sentences, in prose: where the artifact sits relative to that rung and what the
 gap costs, or that the fidelity cannot be right-sized because no question was stated.
 Prose on purpose: there is no enumerated value here for a gate to match.]

## The lo-fi phase, as far as this read can see
[One sentence, in prose: what lo-fi or flow artifact is present in the session, or that none
 is visible here. A note, never a block.]

## What this read cannot see
[hidden alternatives, unshared sketches, the room's reasons]

## ⛔ Whether to diverge further — NEEDS HUMAN   ____________
## ⛔ The fidelity call — NEEDS HUMAN            ____________

## Named gate
Design lead / owner of the diverge and fidelity calls: ____________   Date: ______
This read informs those two calls; it records neither until this line is signed by a human.
```

**The read is done when** the count and overlap are stated (with hi-fi variants of one structure collapsed and named), the stimulus is unordered and labeled, the fidelity reading and the phase note are prose sentences, the read's limits are stated, and both ⛔ slots and the gate are blank.

## Step 4: Pre-flight verification

Confirm: no `pass` / `fail` / `status` / `severity` / `score` key exists anywhere in the Read; N is echoed, never compared against the count as a threshold; the stimulus carries no ordering, ranking, or preference word; the fidelity reading and the phase note are prose, not enumerated values; hi-fi variants of one structure were counted as one and the distinction named; the artifact-fidelity classification is tagged `[inferred]`; both ⛔ slots and the gate are empty; the read's limits are stated; no client name appears when `hermetic_seal_confirmed` is true.

---

## What is explicitly out of scope

- **Whether to diverge further, and the fidelity call.** Empty by construction. "Should we explore more options?" returns the count, the stimulus, and the ⛔ slot, never a yes or no.
- **Generating the alternatives.** `flow-and-lofi-author`, on the human's request. The stimulus names an unexplored axis; it does not draft the option.
- **Any verdict, score, threshold, or blocking path.** The Read has no such field, and nothing inside this skill can produce one. **No skill, hook, Exit-Gate header, or CI job may key on the Read.** If a script ever wraps it, a *completed* read exits 0 regardless of what it found; a usage or input failure exits non-zero and is reported as "did not run," never as a reading. Its Exit-Gate presence, if ever adopted (spec § 10 D2, not in v1), is an informational line under an existing header, never a required header: an empty required header is a visible failure by design, and this guard must not be able to produce one.
- **Facilitating the room.** `heyhi-workshop`; the room stays human.
- **Visual divergence.** Area 6. Three color treatments of one flow are one structural option here.
- **Auditing a built prototype.** `heyhi-prototype-audit`.

---

## Exit Gate Required Headers (bottom-of-skill bracket)

This skill closes through Exit Gate Flavor A (`CLAUDE-SESSION-RULES.md § Exit Gate`). Before declaring done, confirm every required header holds real content:

- `## Fixes Applied` (or the delivered Divergence Read)
- `## Smoke Test` (the Step 4 pre-flight checks, pasted)
- `## Next Session Prompt`

If either ⛔ slot is filled, a verdict or score field exists, N is enforced, or the stimulus is ordered, the gate has **not** been satisfied.

---

*HeyHi Confidential. Sheerline area 5 (Wireframing & Prototyping), P3 deepen, build class N. Staged 2026-09-05 (v0.1.0) in `skill-updates/`, registry-inert until the Bucket B convergence pass promotes it. Spec source: `plans/plan-sheerline-p3-prototyping-lofi-2026-09-05.md` § 3 / § 5 / § 6 / § 9. Foundation: `sheerline/os/foundations/prototyping/FOUNDATION.md`. Boundary: `sheerline/os/operating-principles.md` (the ideation-diversity guard, pointed at). The advisory-never-gate construction follows `heyhi-drift-repair`'s `detection`-not-`severity` precedent.*
