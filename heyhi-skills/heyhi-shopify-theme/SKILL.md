---
name: heyhi-shopify-theme
description: >-
  Generates a complete Shopify theme directory from active-brand.json + theme-config.json.
  Three modes: A (Theme Store submission — full 23+ feature set, validator pass required),
  B (Client Custom — complete sections, relaxed submission requirements), C (Section — single
  section for an existing theme). Reads active-brand.json exclusively. Requires direction lock
  confirmed. Mirrors ui-studio gate structure, PROVISIONAL handling, and dark-native logic.
  Triggers: "generate a Shopify theme", "build a theme for [client]", "Mode A theme build",
  "create a section for [theme]", "Shopify theme from brand config". NOT for validating themes
  (use heyhi-theme-validator). NOT for extracting configs from existing themes (use
  heyhi-shopify-onboard — planned, not built; see CANDIDATES.md). NOT for HTML/CSS
  prototypes (use ui-studio).
version: "1.1.0"
depends_on:
  - heyhi-skills/ui-studio/brand-config/schema.json
  - heyhi-skills/heyhi-theme-validator/SKILL.md
  - heyhi-skills/heyhi-shopify-theme/references/token-mapping.md
  - heyhi-skills/heyhi-shopify-theme/references/section-patterns.md
  - heyhi-skills/heyhi-shopify-theme/references/required-features.md
  - heyhi-skills/heyhi-shopify-theme/templates/settings_schema-base.json
  - heyhi-skills/heyhi-shopify-theme/templates/theme-config-schema.json
  - heyhi-skills/heyhi-shopify-theme/templates/css-bridge-template.liquid
---

# HeyHi Shopify Theme

Generate complete Shopify themes from a principled token architecture — not from copying existing themes.

---

> **Exit Gate (Flavor A).** This skill closes through the canonical Exit Gate — see `CLAUDE-SESSION-RULES.md § Exit Gate`. Required headers, in order: `## Fixes Applied`, `## Smoke Test`, `## Next Session Prompt`. Empty headers are visible failures.


## ZONE 1 — Always Loaded

*Complete operating contract for every heyhi-shopify-theme session. ≤2,400 tokens.*

---

### Hard Stop: Missing Inputs

If `active-brand.json` does not exist at the expected path:

**Stop. Do not build.** Say exactly:

> "No brand config found. Run `ui-studio-onboard` to generate one, or activate an existing config with `python3 scripts/switch-brand.py --config [name]`. Theme build cannot proceed without a config."

If `theme-config.json` does not exist (Mode A and B only — not required for Mode C):

**Stop.** Say exactly:

> "No theme-config.json found. Create one using the schema at `heyhi-skills/heyhi-shopify-theme/templates/theme-config-schema.json`. Mode A and B theme builds require a theme-config.json."

---

### Config Validation

On every session start, read `active-brand.json` and check in this order:

**Gate 0 — Direction lock:**
Read `meta.gate_status.direction_lock_confirmed`.

- **Mode A (Theme Store):** If `false` or absent — **hard stop.** Say exactly: *"Gate 0 not confirmed: direction_lock_confirmed is false. Mode A theme builds are blocked. Run design-system-onboard Mode D to confirm the style cluster and primary direction, then set gate_status.direction_lock_confirmed: true."*
- **Mode B (Client Custom):** Proceed with warning logged to the validator report: *"direction_lock_confirmed is false — this build uses unconfirmed design direction. Designer review required before delivery."*
- **Mode C (Section):** No gate check required.

If `meta.gate_status` block is absent entirely (pre-G2 config), treat as `direction_lock_confirmed: false` — apply the appropriate mode rule above.

**Designer review:**
Read `meta.gate_status.designer_review_complete`.

- **Mode A (Theme Store):** If `false` or absent — surface a warning (not a hard stop): *"Designer review not complete. Token values have not been verified against the source design file. Mode A Theme Store output may not match the actual design. This must be documented in the validator report and acknowledged before submission."*
- **Mode B / Mode C:** No gate check required. Log as informational if false.

**Gate 1 — Dual-score unlock:**
Read both `meta.completeness_score` and `meta.fidelity_score` and apply this matrix:

| Completeness | Fidelity | Mode A | Mode B | Mode C |
|---|---|---|---|---|
| < 30 | any | HARD STOP | HARD STOP | HARD STOP |
| 30–49 | any | BLOCKED | Proceed with degradation notice | Proceed |
| 50–69 | any | Requires explicit confirmation (see SI-03) | Proceed | Proceed |
| ≥ 70 | < 60 | BLOCKED — fidelity too low | Proceed with warning | Proceed |
| ≥ 70 | ≥ 60 | PARTIAL_A — Mode A with documented approximations | Proceed | Proceed |
| ≥ 90 | ≥ 60 | FULL — Mode A fully unlocked | Proceed | Proceed |

**SI-03 — Mode A override gate (50–69 completeness):** Surface the score and ask:

> "Completeness score is [N]/100. Mode A at this score produces approximated output — token values are directional estimates that may not match the actual design. Would you like to proceed with Mode A (and document this as provisional output), or switch to Mode B?"

Only proceed with Mode A if the user explicitly confirms. On confirmation, set `gate_status.mode_override_acknowledged: true` and record the score in `gate_status.mode_override_score`.

**Gate 2 — Version check:**
If `meta.version` is `0.x.y` (provisional) — surface once: *"Config is provisional (v[version]). Mode A output will be built on unconfirmed tokens. Run `ui-studio-onboard --refresh [config-name]` after the designer confirms values to promote to v1."* Then continue.

**Gate 3 — Freshness:**
If `meta.last_refreshed` is > 30 days ago — surface a warning (not a blocker): *"Config was last refreshed [date]. Consider running a refresh if the design system has changed."*

**Gate 4 — Scheme detection:**
Read `meta.default_scheme`. Log the result before proceeding. `"dark"` triggers dark-native build rules (see Dark-Native Handling below).

---

### Three Modes

**Mode A — Theme Store**
Full Shopify Theme Store submission quality.

- All 23+ required features implemented (no exceptions)
- Lighthouse targets: Performance ≥ 60, Accessibility ≥ 90
- heyhi-theme-validator (all 3 profiles) must PASS before delivery
- Requires: completeness ≥ 70 AND fidelity ≥ 60 AND direction_lock_confirmed: true
- Output: complete theme directory + validator report + settings_schema.json + settings_data.json

**Mode B — Client Custom**
Merchant-specific Shopify work. Complete sections required; Theme Store submission requirements relaxed.

- Complete sections with correct Shopify schema structure
- heyhi-theme-validator Profile 2 (code standards) blocking; Profile 1 warnings acceptable for optional features
- Direction lock warning if unconfirmed (not a hard stop)
- Output: theme directory + handoff document

**Mode C — Section**
Single Liquid section for an existing merchant theme.

- One section file + CSS + schema
- heyhi-theme-validator Profile 2 (section-scoped) + Profile 3 (section markup only)
- No direction lock gate
- Output: section.liquid + component CSS + brief implementation notes

| | Mode A | Mode B | Mode C |
|---|---|---|---|
| Direction lock | Required (hard stop if false) | Warning if false | Not required |
| Feature completeness | All 23+ required | Core required, optional = warnings | N/A (section scope) |
| Validator profiles | All 3 required, PASS | Profile 2 blocking, 1 + 3 = warnings | Profile 2 + 3 (section-scoped) |
| Lighthouse | Perf ≥ 60 / Access ≥ 90 | Not required | Not required |
| Completeness score | ≥ 70 required | 50+ recommended | 30+ usable |
| Fidelity score | ≥ 60 required | 40+ recommended | Not gated |

---

### PROVISIONAL Prefix Handling

Before emitting any token value to `settings_data.json`, CSS output, or any Liquid template:

1. **Detect** the `PROVISIONAL:` prefix on any string value in `active-brand.json`
2. **Strip** the prefix — use only the value after the colon as the provisional default
3. **Log** all provisional fields in the validator report under a "PROVISIONAL VALUES" section, listing each affected setting with its token path
4. **Flag** the delivery as: *"PROVISIONAL OUTPUT — designer review required before submission."*

A provisional field is a warning, not a hard stop. Mode A builds may proceed with provisional tokens if the operator acknowledges. Mode A submissions to Shopify Theme Store require designer review of all provisional fields before submission.

---

### Dark-Native Config Handling

**Detecting the scheme:** Read `meta.default_scheme` during Gate 4.

- `"light"` or absent → standard light-baseline build
- `"dark"` → dark-native build. Apply all rules below.

**Dark-native build rules:**
1. **Primary color scheme:** Use `tokens.color.schemes.dark` values as the primary color scheme in `color_scheme_group` (see Section Schema Pattern in Zone 2). Set `color_scheme: "scheme-dark"` as the default in `settings_data.json`.
2. **Light scheme:** Use `tokens.color.schemes.light` if present; emit a warning if absent and derive a light adaptation.
3. **CSS bridge:** The `:root` defaults in the CSS bridge emit dark-scheme values.
4. **Contrast checks:** WCAG verification runs against dark background tokens, not white.
5. **No guessing:** Never construct a light scheme by inverting dark token values without surfacing:

> ⚠ Provisional: color values checked against light backgrounds only. This config is dark-native (`meta.default_scheme: dark`). Light-scheme output is an adaptation and has not been verified against the source design.

---

### Workflow — 13 Steps

**Generation order is mandatory.** Settings schema before sections (sections reference `settings.*` variables that must be defined). Snippets before sections (sections include snippets). Templates last (reference sections).

```
Step 1  — Read inputs
Step 2  — Validate config (Gates 0–4 above)
Step 3  — Resolve token paths (color_role_map or fallback)
Step 4  — Generate config/settings_schema.json
Step 5  — Generate config/settings_data.json
Step 6  — Generate layout/theme.liquid (CSS bridge + font loading)
Step 7  — Generate assets/base.css (non-settings token layer)
Step 8  — Generate snippet library (13 required snippets)
Step 9  — Generate section library (20 required sections, cluster-appropriate)
Step 10 — Generate template files (11 JSON + gift_card.liquid + customer account .liquid files)
Step 11 — Generate locales/en.default.json
Step 12 — Run heyhi-theme-validator (all 3 profiles — fix before declaring complete)
Step 13 — Produce theme directory + validator report
```

**Step 1 — Read inputs**
Read `active-brand.json` in full. Read `theme-config.json`. Extract:
- `brand.cluster` — drives section architecture selection
- `brand.style_entry` — informs preset naming
- `layout.spacing_density` — drives section padding defaults
- `meta.default_scheme` — dark/light build foundation
- `meta.gate_status` — all gate checks
- `meta.provisional_fields` — fields needing PROVISIONAL handling
- `color_role_map` block if present

**Step 2 — Validate config**
Run all four gates. Do not proceed to Step 3 if any hard stop fires.

**Step 3 — Resolve token paths**
For each color role, resolve the source token path using this priority order:
1. `color_role_map` block (explicit path — use this if present)
2. Key named `primary` within the relevant sub-object
3. Key named `default`
4. Key named `base`
5. Key named `main`
6. First key in the object (alphabetically)

Log every fallback resolution as a WARNING in the validator report: "Setting [id] used fallback resolution from [object].[key] — verify this is the intended color."

See `references/token-mapping.md` for the complete role-to-path resolution table.

**Step 4 — Generate settings_schema.json**
Start from `templates/settings_schema-base.json`. Customize:
- Populate `theme_info` with values from `theme-config.json` (name, version, author, documentation_url)
- Map resolved token paths to their Shopify setting IDs per the token mapping table
- Add color_scheme_group with schemes derived from the brand token architecture
- For dark-native configs, set the primary scheme to `scheme-dark`
- Localize all labels through `en.default.schema.json`

**Step 5 — Generate settings_data.json**
For every setting in `settings_schema.json`, populate a default value from the resolved token:
- Colors: use the hex/RGB value from the resolved token path
- Fonts: use the font family name (Shopify font picker format)
- Ranges: convert token values to the integer/float the range expects (e.g., `8px` → `8`)
- Provisional tokens: strip prefix, use value, log warning

> **⚠ Font Picker Gate (hard check before writing).** Shopify's font picker registry is a curated subset of Google Fonts — it is NOT the same set. Many Google Fonts families (including Cormorant Garamond) have no valid Shopify picker handle. Before writing any `type_header_font` or `type_body_font` value to `settings_data.json`, verify the exact handle exists in Shopify's registry. Do NOT derive picker handles from Google Fonts family names — the registries differ. If the brand typeface has no Shopify picker handle, use the two-track architecture: (1) Google Fonts CDN preload + hardcoded `font-family` in `base.css` for actual delivery; (2) a known-valid Shopify registry handle (e.g., `libre_baskerville_n4`) in the picker slot as a CSS fallback only. Document this split in the validator report. *Promoted from corrections-registry.yaml `shopify-font-picker-registry-limitation` (2026-04-22).*

**Step 6 — Generate layout/theme.liquid**
Use `templates/css-bridge-template.liquid` as the base. Customize:
- Merchant-configurable tokens: emit as `{{ settings.[id] }}` references
- Non-configurable tokens (semantic colors, spacing, motion): do NOT emit via Liquid — these go in base.css (Step 7)
- Font loading: use `{{ settings.type_header_font | font_face }}` + `{{ settings.type_body_font | font_face }}`
- For dark-native: emit dark-scheme values as the `:root` defaults
- Include `<html lang="{{ request.locale.iso_code }}">` — required
- Include skip navigation link targeting `#MainContent`
- Include `page_image` meta tag for social sharing (F-07)
- Include `login_button` filter output for Follow on Shop (F-19)

**Step 7 — Generate assets/base.css**
Emit all non-merchant-settable tokens as hardcoded CSS custom properties:
- Semantic colors: `--color-error`, `--color-success`, `--color-warning`
- Spacing scale: `--spacing-xs` through `--spacing-3xl` from `tokens.spacing.tiers`
- Motion tokens: `--duration-fast`, `--duration-base`, `--easing-standard`
- Focus styles: `:focus-visible` for `a`, `button`, `input`, `select`, `textarea`
- Touch target minimums: `min-height: 44px; min-width: 44px` on `.button`, `.link`
- Heading hierarchy: distinct `font-size` / `font-weight` for `h1` through `h4`
- Typography foundation: CSS vars for `--font-heading-*`, `--font-body-*` derived from `--` prefixed settings

**Step 8 — Generate snippet library**

Generate all 14 required snippets (the table below is the authoritative count). Each snippet must have semantic HTML, ARIA where needed, mobile-first CSS using CSS custom properties, and accessibility baked in.

| Snippet | Key requirements |
|---------|-----------------|
| `product-media-gallery.liquid` | Handles `model` + `video` + `image` media types; focal_point attribute |
| `product-thumbnail.liquid` | Used in collections/search; lazy loading; alt attribute pattern |
| `price.liquid` | Unit pricing with `unit_price_measurement`; compare-at; selling plan price |
| `variant-picker.liquid` | Radio + select variants; triggers media gallery swap via JS |
| `cart-drawer.liquid` | Side cart (optional but expected); accessible close button |
| `quantity-input.liquid` | Stepper with `aria-label`; min/max validation |
| `icon-*.liquid` | Cart, search, hamburger, close — all with `aria-hidden="true"` when decorative |
| `breadcrumbs.liquid` | `<nav aria-label="Breadcrumb">` with structured markup |
| `pagination.liquid` | `<nav aria-label="Pagination">` with prev/next |
| `social-sharing.liquid` | Social share links with `rel="nofollow"` |
| `facets.liquid` | Filter sidebar/drawer; keyboard accessible |
| `predictive-search.liquid` | `/search/suggest` API; ARIA live region |
| `header-drawer.liquid` | Mobile navigation; focus trap on open |
| `country-localization.liquid` | Multi-currency/language selector |

**Step 9 — Generate section library**

Generate all 20 required sections. Apply cluster-derived architecture to every section (not just visual tokens — the structural HTML differs by cluster). See `references/section-patterns.md` for full cluster rules.

Every section must include:
- Valid `{% schema %}` with `name`, `tag`, `class`, `settings[]`, `blocks[]` (where applicable), `presets[]`
- `color_scheme` setting of type `color_scheme` referencing the `color_scheme_group`
- Mobile-first CSS at 375px / 768px / 1440px breakpoints
- Semantic HTML: `<section>`, `<article>`, `<nav>`, `<header>`, `<footer>` — no `<div>` soup
- ARIA labels on icon-only interactive elements
- Visible focus states via CSS custom properties from `base.css`
- `alt="{{ image.alt | escape }}"` on all `<img>` tags
- All form `<input>` elements have `id` and matching `<label for="[id]">`

**Generation priority order (blocked on prior completion):**

*Priority 1 — required for template assembly:*
1. `header.liquid` — navigation (multi-level), logo, cart, search, language/currency
2. `footer.liquid` — links, newsletter, social icons, payment icons
3. `main-product.liquid` — full product feature surface (see required-features.md for complete list)
4. `main-collection.liquid` — grid/list, facets, sort, pagination
5. `main-cart.liquid` — line items, discounts, selling plans, checkout

*Priority 2 — required for homepage:*
6. `hero-banner.liquid` — cluster-appropriate hero structure
7. `featured-collection.liquid` — product grid from selected collection
8. `image-with-text.liquid` — split layout section

*Priority 3 — required features:*
9. `main-search.liquid` — search results with predictive
10. `main-blog.liquid` — blog listing with pagination
11. `main-article.liquid` — post with comments
12. `newsletter.liquid` — email signup with `form_type: 'customer'`
13. `custom-liquid.liquid` — custom liquid section with `type: liquid` input
14. `video.liquid` — embedded video section

*Priority 4 — polish + demo store:*
15. `slideshow.liquid` — multi-image carousel
16. `rich-text.liquid` — editorial text block
17. `testimonials.liquid` — social proof section
18. `multicolumn.liquid` — feature grid
19. `contact-form.liquid` — contact page section
20. `apps.liquid` — app block insertion points

**Step 10 — Generate template files**

Generate all required templates. JSON templates use Sections Everywhere (OS 2.0) — all `.json` except `gift_card.liquid` and `customers/*.liquid`.

*Required JSON templates (11 — validator F-22 checks these):*
`index.json`, `product.json`, `collection.json`, `search.json`, `cart.json`, `blog.json`, `article.json`, `page.json`, `password.json`, `404.json`, `list-collections.json`

*Recommended additional JSON templates (3 — not required by validator but expected for full theme):*
`product.preorder.json`, `collection.with-sidebar.json`, `page.contact.json`

*Required Liquid templates (not JSON — customer system does not support OS 2.0):*
`customers/login.liquid`, `customers/register.liquid`, `customers/account.liquid`, `customers/order.liquid`, `customers/addresses.liquid`, `customers/reset_password.liquid`, `templates/gift_card.liquid`

*Multi-preset themes:* If `theme-config.json` defines more than one preset, generate the `listings/` directory with one subdirectory per preset containing a preset-specific `templates/index.json`.

**Step 11 — Generate locales/en.default.json**

All merchant-facing strings must be in locales. No hardcoded UI strings in Liquid templates. Include:
- Section names, setting labels, block names
- Commerce strings: "Add to cart", "Quantity", "Discount code", etc.
- Accessibility strings: aria-label values, skip link text
- Error/empty state messages
- All strings from snippets

Also generate `locales/en.default.schema.json` for settings_schema labels.

**Step 12 — Run heyhi-theme-validator**

Run all three validation profiles before declaring the build complete. Fix all blocking failures before proceeding to Step 13. Do not proceed to delivery on any Mode A blocking failure.

For each Profile 1 FAIL: return to the relevant section/snippet/template and remediate before continuing.
For each Profile 2 FAIL: fix the code standard violation.
For each Profile 3 FAIL: fix the accessibility issue — these are hard gates in all modes.

**Step 13 — Deliver**

Mode A: complete theme directory + validator report
Mode B: theme directory + handoff document (sections used, token mapping summary, color scheme names)
Mode C: section.liquid + component CSS + brief implementation notes

---

### Section Schema Pattern

Every section follows this schema structure. The `color_scheme` setting type (not a raw `color` picker) is mandatory for Theme Store submissions:

```liquid
{% schema %}
{
  "name": "[Section Name]",
  "tag": "section",
  "class": "section-[kebab-name]",
  "settings": [
    {
      "type": "header",
      "content": "Layout"
    },
    {
      "type": "color_scheme",
      "id": "color_scheme",
      "label": "t:sections.[section-id].settings.color_scheme.label",
      "default": "scheme-1"
    }
  ],
  "blocks": [],
  "presets": [
    {
      "name": "t:sections.[section-id].presets.[preset-name].name"
    }
  ]
}
{% endschema %}
```

**color_scheme_group architecture (H-3):**
The `color_scheme_group` in `settings_schema.json` defines 5–8 named schemes (each with background, text, accent, button colors derived from the token architecture). Sections reference scheme names — they do not define raw colors. Dark-native configs set `scheme-dark` as the default scheme in `settings_data.json`.

---

## Liquid Syntax Constraints — Read before generating any Liquid

Shopify's Liquid parser is stricter than the generic Liquid spec in three specific positions.
These rules are non-negotiable. Violating them produces runtime errors that render sections
as raw error text in the storefront.

---

### Rule 1 — No filter pipelines inside `{% %}` tag named parameters

**Applies to:** `form`, `render`, `paginate`, `video_tag` (block tag form), and all `{% %}` tags.

WRONG:
```liquid
{%- form 'product', product, id: 'ProductForm-' | append: section.id -%}
{%- render 'image-snippet', id_prefix: 'Item-' | append: item.id -%}
```

RIGHT:
```liquid
{%- assign product_form_id = 'ProductForm-' | append: section.id -%}
{%- form 'product', product, id: product_form_id -%}

{%- assign item_id_prefix = 'Item-' | append: item.id -%}
{%- render 'image-snippet', id_prefix: item_id_prefix -%}
```

**The rule:** Assign first. Reference a clean variable name in the tag parameter. Never pipe inside `{% %}` named params.

---

### Rule 2 — No filter pipelines in `{{ output | filter: named_params }}` when followed by a comma

**Applies to:** `image_tag`, `video_tag` (filter form), `external_video_tag`, and any output filter that accepts named parameters.

WRONG:
```liquid
{{ image | image_tag: alt: image.alt | default: '' | escape, style: focal_point }}
```

RIGHT:
```liquid
{%- assign img_alt = image.alt | default: '' | escape -%}
{{ image | image_tag: alt: img_alt, style: focal_point }}
```

**The rule:** Any named parameter value that uses `| default:` or `| escape` (or any filter) must be pre-assigned when additional named parameters follow it. Apply this proactively — even if the filter-chained value is the LAST parameter today, pre-assign it anyway. A future parameter addition would silently break the file.

---

### Rule 3 — `ternary` is not a Shopify Liquid filter

**Applies to:** Any conditional value used in template attributes or tag parameters.

WRONG:
```liquid
aria-live="{{ autoplay | ternary: 'off', 'polite' }}"
loading: forloop.first | ternary: 'eager', 'lazy',
```

RIGHT:
```liquid
{%- if autoplay -%}
  {%- assign aria_live_value = 'off' -%}
{%- else -%}
  {%- assign aria_live_value = 'polite' -%}
{%- endif -%}
<div aria-live="{{ aria_live_value }}">

{%- if forloop.first -%}
  {%- assign slide_loading = 'eager' -%}
{%- else -%}
  {%- assign slide_loading = 'lazy' -%}
{%- endif -%}
```

**The rule:** Shopify Liquid has no `ternary` filter. It also lacks `compact` (in output context) and several other filters from non-Shopify Liquid forks. All conditional values must be produced via `{% if %}` + pre-assign before use.

---

### Non-existent filters — reference list

Never generate these — they do not exist in Shopify's Liquid implementation:

- `ternary` — use `{% if %}` + pre-assign
- `compact` — not available in output context
- `dig` — not a Shopify filter
- Any filter from Nunjucks, Twig, or generic Ruby Liquid that isn't listed in Shopify's Liquid reference

When unsure whether a filter exists: check https://shopify.dev/docs/api/liquid/filters before generating.

---

### Quality Checklist

Before declaring any build complete, verify all items:

**Token fidelity:**
- [ ] Every color in `settings_data.json` traces back to a resolved token path
- [ ] No arbitrary hex values in CSS — all colors use `var(--color-*)` from the bridge layer
- [ ] PROVISIONAL fields listed in validator report; delivery flagged if any present
- [ ] All fallback resolutions logged as warnings

**Shopify compliance:**
- [ ] All JSON templates present (11 required + 3 recommended alternates + `templates/gift_card.liquid` + `customers/*.liquid` — see Step 10)
- [ ] All 23+ required features implemented (run Profile 1 to verify)
- [ ] `color_scheme` setting type used (not raw `color` picker) in all sections
- [ ] No `.scss` files; no minified CSS/JS; no hardcoded `http://` URLs
- [ ] `routes.*` used for all internal path references
- [ ] `theme_info` block present in `settings_schema.json`
- [ ] `favicon` setting present in `settings_schema.json`
- [ ] `<html lang="{{ request.locale.iso_code }}">` in `theme.liquid`

**Accessibility (hard gate — all modes):**
- [ ] Skip navigation link in `theme.liquid` targeting `#MainContent`
- [ ] `:focus-visible` styles in `base.css`
- [ ] All image alt attributes pre-assigned via variable before `image_tag` call (e.g. `{%- assign img_alt = image.alt | default: '' | escape -%}` then `alt: img_alt`) — see Liquid Syntax Constraints above
- [ ] All form inputs have `id` + matching `<label for>`
- [ ] `min-height: 44px` on all buttons and links
- [ ] WCAG 4.5:1 contrast for body text verified against token pairs
- [ ] WCAG 3:1 contrast for heading text verified
- [ ] ARIA labels on all icon-only interactive elements

**Cluster architecture:**
- [ ] Section structure matches the active cluster's architectural signature
- [ ] Spacing density from `layout.spacing_density` applied to section padding
- [ ] Typography hierarchy reflects cluster character

**Pre-push lint (mandatory — run before every `shopify theme push`):**

From the theme root directory, run all three checks. Any match = stop, fix, re-run.

```bash
# RC1: filter pipelines inside {% form/render/paginate/video_tag %} named params
grep -rn "{%-\?\s*\(form\|render\|paginate\|video_tag\)\b.*:.*|" sections/ snippets/ layout/

# RC2a: alt filter chains with trailing comma in output named params
grep -rn "alt:.*|.*escape," sections/ snippets/

# RC2b: default filter chains with trailing comma in output named params
grep -rn "alt:.*|.*default.*," sections/ snippets/

# RC3: non-existent ternary filter
grep -rn "| ternary" sections/ snippets/ layout/
```

All four commands must return zero matches before pushing. If any match is found:
1. Open the matching file at the matching line
2. Apply the pre-assign pattern (see Liquid Syntax Constraints above)
3. Re-run the grep checks
4. Push only when all four are clean

**Validator gate:**
- [ ] heyhi-theme-validator run (all 3 profiles for Mode A)
- [ ] Zero blocking failures before delivery

---

## ZONE 2 — Context Loading

*Load only what the task requires.*

### Always Load (every build)

| Reference | When |
|---|---|
| `references/token-mapping.md` | Step 3 (token resolution) and Step 4 (settings_schema generation) — required |
| `references/section-patterns.md` | Step 9 (section generation) — required for cluster architecture |

### Task-Conditional

| Reference | When |
|---|---|
| `references/required-features.md` | Step 9 when building Priority 1/2 sections (main-product.liquid especially), Step 12 when running Profile 1 validation |
| `references/shopify-liquid-constraints.md` | When debugging Liquid runtime errors, reviewing generated theme code for parser violations, or running the pre-push lint |
| `templates/settings_schema-base.json` | Step 4 (customize this into the final settings_schema.json) |
| `templates/css-bridge-template.liquid` | Step 6 (customize this into layout/theme.liquid) |
| `templates/theme-config-schema.json` | When operator needs to create a theme-config.json from scratch |
| `heyhi-theme-validator/SKILL.md` | Step 12 (run validator) |

### Connecting to Other Skills

| Concern | Skill | When |
|---|---|---|
| Brand config generation | `ui-studio-onboard` | No config exists or needs refresh |
| Config pipeline validation | `heyhi-pipeline-validator` | Verify style entry passes pipeline before building |
| Post-build validation | `heyhi-theme-validator` | Step 12 — required before Mode A delivery |
| Extracting config from existing theme | `heyhi-shopify-onboard` (planned, not built — see CANDIDATES.md) | Client has existing Shopify theme to extract from |
| Client engagement design system care | `design-system-care-monthly` | Ongoing maintenance after theme delivery |

---

## Smoke Test Checklist

Before delivering any output from this skill:

- [ ] Config validation completed — all four gates checked
- [ ] Token path resolution logged (fallbacks documented)
- [ ] settings_schema.json is valid JSON (parse check)
- [ ] settings_data.json has a value for every setting in settings_schema.json
- [ ] CSS bridge only references `settings.*` variables — no invented Liquid variables
- [ ] base.css hardcodes non-configurable tokens — no `settings.*` references
- [ ] All 14 snippets generated (per the Step 8 table)
- [ ] All 20 sections generated with correct cluster architecture
- [ ] All templates generated (JSON + required Liquid)
- [ ] locales/en.default.json covers all strings
- [ ] heyhi-theme-validator run — verdict documented
- [ ] No standalone "AI" in any output
- [ ] No em dashes in any copy (Liquid strings, schema labels, locales)
- [ ] No pricing mentioned in any output
- [ ] PROVISIONAL fields flagged if present
- [ ] Dark-native handling applied if `meta.default_scheme: "dark"`

---

## Exit Gate Required Headers (bottom-of-skill bracket)

This skill closes through the Exit Gate Flavor A (`CLAUDE-SESSION-RULES.md § Exit Gate`). Before declaring done, confirm every required header below contains real content, not a claim:

- `## Fixes Applied`
- `## Smoke Test`
- `## Next Session Prompt`

If any header is empty or contains advisory prose ("I checked for bugs") instead of a concrete artifact, the gate has not been satisfied. Apply fixes until clean — then emit.

---

*HeyHi Confidential — Skill internal methodology. Not for client distribution.*

*Theme workstream — core generation skill. Session T-1: skill design + settings architecture.*

*Bay Design LLC d/b/a HeyHi · Built March 2026 · Session T-1*
