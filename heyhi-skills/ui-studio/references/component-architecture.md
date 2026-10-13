---
name: component-architecture
zone: 2
load_trigger: Build requires headless UI components, compound component patterns, Server Components architecture, or Suspense/ErrorBoundary composition
token_estimate: ~1100
classification: HeyHi Internal Use Only
created: 2026-04-18
version: "1.0.0"
---

# Component Architecture Reference

Reference for React component architecture patterns as of April 2026. Load when a build requires headless UI primitives (Radix), compound components, polymorphic components, Suspense+ErrorBoundary nesting, or Server Component boundaries.

The companion file `form-patterns.md` covers React Hook Form + Zod — load that when forms are part of the build.

---

## Where the Field Is

Three forces define current React component architecture:

**1. Behavior/style separation.** Headless component libraries (Radix, Ariakit, Base UI) separate accessible behavior from visual styling. The library owns ARIA, keyboard navigation, and focus management. You own all styling.

**2. Composition patterns.** Compound components, Slots, and polymorphic components are table stakes for design-system-aware application APIs.

**3. React maturity.** Suspense, Error Boundaries, `React.lazy`, and Server Components are the expected baseline for production React — not experimental features.

---

## Headless UI: Radix Primitives

Radix handles every complex interactive component — Dialog, Dropdown, Tooltip, Select, Tabs, Accordion, etc. — with full WAI-ARIA compliance, keyboard navigation, and focus management.

**Mental model:** Radix manages behavior. You manage appearance.

```jsx
import * as Dialog from '@radix-ui/react-dialog';

// Radix manages: focus trap, aria-labelledby, escape key, scroll lock
// You control: all visual styling
<Dialog.Root>
  <Dialog.Trigger asChild>
    <button className="your-trigger-styles">Open</button>
  </Dialog.Trigger>
  <Dialog.Portal>
    <Dialog.Overlay className="your-overlay-styles" />
    <Dialog.Content className="your-content-styles">
      <Dialog.Title>Dialog Title</Dialog.Title>
      <Dialog.Description>Description here.</Dialog.Description>
      <Dialog.Close asChild>
        <button>Close</button>
      </Dialog.Close>
    </Dialog.Content>
  </Dialog.Portal>
</Dialog.Root>
```

**When to use Radix vs. alternatives:**

| Component type | Approach |
|---------------|---------|
| Tooltip, Dropdown, Dialog, Popover, Select, Tabs, Accordion | **Radix — always.** Accessibility complexity is non-trivial. |
| Button, Card, Badge, Tag, Avatar | **Build from scratch.** Stateless or trivially stateful. |
| Complex data tables, date pickers | **Radix or specialized library.** Evaluate per project. |
| 90%+ headless behavior matches but one interaction needs customization | **Fork and extend.** Preserve the accessibility foundation, override the specific behavior. |

Build from scratch only when a specific, named constraint demands it: strict bundle size limits (embedded contexts), security-restricted environments requiring formal dependency approval, or accessibility requirements that exceed current library support.

**The `asChild` prop** — Radix's composability API. Merges Radix behavior onto your component without adding a DOM wrapper node.

```jsx
<Dialog.Trigger asChild>
  <MyButton variant="primary">Open dialog</MyButton>
</Dialog.Trigger>
```

**Alternatives:** React Aria (Adobe — more complete, more verbose), Ariakit (smaller API surface, similar philosophy). Radix is the most widely adopted in design-system contexts.

---

## Compound Component Pattern

Compound components model parent-child relationships with shared implicit state — the way `<select>` and `<option>` work in HTML.

```typescript
import React, { createContext, useContext, useState } from 'react';

// 1. Context for shared state
const AccordionContext = createContext<{
  activeId: string | null;
  toggle: (id: string) => void;
} | null>(null);

function useAccordion() {
  const ctx = useContext(AccordionContext);
  if (!ctx) throw new Error('useAccordion must be used within Accordion');
  return ctx;
}

// 2. Root component — owns state
function Accordion({ children }: { children: React.ReactNode }) {
  const [activeId, setActiveId] = useState<string | null>(null);
  const toggle = (id: string) => setActiveId(prev => prev === id ? null : id);
  return (
    <AccordionContext.Provider value={{ activeId, toggle }}>
      {/* Accordion is NOT a list — do not use role="list" */}
      <div>{children}</div>
    </AccordionContext.Provider>
  );
}

// 3. Sub-components — correct WAI-ARIA accordion pattern:
//    button[aria-expanded][aria-controls] → div[role="region"][aria-labelledby]
function AccordionItem({
  id, title, children
}: { id: string; title: string; children: React.ReactNode }) {
  const { activeId, toggle } = useAccordion();
  const isOpen = activeId === id;
  const triggerId = `accordion-trigger-${id}`;
  const panelId = `accordion-panel-${id}`;
  return (
    <div>
      <button
        id={triggerId}
        onClick={() => toggle(id)}
        aria-expanded={isOpen}
        aria-controls={panelId}
      >
        {title}
      </button>
      {isOpen && (
        <div id={panelId} role="region" aria-labelledby={triggerId}>
          {children}
        </div>
      )}
    </div>
  );
}

// 4. Attach sub-components to parent
Accordion.Item = AccordionItem;

// Usage
<Accordion>
  <Accordion.Item id="a" title="First">Content A</Accordion.Item>
  <Accordion.Item id="b" title="Second">Content B</Accordion.Item>
</Accordion>
```

**Note:** For production accordions, use `@radix-ui/react-accordion` — it handles keyboard navigation (arrow keys, Home/End) and the full WAI-ARIA pattern correctly. The pattern above illustrates the architecture; Radix is the correct production choice for this component type.

---

## Polymorphic Components

A polymorphic component renders as different HTML elements based on an `as` prop, while preserving TypeScript type safety.

```typescript
import { ElementType, ComponentPropsWithoutRef } from 'react';

type PolymorphicProps<T extends ElementType, Props = {}> = Props &
  Omit<ComponentPropsWithoutRef<T>, keyof Props> & { as?: T };

function Text<T extends ElementType = 'p'>({
  as,
  children,
  className,
  ...rest
}: PolymorphicProps<T, { className?: string }>) {
  const Component = as || 'p';
  return <Component className={className} {...rest}>{children}</Component>;
}

// TypeScript infers correct props for each element type
<Text as="h1">Heading</Text>
<Text as="label" htmlFor="input">Label</Text>
<Text as="span" onClick={() => {}}>Clickable span</Text>
```

**When to use:** Typography components, Box/Stack layout primitives, button-like elements that sometimes render as links. Not needed for most components.

---

## Slots Pattern

The Slots pattern (used by Radix via `@radix-ui/react-slot`) passes behavior to a child element rather than wrapping it — keeping DOM depth minimal.

```typescript
import { Slot } from '@radix-ui/react-slot';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  asChild?: boolean;
}

function Button({ asChild, children, ...props }: ButtonProps) {
  const Comp = asChild ? Slot : 'button';
  return <Comp {...props}>{children}</Comp>;
}

// Renders as <a> with button's event handlers and props merged in
<Button asChild>
  <a href="/contact">Contact us</a>
</Button>
```

---

## Suspense + Error Boundaries

**Suspense** — declarative loading states. A component that needs data throws a Promise; Suspense catches it and shows the fallback until the data resolves.

```jsx
import { Suspense } from 'react';
import { ErrorBoundary } from 'react-error-boundary';

// Fallback UI for errors
function ErrorFallback({ error, resetErrorBoundary }) {
  return (
    <div role="alert">
      <p>Something went wrong: {error.message}</p>
      <button onClick={resetErrorBoundary}>Try again</button>
    </div>
  );
}

// Route-level pattern
<ErrorBoundary FallbackComponent={ErrorFallback} onReset={() => {}}>
  <Suspense fallback={<SkeletonCard />}>
    <UserProfile userId={id} />
  </Suspense>
</ErrorBoundary>

// Code splitting with React.lazy
const Dashboard = React.lazy(() => import('./Dashboard'));

<Suspense fallback={<div>Loading dashboard...</div>}>
  <Dashboard />
</Suspense>
```

**Nesting pattern — one boundary per independent section:**

```jsx
// Prevents one failing section from crashing or blocking the whole page
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

Each section fails independently. A broken chart does not prevent the table from loading.

**Framework notes:**
- **Next.js App Router:** `loading.tsx` files create Suspense boundaries at route level automatically. Add Suspense manually inside Server Components for granular control.
- **Vite + React (a marketing site):** `React.lazy` + Suspense for route-level code splitting. A single lazy import on large routes reduces initial bundle by 50–80%.

---

## Server Components vs. Client Components

**Default behavior (Next.js App Router):** Components are Server Components by default — run only on the server, produce no client JS, can `await` data directly.

**Decision rule:**

```
Does it need: useState, useEffect, event handlers, browser APIs, motion/animation?
  YES → add 'use client'
  NO  → Server Component (default)
```

**Push the client boundary as low as possible:**

```jsx
// page.tsx — Server Component
export default async function Page() {
  const data = await fetchData(); // Direct await, no useEffect
  return (
    <main>
      <StaticHero />               {/* Server Component */}
      <InteractiveTable data={data} /> {/* Client Component — receives data as prop */}
    </main>
  );
}
```

**Serializable props constraint.** Server Components can only pass serializable values to Client Components: strings, numbers, plain objects, arrays, `null`. Functions, class instances with methods, and `Date` objects with their prototype cannot cross the boundary.

```jsx
// ✓ Safe — serializable
<ClientComponent title="Dashboard" records={data.records} count={data.count} />

// ✗ Will throw at runtime — not serializable
// <ClientComponent onClick={() => doSomething()} />
// <ClientComponent date={new Date()} />

// Workaround for dates: pass ISO string, parse on the client
<ClientComponent createdAt={record.createdAt.toISOString()} />
// In ClientComponent: const date = new Date(props.createdAt);
```

---

## Accessibility Quality Gate for Interactive Components

**Hard block.** Before marking any interactive component complete, verify one of the following:

1. The component uses a Radix primitive (or equivalent headless library), OR
2. You have manually verified the component against the WAI-ARIA Authoring Practices for that component type

This applies to: Dialog, Dropdown, Tooltip, Select, Accordion, Tabs, Combobox, DatePicker.

No exceptions. Components that fail this gate are not shippable regardless of visual correctness.

---

*HeyHi Internal Use Only. Zone 2 — task-conditional. Load when build requires headless UI primitives, compound component patterns, or Suspense/ErrorBoundary composition. v1.0.0 created 2026-04-18 from frontend-research-reference.md v1.2.0.*
