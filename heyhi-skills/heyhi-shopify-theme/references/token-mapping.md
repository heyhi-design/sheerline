---
title: "Token Mapping — active-brand.json → Shopify settings_schema.json"
classification: confidential
session: T-1
version: "1.0.0"
created: "2026-03-29"
---

# Token Mapping

The intellectual center of `heyhi-shopify-theme`. Every active-brand.json token path and its corresponding Shopify setting — with full bidirectional traceability and the complete color_role_map resolution logic.

---

## How to Read This Document

**Forward direction (token → setting):** Given a token path in active-brand.json, find the Shopify setting ID and type it maps to.

**Reverse direction (role → token):** Given a color_scheme_group role ID (e.g., `background`) or setting ID (e.g., `heading_scale`), trace back to the active-brand.json token path that populates it.

**Resolution notation:** Token paths use dot-notation. `[resolved]` indicates a path resolved via `color_role_map` or the fallback priority chain (see Color Role Resolution below).

---

## Color Role Resolution

### The Problem

Active-brand.json color sub-keys vary across configs. Real configs use names like:
- `tokens.color.backgrounds.primary`
- `tokens.color.backgrounds.canvas`
- `tokens.color.backgrounds.base`
- `tokens.color.backgrounds.surface`
- `tokens.color.backgrounds.default`

The color_scheme_group definition uses fixed role IDs: `background`, `text`, `text_2`, `button`, `button_label`, `secondary_button_label`, `shadow`. The mapping from token sub-keys to these roles cannot be hardcoded to `.primary`.

### Resolution Logic (C-3 — hybrid A+B)

**Step 1 — Check for explicit color_role_map**

If `active-brand.json` contains a `color_role_map` block at the root level, use it for exact path resolution:

```json
"color_role_map": {
  "page_background":   "tokens.color.backgrounds.primary",
  "page_background_2": "tokens.color.backgrounds.surface",
  "body_text":         "tokens.color.text.primary",
  "body_text_2":       "tokens.color.text.secondary",
  "accent_1":          "tokens.color.accent.primary",
  "accent_2":          "tokens.color.accent.secondary",
  "button_outline":    "tokens.color.structural.border"
}
```

When `color_role_map` is present, use exact paths. No fallback logic fires. Log: "color_role_map present — using explicit path resolution."

**Step 2 — Fallback priority chain (when color_role_map absent)**

For each color group (`backgrounds`, `text`, `accent`, `structural`), select keys in this order:

| Priority | Key name | Notes |
|----------|----------|-------|
| 1 | `primary` | Most common in principled configs |
| 2 | `default` | Used in some system-generated configs |
| 3 | `base` | Common in design token taxonomies |
| 4 | `main` | Used in some branding frameworks |
| 5 | first key | Alphabetical first key in the object |

For secondary scheme roles (e.g., `background` in scheme-2, `text_2`): apply the same chain to the remaining keys after the primary is resolved. If only one key exists in the group, both the primary and secondary scheme roles receive the same value.

**Step 3 — Log all fallback resolutions as warnings**

Every fallback resolution fires a WARNING in the validator report:

```
WARNING: color_scheme_group role `background` used fallback resolution → tokens.color.backgrounds.[key]
Verify this is the intended color for the page background.
```

The operator must review fallback-resolved settings before Mode A submission.

---

## Complete Token Mapping Table

### Color Settings (via color_scheme_group)

**Architecture:** Colors are NOT individual standalone settings (no `colors_background_1` etc. in settings_schema.json). Instead, all colors are defined within a `color_scheme_group` — a Shopify construct that bundles background + text + accent + button colors into named schemes. Sections reference scheme names (e.g., `"scheme-1"`, `"scheme-dark"`) via a single `color_scheme` setting. This is required for 2026 Theme Store submissions (H-3).

**color_scheme_group definition fields → active-brand.json tokens:**

| Scheme Definition Field | Type | active-brand.json Token Path | Role |
|---|---|---|---|
| `background` | `color` | `tokens.color.backgrounds.[resolved:page_background]` | Scheme background |
| `background_gradient` | `color` | (derived from background — optional gradient) | Background gradient |
| `text` | `color` | `tokens.color.text.[resolved:body_text]` | Body text — must achieve 4.5:1 on background |
| `text_2` | `color` | `tokens.color.text.[resolved:body_text_2]` | Secondary text — captions, metadata |
| `button` | `color` | `tokens.color.accent.[resolved:accent_1]` | Button fill / primary accent |
| `button_label` | `color` | (derived — typically white or background for contrast) | Button text |
| `secondary_button_label` | `color` | `tokens.color.accent.[resolved:accent_2]` | Outline button text |
| `shadow` | `color` | `tokens.color.structural.[resolved:button_outline]` | Shadows and borders |

**How sections access colors:** Via `color_scheme` setting → `{{ section.settings.color_scheme }}` → resolves to the named scheme's colors. NOT via `{{ settings.colors_background_1 }}`.

**Named scheme generation:** Generate 5-8 named schemes from the active-brand.json token set. At minimum: `scheme-1` (light primary), `scheme-2` (accent on dark), `scheme-3` (inverted), `scheme-dark` (dark-native default if `meta.default_scheme: "dark"`).

**Semantic colors (internal only — not merchant-settable):**

| Token Path | CSS Custom Property | Notes |
|---|---|---|
| `tokens.color.semantic.error` | `--color-error` | In base.css only — not in settings |
| `tokens.color.semantic.success` | `--color-success` | In base.css only |
| `tokens.color.semantic.warning` | `--color-warning` | In base.css only |
| `tokens.color.semantic.info` | `--color-info` | In base.css only |

Semantic colors are hardcoded into `assets/base.css` at build time. They are NOT emitted via Liquid in the CSS bridge. Shopify's Liquid runtime has no variables for these — only `settings.*` references belong in the `{% style %}` block.

---

### Typography Settings

| Shopify Setting ID | Shopify Type | active-brand.json Token Path | Settings Schema Config |
|---|---|---|---|
| `type_header_font` | `font_picker` | `tokens.typography.families.display.family` | `default: "assistant_n4"` (style-entry specific) |
| `type_body_font` | `font_picker` | `tokens.typography.families.body.family` | `default: "assistant_n4"` (style-entry specific) |
| `heading_scale` | `range` | `tokens.typography.scale.h1` (converted to percentage) | `min: 100, max: 150, step: 5, unit: %` |
| `body_scale` | `range` | `tokens.typography.scale.body` (converted to percentage) | `min: 100, max: 130, step: 5, unit: %` |

**Scale conversion note:**
Token scale values are CSS values (`clamp(2.5rem, 5vw, 4rem)`). Convert to a percentage scale relative to the base: 100% = default browser size. The schema uses percentage-based scaling (`heading_scale`, `body_scale`), NOT pixel-based individual sizes (`font_size_h1`, etc.). The actual pixel sizes are computed in `base.css` from these percentage scales. Individual heading sizes (h1-h4) are derived from the heading_scale percentage applied to a type ratio in base.css.

**Important:** The workstream plan's original mapping table references `font_size_h1`, `font_size_base` as pixel ranges. The actual schema uses `heading_scale` and `body_scale` as percentages — this is the correct Shopify pattern used by Dawn and Skeleton themes.

**Non-configurable typography (hardcoded in base.css):**

| Token Path | CSS Custom Property |
|---|---|
| `tokens.typography.families.display.fallback` | `--font-heading-fallback` |
| `tokens.typography.families.body.fallback` | `--font-body-fallback` |
| `tokens.typography.families.utility.family` | `--font-utility-family` |
| `tokens.typography.scale.h3` | `--font-size-h3` |
| `tokens.typography.scale.h4` | `--font-size-h4` |
| `tokens.typography.scale.label` | `--font-size-label` |
| `tokens.typography.scale.caption` | `--font-size-caption` |

---

### Spacing Settings

| Shopify Setting ID | Shopify Type | active-brand.json Token Path | Settings Schema Config |
|---|---|---|---|
| `page_width` | `range` | `tokens.spacing.content_max_width` | `min: 1000, max: 1600, step: 100, unit: px` — default: 1440 |
| `spacing_sections` | `range` | `tokens.spacing.grid_gap` or `tokens.spacing.tiers.lg` | `min: 0, max: 100, step: 4, unit: px` — section-to-section gap; default: 0 |

**Spacing architecture note:**
The schema uses two merchant-configurable spacing controls: `page_width` (container max-width, 1000–1600px) and `spacing_sections` (gap between sections, 0–100px). The CSS bridge emits these as `--page-width: {{ settings.page_width }}px` and `--section-gap: {{ settings.spacing_sections }}px`. There is no `spacing_multiplier` setting. The full spacing scale (`--spacing-xs` through `--spacing-3xl`) is hardcoded in `assets/base.css` from token tier values — not derived from a runtime multiplier.

**Non-configurable spacing (hardcoded in base.css):**

| Token Path | CSS Custom Property | Notes |
|---|---|---|
| `tokens.spacing.tiers.xs` | `--spacing-xs` | |
| `tokens.spacing.tiers.sm` | `--spacing-sm` | |
| `tokens.spacing.tiers.md` | `--spacing-md` | |
| `tokens.spacing.tiers.lg` | `--spacing-lg` | |
| `tokens.spacing.tiers.xl` | `--spacing-xl` | |
| `tokens.spacing.tiers.2xl` | `--spacing-2xl` | |
| `tokens.spacing.tiers.3xl` | `--spacing-3xl` | |
| `tokens.spacing.content_max_width` | `--content-max-width` | |
| `tokens.spacing.page_padding` | `--page-padding` | clamp() value |
| `tokens.spacing.grid_gap` | `--grid-gap` | clamp() value |
| `tokens.spacing.touch-target.min` | `--touch-target-min` | Default: 44px |

---

### Radius Settings

| Shopify Setting ID | Shopify Type | active-brand.json Token Path | Settings Schema Config |
|---|---|---|---|
| `buttons_radius` | `range` | `tokens.radius.sm` | `min: 0, max: 40, step: 1, unit: px` |
| `inputs_radius` | `range` | `tokens.radius.md` | `min: 0, max: 40, step: 1, unit: px` |

**Radius extraction note:**
Token values are CSS values (`4px`, `0.5rem`, `9999px`). Extract the numeric pixel value for the Shopify range default. Values in `rem` should be converted to `px` at base font size 16px. Values of `9999px` or `50%` (pill/full-round) map to `max` (40).

**Non-configurable radius (hardcoded in base.css):**

| Token Path | CSS Custom Property |
|---|---|
| `tokens.radius.lg` | `--radius-lg` |
| `tokens.radius.full` | `--radius-full` |

---

### Motion Tokens (all internal — not merchant-settable)

Motion tokens are not exposed as Shopify settings. All motion goes into `assets/base.css`.

| Token Path | CSS Custom Property | Notes |
|---|---|---|
| `tokens.motion.durations.fast` | `--duration-fast` | |
| `tokens.motion.durations.base` | `--duration-base` | |
| `tokens.motion.durations.slow` | `--duration-slow` | |
| `tokens.motion.easing.standard` | `--easing-standard` | |
| `tokens.motion.easing.enter` | `--easing-enter` | |
| `tokens.motion.easing.exit` | `--easing-exit` | |

**prefers-reduced-motion:** All motion CSS in `base.css` and section CSS must include:
```css
@media (prefers-reduced-motion: reduce) {
  /* reset transitions / animations */
}
```

---

### Focus Tokens (internal — critical for WCAG)

| Token Path | CSS Custom Property | Implementation |
|---|---|---|
| `tokens.focus.outline.width` | `--focus-width` | Used in `:focus-visible` in base.css |
| `tokens.focus.outline.color` | `--focus-color` | Must achieve 3:1 contrast against adjacent background |
| `tokens.focus.outline.offset` | `--focus-offset` | Recommended: 2px |
| `tokens.focus.outline.style` | `--focus-style` | Typically `solid` or `auto` |

---

### Meta Tokens (not emitted to CSS or settings)

These active-brand.json fields inform generation decisions but are not emitted as settings or CSS:

| active-brand.json Field | How it's used | Emitted? |
|---|---|---|
| `brand.style_entry` | Informs preset naming in `theme-config.json` | No |
| `brand.cluster` | Selects cluster architecture for section generation | No |
| `layout.spacing_density` | Drives default section padding tiers | No — informs CSS calculations |
| `meta.default_scheme` | Selects dark/light build foundation | No — drives scheme selection |
| `meta.provisional_fields` | Flags provisional values in validator report | No — documentation only |
| `meta.gate_status.*` | Gate check inputs | No |

---

## Bidirectional Traceability

### Given a Shopify setting ID, find the token

| Shopify Setting | → active-brand.json Token Path |
|---|---|
| `color_schemes` (group) | `tokens.color.backgrounds.*`, `tokens.color.text.*`, `tokens.color.accent.*`, `tokens.color.structural.*` — via color_role_map or fallback |
| `color_schemes.[scheme].background` | `tokens.color.backgrounds.[resolved:page_background]` |
| `color_schemes.[scheme].text` | `tokens.color.text.[resolved:body_text]` |
| `color_schemes.[scheme].button` | `tokens.color.accent.[resolved:accent_1]` |
| `type_header_font` | `tokens.typography.families.display.family` |
| `type_body_font` | `tokens.typography.families.body.family` |
| `heading_scale` | `tokens.typography.scale.h1` (converted to percentage) |
| `body_scale` | `tokens.typography.scale.body` (converted to percentage) |
| `spacing_sections` | `tokens.spacing.base` (derived section spacing) |
| `page_width` | `tokens.spacing.content_max_width` (px value) |
| `buttons_radius` | `tokens.radius.sm` (px value) |
| `inputs_radius` | `tokens.radius.md` (px value) |

### Given a token path, find the Shopify setting

| active-brand.json Token Path | → Shopify Setting (type) |
|---|---|
| `tokens.color.backgrounds.*` | `color_schemes` group → `background` field in each named scheme |
| `tokens.color.text.*` | `color_schemes` group → `text` / `text_2` fields in each named scheme |
| `tokens.color.accent.*` | `color_schemes` group → `button` / `secondary_button_label` fields |
| `tokens.color.structural.*` | `color_schemes` group → `shadow` field |
| `tokens.color.semantic.*` | CSS custom property in `base.css` only — no Shopify setting |
| `tokens.typography.families.display.family` | `type_header_font` (font_picker) |
| `tokens.typography.families.body.family` | `type_body_font` (font_picker) |
| `tokens.typography.scale.h1` | `heading_scale` (range, %) |
| `tokens.typography.scale.body` | `body_scale` (range, %) |
| `tokens.typography.scale.h2/h3/h4/label/caption` | CSS custom property in `base.css` only — derived from heading_scale |
| `tokens.spacing.content_max_width` | `page_width` (range, px) |
| `tokens.spacing.grid_gap` | `spacing_sections` (range, px) |
| `tokens.spacing.base` | CSS custom property in `base.css` only |
| `tokens.spacing.tiers.*` | CSS custom property in `base.css` only |
| `tokens.radius.sm` | `buttons_radius` (range) |
| `tokens.radius.md` | `inputs_radius` (range) |
| `tokens.radius.lg/full` | CSS custom property in `base.css` only |
| `tokens.motion.*` | CSS custom property in `base.css` only — no Shopify setting |
| `tokens.focus.*` | CSS custom property in `base.css` only |

---

## color_role_map Schema

The `color_role_map` block is an optional extension to `active-brand.json`. Generate it during `heyhi-shopify-theme` setup when the config's color sub-keys are non-standard:

```json
"color_role_map": {
  "page_background":   "tokens.color.backgrounds.[key]",
  "page_background_2": "tokens.color.backgrounds.[key]",
  "body_text":         "tokens.color.text.[key]",
  "body_text_2":       "tokens.color.text.[key]",
  "accent_1":          "tokens.color.accent.[key]",
  "accent_2":          "tokens.color.accent.[key]",
  "button_outline":    "tokens.color.structural.[key]"
}
```

**When to generate a color_role_map:**
- Config uses non-standard sub-keys (not `primary`, `default`, `base`, `main`)
- Multiple tokens could plausibly fill a role and the automatic selection is ambiguous
- Dark-native config where `tokens.color.schemes.dark.*` sub-keys need explicit mapping

**How to propose it:**
When the operator runs heyhi-shopify-theme for the first time against a config without a `color_role_map`, inspect the color sub-keys, propose the mapping, and ask:

> "Your config uses custom color key names. I've proposed this color role mapping — confirm or adjust before I generate settings_schema.json:
>
> - Page background: tokens.color.backgrounds.[key] = [value]
> - Page background 2: tokens.color.backgrounds.[key] = [value]
> - Body text: tokens.color.text.[key] = [value]
> [...]"

After confirmation, write the `color_role_map` block into `active-brand.json`.

---

## Extraction Notes for Specific Token Types

### clamp() values
Many token scale values use CSS `clamp(min, preferred, max)`. For Shopify range settings, extract the **max** value (desktop size). The range setting represents the merchant's ability to scale the value — the max is the designed intent.

Example: `tokens.typography.scale.h1: "clamp(2.5rem, 5vw, 4rem)"` → `heading_scale` default: `100` (base scale; the fluid heading size is hardcoded in `assets/base.css` from this token value, not emitted via a range setting).

### rem values
Convert to px at base 16px. `1rem = 16px`, `0.5rem = 8px`, `2rem = 32px`.

### Percentage radius
`50%` = full round. Map to `buttons_radius: 40` (range max). Note in the validator report: "buttons_radius set to maximum (40px) — original token was 50% (fully rounded)."

### Shopify font format
`type_header_font` default uses Shopify's font naming convention: `"[font_family]_n[weight]"`. Examples:
- `"barlow_condensed_n9"` = Barlow Condensed, weight 900
- `"inter_n4"` = Inter, weight 400
- `"playfair_display_n7"` = Playfair Display, weight 700

Match the config's font family name to the Shopify font identifier. When the exact font isn't in Shopify's library, use the closest available alternative and log a warning.

---

*HeyHi Confidential — Session T-1. The authoritative token-to-settings reference for the theme workstream.*
