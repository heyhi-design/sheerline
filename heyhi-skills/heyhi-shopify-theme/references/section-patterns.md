---
title: "Section Patterns — Cluster-to-Section Architecture"
classification: confidential
session: T-1
version: "1.0.0"
created: "2026-03-29"
---

# Section Patterns

The design cluster from active-brand.json determines section structural choices — not just visual token values. This is where HeyHi's style intelligence creates genuine architectural differentiation between themes. A Cluster C theme and a Cluster A theme cannot become the same theme through settings adjustments — the underlying HTML section structure differs.

---

## How to Use This Document

1. Read `brand.cluster` from `active-brand.json`
2. Find the matching cluster section below
3. Apply all structural rules to every section generated in Step 9 of the workflow
4. Structural rules apply in addition to (not instead of) the token and schema requirements in SKILL.md

The cluster creates structural differentiation. The tokens create visual differentiation. Both are required.

---

## Cluster-to-Section Architecture Mapping

| Cluster | Section Architecture Signature |
|---------|-------------------------------|
| **A — Minimal/Refined** | Full-bleed sections separated by generous whitespace. Typography as the primary visual element. Minimal block count. No decorative dividers. Image blocks secondary to text hierarchy. |
| **B — Warm/Human** | Editorial rhythm — alternating text-left/image-right layouts. Sections breathe with extra padding. Block structure emphasizes testimonials and human content. |
| **C — Bold/Distinctive** | Oversized type anchors as section headers. High-contrast section alternation (dark/light). Fewer but larger sections. Grid-breaking elements in hero and feature sections. |
| **D — Technical/Precision** | Dense data-forward layouts. Grid systems over free-form. Table and list structures. Information density is a feature, not a bug. Clear sectional separation without decoration. |
| **E — Organic/Natural** | Textural section backgrounds. Asymmetric block arrangements. Overlapping elements. Generous radius. Motion that feels physical (spring physics). |

---

## Cluster A — Minimal/Refined

**Character:** Restraint as craft. Negative space as signal. Typography leads; imagery serves.

### Structural Rules

**Hero sections:**
- Single full-bleed section with text centered or left-aligned at large type scale
- Maximum 2 blocks: one text block, one optional CTA
- No image overlay gradients — text must contrast cleanly against the background color alone
- No animated entry effects; fade-in at most
- `section_height` default: `large` or `full`

**Content sections:**
- Single-column at mobile; max 2 columns at desktop
- No decorative dividers between sections — whitespace alone creates separation
- Section padding: derive from `spacious` tier regardless of config's spacing_density (Cluster A always breathes)
- `presets[0].blocks` count: maximum 3 blocks per section

**Product grid:**
- Clean grid: 2 columns mobile, 3-4 columns desktop
- Card structure: image → title → price, nothing else
- No hover overlays that obscure the image — use subtle border or shadow only
- Product thumbnail: minimal — no badges, no "quick add" visible on load (reveal on hover at most)

**Typography:**
- Headings carry the section — use oversized h2/h3 for section identity
- Body text narrow-column (max `--content-max-width`) for reading comfort
- No inline icons or bullet decorations — em dashes or whitespace only

**Image placement:**
- Images below text, not above, in most content sections
- Full-bleed images only in dedicated image sections — not mixed with text in the same visual field
- When text overlays an image: black/white background swatch behind text (no gradient)

### Section-Specific Rules (Cluster A)

**hero-banner.liquid:**
```
Layout: editorial-split (image right, text left) OR full-bleed centered text
Blocks: text (required), image (optional), CTA (optional)
Default height: large
Color scheme: scheme-1 (primary background)
Max block count: 3
```

**featured-collection.liquid:**
```
Layout: clean grid (default) or asymmetric-grid (variant)
Column count: 2 mobile, 4 desktop
Card structure: image + title + price (nothing else)
Section padding: spacious top and bottom
```

**Collection layout options (via theme-config.json `section_library.collection_layout`):**
- `clean-grid` — uniform column widths, equal spacing (Cluster A default)
- `asymmetric-grid` — see full structural spec below (Cluster A only — other clusters TBD when they reach build stage)
- `masonry` — variable height cards (Cluster E only)
- `list` — single-column list view option

**asymmetric-grid structural spec (Cluster A):**
```
CSS Grid:
  grid-template-columns: repeat(4, 1fr)
  gap: var(--grid-gap)
    ↳ --grid-gap is a base.css layout token derived from the spacing tier scale.
      Not a CSS bridge token (not in settings). Defined in base.css at theme build time.
      Cluster A spacious density: recommended --grid-gap value = --spacing-lg (24px typical).
      Do not reference --spacing-grid-gap (undefined) or --section-gap (section-level only).

Featured card (forloop.first):
  grid-column: span 2
  NO row span — Cluster A uses proportion, not height drama (row span is Cluster C behavior)
  Remaining products: auto placement, uniform 4-column

  Accessibility: featured card must be FIRST in HTML source order, not just visually first
    via CSS span. Do not reorder via CSS — keyboard and screen reader users encounter
    products in DOM order. The first product in the Liquid loop renders first in the HTML.

Aspect ratio:
  ALL cards (including featured): aspect-ratio: 1 / var(--card-image-ratio);
    object-fit: cover; object-position: center
  --card-image-ratio is emitted from settings.card_image_ratio in the CSS bridge.
    ↳ NOTE: settings.card_image_ratio exists in settings_schema-base.json but is NOT yet
      emitted in css-bridge-template.liquid. Add this line to the bridge during T-2a:
      --card-image-ratio: {{ settings.card_image_ratio }};
  Default value in schema: 1.0 (square, 1:1). Cluster A default stays 1.0.
  Merchant-configurable range: 0.8 (landscape) → 2.0 (portrait).
  Do NOT use a different aspect ratio on the featured card — the column span is the only
    asymmetry. Changing the ratio adds a second axis of variation that breaks Cluster A restraint.
  Rationale: Theme Store requires layout not break on varying merchant image ratios.
    object-fit: cover enforces the container aspect ratio regardless of uploaded image dimensions.

Image sizing (Liquid):
  Featured card:  image | image_url: width: 1200
  Standard cards: image | image_url: width: 600
  Aspect ratio enforcement is CSS-side (object-fit: cover on --card-image-ratio container).
  Larger image request on featured card provides better resolution for the larger display size,
    regardless of the displayed aspect ratio.

Mobile collapse:
  ≤ 768px: reset featured to grid-column: span 1 — uniform 2-column for all cards
  ≤ 375px: 1 column, all cards equal
  Asymmetry is a desktop-only pattern; do not attempt to preserve it at smaller breakpoints

Card content:
  image + title + price only — identical to clean-grid, no additions
  No hover overlay, no row span, no extra content fields

Cluster A constraint: the column width difference is the only asymmetry.
  Restraint is the signal. Do not add to it.
```

**main-collection.liquid:**
```
Layout: clean-grid (default) or asymmetric-grid (variant) — driven by section_library.collection_layout
Product grid: same structural rules as featured-collection for the chosen layout

asymmetric-grid on main-collection:
  Featured treatment applies to the FIRST product on PAGE 1 ONLY.
  Implementation: wrap the featured logic in a pagination check:
    {% assign is_featured = forloop.first and paginate.current_page == 1 %}
    Use is_featured to conditionally apply the product-card--featured class.
  Pages 2+: all products render as clean-grid (uniform 4-column). The asymmetry anchors
    the top of the collection on first entry, not on every paginated view.
  Rationale: featured treatment signals discovery at the primary entry point.
    On deeper pages, users are already browsing — a repeated featured card reads as
    disorienting repetition, not intentional design. (Research-backed, 2026-03-30.)
  Accessibility: paginate.current_page check does not affect DOM order.
    The first product in the loop is still first in the HTML — keyboard/focus order intact.

Facets (filter/sort):
  Pattern: sidebar + drawer
  Desktop: persistent left sidebar — no background fill, no visual weight.
    Filter groups: expandable, collapsed by default. Left-aligned labels only.
    Width: --sidebar-width
      ↳ New layout token — does not yet exist. Define in T-2a as an explicit layout
        composition token in base.css. Do NOT derive from spacing.base (spacing scale
        values are unit-level, ~4–48px — too small for sidebar width).
        Recommended starting value: 240px. Expose as a CSS custom property:
        --sidebar-width: 240px; (in base.css, not the CSS bridge)
        Adjust per config if needed, but do not make it merchant-configurable.
    The sidebar is navigation, not content. It must not compete with the grid.
  Mobile: single "Filter + Sort" button triggers a full-height side drawer
  Active filters: dismissible pills displayed above the product grid (not inside the sidebar)
  Accessibility: native <details> disclosure pattern for filter groups; form-based
    (progressive enhancement — must function without JS)

Sort:
  Position: top right, above grid, aligned to grid's right edge
  Style: small text — muted, no custom-styled dropdown
  Cluster A: the sort control should be nearly invisible until needed

Pagination:
  Type: numbered page links — not load more, not infinite scroll
  Position: centered below grid
  Style: prev / 1 2 3 ... / next — no decorative arrows, no result count text
  Cluster A: minimal. Pagination is wayfinding, not a design feature.
```

**Note — asymmetric-grid cluster scope:**
Asymmetric-grid structural rules are defined here for Cluster A only. Other clusters may
define their own asymmetric-grid variants with different behavior (e.g., Cluster C may
warrant a 2-col × 2-row span; Cluster E may use staggered sizing). Add those rules to
the relevant cluster section when that cluster reaches the build stage. Do not apply
Cluster A's no-row-span rule to other clusters without confirming it fits their character.

**image-with-text.liquid:**
```
Layout: 50/50 split, image-right default
Image position: right (default), left (user-selectable)
Content zone: max-width constrained text block, not full column
```

**testimonials.liquid:**
```
Layout: single column, centered
One testimonial visible at a time (not a grid of cards)
Quote mark typographic (not icon)
```

**multicolumn.liquid:**
```
Layout: 3 columns desktop, 1 column mobile
Each column: heading + short text (no icons, no images)
Visual separator: none (whitespace only)
```

---

## Cluster B — Warm/Human

**Character:** Breathing room. Human connection. Editorial warmth in hierarchy.

### Structural Rules

**Hero sections:**
- Organic feel — slight asymmetry acceptable; text does not need to be perfectly centered
- Image is a foreground element (not a full-bleed background) — side-by-side or overlapping
- Warm tone: rounded corners on image frames, generous section padding
- Allow a subheading or short intro paragraph above the primary heading

**Content sections:**
- Alternating layout: text-left/image-right in one section, flipped in the next
- Sections should alternate color schemes (light → warm neutral → light) for visual breathing
- Extra padding — sections should feel open and unhurried
- Block structures: testimonials, people/team, story content are first-class

**Product grid:**
- Slightly rounded card corners (`--radius-md`)
- "Lifestyle" framing: product images can be contextual/atmospheric, not just product-only
- Allow 2 columns mobile, 3 columns desktop — don't crowd
- "Add to cart" visible on hover (warm, inviting — not aggressive)

**Typography:**
- Serif or humanist sans display is a strong fit
- Pull quotes as section anchors
- Subheadings and body copy share similar weight — no stark hierarchy

**Human content signals:**
- Testimonials section always includes name, role/location (not just the quote)
- Blog/article featured image large and warm — section padding generous above and below
- Newsletter signup has a personal, conversational heading (enforced via locale strings)

### Section-Specific Rules (Cluster B)

**hero-banner.liquid:**
```
Layout: side-by-side (image left or right, text on the other side)
Blocks: text (required), image (required), CTA (optional), sub-text (optional)
Image: constrained within section (not full bleed)
Default height: auto (adapts to content)
```

**featured-collection.liquid:**
```
Layout: loose grid with slight variation in card height acceptable
Column count: 2 mobile, 3 desktop
Card: image (atmospheric allowed) + title + price
```

**testimonials.liquid:**
```
Layout: alternating — large quote left, attribution right; next quote flips
Name + location/role required per testimonial block
```

**multicolumn.liquid:**
```
Layout: icon + heading + body text per column
Icons (optional): warm, rounded style
3 columns desktop, stacked mobile
```

---

## Cluster C — Bold/Distinctive

**Character:** Contrast-forward. Type as architecture. Graphic decisiveness.

### Structural Rules

**Hero sections:**
- Oversized type anchor — the heading IS the section; image is secondary
- High contrast: dark-on-light or light-on-dark (never muted or mid-tone)
- Section alternation: hero sets a dark scheme, next section light, alternate throughout
- Allow grid-breaking elements: one image or graphic element crosses the grid boundary

**Content sections:**
- Fewer, larger sections — each section makes a single bold statement
- Dark/light alternation at each section boundary (not just optionally — by default)
- Section padding: generous, but the content itself fills the space with scale, not decoration
- Avoid multi-column layouts where a single full-width statement works instead

**Product grid:**
- Bold type overlay on product image on hover (not a subtle overlay — legible, high contrast)
- 2 columns mobile, 3-4 columns desktop — but cards are taller/more dramatic
- Price typography as large as the product title

**Typography:**
- One dominant heading per section — NO competing sub-headings at similar scale
- Display typefaces at maximum scale — break the type scale ceiling
- Utility/mono type for labels, prices, metadata (sharp contrast to display)

**Grid-breaking rule:**
- Exactly one element per section may cross the grid boundary — image, pull quote, or graphic
- Never two grid-breaking elements in the same section (chaos, not intent)

### Section-Specific Rules (Cluster C)

**hero-banner.liquid:**
```
Layout: oversized heading full-width, image as supporting element (not dominant)
OR full-bleed image with oversized type overlay (dark/light solid swatch, no gradient)
Blocks: heading (required, oversized), image (optional), CTA (required)
Default height: full OR large
Color scheme: scheme-dark (if dark-native) or scheme-contrast
```

**featured-collection.liquid:**
```
Layout: bold grid; each card is a visual statement
Card: image fills card, product name overlays as large type on hover
Column count: 2 mobile, 3-4 desktop (cards taller than wide)
```

**image-with-text.liquid:**
```
Layout: 40/60 or 60/40 split (not 50/50) for asymmetric energy
One element may cross the grid boundary (image bleeds past its column)
```

**testimonials.liquid:**
```
Layout: oversized pull quote centered, full width
Attribution small, below — not competing with the quote
Single quote at a time (no grid of testimonials)
```

**rich-text.liquid:**
```
Allow ONE oversized statement line at the top of the section
Body text below at normal scale — the contrast IS the design
```

---

## Cluster D — Technical/Precision

**Character:** Grid as system. Density hierarchy. Functional clarity.

### Structural Rules

**Hero sections:**
- Information-forward: key specs or value propositions visible in the hero, not hidden below the fold
- Structured layout — header region clearly distinct from content region
- Typography: mono or condensed sans for data/specs; proportional for prose
- No atmospheric imagery — product-specific, precise imagery only

**Content sections:**
- Dense — more information per section is a design goal, not a problem
- Grid structures and aligned columns — everything lines up with everything else
- Table structures for comparison content (products, specs, plans)
- Clear sectional separation via ruled lines or background color change — not whitespace alone

**Product grid:**
- Small, precise thumbnails + complete metadata: SKU, spec summary, price
- Allow 4-5 columns desktop (dense catalog view)
- Sort and filter controls always visible (not hidden in a drawer by default)
- List view as default (or as equally prominent toggle)

**Typography:**
- Utility/mono for data, labels, prices — this is the display register in Cluster D (see `body_register: "monospace-primary"`)
- Proportional body for prose descriptions
- No oversized decorative headings — headings are navigation aids, not visual statements

**Information hierarchy:**
- Structured nested sections using defined spacing tiers (not intuitive)
- Labels visually distinct from values
- SCADA/industrial: secondary shape/symbol encoding alongside color (never color alone)

### Section-Specific Rules (Cluster D)

**hero-banner.liquid:**
```
Layout: structured two-column — specs/key points left, image right
OR header + data-table style value comparison
Blocks: heading, spec list, image, CTA
Default height: auto (no full-bleed theatrics)
```

**featured-collection.liquid:**
```
Layout: dense grid OR list/table toggle
List view available by default (not hidden)
Column count: 3-5 desktop, 2 mobile
Card: image (small) + full title + price + key spec
```

**multicolumn.liquid:**
```
Layout: comparison table-style (not icon + text cards)
Row structure: feature name | col 1 value | col 2 value | col 3 value
Mobile: stacked comparison blocks
```

---

## Cluster E — Organic/Natural

**Character:** Material honesty. Textural depth. Asymmetric rhythm.

### Structural Rules

**Hero sections:**
- Textural or atmospheric full-bleed background (image-heavy)
- Generous radius on all framing elements — cards, image containers, CTAs
- Asymmetric — text block not perfectly centered; offset horizontally or with uneven padding
- Motion: subtle entrance animations with spring/ease-out physics (no linear)
- Allow overlapping elements: text over image edge, one element visually "on top of" another

**Content sections:**
- Textural backgrounds — section background colors can be off-white, warm tan, stone gray
- Asymmetric block arrangements — text left with more left padding, image slightly larger than column
- Sections should feel hand-crafted, not machined — slight variation in padding between sections

**Product grid:**
- Atmospheric product photography expected
- Cards with generous radius (`--radius-lg`)
- Staggered grid (card heights vary) on desktop
- Allow material/ingredient callouts in the card footer

**Typography:**
- Serif or organic display typefaces
- Mix type weights within a section for texture (bold heading + light sub-heading + regular body)
- Avoid hard geometric type (sans-serif with zero personality) — the type should have character

**Motion:**
- Spring physics for entrance animations
- Subtle parallax on image sections
- Staggered entrance for grid cards (CSS animation-delay)
- `prefers-reduced-motion`: all animations must have a static fallback

### Section-Specific Rules (Cluster E)

**hero-banner.liquid:**
```
Layout: full-bleed image with asymmetric text overlay (not perfectly centered)
Text block: floated left or right, with extra padding on the weighted side
Allow image to fill the section; text overlay has a semi-opaque background swatch
Blocks: image (required), text, CTA
Default height: large or full
```

**featured-collection.liquid:**
```
Layout: staggered masonry-style grid (CSS Grid with row-span variation)
Column count: 2 mobile, 3-4 desktop
Card: generous radius, atmospheric image, minimal text
```

**testimonials.liquid:**
```
Layout: offset cards — alternating left/right alignment, slightly overlapping vertically
Background: textural (warm off-white or stone)
Include: optional small photo of the person
```

**image-with-text.liquid:**
```
Layout: asymmetric split — image takes 55-60%, text takes remaining
Image: larger than its column, slightly overlapping the text column
Generous radius on image container
```

---

## Cross-Cluster Rules (Apply in All Clusters)

These rules apply regardless of cluster. They are not optional.

**Color scheme usage:**
Every section has a `color_scheme` setting of type `color_scheme`. Sections do not have raw `color` type settings for background colors. All color variations are achieved through scheme selection, not custom color input.

**Accessibility floor:**
- All interactive elements: `<a href>` or `<button>` — never `<div onclick>`
- All images: `alt="{{ image.alt | escape }}"` — no exceptions
- All forms: `<input>` has `id` + matching `<label for="[id]">`
- Focus visible on all interactive elements
- Touch targets: `min-height: 44px; min-width: 44px`

**Mobile-first CSS:**
Every section generates CSS for 375px first, then scales up:
```css
/* Mobile (375px — base styles) */
.section-[name] { ... }

/* Tablet */
@media (min-width: 768px) { ... }

/* Desktop */
@media (min-width: 1440px) { ... }
```

**Schema completeness:**
Every section schema includes:
- `"name"` — localized via `t:sections.[id].name`
- `"tag": "section"`
- `"class": "section-[kebab-id]"`
- At minimum: one `color_scheme` setting
- `"presets"` array with at least one preset

---

*HeyHi Confidential — Session T-1. Cluster architecture reference for section generation.*
