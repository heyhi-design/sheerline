---
name: design-measurability-mapper
description: >-
  Answer one question about a design goal or product bet — "is this measurable
  at all?" — and build the Goals→Signals→Metrics scaffold that makes the answer
  legible. Runs the mechanical work: a G→S→M traceability table, an
  instrumentation audit (would the signal actually be captured today), a gaming
  / Goodhart stress-test, candidate guardrail (counter-metric) drafting, and an
  unmeasurable-as-designed flag. Triggers: "is this measurable", "how would we
  measure this", "build a goals-signals-metrics map", "what should we track for
  this feature", "measurability check". Produces a Measurability Map where which
  signal becomes the metric, which guardrails to adopt, and what the target is
  ship EMPTY behind a named human gate — metric selection is a values decision,
  not a mechanical one. NOT for auditing a completed experiment readout (use
  experiment-readout-linter). NOT for auditing an opportunity or JTBD artifact's
  reasoning (use strategy-integrity-warden). NOT for a design system's own
  adoption metrics (that is design-system-care-monthly /
  heyhi-design-intelligence-audit territory).
version: "0.2.0"
updated: "2026-08-23"
status: "deployed — heyhi-skills/; v0.2.0 promoted 2026-08-23 (Gate G-C, plans/plan-sheerline-skills-upgrade-2026-08-22.md) — adds attitudinal/qualitative signal-class guidance, candidate guardrail drafting, open-questions + near-misses surfaces, a worked example, 2 eval cases (5→7). v0.1.0 promoted 2026-08-15 (DISPATCH-D). Sheerline area 9 (Design Strategy), P1.5. Registered in skill-registry.yaml v2.35.0."
classification: HeyHi Confidential
---

# Design Measurability Mapper

**Sheerline area 9 (Design Strategy & Product Thinking) · P1.5 · pure validate/audit skill.** A team states a design goal — "make onboarding feel effortless," "increase trust in the results." This skill does the chartered measurement job: it maps the goal to candidate signals and candidate metrics, checks whether those signals are even *capturable* today, stress-tests each for gaming, drafts the counter-metric that would catch that gaming, and flags goals that are **unmeasurable as designed**. It stops at the point where a human must choose *which* signal to elevate to the metric, *which* guardrails to adopt, and *what* number counts as good. Those choices are values decisions.

**The boundary this skill obeys (Sheerline § 9, absolute).** A structured artifact with explicit empty judgment slots, a named human gate, and provenance labels on anything synthetic. *Metric selection, guardrail selection, and target-setting are the empty slots.* Building the traceability scaffold — including drafting candidate guardrails and naming the *class* of instrument an unmeasurable goal would need — is mechanical; choosing what the team will be held to is judgment. A version of this skill that picks the North Star, adopts a guardrail, or sets the target has exceeded its charter. Grades never gates; mechanics never taste. Drafting a candidate is not selecting it — the candidate widens the human's options; it does not narrow them to a choice.

> **This skill closes through the Exit Gate (`CLAUDE-SESSION-RULES.md § Exit Gate`).** See the bottom-of-skill bracket.

---

## Routing — disambiguation with sibling skills

| If the task is… | Use |
|---|---|
| "Is this design goal measurable, and what's the G→S→M scaffold?" (upstream, before the experiment) | **this skill** |
| Auditing a completed A/B / experiment readout for integrity (downstream) | `experiment-readout-linter` |
| Auditing an opportunity / JTBD / prioritization artifact's *reasoning* | `strategy-integrity-warden` |
| Tracking a **design system's** adoption / token-drift / component health | `design-system-care-monthly`, `heyhi-design-intelligence-audit` |
| Choosing the metric, adopting the guardrails, or setting the target | **the human** (this skill's named gate) |

The seam with `experiment-readout-linter` is temporal: this skill works *before* there is a result (is there a measurable signal to test); the linter works *after* (was the test honest). The seam with the design-system audit skills is object: they measure the *system's own* adoption; this measures a *product/design outcome*.

---

## Step 0: Improvement hook check

Retrieve any recurring corrections for measurement/strategy work (`retrieve_design_corrections` or the Sheerline `os/corrections/` registry). Fold a match into the pass. Skip silently if none.

## Step 1: Load context

1. The **goal artifact** the human brought — a product brief, a feature one-pager, a stated design goal, an OKR draft. This is what gets mapped.
2. `references/measurability-canon.md` — HEART, the Goals→Signals→Metrics method, the attitudinal/qualitative signal-class taxonomy, the guardrail-candidate method, the no-validation caveat, the North-Star gaming critiques, and the unmeasurable-as-designed test. THE method spine.
3. `references/worked-example.md` — a filled Measurability Map on synthetic input. Read it to calibrate the register and depth of the free-prose slots (open questions, near-misses, the unmeasurable flag); do not copy its findings.
4. The Sheerline area-9 governed context (`sheerline/os/foundations/registry.yaml` area-design-strategy; the area-9 foundation is deferred to P3, though a manifest-grade foundation is under consideration — Wave G). Register under it; do not author it.

## Step 2: Build the map, mechanically

Each column below is mechanical work. None of it selects the metric, adopts a guardrail, or sets a target.

1. **Goals → Signals → Metrics traceability.** For each stated goal, derive candidate *signals* (observable user behaviors — or attitudes — that would move if the goal were met) and, under each signal, candidate *metrics* (a specific measurable expression). Every signal and metric the agent drafts is a **candidate**, labeled so — see provenance. When a goal is about a *feeling* (trust, confidence, effort, satisfaction), reach for the **attitudinal/qualitative signal-class taxonomy** in the canon: name the *class of instrument* the goal would need (attitudinal self-report, task-based, generative-qualitative, behavioral-proxy), still as a candidate, never as a picked metric.
2. **Instrumentation audit.** For each candidate metric, ask: is the event (or the instrument) that produces it *actually captured today*? Tag each `instrumented` / `capturable-not-instrumented` / `not-capturable`. A metric that depends on an event nobody logs — or an attitude no survey captures — is not a metric yet; it is a request for instrumentation.
3. **Gaming / Goodhart stress-test.** For each candidate metric, state how a team optimizing it would game it, and the perverse incentive that follows ("time-on-page" rewards confusion; "tickets closed" rewards premature closure). This is the honest counter to every metric, surfaced next to it, not hidden.
4. **Candidate guardrail (counter-metric) drafting.** For each candidate primary metric, draft the **counter-metric that would catch the gaming path named in step 3** — the thing that would move the wrong way if the primary were gamed (for "sessions per user," the guardrail catching notification-spam gaming is unsubscribe / mute rate; for "time-to-first-value," the guardrail catching rush-users-past-setup is downstream activation / early-churn). These are *candidates*, labeled, and drafting them is mechanical: the counter-metric follows from the gaming path. **Which guardrails the team actually adopts stays in the empty selection slot** — drafting the candidate is not adopting it.
5. **Unmeasurable-as-designed flag.** Flag any goal with no capturable signal — the honest answer to "is this measurable at all?" is sometimes *no, not as currently framed*. That flag is a finding, not a failure; it hands the team a real choice (instrument the missing signal-class, reframe the goal, or accept it stays a qualitative intent). Naming the signal-*class* the goal would need (per the taxonomy) is part of the flag; picking the instrument is not.

## Step 3: Produce the Measurability Map

Output this exact structure. The selection, guardrail-adoption, and target slots stay empty by construction; the open-questions and near-misses surfaces carry questions and traces, never recommendations.

```
# Measurability Map — [goal / feature name]
Source: [artifact]        Mapped: [date]

## Goals → Signals → Metrics
| Goal | Candidate signal | Candidate metric | Instrumentation | Gaming risk | Candidate guardrail |
|------|------------------|------------------|-----------------|-------------|---------------------|
| Effortless onboarding | time-to-first-value | median mins to first saved map | capturable-not-instrumented | rushes users past setup | downstream 7-day activation rate |
| …    | …                | …                | instrumented / not-capturable | … | … |

All signals, metrics, and guardrails above are AGENT-DRAFTED CANDIDATES — see provenance.

## Signal-class note (for feeling/attitude goals)
[When a goal is about a perception, name the instrument CLASS it would need — attitudinal
 self-report (e.g. an in-product confidence/effort survey battery), task-based
 (moderated/unmoderated usability), generative-qualitative (interviews, diary, open-text),
 or behavioral-proxy — as candidate options. Do NOT pick the instrument or the metric.]

## Unmeasurable-as-designed
[Goals with no capturable signal, stated plainly, with the signal-class they would need.
 Empty if every goal has one.]

## Open questions for the team (questions, not judgments)
[What the goal artifact does not answer and what you would ask the PM / design lead.
 Each is a question that, answered, would change or firm up the map. No recommendation.]
- [e.g. "Is 'trust' here about the results' accuracy or the brand's reputation? They need
   different signal classes."]
- [e.g. "Is there appetite to instrument an attitudinal survey, or must this stay
   behaviorally inferred?"]

## Near-misses and unchecked territory (the mapping journey, made inspectable)
[Signal classes considered and set aside, metrics that looked capturable but aren't, goals
 that almost got an unmeasurable flag. Traces, no verdicts.]
- Considered, set aside: [e.g. "NPS as a trust proxy — set aside, it measures advocacy, not
   trust in the results specifically."]
- Almost flagged unmeasurable: [e.g. "'effortless' looked unmeasurable until time-to-first
   -value surfaced as a capturable-not-instrumented signal."]
- Could not check: [e.g. "whether the survey vendor supports in-product batteries — outside
   the artifact."]

## ⛔ Metric selection — NEEDS HUMAN
This slot is intentionally empty. Which candidate signal becomes THE metric the
team is held to is a values decision (what does this team choose to care about?),
not a mechanical one.
   Chosen primary metric(s):    ____________________
   Adopted guardrail / counter-metrics (from the candidates above, or others): ____________________

## ⛔ Targets — NEEDS HUMAN
   What number counts as success: ____________________

## Named gate
Sign-off owner (metric owner / PM / design lead): ____________________  Date: ______
No metric, guardrail, or target is recorded until this line is signed by a human.
```

**The map is done when every goal has a traceability row (or an unmeasurable-as-designed flag), every candidate metric carries an instrumentation tag, a gaming note, and a candidate guardrail, the open-questions and near-misses surfaces carry questions/traces, and the selection + guardrail-adoption + target slots are still blank.**

## Step 4: Pre-flight verification

Confirm: no candidate metric was silently promoted to "the metric" and no candidate guardrail was silently "adopted"; every signal/metric/guardrail is labeled `[candidate — agent-drafted]`; the selection, guardrail-adoption, and target lines are empty; each gaming note is specific to its metric (not a generic "beware Goodhart") and each candidate guardrail catches the gaming path named beside it; any imported dashboard figure carries a source, and anything modeled is tagged `synthetic`. New in v0.2.0: confirm every attitude/feeling goal names an instrument *class* (not a picked instrument); confirm every open question is phrased as a question and every near-miss is a trace with no verdict.

---

## What is explicitly out of scope

- **Metric selection, guardrail adoption, and target-setting.** Empty by construction (§ 9). The skill lays out the options, their gaming risks, and the counter-metrics that would catch each; the human chooses.
- **Claiming a candidate metric is validated.** The no-validation caveat holds: a HEART/GSM metric is a *proposal to measure*, not evidence the thing works. Never present the scaffold as proof.
- **Picking the instrument for an attitudinal goal.** The skill names the signal *class* the goal needs; which survey/interview protocol to run, and what it must score, is the human's (and a downstream research-craft task).
- **Design-system adoption metrics** — `design-system-care-monthly` / `heyhi-design-intelligence-audit`. **Completed-experiment integrity** — `experiment-readout-linter`. **Opportunity/JTBD reasoning** — `strategy-integrity-warden`.

---

## Exit Gate Required Headers (bottom-of-skill bracket)

This skill closes through Exit Gate Flavor A (`CLAUDE-SESSION-RULES.md § Exit Gate`). Before declaring done, confirm every required header holds real content:

- `## Fixes Applied` (or the delivered Measurability Map)
- `## Smoke Test` (the Step 4 pre-flight checks, pasted)
- `## Next Session Prompt`

If the metric-selection, guardrail-adoption, or target slot is filled, the gate has **not** been satisfied.

---

*HeyHi Confidential. Sheerline area 9 (Design Strategy & Product Thinking), P1.5 net-new. v0.1.0 deployed 2026-08-15 (DISPATCH-D); registered in `skill-registry.yaml` v2.32.0. v0.2.0 staged 2026-08-23 (Wave D, `plans/plan-sheerline-skills-upgrade-2026-08-22.md`). Spec source: `ai-services/design-intelligence/research/sheerline-skill-buildout-research-2026-08-09.md` § 6.1 / § 8; attitudinal signals, guardrail candidates, and curiosity surfaces from the 2026-08-22 skills audit § 2.4 / § 5. Boundary: § 9.*
