---
classification: confidential
title: "Business-case canon — the method spine"
skill: design-business-case-drafter
loaded_by: "SKILL.md Step 1"
---

# Business-case canon — the method spine

The method knowledge `design-business-case-drafter` loads to build a Design Business Case Draft. Authored here as craft; the always-loaded behavioral invariants it obeys live in `sheerline/os/operating-principles.md` and the area canon in `sheerline/os/foundations/business-acumen/FOUNDATION.md`, both cited, never restated. Everything here is scaffolding for a human decision. None of it makes the business claim, states an ROI number, or takes a stance.

---

## 1. The four-step structure

A buy-in argument that leadership can act on has four parts, in order (foundation § The stakeholder buy-in structure):

1. **Problem.** What is costing the organization something now: time, quality, risk, or rework. Restated as a candidate the audience would recognize in their own words.
2. **Evidence.** What supports the problem statement and the response, each item with its provenance status (§ 2). Evidence that cannot be traced is flagged, not asserted.
3. **Response.** The design investment, described: what it is, what it changes, what it depends on. Described, not argued; the argument is the human's claim.
4. **Measurable expectation.** The signals that would move if the response worked, as candidates, handed to `design-measurability-mapper` for the metric scaffold. No target is set in the draft.

The order matters: evidence before response keeps the case from being a solution looking for a problem (the same failure the strategy warden catches upstream).

## 2. The four-state provenance taxonomy

Every statistic or external claim gets one status. The taxonomy **extends** the three states recorded for the `heyhi-citation-auditor` candidate (verified / partially verified / unverifiable) by splitting out the fourth and sharpening the first:

| Status | Meaning | What the draft does |
|---|---|---|
| `verified-primary` | The claim traces to an inspectable primary source (the original report, paper, or dataset), and the figure matches it. | May be cited, with the source, and with its correlational flag. |
| `partially-verified` | An attribution exists (a named report or organization) but the primary is not inspectable, or the figure is quoted second-hand and cannot be matched to the original. | Cited only with the caveat that the primary was not inspected; proposed restatement alongside. |
| `unverifiable` | A source is offered but cannot be found, or the source does not contain the claim. | **Flagged, never asserted.** A qualitative restatement or a verified alternative is proposed. |
| `unsourced` | No source is offered at all. | **Flagged, never asserted.** Same as above. `unsourced` is distinct from `unverifiable`: the first is a missing citation, the second is a citation that fails. |

Plus one flag on every row: **`correlational`** or **`causal-as-stated`**. A correlational finding presented with causal language ("design-led companies grow faster *because* …") is mis-stated regardless of provenance, and the caveat block (§ 3) exists to keep the two apart.

**Provenance is checked, not asserted.** The human saying "that stat is real" does not upgrade a row. The human may still use a flagged claim, knowingly, at the gate; the ledger's job is that the choice is knowing.

**A misquoted verified figure.** Briefs routinely carry a real finding in the wrong shape: "32% higher revenue growth" for McKinsey's "32 percentage points higher over five years," an annual figure that the source states over a period, a top-quartile result quoted as if it applied to every company. When the source is reachable, the row stays `verified-primary`, the note records the correction, and only the corrected form appears in the draft (inside the caveat block when it is a design-ROI figure). Silently swapping the brief's figure for the right one, without the note, hides the correction from the human who will be asked about it.

**Not reachable this session.** A paid report, a source behind a login, or a session with no web access cannot be inspected. When the brief **names** the source, the status is `partially-verified` (an attribution exists; the primary was not inspected) with the note "primary not reachable this session," and it is never upgraded to `verified-primary` on the attribution alone. When the brief names **no** source, reachability is moot: the status is `unsourced`. `unverifiable` is reserved for a named source that was reached and does not contain the claim, or a named source that cannot be found at all. The two figures traced and recorded in the foundation's first canon row (McKinsey: `verified-primary`, `correlational`; the "$1 → $100" figure: `partially-verified` at best) may be reused at their recorded status without re-tracing.

**Two more columns the ledger carries.** An internal measurement (a grep count, a log, a ticket tally) is neither correlational nor causal; its flag reads `n/a (observation)`. A modeled or projected figure carries `synthetic (modeled)` in a separate `Synthetic?` column and on every surface it appears; provenance still gets one of the four states (a modeled figure with a stated method is usually `verified-primary` as to *how* it was produced and `synthetic` as to *what* it is).

## 3. The design-ROI caveat block (inserted by construction)

The foundation's first canon row, applied. Insert this block whenever any design-ROI figure appears in the evidence, and as a standing note when none does. The provenance statuses were traced 2026-09-05 and live in `FOUNDATION.md § The knowledge canon`; re-trace at build of a case if a figure's status is in doubt.

> **Design-ROI figures, read carefully.** The two most-quoted numbers in design business cases are correlational and weak-provenance, and they are routinely misquoted as causal.
> **McKinsey Design Index** (*The Business Value of Design*, 2018; ~300 companies, three industries, five years): top-quartile scorers showed revenue growth 32 percentage points higher and total-returns-to-shareholders growth 56 points higher than industry peers. McKinsey's own text calls this a correlation. Status: `verified-primary`, `correlational`. It says design-strong companies also grew; it does not say design caused the growth.
> **"Every $1 invested in UX returns $100 (9,900% ROI)."** Attributed to a paid Forrester report (circa 2016) that secondary sources cite and never link or quote directly; the method is not open to inspection; frequently conflated with a separate IBM "100x cost to fix after development" claim of similar provenance. Status: `partially-verified` at best, `causal-as-stated`. Do not lead with it.
> Neither figure appears in this case as a headline claim. Where the case cites either, it cites it here, with this note.

## 4. The measurable-expectation hand-off

The draft names **candidate signals** (what would move if the response worked: rework time, time-to-first-design-review, defect escapes, adoption of shared components) and hands the metric scaffold to `design-measurability-mapper`: it builds Goals → Signals → Metrics, audits instrumentation, and stress-tests for gaming; the team then chooses the metric and sets the target at the mapper's own human gate. The drafter never sets a target. A case with a target in it has jumped two gates.

## 5. The pricing refusal

`OPERATING_PRINCIPLES.md` § Pricing is absolute: no specific price in any external-facing document. A business case is an argument, not a quote, and it will travel inside the designer's organization. So the draft carries **no currency amount, rate, day-rate, fee, or budget figure** of any kind, including the designer's own internal numbers and a figure spoken out in words. Each is removed and the removal recorded in the pricing-check line. Budget is a conversation between humans; the case earns that conversation.

**Scope is not price.** Headcount and duration ("two designers for six months," "about ten weekend hours," "one sprint") describe the investment the response section needs and stay in the draft. The refusal is for money, not for effort.

## 6. The boundary (cited, not restated)

The business claim is this area's extension of the canonical "what stays human" list (`sheerline/os/operating-principles.md` § What stays human names the positioning stance and metric selection; the foundation's judged layer adds the claim). Scoring and evidence are advisory (§ the taste-and-critique boundary). The scope fence (§ The Business-Acumen scope fence): whose money is on the table? The designer's organization's. If it is a HeyHi client's, this is `heyhi-proposal`'s work.

---

*HeyHi Confidential. Method reference for `design-business-case-drafter` (Sheerline area 10). Foundation: `sheerline/os/foundations/business-acumen/FOUNDATION.md` § The knowledge canon (first row). Research of record: `sheerline-skill-buildout-research-2026-08-09.md` § 6.2.*
