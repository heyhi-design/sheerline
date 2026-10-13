---
name: figma-library-census
description: >-
  Read-only census of a client's Figma component and token libraries, plus the
  crosswalk that joins them to the served code-component manifest. Produces three
  machine-readable maps: figma-library-map.json (component/style name to published
  key + property axes), figma-variable-map.json (variable name to key, resolved
  type, modes, code syntax), and ds-map.json (the crosswalk with a coverage state
  and a CANDIDATE atomic level per component). Triggers: "census this Figma
  library", "map figma components and tokens to code", "which components exist in
  figma but not in code", "figma to code crosswalk", "coverage matrix figma to
  code". Runs the
  mechanical join and enumerates every conflict; the token-conflict winner, the
  naming reconciliation, and the confirmed level ship EMPTY behind a named human
  gate (the crosswalk review). NOT a design-system health or drift audit (use
  heyhi-design-intelligence-audit); NOT extracting tokens into a build config (use
  ui-studio-onboard); NOT writing or generating anything into a Figma file (use
  app-to-figma or heyhi-figma-ds-generator); NOT reading an application codebase
  into a manifest (use app-recon).
version: "0.1.0"
updated: "2026-09-07"
status: "deployed 2026-09-07 (Sheerline fdde-loop convergence pass 1, DISPATCH-06; promoted from skill-updates/figma-library-census/). Sheerline area 7 (Design Systems), forward-deployed loop stage 2 (read/serve). Spec: plans/plan-sheerline-fdde-loop-2026-09-07.md sections 3.2, 3.3, DISPATCH-01. Emits the three contracts Lanes B, F, G, I read."
review_by: "2026-09-21"
classification: confidential
---

# Figma Library Census

**Sheerline area 7 (Design Systems) · forward-deployed loop stage 2 · read-only census + crosswalk.** Given a client's published Figma libraries and the design system served through the per-system heyhi-mcp instance, this skill reads (never writes) the Figma side and produces the two join tables and the crosswalk that every later Figma write (`app-to-figma`), feature increment (`feature-increment`), and the pattern ledger depend on. The join tables (component name to key, variable name to key) and the atomic classification do not exist anywhere else in the harness; the loop cannot place a library instance into an app file without them.

**The boundary this skill obeys (Sheerline § 7, absolute).** The census is mechanical: it reads the Figma libraries, joins them to the served manifest, and enumerates every disagreement. It fills no judgment. Which side of a token conflict wins, whether a `figma-only` and a `code-only` row are one component under two names, and the confirmed atomic level of each component all ship EMPTY behind the crosswalk-review gate. The census flags; the human adjudicates. Mechanics never taste.

> **This skill closes through the Exit Gate** (`## Fixes Applied`, `## Smoke Test`, `## Next Session Prompt`). See the bottom-of-skill bracket.

## Routing and disambiguation with sibling skills

| If the task is… | Use |
|---|---|
| Read a Figma library and map it to code (this skill) | **figma-library-census** |
| Judge a design system's health, drift, or component-code fidelity | `heyhi-design-intelligence-audit` |
| Extract Figma tokens/components into a ui-studio build config | `ui-studio-onboard` |
| Write, generate, or sync anything into a Figma file | `app-to-figma` (surfaces) or `heyhi-figma-ds-generator` (a system) |
| Read the application codebase into an app-manifest | `app-recon` |
| Decide the token-conflict winner, the naming merge, or the confirmed level | **the human** (the crosswalk-review gate) |

## Step 0: Improvement hook check

Call `retrieve_design_corrections` for anything learned about this system's tokens, components, or naming, and check `sheerline/os/corrections/` for census-relevant entries. Fold what applies; if nothing applies, skip silently. Do not invent a correction.

## Step 1: Confirm the read-only, hermetic, instance-scoped setup

Before any read:

1. **The instance is the only spec.** The code side of the crosswalk is retrieved through the per-system heyhi-mcp instance (`retrieve_design_context` for the component list and token maps; `retrieve_design_relationships` with `query_type: component_uses` for containment). **Never read a `components.json`, a token file, or a `DESIGN.md` from disk as the spec.**
2. **Confirm the Figma connection.** Run `whoami` (or a read-only `use_figma`) and confirm the target file is a saved cloud file. A LOCAL or unsaved file (a `localFileKey` URL) is refused, ask for the saved `figma.com/design/<fileKey>` URL.
3. **Hermetic seal.** The `file_key` and every asset key (component, variable, style) of a client library are engagement detail. The real keys go only to the gitignored proof folder in the instance's engagement folder (outside the tracked tree). The tracked maps redact the `file_key` AND every asset key to name-derived placeholders (e.g. `redacted-comp-<name>`): the real 40-char hex keys read as high-entropy secrets to the Gitleaks pre-commit hook, and are engagement-specific. Never write a client name, a file key, or a real asset key into a tracked file.
4. **Inputs.** The consuming file key (the app file that has the library added) OR the defining library file key; the tier; and the served system id. For the instance's own first proof run the input was its own 2026-09-04 generated library (key read from its gitignored proof record).

## Step 2: Run the census (the method)

Full method, rules, and the worked example: `references/method.md`. Read-only `use_figma` scripts: `scripts/`. Probe log (every API call, observed on the scratch library at Pro tier): `references/probes.md`. Probe any Plugin API call in a scratch read before you depend on it (Arc rule 9).

1. **Libraries and pages.** `get_libraries({ fileKey })` on the consuming file, paginating `libraries_available_to_add` via `libraries_available_to_add_next_offset`; record added vs available. Then `scripts/census-step1-pages.js` for the page list (the fan-out targets for step 3). Do not trust `get_metadata`'s page list, the `use_figma` read is authoritative.
2. **Variable census** (`scripts/census-step2-variables-styles.js`). From a consuming file, `teamLibrary.getAvailableLibraryVariableCollectionsAsync()` then `getVariablesInLibraryCollectionAsync(key)` give `name`, `key`, `resolved_type` and the `remote: true` provenance. **Modes and code syntax are NOT returned by that remote read** (Ground-truth correction); read them in the DEFINING token file via `getLocalVariableCollectionsAsync` (modes) and `getLocalVariablesAsync` (code syntax, resolved type, scopes). Census the text and effect styles the same pass.
3. **Component census** (`scripts/census-step3-components.js`, one page per call via `page.loadAsync()`, not `setCurrentPageAsync`, so the census makes no view-state change and the per-page calls run in parallel safely). `findAllWithCriteria({ types: ['COMPONENT_SET','COMPONENT'] })` per library page; keep the sets and the standalone components as rows (variant children are not rows). Read `componentPropertyDefinitions` on the property-owner (a COMPONENT_SET, never a variant, it throws on a variant) for `name`, `type` in TEXT / BOOLEAN / VARIANT / INSTANCE_SWAP / SLOT, and the values; read `defaultVariant`.
4. **The crosswalk** (`references/method.md` § step 4). Join the Figma component census against the served manifest (through the instance). Set `coverage` per row: `both` / `code-only` / `figma-only` / `divergent`. Copy `token_refs[]` from the served token map. Flag every `divergent` row and every naming mismatch; do not merge or adjudicate.
5. **The candidate classification** (`references/method.md` § step 5). Assign a candidate `level` (`token / atom / molecule / organism / template`) from Figma composition first, refined by served-graph containment where the manifest encodes it, raised by cross-surface recurrence. An `INSTANCE_SWAP` of a leaf/icon component does not promote an atom. Set `level_confirmed: false` on every row. Note honestly if the served graph encodes no containment (HeyHi's does not today, so Figma composition is authoritative there).

## Step 3: Produce the three maps

Emit the three files against `schemas/*.schema.json` (version 1.0), redacting the `file_key` and every asset key to placeholders in the tracked copies (real keys to the gitignored proof only). Then print the review surface with the empty slots and the gate.

The step-2 script output is DIAGNOSTIC, not the emitted map: it carries each variable's `remote` provenance (recorded to distinguish a library variable from a local one) and its `scopes` for the census's own reasoning, and step-3 output carries a `read_errors[]` for any owner whose definitions could not be read. The emitted `figma-variable-map.json` keeps only the § 3.3 fields (`name`, `key`, `resolved_type`, `code_syntax`, `dtcg_token` filled here) and drops `remote`/`scopes`; remote provenance is preserved by the collection's `library_key` (non-null = a remote library) and the remote-vs-local read path. A non-empty `read_errors[]` is surfaced to the human, never emitted into a map.

```
FIGMA LIBRARY CENSUS: <system id>
  Libraries: <N added / M available>   Figma plan tier: <tier>
  Components: <N> (sets <a>, standalone <b>)    Styles: <text> text, <effect> effect
  Variables: <N> across <C> collections (<mode summary>)

CROSSWALK COVERAGE (true counts)
  both <n> · code-only <n> · figma-only <n> · divergent <n>

CANDIDATE LEVELS (all level_confirmed: false)
  <component> / <coverage> / level candidate: <level>
  ...

## ⛔ Token conflicts: NEEDS HUMAN
This slot is intentionally empty. Each `divergent` row and each unmatched `dtcg_token`
is a candidate disagreement between Figma and code. Which side is correct is a values
decision, not a mechanical one.
  Divergent / unmatched rows: ____________________  Winner (per row): ____________________

## ⛔ Naming reconciliation: NEEDS HUMAN
A `figma-only` and a `code-only` row that are really one component under two names:
  Candidate pairs: ____________________  Merge? (per pair): ____________________

## ⛔ Confirmed levels: NEEDS HUMAN
The candidate levels above use HeyHi's atomic vocabulary; the client may use another.
  Confirmed level (per component): ____________________  Vocabulary the client uses: ______

## Named gate: the crosswalk review
Sign-off owner (design-system lead): ____________________  Date: ______
No token-conflict winner, no naming merge, and no `level_confirmed: true` is recorded
until this line is signed by a human.
```

## Step 4: Pre-flight verification

- The three maps validate against their schemas (`schemas/*.schema.json`).
- No `use_figma` script created, mutated, or deleted anything (grep the scripts; the census is read-only).
- The `file_key` and real keys appear only in the gitignored proof folder, never in a tracked file.
- Every ⛔ slot is empty and the gate line is unsigned; `level_confirmed` is `false` on every row.
- The true coverage counts are reported (do not invent a `figma-only` or `divergent` row that the read did not find).

## What is explicitly out of scope

Writing anything into a Figma file (that is `app-to-figma`); building or generating a design system in Figma (`heyhi-figma-ds-generator`); judging system health or drift (`heyhi-design-intelligence-audit`); extracting into a ui-studio config (`ui-studio-onboard`); reading the application codebase (`app-recon`); adding pattern rows to the served data (the pattern ledger is written only by the convergence pass or a cleared Care run); adjudicating any conflict, merge, or level (the human, at the gate).

## Exit Gate Required Headers (bottom-of-skill bracket)

Close every run with:

- `## Fixes Applied`, the three maps produced, coverage counts, what the census read.
- `## Smoke Test`, schemas validate; scripts read-only; no file key in tracked output; slots empty.
- `## Next Session Prompt`, the open judgment slots for the crosswalk review, and any Plugin API path not yet observed on a populated run.

*HeyHi Confidential. Sheerline area 7 (Design Systems). Boundary: § 7. The census reads and joins; the human adjudicates.*
