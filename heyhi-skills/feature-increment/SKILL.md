---
name: feature-increment
description: >-
  Add one feature to all three targets of a design system from a single bound
  contract: the Figma artifact, the living prototype, and the frontend repo,
  each kept in step with the others and with the application's real API. Given a
  feature's intent-journey map and its prop contract, the served application
  context, the artifact file key, the prototype root, and the frontend repo, it
  runs the mechanical work: a delta plan (surfaces, states, components, endpoints,
  copy slots); the Figma increment through the promoted app-to-figma in update
  mode; the prototype increment through ui-studio Mode A with the instance's
  validate_output (rendered_css) as a blocking gate; a propose-first repo
  increment on its own branch (component scaffolds typed from the contract, a
  story per variant, imports from the design-system package where the crosswalk
  says the component exists and a local pattern where it does not, route and hook
  stubs, a typecheck, a conformance read, a reversible deviation record); and a
  three-way contract coverage table that fails on any unexplained miss. Triggers:
  "add this feature to the artifact and the prototype and the repo", "feature
  increment", "build the new feature off the artifact", "increment this feature
  across all three targets". Leaves the judgment (which interactions matter and
  which copy ships, one-off versus pattern, the component match when inexact, the
  merge) as labeled empty slots behind a named human gate. NOT for building an
  HTML or code prototype from scratch (use ui-studio for client UI, heyhi-ui-ux
  for HeyHi pages, per CLAUDE.md ui-studio routing); NOT for auditing a built
  prototype's interaction completeness (use heyhi-prototype-audit, the audit this
  hands to); NOT for writing screens into Figma from the library as a standalone
  build (use app-to-figma, this skill's Figma leg); NOT for reading the
  application into a manifest (use app-recon); NOT for mapping a feature's intent
  and contract (use intent-journey-map, this skill's input).
version: "0.2.0"
updated: "2026-09-14"
status: "deployed 2026-09-08: heyhi-skills/feature-increment/ (promoted at convergence pass 2, DISPATCH-11). Built from plans/plan-sheerline-fdde-loop-2026-09-07.md (DISPATCH-07, Lane F, Wave 2). Sheerline area 12 (DesignOps), serves_areas hints 5 and 7; the loop's Care/increment verb. Consumes the promoted app-to-figma (Figma leg), ui-studio Mode A (prototype leg), intent-journey-map and app-recon (inputs), and the served retrieve_application_context and validate_output. Proof run on the instance's own site: one feature added to the heyhi.design Log-index artifact, prototype, and a propose-first PR on the site repo. Release tier: buildable-now-internal-first; D10 keeps this arc inside the D-3 hold (2026-10-09). v0.2.0 (2026-09-14): added the dependency-ripple fold to Step 6 (W7/G12; CLOSE-03 disposition, owner-approved promotion of the staged skill-updates step) and its references/dependency-ripple.md, loaded in Step 1."
review_by: "2026-09-21"
classification: confidential
---

# feature-increment

**Sheerline area 12 (DesignOps) · serves areas 5 and 7 · Care/increment verb · multi-target build skill.** A feature is decided and its contract is written. This skill lands that one feature in the three places a feature has to live at once and keeps them in step: the **Figma artifact** (the client's own library instances, updated in place), the **living prototype** (an HTML/CSS render, conformance-gated), and the **frontend repo** (typed component scaffolds and stubs on a branch, proposed for review). It reads the same bound contract for all three, so a prop the API cannot serve is caught once, not three times, and it closes with a coverage table that shows every contract row present in Figma, in the prototype, and in code, or names the miss. It is the per-feature unit of Care, and the step no single existing pipeline has: the join across the three targets.

**What this is.** A contract-driven, three-target increment: one delta plan, three builds that consume promoted skills rather than re-implementing them, and one coverage table that reconciles them. **What this is not.** Not a from-scratch prototype builder (`ui-studio` / `heyhi-ui-ux`). Not a standalone Figma write (`app-to-figma`, which this consumes as its Figma leg). Not the application read (`app-recon`). Not the intent map (`intent-journey-map`, which this consumes). Not the post-build audit (`heyhi-prototype-audit`, which this hands to). Not a judge of whether the feature is right.

**The boundary this skill obeys (Sheerline § 9, absolute).** A structured build with explicit empty judgment slots, a named human gate, and provenance labels on anything synthetic. The charter is one sentence: *a capability that fills its own judgment slot has exceeded its charter* (`sheerline/os/operating-principles.md` § Design Constraints). The empty slots here are **which interactions matter and which copy ships** (inherited from the states seam, `interaction-inventory` and `microcopy-states-writer`), the **one-off versus pattern** ruling on each NEW element, the **component match when inexact**, and **the merge**. The skill plans the delta, builds the three increments, and reconciles them; it never rules a feature done, promotes a pattern on its own authority, or merges a branch. Applied as a build-time test: *does any step below fill one of the slots in [§ The human-gated slots]?* If so, stop.

> **This skill closes through the Exit Gate (`CLAUDE-SESSION-RULES.md § Exit Gate`), Flavor A.** See the bottom-of-skill bracket.

---

## Prerequisites

- **The promoted engine skills are deployed.** `app-to-figma` (the Figma leg, consumed in update mode), `intent-journey-map` (the contract input), and `app-recon` (the manifest input) must live under `heyhi-skills/`, not `skill-updates/`. If any is still staged, **stop and report**: this skill orchestrates them and does not re-implement them.
- **The served application context is reachable.** `retrieve_application_context` (scope `manifest`, `intent`, `ijm`, `ds-map`, `patterns`) and `validate_output` are served by the per-system heyhi-mcp instance. Without them the skill has no contract to read and no conformance gate to run.
- **The Figma MCP is connected** and `use_figma` is reachable (probe it, do not trust the tool list), for the Figma leg. The artifact file is a **saved cloud** file and its library is **published** (an unpublished library is a human publish step named at the gate, not a thing the skill can do; `app-to-figma` § Prerequisites).
- **The frontend repo is present and typechecks clean at the baseline** (a repo that does not build before the increment cannot show the increment's typecheck as a signal). Its build/typecheck command is known (for `heyhi-website`: `eslint . && tsc --noEmit`).

---

## Routing: the cell this occupies, and its siblings

| If the task is… | Use |
|---|---|
| **Add one feature** across the Figma artifact, the prototype, and the repo from **one contract**, with the three-way coverage table | **this skill** |
| Write an application's surfaces into a Figma app file from the published library (standalone, or as this skill's Figma leg) | `app-to-figma`. This skill consumes it in **update mode** |
| Build an HTML / code prototype or interface from scratch | `ui-studio` (client) / `heyhi-ui-ux` (HeyHi), per CLAUDE.md § ui-studio routing. This skill consumes `ui-studio` **Mode A** for the prototype leg |
| Read the application into a manifest (surfaces, components, endpoints, copy) | `app-recon`. This skill's input |
| Map a feature's intent, journey, and prop contract | `intent-journey-map`. This skill's input |
| Audit a built prototype's interaction completeness / readiness | `heyhi-prototype-audit`. The audit this skill **hands to**, not one it runs |
| Turn located drift or an accessibility finding into an applied or proposed repair | `heyhi-drift-repair`. This skill reuses its **deviation-record** shape for the repo leg, and hands drift to it |
| Enumerate the interaction states of a screen, or write the copy for each state | `interaction-inventory` (area 4) / `microcopy-states-writer` (area 3). This skill **reads** their sidecars for the delta plan; it never enumerates or writes copy itself |
| Decide which interactions matter, which copy ships, one-off vs pattern, or the merge | **the human** (this skill's named gates) |

**The ui-studio routing override (plan D7).** A general "build a page / prototype" query still routes per CLAUDE.md § ui-studio routing; this skill's triggers are specifically the three-target increment ("add this feature to the artifact and the prototype and the repo", "feature increment", "build the new feature off the artifact"). This skill does not compete with `ui-studio` for a plain prototype build; it consumes `ui-studio` Mode A as its prototype leg.

---

## Inputs (retrieved through the instance, never pasted as a spec)

The source of truth is the per-system heyhi-mcp instance (Sheerline area-7 FOUNDATION, Invariant 4: *retrieved, never pasted*). This skill loads no contract file, token file, brand config, or DESIGN.md from disk as its spec.

1. **The feature's intent-journey map and its prop contract**, produced by `intent-journey-map` (Lane D) and served through `retrieve_application_context(scope: ijm)`. The 14-column contract row binds each data prop by JSON pointer to the application's OpenAPI; a prop whose field the spec does not carry arrives already flagged, never invented.
2. **The served application context**: `retrieve_application_context(scope: manifest)` for the surfaces, components, and endpoints (`app-recon`, Lane C); `scope: intent` for the encoded decisions and constraints (`app-intent-map`); `scope: ds-map` for the crosswalk that says which contract component exists in the design-system package and which is a local pattern (`figma-library-census`, Lane A); `scope: patterns` for the ledger. Until an upstream artifact lands, a hand-written input in the same § 3.3 shape is the substitute, and that is how the instance's own proof run ran.
3. **`figma_app_file_key`** is the **target artifact** file (the app/screens file `app-to-figma` built, updated in place). A saved cloud key; a local/unsaved key is refused by the Figma leg.
4. **The prototype root** (the living prototype's source tree) and **the frontend repo** (the code target). For the instance's own proof run these are the same tree, `heyhi-website/`; in a client engagement they are named separately in the profile.

Echo one line before any write: `Feature:<name> · surfaces:<n> · contract rows:<n> · targets:[figma|proto|repo] · seal:<bool>`.

The delta-plan rules and the coverage-table columns live in **[references/method.md](references/method.md)** and **[references/coverage-table.md](references/coverage-table.md)**; the per-framework repo scaffolds live in **[references/repo-adapters.md](references/repo-adapters.md)**; the probe log (the update-mode Plugin-API calls this skill depends on) lives in **[references/probes.md](references/probes.md)**; the dependency-ripple step (exercise every dependent, folded into Step 6) lives in **[references/dependency-ripple.md](references/dependency-ripple.md)**. All load on demand, not at session start.

---

## Step 0: Improvement hook check

Before running, retrieve any recurring corrections for increment / three-target / contract-coverage work (`retrieve_design_corrections` if the instance is reachable, or the Sheerline `os/corrections/` registry). Fold a matching recurring correction into the run. Skip silently if none.

## Step 1: Load context, the promoted engine skills, and the contract

1. **The promoted engine skills.** Confirm `app-to-figma`, `intent-journey-map`, and `app-recon` are deployed (§ Prerequisites). Load `app-to-figma` (its update mode, Step 7) and `ui-studio` (Mode A, the Page Plan gate, the Component Implementation Map) as the engines this skill orchestrates. This skill assumes them; it does not restate the Figma call sequence or the prototype build.
2. **The served context** through the instance (§ Inputs): the ijm contract, the manifest, the intent, the ds-map, the patterns. Never inline a file as the spec.
3. **The states seam.** Read the feature's `interaction-inventory` sidecar (`inventory-schema.json`) and its `microcopy-states-writer` sidecar (`microcopy-schema.json`) when they exist: the states to build and the copy slots to fill. This skill **reads** them; it never enumerates the states or writes the strings (those are areas 4 and 3, and they are two of this skill's empty slots).

## Step 2: The delta plan (the load-bearing human gate, no writes)

Before any target is touched, produce the **delta plan** and get it approved. It writes nothing. It is the Earn-the-Room approval artifact, the one gate that fires before the Figma, prototype, and repo builds begin.

The delta-plan table, one row per contract element:

| Column | What it holds |
|---|---|
| **Surface** | the surface `id` from the manifest the element lands on (an existing surface updated, or a NEW surface) |
| **State** | the interaction state from the `interaction-inventory` sidecar (default / hover / focus / selected / loading / empty / error / success), or the human's list in that shape |
| **Component** | the component that renders it, with its **resolution**: `library` (exists in the design-system package per the ds-map), `local pattern` (a composition the library lacks), or `NEW` (a genuinely new element) |
| **Endpoint** | the endpoint the state binds to (`method path`, or `none` for a client-only state), grounded through the contract's JSON pointer |
| **Copy slot** | the UX-writing slot the state needs (from `microcopy-states-writer`), left as a named slot; the string is **not** written here |

**Per NEW element, name the one-off-versus-pattern question** and leave it for the human: is this a one-off for this surface, or the first sighting of a pattern that will recur? The skill records the promotion signal it can compute (the ds-map recurrence, the plan § 5 D4 defaults) as a neutral fact; it does not rule the element a pattern. **Print the delta plan** to chat and get approval before Step 3. Surface every live fork (an inexact component match, a contract row the spec cannot ground, a NEW element's ruling); do not resolve one to keep moving.

Produce this exact structure. The one-off-vs-pattern, inexact-match, and merge slots stay empty by construction; the promotion-signal line carries a fact, never a ruling.

```
# Delta plan: [feature name]
Contract: [ijm id / served scope]     Targets: [figma | prototype | repo]     Planned: [date]

## Delta rows
| Surface | State | Component (resolution) | Endpoint | Copy slot |
|---------|-------|------------------------|----------|-----------|
| /log (existing) | filter: idle/selected | CategoryFilter (NEW → one-off? pattern?) | none (client filter) | "All", <category labels> |
| /log (existing) | list: empty-result | (reuse existing card + empty state) | none | empty-state message |

## Promotion signal (fact, not a ruling)
[e.g. "CategoryFilter recurs on 1 surface; D4 threshold is 3 surfaces / 2 apps / 2nd IJM. Below threshold." No verdict.]

## Unresolved forks (surface every one; resolve none)
- [inexact component match, with the nearest ds-map candidate]
- [a contract row the spec cannot ground (flagged, not invented)]

## ⛔ One-off vs pattern: NEEDS HUMAN (per NEW element)
   Ruling: ____________________

## ⛔ The merge: NEEDS HUMAN
   The repo increment ships as a propose-first PR; whether it merges is the reviewer's.

## Named gate
Sign-off owner (design lead / eng owner): ____________________  Date: ______
No target is written until this delta plan is approved.
```

## Step 3: The Figma artifact increment (through app-to-figma, update mode)

Consume the promoted `app-to-figma` in **update mode** (its Step 7). Do not re-implement the build inline.

- `get_metadata` the existing artifact frames for the feature's surface; find-or-update by the state ledger, never duplicate a section.
- For each delta-plan row resolved `library`: `app-to-figma` imports the component set / variable / style by key and instances it, or `swapComponent` for a changed variant and `setProperties` for changed props.
- For each row resolved `local pattern`: `app-to-figma` builds the pattern once as a component (only at the human's ruling from Step 2), places instances, and emits a ledger row (Step 7 below) into the proof folder.
- Edit only the target artifact file (the Wave 1 scratch file for the instance's own proof run). Never write to a production Figma file. Never detach an instance. Never clobber a human-ruled deviation on a re-run.

The Figma leg is **propose-first** in spirit (plan D9): it lands the increment into the scratch artifact, and whether the increment is right stays the surface verdict (`app-to-figma`'s empty slot, inherited here).

## Step 4: The prototype increment (through ui-studio Mode A, conformance-gated, BLOCKING)

Consume `ui-studio` **Mode A** for the prototype increment (its Page Plan gate and Component Implementation Map). Then run the conformance gate, which is **blocking** (plan D9):

- Build the feature's prototype section as HTML/CSS through Mode A, grounded in the served design system, not generic defaults.
- Run `validate_output(artifact: <the emitted CSS/HTML>, artifact_type: "rendered_css")`. **A `valid: false` result fails the step.** Read the `errors[]`, fix the increment, re-validate. The prototype increment does not pass until `validate_output` returns `valid: true`. Paste the result (the `valid` field and any `errors`) into the proof record.
- This is the one blocking gate across the three legs. The Figma and repo legs are propose-first; the prototype conformance gate blocks.

## Step 5: The repo increment (propose-first, on its own branch)

On a **second, proof branch** (never `main`, never merged by this skill), scaffold the feature in the frontend repo, typed from the contract. See **[references/repo-adapters.md](references/repo-adapters.md)** for the per-framework shape (React is built for this arc, plan D5; Lit and Angular are named stubs).

1. **Component scaffolds typed from the contract.** For each NEW or changed component, a typed scaffold whose props are the contract's prop rows (name, type, required, enum). A prop the contract flags as unbindable is scaffolded with a typed placeholder and a `// contract: unbound` marker, never a fabricated value.
2. **A story per variant.** For each variant axis in the contract, a story (Storybook when the repo has it; when the repo has no story harness, record the story as a named gap with a finding id, do not invent a harness). The story is a render surface for the reviewer, not a test.
3. **Import from the package where the crosswalk says the component exists; a local pattern where it does not.** Read the ds-map: a `both` / `code-only` row imports from the design-system package; a `figma-only` or absent row is a local pattern in the repo, named from the ds-map, with a ledger row.
4. **Route and hook stubs.** The route registration and the data hook the contract's endpoints imply, as stubs typed to the endpoint's request/response pointer, never a live fetch invented beyond the contract.
5. **Typecheck.** Run the repo's typecheck (`eslint . && tsc --noEmit` for `heyhi-website`). A failing typecheck is a finding on the increment, recorded, not hidden.
6. **The conformance read (informing, not blocking).** Run `validate_output` on the increment's rendered CSS. Unlike Step 4's prototype gate, this leg is propose-first: a conformance finding is written into a **reversible deviation record** (the `heyhi-drift-repair` shape verbatim: `{ finding, matched_correction, before, after, surface, location, timestamp, provenance: automated, confirmed: false }`, where `matched_correction` is `null` for a raw conformance finding with no registry match), it does not block. The human confirms or reverts at review.
7. **Open a propose-first PR** on the proof branch. Never merge it. `heyhi-website/` is a folder of this monorepo, not a separate repository, so the proof branch is a branch of this repo touching that folder only.

## Step 6: The three-way contract coverage table

Reconcile the three increments against the one contract. Emit the table **even when every row passes** (a clean table is the proof the join held). See **[references/coverage-table.md](references/coverage-table.md)** for the exact columns and the miss rules.

One row per contract element. Each of the three target columns holds either the evidence of presence or a **finding id**:

| Contract element | In Figma | In the prototype | In code | Verdict |
|---|---|---|---|---|
| a prop / state / component from the contract | a property, a text value, or a bound variable on the artifact node | a data binding or a rendered state in the prototype | a prop or a hook field in the repo increment | pass, or a finding id |

**The miss rules.** A contract row absent from a target is either an **explained miss** (a finding id with a stated reason: operator-gated, deferred, or a genuine gap the human must close) or an **unexplained miss** (a row silently absent from a target with no finding). An unexplained miss fails the coverage table. There is no "close enough": a row is present with evidence, or it is a finding.

Emit this exact structure. Presence carries evidence (a node property, a data binding, a prop name); absence carries a finding id and its reason. The verdict column is mechanical (pass when all three carry evidence; otherwise the finding that explains it); it is not a judgment of whether the feature is good.

**Dependency ripple.** After reconciling the three targets, exercise every dependent of the changed node and fold the results into this same table. Root `retrieve_design_relationships(query_type="impact_analysis", ...)` at the semantically-changed node (the changed **token** for a token/variable-value change), `max_hops=4` (full-within-cap, narrowed by a dependent-count cap). Add one row per dependent with a three-state verdict — `exercised: pass` / `exercised: FAIL → finding` / `NOT exercised (beyond horizon / cost cap): N` — under the same miss rules: a dependent absent with no finding is an unexplained miss and fails the table; `NOT exercised: N` is the explained-miss form for a beyond-horizon dependent. A failed dependent is a **hard finding** in the reversible-deviation-record shape (Step 5), never a silent miss, never an auto-revert. Full method: `references/dependency-ripple.md`.

```
# Contract coverage: [feature name]
Contract: [ijm id]     Reconciled: [date]     Unexplained misses: [must read 0]

| Contract element | In Figma | In prototype | In code | Verdict |
|------------------|----------|--------------|---------|---------|
| CategoryFilter.categories: string[] | chip-row instances (nodes …) | rendered chip row | prop categories: string[] | pass |
| CategoryFilter.selected (state) | Selected variant | .is-selected class | useState selected | pass |
| filter chip: focus-visible | (finding F-01: operator-gated) | :focus-visible ring | :focus-visible | F-01 |
| list: empty-result state | frame present | empty-state block | conditional render | pass |

## Findings (every non-pass row)
- F-01 [operator-gated]: the Figma column is blocked on the proof library being published
  (a Figma UI action, no Plugin-API path). Not an unexplained miss; a named operator step.

## Read-out (fact, not a verdict)
Rows: [n]     Pass: [n]     Findings: [n]     Unexplained misses: 0
```

An unexplained miss (a blank target cell with no finding) is a hard failure of the run; the read-out line must show `Unexplained misses: 0`.

## Step 7: Ledger emission for a NEW composition

When Step 2 ruled a NEW element a **local pattern** (a composition that repeats and the library lacks), emit a **pattern ledger row** in the plan § 3.3 shape (`name`, `signature`, `level`, `status: local`, `usage.applications / surfaces / figma_nodes / code_paths`, `origin`) into the **proof folder** (the instance's engagement folder, `<engagement folder>/<proof>/`), not the served data. The served `components.json` ledger is written only by the convergence pass or a Care run under the human's clearance. Emitting a `local` row records the sighting; the `candidate` and `promoted` flips are the human's, downstream. This skill never writes `candidate` or a gate/approval field (§ Hard constraints).

---

## Idempotency and re-runs

The Figma leg re-reads the `app-to-figma` state ledger (`<engagement folder>/<proof>/app-to-figma-state-{RUN_ID}.json`) and updates by node ID (find-or-update), so a re-run never duplicates a section and never re-imports a component already present. The repo leg is idempotent by branch: a re-run updates the same proof branch and the same PR, it does not open a second one. The coverage table is regenerated each run from the current three targets, so a re-run's table reflects what is actually present now, not a cached pass. A human-ruled deviation (a deliberate departure from the library or the contract, recorded at the delta-plan gate) is never silently reverted on a re-run.

## The Care seam

`feature-increment` is the per-feature unit that `design-system-care-monthly` § 5e (the bidirectional artifact re-sync) runs at cadence. Care detects that the served system drifted from the artifact and calls this skill to re-land the affected features; this skill does the increment and hands the coverage table back. The seam is direction: Care decides *when* to re-sync and *which* features; this skill does the three-target increment and reconciles it. Neither skill promotes a pattern on its own authority: the ledger rows this skill emits (`status: local`) are read by Care's § 3b ledger review, and the promotion to `candidate` is the human's at that review.

## Worked example: the instance's own proof run (the Log-index category filter)

The proof (plan § 5 D2 substrate, the heyhi.design Log index) adds one small feature: a **category filter** on the Log index. The distinct categories are derived from the served log data (a small, closed set); the filter is a row of selectable chips (`All` plus one per category) that narrows the visible entries client-side, with an empty-result state when a category has none.

- **Contract (hand-written in the ijm shape, since the upstream IJM runs separately):** a `CategoryFilter` component with a `categories: string[]` prop (derived, not fetched), a `selected: string` state prop, an `onSelect` callback, and the interaction states idle / hover / selected / focus-visible per chip, plus the list's empty-result state. No endpoint (client-side filter).
- **Figma leg:** through `app-to-figma` update mode into the Wave 1 scratch artifact, a chip-row section added to the Log-index frame, chips as instances of the library's chip/tag component with the `selected` variant, bound to the served type and color variables. (Operator-gated when the proof library is unpublished; recorded as a finding, not an unexplained miss.)
- **Prototype leg:** through `ui-studio` Mode A, an HTML/CSS render of the filter and the filtered list, validated with `validate_output(rendered_css)` until `valid: true`.
- **Repo leg:** a typed React `CategoryFilter` on the `feature-increment-proof-<date>` branch, wired into the Log-index route with `useState` for the selection and a derived category list, typechecked with `eslint . && tsc --noEmit`, opened as a propose-first PR, never merged.
- **Coverage table:** every contract row present in all three columns, or a finding (the Figma column carries the operator-gated finding when the library is unpublished). The proof record, the file keys, the acceptance table, and the per-section screenshots live in `<engagement folder>/feature-increment-proof/` (gitignored, main workspace).

---

## The human-gated slots (§ 9 boundary, enumerated and non-empty)

Each row below is a **NEEDS HUMAN** slot: the skill leaves it empty and names the gate; a version that fills one has overstepped. The load-bearing gate is the **delta plan** (Step 2), a **NEEDS HUMAN** approval before any target write, and the **PR review** (Step 5), a **NEEDS HUMAN** approval before any merge.

| Judgment slot (NEEDS HUMAN, stays human) | Trigger | The gate + provenance rule |
|---|---|---|
| **The delta plan** (load-bearing) | Before any target write | The delta-plan table + the unresolved forks are printed and **approved** before Step 3. Read-only; writes nothing. |
| **Which interactions matter, and which copy ships** | Inherited from the states seam | The skill reads the `interaction-inventory` and `microcopy-states-writer` sidecars; it never enumerates the states or writes a string. Which states to build and which copy ships stay areas 4 and 3, behind their own gates. |
| **One-off versus pattern** | A NEW element | The skill records the computed promotion signal as a neutral fact and emits a `local` ledger row; whether the element is a pattern to promote is the human's, at the ledger-review gate. Never writes `candidate`. |
| **The component match when inexact** | A contract component has no exact library/package match | Surface the nearest candidate from the ds-map; the human chooses reuse / wrap / local-pattern. Never pick the inexact match yourself (this is `app-to-figma`'s gate, inherited). |
| **The merge** | Always | The repo increment is a propose-first PR; whether it merges is the reviewer's call (the `dont-automate` line). The skill proposes and validates; it never merges. |

`figma-generate-design`'s own floor holds via `app-to-figma`: when exactly one path is clearly correct from the contract and the ds-map, take it. The gate fires on genuine ambiguity, not on every mechanical choice.

---

## Hard constraints (every run)

- **One contract, three targets.** Every target reads the same served contract. A prop the contract flags unbindable is unbound in all three; the skill never fabricates a value in one target to make a coverage row pass.
- **Consume the promoted skills; never re-implement them.** The Figma build is `app-to-figma` in update mode; the prototype build is `ui-studio` Mode A; the manifest and contract are `app-recon` and `intent-journey-map`. This skill orchestrates and reconciles; it re-implements no engine.
- **The prototype conformance gate is blocking; the Figma and repo legs are propose-first** (plan D9). A `validate_output` `valid: false` fails Step 4. The repo leg's conformance finding is a deviation record, not a block; the PR is never merged by the skill.
- **The coverage table is emitted every run**, pass or miss. An unexplained miss (a silently absent contract row) fails the run. A miss is a finding with a reason, never "close enough".
- **Ledger a NEW composition as `local` only, into the proof folder.** Never write `candidate`, `promoted`, or any gate/approval field; those are the human's, downstream (§ Step 7). The served ledger is the convergence pass's or a cleared Care run's, never this skill's.
- **Propose-first, never merge, never push to `main`.** The repo increment is a branch and a PR. The Figma increment edits only the scratch/target artifact file (never a production Figma file). Never detach a Figma instance.
- **Prose and seal.** No em dashes, no banned words, no pricing; no client name, file key, or engagement detail in a tracked file. Proof records, file keys, screenshots, and the state ledger go to the instance's engagement folder (`<engagement folder>/<proof>/`, gitignored).

## Failure modes and recovery

| Symptom | Cause | Recovery |
|---|---|---|
| an engine skill is still under `skill-updates/` | the convergence pass has not promoted it | **stop and report**; this skill orchestrates promoted skills, it does not re-implement them |
| `validate_output` returns `valid: false` on the prototype | the increment drifted from the served system | read `errors[]`, fix the increment, re-validate; Step 4 does not pass until `valid: true` |
| a contract row has no target evidence and no finding | an unexplained miss | fail the coverage table; either land the row in the target or write the finding with its reason |
| the Figma library is unpublished, so `app-to-figma` cannot import by key | import-by-key resolves nothing from an unpublished source | name the publish step for the human (a Figma UI action, no Plugin-API path); record the Figma column as an operator-gated finding, not an unexplained miss |
| the repo has no story harness | not every repo runs Storybook | record the story as a named gap with a finding id; do not invent a harness or fake a story |
| the typecheck fails on the increment | a scaffold's type does not match the contract or the repo | record the failure as a finding on the increment; fix the scaffold toward the contract, never loosen the repo's types to pass |

## What is explicitly out of scope

- **The design truth**: which interactions matter, which copy ships, whether an element is a pattern, whether the increment is right, whether to merge. Empty slots by construction (§ 9).
- **Building a prototype or interface from scratch**: `ui-studio` / `heyhi-ui-ux` (CLAUDE.md § ui-studio routing). This skill consumes Mode A, it does not compete with it.
- **Writing screens into Figma as a standalone build**: `app-to-figma` (this skill's Figma leg, consumed in update mode, never re-implemented). **Reading the application**: `app-recon`. **Mapping intent and the contract**: `intent-journey-map`.
- **Enumerating interaction states**: `interaction-inventory` (area 4). **Writing state copy**: `microcopy-states-writer` (area 3). This skill reads their sidecars; it authors neither.
- **Auditing the built prototype**: `heyhi-prototype-audit` (the audit this hands to). **Repairing located drift**: `heyhi-drift-repair` (whose deviation-record shape this reuses).
- **Writing pattern rows into the served `components.json`**: the convergence pass or a cleared Care run only. **Creating `pattern-intake/`**: Lane I. **Editing any shared anchor**: the convergence pass.
- **Merging the proof PR, or writing to any production Figma file or client repo**: the instance's own proof run uses the scratch artifact file and a propose-first, unmerged branch of this monorepo only.

---

## Exit Gate Required Headers (bottom-of-skill bracket)

This skill closes through the Exit Gate Flavor A (`CLAUDE-SESSION-RULES.md § Exit Gate`). Before declaring done, confirm every header carries real content, not a claim:

- `## Fixes Applied`: the feature added, the three targets touched (the Figma section and its link, the prototype section, the repo PR URL), the coverage table with zero unexplained misses, the ledger rows emitted, and where the proof is filed.
- `## Smoke Test`: the prototype `validate_output` result (`valid: true`), the coverage table, the typecheck result, the render-and-look (a screenshot of the Figma section and the prototype section), and the proof-branch PR open and unmerged.
- `## Next Session Prompt`: the human-gated slots still open (the one-off-vs-pattern rulings, the inexact matches, the merge), any target deferred (an operator-gated Figma leg), and the ledger candidates awaiting review.

If the coverage table has an unexplained miss, or the prototype gate did not pass, or the PR was merged, the gate has **not** been satisfied.

---

*HeyHi Confidential. Sheerline area 12 (DesignOps), Care/increment verb. v0.1.0 staged 2026-09-07 from `plans/plan-sheerline-fdde-loop-2026-09-07.md` (DISPATCH-07, Lane F). Engines consumed: `app-to-figma` (update mode), `ui-studio` (Mode A), `intent-journey-map` + `app-recon` (inputs), `validate_output` (the blocking prototype gate). Deviation-record shape reused from `heyhi-drift-repair`. Boundary: § 9.*
