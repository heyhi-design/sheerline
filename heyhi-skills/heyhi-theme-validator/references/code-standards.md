---
title: "Code Standards Checklist — Profile 2"
profile: 2
checks: 13
version: "1.0.0"
---

# Profile 2: Code Standards Checklist

13 checks verifying Shopify Theme Store code requirements. Most are automated grep/glob checks.

---

## C-01: No .scss Files

**Check:** Theme contains no Sass/SCSS source files.

**Method:**
```
Glob: **/*.scss across entire theme directory
Expected: zero matches
```

**Pass criteria:** No `.scss` files anywhere in the theme.

**Auto-fix:** No (requires manual conversion to CSS).

**Common failures:** Build artifacts left in assets/; source files committed alongside compiled CSS.

**Remediation:** Remove all `.scss` files. If styles were authored in Sass, compile to CSS and include only the compiled output in `assets/`.

---

## C-02: No Minified CSS/JS

**Check:** No minified or obfuscated CSS or JavaScript files.

**Method:**
```
For each .css and .js file in assets/:
  Read file, check for lines exceeding 500 characters
  If any line > 500 chars AND file has fewer than 10 lines → likely minified
  Exception: third-party vendor files may be flagged — operator reviews
```

**Pass criteria:** No CSS or JS file appears minified (readable, formatted source code).

**Auto-fix:** No (requires source code).

**Common failures:** Build pipeline outputs minified bundles; vendor libraries included in minified form.

**Remediation:** Replace minified files with readable source. Shopify handles minification at serve time. Do not include build tool output.

---

## C-03: No Hardcoded http://

**Check:** No insecure HTTP URLs in Liquid or JavaScript files.

**Method:**
```
Grep across all .liquid and .js files:
  Pattern: "http://" (literal string)
  Exclude: comments (lines starting with // or {%- comment -%})
  Expected: zero matches
```

**Pass criteria:** No `http://` URLs in any Liquid or JS file (comments excluded).

**Auto-fix:** Yes — replace `http://` with `https://`.

**Common failures:** Hardcoded URLs to external resources; example code in comments not excluded from grep.

**Remediation:** Replace all `http://` with `https://`. If the resource doesn't support HTTPS, remove the reference.

---

## C-04: No Protocol-Relative src

**Check:** No `src="//` without explicit `https:` prefix.

**Method:**
```
Grep across all .liquid and .js files:
  Pattern: 'src="//' NOT preceded by 'https:'
  Expected: zero matches
```

**Pass criteria:** No protocol-relative `src` attributes.

**Auto-fix:** Yes — prefix with `https:`.

**Common failures:** CDN resources loaded with `//cdn.example.com`; legacy pattern from mixed HTTP/HTTPS era.

**Remediation:** Replace `src="//` with `src="https://`.

---

## C-05: Valid Semantic HTML Structure

**Check:** theme.liquid has proper HTML document structure.

**Method:**
```
Grep in layout/theme.liquid:
  Required elements (in order):
    <!doctype html> OR <!DOCTYPE html>
    <html
    <head>
    </head>
    <body>
    </body>
    </html>
  No block elements (<div>, <section>, <article>) inside inline elements (<span>, <a>)
```

**Pass criteria:** Proper HTML5 document structure with correct element nesting.

**Auto-fix:** No (structural).

**Common failures:** Missing doctype; `<body>` content before `</head>`; block elements inside inline.

**Remediation:** Restructure `theme.liquid` to follow standard HTML5 document order.

---

## C-06: lang Attribute on html

**Check:** The `<html>` tag includes a dynamic language attribute.

**Method:**
```
Grep in layout/theme.liquid:
  Pattern: '<html.*lang=.*request.locale.iso_code'
  Exact expected: <html lang="{{ request.locale.iso_code }}"
```

**Pass criteria:** `<html>` tag has `lang="{{ request.locale.iso_code }}"` (dynamic, not hardcoded).

**Auto-fix:** Yes — add or replace lang attribute.

**Common failures:** `lang="en"` hardcoded; lang attribute missing entirely; using wrong Liquid variable.

**Remediation:** Set `<html lang="{{ request.locale.iso_code }}">` in theme.liquid.

---

## C-07: Routes Object Used

**Check:** No hardcoded URL paths; uses Shopify's `routes` object instead.

**Method:**
```
Grep across all .liquid files:
  Patterns to flag:
    href="/collections/" (should be routes.collections_url)
    href="/products/" (should be routes.root_url + product handle)
    href="/cart" (should be routes.cart_url)
    href="/search" (should be routes.search_url)
    href="/account" (should be routes.account_url)
  Exclude: schema JSON blocks, comments, and strings inside {% schema %}
```

**Pass criteria:** No hardcoded URL paths for standard Shopify routes in Liquid templates.

**Auto-fix:** Partial — can suggest replacements but context-dependent.

**Common failures:** `/collections/` in navigation links; `/cart` in header cart icon link; `/search` in search form action.

**Remediation:** Replace hardcoded paths with `routes.*` equivalents: `{{ routes.collections_url }}`, `{{ routes.cart_url }}`, `{{ routes.search_url }}`, `{{ routes.account_url }}`.

---

## C-08: rel="nofollow" on Shopify Links

**Check:** All links to shopify.com have `rel="nofollow"`.

**Method:**
```
Grep across all .liquid files:
  Step 1: Find all links containing "shopify.com"
  Step 2: For each match, verify rel="nofollow" is present
  Any shopify.com link without rel="nofollow" → FAIL
```

**Pass criteria:** Every `<a>` linking to shopify.com includes `rel="nofollow"`.

**Auto-fix:** Yes — add `rel="nofollow"` to matching links.

**Common failures:** "Powered by Shopify" footer link missing nofollow; attribution links missing the attribute.

**Remediation:** Add `rel="nofollow"` to all `<a href="...shopify.com...">` tags.

---

## C-09: No robots.txt.liquid

**Check:** Theme does not include a robots.txt template.

**Method:**
```
File exists check: templates/robots.txt.liquid
Expected: file does NOT exist
```

**Pass criteria:** `templates/robots.txt.liquid` does not exist in the theme.

**Auto-fix:** Yes — delete the file.

**Common failures:** File carried over from older theme versions; manually created for SEO customization.

**Remediation:** Delete `templates/robots.txt.liquid`. Shopify manages robots.txt at the platform level.

---

## C-10: No config/markets.json

**Check:** Theme does not include a markets configuration file.

**Method:**
```
File exists check: config/markets.json
Expected: file does NOT exist
```

**Pass criteria:** `config/markets.json` does not exist in the theme.

**Auto-fix:** Yes — delete the file.

**Common failures:** File generated by development tools or theme export.

**Remediation:** Delete `config/markets.json`. Markets configuration is managed through Shopify admin, not the theme.

---

## C-11: No App-Dependent Functionality

**Check:** Core theme functionality does not depend on any third-party Shopify app being installed.

**Method:**
```
Manual review with automated assist:
  Grep across all .liquid and .js files:
    Patterns to flag:
      "app_block" (check context — @app block type is fine, app-specific logic is not)
      External API calls to non-Shopify domains
      Metafield references to app-specific namespaces
  Operator must verify: does removing any app break core theme functionality?
```

**Pass criteria:** All core theme features work without any third-party app installed. `@app` block support (F-21) is required, but no specific app can be required.

**Auto-fix:** No (requires architectural review).

**Common failures:** Reviews section depending on a reviews app; wishlist functionality requiring an app; product customization fields tied to app metafields.

**Remediation:** Remove or replace app-dependent functionality with native Shopify features or make the feature gracefully degrade when the app is not installed.

---

## C-12: theme_info Section Present

**Check:** settings_schema.json includes a theme_info header section.

**Method:**
```
Parse config/settings_schema.json
Find first element with "name": "theme_info"
Verify it contains: theme_name, theme_version, theme_author, theme_documentation_url
```

**Pass criteria:** First section in settings_schema.json is a theme_info block with name, version, author, and documentation URL.

**Common failures:** theme_info section missing; present but missing documentation_url; not the first element in the array.

**Remediation:** Add as the first element of settings_schema.json:
```json
{
  "name": "theme_info",
  "theme_name": "[Theme Name]",
  "theme_version": "1.0.0",
  "theme_author": "HeyHi",
  "theme_documentation_url": "https://heyhi.design/docs/[theme]",
  "theme_support_url": "https://heyhi.design/theme-support"
}
```

---

## C-13: Favicon Setting Present

**Check:** Theme settings include a favicon image picker.

**Method:**
```
Parse config/settings_schema.json
Search all setting groups for:
  A setting with type: "image_picker" AND id: "favicon"
```

**Pass criteria:** A favicon setting with `type: "image_picker"` and `id: "favicon"` exists in settings_schema.json.

**Common failures:** Favicon setting missing entirely; setting exists but uses wrong type (e.g., `url` instead of `image_picker`); setting ID is not exactly `favicon`.

**Remediation:** Add to the appropriate settings group in settings_schema.json:
```json
{
  "type": "image_picker",
  "id": "favicon",
  "label": "Favicon",
  "info": "Recommended size: 32x32px .png"
}
```

*HeyHi Confidential*
