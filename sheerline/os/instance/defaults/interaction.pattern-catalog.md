---
title: "Cross-surface UX pattern catalog (the area-4 slot)"
status: unratified
ratified_by: null
version: "0.0.0"
effective_date: null
---

# Cross-surface UX pattern catalog

> **Slot `interaction.pattern-catalog`: the shape only.** No patterns ship. An instance fills this slot with the patterns it has harvested from its own surfaces, in the shape below, and ratifies the catalog in this file's frontmatter (who signed off, the version, the date). Until then the resolver reports `ratified: false` and readers treat every entry as a candidate.

A pattern catalog records the interaction patterns that recur across an instance's surfaces (a filter bar, an inline edit, a bulk-select table), so the next screen reuses a pattern instead of re-deriving it. It sits above the control-state contract: the contract says which states a control has; the catalog says how this product combines controls into a recurring job. Readers: `interaction-inventory` notes a matching element as a candidate, and `flow-and-lofi-author` may cite an entry in a skeleton. Neither rules that an element is an instance of a pattern; that call, and every open call below, is the owner's.

## Entry shape

Each entry is one `##` section with these fields, in this order:

| Field | What it holds |
|---|---|
| `id` | a stable kebab-case id, never reused |
| `name` | the pattern's plain name |
| `job` | the recurring job it does, in one sentence |
| `where` | the surfaces it appears on, each with a link (a frame, a route, a component story) |
| `anatomy` | the components it combines, by the design system's own names |
| `states` | the control-state contract states it relies on, and any it adds |
| `keyboard_and_focus` | the keyboard path and focus moves, citing the ARIA APG pattern where one applies |
| `copy_slots` | the strings it carries, as slot names (terms from the shared vocabulary slot, `content.shared-vocabulary`) |
| `accessibility_hooks` | the name, role and value each part needs |
| `variants` | the sanctioned variations, each with when to use it |
| `evidence` | the screens or sessions it was harvested from |
| `status` | `candidate` (harvested, not ruled) · `ratified` (the owner ruled it in) · `retired` |
| `since` | the catalog version that added or last changed it |
| `open_calls` | the questions only the owner can rule on, listed and left open. Empty until a call exists; never answered by a run |

## Versioning

Every change to an entry bumps the frontmatter `version` and sets that entry's `since`. A retired entry stays in the file with `status: retired`, so a link to it never breaks.

## Entries

None in the default.

