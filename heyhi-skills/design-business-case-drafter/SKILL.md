---
name: design-business-case-drafter
description: >-
  Draft-for-judgment a stakeholder buy-in argument for a design investment
  inside the designer's own organization, with the correlational caveat and a
  claims-provenance check built in, and no pricing, ever. Runs the mechanical
  work: the problem → evidence → response → measurable-expectation structure
  (each restated as a candidate), a four-state provenance check on every
  statistic (verified-primary / partially-verified / unverifiable / unsourced,
  plus correlational vs causal-as-stated), the design-ROI caveat block inserted
  by construction whenever a design-ROI figure appears, candidate signals that
  hand to design-measurability-mapper, and a hard refusal of any currency
  figure. Triggers: "draft a business case", "make the case for design",
  "business case for the design system", "help me make the case to my VP",
  "stakeholder buy-in for a design investment", "justify the design
  investment", "the case for a design hire". Produces a Design Business Case
  Draft where the business claim and the positioning stance ship EMPTY behind
  a named human gate. NOT for writing a proposal, SOW, or scope for a HeyHi
  client (use heyhi-proposal). NOT for building a deck or slides for the case
  (use heyhi-deck). NOT for auditing a client's own design system for health,
  drift, or tokens (use heyhi-design-intelligence-audit). NOT for auditing a
  completed experiment or A/B readout
  (use experiment-readout-linter). NOT for metric selection or setting the
  target (use design-measurability-mapper, then the human). NOT for making the
  business claim or stating the ROI number (the human's, always).
version: "0.1.1"
updated: "2026-09-05"
status: "deployed 2026-09-05 — heyhi-skills/design-business-case-drafter/ (Tier 1, buildable-now, self-application-first); registered in the main registry and the Sheerline area-10 subset registry, promoted in the Bucket B promotion pass (staged #781, cleared by the instance owner 2026-09-05). Area 10 coverage partial -> covered (both area-10 skills promoted). v0.1.1 (2026-09-05): self-application proof run (a Design Business Case Draft for a real instance-internal investment, one token contract shared across two of the instance's own surfaces; record in the instance's engagement folder) + eval-by-hand 6/6; harvest: correct a misquoted verified figure against the traced source, the not-reachable-this-session status, scope vs price in the pricing refusal. Sheerline area 10 (Business Acumen), P3, build class N. Spec: plans/plan-sheerline-p3-business-acumen-2026-09-05.md § 4 / § 5 / § 6 / § 9. Foundation: sheerline/os/foundations/business-acumen/FOUNDATION.md (filled 2026-09-05)."
classification: HeyHi Confidential
---

# Design Business Case Drafter

**Sheerline area 10 (Business Acumen) · P3 · buildable-now (Tier 1), self-application-first.** A designer needs to argue, inside their own organization, for a design investment: a design system, a research hire, a redesign, protected time. This skill does the chartered drafting job: it structures the argument as problem → evidence → response → measurable expectation, runs a **claims-provenance check** on every statistic the draft would lean on, inserts the **design-ROI caveat by construction** whenever the two most-quoted (and correlational) figures appear, and refuses any currency figure. It stops at the point where a human must make **the business claim** (what design will do for which number) and take **the positioning stance**. Those are theirs.

**The boundary this skill obeys (Sheerline, absolute).** A structured artifact with explicit empty judgment slots, a named human gate, and provenance labels on anything synthetic. *The business claim and the positioning stance are the empty slots.* Structuring the argument, checking provenance, inserting the caveat, naming candidate signals, and stripping pricing is mechanical; asserting what design will deliver is judgment. A version of this skill that states an ROI number, presents a correlational figure as causal, asserts an unsourced statistic, or writes a price has exceeded its charter. Evidence informs; it never asserts.

**The scope fence.** This is a buy-in argument inside the designer's organization, for the designer-as-practitioner (`sheerline/os/operating-principles.md` § The Business-Acumen scope fence; the foundation points at it). The self-test: *whose money is on the table?* If it is a HeyHi client's, this is a proposal, and `heyhi-proposal` owns it.

> **This skill closes through the Exit Gate (`CLAUDE-SESSION-RULES.md § Exit Gate`).** See the bottom-of-skill bracket.

---

## Routing — disambiguation with sibling skills

| If the task is… | Use |
|---|---|
| Draft a buy-in argument for a design investment inside the designer's own organization | **this skill** |
| Write a proposal, SOW, or scope for a HeyHi client | `heyhi-proposal` (the keel/sales layer; main registry only) |
| Build a deck or slides from a finished case | `heyhi-deck` |
| Audit a completed experiment or A/B readout the case wants to cite | `experiment-readout-linter` |
| Audit the organization's own design system for health, drift, or tokens (evidence the case may cite, not the case itself) | `heyhi-design-intelligence-audit` |
| Choose the metric or set the target the case commits to | `design-measurability-mapper`, then **the human** |
| Supply the competitive evidence the case leans on | `competitive-teardown-runner` |
| Make the business claim or state the ROI number | **the human** (this skill's named gate) |

The seam with `heyhi-proposal` is purpose and money: a case argues to the designer's own leadership; a proposal sells HeyHi's work to a client. The seam with `design-measurability-mapper` is a hand-off: this skill names candidate signals in the measurable-expectation slot; the mapper builds the Goals → Signals → Metrics scaffold; the human chooses. The seam with `experiment-readout-linter` is object: the linter audits a *result*; this drafts an *argument* that may cite one.

---

## Step 0: Improvement hook check

Retrieve any recurring corrections for business-case or claims-provenance work (`retrieve_design_corrections`, or the Sheerline `os/corrections/` registry). Fold a match into the pass. No area-10 correction has been filed yet, so this normally finds nothing; skip silently. The hook is live from day one so `insight-activation` can close the loop later.

## Step 1: Load context

1. **The initiative brief and whatever the human already has:** the investment being argued for, the audience (role, not name), the statistics and claims the human wants to use, any prior draft, and the decision the case feeds. This is what gets structured.
2. `sheerline/os/foundations/business-acumen/FOUNDATION.md` — the area-10 governed context. Its § The knowledge canon **first row** (the caveat-by-construction, with the traced provenance status of the McKinsey and "$1 → $100" figures) and its stakeholder-buy-in row are the spine of Step 2. Register under it; do not author it.
3. `references/business-case-canon.md` — the four-step structure, the four-state provenance taxonomy, the caveat block verbatim, the pricing refusal, and the hand-off to measurability. THE method spine.
4. `references/worked-example.md` — a filled Design Business Case Draft on synthetic input. Read it to calibrate register and depth on the free-prose slots; do not copy its findings.
5. The engagement-intake resolution (`sheerline/profile/engagement-intake.yaml`): the client's voice source (`brand_voice_source` / `voice_prohibited`), the em-dash policy (`dash_rule`), the hermetic-seal state (`hermetic_seal_confirmed`), and any engagement-specific `do_not_automate` calls. Output copy uses the client's (the designer's organization's) voice, never HeyHi's; no client name appears on a shared artifact when the seal is confirmed.

## Step 2: Build the draft, mechanically

Each step is mechanical. None of it makes the business claim, states an ROI number, or takes a stance.

1. **Problem (candidate).** Restate the problem the investment addresses in one or two sentences the audience would recognize, labeled `[candidate — agent-drafted]`. Name any ambiguity (is the problem speed, quality, or risk?) without resolving it.
2. **Evidence ledger with the claims-provenance check.** Every statistic or external claim the draft would lean on gets a row: the claim, its source as given, a **provenance status** (`verified-primary` / `partially-verified` / `unverifiable` / `unsourced`), a **correlational / causal-as-stated** flag, and a note. An `unsourced` or `unverifiable` claim is **flagged, never asserted**; the row proposes a qualitative restatement or a verified alternative. Provenance is checked against what can actually be traced in the session; a claim the skill cannot trace is not upgraded on the human's say-so. **When a source is reachable and the brief misquotes it** (a percentage where the source says percentage points, a five-year figure quoted as annual), the row keeps its `verified-primary` status, the note records the correction, and only the corrected form appears in the draft, inside the caveat block if it is a design-ROI figure. **When a named source cannot be reached this session** (no web access, a paid report, a login wall), the status is `partially-verified` with the note "primary not reachable this session" (an attribution exists; the primary was not inspected), never `verified-primary` on the attribution alone; a claim with **no** source offered stays `unsourced` regardless of reachability. The two figures already traced in the foundation's first canon row may be reused at their recorded status without re-tracing.
3. **The design-ROI caveat, by construction.** Whenever the McKinsey Design Index figure, the "$1 → $100 / 9,900%" figure, or any other design-ROI statistic appears in the evidence, insert the foundation's caveat block (canon § 3) with each figure's provenance status. The figures may appear **inside** the block, never as a headline claim. If no design-ROI figure appears, the block still appears as a standing note so the reader knows the drafter looked.
4. **Response (described, not chosen).** Describe the design investment as the human framed it: what it is, what it would change, what it depends on. The description is structured; it does not argue that this is the right response.
5. **Measurable expectation (candidate signals).** Name the signals that would move if the response worked, each labeled a candidate, and hand off: "for the metric scaffold, run `design-measurability-mapper`; the metric and the target are the team's." No target is set here.
6. **Pricing check.** Scan the draft for any currency amount, rate, day-rate, fee, or budget figure, including one spoken out in words. Remove each, record the removal in the pricing-check line, and say why: the pricing rule is absolute and a case is an argument, not a quote. A budget conversation happens between humans. **Scope is not price:** headcount and duration ("two designers for six months," "about ten weekend hours") describe the investment and stay; only currency, rates, and budget figures go. **The scan covers the whole artifact**, including a reproduced or quoted brief: if the draft reproduces the brief, redact the currency there too (write `[a currency figure]`), or the pricing check's "none remains" is false.
7. **Open questions and near-misses.** What the brief does not answer and what you would ask the audience or the design lead (questions, not recommendations); claims considered and set aside, figures that almost passed provenance, what could not be traced (traces, no verdicts).

## Step 3: Produce the Design Business Case Draft

Output this exact structure. The two judgment slots stay empty by construction.

```
# Design Business Case Draft — [initiative] · for [audience role]
Source artifacts: [what the human brought]     Drafted: [date]

## Problem (candidate — the human confirms it)
[candidate — agent-drafted] …

## Evidence ledger
| # | Claim | Source (as given) | Provenance | Correlational / causal-as-stated | Synthetic? | Note |
   provenance ∈ verified-primary / partially-verified / unverifiable / unsourced
   correlational flag: correlational / causal-as-stated / n/a (observation) for an internal measurement
   Synthetic?: `synthetic (modeled)` for any modeled or projected figure, on every surface it appears; blank otherwise
   An unsourced or unverifiable claim is FLAGGED with a proposed qualitative restatement, never asserted.

## ⚠ Design-ROI figures — caveat (inserted by construction)
[The foundation's caveat block: the McKinsey Design Index figure (correlational, verified-primary)
 and the "$1 → $100" figure (partially-verified at best, causal-as-stated) are correlational and
 weak-provenance; their provenance status is listed here; neither appears as a headline claim.]

## Response (the design investment, described — not chosen)
…

## Measurable expectation (candidate signals; hands to design-measurability-mapper)
- [candidate signal] …
The metric and the target are the team's; run design-measurability-mapper for the scaffold.

## Pricing check
[No currency / rate / fee present — or: N items removed, listed with the reason.]

## Open questions for the audience (questions, not judgments)
## Near-misses and unchecked territory
- Considered, set aside: …
- Almost passed provenance: …
- Could not trace: …

## ⛔ The business claim — NEEDS HUMAN
What design will do for which number is the designer's claim to make, not the drafter's.
   The claim: ____________________

## ⛔ Positioning stance — NEEDS HUMAN
   The stance this case takes: ____________________

## Named gate
Sign-off owner (design lead): ____________________  Date: ______
No claim, stance, or number is recorded until this line is signed by a human.
```

**The draft is done when** the problem is restated as a candidate, every claim carries a provenance status and a correlational flag, every unsourced or unverifiable claim is flagged with a restatement, the caveat block is present, the response is described and not argued, the measurable expectation names candidate signals and hands off, the pricing check reports zero currency figures remaining, the open questions are questions, and the two ⛔ slots are still blank.

## Step 4: Pre-flight verification

Confirm: no business claim or ROI number appears anywhere (including inside the response or a note); no correlational figure is presented as causal outside the caveat block; no `unsourced` or `unverifiable` claim is asserted as fact; no provenance status was upgraded on the human's assertion alone; the caveat block is present; no currency amount, rate, or fee remains anywhere in the artifact, a reproduced brief included; headcount and duration were not stripped as if they were prices; the measurable expectation names candidates and sets no target; the em-dash policy in the intake's `dash_rule` is honored; each open question is phrased as a question; the copy uses the client's voice per `engagement-intake.yaml` and carries no client name when `hermetic_seal_confirmed` is true; anything modeled or illustrative is tagged `synthetic`.

---

## What is explicitly out of scope

- **The business claim and the positioning stance.** Empty by construction. The draft lays out the evidence and its provenance; the human says what design will deliver.
- **Any price, rate, fee, or budget figure.** Removed and recorded. The pricing rule is absolute.
- **Upgrading a claim's provenance because the human says it is true.** The ledger records what can be traced; a claim that cannot be traced is flagged, and the human may still choose to use it, knowingly, at the gate.
- **HeyHi proposals** — `heyhi-proposal`. **Slides** — `heyhi-deck`. **Auditing a cited experiment** — `experiment-readout-linter`. **The metric and the target** — `design-measurability-mapper`, then the human.

---

## Exit Gate Required Headers (bottom-of-skill bracket)

This skill closes through Exit Gate Flavor A (`CLAUDE-SESSION-RULES.md § Exit Gate`). Before declaring done, confirm every required header holds real content:

- `## Fixes Applied` (or the delivered Design Business Case Draft)
- `## Smoke Test` (the Step 4 pre-flight checks, pasted)
- `## Next Session Prompt`

If the business-claim or positioning slot is filled, a currency figure remains, or an unsourced claim is asserted, the gate has **not** been satisfied.

---

*HeyHi Confidential. Sheerline area 10 (Business Acumen), P3, build class N. Tier 1 (buildable-now, self-application-first) — deployed 2026-09-05 (v0.1.1, Bucket B promotion pass; staged #781), registered in both registries. Spec source: `plans/plan-sheerline-p3-business-acumen-2026-09-05.md` § 4 / § 5 / § 6 / § 9. Foundation: `sheerline/os/foundations/business-acumen/FOUNDATION.md`. Boundary: `sheerline/os/operating-principles.md`.*
