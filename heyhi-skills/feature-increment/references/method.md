---
classification: confidential
title: "feature-increment: method spine"
---

# feature-increment: the method

The method for landing one feature in three targets from one contract. The SKILL.md carries the steps and the gates; this reference carries the rules each step follows, the exact call order for the three legs, and the seam discipline between them. Read it before running the increment. It restates nothing from `app-to-figma`, `ui-studio`, or `intent-journey-map`; it names where each is consumed.

## The one-contract principle

Every target reads the same served contract. The contract is the feature's `intent-journey-map` output: a 14-column prop-contract where each data prop is bound by JSON pointer to the application's OpenAPI, plus the feature's states and the components that render them. The three legs never re-derive the contract; they consume it. This is what makes the coverage table meaningful: a row is one contract element, and the table asks whether that same element is present in Figma, in the prototype, and in code. A leg that invents a prop the contract does not carry, or fills a value the contract flags unbindable, breaks the join and is a defect, not a convenience.

The contract is retrieved, never pasted (Sheerline area-7 Invariant 4): `retrieve_application_context(scope: ijm)` for the contract, `scope: manifest` for the surfaces and components, `scope: ds-map` for the crosswalk, `scope: intent` for the constraints. Until the upstream IJM lands, a hand-written contract in the same shape is the substitute, and that is how the instance's own proof run ran.

## Step 2, the delta plan: the rules

The delta plan is one row per contract element (a prop, a state, a component). Per row:

- **Surface**: the manifest surface `id` the element lands on. An existing surface is updated; a NEW surface is named as NEW and its recon is a prerequisite (call `app-recon` if the surface is not in the manifest).
- **State**: read from the feature's `interaction-inventory` sidecar (`inventory-schema.json`), or the human's list in that shape. The skill does not enumerate the states; area 4 does. A state marked MISSING in the sidecar is carried as a row, so the increment does not silently skip it.
- **Component + resolution**: the component that renders the state, resolved against the ds-map. `library` (the design-system package has it, per a `both` or `code-only` row), `local pattern` (a `figma-only` or absent row, a composition the package lacks), or `NEW` (no row at all). The resolution decides which leg does what: `library` imports/instances; `local pattern` builds once and ledgers; `NEW` prompts the one-off-vs-pattern question.
- **Endpoint**: the endpoint the state binds to, grounded through the contract's JSON pointer. `none` for a client-only state. A contract row whose pointer does not resolve in the served OpenAPI is flagged (never invented), the same discipline `intent-journey-map` applies at bind time.
- **Copy slot**: the UX-writing slot the state needs, from `microcopy-states-writer`'s sidecar (`microcopy-schema.json`), left as a named slot. The string is not written here; area 3 writes it against the confirmed voice.

**The one-off-vs-pattern question** is named per NEW element and left empty. The skill computes and states the promotion signal as a fact (the ds-map recurrence count against the plan § 5 D4 defaults: three surfaces in one application, or two applications, or a second feature's IJM naming it). Stating the count is mechanical; ruling the element a pattern is the human's. The delta plan prints, and Step 3 does not begin until it is approved.

## Step 3, the Figma leg: consuming app-to-figma update mode

The Figma leg is `app-to-figma` Step 7 (update mode), consumed as a promoted skill. The call order is `app-to-figma`'s, not restated here. The join this skill owns:

1. Resolve each delta-plan row's component to its published key through the served `figma-library-map.json` (a `library` row) or to a local pattern (a `local pattern` row).
2. `get_metadata` the artifact's frame for the feature's surface; find-or-update by the `app-to-figma` state ledger. A changed variant is a `swapComponent`; changed props are `setProperties`; a new section is appended.
3. A `local pattern` row builds the pattern once (only at the human's ruling) and emits a ledger row (SKILL.md Step 7) into the proof folder.
4. The theme mode is set once per surface on the wrapper (`app-to-figma` § Theme mode). Bound children resolve to the surface's mode.

The Figma leg edits only the target artifact file (the Wave 1 scratch file for the instance's own proof run), never a production Figma file, and never detaches an instance. Its verdict (is the increment right) is `app-to-figma`'s empty slot, inherited here. When the library is unpublished, import-by-key resolves nothing; the leg records an operator-gated finding (name the publish step for the human) rather than drawing a primitive or reporting an unexplained miss.

## Step 4, the prototype leg: the blocking conformance gate

The prototype leg is `ui-studio` Mode A (its Page Plan gate and Component Implementation Map), then the blocking conformance gate:

1. Build the feature's section as HTML/CSS through Mode A, grounded in the served system.
2. `validate_output(artifact: <emitted CSS/HTML>, artifact_type: "rendered_css")`.
3. Read the result. `valid: false` fails the step; read `errors[]`, fix the increment, re-validate. The leg does not pass until `valid: true`. Paste the `valid` field and any `errors` into the proof record.

This is the one blocking gate (plan D9). The Figma and repo legs propose; the prototype conformance gate blocks. The reason: the prototype is the readable render the human reviews, so a prototype that drifts from the served system is a false render and must be fixed before it is shown, whereas a Figma or code deviation is a proposal a human rules on.

## Step 5, the repo leg: propose-first

The repo leg scaffolds the feature typed from the contract, on a proof branch, never merged. The per-framework shape is in `repo-adapters.md`; the discipline is:

1. **Typed from the contract.** Every prop is a contract row (name, type, required, enum). An unbindable prop is scaffolded with a typed placeholder and a `// contract: unbound` marker.
2. **A story per variant**, when the repo has a story harness. When it does not, record the story as a named gap with a finding id; do not invent a harness.
3. **Import vs local pattern**, read from the ds-map: `both` / `code-only` imports from the package; `figma-only` / absent is a local pattern named from the ds-map with a ledger row.
4. **Route and hook stubs** typed to the endpoint's request/response pointer; no live fetch beyond the contract.
5. **Typecheck** with the repo's command. A failure is a finding on the increment, fixed toward the contract, never by loosening the repo's types.
6. **The conformance read** (informing, not blocking): `validate_output` on the increment's CSS, written into a reversible deviation record (`heyhi-drift-repair`'s shape), not a block.
7. **A propose-first PR**, never merged, on a branch of this monorepo touching only the frontend folder.

## Step 6, the coverage table: the reconciliation

One row per contract element, three target columns, one verdict column. Presence carries evidence; absence carries a finding id with a reason. The full column definitions and the miss rules are in `coverage-table.md`. The table is emitted every run, pass or miss; an unexplained miss (a blank target cell with no finding) fails the run. The read-out line must show `Unexplained misses: 0`.

## The seams (what this skill owns, what it delegates)

| Concern | Owner | This skill |
|---|---|---|
| Which interaction states exist | `interaction-inventory` (area 4) | reads the sidecar |
| The copy for each state | `microcopy-states-writer` (area 3) | reads the sidecar, names the slot |
| The feature's intent and prop contract | `intent-journey-map` | consumes it |
| The application manifest | `app-recon` | consumes it |
| The Figma build | `app-to-figma` (update mode) | orchestrates it |
| The prototype build | `ui-studio` Mode A | orchestrates it, gates it |
| The repo scaffold shape | `repo-adapters.md` | applies it |
| The deviation record | `heyhi-drift-repair` shape | reuses it |
| Whether the feature is right | the human | never rules it |

## Idempotency

The Figma leg re-reads the `app-to-figma` state ledger and updates by node ID. The repo leg is idempotent by branch (one proof branch, one PR). The coverage table is regenerated each run from the current three targets. A human-ruled deviation is never silently reverted on a re-run.

*HeyHi Confidential. `skill-updates/feature-increment/references/`. The method spine for the three-target increment. Engines: `app-to-figma` (update mode), `ui-studio` Mode A, `intent-journey-map`, `app-recon`, `validate_output`.*
