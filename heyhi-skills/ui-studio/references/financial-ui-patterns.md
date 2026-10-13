---
name: financial-ui-patterns
zone: 2
load_trigger: Build requires financial data display — currency formatting, KPI cards, accessible charts, dashboard composition, or positive/negative value encoding
token_estimate: ~950
classification: HeyHi Internal Use Only
created: 2026-04-18
version: "1.1.0"
scope:
  - client-engagement
  - heyhi-wide
dependencies:
  - heyhi-skills/ui-studio/references/data-table-patterns.md
# Agent context layering — added 2026-04-20 (synthesis session)
# This reference extends TanStack's base Query skill with HeyHi financial domain depth.
# The TanStack Intent skill provides correct API guidance. This file provides
# AmountCell formatting conventions, allocation chart accessibility patterns, and
# net worth computation display decisions that TanStack's skill has no mandate to document.
extends: "@tanstack/intent/tanstack-query"
# VERIFY — SUSPECTED MISMATCH: This file covers display and formatting patterns (currency
# formatting, KPI cards, accessible charts, dashboard layout). It has no Query-specific
# data-fetching content. The `@tanstack/intent/tanstack-query` extends value may be wrong.
# Candidate correct values: `@tanstack/intent/tanstack-table` (if TanStack Intent has a
# table/display skill) or no `extends` at all (if no Intent skill cleanly covers chart
# accessibility and display conventions). Cannot resolve until Session 1 runs
# `npx @tanstack/intent list` and the available skill names are in hand.
# Wrong extends = agent loads Query data-fetching context when this file is activated,
# which contradicts this file's display-only scope. Fix in Session 1 before deploying Intent.
# See: engineering-handoff/NEXT-SESSION-tanstack-week2.md → New Thinking.
load_order: after_base
domain_scope: "financial data display — AmountCell formatting, allocation charts, net worth computation patterns, positive/negative value encoding"
conflict_resolution: "This reference takes precedence over the base TanStack Query skill for HeyHi financial UI builds. On any conflict, apply the guidance here."
---

# Financial UI Patterns

Reference for financial data display. Covers currency formatting, positive/negative value encoding, KPI cards with live regions, accessible charts (three-layer pattern, WCAG 1.4.1 color-blind encoding), and dashboard composition.

**Scope:** Dual — applies to both a specific financial-product client engagement and general HeyHi client work involving financial data display.

**Soft dependency on `data-table-patterns.md`:** The summary rows and table-specific sections below reference TanStack Table patterns. Load `data-table-patterns.md` alongside this file for builds that combine financial display with sortable/filterable data tables.

**Currency formatting and KPI card patterns are independent of `data-table-patterns.md`** — load this file alone for dashboard-only or chart-only builds.

---

## Currency Formatting

```typescript
// Use Intl.NumberFormat — never format currency with string manipulation
const formatCurrency = (value: number, currency = 'USD', locale = 'en-US') =>
  new Intl.NumberFormat(locale, {
    style: 'currency',
    currency,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(value);

// Compact display (dashboard cards) — outputs "1.3M" (no currency symbol)
const formatCompact = (value: number) =>
  new Intl.NumberFormat('en-US', {
    notation: 'compact',
    maximumFractionDigits: 1,
  }).format(value);
// 1250000 → "1.3M"

// Compact WITH currency symbol — requires a two-step approach
// Intl.NumberFormat does not combine 'compact' with 'currency' style in one call
const formatCompactCurrency = (value: number, currency = 'USD', locale = 'en-US') => {
  const symbol = new Intl.NumberFormat(locale, {
    style: 'currency',
    currency,
    maximumFractionDigits: 0,
  }).formatToParts(0).find(p => p.type === 'currency')?.value ?? '$';

  const compact = new Intl.NumberFormat(locale, {
    notation: 'compact',
    maximumFractionDigits: 1,
  }).format(value);

  return `${symbol}${compact}`;
};
// formatCompactCurrency(1250000) → "$1.3M"
// formatCompactCurrency(750000, 'EUR', 'de-DE') → "€750K"
```

**Why the two-step approach for compact currency:** `Intl.NumberFormat` does not support `notation: 'compact'` combined with `style: 'currency'` in a single formatter. The pattern above extracts the currency symbol via `formatToParts`, then applies compact notation separately.

---

## Positive/Negative Value Display

Color alone is insufficient for accessibility (WCAG 1.4.1). Always supplement color with semantic text.

```typescript
function AmountCell({ value }: { value: number }) {
  const isPositive = value >= 0;
  return (
    <span
      style={{ color: isPositive ? 'var(--color-positive)' : 'var(--color-negative)' }}
    >
      {/* Screen readers announce: "Gain: $1,234.00" or "Loss: $1,234.00" */}
      <span className="sr-only">
        {isPositive ? 'Gain' : 'Loss'}: {formatCurrency(Math.abs(value))}
      </span>
      {/* Visual display — hidden from screen readers */}
      <span aria-hidden="true">
        {isPositive ? '+' : ''}{formatCurrency(value)}
      </span>
    </span>
  );
}
```

The `.sr-only` class: `position: absolute; width: 1px; height: 1px; padding: 0; overflow: hidden; clip: rect(0, 0, 0, 0); white-space: nowrap; border: 0;`

---

## KPI Card Pattern — With Live Region

```jsx
function KpiCard({ label, value, change, isLoading }) {
  if (isLoading) return <div className="skeleton card" aria-hidden="true" />;
  const isPositive = change >= 0;
  return (
    <article className="card kpi-card">
      <p className="kpi-label">{label}</p>

      {/*
        aria-live="polite": announces updates when the user is idle — does not interrupt.
        aria-atomic="true": announces the complete value, not just the changed digits.
        Both together are required for financial values — partial announcements
        ("3" without currency context) are confusing and inaccessible.
      */}
      <p className="kpi-value" aria-live="polite" aria-atomic="true">
        {formatCurrency(value)}
      </p>

      <p
        className={`kpi-change ${isPositive ? 'positive' : 'negative'}`}
        aria-live="polite"
        aria-atomic="true"
      >
        {/*
          Arrow glyph hidden from screen readers.
          sr-only span provides the directional word.
          aria-label on <p> has inconsistent behavior across NVDA, VoiceOver, and JAWS —
          the aria-hidden + sr-only pattern is more robust across AT.
        */}
        <span aria-hidden="true">{isPositive ? '↑' : '↓'} </span>
        <span className="sr-only">{isPositive ? 'Up' : 'Down'} </span>
        {Math.abs(change).toFixed(1)}% from last period
      </p>
    </article>
  );
}
```

---

## Financial Table Conventions

**Date range selectors:** Conventional patterns for financial data: Last 30 days / 90 days / 12 months / YTD / Custom. Period-start / period-end approach, not individual date pickers. Avoid calendar grids unless custom date ranges are a primary user need.

**Summary rows:** Totals should be visually separated (border-top, background shift, or weight change) and exempt from sorting logic. In TanStack Table, use `getFooterGroups()` for total rows — do not put them in the body where they could be sorted or filtered.

**Empty states:** Be specific about why there's no data. "No transactions in this period" is more useful than "No results." Offer the next logical action: "Adjust the date range" or "Add your first account."

---

## Accessible Charts — Three-Layer Pattern

SVG charts are invisible to screen readers without explicit markup. This is a WCAG 2.1 AA failure (1.1.1 Non-text Content). Use the three-layer pattern:

```jsx
function AccessibleNetWorthChart({ data, title }) {
  return (
    <figure aria-labelledby="chart-title" aria-describedby="chart-desc">
      <figcaption>
        <h3 id="chart-title">{title}</h3>
        <p id="chart-desc">
          Net worth from {data[0].date} to {data[data.length - 1].date}.{' '}
          {getTrendDescription(data)}
        </p>
      </figcaption>

      {/* Layer 1: Visual chart — hidden from screen readers */}
      <div aria-hidden="true">
        <ResponsiveContainer width="100%" height={300}>
          {/* chart config */}
        </ResponsiveContainer>
      </div>

      {/* Layer 2: Data table — visually hidden, accessible to screen readers */}
      <table className="sr-only">
        <caption>Net worth by month</caption>
        <thead>
          <tr><th scope="col">Date</th><th scope="col">Net Worth</th></tr>
        </thead>
        <tbody>
          {data.map(row => (
            <tr key={row.date}>
              <td>{row.date}</td>
              <td>{formatCurrency(row.netWorth)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </figure>
  );
}

// Layer 3: Prose trend description (required — appears in figcaption above)
function getTrendDescription(data) {
  const change = data[data.length - 1].netWorth - data[0].netWorth;
  const pct = ((change / Math.abs(data[0].netWorth)) * 100).toFixed(1);
  return `Overall ${change >= 0 ? 'increase' : 'decrease'} of ${formatCurrency(Math.abs(change))} (${pct}%).`;
}
```

The three layers: (1) `aria-hidden` visual chart, (2) `.sr-only` data table with actual values, (3) prose trend description in `figcaption`. All three are required — visual chart without prose context and data table is a WCAG 2.1 AA failure.

---

## Color-Blind Accessible Charts — WCAG 1.4.1

Color alone to differentiate data series is a WCAG 1.4.1 failure. Supplement with a secondary visual encoding.

```jsx
import { LineChart, Line } from 'recharts';

// Multi-series — distinguishable without color
<LineChart data={data}>
  {/* Primary series — solid line */}
  <Line
    type="monotone"
    dataKey="savings"
    stroke="var(--color-primary)"
    strokeWidth={2}
    strokeDasharray="0"
    dot={{ r: 4 }}
    isAnimationActive={false}  // Required for live-updating data
  />
  {/* Secondary series — dashed */}
  <Line
    type="monotone"
    dataKey="investments"
    stroke="var(--color-secondary)"
    strokeWidth={2}
    strokeDasharray="6 3"
    dot={{ r: 4, strokeDasharray: '0' }}
    isAnimationActive={false}
  />
  {/* Tertiary series — dotted */}
  <Line
    type="monotone"
    dataKey="withdrawals"
    stroke="var(--color-tertiary)"
    strokeWidth={2}
    strokeDasharray="2 2"
    isAnimationActive={false}
  />
</LineChart>
```

Three supplementary encoding strategies:
1. **Stroke patterns** — solid / dashed / dotted. Works in monochrome print and for all common color vision deficiencies.
2. **Marker shapes** — circle, square, diamond, triangle at data points.
3. **Direct labels** — annotate series at end-of-line rather than relying on a color-coded legend alone.

For bar charts, pattern fills (hatching, crosshatch, diagonal) serve the same purpose.

**Design system integration:** Map chart colors to design tokens via props — `stroke="var(--color-accent)"`. Recharts does not consume CSS variables automatically; token values must be passed as props, not set in CSS.

**`isAnimationActive={false}`:** Required when data updates frequently (live dashboards, polling). Without it, Recharts re-runs the entrance animation on every data refresh — visually jarring and CPU-wasteful.

---

## Library Selection

| Use case | Library |
|----------|---------|
| Standard business charts (bar, line, area, pie) | Recharts |
| Financial time series, candlestick, OHLC | React-Financial-Charts |
| shadcn/ui projects | shadcn charts (Recharts wrapper) |
| Complex custom charts | Observable Plot + D3 |
| Real-time / live-updating | Recharts with `isAnimationActive={false}` |
| Dashboard with mixed chart types | Tremor |

---

## Dashboard Composition

**Bento grid for dashboard cards:**

```css
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  grid-auto-rows: minmax(80px, auto);
  gap: var(--space-4);
}

.card-full       { grid-column: span 12; }
.card-half       { grid-column: span 6; }
.card-third      { grid-column: span 4; }
.card-two-thirds { grid-column: span 8; }

@media (max-width: 768px) {
  .card-full, .card-half, .card-third, .card-two-thirds {
    grid-column: span 12;
  }
}
```

**Skeleton loading matching the final layout:**

```jsx
function DashboardSkeleton() {
  return (
    <div className="dashboard-grid">
      <div className="card card-half skeleton" style={{ height: '200px' }} aria-hidden="true" />
      <div className="card card-half skeleton" style={{ height: '200px' }} aria-hidden="true" />
      <div className="card card-full skeleton" style={{ height: '300px' }} aria-hidden="true" />
    </div>
  );
}
```

```css
.skeleton {
  background: linear-gradient(
    90deg,
    var(--color-surface-muted) 25%,
    var(--color-surface) 50%,
    var(--color-surface-muted) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0%   { background-position: -200% 0; }
  100% { background-position:  200% 0; }
}

@media (prefers-reduced-motion: reduce) {
  .skeleton { animation: none; }
}
```

Skeleton shapes must match the loaded layout — mismatched skeletons cause layout shift. `aria-hidden="true"` on skeletons prevents screen readers from announcing meaningless placeholder content.

---

*HeyHi Internal Use Only. Zone 2 — task-conditional. Scope: client-engagement + heyhi-wide. Load when build requires financial data display, accessible charts, or dashboard composition. v1.0.0 created 2026-04-18 from frontend-research-reference.md v1.2.0.*
