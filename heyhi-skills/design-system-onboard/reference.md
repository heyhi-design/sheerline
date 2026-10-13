# Design System Onboarding Reference

Templates, formats, and quick-lookup guides for extracting design systems into validated `active-brand.json` configuration files.

---

## 1. Completeness Report Template

Generate this at the end of Step 7. Use it to communicate gaps and readiness to the client.

```
DESIGN SYSTEM ONBOARDING REPORT
================================

Client: [organization name]
Design System: [system name]
Generated: [ISO date/time]
Mode: [A | B | C]

SECTION COMPLETENESS
=====================

Brand:              [✓ | ◐ | ✗] [status line]
Typography:        [✓ | ◐ | ✗] [status line]
Color:             [✓ | ◐ | ✗] [status line]
Spacing:           [✓ | ◐ | ✗] [status line]
Motion:            [✓ | ◐ | ✗] [status line]
Elevation:         [✓ | ◐ | ✗] [status line]
Radius:            [✓ | ◐ | ✗] [status line]
Voice:             [✓ | ◐ | ✗] [status line]
Components:        [✓ | ◐ | ✗] [status line]
Repository:        [✓ | ◐ | ✗] [status line]

OVERALL: [✓ Ready | ◐ Ready with flags | ✗ Blocked]

GAPS & FLAGS
============

[Optional] 1. [category]: [specific gap and recommendation]
[Warning] 2. [category]: [issue affecting downstream work]
[Info] 3. [category]: [note or confirmation]

USAGE NOTES
===========

The active-brand.json is ready for immediate use with:
- ui-studio skill: Build brand-conformant pages
- design-system-care-monthly: Monthly maintenance and drift detection

To extend the system:
- design-system-patterns: Add custom interaction patterns
- design-system-voice: Refine voice rules based on deployed content
```

---

## 2. Brand Config Quick Reference

Schema sections with required fields and "Green" indicators. Reference the schema-conformant object shape when assembling configs.

### Brand Section

| Field | Type | Required | Green Indicator |
|-------|------|----------|---|
| `name` | string | Yes | Non-empty, matches the system's official name |
| `description` | string | No | 1-2 sentence description of visual identity or design philosophy |
| `temperature` | enum: warm, cool, neutral | No | One of the three values; influences neutral color choices |
| `personality` | string | No | 1-2 sentences describing brand personality as expressed through UI |

**Green example:**
```json
{
  "brand": {
    "name": "Acme Design System v2",
    "description": "Modern, accessible, and flexible. Built for scale.",
    "temperature": "warm",
    "personality": "Professional yet approachable. Confident without being corporate."
  }
}
```

### Tokens Section

**Required minimum:** `tokens.typography` and `tokens.color` (both non-empty).

| Category | Fields | Green Indicator |
|----------|--------|---|
| **typography** | families (display, body, utility with family, fallback, weights); scale (at least h1-h6, body, label); loading (provider, url) | All three families present; scale covers heading and body tiers; weights consistent per family |
| **color** | backgrounds (3+); text (3+); structural; accent; semantic (success, warning, error, info); contrast_notes array | All five categories populated; contrast_notes includes pass/fail notation for AA pairs |
| **spacing** | base (string, e.g., "8px"); rhythm (description); tiers (named values); content_max_width; page_padding; grid_gap | base and rhythm defined; tiers use multiples of base; clamp() used for responsive values |
| **motion** (optional) | easing (named curves); durations (by type); stagger; principles | At least easing and durations; principles describe brand motion philosophy |
| **elevation** (optional) | Named shadow tiers (sm, md, lg, xl) | 3 or more distinct shadow values |
| **radius** (optional) | Named radius tiers (sm, md, lg, full) | 3 or more distinct radius values |

---

## 3. Token Extraction Cheat Sheet

Map from source formats to the brand config schema.

### DTCG (Design Token Format Spec) JSON

**Source structure:**
```json
{
  "colors": {
    "primary": { "value": "#0066FF", "$type": "color" },
    "text-primary": { "value": "#111111", "$type": "color" }
  },
  "typography": {
    "font-family-display": { "value": "Poppins", "$type": "fontFamily" },
    "font-size-h1": { "value": "2.5rem", "$type": "dimension" }
  }
}
```

**Mapping:**
- `colors.*` that start with `bg-`, `background-`, or match common background names → `tokens.color.backgrounds`
- `colors.*` that start with `text-` or are clearly text colors → `tokens.color.text`
- `colors.*` that are semantic (success, warning, error, info) → `tokens.color.semantic`
- `typography.font-family-*` → `tokens.typography.families` (sort by role: display, body, utility)
- `typography.font-size-*` → `tokens.typography.scale` (use semantic names: h1, h2, body, label, etc.)
- `typography.font-weight-*` → `tokens.typography.families[role].weights` (array)
- `spacing.*` → `tokens.spacing.tiers` (if unit is consistent, derive base and rhythm)

**Extraction command:**
```
For each category in DTCG JSON:
1. Filter by semantic naming (bg-, text-, size-, weight-, etc.)
2. Extract value and $type
3. Sort by category and semantic intent
4. Derive scale/tiers from multiples if needed
```

### Style Dictionary Config

**Source structure:**
```javascript
module.exports = {
  "platforms": {
    "web": {
      "buildPath": "dist/web/",
      "files": [{"destination": "tokens.css", "format": "css/variables"}]
    }
  },
  "source": ["tokens/**/*.json"],
  "format": {"tokenTypeFilePath": true}
}
```

**Mapping:**
- Read `source` paths for token file locations
- Extract tokens from matched JSON files (same DTCG mapping as above)
- Use `platforms` and `buildPath` to understand deployment targets (web, native, etc.)

**Extraction command:**
```
1. Locate and read files matching source[*] glob
2. Parse JSON; apply DTCG mapping
3. Note output targets from platforms[*].buildPath
```

### Figma Tokens Plugin Export

**Source structure:**
```json
{
  "$themes": [],
  "$metadata": {},
  "colors": {
    "primary": {"value": "#0066FF", "type": "color"},
    "text": {"primary": {"value": "#111111", "type": "color"}}
  }
}
```

**Mapping:**
- Identical to DTCG except nested objects (like `text.primary`) flatten to `text-primary`
- Flatten nested hierarchies before applying DTCG mapping
- Check `$metadata` for color modes (light/dark); if multiple modes exist, note in report

**Extraction command:**
```
1. Flatten nested structure: text.primary → text-primary
2. Apply DTCG mapping
3. If color modes exist, document which mode is the base
```

### Supernova MCP API Response

**Source structure:**
```
Workspace → Token Sets → Token Collections
{
  "tokenSets": [
    {
      "id": "core",
      "name": "Core",
      "tokens": [
        {"name": "colors.primary", "value": "#0066FF", "type": "color"}
      ]
    }
  ]
}
```

**Mapping:**
- Each token set corresponds to a category (colors, typography, spacing, etc.)
- Token names use dot notation: `colors.primary` → flatten to `colors.primary` or map to semantic name
- Query all token sets before extraction (use Supernova API to get full inventory)

**Extraction command:**
```
1. Query Supernova workspace metadata (token sets, last updated)
2. For each token set, extract tokens
3. Map token names to semantic categories (colors.primary → color.accent, etc.)
```

### Inferred From Component Library

When explicit tokens don't exist, scan component code for token/variable references:

```javascript
// In Button.tsx
const styles = {
  padding: "var(--spacing-md)",
  color: "var(--color-text-primary)",
  borderRadius: "var(--radius-sm)"
}
```

**Mapping:**
- Extract CSS variable names: `--spacing-md`, `--color-text-primary`, `--radius-sm`
- Group by category (spacing, color, radius, etc.)
- If values are hardcoded (no variables), infer tokens from the most common values
- Flag as "inferred" in completeness report

---

## 4. Contrast Validation Reference

WCAG AA requires 4.5:1 for normal text, 3:1 for large text (18px+ or 14px+ bold).

### Contrast Ratio Calculation

**Formula:** (L1 + 0.05) / (L2 + 0.05), where L is relative luminance

**Relative luminance (L):**
- For R, G, B in 0-1 range: if RGB ≤ 0.03928 then RGB/12.92, else ((RGB+0.055)/1.055)^2.4
- L = 0.2126*R + 0.7152*G + 0.0722*B

**Practical:** Use a JavaScript library or online calculator rather than manual math.

### Testing Matrix

For each text color token and each background color token, calculate and document:

| Text Color | Background Color | Ratio | Pass? | Notation |
|------------|---|---|---|---|
| primary (dark gray #1a1a1a) | light (#ffffff) | 15.3 | Yes | "primary on light: 15.3:1 ✓" |
| secondary (medium gray #666) | light (#ffffff) | 5.1 | Yes | "secondary on light: 5.1:1 ✓" |
| secondary (medium gray #666) | light-secondary (#f0f0f0) | 2.8 | No | "secondary on light-secondary: 2.8:1 ✗ FAILS AA" |

### Reporting Format

Store results in `tokens.color.contrast_notes` (array of strings):

```json
{
  "tokens": {
    "color": {
      "contrast_notes": [
        "primary text on light bg: 15.3:1 ✓",
        "primary text on dark bg: 14.2:1 ✓",
        "secondary text on light bg: 5.1:1 ✓",
        "secondary text on secondary-light bg: 2.8:1 ✗ FAILS AA. Recommend token adjustment.",
        "All semantic colors (success/warning/error/info) pass AA on both light and dark backgrounds"
      ]
    }
  }
}
```

### Critical Failures to Flag

- Primary text on primary background fails → immediate escalation
- Multiple semantic color pairs fail → blocks deployment
- Large blocks of text rely on contrast < 4.5:1 → UX concern, not just compliance

---

## 5. Component Analysis Levels

### Level 1: Inventory

Scan component directory and extract metadata for each component.

**Fields per component:**

| Field | Example | Notes |
|-------|---------|-------|
| `name` | "Button" | Component file or folder name |
| `path` | "src/components/Button/Button.tsx" | Relative to repo root |
| `category` | "primitive" | primitive, composite, layout, utility, page-level |
| `variants` | ["primary", "secondary", "outline"] | Enum values from props.variant or similar |
| `tokens_used` | ["color-primary", "spacing-md", "radius-sm"] | CSS variable or token names referenced in code |
| `dependencies` | ["Icon", "Spinner"] | Other components imported by this component |

**Inventory template:**

```json
{
  "components": {
    "inventory": [
      {
        "name": "Button",
        "path": "src/components/Button.tsx",
        "category": "primitive",
        "variants": ["primary", "secondary", "outline", "ghost"],
        "tokens_used": ["color-primary", "color-text-primary", "spacing-md", "radius-sm"],
        "dependencies": [],
        "notes": "Core primitive. Used by Modal, Card, and most composites."
      },
      {
        "name": "Card",
        "path": "src/components/Card.tsx",
        "category": "composite",
        "variants": ["elevated", "outlined"],
        "tokens_used": ["color-surface", "elevation-md", "spacing-lg", "radius-md"],
        "dependencies": ["Button"],
        "notes": "Composition of primitives. Elevation applied via shadow tokens."
      }
    ]
  }
}
```

### Level 2: Props and Variants Analysis

For each component, extract prop interface and variant patterns.

**Props template (first 10 props max):**

```typescript
interface ButtonProps {
  variant: "primary" | "secondary" | "outline";
  size: "sm" | "md" | "lg";
  isDisabled: boolean;
  isLoading: boolean;
  onClick: () => void;
  children: React.ReactNode;
}
```

**Store as:**

```json
{
  "components": {
    "inventory": [
      {
        "name": "Button",
        "props": [
          {"name": "variant", "type": "enum: primary|secondary|outline|ghost", "required": true},
          {"name": "size", "type": "enum: sm|md|lg", "required": false},
          {"name": "isDisabled", "type": "boolean", "required": false},
          {"name": "isLoading", "type": "boolean", "required": false},
          {"name": "onClick", "type": "function", "required": false},
          {"name": "children", "type": "node", "required": true}
        ]
      }
    ]
  }
}
```

---

## 6. Voice Extraction Patterns

Extract voice rules from brand documents (PDF, MD, Notion, or summarized by the instance owner).

### Tone (Explicit)

**Look for:**
- Narrative voice descriptions: "Warm, conversational, expert"
- Personality attributes: "Professional yet approachable"
- Implied audience: "speaks to designers, not executives"

**Store as 1-3 sentences:**
```json
{
  "voice": {
    "tone": "Warm, expert, conversational. Sounds like a smart friend who knows the domain. Professional without being corporate."
  }
}
```

### Prohibited Words (Explicit List)

**Look for:**
- Explicit "never use" lists
- Words marked as "cliché," "overused," "banned"
- Corporate jargon to avoid

**Store as array:**
```json
{
  "voice": {
    "prohibited_words": [
      "leverage",
      "unlock",
      "supercharge",
      "disrupt",
      "synergy",
      "stakeholder alignment",
      "cutting-edge",
      "seamless",
      "revolutionary"
    ]
  }
}
```

Also include HeyHi's banned word list (see CLAUDE.md) if building for HeyHi clients.

### Prohibited Patterns (Inferred or Explicit)

**Look for:**
- Voice guidance that names structures to avoid
- Syntax rules: "avoid passive voice," "no double negatives"
- Tone rules: "no corporate jargon," "no overexplanation"

**Store as array:**
```json
{
  "voice": {
    "prohibited_patterns": [
      "passive voice in CTAs",
      "double negatives",
      "overexplanation or hedging",
      "acronyms without explanation",
      "corporate jargon",
      "superlatives without evidence"
    ]
  }
}
```

### CTA Style (Explicit Guidance)

**Look for:**
- How buttons and links should sound
- Verb choice: "Start a conversation" vs. "Get started"
- Level of specificity: generic vs. specific

**Store as 1-2 sentences with example:**
```json
{
  "voice": {
    "cta_style": "Human, specific, and direct. Use strong verbs. Prefer 'Start a conversation' over 'Get started.' Be concrete about what happens next."
  }
}
```

### Formatting Rules (Explicit or Inferred)

**Look for:**
- Title case vs. sentence case preferences
- Separator characters: em dash, comma, period, colon
- List formatting: bullets, numbered, sentences
- Abbreviation style: "e.g." vs. "for example"

**Store as flat key-value pairs:**
```json
{
  "voice": {
    "formatting": {
      "titles": "Title Case",
      "lists": "Sentence case, period at end",
      "separators": "em dash only (maximum 2 per page)",
      "abbreviations": "spell out on first mention",
      "contractions": "preferred (don't, can't, won't)"
    }
  }
}
```

### Terminology (Preferred Terms)

**Look for:**
- Custom vocabulary: words the brand prefers over common alternatives
- Role-specific terms: "team member" instead of "user"
- Brand-specific naming: "workflow" vs. "process"

**Store as key-value mapping (generic → preferred):**
```json
{
  "voice": {
    "terminology": {
      "user": "team member",
      "tool": "platform",
      "feature": "capability",
      "workflow": "process",
      "dashboard": "workspace"
    }
  }
}
```

---

## 7. Troubleshooting Guide

### Connection Issues

| Problem | Root Cause | Solution |
|---------|-----------|----------|
| Supernova workspace empty | Client hasn't populated tokens yet | Escalate to client. Do not proceed with Mode A. Fall back to Mode B (file export) or Mode C (direct input). |
| Git repo not accessible | URL wrong or permissions missing | Verify URL. Check authentication credentials. Fall back to Mode B if access cannot be granted. |
| Figma file has no token plugin installed | Client uses raw Figma design, not structured tokens | Extract manually from Design panel (RGB, sizing, etc.). Flag in completeness as "manual extraction." |

### Extraction Issues

| Problem | Root Cause | Solution |
|---------|-----------|----------|
| Component library uses custom token naming (not DTCG) | Non-standard token format | Document the format in Step 1C. Create a mapping table from custom names to semantic names. Proceed manually through Step 2-3. Flag in report. |
| DTCG JSON has deeply nested structure (5+ levels) | Over-engineered token hierarchy | Flatten before mapping. Example: `color.semantic.interactive.states.hover` → `color-interactive-hover`. Simplify hierarchy for config. |
| Motion tokens are CSS custom properties but no easing values | Easing was never extracted | Ask client for easing names or CSS cubic-bezier values. If unavailable, set `tokens.motion.easing` to empty object and flag as optional gap. |
| No component library exists yet | Client is pre-component or components live in Figma | Skill still runs. Set `components.source` to `null`. Flag in completeness as optional gap. Design-system-ux can work without components. |

### Validation Issues

| Problem | Root Cause | Solution |
|---------|-----------|----------|
| Contrast fails for several color pairs | Color tokens don't meet WCAG AA when combined | Do not block config creation. Document which pairs fail in `contrast_notes`. Flag as Yellow completeness with "Warning: contrast remediation needed." Recommend client adjust affected tokens. |
| `brand.name` is empty or null | Extraction skipped brand definition step | Escalate to client. `brand.name` is required. Do not save config until it's populated. |
| `tokens.typography.scale` is incomplete | Some heading levels missing (e.g., h4, h5, h6) | Flag as Yellow completeness. Typical: client provides h1-h3 but not h4-h6. Ask if smaller heading levels are needed. Infer from scale ratio if not provided. |
| `tokens.spacing` has no clear rhythm | Base unit is unclear or rhythm is inferred | Document in report: "spacing rhythm inferred from observed multiples." Recommend client verify base unit. Mark as Yellow completeness. |

### Report Issues

| Problem | Root Cause | Solution |
|---------|-----------|----------|
| All sections are Red or too many Yellow flags | Extracted data is incomplete or missing critical fields | Reassess input source. If using Mode C (conversational), ask the instance owner to clarify values. If using Mode B (file-based), request additional exports. Do not deploy config in production without at least typography and color Green. |
| Completeness report is too long (10+ gaps) | Too many gaps to address in one session | Prioritize by impact: color and typography are critical; motion and elevation are optional. Recommend a follow-up session for full remediation. Deliver current config as MVP. |

---

## 8. Quick Validation Checklist

Before confirming Step 8 (Write and confirm), verify:

- [ ] Config is valid JSON (no syntax errors)
- [ ] `brand.name` is non-empty string
- [ ] `tokens.typography` exists and has at least one family
- [ ] `tokens.color` exists and has at least backgrounds and text
- [ ] All hex color values match `^#[0-9A-Fa-f]{6}$`
- [ ] All spacing values are valid CSS (px, rem, clamp(), etc.)
- [ ] Type scale values use consistent units (not mixed px and rem)
- [ ] `meta.generated_at` and `meta.last_refreshed` are ISO 8601 timestamps
- [ ] `meta.generated_by` is one of: A, B, C
- [ ] `meta.version` is set to "1.0"
- [ ] Repository section has at least one source (supernova_workspace, token_repo, or component_repo)
- [ ] Completeness report generated and reviewed
- [ ] All Red flags documented (even if optional)
- [ ] Config file written to disk
- [ ] User can read the output file

---

*Design System Onboarding Reference. HeyHi. March 2026.*

*HeyHi Confidential*
