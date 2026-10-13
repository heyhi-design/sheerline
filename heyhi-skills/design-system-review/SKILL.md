---
name: design-system-review
description: >-
  Run a structured visual fidelity review on a design system config and its generated output. Use at any design system milestone: v0 → v1 promotion (Mode D provisional to confirmed), component release gates, after significant token changes, or as a periodic config fidelity check. Triggers: "review the design system," "validate the config against the moodboard," "run a fidelity check," "does this match the design intent," "v0 to v1 review," "promote the config," "token validation," "config fidelity check," "review generated output," "does this look right," "flag what's off." Not for: token value authoring (use heyhi-token-description-author), new system onboarding (use design-system-onboard), monthly drift monitoring (use design-system-care-monthly), or auditing the health of a client's design system — drift, coverage, documentation, team relationship (use heyhi-design-intelligence-audit).
version: "1.0.2"
updated: "2026-10-13"
changes: "v1.0.2 (2026-10-13): Generalized for the Sheerline scaffold: instance data (brand defaults, client/engagement history, owner names, ratified values) moved to instance-only files or neutral wording; method unchanged. v1.0.1 (2026-07-04): description rescoped by the setup-grade routing pass (PR #295) — 'design system health check' trigger reworded to 'config fidelity check'; mutual not_for added with heyhi-design-intelligence-audit. v1.0.0 (2026-07-04): version/updated frontmatter added retroactively (setup-grade F15 — this was the only deployed skill with no version field), covering the skill as first committed 2026-03-20 plus in-place refinements through 2026-06-10 (Build-pipeline dry-run workflow integrations, PR #166). Version history before this line is reconstructable only from git."
---

# Design System Review

Structured visual fidelity review for a design system config and its generated output. Validates that what the system produces actually reflects the design intent it was built from.

---

> **Exit Gate (Flavor A).** This skill closes through the canonical Exit Gate — see `CLAUDE-SESSION-RULES.md § Exit Gate`. Required headers, in order: `## Fixes Applied`, `## Smoke Test`, `## Next Session Prompt`. Empty headers are visible failures.


## Overview

The review answers one question: **does the generated output match the design intent?**

This is not a code review. It is not an accessibility audit. It is the taste checkpoint — the structured comparison between what the designer intended and what the system produced. Design intent lives in the moodboard, the locked direction, or the original brand brief. Generated output lives in components, pages, and prototypes built against the config.

The review runs in two modes:

**Mode A — v0 → v1 Promotion:** Triggered after Mode D produces a provisional config and at least one piece of generated output exists. Goal: resolve all provisional fields and confirm visual fidelity before the config enters the monthly care cycle. Requires a HUMAN GATE before promotion.

**Mode B — Milestone Review:** Triggered at any design system milestone (component release, major token update, quarterly health check). Goal: surface drift, identify what's working, flag what's degraded. Produces a review report. No promotion required.

---

## Before You Start

Load these references before running the review:

- **`ai-services/design-intelligence/designer-review-protocol.md`** — The step-by-step protocol for Mode A reviews. Load if running v0 → v1 promotion.
- **The locked moodboard direction** (from `ai-services/design-intelligence/moodboard-template.md` or the Gate 0 capture document) — Load the relevant direction sections. Required for Mode A. Helpful for Mode B.
- **The active-brand.json config** — Load and check `meta.generated_by` to determine if this is a Mode D provisional config.
- **Generated output** — Screenshots, live components, or page previews built against the config. At least one piece of output is required to run the review.
- **`ai-services/design-intelligence/style-descriptor-vocabulary.md` (summary keyword list)** — Load when Phase 2 Q5 requires evaluating personality descriptors, or when reviewing `descriptors.mood`, `descriptors.anti_mood`, or `descriptors.keywords` fields for canonical vocabulary compliance. The ~60-token summary keyword list is sufficient for most reviews; load the full vocabulary only when the mood descriptor set needs to be rewritten or significantly expanded.

If the config is a Mode D v0 (`meta.generated_by: "mode-d"`) and no generated output exists yet, the review cannot run. Return to the ui-studio skill to generate output first.

---

## Mode A: v0 → v1 Promotion Review

### Pre-check

Before starting the review, confirm both conditions are met:

1. Config exists with `meta.generated_by: "mode-d"` and `meta.provisional_fields` populated.
2. At least one piece of generated output exists (screenshot, live component, or page preview).

If condition 1 fails: this is not a Mode D config. Run Mode B instead.
If condition 2 fails: output must be generated before the review can proceed. Stop and request output.

---

### Phase 1: Prepare the Review Package

Extract from the moodboard template and the config:

**1a. Direction summary**
Pull the locked direction's data from moodboard Sections 1–7 in a concise table. Include the direction lock rationale from Section 8B and the token translation notes from Section 9.

**1b. Provisional fields table**
Create a table for every field listed in `meta.provisional_fields[]`:

| Token path | Provisional value | Assumption | Confirmation needed |
|---|---|---|---|
| `tokens.typography.families.display.family` | "PROVISIONAL: High-character serif" | Personality specified; face not named | Specific typeface or 2–3 shortlist candidates |
| `tokens.color.accent.primary` | "PROVISIONAL: approximately #2D5A3D" | Inferred from moodboard references | Designer confirms or provides alternative hex |

**1c. Generated output inventory**
For each piece of generated output, note:
- What component or page it represents
- Which tokens it exercises (color, typography, spacing, radius, elevation)
- What aspect of the moodboard it should reflect (e.g., "This card uses color-bg-primary and type-display — should feel editorial per Direction C")

**HUMAN GATE: Review Package Sign-Off**

Present the review package to the human reviewer (or the designer if they're in the session). Confirm:
- [ ] The direction summary accurately reflects the locked direction
- [ ] The provisional fields table is complete
- [ ] The generated output inventory covers the key token categories

Do not proceed to Phase 2 until the review package is confirmed. If the reviewer finds an error in the package, fix it first.

---

### Phase 2: Visual Fidelity Check

Five questions. For each: **Pass / Partial / Fail** with a one-sentence explanation.

**Q1. Typography: does the type treatment match the direction?**

Check: display face character (or PROVISIONAL status), scale contrast between h1 and body, line-height and reading comfort, label/utility treatment. Reference: moodboard Section 3.

**Q2. Color: does the palette match the direction?**

Check: primary brand color impression (warmth, saturation), background temperature (warm neutral vs. cool neutral vs. true neutral), accent color contrast and character. Reference: moodboard Section 2. Note: if color tokens are PROVISIONAL, this check is visual estimation only — not a production validation.

**Q3. Spacing and density: does the spatial rhythm match the direction?**

Check: section padding (generous vs. tight), component spacing (breathing room vs. compact), grid behavior. Reference: moodboard Section 4.

**Q4. Shape language: do the radius and surface treatments match?**

Check: corner treatment (sharp vs. rounded vs. pill), elevation or shadow approach (flat vs. subtle vs. material), border usage. Reference: moodboard Section 5.

**Q5. Personality: does the overall output feel right?**

This is the taste check. Read the mood descriptors from moodboard Section 1.3 and the brand personality from `brand.personality` in the config. Ask: does the generated output feel like what those words describe? This is a gut check, not a specification check. If it doesn't feel right, something is off even if every individual token passes.

**Q6. Optional enrichment fields: are applicable optional fields present?** *(ADR-004, March 24, 2026)*

Check the matched style entry in `style-reference-library.md` for any optional enrichment fields that should be reflected in the config:

- **`default_scheme: dark`** — If the entry carries this (Entries 2, 3, 10, 15), verify the config's color scheme baseline is dark-native. If not: flag as enrichment gap.
- **`border_radius_strategy`** — If the entry carries this (variable radius intent), verify the config documents the variable approach, even if the single enum is filled with the dominant radius. If not: flag as a note.
- **`motion_override` block** — If the entry carries this (Entry 8 and future sensitive-context entries), verify the config either respects the override or explicitly notes that the client's use case doesn't apply. If the client's industry includes a cognitive load scope condition (mental health, crisis, trauma, recovery) and no override is present: flag as a concern.

Pass = applicable optional fields are reflected; Partial = some present, some missing; Fail = applicable fields clearly missing and contextually significant; N/A = no optional fields apply to this entry.

---

### Phase 3: Provisional Field Resolution

For each item in `meta.provisional_fields[]`:

> **When the resolution source is a canonical artifact (a logo spec, a Figma extraction, a hand-drawn identity authored in a separate session), not a live designer, treat `meta.provisional_fields[]` as a hint, not the reconciliation scope.** It was written before the source existed and can under-count. Diff every overlapping value between the config and the source (every spot color or token that appears in both); reconcile all that differ, source wins, then re-derive dependents and recompute every value the config asserts (contrast ratios, scores) against the reconciled hexes rather than trusting the stored prose (`CLAUDE-SESSION-RULES.md` § Task-level verification, "Recompute computable values"). When the source itself marks a value provisional ("lock with the client"), make config and source agree while both stay jointly-provisional until the client locks; do not record a false "locked" state to clear a gate (§ Never write a false confirmation into machine state).

**Semantic color fields — use Step 2D.2a, not raw prompting:**
If any provisional field is a semantic color (`tokens.color.semantic.success`, `.warning`, `.error`, `.info`), do not ask the designer for a hex value directly. Run Step 2D.2a first:

```bash
node heyhi-design-intelligence-tests/scripts/generate-semantic-colors.cjs path/to/active-brand.json
```

This generates 3 palette-harmonized, WCAG-AA-validated options per role (output: `semantic-color-options.md` alongside the config). Present the options to the designer for selection. Once the designer picks, write the confirmed value and remove the field from `meta.provisional_fields[]`. This applies even mid-review — if backgrounds.primary and accent.primary are already confirmed, Step 2D.2a can run immediately.

**Option A — Designer provides the answer:**
Record the confirmed value. Mark the field as resolved in the review report.

**Option B — Confident visual inference:**
If the generated output + moodboard references provide enough signal to make a confident determination, propose a specific value. Mark as "proposed pending designer confirmation."

**Option C — Still unclear:**
Mark as "unresolved." Note what additional input is needed. Do not block promotion if fewer than 3 fields remain unresolved — proceed with those fields still provisional and note in the report.

Blocking threshold: if more than 5 fields remain unresolved, or if typography.display.family is unresolved, the config cannot be promoted to v1. Return to the designer with the specific questions needed.

---

### Phase 4: v0 → v1 Promotion Decision

**Promotion criteria (all must be met):**

- [ ] Visual fidelity check: no more than 1 "Fail" across the 5 questions
- [ ] `tokens.typography.families.display.family` is not null and not PROVISIONAL
- [ ] `tokens.color.backgrounds.primary` and `tokens.color.text.primary` are confirmed hex values
- [ ] `tokens.spacing.base` is confirmed
- [ ] Fewer than 3 provisional fields remain in `meta.provisional_fields[]`
- [ ] The human reviewer confirms: "promote to v1"

If criteria are not met: document what's blocking. Do not promote. Return to the designer with the specific open items.

**HUMAN GATE: Promotion Confirmation**

```
Review result: [Pass / Conditional pass / Not ready]
Visual fidelity: Q1 [Pass/Partial/Fail] | Q2 [...] | Q3 [...] | Q4 [...] | Q5 [...]
Provisional fields resolved: N of M
Remaining provisional: [list if any]
Recommendation: [Promote to v1 / Return to designer with N open items]

Does this meet the bar for v1? Confirm to promote or return the open items list to the designer.
```

Wait for the human reviewer's explicit confirmation before executing the promotion.

---

### Phase 5: Execute Promotion

On confirmation:

1. Update the config file:
   - Replace all resolved PROVISIONAL values with confirmed values
   - Remove resolved entries from `meta.provisional_fields[]`
   - Update `meta.generated_by` from `"mode-d"` to `"mode-d-v1"`
   - Update `meta.version` from `"0.x.y"` to `"1.0.0"`
   - Update `meta.last_refreshed` to current timestamp

2. Write the promotion record:
   - File: `[output-path]/mode-d-v1-promotion-record.md`
   - Contents: date, who reviewed, which fields were resolved, which remain provisional (if any), visual fidelity scores, config diff summary

3. Notify design-system-care-monthly that Month 1 baseline is now established:
   - If `design-system-care-monthly` is active for this client, add a note in the client folder: "Mode D v1 promoted [date]. Use this as the baseline for drift detection starting Month 1."

---

## Mode B: Milestone Review

Use when running a periodic health check, component release gate, or post-change validation. No direction lock or provisional fields required.

### What to Review

**Scope:** Define the review scope before starting. Options:
- Full system: all token categories + all major components
- Token-focused: color, typography, spacing — no component review
- Component-focused: specific components or new additions
- Change-focused: what changed since the last review

**What to check:**

1. **Token integrity:** Are any token values that should be stable unexpectedly changed? (Run against the last known-good config if available.)

2. **Consistency:** Do components use the design tokens consistently, or have hardcoded values crept in?

3. **Voice compliance:** Does any UI copy contain banned words or prohibited patterns from `voice.prohibited_words` and `voice.prohibited_patterns` in the config?

4. **Coverage:** Are there components or states that have no tokens backing them (design-code drift)?

5. **Accessibility:** For key text/background combinations, do contrast ratios still pass WCAG AA? (Use `tokens.color.contrast_notes` if populated, otherwise note for manual check.)

### Output

A review report structured as:

```markdown
## Design System Review — [Client/System Name]
Date: [date]
Mode: Milestone Review
Scope: [Full system / Token-focused / etc.]

### Status by Dimension
| Dimension | Status | Notes |
|-----------|--------|-------|
| Token integrity | Pass / Flag / Fail | [detail] |
| Component consistency | Pass / Flag / Fail | |
| Voice compliance | Pass / Flag / Fail | |
| Coverage | Pass / Flag / Fail | |
| Accessibility | Pass / Flag / Fail | |

### Flagged Items
[List of specific issues with token path, description, and recommended action]

### Passing Items
[Brief confirmation of what's working well — this prevents regression anxiety]

### Recommended Actions
[Priority-ordered list of what to fix, if anything]

### Next Review
[When should the next review run? Based on change frequency and flag count.]
```

---

## Reference Files

Load when relevant, not by default:

- `ai-services/design-intelligence/designer-review-protocol.md` — detailed v0 → v1 review procedure, Phase-by-Phase
- `ai-services/design-intelligence/moodboard-template.md` — moodboard template to cross-reference direction
- `ai-services/design-intelligence/moodboard-to-brand-json.md` — translation spec, confidence rules
- `heyhi-skills/ui-studio/SKILL.md` — how the config was used to generate output
- `heyhi-skills/design-system-care-monthly/SKILL.md` — what happens after v1 promotion

---

## Smoke Test Checklist

Before delivering a review output, check:

- [ ] Both Mode A and Mode B paths tested separately
- [ ] HUMAN GATE blocks are present in Mode A (Phase 1 sign-off, Phase 4 promotion confirmation)
- [ ] Promotion criteria list is non-circular (does not include "the reviewer approves" as the only criterion)
- [ ] Visual fidelity Q5 (personality) is not reducible to a checklist — it requires a judgment call, not a formula
- [ ] Visual fidelity Q6 (optional enrichment fields) checked against the matched style entry — note any applicable fields missing from the config
- [ ] Mode B review report includes passing items (not just flags)
- [ ] No pricing mentioned in output
- [ ] No standalone "AI" in output copy
- [ ] No em dashes beyond 2 in any client-facing content generated by this skill (the 2-em-dash rule applies to output copy, not to this procedural SKILL.md document)

---

## Exit Gate Required Headers (bottom-of-skill bracket)

This skill closes through the Exit Gate Flavor A (`CLAUDE-SESSION-RULES.md § Exit Gate`). Before declaring done, confirm every required header below contains real content, not a claim:

- `## Fixes Applied`
- `## Smoke Test`
- `## Next Session Prompt`

If any header is empty or contains advisory prose ("I checked for bugs") instead of a concrete artifact, the gate has not been satisfied. Apply fixes until clean — then emit.

---

*HeyHi internal + client delivery skill. Bay Design LLC. March 2026.*
*Mode A wraps `ai-services/design-intelligence/designer-review-protocol.md`.*
*Mode B is a standalone milestone health check.*

*HeyHi Confidential*
