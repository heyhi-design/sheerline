---
name: heyhi-a11y-audit
description: >-
  Run a standalone WCAG 2.2 conformance audit and produce an ACR/VPAT-shaped
  per-criterion report at a stated conformance level. Consumes the deterministic
  accessibility floor (the DS-MCP conformance lane and the heyhi-mcp validator's
  accessibility rules) for the automated tier — contrast, target size, ARIA
  validity, alt/label/focus/landmark presence, heading structure — and never
  re-implements contrast math. The judged tier ships EMPTY (NEEDS HUMAN / AT
  CONFIRMATION): does it work for an assistive-technology user, alt-text
  meaningfulness, focus-order logic, whether the ARIA is right, severity for real
  disabled users, and the conformance verdict. Every ACR row carries a provenance
  label (automated / human-reviewed / AT-confirmed) so a never-confirmed row
  cannot roll into a conformance claim, and the conformance sign-off is a named
  human gate. Includes an assistive-technology testing protocol (keyboard
  traversal, screen-reader passes, 200% zoom / 400% reflow) as a MODE. Triggers:
  "run a WCAG audit", "accessibility conformance report", "is this AA conformant",
  "produce an ACR/VPAT", "screen-reader audit", "a11y audit". NOT for a design
  system's health, token drift, or component-code drift — that is a design-system
  audit (use heyhi-design-intelligence-audit; its accessibility spot-check ends
  where this begins). NOT for interaction completeness or "is this prototype
  ready" (use heyhi-prototype-audit). NOT for making the conformance claim itself
  — that is the human's signature at the named gate.
version: "0.1.0"
updated: "2026-08-27"
status: "Deployed — heyhi-skills/heyhi-a11y-audit/; registered in the main + Sheerline subset registries (Sheerline Wave G-2, 2026-08-28). Sheerline area 8 (Accessibility), P2, the area anchor. Spec: ai-services/design-intelligence/research/sheerline-skill-buildout-research-2026-08-09.md § 5.1. Canon: sheerline/os/foundations/accessibility/FOUNDATION.md. Boundary: § 9."
classification: HeyHi Confidential
---

# HeyHi Accessibility Audit

**Sheerline area 8 (Accessibility) · P2 · pure validate/audit skill (the area anchor).** A team brings a shipped page, a component, or a prototype and asks the conformance question: "is this AA conformant, and can we say so?" This skill produces the answer in the shape the answer is asked for — an **ACR/VPAT-shaped, per-criterion report at a stated conformance level**. It runs the deterministic checks a machine can settle, lays out every WCAG 2.2 AA criterion the machine cannot, and hands the *conformance verdict itself* back to a human at a named gate. It is the "does it actually work for an assistive-technology user" instrument: it structures the evidence, it never issues the claim.

**The boundary this skill obeys (Sheerline § 9, absolute).** A structured artifact with explicit empty judgment slots, a named human gate, and provenance labels on anything synthetic or machine-derived. *The per-criterion conformance verdicts and the overall conformance claim are the empty slots.* Running the automated tier and laying out the criteria grid is mechanical; deciding whether the interface works for a disabled user, how severe a defect is for a real person, and whether the thing conforms is judgment. **An automated pass is never a conformance claim.** A version of this skill that reads "Supports Level AA" off a clean automated scan has exceeded its charter — grades never gates; mechanics never taste.

> **This skill closes through the Exit Gate (`CLAUDE-SESSION-RULES.md § Exit Gate`).** See the bottom-of-skill bracket.

---

## Routing — disambiguation with sibling skills

| If the task is… | Use |
|---|---|
| A WCAG conformance audit → an ACR/VPAT per-criterion report at a stated level; a screen-reader / keyboard / reflow pass | **this skill** |
| A **design system's** health — token drift, component-code drift, Figma file health, an accessibility *spot-check* inside a broader system diagnosis | `heyhi-design-intelligence-audit` (its Area 5 line already says "a full accessibility audit should be a separate engagement" — that seam is this skill) |
| Interaction completeness / "is this prototype ready to show" | `heyhi-prototype-audit` |
| Annotating a design or prototype with the accessibility spec *before* build (headings, landmarks, focus order, alt, name/role/value, target size) | `heyhi-a11y-annotation` (the design-side extension; build after this anchor) |
| Making the conformance claim, or signing the ACR | **the human** (this skill's named gate) |

The seam with `heyhi-design-intelligence-audit` is object and depth: DI-audit measures a *system's* health and runs an accessibility *spot-check* as one of its areas; this skill runs a *full, criterion-by-criterion conformance audit* on a specific surface and produces the governed ACR/VPAT artifact. The seam with `heyhi-prototype-audit` is question: prototype-audit asks "are the interactions complete"; this asks "does it conform, and does it work for an assistive-technology user." Reciprocal `not_for` clauses in the skill registries hold the boundary in both directions.

---

## Modes

This skill runs in two modes over one shared artifact (the ACR). The assistive-technology testing protocol is a **mode of this skill, not a separate skill.**

- **Mode A — Conformance Audit (default).** Build the ACR/VPAT report: run the automated tier from the deterministic floor, lay out every WCAG 2.2 AA criterion, ship the judged verdicts empty (`NEEDS HUMAN / AT CONFIRMATION`), tag provenance on every row, and name the sign-off gate. This mode produces the artifact; it never fills the verdicts.
- **Mode B — Assistive-technology (AT) confirmation pass.** Run the manual AT-testing protocol (§ Step 4) against the surface — keyboard traversal, screen-reader passes on the WebAIM-weighted pairings, 200% zoom / 400% reflow — and record results that flip judged rows from `NEEDS HUMAN / AT CONFIRMATION` to `human-reviewed` or `AT-confirmed`. Mode B feeds Mode A's rows. The overall conformance sign-off still stays behind the human gate; an AT-confirmed row is confirmed *evidence*, not the claim.

If mode is unclear, ask one question: "Do you want the criteria grid built (Mode A), or is a human running assistive-technology tests whose results I should record onto it (Mode B)?"

---

## The provenance model (the mechanism that stops an automated pass from becoming a claim)

Every ACR row carries a **provenance label**. The label is the load-bearing part of this skill — it is what keeps a never-confirmed criterion from silently rolling into a conformance claim.

| Provenance | Meaning | May the row carry a VPAT verdict (Supports / Partially / Does Not Support)? |
|---|---|---|
| `automated` | Result came only from the deterministic floor (a defect scan). | **No.** Its conformance status stays `NOT YET EVALUATED`. An automated PASS means "no automated defect found," never "conforms." An automated FAIL is surfaced as *evidence toward* Does Not Support, but the verdict still needs human confirmation of context and severity. |
| `human-reviewed` | A person inspected the criterion in context (code, rendered output, intent). | Yes. |
| `AT-confirmed` | A person exercised the criterion with assistive technology (Mode B) and recorded the result. | Yes — the strongest evidence for the criteria only assistive technology can settle (does the screen reader announce it, is the focus order usable). |

**The rule, stated once:** a criterion's conformance status may read a real VPAT verdict *only* when its provenance is `human-reviewed` or `AT-confirmed`. A row still at `automated` keeps status `NOT YET EVALUATED — NEEDS HUMAN / AT CONFIRMATION`, even when the automated result is a clean PASS. The **overall conformance claim** (the "Supports all Level A and Level AA" line) aggregates *only* rows whose provenance is human-reviewed or AT-confirmed; any row still at `automated` blocks the aggregate claim by construction. This is how "an automated pass is never a conformance claim" is enforced mechanically rather than promised in prose.

Anything modeled, sampled, or machine-derived carries its provenance on every surface it appears, so a scan result can never be mistaken for a confirmed one.

---

## Step 0: Improvement hook check

Retrieve any recurring corrections for accessibility work (`retrieve_design_corrections` if the design MCP is reachable, or the Sheerline `os/corrections/` registry `category: accessibility` — the seeded `theme-flip-fill-needs-on-color-token` slot lives there, and the heyhi-mcp R1 runtime carries `contrast-pairing-not-declared-safe`). Fold a matching recurring correction into the pass. Skip silently if none.

## Step 1: Load context and determine mode

Read what the human brought and the governed canon it sits under.

1. The **subject of the audit** — the rendered surface, the component, the prototype, or the declared structured output. This is what gets audited; note whether you have live rendered output (required for Mode B and for the judged visual/AT criteria) or only source/markup (limits how far Mode A can reach — say so).
2. `sheerline/os/foundations/accessibility/FOUNDATION.md` — the area-8 canon: WCAG 2.2 on POUR, the nine criteria new in 2.2, the AA legal-version fork, ARIA APG + the first rule of ARIA, the AT-testing protocol, the automated-coverage ceiling, and the legal context. **This skill REFERENCES the foundation for the canon; it does not restate it.** Load it; do not copy it.
3. `references/acr-vpat-template.md` — the ACR/VPAT report structure, the VPAT verdict vocabulary, the criteria grid with the judged slots pre-marked empty, and the provenance column. THE artifact spine.
4. `references/at-testing-checklist.md` — the Mode B protocol: keyboard traversal, the WebAIM-weighted screen-reader pairings, and the zoom/reflow passes, each as a checklist that records `AT-confirmed` / defect / `not-run`.
5. The Sheerline area-8 governed context (`sheerline/os/foundations/registry.yaml` area-accessibility). Register under it; do not author it.

Determine the mode (§ Modes). Confirm which tier of evidence is available: is the deterministic floor reachable this session (the DS-MCP conformance lane / the heyhi-mcp validator's accessibility rules), and is there rendered output for the judged and AT passes? Record both — a floor that could not be reached is a gap in the report, never a silent pass.

## Step 2: Run the two tiers

### 2a. The automated tier — consumed, never re-implemented

Read the deterministic floor's results as the automated tier. **Do not re-implement any of this; consume it generically.** The floor already exists inside Sheerline's machinery (foundation § "The mechanical floor already exists"): the DS-MCP conformance lane, the heyhi-mcp validator's accessibility rules (Rule 2 contrast, Rule 3 touch-target below 44×44 as a warning, Rule 4 label coverage, Rule 5 focus state), the health-check C4 checks, and the eval harness's dimension 3. Consume whichever is reachable this session; **do not hard-depend on the unpromoted `heyhi-prototype-verify`** — name the mechanical source you actually read.

The automated tier covers, as a defect scan only:

- **Contrast** — read from the conformance lane / validator accessibility rules. **Do not re-implement contrast math.** A firing contrast defect maps to evidence toward SC 1.4.3 (Contrast Minimum) / 1.4.11 (Non-text Contrast). Pass the instance's own token set and any out-of-palette declaration through the validator's `constraints`; the floor reads the instance, not HeyHi's palette.
- **Target size** — the floor's Rule 3 flags controls below **44×44** (a warning, the stricter SC 2.5.5 Enhanced bar), *not* the SC 2.5.8 AA **24×24** minimum. A control between 24 and 44 px passes SC 2.5.8 (AA) yet trips the floor warning, so treat Rule 3 as an input toward SC 2.5.8 / 2.5.5, and the SC 2.5.8 (24×24) verdict itself as **judged**, never an automated pass.
- **ARIA validity** — is the ARIA well-formed and are name/role/value present (toward SC 4.1.2). Validity is mechanical; *whether the ARIA is the right ARIA* is judged (Step 3).
- **alt / label / focus / landmark presence** — does an image have an `alt` attribute at all, does a control have an accessible name, is there a visible focus style declared, do landmarks exist. This is *presence*, toward 1.1.1 / 3.3.2 / 2.4.7 / 1.3.1; *meaningfulness* is judged.
- **Heading structure** — presence and nesting order of headings, toward SC 1.3.1 / 2.4.6.

Every result from this tier is tagged provenance `automated`. A clean automated result is `PASS (no automated defect)`, not "conforms."

### 2b. The judged tier — laid out empty

For every WCAG 2.2 AA criterion whose verdict requires judgment — which is every criterion for a *conformance claim* — place the row with its conformance status set to `NOT YET EVALUATED — NEEDS HUMAN / AT CONFIRMATION` and provenance blank (to be filled `human-reviewed` or `AT-confirmed`). The judged half the automated tier structurally cannot reach, spelled out so the empty slots are visible:

- **Does it work for an assistive-technology user** — the criteria only Mode B can settle (screen-reader announcement, usable focus order, operable-by-keyboard-in-practice).
- **Alt-text meaningfulness** — the floor confirms an `alt` exists; whether it conveys the image's purpose is judged.
- **Focus-order logic** — the floor confirms focus styles exist; whether the order is logical is judged.
- **Whether the ARIA is right** — the floor confirms the ARIA is valid; whether it names the correct role/state (and whether native HTML should have been used instead — the first rule of ARIA) is judged.
- **Severity for real disabled users** — whether a defect is a blocker or an annoyance for an actual assistive-technology user. The automated tier flags presence; it cannot weigh impact.
- **The conformance verdict** — per criterion and overall. Empty by construction.

Do not fill these. Laying them out *is* the work of Step 2b; a criterion left off the grid is a worse failure than one left empty.

## Step 3: Produce the ACR/VPAT report

Output the structure in `references/acr-vpat-template.md`. The judged verdict slots and the overall conformance claim stay empty by construction; the provenance column is filled on every row.

```
# Accessibility Conformance Report — [surface / product name]
Subject: [what was audited]      Audited: [date]      Mode: A (grid) / B (AT pass recorded)
Audited against: WCAG 2.2, Level AA
Conformance claim maps to: [the version the jurisdiction names — see the AA legal-version fork]
Evidence available: [rendered output? floor reachable? which mechanical source was read?]

## Per-criterion table (WCAG 2.2, Level A + AA)
| WCAG 2.2 SC | Lvl | Automated result | Conformance status (VPAT) | Provenance | Remarks |
|-------------|-----|------------------|---------------------------|------------|---------|
| 1.4.3 Contrast (Minimum) | AA | PASS (no automated defect) | NOT YET EVALUATED — NEEDS HUMAN | automated | contrast scan clean; text-in-image + state contrast not machine-checkable |
| 1.1.1 Non-text Content   | A  | PASS (alt present)          | NOT YET EVALUATED — NEEDS HUMAN | automated | alt attributes present; MEANINGFULNESS needs human review |
| 2.5.8 Target Size (Min)  | AA | FAIL (2 controls < 24×24)  | NOT YET EVALUATED — NEEDS HUMAN | automated | evidence toward Does Not Support; human confirms severity/context |
| 2.4.3 Focus Order        | A  | not-automatable            | NOT YET EVALUATED — NEEDS AT    | (blank)  | focus-order logic is a Mode B / human call |
| 4.1.2 Name, Role, Value  | A  | PASS (ARIA valid)          | NOT YET EVALUATED — NEEDS AT    | automated | ARIA well-formed; whether it is the RIGHT role needs AT confirmation |
| …                         | …  | …                          | …                               | …        | (full 2.2 A+AA criteria set — foundation carries the canon) |

Note: SC 4.1.1 (Parsing) was removed in WCAG 2.2 — it is not audited.

## Automated tier summary (defect scan, provenance: automated)
[What the floor found and which mechanical source was read (conformance lane / validator rules /
 health-check C4 / eval dim 3). State the automated-coverage ceiling honestly: automated tooling
 reaches ~30–40% of WCAG issues by criteria type (a higher share by instance count); the judged
 remainder is large under either framing. This is a defect scan, NOT a conformance result.]

## Judged tier — NEEDS HUMAN / AT CONFIRMATION
[Every criterion whose provenance is still `automated` or blank, listed as the outstanding
 confirmation work: what a human reviewer and an AT tester still have to settle before any row can
 carry a VPAT verdict.]

## Open questions for the audit owner (questions, not judgments)
[What the subject or its context does not answer and what you would ask. Each ends in a question
 mark and asks rather than tells. No recommendation, no verdict.]
- [e.g. "Which jurisdiction's standard does the conformance claim need to map to? It sets whether
   we claim 2.2 AA or 2.1 AA."]
- [e.g. "Is there a data table here, or is that a layout grid? It changes which 1.3.1 checks apply."]

## Near-misses and unchecked territory (the audit journey, made inspectable)
[What was considered and passed, what almost flagged, and what could not be checked because there
 was no rendered output / the floor was unreachable / no AT pass was run. Traces, no verdicts.]
- Could not check: [e.g. "no rendered output this session, so all Mode B criteria return NEEDS AT."]

## ⛔ Conformance verdict — NEEDS HUMAN
This block is intentionally empty. An automated pass is not a conformance claim. No per-criterion
VPAT verdict is written until its row is human-reviewed or AT-confirmed, and the overall claim
aggregates only those rows.
   Overall conformance claim (target level): ____________________
   Maps to jurisdiction standard:            ____________________

## Named gate — conformance sign-off
Sign-off owner (accessibility lead / responsible engineer): ____________________   Date: ______
No conformance claim is recorded, and no ACR is issued, until this line is signed by a human.
Any row still at provenance `automated` must be resolved (or explicitly scoped out) before sign-off.
```

**The report is done when every WCAG 2.2 A+AA criterion has a row, every row carries a provenance label, every judged verdict slot is `NOT YET EVALUATED` (or a real verdict only where provenance is human-reviewed/AT-confirmed), the automated-coverage ceiling is stated honestly, the open-questions and near-misses surfaces carry questions/traces, and the conformance-verdict block and sign-off line are blank.** A report that writes "Supports Level AA" off an automated scan, or that omits a criterion to make the grid look complete, has failed its own charter.

## Step 4: Mode B — the assistive-technology (AT) testing protocol

The manual protocol that produces `AT-confirmed` (and `human-reviewed`) evidence. It is a **mode of this skill**, not a separate skill. Run it against rendered output; record each result onto the ACR row it settles, with a one-line note of what was observed. Full checklist: `references/at-testing-checklist.md`; canon: foundation § "The AT-testing protocol."

1. **Keyboard traversal.** Every interactive element reachable and operable by keyboard alone; visible focus at every stop; a logical focus order; no keyboard traps. Feeds 2.1.1 / 2.1.2 / 2.4.3 / 2.4.7 / 2.4.11.
2. **Screen-reader passes on the WebAIM-survey-weighted pairings.** JAWS + Chrome, NVDA + Chrome/Firefox, VoiceOver + Safari (macOS/iOS). Confirm names, roles, states, and announcements match intent — this is where "whether the ARIA is right" is settled. Feeds 1.1.1 (meaningfulness) / 1.3.1 / 4.1.2 / 4.1.3.
3. **200% zoom and 400% reflow.** Content and function survive 200% text zoom and 400% viewport reflow without loss or horizontal scrolling of content. Feeds 1.4.4 / 1.4.10.

Each line records `AT-confirmed` (with the pairing/observation), a defect (with severity a human assigns), or `not-run` (never a silent pass). A criterion no one exercised with assistive technology stays `NEEDS AT`; it does not graduate to a verdict.

## Step 5: Pre-flight verification

Before handing the report over, confirm:

- **Every criterion is present** (full WCAG 2.2 A+AA set; 4.1.1 excluded), and every row carries a provenance label.
- **No automated pass was upgraded to a verdict.** Every row at provenance `automated` reads `NOT YET EVALUATED`; a VPAT verdict appears only where provenance is `human-reviewed` or `AT-confirmed`.
- **The overall conformance claim aggregates only confirmed rows**, and the conformance-verdict block + sign-off line are blank.
- **Contrast math was not re-implemented** — the contrast result was read from the floor, and the mechanical source you read is named.
- **The AA legal-version fork is resolved or flagged** (§ below): the report audits to 2.2 AA and states the version the claim maps to, or raises the jurisdiction question as an open question.
- **The automated-coverage ceiling is stated honestly** — the report never positions itself as "we ran axe."
- **Every FAIL cites a specific element/location** (not a generic "check contrast"), and every open question is a question, every near-miss a trace.

---

## The AA legal-version fork (audit to the newer standard, claim to the named one)

Audit *to* WCAG 2.2 AA — the current, strictest baseline. But the conformance *claim* maps to the version the jurisdiction names: some legal regimes (EAA, ADA Title II referencing) still cite 2.1 AA, or 2.0. **Audit to the newer standard; claim to the named one; never assert a version the law does not require.** If the jurisdiction is not stated, that is an open question for the audit owner, not an assumption to make. Legal-timeline facts of record (EAA in force since 28 June 2025; ADA Title II deadlines slipped ~a year under an April-2026 rule — retire any "2026 ADA deadline" framing; WCAG 3.0 still a Working Draft, not before 2028 — anchor on 2.2 AA) live in the foundation § "Legal context." Do not restate them here; read them there. Position the audit on the judged half, the governed ACR/VPAT artifact, and AT confirmation — never on "we run axe" (the mechanical floor is commoditized).

---

## What is explicitly out of scope

- **The conformance verdict and the conformance claim.** Empty by construction (§ 9). The skill can say "contrast scan clean, focus order not yet confirmed by AT"; it cannot say "conforms to AA." That is the human's signature.
- **Re-implementing contrast math (or any of the automated floor).** Consumed generically from the deterministic floor; never rebuilt. If the floor is unreachable this session, that is a gap in the report, not an invitation to recompute contrast by hand.
- **Design-system health, token drift, component-code drift** — `heyhi-design-intelligence-audit` (its Area 5 spot-check is where this skill's engagement begins). **Interaction completeness / prototype readiness** — `heyhi-prototype-audit`. **Design-side accessibility annotation before build** — `heyhi-a11y-annotation`.
- **Legal advice.** The skill maps a conformance claim to a named standard; it does not opine on legal exposure or represent that a claim satisfies any statute. That is counsel's call.

---

## Exit Gate Required Headers (bottom-of-skill bracket)

This skill closes through Exit Gate Flavor A (`CLAUDE-SESSION-RULES.md § Exit Gate`). Before declaring done, confirm every required header holds real content, not a claim:

- `## Fixes Applied` (or, for an audit run, the delivered Accessibility Conformance Report)
- `## Smoke Test` (the Step 5 pre-flight checks, pasted)
- `## Next Session Prompt`

If the conformance-verdict block is filled, or any row carries a VPAT verdict while its provenance is still `automated`, or a criterion was omitted to complete the grid, the gate has **not** been satisfied.

---

*HeyHi Confidential. Sheerline area 8 (Accessibility), P2 net-new — the area anchor. Deployed in `heyhi-skills/heyhi-a11y-audit/`; registered in the main + Sheerline subset registries (Wave G-2, 2026-08-28). Spec source: `ai-services/design-intelligence/research/sheerline-skill-buildout-research-2026-08-09.md` § 5.1. Canon by reference: `sheerline/os/foundations/accessibility/FOUNDATION.md`. Boundary: § 9.*
