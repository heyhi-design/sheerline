# Interaction Pattern Library

Implementation reference for UI micro-interactions and motion design. Every pattern includes working code that can be dropped into a single-file HTML prototype. All patterns use CSS custom properties for brand tokens — replace the variable references with values from your brand config.

These are base patterns. The companion `design-system-patterns` skill can generate brand-specific variants that extend this library with custom interaction vocabulary.

---

## Table of Contents

1. [Loading States](#1-loading-states)
2. [Hero Text Reveal](#2-hero-text-reveal)
3. [Scroll Reveal (Intersection Observer)](#3-scroll-reveal)
4. [Staggered Children Reveal](#4-staggered-children)
5. [Parallax](#5-parallax)
6. [Marquee](#6-marquee)
7. [Nav Scroll State](#7-nav-scroll-state)
8. [Hover Micro-interactions](#8-hover-micro-interactions)
9. [CTA Arrow Animation](#9-cta-arrow)
10. [Card Hover Effects](#10-card-hover)
11. [Section Background Transitions](#11-section-backgrounds)
12. [Smooth Scroll Anchors](#12-smooth-scroll)

---

## Token Variables Used

All patterns reference these CSS custom properties. Map them from your brand config before use:

```css
:root {
  /* From brand config — these are placeholders */
  --ff-display: /* config.tokens.typography.families.display */;
  --ff-body:    /* config.tokens.typography.families.body */;
  --ff-utility: /* config.tokens.typography.families.utility */;

  --bg:      /* config.tokens.color.backgrounds.primary */;
  --dark:    /* config.tokens.color.backgrounds.inverted */;
  --dark-mid:/* config.tokens.color.backgrounds.inverted_hover */;
  --text:    /* config.tokens.color.text.primary */;
  --muted:   /* config.tokens.color.text.muted */;
  --accent:  /* config.tokens.color.accent.primary */;
  --accent-l:/* config.tokens.color.accent.light */;
  --divider: /* config.tokens.color.structural.divider */;
  --warm:    /* config.tokens.color.text.inverted_secondary */;

  --ease-default: /* config.tokens.motion.easing.default */;
  --ease-reveal:  /* config.tokens.motion.easing.reveal */;
}
```

---

## Baseline Timing and Easing

When `config.tokens.motion` is not populated, use these fallback values. When the config has motion tokens, those values take precedence — the CSS variables in every pattern below accept them automatically via `var(--ease-default)` and `var(--ease-reveal)`.

**Easing curves:**

| Variable | Curve | Use |
|----------|-------|-----|
| `--ease-default` | `cubic-bezier(0.65, 0, 0.35, 1)` | General transitions — state changes, hovers, nav |
| `--ease-reveal` | `cubic-bezier(0.33, 1, 0.68, 1)` | Entrances and reveals — elements arriving into view |

**Duration ranges:**

| Category | Range | Use |
|----------|-------|-----|
| Micro-interactions | 150–300ms | Hover states, focus rings, button press, state toggles |
| Scroll reveals / entrances | 600–800ms | Elements entering the viewport, hero text |
| Stagger offset | 60–100ms per child | Grid reveals, list items, cascading sequences |

**Config token mapping:** When `config.tokens.motion` is populated, map its fields to these CSS variables. The config may store easing values as CSS cubic-bezier strings, named shorthand (e.g., "standard", "decelerate"), or omit the field entirely.

| Config field | Maps to CSS variable | If missing or non-string value |
|---|---|---|
| `tokens.motion.easing.default` | `--ease-default` | Use `cubic-bezier(0.65, 0, 0.35, 1)` |
| `tokens.motion.easing.reveal` | `--ease-reveal` | Use `cubic-bezier(0.33, 1, 0.68, 1)` |
| `tokens.motion.easing.micro` | `--ease-micro` (if present) | Use `ease-out` |
| `tokens.motion.duration.micro_min` | Set floor of micro range | Use 150ms |
| `tokens.motion.duration.micro_max` | Set ceiling of micro range | Use 300ms |
| `tokens.motion.duration.reveal_min` | Set floor of reveal range | Use 600ms |
| `tokens.motion.duration.reveal_max` | Set ceiling of reveal range | Use 800ms |
| `tokens.motion.stagger` | Set stagger offset | Use 80ms |

**Procedure:** Read `tokens.motion` from the config before building. Assign each field to its CSS variable. If the field is a named shorthand (not a cubic-bezier string), look up the equivalent value in the brand config's motion glossary — or document the gap and use the fallback. Never leave a CSS variable unset; the fallback values ensure consistent behavior even on an incomplete config.

**`prefers-reduced-motion` mapping by effect type:**

Not all motion should be treated identically. The question is whether motion communicates information or is purely aesthetic.

| Effect type | Reduced-motion behavior | Rationale |
|---|---|---|
| Loading animation (letter reveal, line grow) | **Eliminate** — show final state immediately | Purely atmospheric; delay without the animation is just delay |
| Hero text reveal (translateY entrance) | **Eliminate** — set `transform: none; opacity: 1` immediately | The text must be readable; the entrance is decorative |
| Scroll reveals (`[data-reveal]`) | **Eliminate** — set `opacity: 1; transform: none` at parse time | Hidden content that never appears is an accessibility failure |
| Stagger cascades | **Eliminate** — remove `transitionDelay` from all children | Stagger is a purely aesthetic sequencing device |
| Parallax | **Eliminate** — set `transform: none` in the scroll handler | Parallax can trigger vestibular symptoms; eliminate entirely |
| Marquee | **Eliminate** — pause the animation (`animation-play-state: paused`) | Continuous motion is high-risk for vestibular users |
| Hover micro-interactions (underline grow, button lift) | **Reduce** — instant state change instead of transition | State change communicates information; preserve it, remove the duration |
| Nav scroll state (background transition) | **Reduce** — instant background swap, no blur transition | The background state is informational; preserve, remove the transition |
| Section background color | **Reduce** — no transition between states | Background color is structural, not decorative |
| Focus states | **Keep unchanged** — never suppress focus transitions | Focus indicators are functional and required for keyboard users |

**Implementation pattern:**

```css
@media (prefers-reduced-motion: reduce) {
  /* Eliminate: loading, reveals, parallax, marquee */
  .loader { display: none; }
  [data-reveal] { opacity: 1; transform: none; transition: none; }
  [data-reveal-stagger] > * { opacity: 1; transform: none; transition: none; }
  .marquee-track { animation-play-state: paused; }

  /* Reduce: hover and state transitions become instant */
  .nav-link::after,
  .btn,
  .case-card,
  .service-card,
  nav { transition: none; }
}
```

In JavaScript: check `window.matchMedia('(prefers-reduced-motion: reduce)').matches` before initializing parallax scroll listeners and `IntersectionObserver` reveal logic. If reduced motion is active, set the final state directly and skip the observer setup.

```javascript
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

if (!prefersReducedMotion) {
  // Initialize scroll reveals, parallax, stagger observers
  document.querySelectorAll('[data-reveal]').forEach(el => revealObserver.observe(el));
} else {
  // Apply final states immediately
  document.querySelectorAll('[data-reveal]').forEach(el => {
    el.style.opacity = '1';
    el.style.transform = 'none';
  });
}
```

---

## 1. Loading States

A brief mood-setting sequence. Use for landing pages and major entry points. Keep total duration under 2.5 seconds.

**Pattern: Letter-by-letter reveal with growing line**

```html
<div class="loader" id="loader">
  <div class="loader-word">
    <!-- Split brand name into individual spans -->
    <span>B</span><span>r</span><span>a</span><span>n</span><span>d</span>
  </div>
  <div class="loader-line" id="loader-line"></div>
  <div class="loader-sub" id="loader-sub">Tagline Here</div>
</div>
```

```css
.loader {
  position: fixed;
  inset: 0;
  z-index: 1000;
  background: var(--dark);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition: opacity 0.6s var(--ease-default), visibility 0.6s;
}

.loader.done {
  opacity: 0;
  visibility: hidden;
  pointer-events: none;
}

.loader-word {
  font-family: var(--ff-display);
  font-size: clamp(3rem, 8vw, 6rem);
  font-weight: 300;
  color: var(--bg);
  letter-spacing: 0.04em;
  overflow: hidden;
}

.loader-word span {
  display: inline-block;
  transform: translateY(110%);
  transition: transform 0.7s var(--ease-reveal);
}

.loader-word span.show {
  transform: translateY(0);
}

.loader-line {
  width: 0;
  height: 1px;
  background: var(--warm);
  margin-top: 1.5rem;
  transition: width 1.2s var(--ease-default);
}

.loader-line.grow { width: 120px; }

.loader-sub {
  font-family: var(--ff-utility);
  font-size: 0.55rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--muted);
  margin-top: 1rem;
  opacity: 0;
  transform: translateY(8px);
  transition: opacity 0.5s, transform 0.5s var(--ease-reveal);
}

.loader-sub.show { opacity: 1; transform: translateY(0); }
```

```javascript
(function() {
  const letters = document.querySelectorAll('.loader-word span');
  const line = document.getElementById('loader-line');
  const sub = document.getElementById('loader-sub');
  const loader = document.getElementById('loader');

  letters.forEach((letter, i) => {
    setTimeout(() => letter.classList.add('show'), 200 + i * 80);
  });
  setTimeout(() => line.classList.add('grow'), 600);
  setTimeout(() => sub.classList.add('show'), 1000);
  setTimeout(() => {
    loader.classList.add('done');
    if (typeof animateHero === 'function') animateHero();
  }, 2200);
})();
```

**Timing guidance:** Letters stagger at 80ms. Line grows at 600ms. Subtitle appears at 1000ms. Loader dismisses at 2200ms. Adjust timings to match the brand's motion principles — some brands want snappier (reduce all by 20-30%), some want more languid (increase by 20-30%).

---

## 2. Hero Text Reveal

Split headline into lines, reveal each with a vertical translate and opacity transition.

```html
<h1>
  <span class="line"><span class="line-inner">First line of headline</span></span>
  <span class="line"><span class="line-inner">Second line with <em>emphasis</em></span></span>
  <span class="line"><span class="line-inner">Third line closing thought.</span></span>
</h1>
```

```css
.hero h1 .line {
  display: block;
  overflow: hidden;
}

.hero h1 .line-inner {
  display: block;
  transform: translateY(110%);
  opacity: 0;
}
```

```javascript
function animateHero() {
  const lines = document.querySelectorAll('.hero .line-inner');
  lines.forEach((line, i) => {
    setTimeout(() => {
      line.style.transition = `transform 0.8s var(--ease-reveal, cubic-bezier(0.33, 1, 0.68, 1)), opacity 0.8s ease`;
      line.style.transform = 'translateY(0)';
      line.style.opacity = '1';
    }, 200 + i * 150);
  });
}
```

**Stagger:** 150ms between lines. The italic emphasis on key phrases creates visual interest within the animation.

---

## 3. Scroll Reveal

Single elements that fade and translate up when they enter the viewport.

```css
[data-reveal] {
  opacity: 0;
  transform: translateY(30px);
}

[data-reveal].revealed {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 0.8s var(--ease-reveal, cubic-bezier(0.33, 1, 0.68, 1)),
              transform 0.8s var(--ease-reveal, cubic-bezier(0.33, 1, 0.68, 1));
}
```

```javascript
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('revealed');
      revealObserver.unobserve(entry.target);
    }
  });
}, {
  threshold: 0.12,
  rootMargin: '0px 0px -60px 0px'
});

document.querySelectorAll('[data-reveal]').forEach(el => revealObserver.observe(el));
```

**Usage:** Add `data-reveal` to any element. The negative rootMargin means elements reveal when they're 60px above the bottom of the viewport.

---

## 4. Staggered Children

Container-level animation where children cascade in sequence.

```css
[data-reveal-stagger] > * {
  opacity: 0;
  transform: translateY(25px);
}

[data-reveal-stagger].revealed > * {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 0.6s var(--ease-reveal, cubic-bezier(0.33, 1, 0.68, 1)),
              transform 0.6s var(--ease-reveal, cubic-bezier(0.33, 1, 0.68, 1));
}
```

```javascript
// Inside the IntersectionObserver callback:
if (entry.target.hasAttribute('data-reveal-stagger')) {
  const children = entry.target.children;
  Array.from(children).forEach((child, i) => {
    child.style.transitionDelay = `${i * 0.08}s`;
  });
}
```

**Stagger:** 80ms per child. For grids with 8+ items, cap the max delay at ~500ms.

---

## 5. Parallax

Differential scroll speeds between elements. Keep it subtle.

```javascript
const section = document.querySelector('.split-section');
window.addEventListener('scroll', () => {
  requestAnimationFrame(() => {
    const rect = section.getBoundingClientRect();
    const progress = (window.innerHeight - rect.top) / (window.innerHeight + rect.height);
    if (progress > 0 && progress < 1) {
      const leftEl = section.querySelector('.left');
      const rightEl = section.querySelector('.right');
      if (leftEl) leftEl.style.transform = `translateY(${(progress - 0.5) * -30}px)`;
      if (rightEl) rightEl.style.transform = `translateY(${(progress - 0.5) * 15}px)`;
    }
  });
}, { passive: true });
```

**Movement range:** -30px to +15px. Asymmetric movement creates depth. Always `requestAnimationFrame` and `{ passive: true }`.

---

## 6. Marquee

Infinite horizontal scroll for capability lists, service tags, or partner logos.

```html
<div class="marquee">
  <div class="marquee-track">
    <span class="marquee-item">Item One</span>
    <span class="marquee-dot">&bull;</span>
    <span class="marquee-item">Item Two</span>
    <span class="marquee-dot">&bull;</span>
    <!-- Duplicate the full set for seamless loop -->
    <span class="marquee-item">Item One</span>
    <span class="marquee-dot">&bull;</span>
    <span class="marquee-item">Item Two</span>
    <span class="marquee-dot">&bull;</span>
  </div>
</div>
```

```css
.marquee {
  overflow: hidden;
  white-space: nowrap;
  border-top: 1px solid var(--divider);
  border-bottom: 1px solid var(--divider);
  padding: 1rem 0;
}

.marquee-track {
  display: inline-flex;
  animation: marquee 40s linear infinite;
}

.marquee-item {
  font-family: var(--ff-utility);
  font-size: 0.58rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--muted);
  padding: 0 2.5rem;
  flex-shrink: 0;
}

@keyframes marquee {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}
```

**Speed:** 40s for moderate pace. Content must be duplicated for seamless `-50%` loop. Atmospheric, not attention-grabbing.

---

## 7. Nav Scroll State

Transparent nav that gains background on scroll.

```css
nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  transition: background 0.4s, backdrop-filter 0.4s;
}

nav.scrolled {
  background: rgba(from var(--bg) r g b / 0.9);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
}
```

```javascript
const nav = document.getElementById('nav');
let ticking = false;

window.addEventListener('scroll', () => {
  if (!ticking) {
    requestAnimationFrame(() => {
      nav.classList.toggle('scrolled', window.scrollY > 60);
      ticking = false;
    });
    ticking = true;
  }
}, { passive: true });
```

**Note:** The `rgba(from var(--bg) ...)` syntax uses relative color syntax. For broader browser support, hardcode the rgba value from your brand config's background color.

---

## 8. Hover Micro-interactions

**Link underline grow:**
```css
.nav-link {
  position: relative;
}

.nav-link::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 0;
  height: 1px;
  background: var(--accent);
  transition: width 0.3s var(--ease-default);
}

.nav-link:hover::after {
  width: 100%;
}
```

**Button lift:**
```css
.btn:hover {
  transform: translateY(-2px);
  transition: transform 0.2s;
}
```

**Row highlight:**
```css
.service-row {
  transition: background 0.3s;
}

.service-row:hover {
  background: var(--accent-l);
  margin: 0 -1rem;
  padding-left: 1rem;
  padding-right: 1rem;
  border-radius: 2px;
}
```

---

## 9. CTA Arrow

Arrow that extends on hover.

```html
<a href="#" class="cta-link">
  Call to action text
  <span class="cta-arrow"></span>
</a>
```

```css
.cta-link {
  display: inline-flex;
  align-items: center;
  gap: 0.8rem;
  transition: gap 0.3s var(--ease-default);
}

.cta-link:hover { gap: 1.2rem; }

.cta-arrow {
  display: inline-block;
  width: 32px;
  height: 1px;
  background: currentColor;
  position: relative;
  transition: width 0.3s var(--ease-default);
}

.cta-arrow::after {
  content: '';
  position: absolute;
  right: 0;
  top: -3px;
  width: 8px;
  height: 8px;
  border-top: 1px solid currentColor;
  border-right: 1px solid currentColor;
  transform: rotate(45deg);
}

.cta-link:hover .cta-arrow { width: 48px; }
```

---

## 10. Card Hover

Subtle lift with optional border color shift.

```css
.case-card {
  transition: transform 0.4s var(--ease-default);
}

.case-card:hover {
  transform: translateY(-4px);
}

/* Alternative: border color shift */
.service-card {
  border: 1px solid var(--divider);
  transition: border-color 0.2s;
}

.service-card:hover {
  border-color: var(--accent);
}
```

---

## 11. Section Backgrounds

Use inverted sections to break monotony. Place strategically to create rhythm.

```css
.dark-section {
  background: var(--dark);
  color: var(--bg);
}

.dark-section .muted-text {
  color: var(--warm);  /* Use the brand's inverted-secondary color */
}

.dark-section .accent-text {
  color: var(--accent);
}
```

**Key:** Dark sections should match the brand temperature. Warm brands use warm darks. Cool brands can use true darks.

---

## 12. Smooth Scroll

Anchor links with offset for fixed nav.

```javascript
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      const offset = 80; // nav height + buffer
      const top = target.getBoundingClientRect().top + window.pageYOffset - offset;
      window.scrollTo({ top, behavior: 'smooth' });
    }
  });
});
```

---

## Pattern Selection Guide

| Situation | Patterns to use |
|-----------|----------------|
| Landing page / homepage | Loading state, hero reveal, scroll reveals, marquee, parallax, nav state |
| Internal tool / dashboard | Nav state, card hovers, scroll reveals (no loading state, no marquee) |
| Case study page | Hero reveal, parallax on images, scroll reveals, section backgrounds |
| Component prototype | Card hovers, micro-interactions only |
| Presentation / pitch prototype | Loading state, hero reveal, full interaction suite |

---

## Extending with Brand-Specific Patterns

The `design-system-patterns` companion skill can generate additional patterns tailored to a specific brand's interaction vocabulary. Those patterns are stored in `brand-config/custom-patterns/` and supplement (not replace) this base library.

---

*Base interaction patterns for ui-studio skill. Originally authored for design-system-ux, All code is vanilla HTML/CSS/JS with no external dependencies.*

*HeyHi Confidential*

---

## CSS Scroll-Driven Animations

*Added 2026-04-18. Browser support: Chrome 115+, Edge 115+, Safari 26+ (beta). For production, use the progressive enhancement pattern.*

**Two timeline types — understand before choosing:**

`scroll()` creates a **ScrollTimeline**: animation progress mapped to how far the *scroll container* has traveled. Use for reading progress bars and global scroll-linked effects.

`view()` creates a **ViewTimeline**: animation progress mapped to a *specific element's* position within the viewport. Use for enter-viewport reveals. The `entry` / `exit` range keywords are **only valid with `view()`** — never combine them with `scroll()`.

```css
/* ScrollTimeline — reading progress bar */
.progress-bar {
  animation: grow-width linear;
  animation-timeline: scroll(root block);
  transform-origin: left;
}

/* ViewTimeline — fade-in as element enters viewport */
@keyframes fade-in {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}

.reveal {
  animation: fade-in linear both;
  animation-timeline: view();
  animation-range: entry 10% entry 40%; /* entry keyword ONLY valid with view() */
}
```

**Progressive enhancement — @supports wrapper + JS fallback:**

```css
@supports (animation-timeline: scroll()) {
  .reveal {
    animation: fade-in linear both;
    animation-timeline: view();
    animation-range: entry 10% entry 40%;
  }
}

/* Fallback — triggered via JS when scroll-driven is unavailable */
.reveal {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.4s ease, transform 0.4s ease;
}
.reveal.is-visible {
  opacity: 1;
  transform: none;
}
```

```js
if (!CSS.supports('animation-timeline: scroll()')) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    },
    { rootMargin: '-60px 0px' }
  );
  document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));
}
```

**When to use:** Reading progress bars, parallax effects, sticky state changes, scroll-linked reveals. These are zero-JavaScript, high-performance effects. For complex logic (stagger, conditional reveals, callback-dependent behavior), IntersectionObserver remains the right tool.

---

## View Transitions API

*Added 2026-04-18. Browser support: Same-document — Chrome 111+, Firefox 133+, Safari 18+ (Baseline Newly Available, October 2025). Cross-document — Chrome 126+, Safari 18.2+.*

**Capability:** Smooth animated transitions between DOM states — page navigations, content swaps, tab changes — without complex JavaScript or a full SPA router.

```javascript
// Wrap any DOM change
document.startViewTransition(() => {
  updateDOM(); // swap content, change routes, etc.
});
```

```css
::view-transition-old(root) { animation: slide-out 0.3s ease-in; }
::view-transition-new(root) { animation: slide-in 0.3s ease-out; }

/* Named transition for a specific element */
.hero-image { view-transition-name: hero; }
```

**Cross-document (MPA):** Add `@view-transition { navigation: auto; }` to CSS. The browser handles page transition animations automatically — no JavaScript required.

**React Router integration (production-safe):**

```jsx
import { useNavigate } from 'react-router-dom';

function NavLink({ to, children }) {
  const navigate = useNavigate();
  const handleClick = (e) => {
    e.preventDefault();
    if (!document.startViewTransition) {
      navigate(to); // fallback: unsupported browsers
      return;
    }
    document.startViewTransition(() => { navigate(to); });
  };
  return <a href={to} onClick={handleClick}>{children}</a>;
}
```

React Router v6.28+ added `unstable_viewTransition` prop on `<Link>` — handles this automatically but remains unstable API. The manual wrapper above is production-safe.

**When to use:** Page-level transitions in Astro or MPA builds. Content swaps in dashboards. A content site should use same-document transitions for route changes rather than CSS opacity fades.

For React-component-level motion (exit animations, layout transitions, gesture-driven animation), see `framer-motion-patterns.md` instead.

---

## Animation Constraints

The following rules govern all motion in builds produced by this skill. These supplement the patterns above.

- **Exit faster than enter.** Exit animations should run at 60–70% of the enter duration. A 600ms reveal exits in ~380ms. Faster exits feel more responsive.
- **Animations must be interruptible.** A user tap or gesture must cancel an in-flight animation immediately. No animation should hold the interface hostage.
- **Never block user input.** UI must stay fully interactive during any animation — no `pointer-events: none` on the page container while motion is running.
- **Modal motion from source.** Modals and sheets animate from their trigger element (scale + fade from trigger point) to maintain spatial context.
- **Spring physics over cubic-bezier for large elements.** For elements moving significant distances (hero reveals, full-screen transitions), spring/physics-based easing reads as more natural than a fixed curve. Use CSS `linear()` or JS spring if needed.
- **Shared element transitions for navigation.** When navigating between states where an element persists (e.g., a card expanding to a full view), use shared element / hero transition to maintain spatial continuity.

**Note on stagger timing:** the 60–100ms stagger spec is intentional for sparse editorial reveals with larger, heavier elements. Do not reduce it to a dense-list 30–50ms cadence unless the brief calls for dense list reveals.
