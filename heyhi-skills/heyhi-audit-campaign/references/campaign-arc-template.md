---
classification: internal
title: Audit Campaign Arc Template
purpose: Template and rules for structuring the campaign plan that governs an audit's multi-session arc. Loaded by heyhi-audit-campaign at Step 3 (Design stage) and Step 6 (Restructure stage).
created: 2026-05-21
loaded_by: heyhi-audit-campaign
canonical_example: plans/plan-ai-services-audit-campaign-2026-05-21.md
---

# Audit Campaign Arc Template

The campaign arc is the plan: how many sessions, what each does, how findings accumulate, what the close looks like. The arc lives in `plans/`, follows the project's planning-artifact convention, and is the document every audit session loads to know where it sits in the larger work.

The canonical worked example is [plans/plan-ai-services-audit-campaign-2026-05-21.md](../../../plans/plan-ai-services-audit-campaign-2026-05-21.md). Read it before producing a new arc.

---

## Skeleton

A campaign plan has eight sections plus frontmatter. Skip any section the campaign genuinely does not need; do not invent sections.

```
Frontmatter (planning-artifact convention)
1. Why this plan exists
2. The items at a glance
3. Campaign structure — workstreams and sessions
4. Session detail
5. Sequencing, cadence, and decisions
6. Risks and how the plan handles them
7. Definition of done (+ deferral paths)
8. Cross-references
```

The order matters. Sections 1–2 establish *why* and *what*. Section 3 establishes *how* (the structure). Section 4 is the bulk — per-session detail. Sections 5–6 establish operational reality (cadence, risk). Section 7 names the finish line. Section 8 links out.

---

## Frontmatter

```yaml
---
title: <Campaign Name> — Audit Campaign Plan
classification: internal
status: ready-to-work  # flips to partial, then executed as sessions land
created: YYYY-MM-DD
author: claude-cowork
type: campaign-plan
sources:
  - <predecessor plan, source-of-truth file, or research artifact that produced this plan>
covers:
  - <N areas / surfaces / topics this campaign audits>
sessions: <N>
workstreams: <N>
linear_issues: []
session_1_status: ready-to-work  # add per-session status fields as the arc lands
session_2_status: pending
# ... through session_N_status
---
```

The per-session status fields are the canonical machine-readable surface for "where is the campaign right now?" Per Q5 (split-schema-canonicalization-drift), `status` is the campaign-level canonical answer; per-session statuses are the granular witnesses. They cannot contradict — if any `session_N_status` is `executed`, campaign `status` must be `partial` or `executed`, not `ready-to-work`.

---

## Section 1: Why this plan exists

One short section (3–8 paragraphs). Names:

- **The trigger.** What surfaced the need for the audit? A retrospective? A drift surfaced in another campaign? A client request? A scaling signal?
- **Why now rather than later.** Two reasons. The first is usually freshness of the signal; the second is downstream impact.
- **Why later rather than now (counter-argument).** Two reasons. The honest negative space — what defers or compresses the campaign would buy. Acknowledging the counter-argument prevents the plan from reading as a foregone conclusion.

The section ends with a statement of how this campaign is sequenced against other work (revenue-facing, blocking, interleavable).

---

## Section 2: The items at a glance

A table that fits on one screen. Each row is one item the campaign covers. Columns:

| ID | Pattern / area / question | Integration target / output | Estimated effort |
|----|--------------------------|------------------------------|------------------|

The ID is short and stable (Q1 / Q2 / Q3 for queued items; N1 / N2 / N3 for new artifacts; DG-1 / DG-2 for dispatch items). The ID is what later sections refer to; pick it once.

**Decision gates** belong in this section. Name each gate (Decision Gate N) with: which session resolves it, what the question is, the plan's recommendation. A campaign with no gates is rare; if the plan has no gates, ask whether the campaign is actually as deterministic as it appears.

---

## Section 3: Campaign structure — workstreams and sessions

A table that names the arc:

| # | Session | Workstream | Scope | Est. | Depends on |
|---|---------|-----------|-------|------|------------|

**Workstreams** separate threads of work that could parallelize. The ai-services campaign used 2 (instrument design, then bucket audits). The workflow-integrations campaign also used 2 (governance updates, then skill design). Most campaigns are 1–3 workstreams.

**Hard order** statements follow the table. Name which sessions are strictly sequential and which can interleave with other work.

**What can be dispatched.** Some campaigns have early sessions that meet dispatch criteria (output is a document, source material exists in the workspace, constraints knowable, no live-action requirement). Name those sessions explicitly. See `dispatch/README.md` for dispatch criteria.

**Cadence.** Loose vs. tight. Most HeyHi audit campaigns are interleavable: one session per week, total arc resolves in two to six weeks.

---

## Section 4: Session detail

The bulk of the plan. One subsection per session, in arc order. Each subsection follows the same six-field shape:

```
### Session N — <Session name>

**Workstream:** <Workstream name>. **Estimate:** <min–max time>. **Depends on:** <prior session>.

**Objective.** <One paragraph naming the session's central deliverable.>

**Scope and method.**
<Numbered list of what the session does, step by step.>

**Output.** <Concrete artifacts: files written, plans updated, ledger entries appended.>

**Exit criteria.** <What "done" looks like. Specific. Testable.>

**Hands forward.** <What the next session inherits. Concrete.>
```

**Required for every session:**

- Exit Gate Flavor B close. The session advances the campaign plan; Flavor B applies (`CLAUDE-SESSION-RULES.md § Exit Gate`).
- A `## Findings Integration` slot that names what changes in the plan during the session. Findings are integrated into the plan, not just flagged.
- A `## Session Integrity` slot that runs the lightweight in-skill check against the integrated plan.

**For instrument-design sessions (typically Session 1):** the output must include the instrument file at its canonical path, the campaign's bucket / area list (the file inventory the audit will work through), and ledger scaffolding.

**For audit-pass sessions (typically Sessions 2 through N-2):** the output must include records for every area the session audits, written to the ledger in the instrument's locked format. Number of areas per session varies; aim for sessions producing 5–15 records.

**For cross-cutting synthesis sessions (typically Session N-2):** the output is a finding catalog that examines records across buckets/areas for cross-cutting drift, contradiction, or pattern. Does not write new area records; produces cross-bucket finding IDs (CBD-N).

**For close-out sessions (typically Sessions N-1 and N):** the output is the synthesis brief (N-1) and the fix specification (N, when applicable). See [`close-out-artifacts.md`](close-out-artifacts.md) for the structures.

---

## Section 5: Sequencing, cadence, and decisions

A compact recap of arc constraints, condensed from Section 3:

- **Hard order.** One sentence per strict dependency.
- **Recommended cadence.** Loose vs. tight, with a calendar window estimate.
- **Decision gates summarized.** A short table mapping each gate to the session that resolves it, the question, and the plan's recommendation.

This section exists because Section 3 may be too dense for a quick "what do I need to know to start" read. Section 5 is the operating-room one-pager.

---

## Section 6: Risks and how the plan handles them

A short risk register. Three to six rows, each with the same shape:

```
**<Risk name>.** <What could go wrong, in one sentence.> Mitigation: <how the plan handles it>. If the risk materializes anyway: <what happens>.
```

Common risk archetypes for audit campaigns:

- **The campaign adds infrastructure when revenue is the priority.** Mitigation: interleavable cadence; nothing in the arc gates revenue work.
- **The instrument is wrong.** Mitigation: the campaign's first session is dedicated to instrument design; remaining sessions use it unchanged unless explicitly amended.
- **A finding type was missed.** Mitigation: the cross-cutting synthesis session (N-2) is the catch.
- **The close-out artifacts sit unread.** Mitigation: propagation pass in the final session updates dependent surfaces; the brief is offerable, not just authored.
- **Scope fatigue.** Mitigation: the arc has an explicit definition of done (Section 7) and named deferral paths.

Do not list risks that have no mitigation. A risk with no plan is a finding, not a risk.

---

## Section 7: Definition of done

The campaign is complete when all of:

1. The ledger has one record per area, each with the instrument's required fields.
2. The rollup state file (if used) is updated with the campaign's results.
3. The synthesis brief is published at its canonical path.
4. The fix specification is published (when applicable).
5. The decision-log entry is appended.
6. Dependent surfaces are updated per `CLAUDE-SESSION-RULES.md § Propagation tier discipline`.
7. The plan's `status` is `executed`, every `session_N_status` is `executed`, and `executed_date` is set.

### Deferral paths

The plan can cleanly pause at any session boundary. Name what each pause point preserves and what it leaves undone:

- **After Session 1 (instrument design only):** The instrument exists; sessions 2+ remain. The campaign is paused; restarting picks up at Session 2.
- **After audit-pass sessions but before synthesis:** The ledger has records but no close-out. The "minimum viable" close: a one-paragraph note in the plan saying the campaign paused with records-in-hand.
- **After synthesis brief but before fix spec:** The synthesis brief stands alone. Fix specification can be authored later if the campaign reopens.
- **After everything:** Campaign closes as a unit. The next natural campaign reuses the instrument or revises it explicitly.

---

## Section 8: Cross-references

Standard closing block:

- Predecessor campaign (if any)
- Source analysis / research / retrospective that produced this plan
- The instrument file
- The ledger file
- The rollup state file
- The close-out artifact paths
- The parent skill: `heyhi-skills/heyhi-audit-campaign/SKILL.md`

---

## Q3 verify-before-claim discipline (applies to writing the arc itself)

When the arc cites a predecessor file, an instrument path, a ledger location, or a downstream surface, verify it before locking the plan. Common verifications:

- Predecessor plan path: `test -f <path>` before referencing.
- Cited file inventory counts: `find <dir> -name '*.md' | wc -l` matches what the plan claims.
- Dependency-graph references: read `ai-services/_core/dependency-graph.json` and confirm cited nodes exist.

A campaign plan that cites a non-existent predecessor or an inflated file count is the kind of soft hallucination Q3 catches at write time.

---

## Quick checklist before declaring an arc done

- [ ] All eight sections present.
- [ ] Frontmatter follows planning-artifact convention (`status`, `created`, `linear_issues`, per-session status fields).
- [ ] Section 2's at-a-glance table fits on one screen.
- [ ] Section 4 has one subsection per session with all six fields filled.
- [ ] At least one decision gate is named (or the absence is justified).
- [ ] Section 6's risks each have a mitigation.
- [ ] Section 7's definition of done is testable, not aspirational.
- [ ] Deferral paths name what each pause point preserves.
- [ ] Q3 verifications run on every cited path.
- [ ] The plan reads cold: a reviewer who was not in the room can determine what session 1 must produce.

---

*HeyHi Internal Use Only. heyhi-skills/heyhi-audit-campaign/references/. Loaded by SKILL.md Step 3 (Design stage) and Step 6 (Restructure stage).*
