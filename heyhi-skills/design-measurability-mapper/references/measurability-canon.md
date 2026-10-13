---
classification: confidential
title: "Measurability canon — the method spine"
skill: design-measurability-mapper
loaded_by: "SKILL.md Step 1"
---

# Measurability canon

The measurement frameworks behind the Measurability Map, held as *read-and-apply reference*, never as a metric generator that picks for the team. On-demand — load when running the mapper.

*Internal operational reference (deployed under `heyhi-skills/`): em-dash limit exempt per `OPERATING_PRINCIPLES.md`. Framework provenance stated inline.*

---

## Goals → Signals → Metrics (GSM)

Google's chain. A **goal** is what you want to happen (usually stated in human terms). A **signal** is an observable behavior — or attitude — that would change if the goal were met. A **metric** is a specific, capturable expression of a signal. The discipline: never jump from goal straight to metric — the signal is the missing middle that keeps the metric honest to the goal.

- One goal usually yields several candidate signals; each signal, several candidate metrics. Lay them out as a tree, do not pre-collapse to one.
- The value of the scaffold is *tracing* — a metric with no line back to a goal is a vanity metric; a goal with no signal is unmeasurable as designed.

## HEART (the dimensions to check a product goal against)

Happiness, Engagement, Adoption, Retention, Task success. Use HEART as a *checklist of dimensions* a goal might live in, not as five metrics to fill in. Many goals touch only one or two; forcing all five manufactures metrics nobody needs.

**Happiness is the attitudinal dimension.** When a goal lives here ("feels trustworthy," "feels effortless," "is satisfying"), the signal is a *perception*, not a click — which is exactly where the taxonomy below is needed, because clickstream alone cannot see a feeling.

**The no-validation caveat (load-bearing).** A HEART or GSM metric is a *proposal to measure*, not evidence the design works. The scaffold says "here is how you could tell"; it never says "and it is working." Presenting the map as validation is the exact overclaim this skill's boundary exists to prevent.

## Attitudinal and qualitative signal classes (v0.2.0)

When a goal is about a **feeling or perception** — trust, confidence, effort, satisfaction, delight — behavioral logs usually cannot see it, so the honest instrumentation state is often `not-capturable` *until an attitudinal instrument is added*. The mapper's chartered job here is to name the **class** of instrument the goal would need, as candidate options for the human to weigh. Naming the class is enumeration (mechanical); picking the instrument, writing its items, or setting what score counts as good is judgment (out of charter).

The four signal classes to draw from:

| Signal class | What it captures | Instrument options (candidates, not picks) | What it cannot do |
|---|---|---|---|
| **Attitudinal self-report** | Stated perception / feeling | In-product micro-survey or Likert battery; task-level single-ease question (SEQ); post-task confidence rating; standardized batteries as *references* (SUS for usability, UMUX-Lite, CSAT, an experience-sampling prompt) | It measures what people *say*, which can diverge from what they do; needs enough responses to be stable |
| **Task-based / observational** | Demonstrated ability, effort, error | Moderated or unmoderated usability test; task success + time-on-task; error / recovery rate | Captures ability, not feeling; small-n and situational |
| **Generative-qualitative** | The *why* behind a behavior or feeling | Interviews, diary study, open-text feedback, session-replay review | Rich but not a metric — it explains, it does not quantify; do not force a number onto it |
| **Behavioral proxy for attitude** | A behavior that *correlates* with the feeling | Return frequency, unprompted feature re-use, referral / share, opt-in retention | It is a proxy — it can move for reasons unrelated to the feeling, so it needs the gaming stress-test hardest |

**The discipline.** For an attitudinal goal, the map states: "this goal needs a signal from the *attitudinal self-report* class (or *generative-qualitative* for the why); no such instrument exists today, so it is `not-capturable` until one is added." That is the honest, in-charter answer. It does **not** say "run an SUS survey and target 80" — that picks the instrument (research-craft) and sets the target (the human's values call). The class is the candidate; the instrument and the number are not the mapper's to choose.

## Candidate guardrail (counter-metric) drafting (v0.2.0)

Every primary metric invites gaming (see below). A **guardrail** (counter-metric) is the metric that would move the wrong way if the primary were gamed — the tripwire that catches the perverse incentive. Drafting a guardrail *candidate* is mechanical: it follows directly from the gaming path.

- The gaming note says *how* the metric would be gamed. The guardrail candidate is *what would detect that*.
- Worked pairings (the guardrail candidate follows the gaming path):
  - Primary "sessions per user per week" → gamed by notification spam / session fragmentation → **guardrail candidate: unsubscribe / mute rate, or sessions-per-*task*** (catches fragmentation).
  - Primary "time-to-first-value" (lower is better) → gamed by rushing users past setup → **guardrail candidate: downstream 7-day activation or early-churn** (catches hollow speed).
  - Primary "tickets closed" → gamed by premature closure → **guardrail candidate: reopen rate / CSAT on closed tickets**.
  - Primary "add-to-cart rate" → gamed by friction-free adds that don't convert → **guardrail candidate: checkout-completion and refund rate**.
- **The boundary.** The map *drafts* guardrail candidates and labels them candidates. *Which* guardrails the team adopts — and what bound counts as a breach — stays in the empty selection slot. A drafted counter-metric is an option placed in view; adopting it is the human's. This closes the candidate asymmetry the 2026-08-22 audit named: the map used to draft primary-metric candidates but hand the human an empty guardrail line with nothing to react to.

## The North Star and its gaming critiques

A single North-Star metric focuses a team, but every North Star invites Goodhart's law: *when a measure becomes a target, it ceases to be a good measure.* The mapper's job is to surface the gaming path next to each candidate — and now the counter-metric that would catch it — so the human choosing the metric chooses with the perverse incentive and its tripwire in view.

**Common gaming patterns to name (per metric, specifically):**
- **Proxy inflation** — optimizing the proxy, not the goal (time-on-page rewards confusion, not value).
- **Denominator games** — improving a rate by shrinking who counts.
- **Counting the easy thing** — "tickets closed" rewards premature closure; "features shipped" rewards small features.
- **Guardrail blindness** — the primary rises while an unwatched counter-metric (retention, complaints, latency) moves the wrong way. (This is the pattern the guardrail-candidate step exists to pre-empt.)

A metric with no plausible gaming path usually means the stress-test was not run hard enough, not that the metric is safe.

## The instrumentation audit

The question that separates a metric from a wish: **is the event (or the instrument) that produces this metric captured today?** Three honest states:
- `instrumented` — the event / instrument is logged; the metric is computable now.
- `capturable-not-instrumented` — the event could be logged, or the survey could be run, but is not; the metric is a request for instrumentation, not a metric yet.
- `not-capturable` — nothing in the current product would ever produce this signal; the goal is unmeasurable as built (common for attitudinal goals with no survey instrument).

Naming the state prevents the most common measurement fiction: a dashboard of metrics half of which nothing actually feeds.

## The unmeasurable-as-designed flag

Sometimes the honest answer to "is this measurable at all?" is **no, not as currently framed.** That is a finding, not a failure. It hands the team a real, in-view choice: instrument the missing signal-class (name the class per the taxonomy above), reframe the goal so a capturable signal exists, or accept that the goal stays a qualitative intent held by human judgment (some design goals — "feels trustworthy" — are legitimately in the don't-force-a-number category until a team decides to instrument for them). The skill surfaces the choice and names the signal-class; it does not resolve the choice or pick the instrument.

---

## The two curiosity surfaces (open questions, near-misses) — why they are not verdicts (v0.2.0)

Both exist to make the map a thinking instrument, and both stay inside § 9 because neither renders a decision:

- **Open questions for the team** are questions to the PM / design lead — what the goal artifact does not resolve, what would change the map. Every entry ends in a question mark and asks rather than tells. "Is 'trust' about accuracy or reputation?" is in charter; "You should split trust into two goals" is a recommendation and is out.
- **Near-misses and unchecked territory** are the mapping journey's trace: signal classes considered and set aside, metrics that looked capturable but aren't, goals that almost got an unmeasurable flag. It renders no verdict — it shows where the map's confidence is thin.

---

## Why selection, guardrails, and targets ship empty

Which candidate signal a team elevates to *the* metric encodes what the team chooses to care about and be held to — a values decision. Which guardrails it adopts, and what bound counts as a breach, is a commitment. What number counts as "good" is a commitment, not a calculation. All three are the judgment slots. The mapper can show every option, its instrumentation state, its gaming risk, and the counter-metric that would catch it; the choosing is the human's. A mapper that returns "your North Star should be X, guardrail Y, target Z" has quietly made the three decisions the boundary reserves for people.

## Provenance discipline for this skill

Every signal, metric, and guardrail the mapper writes is agent-drafted and labeled `[candidate — agent-drafted]`. It is a proposal, never a measured value or an endorsed choice. Any number pulled from an existing dashboard carries its source; anything modeled or projected is tagged `synthetic` so a candidate map can never be mistaken for a live measurement.

*HeyHi Confidential. Reference for `design-measurability-mapper`. Spec source: `sheerline-skill-buildout-research-2026-08-09.md` § 6.1; attitudinal signal classes + guardrail candidates added v0.2.0 per the 2026-08-22 skills audit § 2.4.*
