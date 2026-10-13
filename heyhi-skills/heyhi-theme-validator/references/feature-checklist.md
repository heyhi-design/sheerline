---
title: "Feature Completeness Checklist — Profile 1"
profile: 1
checks: 25
version: "1.0.0"
---

# Profile 1: Feature Completeness Checklist

25 checks verifying all required Shopify OS 2.0 features. Each check has a machine-executable verification method.

---

## F-01: Sections Everywhere (OS 2.0)

**Check:** All templates use JSON format (not `.liquid`) except `gift_card.liquid` and customer account templates.

**Method:**
```
Glob: templates/*.liquid
Expected: only gift_card.liquid and customers/*.liquid
Any other .liquid template file → FAIL
```

**Pass criteria:** Zero `.liquid` template files outside `gift_card.liquid` and `customers/` directory.

**Common failures:** Legacy `.liquid` templates not converted to JSON; `password.liquid` mistakenly kept as Liquid.

**Remediation:** Convert each `.liquid` template to `.json` format with section references. Example: `templates/page.liquid` → `templates/page.json` containing `{"sections": {"main": {"type": "main-page"}}}`.

---

## F-02: Discounts

**Check:** Cart page includes discount code input and discount display.

**Method:**
```
Grep in sections/main-cart.liquid OR snippets/cart-*.liquid:
  Pattern 1: "discount" (case-insensitive)
  Pattern 2: <input.*discount OR form.*discount_code
  Pattern 3: cart.total_discount OR cart.discount_applications
Both input mechanism AND display must be present.
```

**Pass criteria:** Discount code input field present AND discount amount/name display present in cart.

**Common failures:** Discount display present but no input field; discount code form present but applied discounts not shown.

**Remediation:** Add discount code form with `<form action="/cart" method="post"><input type="text" name="discount">` and display block with `{% for discount in cart.discount_applications %}`.

---

## F-03: Accelerated Checkout

**Check:** Product page includes accelerated checkout (Shop Pay, Apple Pay, Google Pay buttons).

**Method:**
```
Grep in sections/main-product.liquid:
  Pattern: "payment_button" OR "shopify-payment-button" OR "accelerated"
  OR check product.json schema blocks for dynamic checkout block
```

**Pass criteria:** Dynamic checkout button rendered on product page via `{{ form | payment_button }}` or equivalent.

**Common failures:** Standard add-to-cart present but `payment_button` filter missing; checkout button exists but not the accelerated/dynamic version.

**Remediation:** Add `{{ form | payment_button }}` inside the product form after the standard add-to-cart button.

---

## F-04: Faceted Search

**Check:** Collection and search pages include faceted filtering.

**Method:**
```
Grep in sections/main-collection.liquid:
  Pattern: "facet" OR "filter" OR "active_filters"
Check for: snippets/facets.liquid existence
Grep in sections/main-search.liquid:
  Pattern: "facet" OR "filter"
```

**Pass criteria:** Faceted filter UI present on collection page AND search results page; `facets.liquid` snippet exists.

**Common failures:** Filters on collection but not search; filter UI present but not wired to Shopify's storefront filtering API.

**Remediation:** Create `snippets/facets.liquid` with filter form using `collection.filters` or `search.filters`. Include in both collection and search sections.

---

## F-05: Gift Cards

**Check:** Gift card template exists with QR code and Apple Wallet support.

**Method:**
```
File exists: templates/gift_card.liquid
Grep in templates/gift_card.liquid:
  Pattern 1: "qr_code" OR "qr-code" OR "QR"
  Pattern 2: "apple" OR "wallet" OR "apple_wallet_pass_url"
```

**Pass criteria:** `gift_card.liquid` exists AND contains QR code output AND Apple Wallet link.

**Common failures:** Gift card template missing entirely; template exists but no QR code; QR present but Apple Wallet link missing.

**Remediation:** Create `templates/gift_card.liquid` with `{{ gift_card | qr_code }}` and `<a href="{{ gift_card.apple_wallet_pass_url }}">`.

---

## F-06: Image Focal Points

**Check:** Image rendering uses focal point data.

**Method:**
```
Grep across all .liquid files:
  Pattern: "focal_point" OR "object-position" with Liquid variable
  At least one instance in product media or section image rendering
```

**Pass criteria:** At least one image render call uses focal point positioning.

**Common failures:** Images rendered with `object-fit: cover` but no focal point offset; `image_tag` used without focal point parameter.

**Remediation:** Use `{{ image | image_url: width: 800 | image_tag: class: 'object-cover', style: 'object-position: {{ image.presentation.focal_point }}' }}`.

---

## F-07: Social Sharing Images

**Check:** Theme generates Open Graph / social sharing image meta tags.

**Method:**
```
Grep in layout/theme.liquid:
  Pattern: "og:image" OR "page_image" OR "twitter:image"
```

**Pass criteria:** `<meta property="og:image"` tag present in theme.liquid head.

**Common failures:** No OG image meta tag; tag present but hardcoded to a single image instead of page-contextual.

**Remediation:** Add `<meta property="og:image" content="{{ page_image | image_url: width: 1200 }}">` to theme.liquid `<head>`.

---

## F-08: Multi-Currency / Language

**Check:** Country/language selector present and functional.

**Method:**
```
File exists: snippets/country-localization.liquid
Grep in sections/header.liquid:
  Pattern: "country-localization" OR "localization" OR "country_selector"
```

**Pass criteria:** `country-localization.liquid` snippet exists AND is referenced in header section.

**Common failures:** Snippet exists but not included in header; selector renders but form action missing.

**Remediation:** Create `snippets/country-localization.liquid` with localization form using `{% form 'localization' %}` and country/language selectors. Include in header section.

---

## F-09: Multi-Level Menus

**Check:** Header navigation supports at least 3 levels of menu depth.

**Method:**
```
Grep in sections/header.liquid:
  Pattern: "link.links" (nested links property)
  OR: nested loop structure (for link in linklists... for child in link.links... for grandchild)
Check header schema for linklist/menu input settings
```

**Pass criteria:** Header supports 3+ levels of navigation depth via nested `link.links` iteration.

**Common failures:** Only single-level navigation; two levels but no grandchild support; mobile drawer only shows top level.

**Remediation:** Add nested `{% for child_link in link.links %}{% for grandchild_link in child_link.links %}` loops in header navigation and mobile drawer.

---

## F-10: Newsletter Forms

**Check:** Newsletter signup section exists with proper form type.

**Method:**
```
File exists: sections/newsletter.liquid
Grep in sections/newsletter.liquid:
  Pattern: "form" AND "customer" (form_type: 'customer' for Shopify's newsletter)
```

**Pass criteria:** `newsletter.liquid` section exists with a customer signup form.

**Common failures:** Section exists but uses generic HTML form instead of Shopify's customer form; form type incorrect.

**Remediation:** Use `{% form 'customer', class: 'newsletter-form' %}` with email input in newsletter section.

---

## F-11: Pickup Availability

**Check:** Product page shows store pickup availability.

**Method:**
```
Grep in sections/main-product.liquid:
  Pattern: "store-availability" OR "pickup" OR "pickup_availabilities"
```

**Pass criteria:** Store availability / pickup information block present on product page.

**Common failures:** Block missing entirely; present in schema but not rendered in section markup.

**Remediation:** Add `<store-availability>` custom element or pickup availability block to main-product section, referencing `product.selected_or_first_available_variant`.

---

## F-12: Product Recommendations

**Check:** Product page includes product recommendations.

**Method:**
```
Option A — Grep in sections/main-product.liquid schema:
  Pattern: "product-recommendations" in blocks[] type
Option B — File exists: sections/product-recommendations.liquid
  Grep: "/recommendations/products.json"
At least one option must be present.
```

**Pass criteria:** Product recommendations present via either a schema block type OR standalone section with API integration.

**Common failures:** Neither block nor section present; section exists but doesn't use Shopify's recommendations API.

**Remediation:** Add `{"type": "product-recommendations"}` block to main-product schema, OR create standalone `sections/product-recommendations.liquid` fetching from `/recommendations/products.json?product_id={{ product.id }}`.

---

## F-13: Rich Media (3D / Video)

**Check:** Product media gallery handles 3D models and video in addition to images.

**Method:**
```
Grep in snippets/product-media-gallery.liquid OR sections/main-product.liquid:
  Pattern 1: "model" OR "model-viewer" OR "media.media_type == 'model'"
  Pattern 2: "video" OR "external_video" OR "media.media_type == 'video'"
  Both patterns must match.
```

**Pass criteria:** Product media rendering handles `model` AND `video` media types in addition to images.

**Common failures:** Only images rendered; video supported but 3D models not; media type switch/case missing model branch.

**Remediation:** Add media type branching: `{% case media.media_type %}{% when 'model' %}...{% when 'video' %}...{% when 'external_video' %}...{% endcase %}` with `<model-viewer>` element for 3D.

---

## F-14: Search + Predictive Search

**Check:** Search results page and predictive (typeahead) search implemented.

**Method:**
```
File exists: snippets/predictive-search.liquid
Grep in snippets/predictive-search.liquid:
  Pattern: "/search/suggest" OR "predictive-search" OR "search/suggest.json"
File exists: templates/search.json (search results page)
```

**Pass criteria:** `predictive-search.liquid` exists with API integration AND `search.json` template exists.

**Common failures:** Search results page exists but no predictive/typeahead; predictive search snippet missing API call.

**Remediation:** Create `snippets/predictive-search.liquid` that fetches from `/search/suggest.json?q=` and renders results in a dropdown.

---

## F-15: Selling Plans

**Check:** Product and cart pages display selling plan (subscription) information.

**Method:**
```
Grep in sections/main-product.liquid:
  Pattern: "selling_plan" OR "selling-plan" OR "sellingPlan"
Grep in sections/main-cart.liquid OR snippets/cart-*.liquid:
  Pattern: "selling_plan_allocation" OR "selling_plan"
```

**Pass criteria:** Selling plan selector on product page AND selling plan info displayed in cart.

**Common failures:** Product page has selector but cart doesn't show subscription details; selling plan data present but no user-facing UI.

**Remediation:** Add selling plan group selector to product form. Display `line_item.selling_plan_allocation` in cart line items.

---

## F-16: Shop Pay Installments

**Check:** Product page shows Shop Pay Installments banner.

**Method:**
```
Grep in sections/main-product.liquid:
  Pattern: "shopify-payment-terms" OR "shop-pay-installments" OR "payment-terms"
```

**Pass criteria:** Shop Pay installments banner element present on product page.

**Common failures:** Banner element missing; present but hidden by CSS; wrong element name.

**Remediation:** Add `<shopify-payment-terms variant-id="{{ product.selected_or_first_available_variant.id }}" shopify-meta="{{ shop.metafields.payment_terms }}">` to product section.

---

## F-17: Unit Pricing

**Check:** Price display handles unit pricing.

**Method:**
```
Grep in snippets/price.liquid OR sections/main-product.liquid:
  Pattern: "unit_price" OR "unit_price_measurement"
```

**Pass criteria:** Unit price rendering logic present in price display.

**Common failures:** Standard price shown but unit price ignored; unit_price referenced but measurement unit not displayed.

**Remediation:** Add `{% if variant.unit_price %}<span>{{ variant.unit_price | money }}/{{ variant.unit_price_measurement.reference_value }}{{ variant.unit_price_measurement.reference_unit }}</span>{% endif %}`.

---

## F-18: Variant Images

**Check:** Selecting a variant updates the product media gallery.

**Method:**
```
Grep in snippets/variant-picker.liquid OR sections/main-product.liquid:
  Pattern: "featured_media" OR "featured_image" OR "variant.featured_media"
  AND: JS/Liquid logic that swaps gallery on variant change
```

**Pass criteria:** Grep confirms variant-media wiring exists (JS references to `featured_media` and gallery update logic). **Manual verification required:** Actual swap behavior must be confirmed in browser — grep validates code presence, not runtime behavior.

**Common failures:** Variant selector works for pricing but doesn't update images; gallery swap logic present but targeting wrong element.

**Remediation:** Add JavaScript event listener on variant change that updates the media gallery to show `variant.featured_media`.

---

## F-19: Follow on Shop

**Check:** Theme includes Follow on Shop / Shop login button.

**Method:**
```
Grep in layout/theme.liquid:
  Pattern: "login_button" OR "shop_login_button" OR "customer_accounts_url"
```

**Pass criteria:** Shop login/follow button output present in theme layout.

**Common failures:** Filter not called; called but output hidden; incorrect filter name.

**Remediation:** Add `{{ shop | login_button: action: 'follow' }}` to theme.liquid, typically in the header area.

---

## F-20: Custom Liquid Section

**Check:** A custom Liquid section exists for merchant-authored Liquid code.

**Method:**
```
File exists: sections/custom-liquid.liquid
Grep in sections/custom-liquid.liquid schema:
  Pattern: "type.*liquid" (setting type is "liquid")
```

**Pass criteria:** `custom-liquid.liquid` exists with a `type: "liquid"` input setting in its schema.

**Common failures:** Section missing entirely; section exists but uses `type: "html"` instead of `type: "liquid"`.

**Remediation:** Create `sections/custom-liquid.liquid` with schema containing `{"type": "liquid", "id": "custom_liquid", "label": "Custom Liquid"}`.

---

## F-21: App Blocks

**Check:** Product page supports third-party app blocks.

**Method:**
```
Grep in sections/main-product.liquid schema:
  Pattern: '"@app"' OR "'@app'" (block type for app extensions)
```

**Pass criteria:** `main-product.liquid` schema blocks array includes `{"type": "@app"}`.

**Common failures:** App block type missing from schema; present in section body but not declared in schema blocks.

**Remediation:** Add `{"type": "@app", "name": "App block"}` to the `blocks` array in main-product.liquid's schema.

---

## F-22: Required Templates (11 JSON)

**Check:** All required JSON template files present.

**Method:**
```
File exists check for each:
  templates/index.json
  templates/product.json
  templates/collection.json
  templates/cart.json
  templates/blog.json
  templates/article.json
  templates/search.json
  templates/page.json
  templates/password.json
  templates/404.json
  templates/list-collections.json
All 11 must exist.
```

**Pass criteria:** All 11 required JSON templates present in `/templates/`.

**Common failures:** `list-collections.json` missing (commonly forgotten); `password.json` missing; template exists but is `.liquid` instead of `.json`.

**Remediation:** Create the missing `.json` template file with appropriate section references.

---

## F-23: theme.liquid

**Check:** Root layout file exists with required attributes.

**Method:**
```
File exists: layout/theme.liquid
Grep in layout/theme.liquid:
  Pattern 1: '<html' (html tag present)
  Pattern 2: 'lang=' (lang attribute set)
  Pattern 3: '{{ content_for_header }}' (required Shopify output)
  Pattern 4: '{{ content_for_layout }}' (required Shopify output)
```

**Pass criteria:** `theme.liquid` exists with `<html lang=...>`, `{{ content_for_header }}`, and `{{ content_for_layout }}`.

**Common failures:** File missing; `content_for_header` or `content_for_layout` missing; lang attribute hardcoded instead of using `request.locale.iso_code`.

**Remediation:** Ensure `layout/theme.liquid` contains `<html lang="{{ request.locale.iso_code }}">` in the opening tag, `{{ content_for_header }}` in `<head>`, and `{{ content_for_layout }}` in `<body>`.

---

## F-24: gift_card.liquid

**Check:** Gift card template exists with required elements.

**Method:**
```
File exists: templates/gift_card.liquid
Grep in templates/gift_card.liquid:
  Pattern 1: "qr_code" OR "QR"
  Pattern 2: "apple_wallet_pass_url" OR "wallet"
  Pattern 3: "gift_card.code" OR "gift_card.balance"
```

**Pass criteria:** Gift card template exists with QR code, Apple Wallet link, and gift card code/balance display.

**Common failures:** Template missing; QR code missing; Apple Wallet link missing; gift card code not displayed.

**Remediation:** Create template with `{{ gift_card | qr_code }}`, `<a href="{{ gift_card.apple_wallet_pass_url }}">`, and `{{ gift_card.code }}` / `{{ gift_card.balance | money }}`.

---

## F-25: settings_schema.json

**Check:** Theme settings schema exists and is valid JSON.

**Method:**
```
File exists: config/settings_schema.json
Parse as JSON: must not throw parse error
Check for required top-level array structure
```

**Pass criteria:** `settings_schema.json` exists, parses as valid JSON, and is a top-level array.

**Common failures:** File missing; invalid JSON (trailing comma, missing bracket); file is an object instead of array.

**Remediation:** Ensure `config/settings_schema.json` is a valid JSON array of setting group objects.

*HeyHi Confidential*
