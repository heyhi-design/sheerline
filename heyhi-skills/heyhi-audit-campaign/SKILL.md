---
name: heyhi-audit-campaign
description: >-
  Runs a HeyHi audit campaign end-to-end: designing the instrument that produces
  consistent findings across N sessions, structuring the multi-session arc, executing
  per-session audit passes, and emitting the synthesis brief plus fix specification
  that close the campaign as a unit. Use when the user says "design an audit campaign for
  [topic]," "structure a multi-session audit," "we need to audit [bucket / area / system]
  across N sessions," "draft the audit instrument," "build the campaign arc," "what's
  the close-out artifact for this audit," "write the synthesis brief for [campaign],"
  or "fix specification from [campaign]." Also use when an existing campaign needs a
  mid-stream restructure (sessions are diverging from the instrument, a finding type was
  missed, the arc is producing inconsistent shapes). Justified only for diagnostic
  multi-session arcs of three or more sessions. NOT for single-session design system
  audits (use heyhi-design-intelligence-audit), single-session prototype audits
  (heyhi-prototype-audit), status reports, workshops (heyhi-workshop), or generic
  non-audit multi-session work.
version: "1.0.2"
updated: "2026-10-13"
status: deployed
changes: "v1.0.2 (2026-10-13): Generalized for the Sheerline scaffold: instance data (brand defaults, client/engagement history, owner names, ratified values) moved to instance-only files or neutral wording; method unchanged. v0.1.0 (Session 3, skill-updates): Initial build per heyhi-skills/skill-specs/heyhi-audit-campaign-spec.md. Seven-step structure (Step 0 Determine stage / Step 1 Intake / Step 2 Design instrument / Step 3 Design arc / Step 4 Run session / Step 5 Produce close-out / Step 6 Restructure mid-stream). Four supporting references. Three Session-3 open questions resolved per spec recommendations. v1.0.0 (Session 4, promoted to heyhi-skills/): relative paths updated for new location; status flipped to deployed; footer updated. No content changes. v1.0.1 (integrity follow-up, 2026-05-21): description corrected from 'Six-step' to 'Seven-step' to match actual Step 0–6 structure; Q1 propagation gaps from Session 4 closed across CLAUDE.md / README.md / infrastructure-overview.md / project-state.yaml IP-B3 scope."
---

# HeyHi Audit Campaign

*The skill that turns a sprawling audit into one coherent picture.*

This skill runs a HeyHi audit campaign — a multi-session diagnostic that decomposes a subject into auditable areas, applies a consistent instrument across sessions, accumulates findings in a shared ledger, and closes with a synthesis brief that lets one reader open one document and see where things stand.

The skill exists because the ai-services Audit Campaign (11 sessions, May 2026) proved that two patterns are coupled: instrument design (how findings get produced) and campaign arc design (how findings accumulate into a coherent close). Splitting them risks an instrument that does not fit a campaign or a campaign with no instrument. The combined skill is the structural form.

This is not generic project management. The skill's scope is *diagnostic* multi-session arcs that produce findings and close in synthesis. Build campaigns, workshop series, content-production sprints, and other multi-session work do not qualify.

For the canonical worked examples this skill draws from, see the references below. For the close-out artifact structure, see [heyhi-skills/heyhi-voice/references/synthesis-brief-structure.md](../heyhi-voice/references/synthesis-brief-structure.md).

---

> **Exit Gate (Flavor B).** This skill closes through the canonical Exit Gate — see `CLAUDE-SESSION-RULES.md § Exit Gate`. Required headers, in order: `## Findings Integration`, `## Session Integrity`, `## Fixes Applied`, `## Smoke Test`, `## Next Session Prompt`. Flavor B applies because every session of an audit campaign reads, writes, or advances a planning artifact. Empty headers are visible failures.

---

## When to Trigger

Run this skill when:

- The user says: *"design an audit campaign for [topic]," "structure a multi-session audit," "we need to audit [X] across N sessions," "draft the audit instrument," "build the campaign arc," "what's the close-out artifact for this audit," "write the synthesis brief for [campaign]," "fix specification from [campaign]."*
- An existing campaign needs a mid-stream restructure: a session is over-running, a finding type was missed, the arc is producing inconsistent shapes session-to-session.
- A capability area, design system at scale, evaluation rollout, or any subject would benefit from a structured diagnostic that produces comparable findings across sessions.

**Not for:**
- Single-session design system audits → `heyhi-design-intelligence-audit`.
- Single-session prototype audits → `heyhi-prototype-audit`.
- Status reports or mid-stream updates → `atlassian:generate-status-report`, or write directly.
- Workshop facilitation (live human interaction) → `heyhi-workshop`.
- Generic multi-session work that is not diagnostic → use the plan template at `plans/README.md`.

The three-session threshold is a hard floor. Two-session audits are not campaigns; they are pair-runs of a single-session audit skill.

---

## How References Load

This skill follows the Earn the Room principle: references load on demand per stage, not all at once. The four references and when each loads:

| Reference | Loads at | Purpose |
|---|---|---|
| [`references/instrument-design-template.md`](references/instrument-design-template.md) | Step 2 (Design stage), Step 6 (Restructure stage) | Skeleton for the instrument itself: area schema, per-unit fields, rubric, finding-type codes |
| [`references/campaign-arc-template.md`](references/campaign-arc-template.md) | Step 3 (Design stage), Step 6 (Restructure stage) | Skeleton for the campaign plan: session count, session detail, ledger pointer, definition of done |
| [`references/rubric-library.md`](references/rubric-library.md) | Step 2 (Design stage), Step 4 (Run stage) | Reusable rubrics: 5-rung maturity ladder, 8-value status taxonomy, finding-type codes (DF/CBD/PL/DG), follow-on artifact taxonomy (A/B/C) |
| [`references/close-out-artifacts.md`](references/close-out-artifacts.md) | Step 5 (Close stage) | Wrapper that points at the synthesis-brief structure (in heyhi-voice) and adds the fix-specification template |

Do not pre-load. The Intake step (Step 1) determines which stage applies; the stage's references load then.

---

## Execution Instructions

### Step 0: Determine Campaign Stage

The skill operates in four stages. The user names the stage; if unclear, ask one question.

- **Design stage.** No campaign exists yet. The session designs the instrument, the arc, and the close-out artifact templates. Output: a campaign plan in `plans/`, an instrument file, ledger scaffolding.
- **Run stage.** A campaign exists; the current session is one of the N audit sessions. The session loads the instrument and executes its audit pass against assigned areas, writing records to the ledger.
- **Close stage.** All audit sessions are complete. The session produces the synthesis brief and (when applicable) the fix specification, per the structure in `heyhi-skills/heyhi-voice/references/synthesis-brief-structure.md`.
- **Restructure stage.** A campaign is mid-stream and drifting. The session audits the campaign-so-far against the instrument, names the drift, and produces a revised arc for remaining sessions.

If unclear, the disambiguating question is one of:

- "Do we have an instrument and a plan, or are we designing them this session?"
- "Is this an audit session, or are we closing the campaign?"

---

### Step 1: Intake (always runs)

Collect these before doing any stage-specific work. Ask as a single set, not one at a time.

**Subject context**
- What is being audited? Name the subject as one phrase (e.g., "ai-services capability state," "client X's design system at scale," "the evaluation framework's coverage of deployed agents").
- What is the user's central question? (The campaign's close-out artifact will answer this.)
- Is there a predecessor audit, related diagnostic, or earlier finding catalog?

**Source context**
- Where does the truth-of-the-thing live? Files, ledgers, schemas, repos, Figma files, documentation, databases.
- What is the source's read pattern? Single folder, multiple folders, version-controlled, live database?
- Are there files exceeding 1,500 lines that the audit will need to scan? (Per Q4: those get programmatic extraction, not linear reads.)

**Output context**
- What does the close-out artifact look like? Synthesis brief, fix specification, both, something else?
- Who reads the close-out? Internal owner-only, design team, client, executive, all?
- Does the audit need to produce a decision-log entry?

**Scope context**
- Session count target. (Hard floor: 3. Typical range: 5–12.)
- Calendar window. (Tight: 1–2 weeks. Loose: interleaved over months.)
- Reviewer availability for instrument approval and close-out artifact review.
- Dependencies on parallel work that could change the subject mid-audit.

If the intake reveals the subject is single-area (audit-able in one session), redirect to `heyhi-design-intelligence-audit`, `heyhi-prototype-audit`, or a direct audit pass. Do not run a three-session campaign for a one-session subject.

---

### Step 2: Design the Instrument (Design stage)

Load [`references/instrument-design-template.md`](references/instrument-design-template.md).

**Objective.** Produce an audit instrument that defines how the audit is performed, what counts as evidence, and what record each area produces. The worked example is [ai-services/_core/audit-instrument.md](../../ai-services/_core/audit-instrument.md).

**The instrument defines:**

- **Unit of audit (the "area").** How the subject is decomposed into audited units. Areas must be nameable in one short phrase, must share purpose (not just folder), and may span subfolders. The template's §1 covers area construction rules.
- **Maturity ladder.** A small-N ladder (canonical: 5 rungs — Researched, Specified, Built, Evaluated, Deployed). Each rung has stated evidence requirements; no rung is granted on assertion. The template's §2 covers the canonical ladder; alternative ladders are documented in `references/rubric-library.md`.
- **Status taxonomy.** The canonical 8-value taxonomy (`backlog`, `in-progress`, `in-review`, `blocked`, `ready-to-work`, `done`, `superseded`, `archived`). Reuse, do not invent. The rubric library names the source: the Studio Graph work.
- **Per-area record format.** Locked schema for what every audit pass writes. Template §4 holds the canonical YAML record. **Q5 compliance required:** any field that splits a logical concept into multiple parts (e.g., `maturity_rung` + `evidence`) must declare which is canonical and what the other adds. The `evidence` field is non-optional and prose; the `maturity_rung` is canonical state.
- **Finding-type codes.** The codes the audit uses to refer to findings cross-session: `DF-N` (downstream finding), `CBD-N` (cross-bucket drift), `PL-N` (plan/follow-on), `DG-N` (dispatch). The rubric library covers their definitions.
- **Follow-on artifact taxonomy.** Type A (dispatch — pure documentation drift), Type B (plan — capability/state disagreement), Type C (research — knowledge gap). Verified against `ai-services/_core/audit-instrument.md:163-166`. Every contradiction or finding the audit surfaces becomes a typed follow-on, not silently fixed.
- **Required output framing.** The audit answers the user's central question (Step 1 intake). The canonical framing for capability audits is *Finished / In Progress / Left to Do*; other framings (Risks / Gaps / Strengths; Compliant / Out of Compliance / Unknown) are valid when the central question demands them.

**Output.** A new file at `[subject-area]/audit-instrument.md` (e.g., for a client engagement, `audit-instrument.md` in the instance's engagement folder for that client; for internal audits, the path the subject's source files already live in). The file is the instrument; subsequent sessions load it unchanged.

**Exit criteria.** The instrument's per-area record format passes a smoke test: take a sample of three areas from the subject (the first three from the file inventory), draft a record for each by hand using the instrument, and confirm the records are well-formed under the schema. If any draft trips on a missing field or ambiguous rubric value, the instrument is not done.

**Q3 verify-before-claim discipline:** if the instrument cites a field name from an existing schema (e.g., reusing the ai-services `area_id` shape), verify the cited field exists in the cited source with `grep` before locking the instrument. The Session 2 self-caught defect (claiming `rung` when the canonical field is `maturity_rung`) is the failure mode this discipline prevents.

---

### Step 3: Design the Campaign Arc (Design stage)

Load [`references/campaign-arc-template.md`](references/campaign-arc-template.md).

**Objective.** Produce the campaign plan: session count, per-session scope, ledger format, close-out artifacts, definition of done. The worked example is [plans/plan-ai-services-audit-campaign-2026-05-21.md](../../plans/plan-ai-services-audit-campaign-2026-05-21.md).

**The arc defines:**

- **Session count and shape.** For capability audits, the canonical shape is *1 instrument-design session + N bucket/area audit sessions + 1 cross-cutting synthesis session + 1 readiness brief + 1 fix specification*. For design system audits at scale, the canonical shape adjusts to match the subject's natural decomposition (typically *1 instrument + 1 session per major surface + 1 close*). The template covers shape selection.
- **Session detail.** Each session entry names: objective, scope, method, output, exit criteria, hand-forward. The Exit Gate close (Flavor B) is required for every session because every session advances the campaign plan.
- **Cross-session ledger.** One canonical file where every session writes its findings. YAML is the default format (matches the `capability-audit-ledger.yaml` worked example); alternative formats (Markdown, SQL, JSON) are documented in the campaign-arc template as a fallback option when source material is in a non-YAML shape (e.g., an audit that pulls from a database).
- **Close-out artifacts.** The synthesis brief is the canonical close-out artifact; the fix specification is added when the audit surfaces a structural failure pattern that requires repair beyond per-finding follow-ons. The structures live in `references/close-out-artifacts.md` and in `heyhi-skills/heyhi-voice/references/synthesis-brief-structure.md`.
- **Decision-log entry plan.** A single consolidated entry at campaign close, covering all sessions. Per the project rule that the decision log is append-only and entries are scoped by decision, not by session.
- **Definition of done.** Concrete: ledger populated with one record per area; rollup written to the appropriate state file; synthesis brief published; fix spec published (when applicable); decision-log entry appended; dependent surfaces updated.
- **Deferral paths.** Where the campaign can cleanly pause if capacity changes. The plan-workflow-integrations-campaign demonstrates this with per-session pause points.

**Output.** A new plan file at `plans/plan-[campaign-name]-YYYY-MM-DD.md`. Frontmatter follows the canonical planning-artifact convention (`status:`, `created:`, `linear_issues:`, etc.) defined in `CLAUDE-SESSION-RULES.md § Planning Artifact Convention`.

**Exit criteria.** The plan answers all of: how many sessions, what each does, what the close looks like, what counts as done. A reviewer should be able to read the plan cold and know what session 1 must produce.

---

### Step 4: Run a Session (Run stage)

Load [`references/rubric-library.md`](references/rubric-library.md). Also load the instrument file from Step 2.

**For each session in the arc:**

1. **Phase 0 — Identify the session's audit footprint.** Determine which areas this session audits per the campaign arc. For sessions in a large subject (1,000+ files), use programmatic extraction (Q4): `find`, `grep`, or directory traversal to enumerate, not linear reads.
2. **Phase 1 — Area definition (first 15 minutes).** Cluster the session's files into areas per the instrument. Aim for 4–10 files per area; adjust by judgment. Write names down before opening files in depth.
3. **Phase 2 — Per-area audit pass.** For each area:
   - Read the area's files. All of them, at least to skim. For files exceeding 1,500 lines: programmatic extraction (`grep -n`, `git diff HEAD --`, `sed -n`).
   - Determine the maturity rung. Demand evidence for every rung claim. *No rung without evidence* is the instrument's foundational rule.
   - Determine the status from the 8-value taxonomy.
   - Check the status–rung consistency rule. A `done`-flagged area at rung `built` (3) is a finding, not a valid record.
   - Identify blockers. One per line.
   - Identify downstream dependents. Cite by `area_id` or file path.
   - Write the record. Append to the campaign ledger under the bucket/area section.
4. **Phase 3 — Cross-session check.** Read the prior sessions' ledger entries. Flag any new finding that contradicts a prior record (CBD-N) or that surfaces a downstream surface lagging the ledger (DF-N). These become follow-on artifacts per the rubric library.
5. **Phase 4 — Rollup write.** If the campaign uses a rollup state file (e.g., `project-state.yaml capability_readiness`), write or update the session's bucket in the rollup.
6. **Phase 5 — Follow-on artifact log.** Append any typed follow-ons (A/B/C) to the ledger's `follow_on_artifacts` section.
7. **Phase 6 — Exit Gate Flavor B close.** Required headers: `## Findings Integration`, `## Session Integrity`, `## Fixes Applied`, `## Smoke Test`, `## Next Session Prompt`. The campaign plan's `session_N_status` frontmatter field flips `ready-to-work → executed` (or `partial` if work remains).

**Q3 verify-before-claim discipline applies through every phase.** Every claim in the session's findings must either name the verification command (or file path consulted) or be marked `[judgment]`. Verifiable claims include rung assignments, status assignments, blocker identifications, downstream-dependent claims, and cross-session contradictions.

**Resist the urge to fix mid-audit.** The audit produces records. It does not reconcile, repair, or finish half-built areas. Reconciliation is downstream work (Step 5 close-out or per-finding follow-on artifacts). Resisting the fix-mid-audit pull is the campaign's foundational discipline.

---

### Step 5: Produce the Close-Out Artifacts (Close stage)

Load [`references/close-out-artifacts.md`](references/close-out-artifacts.md) and [`heyhi-skills/heyhi-voice/references/synthesis-brief-structure.md`](../heyhi-voice/references/synthesis-brief-structure.md).

**Synthesis brief.** Apply the three-level structure (headline / per-layer detail / cited evidence) from the synthesis-brief reference.

- Headline: counts and the verdict on the campaign's central question (from Step 1 intake).
- Per-layer detail: tables decomposing the headline along the natural categories of the subject. For capability audits: layers (Consult / Build / Sustain / Products / Workshops). For design system audits at scale: surfaces (tokens / components / documentation / governance / Figma).
- Cited evidence: every claim grounded in a ledger row, finding ID, or downstream surface.

The worked example is [ai-services/_core/service-readiness-brief-2026-05-21.md](../../ai-services/_core/service-readiness-brief-2026-05-21.md).

**Fix specification (when applicable).** When the audit surfaced a structural failure pattern (not just per-area gaps), produce a fix spec following the four-part shape (what / where / why / how verified / scope discipline per part).

The fix spec is justified when:

- A pattern recurs across multiple areas in the audit (not just one).
- The pattern points to a structural mechanism, not a per-area gap (the integrity-mechanism in the ai-services campaign; the synthesis-vs-bucket drift in Session 9).
- A repair beyond per-finding follow-ons is needed (the fix changes a tool, a skill, a rule, or a schema, not a single file).

If the audit surfaced only per-area gaps and no structural pattern, the synthesis brief alone is the close-out. The fix spec is not produced for completeness; it is produced when the campaign's evidence demands one.

The worked example is [ai-services/_core/integrity-mechanism-fix-spec-2026-05-21.md](../../ai-services/_core/integrity-mechanism-fix-spec-2026-05-21.md).

**Decision-log entry.** Append one consolidated entry to `ai-services/_core/decision-log.md` covering the campaign as a unit. The entry names the campaign, the close-out artifact paths, the structural findings, and any decisions issued by the close.

**Propagation pass.** Update dependent surfaces per `CLAUDE-SESSION-RULES.md § Propagation tier discipline`. Tier 1 (in-task): index documents that should now reference the close-out artifacts. Tier 2 (session integrity): stale references in surfaces that paraphrase the audit's findings. Surfaces typically updated for capability audits: `synthesis.md`, `ai-service-offerings.md`, `productized-services.md`, `competitive-brief.md`, `project-state.yaml capability_readiness`.

**Exit Gate Flavor B close.** Plan status flips from `ready-to-work` or `partial` to `executed`. The campaign's `executed_date` is set.

---

### Step 6: Restructure Mid-Stream (Restructure stage)

**When to invoke.** A campaign in flight is producing inconsistent shapes, an instrument gap is creating ambiguous records, the per-session scope is over- or under-running, or a finding type was missed and needs to be added. The earlier this is caught, the less rework compounds (per `CLAUDE-SESSION-RULES.md § Mid-session replanning`).

**Procedure:**

1. **Load the instrument and the sessions-so-far ledger.** Use programmatic extraction if either exceeds 1,500 lines.
2. **Audit the ledger against the instrument.** Three checks:
   - **Field completeness.** Do all records have the required fields? Missing required fields are instrument-application failures.
   - **Vocabulary compliance.** Are all values within the rubric's vocabulary? Out-of-rubric values are either a rubric gap (the instrument needs a new term) or a session-side error (the auditor used non-canonical terms).
   - **Cross-session consistency.** Are cross-references consistent? Do `area_id` values referenced across records resolve to actual records? Are the same areas appearing under different IDs?
3. **Name the drift.** Use one of three named patterns:
   - **Instrument gap.** The instrument lacks a field, rung, or finding-type code the audit needs. Propose an amendment. Per the audit-instrument's §9, amendments are not adopted mid-campaign without explicit versioning.
   - **Arc miscalibration.** Sessions are too large or too small. The session count needs to grow or shrink. The remaining arc is revised.
   - **Inconsistency.** Different sessions applied the rubric differently. Reconcile by surfacing the inconsistency as a Phase 1 finding for the next session, not by silently rewriting prior records.
4. **Produce a revised arc.** Update the campaign plan with the new session count, revised scopes, and any amendment-to-instrument notes. Frontmatter status remains `partial`; per-session statuses are updated.
5. **Re-validate prior entries against any instrument amendments.** If the instrument gained a new required field, prior records become subject to a backfill pass — recorded as a Type B follow-on plan.
6. **Exit Gate Flavor B close.** The plan's `## Findings Integration` slot lists every section of the plan that changed.

**Restraint.** Restructure is not redesign. The instrument changes only by explicit amendment (Section 9 of the audit-instrument template). The campaign arc changes only by reasoned response to drift, not by preference. A restructure session that produces a totally new campaign is a sign the original instrument was wrong; surface that as a finding and consider whether to close the current campaign and start a new one.

---

## Skill Diary

This skill maintains a memory diary wing (through the `memory` shim): `heyhi-audit-campaign-diary`. The diary captures: audit-instrument calibration patterns that surface across campaigns; cross-bucket drift archetypes; session-cadence learnings; close-out artifact phrasings that survived client review.

**Read trigger:** At session start, before beginning any campaign work, query both wing name forms:

```
memory_search(query="[campaign type, subject area, or instrument gap relevant to the task]", wing="heyhi-audit-campaign-diary")
memory_search(query="[campaign type, subject area, or instrument gap relevant to the task]", wing="wing_heyhi-audit-campaign-diary")
```

*Note: The memory shim's `memory_diary_write` creates wings with a `wing_` prefix; `memory_write` uses the unprefixed form. Both must be queried to ensure complete retrieval.*

**Write trigger:** At the end of any session where a correction is issued or a pattern is noticed while running this skill, draft a diary entry and stage it at `.auto-memory/diary-staging/heyhi-audit-campaign-[YYYY-MM-DD].md` for the instance owner's review before committing.

**Entry format:**
```
skill: heyhi-audit-campaign
pattern_type: correction | preference | recurring-issue | instrument-calibration
observed_in_session: YYYY-MM-DD
valid_from: YYYY-MM-DD
entry: [body — what happened, what the correct behavior is, why it matters]
```

Entries older than 90 days without a `valid_to` are flagged during session integrity.

---

## Composition with other skills

**Always co-loads:**
- The instance's voice skill (in HeyHi, `heyhi-voice`) — the close-out artifacts (synthesis brief, fix specification) pass through its Pre-Output Gate.

**Composes with:**
- `heyhi-session-integrity` — each session's Exit Gate Flavor B close-out runs through session integrity. Steps 4 (Run session) and 6 (Restructure) explicitly close through Flavor B.
- `heyhi-design-intelligence-audit` and `heyhi-prototype-audit` — when a campaign session is itself a single-system audit (e.g., a multi-client design-system audit where each session audits one client), this skill invokes them as inner subroutines. The instrument records reference the inner skill's output.
- `heyhi-research-evaluator` — Design stage may use the research evaluator's scoring when ranking which areas the campaign should audit first.

**Does not compose with:**
- `ui-studio` family — different surface area entirely.
- `heyhi-shopify-theme` family — theme generation, not diagnostic.
- `heyhi-workshop` — workshops are live human interactions; this skill is artifact-producing.

---

## References

| File | Loads at | Purpose |
|---|---|---|
| [references/instrument-design-template.md](references/instrument-design-template.md) | Step 2, Step 6 | Skeleton for the audit instrument: area schema, per-unit fields, rubric, finding-type codes, evidence standard |
| [references/campaign-arc-template.md](references/campaign-arc-template.md) | Step 3, Step 6 | Skeleton for the campaign plan: session count, per-session detail, ledger pointer, close-out artifacts, definition of done |
| [references/rubric-library.md](references/rubric-library.md) | Step 2, Step 4 | Reusable rubrics: 5-rung maturity ladder, 8-value status taxonomy, finding-type codes (DF/CBD/PL/DG), follow-on artifact taxonomy (A/B/C) |
| [references/close-out-artifacts.md](references/close-out-artifacts.md) | Step 5 | Wrapper that points at the synthesis-brief structure (in heyhi-voice) and adds the fix-specification template |

**External cross-references:**
- [heyhi-skills/heyhi-voice/references/synthesis-brief-structure.md](../heyhi-voice/references/synthesis-brief-structure.md) — the three-level structure for synthesis briefs. Required for Step 5.
- [ai-services/_core/audit-instrument.md](../../ai-services/_core/audit-instrument.md) — canonical worked example of an audit instrument.
- [ai-services/_core/capability-audit-ledger.yaml](../../ai-services/_core/capability-audit-ledger.yaml) — canonical worked example of a campaign ledger.
- [ai-services/_core/service-readiness-brief-2026-05-21.md](../../ai-services/_core/service-readiness-brief-2026-05-21.md) — canonical worked example of a synthesis brief.
- [ai-services/_core/integrity-mechanism-fix-spec-2026-05-21.md](../../ai-services/_core/integrity-mechanism-fix-spec-2026-05-21.md) — canonical worked example of a fix specification.
- [plans/plan-ai-services-audit-campaign-2026-05-21.md](../../plans/plan-ai-services-audit-campaign-2026-05-21.md) — canonical worked example of a campaign plan.
- `CLAUDE-SESSION-RULES.md § Exit Gate` — session close-out structure (Flavor B).
- `CLAUDE-SESSION-RULES.md § Propagation tier discipline` — what dependent surfaces must update in-task vs at session integrity.
- `OPERATING_PRINCIPLES.md § Structured-Over-Prose on Propagation Surfaces` — all stages produce propagation surfaces; structure first.
- `corrections-registry.yaml § split-schema-canonicalization-drift` — instrument schema design must declare canonical fields.

---

## Exit Gate Required Headers (bottom-of-skill bracket)

This skill closes through the Exit Gate Flavor B (`CLAUDE-SESSION-RULES.md § Exit Gate`). Before declaring done, confirm every required header below contains real content, not a claim:

- `## Findings Integration`
- `## Session Integrity`
- `## Fixes Applied`
- `## Smoke Test`
- `## Next Session Prompt`

If any header is empty or contains advisory prose ("I checked for bugs") instead of a concrete artifact, the gate has not been satisfied. Apply fixes until clean — then emit.

---

*HeyHi Internal Use Only. heyhi-skills/heyhi-audit-campaign/. Built 2026-05-21 in Workflow Integrations Campaign Session 3 (skill-updates/), promoted 2026-05-21 in Session 4. The Workflow Integrations Campaign closed as a unit with this skill's promotion.*
