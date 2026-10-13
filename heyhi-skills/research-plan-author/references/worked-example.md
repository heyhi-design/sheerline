---
classification: confidential
title: "Worked example — a filled Research Plan"
skill: research-plan-author
loaded_by: "SKILL.md Step 1 (calibration)"
---

# Worked example — a filled Research Plan

**Synthetic input, invented product. No client content.** Read this to calibrate the register and depth of the free-prose slots; do not copy its findings. The empty slots are shown empty on purpose — that is the output shape, not an omission.

**Synthetic goal brought by the (invented) team:** *"Users keep dropping out at the account-linking step in our budgeting app. We think a manual-entry fallback would fix it. Can we prove the fallback works before we build it?"*

---

```
# Research Plan — Account-linking drop-off (LedgerLite, synthetic)
Source: synthetic team note        Drafted: 2026-09-01

## Research question (candidate — the human locks it)
[candidate — agent-drafted] Two questions are tangled in the goal, and they are different studies:
  Q1 (generative): "Why do users abandon the account-linking step?" — the unmet need is unknown;
     "a manual-entry fallback" is a *solution* proposed before the opportunity is understood
     (Opportunity-Solution-Tree warning: the goal names the answer, not the problem).
  Q2 (evaluative): "Does a manual-entry fallback let more users complete setup than linking does?"
     — a solution test, only worth running once Q1 says a fallback addresses the real barrier.
Naming the ambiguity is mechanical; deciding whether to answer Q1 first, or bet on the fallback
and go straight to Q2, is the team's.

## Method options (candidates)
| Candidate method | Generative / Evaluative | What it answers | What it cannot | Sample-size basis | Fieldwork cost |
|------------------|-------------------------|-----------------|----------------|-------------------|----------------|
| Moderated usability test on the current link step | Evaluative | where and why users stall on linking | how often it happens across the base | 5 directional / 10 reliable | med |
| 5–8 user interviews (recent abandoners) | Generative | the real reason they stopped (trust? bank not supported? friction?) | whether a fix works | 5 directional / 10 for a stable read | med-high |
| Unmoderated task test: link vs. manual-entry prototype | Evaluative (comparative) | completion-rate difference between the two flows | *why* one wins | power-based (baseline + MDE), not the usability floor | low-med |
| Funnel analytics on the existing link step | Quantitative (behavioral) | where in the funnel the drop happens, at what rate | why, or whether the fallback helps | power-based, not the usability floor | low |

All methods above are AGENT-DRAFTED CANDIDATES — see provenance. None is selected.

## Faulkner sample-size basis
Two different sample-size questions live in this goal, and conflating them is the trap. **Problem
discovery** (the moderated usability test on the link step, the generative interviews) uses the
Faulkner floor: **5 directional, 10 for a stable read, 20 for a ≥95% detection floor** — that floor
is about *finding usability problems*. **A completion-rate comparison** ("prove more users finish
with the fallback than with linking") is *not* a discovery question; it is quantitative, so its n
comes from a **power calculation** — baseline completion rate + the minimum improvement worth
detecting + confidence — not the 5/10/20 usability floor. **FLAG:** the goal's word "prove" is
attached to a rate difference, so it needs that power calculation; 5 users cannot prove it, and
even the 20-user detection floor proves nothing about a rate — it is the wrong instrument for the
claim. Running under-powered is a valid speed choice, but it is the team's go decision to make
knowingly, not a number to bury.

## Consent + ethics checklist (for the human to complete)
- [ ] Informed consent captured (purpose, use, retention stated to participant)
- [ ] Recording / screen-capture permission
- [ ] Right to withdraw, without penalty
- [ ] Incentive handling stated
- [ ] PII minimized — this study touches financial-account UX; collect no real account
      credentials or balances, use a sandbox/prototype, name storage + deletion
- [ ] Ingested transcripts/recordings neutralized + provenance-stamped at the write boundary

## Open questions for the team (questions, not judgments)
- What decision does this feed, and by when? "Prove before we build" implies a build gate — that
  bounds whether Q1 (understand first) or Q2 (test the bet) is the right first move.
- Is the drop-off concentrated in users whose bank is unsupported? If so the barrier is coverage,
  and a manual fallback treats a symptom — analytics could answer this before any moderated study.
- Is "manual entry" acceptable to the team given its ongoing data-freshness cost, or is this a test
  of a flow you would not actually ship?

## ⛔ Research question — NEEDS HUMAN
This slot is intentionally empty. The final question the study is designed around is the team's to lock.
   Locked question(s): ____________________

## ⛔ Method selection — NEEDS HUMAN
Which candidate method the team runs is a study-design judgment, not a mechanical one.
   Chosen method(s): ____________________

## ⛔ Go decision — NEEDS HUMAN
   Proceed / revise / hold: ____________________

## Named gate
Sign-off owner (research owner / design lead): ____________________  Date: ______
No question, method, or go decision is recorded until this line is signed by a human.
```

---

*What this example demonstrates for calibration:* the question slot **restates and separates** the tangled goal (and names the solution-dressed-as-opportunity) without picking one; each method carries an honest sample-size basis — the Faulkner floor for problem discovery, a power calculation for the rate comparison; the "prove" claim is **flagged** for conflating the two (5 users cannot prove a rate difference, and the detection floor is the wrong instrument for it); the go decision is left to the human; and the financial-UX PII risk is caught in the consent checklist. Nothing is selected, declared, or signed.

*HeyHi Confidential. Calibration reference for `research-plan-author` (Sheerline area 1). Synthetic content only.*
