---
classification: confidential
title: "Worked example — a filled Reasoning Integrity Report"
skill: strategy-integrity-warden
loaded_by: "SKILL.md Step 1 (calibration)"
---

# Worked example — Reasoning Integrity Report

A filled golden report, start to finish, on a **synthetic, invented** opportunity solution tree. No client content; every node and citation below is fabricated for calibration. Read it to anchor register and depth on the free-prose slots (the restatement, open questions, near-misses). Do not copy its findings.

This example is built to exercise the two things v0.2.0 adds: an **outcome-quality FLAG on a lagging-business-metric root** (named as a type-mismatch, with no replacement outcome supplied) and the **staleness heuristic band** (one FLAG on a since-rebuilt flow, one PASS on an old-but-stable-behavior citation held in near-misses). The load-bearing property throughout: the report audits five checks, flags real problems, and **never ranks the three opportunities or names the one to pursue** — warden shape held.

---

## The input (synthetic OST the team brought)

> **Opportunity Solution Tree — "Q3 growth"** *(invented)*
> **Outcome:** Increase quarterly revenue by 15%.
> **Opportunities:**
> 1. *Users abandon during trial setup* — linked: "Q2-2026 trial-funnel study, 38% drop at the
>    workspace-creation step." (The workspace-creation step is unchanged since that study.)
> 2. *Users want a configurable dashboard* — no evidence linked.
> 3. *Onboarding is confusing* — linked: "2023 onboarding usability study." (Onboarding was
>    fully rebuilt in early 2026.)
> **Mini RICE:** dashboard — Reach 8, Impact 3, **Confidence 100%, Effort 1** → top rank.
> Setup-abandon — Reach 6, Impact 2, Confidence 70%, Effort 4. Onboarding — Reach 5, Impact 2,
> Confidence 60%, Effort 3.
> "Team wants to know which to pursue."

---

## The filled report

```
# Reasoning Integrity Report — Q3 growth OST (SYNTHETIC)
Source: opportunity solution tree (invented)   Audited: 2026-08-23   Type: OST + RICE

## Canonical restatement
Outcome → 3 opportunities → (no solutions or experiments attached below opportunities 1 and 3;
opportunity 2 carries an implied solution in its own name). Restated shape:
  Outcome: "increase quarterly revenue 15%"
    - Opp 1: users abandon during trial setup            [evidence: Q2-2026 funnel study]
    - Opp 2: "users want a configurable dashboard"       [agent-restructured — verify: this reads
              as a solution ("a dashboard"), not an unmet need; the need it implies is unstated]
    - Opp 3: onboarding is confusing                     [evidence: 2023 usability study]
The solution and experiment layers are largely empty — the tree is opportunity-only below the root.

## Integrity checks (check 1 is the Canonical restatement above)
| # | Check | Verdict | What triggered it (node-specific) |
|---|-------|---------|-----------------------------------|
| 6 | Outcome-quality (top-node influenceable) | FLAG | Root "increase quarterly revenue 15%" is a lagging business metric, not a team-influenceable product outcome. You cannot run opportunity discovery against revenue directly — it is moved by pricing, sales, and market as much as by product — so every opportunity below inherits the gap. (Type-mismatch named; no replacement outcome supplied — that is yours to articulate.) |
| 2 | Evidence-linkage / assumption-flag | FLAG | Opp 2 ("configurable dashboard") links no evidence and is presented as a need. Opp 1 and Opp 3 are evidence-linked. |
| 3 | Solutions-dressed-as-opportunities | FLAG | Opp 2 is a solution ("a dashboard") in the opportunity space; the unmet need it would serve is unstated. Not rewritten here — articulating the real need is yours. |
| 4 | Evidence staleness | FLAG | Opp 3 cites a 2023 study of an onboarding flow rebuilt in early 2026 — the referenced surface has changed, so the citation is stale regardless of age. Opp 1's Q2-2026 study is current and about an unchanged step — PASS. |
| 5 | Back-solved scores | FLAG | Dashboard RICE: Confidence 100% and Effort 1 are the classic back-solve tells (nothing is 100% confident; Effort 1 on an unspecified feature), producing its top rank. Not re-scored here. |

## Open questions for the team (questions, not judgments)
- The outcome is "increase revenue" — is there a product outcome your team owns (an activation,
  adoption, or retention behavior) that ladders up to that revenue goal and could root the tree
  instead?
- What is the unmet need behind "users want a dashboard" — what can't they do or see today?
- Opp 3 cites a 2023 study, but onboarding was rebuilt in 2026 — is there a post-rebuild
  finding, or is this opportunity currently running on stale evidence?
- The dashboard's RICE effort is 1 with no solution specified — what scope produced that
  estimate?

## Near-misses and unchecked territory (the audit journey, made inspectable)
- Considered, did not flag: Opp 1 "users abandon during trial setup" reads as a genuine unmet
  need (not a solution) and is evidence-linked to a current study — no FLAG.
- Almost flagged (staleness): weighed whether Opp 1's Q2-2026 citation was aging; it is recent
  and about an unchanged workspace-creation step — held at PASS.
- Could not check: the Q2-2026 funnel study is cited but not attached, so its 38% figure is
  taken as linked, not independently verified from the artifact.
- NOT done: no ranking of the three opportunities, and no replacement outcome authored — both
  are the team's calls (see the empty slots).

## ⛔ Which opportunity to pursue — NEEDS HUMAN
This slot is intentionally empty. Ranking and selecting the opportunity is the team's
strategy call. The warden guards the reasoning; it does not choose.
   Selected opportunity: ____________________

## ⛔ What to build — NEEDS HUMAN
   Decision: ____________________

## Named gate
Sign-off owner (product / design lead): ____________________   Date: ______
No opportunity is selected until a human signs.
```

---

## Why this is a good golden

- **The outcome-quality flag names a type, not a replacement.** It says the root is a lagging business metric and why that breaks the tree — and it stops. The open question *asks* whether a product outcome exists to ladder up; it does not answer it. That is the warden-shape line for the new check.
- **The staleness band leads with "what changed."** Opp 3's citation is flagged because the flow was rebuilt, not because 2023 is old; Opp 1's 20-month-old-adjacent reasoning gets a near-miss PASS because its subject is unchanged. Age is the secondary signal, as the band prescribes.
- **Five FLAGs, zero rankings.** The report finds real problems on every check and still refuses to say which opportunity is strongest, even though the team asked directly and a back-solved RICE is sitting right there tempting a "corrected" ranking.
- **Open questions are questions; near-misses are traces.** None ranks; the near-misses explicitly record what was *not* done (ranking, outcome authoring) so the boundary is visible in the artifact itself.

*HeyHi Confidential. Worked example for `strategy-integrity-warden` v0.2.0. Fully synthetic; added 2026-08-23 (Wave D) per the 2026-08-22 skills audit § 4 (no worked examples) and § 2.4 / § 5.*
