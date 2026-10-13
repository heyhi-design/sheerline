---
classification: confidential
title: "Reasoning integrity checks — the method spine"
skill: strategy-integrity-warden
loaded_by: "SKILL.md Step 1"
---

# Reasoning integrity checks

The strategy-artifact canon and the six integrity checks, held as reference. On-demand — load when running the warden.

*Internal operational reference (deployed under `heyhi-skills/`): em-dash limit exempt per `OPERATING_PRINCIPLES.md`. Framework provenance stated inline.*

---

## The artifacts this warden audits

- **Opportunity Solution Tree (OST)** — Teresa Torres' structure: a desired **outcome** at the top, branching into **opportunities** (unmet needs / pain points / desires), each branching into **solutions**, each into **experiments/assumption tests**. The tree keeps a team in the problem space before the solution space.
- **JTBD** — Jobs To Be Done. Two lineages, kept distinct: **Ulwick's ODI** (outcome-driven, jobs decomposed into measurable desired outcomes) and **Christensen's** (the job as the progress a person is trying to make, forces of progress). Do not blur them; a JTBD map that mixes the two incoherently is itself a finding.
- **Prioritization sheet** — RICE (Reach × Impact × Confidence ÷ Effort) or a kin. A *read-and-challenge* instrument that structures a conversation, never a truth oracle that ranks for you.

## The six checks

### 1. Canonical restatement

Restate the artifact in its proper shape first. Restructuring is diagnostic: a starved OST (opportunities with nothing under them), a JTBD with jobs but no outcomes, a prioritization with factors but no basis — these become visible only once the artifact is laid out canonically. Every node the warden infers or reshapes to do this is tagged `[agent-restructured — verify]` so the restatement is never mistaken for the team's own authored structure.

### 2. Evidence-linkage-or-assumption-flag

**Every opportunity/need node must either link to evidence or be flagged an assumption.** An unlinked node presented as established fact is the finding.

*The 2026 failure mode this is aimed at:* the dominant OST critique is not that teams draw the tree wrong — it is that they **starve** it, populating opportunities from opinion with no research underneath. So the check is not "is the tree shaped right," it is "does anything actually feed each opportunity." An honestly-flagged assumption is fine (it names what to go learn); an assumption dressed as a finding is not.

### 3. Solutions-dressed-as-opportunities

Detect solutions sitting in the opportunity space. "Add a dashboard," "build a mobile app," "add SSO" are *solutions*; the opportunity is the unmet need each claims to serve ("users can't see status at a glance"). A tree whose opportunity layer is full of solutions has skipped the problem space — the single most common way an OST goes hollow. Flag each; do not rewrite it into a proper opportunity (that is the team's articulation work, and proposing the "real" opportunity would be the warden authoring strategy).

### 4. Evidence staleness

Flag cited evidence that is old enough to be suspect, references a since-changed product or flow, or leans on a source the team has said it no longer trusts. Stale evidence presented as current is a live integrity risk — a 2024 usability finding about a flow rebuilt in 2026 is not support, it is a liability.

**The staleness heuristic band (v0.2.0) — a flag-not-gate.** Calendar age is the *secondary* signal; *what changed* is the primary one. Read in this order:

1. **Does the evidence reference a surface that has since changed?** A rebuilt flow, a redesigned screen, a deprecated feature, a migrated platform, a changed pricing model, an audience shift. If yes → **FLAG regardless of age** (a 2-month-old finding about a flow shipped last week is stale). This is the check that actually matters.
2. **If the referenced surface is unchanged, use the calendar band as a prompt (not a cutoff):**
   - **≲ 6 months** — generally current for digital-product evidence.
   - **~6–18 months** — aging; confirm the referenced surface and audience are unchanged. Usable if they are; FLAG if you cannot confirm.
   - **≳ 18–24 months** — presumptively stale for a fast-moving product surface; FLAG unless the team affirms the underlying behavior/flow is unchanged.
3. **Stable-behavior exception.** Evidence about a durable human behavior (reading patterns, a fundamental navigation habit, a well-established heuristic) can be old and still sound. Age alone does not condemn it; only a change in the thing it describes does. Note the age, hold at PASS, and record the reasoning in near-misses.

The band is a heuristic, not a rule — its whole point is to prompt "verify this still holds," never to auto-reject on a birthday. When it fires, the FLAG says what to re-confirm, it does not delete the evidence.

### 5. Back-solved scores

In a RICE (or similar) sheet, detect scores reverse-engineered to produce a predetermined ranking. Tells: suspiciously round numbers across the board, **confidence set to justify a favorite** (100% confidence on the sponsor's pet), effort conveniently shaved on the preferred item, reach inflated on the same. RICE's honest use is to *surface disagreement* about the inputs; a sheet where every input was tuned to a foregone ranking has inverted the tool. Flag the pattern; do not re-score (re-scoring would be the warden making the prioritization call).

### 6. Outcome-quality (top-node influenceability)

Examined at the tree's root. The standard Torres critique, made structurally checkable: **an OST must be rooted in an outcome the team can actually influence.** Three types the top node can be:

- **Product outcome (PASS).** A user behavior the team's work can move — activation rate, weekly active creators, task-completion rate, adoption of a workflow, frequency of a valuable action. A team can run opportunity discovery against this: "what stops users from activating?" has answers the team can pursue.
- **Lagging business / financial metric (FLAG).** Revenue, ARR, gross margin, churn dollars, LTV. These are *results* the team contributes to but does not control — they lag, they are moved by pricing, sales, market, and a dozen teams at once. An OST rooted here is confused from the top: you cannot run design discovery against "increase revenue," so every opportunity beneath it inherits the gap between what the team can move and what the metric measures.
- **Output / solution masquerading as an outcome (FLAG).** "Ship the redesign," "launch the mobile app," "migrate to the new stack." These are things to *do*, not outcomes to *achieve*; a tree rooted in an output has no outcome at all, and its "opportunities" are really a work-breakdown.

**The warden's move on a FLAG: name the type-mismatch and stop.** State that the top node is a lagging metric (or an output), and why that undermines the tree beneath it. **Do not supply the product outcome that should replace it** — naming "the right outcome" is authoring strategy, the exact overreach warden shape forbids, and it is the team's articulation work (the same discipline as solutions-dressed-as-opportunities in check 3). An open question may *ask* whether a team-owned product outcome exists that ladders up to the business metric; it may not answer it. And this check never touches the *ranking* of the opportunities — it is a type-check on the root, not a judgment on the branches.

---

## Why selection ships empty — and why warden shape is load-bearing

The warden's charter is the *reasoning*, never the *choice*. Which opportunity a team pursues, and what it builds, are strategy decisions that belong to the people accountable for them. The instant the warden ranks the opportunities, scores them, names "the strongest one," or authors the outcome the tree "should" have, it has stopped auditing and started deciding — and a warden that decides is no longer a warden. This is why the skill is specified with the which-opportunity and what-to-build slots empty and a named human gate: the boundary is the whole point of the tool. A merely-plausible ranking (or a merely-plausible replacement outcome) from the warden is *worse* than none, because it launders a machine's guess into the team's strategy under the authority of an "integrity audit."

## The two curiosity surfaces (open questions, near-misses) — why they are not verdicts (v0.2.0)

Both exist to make the report a thinking instrument, and both stay inside § 9 because neither ranks or decides:

- **Open questions for the team** are questions to the artifact's authors — what it does not resolve, what would firm up the reasoning. The special hazard here: a ranking can hide inside a question. "Isn't opportunity 2 the strongest?" is a ranking wearing a question's clothes and is out. "What evidence would distinguish opportunity 2 from opportunity 3?" is a real question and is in. The outcome-quality open question ("is there a product outcome that ladders up to this revenue goal?") is in charter precisely because it asks rather than answers.
- **Near-misses and unchecked territory** are the audit's trace: nodes considered and passed, checks that almost fired (a 20-month-old citation about an unchanged habit, held at PASS), evidence links that are present but unverifiable from the artifact. No verdict, no ranking.

## Provenance discipline for this skill

Any node the warden infers, reshapes, or restates carries `[agent-restructured — verify]`. The canonical restatement is a proposal about what the team's artifact means, not a replacement for it. No synthetic opportunity, outcome, or score is ever presented as the team's own.

*HeyHi Confidential. Reference for `strategy-integrity-warden`. Spec source: `sheerline-skill-buildout-research-2026-08-09.md` § 6.1; outcome-quality check + staleness heuristic band added v0.2.0 per the 2026-08-22 skills audit § 2.4. Extends the `futurecasting` Decision-Register discipline while staying warden-shaped (audit, not generate).*
