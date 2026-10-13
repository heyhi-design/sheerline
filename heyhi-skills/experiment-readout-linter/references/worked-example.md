---
classification: confidential
title: "Worked example — a filled Readout Integrity Report"
skill: experiment-readout-linter
loaded_by: "SKILL.md Step 1 (calibration)"
---

# Worked example — Readout Integrity Report

A filled golden report, start to finish, on a **synthetic, invented** experiment. No client content; every number below is fabricated for calibration. Read it to anchor the register and depth of the free-prose slots (confidence framing, open questions, near-misses). Do not copy its findings into a real run.

This example is built to fire the two things v0.2.0 adds: a **SRM FLAG that eyeballing would miss** (the split reads as balanced and is not) and populated **open-questions / near-misses** surfaces that carry questions and traces, never a recommendation. Note especially that the ship slot stays empty even though the reader can feel where the evidence points — that pull toward "so don't ship" is exactly what the boundary holds back.

---

## The input (synthetic readout the human brought)

> **Experiment: Quick-Add on the cart page** *(all figures invented)*
> "We shipped a one-tap Quick-Add control to the product card. Variant B (Quick-Add) vs
> Control (existing two-step add). Designed 50/50. Ran 9 days.
> - **Add-to-cart rate: +2.1% relative (B over Control), p = 0.008.** Primary metric,
>   fixed in the test plan before launch.
> - Samples: **Control 101,200 users, Variant B 98,800 users.**
> - MDE was set at 1.5% relative with 80% power; n cleared the plan.
> - Guardrails: checkout-completion rate flat (p = 0.6); refund rate flat.
> - Baseline add-to-cart rate **8.0%** (from last quarter's funnel model).
> - Recommendation: B wins, ship to 100%."

---

## The filled report

```
# Readout Integrity Report — Quick-Add on the cart page (SYNTHETIC)
Source readout: pasted summary (invented example)          Audited: 2026-08-23

## Mechanical checks
| # | Check | Verdict | Evidence / what triggered it |
|---|-------|---------|------------------------------|
| 6 | Sample-ratio mismatch (SRM) | FLAG | Designed 50/50; observed 101,200 / 98,800 (N=200,000). χ² = (2·101,200 − 200,000)²/200,000 = 2,400²/200,000 = 28.8, 1 df → p ≈ 8e-8, far past the p<0.001 flag. The 50.6/49.4 split looks balanced but is a randomizer defect at this N. |
| 1 | Peeking / optional-stopping | UNKNOWN — not reported | No stopping rule stated; "ran 9 days" is a duration, not a pre-declared horizon or sequential method. Cannot confirm the 9-day stop wasn't a stop-on-significance. |
| 2 | Power / sample sufficiency  | PASS (moot) | MDE 1.5% rel at 80% power declared up front, n cleared it. But power is computed off the arm sizes SRM just impugned, so the PASS is moot until the split is explained. |
| 3 | Back-solved primary metric  | PASS | Add-to-cart named as primary in the test plan before launch; not swapped after results. |
| 4 | Single-method over-reliance | PASS (with a note) | Two guardrails reported (checkout-completion, refund), both flat — better than the report-only-what-moved tell. No qual/holdback triangulation, but not a single-metric readout. |
| 5 | Provenance                  | FLAG | Baseline add-to-cart 8.0% is a MODEL output ("last quarter's funnel model") sitting in the same list as measured numbers. Tag `synthetic`. The +2.1% relative lift, if read against a modeled baseline, is not a measured delta. |

## Provenance ledger
| Headline number | Source | Provenance tag |
|-----------------|--------|----------------|
| +2.1% rel add-to-cart | experiment analytics (unnamed query) | analytics-query (source not named) |
| p = 0.008 | experiment analytics | analytics-query |
| Control 101,200 / B 98,800 | experiment logs | analytics-query |
| Baseline 8.0% | last quarter's funnel model | synthetic |

## Confidence framing (honest, not a grade)
The arms are unbalanced beyond chance (SRM χ² = 28.8, p ≈ 8e-8), so the randomizer is
suspect — a redirect, a bot filter, or a late-instrumented arm can produce exactly this.
Until that imbalance is explained, the two groups are not exchangeable and the +2.1% cannot
be read as a clean treatment effect, no matter how small the p-value looks. Two secondary
issues stand behind it: the stopping rule was not reported, and the 8.0% baseline is a model
output presented alongside measured numbers. The direction may still be real; the point is
the readout as written does not license the conclusion it draws.

## Open questions for the team (questions, not judgments)
- What produced the 101,200 / 98,800 split — is there a redirect, a bot filter, or a
  bucketing change that would drop traffic from one arm?
- Was the 9-day stop a pre-declared horizon, or did the test end when add-to-cart crossed
  significance?
- The 8.0% baseline is modeled — what is the measured pre-experiment add-to-cart rate, and
  does the +2.1% hold against it?
- Checkout-completion is flat while add-to-cart rose — is the added intent converting, or
  is Quick-Add moving a metric that doesn't reach revenue?

## Near-misses and unchecked territory (the audit journey, made inspectable)
- Considered, did not flag: the guardrail set is genuinely reported (both flat), so check 4
  did not fire on the report-only-what-moved pattern — noted, not flagged.
- Almost flagged: the 9-day window looked short for novelty decay, but there is no stated
  novelty population and the surface is a returning-user cart — left as an open question,
  not a FLAG.
- Could not check: randomization unit vs analysis unit is unstated (users randomized,
  users analyzed is assumed but not confirmed); raised as context, not scored.
- Could not check: the analytics query behind +2.1% is unnamed, so provenance is
  "analytics-query (source not named)" rather than a verified source.

## ⛔ Ship / no-ship decision — NEEDS HUMAN
This slot is intentionally empty. Whether the measured effect is large enough to
matter, and whether to ship, is a business judgment this skill does not make.
   Materiality call (is the effect worth it?): ____________________
   Ship / hold / re-run:                        ____________________

## Named gate
Sign-off owner (experiment owner / PM): ____________________   Date: ______
No ship decision is recorded until this line is signed by a human.
```

---

## Why this is a good golden

- **SRM ran first and led the framing.** The one check that subsumes the others is not buried at position 6 in the reader's mind — the confidence statement opens with it.
- **The eye-test trap is shown, not told.** 50.6/49.4 *looks* fine; the arithmetic says broken. A reader who internalizes only one thing should internalize that.
- **The ship slot is empty under pressure.** Every signal points one way and the report still refuses to say "don't ship." It says what the checks license and stops.
- **The open questions are questions.** Each ends in a question mark and could be answered in a way that leaves the team where they are (maybe the redirect is benign) — none is a recommendation in disguise.
- **The near-misses are traces.** They record what was considered, almost-flagged, and could-not-be-checked, with no verdict attached — so the next reader sees exactly where the audit's confidence is thin.

*HeyHi Confidential. Worked example for `experiment-readout-linter` v0.2.0. Fully synthetic; added 2026-08-23 (Wave D) per the 2026-08-22 skills audit § 4 (no worked examples) and § 5 (curiosity surfaces).*
