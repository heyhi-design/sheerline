---
name: heyhi-token-description-author
description: >-
  Write or improve semantic $description fields for DTCG-format design tokens. Use when a client's token files are missing descriptions, have appearance-only descriptions (e.g., "blue" or "#3B82F6"), or need descriptions enhanced for agent retrieval. Triggers: "write token descriptions," "document the design tokens," "add descriptions to the token schema," "enhance token descriptions," "audit token descriptions," "make these tokens agent-readable," "tokens are missing descriptions," "improve the $description fields." Not for: token value changes, token naming conventions, or design system architecture decisions.
---

# Token Description Author

Write semantic `$description` fields for design tokens in W3C DTCG format. Converts bare token names and values into meaningful, retrievable documentation that tells both humans and agents what each token is for.

---

> **Exit Gate (Flavor A).** This skill closes through the canonical Exit Gate — see `CLAUDE-SESSION-RULES.md § Exit Gate`. Required headers, in order: `## Fixes Applied`, `## Smoke Test`, `## Next Session Prompt`. Empty headers are visible failures.


## What This Skill Produces

For each token, one of three outcomes:

**Authored:** Token was missing a description or had a weak one. A new description is written.

**Preserved:** Token already has a strong semantic description. No change.

**Flagged:** Token's naming, value, or position makes a description ambiguous. Flagged with a question for the human reviewer or the client before writing.

Output: updated token file(s) with a completeness report listing authored, preserved, and flagged counts.

---

## The Description Pattern

The canonical form from Stream B (March 2026):

```
"[Semantic role] — [Context detail or constraint]"
```

**Rules:**

1. **Function-first.** Start with what the token is FOR, not what it looks like. `"Primary CTA color — AA compliant on white"` not `"Dark blue (#3B82F6)"`.

2. **Short.** Target under 15 words. Hard limit: 25 words. If you can't say it in 25 words, the token's purpose is unclear — that's worth flagging.

3. **Semantic role over scale.** Avoid `"level 6 of the neutral scale."` Write `"Primary text on light — maximum contrast."` The number is in the key. The description earns its place by adding meaning the key can't convey.

4. **Compliance notes where they matter.** When a color is specifically designed for text or interactive states, include WCAG compliance: `"(AA compliant on white)"` or `"(AAA on white)"`. Omit when the token is decorative or not intended for text.

5. **Do-not-use clauses for misuse-prone tokens.** If a token is frequently misused (e.g., a decorative tint used as a background), add a constraint: `"Decorative use only — fails AA as text color."` These are the highest-value descriptions in the system.

6. **File-level `$description`.** Every token file should have a file-level `$description` that describes the group's purpose, brand character, and what NOT to use these tokens for directly.

**Examples from Stream B:**

| Token path | Value | Before | After |
|---|---|---|---|
| `color.neutral.800` | `#1F2937` | (missing) | `"Near-black — primary text on light"` |
| `color.brand.accent.600` | `#4F46E5` | `"Brand A accent"` | `"Brand A accent — primary CTA color (AA compliant on white)"` |
| `color.status.red.100` | `#FEE2E2` | `"Light red"` | `"Error — light background"` |
| `color.neutral.300` | `#D1D5DB` | (missing) | `"Gray — disabled borders, decorative lines"` |
| `color.shadow.black-alpha.5` | `#0000000D` | (missing) | `"Shadow color — 5% opacity black"` |

**Anti-patterns to avoid:**

- `"#3B82F6"` — this is the value, not a description.
- `"Blue color token"` — states what the token type already says.
- `"Used in buttons"` — too component-specific. Tokens describe their own identity, not their implementation.
- `"Do not use"` — if a token exists, it has a use. If it doesn't, it should be removed.
- `"Brand primary blue — a rich, vibrant, high-energy blue that captures the essence of..."` — too long. Cut it.

---

## Before You Start

Load these references before authoring descriptions:

1. **Token file(s)** — read the full file to understand the naming convention, scale structure, and token type distribution before writing any descriptions.
2. **`ai-services/design-intelligence/README.md`** — for Layer 0 context (brand character influences description voice).
3. **`heyhi-design-intelligence-tests/tokens/primitives/color/brand-a.json`** and **`global.json`** — canonical Stream B examples. Read these if you haven't seen the pattern before.

If the client has a brand config (`active-brand.json`), load it. The `brand.personality` and `brand.description` fields inform whether the token descriptions should feel technical-neutral or have voice. Most primitive tokens are technical-neutral. Semantic tokens can carry a slight voice character.

---

## Step 1: Audit

Read the token file. For each token, classify it:

**A — Missing description:** `$description` field is absent.

**B — Appearance-only description:** Description states only what the token looks like (`"Blue"`, `"#2D5A3D"`, `"Light gray"`).

**C — Role-stated description:** Description names the role but not the context (`"Primary color"`, `"Error state"`).

**D — Full semantic description:** Describes role, context, and any constraint. Meets the Stream B standard.

Write the audit summary:
```
File: [filename]
Total tokens: N
A (missing): N
B (appearance-only): N
C (role-stated): N
D (full semantic): N
Flagged for review: N
```

If more than 30% of tokens are Class D already, state that before proceeding — the file may be in better shape than the task implied.

---

## Step 2: Author

For each token in Class A, B, or C:

1. Read the token's key (name), `$type`, and `$value`.
2. Read its position in the token hierarchy (is it in a primitives file, semantic file, or component-specific file?).
3. Read its scale position if applicable (neutral.50 is always light; neutral.900 is always dark).
4. Write a description following the pattern in "The Description Pattern" section.

**If authoring color tokens:**
- Include the semantic role first: `"Error —"`, `"Primary text —"`, `"Success —"`, `"Shadow color —"`.
- Include WCAG compliance for text-intended and interactive-state tokens.
- Decorative tokens: flag as `"Decorative use only — fails AA as text color"` when relevant.

**If authoring spacing tokens:**
- Reference the spatial intent: `"Section padding — generous tier"`, `"Component gap — tight tier"`.

**If authoring typography tokens:**
- Reference the reading context: `"Body text size — optimized for paragraph reading"`, `"Label size — uppercase utility contexts"`.

**If authoring motion tokens:**
- Reference the interaction type: `"Micro-interaction duration — hover states, focus rings"`, `"Page transition duration — route changes"`.

---

## Step 3: File-Level Description

If the file is missing a top-level `$description`, write one. This description should:

1. Name the token group (primitives, semantic, component, brand-specific).
2. Describe the group's character or purpose in 1–2 sentences.
3. Include a usage constraint where appropriate: `"Do not use directly in components — reference via semantic/color/light.json"` for primitive files.

**Example from Stream B (brand-a.json):**
> `"Brand A color primitives — indigo/violet accent palette. These override the brand.accent path when building Brand A outputs. Brand A character: precise, professional, enterprise-facing."`

---

## Step 4: Flag Ambiguous Tokens

Some tokens cannot be described without additional context. Flag these rather than inventing intent.

**Flag conditions:**

- The token name conflicts with its value (e.g., a `brand-blue` token with a green value).
- The token appears to be a duplicate of another token with identical value but different name.
- The token is in a scale position that doesn't match its expected value range (e.g., `neutral.50` with a mid-gray value).
- The token's intended use cannot be inferred from name, value, or position.

**Flag format:**
```
⚠️ Flagged: [token path]
   Issue: [what's ambiguous]
   Question: [what the human reviewer or the client needs to clarify]
   Proceeding with best guess: [description if a confident guess exists, else skip]
```

---

## Step 5: Completeness Report

After authoring, write a completeness report:

```markdown
## Token Description Completeness Report
File: [filename]
Date: [date]

### Summary
| Class | Before | After |
|-------|--------|-------|
| A — Missing | N | 0 |
| B — Appearance-only | N | 0 |
| C — Role-stated | N | N (improved) or 0 |
| D — Full semantic | N | N (final total) |
| Flagged | 0 | N |

### Authored Descriptions
[List of tokens with new descriptions]

### Preserved Descriptions
[List of tokens whose descriptions were kept]

### Flagged for Review
[List of flagged tokens with issue + question]

### Next Step
[If all tokens are Class D: "File is complete. Ready for integration."]
[If flags remain: "Review flagged tokens before integrating. N questions need answers."]
```

---

## Output Format

**Two target formats — use the right one for the file type being processed.**

### Target A: DTCG token files (`.json` with `$description` fields)

Return the updated token file with all authored descriptions in place. Do not change any field other than `$description` (and file-level `$description`). Do not reorder tokens. Do not change `$type`, `$value`, or any structural nesting.

If the task covers multiple files, process them one at a time. Return each file followed by its completeness report before moving to the next.

### Target B: ui-studio brand configs (`active-brand.json` / named configs such as `example.json`)

When the task involves a ui-studio brand config (files matching the `brand-config/schema.json` schema), descriptions are written to `meta.field_provenance[path].description` — not to inline token fields. The field_provenance map is the source of truth for G6 engineer context in the Cursor export.

**Path format:** Dot-notation matching the token's position in the config. Examples:
- `tokens.color.text.muted` → `meta.field_provenance["tokens.color.text.muted"].description`
- `tokens.typography.scale.h1` → `meta.field_provenance["tokens.typography.scale.h1"].description`
- `tokens.spacing.tiers.xl` → `meta.field_provenance["tokens.spacing.tiers.xl"].description`

**If a field_provenance entry already exists for the token:** Add or update only the `description` and `usage_notes` fields. Do not touch `source`, `confidence`, `extracted_at`, `last_verified_at`, `verified_by`, or `notes`.

**If no field_provenance entry exists for the token yet:** Create a new entry with at minimum: `source`, `confidence`, `extracted_at`, `description`. Use the same source/confidence as adjacent tokens in the same namespace when the provenance origin is clear. Use `"inferred_from_context"` and `"inferred"` when it isn't.

**What NOT to write:** Do not add `_note`, `_description`, or any documentation key inside the `tokens.*` namespace. The tokens namespace is a delivery surface — documentation goes in `meta.field_provenance` exclusively.

**Completeness report for Target B:**
After backfilling, write the same report format as Target A, but replace "token file" with "brand config" and note the field_provenance path for each authored entry instead of the token key.

After completing a brand config backfill, the engineer context in the generated `.mdc` file (produced by `cursor-export.py`) will include the descriptions as CSS comments. Verify by running `python3 scripts/cursor-export.py` from the ui-studio skill directory.

**Which target to use:** Read the first few lines of the file. If it has `$schema` and `$value` fields, use Target A (DTCG). If it has a `brand`, `tokens`, and `meta` structure (or a `meta.field_provenance` block), use Target B (brand config).

---

## Smoke Test Checklist

Before marking the output complete, verify:

- [ ] No description exceeds 25 words
- [ ] No description contains the value (hex, px, etc.) as a substitute for meaning
- [ ] No description starts with "A color token that..." or similar type-restating patterns
- [ ] All Class A and B tokens have been authored
- [ ] File-level `$description` is present and describes the group character
- [ ] Flagged tokens are documented, not silently skipped
- [ ] No structural changes were made (no token reordering, no field modifications beyond `$description`)
- [ ] No banned words from HeyHi voice rules appear in the authored descriptions or completeness report output (check: leverage, unlock, seamless, holistic, empower, etc.) — note: banned words may appear in the skill's own instructions as examples of what to avoid; that's correct usage

---

## Exit Gate Required Headers (bottom-of-skill bracket)

This skill closes through the Exit Gate Flavor A (`CLAUDE-SESSION-RULES.md § Exit Gate`). Before declaring done, confirm every required header below contains real content, not a claim:

- `## Fixes Applied`
- `## Smoke Test`
- `## Next Session Prompt`

If any header is empty or contains advisory prose ("I checked for bugs") instead of a concrete artifact, the gate has not been satisfied. Apply fixes until clean — then emit.

---

*HeyHi internal + client delivery skill. Bay Design LLC. March 2026.*
*Source pattern: Stream B — 101 `$description` fields, 6 token files. See `heyhi-design-intelligence-tests/tokens/`.*

*HeyHi Confidential*
