# Futurecasting UI Reference

**`ui-studio/references` · Load when Mode C is active · March 2026**

*Speculative aesthetic rules for concept work. Extended palette logic, contrast verification requirements, concept narrative format, and composition blueprint schema.*

---

## What Mode C Is For

Mode C builds things that don't exist yet. The brand config is a personality baseline and temperature anchor, not a constraint boundary. You can invent components, extend the palette, and derive new layout logic from named patterns — as long as every decision is documented and every color is contrast-verified before it touches CSS.

The goal is a deliverable that makes a client see what's possible. It must hold together as a coherent aesthetic argument, not just a speculative exercise.

---

## Speculative Aesthetic Rules

**Start from the brand config's personality, not its tokens.** The config's `brand.personality` and `brand.temperature` are the anchor. The specific hex values are departure points, not walls.

**Document every departure.** Any token value you invent, extend, or reinterpret gets a comment in the CSS and an entry in the concept narrative's "Extended Palette" section. The documentation is part of the deliverable.

**Named patterns as departure points, not starting points.** In Mode A, you pick the pattern and follow it exactly. In Mode C, you name which pattern you're departing from and describe the derivation. "Derived from Hero-First: hero fills 100vh but breaks into asymmetric 65/35 at the midpoint rather than centered content" is a valid Mode C layout derivation.

**Custom components require semantic HTML.** Even if the component doesn't exist in the library, the HTML must be semantic. A custom `<timeline-marker>` element wraps in a `<li>` inside an `<ol>`. A custom card that functions as a button uses `<button>` or `role="button"` with keyboard interaction. Speculation does not exempt from semantics.

**`prefers-reduced-motion` is non-negotiable.** Mode C prototypes can use animation liberally. Every animation must have a `prefers-reduced-motion` variant — either removing the motion entirely or reducing it to an immediate state change. This is not optional.

---

## Extended Palette Logic

Mode C permits inventing colors beyond the brand config's palette. Every invented color must pass contrast verification before use in CSS.

### Contrast Verification Protocol

Before writing any CSS that uses an invented color:

1. **State the invented color** with its hex value and intended use: *"Extended accent: #A47A55 — warm terracotta, intended for section dividers and accent marks"*

2. **State the background it will appear against**: *"Will appear against #FFFFFF (primary background)"*

3. **Calculate the contrast ratio**: Use the WCAG relative luminance formula, or state the tool used. Do not approximate.

4. **State the result against the threshold:**
   - Body text: 4.5:1 minimum
   - Large text (18px+ regular, 14px+ bold): 3:1 minimum
   - UI components and decorative elements: 3:1 minimum

5. **If it fails:** Adjust the value until it passes. Document the adjustment: *"Initial value #A47A55 was 3.82:1 against #FFFFFF — insufficient for body text. Darkened to #8B5E3C → 5.58:1. Passes."*

**Failure to verify is not a technical gap — it is a spec error.** Extended palette colors that appear in CSS without a preceding contrast verification in the documentation are a bug, not an approximation.

### Extended Palette Documentation Format

Include in the concept narrative's "Extended Palette" section:

```
Extended color: [name]
Value: [hex]
Appears against: [background hex]
Contrast ratio: [X.X:1]
Threshold: [body text 4.5:1 / large text 3:1 / UI component 3:1]
Result: PASS / FAIL
Use in this concept: [where and why]
```

---

## Two Output Paths

Mode C produces one of two deliverable types. Clarify with the user at the start of the session.

### Path 1: Interactive Prototype

HTML/CSS/JS output with custom components, extended tokens, and speculative layout. The prototype is interactive — hover states, transitions, scroll behavior, responsive breakpoints.

**What the prototype file includes:**
- Full CSS custom properties for both base config tokens and extended palette
- Layout Declaration for every section (with Mode C derivation notation)
- Extended palette verification comments immediately before any invented color is used in CSS
- Semantic HTML throughout
- `prefers-reduced-motion` media query blocks for all animations
- Visible focus states on all interactive elements

**What the prototype file does NOT include:** A cover sheet, concept narrative, or explanatory prose. The narrative is a separate file.

### Path 2: Composition Blueprint

A structured markdown document describing the visual concept for a designer to reproduce. The blueprint does not include CSS or HTML — it describes the decisions at a level of specificity that allows an experienced designer to build it.

**Composition Blueprint Schema:**

```markdown
# Composition Blueprint: [Concept Name]

## Visual Intent
[2-3 sentences: what this concept communicates and why. The argument, not the description.]

## Palette
### Base tokens used from config
[List only the tokens from active-brand.json that are actively applied — omit unused tokens]

### Extended palette
[For each invented color, include the full verification block from the Extended Palette Documentation Format above]

## Typography
### Type roles and their scales
[For each type role (display, body, label, etc.): which font, which weight, which size. State any departures from the config's type scale and why.]

### Typographic moments
[Any deliberate typographic design decisions: size contrast, weight contrast, mixed-family moments, mono + serif pairings, etc.]

## Layout
### Structure
[Name the base pattern and state the derivation. Describe the grid at a section-by-section level.]

### Section breakdown
[For each section:
- Pattern: [named pattern + derivation if Mode C]
- Spacing tier: [generous/standard/tight from config.layout.spacing_density]
- Key layout decision: [what makes this section distinctive]
- Content: [what appears in this section]]

## Motion and Interaction
[Describe animation intent for each animated element. Include the prefers-reduced-motion behavior for each.]

## Custom Components
[For each invented component: what it is, how it behaves, what semantic HTML would underlie it, what accessibility behavior it requires]

## Figma Notes
[Optional. If the designer will build this in Figma, note which frames to create, which libraries to use as references, and where to use Figma variables vs. hardcoded values.]
```

---

## Concept Narrative Format

The concept narrative is a standalone deliverable. It is NOT a heyhi-deck input — when a deck is needed from this concept, the user summarizes the narrative conversationally to heyhi-deck. The narrative and the deck are produced through different paths.

**File:** `[concept-name]-concept-narrative.md`

**YAML frontmatter:**
```yaml
---
concept: [Name]
client: [Client name or "HeyHi internal"]
mode: C
config_used: [active-brand.json brand.name + version]
date: [ISO date]
output_type: prototype | blueprint
status: done
classification: HeyHi Confidential
---
```

**Narrative structure:**

```markdown
## The Argument
[What this concept proposes. The aesthetic thesis. 1-3 paragraphs.]

## Extended Palette
[All extended colors with full verification blocks]

## Layout Decisions
[Named departures from patterns with rationale. Why these decisions serve the concept's argument.]

## Typographic Decisions
[Any deliberate typographic choices not encoded in the config]

## Motion Intent
[What moves, why, and how prefers-reduced-motion is handled]

## What Needs Validation
[Things that look right but need designer confirmation: provisional colors, unvalidated font pairings, spacing that may need adjustment at real content scale]

## Connection to Brand Config
[How the config's personality and temperature anchored the speculative decisions. Where you departed and why.]
```

---

## Mode C WCAG Checklist

Before delivering any Mode C output (prototype or blueprint):

- [ ] Every invented color has a documented contrast verification showing ratio ≥ 4.5:1 body text, ≥ 3:1 large text/UI components
- [ ] All prototype HTML uses semantic elements (`<nav>`, `<section>`, `<article>`, `<button>`, etc.)
- [ ] All custom interactive components have keyboard interaction described or implemented
- [ ] All animations have `@media (prefers-reduced-motion: reduce)` variants
- [ ] All images have alt text (or explicit `alt=""` for decorative images)
- [ ] Focus states visible on all interactive elements
- [ ] Sequential heading hierarchy maintained (one `<h1>`, then `<h2>`, then `<h3>`)

---

*HeyHi Internal Use Only. Created March 25, 2026.*
