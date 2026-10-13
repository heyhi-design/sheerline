---
classification: confidential
title: "Experiment integrity checks — the method spine"
skill: experiment-readout-linter
loaded_by: "SKILL.md Step 1"
---

# Experiment integrity checks

The definitions and flag thresholds behind the six mechanical checks. On-demand reference — load when running the linter, not by default. Every threshold here is a *flag* threshold, not a *gate*: a flag surfaces a risk for the human to weigh; nothing here blocks a ship or renders the decision.

*Internal operational reference (deployed under `heyhi-skills/`): the em-dash limit is exempt per `OPERATING_PRINCIPLES.md`. Provenance caveats on the cited figures are stated inline.*

**Run order.** Check 6 (SRM) is the canonical *first* check even though it is numbered last (the number is kept high so checks 1–5 keep their stable ids and the existing eval cases stay valid). A firing SRM means the randomizer is broken, which moots checks 1–5 — run it first, and if it fires, lead the confidence framing with it.

---

## 1. Peeking / optional-stopping

**What it is.** Checking an A/B test repeatedly and stopping as soon as it crosses significance. Under a fixed-horizon p-value, every extra look is another chance to cross the line by noise, so the real false-positive rate climbs well above the nominal 5%.

**What to look for.**
- A stated **stopping rule fixed before the run** (a target sample size, or a declared sequential / always-valid / Bayesian method). Present and honored → PASS.
- Language like "we saw it hit significance and called it," "checked daily and stopped when it turned green" → **FLAG (peeking)**.
- No stopping rule reported at all → **UNKNOWN — not reported** (do not assume clean).

**The honest magnitude.** Repeated naive peeking inflates the false-positive rate materially; the independently corroborated range is roughly **20–40%** depending on how often you look. Do not cite a single false-precision figure — the range is the honest statement. The fix teams should have used (sequential testing / always-valid inference) is what the PASS evidence looks like.

## 2. Power / sample sufficiency

**What it is.** Whether the test could have detected the effect it claims, and whether the winner is trustworthy rather than an inflated fluke.

**What to look for.**
- A **minimum detectable effect (MDE) and a power target (usually 80%) declared up front**, with an n that meets it → PASS.
- Significant result on an underpowered test → **FLAG (winner's curse)**: low-powered significant findings systematically *overstate* effect size. The direction may hold; the magnitude is suspect.
- A short run that could be riding a **novelty or primacy** spike (new UI attracts clicks that decay) → **FLAG** unless the window is long enough to have decayed.
- No power/MDE analysis reported → **UNKNOWN — not reported**.

## 3. Back-solved primary metric

**What it is.** Choosing or swapping the success metric *after* seeing the data (HARKing / metric-shopping). It manufactures significance out of multiple looks at different outcomes.

**What to look for.**
- The **primary metric and success threshold fixed before results were seen** → PASS.
- A headline metric that appears selected after the fact; a primary that disappointed and a secondary quietly promoted to the headline; a threshold that moved → **FLAG (back-solved)**.
- No pre-registration or pre-stated metric → **UNKNOWN — not reported**.

## 4. Single-method over-reliance

**What it is.** Letting one quantitative test carry a decision it cannot bear alone.

**What to look for (any one → FLAG).**
- One A/B test, no triangulation (no qualitative signal, no replication, no holdback).
- **Segment cherry-picking** — "it won for logged-in mobile users in week 2."
- **Multiple comparisons** across many metrics/segments with no correction (someone will look significant by chance).
- **Guardrail / counter-metrics ignored** — the primary rose while retention, latency, complaint rate, or unsubscribes quietly moved the wrong way. A readout that reports only the metric it wanted to move is the classic tell.

## 5. Provenance

**What it is.** Whether every headline number can be traced to a real source, and whether any number is modeled rather than measured.

**What to look for.**
- Each headline number tagged: `analytics-query` (name the query/source), `vendor-tool` (Optimizely, Statsig, GA, etc.), `hand-computed`, or `modeled/synthetic`.
- A number with **no traceable origin** → **FLAG (unsourced)**.
- **Any modeled, simulated, projected, or synthetic input** → tag `synthetic` and carry that label on every surface. A synthetic baseline, a projected lift, or a model-estimated denominator must never be presented as a measured value. This is the write-side of Sheerline's provenance rule: synthetic content is labeled at the boundary so a later reader cannot mistake it for ground truth.

## 6. Sample-ratio mismatch (SRM)

**What it is.** Whether the *observed* number of subjects in each arm matches the *designed* allocation. A 50/50 experiment that logged 51.2% of users into control did not randomize the way it claims — a redirect dropped traffic from one arm, a bot filter fired asymmetrically, a bucketing hash skewed, or an arm was instrumented late. When the split is broken, the two groups are no longer exchangeable, so every downstream comparison (including a perfectly clean-looking p-value) is confounded. This is the single most important mechanical check and the cheapest: it needs only the per-arm counts the readout already reports.

**What to look for.**
- Per-arm counts **consistent with the designed split** (deviation within chance) → PASS.
- Per-arm counts **deviating beyond the p < 0.001 convention** → **FLAG (SRM)**: the randomizer is suspect; state that the whole readout is untrustworthy until the imbalance is explained, and note checks 1–5 are moot on a broken randomizer.
- **No per-arm counts reported** → **UNKNOWN — not reported**. You cannot verify the split; surface the gap (this is a common omission and worth an open question).

**The mechanics (purely mechanical — this is arithmetic, not judgment).**
- Let the observed counts be `O_i` and the expected counts under the designed split be `E_i = N × p_i`, where `N` is the total and `p_i` is arm *i*'s designed share (0.5 each for a balanced two-arm test).
- Chi-square goodness-of-fit: `χ² = Σ (O_i − E_i)² / E_i`, summed over arms. Degrees of freedom = (number of arms − 1); **1** for a two-arm test.
- **Flag threshold:** `p < 0.001`, i.e. `χ² > 10.83` for 1 df. (The strict 0.001 convention is the widely-adopted ExP/industry cutoff, chosen because SRM p-values are uniform under a healthy randomizer, so anything this extreme is far more likely a bug than bad luck. It is a *flag* threshold, not a gate — a borderline value near the cutoff is itself worth an open question, not a silent pass.)
- **Balanced-design shortcut.** For a 50/50 two-arm test the statistic collapses to `χ² = (2·O_control − N)² / N`. Worked: designed 50/50, observed 101,200 control / 98,800 treatment, `N = 200,000`. `χ² = (202,400 − 200,000)² / 200,000 = 2,400² / 200,000 = 5,760,000 / 200,000 = 28.8`. That is far above 10.83 → **FLAG**, even though 50.6% / 49.4% looks balanced to the eye. This is the teaching point: **SRM is invisible to eyeballing at scale** — a fraction of a percent is a broken randomizer when N is large.
- **Randomization-unit / interference note (pairs with check 4).** Confirm the randomization unit matches the analysis unit. If users were randomized but sessions were analyzed (or vice versa), or if subjects in one arm can affect subjects in the other (network/marketplace interference, a shared inventory pool, a two-sided market), the independence the statistics assume is violated even when the SRM passes. This is not always computable from the readout; when the unit is unstated, raise it as an open question rather than a FLAG.

**When SRM does not apply — randomized-assignment designs only.** The χ² above tests a *randomizer*; it is meaningful only when subjects were randomly assigned to arms. Two design families carry no randomizer, and running them through the χ² manufactures a spurious statistic:

- **Paired / within-subject** — the *same* units are measured under both conditions (the same task set, users, or sessions run against each arm). Balance is guaranteed by construction, not by a randomizer.
- **Deterministic / seeded** — assignment is fixed by a rule or seed (e.g. a named design system vs a SHA-seeded scramble of it, same runner, same task list), so there is nothing to randomize.

On either family, do **not** compute χ² on the per-arm counts — and never on *output* counts (tokens emitted, rows returned), which are results, not an allocation, so an SRM χ² on them is meaningless. Instead verify **balance by construction**: confirm the two arms share an identical task/condition set (e.g. an identical 31/31 component set and task list) and record check 6 as `PASS — classical SRM N/A (balanced by construction)`. Reserve the χ² for genuinely randomized-assignment designs, where a broken randomizer is possible. Most internal eval-harness readouts (a practice testing its own skills) are deliberately paired and seeded to control confounds, so for that class this N/A path is the norm, not the exception.

---

## The confidence framing (why there is no grade)

The report ends in a plain-language confidence statement, never a score. A letter grade or a 0–100 number would *be* a ship recommendation wearing a costume — it collapses "the statistics are shaky" and "don't ship" into one figure, which is exactly the judgment slot this skill leaves empty. State what the checks let the team conclude ("consistent direction, but stopped early and underpowered, so treat the magnitude as a ceiling") and stop. If SRM fired, the framing leads with it — a broken randomizer is not one flag among five, it is the finding that subsumes the rest. The materiality and ship calls are the human's.

## The two curiosity surfaces (open questions, near-misses) — why they are not verdicts

Added in v0.2.0. Both exist to make the report a thinking instrument instead of a closed checklist, and both are inside the § 9 boundary precisely because neither renders a decision:

- **Open questions for the team** are questions to the experiment owner — what the readout does not answer, what evidence would move the picture. The discipline: every entry ends in a question mark and *asks* rather than *tells*. "Did retention move?" is in charter. "You should check retention" is a recommendation wearing a question's clothes, and it is out. The test: if answering the question could leave the team exactly where they are, it is a real question; if the only acceptable answer is the action you had in mind, it is a smuggled verdict.
- **Near-misses and unchecked territory** are the audit's own trace: what was considered and passed, what almost flagged, what could not be checked because the readout omits it. It renders the journey inspectable so the next reader sees where confidence is thin. It carries no verdict — "could not check SRM, no per-arm counts" is a trace; "the missing counts mean this is untrustworthy" is a verdict and belongs (if anywhere) in the confidence framing, stated as what the checks do and do not license.

---

## Provenance of the figures cited here

- The peeking false-positive inflation **range (≈20–40%)** is independently corroborated; the often-quoted single-point figure was not re-surfaced at that precision, so the range is used deliberately (`sheerline-skill-buildout-research-2026-08-09.md` § 6.4 provenance note).
- Winner's-curse / low-power effect inflation is a standard result in the experimentation literature; stated directionally, no single vendor figure relied on.
- The SRM **p < 0.001** flag threshold is the widely-adopted industry convention (Microsoft ExP and the broader online-experimentation literature); it is a convention, not a law of nature, and is used here as a flag threshold with a borderline band explicitly called out rather than a hard gate.

*HeyHi Confidential. Reference for `experiment-readout-linter`. Spec source: `sheerline-skill-buildout-research-2026-08-09.md` § 6.2; SRM check added v0.2.0 per the 2026-08-22 skills audit § 2.4.*
