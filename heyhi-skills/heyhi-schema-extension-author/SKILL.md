---
name: heyhi-schema-extension-author
description: >-
  Runs the full schema extension procedure when a new token namespace is needed in active-brand.json.
  Use when a client context or pipeline validation surfaces a field gap that the current schema cannot
  express. Covers all five extension classes: accessibility (focus rings, contrast targets),
  functional safety (ISA-101 alarm states), internationalization (text expansion, RTL, logical
  properties), motion architecture (dark/light scheme branching), and sensitive-context overrides.
  Produces: a filed ADR, an updated schema.json, updated design-system-onboard SKILL.md Mode D
  documentation, updated moodboard-to-brand-json.md Part 4.6, and a validated reference entry
  demonstrating the extension. Not for: style entry authoring (use heyhi-style-entry-author),
  token config review (use heyhi-style-to-token-reviewer), or design system audits
  (use heyhi-design-intelligence-audit).
  Triggers: "extend the schema for [field]," "add a new token namespace," "the schema doesn't
  have a field for [requirement]," "write a schema extension," "we need [type] tokens in
  active-brand.json," "file the ADR and add the field."
---

# Schema Extension Author

Procedure for adding new token namespaces to `active-brand.json` when a client context or
pipeline validation surfaces a field gap. ADR-007 is the canonical reference implementation —
five extensions authored in one session (focus ring, touch target, functional color, contrast
target, i18n). This skill formalizes that procedure so future schema work follows the same
pattern.

---

> **Exit Gate (Flavor B).** This skill closes through the canonical Exit Gate — see `CLAUDE-SESSION-RULES.md § Exit Gate`. Required headers, in order: `## Findings Integration`, `## Session Integrity`, `## Fixes Applied`, `## Smoke Test`, `## Next Session Prompt`. Empty headers are visible failures.


## Reference Architecture

**The files this skill modifies (in order):**

1. `ai-services/_core/architecture-decisions/` — new ADR filed here
2. `heyhi-skills/ui-studio/brand-config/schema.json` — schema update target
3. `heyhi-skills/design-system-onboard/SKILL.md` — Mode D documentation update target
4. `ai-services/design-intelligence/moodboard-to-brand-json.md` — Part 4.6 update target
5. A reference test fixture in `ai-services/design-intelligence/test-fixtures/` — validation target

**The ADR that anchors this procedure:**
`ai-services/_core/architecture-decisions/007-schema-extensions-accessibility-functional-color-i18n.md`

Read it before starting. It is the ground truth for how an extension is reasoned and documented.

---

## Step 0: Identify the Field Gap

Before writing anything, establish that the gap is real, that it belongs in the schema, and
that it is not already covered by an existing field.

**Questions to answer:**

1. **What client context or validation result surfaces the gap?**
   Name the specific entry, engagement, or pipeline stage where the gap appeared.
   Example: "Entry 16 (Civic Modern) Mode D validation — no field for 2px focus ring minimum."

2. **Is there an existing schema field that can express this requirement?**
   Read `heyhi-skills/ui-studio/brand-config/schema.json` carefully.
   Check: `tokens.focus.*`, `tokens.spacing.*`, `meta.accessibility.*`, `meta.internationalization.*`,
   `tokens.color.semantic.*`, `tokens.color.schemes.*`, `brand.style_notes`.
   If a field already exists: document it in `design-system-onboard/SKILL.md` and stop here.

3. **What does the requirement actually need the schema to carry?**
   Distinguish between: (a) a token value that downstream tools must use, (b) a generation
   constraint annotation that code generators must apply, and (c) a documentation note that
   prose captures adequately. Only (a) and (b) warrant schema fields.
   Example: `logical_properties_required: true` is a generation constraint annotation, not a
   token value — but it belongs in the schema because it signals code generators.

4. **Which of the five extension classes does it belong to?**

   | Class | Namespace pattern | Triggering context |
   |-------|------------------|--------------------|
   | Accessibility | `tokens.focus.*`, `tokens.spacing.touch-target.*`, `meta.accessibility.*` | WCAG 2.2 SC 2.4.13, SC 2.5.8; civic, healthcare, education clients |
   | Functional safety | `tokens.color.semantic.alarm_*`, `tokens.color.schemes.dark.semantic.*` | ISA-101, SCADA, industrial IoT, manufacturing, utilities |
   | Internationalization | `meta.internationalization.*` | Government, civic, multilingual-primary clients |
   | Motion architecture | `tokens.color.schemes.*`, `meta.default_scheme` | Dark-native style entries (Entries 2, 3, 10, 15); ADR-006 scope |
   | Sensitive-context | `tokens.motion.override.*` (in style entry, not active-brand.json) | Mental health, crisis, trauma recovery, neurodivergent-serving apps |

5. **Is this a one-off or a repeatable class?**
   If it surfaces in a single client context and no other entry will ever need it: consider
   whether `brand.style_notes` and `meta.implementation_notes` can carry it adequately before
   creating a schema field.

**Decision gate:** If you cannot name the specific client context, confirm no existing field
covers it, and classify it into an extension class — stop and ask the user before continuing.

---

## Step 1: Draft the ADR

The ADR is the authoritative record of the decision. Write it before touching any code or schema.

**ADR file naming:** `[NNN]-[slug]-[brief-description].md`
Example: `008-focus-ring-tokens-wcag-22.md`
File location: `ai-services/_core/architecture-decisions/`

**Read the last filed ADR** to confirm the correct next ADR number. Do not skip numbers.

**ADR template:**

```markdown
# ADR-[NNN]: [Title]

**Date:** [YYYY-MM-DD]
**Status:** active
**Domain:** schema, [primary domain tags]
**Decided by:** [decider name]
**Replaces:** None
**Superseded by:** None

*HeyHi Confidential*

---

## Problem

[Why does the current schema fall short for this requirement? Which client context or
pipeline stage surfaces the gap? What happens today when an engineer or agent hits this
ceiling — what workaround is being used and why it's inadequate?]

---

## Decision: [N] Schema Extension(s)

### Extension [N] — [Field name] (`[namespace].*`)

**Namespace:** `[tokens.* or meta.*]`

**Proposed schema:**
[JSON block showing the exact field structure]

**Rationale:** [Why this namespace, why these fields, why now. Reference the external
standard or client requirement that drives the specification.]

**Required for:** [Which entries or client sectors need this field.]

**Mode D behavior:** [Specific instructions for the design-system-onboard Mode D extraction
procedure. What signals in the style entry or moodboard trigger population? What PROVISIONAL
values are appropriate? What gets added to meta.provisional_fields[]?]

---

## Consequences

### For Mode D agents (design-system-onboard)
[How Mode D behavior changes. Reference the SKILL.md section that will be updated.]

### For design-system-review (Mode A promotion)
[What additional checks are required at v0→v1 promotion for the new extension field(s).]

### For design-system-care-monthly
[Whether drift detection applies to the new field(s).]

---

## Implementation Checklist

- [ ] ADR filed
- [ ] schema.json updated with new field(s)
- [ ] design-system-onboard SKILL.md Mode D section updated
- [ ] moodboard-to-brand-json.md Part 4.6 updated
- [ ] Reference entry validated with new field(s) populated
- [ ] skill-registry.yaml ADR reference entry added

---

*HeyHi Confidential · `ai-services/_core/architecture-decisions/` · [Date]*
```

**Alternatives considered:** Every ADR must document at least two alternatives:
- Option A: The proposed extension (default recommendation)
- Option B: Express the requirement in `brand.style_notes` prose only (the always-available
  alternative — document why it is insufficient before rejecting it)
- Option C (if applicable): A third approach specific to the domain

---

## Step 2: Write the Schema Extension

Add the new field(s) to `heyhi-skills/ui-studio/brand-config/schema.json`.

**Before editing:** Read the full schema to understand where the new namespace fits in the
object hierarchy. Common insertion points:

- `tokens.focus.*` — already present (ADR-007). Extensions go inside the `focus` object.
- `tokens.spacing.*` — existing namespace. New sub-objects (like `touch-target`) go here.
- `tokens.color.semantic.*` — additional properties pattern already uses `additionalProperties`.
  New named fields use the same `"type": "string"` pattern; add a description that references
  the standard driving the requirement.
- `meta.accessibility.*` — present (ADR-007). Additional properties go inside this object.
- `meta.internationalization.*` — present (ADR-007). Additional properties go inside this object.
- New top-level token namespace — follow the pattern of existing objects: `"type": "object"`,
  `"description"` citing the ADR, nested `"properties"` for sub-fields.

**Schema description quality requirements:**

Every new field description must include:
- What the field carries (token value, constraint annotation, metadata)
- Which standard or requirement drives it (WCAG 2.2 SC number, ISA-101 section, etc.)
- Which entries or client sectors it applies to
- Whether it is optional, conditional, or required
- A reference to the governing ADR: `(ADR-[NNN] Extension [N])`

Example of a well-formed description:
```json
"width": {
  "type": "string",
  "description": "Focus outline width — minimum 2px for WCAG 2.2 SC 2.4.13 compliance
    (e.g., '2px'). Required for all civic, public-sector, healthcare, and education
    clients. Mandatory for Civic Modern (Entry 16). (ADR-007 Extension 1)"
}
```

**DTCG alignment note:** The W3C Design Token Community Group format (`$value`, `$type`,
`$description`) is the migration target for this schema. New fields should use semantic
names (not `$`-prefixed) that translate cleanly to DTCG when the migration runs. If a
new field carries a token value (hex, px, boolean), note the future DTCG `$type` it would
map to in the description. DTCG `$type` vocabulary: `color`, `dimension`, `fontFamily`,
`fontWeight`, `duration`, `cubicBezier`, `boolean`, `string`.

**Cross-check for `_note` keys:** Never add underscore-prefixed keys (`_note`, `_rationale`,
`_context`) inside the `tokens.*` namespace. These are treated as CSS custom properties by
downstream consumers. Implementation rationale belongs in `meta.implementation_notes` or
`brand.style_notes`. See corrections-registry.yaml entry `design-note-fields-in-token-namespace`.

---

## Step 3: Update design-system-onboard SKILL.md

The Mode D documentation in `design-system-onboard/SKILL.md` must know about the new field
so agents running Mode D populate it correctly for applicable clients.

**Locate the right section:** The existing schema gap documentation lives under:
`## Schema Gap Notes for Accessibility-First and Sector-Specific Clients (ADR-007)`

If the new extension belongs to a different domain (motion architecture, sensitive-context),
create a parallel section following the same structure.

**What to write per extension:**

```markdown
**Extension [N] — [field name] (`[namespace].*`)**
Required for: [client context, entry numbers, standards reference]
[If schema field now exists:] Populate `[namespace.field]` with [value guidance]. For
[client type], set `[field]` to `[PROVISIONAL value or range]`. Add to
`meta.provisional_fields[]` if moodboard-derived.
[If schema field does not yet exist:] Add to `brand.style_notes`:
"[Requirement description + workaround note]. Token namespace pending ADR-[NNN] schema
extension."
```

**Imperative form rule (from corrections-registry.yaml, `arch-advisory-language-in-skill-post-build`):**
All new Mode D steps must be written as imperatives, not as advisory suggestions.
"Populate this field" not "Consider populating this field."
"Add to `meta.provisional_fields[]`" not "You may want to add..."

---

## Step 4: Update moodboard-to-brand-json.md Part 4.6

`ai-services/design-intelligence/moodboard-to-brand-json.md` Part 4.6 documents the
extraction procedure for sector-specific and dark-native extension fields.

**Locate Part 4.6.** It begins at the heading:
`## Part 4.6: Sector-Specific and Dark-Native Extension Field Extraction (ADR-006 + ADR-007)`

**Add an entry for the new extension** following the table format used for existing extensions:

```markdown
### [Extension class name]

**Condition:** [Which matched style entry signals or industry_fit.natural values trigger this]

**[Extension name] (`[namespace].*`)**

| Field | PROVISIONAL value | Notes |
|-------|------------------|-------|
| `[field.path]` | `"PROVISIONAL: [estimated value + rationale]"` | [Standard compliance note] |
```

**Update the footer citations** to include the new ADR:
`*ADR-[NNN] governs [extension class]: `ai-services/_core/architecture-decisions/[filename].md`*`

---

## Step 5: Validate with a Reference Entry

Before marking any extension complete, validate it by running Mode D on at least one style
entry that exercises the gap. This is the proof-of-implementation check.

**Selecting the reference entry:**

- For accessibility extensions: use Entry 16 (Civic Modern) — ADR-007 reference implementation.
  Config: `ai-services/design-intelligence/test-fixtures/civic-modern-v0.1.0-active-brand.json`
- For ISA-101 / functional safety: use Entry 10 (Neo-Industrial).
  Config: `ai-services/design-intelligence/test-fixtures/neo-industrial-active-brand.json`
- For a new extension class: run Mode D on the entry whose `industry_fit.natural` matches the
  extension's triggering context. Generate a v0 config with the new field populated.

**Validation procedure:**

1. Open the reference config or generate a new one.
2. Confirm the new field is populated (with PROVISIONAL prefix if moodboard-derived).
3. Confirm the new field is listed in `meta.provisional_fields[]` if its value is inferred.
4. Confirm the `brand.style_notes` note is present if the standard requires a secondary
   indicator (ISA-101) or implementation constraint (i18n logical properties).
5. Run `heyhi-style-to-token-reviewer` warning signs against the config to confirm the
   extension field does not introduce incoherence. If the extension carries a color token,
   WS6 (Semantic Orphan) applies.
6. Check `meta.implementation_notes` — if the extension requires a rationale for the
   specific values chosen (e.g., why 48px rather than 44px touch target), write it there.

**ADR checklist item:** Mark the implementation checklist item in the ADR:
`- [x] Reference entry validated with new field(s) populated — [Date]`

---

## Step 6: Human Gate

Before declaring the extension complete, present the following to the human reviewer:

```
Schema Extension Summary — ADR-[NNN]: [title]

Extension class: [accessibility / functional safety / i18n / motion architecture / sensitive-context]
New namespace(s): [namespace paths]
Files modified: schema.json, design-system-onboard SKILL.md, moodboard-to-brand-json.md Part 4.6
Reference entry validated: [entry name] — [PASS / PASS with notes]

ADR filed at: ai-services/_core/architecture-decisions/[filename].md
Schema diff: [brief description of what was added]

ADR implementation checklist: [N]/[N] items complete

Confirm to mark extension complete and update skill-registry.yaml ADR entry?
```

Wait for the human reviewer's explicit confirmation before marking the ADR implementation checklist complete
and before updating the skill-registry.yaml ADR reference entry.

---

## Extension Class Reference

Quick reference for the five extension classes. Load the governing ADR for full spec before
working within each class.

**Class 1 — Accessibility**
Governing ADR: ADR-007 (Extensions 1, 2, 4)
Namespaces: `tokens.focus.outline.*`, `tokens.spacing.touch-target.*`, `meta.accessibility.*`
Trigger signals: `industry_fit.natural` includes civic, government, healthcare, education.
`keyword_set` includes "accessibility-first," "WCAG 2.2 AA/AAA," "public-sector."
Reference entry: Entry 16 (Civic Modern)
Key standards: WCAG 2.2 SC 2.4.13 (Focus Appearance), SC 2.5.8 (Target Size)

**Class 2 — Functional Safety**
Governing ADR: ADR-007 (Extension 3)
Namespaces: `tokens.color.semantic.alarm_high_priority`,
`tokens.color.schemes.dark.semantic.alarm_high_priority`
Trigger signals: `industry_fit.natural` includes industrial IoT, SCADA, manufacturing,
utilities, construction tech.
Reference entry: Entry 10 (Neo-Industrial)
Key standard: ISA-101 High Performance HMI color encoding
Critical implementation note: Color is never the sole status indicator. Every chromatic
alarm state requires a secondary shape/symbol encoding. Always write this note to
`brand.style_notes` for any ISA-101 client. This cannot be encoded as a token.

**Class 3 — Internationalization**
Governing ADR: ADR-007 (Extension 5)
Namespace: `meta.internationalization.*`
Trigger signals: `industry_fit.natural` includes government, civic. Moodboard Section 1
references bilingual content. `visual_characteristics.spatial_approach` mentions text
expansion budget.
Reference entry: Entry 16 (Civic Modern)
Key constraint: `logical_properties_required: true` is a code generator annotation, not a
token value — use `min-height/min-width` over fixed dimensions throughout.

**Class 4 — Motion Architecture**
Governing ADR: ADR-006 (scheme namespacing)
Namespace: `tokens.color.schemes.*`, `meta.default_scheme`
Trigger signals: Style entry has `default_scheme: dark`. Applies to Entries 2, 3, 10, 15.
Reference entries: Entry 10 (Neo-Industrial), Entry 3 (Night Shift)
Note: ADR-006 is already implemented in schema.json. This class is not a pending extension —
it is a reference case for how a motion architecture extension would follow the same pattern
if new dark/light branching fields were needed.

**Class 5 — Sensitive-Context Overrides**
Governing document: `heyhi-skills/heyhi-style-entry-author/SENSITIVE_CONTEXT_OVERRIDE.md`
Namespace: `tokens.motion.override.*` (in style entry schema, not active-brand.json directly)
Trigger signals: `industry_fit.natural` includes mental health, crisis support, trauma
recovery, neurodivergent-serving.
Reference entry: Entry 8 (reference implementation per SENSITIVE_CONTEXT_OVERRIDE.md)
Note: Sensitive-context overrides live in the style entry, not in active-brand.json directly.
A schema extension for this class would add an override field to active-brand.json so the
override block from the style entry propagates into the config. Build the
`heyhi-sensitive-context-reviewer` skill before attempting this class — it provides the
validation layer the extension would depend on.

---

## Smoke Test Checklist

Before delivering any schema extension output, verify:

- [ ] ADR filed with problem statement, extension specification, consequences, and implementation checklist
- [ ] At least two alternatives considered in the ADR (including "brand.style_notes prose only" as Option B)
- [ ] New field added to schema.json with description citing the external standard and ADR number
- [ ] No `_note` keys inside `tokens.*` namespace (put rationale in `meta.implementation_notes`)
- [ ] Mode D documentation updated in design-system-onboard SKILL.md — imperative form, not advisory
- [ ] moodboard-to-brand-json.md Part 4.6 updated with extraction table and condition
- [ ] Reference entry validated: new field populated, added to `meta.provisional_fields[]` if inferred
- [ ] ISA-101 secondary indicator note present in `brand.style_notes` for any functional safety extension
- [ ] HUMAN GATE block presented before marking ADR checklist complete
- [ ] No standalone "AI" in any output
- [ ] No banned words (leverage, seamless, holistic, etc.)
- [ ] Em dashes: maximum 2 in any client-facing output produced by this skill
- [ ] Document classification: ADR footer says "HeyHi Confidential"
- [ ] skill-registry.yaml ADR reference entry updated after the human reviewer confirms

---

## Reference Files

Load when relevant:

- `ai-services/_core/architecture-decisions/007-schema-extensions-accessibility-functional-color-i18n.md` — canonical reference implementation for extension authoring procedure
- `heyhi-skills/ui-studio/brand-config/schema.json` — modification target; read before editing
- `heyhi-skills/design-system-onboard/SKILL.md` — Mode D documentation target; read the ADR-007 section before editing
- `ai-services/design-intelligence/moodboard-to-brand-json.md` — Part 4.6 update target; read before editing
- `ai-services/design-intelligence/test-fixtures/civic-modern-v0.1.0-active-brand.json` — Civic Modern reference config (Extensions 1, 2, 4, 5)
- `ai-services/design-intelligence/test-fixtures/neo-industrial-active-brand.json` — Neo-Industrial reference config (Extension 3)
- `heyhi-skills/heyhi-style-entry-author/SENSITIVE_CONTEXT_OVERRIDE.md` — motion override pattern (Class 5 reference)
- `corrections-registry.yaml` — check `design-note-fields-in-token-namespace` before any schema edit

---

## Exit Gate Required Headers (bottom-of-skill bracket)

This skill closes through the Exit Gate Flavor B (`CLAUDE-SESSION-RULES.md § Exit Gate`). Before declaring done, confirm every required header below contains real content, not a claim:

- `## Findings Integration`
- `## Session Integrity`
- `## Fixes Applied`
- `## Smoke Test`
- `## Next Session Prompt`

If any header is empty or contains advisory prose ("I checked for bugs") instead of a concrete artifact, the gate has not been satisfied. Apply fixes until clean — then emit.

---

*HeyHi Confidential — Skill internal methodology. Not for client distribution.*

*Layer 0 infrastructure skill. Governs schema evolution procedure for active-brand.json.*

*Bay Design LLC d/b/a HeyHi · Built March 2026 · Deployed at `heyhi-skills/heyhi-schema-extension-author/`*
