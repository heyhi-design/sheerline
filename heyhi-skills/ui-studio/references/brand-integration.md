# Brand Integration Guide

How to map a design system's tokens into concrete CSS decisions. This file is a process guide — the actual values come from `brand-config/active-brand.json`.

---

## Loading the Brand Context

Before starting any UI work, resolve the brand config. The config is the single source of truth for every visual decision.

**What the config provides:**
- Font families, weights, and usage rules
- Type scale with responsive clamp values
- Color palette with semantic roles and contrast-safe combinations
- Spacing rhythm and section padding tiers
- Motion tokens (easing curves, duration ranges, stagger timings)
- Voice rules and prohibited patterns
- Component inventory and conventions

**What the config does NOT provide (and you must design):**
- Layout decisions (grid vs. asymmetric, section ordering)
- Content hierarchy (what's emphasized, what's secondary)
- Interaction choreography (which patterns from the library, in what sequence)
- Editorial voice for specific copy (the rules constrain, they don't write)

---

## CSS Custom Property Naming Convention

ui-studio uses **short semantic aliases** for CSS custom properties in single-file prototypes. This is a deliberate choice for brevity and readability in prototype files.

**The convention:**

| Config path | CSS variable | Why this name |
|---|---|---|
| `tokens.typography.families.display.family` | `--ff-display` | `ff` = font-family; role name |
| `tokens.typography.families.body.family` | `--ff-body` | |
| `tokens.typography.families.utility.family` | `--ff-utility` | |
| `tokens.color.backgrounds.primary` | `--bg` | The primary canvas |
| `tokens.color.backgrounds.secondary` | `--surface` | Secondary surfaces |
| `tokens.color.backgrounds.elevated` | `--white` | Elevated or lightest surface |
| `tokens.color.backgrounds.inverted` | `--dark` | Inverted (dark) sections |
| `tokens.color.text.primary` | `--text` | Primary readable text |
| `tokens.color.text.secondary` | `--text-mid` | Secondary text |
| `tokens.color.text.muted` | `--muted` | Subdued / supporting text |
| `tokens.color.text.decorative` | `--light` | Decorative only — verify AA |
| `tokens.color.text.inverted_secondary` | `--warm` | Inverted section secondary text |
| `tokens.color.structural.divider` | `--divider` | Lines, borders |
| `tokens.color.accent.primary` | `--accent` | Brand accent |
| `tokens.color.accent.light` | `--accent-l` | Accent tint (hover backgrounds) |
| `tokens.color.accent.dark` | `--accent-d` | Accent shade (pressed states) |
| `tokens.motion.easing.default` | `--ease-default` | General transitions |
| `tokens.motion.easing.reveal` | `--ease-reveal` | Entrances and reveals |

**When to use schema-path names instead:** For design system work where the prototype will be integrated into a larger codebase, use the schema-path naming convention: `--color-accent-primary`, `--typography-family-display`, etc. This prevents token name collisions and keeps the custom properties traceable to the source token. For standalone prototypes, short aliases are appropriate. Document the convention used at the top of the `:root` block.

---

## Token Mapping Strategy

### Typography

Read `tokens.typography` from the brand config. Map to CSS custom properties:

```css
:root {
  /* These values come from the brand config — never hardcode */
  --ff-display: '[config.tokens.typography.families.display.family]', [fallback];
  --ff-body:    '[config.tokens.typography.families.body.family]', [fallback];
  --ff-utility: '[config.tokens.typography.families.utility.family]', [fallback];
}
```

**Display font:** Used for headlines, pullquotes, large statement text. Check the config for available weights and intended usage.

**Body font:** Used for paragraph text, descriptions, navigation labels. Check weight range.

**Utility font:** Used for labels, metadata, tags, technical annotations. Often monospaced. Check the config for sizing and letter-spacing conventions.

**Type scale construction:**

Build from `tokens.typography.scale`. If the config provides explicit clamp values, use them directly. If it provides a scale ratio and base size, derive the clamp values:

**Derivation procedure (when config has `scale.base` + `scale.ratio`):**

Step 1 — Calculate each scale step in px:
```
body:    base × ratio^0  = base (e.g., 16px)
lead:    base × ratio^1  (e.g., 16 × 1.333 = 21.3px)
h3:      base × ratio^2  (e.g., 16 × 1.778 = 28.4px)
h2:      base × ratio^3  (e.g., 16 × 2.370 = 37.9px)
h1:      base × ratio^4  (e.g., 16 × 3.160 = 50.6px)
display: base × ratio^5  (e.g., 16 × 4.209 = 67.3px)
```

Step 2 — Derive mobile-min and desktop-max (in rem, base 16px):
```
desktop-max = step_px / 16
mobile-min  = desktop-max × 0.65  (scales to ~65% on smallest screens)
```

Step 3 — Derive the fluid viewport coefficient:
```
fluid_vw = (desktop-max_rem - mobile-min_rem) / (1440 - 375) × 100
          ≈ (desktop-max_rem - mobile-min_rem) × 0.0939
```
Round to 2 decimal places.

Step 4 — Calculate the intercept (the `rem` constant in the fluid expression):
```
intercept = mobile-min_rem - fluid_vw × (375 / 100)
```

Step 5 — Construct clamp():
```css
font-size: clamp([mobile-min]rem, [fluid_vw]vw + [intercept]rem, [desktop-max]rem);
```

**Worked example** (scale.base=16, scale.ratio=1.333 — perfect fourth):
```css
h1 {
  /* step = 16 × 1.333^4 = 50.6px = 3.16rem
     mobile-min = 3.16 × 0.65 = 2.05rem
     fluid_vw = (3.16 - 2.05) × 0.0939 = 0.104 → ~1.04vw
     intercept = 2.05 - 1.04 × 3.75 = 2.05 - 3.90 = -1.85
     Result: clamp(2.05rem, 1.04vw + 1.66rem, 3.16rem) */
  font-size: clamp(2.05rem, 1.04vw + 1.66rem, 3.16rem);
}

h2 {
  /* step = 16 × 1.333^3 = 37.9px = 2.37rem
     mobile-min = 2.37 × 0.65 = 1.54rem
     fluid_vw = (2.37 - 1.54) × 0.0939 = 0.078 → ~0.78vw
     intercept = 1.54 - 0.78 × 3.75 = 1.54 - 2.925 = -1.38 → round to nearest workable value
     Result: clamp(1.54rem, 0.78vw + 1.25rem, 2.37rem) */
  font-size: clamp(1.54rem, 0.78vw + 1.25rem, 2.37rem);
}
```

**If the config provides only a named ratio** (e.g., "perfect-fourth", "major-third", "minor-third"), use these standard ratio values:

| Named ratio | Value |
|---|---|
| minor-second | 1.067 |
| major-second | 1.125 |
| minor-third | 1.200 |
| major-third | 1.250 |
| perfect-fourth | 1.333 |
| augmented-fourth | 1.414 |
| perfect-fifth | 1.500 |
| major-sixth | 1.667 |

```css
/* Result: clamp values by type role */
h1 { font-size: clamp([mobile-min], [fluid-vw], [desktop-max]); }
h2 { font-size: clamp([mobile-min], [fluid-vw], [desktop-max]); }
h3 { font-size: clamp([mobile-min], [fluid-vw], [desktop-max]); }

.lead { font-size: clamp([mobile-min], [fluid-vw], [desktop-max]); }
body  { font-size: clamp([mobile-min], [fluid-vw], [desktop-max]); }
.small { font-size: [value]; }

.label { font-size: [value]; letter-spacing: [value]; text-transform: uppercase; }
.meta  { font-size: [value]; letter-spacing: [value]; }
```

### Color

Read `tokens.color` from the brand config. Map semantic roles to CSS custom properties:

```css
:root {
  /* Backgrounds */
  --bg:       [config.tokens.color.backgrounds.primary];
  --surface:  [config.tokens.color.backgrounds.secondary];
  --white:    [config.tokens.color.backgrounds.elevated];
  --dark:     [config.tokens.color.backgrounds.inverted];

  /* Text */
  --text:     [config.tokens.color.text.primary];
  --text-mid: [config.tokens.color.text.secondary];
  --muted:    [config.tokens.color.text.muted];
  --light:    [config.tokens.color.text.decorative];  /* Check AA compliance */

  /* Structural */
  --divider:  [config.tokens.color.structural.divider];

  /* Accent */
  --accent:   [config.tokens.color.accent.primary];
  --accent-l: [config.tokens.color.accent.light];
  --accent-d: [config.tokens.color.accent.dark];
}
```

**Contrast verification:** After mapping, verify every text/background combination:
- Primary text on primary bg: must pass AA (4.5:1 minimum)
- Muted text on primary bg: must pass AA (4.5:1)
- Decorative text: document if it fails AA. Use only for non-meaningful content.
- Accent as text: verify against both light and dark backgrounds
- Inverted section text: verify warm/light text on dark backgrounds

**Role-split a boundary-near accent.** When a brand's signature accent is a mid-saturation hue near the WCAG 4.5:1 boundary (common for oranges, reds, golds, mid-greens), one token value cannot serve every role. Compute white-on-accent and accent-on-ground first; if either lands near 4.5:1, define role-tuned cuts rather than forcing one value: a **decorative/large** cut (the lively brand hue — illustration and display, where a thin pass or large-text-only is acceptable); an **action** cut (darkened so white — or dark — text on the fill clears 4.5:1 with margin) for interactive CTA fills, plus its hover cut; and a **text-safe** cut (darkest) for small accent-colored text on the page ground. Record each cut's computed contrast in `tokens.color.contrast_notes` so a builder routes CTA text to the action cut, never the decorative one. This is distinct from `accent.light`/`accent.dark` *state* cuts (hover/pressed): role cuts are about *what carries text*, state cuts about *interaction feedback*.

**Prohibited colors:** Check `tokens.color.prohibited`. These are colors or color ranges the brand explicitly avoids. Document why if the config includes rationale.

### Spacing

Read `tokens.spacing` from the brand config:

```css
:root {
  --pad:   clamp([mobile], [fluid], [desktop]);  /* Page-level horizontal padding */
  --max-w: [config.tokens.spacing.content_max_width];
  --gap:   clamp([mobile], [fluid], [desktop]);  /* Grid gaps */
}

/* Vertical section padding tiers from config */
/* Generous: [tier values] (major sections) */
/* Standard: [tier values] (subsections) */
/* Tight:    [tier values] (within components) */
```

**Key principle:** Not every section should have the same padding. The brand config may specify tier names and values. If it only provides a base unit and rhythm, derive tiers that create variety.

### Motion

Read `tokens.motion` from the brand config:

```css
/* Easing curves from config */
--ease-default: [config.tokens.motion.easing.default];
--ease-reveal:  [config.tokens.motion.easing.reveal];
--ease-micro:   [config.tokens.motion.easing.micro];

/* Duration ranges from config */
/* Micro: [range] (hover, focus, small state changes) */
/* Reveal: [range] (scroll reveals, section entries) */
/* Stagger: [value] per child */
```

If the brand config doesn't specify motion tokens, use sensible defaults:
- Default: `cubic-bezier(0.65, 0, 0.35, 1)`
- Reveal: `cubic-bezier(0.33, 1, 0.68, 1)`
- Micro: 150-300ms
- Reveal: 600-800ms
- Stagger: 60-100ms per child

---

## Brand Temperature

The brand config includes a `temperature` field (`warm`, `cool`, `neutral`). This influences decisions beyond explicit tokens:

**Warm brands:**
- Neutral grays should lean warm (brown/amber undertones, not blue/gray)
- Dark sections use warm darks (e.g., #2A2825 not #2A2A2A)
- Inverted text should feel warm (cream, not pure white)

**Cool brands:**
- Neutral grays can lean cool (blue/slate undertones)
- Dark sections can use pure darks
- Inverted text can be pure white or cool light

**Neutral brands:**
- True grays are appropriate
- Follow the token values exactly without temperature adjustment

---

## Selection Styling

A detail that signals craft:

```css
::selection {
  background: var(--accent);
  color: var(--bg);
}
```

Use the brand's accent color for selection background and the lightest background color for text. This makes text selection feel intentional and branded.

---

## Font Loading

Construct from `tokens.typography.loading`:

```html
<!-- Adapt this to the brand's font provider -->
<link rel="preconnect" href="[font-provider-origin]">
<link rel="preconnect" href="[font-static-origin]" crossorigin>
<link href="[config.tokens.typography.loading.url]" rel="stylesheet">
```

Always use `display=swap`. Always `preconnect`. Always provide system font fallbacks in the CSS font stacks.

If fonts are self-hosted (from the token repo), use `@font-face` declarations with the appropriate font files and `font-display: swap`.

---

## Working Without Full Config Data

Sometimes the brand config is incomplete. Handle gaps:

| Missing data | What to do |
|-------------|-----------|
| Typography scale | Derive from base size + musical fourth (1.333) or perfect fourth (1.414) ratio. Document the choice. |
| Motion tokens | Use the sensible defaults listed above. Document that these aren't from the brand system. |
| Voice rules | Write clean, professional copy. Flag that voice guidelines should be established. |
| Component inventory | Build from scratch following general best practices. Document that no existing library was available to reference. |
| Spacing tiers | Derive from base unit. Generous = 5-9 base units, Standard = 3-5, Tight = 1.5-2.5. Document. |
| Color contrast data | Calculate contrast ratios yourself. Flag any combinations that fail AA. |

Always document what was derived vs. what came from the brand config. This makes it possible to update later when the config is completed.

---

*Reference for ui-studio skill. Originally authored for design-system-ux, March 2026.*

*HeyHi Confidential*

---

## CSS Cascade Layers (@layer)

*Added 2026-04-18. Browser support: All modern browsers since 2022. Fully safe for production.*

**What @layer solves:** Specificity conflicts in design systems. When a utility class needs to override a component style, and that component style needs to override a base style — without `@layer`, this requires specificity gymnastics or `!important`.

```css
/* Declare layer order upfront — lower in list = higher priority */
@layer reset, base, tokens, components, utilities, overrides;

@layer reset {
  *, *::before, *::after { box-sizing: border-box; margin: 0; }
}

@layer tokens {
  :root {
    --color-accent: #2563EB;
    --font-display: 'Inter', sans-serif;
  }
}

@layer components {
  .btn {
    background: var(--color-accent);
    font-family: var(--font-display);
    padding: 0.75rem 1.5rem;
  }
}

@layer utilities {
  /* Utility classes always win over components — no specificity hacks needed */
  .mt-0  { margin-top: 0; }
  .hidden { display: none; }
}
```

**Design system application — wrapping third-party CSS:**

```css
/* Third-party library always loses to your design system tokens and components */
@import url('third-party.css') layer(vendor);

@layer vendor, tokens, components; /* tokens and components always win over vendor */
```

This is the correct approach when integrating any external CSS library (normalize, reset, UI framework base styles) into a design system build. Wrapping it in a named layer means you never need to fight its specificity.

**`!important` reversal:** `!important` reverses layer priority — an `!important` declaration in a lower-priority layer beats a normal declaration in a higher-priority layer. Avoid `!important` inside layered design system code; the behavior is counterintuitive and difficult to debug.

**Public/private layers:** `@layer` rules inside `@layer` declarations create nested layers. The outer layer name is the public API; inner layers are private implementation details. Useful when distributing a design system as a library.

**Relationship to token output:** Style Dictionary can be configured to emit all token custom properties inside a `@layer tokens` block. This is the correct architecture when token values need to be overridable by component utilities without specificity conflicts.
