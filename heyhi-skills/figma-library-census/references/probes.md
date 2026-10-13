---
classification: confidential
title: "figma-library-census: Plugin API probe log"
created: "2026-09-07"
---

# Probe log

Every Plugin API call this skill depends on was run against a real Figma file before the method built on it (Arc rule 9: probe, never trust). All probes ran on the worked-example scratch library (the instance's own 2026-09-04 generated library), **Figma plan tier Pro**, 2026-09-07. The file key is recorded only in the gitignored proof record; it is not written here.

Every probe is read-only. None adds, mutates, or deletes a node, variable, or style.

## Summary table

| API call | Surface | Observed result (scratch library, Pro tier) | Probe |
|---|---|---|---|
| `get_libraries({ fileKey })` | MCP tool | `libraries_added_to_file: []`; 8 community kits in `libraries_available_to_add`; `libraries_available_to_add_next_offset: null` | P-00 |
| `figma.teamLibrary.getAvailableLibraryVariableCollectionsAsync()` | `use_figma` | `[]` from the defining file (its own collections are local, `remote:false`; no library added) | P-01 |
| `figma.teamLibrary.getVariablesInLibraryCollectionAsync(key)` | `use_figma` | called with a local published collection key → `count 0`, no throw (a defining file's own collections do not return via the remote API) | P-02 |
| `figma.variables.getLocalVariableCollectionsAsync()` | `use_figma` | 4 collections: Primitives (1 mode `Value`, 69), Color (2 modes `Light`/`Dark`, 35), Spacing (1 mode, 27), Typography (1 mode, 26); each has `.key` | P-01 |
| `figma.variables.getLocalVariablesAsync()` | `use_figma` | 157 variables; each has `name`, `key`, `resolvedType`, `codeSyntax.WEB`, `scopes`, `remote:false` | P-01 |
| `figma.getLocalTextStylesAsync` / `getLocalEffectStylesAsync` / `getLocalPaintStylesAsync` | `use_figma` | 12 text, 6 effect, 0 paint; each has `name`, `key` | P-01 |
| `page.findAllWithCriteria({ types: ['COMPONENT_SET','COMPONENT'] })` | `use_figma` | Button page → 1 set (`Button`) + its 27 variant children; Utilities → 1 standalone `Icon/ChevronRight` | P-02, P-03 |
| `componentSet.componentPropertyDefinitions` (owner) | `use_figma` | Button set → 6 props: Label (TEXT), Show Icon (BOOLEAN), Icon (INSTANCE_SWAP), Style/Size/State (VARIANT with options); read on the SET, not a variant | P-02 |
| `componentSet.defaultVariant` | `use_figma` | Button → `Style=primary, Size=sm, State=default` | P-02 |
| `pageNode.loadAsync()` | `use_figma` | loads one page's subtree without switching the current page; the ADOPTED per-page mechanism for step 3 (read-only, parallel-safe across pages) | P-03 |

## P-00 · library availability, `get_libraries` (MCP tool)

`get_libraries({ fileKey })` on the scratch library returned `libraries_added_to_file: []` and eight community UI kits under `libraries_available_to_add` (Material 3, Simple Design System, iOS/macOS/watchOS/visionOS kits), with `libraries_available_to_add_next_offset: null` (no org libraries; a single page). Interpretation: the scratch library is a standalone defining file with no libraries added, which is why the remote variable path (P-01) returns empty from it. For a real client census, the CONSUMING app file's `get_libraries` names the added library and its `libraryKey`, which becomes `library_key` in the maps; page with `libraries_available_to_add_next_offset` when it is non-null.

## P-01 · variable + style census (defining-file read)

Script: `scripts/census-step2-variables-styles.js`. Observed: 4 local collections with the mode names and variable counts in the summary table; 157 variables, every one `remote:false` with a WEB `codeSyntax` set (`var(--...)`) and explicit `scopes` (Primitives carry `[]` = hidden; Color `text/*` carry `TEXT_FILL`; Spacing `space/*` carry `GAP`, `radius/*` carry `CORNER_RADIUS`; Typography carries `FONT_FAMILY` / `FONT_SIZE`). `teamLibrary.getAvailableLibraryVariableCollectionsAsync()` returned `[]`. **This is the load-bearing observation:** a defining file sees its own collections as local, not through `teamLibrary`; the remote path needs a consuming file. Modes and code syntax are therefore always read through the local path in the defining file (consistent with the Ground-truth correction that `getVariablesInLibraryCollectionAsync` returns only name/key/resolvedType).

## P-02 · component census + the remote-variable API shape

Script: `scripts/census-step3-components.js` (Button page). Observed: `findAllWithCriteria` returned the `Button` COMPONENT_SET plus its 27 variant children; filtering to rows (set or standalone) left one row. `componentPropertyDefinitions` read on the SET returned the 6 properties; reading it on a variant COMPONENT throws (owner-narrowing is mandatory). `defaultVariant.name` returned the default combination. This probe reached the Button page with `setCurrentPageAsync`; the shipped script adopts `page.loadAsync()` instead (proven in P-03): read-only (no current-page switch) and parallel-safe, reaching the same `findAllWithCriteria` result. In the same probe, `getVariablesInLibraryCollectionAsync(<Primitives local key>)` returned `count 0` with no throw, the definitive confirmation that a defining file's own collections do not surface through the remote API.

## P-03 · page discovery + remaining-page census

Script: `scripts/census-step1-pages.js` (page list) then a `loadAsync`-per-page read of the other content pages. Observed: 7 pages (Cover, Getting Started, Foundations, `---`, Button, `---`, Utilities). Cover / Getting Started / Foundations carry no components (documentation frames); Utilities carries the standalone `Icon/ChevronRight` COMPONENT (`figma-only` in the crosswalk). `get_metadata` (no nodeId) reported only the first page ("Cover"); the `use_figma` page read is authoritative and returned all seven, do not trust `get_metadata`'s page list for a census.

## What is NOT yet probed (carried to the handoff)

- The remote variable path end to end (`getAvailableLibraryVariableCollectionsAsync` → `getVariablesInLibraryCollectionAsync` returning a non-empty collection) needs a file with the library added. The worked example's read-only scope adds nothing, so this path is confirmed by the served Figma reference and by the empty/`count 0` observations, not by a populated run. The first real client census (from a consuming app file) exercises it; record the populated result then.
- `SLOT`-typed component properties: the scratch Button has none. The property-type enum includes `SLOT` (Card-like components use it); the census reads it the same way (`componentPropertyDefinitions` on the owner), but a populated `SLOT` observation waits for a library that has one.

*HeyHi Confidential.*
