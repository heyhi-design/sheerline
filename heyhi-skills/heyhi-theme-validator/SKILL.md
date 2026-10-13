---
name: heyhi-theme-validator
description: >-
  Runs a structured pre-submission checklist against a completed Shopify theme directory. Three validation profiles: Feature Completeness (25 required features), Code Standards (13 code rules), Accessibility Audit (15 checkpoints). Returns a structured pass/fail/warning report with specific remediation steps per finding. Three mode contexts: A (Theme Store — all checks blocking), B (Client Custom — relaxed submission requirements), C (Section — targeted check scope). Use before any theme delivery or submission. Not for: generating themes (use heyhi-shopify-theme), brand token extraction (use design-system-onboard), or pipeline config validation (use heyhi-pipeline-validator).
---

# Theme Validator

Structured pre-submission checklist for Shopify theme directories. Runs one or more validation profiles, aggregates findings, and produces a report with a clear verdict and prioritized remediation list — before any delivery or Theme Store submission.

---

> **Exit Gate (Flavor A).** This skill closes through the canonical Exit Gate — see `CLAUDE-SESSION-RULES.md § Exit Gate`. Required headers, in order: `## Fixes Applied`, `## Smoke Test`, `## Next Session Prompt`. Empty headers are visible failures.


## Scope Boundary: V-1 Detection + V-2 Calibration

This skill is a **validated detection system with output calibration complete** (V-2, conditional).

- **V-1 (2026-03):** Detection capability validated against the Shopify Skeleton Theme. Test 1 (Skeleton baseline) confirms the validator produces structured reports and correctly categorizes known states. Test 2 (mutation testing) confirms the validator catches deliberately introduced violations. Test 3 (mode behavior) confirms blocking/warning/skip logic across Modes A, B, and C.
- **V-2 (complete 2026-03-30):** Output calibration ran against the first complete HeyHi-generated theme — CONDITIONAL PASS 46/50 (0 failures, 4 warnings, 0 skipped; authority: `project-state.yaml` heyhi-theme-validator notes). FAIL-accuracy and PASS-accuracy verified at that bar. A PASS result still means "no detected issues" — not a guarantee that the theme will pass Shopify Theme Store review.

State this V-1/V-2 status in any report this skill produces. Do not claim the validator is a Theme Store review guarantee — it is a calibrated detection system, and the V-2 pass was conditional.

---

## Validation Architecture

```
[Theme Directory]
        ↓
  Mode Context Check (A / B / C)
  (determines which checks are blocking vs. warning)
        ↓
  Profile 1: Feature Completeness (25 checks)
  (all required Shopify OS 2.0 features present)
        ↓
  Profile 2: Code Standards (13 checks)
  (Shopify Theme Store code requirements)
        ↓
  Profile 3: Accessibility Audit (15 checkpoints)
  (WCAG 2.1 AA minimum; AAA for civic/government)
        ↓
  ── HUMAN GATE: Operator Reviews Report ──
        ↓
  [Proceed / Return for Remediation]
```

Profiles are independent — run one, two, or all three depending on the `profile` input. All three are required before any Mode A (Theme Store) submission.

---

## What You Need Before Starting

**Required for all modes:**
1. A path to the theme directory (local filesystem or unpacked .zip)
2. Profile selection: `1`, `2`, `3`, or `all`
3. Mode context: `A` (Theme Store), `B` (Client Custom), or `C` (Section)

**Optional but recommended:**
- `theme-config.json` — provides theme name, version, and style entry for the report header
- `active-brand.json` — used by Profile 3 to verify contrast tokens against declared values

**Reference files (load only when relevant):**
- `heyhi-skills/heyhi-theme-validator/references/feature-checklist.md` — full feature list with check methods
- `heyhi-skills/heyhi-theme-validator/references/code-standards.md` — code audit rules
- `heyhi-skills/heyhi-theme-validator/references/accessibility-checkpoints.md` — all 15 checkpoints with pass criteria

---

## Mode Context

Mode context determines whether a failing check is **blocking** (stops delivery) or a **warning** (flagged, operator decides).

| Mode | Context | Blocking Checks | Warning Checks |
|------|---------|-----------------|----------------|
| **A** | Theme Store submission | All Profile 1 + 2 + 3 failures | None — all failures block |
| **B** | Client custom delivery | Profile 2 code violations; Profile 3 contrast failures | Profile 1 optional features (Selling Plans, Unit Pricing, Shop Pay Installments) |
| **C** | Single section | Section-level code standards only | Feature completeness N/A; accessibility warnings only |

When running Mode C, skip Profile 1 entirely (feature completeness is whole-theme scope). Run Profile 2 checks that apply to a single section file. Run Profile 3 checks that apply to the section's markup.

---

## Profile 1: Feature Completeness

**Purpose:** Verify all required Shopify OS 2.0 features are implemented before submission. Each check has a specific verification method — "it looks like it's there" is not a pass.

**What to check:**

| # | Feature | Check Method | Blocking? |
|---|---------|-------------|-----------|
| F-01 | Sections Everywhere (OS 2.0) | All templates are `.json` (not `.liquid`) except `gift_card.liquid` and `customers/*.liquid` | A: Yes / B: Yes / C: N/A |
| F-02 | Discounts | `cart.liquid` includes discount code `<input>` + display block | A: Yes / B: Yes / C: N/A |
| F-03 | Accelerated Checkout | `product.json` schema blocks has `"type": "main-product"` with accelerated checkout block present | A: Yes / B: Warning / C: N/A |
| F-04 | Faceted Search | `collection` + `search` templates include `facets.liquid` snippet | A: Yes / B: Warning / C: N/A |
| F-05 | Gift Cards | `gift_card.liquid` exists; includes Apple Wallet + QR code output | A: Yes / B: Warning / C: N/A |
| F-06 | Image Focal Points | Image render calls use `focal_point` attribute | A: Yes / B: Yes / C: N/A |
| F-07 | Social Sharing Images | `theme.liquid` has `page_image` meta tag | A: Yes / B: Warning / C: N/A |
| F-08 | Multi-Currency/Language | `country-localization.liquid` snippet exists; referenced in header section | A: Yes / B: Warning / C: N/A |
| F-09 | Multi-Level Menus | Header section schema has `linklist` + `link_list` inputs with depth support | A: Yes / B: Yes / C: N/A |
| F-10 | Newsletter Forms | `newsletter.liquid` section exists; uses `form_type: 'customer'` | A: Yes / B: Yes / C: N/A |
| F-11 | Pickup Availability | `main-product.liquid` has `store-availability` block | A: Yes / B: Warning / C: N/A |
| F-12 | Product Recommendations | `"type": "product-recommendations"` block in `main-product.liquid` schema OR standalone `sections/product-recommendations.liquid` with `/recommendations/products.json` API integration | A: Yes / B: Warning / C: N/A |
| F-13 | Rich Media (3D/Video) | Product media gallery handles `model` + `video` + `image` media types | A: Yes / B: Warning / C: N/A |
| F-14 | Search + Predictive | `predictive-search.liquid` snippet exists; uses `/search/suggest` API | A: Yes / B: Warning / C: N/A |
| F-15 | Selling Plans | Cart shows selling plan info; product page displays selling plan options | A: Yes / B: Warning / C: N/A |
| F-16 | Shop Pay Installments | Product page includes `shop-pay-installments-banner` | A: Yes / B: Warning / C: N/A |
| F-17 | Unit Pricing | `price.liquid` handles `unit_price_measurement` | A: Yes / B: Warning / C: N/A |
| F-18 | Variant Images | Variant picker triggers media gallery swap. **Manual verification required** — grep confirms variant-media JS wiring exists; actual swap behavior requires browser test | A: Yes / B: Yes / C: N/A |
| F-19 | Follow on Shop | `theme.liquid` includes `login_button` filter output | A: Yes / B: Warning / C: N/A |
| F-20 | Custom Liquid Section | `sections/custom-liquid.liquid` exists with `type: liquid` input | A: Yes / B: Yes / C: N/A |
| F-21 | App Blocks | `main-product.liquid` schema has `blocks: [{type: "@app"}]` | A: Yes / B: Warning / C: N/A |
| F-22 | 11 Required JSON Templates | All 11 `.json` templates present in `/templates/` | A: Yes / B: Yes / C: N/A |
| F-23 | `theme.liquid` | `layout/theme.liquid` present; `lang` attribute set | A: Yes / B: Yes / C: N/A |
| F-24 | `gift_card.liquid` | `templates/gift_card.liquid` present with QR + wallet output | A: Yes / B: Yes / C: N/A |
| F-25 | `settings_schema.json` | `config/settings_schema.json` present + valid JSON | A: Yes / B: Yes / C: N/A |

**Profile 1 Verdict:**
- **PASS:** All Mode A checks pass (or all applicable checks for Mode B/C)
- **CONDITIONAL PASS:** Zero blocking failures; one or more warnings present
- **FAIL:** Any blocking check fails

---

## Profile 2: Code Standards

**Purpose:** Verify the theme meets Shopify's code submission standards. Many of these are automated grep/glob checks — run them mechanically, not by visual inspection.

**What to check:**

| # | Check | Method | Blocking? |
|---|-------|--------|-----------|
| C-01 | No `.scss` files | Glob `**/*.scss` in all directories → must return empty | A: Yes / B: Yes / C: Yes |
| C-02 | No minified CSS/JS | Check `.css` and `.js` files for lines exceeding 500 characters; minified files will have very long single lines | A: Yes / B: Yes / C: Yes |
| C-03 | No hardcoded `http://` | Grep for `http://` in all `.liquid` + `.js` files | A: Yes / B: Yes / C: Yes |
| C-04 | No `src="//` without `https` | Grep for `src="//` not preceded by `https` | A: Yes / B: Yes / C: Yes |
| C-05 | Valid semantic HTML structure | Check `theme.liquid` for proper `<html>`, `<head>`, `<body>` nesting; no block elements inside inline elements | A: Yes / B: Yes / C: Warning |
| C-06 | `lang` attribute on `<html>` | `theme.liquid`: `<html lang="{{ request.locale.iso_code }}">` — exact pattern | A: Yes / B: Yes / C: N/A |
| C-07 | `routes` object used | Grep for hardcoded `/collections/`, `/products/` path strings in Liquid/JS; any found must use `routes.*` equivalents instead | A: Yes / B: Warning / C: Warning |
| C-08 | `rel="nofollow"` on Shopify links | Grep for `shopify.com` links → all must have `rel="nofollow"` | A: Yes / B: Yes / C: Yes |
| C-09 | No `robots.txt.liquid` | `templates/robots.txt.liquid` must NOT exist | A: Yes / B: Yes / C: N/A |
| C-10 | No `config/markets.json` | `config/markets.json` must NOT exist | A: Yes / B: Yes / C: N/A |
| C-11 | No app-dependent functionality | **Manual verification required.** Automated assist: grep for external API calls and app-specific metafield namespaces. Operator must verify no core feature depends on a third-party app | A: Yes / B: Warning / C: Warning |
| C-12 | `theme_info` block present | `settings_schema.json` first element has `"name": "theme_info"` with theme_name, theme_version, theme_author, theme_documentation_url | A: Yes / B: Yes / C: N/A |
| C-13 | Favicon setting present | `settings_schema.json` has `type: image_picker, id: favicon` | A: Yes / B: Yes / C: N/A |

**Profile 2 Verdict:**
- **PASS:** All applicable checks pass
- **CONDITIONAL PASS:** Warnings only; no blocking failures in Mode A; operator must review in Mode B
- **FAIL:** Any blocking check fails

---

## Profile 3: Accessibility Audit

**Purpose:** Verify the theme meets WCAG 2.1 AA minimum accessibility requirements. Contrast checks require a live render or reference to `active-brand.json` token values — do not skip them.

**What to check:**

| # | Checkpoint | Implementation Check | Blocking? |
|---|------------|---------------------|-----------|
| A-01 | Keyboard accessible (all elements) | All interactive elements use `<a href>` or `<button>` — not `<div>` with `onclick`, `<span>` with `role="button"`, or equivalent | A: Yes / B: Yes / C: Yes |
| A-02 | Visible focus states | `base.css` has `:focus-visible` styles for `a`, `button`, `input`; styles are not `outline: none` | A: Yes / B: Yes / C: Yes |
| A-03 | Alt attributes on all images | All `<img>` tags have `alt="{{ image.alt | escape }}"` pattern; decorative images have `alt=""` | A: Yes / B: Yes / C: Yes |
| A-04 | Form input-label association | All `<input>` has `id`; matching `<label for="[id]">` present; no orphan inputs | A: Yes / B: Yes / C: Yes |
| A-05 | Valid HTML nesting | Best-effort static check: no unclosed tags in non-conditional markup; heading hierarchy sequential. **Caveat:** Liquid conditionals may produce valid HTML in both branches but static analysis cannot verify all paths | A: Yes / B: Yes / C: Yes |
| A-06 | Text contrast 4.5:1 (body) | **Requires computation:** Parse color values from `settings_data.json` or `active-brand.json`, compute WCAG relative luminance ratio. Use formula: L = 0.2126*R + 0.7152*G + 0.0722*B (linearized). Ratio = (L1 + 0.05)/(L2 + 0.05) ≥ 4.5:1 | A: Yes / B: Yes / C: Warning |
| A-07 | Text contrast 3:1 (large text) | **Requires computation:** Same luminance formula as A-06. Ratio ≥ 3:1 for heading text (≥ 24px regular or ≥ 18.67px bold) against background | A: Yes / B: Yes / C: Warning |
| A-08 | Focus order matches DOM order | Grep for CSS `order:` property usage. **Manual verification required** for actual tab-order behavior — CSS grep flags potential issues, browser testing confirms | A: Yes / B: Warning / C: Warning |
| A-09 | Touch targets minimum size | All buttons and links have `min-height: 44px` in CSS; verify in `base.css` and section-specific CSS | A: Yes / B: Yes / C: Yes |
| A-10 | Headings visually distinct h1-h6 | `base.css` has distinct font-size or weight styles for `h1` through `h4` at minimum; heading levels are not visually identical | A: Yes / B: Yes / C: Warning |
| A-11 | ARIA labels on icon-only buttons | All icon-only `<button>` and `<a>` elements have `aria-label` or `aria-labelledby`; no unlabeled icon interactions | A: Yes / B: Yes / C: Yes |
| A-12 | Skip navigation link | `theme.liquid` contains a skip-to-main-content link targeting `#MainContent`; link visible on `:focus` | A: Yes / B: Warning / C: N/A |
| A-13 | `role="alert"` on runtime-injected regions only | Grep for `role="alert"` / `role="status"` / `aria-live`. Flag any live region that carries **static** template text (it should render empty and be populated by JS at runtime — a static alert announces stale content or nothing). **Manual verification required:** confirm the region is injected/updated at runtime, not present on load. A confirmed static `role="alert"` is a WCAG 4.1.3 defect | A: Warning / B: Warning / C: Warning |
| A-14 | Focus returns on dismiss | Grep for modal / drawer / cart / menu / dialog close handlers. **Manual verification required:** when the overlay is dismissed, focus returns to the control that opened it (or a sensible fallback), not lost to `<body>`. Static analysis flags the dismiss handler; browser + keyboard testing confirms the focus return. Lost focus on dismiss is a WCAG 2.4.3 defect | A: Warning / B: Warning / C: Warning |
| A-15 | No redundant ARIA | Grep for role that duplicates a native implicit role (`role="button"` on `<button>`, `role="link"` on `<a href>`, `role="list"` on `<ul>`/`<ol>`, `role="navigation"` on `<nav>`, `role="main"` on `<main>`) and for `aria-label` that merely restates adjacent visible text. Flag each — no ARIA is better than redundant ARIA (an `aria-label` overriding visible text can break voice control). Anti-pattern flag, not a hard block | A: Warning / B: Warning / C: Warning |

**Profile 3 Verdict:**
- **PASS:** All applicable checks pass
- **CONDITIONAL PASS:** Warnings only; blocking failures addressed
- **FAIL:** Any blocking check fails in Mode A or B

---

## Workflow

Run profiles in order. Record each check result independently.

### Step 1: Validate Theme Directory Structure

Before running any profile, confirm:

- [ ] Theme directory exists at the provided path
- [ ] `layout/theme.liquid` is present
- [ ] `config/settings_schema.json` is present
- [ ] `/templates/` directory exists and contains `.json` files
- [ ] `/sections/` directory exists and is non-empty

If the directory structure is incomplete, stop and report:

```
Theme directory at [path] is missing required structure.
Cannot run validation.

Missing: [list]

Resolve the directory structure before running the validator.
```

Do not attempt profile checks against an incomplete directory.

### Step 2: Run Selected Profile(s)

Run each selected profile check-by-check. For each check, record:
- Check number and name
- Result: **PASS** / **FAIL** / **WARN** / **SKIP**
- Evidence: the specific file path, line, or grep result that determined the result
- Remediation: exact fix when FAIL or WARN

Do not summarize check results in bulk — each check gets its own row in the report table.

### Step 3: Aggregate Results

After all profiles complete:

- Count blocking failures (Mode A) or all failures (Mode B/C)
- Count warnings
- Determine overall verdict per the three-tier rubric:
  - **PASS:** Zero failures, zero or more warnings
  - **CONDITIONAL PASS:** Zero blocking failures; warnings present
  - **FAIL:** One or more blocking failures

### Step 4: Generate Report

Produce the structured markdown report using the template at `heyhi-skills/heyhi-theme-validator/templates/report-template.md`.

Include:
- Per-profile results tables with every check (not just failures)
- Overall verdict with counts
- Remediation priority list ordered by impact

### Step 5: Human Gate

After delivering the report, present the verdict to the operator:

```
Theme Validator: [Theme Name] — [PASS / CONDITIONAL PASS / FAIL]

Profile 1: [PASS / FAIL / N/A] | Profile 2: [PASS / FAIL / N/A] | Profile 3: [PASS / FAIL / N/A]
Blocking issues: [count]
Warnings: [count]

[If FAIL or CONDITIONAL PASS:] Priority remediation list is in the report above.

Confirm to proceed with delivery/submission, or return for corrections first?
```

Wait for explicit confirmation before declaring the theme delivery-ready. Do not proceed without it.

---

## Correction Paths

### Profile 1 Failure

| Failure Type | Correction Path |
|-------------|----------------|
| Missing section (e.g., newsletter, custom-liquid) | Add the missing section file + add to relevant template JSON |
| Missing template JSON | Create template `.json` file referencing correct section |
| Missing feature block in section schema | Add the block to the section's `schema.blocks[]` |
| Missing snippet (e.g., country-localization, predictive-search) | Create the snippet; reference it from the appropriate section/template |

### Profile 2 Failure

| Failure Type | Correction Path |
|-------------|----------------|
| `.scss` files found | Remove/convert all `.scss` to plain CSS; add to `assets/` |
| Minified files found | Deobfuscate or replace with readable source; do not use build output directly |
| Hardcoded `http://` URLs | Replace with `https://` or protocol-relative `//` where appropriate |
| Hardcoded paths (`/collections/`) | Replace with `routes.collections_url` Liquid equivalent |
| Missing `lang` attribute | Update `theme.liquid` `<html>` opening tag |
| `robots.txt.liquid` exists | Delete the file — Shopify manages `robots.txt` |
| No `theme_info` in settings schema | Add header section with name, author, version, documentation_url |

### Profile 3 Failure

| Failure Type | Correction Path |
|-------------|----------------|
| `<div onclick>` interactive elements | Replace with `<button>` or `<a href>` with appropriate Liquid render |
| Missing `:focus-visible` styles | Add to `base.css`; do not use `outline: none` without a visible replacement |
| Missing `alt` attributes | Update all `<img>` render calls to include `alt="{{ image.alt | escape }}"` |
| Orphan inputs | Add `id` to input; add matching `<label for="[id]">` |
| Contrast failure | Adjust token values in `settings_data.json`; verify with a contrast ratio tool |
| Touch target too small | Add `min-height: 44px; min-width: 44px` to relevant button/link styles in `base.css` |

---

## Smoke Test Checklist

Before delivering any validation report from this skill, verify:

- [ ] All selected profile checks run and documented (no check skipped; N/A noted for Mode C non-applicable checks)
- [ ] Each check result states PASS / FAIL / WARN / SKIP with specific evidence (not "looks correct")
- [ ] Mode context applied correctly — blocking vs. warning status matches Mode A / B / C rules per check
- [ ] Directory structure validation complete before profile checks run
- [ ] Remediation steps are specific (file path, exact fix) — not generic ("add the missing element")
- [ ] Overall verdict follows three-tier rubric (PASS / CONDITIONAL PASS / FAIL)
- [ ] Human gate block present after report delivery — do not auto-proceed
- [ ] V-1/V-2 scope boundary stated in report header (detection validated; V-2 output calibration complete 2026-03-30, CONDITIONAL PASS 46/50 — not a Theme Store certification)
- [ ] No standalone "AI" in report output
- [ ] No banned words (leverage, unlock, seamless, revolutionize, etc.)
- [ ] Em dashes: maximum 2 in any output generated by this skill
- [ ] No pricing in output
- [ ] **Classification comments stripped from repo files before public submission.** The DES-004 batch pass (2026-03-31) added `# HeyHi Confidential` comments to `.github/workflows/*.yml` and `.theme-check.yml` files inside `themes/`. These comments are appropriate while files are in the internal Bay Design folder, but must be removed before the theme repo goes public or is submitted to the Theme Store. Check: `grep -r "HeyHi Confidential" <theme-dir>/.github` and `grep "HeyHi Confidential" <theme-dir>/.theme-check.yml` — both should return empty.

---

## Reference Files

Load when relevant, not by default:

- `heyhi-skills/heyhi-theme-validator/references/feature-checklist.md` — full feature list with check methods and verification steps (Profile 1)
- `heyhi-skills/heyhi-theme-validator/references/code-standards.md` — code audit rules with grep patterns (Profile 2)
- `heyhi-skills/heyhi-theme-validator/references/accessibility-checkpoints.md` — all checkpoints with pass criteria and contrast ratio lookup (Profile 3)
- `heyhi-skills/heyhi-theme-validator/templates/report-template.md` — report output template

---

## Exit Gate Required Headers (bottom-of-skill bracket)

This skill closes through the Exit Gate Flavor A (`CLAUDE-SESSION-RULES.md § Exit Gate`). Before declaring done, confirm every required header below contains real content, not a claim:

- `## Fixes Applied`
- `## Smoke Test`
- `## Next Session Prompt`

If any header is empty or contains advisory prose ("I checked for bugs") instead of a concrete artifact, the gate has not been satisfied. Apply fixes until clean — then emit.

---

*HeyHi Confidential — Skill internal methodology. Not for client distribution.*

*Theme workstream skill. Sits before any Shopify theme delivery or Theme Store submission. V-1: FAIL-detection validated against Skeleton Theme. V-2 calibration complete 2026-03-30 — CONDITIONAL PASS 46/50.*

*Bay Design LLC d/b/a HeyHi · Built March 2026 · Session V-1*
