---
classification: confidential
title: "Worked example — a filled Measurability Map"
skill: design-measurability-mapper
loaded_by: "SKILL.md Step 1 (calibration)"
---

# Worked example — Measurability Map

A filled golden map, start to finish, on a **synthetic, invented** goal. No client content; every artifact detail below is fabricated for calibration. Read it to anchor register and depth on the free-prose slots (the signal-class note, the unmeasurable flag, open questions, near-misses). Do not copy its findings.

This example is built to exercise the three things v0.2.0 adds: an **attitudinal goal that lands as unmeasurable-as-designed with its signal *class* named** (not an instrument picked), **candidate guardrails drafted from the gaming paths**, and populated **open-questions / near-misses** surfaces that carry questions and traces. Note that the selection, guardrail-adoption, and target slots stay empty even though the map makes the shape of a good answer visible.

---

## The input (synthetic goal artifact the human brought)

> **Feature brief: "Recommendations that teams trust and act on"** *(invented)*
> "Our insights dashboard surfaces recommendations. Two goals for this quarter:
> (1) the recommendations should **feel trustworthy** to the team reading them, and
> (2) teams should **act on** them more often.
> Today we log: which recommendation cards are viewed, expanded, and dismissed. There is no
> survey instrument in the product and no 'accepted / implemented' event."

---

## The filled map

```
# Measurability Map — Recommendations teams trust and act on (SYNTHETIC)
Source: feature brief (invented)        Mapped: 2026-08-23

## Goals → Signals → Metrics
| Goal | Candidate signal | Candidate metric | Instrumentation | Gaming risk | Candidate guardrail |
|------|------------------|------------------|-----------------|-------------|---------------------|
| (1) Recommendations feel trustworthy | stated confidence in a recommendation | post-view confidence rating (1–5) | not-capturable (no survey instrument today) | users click a rating to dismiss the prompt, not to report a belief | response rate + straight-lining rate on the survey |
| (2) Teams act on recommendations | recommendation acted-on | % of surfaced recs marked accepted within 7 days | capturable-not-instrumented (no "accept" event logged) | one-click "accept" inflates without real action | downstream: % accepted recs still in effect / not reversed at 30 days |
| (2) Teams act on recommendations | engagement precursor to acting | expand-to-view ratio on rec cards | instrumented (view + expand logged today) | expands driven by curiosity, not intent to act | dismiss-after-expand rate |

All signals, metrics, and guardrails above are AGENT-DRAFTED CANDIDATES — see provenance.

## Signal-class note (for feeling/attitude goals)
Goal (1) "feel trustworthy" is an attitudinal goal. Behavioral logs cannot see a feeling,
so it needs a signal from the ATTITUDINAL SELF-REPORT class (a post-view confidence or trust
rating), or from the GENERATIVE-QUALITATIVE class (interviews / open-text) to understand the
why. Standardized batteries exist as references (a confidence/trust Likert battery), but which
instrument to field, what items it carries, and what score counts as "trusted" are research-
craft and values calls, not this map's to make. A behavioral proxy (return-to-recommendation
rate) is available today but is a proxy — it can move for reasons unrelated to trust.

## Unmeasurable-as-designed
Goal (1) is unmeasurable as currently built: no attitudinal instrument exists, so trust is
`not-capturable` today. The honest choices are — instrument an attitudinal self-report signal,
reframe the goal toward a behavioral proxy the team accepts as a stand-in, or hold "trust" as
a qualitative intent judged by the team. The map names the class; the team makes the choice.

## Open questions for the team (questions, not judgments)
- Is "trustworthy" here about the recommendations' accuracy, or about how the team feels
  toward the product's judgment? Those point at different instruments.
- Is there appetite (and a vendor) to field an in-product confidence survey, or must goal (1)
  stay behaviorally inferred this quarter?
- What does "act on" mean operationally — clicking accept, or the recommendation actually
  being implemented downstream? The two are logged very differently.
- Would a "reversed within 30 days" event be feasible to capture, since it is the guardrail
  the acted-on metric most needs?

## Near-misses and unchecked territory (the mapping journey, made inspectable)
- Considered, set aside: NPS as a trust proxy — set aside, it measures advocacy of the
  product, not trust in a specific recommendation.
- Almost flagged unmeasurable: goal (2) looked unmeasurable until the existing view/expand
  logs surfaced expand-to-view as an already-instrumented precursor signal.
- Could not check: whether an "accepted" event is technically cheap or expensive to add —
  that is an engineering question outside the brief.
- Could not check: base rates — the brief gives no current view/expand/dismiss numbers, so
  every candidate metric here is a shape, not a calibrated baseline.

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

---

## Why this is a good golden

- **The attitudinal goal lands honestly.** "Feel trustworthy" is flagged unmeasurable-as-designed with its signal *class* named (attitudinal self-report / generative-qualitative) — it does not fabricate a clickstream proxy and call it trust, and it does not pick the survey or the target.
- **Guardrails are drafted, not adopted.** Every candidate primary carries a counter-metric that catches its specific gaming path (one-click-accept inflation → reversed-at-30-days), and the guardrail-*adoption* line stays empty.
- **The empty slots hold under a map that clearly implies a good answer.** A reader can see the shape of the right metric set; the map still refuses to select it.
- **Open questions are questions; near-misses are traces.** Each open question could be answered in a way that reshapes the map (maybe "act on" really does mean one-click accept); each near-miss records a consideration or a gap with no verdict attached.

*HeyHi Confidential. Worked example for `design-measurability-mapper` v0.2.0. Fully synthetic; added 2026-08-23 (Wave D) per the 2026-08-22 skills audit § 4 (no worked examples) and § 2.4 / § 5.*
