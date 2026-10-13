---
name: design-system-onboard
description: >-
  Legacy onboarding skill, retained for moodboard-driven Mode D runs (project-state.yaml marks it legacy; ui-studio-onboard is the current onboarding entry point for new clients). Converts moodboard aesthetic intent into a validated active-brand.json using the PROVISIONAL confidence ceiling (ADR-005/006/007), usually primed by heyhi-style-selection Mode B. Triggers: "moodboard to brand config," "Mode D onboarding," "onboard from a moodboard," "moodboard-driven onboarding," "turn the moodboard into a config." NOT for onboarding from live sources, Figma, token files, Git repos, Supernova, or conversational setup (use ui-studio-onboard). NOT for building UI (use ui-studio), general design critique, token naming discussions, or component API design.
---

# Design System Onboarding Skill

Extract a client's design system into a validated, schema-conformant `active-brand.json` configuration file. This config becomes the foundation for all ui-studio work and design-system-care-monthly retainers.

> **Exit Gate (Flavor A).** This skill closes through the canonical Exit Gate — see `CLAUDE-SESSION-RULES.md § Exit Gate`. Required headers, in order: `## Fixes Applied`, `## Smoke Test`, `## Next Session Prompt`. Empty headers are visible failures.


## Overview

The skill operates in four modes, each producing the same output but extracting differently:

- **Mode A (Live):** Supernova MCP + Git repositories + Figma. Real-time token and component inventory. Best when infrastructure is connected.
- **Mode B (File-based):** DTCG JSON, Style Dictionary configs, exported Figma data, or PDF/MD brand documents. Best when the client provides snapshots.
- **Mode C (Conversational):** The instance owner supplies values directly based on reviewed client materials. Best for rapid setup or when sources are incomplete.
- **Mode D (Moodboard-Driven):** Starts upstream of tokens — takes a designer's moodboard (structured via the moodboard template) and translates aesthetic intent into a token-ready config. Use for new brand identity work where no existing token infrastructure exists yet. Requires direction lock before token extraction. See `ai-services/design-intelligence/gate0-facilitation-guide.md` for the full intake process.

All modes feed the same extraction pipeline and produce identical outputs. The choice depends on what's available and how much setup overhead is acceptable.

## Prerequisites

Before starting, you need:

1. **At least one input source** (Supernova workspace, Git repo, Figma file, DTCG JSON, or brand documents)
2. **Access to the schema** (`heyhi-skills/ui-studio/brand-config/schema.json`)
3. **Access to a working directory** where output files will be written
4. **Clarity on the client** (organization name, design system name, date)

If none of these are available, ask before proceeding.

---

## Step 0: Determine Input Availability (Conversational)

Before extracting, map what's available. Ask the client or the instance owner:

**Questions to ask upfront:**

1. "Do you have a Supernova workspace?" (If yes, get workspace ID or URL.)
2. "Are your tokens in Git?" (If yes, get repo URL and branch.)
3. "Do you have a component library repository?" (If yes, framework and repo URL.)
4. "Are there Figma files we should analyze?" (If yes, get file URLs and page names.)
5. "Do you have existing token exports?" (DTCG JSON, Style Dictionary config, or token.json?)
6. "Do you have voice/brand guidelines?" (PDF, Markdown, Notion, or in-memory?)

**Entry conditions for each mode:**

| Mode | You have | You don't have | Proceed if |
|------|----------|---|---|
| **A (Live)** | Supernova MCP endpoint + Git token repo URL + (optionally) component repo URL | Any of the above missing | MCP endpoint and token repo are both confirmed |
| **B (File-based)** | DTCG JSON or Style Dictionary config file(s) + (optionally) exported Figma data or brand docs | Live infrastructure | At least one token file format and intent to work with snapshots |
| **C (Conversational)** | Client materials already reviewed; the instance owner or client can supply values directly | Structured sources | Everything else fails, or the client prefers direct conversation |

**If you can't determine the mode, ask explicitly:**
- "What's your preferred source? Should I connect live to Supernova, extract from files you'll provide, or shall we set it up conversationally?"

---

## Step 1: Connect to All Available Sources

This step differs by mode. Complete only the substeps that apply.

### 1A: Connect to Supernova MCP (Mode A only)

**Entry condition:** Supernova MCP endpoint is available and confirmed.

**Procedure:**

1. Verify the Supernova workspace URL or workspace ID.
2. Via the MCP connection, query the workspace for:
   - Current token set metadata (last updated, version)
   - All token collections (colors, typography, spacing, motion, elevation, radius)
   - Component sets (if Supernova tracks components)
3. Validate that the token set is populated (not empty). If empty, escalate and ask the client to populate tokens first.
4. Cache the Supernova connection details for later refresh.

**Output for this substep:** MCP connection confirmed; token metadata loaded.

### 1B: Connect to Git Token Repository (Mode A/B)

**Entry condition:** Git token repository URL is available.

**Procedure:**

1. Clone or pull the token repository to a working directory.
2. Identify the token source format:
   - DTCG token JSON file(s) (default: `tokens.json` or `tokens/`)
   - Style Dictionary config (`style-dictionary.config.js` or `config.json`)
   - Custom token structure (document the structure; proceed with 1D)
3. If Style Dictionary: extract the `platforms` and `buildPath` to understand the output targets.
4. Validate that token definitions exist. If the repo is empty or token files are missing, report and ask the client to commit token definitions.
5. **For Mode B (file-based):** If no Git URL is available (i.e., tokens are provided as exported files), record the source as `"file://uploaded/tokens.json"` or describe the original source path if known. The schema allows string values, so document the file location or "uploaded" if provided directly.

**Output for this substep:** Git repository cloned (Mode A) or file source recorded (Mode B); token format identified.

### 1C: Connect to Git Component Repository (Mode A/B)

**Entry condition:** Component library repository URL is available.

**Procedure:**

1. Clone or pull the component repository.
2. Identify the framework and structure:
   - React + TypeScript: look for `src/`, `components/`, or component.tsx files
   - Web Components: look for `.js` files with class definitions or custom element registration
   - Vue: look for `.vue` files
   - Svelte: look for `.svelte` files
   - Other: document the structure
3. Document the root component directory and the naming/file conventions.
4. Do NOT analyze all components yet. That happens in Step 3.

**Output for this substep:** Component repository cloned; framework and structure identified.

### 1D: Connect to Figma (Mode A/B)

**Entry condition:** Figma file URL(s) are provided.

**Procedure:**

1. For each Figma file:
   - Extract the file key and node IDs (if available).
   - Query Figma API (or note that manual export is required) for token sets and component pages.
   - If live Figma API access is unavailable, ask the client to export:
     - Design tokens as JSON (if Figma Tokens plugin is in use)
     - Component screenshots or page PDF
2. Store the file metadata (name, URL, last accessed) for reference.

**Output for this substep:** Figma file(s) identified; token/component data extracted or export requested.

### 1E: Locate and Validate Brand/Voice Documents (All modes)

**Entry condition:** Any reference to voice guidelines, brand guidelines, or copy rules.

**Procedure:**

1. Request or locate all documents that define brand voice, copy rules, or tone guidelines.
   - PDFs, Markdown files, Notion pages, Google Docs, or in-memory guidelines from the client.
2. For each document, note:
   - Format (PDF, MD, Google Doc, etc.)
   - Sections that cover: tone, prohibited words, CTA style, formatting rules, terminology.
   - Date created and last updated.
3. If no voice/brand guidelines exist, flag this. Voice rules are optional but should be flagged as a gap.

**Output for this substep:** Brand/voice documents located and inventoried.

---

## Step 2: Extract and Validate Design Tokens

This step is identical across all modes. The input may differ (MCP vs. files vs. conversation), but the output is the same.

### 2A: Extract Typography Tokens

**Procedure:**

1. From the token source (Supernova MCP, DTCG JSON, or Style Dictionary), extract all typography-related tokens:
   - Font families (display, body, utility/mono)
   - Font weights available for each family
   - Type scale (h1, h2, h3, h4, h5, h6, body-large, body, body-small, label, label-small, caption, etc.)
   - Font provider/loading strategy (Google Fonts, Adobe Fonts, self-hosted)
   - Font loading URLs or @import statements

2. For each font family, document:
   - CSS font-family name (e.g., `"Inter", sans-serif`)
   - Fallback stack
   - Available weights (e.g., [300, 400, 500, 700])
   - When this family should be used (e.g., "Headings only" or "Body text and UI")

3. Validate the type scale:
   - Each scale value should be a CSS clamp() expression (preferred) or a fixed size (px, rem, etc.)
   - clamp() values should follow the pattern: `clamp(min, preferred, max)` where the preferred value scales with viewport size.
   - Example: `clamp(1.5rem, 2vw + 1rem, 3rem)` for h1.
   - If fixed values: ensure each scale step has a consistent ratio (1.25x, 1.5x, or 1.618x golden ratio).

4. If any typography token is missing or incomplete, flag it in the completeness report (Step 7).

**Output for this substep:** `tokens.typography` object with families, scale, and loading metadata.

### 2B: Extract Color Tokens

**Procedure:**

1. From the token source, extract all color tokens organized by category:
   - **Backgrounds:** primary, secondary, surface, surface-elevated, etc.
   - **Text:** primary, secondary, tertiary, inverse, etc.
   - **Structural:** borders, dividers, outlines, etc.
   - **Accent:** brand colors, highlights, focus states, etc.
   - **Semantic:** success (green), warning (yellow/orange), error (red), info (blue), etc.

2. For each color, document:
   - Semantic name (e.g., `text-primary`)
   - Value (hex, rgb, HSL, or CSS variable reference)
   - Role/usage (e.g., "Primary text on light backgrounds")
   - Any light/dark mode variants (if applicable)

3. Extract prohibited colors (if documented):
   - Colors the brand explicitly avoids and why (e.g., "No pure blue. Uses adjusted blue for accessibility")
   - Store as objects with `value` and `reason` fields.

4. Validate contrast pairs:
   - Pair each text color with each background color.
   - Calculate WCAG contrast ratio (see Step 5).
   - Flag any text/background pair that fails AA (< 4.5:1 for normal, < 3:1 for large).

5. If any color token is missing, flag in completeness report.

**Output for this substep:** `tokens.color` object with backgrounds, text, structural, accent, semantic, prohibited, and contrast notes.

### 2C: Extract Spacing Tokens

**Procedure:**

1. From the token source, extract spacing tokens:
   - **Base unit:** The foundational spacing unit (e.g., `8px` or `0.5rem`).
   - **Rhythm description:** How spacing scales (e.g., "Multiples of base unit: 4px, 8px, 16px, 24px, 32px, 48px, 64px, etc." or "Fibonacci sequence").
   - **Tiers:** Named spacing tiers for section padding (e.g., `tight: 1rem`, `default: 2rem`, `spacious: 3rem`).
   - **Content max-width:** Maximum width for readable content (e.g., `1200px`).
   - **Page padding:** CSS clamp() for horizontal page-level padding (e.g., `clamp(1rem, 5vw, 2rem)`).
   - **Grid gap:** CSS clamp() for grid gaps (e.g., `clamp(1rem, 2vw, 2rem)`).

2. Validate the spacing system:
   - Base unit should be consistent across all scale multiples.
   - Tiers should be relative multiples of the base unit (e.g., 2x, 3x, 4x, etc.).
   - Page padding and grid gap should use clamp() for responsive behavior.

3. If spacing is not explicitly defined, infer it from the token set using this algorithm:
   - **Multiplicative rhythm (e.g., 4px, 8px, 16px, 32px):** Identify the smallest value as base unit (e.g., 4px). Calculate the multiplier (2x in this case). Describe as "multiplicative, base 4px, 2x scale."
   - **Linear rhythm (e.g., 8px, 16px, 24px, 32px):** Identify the base unit (8px) and the increment (8px). Describe as "linear, 8px increments."
   - **Mixed rhythm:** If no clear pattern emerges, set rhythm to "mixed" and document the observed pattern in the completeness report.
   - Use the most common spacing value as the base unit when unclear.
   - Flag as "inferred" in the completeness report when rhythm is derived from observations rather than explicit documentation.

**Output for this substep:** `tokens.spacing` object with base, rhythm, tiers, content max-width, page padding, and grid gap.

### 2D: Extract Motion Tokens (Optional)

**Procedure:**

1. From the token source, extract motion tokens (if defined):
   - **Easing curves:** Named easing functions (e.g., `ease-in-out`, `ease-out-quart`, `custom-entrance`, etc.)
   - **Durations:** Duration ranges by interaction type (e.g., `micro: 100ms`, `standard: 200ms`, `entrance: 300ms`)
   - **Stagger:** Default timing delay per child element in sequences (e.g., `50ms`)
   - **Principles:** Prose description of the brand's motion philosophy (e.g., "Subtle and purposeful. No gratuitous movement. Respects prefers-reduced-motion.")

2. Validate easing curves:
   - If CSS keyword (e.g., `ease-in-out`): accept as-is.
   - If cubic-bezier: validate the syntax (e.g., `cubic-bezier(0.43, 0.13, 0.23, 0.96)`).
   - If custom named: document the name and ask for the actual CSS value.

3. If motion tokens are not defined, that's acceptable. Motion is optional. Set to empty object and flag in completeness report.

**Output for this substep:** `tokens.motion` object with easing, durations, stagger, and principles (or empty if undefined).

### 2E: Extract Elevation and Radius Tokens

**Procedure:**

1. From the token source, extract elevation tokens (shadows):
   - Named shadow values (e.g., `shadow-sm`, `shadow-md`, `shadow-lg`, `shadow-xl`)
   - Each shadow should be a CSS box-shadow value (e.g., `0 1px 3px rgba(0,0,0,0.12)`)
   - Document when each elevation tier is used (e.g., "sm for subtle elevation, md for raised cards")

2. Extract border radius tokens:
   - Named radius values (e.g., `radius-none`, `radius-sm`, `radius-md`, `radius-lg`, `radius-full`)
   - Each should be a CSS border-radius value (px, rem, or %)
   - Document when each tier is used (e.g., "sm for input fields, md for cards, full for pills/avatars")

3. If either category is undefined, set to empty object and flag in completeness report.

**Output for this substep:** `tokens.elevation` and `tokens.radius` objects.

---

## Step 3: Analyze Component Library (Level 1-2 Analysis)

**Entry condition:** Component repository is available (Mode A/B) or the instance owner provides component inventory directly (Mode C).

**Skip this step if:** No component repository exists and the instance owner does not provide component data. Note in completeness report.

### 3A: Scan Repository Structure

**Procedure:**

1. Navigate to the component directory root.
2. List all components at the top level. Do not recurse deeply yet.
3. For each component, extract:
   - **Name:** Component file or folder name
   - **Path:** Relative path to component source
   - **Category:** Classify as one of:
     - `primitive` (Button, Icon, Input, Checkbox, etc. Lowest-level building blocks)
     - `composite` (Card, Modal, Dropdown, Tabs, etc. Combines primitives)
     - `layout` (Grid, Stack, Sidebar, Header, Footer, etc. Structural)
     - `utility` (Spacer, Divider, Badge, etc. Supplementary)
     - `page-level` (Page, Template, etc. Full-page components)
   - **Framework:** React, Vue, Web Component, etc. (from repo metadata)

4. Extract visible metadata from each component:
   - README if present
   - Storybook stories if present
   - PropTypes or TypeScript interface (first 10 props max)
   - Variant enum values (e.g., `variant: "primary" | "secondary"`)
   - Common slot names (e.g., `icon`, `label`, `children`)

**Output for this substep:** Inventory of top-level components with names, paths, categories, and visible props/variants.

### 3B: Extract Component Dependencies and Token Usage

**Procedure:**

1. For each component, scan the source code (first 50-100 lines, then look for token/CSS references):
   - What tokens does it use? (Look for references to color tokens, spacing tokens, font names.)
   - What other components does it import/depend on?
   - What CSS custom properties are referenced? (e.g., `var(--color-primary)`)

2. Build a lightweight dependency graph:
   - Button might use color tokens and depend on nothing.
   - Card might use elevation tokens and spacing tokens.
   - Modal might depend on Button, Overlay, and use motion tokens.

3. Do NOT deep-dive into every line of code. Aim for a 10-30 second scan per component.

**Output for this substep:** For each component, a list of tokens used and direct dependencies.

### 3C: Extract Component Conventions

**Procedure:**

1. From the component source, extract library-wide conventions:
   - **Naming:** Are components named with PascalCase? Kebab-case? Do they have consistent prefixes?
   - **Props:** Do all components use prop objects? Are props consistently named (e.g., `isOpen`, `isDisabled`, `variant`)?
   - **Variants:** How are variants defined? (enum, union types, CSS classes?)
   - **Composition:** Do components use render props, slots, or compound components? How is composition typically structured?
   - **Styling:** CSS Modules? CSS-in-JS? Inline styles? BEM? Utility classes?
   - **Testing:** Do all components have test files? What's the naming convention? What's tested?

2. Read one-two representative component implementations to understand the pattern.

3. Document findings as prose (1-2 sentences per convention).

**Output for this substep:** `components.conventions` object with naming, props, variants, composition, styling, and testing.

### 3D: Detect Design System Drift (Optional, Lightweight)

**Procedure:**

1. For a sample of 5-10 components, check for drift:
   - **Token drift:** Does the component use tokens from `tokens.color`, `tokens.spacing`, etc., or hardcoded values?
   - **Pattern drift:** Does the component follow the conventions from 3C, or does it deviate (e.g., uses a different prop naming scheme)?
   - **API drift:** Do component props follow a consistent pattern across the library, or do similar components have different prop interfaces?

2. For each drift instance, document:
   - Component name
   - Drift type (token/pattern/api)
   - Specific example (e.g., "Button uses hardcoded #007BFF instead of color-primary token")

3. Do NOT attempt a full audit. This is a lightweight scan to catch obvious issues.

4. If no drift is detected in the sample, note "No obvious drift detected in sample."

**Output for this substep:** `components.drift` object (if drift detected) with token_drift, pattern_drift, and api_drift arrays.

---

## Step 4: Extract Voice Rules (Inline, All Modes)

**Entry condition:** Brand/voice documents exist (from Step 1E).

**Procedure:**

1. Read all brand/voice documents (PDFs, Markdown, Notion, or summarized by the instance owner).

2. Extract the following into structured form:

   **Tone (string):**
   - Look for prose describing the overall tone. Example: "Warm, conversational, expert. Sounds like a smart friend."
   - Document 1-3 sentences.

   **Prohibited words (array of strings):**
   - Explicit list of words that must never appear in UI copy.
   - Common examples: "leverage," "unlock," "supercharge," "disrupt," "synergy," etc.
   - Also HeyHi's banned words: leverage, unlock, supercharge, disrupt, 10x, full-service, digital experiences, synergy, stakeholder alignment, cutting-edge, next-gen, revolutionary, game-changing, empower, holistic, seamless.
   - Return as array: `["leverage", "unlock", "supercharge"]`

   **Prohibited patterns (array of strings):**
   - Sentence structures or phrase patterns to avoid.
   - Examples: "Don't use passive voice in CTAs," "Avoid double negatives," "No corporate jargon."
   - Return as array: `["passive voice in CTAs", "double negatives", "corporate jargon"]`

   **CTA style (string):**
   - How should call-to-action buttons and links sound?
   - Example: "Human, specific, and direct. Use verbs. Example: 'Start a conversation' instead of 'Get started.'"
   - Document as 1-2 sentences.

   **Formatting rules (object):**
   - Preferences for capitalization, punctuation, separators, etc.
   - Examples: `{ "titles": "title case", "lists": "sentence case", "separators": "em dash" }`
   - Keep as flat key-value pairs.

   **Terminology (object):**
   - Preferred terms. Map generic/common terms to the brand's specific vocabulary.
   - Examples: `{ "user": "team member", "workflow": "process", "tool": "platform" }`
   - Return as flat key-value pairs.

3. If any section is not defined in the brand documents:
   - Set to `null` (not empty string, not empty array).
   - Flag in completeness report as a gap.

4. Validate the extracted rules:
   - Are prohibited words actual words (not phrases)?
   - Does tone description match the brand personality from Step 2A?
   - Is CTA style specific and actionable?

**Output for this substep:** `voice` object with tone, prohibited_words, prohibited_patterns, cta_style, formatting, and terminology.

---

## Step 5: Calculate and Validate Contrast Ratios

**Entry condition:** Color tokens are extracted (Step 2B).

**Procedure:**

1. **Prioritize contrast testing to avoid scope explosion.** Check these pairs in this order:
   - Primary text color on all background colors (typically 3-5 pairs)
   - Secondary text color on all background colors (typically 3-5 pairs)
   - Each accent/semantic color (success, warning, error, info) on their most likely background(s) (typically 5-10 pairs)
   - This yields approximately 15-25 pairs, not a full combinatorial matrix of every text color on every background.
   - Skip pairs that are unlikely to be used (e.g., "primary text on error background" if error is used as an alert badge, not a background).

2. For each selected pair, calculate the WCAG AA contrast ratio:
   - Formula: (L1 + 0.05) / (L2 + 0.05), where L1 and L2 are relative luminance values.
   - Use a contrast calculator (JavaScript library, online tool, or manual calculation).
   - Validate that each pairing meets AA minimum:
     - Normal text: 4.5:1
     - Large text (18px+ or 14px+ bold): 3:1

3. Generate a `contrast_notes` array:
   - For each passing pair, note: "primary text on light background: 7.2:1 ✓"
   - For each failing pair, note: "secondary text on secondary-light background: 2.8:1 ✗ FAILS AA"

4. Highlight critical failures:
   - If primary text on primary background fails, that's a critical issue. Flag for escalation.
   - If multiple semantic color pairs fail, document the impact.

5. If all pairs pass, note: "All tested text/background combinations meet WCAG AA." If partial failures exist, provide a summary of which combinations fail.

6. Store findings in `tokens.color.contrast_notes` as an array of strings.

**Output for this substep:** Updated `tokens.color` object with `contrast_notes` array.

---

## Step 6: Assemble the Configuration Object

**Procedure:**

1. **Brand section guidance (if temperature or personality are missing):**
   - **Temperature:** Infer from the dominant color palette. Warm hues (reds, oranges, yellows) indicate "warm" temperature. Cool hues (blues, purples, teals) indicate "cool" temperature. Neutral grays dominant indicate "neutral" temperature. If unsure, ask the instance owner.
   - **Personality:** Extract from the brand guidelines document if available (typically a 1-2 sentence description of the visual language). If no explicit guidelines exist, draft a 1-2 sentence personality description based on the visual language of the token set. Example: "Modern and technical. Uses primary color sparingly for impact, plenty of white space, sans-serif typography." After drafting, ask the instance owner to confirm it matches the intended brand.

2. Combine all extracted data into the full schema-conformant object:

   ```json
   {
     "brand": {
       "name": "[from client or Supernova workspace]",
       "description": "[from brand docs or inferred from workspace]",
       "temperature": "[warm | cool | neutral, from design philosophy]",
       "personality": "[from brand docs, 1-2 sentences]"
     },
     "tokens": {
       "typography": "[from Step 2A]",
       "color": "[from Step 2B + Step 5]",
       "spacing": "[from Step 2C]",
       "motion": "[from Step 2D]",
       "elevation": "[from Step 2E]",
       "radius": "[from Step 2E]"
     },
     "voice": "[from Step 4]",
     "components": "[from Step 3A-3D]",
     "repository": {
       "token_repo": "[Git URL from Step 1B]",
       "component_repo": "[Git URL from Step 1C]",
       "supernova_workspace": "[URL or ID from Step 1A]"
     },
     "custom_patterns": [],
     "meta": {
       "generated_at": "[ISO 8601 timestamp]",
       "generated_by": "[Mode A | Mode B | Mode C]",
       "last_refreshed": "[ISO 8601 timestamp, same as generated_at]",
       "version": "1.0"
     }
   }
   ```

3. **Note on custom_patterns:** This field starts as an empty array. It is intentionally not extracted during onboarding. Custom patterns are populated later by the companion design-system-patterns workflow (currently in development). This is not a gap; it is by design.

4. Validate the object against the schema (see Step 7).

3. Do not write to disk yet. Move to validation first.

**Output for this substep:** Complete, unsaved configuration object in memory.

---

## Step 7: Validate Against Schema and Completeness Report

**Procedure:**

1. **Schema validation:**
   - Check that all required fields (`brand` and `tokens`) are present and non-empty.
   - Check that all object properties conform to their expected types (string, array, object).
   - Verify that `brand.name` is a non-empty string (required).
   - Verify that `tokens` contains at least typography and color (required).
   - If any required field is missing or malformed, report error and do not proceed to Step 8.

2. **Completeness scoring:**
   - For each section (brand, tokens.typography, tokens.color, tokens.spacing, tokens.motion, tokens.elevation, tokens.radius, voice, components, repository), assign a status:

     | Status | Criteria | Visual |
     |--------|----------|--------|
     | **Green (Complete)** | All expected fields present, validated, and populated with meaningful data. No gaps or warnings. | ✓ |
     | **Yellow (Partial)** | Core fields present and valid, but some optional fields missing or unverified. Safe to use but some functionality limited. | ◐ |
     | **Red (Critical Gap)** | Required fields missing, invalid, or empty. Blocks downstream workflows (e.g., missing token_repo blocks design-system-care-monthly refresh; missing brand.name blocks all usage). | ✗ |

   **Clarification on scoring behavior:** Red does NOT mean the config file is not written. The skill ALWAYS writes the config file to disk (even with Red sections). Red sections are flagged prominently in the completeness report. The rule is: STOP and ask the instance owner ONLY if `brand.name` or `tokens` (both required by schema) are Red. Yellow and Red for optional sections (motion, elevation, voice, components) are documented in the report but do not block file creation.

   - **Brand:** Green if name, description, temperature, and personality are all non-empty and coherent. Yellow if one is missing. Red if name is missing.
   - **Tokens.Typography:** Green if families (display, body, utility) and scale are present and complete. Yellow if scale is partial or families lack weights. Red if families or scale are missing.
   - **Tokens.Color:** Green if all five categories (backgrounds, text, structural, accent, semantic) are populated. Yellow if one category is sparse. Red if backgrounds or text are missing.
   - **Tokens.Spacing:** Green if base, rhythm, tiers, content max-width, and page padding are defined. Yellow if some are inferred or incomplete. Red if base and rhythm are missing.
   - **Tokens.Motion:** Green if easing, durations, and principles are defined. Yellow if only one is defined. Red if all are absent (note: motion is optional, so Red is acceptable with a flag).
   - **Tokens.Elevation:** Green if at least 3 elevation tiers are defined. Yellow if fewer. Red if absent (note: elevation is optional).
   - **Tokens.Radius:** Green if at least 3 radius tiers are defined. Yellow if fewer. Red if absent (note: radius is optional).
   - **Voice:** Green if tone, prohibited_words, cta_style, and terminology are present. Yellow if some are missing. Red if all are missing (note: voice is optional but should be flagged).
   - **Components:** Green if inventory is populated and conventions are documented. Yellow if only partial inventory or conventions missing. Red if inventory is empty or missing (note: components are optional but recommended).
   - **Repository:** Green if at least one source (supernova_workspace, token_repo, or component_repo) is recorded. Yellow if sources are incomplete or partially recorded. Red if all are missing.

3. **Generate completeness report:**

   ```
   DESIGN SYSTEM ONBOARDING REPORT
   ================================

   Client: [name]
   Design System: [name]
   Generated: [ISO date/time]
   Mode: [A | B | C]

   SECTION COMPLETENESS
   =====================

   Brand:              ✓ Complete
   Typography:        ◐ Partial (scale complete, weights incomplete for utility font)
   Color:             ✓ Complete (16 tokens, all AA contrast-safe)
   Spacing:           ✓ Complete (base 8px, 5 tiers, rhythm defined)
   Motion:            ◐ Partial (easing defined, durations incomplete)
   Elevation:         ✓ Complete (5 shadow tiers)
   Radius:            ✓ Complete (4 radius tiers)
   Voice:             ✓ Complete (tone, prohibited_words, cta_style, terminology)
   Components:        ◐ Partial (18 components catalogued, drift analysis incomplete)
   Repository:        ✓ Complete (Supernova + token repo + component repo connected)

   OVERALL: ✓ Ready for ui-studio

   GAPS & FLAGS
   ============

   [Optional] 1. Motion durations are defined but stagger timing is missing. Recommend adding.
   [Optional] 2. No custom patterns catalogued yet. Can be added later via design-system-patterns skill.
   [Warning] 3. Component library has light token drift in Button component (uses hardcoded color instead of token). Recommend audit and fix before first build.
   [Info] 4. Voice rules are complete. No AI-tell patterns detected.

   USAGE NOTES
   ===========

   The active-brand.json is ready for immediate use with the ui-studio skill.

   For monthly maintenance, use design-system-care-monthly to:
   - Re-validate contrast ratios
   - Detect token or pattern drift in component library
   - Refresh voice rule compliance across deployed UI

   To extend the system, use:
   - design-system-patterns (future skill, not built): Add brand-specific interaction patterns
   - design-system-voice (future skill, not built): Refine voice rules based on launched content

   ```

4. If the overall completeness is Red (any required field missing), ask the instance owner before proceeding. Do not save an incomplete config.

**Output for this substep:** Completeness report (printed to console) and schema validation status.

---

## Step 8: Store the Config and Confirm

**Entry condition:** Schema validation passes (Step 7). Completeness is Green or Yellow (not Red for required fields).

**Procedure:**

1. **Determine output path:**
   - If this is a new design system: write to `/heyhi-skills/ui-studio/brand-config/active-brand.json`
   - If this is a refresh: overwrite the existing file.
   - If the instance owner specifies a different path: use that path.

2. **Write the file:**
   - Serialize the config object to JSON with 2-space indentation.
   - Include the full object (no truncation).
   - Write to disk at the chosen path.

3. **Confirm success:**
   ```
   ✓ Config written to: [path]
   ✓ File size: [X KB]
   ✓ Schema validation: PASSED
   ✓ Completeness: [Green | Yellow with flags]
   ✓ Ready for ui-studio skill
   ```

4. **Next steps:**
   - If completeness is Yellow with gaps: list the gaps and recommend follow-up actions (e.g., "Add motion durations via Step 2D" or "Re-run component analysis via Step 3 after drift fixes").
   - If Red flags exist: note what needs to be addressed before first use.
   - If all is Green: confirm the system is ready for immediate use.

5. **Provide access info:**
   - Print the config object (full JSON) so the instance owner can review.
   - Highlight any sections that required conversion, inference, or manual entry (so the instance owner knows what needs verification).

**Output for this substep:** Config file written; validation report printed.

---

## Mode-Specific Workflows

### Mode A: Live Supernova + Git (Connected Environment)

**Flow:**
1. Step 0: Confirm Supernova MCP endpoint and Git repo URLs
2. Step 1: Connect to Supernova (1A), token repo (1B), component repo (1C), brand docs (1E)
3. Step 2: Extract tokens from Supernova and Git
4. Step 3: Analyze component repo
5. Step 4: Extract voice rules from brand docs
6. Step 5: Validate contrast
7. Step 6: Assemble config
8. Step 7: Validate and report
9. Step 8: Write to disk

**When to use:** First-time onboarding. Client has infrastructure in place.

**Advantage:** Real-time data. Components can be re-analyzed monthly without re-running Step 3. Token updates in Supernova are reflected on refresh.

---

### Mode B: File-Based (Snapshots)

**Flow:**
1. Step 0: Confirm that DTCG JSON, Style Dictionary config, or exported Figma data will be provided
2. Step 1: Request and receive files; unzip/validate formats
3. Step 2: Parse DTCG JSON or Style Dictionary config to extract tokens
4. Step 3: If component exports exist, analyze them; otherwise skip
5. Step 4: If brand documents provided, extract voice rules; otherwise flag gap
6. Step 5: Validate contrast
7. Step 6: Assemble config
8. Step 7: Validate and report
9. Step 8: Write to disk

**When to use:** Client cannot provide live infrastructure access. Prefers to export snapshots. Good for rapid setups.

**Advantage:** No MCP dependencies. Works offline. Can be repeated with new exports to refresh.

---

### Mode C: Conversational (Direct Entry)

**Flow:**
1. Step 0: Confirm the instance owner has reviewed client materials and can supply values directly
2. Step 1: Skip (no sources to connect to)
3. Step 2: Ask the instance owner for token values. Prompt structured questions:
   - "What are your font families? Display, body, utility?"
   - "What's your primary text color and primary background color? (Hex or color name)"
   - "What's your spacing base unit?" etc.
4. Step 3: Ask for component list (or skip if no library yet)
5. Step 4: Ask about voice rules or infer from brand personality
6. Step 5: Calculate contrast for provided colors
7. Step 6: Assemble config
8. Step 7: Validate and report
9. Step 8: Write to disk

**When to use:** Rapid iteration. Client materials are simple or well-understood. Design system is nascent.

**Advantage:** Fast setup. No parsing required. Good for MVPs.

**Limitation:** More prone to gaps; requires manual follow-up to fill in detail.

---

### Mode D: Moodboard-Driven (New Identity Work)

**Entry condition:** A designer has delivered a moodboard (freeform visual board, FigJam, PDF, or structured template). No existing token infrastructure exists. Direction may or may not be resolved.

**Before you start:** Read `ai-services/design-intelligence/gate0-facilitation-guide.md`. If the designer delivered multiple directions, you must complete Gate 0 (direction lock) before this mode can run. Token extraction cannot begin until a single direction is locked.

**If the moodboard is primarily visual with no labeled values (Inferred confidence):** Before opening the extraction spec, first read `ai-services/design-intelligence/style-to-token-translation.md`. Work through Parts 1–4 against the specific moodboard in front of you. The translation doc produces the values (interpretation); `moodboard-to-brand-json.md` writes them (extraction). Running extraction without the interpretation step produces structurally correct configs that are aesthetically undergrounded. This pre-step is not optional for visual-only moodboards.

Read `ai-services/design-intelligence/moodboard-to-brand-json.md` for the section-by-section mapping from moodboard template → active-brand.json, confidence handling rules, and validation checks (REQUIRED / WARNING / BLOCKING).

**After Mode D produces a v0 config:** Run `ai-services/design-intelligence/designer-review-protocol.md` to validate with the designer and reach v1 before using the config as a constraint boundary.

**Flow:**
1. **Gate 0 pre-check:** Determine direction count and resolution level (see facilitation guide Phase 0)
   - If one resolved direction: proceed to step 2
   - If multiple directions: run `gate0-facilitation-guide.md` Phases 0–3 first. Return here after direction lock.
2. **Step 0:** Confirm the locked direction. Retrieve completed moodboard template (Sections 1–9) for that direction.
3. **Step 1:** Skip live sources (Mode A/B steps). Input is the completed moodboard template.
4. **Step 2A (Typography):** Extract from moodboard template Section 3. Check candidate confidence level. If font candidate is "Not yet selected," block typography token extraction and flag as critical gap.
5. **Step 2B (Color):** Extract from moodboard template Section 2. Use confidence levels: Extracted values seed tokens directly. Inferred values are flagged as provisional. TBD blocks that color role's token. Do not write semantic token values here — those are handled in Step 5a after palette confirmation.
5a. **Step 2D.2a (Semantic Color Generation — conditional):** Run this step only after `tokens.color.backgrounds.primary`, `tokens.color.accent.primary`, and `tokens.color.text.primary` are all `CONFIRMED` (not `PROVISIONAL`). This may be in the same session (if the designer confirms palette mid-session) or a follow-up session after the missing-values-request form is returned.
   - Run `node heyhi-design-intelligence-tests/scripts/generate-semantic-colors.cjs path/to/active-brand.json` to generate three palette-harmonized options for each semantic role (success, warning, error, info), validated at WCAG AA (4.5:1) against the actual brand background.
   - Deliver the generated `semantic-color-options.md` table to the designer via the missing-values-request form (Section: Semantic Colors), or share directly.
   - **Warning color rule:** Warning must never be a bright yellow or saturated amber. All warning options use dark amber or rust tones. Non-negotiable.
   - Wait for designer selection and the instance owner's validation before writing any semantic token value to the config.
   - Write confirmed values as `CONFIRMED: #hex`. Log selection rationale in `meta.implementation_notes`.
   - Full procedure and interpretation guidance (flag patterns by palette temperature): `skill-updates/design-system-onboard-mode-d/MODE-D-EXTENSION.md` → Step 2D.2a.
   - **If brand colors are still PROVISIONAL at end of session:** Skip this step. Add a note in the completeness report that semantic color generation is blocked pending palette confirmation. The script will exit with code 1 and explain what's missing if run prematurely.
6. **Step 2C (Spacing):** Extract from moodboard template Section 4 (density, grid intent, content width). For grid intent specifically: use a named pattern from `ai-services/design-intelligence/grid-layout-examples.md` as the primary value in `meta.grid_structure` wherever one fits — load the Pattern Summary Index (~300 tokens) for lightweight lookup. Follow the extraction rules in `moodboard-to-brand-json.md` Part 1, Section 4.2 Grid Intent.
7. **Step 2D (Motion):** Extract from moodboard template Section 6 (motion philosophy, personality).
8. **Step 2E (Elevation/Radius):** Extract from moodboard template Sections 5.1–5.2.
9. **Step 3:** Skip component analysis (no library yet). Flag as gap.
10. **Step 4:** Extract voice rules from brand documents or HeyHi positioning docs.
11. **Step 5:** Validate contrast on all confirmed color tokens. Flag provisional colors as not-yet-validated. If Step 5a ran and semantic colors are confirmed, include all four semantic pairs (`semantic.*` on `backgrounds.primary`) in this validation pass.
12. **Step 6:** Assemble config. Mark `meta.generated_by` as `"mode-d"`. Write provisional token values using the `PROVISIONAL:` string prefix convention: `"PROVISIONAL: approximately #2D5A3D based on moodboard references"`. For each provisional field, add an entry to `meta.provisional_fields[]` as an object: `{ "path": "tokens.color.accent.primary", "reason": "Inferred from Direction C references. Awaiting designer confirmation.", "confidence": "inferred" | "pending" }`. See `ai-services/design-intelligence/moodboard-to-brand-json.md` Part 7 for the full convention and examples.
13. **Step 7:** Validate and report. The completeness report will show gaps — this is expected for Mode D. Name what's provisional and what's blocked.
14. **Step 8:** Write to disk. Config is a starting point, not a finished system.
15. **Designer Handoff Artifact:** After writing the config, check `meta.field_provenance` for confidence levels.
    - If any field has `confidence: failing` → auto-generate the handoff artifact. Mode A is blocked until failing fields are resolved.
    - If fields have `confidence: provisional` or `confidence: inferred` only → offer the artifact. Mode A can proceed but output will be provisional.
    - Template: `heyhi-skills/ui-studio-onboard/templates/designer-handoff-artifact.md`
    - Output filename: `[client-name]-token-review-[date].md`
    - Mode D configs almost always require this step — provisional color and typography fields are the norm, not the exception.

**When to use:** New brand identity work. Website build with no prior token system. Client is starting from scratch with a designer's moodboard.

**Advantage:** Establishes a token foundation before any infrastructure exists. Embeds the taste decisions made in Gate 0 into the system from day one.

**Limitation:** Config will have provisional fields (color, typography) until the designer confirms specific values. Treat the first Mode D output as a version 0 that evolves through design refinement.

**After Mode D:** Once provisional fields are resolved (typeface selected, hex values confirmed), run the `design-system-review` skill in Mode A (v0→v1 promotion). Mode A resolves `PROVISIONAL:` prefixed values, removes their entries from `meta.provisional_fields[]`, updates `meta.generated_by` to `"mode-d-v1"`, and confirms 5-dimension visual fidelity before the config enters production. Do not manually remove provisional markers — Mode A handles the transition and requires a HUMAN GATE before promotion.

---

## Completeness Scoring Reference

| Section | Green (✓) | Yellow (◐) | Red (✗) |
|---------|-----------|-----------|---------|
| **Brand** | name, description, temperature, personality all present | One field missing | name missing |
| **Typography** | families (D, B, U) + scale complete; at minimum regular (400) and bold (700) weights for body text. Display fonts may have single weight if that matches the brand's usage pattern. 3+ weights across all families preferred. | Scale partial or weights incomplete (e.g., fewer than 2 weights for body text); fewer than 3 total weights across families | families or scale missing |
| **Color** | All five categories populated (BG, text, structural, accent, semantic). In Mode D: semantic colors are generated via Step 2D.2a after palette confirmation — a Yellow score for semantic is expected until that step completes. | One category sparse | BG or text missing |
| **Spacing** | base, rhythm, tiers, max-width, page-padding all defined | Some inferred or incomplete | base/rhythm missing |
| **Motion** | easing, durations, stagger, principles present | One or two present | All missing (optional, flag) |
| **Elevation** | 3+ shadow tiers | 1-2 tiers | All missing (optional, flag) |
| **Radius** | 3+ radius tiers | 1-2 tiers | All missing (optional, flag) |
| **Voice** | tone, prohibited_words, cta_style, terminology present | Some missing | All missing (optional, flag) |
| **Components** | Inventory + conventions documented | Partial inventory, conventions incomplete | Inventory empty (optional, flag) |
| **Repository** | At least one source recorded (MCP, Git, Figma) | Sources incomplete | All missing |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Supernova workspace is empty | Ask client to populate tokens in Supernova first. Do not proceed with Mode A until tokens exist. |
| Git repo is not accessible | Verify URL and permissions. Fall back to Mode B (file export) if access cannot be granted. |
| Component library uses custom token format | Document the format in Step 1C. Proceed with manual extraction in Step 2 and Step 3. |
| Brand documents are informal or incomplete | Use Mode C: ask the instance owner for clarification and capture values directly. Flag gaps in completeness report. |
| Contrast fails for several color pairs | Document which pairs fail. Do not block config creation, but flag as critical for client to address. Recommend token adjustment. |
| No component library exists yet | Skill still runs. Set `components.source` to null. Flag in completeness as optional gap. ui-studio will work without components (Mode A will use token-level output only). |

---

## Output Checklist

Before confirming Step 8 complete, verify:

- [ ] Config object is valid JSON and matches schema
- [ ] `brand.name` is non-empty
- [ ] `tokens.typography` and `tokens.color` are populated
- [ ] All color hex values are valid (regex check: `^#[0-9A-Fa-f]{6}$`)
- [ ] All spacing values are valid CSS (px, rem, clamp(), etc.)
- [ ] Type scale uses consistent units (not mixed px and rem)
- [ ] `meta.generated_at` and `meta.last_refreshed` are ISO 8601 timestamps
- [ ] `meta.generated_by` is set to the mode used (A, B, C, or D)
- [ ] Repository section has at least one source URL
- [ ] Completeness report is generated and reviewed
- [ ] All Red gaps are flagged (even if optional)
- [ ] Config file is written to disk and readable

---

## Integration Points

**Consumed by:**
- `ui-studio`: Uses active-brand.json to drive all UI output
- `design-system-care-monthly`: Uses config to detect drift and regenerate monthly reports

**Mode B note for design-system-care-monthly:** Mode B configs are snapshot-based (no live connection to Supernova or Git). For design-system-care-monthly to track drift over time, Mode B clients should have their config refreshed at each care cycle by re-running design-system-onboard extraction against updated source files. This is lighter than Mode A (no live connection required) but requires the source files (DTCG JSON, Style Dictionary, or exported Figma data) to be current.

**Can reference:**
- `heyhi-design-intelligence-audit`: Can use the config as audit baseline
- `heyhi-voice`: If voice rules are incomplete, refer to this skill for refinement
- `ai-services/design-intelligence/gate0-facilitation-guide.md`: Multi-direction moodboard intake process (Mode D prerequisite when direction count ≥ 2)
- `ai-services/design-intelligence/moodboard-template.md`: Structured intake form that feeds Mode D
- `heyhi-style-selection` (Mode B): **Run this before Mode D begins when a moodboard is the input.** Mode B produces a structured YAML pre-classification — matched style name, confidence level, token implications, and `designer_confirmation_needed` fields — that primes Mode D before token extraction starts. This is the recommended path for all moodboard-driven onboarding.
- `ai-services/design-intelligence/style-reference-library.md`: Named style entries with `agent_context_snippet` and `token_implications` fields. Load the matched style's cluster entries during Mode D — the entry's token_implications are the authoritative token decisions for that direction. For font families specifically, use `typography_specimens.recommended_pairings` — `token_implications` carries type *personality* and *scale*, not font names; you may recombine across two recommended pairings or depart from one, but only with a one-line rationale tied to a brief constraint (credibility calibration, a font-count/performance budget, a forms-readability requirement), recorded in `meta.implementation_notes`. Five pilot entries complete (Grounded Modern, Warm Technical, Editorial Bold, Energy Redesign, Studio Craft) as of March 22, 2026; full library (20 entries) after Session F.

**Follow-up skills (recommended):**
- `design-system-patterns` (future skill, not built): Add custom interaction patterns after onboarding
- `design-system-voice` (future skill, not built): Refine and expand voice rules based on launched content

---

## Optional Schema Fields (ADR-004)

The style reference library includes optional enrichment fields that may be present in a style entry's `token_implications` but are not required during onboarding. When processing Mode D moodboard-driven configs, treat absent optional fields as "not yet enriched" — not as missing required data.

**Current optional fields (from ADR-004, March 24, 2026):**

- `default_scheme: dark` — Present on dark-native entries only (Entries 2, 3, 10, 15). Absent means light baseline is assumed. If this field is absent on a client's matched style entry, the config baseline defaults to light. Do not mark this as a gap.
- `border_radius_strategy` — Present when the entry requires variable radius logic beyond what the single-enum `border_radius_range` can express. Absent is normal for most entries.
- Motion optional fields (`motion_duration_range`, `motion_easing`) — See `style-to-token-translation.md` Part 4.4 for the Motion Token Priors Table. If the matched style entry lacks explicit motion range fields, use the cluster prior from the priors table.
- `motion_override` block — Present only when the entry's `industry_fit.natural` includes cognitive load conditions (mental health, crisis, trauma recovery, etc.). Absent is normal. See `heyhi-skills/heyhi-style-entry-author/SENSITIVE_CONTEXT_OVERRIDE.md` if the client's context includes any of those scope conditions.

**Handling absent optional fields in completeness report:** Do not flag absent optional fields as Red or Yellow gaps unless the client's context explicitly requires them. Sensitive context scope conditions (mental health platforms, crisis services) are the only case where an absent `motion_override` block should be raised as a concern — and only if the client's industry is in the scope list.

---

## Schema Gap Notes for Accessibility-First and Sector-Specific Clients (ADR-007)

When generating Mode D configs for clients in **civic, public-sector, healthcare, industrial IoT, or manufacturing** contexts, the current `active-brand.json` schema may not have dedicated fields for the following requirements. For each gap: document it in the completeness report, add a placeholder note to `brand.style_notes`, and list it in `meta.provisional_fields[]` as a TBD entry.

Full specification for all five extensions: `ai-services/_core/architecture-decisions/007-schema-extensions-accessibility-functional-color-i18n.md`

**Extension 1 — Focus ring tokens (`tokens.focus.outline.*`)**
Required for: WCAG 2.2 SC 2.4.13 — 2px minimum perimeter, 3:1 contrast between focused and unfocused states. Applies to all civic, public-sector, healthcare, and education engagements; mandatory for Civic Modern (Entry 16).
If `focus.outline.width/color/offset` fields are not yet in the schema: add to `brand.style_notes`: "Focus ring implementation required at component level (WCAG 2.2 SC 2.4.13): min 2px outline, 3:1 contrast against adjacent background. Token namespace pending ADR-007 schema extension."

**Extension 2 — Touch target minimum (`tokens.spacing.touch-target.*`)**
Required for: WCAG 2.2 SC 2.5.8 and accessible mobile interfaces. Mandatory for Civic Modern engagements; recommended for all clients.
If `spacing.touch-target.min` is not yet in the schema: add to `brand.style_notes`: "Touch target minimum: 44px (accessible baseline) / 48px (Civic Modern specification). Enforce at component level via min-height/min-width — not fixed dimensions."

**Extension 3 — ISA-101 alarm state (`tokens.color.feedback.alarm_high_priority`)**
Required for: Industrial IoT, SCADA, manufacturing, utilities, and construction tech clients using ISA-101 functional color conventions. Mandatory for Neo-Industrial (Entry 10) engagements.
The current `tokens.color.feedback` namespace covers three states (success/warning/error). ISA-101 requires five: gray (nominal), green (running), yellow (abnormal), orange (high-priority alarm), red (critical). If `alarm_high_priority` is not yet in the schema: populate as a PROVISIONAL value (~#E65100 ISA-101 orange) and document as a schema gap.
**Always add to `brand.style_notes` for ISA-101 clients regardless of schema status:** "ISA-101 requirement: color is never the sole status indicator. All chromatic alarm states require secondary shape/symbol encoding. Applies to all operational and industrial interfaces (~8% male operators have color vision deficiency)."

**Extension 4 — Contrast target (`meta.accessibility.contrast_target`)**
Required for: Clients targeting WCAG AAA (7:1) rather than the AA floor (4.5:1). Applies to public-sector, civic, healthcare, and education clients with above-standard accessibility commitments.
If `meta.accessibility.contrast_target` is not yet in the schema: add to `brand.style_notes`: "Accessibility target: WCAG 2.2 AAA (7:1 body text contrast). All color tokens must be validated against the AAA target, not the AA floor."

**Extension 5 — Internationalization budget (`meta.internationalization`)**
Required for: Civic, government, and multilingual-primary clients. Mandatory for Civic Modern engagements.
If `meta.internationalization` is not yet in the schema: add to `brand.style_notes`: "Text expansion budget: 35–40% for translated/bilingual content. All container dimensions must use min-height/min-width over fixed values. CSS logical properties required throughout (margin-inline-start, padding-block-start, etc.)."

---

## Dark-Native Mode D Procedure (ADR-006)

When Mode D is running for a client whose matched style entry has `default_scheme: dark` (Entries 2, 3, 10, 15), the config structure requires the `tokens.color.schemes` block in addition to the standard flat tokens. This applies to: Invisible Infrastructure (Entry 2), Night Shift (Entry 3), Neo-Industrial (Entry 10), and Invisible Grid (Entry 15).

**Step 1 — Detect dark-native entry.** After style selection returns the matched style entry, check for `default_scheme: dark`. If present, activate the dark-native extraction path.

**Step 2 — Populate `meta.default_scheme: "dark"`.** Set this field in the config metadata.

**Step 3 — Generate the `tokens.color.schemes` block.** Under `tokens.color.schemes`, populate two parallel objects: `dark` (the foundation scheme matching the style entry's dark foundation values) and `light` (the alternative scheme for accessibility, print, or high-contrast contexts). Both objects mirror the flat `tokens.color.*` structure: `backgrounds`, `text`, `structural`, `accent`, `semantic`.

**Confidence ceiling applies to both schemes (ADR-005):**
- Dark scheme values extracted from Figma color variables: `confidence: extracted`
- Dark scheme values inferred from moodboard mood/imagery: prefix with `PROVISIONAL:`, add to `meta.provisional_fields[]`
- Light scheme values for a dark-native entry: almost always `PROVISIONAL:` unless the client has a defined light mode — document in `meta.provisional_fields[]`

**Step 4 — Retain the flat tokens.color.* structure.** The flat tokens (`tokens.color.backgrounds`, `tokens.color.text`, etc.) should reflect the active default scheme values (dark for dark-native entries). The `schemes` block holds both parallel sets; the flat structure is the active scheme's shorthand.

**Step 5 — Document the dark architecture in the completeness report.** Note that the config uses Option C scheme namespacing (ADR-006). Call out which scheme values are provisional and what designer confirmation is needed to resolve them. Flag light scheme as provisional if the client has not yet confirmed their light mode intent.

**Step 6 — Mode D re-validation after designer confirmation.** When a designer confirms the dark-native color palette, run the `heyhi-style-to-token-reviewer` warning signs against both the dark and light scheme tokens. For Entry 10 (Neo-Industrial), the WS3 zone-density requirement requires confirming that the Augmented Fourth scope restriction (display headers only) is documented in `brand.style_notes`.

**Migration note for engineers:** The `tokens.color.schemes` block can be migrated to W3C DTCG `$modes` format by a future migration script when Style Dictionary 4.x + Token Studio MCP Server `$modes` support is confirmed stable. The migration path is documented in ADR-006.

---

## Session Notes

- **Time estimate:** 30-60 minutes depending on source complexity and completeness of client materials.
- **If you get stuck:** Ask the instance owner. This skill is conversational by design; gaps in data warrant clarification, not guessing.
- **Do not skip contrast validation:** WCAG compliance is not optional.
- **Flag all gaps, even optional ones:** Design system care happens monthly via design-system-care-monthly. Starting with a gap inventory makes that work clearer.

---

## Exit Gate Required Headers (bottom-of-skill bracket)

This skill closes through the Exit Gate Flavor A (`CLAUDE-SESSION-RULES.md § Exit Gate`). Before declaring done, confirm every required header below contains real content, not a claim:

- `## Fixes Applied`
- `## Smoke Test`
- `## Next Session Prompt`

If any header is empty or contains advisory prose ("I checked for bugs") instead of a concrete artifact, the gate has not been satisfied. Apply fixes until clean — then emit.

---

*Design System Onboarding. HeyHi. Bay Design LLC. March 2026.*

*HeyHi Confidential*
