---
classification: HeyHi Internal Use Only
name: shopify-liquid-constraints
description: Known Shopify Liquid parser constraints and non-existent filters — load when debugging Liquid errors or reviewing generated theme code
type: reference
created: 2026-03-31
---

# Shopify Liquid — Known Constraints and Non-Existent Filters

## Parser constraints (cause runtime errors)

### Filter pipelines in `{% %}` tag named parameters

Shopify's Liquid parser treats `|` inside `{% %}` tag named parameter lists as a
tag-level construct separator, not a filter operator. This affects `form`, `render`,
`paginate`, and `video_tag` (block form).

**Affected tags:** `{% form %}`, `{% render %}`, `{% paginate %}`, `{% video_tag %}` (block form)

**Pattern that breaks:**
```liquid
{%- form 'product', product, id: 'ProductForm-' | append: section.id -%}
```

**Correct pattern — assign first:**
```liquid
{%- assign product_form_id = 'ProductForm-' | append: section.id -%}
{%- form 'product', product, id: product_form_id -%}
```

---

### Filter pipelines in `{{ }}` output named parameters with trailing commas

Inside any filter's named parameter list (`image_tag`, `video_tag`, `external_video_tag`, etc.),
a filter pipeline on a named param value causes a parse error if a comma follows it
(i.e., another named param comes after it).

**Error message:** `Expected end_of_string but found Comma`

**Pattern that breaks:**
```liquid
{{ image | image_tag: alt: image.alt | default: '' | escape, style: focal_point }}
```

**Correct pattern — pre-assign:**
```liquid
{%- assign img_alt = image.alt | default: '' | escape -%}
{{ image | image_tag: alt: img_alt, style: focal_point }}
```

**Proactive rule:** Even if the filter-chained value is the LAST named parameter today (no trailing comma),
pre-assign it anyway. A future parameter addition would silently break the file.

---

## Filters that do not exist in Shopify Liquid

| Filter | Status | Correct alternative |
|--------|--------|---------------------|
| `ternary` | Does not exist | `{% if %}` + pre-assign |
| `compact` | Not available in output context | `{% for %}` with `{% if %}` check |
| `dig` | Not a Shopify filter | Direct property access |

**Note on `ternary`:** This filter exists in some Ruby Liquid forks and is commonly hallucinated
by language models. Shopify has no shorthand conditional filter. Always use `{% if %}` + pre-assign.

---

## Filters that exist but behave differently than generic Liquid

| Filter | Shopify behavior |
|--------|-----------------|
| `default` | Works as expected for nil/false/blank values |
| `escape` | Applies HTML entity encoding — safe for attribute values |
| `url_encode` | Required for URL parameter values — different from `escape` |
| `json` | Available but outputs raw JSON — use carefully in HTML attributes |

---

## Common hallucination patterns to avoid

These patterns appear plausible but do not work in Shopify Liquid:

```liquid
# WRONG — ternary does not exist
{{ forloop.first | ternary: 'eager', 'lazy' }}
{{ autoplay | ternary: 'off', 'polite' }}

# WRONG — compact not available in output context
{{ array | compact | join: ', ' }}

# WRONG — filter pipeline in {% %} tag named param
{%- render 'snippet', id: 'prefix-' | append: section.id -%}
```

---

## Pre-push lint commands

Run from the theme root before every `shopify theme push`:

```bash
# Or: bash shopify-lint.sh (if present in theme root)

# RC1: filter pipelines in {% form/render/paginate/video_tag %} named params
grep -rn "{%-\?\s*\(form\|render\|paginate\|video_tag\)\b.*:.*|" sections/ snippets/ layout/

# RC2a: alt filter chains with trailing comma
grep -rn "alt:.*|.*escape," sections/ snippets/

# RC2b: default filter chains with trailing comma
grep -rn "alt:.*|.*default.*," sections/ snippets/

# RC3: ternary filter
grep -rn "| ternary" sections/ snippets/ layout/
```

All must return zero matches before pushing.

---

## Reference

Shopify Liquid filter reference: https://shopify.dev/docs/api/liquid/filters
Shopify Liquid tags reference: https://shopify.dev/docs/api/liquid/tags

---

*HeyHi Internal Use Only*
