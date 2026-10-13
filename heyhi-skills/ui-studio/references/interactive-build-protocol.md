---
name: interactive-build-protocol
zone: 2
load_trigger: Build is rated "interactive" or "immersive" in Spec Intake, or Complexity Tier Detection activates the phased structure
token_estimate: ~900
classification: HeyHi Internal Use Only
created: 2026-04-07
---

# Interactive Build Protocol

Reference for complex builds: multi-component state, custom events, and interactive proofs of system capability. Load when Complexity Tier Detection returns **Complex**, or when the build's interaction level is "interactive" or "immersive."

---

## The 4-Phase Model — Full Descriptions

The phased model exists because complex builds fail at the seams between tiers. TypeScript errors, undocumented state architecture, and mobile patterns that degrade silently all emerge when multiple complexity tiers are built at once. The phases create explicit stopping points so structural problems surface before they compound.

### Phase 1 — Aesthetic Intent

**Scope:** Lock typography, CSS variables, and color tokens. No components. No layout. No interactivity.

**What this phase produces:**
- A `:root` block with all CSS custom properties drawn from the brand config
- Google Fonts `@import` with `display=swap` and `preconnect`
- Type scale variables (`--text-xs` through `--text-display`) using `clamp()` for fluid sizing
- Color aliases (`--color-surface`, `--color-text-primary`, etc.) mapped to config token values
- Motion variables (`--duration-micro`, `--duration-reveal`, `--easing-standard`, `--easing-reveal`) from `config.motion`

**Gate before Phase 2:**
- All tokens verified against config — no arbitrary values
- CSS custom properties are the only way values enter the stylesheet; no hardcoded hex, no hardcoded `px` font sizes
- Variables render correctly in a blank HTML page (no layout, no content)

**Why this gate matters:** Token drift introduced in Phase 1 propagates through every subsequent phase. Starting clean costs nothing. Fixing it in Phase 3 costs an hour.

---

### Phase 2 — Static Structure

**Scope:** Routing (if multi-page), component scaffolding, and layout. No interactivity — no state, no event listeners, no simulated data.

**What this phase produces:**
- Component shells: correct HTML structure, semantic elements, class names, token-driven styles applied
- Layout Declaration enforced: every section matches a named pattern before CSS is written
- Static content placeholders: copy inserted as strings, images as `<img>` tags with `alt` text, no dynamic rendering
- Navigation structure if applicable

**Gate before Phase 3:**
- All components render without errors — no console errors, no missing imports, no broken references
- Layout Declaration matches the built structure: run the post-build verification from the Workflow Skeleton for static structure
- WCAG AA checked for all color combinations used in Phase 2 output
- No interactive logic present — if a component needs state, leave a `// TODO: Phase 3 — [description]` comment

**Why this gate matters:** Building interactivity on top of unverified static structure means debugging two things at once. Phase 2 isolates structural failures so Phase 3 can focus entirely on state and events.

---

### Phase 3 — Interactive Proofs

**Scope:** State, contexts, event listeners, and simulated data. The architectural decisions made in Spec Intake (component communication pattern) are implemented here.

**What this phase produces:**
- State management: React Context providers, store initialization, or DOM event infrastructure — as decided in Spec Intake
- Simulated data: live-feed simulations using `setInterval`, `requestAnimationFrame`, or randomized data generators; token sync via CSS variable writes; observability readouts from real DOM metrics
- Cross-component communication: implemented per the documented pattern (Context, DOM events, or the Mixed boundary)
- Interactive states: hover, focus, active, loading, empty, error — all token-driven

**Gate before Phase 4:**
- State management pattern is documented and consistent: no undocumented mixing of React Context and DOM events; if Mixed was declared, the boundary is implemented as specified
- Key interactions are functional: every system concept declared in Spec Intake (telemetry simulation, token sync, live data feed) is demonstrably working
- No pattern drift: the implementation matches what was decided in the Component communication pattern signal, not what was convenient to build

**Why this gate matters:** Undocumented state architecture creates debugging debt proportional to the number of components involved. The gate enforces that the pattern was chosen, not discovered.

---

### Phase 4 — Narrative Polish

**Scope:** Cross-component dialogue, mobile adaptation, and UX refinement. The site becomes coherent rather than assembled.

**What this phase produces:**
- Mobile pattern rethinking (see below): complex desktop components reviewed for `sm` breakpoint viability; patterns replaced if needed
- Animation sequence: stagger timing, reveal order, and entrance choreography coordinated across components
- Reduced motion implementation: `@media (prefers-reduced-motion: reduce)` verified across all animated elements
- UX edge cases: loading states, empty states, error states — all present and token-driven
- Content finalization: copy passes voice rules + prohibited word scan; CTAs reviewed

**Gate (this is the full quality gate from the Workflow Skeleton, step 12):**
- All five domains: Brand, Interaction, Visual, Accessibility (hard gate), Code
- Mobile patterns validated at 375px: every section tested; pattern replacements documented in Layout Declaration
- Reduced motion respected in all animations
- State management pattern matches documented decision

---

## Cross-Component Dialogue Patterns

When multiple components share state or trigger each other, the pattern must be decided before Phase 3 begins. Three options, with decision criteria.

### (a) Unified State — React Context (or lightweight store)

**Use when:**
- Multiple components read from and write to the same data model
- Components are in the same React tree
- The data has a clear owner and clear consumers
- State updates need to be synchronous and traceable

**Implementation:**
```jsx
// Define once at app root
const SystemStateContext = React.createContext(null);

export function SystemStateProvider({ children }) {
  const [state, setState] = React.useState(initialState);
  return (
    <SystemStateContext.Provider value={{ state, setState }}>
      {children}
    </SystemStateContext.Provider>
  );
}

// Consume anywhere in the tree
const { state, setState } = React.useContext(SystemStateContext);
```

**When to use Zustand instead of Context:** If the component tree is deep and re-render performance matters, or if state updates come from outside React (DOM events, WebSocket), use a lightweight store. Context re-renders all consumers on every change; Zustand only re-renders subscribed components.

---

### (b) Custom DOM Events — `window.dispatchEvent`

**Use when:**
- Components should not know about each other (loose coupling)
- Communication crosses React tree boundaries (e.g., a vanilla JS component triggering a React component)
- The trigger is fire-and-forget (no state return needed)
- Simulating event-driven architectures (telemetry events, system signals)

**Implementation:**
```js
// Dispatch
window.dispatchEvent(new CustomEvent('system:token-update', {
  detail: { token: '--color-accent', value: '#2563EB' }
}));

// Listen (in a React component)
React.useEffect(() => {
  const handler = (e) => { /* handle e.detail */ };
  window.addEventListener('system:token-update', handler);
  return () => window.removeEventListener('system:token-update', handler);
}, []);
```

**Naming convention:** Use namespaced event names (`system:`, `ui:`, `data:`) to prevent collisions. Document every custom event in the Layout Declaration or a comment block at the top of the component file.

---

### (c) Mixed Pattern — Documented Boundary

**Use when:**
- Some state is shared within a React subtree (Context), and other communication crosses tree boundaries (DOM events)
- The build calls for system concepts (telemetry, observability) that are naturally event-driven, alongside UI state that is naturally Context-driven

**The rule:** The boundary must be declared explicitly. "Context for data; DOM events for cross-tree triggers" is a valid boundary. "We'll figure it out as we build" is not.

**Example boundary declaration (to record in Spec Intake):**
> "Context manages the active token set and UI visibility state. DOM events carry telemetry signals from the simulation layer to the display components. No component reads from both patterns without passing through an adapter."

**Anti-pattern:** A component that both consumes Context and dispatches DOM events that other Context consumers react to. This creates a hidden state dependency — Context consumers are affected by DOM events, but the dependency is invisible in the component tree. If this is genuinely needed, document it as an explicit bridge and give it a name.

---

## Mid-Build Verification Checklist (Phase 2 Gate — Expanded)

Run this before leaving Phase 2. Each item is a binary pass/fail.

**Structural integrity:**
- [ ] All components render without errors in the browser console
- [ ] No `undefined` values in required props (add defaults or explicit `// Phase 3` placeholders)
- [ ] No broken imports — every referenced component, utility, and asset resolves
- [ ] Semantic HTML in every component: `<nav>`, `<section>`, `<article>`, `<header>`, `<footer>` where applicable; no `<div>` for structural elements

**Token compliance:**
- [ ] No hardcoded color values — all colors use CSS custom properties from Phase 1
- [ ] No hardcoded `px` font sizes — all type uses `clamp()` or CSS custom property variables
- [ ] No hardcoded spacing values outside the config-derived scale

**Layout compliance:**
- [ ] Layout Declaration verified: every section's grid, spacing, and structural HTML matches the declared pattern
- [ ] WCAG AA checked for all text/background color combinations present in Phase 2 output
- [ ] No interactive logic in Phase 2 output — stubs are acceptable; partial implementations are not

**Component inventory:**
- [ ] No redundant component builds — Phase 2 uses existing library components where they exist
- [ ] Every `// TODO: Phase 3` comment identifies a specific interaction, not a vague placeholder

---

## Mobile Pattern Rethinking — Before/After Reference

Applied in Phase 4. For each complex component, run this evaluation before writing mobile CSS.

**Evaluation question:** "Can this component remain functional at 375px without significant content degradation?"

If yes: restack with standard responsive CSS. If no: replace the pattern.

### Common replacements

**Vertical accordion (desktop) → Expandable sections (mobile)**
- Desktop: all sections visible, stacked vertically
- Mobile (restack): same structure, columns collapse — works if content is short
- Mobile (replace): progressive disclosure with show/hide toggle — use when content per section is more than 3–4 lines

**Bento grid (desktop) → Prioritized single column (mobile)**
- Desktop: grid of 4–6 tiles in varied sizes
- Mobile (restack): grid collapses to 2-column — works if tiles are independent and roughly equal weight
- Mobile (replace): show top 2–3 tiles, remainder behind "See more" — use when grid has a clear hierarchy and lower-priority tiles can be deferred

**Multi-column stack (desktop) → Horizontal snap-scroll (mobile)**
- Desktop: 3–5 items in a row, full content visible
- Mobile (restack): items wrap to multiple rows — works if items are short and count is ≤ 4
- Mobile (replace): horizontal snap-scroll — use when items must stay in a single row, or when count is > 4 and wrapping produces a wall of content

**Tab bar (desktop) → Accordion or paginated sections (mobile)**
- Desktop: tab bar with panel content below
- Mobile (restack): horizontal scrolling tab bar — works if tab labels are short
- Mobile (replace): accordion where tab titles become section headers — use when tab labels are long or tab count is > 4

**Document the replacement in the Layout Declaration:**
```
Section: Stack Explorer
Pattern: Multi-Column Stack
Derivation: mobile-rethink: horizontal snap-scroll at sm — 5 items cannot wrap without producing a content wall
```

---

*HeyHi Internal Use Only. Zone 2 — task-conditional. Load when interaction level is "interactive" or "immersive," or when Complexity Tier Detection activates the phased structure.*

---

## Suspense + Error Boundary Composition

*Added 2026-04-18. For complex builds in Vite + React or Next.js App Router.*

**The pattern:** Each independent data section gets its own Suspense boundary and ErrorBoundary. This prevents one failing or slow section from blocking or crashing the rest of the page.

```jsx
import { Suspense } from 'react';
import { ErrorBoundary } from 'react-error-boundary';

function ErrorFallback({ error, resetErrorBoundary }) {
  return (
    <div role="alert">
      <p>Something went wrong: {error.message}</p>
      <button onClick={resetErrorBoundary}>Try again</button>
    </div>
  );
}

// Independent sections — each fails gracefully in isolation
<main>
  <ErrorBoundary FallbackComponent={ErrorFallback}>
    <Suspense fallback={<HeaderSkeleton />}>
      <DashboardHeader />
    </Suspense>
  </ErrorBoundary>

  <ErrorBoundary FallbackComponent={ErrorFallback}>
    <Suspense fallback={<TableSkeleton />}>
      <TransactionTable />
    </Suspense>
  </ErrorBoundary>

  <ErrorBoundary FallbackComponent={ErrorFallback}>
    <Suspense fallback={<ChartSkeleton />}>
      <NetWorthChart />
    </Suspense>
  </ErrorBoundary>
</main>
```

**Code splitting (Vite + React):** `React.lazy` + Suspense at route level. A single lazy import can reduce initial bundle 50–80% on large routes.

```jsx
const Dashboard = React.lazy(() => import('./Dashboard'));

<Suspense fallback={<div>Loading...</div>}>
  <Dashboard />
</Suspense>
```

**Next.js App Router:** `loading.tsx` files create Suspense boundaries at route level automatically. Add Suspense manually inside Server Components for granular, per-section control.

**When this matters for interactive builds:** Complex interactive builds (Complexity Tier: Complex) typically load multiple data sources. Each source can fail independently. Wrapping each section prevents the cascade where one 500 error takes down the entire page. This is a structural requirement for production-ready interactive builds, not optional polish.
