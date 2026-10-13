# GEO Readiness Reference

*Zone 2 — on-demand. Load before delivery handoff on any content-bearing ui-studio build, alongside `web-quality.md`. Skip for single-page tools, internal admin UIs, and pure prototypes that will never be public.*

*Parent: `engineering-handoff/geo-ui-studio-integration-2026-06-02.md` § B3 (GEO readiness gate). The originating research plan was never written to disk; the two engineering-handoff geo docs are its surviving distillation.*

---

## What this reference is

A pre-handoff verification pass that confirms a ui-studio deliverable is **extractable by the systems that mediate generative discovery** — ChatGPT/SearchGPT, Google AI Overviews/Mode, Perplexity, Claude web search, Copilot. Sits inside the existing *Evaluation Before Deployment* invariant, alongside the WCAG and token-fidelity gates. Not a separate ceremony.

## What this reference is not

- **Not a citation-prediction tool.** No one can verify in advance that a page will be cited. This gate verifies extractability — the necessary upstream of citation.
- **Not a content quality gate.** Content quality (structure, sourcing, voice) is owned by `heyhi-content-writer`. This is a structural/infrastructural gate.
- **Not a duplicate of WCAG or fidelity checks.** Those gates remain; GEO readiness runs alongside them.

## The eight-item checklist

Run all eight against the **deployed** URL, not localhost. CDN, WAF, and prerender pipelines behave differently in production. Pass-or-fail per item — any FAIL blocks handoff until resolved.

> **Scope: design + handoff engagements (HeyHi does not deploy).** When HeyHi delivers the prototype and the client's developer builds and deploys, the gate does not run at build time; carry it as a handoff requirement and split the eight items by owner. The prototype owns the content-side items by construction: real-HTML structure (1), route-specific title/meta/canonical templates (2), valid JSON-LD scaffolding (3), and one-h1 / no-skipped-levels heading hierarchy (7). Verify these in the static reference and mark them "satisfied, preserve when porting." The developer runs the deploy-side items against the live URL before launch: robots.txt answer-crawler access (4), sitemap accuracy (5), no CDN/WAF block (6), and no orphaned content behind JS (8). Record the split as a table in the dev handoff.

### 1. Real HTML for content

The user-visible content of the page exists in the prerendered HTML, not just after JS execution.

```bash
curl -s "<deployed-url>" | grep -F "<phrase visible to the user on this page>"
```

Returns ≥ 1: **PASS**. Returns 0: **FAIL** — the page is client-rendered for content. Per plan §4, this makes the page invisible to GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, PerplexityBot, and CCBot. Move to SSR / SSG / prerender before shipping.

### 2. Title, meta description, canonical present and route-specific

```bash
curl -s "<deployed-url>" | grep -E "<title>|name=\"description\"|rel=\"canonical\""
```

Three matches expected per route. Each must be route-specific (not a site-wide default), non-empty, and the canonical must resolve to the same URL or a deliberate redirect target.

Returns 3 distinct matches, each populated and correct: **PASS**. Otherwise: **FAIL**.

### 3. Schema.org JSON-LD present and valid

At minimum: Organization on the home route. On article/log/blog routes: BlogPosting (or Article). Where applicable per the build: ProfessionalService, Person, BreadcrumbList, FAQPage.

Inspect the prerendered HTML for `<script type="application/ld+json">` blocks, then paste each into https://validator.schema.org/. All blocks valid: **PASS**. Any invalid block: **FAIL**.

Common failures: missing required fields, `@id` mismatches between cross-referenced entities (Organization `@id` vs. Person.worksFor `@id`), URLs that don't resolve, FAQPage emitted on a non-FAQ page.

### 4. robots.txt allows answer crawlers

The deployed `robots.txt` must explicitly allow (or not disallow) the answer/search crawlers.

```bash
curl -s "<deployed-host>/robots.txt"
```

Verify each of the following is **not** under a `Disallow: /` block:
- `Googlebot`
- `OAI-SearchBot`
- `ChatGPT-User`
- `Claude-SearchBot`
- `Claude-User`
- `PerplexityBot`
- `Perplexity-User`
- `Applebot`

All allowed (or not mentioned with a default `User-agent: *` `Allow: /`): **PASS**. Any one Disallowed by accident: **FAIL** — the site has opted itself out of that engine's answers.

Common failure: a `User-agent: *` `Disallow: /` block written years ago for staging, never removed in production. Or a blanket "block all bots" rule that swept up the answer crawlers along with scrapers.

### 5. Sitemap accurate

```bash
curl -sI "<deployed-host>/sitemap.xml" | head -1
```

Returns `200 OK`: **PASS** for the first check.

Then sample at least 3 URLs from the sitemap and verify each resolves to a 200 with the expected content:

```bash
curl -sI "<sample-url-1>" | head -1
curl -sI "<sample-url-2>" | head -1
curl -sI "<sample-url-3>" | head -1
```

All three 200: **PASS**. Any 404, 5xx, or redirect to an unexpected page: **FAIL**. Per plan §4, ChatGPT's crawler specifically hit 404s on roughly 35% of fetches in the Vercel/MERJ measurement — generative crawlers are inefficient at URL selection in general, so an accurate sitemap is more load-bearing here than for Googlebot.

### 6. No CDN / WAF block above the robots.txt layer

robots.txt allows a crawler, but the upstream firewall might silently 403 it. Confirm with synthetic user-agent fetches:

```bash
curl -sI -A "OAI-SearchBot/1.0" "<deployed-url>" | head -1
curl -sI -A "PerplexityBot/1.0" "<deployed-url>" | head -1
curl -sI -A "GPTBot/1.0" "<deployed-url>" | head -1
curl -sI -A "ClaudeBot/1.0" "<deployed-url>" | head -1
```

All 200: **PASS**. Any 403, 429, or unexpected redirect: **FAIL** — investigate Vercel/Cloudflare/Fastly WAF rules, bot-management settings, and rate-limit configuration.

Common failure: Vercel "Bot Protection" or Cloudflare "Bot Fight Mode" enabled at a tier that challenges/blocks unknown bots, which includes answer crawlers.

### 7. Semantic heading hierarchy

Exactly one `<h1>` per route. `<h2>` and below in sequence, no skipped levels (no `<h2>` followed directly by `<h4>`).

```bash
curl -s "<deployed-url>" | grep -oE "<h[1-6][^>]*>" | sort | uniq -c
```

Exactly one `<h1>`, then `<h2>`, `<h3>` etc. in sequence with no gaps: **PASS**. Multiple `<h1>` (common in SPA-converted templates where the page title and a section title both render as h1) or skipped levels: **FAIL**.

### 8. No orphaned content behind JS

For at least 3 representative content routes (home, an article/log, a service/product page), verify that the prose users see is in the view-source, not just the runtime DOM.

```bash
curl -s "<deployed-url>" | wc -c        # Total bytes
curl -s "<deployed-url>" | grep -F "<phrase from each page>"
```

The grep returns at least one hit on each: **PASS**. If the byte count is suspiciously low (< 10 KB on a content page) and the grep returns 0, the page is shipping a JS shell: **FAIL**. Same fix as #1 — SSR / SSG / prerender.

---

## Output: pass-or-block summary

Record the result of each item as `PASS` or `FAIL` with the offending URL and the specific failure mode. The handoff doc carries this as a single block:

```
GEO Readiness Gate: <date>
  1. Real HTML for content              PASS
  2. Title/meta/canonical               PASS
  3. JSON-LD valid                      PASS
  4. robots.txt allows answer crawlers  PASS
  5. Sitemap accurate                   PASS
  6. No CDN/WAF block                   PASS
  7. Heading hierarchy                  PASS
  8. No orphaned content behind JS      PASS
  Gate: PASSED — build cleared for delivery.
```

Or, on failure:

```
GEO Readiness Gate: <date>
  1. Real HTML for content              FAIL
       — /pricing returns empty <main>; content appears only after
         hydration. Recommended fix: enable prerender for /pricing
         in <build config>. Rerun after.
  ...
  Gate: BLOCKED — see item 1. Build does not ship until resolved.
```

## What to do with the result

- **All PASS:** clear for delivery handoff. Note the gate result in the engagement record.
- **Any FAIL:** the build does not ship until the failing item is resolved. The fixes are mechanical, not judgment calls — none of these eight items is a matter of taste.

## Cross-references

- Eight-item rationale: `engineering-handoff/geo-ui-studio-integration-2026-06-02.md` § B1 (real HTML); `engineering-handoff/geo-website-handoff-2026-06-02.md` § A1 (crawler taxonomy → robots.txt) and § A2 (schema as entity clarity).
- Routing: ui-studio Phase 7 Quality Gate in `engineering-handoff/website-generation-runbook.md`.
- Skill candidate: `heyhi-geo-readiness` in `heyhi-skills/CANDIDATES.md` — when this checklist runs ≥ 2 engagements, promote to a skill.

---

*HeyHi Internal Use Only. ui-studio Zone 2 reference. On-demand load — content-site builds only.*
