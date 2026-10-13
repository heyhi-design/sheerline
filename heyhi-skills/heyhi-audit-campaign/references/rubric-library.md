---
classification: internal
title: Rubric Library
purpose: Reusable rubrics for audit campaigns — maturity ladders, status taxonomy, finding-type codes, follow-on artifact taxonomy. Loaded by heyhi-audit-campaign at Step 2 (Design stage) and Step 4 (Run stage).
created: 2026-05-21
loaded_by: heyhi-audit-campaign
canonical_sources:
  - ai-services/_core/audit-instrument.md (5-rung maturity ladder, 8-value status taxonomy, A/B/C follow-on taxonomy)
  - ai-services/_core/capability-audit-ledger.yaml (finding-type codes in active use)
---

# Rubric Library

The vocabulary HeyHi audit campaigns use. Reuse before invent.

This reference is loaded at Step 2 (Design stage) when the instrument is being designed, and at Step 4 (Run stage) when a session needs to apply the rubrics to actual records.

---

## 1. The 5-rung maturity ladder (canonical)

The ladder the ai-services campaign used. Default for capability audits, sellable-services audits, and any audit answering *"how mature is the work?"*

| Rung | Name | Evidence requirement |
|-----:|------|----------------------|
| 1 | **Researched** | Research, source material, or exploratory writing exists. Knowledge is captured. The deliverable can be a literature review, a comparative analysis, a discovery doc. |
| 2 | **Specified** | A coherent spec or build plan exists and is internally consistent. The next step is buildable from what is written. Spec passes a "could another HeyHi practitioner build from this?" read. |
| 3 | **Built** | An implementation exists. For code: the code runs without errors. For document deliverables: the deliverable is complete and not a draft. For skills: the SKILL.md is deployed. Path-to-artifact citable. |
| 4 | **Evaluated** | The implementation has passed its trajectory and outcome tests. For non-code: validated against acceptance criteria. Named test results, benchmark outputs, or review records exist. Test path citable. |
| 5 | **Deployed / Sellable** | The capability is in active use, or it can be genuinely offered to a client today. Demonstrable end-to-end. A client engagement, a published artifact, or a credible offer letter. |

**The foundational rule:** an area's rung is the highest one for which **named evidence** exists. No rung on assertion. The confidence of a document does not earn rungs; the evidence the document cites does.

**Ladder edge cases:**

- A research area whose only deliverable *is* the research can reach rung 5 if the research is finished, cited downstream, and not in revision (e.g., a comparative analysis that informed a project decision).
- A capability built but superseded sits at the rung the original build reached, with status `superseded`. It is not retroactively downgraded.
- A skill in `heyhi-skills/` with a deployed SKILL.md is at least rung 3. It reaches rung 4 only with named evaluation evidence. Deployment alone does not earn rung 5 — only active use does.

---

## 2. Alternative ladders for non-capability audits

When the central question is not "how mature?" the ladder shape changes. Cataloged options:

### 2a. Design system at scale (3-rung coverage ladder)

For audits answering *"how complete is this design system?"*

| Rung | Name | Evidence requirement |
|-----:|------|----------------------|
| 1 | **Token coverage** | Token-by-token mapping exists between design source (Figma) and code. Coverage percentage citable. |
| 2 | **Component coverage** | Components in the system have Storybook entries (or equivalent), each linked to the matching Figma component. Coverage percentage citable. |
| 3 | **Documentation coverage** | Each component has named documentation: usage, props, accessibility, examples. Coverage percentage citable. |

### 2b. Evaluation framework rollout (4-rung)

For audits answering *"how well is this evaluation framework deployed?"*

| Rung | Name | Evidence requirement |
|-----:|------|----------------------|
| 1 | **Eval defined** | The eval criteria are written down. Pass/fail conditions specified. |
| 2 | **Golden set populated** | A golden set of cases exists with expected outputs. Size cited. |
| 3 | **Trajectory tests passing** | The ReAct cycle for each case is logged and verified. Test results citable. |
| 4 | **Outcome tests passing** | The final outputs match acceptance criteria. Results citable. |

### 2c. Compliance audit (3-rung)

For audits answering *"is this in compliance?"*

| Rung | Name | Evidence requirement |
|-----:|------|----------------------|
| 1 | **Compliant** | Compliance evidence cited for every requirement. |
| 2 | **Out of compliance** | At least one requirement fails; named gap with named impact. |
| 3 | **Unknown** | Compliance status could not be determined; named reason. |

**Default when in doubt:** use the canonical 5-rung capability ladder. It is the most-tested.

---

## 3. The 8-value status taxonomy (canonical)

The status taxonomy reused across HeyHi work — origin: the Studio Graph work. **Reuse, do not invent.** Status-word drift is itself a logged failure mode.

| Status | Meaning |
|--------|---------|
| `backlog` | Identified but not yet started. |
| `in-progress` | Active work underway. |
| `in-review` | Built; awaiting evaluation or sign-off. |
| `blocked` | Cannot advance until an external dependency resolves. The blocker is named. |
| `ready-to-work` | Specified and unblocked; awaiting an executor or session slot. |
| `done` | Complete. For audit records, "done" requires the maturity rung to be `evaluated` (4) or `deployed` (5). |
| `superseded` | Replaced by something newer. Excluded from "active" rollups. The supersession reference is named. |
| `archived` | Intentionally retired. Excluded from "active" rollups. |

**The status–rung consistency rule.** A `done` area at rung `researched`, `specified`, or `built` is a finding, not a valid record. The audit flags these explicitly under the campaign's required output framing.

**Reading status values from prior work:** if an existing ledger uses a status value not in this taxonomy (e.g., `wip`, `ongoing`, `complete`), the audit treats it as an instrument-calibration finding. Map to the canonical 8 in the new record; log the mapping in `audit_notes`.

---

## 4. Finding-type codes

The codes audit campaigns use to refer to findings cross-session. Stable IDs make findings citable in the synthesis brief, the fix spec, and the decision-log entry.

### Canonical codes (used by the ai-services campaign)

| Code prefix | Meaning | Source |
|-----|---------|--------|
| `DF-N` | **Downstream Finding.** A downstream surface lags the ledger or the audit's truth. Example: `synthesis.md` claims Signal Reader is "build-ready" but the ledger records it as `specified`. | Sessions 9-10 of the ai-services campaign |
| `CBD-N` | **Cross-Bucket Drift.** Two or more bucket records disagree about the same fact, or a structural drift surfaces across buckets. Example: figure staleness across three documents about the same counter. | Session 9 of the ai-services campaign |
| `PL-N` | **Plan / Follow-on Plan.** A typed follow-on artifact: a plan that captures a capability/state disagreement requiring more work than a dispatch can hold. | Type B follow-ons across the campaign |
| `DG-N` | **Dispatch.** A typed follow-on artifact: a dispatch prompt that captures a pure documentation drift fixable by a single self-contained session. | Type A follow-ons across the campaign |
| `RT-N` | **Research Task.** A typed follow-on artifact: a research task that captures a knowledge gap requiring exploration before a plan can be written. | Type C follow-ons across the campaign |

### Choosing codes for a new campaign

- If the new campaign reuses the ai-services campaign's pattern (capability audit, summary surfaces, typed follow-ons), reuse the codes verbatim.
- If the new campaign has a fundamentally different shape (e.g., a compliance audit), define new code prefixes in the instrument and document them here as canonical for that campaign type. The first new campaign that needs them defines them; subsequent campaigns reuse.

---

## 5. The follow-on artifact taxonomy (A/B/C)

Every contradiction, gap, or drift the audit surfaces becomes a typed follow-on artifact, not silently fixed. Verified against `ai-services/_core/audit-instrument.md:163-166`.

| Type | What it is | When it fires | Output |
|------|------------|---------------|--------|
| **Type A — Dispatch** | A pure documentation drift fixable in one self-contained session. The fix is the closing artifact; no further plan needed. | A downstream surface paraphrased an audit finding incorrectly; the fix is to update the paraphrase. A README is stale relative to a directory. A status field needs a flip. | A dispatch prompt at `dispatch/dispatch-prompts-YYYY-MM-DD.md` per `dispatch/README.md` |
| **Type B — Plan** | A capability/state disagreement requiring more work than a dispatch can hold. The fix is a planned multi-step (or multi-session) effort. | The audit surfaced a capability claimed-but-not-built; closing the gap requires a build session. A schema needs to change. A skill needs new behavior. | A plan at `plans/plan-[topic]-YYYY-MM-DD.md` per `plans/README.md` |
| **Type C — Research** | A knowledge gap that has to be closed before a plan can be written. The fix is research; the plan comes later. | The audit surfaced an unknown — a question the team cannot answer with current evidence. A trade-off was logged but never decided. | A research task entry (in a research ledger if one exists, otherwise a brief at `ai-services/<bucket>/research/`) |

**How follow-ons are logged.** During an audit session, follow-ons accumulate in the ledger's `follow_on_artifacts` section. At the campaign's close, the close-out artifact (synthesis brief or fix spec) cites them by ID. The actual artifact files (dispatch prompts, plans, research briefs) are produced post-campaign by the work the follow-on represents — not by the audit campaign itself.

**The discipline:** the audit produces records and follow-on entries. It does not produce the follow-on artifacts themselves. That is downstream work.

---

## 6. Cross-rubric consistency rules

A small set of rules enforced across all rubrics:

1. **Status–rung consistency.** Every record's status and rung must agree per §3 above. Violations are findings.
2. **Evidence required for every rung claim.** Per §1 and §2 (no rung without evidence). Violations are findings.
3. **One taxonomy per dimension.** A campaign does not mix the 5-rung ladder with the 3-rung coverage ladder in the same audit. Pick once.
4. **Finding-type codes are stable across the campaign.** A finding logged as `DF-3` in Session 2 stays `DF-3` through Session 11. Renumbering mid-campaign destroys citation integrity.
5. **Follow-on type matches the finding shape.** A documentation drift is Type A; a state disagreement is Type B; a knowledge gap is Type C. Cross-typing is an instrument-application error.

---

## 7. When to extend the library

This library is short on purpose. Extend it when:

- A new campaign's central question genuinely cannot be answered by the existing ladders. Document the new ladder here with the campaign that introduced it.
- A new finding-type code is needed for a campaign archetype that recurs. Adding a code requires past evidence — at least one prior campaign that needed and used the code informally.

Do not extend it when:

- A single session of a single campaign needed an ad-hoc category. Log the ad-hoc category in `audit_notes`, not in the library.
- The existing 5-rung ladder feels rigid for a soft case. The rigidity is the point; flex the rung *evidence* (e.g., what counts as Built for a non-code area), not the rung labels.

Library extension requires the instance owner's review path (same governance as `OPERATING_PRINCIPLES.md` non-negotiable constraints).

---

## Quick reference table

For session-running cheat-sheet use:

| Need | Default |
|------|---------|
| Maturity ladder | 5-rung capability ladder (§1) |
| Status taxonomy | 8-value canonical (§3) |
| Finding-type for downstream drift | `DF-N` |
| Finding-type for cross-bucket drift | `CBD-N` |
| Follow-on for a documentation drift | Type A dispatch |
| Follow-on for a state disagreement | Type B plan |
| Follow-on for a knowledge gap | Type C research |
| Status of a `done` area without evaluation evidence | Finding, not `done`; record at rung `built` (3) with the rung-status gap logged |

---

*HeyHi Internal Use Only. heyhi-skills/heyhi-audit-campaign/references/. Loaded by SKILL.md Step 2 (Design stage) and Step 4 (Run stage).*
