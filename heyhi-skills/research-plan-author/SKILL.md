---
name: research-plan-author
description: >-
  Draft a governed research plan from a stated learning goal — restate the
  research question as a candidate, lay out candidate methods, wire a
  Faulkner-corrected sample size into each, and draft a consent + ethics
  checklist. Runs the mechanical work: a question restatement, a
  generative-vs-evaluative method comparison, the Faulkner sample-size standard
  (5 directional / 10 reliable-mean / 20 for a ≥95% detection floor) wired into
  every option and FLAGGED when a plan sits under the floor for its stated
  confidence, and a consent/data-handling checklist. Triggers: "write a research
  plan", "plan a user study", "how many participants do we need", "sample size
  for this study", "draft a research protocol", "what method should we run",
  "consent checklist for research". Produces a Research Plan where the final
  research question, the chosen method, and the go decision ship EMPTY behind a
  named human gate — the method is a study-design judgment, and go/no-go is the
  owner's. NOT for sales/qualification discovery (use heyhi-discovery-call). NOT
  for reading organizational signals or foresight (use futurecasting). NOT for
  analyzing fieldwork after it is collected — coding, theming, synthesis (that
  is synthesis-pipeline, held on corpus thickness). NOT for drafting the
  screeners/guides/task-scripts themselves (that is instrument-smith, held on
  engagement pull; this plan names the instruments the study needs, it does not
  write them).
version: "0.1.0"
updated: "2026-09-04"
status: "deployed 2026-09-04 — heyhi-skills/research-plan-author/ (Tier 1, buildable-now, self-application-first); registered in the main registry and the Sheerline area-1 subset registry, promoted in the 2026-09-04 promotion pass (staged PR #753). Area 1 coverage partial -> covered. Sheerline area 1 (User Research), P3, build class N. Spec: plans/plan-sheerline-p3-ur-ia-foundations-2026-08-29.md § 1.2 (Tier 1) / § 4.1 / § 4.4. Foundation: sheerline/os/foundations/user-research/FOUNDATION.md."
classification: HeyHi Confidential
---

# Research Plan Author

**Sheerline area 1 (User Research) · P3 · buildable-now (Tier 1), self-application-first.** A team states what it wants to learn — "do people trust the results," "where does onboarding lose them," "which of these two flows is clearer." This skill does the chartered planning job: it restates that into a candidate research question, lays out the candidate methods that could answer it (generative or evaluative), wires a **Faulkner-corrected sample size** into each so the plan carries an honest floor instead of the folk "5 users is enough," and drafts the consent and data-handling checklist the study needs. It stops at the point where a human must **lock the question**, **choose the method**, and make the **go decision**. Those are study-design and values calls.

**The boundary this skill obeys (Sheerline, absolute).** A structured artifact with explicit empty judgment slots, a named human gate, and provenance labels on anything synthetic. *The final research question, the chosen method, and the go/no-go decision are the empty slots.* Building the plan skeleton — restating the question as a candidate, comparing methods, wiring the sample-size floor, drafting the consent checklist — is mechanical; choosing what the team will actually run is judgment. A version of this skill that picks the method, declares the study a go, or presents a synthetic participant as a real one has exceeded its charter. Scoring and sample-size figures inform; they never gate. Drafting a candidate is not selecting it — the candidate widens the human's options; it does not narrow them to a choice.

> **This skill closes through the Exit Gate (`CLAUDE-SESSION-RULES.md § Exit Gate`).** See the bottom-of-skill bracket.

---

## Routing — disambiguation with sibling skills

| If the task is… | Use |
|---|---|
| "Plan a user study — question, method, sample size, consent" (before fieldwork) | **this skill** |
| Qualifying a sales prospect / running a discovery call | `heyhi-discovery-call` (the keel/sales layer) |
| Reading *organizational* signals, foresight, preferred-future work | `futurecasting` |
| Analyzing fieldwork after it is collected — coding, theming, synthesis | `synthesis-pipeline` (Sheerline area 1, **held** on corpus thickness) |
| Drafting the screeners / interview guides / task-scripts themselves | `instrument-smith` (Sheerline area 1, **held** on engagement pull) |
| Choosing the method, or declaring the study a go | **the human** (this skill's named gate) |

The seam with `synthesis-pipeline` is temporal: this skill works *before* there is data (design the study); the pipeline works *after* (make sense of what came back). The seam with `instrument-smith` is object: this plan **names** the instruments the study needs and the sample size they must recruit for; `instrument-smith` **writes** them. The seam with `heyhi-discovery-call` is purpose: discovery qualifies a buyer, research studies a user.

---

## Step 0: Improvement hook check

Retrieve any recurring corrections for research-planning work (`retrieve_design_corrections`, or the Sheerline `os/corrections/` registry). Fold a match into the pass. No User Research correction category exists yet, so this normally finds nothing — skip silently. This hook is the seam for when `insight-activation` files a research-planning correction into `corrections-intake/` and a human curates it; it is live from day one so the loop can close later.

## Step 1: Load context

1. The **goal artifact** the human brought — a stated learning goal, a feature brief, a "we need to understand X" note, a research request. This is what gets planned.
2. `sheerline/os/foundations/user-research/FOUNDATION.md` — the area-1 governed context. Register under it; do not author it. Its § "The knowledge canon" method-selection row and Faulkner standard are the spine of Step 2.
3. `references/research-plan-canon.md` — the method-selection framework (generative vs. evaluative; the Opportunity-Solution-Tree framing), the **Faulkner-corrected sample-size standard** with its worked floors, and the consent/ethics checklist. THE method spine.
4. `references/worked-example.md` — a filled Research Plan on synthetic input. Read it to calibrate the register and depth of the free-prose slots (open questions, method notes); do not copy its findings.
5. The engagement-intake resolution (`sheerline/profile/engagement-intake.yaml`) — the client's voice source (`brand_voice_source` / `voice_prohibited`), the hermetic-seal state (`hermetic_seal_confirmed`), and any engagement-specific `do_not_automate` calls. Skill output copy uses the client's voice, never HeyHi's; no client name appears on a shared artifact when the seal is confirmed.

## Step 2: Build the plan, mechanically

Each step below is mechanical work. None of it locks the question, selects the method, or declares the study a go.

1. **Restate the research question (candidate).** Turn the stated goal into one or more crisp, answerable research questions — the version a study could actually be designed around. Every restatement is a **candidate**, labeled so. Naming a vague goal's hidden ambiguity ("is 'trust' about the results' accuracy or the brand's reputation? Those need different studies") is part of the restatement; resolving it is the human's.
2. **Lay out candidate methods.** For each candidate question, derive the methods that could answer it, tagged **generative** (widen the problem space — interviews, diary, contextual inquiry) or **evaluative** (test a design — usability test, tree test, A/B, heuristic evaluation). Say what each answers and what it cannot. Every method is a **candidate**; the comparison does not pick one.
3. **Wire the honest sample-size basis into every method.** For each candidate *discovery* method (usability tests, interviews — finding problems), state the sample size its stated confidence demands under the Faulkner floor — **5 for directional, 10 for a reliable mean, 20 for a ≥95% detection floor** — never the folk "5 users = 85%." For each *quantitative* method (a survey, an A/B or completion-rate comparison, analytics), the n is a **power calculation** (baseline + minimum detectable effect + confidence), not the 5/10/20 floor — say so rather than forcing a usability number onto it (canon § 2). Either way, if the plan (or the human's stated constraint) sits **under** what its claimed confidence demands, **flag it**: an under-powered plan is a finding, not a silent pass. Name the recruit target the instruments will need.
4. **Draft the consent + ethics checklist.** Assemble the consent, participant-welfare, and data-handling checklist the study needs: informed consent, recording/permission, right to withdraw, incentive handling, PII minimization and storage, and — where the study ingests transcripts or recordings — the untrusted-content-at-the-write-boundary note (neutralize and provenance-stamp on ingest). This is a checklist for a human to complete and confirm, not a claim that consent is handled.
5. **Surface the open questions.** What the goal artifact does not answer and what you would ask the research owner / design lead before the study is locked — each a question that, answered, would firm up the plan. No recommendation.

## Step 3: Produce the Research Plan

Output this exact structure. The question-lock, method-selection, and go slots stay empty by construction; the open-questions surface carries questions, never recommendations.

```
# Research Plan — [study / goal name]
Source: [artifact]        Drafted: [date]

## Research question (candidate — the human locks it)
[Restated, sharpened candidate question(s) derived from the stated goal, each labeled
 [candidate — agent-drafted]. Name any ambiguity in the goal without resolving it.]

## Method options (candidates)
| Candidate method | Generative / Evaluative | What it answers | What it cannot | Sample-size basis (n for the stated confidence) | Fieldwork cost |
|------------------|-------------------------|-----------------|----------------|-----------------------------------------------------|----------------|
| Moderated usability test | Evaluative | where the flow breaks, why | frequency/rates | 5 (directional) / 10+ (reliable) | med |
| …                | …                       | …               | …              | …                                                   | …              |

All methods above are AGENT-DRAFTED CANDIDATES — see provenance. None is selected.

## Faulkner sample-size basis
[The standard applied and which target this plan assumes: 5 directional / 10 reliable-mean /
 20 for a ≥95% detection floor. State the recruit target per method. FLAG any option whose
 stated confidence exceeds what its n supports — an under-powered plan named, not hidden.]

## Consent + ethics checklist (for the human to complete)
- [ ] Informed consent captured (purpose, use, retention stated to participant)
- [ ] Recording / screen-capture permission
- [ ] Right to withdraw, without penalty
- [ ] Incentive handling stated
- [ ] PII minimized; storage + retention + deletion named
- [ ] Ingested transcripts/recordings neutralized + provenance-stamped at the write boundary
[Add engagement-specific items from engagement-intake do_not_automate.]

## Open questions for the team (questions, not judgments)
- [e.g. "Is 'trust' the results' accuracy or the brand's reputation? Different studies."]
- [e.g. "What decision does this research feed, and by when? That bounds the method."]

## ⛔ Research question — NEEDS HUMAN
This slot is intentionally empty. The final question the study is designed around is the
team's to lock.
   Locked question(s): ____________________

## ⛔ Method selection — NEEDS HUMAN
Which candidate method the team runs is a study-design judgment, not a mechanical one.
   Chosen method(s): ____________________

## ⛔ Go decision — NEEDS HUMAN
   Proceed / revise / hold: ____________________

## Real-user validation — NEEDS HUMAN
This is a research plan, drafted and reviewed for study design, not evidence from real users;
and naming participants is not the same as genuine, naive-participant access — a convenience
proxy (a teammate or stakeholder standing in for a user) is not the population the question is
about. Whether the recruit reaches real, naive users, and who confirms it, is not this skill's
call — see operating-principles.md "What stays human."
   Real-user validation run?  yes / no / not-applicable: ____________________
   If yes, by whom and how:   ____________________

## Named gate
Sign-off owner (research owner / design lead): ____________________  Date: ______
No question, method, or go decision is recorded until this line is signed by a human.
```

**The plan is done when every candidate question has method options, every method carries a sample-size basis — the Faulkner floor for discovery methods, a power calculation for quantitative ones — with any under-powered option flagged, the consent checklist is drafted, the open-questions surface carries questions, and the question-lock + method-selection + go slots are still blank.**

## Step 4: Pre-flight verification

Confirm: no candidate question was silently locked, no candidate method was silently selected, and the go slot is empty; every question and method is labeled `[candidate — agent-drafted]`; every method carries a sample-size basis (the Faulkner floor for discovery methods, a power calculation for quantitative ones) and any plan under what its stated confidence demands is flagged (not silently passed); the consent checklist is present; each open question is phrased as a question, not a recommendation; the real-user-validation slot is present with its run-line blank; the copy uses the client's voice per `engagement-intake.yaml` and carries no client name when `hermetic_seal_confirmed` is true; anything modeled or illustrative is tagged `synthetic`.

---

## What is explicitly out of scope

- **Locking the question, selecting the method, and the go decision.** Empty by construction. The plan lays out the options and their sample-size floors; the human chooses and signs.
- **Running the study.** This produces the plan, not the fieldwork.
- **Writing the instruments.** The plan names the screeners / guides / task-scripts the study needs and the sample they must recruit; drafting them is `instrument-smith` (held on engagement pull).
- **Synthesizing results.** Coding, theming, disconfirming passes, the outlier audit — `synthesis-pipeline` (held on corpus thickness), which works after the data is in.
- **Sales/qualification discovery** — `heyhi-discovery-call`. **Organizational foresight** — `futurecasting`.

---

## Exit Gate Required Headers (bottom-of-skill bracket)

This skill closes through Exit Gate Flavor A (`CLAUDE-SESSION-RULES.md § Exit Gate`). Before declaring done, confirm every required header holds real content:

- `## Fixes Applied` (or the delivered Research Plan)
- `## Smoke Test` (the Step 4 pre-flight checks, pasted)
- `## Next Session Prompt`

If the question-lock, method-selection, or go slot is filled, the gate has **not** been satisfied.

---

*HeyHi Confidential. Sheerline area 1 (User Research), P3, build class N. Tier 1 (buildable-now, self-application-first) — deployed 2026-09-04 (v0.1.0), registered in both registries. Spec source: `plans/plan-sheerline-p3-ur-ia-foundations-2026-08-29.md` § 1.2 / § 4.1 / § 4.4. Foundation: `sheerline/os/foundations/user-research/FOUNDATION.md`. Boundary: `sheerline/os/operating-principles.md`.*
