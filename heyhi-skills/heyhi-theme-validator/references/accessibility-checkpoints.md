---
title: "Accessibility Audit Checkpoints — Profile 3"
profile: 3
checks: 12
version: "1.0.0"
wcag_target: "2.1 AA"
---

# Profile 3: Accessibility Audit Checkpoints

15 checkpoints verifying WCAG 2.1 AA compliance for Shopify themes. Each maps to a specific WCAG criterion. A-13 through A-15 cover runtime behaviors (live-region injection, focus-on-dismiss, redundant ARIA) that static analysis flags but a human confirms.

---

## A-01: Keyboard Accessible Elements

**WCAG:** 2.1.1 Keyboard (Level A)

**Check:** All interactive elements use native keyboard-accessible HTML elements.

**Method:**
```
Grep across all .liquid files:
  Flag: <div.*onclick, <span.*onclick, <div.*role="button", <span.*role="link"
  Expected: zero matches
  All interactive elements should be <a href>, <button>, <input>, <select>, or <textarea>
```

**Pass criteria:** No `<div>` or `<span>` elements used as interactive controls. All click handlers on semantic HTML elements.

**Remediation:** Replace `<div onclick="...">` with `<button type="button">`. Replace `<span role="link">` with `<a href="...">`.

---

## A-02: Visible Focus States

**WCAG:** 2.4.7 Focus Visible (Level AA)

**Check:** All focusable elements have visible focus indicators.

**Method:**
```
Grep in assets/base.css AND all component CSS:
  Required patterns:
    :focus-visible (must exist)
    outline: none (must NOT appear without a replacement style)
  Verify: :focus-visible rules exist for a, button, input, select, textarea
```

**Pass criteria:** `:focus-visible` styles defined for all interactive element types. No `outline: none` without a visible replacement (e.g., box-shadow, border-color change).

**Remediation:** Add to `base.css`:
```css
:focus-visible {
  outline: 2px solid var(--color-accent-1);
  outline-offset: 2px;
}
```

---

## A-03: Alt Attributes on Images

**WCAG:** 1.1.1 Non-text Content (Level A)

**Check:** All `<img>` tags have alt attributes.

**Method:**
```
Grep across all .liquid files:
  Find all <img tags
  For each: verify alt= attribute present
  Pattern for Shopify images: alt="{{ image.alt | escape }}"
  Decorative images: alt="" (empty, not missing)
  Flag: any <img without alt attribute
```

**Pass criteria:** Every `<img>` has an `alt` attribute. Content images use `alt="{{ image.alt | escape }}"`. Decorative images use `alt=""`.

**Remediation:** Add `alt="{{ image.alt | escape }}"` to all content images. Add `alt=""` to decorative images (icons, backgrounds).

---

## A-04: Form Input-Label Association

**WCAG:** 1.3.1 Info and Relationships (Level A)

**Check:** All form inputs have associated labels.

**Method:**
```
Grep across all .liquid files:
  Find all <input, <select, <textarea elements
  For each: verify it has an id attribute
  For each id: verify a matching <label for="[id]"> exists
  Exception: inputs with type="hidden" or type="submit"
  Exception: inputs with aria-label or aria-labelledby attribute
```

**Pass criteria:** Every visible form input has either a matching `<label for>` OR an `aria-label`/`aria-labelledby` attribute.

**Remediation:** Add `id` to input elements and create matching `<label for="[input-id]">` elements. For icon-only inputs, use `aria-label`.

---

## A-05: Valid HTML Nesting

**WCAG:** 4.1.1 Parsing (Level A)

**Check:** HTML elements are properly nested without structural errors.

**Method:**
```
Review all .liquid section files:
  Check 1: No unclosed tags (every opening tag has a closing tag or is self-closing)
  Check 2: Block elements (<div>, <section>, <article>, <main>) not inside inline elements (<span>, <a>, <em>)
  Check 3: Heading hierarchy not skipped (no h1 → h3 without h2)
  Note: Liquid {% if %} blocks may make static analysis incomplete — check both branches
```

**Pass criteria:** No structural HTML nesting errors in non-conditional markup. Heading hierarchy is sequential within each section. **Caveat:** Liquid conditionals (`{% if %}`, `{% for %}`) may produce valid HTML in both branches but static analysis cannot verify all runtime paths. Flag conditional blocks with complex nesting for manual review.

**Remediation:** Fix unclosed tags. Move block elements outside inline parents. Ensure heading levels follow h1 → h2 → h3 order without skipping.

---

## A-06: Text Contrast 4.5:1 (Body)

**WCAG:** 1.4.3 Contrast Minimum (Level AA)

**Check:** Body text meets 4.5:1 contrast ratio against its background.

**Method:**
```
Extract color values from:
  settings_data.json: colors_text (foreground)
  settings_data.json: colors_background_1 (background)
  OR from active-brand.json: tokens.color.text.primary, tokens.color.backgrounds.primary
Calculate contrast ratio using WCAG relative luminance formula:
  1. Convert hex to sRGB (0-1 range): R/G/B = channel_value / 255
  2. Linearize: if channel <= 0.04045, linear = channel/12.92; else linear = ((channel+0.055)/1.055)^2.4
  3. Relative luminance: L = 0.2126*R_lin + 0.7152*G_lin + 0.0722*B_lin
  4. Contrast ratio: (L_lighter + 0.05) / (L_darker + 0.05)
Minimum: 4.5:1 for normal text (< 24px regular / < 18.67px bold)
```

**Pass criteria:** Calculated contrast ratio >= 4.5:1 for body text against primary background.

**Remediation:** Adjust either text color or background color to achieve 4.5:1 minimum. Update in `settings_data.json` defaults and verify in `active-brand.json` tokens.

---

## A-07: Text Contrast 3:1 (Large Text)

**WCAG:** 1.4.3 Contrast Minimum (Level AA)

**Check:** Large text (headings) meets 3:1 contrast ratio against its background.

**Method:**
```
Extract heading color values from:
  settings_data.json or base.css heading styles
  Background from settings_data.json: colors_background_1
Calculate contrast ratio using same WCAG luminance formula as A-06
Minimum: 3:1 for large text (>= 24px regular OR >= 18.67px bold)
Check: h1, h2, h3, h4 color values against their likely backgrounds
```

**Pass criteria:** Calculated contrast ratio >= 3:1 for heading text against background.

**Remediation:** Adjust heading colors or backgrounds. If headings inherit body text color, body contrast (A-06) may already satisfy this.

---

## A-08: Focus Order Matches DOM Order

**WCAG:** 2.4.3 Focus Order (Level A)

**Check:** Visual presentation order matches DOM order for keyboard navigation.

**Method:**
```
Grep in all CSS files:
  Flag patterns that reorder visual presentation:
    order: (CSS flexbox/grid order property, when used to reorder content)
    direction: rtl (when used for layout hacks, not actual RTL language support)
  Review: CSS that changes visual order should not break tab focus sequence
  Exception: display: none or visibility: hidden (removes from focus order entirely — acceptable)
```

**Pass criteria:** Grep flags no CSS `order:` property usage that could disrupt tab flow. **Manual verification required:** CSS grep identifies potential issues; actual tab-order behavior must be confirmed by keyboard-tabbing through the page in a browser. Automated check is necessary but not sufficient.

**Remediation:** Restructure HTML to match desired visual order instead of using CSS `order` property. If `order` is necessary, verify tab sequence matches visual flow via browser testing.

---

## A-09: Touch Targets Minimum Size

**WCAG:** 2.5.8 Target Size Minimum (Level AA)

**Check:** Interactive elements have minimum 44x44px touch target size.

**Method:**
```
Grep in base.css and component CSS:
  Check button, a, input[type="submit"] styles for:
    min-height (should be >= 44px)
    min-width or padding sufficient for 44px minimum
  Specific elements to verify:
    Cart icon link
    Search icon button
    Navigation menu items
    Form submit buttons
    Quantity stepper buttons
```

**Pass criteria:** All interactive elements have at least 44px minimum dimension (height and width).

**Remediation:** Add `min-height: 44px; min-width: 44px;` to button and link base styles in `base.css`. For icon buttons, ensure padding provides adequate touch area.

---

## A-10: Headings Visually Distinct

**WCAG:** 1.3.1 Info and Relationships (Level A)

**Check:** Heading levels h1-h4 are visually distinct from each other and from body text.

**Method:**
```
Grep in base.css:
  Find styles for h1, h2, h3, h4
  Verify: each heading level has a distinct font-size OR font-weight
  Verify: heading styles differ from body text styles
  Minimum: h1, h2, h3, h4 must have at least 4 distinct visual treatments
```

**Pass criteria:** h1, h2, h3, and h4 each have visually distinct styling (size, weight, or both).

**Remediation:** Add distinct heading styles to `base.css`:
```css
h1 { font-size: var(--font-size-h1, 2.5rem); font-weight: 700; }
h2 { font-size: var(--font-size-h2, 2rem); font-weight: 700; }
h3 { font-size: var(--font-size-h3, 1.5rem); font-weight: 600; }
h4 { font-size: var(--font-size-h4, 1.25rem); font-weight: 600; }
```

---

## A-11: ARIA Labels on Icon-Only Buttons

**WCAG:** 4.1.2 Name, Role, Value (Level A)

**Check:** Buttons and links with only icon content have accessible names.

**Method:**
```
Grep across all .liquid files:
  Find <button> and <a> elements that contain only:
    An SVG, an <img>, an icon class, or a Liquid icon snippet render
    No visible text content
  For each: verify aria-label or aria-labelledby is present
  Common icon-only elements: cart button, search button, close button, hamburger menu, social links
```

**Pass criteria:** All icon-only interactive elements have `aria-label` or `aria-labelledby` providing an accessible name.

**Remediation:** Add `aria-label="[action description]"` to icon-only buttons/links. Examples: `aria-label="Open cart"`, `aria-label="Search"`, `aria-label="Close menu"`.

---

## A-12: Skip Navigation Link

**WCAG:** 2.4.1 Bypass Blocks (Level A)

**Check:** A skip-to-main-content link exists for keyboard users.

**Method:**
```
Grep in layout/theme.liquid:
  Pattern: "skip" AND ("main" OR "content")
  Expected: <a> element linking to #main-content or #MainContent
  Verify: target element exists in the page (id="main-content" or id="MainContent")
  The skip link may be visually hidden but must be visible on focus
```

**Pass criteria:** Skip navigation link present in theme.liquid, targeting a main content landmark. Link is visible when focused.

**Remediation:** Add before the header in `theme.liquid`:
```liquid
<a class="skip-to-content-link" href="#MainContent">Skip to content</a>
```
With CSS:
```css
.skip-to-content-link {
  position: absolute;
  top: -100%;
  left: 0;
  z-index: 9999;
}
.skip-to-content-link:focus {
  top: 0;
  background: var(--color-background);
  padding: 1rem;
}
```
And ensure `<main id="MainContent">` exists in the layout.

---

## A-13: `role="alert"` on Runtime-Injected Regions Only

**WCAG:** 4.1.3 Status Messages (Level AA)

**Check:** Live regions (`role="alert"`, `role="status"`, `aria-live`) announce content *changes* to assistive technology. The region must exist in the DOM before the change and render **empty** on load, then be populated by JS at runtime. A live region shipped with static template content announces stale content on load, or nothing at all when the real message arrives.

**Method:**
```
Grep in sections/ and snippets/:
  Pattern: role="alert" | role="status" | aria-live=
  For each match: inspect the container's template body.
    Flag if it carries static or Liquid-interpolated text at render time
    (it should render empty and be filled by JS on the event).
  Manual verification required: confirm the region is updated at runtime
    (form validation error, cart notice, toast) — not present on load.
```

**Pass criteria:** Every live region renders with an empty message slot and is populated at runtime. No static `role="alert"` with baked-in content. The runtime injection path is confirmed by manual test. A confirmed static alert is a WCAG 4.1.3 defect.

**Remediation:** Keep the empty container in markup; inject the message via JS.
```html
<!-- Correct: empty on load, JS sets textContent on the event -->
<div role="alert" aria-live="assertive" class="form-status" hidden></div>
```
```js
statusEl.hidden = false;
statusEl.textContent = "Please enter a valid email.";
```

---

## A-14: Focus Returns on Dismiss

**WCAG:** 2.4.3 Focus Order (Level A)

**Check:** When a dismissible overlay (modal, dialog, drawer, cart, menu, toast) is closed, focus must return to the control that opened it — or a documented fallback — never lost to `<body>`. Focus lost to the top of the page after closing a dialog strands keyboard and screen-reader users.

**Method:**
```
Grep in sections/ and assets/ JS:
  Pattern: close / dismiss / [data-close] / aria-modal / <dialog / .hide(
  Static analysis flags the presence of a dismiss handler; it CANNOT
    verify the focus-return behavior.
  Manual verification required: keyboard-open the overlay, then close it,
    and confirm focus returns to the trigger (or a sensible fallback).
```

**Pass criteria:** On dismiss, focus moves to the invoking control or a documented fallback element. Focus is never dropped to `<body>`. Lost focus on dismiss is a WCAG 2.4.3 defect.

**Remediation:** Store the trigger element on open; restore focus to it on close.
```js
let opener;
function openOverlay(el){ opener = document.activeElement; /* …show, focus first item… */ }
function closeOverlay(){ /* …hide… */ (opener || document.body).focus(); }
```

---

## A-15: No Redundant ARIA

**WCAG:** 4.1.2 Name, Role, Value (Level A) — the "no ARIA is better than bad ARIA" principle

**Check:** Redundant ARIA duplicates semantics the native element already provides, and can actively harm — an `aria-label` that merely restates visible text breaks voice-control ("click <visible text>" no longer matches the accessible name).

**Method:**
```
Grep in sections/, snippets/, layout/:
  Redundant role on a native element:
    role="button"     on <button>
    role="link"       on <a href>
    role="list"       on <ul> or <ol>
    role="listitem"   on <li>
    role="navigation" on <nav>
    role="main"       on <main>
    role="banner"     on <header> (top-level)
  Redundant name:
    aria-label on an element whose visible text already names it
  Flag each occurrence.
```

**Pass criteria:** No role duplicates a native implicit role. No `aria-label` overrides or duplicates adjacent visible text. This is an anti-pattern flag (Warning), not a hard block — but an `aria-label` contradicting visible text is a real defect.

**Remediation:** Remove the redundant `role`; drop the `aria-label` where visible text already provides the accessible name. Reserve `aria-label` for genuinely nameless controls (icon-only buttons — see A-11).

*HeyHi Confidential*
