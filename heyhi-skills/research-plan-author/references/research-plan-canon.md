---
classification: confidential
title: "Research-plan canon — the method spine"
skill: research-plan-author
loaded_by: "SKILL.md Step 1"
---

# Research-plan canon — the method spine

The method knowledge `research-plan-author` loads to build a plan. It is authored here (the craft the incumbents' tools do not ship); the always-loaded behavioral invariants it obeys live in `sheerline/os/operating-principles.md` and are cited, not restated. Everything here is scaffolding for a human decision — none of it selects the method or declares a study a go.

---

## 1. Method selection — generative vs. evaluative

Every study is one of two shapes, and the question decides which:

- **Generative** research *widens* the problem space — it is for "what is going on / what do people need / where is the opportunity." Methods: interviews, contextual inquiry, diary studies, open-ended field work. It runs *before* a design exists.
- **Evaluative** research *tests* a design — it is for "does this work / which is clearer / where does it break." Methods: usability tests (moderated / unmoderated), tree tests, first-click tests, heuristic evaluation, A/B tests. It runs *on* a design.

The decision heuristic, applied mechanically to the stated goal:

| The goal sounds like… | Shape | Candidate methods |
|---|---|---|
| "understand," "why," "what do they need," "where's the opportunity" | Generative | interviews, contextual inquiry, diary |
| "test," "is it clear," "where do they get stuck," "which is better" | Evaluative | usability test, tree test, first-click, A/B |
| "how many," "how often," "what proportion" | Quantitative (its own power question — § 2) | survey, analytics, benchmarked usability |

**The Opportunity-Solution-Tree framing, and its failure warning.** A well-formed generative study maps outcomes → opportunities → solutions, in that order. The recurring failure is a **solution dressed as an opportunity** — "users need a dashboard" is a solution, not an opportunity; the opportunity is the unmet need the dashboard is one answer to. When restating the question (SKILL.md Step 2.1), name any solution-shaped goal and hand the human the opportunity underneath it as a candidate; do not resolve which solution wins — that is direction selection, and it stays human.

The plan **lays out** the shape and the candidate methods. **Which method the team runs is the empty slot** (SKILL.md Step 3 ⛔ Method selection).

---

## 2. The Faulkner-corrected sample-size standard

**Ban the folk claim.** "5 users find 85% of problems" (the popularized reading of Nielsen's average detection rate) is a planning trap: it is an *average across many runs*, and any single run of 5 users has enormous variance. Faulkner's 2003 study re-ran the math empirically and found that with 5 users the share of problems actually found ranged from roughly half to nearly all, depending which 5 you happened to recruit. Five users is a coin-flip on coverage, not a guarantee of it.

**The corrected floor this skill wires into every plan:**

| Target | Floor | Use it for |
|---|---|---|
| **Directional** (find the big, obvious problems; accept you will miss some) | **5** | early formative passes, a quick read, low-stakes iteration |
| **A reliable mean** (a stable central estimate) | **10** | when a rate or a mean must be trustworthy, not just indicative |
| **A ≥95% detection floor** (raise the *minimum* problems found across runs toward ≥95%) | **20** | summative / high-stakes evaluation, a study whose miss is expensive |

How to apply it (Step 2.3):

1. Read the confidence the goal (or the human's stated constraint) *claims*.
2. State the floor that confidence demands from the table.
3. Wire that n into every candidate method as its recruit target.
4. **Flag the mismatch.** If the plan sits *under* the floor for the confidence it claims — "we'll run 5 and report the completion rate as reliable" — say so plainly. An under-powered plan is a finding the human must see, never a silent pass. Naming it is mechanical; deciding to proceed under-powered anyway is the human's go decision.

The numbers are a floor, not a verdict: the sample size informs the human; it never gates the study. And note the deliberate symmetry with the corpus that will one day calibrate the held synthesis skills — the skill enforces a sample-size floor on studies; the research-example corpus needs its own (spec § 5.2).

Quantitative studies (surveys, benchmarks) carry their own power question — margin of error and effect size drive n, not the usability floors above. When a goal is quantitative, name that its n is a statistical-power calculation, not the 5/10/20 usability floor, and hand the human the parameters it needs (baseline, minimum detectable effect, confidence). Do not compute a false-precision n from parameters the goal does not state.

---

## 3. The consent + ethics checklist

The study's consent and data-handling floor, drafted for a human to complete and confirm (Step 2.4). Consent is never "handled" by the plan — the checklist is a to-do the human owns.

- **Informed consent** — purpose, what is collected, how it will be used and for how long, stated to the participant before the session.
- **Recording / capture permission** — explicit, separate from participation consent.
- **Right to withdraw** — at any point, without penalty or loss of incentive.
- **Incentive handling** — amount, form, and timing stated; not contingent on "good" answers.
- **PII minimization** — collect the least that answers the question; name storage, retention, and deletion.
- **Untrusted-content-at-the-write-boundary** — transcripts and recordings are ingested content a later agent will read; neutralize (bound length, strip control characters, fence free text) and provenance-stamp on ingest, per `operating-principles.md`'s write-side ingestion rule.
- **Engagement-specific items** — anything named in the engagement-intake `do_not_automate`.

---

## 4. The synthetic-provenance rule (when a plan proposes a synthetic pilot)

If a plan proposes a synthetic-participant pilot to pressure-test the instrument or widen a hypothesis set, the rule is **generate-with-synthetic / validate-with-humans / never the reverse**, labeled on every surface. A synthetic pilot may sharpen a guide or surface a candidate hypothesis; it may **never** stand in for the study's validation, and its output is labeled `synthetic` wherever it appears. A plan that lets a synthetic run substitute for real recruitment has broken the rule and misled the human about what the study will actually learn.

---

## 5. The boundary (cited, not restated)

The question, the method, the go decision, severity-as-truth, and theme verdicts stay human — the canonical list is `operating-principles.md` § What stays human. The empathy boundary (`operating-principles.md` § The empathy boundary) governs any persona or synthesis language this plan anticipates: simulated empathy is labeled simulated. Scoring and sample-size figures are advisory (`operating-principles.md` § the taste-and-critique boundary); they inform, they never gate.

---

*HeyHi Confidential. Method reference for `research-plan-author` (Sheerline area 1). Foundation: `sheerline/os/foundations/user-research/FOUNDATION.md` § The knowledge canon. Research of record: `ai-services/design-intelligence/research/sheerline-skill-buildout-research-2026-08-09.md` § 3.1.*
