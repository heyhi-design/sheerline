---
classification: confidential
title: "ACR/VPAT report template — the artifact spine"
skill: heyhi-a11y-audit
loaded_by: "SKILL.md Step 1"
---

# ACR/VPAT report template

The structured artifact `heyhi-a11y-audit` produces, held as *fill-and-apply reference*. It is an **Accessibility Conformance Report** in the shape a VPAT is read in — per-criterion, at a stated level — with the judged verdicts shipped empty and a provenance label on every row. On-demand: load when running the audit.

*Internal operational reference (staged under `skill-updates/`): em-dash limit exempt per `OPERATING_PRINCIPLES.md`. The WCAG 2.2 canon, POUR, the nine new-in-2.2 criteria, and the ARIA/first-rule material are NOT restated here — they live in `sheerline/os/foundations/accessibility/FOUNDATION.md`. This file carries the report structure only.*

---

## What ACR and VPAT are (one line each, so the artifact reads right)

- A **VPAT** (Voluntary Product Accessibility Template) is the industry template for reporting how a product measures against accessibility standards, criterion by criterion.
- An **ACR** (Accessibility Conformance Report) is the *filled-in* VPAT — the actual report for a specific product at a point in time.

This skill produces an ACR-shaped report. It is "VPAT-shaped" because it uses the VPAT verdict vocabulary and the per-criterion table; it is not a legal instrument and does not represent that a claim satisfies any statute (that is counsel's call, per SKILL.md § out of scope).

## The VPAT verdict vocabulary (the conformance-status column)

The conformance-status column uses the standard VPAT terms — but every one of them is a **judged verdict** and ships empty until the row's provenance is `human-reviewed` or `AT-confirmed`.

| Verdict | Meaning | Who may write it |
|---|---|---|
| **Supports** | The functionality meets the criterion. | Human, after review/AT |
| **Partially Supports** | Some functionality does not meet the criterion. | Human, after review/AT |
| **Does Not Support** | The majority of functionality does not meet the criterion. | Human, after review/AT (an automated FAIL is *evidence toward* this, not the verdict) |
| **Not Applicable** | The criterion does not apply to the subject. | Human (applicability is a judgment) |
| **NOT YET EVALUATED — NEEDS HUMAN / AT CONFIRMATION** | The default. No confirmed evaluation yet. | The skill (this is what ships) |

The skill only ever writes the last row's value. The first four are the human's, at the gate.

## The provenance column (the mechanism, restated for the fill-in)

Every row carries one of `automated` / `human-reviewed` / `AT-confirmed` (or blank, for a not-yet-touched judged row). The binding rule: **a real VPAT verdict may appear only where provenance is `human-reviewed` or `AT-confirmed`.** A row at `automated` keeps `NOT YET EVALUATED`, even on a clean scan. The overall conformance claim aggregates only human-reviewed/AT-confirmed rows. See SKILL.md § "The provenance model" for the full table.

## The report structure

```
# Accessibility Conformance Report — [surface / product name]
Subject: [what was audited — a page, a component, a prototype, declared structured output]
Audited: [date]      Mode: A (grid built) / B (AT pass recorded onto it)
Audited against: WCAG 2.2, Level AA
Conformance claim maps to: [the version the jurisdiction names — AA legal-version fork; if
                            unknown, "OPEN QUESTION — jurisdiction not stated"]
Evidence available: [rendered output present? deterministic floor reachable, and which source
                     was read? AT pass run?]

## Per-criterion table (WCAG 2.2, Level A + AA — the full set)
| WCAG 2.2 SC | Lvl | Automated result | Conformance status (VPAT) | Provenance | Remarks |
|-------------|-----|------------------|---------------------------|------------|---------|
| 1.1.1 Non-text Content        | A  | PASS (alt present) / FAIL / N/A | NOT YET EVALUATED | automated | presence only; MEANINGFULNESS is judged |
| 1.3.1 Info and Relationships  | A  | PASS (headings/landmarks present) | NOT YET EVALUATED | automated | structure present; semantics-correct is judged |
| 1.4.3 Contrast (Minimum)      | AA | PASS/FAIL (read from floor) | NOT YET EVALUATED | automated | contrast math NOT re-implemented; text-in-image + state contrast not machine-checkable |
| 1.4.4 Resize Text             | AA | not-automatable | NOT YET EVALUATED — NEEDS AT | (blank) | 200% zoom = Mode B |
| 1.4.10 Reflow                 | AA | not-automatable | NOT YET EVALUATED — NEEDS AT | (blank) | 400% reflow = Mode B |
| 1.4.11 Non-text Contrast      | AA | PASS/FAIL (from floor) | NOT YET EVALUATED | automated | UI-component + graphics contrast |
| 2.1.1 Keyboard                | A  | not-automatable | NOT YET EVALUATED — NEEDS AT | (blank) | keyboard traversal = Mode B |
| 2.1.2 No Keyboard Trap        | A  | not-automatable | NOT YET EVALUATED — NEEDS AT | (blank) | Mode B |
| 2.4.3 Focus Order             | A  | not-automatable | NOT YET EVALUATED — NEEDS AT | (blank) | focus-order LOGIC is judged |
| 2.4.6 Headings and Labels     | AA | PASS (present) | NOT YET EVALUATED | automated | descriptiveness is judged |
| 2.4.7 Focus Visible           | AA | PASS (focus style declared) / FAIL | NOT YET EVALUATED | automated | declared ≠ usable; confirm in Mode B |
| 2.4.11 Focus Not Obscured (Min) | AA | not-automatable | NOT YET EVALUATED — NEEDS AT | (blank) | new in 2.2; Mode B |
| 2.5.8 Target Size (Minimum)   | AA | floor Rule 3 warns <44×44 (stricter than 24×24 AA) | NOT YET EVALUATED — NEEDS HUMAN | automated (input only) | new in 2.2; floor checks 44×44, so 24×24 AA is JUDGED, not an automated pass |
| 3.2.6 Consistent Help         | A  | not-automatable | NOT YET EVALUATED | (blank) | new in 2.2; judged |
| 3.3.2 Labels or Instructions  | A  | PASS (label present) | NOT YET EVALUATED | automated | presence; adequacy is judged |
| 3.3.7 Redundant Entry         | A  | not-automatable | NOT YET EVALUATED | (blank) | new in 2.2; judged |
| 3.3.8 Accessible Auth (Min)   | AA | not-automatable | NOT YET EVALUATED | (blank) | new in 2.2; judged |
| 4.1.2 Name, Role, Value       | A  | PASS (ARIA valid) / FAIL | NOT YET EVALUATED — NEEDS AT | automated | validity ≠ the RIGHT role; confirm in Mode B |
| 4.1.3 Status Messages         | AA | not-automatable | NOT YET EVALUATED — NEEDS AT | (blank) | announced-to-AT is Mode B |
| … (remaining WCAG 2.2 A + AA criteria — foundation carries the full 87-SC canon) | | | | | |

Excluded by construction: SC 4.1.1 (Parsing) — removed in WCAG 2.2, not audited.
The rows above are the high-frequency + all-nine-new-in-2.2 anchors; the full A+AA set must
appear in a real ACR. The foundation's POUR canon is the source for the complete list.

## Automated tier summary (defect scan — provenance: automated)
[What the deterministic floor found, and which mechanical source was actually read (the DS-MCP
 conformance lane / heyhi-mcp validator accessibility Rules 2 & 5 / health-check C4 / eval dim 3).
 State the automated-coverage ceiling HONESTLY: ~30–40% of WCAG issues by criteria type, a higher
 share by instance count (Deque reports ~57% of instances); the judged remainder is large under
 either framing. This is a defect scan, NOT a conformance result — the mechanical floor is
 commoditized (axe/Lighthouse are free); the value is the judged half + this governed artifact.]

## Judged tier — NEEDS HUMAN / AT CONFIRMATION
[Every criterion still at provenance `automated` or blank, listed as outstanding confirmation work:
 what a reviewer and an AT tester must still settle before any row can carry a verdict. This is the
 honest map of how far the audit has and has NOT gone.]

## Open questions for the audit owner (questions, not judgments)
- [e.g. "Which jurisdiction's standard does the claim map to? It sets 2.2 AA vs 2.1 AA."]
- [e.g. "Is this a data table or a layout grid? It changes which 1.3.1 checks apply."]

## Near-misses and unchecked territory (the audit journey, made inspectable)
- Considered, did not flag: [e.g. "the icon-only buttons looked unlabeled; each carries an
   aria-label — no automated FAIL, meaningfulness still needs AT."]
- Could not check: [e.g. "no rendered output this session — all Mode B criteria return NEEDS AT."]

## ⛔ Conformance verdict — NEEDS HUMAN
This block is intentionally empty. An automated pass is not a conformance claim.
   Overall conformance claim (target level): ____________________
   Maps to jurisdiction standard:            ____________________

## Named gate — conformance sign-off
Sign-off owner (accessibility lead / responsible engineer): ____________________   Date: ______
No conformance claim is recorded, and no ACR is issued, until this line is signed.
Any row still at provenance `automated` must be resolved or explicitly scoped out before sign-off.
```

## Why the conformance verdict ships empty

A conformance claim is a representation a product makes to its buyers, its users, and — where a standard is cited in law — to a regulator. Whether an interface *works for a disabled person* is not settled by a clean scan; it is settled by review and by exercising the thing with assistive technology. The skill can lay out every criterion, read the deterministic floor onto the rows it settles, and run the AT protocol; the *claim* is the human's, at the gate. An ACR that writes "Supports Level AA" off automated results has made — quietly, on the product's behalf — the one representation the boundary reserves for a person.

*HeyHi Confidential. Reference for `heyhi-a11y-audit`. Spec source: `sheerline-skill-buildout-research-2026-08-09.md` § 5.1. Canon: `sheerline/os/foundations/accessibility/FOUNDATION.md`.*
