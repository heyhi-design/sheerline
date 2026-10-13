---
classification: confidential
title: "Intent-Journey Map, worked example (the instance's own site)"
skill: intent-journey-map
version: "0.1.0"
substrate: heyhi.design (the instance's own site; no client)
---

# Worked example, the Log browse-and-read flow (the instance's own site)

Run on the instance's own site (`heyhi-website/`), so no client content appears. The feature: a reader lands on the Log index, narrows it by category, and opens an entry. It is mapped from a hand-written manifest in the `app-manifest.json` shape (§ 3.3), because Lane C (`app-recon`) runs in parallel and its real manifest is not yet available. The point of the example is to calibrate register and depth, and to exercise the honest `no-spec` binding path: `heyhi-website` carries no OpenAPI, so every data prop binds to its typed data module by file and symbol, and the contract records that truthfully.

## Tier

**Tier 2**, because the flow spans multiple steps across two surfaces (`/log/` and `/log/$slug`) and carries a filter state. It writes no data and crosses no auth boundary, so the precedence rule does not force Tier 2; the multi-step, multi-surface shape earns it. A one-step "open one entry from a direct link" would be Tier 1. This borderline is recorded as an open decision below, per the method (the tier when the precedence rule does not decide it is the human's).

## Domain band in use

**Document-state band** (the Log is a content product). The load-bearing lane is the **visibility gate**: an entry is publicly visible only when its `published` flag is exactly `true`, so file existence never equals visibility. The band also carries the revision lane (a published slug is stable; changing it requires a redirect).

## The lane model

| Band | Step 1, Land on the Log index | Step 2, Filter by category | Step 3, Open an entry |
|---|---|---|---|
| **Intent** | *When I hear HeyHi has a writing log, I want to see what is there, so I can decide if it is worth my time.* Reader, desktop or mobile, `/log/`. | *When the list is long, I want to narrow it to a topic, so I can find the thread I care about.* | *When a title catches me, I want to read the piece, so I can get the actual argument.* |
| **Journey** | Stage: arrive. Action: scan the index of published entries. Friction: is the newest first? *(observation, severity is the human's)* | Stage: narrow. Action: pick a category chip. Friction: does an empty category read as "broken" or "nothing here yet"? *(observation)* | Stage: read. Action: open the entry, read to the end, find the Substack link. Opportunity: a clear next-read at the foot. *(observation)* |
| **Document-state** | Visibility gate: only `published: true` entries render. | Visibility gate unchanged; filter narrows the visible set, it does not change visibility. | Visibility gate: a non-published slug must 404, not render a draft. Revision: the slug is stable. |
| **System-and-data** | Source: the typed data module `src/data/logs.ts` (no backend endpoint; a static import). Frontstage. | Same source, filtered client-side by `LogMeta.category`. Frontstage. | Same module resolves the slug to a `LogEntryData`. Frontstage. Backstage: a redirect map in `vercel.json` for migrated slugs. |
| **UI-and-component** | `LogIndex` (container) rendering a list of `LogEntryCard` (presentational), state: filled / empty. | `CategoryFilter` (presentational), state: filled; the list re-renders to the narrowed set or its empty state. | `LogArticle` (container), state: filled / error (404). |
| **Acceptance** | Given published entries exist, When the reader opens `/log/`, Then the index shows them newest-first and hides every non-published entry. | Given a category is selected, When it matches no published entry, Then an explicit empty state renders (not a blank page, not an error). | Given a slug with `published: true`, When opened, Then the entry renders; Given a slug that is missing or not published, Then a 404 renders. |

*Component names above are illustrative role-names for the worked-example site; a real run resolves them through the per-system instance (`retrieve_design_context`), not from disk.*

## Prop-contract → the-log-browse-flow-ijm-contract.json

Every data prop binds to the typed module `src/data/logs.ts` and its `LogMeta` / `LogEntryData` interfaces. `heyhi-website` carries no OpenAPI, so every row is `binding_status: no-spec`, bound to the module by file and symbol. That is the truthful state, recorded rather than hidden. The paired machine file is `worked-example.ijm-contract.json` beside this reference; it validates against `schemas/ijm-contract.schema.json`.

Summary of the rows:

| Prop | Component | Role | Type | Source | Binding |
|---|---|---|---|---|---|
| `entries` | LogIndex (container) | data | `LogMeta[]` | `src/data/logs.ts` (static import) | no-spec |
| `categories` | CategoryFilter | data | `string[]` (derived from `LogMeta.category`) | `src/data/logs.ts` | no-spec |
| `entry` | LogArticle (container) | data | `LogEntryData` | `src/data/logs.ts` (slug lookup) | no-spec |
| `published` | LogArticle (container) | data | `boolean` | `src/data/logs.ts` (`LogMeta.published`) | no-spec |

## Opportunities and observed friction (observations, not rulings)

- Newest-first ordering on the index is assumed; whether readers expect it is unverified.
- An empty filtered category needs a distinct empty state so it does not read as broken.
- A visible next-read at the foot of an entry is an opportunity, not a decided feature.

*These are observations. Their severity, and whether each is real, are the human's (the theme-and-severity slot).*

## ⛔ Research question behind the feature, NEEDS HUMAN

Recorded framing from the brief: "help a first-time reader find and read the writing." The actual research question (is discovery the problem, or is it retention past the first entry?) is the human's to lock. Empty.

## ⛔ Theme and severity calls, NEEDS HUMAN

Which of the three observed frictions are real, and how much each matters. Empty.

## ⛔ Open decisions, NEEDS HUMAN (each carries a named owner)

- Tier for a single direct-link entry open (Tier 1 or Tier 2 by the multi-surface reading), owner: the mapping lead.
- Whether the empty-category state is in scope for this feature or a follow-on, owner: the product owner.

## Named gate

Contract review by the engineering owner: ____________________  Date: ______

No open decision is resolved, no severity is set, and no unverified observation is promoted to a real finding, by this map.

---

*HeyHi Confidential. `intent-journey-map` worked example v0.1.0, the instance's own site (heyhi.design). Hand-written manifest in the § 3.3 shape; the paired contract validates against `schemas/ijm-contract.schema.json`.*
