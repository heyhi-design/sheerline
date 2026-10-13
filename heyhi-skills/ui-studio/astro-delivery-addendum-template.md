---
classification: "HeyHi Internal Use Only"
title: "Astro Delivery Addendum — Template"
created: 2026-04-10
version: "1.0"
status: in-progress
purpose: >
  Template for the Astro Delivery Addendum — a one-page addition to Mode A developer
  handoff when the target framework is Astro. Reduces per-engagement hydration designation
  overhead from 1–2 hours to approximately 30 minutes by providing a structured
  hydration map and implementation skeletons.
source: engineering-handoff/ui-studio-framework-compatibility.md (Astro Mitigation section)
phase_f_target: "heyhi-skills/ui-studio/SKILL.md (add as Mode A Astro path addendum)"
---

# Astro Delivery Addendum — Template

**What this is.** A template for the addendum that gets appended to Mode A developer handoff
documents when the target framework is Astro. Fill this in per engagement; do not deliver
the template itself.

**When to use.** Any Mode A build where the client's target framework is Astro. The framework
question should be confirmed in Spec Intake — if Astro is the target, include this addendum
in the Mode A handoff package.

**Why it exists.** ui-studio's HTML/CSS prototype and developer handoff do not currently
designate hydration strategy. For Astro builds, the developer must assign `client:*`
directives per component — deciding which components are static `.astro` files and which
are React Islands. Without this addendum, that designation requires a manual per-engagement
audit (1–2 hours). With this template, it takes approximately 30 minutes once the developer
handoff exists.

**Source:** `engineering-handoff/ui-studio-framework-compatibility.md` — Astro assessment
and Mitigation section.

---

## Template: Astro Delivery Addendum

*Copy this block and fill in the component list for each engagement.*

---

```markdown
## Astro Delivery Addendum

**Framework:** Astro
**Compatibility reference:** engineering-handoff/ui-studio-framework-compatibility.md
**Prepared:** [date]
**Engagement:** [client / project name]

---

### Component Hydration Map

For each component in this build, the hydration strategy is specified below.
Static components are implemented as `.astro` files with zero JavaScript budget.
Interactive components are implemented as React Islands with the specified
`client:*` directive.

| Component | Type | Directive | Rationale |
|-----------|------|-----------|-----------|
| [Nav / header] | Interactive | `client:load` | Mobile menu state |
| [Hero section] | Static | — | No client JS needed |
| [Feature grid / content sections] | Static | — | No client JS needed |
| [Testimonials / carousel] | Interactive | `client:visible` | Below fold, deferred hydration acceptable |
| [Contact form] | Interactive | `client:load` | Form validation + submission handler |
| [Footer] | Static | — | No client JS needed |
| [Embedded demo / tool] | Interactive | `client:only="react"` | Browser-only APIs or heavy dependencies |

*Adjust component list to match the actual build. Add rows as needed.*

---

### Directive Reference

| Directive | Hydration trigger | Use when |
|-----------|-----------------|----------|
| `client:load` | Immediately on page load | Component must be interactive on first paint (nav, always-visible forms) |
| `client:idle` | When browser is idle (requestIdleCallback) | Below-the-fold components that can wait until main thread is free |
| `client:visible` | When component enters the viewport | Any interactive element that may not be seen immediately |
| `client:only="react"` | Client-side only (no SSR) | Components with browser-only APIs; avoids server-render errors |

**Default rule:** If a component has no interactive behavior (state, event listeners,
dynamic data), implement it as a `.astro` file. Do not add React hydration overhead
to static content.

---

### React Island Import Pattern

For each interactive component, use this import and usage pattern in the `.astro` file:

```astro
---
// At the top of the .astro file
import ComponentName from '../components/ComponentName.tsx';
---

<!-- In the template -->
<ComponentName client:load />
```

For `client:only` components (browser-only rendering):
```astro
<ComponentName client:only="react" />
```

---

### CSS Token Integration

No changes to the token layer for Astro. Apply CSS custom properties globally:

```astro
---
// In a layout file (e.g., BaseLayout.astro)
import '../styles/tokens.css';  // Style Dictionary output
---
```

Or apply via `<style is:global>` in the layout component if bundled styles are preferred.
The type swappability pattern (single Google Fonts URL + three `--ff-*` custom properties)
applies without modification.

---

### Checklist Before Handoff

- [ ] Every component in the build is listed in the Hydration Map
- [ ] Static vs. Interactive designation is justified (not assumed)
- [ ] `client:*` directive is specified for every Interactive component
- [ ] CSS token import pattern is confirmed with the developer
- [ ] Google Fonts URL is in the layout file (not hardcoded in component files)

---

*Generated from `heyhi-skills/ui-studio/astro-delivery-addendum-template.md`*
```

---

## Notes for Phase F Propagation

When Phase F runs, two updates to `heyhi-skills/ui-studio/SKILL.md` are needed:

1. **Add "Target framework" to Mode A Spec Intake.** The framework question should be
   asked in intake, not discovered post-build. Suggested intake signal: "Target framework
   (if known): Astro / Next.js / TanStack Start / SvelteKit / other." When Astro is
   confirmed, the Astro Delivery Addendum is automatically included in the Mode A handoff.

2. **Add Astro routing note to Mode routing section.** When Astro is the target framework,
   Mode A is the correct mode (includes developer handoff). Mode B (no handoff) is not
   appropriate for Astro because the hydration designation decision belongs in the handoff
   document, not as a separate exercise. For Mode B requests targeting Astro, prompt for
   Mode A confirmation or document that hydration designation is out of scope.

These are Phase F tasks. Do not modify the deployed SKILL.md before Phase F runs.
Stage changes in `skill-updates/ui-studio-astro-update.md` if partial updates are needed
before Phase F.

---

*HeyHi Internal Use Only*
*Template file — fill in per engagement, do not deliver the template itself.*
*Version 1.0 — 2026-04-10.*
