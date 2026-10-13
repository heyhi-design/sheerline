# Layout Patterns Reference

**`ui-studio/references` · Distilled from `ai-services/design-intelligence/grid-layout-examples.md` · March 2026**

*Named catalog of 15 grid and layout patterns. This is operational vocabulary: names a designer can point to and an agent can enforce. Use pattern names in Layout Declarations, not raw grid specs.*

**Loading strategy:** Pattern Summary Index (~300 tokens) — load at every Layout Declaration. Full pattern specs — load on demand when implementation detail is needed for a specific named pattern.

---

## PATTERN SUMMARY INDEX

*Load this section at the start of every Layout Declaration. ~300 tokens.*

| # | Pattern Name | Family | Cluster Fit | Density |
|---|-------------|--------|-------------|---------|
| 1 | Single Column Reader | Editorial / Reading | E · B | Spacious |
| 2 | Editorial Split | Editorial / Reading | E · A · B | Balanced |
| 3 | Long-Form Cascade | Editorial / Reading | E · C · B | Balanced |
| 4 | Research Document | Editorial / Reading | A · D | Dense |
| 5 | Hero-First | Marketing / Landing | A · B · C | Balanced |
| 6 | Alternating Narrative | Marketing / Landing | B · A | Balanced |
| 7 | Value Cascade | Marketing / Landing | C · A | Dense |
| 8 | Bento Marketing | Marketing / Landing | A · C | Dense |
| 9 | Sidebar + Main | Application / Dashboard | A · D | Balanced–Dense |
| 10 | Data Dashboard | Application / Dashboard | A · D | Dense |
| 11 | Command Interface | Application / Dashboard | A | Spacious–Balanced |
| 12 | Card Grid Application | Application / Dashboard | A · B · C | Balanced–Dense |
| 13 | Masonry Gallery | Portfolio / Gallery | E · C | Dense |
| 14 | Editorial Portfolio | Portfolio / Gallery | E · C | Balanced |
| 15 | Case Study Scroll | Portfolio / Gallery | E · A | Spacious |

**Cluster quick reference:** A=Clean/Structured · B=Warm/Human · C=Bold/Distinctive · D=Sustainable/Infrastructure · E=Craft/Studio

**Density scale:** Spacious=reading-focused, whitespace-dominant · Balanced=mixed content and space · Dense=information-rich, compressed whitespace

**Cross-reference by cluster:**
- **Cluster A:** Hero-First, Bento Marketing, Research Document, Sidebar + Main, Data Dashboard, Command Interface, Card Grid Application, Case Study Scroll
- **Cluster B:** Single Column Reader, Editorial Split, Alternating Narrative, Hero-First, Card Grid Application
- **Cluster C:** Value Cascade, Long-Form Cascade, Bento Marketing, Card Grid Application, Masonry Gallery, Editorial Portfolio
- **Cluster D:** Research Document, Sidebar + Main, Data Dashboard
- **Cluster E:** Single Column Reader, Editorial Split, Long-Form Cascade, Masonry Gallery, Editorial Portfolio, Case Study Scroll

---

## FULL PATTERN SPECIFICATIONS

*Load on demand. Find the specific pattern you need by name.*

---

### 1. Single Column Reader

**Family:** Editorial / Reading | **Cluster:** E · B | **Density:** Spacious

**Grid:** Single column, 680–720px max content width, 48px+ horizontal margin desktop, 24px mobile

**Responsive:**
- Desktop 1200px+: Column centered 680–720px, 240px+ side margins. Optional pull-quote offset (column shifts left, 120–160px annotation margin right).
- Tablet 768–1200px: 80% viewport, side margins contract. Pull-quote offset collapses.
- Mobile: Full-width, 24px horizontal padding.

**Use when:** Long-form essays, newsletters, research publications. Reading is the primary purpose. Voice and thought are the primary brand expression.

**Avoid when:** Multiple simultaneous value propositions, application interfaces, frequent wide figures or data tables.

---

### 2. Editorial Split

**Family:** Editorial / Reading | **Cluster:** E · A · B | **Density:** Balanced

**Grid:** Two-column asymmetric: 60% main / 40% annotation, 32–40px gutter

**Responsive:**
- Desktop: Fixed 60/40, 32–40px gutter. Annotations inline beside text blocks.
- Tablet: 70/30 or annotations stack below reference block.
- Mobile: Single column, annotations move below content.

**Use when:** Long-form with commentary margin, print-borrowed argument + context structure. Main column holds the argument; sidebar holds references, pull quotes, data.

**Avoid when:** Dense product information, uniform communication priority required.

---

### 3. Long-Form Cascade

**Family:** Editorial / Reading | **Cluster:** E · C · B | **Density:** Balanced

**Grid:** Single primary column (720–760px) with occasional full-bleed or extended-width interruptions (images, quotes, callouts can break to 100% width)

**Responsive:**
- Desktop: Text column 720–760px. Interruptions: full-bleed or extended (1100px). Pull quotes may extend to 900px.
- Tablet: Text column 90% viewport. Interruptions scale proportionally.
- Mobile: Single column, all interruptions full-width.

**Use when:** Editorial content where visual rhythm punctuates reading. The interruptions are deliberate emphasis devices, not layout accidents.

**Avoid when:** Consistent information density required, utility interfaces.

---

### 4. Research Document

**Family:** Editorial / Reading | **Cluster:** A · D | **Density:** Dense

**Grid:** Two-column: 65% primary / 35% reference sidebar, 24px gutter. Fixed navigation panel (sidebar or top nav) for long documents.

**Responsive:**
- Desktop: Fixed two-column with document navigation. Dense information, tables, charts fully visible.
- Tablet: Sidebar narrows to 25% or collapses to off-canvas drawer.
- Mobile: Single column. Navigation becomes a sticky header dropdown.

**Use when:** Technical documentation, research publications, long-form reports requiring cross-referencing. Information density is the feature.

**Avoid when:** Marketing content, first-impression contexts, consumer audiences unfamiliar with dense layouts.

---

### 5. Hero-First

**Family:** Marketing / Landing | **Cluster:** A · B · C | **Density:** Balanced

**Grid:** Full-viewport hero (100vh or 80vh), then alternating full-width sections. 12-col grid for hero content, 24–32px gutters.

**Responsive:**
- Desktop: Hero full-viewport. Content centered within 1100–1200px max-width. Below-fold sections full-width with constrained content.
- Tablet: Hero 70–80vh. Text and CTA reflow to narrower column.
- Mobile: Hero 60–70vh. Single column below fold.

**Use when:** Primary landing pages, product homepages, marketing pages where the first impression is the primary job.

**Avoid when:** Content-heavy pages where the hero delays reaching the information, documentation sites.

---

### 6. Alternating Narrative

**Family:** Marketing / Landing | **Cluster:** B · A | **Density:** Balanced

**Grid:** Full-width sections, alternating 50/50 or 55/45 content-image columns. Images left on odd sections, right on even. 48–64px gutters.

**Responsive:**
- Desktop: True side-by-side alternating. Rhythm established by image/content switching.
- Tablet: Narrower splits or content stacks above image.
- Mobile: All sections stack — image above content or hidden.

**Use when:** Explaining multiple features or benefits with equal weight. Human-centered narratives. The alternating rhythm creates reading momentum.

**Avoid when:** More than 6–7 alternating sections (rhythm becomes exhausting). Complex information that needs text-dominant space.

---

### 7. Value Cascade

**Family:** Marketing / Landing | **Cluster:** C · A | **Density:** Dense

**Grid:** Tight, asymmetric grid: featured value full-width at top, then 3-column or 4-column grid below. Small gutters (16–20px). Dense information, many simultaneous elements.

**Responsive:**
- Desktop: 3–4 column value grid below featured block. Consistent card height.
- Tablet: 2 columns.
- Mobile: Single column or 2-column compact.

**Use when:** Communicating many features or benefits simultaneously. Comparison grids. Feature matrices. Audiences who want to evaluate comprehensively before deciding.

**Avoid when:** Brand personality requires breathing room. Audiences unfamiliar with dense layouts. Where trust must be built before information is consumed.

---

### 8. Bento Marketing

**Family:** Marketing / Landing | **Cluster:** A · C | **Density:** Dense

**Grid:** Variable-size cards on a 12-col grid. Some cards 4 cols, some 8, some 6. Card heights vary by content importance. Tight gutters (12–16px).

**Responsive:**
- Desktop: Bento grid in full expression. Card sizes communicate hierarchy visually.
- Tablet: Simpler grid — fewer unique card sizes.
- Mobile: Single-column card stack or 2-column compact grid.

**Use when:** Tech product marketing, SaaS feature showcases, modern landing pages where visual hierarchy through card size communicates importance.

**Avoid when:** Craft or artisan brands where structured grids conflict with personality. Audiences who read rather than scan.

---

### 9. Sidebar + Main

**Family:** Application / Dashboard | **Cluster:** A · D | **Density:** Balanced–Dense

**Grid:** Fixed sidebar (220–280px) + fluid main content area. Sidebar holds navigation; main holds working content.

**Responsive:**
- Desktop: Persistent sidebar. Main content maximizes available width.
- Tablet: Sidebar narrows to icon-only rail (60px) or collapses to top bar.
- Mobile: Sidebar becomes bottom navigation or hamburger menu.

**Use when:** Applications requiring persistent navigation. Content that users navigate to within a session. Tools where the user needs orientation at all times.

**Avoid when:** Single-purpose applications, reading-focused content, marketing pages.

---

### 10. Data Dashboard

**Family:** Application / Dashboard | **Cluster:** A · D | **Density:** Dense

**Grid:** Card-based data grid. 12-col base. Widgets: 3, 4, 6, or 12 col widths. Small gutters (12–16px). Fixed header with global controls.

**Responsive:**
- Desktop: Full card grid. Multiple data widgets simultaneously visible.
- Tablet: 2-column widget grid. Some widgets expand to full width.
- Mobile: Single column. Key metrics at top; secondary widgets below.

**Use when:** Monitoring, analytics, reporting, operational control surfaces. Information density is the product.

**Avoid when:** Consumer-facing content, onboarding flows, contexts where data density would overwhelm.

---

### 11. Command Interface

**Family:** Application / Dashboard | **Cluster:** A | **Density:** Spacious–Balanced

**Grid:** Minimal top bar (48–56px) + maximum workspace. Contextual panels on-demand only.

**Responsive:**
- Desktop 1200px+: Minimal top bar, workspace fills remainder. Contextual panels slide in from right or appear as popovers.
- Desktop 1440px+: Optional soft sidebar (160–200px left) for persistent file tree without compressing the working area.
- Tablet: Contextual panels become full-screen or reduce in width.
- Mobile: View-only mode or companion app pattern.

**Use when:** Creative tools, editors, design environments, canvas-based applications. The user is competent and wants room. The interface recedes; the work surfaces.

**Avoid when:** Consumer applications requiring discoverability, first-use experiences needing explicit orientation.

---

### 12. Card Grid Application

**Family:** Application / Dashboard | **Cluster:** A · B · C | **Density:** Balanced–Dense

**Grid:** Header nav (fixed, 48–56px), optional filter/sort bar (40px), 3–4 column equal-height card grid. 16–20px gutters.

**Responsive:**
- Desktop: 3–4 column grid, consistent card height.
- Tablet: 2–3 columns.
- Mobile: 1–2 columns. Filter bar becomes filter sheet.

**Use when:** Resource libraries, project collections, content catalogs, e-commerce grids. Browsable collections where all items have equal weight.

**Avoid when:** Deep nested content requiring persistent context panels, content too complex for card format.

---

### 13. Masonry Gallery

**Family:** Portfolio / Gallery | **Cluster:** E · C | **Density:** Dense

**Grid:** 3-column (desktop) or 2-column (tablet) variable-height column grid. 8–12px gutters.

**Responsive:**
- Desktop: 3–4 columns, 8–12px gutters.
- Tablet: 2–3 columns, 12–16px gutters.
- Mobile: 2 columns or single column.

**Use when:** Photography portfolios, visual art collections, inspiration boards, mixed-media archives where content dimensions vary. The variable height feels organic and exploratory.

**Avoid when:** Product catalogs needing comparison, collections with significant text, UI component libraries.

---

### 14. Editorial Portfolio

**Family:** Portfolio / Gallery | **Cluster:** E · C | **Density:** Balanced

**Grid:** Asymmetric case study grid: one full-width feature block, then pairs of half-width blocks, occasional 65/35 or 70/30 asymmetric breaks. 24–32px gutters.

**Responsive:**
- Desktop: Full asymmetric expression. Feature block 480–640px height. Half-width blocks 360–480px.
- Tablet: Half-width blocks may remain or collapse to full-width. Asymmetric breaks collapse. Opening block stays full-width.
- Mobile: All blocks stack to full-width. Curatorial logic is lost; individual block quality carries.

**Use when:** Design agency or studio portfolios where selection and arrangement signals taste. Creative director portfolios with a defined body of work. Case study archives.

**Avoid when:** Large collections (20+ items), client-facing comparison tools, contexts where visual weight differences create awkward contrast.

---

### 15. Case Study Scroll

**Family:** Portfolio / Gallery | **Cluster:** E · A | **Density:** Spacious

**Grid:** Single primary column (680–800px text), variable-width image insertions. Images: in-column, extended (960–1100px), or full-bleed. Text annotations at reduced type size alongside extended images.

**Responsive:**
- Desktop: Text column 680–800px. Extended images 960–1100px. Full-bleed images viewport-width. Annotations at right margin of extended images.
- Tablet: Text column 90% width. Extended images 100% width. Annotations move below image.
- Mobile: Single column. All image widths resolve to full-width.

**Use when:** Design portfolio case studies requiring documented process. Agency project documentation. Post-mortems and research publications where image and text evidence interweave.

**Avoid when:** Image-dominant portfolios where narrative depth slows browsing. Multiple projects in parallel comparison.

---

*HeyHi Internal Use Only. Source: ai-services/design-intelligence/grid-layout-examples.md (Session C, March 2026). Distilled March 25, 2026.*
