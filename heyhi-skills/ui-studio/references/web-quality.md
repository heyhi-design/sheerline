# Web Quality Reference

Pre-delivery quality standards for design-system-aware UI work. This expands the checklist in the main SKILL.md with specific techniques, thresholds, and testing procedures.

---

## Priority Map

| Priority | Category | Why |
|----------|----------|-----|
| CRITICAL | Accessibility | Enterprise clients expect AA compliance minimum. Inaccessible work contradicts any design system's purpose. |
| CRITICAL | Touch & Interaction | If interactive elements don't respond correctly, the craft story falls apart. |
| CRITICAL | Token Compliance | Every visual value must trace back to a design token. Raw hex values, magic numbers, and hardcoded fonts break the system. |
| HIGH | Performance | Slow-loading pages undermine quality positioning. |
| HIGH | Layout & Responsive | Prototypes get shared on phones, tablets, and projectors. Breaking at any viewport is unacceptable. |
| HIGH | Component Library Alignment | New builds should use or extend existing components, not duplicate them. |
| MEDIUM | Typography & Color | Covered by the brand integration system, but verify on every build. |
| MEDIUM | Animation | Guided by interaction patterns, but the "does it have a reason" test applies to every animation. |
| MEDIUM | Forms & Feedback | Relevant when building interactive tools, dashboards, or contact forms. |

---

## Accessibility Checks

### Contrast

After mapping the brand's color tokens, verify every text/background combination:

**Test procedure:**
1. Calculate contrast ratio for primary text on primary background
2. Calculate contrast ratio for muted text on primary background
3. Calculate contrast ratio for any decorative/light text — document if it fails AA
4. Calculate contrast ratio for accent text on both light and dark backgrounds
5. Calculate contrast ratio for inverted section text (light on dark)

**Thresholds:**
- Normal text (< 24px / < 19px bold): 4.5:1 minimum (AA)
- Large text (>= 24px / >= 19px bold): 3:1 minimum (AA)
- Decorative/non-meaningful text: no requirement, but document the decision

**Pay special attention to:**
- Text overlaid on images or gradients
- Hover/focus state colors
- Disabled state opacity (should not drop below 0.38)
- Inverted section text colors

### Keyboard Navigation

- Tab order follows visual reading order (left-to-right, top-to-bottom)
- All interactive elements (links, buttons, form inputs) reachable via Tab
- Focus states visible: use outline or box-shadow, never `outline: none` without a replacement
- Skip-to-content link for pages with navigation
- Heading hierarchy is sequential: one h1, then h2s, then h3s. No skipping levels.

**Recommended focus style:**
```css
:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 3px;
}
```

Use `:focus-visible` (not `:focus`) to avoid showing outlines on mouse clicks while keeping them for keyboard navigation.

### Screen Readers

- All images have `alt` text (decorative images get `alt=""`)
- Icon-only buttons have `aria-label`
- Dynamic content updates use `aria-live` regions
- Form inputs have associated `<label>` elements (not just placeholder text)
- Landmarks: `<nav>`, `<main>`, `<footer>`, `<section>` with `aria-label` when multiple exist

### Motion

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

This must be present in every prototype that uses animation. Non-negotiable.

---

## Token Compliance Checks

### What to verify

After building, scan the CSS for any value that doesn't reference a custom property:

- **Colors:** No raw hex values (`#FF0000`), rgb values, or named colors. Every color should be `var(--token-name)`.
- **Font families:** No raw font names. Every font-family should be `var(--ff-*)`.
- **Spacing:** No magic numbers for padding, margin, or gap. Use the brand's spacing tokens or derive from them.
- **Font sizes:** Should reference the type scale or use `clamp()` values from the brand config.
- **Shadows/elevation:** Should use elevation tokens if the brand defines them.

### Exceptions

- Reset/normalize values (e.g., `margin: 0`, `padding: 0`) don't need tokens
- Structural values (e.g., `width: 100%`, `position: fixed`) don't need tokens
- Animation transform values (e.g., `translateY(30px)`) are implementation details, not design tokens
- Border radius for specific components may not have a token — document the value and suggest it be tokenized

---

## Performance

### Font Loading

Provider-specific preconnect + `display=swap` (see brand-integration.md). Without preconnect, font loading can add 300-500ms to first paint.

Test: Load the page on a throttled connection (3G). The page should be readable with system fonts before web fonts load, then swap smoothly.

### Image Handling

- Use `loading="lazy"` on all images below the fold
- Set explicit `width` and `height` attributes (or use `aspect-ratio` in CSS) to prevent layout shift
- For hero images: preload with `<link rel="preload" as="image">`
- Prefer SVG for icons and illustrations. For photos, WebP with JPEG fallback.

### Animation Performance

- Only animate `transform` and `opacity`. Never animate `width`, `height`, `top`, `left`, `margin`, or `padding`.
- Use `will-change: transform` sparingly and only on elements that actually animate
- Parallax calculations in `requestAnimationFrame`, not scroll event handlers
- Scroll listeners with `{ passive: true }`

### Critical Rendering

- CSS in a `<style>` block in `<head>` for single-file prototypes (no render-blocking external stylesheet)
- JavaScript at end of `<body>` or with `defer`
- No blocking third-party scripts unless absolutely required

### Targets

- First Contentful Paint: under 1.5s on broadband
- Cumulative Layout Shift: under 0.1
- Loading animation (when present): completes in 2-2.5s, then page is fully interactive

---

## Layout & Responsive

### Breakpoint Testing

Test at these widths:
- 375px (iPhone SE / small phones)
- 428px (iPhone Pro Max / large phones)
- 768px (iPad portrait)
- 1024px (iPad landscape / small laptops)
- 1440px (standard desktop)
- 1920px (large desktop)

### What to Check at Each Breakpoint

**375px:**
- No horizontal scroll
- Text readable without zooming (minimum 15px body)
- Touch targets at least 44x44px
- Navigation accessible (hamburger or simplified)
- Grid layouts collapse to single column
- Hero text scales down gracefully (clamp handles this)

**768px:**
- Two-column layouts work
- Navigation may start showing full menu
- Grid items can go 2-up
- Adequate horizontal padding

**1440px:**
- Content max-width constraint active
- Generous whitespace around content
- Full multi-column layouts
- Type scale at upper clamp bounds

### Common Failures

- Horizontal overflow from fixed-width elements
- Grid gaps too tight on mobile
- Nav items wrapping awkwardly between breakpoints
- Hero text overlapping or losing impact at breakpoints
- Parallax too aggressive on small screens (reduce or disable below 768px)

---

## Interaction Quality

### Hover States

Every interactive element needs a hover state. The interaction vocabulary from interaction-patterns.md:

- **Text links:** underline grows from left (width 0 to 100%, 300ms)
- **Buttons:** subtle translateY(-2px) lift, or background color shift
- **Cards:** border-color shift to accent, or slight scale (1.01-1.02)
- **Navigation items:** color shift toward primary text from muted
- **CTA arrows:** gap between text and arrow increases

### Loading and Transition States

- Buttons that trigger async actions: disable and show loading indicator
- Content that loads asynchronously: use skeleton or shimmer, not spinners
- State changes: animate smoothly (150-300ms), don't snap

---

## Typography Quality

### Type Hierarchy Verification

Check that the type hierarchy creates clear visual levels:
1. Hero headline: largest, display font, maximum weight contrast
2. Section headings: clearly subordinate to hero but dominant in their section
3. Subsection headings: body font at larger size, or display font at smaller size
4. Body text: comfortable reading size, adequate line-height (1.5-1.7)
5. Labels/metadata: utility font, small, uppercase if convention dictates, letter-spaced

If any two adjacent levels look too similar, increase contrast. Scale, weight, and font family are all tools for separation.

### Line Length

Body text: 50-75 characters per line.

```css
p, .lead { max-width: 65ch; }
```

### Orphans and Widows

Check large display text for awkward line breaks. Solutions:
- `text-wrap: balance` (progressive enhancement)
- Manual `<br>` at chosen break points with responsive display
- Container width adjustment

---

## Code Quality

### HTML Semantics

- `<nav>` for navigation
- `<section>` with headings for content sections
- `<article>` for self-contained content blocks
- `<footer>` for page/section footers
- `<button>` for clickable actions, `<a>` for navigation
- No `<div>` or `<span>` when a semantic element exists

### CSS Organization

For single-file prototypes:
1. Custom properties (`:root { ... }`)
2. Reset/base styles
3. Typography
4. Layout (grid, containers)
5. Components (nav, cards, sections)
6. Utilities (reveal animations, states)
7. Media queries
8. Reduced motion query (always last)

### JavaScript Patterns

- `IntersectionObserver` over scroll event listeners for visibility detection
- `requestAnimationFrame` for animation calculations
- Event delegation where possible
- `{ passive: true }` on scroll/touch listeners
- No heavy frameworks for prototypes
- `DOMContentLoaded` or end-of-body placement

### No Console Errors

Before delivery, trace through the JavaScript:
- Are all `querySelector` targets guaranteed to exist?
- Are event listeners attached to elements in the DOM?
- Are there any undefined variable references?
- Do all `IntersectionObserver` callbacks handle edge cases?

---

## Component Library Alignment

### Before Building

1. Check the component inventory in the brand config
2. Search for existing components that match or overlap with what you're building
3. Review the library's naming, prop, and variant conventions

### When Using Existing Components

- Use the component's documented API (props, variants, slots)
- Don't override internal styles unless the component exposes customization tokens
- If you need something the component doesn't support, extend rather than replace

### When Building New Components

- Follow the naming conventions from `components.conventions.naming`
- Match the prop API style from `components.conventions.props`
- Use variant naming from `components.conventions.variants`
- Document the new component for potential library contribution

---

## Pre-Delivery Checklist (Condensed)

Run through before handing off any UI work:

- [ ] Brand tokens applied (all visual values trace to design tokens)
- [ ] Voice rules followed (all prohibited words/patterns checked)
- [ ] Contrast ratios verified for all text/background combinations
- [ ] Keyboard navigable (Tab through all interactive elements)
- [ ] Focus states visible
- [ ] `prefers-reduced-motion` respected
- [ ] Tested at 375px, 768px, 1440px
- [ ] No horizontal scroll at any viewport
- [ ] All animations have a purpose
- [ ] Section layouts varied (no repeating patterns)
- [ ] Type hierarchy creates clear visual levels
- [ ] Hover states on all interactive elements
- [ ] Semantic HTML throughout
- [ ] No console errors
- [ ] Fonts load with display=swap and preconnect
- [ ] Existing components used where available (no unnecessary rebuilds)
- [ ] New components follow library conventions
- [ ] No raw hex/font/spacing values outside of :root token definitions

## Forms & Feedback

These rules apply to form-heavy interfaces (the MEDIUM-priority "Forms & Feedback" item flagged in the table above).

- **Validate on blur, not keystroke.** Show field errors only after the user finishes input (on blur), not while they're still typing.
- **Autofill support.** Use `autocomplete` attributes on all form inputs. Maps directly to user-expected autofill behavior and reduces friction.
- **Password show/hide toggle.** Include a visibility toggle on all password fields. No exceptions for "security reasons": hiding the toggle harms UX without improving security.
- **Sheet and modal dismiss confirmation.** When dismissing a sheet or modal with unsaved changes, confirm before closing. Silence is data loss.
- **Focus management on submit error.** After a failed form submission, `focus()` the first invalid field. Do not leave focus in an ambiguous state.
- **Multi-step progress indicator.** Forms spanning more than 2 steps require a visible step indicator. Allow back navigation between steps.
- **Undo for destructive actions.** When a user deletes or bulk-removes content, offer an undo action (toast with undo button, 5-second window).
- **Error message clarity.** Error messages must state the cause and the fix, not just "Invalid input." "Email must include @ symbol" beats "Invalid email."
- **Input height minimum on mobile.** All form inputs must meet the 44px touch target minimum on mobile, not just buttons.
- **Form autosave.** Long or multi-step forms should autosave drafts. Accidental dismissal should not destroy work.

---

*Reference for ui-studio skill. Originally authored for design-system-ux, March 2026.*

*HeyHi Confidential*
