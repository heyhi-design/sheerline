---
classification: internal
title: Audit Instrument Design Template
purpose: Template and rules for designing the audit instrument that anchors a HeyHi audit campaign. Loaded by heyhi-audit-campaign at Step 2 (Design stage) and Step 6 (Restructure stage).
created: 2026-05-21
loaded_by: heyhi-audit-campaign
canonical_example: ai-services/_core/audit-instrument.md
---

# Audit Instrument Design Template

The instrument is the document every audit session loads before doing its pass. It defines how the audit is performed, what counts as evidence, and what record each area produces. A consistent instrument is what makes N sessions comparable and lets the results roll up into one picture.

Build the instrument once, in the campaign's first session. Then leave it alone unless explicitly amended (Section 9 below).

The canonical worked example is [ai-services/_core/audit-instrument.md](../../../ai-services/_core/audit-instrument.md). Read it before producing a new instrument; it earned its shape across an 11-session campaign.

---

## Skeleton

An instrument has ten sections. Skip any section the audit genuinely does not need; do not invent sections.

```
1. The unit of audit (the "area")
2. The maturity ladder
3. The status taxonomy
4. The per-area finding record
5. The required output framing (Finished / In Progress / Left to Do, or campaign-specific)
6. The evidence standard
7. Working procedure per session
8. What the audit does not do (negative space)
9. Versioning and amendment
10. Reference cross-links
```

The order matters. Sections 1–4 define the *what* (the record). Sections 5–6 define the *standard* (the rubric and the evidence rule). Section 7 defines the *how* (the procedure). Section 8 defines the *not* (scope discipline). Sections 9–10 are operational (versioning, links).

---

## Section 1: The unit of audit (the "area")

The audit's atomic unit is the **area** — a coherent unit of capability or work, typically a cluster of related files or surfaces that together represent one thing the subject does or knows. Examples from the ai-services campaign:

- "The Layer-0 → token pipeline" — one area spanning roughly a dozen files in `design-intelligence/`.
- "The architecture decision set" — one area spanning 7 ADRs plus `architecture-principles.md`.
- "The Signal Reader capability family" — one area spanning intake, DPA, output spec, validation framework, and signal categories.

Area construction rules (locked):

1. An area must be nameable in one short phrase. If naming requires a paragraph, it is two areas.
2. An area's files must share a purpose, not just a folder. "Everything in `agentic-infrastructure/research/`" is not an area; it is a folder.
3. An area can span subfolders. A capability that lives partly in `_core/` and partly in `agentic-infrastructure/` is one area; the audit notes both file locations.
4. The session's area list is finalized in its first 15 minutes. Adjusting the area list mid-audit is allowed if the structure is genuinely wrong; it is logged as an instrument-calibration note.

Granularity heuristic: 4–10 files per area is the sweet spot. A subject with 100 files and 8 areas is under-decomposed; the same subject with 50 areas is over-decomposed. Use judgment.

---

## Section 2: The maturity ladder

Each area is placed on a small-N ladder. The canonical 5-rung ladder, used by capability audits:

| Rung | Name | What it requires |
|-----:|------|------------------|
| 1 | **Researched** | Research, source material, or exploratory writing exists. Knowledge is captured. |
| 2 | **Specified** | A coherent spec or build plan exists and is internally consistent. The next step is buildable from what is written. |
| 3 | **Built** | An implementation exists. For code: the code runs. For document deliverables: the deliverable is complete and not a draft. For skills: the SKILL.md is deployed. |
| 4 | **Evaluated** | The implementation has passed its trajectory and outcome tests. For non-code areas: validated against acceptance criteria. Named test results, benchmark outputs, or review records exist. |
| 5 | **Deployed / Sellable** | The capability is in active use, or it can be genuinely offered to a client today. Demonstrable end-to-end. |

**An area's rung is the highest one for which evidence exists.** No rung is granted on assertion. The rule is the instrument's foundational mechanism — see §6.

Alternative ladders for non-capability audits:

- **Design system at scale (3 rungs):** Token coverage / Component coverage / Documentation coverage. Each rung has an evidence requirement (token-by-token mapping; Storybook entry counts; named governance docs).
- **Evaluation framework rollout (4 rungs):** Eval defined / Golden set populated / Trajectory tests passing / Outcome tests passing.
- **Compliance audit (2 rungs):** Compliant / Out of compliance. Plus a third *Unknown* category for areas where compliance status could not be determined.

When in doubt, default to the 5-rung capability ladder. It is the most-tested.

The rubric library at [`rubric-library.md`](rubric-library.md) holds the rung-evidence requirements in detail.

---

## Section 3: The status taxonomy

Status and rung are separate dimensions. The rung is a *depth* check (how mature); the status is a *state* check (where the work is in flight). Use the canonical 8-value status taxonomy (origin: the Studio Graph work):

| Status | Meaning |
|--------|---------|
| `backlog` | Identified but not yet started. |
| `in-progress` | Active work underway. |
| `in-review` | Built; awaiting evaluation or sign-off. |
| `blocked` | Cannot advance until an external dependency resolves. |
| `ready-to-work` | Specified and unblocked; awaiting an executor or session slot. |
| `done` | Complete. For the audit, "done" requires the rung to be `evaluated` (4) or `deployed` (5). |
| `superseded` | Replaced by something newer. Excluded from "active" rollups. |
| `archived` | Intentionally retired. Excluded from "active" rollups. |

**Reuse, do not invent.** Status-word drift is itself a logged failure mode. New campaigns should not introduce new status values unless the canonical 8 genuinely cannot describe the subject.

**The status–rung consistency rule.** Status and rung must not contradict. A `done` area at rung `researched` is a finding, not a valid record. The audit flags these explicitly (§5).

---

## Section 4: The per-area finding record

Every audited area produces exactly one record. The record format is locked at the start of the campaign; sessions append records to the campaign's ledger.

```yaml
- area_id: <bucket>-<kebab-name>
  name: <human-readable name>
  bucket: <bucket name from the campaign's bucket list>
  files:
    - <list of files or folder globs that constitute this area>
  maturity_rung: <researched | specified | built | evaluated | deployed>
  status: <backlog | in-progress | in-review | blocked | ready-to-work | done | superseded | archived>
  evidence: >
    <What file, test result, decision-log entry, or deployment proves the rung. Required.
    No rung is recorded without named evidence. Cite specific paths and dates.>
  blockers:
    - <what stands between this area and the next rung — one per item>
  downstream_dependents:
    - <area_id of another area, or a service / skill / external file that this area gates>
  audit_notes: >
    <Anything that does not fit above — contradictions found, stale data, surprises,
    instrument-calibration notes. Honest, specific.>
  last_audited: <YYYY-MM-DD>
  auditor: session-<N>
```

**Required fields:** every field except `blockers`, `downstream_dependents`, and `audit_notes` is required. Empty lists are allowed for the three optional fields; omit the key only if the list is genuinely empty AND the auditor confirms nothing belongs there.

**`evidence` is the most important field.** It is what makes the audit honest. If `evidence` reads "the area looks complete" or "no apparent gaps," that is not evidence — that is assertion. Rewrite with a file path, a test result, a benchmark run, or a deployment fact. If none can be cited, the rung is wrong.

**Q5 compliance — canonical field declarations.** The record carries two fields that together describe maturity state: `maturity_rung` (the canonical answer) and `evidence` (the qualifier that justifies it). The instrument declares: `maturity_rung` is canonical; `evidence` is the prose witness; if the two disagree (e.g., `maturity_rung: evaluated` but `evidence` cites no test), the record is invalid, not a parallel record. Per `corrections-registry.yaml § split-schema-canonicalization-drift`.

**Format alternatives.** YAML is the default and matches the worked example. For audits whose source material is in a non-YAML shape:

- **Markdown table.** When records are short (≤ 5 fields) and the audit produces ≤ 30 areas, a Markdown table can be the canonical ledger format. Cross-references via inline IDs work the same way.
- **JSON.** When the campaign integrates with other tools that consume the ledger programmatically. Field shape is identical; only the encoding changes.
- **SQL audit table.** When the source material is itself a database (e.g., auditing a client's CMS or product catalog), the ledger may be a SQL table. The instrument names the table schema and the queries that produce the rollup.

Document the format choice in the campaign plan (Step 3). Sessions cannot switch format mid-campaign without an instrument amendment.

---

## Section 5: The required output framing

The audit answers the user's central question (Step 1 intake of the parent skill). The canonical framings:

**For capability audits — Finished / In progress / Left to do.** Every audited area lands in exactly one bucket, decided by status alone:

| Output bucket | Status values |
|---------------|---------------|
| **Finished** | `done`, `in-review` |
| **In progress** | `in-progress`, `ready-to-work`, `blocked` |
| **Left to do** | `backlog` |
| **Excluded** | `superseded`, `archived` (reported separately as cleanup candidates) |

The maturity rung is reported alongside each area as a depth check, not folded into the framing.

**For design system audits at scale — Compliant / Drift / Unknown.** Where compliance is the central question.

**For evaluation audits — Passing / Failing / Not yet tested.** Where coverage and correctness are the central question.

**Other framings** are valid when the central question demands them. The framing is locked in the instrument; sessions write to it, they do not choose a new one.

---

## Section 6: The evidence standard

The audit is only worth running if it is honest. Three rules, enforced every session:

### 6.1 No rung without evidence

- **Rung 2 (Specified)** requires a named spec file.
- **Rung 3 (Built)** requires an artifact that exists and runs / opens / renders. For code, the path to the file. For a skill, the deployed SKILL.md. For a document deliverable, the finished file.
- **Rung 4 (Evaluated)** requires named test results, benchmark outputs, a review record, or a working real-world output. A note that says "we tested it" without citing the test is not evidence.
- **Rung 5 (Deployed / Sellable)** requires either active use (a client engagement, a deployed system, a published artifact) or a credible offer — meaning the auditor could write a one-paragraph description of the offer to a client today without inventing capability.

An area with a confident-sounding document but no evaluation is **rung 2**, not rung 4. The confidence of the writing does not earn rungs.

### 6.2 Stale counts as a finding

A spec that no longer matches reality is not "done." It is a finding. The audit records staleness as a blocker, drops the rung accordingly, and notes the staleness in `audit_notes`.

Specifically:
- A spec referencing files that no longer exist → staleness finding.
- A spec referencing decisions superseded in the decision log → staleness finding.
- A spec describing a capability count, file count, or version number that does not match current state → staleness finding.

### 6.3 Contradiction counts as a finding

If two files in a bucket disagree, that is logged in `audit_notes`. **Reconciliation is downstream work**, not audit work. The auditor does not silently resolve contradictions mid-audit; that would erase the signal the campaign is trying to surface.

Each contradiction becomes a typed follow-on artifact (see [`rubric-library.md`](rubric-library.md) for the A/B/C taxonomy):

- A pure documentation disagreement → Type A dispatch prompt.
- A capability / state disagreement → Type B plan.
- A research disagreement → Type C research task.

---

## Section 7: Working procedure per audit session

Every audit session follows the same shape. The procedure goes in the instrument so sessions do not improvise.

### 7.1 First 15 minutes — area definition

1. Load the session's file inventory from the campaign plan.
2. Cluster the files into areas. Aim for 4–10 files per area; adjust by judgment.
3. Name each area. Write the names down before opening any of the files in depth.
4. If the inventory is wrong (files added, moved, deleted since reconnaissance), log the delta as an instrument-calibration note and proceed.

### 7.2 Area-by-area audit — the bulk of the session

For each area, in order:

1. **Read the area's files.** All of them, at least to skim. The audit cannot rate evidence it has not seen. For any file exceeding 1,500 lines: programmatic extraction per `heyhi-session-integrity` Phase 0 Method C — `git diff HEAD --` for changes, `grep -n` for anchors, `sed -n` for targeted lines.
2. **Determine the rung.** Use the ladder in §2. Demand evidence for every rung claim.
3. **Determine the status.** Use the taxonomy in §3. Check the status–rung consistency rule.
4. **Identify blockers.** What stands between this area and the next rung? One blocker per line.
5. **Identify downstream dependents.** What other areas, skills, services, or external files depend on this area? Cite by `area_id` or by file path.
6. **Write the record.** Append to the campaign ledger under the area's bucket section.

### 7.3 End of session — rollup and close

After every area in the session has a record:

1. **Write the session's bucket rollup** in whatever state file the campaign uses (e.g., `project-state.yaml capability_readiness` for ai-services audits).
2. **Log session findings** as candidate typed follow-on artifacts in the ledger.
3. **Close through Exit Gate Flavor B** (`CLAUDE-SESSION-RULES.md § Exit Gate`). The session is plan-bearing.

---

## Section 8: What the audit does not do (negative space)

The instrument carries a negative-space section. Restraint is the campaign's discipline; the negative section makes the restraint visible.

The audit produces records. It does not:

- **Fix anything.** Finding a gap is not the same as closing it. Fixes are typed follow-on artifacts.
- **Change service definitions, the roadmap, or downstream summary surfaces mid-session.** Those propagations belong to the Close stage (Step 5 of the parent skill), not the audit sessions.
- **Reconcile cross-area or cross-bucket contradictions.** Those are logged and resolved in the cross-cutting synthesis session (canonical position: session N-2 in the arc).
- **Write client-facing claims.** The audit is internal; client-facing positioning is downstream.

If a session feels the pull to start finishing a half-built area instead of auditing it, that is the strongest risk the campaign carries. Resist it. The audit's value is the picture, and the picture is only true if the auditor stayed honest.

---

## Section 9: Versioning and amendment

The instrument carries a version (semver-style). The first published version is `v1.0.0`, ratified in the campaign's first session.

**Amending the instrument.** If a session surfaces a genuine problem with the instrument — a rung definition that is unworkable, a status that is missing, a record field that is needed — the session may **propose** an amendment in its Exit Gate output. The amendment is not adopted mid-campaign. A designated review session decides whether to issue a new minor version (`v1.1.0`) for remaining sessions — only if the change does not invalidate previously written records.

**The hard rule:** drift in the instrument across sessions is the failure mode the campaign exists to repair. The instrument stays fixed unless explicitly versioned.

---

## Section 10: Reference cross-links

Every instrument ends with a links section pointing at:

- Campaign plan: `plans/plan-[campaign-name]-YYYY-MM-DD.md`
- Ledger: the YAML / Markdown / JSON / SQL file the campaign writes to
- Rollup home: the state file the campaign rolls up into (e.g., `project-state.yaml`, a dashboard, a tracking sheet)
- Exit Gate definition: `CLAUDE-SESSION-RULES.md § Exit Gate`
- Status taxonomy origin: the source the canonical 8-value taxonomy comes from
- Architecture invariants relevant to the audit: e.g., `Evaluation Before Deployment` from `ai-services/_core/architecture-principles.md`
- This instrument's parent skill: `heyhi-skills/heyhi-audit-campaign/SKILL.md`

---

## Q3 verify-before-claim discipline (applies to writing the instrument itself)

When the instrument cites a field name, file path, or schema element from an existing project surface, verify it before locking the instrument. Common verifications:

- Field names from an existing ledger: `grep -n '<field>' <ledger-path>`
- File paths cited: `test -f <path> || echo MISSING`
- Schema references: read the source schema and confirm the cited element exists

The Session 2 incident — claiming `rung` when the canonical field is `maturity_rung` — is the failure mode this discipline prevents. The cost of `grep` is seconds; the cost of a wrong field name compounds across every audit session that loads the instrument.

---

## Quick checklist before declaring an instrument done

- [ ] All ten sections present (or skipped sections justified in writing).
- [ ] Per-area record format passes the three-area smoke test (draft records for the first three areas by hand; confirm well-formed).
- [ ] Status taxonomy reuses canonical values; does not invent new ones without justification.
- [ ] Maturity ladder rungs each have a stated evidence requirement.
- [ ] Q5 canonical-field declaration present for any split logical concept.
- [ ] Q3 verifications run on every cited field/path/schema reference.
- [ ] Negative-space section (Section 8) names at least three things the audit does *not* do.
- [ ] Version is set (`v1.0.0` at first publication).
- [ ] Reference cross-links resolve.
- [ ] Frontmatter has `classification:`, `created:`, `campaign:`.

---

*HeyHi Internal Use Only. heyhi-skills/heyhi-audit-campaign/references/. Loaded by SKILL.md Step 2 (Design stage) and Step 6 (Restructure stage).*
