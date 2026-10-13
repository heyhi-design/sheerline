---
classification: "HeyHi Internal Use Only"
created: "2026-04-27"
version: "1.0"
type: "reference-template"
scope: "design-system-engagement"
---

# Engagement Plan Template

*For use across Design System Audit, Build, and Care engagements.*

---

## 1. What This Template Is For

HeyHi practitioners use this template to structure any design system engagement before work begins. It formalizes two structural requirements that do not have a natural owner without an explicit template: the Definition of Done as a phase-start artifact (declared before scope items are listed, never appended afterward), and the Phase Gate as the explicit transition mechanism between phases (three states: PASS, OPEN, FAIL). Make a copy per engagement, populate all [BRACKET] fields with client-specific values, and do not alter the section ordering; the ordering is architectural.

---

## 2. Engagement Overview

| Field | Value |
|-------|-------|
| Client | [CLIENT NAME] |
| Engagement Type | [Audit / Build / Care] |
| Phase Count | [NUMBER] |
| Primary Contact | [NAME, role] |
| Start Date | [YYYY-MM-DD] |
| Status | [Planning / Active / On Hold / Closed] |

---

## 3. Definition of Done: Phase Level

**This section appears at the top of every phase description, before any scope items are listed. A phase with no DoD is unscoped.**

The DoD is declared when the phase is planned, not written retrospectively. Each criterion is verifiable: "tested" is not a criterion; "zero console errors in both light and dark mode, confirmed in browser" is. Where the universal items below do not apply to a specific phase, replace them with phase-specific items of equivalent specificity. Do not leave placeholders empty and do not remove items without a written rationale.

**Universal DoD items (starting point for every phase; add phase-specific items below):**

- [ ] Token migration verified: all new or modified components reference semantic tokens only: no raw hex values, no `rgba()` expressions, no Tailwind arbitrary values (`text-[12px]`, `bg-[#fff]`) in changed files. Confirmed by running the grep suite against `src/` and reviewing output.
- [ ] Storybook stories present for all deliverable components: all variants, all states, dark mode rendering verified, i18n usage note included where user-facing strings are involved.
- [ ] Dark mode tested: each component renders correctly under the `.dark` class with no fallback to light mode token values. Dark mode token values are explicitly defined, not inherited from the light tier.
- [ ] Figma components match code: at least one `get_design_context` comparison completed for each high-stakes component in this phase. Result recorded in the PR description or session notes.
- [ ] No hardcoded values remaining in files changed by this phase. Grep scan run and output documented.
- [ ] Zero TypeScript errors and zero ESLint violations on all changed files.
- [ ] Accessibility: all interactive components have a visible `focus-visible` ring using a semantic token class. Touch targets verified at 44×44px minimum.

**Phase-specific DoD additions:**

- [ ] [PHASE-SPECIFIC CRITERION: must name a verifiable outcome, not a goal]
- [ ] [PHASE-SPECIFIC CRITERION]

**This section is never optional. A phase with no DoD is unscoped.**

---

## 4. Scope Items

*Scope items are listed after the DoD. This ordering is not stylistic: it ensures the definition of done is established before the scope is described, not derived from it.*

For each item in this phase, complete one block:

---

**Item:** [ITEM TITLE: specific enough to be unambiguous]

**What it does:** [One to two sentences. What state does this item move the system to, and why does that matter for the phase's goal?]

**Prerequisites:** [List explicit prerequisites: components that must be merged, decisions that must be recorded, conditions that must be confirmed. Do not write "N/A" without a note explaining why no prerequisites exist for this item. An unresolved prerequisite means this item is not ready to start.]

**Verification method:** [Name the specific check that confirms this item is complete: a grep scan with the exact command, a `get_design_context` comparison, a PR checklist review against named items, a smoke test with a defined pass condition. A verification method that cannot be executed is not a method.]

**Status:** [Not started / In progress / Complete / Blocked: specific reason and unblocking owner if blocked]

---

*Add one block per scope item. These blocks supplement the phase DoD; they do not replace it.*

---

## 5. Phase Gate: PASS / OPEN / FAIL

The gate runs at the end of every phase, before the next phase opens. Each condition is assigned exactly one of three states. No other states exist; remove conditions that do not apply to this engagement rather than marking them N/A or TBD.

### State Definitions

| State | Meaning | What happens next |
|-------|---------|-------------------|
| **PASS** | Condition confirmed met. Verified, not assumed. Evidence exists. | Phase transition proceeds for this condition. |
| **OPEN** | Condition known-incomplete. Blocking until resolved or explicitly deferred with a decision record. | Phase transition is held until the owner resolves the condition or records a deferral decision. |
| **FAIL** | Condition attempted and confirmed unable to be met in this phase. | Requires a scope change or a decision record. Not silence, not deferral to the next phase without a structural response. FAIL items do not become OPEN items. |

### Rules

1. Every OPEN item must have a named owner and a documented resolution path before the next phase begins. An unowned OPEN item is a gap, not a decision.
2. Every FAIL item requires a decision entry: name the condition, state why it cannot be met, and record what changes as a result: scope reduction, phase extension, or explicit acceptance of the gap with a rationale.
3. If a condition does not apply to this engagement, remove it from the gate. Do not use N/A, TBD, or any state outside the three defined above.

### Gate Table

Instantiate one table per phase transition. Archive the prior table with its run date when the next phase begins.

| Condition | State | Owner | Resolution Path or Note |
|-----------|-------|-------|------------------------|
| [CONDITION: specific and verifiable] | PASS / OPEN / FAIL | [NAME] | [Required for OPEN and FAIL; optional for PASS] |
| [CONDITION] | PASS / OPEN / FAIL | [NAME] | |
| [CONDITION] | PASS / OPEN / FAIL | [NAME] | |

**Standard gate conditions for Design Discovery → Implementation (Phase 2 → Phase 3):**

- Brand config written and passes the pipeline-validator smoke test
- All architecture decisions recorded (composition model, styling approach, icon system, form primitive API, documentation format)
- Migration map complete: no "Evaluate" entries remaining; each component action must be Token-align, Refactor, New, Deprecate, or Governed External
- All blocking open questions from the audit have a recorded resolution or an explicit deferral decision

**Standard gate conditions for Implementation → Validation (Phase 3 → Phase 4):**

- Each PR passed the reviewer checklist before merge; no PR merged with open checklist items
- All deprecated components have a `@deprecated` JSDoc comment and an active `no-restricted-imports` ESLint entry
- Accessibility checkpoint complete: ARIA roles, focus trap behavior, and keyboard navigation verified on all interactive components shipped in this phase
- Team feedback session scheduled (within one week of the final component PR merging, before the cleanup PR opens)

---

## 6. Kickoff Checklist

Complete before Phase 1 begins. These items are a precondition for starting the engagement, not a gate between phases.

- [ ] **Access confirmed.** Figma file (view rights minimum), codebase (read access minimum), and documentation (Storybook, Confluence, or equivalent) all verified and functional before the audit session.
- [ ] **Baselines recorded.** Token count, component count, and bundle size captured before any work begins. These establish the before-state for all success criteria. Three commands to run and record:
  - Hardcoded color count (token migration baseline): `grep -rE "#[0-9a-fA-F]{3,6}\b" src/ --include="*.tsx" --include="*.jsx" | wc -l`
  - Component count: `ls src/components/ | wc -l` (adjust path to match the client's component directory)
  - Bundle size: run the production build and capture the output size for the main JS chunk

  Record all three results in the engagement plan or a named baseline file before Phase 1 begins.
- [ ] **DoD agreed with client stakeholder.** The phase-level DoD, or its engineering-facing equivalent, has been reviewed with the primary technical contact. They understand what each phase's completion state looks like before Phase 1 starts.
- [ ] **Escalation path named.** A specific person (name and role) is designated to receive findings that require a scope change, a timeline extension, or a structural decision. This is not the day-to-day reviewer. It is the person who can say yes or no to a change in direction.
- [ ] **Engagement alignment confirmed.** Scope, phase structure, and timeline reviewed with the product or engineering lead. No feature freeze or major infrastructure migration is planned during the implementation window.

---

## 7. How to Use This Template

Copy this file, rename it `engagement-plan-[client-slug].md`, and populate all [BRACKET] fields before Phase 1 begins. The DoD (Section 3) must be completed before Section 4 scope items are written: this ordering is the point of the template, not a formatting preference. At each phase transition, instantiate a new gate table (Section 5) with the conditions relevant to that transition, and archive the prior table with the date it was run.

---

*HeyHi Internal Use Only*
