---
classification: confidential
title: "Worked example — a filled Design Business Case Draft"
skill: design-business-case-drafter
loaded_by: "SKILL.md Step 1 (calibration)"
---

# Worked example — a filled Design Business Case Draft

**Synthetic input, invented organization. No client content.** Read this to calibrate the register and depth of the free-prose slots; do not copy its findings. The empty slots are shown empty on purpose. That is the output shape, not an omission.

**Synthetic brief brought by the (invented) design lead:** *"I need to make the case to our VP of Product for a shared design system. I've got three stats: design-led companies grow 2x faster; every $1 in UX returns $100; and our own numbers show engineers rebuilt the same date picker four times last quarter. Budget-wise I'm thinking two designers for six months at about [a figure]."*

---

```
# Design Business Case Draft — Shared design system (Ledgerworks, synthetic) · for VP of Product
Source artifacts: design lead's note; internal component audit (Q2, synthetic)     Drafted: 2026-09-05

## Problem (candidate — the human confirms it)
[candidate — agent-drafted] Product teams rebuild the same interface components independently,
so the same control is built, reviewed, and fixed more than once, and the versions drift apart in
front of users. Ambiguity to resolve: is the cost the team cares about rework time, inconsistent
user experience, or the accessibility risk of four unreviewed date pickers? The three point at
different evidence and different responses.

## Evidence ledger
| # | Claim | Source (as given) | Provenance | Correlational / causal-as-stated | Synthetic? | Note |
| 1 | "Design-led companies grow 2x faster" | none given | unsourced | causal-as-stated | | Flagged. Likely a paraphrase of the McKinsey Design Index finding (row 3); "2x" does not match that report. Proposed restatement: "companies that score high on design practice also showed stronger revenue growth in McKinsey's 2018 study; that is a correlation." |
| 2 | "Every $1 in UX returns $100" | "Forrester" | partially-verified | causal-as-stated | | Attribution exists; the primary is a paid report no secondary source links or quotes ("primary not reachable this session"). See the caveat block. Proposed restatement: drop the figure; the internal evidence (row 4) is stronger for this audience. |
| 3 | McKinsey Design Index: top quartile +32 pts revenue growth over five years | McKinsey, The Business Value of Design (2018) | verified-primary | correlational | | May be cited inside the caveat block only. |
| 4 | "Engineers rebuilt the same date picker four times last quarter" | internal component audit, Q2 (synthetic) | verified-primary | n/a (observation) | | Traceable to the audit; the strongest evidence in the case because it is the organization's own. |

## ⚠ Design-ROI figures — caveat (inserted by construction)
**Design-ROI figures, read carefully.** The two most-quoted numbers in design business cases are correlational and weak-provenance, and they are routinely misquoted as causal.
**McKinsey Design Index** (*The Business Value of Design*, 2018; ~300 companies, three industries, five years): top-quartile scorers showed revenue growth 32 percentage points higher and total-returns-to-shareholders growth 56 points higher than industry peers. McKinsey's own text calls this a correlation. Status: `verified-primary`, `correlational`. It says design-strong companies also grew; it does not say design caused the growth.
**"Every $1 invested in UX returns $100 (9,900% ROI)."** Attributed to a paid Forrester report (circa 2016) that secondary sources cite and never link or quote directly; the method is not open to inspection; frequently conflated with a separate IBM "100x cost to fix after development" claim of similar provenance. Status: `partially-verified` at best, `causal-as-stated`. Do not lead with it.
Neither figure appears in this case as a headline claim. Where the case cites either, it cites it here, with this note.

## Response (the design investment, described — not chosen)
A shared design system: a governed token set and component library, owned by a small design-
systems group of two designers for six months (scope, not price), that product teams consume
rather than rebuild. It changes where a component is built (once, centrally) and reviewed (once,
with accessibility checks). It depends on staffing the group, on a contribution model product
teams accept, and on an adoption path for the four existing date pickers.

## Measurable expectation (candidate signals; hands to design-measurability-mapper)
- [candidate] duplicate-component count across product codebases (the date-picker count, tracked)
- [candidate] engineering hours spent on rebuilt UI (from the existing time-tracking categories)
- [candidate] share of new screens composed from shared components
- [candidate] accessibility defects found in shared vs bespoke components
The metric and the target are the team's; run design-measurability-mapper for the scaffold.

## Pricing check
1 item removed: the currency figure attached to the staffing line in the brief. Reason: the pricing
rule is absolute and the case is an argument, not a quote; the budget conversation happens between
humans once the case has earned it. The scope ("two designers for six months") is not a price and
stays in the response.

## Open questions for the audience (questions, not judgments)
- Which cost does the VP already feel: rework time, drift in front of users, or accessibility risk?
- Is there an existing time-tracking category that captures rebuilt-UI hours, or would that need
  instrumenting first?
- Who would own the contribution model, and does a product team have to accept it?

## Near-misses and unchecked territory
- Considered, set aside: an industry benchmark for design-system adoption rates; none traceable
  to a primary in the session, so not added rather than added unsourced.
- Almost passed provenance: row 1, because it "sounds like" the McKinsey finding; kept unsourced
  because the figure does not match and no source was offered.
- Could not trace: the Forrester report behind row 2 (paid; not inspectable here).

## ⛔ The business claim — NEEDS HUMAN
   The claim: ____________________

## ⛔ Positioning stance — NEEDS HUMAN
   The stance this case takes: ____________________

## Named gate
Sign-off owner (design lead): ____________________  Date: ______
```

---

**What to notice.** The strongest evidence is the organization's own audit, and the draft says so in a note without turning it into a claim. The "2x" statistic is flagged and restated, not silently corrected to the McKinsey number. The Forrester figure is not upgraded because the lead attributed it. The currency figure is gone, with the reason; the staffing scope stays. The candidate signals hand off; no target appears. Nothing in the draft says what the design system will deliver.

*HeyHi Confidential. Synthetic worked example for `design-business-case-drafter` (Sheerline area 10).*
