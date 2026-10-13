---
name: data-table-patterns
zone: 2
load_trigger: Build requires sortable/filterable data tables, virtual scrolling for large datasets, or TanStack Table/Virtual integration
token_estimate: ~900
classification: HeyHi Internal Use Only
created: 2026-04-18
version: "1.1.0"
# Agent context layering — added 2026-04-20 (synthesis session)
# This reference extends TanStack's base Table skill with HeyHi domain depth.
# The TanStack Intent skill provides correct API guidance. This file provides
# the financial-context decisions, accessibility requirements, and token integration
# patterns that TanStack's skill has no mandate to document.
extends: "@tanstack/intent/tanstack-table"
# VERIFY: confirm this extends value against `npx @tanstack/intent list` in Session 1 of
# tanstack-intent-execution-plan.md. The format here follows the synthesis spec but has not
# been validated against the live Intent registry. An incorrect extends value causes an agent
# to load the wrong base skill — set it right before deploying TanStack Intent.
load_order: after_base
domain_scope: "financial UI — accessibility requirements (aria-sort, div[role=grid] virtual table semantics), token integration, column formatting conventions"
conflict_resolution: "This reference takes precedence over the base TanStack Table skill for HeyHi builds. On any conflict, apply the guidance here."
---

# Data Table Patterns

Reference for data-heavy table work using TanStack Table and TanStack Virtual. Load when a build requires sorting, filtering, pagination, or virtual scrolling of tabular data.

The companion file `financial-ui-patterns.md` covers financial display conventions, KPI cards, accessible charts, and dashboard composition — load that alongside this file for financial UI builds.

---

## Where the Field Is

The field has consolidated around:
- **TanStack Table** for headless table logic (sorting, filtering, pagination, virtualization)
- **TanStack Virtual** for virtual scrolling of any list or table
- **display: grid on `<table>`** as the correct semantic pattern for virtualized data tables

Data-heavy UI is where design systems show their cracks. Tokens and component libraries cover atomic elements well — tables, charts, and financial displays are where system gaps emerge.

---

## TanStack Table — Core Pattern

Headless table logic for React. You write all the markup; TanStack handles sorting, filtering, column visibility, pagination, grouping, and selection.

```typescript
import {
  useReactTable,
  getCoreRowModel,
  getSortedRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  flexRender,
  type ColumnDef,
  type SortingState,
  type ColumnFiltersState,
} from '@tanstack/react-table';

interface Transaction {
  id: string;
  date: string;
  description: string;
  amount: number;
  category: string;
}

const columns: ColumnDef<Transaction>[] = [
  {
    accessorKey: 'date',
    header: 'Date',
    cell: ({ getValue }) => formatDate(getValue<string>()),
  },
  {
    accessorKey: 'amount',
    header: ({ column }) => (
      <button onClick={() => column.toggleSorting()}>
        Amount {column.getIsSorted() === 'asc' ? '↑' : '↓'}
      </button>
    ),
    cell: ({ getValue }) => formatCurrency(getValue<number>()),
    // Do NOT specify sortingFn for numeric/monetary columns.
    // TanStack Table's default sort is numeric comparison — correct for amounts.
    // sortingFn: 'alphanumeric' treats values as strings: "9" sorts after "10" alphabetically
    // but before it numerically. Never use alphanumeric for monetary columns.
  },
];

function TransactionTable({ data }: { data: Transaction[] }) {
  const [sorting, setSorting] = useState<SortingState>([]);
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([]);

  const table = useReactTable({
    data,
    columns,
    state: { sorting, columnFilters },
    onSortingChange: setSorting,
    onColumnFiltersChange: setColumnFilters,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),  // Required when columnFilters state is used
    getPaginationRowModel: getPaginationRowModel(),
  });

  return (
    <table>
      <thead>
        {table.getHeaderGroups().map(headerGroup => (
          <tr key={headerGroup.id}>
            {headerGroup.headers.map(header => (
              <th
                key={header.id}
                aria-sort={
                  !header.column.getCanSort()
                    ? undefined
                    : header.column.getIsSorted() === 'asc'
                    ? 'ascending'
                    : header.column.getIsSorted() === 'desc'
                    ? 'descending'
                    : 'none'
                }
              >
                {flexRender(header.column.columnDef.header, header.getContext())}
              </th>
            ))}
          </tr>
        ))}
      </thead>
      <tbody>
        {table.getRowModel().rows.map(row => (
          <tr key={row.id}>
            {row.getVisibleCells().map(cell => (
              <td key={cell.id}>
                {flexRender(cell.column.columnDef.cell, cell.getContext())}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

**Critical accessibility rule:** `aria-sort` belongs on `<th>`, not on the inner `<button>`. Sort indicator arrows inside the button must be `aria-hidden="true"` — `aria-sort` already conveys the state to assistive technology. Duplicating it in the button text creates double-announcement.

**Common mistake:** If `getFilteredRowModel` is imported but not passed to `useReactTable`, filters will not apply. The state and the model must both be present.

---

## Virtual Scrolling — TanStack Virtual

When a table or list has more than ~500 rows, DOM rendering becomes the bottleneck. TanStack Virtual renders only the visible rows.

### List Virtualization (Static Row Height)

```typescript
import { useVirtualizer } from '@tanstack/react-virtual';

function VirtualizedList({ rows }: { rows: Transaction[] }) {
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: rows.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 48,   // row height in px
    overscan: 5,              // rows to render beyond visible area — keep low
  });

  return (
    <div ref={parentRef} style={{ height: '600px', overflow: 'auto' }}>
      {/* Total height spacer preserves scroll position */}
      <div style={{ height: `${virtualizer.getTotalSize()}px`, position: 'relative' }}>
        {virtualizer.getVirtualItems().map(virtualItem => (
          <div
            key={virtualItem.key}
            style={{
              position: 'absolute',
              top: 0,
              transform: `translateY(${virtualItem.start}px)`,
              height: `${virtualItem.size}px`,
            }}
          >
            <ListRow row={rows[virtualItem.index]} />
          </div>
        ))}
      </div>
    </div>
  );
}
```

### Dynamic Row Heights

For rows with variable content (wrapped text, expandable sections, variable-length descriptions):

```typescript
const virtualizer = useVirtualizer({
  count: rows.length,
  getScrollElement: () => parentRef.current,
  estimateSize: () => 48,   // Initial estimate — corrected after measurement
  overscan: 5,
  measureElement: useCallback((element) => element?.getBoundingClientRect().height, []),
});

// Each item needs data-index and the measurement ref
{virtualizer.getVirtualItems().map(virtualItem => (
  <div
    key={virtualItem.key}
    data-index={virtualItem.index}      // Required for measureElement to work
    ref={virtualizer.measureElement}    // Triggers measurement on mount
    style={{ position: 'absolute', top: 0, transform: `translateY(${virtualItem.start}px)` }}
  >
    <ListRow row={rows[virtualItem.index]} />
  </div>
))}
```

### Virtualized Data Table (Table Semantics Preserved)

For tables that need both TanStack Table headless logic and virtual scrolling. The pattern uses `display: grid` on `<table>` to enable absolute positioning while preserving semantic table markup that screen readers require.

```typescript
function VirtualizedDataTable({ data, columns }) {
  const parentRef = useRef<HTMLDivElement>(null);
  const table = useReactTable({ data, columns, getCoreRowModel: getCoreRowModel() });
  const { rows } = table.getRowModel();

  const virtualizer = useVirtualizer({
    count: rows.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 48,
    overscan: 5,
  });

  return (
    <div ref={parentRef} style={{ height: '600px', overflow: 'auto' }}>
      <table style={{ display: 'grid' }}>
        {/* Sticky header */}
        <thead style={{ display: 'grid', position: 'sticky', top: 0, zIndex: 1 }}>
          {table.getHeaderGroups().map(headerGroup => (
            <tr key={headerGroup.id} style={{ display: 'flex', width: '100%' }}>
              {headerGroup.headers.map(header => (
                <th
                  key={header.id}
                  style={{ display: 'flex', width: header.getSize() }}
                  aria-sort={
                    !header.column.getCanSort() ? undefined :
                    header.column.getIsSorted() === 'asc' ? 'ascending' :
                    header.column.getIsSorted() === 'desc' ? 'descending' : 'none'
                  }
                >
                  {flexRender(header.column.columnDef.header, header.getContext())}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody
          style={{
            display: 'grid',
            height: `${virtualizer.getTotalSize()}px`,
            position: 'relative',
          }}
        >
          {virtualizer.getVirtualItems().map(virtualItem => {
            const row = rows[virtualItem.index];
            return (
              <tr
                key={row.id}
                style={{
                  display: 'flex',
                  position: 'absolute',
                  transform: `translateY(${virtualItem.start}px)`,
                  width: '100%',
                }}
              >
                {row.getVisibleCells().map(cell => (
                  <td key={cell.id} style={{ display: 'flex', width: cell.column.getSize() }}>
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </td>
                ))}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
```

`display: grid` on `<table>` transfers layout control to CSS while preserving the semantic table structure that screen readers expect. This is the correct stack for financial grids with 10,000+ rows.

**Why not a div-based grid?** Div-based rendering (common in other virtual scroll patterns) loses table semantics — screen reader users cannot navigate by row or column. For data tables, always preserve `<table>`, `<thead>`, `<tbody>`, `<th>`, `<td>` markup.

---

## Common Defects to Avoid

| Mistake | Correct behavior |
|---------|-----------------|
| `sortingFn: 'alphanumeric'` on amount/price columns | Omit `sortingFn` — default is numeric comparison |
| `aria-sort` on inner `<button>` instead of `<th>` | `aria-sort` goes on `<th>` |
| Sort indicator text in button without `aria-hidden` | Wrap `↑`/`↓` glyphs in `aria-hidden="true"` |
| `getFilteredRowModel` imported but not wired into `useReactTable` | Pass it in the config and add `onColumnFiltersChange` |
| Div-based virtualizer for semantic data tables | Use `display: grid` on `<table>` pattern |

---

*HeyHi Internal Use Only. Zone 2 — task-conditional. Load when build requires sortable/filterable data tables or virtual scrolling for large datasets. v1.0.0 created 2026-04-18 from frontend-research-reference.md v1.2.0.*
