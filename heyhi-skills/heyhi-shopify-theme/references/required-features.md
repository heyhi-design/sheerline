---
title: "Required Features — Shopify Theme Implementation Guide"
classification: confidential
session: T-1
version: "1.0.0"
created: "2026-03-29"
---

# Required Features

Implementation guide for all 23+ required Shopify Theme Store features. For each feature: the validator check ID (cross-references heyhi-theme-validator Profile 1), the file(s) where it lives, and the Liquid implementation pattern.

Reference alongside `references/section-patterns.md` when building Priority 1 and 2 sections. Run heyhi-theme-validator Profile 1 against this checklist at the end of Step 12.

---

## F-01 — Sections Everywhere (OS 2.0)

**Validator check:** All templates are `.json` (not `.liquid`) except `gift_card.liquid` and `customers/*.liquid`

**Files:** All files in `/templates/`

**Implementation:**
All page templates use JSON format (OS 2.0). Each JSON template defines a `sections` array referencing section IDs. No `.liquid` files in `/templates/` except gift_card.liquid and the `customers/` subdirectory (customer templates use a dedicated rendering system that does not support sections).

```json
{
  "sections": {
    "main": {
      "type": "main-product",
      "settings": {}
    }
  },
  "order": ["main"]
}
```

**Exceptions (must be .liquid, not .json):**
- `templates/gift_card.liquid`
- `templates/customers/login.liquid`
- `templates/customers/register.liquid`
- `templates/customers/account.liquid`
- `templates/customers/order.liquid`
- `templates/customers/addresses.liquid`
- `templates/customers/reset_password.liquid`

---

## F-02 — Discounts

**Validator check:** `cart.liquid` (or `main-cart.liquid`) includes discount code `<input>` + display block

**Files:** `sections/main-cart.liquid`

**Implementation:**
```liquid
{%- form 'cart', cart -%}
  {%- if cart.cart_level_discount_applications.size > 0 -%}
    <ul class="cart__discounts" aria-label="{{ 'sections.cart.discounts' | t }}">
      {%- for discount in cart.cart_level_discount_applications -%}
        <li class="cart__discount">
          {{ 'cart.general.discount' | t }}: {{ discount.title }}
          (-{{ discount.total_allocated_amount | money }})
        </li>
      {%- endfor -%}
    </ul>
  {%- endif -%}

  <div class="cart__discount-form">
    <label for="CartDiscountCode">{{ 'sections.cart.discount' | t }}</label>
    <input
      type="text"
      id="CartDiscountCode"
      name="discount"
      value="{{ cart.discount_applications[0].title }}"
      placeholder="{{ 'sections.cart.discount_placeholder' | t }}"
    >
    <button type="submit" name="update">
      {{ 'sections.cart.apply_discount' | t }}
    </button>
  </div>
{%- endform -%}
```

---

## F-03 — Accelerated Checkout

**Validator check:** `product.json` schema blocks has accelerated checkout block present in `main-product.liquid`

**Files:** `sections/main-product.liquid`

**Implementation:**
The `main-product.liquid` section schema must include an accelerated checkout block in `blocks[]`. Shopify renders the accelerated checkout buttons (Shop Pay, Apple Pay, Google Pay, PayPal) when this block type is present.

```json
{
  "type": "buy_buttons",
  "name": "t:sections.main-product.blocks.buy_buttons.name",
  "limit": 1,
  "settings": [
    {
      "type": "checkbox",
      "id": "show_dynamic_checkout",
      "default": true,
      "label": "t:sections.main-product.blocks.buy_buttons.settings.show_dynamic_checkout.label",
      "info": "t:sections.main-product.blocks.buy_buttons.settings.show_dynamic_checkout.info"
    }
  ]
}
```

In the section Liquid, render when the block is present:
```liquid
{%- when 'buy_buttons' -%}
  {%- if block.settings.show_dynamic_checkout -%}
    {{ form | payment_button }}
  {%- endif -%}
```

---

## F-04 — Faceted Search

**Validator check:** Collection + search templates include `facets.liquid` snippet

**Files:** `sections/main-collection.liquid`, `sections/main-search.liquid`, `snippets/facets.liquid`

**Implementation:**
`facets.liquid` uses Shopify's native filter API (`collection.filters`). Must include at least price range and product type filters.

```liquid
{%- if collection.filters != empty -%}
  <div class="facets" id="FacetsWrapperDesktop">
    <form id="FacetFiltersForm">
      {%- for filter in collection.filters -%}
        {%- case filter.type -%}
          {%- when 'price_range' -%}
            {%- render 'facets-price', filter: filter -%}
          {%- when 'list' -%}
            {%- render 'facets-list', filter: filter -%}
          {%- when 'boolean' -%}
            {%- render 'facets-boolean', filter: filter -%}
        {%- endcase -%}
      {%- endfor -%}
    </form>
  </div>
{%- endif -%}
```

Active filter display (required — show what's currently filtered):
```liquid
{%- if collection.filters != empty -%}
  {%- for filter in collection.filters -%}
    {%- for filter_value in filter.active_values -%}
      <a href="{{ filter_value.url_to_remove }}" class="active-filter">
        {{ filter.label }}: {{ filter_value.label }} &times;
      </a>
    {%- endfor -%}
    {%- if filter.type == 'price_range' and filter.min_value.value or filter.max_value.value -%}
      <a href="{{ filter.url_to_remove }}" class="active-filter">
        {{ filter.label }}: {{ filter.min_value.value | default: 0 | money }} -
        {{ filter.max_value.value | default: filter.range_max | money }} &times;
      </a>
    {%- endif -%}
  {%- endfor -%}
{%- endif -%}
```

---

## F-05 — Gift Cards

**Validator check:** `gift_card.liquid` exists; includes Apple Wallet + QR code output

**Files:** `templates/gift_card.liquid`

**Implementation:**
Note: `gift_card.liquid` is a `.liquid` file, not JSON (not OS 2.0). It uses the `gift_card` template object.

```liquid
<!DOCTYPE html>
<html lang="{{ request.locale.iso_code }}">
<head>
  <meta charset="utf-8">
  <title>{{ 'gift_cards.issued.title' | t: value: gift_card.initial_value | money, shop: shop.name }}</title>
  {{ content_for_header }}
</head>
<body>
  <div class="gift-card">
    <h1>{{ 'gift_cards.issued.subtext' | t }}</h1>
    <div class="gift-card__amount">{{ gift_card.initial_value | money }}</div>
    <div class="gift-card__code">{{ gift_card.code | format_code }}</div>

    {%- if gift_card.pass_url -%}
      <a href="{{ gift_card.pass_url }}" class="gift-card__apple-wallet">
        <img src="{{ 'gift-card/add-to-apple-wallet.svg' | shopify_asset_url }}"
             alt="{{ 'gift_cards.issued.add_to_apple_wallet' | t }}"
             width="120" height="40">
      </a>
    {%- endif -%}

    <div class="gift-card__qr" id="QrCode" data-identifier="{{ gift_card.qr_identifier }}"></div>
  </div>

  <script src="{{ 'vendor/qrcode.js' | shopify_asset_url }}" defer></script>
  <script>
    document.addEventListener('DOMContentLoaded', function() {
      var qrEl = document.getElementById('QrCode');
      new QRCode(qrEl, {
        text: qrEl.dataset.identifier,
        width: 120,
        height: 120
      });
    });
  </script>
</body>
</html>
```

---

## F-06 — Image Focal Points

**Validator check:** Image render calls use `focal_point` attribute

**Files:** All sections and snippets that render product or section images

**Implementation:**
All `image_url` + `image_tag` render calls must include the focal_point attribute:

```liquid
{%- if image -%}
  {{
    image
    | image_url: width: 1500
    | image_tag:
      loading: 'lazy',
      sizes: '(min-width: 1440px) 700px, (min-width: 768px) 50vw, 100vw',
      widths: '375, 550, 750, 1000, 1500',
      alt: image.alt | escape,
      class: 'media-image',
      style: 'object-position: ' | append: image.presentation.focal_point
  }}
{%- endif -%}
```

For section image settings (not product images), use the same pattern:
```liquid
{%- assign image = section.settings.image -%}
{%- if image -%}
  {{- image | image_url: width: 1500 | image_tag:
    loading: 'lazy',
    alt: image.alt | escape,
    style: 'object-position: ' | append: image.presentation.focal_point
  -}}
{%- endif -%}
```

---

## F-07 — Social Sharing Images

**Validator check:** `theme.liquid` has `page_image` meta tag

**Files:** `layout/theme.liquid`

**Implementation:**
In the `<head>` of `theme.liquid`:

```liquid
{%- if page_image -%}
  <meta property="og:image" content="{{ page_image | image_url: width: 1200 }}">
  <meta property="og:image:secure_url" content="{{ page_image | image_url: width: 1200 }}">
  <meta property="og:image:width" content="1200">
  <meta name="twitter:image" content="{{ page_image | image_url: width: 1200 }}">
{%- else -%}
  {%- if settings.share_image -%}
    <meta property="og:image" content="{{ settings.share_image | image_url: width: 1200 }}">
    <meta name="twitter:image" content="{{ settings.share_image | image_url: width: 1200 }}">
  {%- endif -%}
{%- endif -%}
```

Also add `share_image` as an `image_picker` setting in `settings_schema.json`.

---

## F-08 — Multi-Currency / Language

**Validator check:** `country-localization.liquid` snippet exists; referenced in header section

**Files:** `snippets/country-localization.liquid`, `sections/header.liquid`

**Implementation:**
```liquid
{%- unless shop.enabled_currencies.size == 1 and shop.enabled_payment_methods.size == 0 -%}
  {%- form 'localization', id: 'HeaderCountryForm' -%}
    <div class="country-selector">
      <button type="button"
              aria-expanded="false"
              aria-controls="HeaderCountryList"
              aria-label="{{ 'localization.country_label' | t }}">
        {{ localization.country.iso_code }}
      </button>
      <ul id="HeaderCountryList" role="list">
        {%- for country in localization.available_countries -%}
          <li>
            <a href="#"
               data-value="{{ country.iso_code }}"
               {% if country.iso_code == localization.country.iso_code %}aria-current="true"{% endif %}>
              {{ country.name }} ({{ country.currency.iso_code }} {{ country.currency.symbol }})
            </a>
          </li>
        {%- endfor -%}
      </ul>
    </div>
    <input type="hidden" name="country_code" value="{{ localization.country.iso_code }}">
  {%- endform -%}
{%- endunless -%}
```

---

## F-09 — Multi-Level Menus

**Validator check:** Header section schema has `linklist` + `link_list` inputs with depth support

**Files:** `sections/header.liquid`

**Implementation:**
Header schema must include:
```json
{
  "type": "link_list",
  "id": "menu",
  "default": "main-menu",
  "label": "t:sections.header.settings.menu.label"
}
```

Multi-level rendering (3 levels):
```liquid
<nav class="nav-main" aria-label="{{ 'accessibility.main_menu' | t }}">
  <ul class="nav__list" role="list">
    {%- for link in linklists[section.settings.menu].links -%}
      <li class="nav__item {% if link.links.size > 0 %}nav__item--has-children{% endif %}">
        <a href="{{ link.url }}"
           class="nav__link"
           {% if link.links.size > 0 %}aria-expanded="false" aria-haspopup="true"{% endif %}>
          {{ link.title }}
        </a>
        {%- if link.links.size > 0 -%}
          <ul class="nav__dropdown" role="list">
            {%- for child_link in link.links -%}
              <li class="nav__dropdown-item {% if child_link.links.size > 0 %}nav__dropdown-item--has-children{% endif %}">
                <a href="{{ child_link.url }}" class="nav__dropdown-link">
                  {{ child_link.title }}
                </a>
                {%- if child_link.links.size > 0 -%}
                  <ul class="nav__dropdown-child" role="list">
                    {%- for grandchild_link in child_link.links -%}
                      <li>
                        <a href="{{ grandchild_link.url }}">{{ grandchild_link.title }}</a>
                      </li>
                    {%- endfor -%}
                  </ul>
                {%- endif -%}
              </li>
            {%- endfor -%}
          </ul>
        {%- endif -%}
      </li>
    {%- endfor -%}
  </ul>
</nav>
```

---

## F-10 — Newsletter Forms

**Validator check:** `newsletter.liquid` section exists; uses `form_type: 'customer'`

**Files:** `sections/newsletter.liquid`

**Implementation:**
```liquid
{%- form 'customer', id: 'NewsletterForm' -%}
  <input type="hidden" name="contact[tags]" value="newsletter">

  {%- if form.posted_successfully? -%}
    <p class="newsletter__success" role="status">
      {{ 'newsletter.success' | t }}
    </p>
  {%- else -%}
    <div class="newsletter__fields">
      <label for="NewsletterEmail" class="visually-hidden">
        {{ 'newsletter.label' | t }}
      </label>
      <input
        type="email"
        id="NewsletterEmail"
        name="contact[email]"
        value="{{ form.email }}"
        placeholder="{{ 'newsletter.placeholder' | t }}"
        required
        autocorrect="off"
        autocapitalize="off"
      >
      {%- if form.errors -%}
        <p class="newsletter__error" role="alert">{{ form.errors.translated_fields.email | capitalize }}
          {{ form.errors.messages.email }}</p>
      {%- endif -%}
      <button type="submit" class="button">
        {{ 'newsletter.button' | t }}
      </button>
    </div>
  {%- endif -%}
{%- endform -%}
```

---

## F-11 — Pickup Availability

**Validator check:** `main-product.liquid` has `store-availability` block

**Files:** `sections/main-product.liquid`

**Implementation:**
Block in schema:
```json
{
  "type": "pickup_availability",
  "name": "t:sections.main-product.blocks.pickup_availability.name",
  "limit": 1
}
```

Render in section:
```liquid
{%- when 'pickup_availability' -%}
  {%- if product.available -%}
    <div class="pickup-availability" id="PickupAvailability">
      {%- assign pick_up_availabilities = product.selected_or_first_available_variant
          | where: 'available', true -%}
      <pickup-availability
        class="pickup-availability__wrapper"
        data-root-url="{{ routes.root_url }}"
        data-variant-id="{{ product.selected_or_first_available_variant.id }}"
        data-has-only-default-variant="{{ product.has_only_default_variant }}">
        {%- if product.selected_or_first_available_variant.store_availabilities.size > 0 -%}
          {%- render 'store-availability',
            product_variant: product.selected_or_first_available_variant,
            store_availabilities: product.selected_or_first_available_variant.store_availabilities
          -%}
        {%- endif -%}
      </pickup-availability>
    </div>
  {%- endif -%}
```

---

## F-12 — Product Recommendations

**Validator check:** `"type": "product-recommendations"` block in `main-product.liquid` schema OR standalone `sections/product-recommendations.liquid` with `/recommendations/products.json` API

**Files:** `sections/main-product.liquid` (preferred) OR `sections/product-recommendations.liquid`

**Implementation (preferred — block approach):**
Schema block:
```json
{
  "type": "product-recommendations",
  "name": "t:sections.main-product.blocks.product_recommendations.name",
  "limit": 1,
  "settings": [
    {
      "type": "range",
      "id": "products_to_show",
      "min": 2,
      "max": 10,
      "step": 1,
      "default": 4,
      "label": "t:sections.main-product.blocks.product_recommendations.settings.products_to_show.label"
    }
  ]
}
```

Render:
```liquid
{%- when 'product-recommendations' -%}
  {%- if recommendations.performed and recommendations.products_count > 0 -%}
    <div class="product-recommendations">
      <h2>{{ 'sections.product_recommendations.heading' | t }}</h2>
      <ul class="product-recommendations__grid" role="list">
        {%- for recommendation in recommendations.products limit: block.settings.products_to_show -%}
          <li>{%- render 'product-thumbnail', product: recommendation -%}</li>
        {%- endfor -%}
      </ul>
    </div>
  {%- endif -%}
```

Note: `@app` blocks satisfy the "App Blocks" requirement (F-21) only — they do NOT satisfy this check.

---

## F-13 — Rich Media (3D / Video)

**Validator check:** Product media gallery handles `model` + `video` + `image` media types

**Files:** `snippets/product-media-gallery.liquid`

**Implementation:**
```liquid
{%- for media in product.media -%}
  {%- case media.media_type -%}
    {%- when 'image' -%}
      <div class="media media--image">
        {{- media | image_url: width: 1500 | image_tag:
          loading: 'lazy',
          alt: media.alt | escape,
          style: 'object-position: ' | append: media.presentation.focal_point
        -}}
      </div>

    {%- when 'video' -%}
      <div class="media media--video">
        {{- media | video_tag:
          image_size: '1024x',
          autoplay: false,
          loop: false,
          controls: true,
          muted: false
        -}}
      </div>

    {%- when 'external_video' -%}
      <div class="media media--external-video">
        {{- media | external_video_tag -}}
      </div>

    {%- when 'model' -%}
      <div class="media media--model"
           data-media-id="{{ media.id }}"
           style="padding-top: {{ 1 | divided_by: media.preview_image.aspect_ratio | times: 100 }}%">
        {{- media | model_viewer_tag:
          image_size: '1024x',
          reveal: 'interaction',
          toggleable: true,
          data-model-id: media.id
        -}}
      </div>
  {%- endcase -%}
{%- endfor -%}
```

Also include in `theme.liquid`:
```liquid
<script type="application/json" id="ModelJson-{{ section.id }}">
  {{ product.media | where: 'media_type', 'model' | json }}
</script>
```

---

## F-14 — Search + Predictive Search

**Validator check:** `predictive-search.liquid` snippet exists; uses `/search/suggest` API

**Files:** `snippets/predictive-search.liquid`, `sections/header.liquid`

**Implementation:**
```liquid
{# In header.liquid #}
<search-form role="search" action="{{ routes.search_url }}" method="get">
  <div class="search__input-wrapper">
    <input
      type="search"
      id="Search-In-Modal"
      name="q"
      value="{{ search.terms | escape }}"
      placeholder="{{ 'general.search.search' | t }}"
      role="combobox"
      autocomplete="off"
      aria-expanded="false"
      aria-owns="predictive-search-results"
      aria-controls="predictive-search-results"
      aria-haspopup="listbox"
      aria-autocomplete="list"
    >
  </div>
  <div id="predictive-search-results"
       class="predictive-search"
       tabindex="-1"
       role="listbox"
       aria-label="{{ 'accessibility.predictive_search_results' | t }}">
  </div>
</search-form>
```

The predictive search component fetches from `/search/suggest.json?q=[query]&resources[type]=product,collection,page,article&resources[limit]=10&section_id=predictive-search` via JavaScript. Results are rendered into the ARIA live region.

---

## F-15 — Selling Plans

**Validator check:** Cart shows selling plan info; product page displays selling plan options

**Files:** `sections/main-product.liquid`, `sections/main-cart.liquid`, `snippets/price.liquid`

**Implementation (product page):**
```liquid
{%- if product.selling_plan_groups.size > 0 -%}
  <div class="selling-plan-group">
    {%- for selling_plan_group in product.selling_plan_groups -%}
      <div class="selling-plan-group__item">
        <input
          type="radio"
          id="SellingPlanGroup-{{ selling_plan_group.id }}"
          name="selling_plan_group"
          value="{{ selling_plan_group.id }}"
        >
        <label for="SellingPlanGroup-{{ selling_plan_group.id }}">
          {{ selling_plan_group.name }}
        </label>
        {%- for option in selling_plan_group.options -%}
          <select name="selling_plan" id="SellingPlan-{{ selling_plan_group.id }}-{{ option.name }}">
            {%- for selling_plan in selling_plan_group.selling_plans -%}
              {%- assign option_value = selling_plan.options | where: 'name', option.name | first -%}
              <option value="{{ selling_plan.id }}">{{ option_value.value }}</option>
            {%- endfor -%}
          </select>
        {%- endfor -%}
      </div>
    {%- endfor -%}
  </div>
{%- endif -%}
```

**In cart (line item selling plan display):**
```liquid
{%- if item.selling_plan_allocation -%}
  <p class="cart-item__selling-plan">
    {{ item.selling_plan_allocation.selling_plan.name }}
  </p>
{%- endif -%}
```

---

## F-16 — Shop Pay Installments

**Validator check:** Product page includes `shop-pay-installments-banner`

**Files:** `sections/main-product.liquid`

**Implementation:**
Block in schema:
```json
{
  "type": "installments",
  "name": "t:sections.main-product.blocks.installments.name",
  "limit": 1
}
```

Render:
```liquid
{%- when 'installments' -%}
  {%- if product.selected_or_first_available_variant.available -%}
    <div class="installments">
      {{ 'shopify-payment-terms' | payment_terms:
          variant: product.selected_or_first_available_variant }}
    </div>
  {%- endif -%}
```

---

## F-17 — Unit Pricing

**Validator check:** `price.liquid` handles `unit_price_measurement`

**Files:** `snippets/price.liquid`

**Implementation:**
```liquid
{%- if variant.unit_price_measurement -%}
  <span class="unit-price">
    <span class="visually-hidden">{{ 'products.product.price.unit_price' | t }}</span>
    {{- variant.unit_price | money -}}
    <span aria-hidden="true">/</span>
    <span class="visually-hidden">&nbsp;{{ 'accessibility.unit_price_separator' | t }}&nbsp;</span>
    {%- if variant.unit_price_measurement.reference_value != 1 -%}
      {{- variant.unit_price_measurement.reference_value -}}
    {%- endif -%}
    {{ variant.unit_price_measurement.reference_unit }}
  </span>
{%- endif -%}
```

---

## F-18 — Variant Images

**Validator check:** Variant picker triggers media gallery swap. Manual verification required — grep confirms JS wiring; browser testing confirms actual swap behavior.

**Files:** `snippets/variant-picker.liquid`, `snippets/product-media-gallery.liquid`, `assets/component-variant-picker.js`

**Implementation:**
Variant picker sets a `data-media-id` on selection:
```liquid
{%- for variant in product.variants -%}
  <input
    type="radio"
    id="Variant-{{ section.id }}-{{ variant.id }}"
    name="options[{{ option.name | escape }}]"
    value="{{ variant.title | escape }}"
    {% if variant.featured_media %}data-media-id="{{ variant.featured_media.id }}"{% endif %}
  >
{%- endfor -%}
```

JavaScript wires the `change` event on variant inputs to update the media gallery:
```javascript
document.querySelectorAll('[name="options[Color]"]').forEach(input => {
  input.addEventListener('change', (event) => {
    const mediaId = event.target.dataset.mediaId;
    if (mediaId) {
      // Scroll gallery to the matching media item
      const mediaItem = document.querySelector(`[data-media-id="${mediaId}"]`);
      if (mediaItem) mediaItem.scrollIntoView({ behavior: 'smooth' });
    }
  });
});
```

---

## F-19 — Follow on Shop

**Validator check:** `theme.liquid` includes `login_button` filter output

**Files:** `layout/theme.liquid`

**Implementation:**
In `theme.liquid`, include this in the appropriate location (typically footer or account area):
```liquid
{{ shop | login_button }}
```

This renders the "Follow on Shop" button when the Shop app is active. If the merchant doesn't use Shop app, the filter outputs nothing — so this is safe to include unconditionally.

---

## F-20 — Custom Liquid Section

**Validator check:** `sections/custom-liquid.liquid` exists with `type: liquid` input

**Files:** `sections/custom-liquid.liquid`

**Implementation:**
```liquid
{% if section.settings.custom_liquid != blank %}
  {{ section.settings.custom_liquid }}
{% endif %}

{% schema %}
{
  "name": "t:sections.custom-liquid.name",
  "tag": "section",
  "class": "section-custom-liquid",
  "settings": [
    {
      "type": "liquid",
      "id": "custom_liquid",
      "label": "t:sections.custom-liquid.settings.custom_liquid.label",
      "info": "t:sections.custom-liquid.settings.custom_liquid.info"
    },
    {
      "type": "color_scheme",
      "id": "color_scheme",
      "label": "t:sections.custom-liquid.settings.color_scheme.label",
      "default": "scheme-1"
    }
  ],
  "presets": [
    {
      "name": "t:sections.custom-liquid.presets.custom_liquid.name"
    }
  ]
}
{% endschema %}
```

---

## F-21 — App Blocks

**Validator check:** `main-product.liquid` schema has `blocks: [{type: "@app"}]`

**Files:** `sections/main-product.liquid`

**Implementation:**
In the `blocks` array of `main-product.liquid` schema, include the app block type:
```json
{
  "type": "@app"
}
```

Full blocks array example:
```json
"blocks": [
  { "type": "text", "name": "..." },
  { "type": "price", "name": "..." },
  { "type": "buy_buttons", "name": "..." },
  { "type": "pickup_availability", "name": "..." },
  { "type": "product-recommendations", "name": "..." },
  { "type": "@app" }
]
```

The `@app` type enables Shopify app integrations (reviews, subscriptions, etc.) to inject blocks directly into the product page. It satisfies the App Blocks requirement independently from Product Recommendations (F-12).

---

## F-22 — 11 Required JSON Templates

**Validator check:** All 11 required `.json` templates present in `/templates/`

**Files:** All files in `/templates/`

**Required templates (must exist as .json):**
1. `templates/index.json`
2. `templates/product.json`
3. `templates/collection.json`
4. `templates/search.json`
5. `templates/cart.json`
6. `templates/blog.json`
7. `templates/article.json`
8. `templates/page.json`
9. `templates/404.json`
10. `templates/list-collections.json`
11. `templates/password.json`

Additional recommended templates:
- `templates/product.preorder.json`
- `templates/collection.with-sidebar.json`
- `templates/page.contact.json`

---

## F-23 — theme.liquid

**Validator check:** `layout/theme.liquid` present; `lang` attribute set

**Files:** `layout/theme.liquid`

**Required elements in theme.liquid:**
```liquid
<!DOCTYPE html>
<html lang="{{ request.locale.iso_code }}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="canonical" href="{{ canonical_url }}">
  <meta name="description" content="{{ page_description | escape }}">
  {{ content_for_header }}
  <!-- CSS bridge, font loading, social meta tags go here -->
</head>
<body class="template-{{ template | replace: '.', ' ' | truncatewords: 1, '' | handle }}">
  <a class="skip-link" href="#MainContent">
    {{ 'accessibility.skip_to_text' | t }}
  </a>

  {%- sections 'header-group' -%}

  <main id="MainContent" role="main" tabindex="-1">
    {{ content_for_layout }}
  </main>

  {%- sections 'footer-group' -%}
</body>
</html>
```

Critical: `lang="{{ request.locale.iso_code }}"` is the exact required pattern. Do not hardcode `lang="en"`.

---

## F-24 — gift_card.liquid

**Validator check:** `templates/gift_card.liquid` present with QR + Apple Wallet output

See F-05 above for full implementation.

---

## F-25 — settings_schema.json

**Validator check:** `config/settings_schema.json` present + valid JSON

**Files:** `config/settings_schema.json`

See `templates/settings_schema-base.json` for the base template. The settings schema must:
- Open with a `theme_info` block (first element, `"name": "theme_info"`)
- Include all required settings: colors, typography, spacing, radius, favicon
- Be valid JSON (parse-check before delivery)
- Reference schema labels via `t:settings_schema.[group].[setting].label` pattern

---

## Additional Required Features (Beyond the 25-point checklist)

### Breadcrumbs
Not a formal validator check but expected by reviewers. Present in all non-homepage templates.

```liquid
{# snippets/breadcrumbs.liquid #}
<nav class="breadcrumbs" aria-label="{{ 'accessibility.breadcrumbs' | t }}">
  <ol role="list">
    <li><a href="{{ routes.root_url }}">{{ 'general.breadcrumbs.home' | t }}</a></li>
    {%- if template == 'product' -%}
      {%- if collection -%}
        <li><a href="{{ collection.url }}">{{ collection.title }}</a></li>
      {%- endif -%}
      <li aria-current="page">{{ product.title }}</li>
    {%- elsif template == 'article' -%}
      <li><a href="{{ blog.url }}">{{ blog.title }}</a></li>
      <li aria-current="page">{{ article.title }}</li>
    {%- endif -%}
  </ol>
</nav>
```

### Social Sharing
Expected on product and article pages. Use `rel="nofollow"` on all external share links.

```liquid
{# snippets/social-sharing.liquid #}
<div class="social-sharing">
  <a href="https://www.facebook.com/sharer.php?u={{ share_url }}"
     rel="nofollow noopener"
     target="_blank"
     aria-label="{{ 'general.social.facebook' | t }}">
    {%- render 'icon-facebook' -%}
  </a>
  <a href="https://twitter.com/intent/tweet?url={{ share_url }}&text={{ share_title }}"
     rel="nofollow noopener"
     target="_blank"
     aria-label="{{ 'general.social.twitter' | t }}">
    {%- render 'icon-twitter' -%}
  </a>
</div>
```

---

*HeyHi Confidential — Session T-1. Implementation reference for heyhi-shopify-theme generation workflow.*
