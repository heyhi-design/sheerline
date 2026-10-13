# Cluster-Derived Design Principles

Zone 2 reference for ui-studio. Load when a build requires design direction beyond mechanical token application — particularly when starting a new client engagement, when a Mode B/C build needs compass, or when Section Rhythm decisions aren't obvious from the config alone.

**Do not load by default.** Zone 1 carries the lightweight lookup table. Load this file when you need the full principle description to make a defensible layout decision.

---

## How These Work

Design principles are derived from `brand.style_cluster` in the active config. They are higher-order craft directives — they shape how the config's tokens are composed into pages, not what the token values are. A principle like "negative space as signal" means: when choosing between tight and generous section padding, choose generous if it serves the content, and let that choice carry communicative weight. It is not a permission to ignore the config's spacing density.

When the config's cluster falls between two named clusters, apply the principles from both and let content hierarchy be the tie-breaker.

---

## Cluster A — Minimal/Refined

**Character:** Restraint as craft. Every element earns its place. Subtraction is an active design decision, not an absence of ideas.

**Principles:**

**1. Negative space as signal.**
Generous white space is not empty — it is the frame that makes the content legible as deliberate. Sections with less content should breathe more, not less. Do not fill space because it's there.
*Well executed:* A single line of heading copy in a section with 8rem of vertical padding reads as editorial confidence. The same copy in 2rem of padding reads as placeholder.

**2. Precision typography.**
Type decisions carry the visual load. A large, restrained display face with minimal supporting elements creates hierarchy without graphic complexity. Weight contrast (light vs. regular, not bold vs. black) is the primary tool.
*Well executed:* Display heading in the lightest available weight, body in regular, utility labels in mono. No bold anywhere. The hierarchy is legible and deliberate without visual noise.

**3. Monochromatic depth.**
Limit the palette to the primary, muted, and background tokens. Color is accent — use it once per section at most, not as decoration. Depth comes from opacity and layering, not hue variation.
*Well executed:* A section uses one background, one text color, and a single accent appearance. The full palette is present across the page, but never competing within a section.

---

## Cluster B — Warm/Human

**Character:** Breathing room. This cluster values the space between elements as much as the elements themselves. Warmth is not softness — it's the sense that someone made deliberate choices for a human reading this.

**Principles:**

**1. Generous section spacing.**
Sections should feel like distinct rooms, not adjacent slides. Use the spacious tier of the config's spacing density as the default, dropping to standard only when content density demands it.
*Well executed:* A testimonial section with one quote, one name, and 8rem of padding above and below. The reader slows down. That pause is the design.

**2. Organic rhythm.**
Alternate between wider and narrower content areas. Not every section needs to span the full container. Vary the reading line — wide for statement copy, narrower for body prose. The variation reads as handcrafted.
*Well executed:* Hero at full width, body section at 70% width centered, stat row at full width again. The rhythm is perceptible without being mechanical.

**3. Editorial warmth in hierarchy.**
Use the warm tonal range of the color palette — secondary text in muted warm tones, not neutral grays. Type scale transitions should feel gradual. Heading weights stay moderate — avoid the sharp contrast of very-large vs. very-small in adjacent elements.
*Well executed:* Section headings are mid-scale (2.5rem), supporting copy is comfortable body size, and the transition between them reads as conversation rather than announcement.

---

## Cluster C — Bold/Distinctive

**Character:** Contrast-forward. This cluster earns attention through decisive visual choices. Nothing is timid. Every section knows what it is.

**Principles:**

**1. Type as architecture.**
Typography is the primary structural element, not a label for layout containers. Large-scale display type can define a section's spatial identity before any other element is placed. The type scale ceiling should be pushed — larger than feels comfortable is usually right.
*Well executed:* A display heading at 8–10rem that establishes the entire section's visual weight. The remaining copy and elements are subordinate to it. The heading is not decorating the section — it is the section.

**2. Graphic decisiveness.**
Background sections, inverted blocks, and high-contrast color breaks should be used with commitment. A section is either normal or inverted — no partial treatments. Section transitions should feel like deliberate scene changes.
*Well executed:* A full-bleed inverted section between two light sections. The transition is sharp — no gradient bridge. The contrast is the statement.

**3. Section drama over uniformity.**
Adjacent sections should feel categorically different from each other. Tight and spacious. Wide and narrow. Text-led and image-led. The monotony of similar sections is the enemy. Every layout pattern change should feel like a choice, not a variation.
*Well executed:* A dense, multi-column services grid immediately followed by a single-column statement section at 50% width with generous padding. The contrast makes both sections more effective.

---

## Cluster D — Technical/Precision

**Character:** Grid as system. Every spacing and layout decision traces to a logical rule. Craft here means consistency, not expression. The absence of decorative choices is itself a statement.

**Principles:**

**1. Density hierarchy.**
Information density should communicate importance. The highest-priority content gets the most space and the fewest surrounding elements. Secondary content earns higher density — more items per row, tighter padding. The density gradient tells the reader where to look.
*Well executed:* A primary stat or finding in a spacious single-column block. Supporting detail in a 3-column grid below it at standard density. The visual hierarchy mirrors the information hierarchy exactly.

**2. Functional clarity over decoration.**
Borders, dividers, and structural elements serve the grid — they are not ornamental. Use them to separate information layers, not to add visual interest. Color is used to encode state or category, not to decorate.
*Well executed:* A table-like section where each row is separated by a 1px divider. No hover animations, no background alternation. The structure is clear because the information is clear.

**3. Structured information.**
Labels, metadata, and supporting information should be visually subordinate but immediately legible. Use utility/mono typefaces for metadata. Use consistent sizing and spacing across all instances of the same information type.
*Well executed:* All dates, categories, and section labels use the same monospaced utility face at the same size, with the same letter-spacing. The system is coherent at a glance.

---

## Cluster E — Organic/Natural

**Character:** Material honesty. Design choices reference the sensory quality of physical materials — texture, weight, layering. Nothing is purely graphic; everything has felt dimensionality.

**Principles:**

**1. Textural depth.**
Surfaces should feel like they have material quality — achieved through subtle background variation, layered elements, or typographic texture (varied weights, sizes, and styles within a text block). Flat, uniform backgrounds read as digital defaults; use them intentionally as contrast against richer sections.
*Well executed:* A section where the background is slightly off-tone from the page default, a second-layer element floats above it at a different opacity, and body copy uses a serif for tactile contrast. The section has depth without 3D effects.

**2. Asymmetric rhythm.**
Column structures should be unequal when the content warrants it. A 60/40 split is more natural than 50/50. Content placement within the grid can bleed slightly — an image that extends past the column boundary reads as intentional rather than constrained.
*Well executed:* A two-column section where the image column is 60% width, the text column 40%, and the image bleeds 5% past the container's right edge. The asymmetry reads as editorial, not broken.

**3. Layered foreground/background.**
Elements can overlap — text over a receding image, a decorative element behind body copy. Layering signals that the design is composed, not assembled from blocks. Use `z-index` and opacity with intention.
*Well executed:* A hero section where a large, low-opacity typographic element sits behind the main heading. The layering creates visual interest without competing with the content hierarchy.

---

## Unlisted Clusters — Derivation Rule

If `brand.style_cluster` does not match A–E, derive principles using this rule:

1. Read `brand.personality` (the descriptor string). Identify the two most dominant qualities.
2. Map each quality to a principle type: expressive → bold heuristics; precise → technical heuristics; warm → human heuristics; restrained → minimal heuristics.
3. Read `config.layout.spacing_density`: spacious → apply "breathing room" principle; dense → apply "density hierarchy" principle; balanced → neither dominates.

Document the derived principles at the top of the build output before the Layout Declaration. This makes the design intent traceable even when the cluster is custom.

---

*HeyHi Internal Use Only. Zone 2 reference for ui-studio. Created 2026-03-25.*
