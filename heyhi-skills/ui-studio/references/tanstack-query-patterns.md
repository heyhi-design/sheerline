---
name: tanstack-query-patterns
zone: 2
load_trigger: Build requires server-side pagination on a TanStack Table, debounced filter input wired to a server fetch, or optimistic mutations on row-level edits or deletions
token_estimate: ~800
classification: HeyHi Internal Use Only
created: 2026-04-20
version: "1.0.0"
scope:
  - client-engagement
  - heyhi-wide
dependencies:
  - heyhi-skills/ui-studio/references/data-table-patterns.md
# Agent context layering — declared at creation (synthesis session 2026-04-20)
# This reference extends TanStack's base Query skill with HeyHi domain depth.
# The TanStack Intent skill provides correct API guidance. This file provides
# the integration patterns between Query and Table that only emerge in production
# financial UIs — patterns TanStack's skill has no mandate to document.
extends: "@tanstack/intent/tanstack-query"
# VERIFY: confirm this extends value against `npx @tanstack/intent list` in Session 1 of
# tanstack-intent-execution-plan.md. The format here follows the synthesis spec but has not
# been validated against the live Intent registry. An incorrect extends value causes an agent
# to load the wrong base skill — set it right before deploying TanStack Intent.
load_order: after_base
domain_scope: "TanStack Query × Table integration — server-side pagination, debounced filter → Query key, optimistic mutations for row edits and deletions"
conflict_resolution: "This reference takes precedence over the base TanStack Query skill for HeyHi builds. On any conflict, apply the guidance here."
---

# TanStack Query Patterns

Reference for TanStack Query v5 integration with TanStack Table. Covers the three patterns that emerge specifically when tables need server-side data: pagination without blank transitions, debounced filter input wired to server fetches, and optimistic mutations for row-level edits and deletions.

**When to load this file:** Load alongside `data-table-patterns.md` whenever a table requires server-side pagination, column filter inputs that trigger fetches, or row edits that must update both the UI and the server.

**This file is not needed for:** client-side tables (sort/filter/page on data already in memory), static data displays, or chart-only financial UIs.

**Prerequisite:** Load `data-table-patterns.md` first. This file assumes you know how TanStack Table's column definition, `manualPagination`, and `manualFiltering` flags work.

**v5 API note — breaking changes from v4:** TanStack Query v5 (succeeds React Query; the rename is the same library with breaking API changes) changed how `keepPreviousData` works. The v4 option `keepPreviousData: true` as a top-level `useQuery` option no longer exists in v5. See Pattern 1 below for the correct v5 API.

---

## Pattern 1 — Server-Side Pagination Without Blank Transitions

### The problem

When a table is server-paginated and the user clicks to the next page, TanStack Query fires a new fetch. During that fetch, the previous page's data is gone — the table goes blank. For financial data tables (portfolio lists, account ledgers), a momentary blank state reads as data loss and damages trust.

### The solution: `placeholderData: keepPreviousData`

TanStack Query v5 ships `keepPreviousData` as a named function import. Pass it as the value of `placeholderData`:

```typescript
import { useQuery, keepPreviousData } from '@tanstack/react-query'

function usePortfolioTable(page: number, pageSize: number) {
  return useQuery({
    queryKey: ['portfolio', 'table', page, pageSize],
    queryFn: () => fetchPortfolioPage({ page, pageSize }),
    placeholderData: keepPreviousData,   // v5: function reference, not boolean
    staleTime: 30_000,                   // 30 seconds — tuned for financial data volatility
  })
}
```

**Critical v5 distinction:** `keepPreviousData` must be imported from `@tanstack/react-query` and passed as a function reference (not called — no parentheses). Passing `placeholderData: true` or the old `keepPreviousData: true` top-level option will silently fail — no error, no placeholder, just a blank table on page transitions.

### Wiring to TanStack Table

```typescript
const [pagination, setPagination] = useState({ pageIndex: 0, pageSize: 25 })

const { data, isFetching, isPlaceholderData } = usePortfolioTable(
  pagination.pageIndex,
  pagination.pageSize,
)

const table = useReactTable({
  data: data?.rows ?? [],
  columns,
  rowCount: data?.totalCount ?? 0,
  state: { pagination },
  onPaginationChange: setPagination,
  manualPagination: true,
  getCoreRowModel: getCoreRowModel(),
  getPaginationRowModel: getPaginationRowModel(),
})
```

**UX note on `isPlaceholderData`:** While `keepPreviousData` keeps the previous page visible, expose `isPlaceholderData` to the UI — a subtle loading indicator (spinner in the pagination controls, reduced table opacity) tells the user data is refreshing without wiping the display. Hiding the fetch entirely reads as the page not responding.

**Query key design:** The `queryKey` array must include all variables that uniquely identify the requested data. For pagination: `['portfolio', 'table', page, pageSize]`. For filtered pagination: add the active filter values. If the query key doesn't change when the page changes, Query returns cached data instead of fetching the new page.

---

## Pattern 2 — Debounced Filter Input → Server Fetch

### The problem

A column filter input fires a keystroke event on every character. If each keystroke triggers a server fetch, a 10-character filter entry fires 10 requests — most wasted, all competing. The last one to resolve wins, which may not be the response the user sees.

### The three-state model

Three distinct state values govern this pattern. Confusing them is where implementation debt accumulates:

1. **`inputValue`** — local React state bound directly to the input element. Updates on every keystroke. This is what the user sees as they type.

2. **`debouncedValue`** — derived from `inputValue` via a debounce hook. Updates only after the user pauses typing (300–500ms delay). This is what triggers the server fetch.

3. **`columnFilters`** — TanStack Table's filter state (set via `setColumnFilters`, used with `manualFiltering: true`). Updated to reflect `debouncedValue` so the table header renders the active filter indicator correctly.

The causal chain:
```
user types → inputValue changes → debouncedValue changes (after delay)
  → Query key changes → server fetch fires → table data updates
  → columnFilters updated → table header shows active filter indicator
```

`columnFilters` does not trigger the fetch. `debouncedValue` in the Query key triggers the fetch. `columnFilters` tells the table which columns have active filters — it is a rendering concern, not a data fetching concern.

### Implementation

```typescript
// useDebounce is not a built-in React hook.
// Use usehooks-ts: npm install usehooks-ts
// Or implement: const useDebounce = (value, delay) => { ... }
import { useDebounce } from 'usehooks-ts'

function AccountTable() {
  // State 1: what the input shows
  const [inputValue, setInputValue] = useState('')

  // State 2: what triggers the fetch (debounced)
  const debouncedValue = useDebounce(inputValue, 350)

  // State 3: what the table reads for its filter indicator
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([])

  // Sync debouncedValue into columnFilters for table header rendering
  useEffect(() => {
    setColumnFilters(
      debouncedValue ? [{ id: 'accountName', value: debouncedValue }] : []
    )
  }, [debouncedValue])

  // debouncedValue in the query key: fetch fires when user pauses, not on every keystroke
  const { data } = useQuery({
    queryKey: ['accounts', 'filtered', debouncedValue],
    queryFn: () => fetchAccounts({ search: debouncedValue }),
    placeholderData: keepPreviousData,
    enabled: true, // always enabled; empty debouncedValue returns all records
  })

  const table = useReactTable({
    data: data?.accounts ?? [],
    columns,
    state: { columnFilters },
    onColumnFiltersChange: setColumnFilters,
    manualFiltering: true, // tells Table not to filter client-side
    getCoreRowModel: getCoreRowModel(),
  })

  return (
    <>
      <input
        value={inputValue}
        onChange={e => setInputValue(e.target.value)}
        placeholder="Search accounts..."
        aria-label="Filter accounts by name"
      />
      {/* table rendering */}
    </>
  )
}
```

**Common failure modes:**

- Putting `inputValue` in the Query key: fires a fetch on every keystroke. Defeats the debounce.
- Putting `columnFilters` in the Query key: `columnFilters` is a derived rendering value, not the fetch trigger. This works coincidentally (because `columnFilters` updates when `debouncedValue` updates via the `useEffect`) but obscures which state actually owns the fetch lifecycle — a maintenance hazard.
- Forgetting `manualFiltering: true`: TanStack Table will attempt to filter client-side against the full fetched dataset, producing incorrect results when the dataset is paginated server-side.

**Debounce delay:** 300–500ms for most cases. Financial data search can go to 500ms — users are searching by account name or ticker, not performing keystroke-by-keystroke autocomplete.

---

## Pattern 3 — Optimistic Mutations for Row-Level Edits

### The problem

When a user edits a row (updating an account balance, changing an asset quantity) and submits, a naive implementation shows a loading state while waiting for server confirmation. The table row goes blank or shows stale data post-mutation. For financial data, this reads as unreliable.

### The solution: `onMutate` → `onError` rollback

TanStack Query's `useMutation` provides three lifecycle callbacks that implement optimistic updates:

- `onMutate`: fires before the server call. Update the cache immediately with the expected new value. Save the previous value for rollback.
- `onError`: fires if the server call fails. Restore the previous value from the rollback snapshot.
- `onSettled`: fires after success or failure. Invalidate the query to trigger a refetch and confirm the server state.

```typescript
const queryClient = useQueryClient()

const updateAccountMutation = useMutation({
  mutationFn: (update: AccountUpdate) => patchAccount(update),

  onMutate: async (update) => {
    // Cancel any in-flight fetches that would overwrite the optimistic update
    await queryClient.cancelQueries({ queryKey: ['accounts'] })

    // Snapshot the current cache value for rollback
    const previousAccounts = queryClient.getQueryData<AccountsResponse>(['accounts'])

    // Apply the optimistic update to the cache immediately
    queryClient.setQueryData<AccountsResponse>(['accounts'], (old) => ({
      ...old!,
      accounts: old!.accounts.map(account =>
        account.id === update.id
          ? { ...account, ...update.fields }
          : account
      ),
    }))

    // Return the snapshot in the mutation context for rollback
    return { previousAccounts }
  },

  onError: (_error, _update, context) => {
    // Rollback to the snapshot on failure
    if (context?.previousAccounts) {
      queryClient.setQueryData(['accounts'], context.previousAccounts)
    }
    // Surface the error to the user — do not silently eat it
    // toast.error('Update failed. Your changes were not saved.')
  },

  onSettled: () => {
    // Refetch to confirm server state — optimistic value is unverified until this resolves
    queryClient.invalidateQueries({ queryKey: ['accounts'] })
  },
})
```

### Row deletion

The same pattern applies to deletions. Remove the row from the cache in `onMutate`, restore it in `onError`:

```typescript
const deleteAssetMutation = useMutation({
  mutationFn: (assetId: string) => deleteAsset(assetId),

  onMutate: async (assetId) => {
    await queryClient.cancelQueries({ queryKey: ['assets'] })
    const previousAssets = queryClient.getQueryData<AssetsResponse>(['assets'])
    queryClient.setQueryData<AssetsResponse>(['assets'], (old) => ({
      ...old!,
      assets: old!.assets.filter(asset => asset.id !== assetId),
    }))
    return { previousAssets }
  },

  onError: (_error, _assetId, context) => {
    if (context?.previousAssets) {
      queryClient.setQueryData(['assets'], context.previousAssets)
    }
  },

  onSettled: () => {
    queryClient.invalidateQueries({ queryKey: ['assets'] })
  },
})
```

### Financial data caution

For financial data specifically: the optimistic update shows users a value that has not yet been confirmed by the server. This is correct UX for most cases — the edit is almost always going to succeed. But surface the unconfirmed state clearly:

- Show a subtle "saving..." indicator on the row while the mutation is in-flight (check `mutation.isPending`).
- If the error rate for a mutation type is elevated (network issues, server validation failures), consider removing the optimistic update and using a loading state instead. Trust over speed is the right trade-off in financial contexts.
- Never optimistically update a computed value (net worth, portfolio total) that depends on the mutated row. Let `onSettled` + `invalidateQueries` update those — the computed refetch happens quickly, and showing a briefly stale computed value is less harmful than showing an incorrectly computed one.

---

## TanStack Form — Flagged Gap

**Not documented here. Flagged for Phase B backfill.**

A data-heavy product's workflows involve user entry of record attribute values, configuration edits, and account data updates. TanStack Form (v0.x — pre-1.0; API is not yet stable) handles field-level and form-level validation (sync and async) and integrates with TanStack Query's mutation primitives for the submit-to-server path.

This gap is lower priority than the three patterns above: forms can be handled near-term with react-hook-form or uncontrolled inputs. Promote to P1 when a ticket on the client's board specifically requires field-level async validation or tightly coupled form + mutation state.

**Build signal:** Any ticket involving multi-field financial data entry with server-side validation (e.g., "validate that account total doesn't exceed portfolio limit before saving"). Until then, keep it on the queue and do not build it.

---

## Load Guidance

| Pattern | Load alongside | Notes |
|---------|---------------|-------|
| Server-side pagination | `data-table-patterns.md` | Required — needs Table's `manualPagination` setup |
| Debounced filter | `data-table-patterns.md` | Required — needs Table's `manualFiltering` and `columnFilters` state |
| Optimistic mutations | `data-table-patterns.md` | Recommended — row mutations affect table data; keep them in the same context |
| All three | `data-table-patterns.md` + `financial-ui-patterns.md` | Full financial table build — load all three |

---

*HeyHi Internal Use Only. Created 2026-04-20 from Frontend × TanStack synthesis.*
*Phase B frontend backfill — promoted to P1 for a client engagement (server-side pagination + row mutations both in scope).*
