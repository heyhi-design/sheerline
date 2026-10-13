---
name: experiment-readout-linter
description: >-
  Audit an A/B test or experiment readout the human brings — before the team
  acts on it — so a shaky result cannot be laundered into a ship decision.
  Runs the mechanical integrity checks a rushed readout skips: sample-ratio
  mismatch, peeking / optional-stopping, power and sample sufficiency,
  back-solved primary metric, single-method over-reliance, and number
  provenance. Triggers: "audit this experiment readout", "is this A/B result
  trustworthy", "did we peek", "was this powered", "check the SRM", "lint this
  test result", "check this experiment before we ship". Produces a Readout
  Integrity Report where every mechanical check has a verdict and the ship /
  no-ship and materiality calls ship EMPTY behind a named human gate. NOT for
  reviewing a live funnel or landing page for conversion (use heyhi-funnel-cro).
  NOT for deciding whether something is measurable at all or building the metric
  scaffold upstream (use design-measurability-mapper). NOT for making the ship
  decision — that is the human's, always.
version: "0.2.1"
updated: "2026-08-28"
status: "deployed — heyhi-skills/; v0.2.0 promoted 2026-08-23 (Gate G-C, plans/plan-sheerline-skills-upgrade-2026-08-22.md) — adds SRM check 6, open-questions + near-misses report surfaces, a worked example, 2 eval cases (6→8). v0.1.0 promoted 2026-08-15 (DISPATCH-D). Sheerline area 10 (Business Acumen), P1.5. Registered in skill-registry.yaml v2.35.0. v0.2.1 (2026-08-28) adds check 6's SRM-not-applicable path for paired/deterministic designs (reference § 6 + SKILL.md check-6 + eval erl-09), from the Wave E / E-5 harvest; registry v2.37.1."
classification: HeyHi Confidential
---

# Experiment Readout Linter

**Sheerline area 10 (Business Acumen) · P1.5 · pure validate/audit skill.** A designer or PM brings a finished experiment readout — "variant B won, +3.2% conversion, ship it." This skill runs the mechanical checks that decide whether that sentence is trustworthy, and hands the *ship decision itself* back to the human. It is the "not being fooled" instrument: it lints the reasoning, it never renders the verdict.

**The boundary this skill obeys (Sheerline § 9, absolute).** A structured artifact with explicit empty judgment slots, a named human gate, and provenance labels on anything synthetic. *The ship / no-ship call and the materiality call are the empty slots.* A version of this skill that concludes "so ship it" has exceeded its charter. Grades never gates; mechanics never taste. The skill scores the *statistics*; the human owns the *decision*. The two new surfaces this version adds — open questions and near-misses — are questions and traces, never verdicts: they widen what the team can think about, they do not narrow it to a recommendation.

> **This skill closes through the Exit Gate (`CLAUDE-SESSION-RULES.md § Exit Gate`).** See the bottom-of-skill bracket.

---

## Routing — disambiguation with sibling skills

| If the task is… | Use |
|---|---|
| Auditing a completed experiment/A-B readout for statistical integrity | **this skill** |
| Reviewing a live funnel / landing page to lift conversion | `heyhi-funnel-cro` |
| Asking "is this design outcome even measurable?" + building the Goals→Signals→Metrics scaffold *before* the experiment | `design-measurability-mapper` |
| Auditing an opportunity / JTBD / prioritization artifact's reasoning | `strategy-integrity-warden` |
| Making the ship decision | **the human** (this skill's named gate) |

The seam with `design-measurability-mapper` is temporal: the mapper works *upstream* (is there a measurable signal, is it instrumented), this linter works *downstream* (the experiment ran — is the readout honest). The seam with `heyhi-funnel-cro` is object: funnel-cro reviews a *surface*, this reviews a *result*.

---

## Step 0: Improvement hook check

Before running, retrieve any recurring corrections for experiment/measurement work (`retrieve_design_corrections` if the design MCP is reachable, or the Sheerline `os/corrections/` registry). Fold a matching recurring correction into the pass. Skip silently if none.

## Step 1: Load context

Read what the human brought and the governed context it sits under.
1. The **readout artifact** (the deck, doc, dashboard export, or pasted summary the human hands over). This is the object of the audit — do not go re-run the experiment.
2. `references/experiment-integrity-checks.md` — the check definitions, the flag thresholds, and the honest-confidence framing. THE method spine.
3. `references/worked-example.md` — a filled Readout Integrity Report on synthetic input. Read it to calibrate register and depth on the free-prose slots (confidence framing, open questions, near-misses); do not copy its findings.
4. The Sheerline area-10 governed context: `sheerline/os/foundations/business-acumen/FOUNDATION.md` (the scope fence — design-business only, and "data literacy as *not being fooled*"). Register under it; do not author it.

If the readout omits the information a check needs (no pre-declared MDE, no stated stopping rule, no per-arm sample counts), that absence **is** the finding — record it as `UNKNOWN — not reported`, never as a pass.

## Step 2: Run the six mechanical checks

Each check returns one of: **PASS** (evidence present and clean), **FLAG** (a specific integrity risk found), or **UNKNOWN — not reported** (the readout does not carry what the check needs). No check returns a ship recommendation.

**Run check 6 (SRM) first.** It is the canonical first integrity check: a broken randomizer invalidates every downstream check, so a firing SRM moots checks 1–5 (still record them, but the confidence framing must lead with the SRM finding). It is numbered 6 only to keep the older checks' numbers stable.

1. **Peeking / optional-stopping.** Was a fixed sample horizon or a valid sequential/always-valid method declared *before* the run? Was the test stopped because it "hit significance"? Repeated interim looks against a fixed-horizon p-value inflate the false-positive rate materially (the corroborated range is roughly 20–40% under naive repeated peeking; do not cite a false-precision single figure). FLAG any "we saw it was significant and stopped."
2. **Power / sample sufficiency.** Was a minimum detectable effect (MDE) and a power target set up front? Is n sufficient for the claimed effect size? An underpowered test that still "won" is a winner's-curse risk — significant *and* inflated. FLAG underpowered-but-significant, and FLAG a novelty/primacy window too short to have decayed.
3. **Back-solved primary metric.** Was the success metric fixed *before* results were seen? FLAG a primary metric that appears chosen after the fact, a success criterion that shifted, or a secondary metric promoted to headline once the primary disappointed (HARKing / metric-shopping).
4. **Single-method over-reliance.** FLAG one quant test carrying the whole decision with no triangulation; segment cherry-picking; multiple comparisons with no correction; guardrail/counter-metrics ignored (did engagement rise while retention or complaints quietly moved?).
5. **Provenance.** Tag every headline number with its source: `analytics-query` (name it), `vendor-tool`, `hand-computed`, or `modeled/synthetic`. FLAG any number with no traceable origin. **Any modeled, simulated, or synthetic input carries a `synthetic` provenance label on every surface it appears** — a synthetic baseline must never read as a measured one.
6. **Sample-ratio mismatch (SRM).** Compare the *observed* per-arm sample counts against the *designed* allocation (usually 50/50). A significant deviation means the randomization or logging is broken — bots filtered from one arm, a redirect dropping traffic, a bad bucketing hash — and when that happens **the whole readout is untrustworthy regardless of how clean checks 1–5 look.** This is purely mechanical: chi-square goodness-of-fit, one degree of freedom for a two-arm test, FLAG at the p < 0.001 convention (χ² > ~10.83). The math and worked arithmetic are in the reference. FLAG a firing SRM; return `UNKNOWN — not reported` when per-arm counts are not given (you cannot verify the randomizer, and that gap is itself worth surfacing). **SRM applies to randomized-assignment designs only** — on a paired/within-subject or deterministic/seeded design (the same task set run against both arms, no randomizer) there is nothing to randomize: verify balance *by construction* and record `PASS — classical SRM N/A (balanced by construction)`, never a χ² on the per-arm (or, worse, the output) counts. Most internal eval-harness readouts are that class; see the reference's *when SRM does not apply* clause.

## Step 3: Produce the Readout Integrity Report

Output this exact structure. The judgment slots stay empty by construction; the open-questions and near-misses surfaces carry questions and traces, never recommendations.

```
# Readout Integrity Report — [experiment name]
Source readout: [file / link / "pasted summary"]     Audited: [date]

## Mechanical checks
| # | Check | Verdict | Evidence / what triggered it |
|---|-------|---------|------------------------------|
| 6 | Sample-ratio mismatch (SRM) | PASS / FLAG / UNKNOWN | run first — observed vs designed split, χ² |
| 1 | Peeking / optional-stopping | PASS / FLAG / UNKNOWN | … |
| 2 | Power / sample sufficiency  | PASS / FLAG / UNKNOWN | … |
| 3 | Back-solved primary metric  | PASS / FLAG / UNKNOWN | … |
| 4 | Single-method over-reliance | PASS / FLAG / UNKNOWN | … |
| 5 | Provenance                  | PASS / FLAG / UNKNOWN | … |

## Provenance ledger
| Headline number | Source | Provenance tag |
|-----------------|--------|----------------|
| +3.2% conv.     | …      | analytics-query / vendor-tool / hand-computed / synthetic |

## Confidence framing (honest, not a grade)
[Plain-language statement of what the checks do and do not let the team conclude —
 e.g. "The direction is consistent, but the test was stopped early and is
 underpowered, so the +3.2% is likely inflated." If SRM fired, this must lead:
 "The arms are unbalanced beyond chance, so the randomizer is suspect and no
 downstream number can be trusted." NO score, NO letter grade.]

## Open questions for the team (questions, not judgments)
[What the readout does not answer and what you would ask the experiment owner.
 Each is a question that, answered, would change or firm up the picture. No
 recommendation — a question is not a verdict.]
- [e.g. "Was the day-6 stop the pre-declared horizon, or did it coincide with
   hitting significance? The readout doesn't say."]
- [e.g. "Guardrails aren't reported — did retention or complaint rate move?"]

## Near-misses and unchecked territory (the audit journey, made inspectable)
[What was considered and passed, what almost flagged, and what could not be
 checked because the readout omits it. No verdicts — this is the trace, so the
 reader can see where the audit's confidence is thin.]
- Considered, did not flag: [e.g. "6-day window looked short for novelty, but the
   surface has no novelty population — passed."]
- Almost flagged: [e.g. "segment table leads with mobile; checked for a cherry-pick,
   the aggregate holds — no FLAG."]
- Could not check: [e.g. "no per-arm counts, so SRM returns UNKNOWN."]

## ⛔ Ship / no-ship decision — NEEDS HUMAN
This slot is intentionally empty. Whether the measured effect is large enough to
matter, and whether to ship, is a business judgment this skill does not make.
   Materiality call (is the effect worth it?): ____________________
   Ship / hold / re-run:                        ____________________

## Named gate
Sign-off owner (experiment owner / PM): ____________________   Date: ______
No ship decision is recorded until this line is signed by a human.
```

**The report is done when every mechanical check carries a verdict, every headline number carries a provenance tag, the open-questions and near-misses surfaces carry questions/traces (not recommendations), and the two ship-decision lines are still blank.** A report that fills the ship line — or that lets an open question smuggle in a recommendation ("Shouldn't you re-run this?") — has failed its own charter.

## Step 4: Pre-flight verification

Before handing the report over: confirm each FLAG cites a *specific* line/number in the source readout (not a generic "consider power"); confirm no check silently upgraded an `UNKNOWN` to `PASS`; confirm the ship/no-ship and materiality lines are empty; confirm every synthetic input is labelled `synthetic` wherever it appears. New in v0.2.0: confirm SRM ran first and, if it fired, the confidence framing leads with it; confirm every open question is phrased as a *question* (ends in a question mark, asks rather than tells) and every near-miss is a *trace* (records what was considered/could-not-check, renders no verdict). New in v0.2.1: confirm SRM applicability was assessed — on a paired/within-subject or deterministic/seeded design, check 6 records `PASS — classical SRM N/A (balanced by construction)` rather than a χ² computed on per-arm or output counts.

---

## What is explicitly out of scope

- **The ship decision and the materiality call.** Empty by construction (§ 9). The skill can say "underpowered and stopped early"; it cannot say "so don't ship."
- **Re-running or re-computing the experiment.** This audits the *readout the human brought*, not a fresh analysis. If the numbers cannot be sourced, that is a provenance FLAG, not an invitation to recompute. (Exception, narrow and mechanical: the SRM chi-square is computed from the per-arm counts the readout *already reports* — that is verifying the reported split, not re-running the experiment.)
- **Free query synthesis ("chat with the data").** The area-10 foundation's text-to-SQL reliability ceiling holds: this skill reads a readout, it does not author SQL against a warehouse.
- **Funnel / surface conversion review** — `heyhi-funnel-cro`. **Upstream measurability** — `design-measurability-mapper`.

---

## Exit Gate Required Headers (bottom-of-skill bracket)

This skill closes through Exit Gate Flavor A (`CLAUDE-SESSION-RULES.md § Exit Gate`). Before declaring done, confirm every required header holds real content, not a claim:

- `## Fixes Applied` (or, for an audit run, the delivered Readout Integrity Report)
- `## Smoke Test` (the Step 4 pre-flight checks, pasted)
- `## Next Session Prompt`

If the ship/no-ship slot is filled, or any FLAG is generic rather than line-cited, or an open question carries a recommendation, the gate has **not** been satisfied.

---

*HeyHi Confidential. Sheerline area 10 (Business Acumen), P1.5 net-new. v0.1.0 deployed 2026-08-15 (DISPATCH-D); registered in `skill-registry.yaml` v2.32.0. v0.2.0 staged 2026-08-23 (Wave D, `plans/plan-sheerline-skills-upgrade-2026-08-22.md`). v0.2.1 (2026-08-28) added the SRM-not-applicable path (paired/deterministic designs) to check 6, from the E-5 harvest. Spec source: `ai-services/design-intelligence/research/sheerline-skill-buildout-research-2026-08-09.md` § 6.2 / § 8; SRM + curiosity surfaces from the 2026-08-22 skills audit § 2.4 / § 5. Boundary: § 9.*
