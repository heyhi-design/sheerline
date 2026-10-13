---
name: ds-component-author
description: >-
  Author ONE design-system component into both Figma and code from a single
  component spec (name, anatomy, property axes, states from an interaction-inventory
  sidecar, slot regions, tokens) plus a target framework. It (1) builds the Figma
  component in the library file (variants, bound TEXT / BOOLEAN / INSTANCE_SWAP
  properties, INSTANCE_SWAP for icons, plus a probed slot step) by reusing
  heyhi-figma-ds-generator's Phase 3 by reference, never reimplementing it; (2)
  emits the code twin (React: a typed props interface from the same axes, CSS bound
  to the served token names, one story per variant; Lit and Angular as named
  stubs); and (3) writes a parserless Code Connect template (Component.figma.ts,
  figma.code) from the node ids and props, publishing it only when the plan and the
  Figma tier allow. Triggers include "create a design system component in Figma and
  code", "author a DS component", "build this component in the library and the
  package", "add a component to the Figma library and the code package from one
  spec". The anatomy and property axes (a design decision), the framework idioms
  where they conflict with the Figma structure, and the craft critique of the
  rendered component ship EMPTY behind two named human gates (spec review before any
  write; component review after). NOT for standing up a WHOLE design system into
  Figma from the served contract (use heyhi-figma-ds-generator; this authors one
  component, that generates the system); NOT for a spec-driven CHANGE to an existing
  component with a deprecation shim, codemod, and changeset (use ds-component-change);
  NOT for translating a built prototype or vectorizing a raster into Figma (use
  heyhi-design-bridge); NOT for repairing located drift back into code or tokens
  (use heyhi-drift-repair); NOT for extracting tokens FROM Figma into a config (use
  ui-studio-onboard); NOT for the read-only census or crosswalk of a library (use
  figma-library-census).
version: "0.1.0"
status: "deployed 2026-09-08: heyhi-skills/ds-component-author/ (promoted at the DISPATCH-11 convergence pass). Built for DISPATCH-08, Lane G of plans/plan-sheerline-fdde-loop-2026-09-07.md. A live proof on the instance's own design system ran green (Chip: a 10-variant Figma component set in the scratch library + a typechecking React twin in @heyhi/components + a parserless Code Connect template, all from one spec; proof PR #822 propose-first; record in the instance's engagement folder). Sheerline area 7 (Design Systems), build class N. React only for this arc (D5); Lit and Angular are named stubs. Code Connect emitted, not published (D1; every current Figma plan is Pro)."
review_by: "2026-09-21"
classification: HeyHi Confidential
---

# DS Component Author

**Sheerline area 7 (Design Systems), build class N, a two-leg component-author skill.** From one component spec it authors a single design-system component into two places at once: a variant component in the Figma library file, and its code twin in the component package, joined by a Code Connect template. It is the **promotion-execution verb**: when a repeating composition is promoted out of `pattern-intake/`, this is what builds the promoted component in the library and in the package from one contract, so the two never drift at birth. The Figma leg reuses `heyhi-figma-ds-generator`'s Phase 3 by reference (the generator stands up a whole system; this authors one component); the code leg and the join across the two are the new work.

**The boundary this skill obeys (Sheerline judgment charter, absolute).** A structured artifact with explicit empty judgment slots, named human gates, and provenance labels on anything synthetic. The one-sentence charter: *a capability that fills its own judgment slot has exceeded its charter.* The empty slots here are the **anatomy and property axes** (a design decision the human authors in the spec, never invented by the skill), the **framework idioms** where a code idiom and the Figma structure genuinely conflict (surfaced, not silently reconciled), and the **craft critique** of the rendered component. The named gates are the **spec review** before any write and the **component review** after. A version that invents an axis, resolves an idiom conflict silently, or grades the result has overstepped. Applied as a build-time test: does any step below fill one of the slots in [The human-gated slots]? If so, stop.

> **This skill closes through the Exit Gate (`CLAUDE-SESSION-RULES.md § Exit Gate`), Flavor A.** See the bottom-of-skill bracket.

---

## Routing, the cell this occupies, and its siblings

| If the task is... | Use |
|---|---|
| **Author one component** into the Figma library AND the code package from one spec | **this skill** |
| Stand up a **whole design system** (collections, token styles, the component library) into Figma from the served contract | `heyhi-figma-ds-generator` (this authors one component; that generates the system) |
| **Change** an existing component (prop rename, variant add, value change) with a deprecation shim, codemod, migration note, changeset | `ds-component-change` |
| Translate a built HTML prototype, or vectorize a raster, into Figma | `heyhi-design-bridge` |
| Repair located drift back into code or tokens | `heyhi-drift-repair` |
| Extract tokens FROM Figma into a config (opposite direction) | `ui-studio-onboard` |
| Read-only census of a library and the code crosswalk | `figma-library-census` |
| Decide the anatomy, the axes, an idiom conflict, or whether the component is any good | **the human** (this skill's named gates) |

This skill orchestrates the generator's Phase 3 and Figma's own `figma-use` and `figma-code-connect` skills; it never reimplements the Plugin API or the Code Connect format. It never opens the Sheerline area-7 foundation, either; it registers under it.

---

## Inputs, the one spec, and the through-line

Everything downstream is driven by **one component spec** (`schemas/component-spec.schema.json`, version 1.0). The spec is the human design decision (anatomy, axes) plus the retrieved facts (states, tokens); the skill consumes it, it never authors the design parts. A worked example is `references/chip.spec.json`; a spec whose VARIANT axis has no values is rejected by the schema, before any write. The fields:

- `name` (PascalCase): the Figma component-set name and the code component name.
- `level`: the atomic level (token / atom / molecule / organism / template), aligned with `ds-map.json`.
- `anatomy[]`: the named regions and their roles. A design decision (human-authored).
- `property_axes[]`: the property model. A design decision. VARIANT axes carry a non-empty `values` array.
- `states[]`: interaction states from an interaction-inventory sidecar, each with its `a11y_hook` and `keyboard` note.
- `slots[]`: optional SLOT content regions (empty when the component uses TEXT/INSTANCE_SWAP instead).
- `tokens{}`: a role to served-token-name map (semantic roles, never primitives, never literals).
- `framework`: the code-leg target (react for this arc; lit and angular are stubs).
- `code_connect{}`: `emit` (default true) and `publish` (default false, plan-gated).
- `gate{}`: the two named human gates (`spec_review`, `component_review`), null until signed.

**The through-line is the property axis.** One axis definition flows to three targets, so the Figma component, the code component, and the Code Connect template all express the same model. This table is the spine of the skill; every step below is an instance of it.

| Spec axis `type` | Figma leg (Plugin API) | Code leg (React) | Code Connect template |
|---|---|---|---|
| `VARIANT` | a variant axis; every value is a variant component (`combineAsVariants`), named `Name=value` | a string-union prop (`type X = 'a' \| 'b'`), one CSS modifier class per value | `getEnum('Name', { value: 'value', ... })`, **exhaustive** |
| `TEXT` | `addComponentProperty(name,'TEXT',default)`, linked via `componentPropertyReferences.characters` | a `string` prop rendered as the label text | `getString('Name')`, interpolated in quotes |
| `BOOLEAN` | `addComponentProperty(name,'BOOLEAN',default)`, linked via `componentPropertyReferences.visible` | a `boolean` prop toggling a region or a class | `getBoolean('Name')`, a conditional bare prop |
| `INSTANCE_SWAP` | `addComponentProperty(name,'INSTANCE_SWAP',compId)`, linked via `componentPropertyReferences.mainComponent` | a `ReactNode` prop (the slotted element) | `getInstanceSwap('Name')`, resolved via `executeTemplate()`, braces |
| `SLOT` | `component.createSlot()` (auto-wires a `SLOT` property) or `addComponentProperty(name,'SLOT','')` | the `children` prop | `getSlot('Name')`, interpolated as a snippet section |

## The references and their reading order

The SKILL.md is the procedure. The mechanism, templates, and probe records are loaded on demand (Earn the Room):

| File | Load when | Carries |
|---|---|---|
| `references/figma-leg.md` | before the Figma write (Step 3) | the by-reference map onto the generator's Phase 3, the probed slot step, the recorded traps this leg inherits |
| `references/code-leg-react.md` | before the code write (Step 4) | the React emitter template, the props-derivation rule, the CSS token-binding rule, and the worked example's actual typecheck output |
| `references/code-leg-adapters.md` | only when an engagement pulls Lit or Angular | the attribute and slot mapping for the two stubbed frameworks |
| `references/code-connect.md` | before the template write (Step 5) | the parserless template shape, the exhaustive-mapping rule, and the plan-gated publish |
| `references/probes.md` | before relying on any probed API | every Plugin API call this skill depends on, its probe script, and the observed result on the scratch file |
| `references/chip.spec.json` | as the spec exemplar | the worked-example spec that drove both legs |
| `schemas/component-spec.schema.json` | to validate a spec | the spec contract (version 1.0) |

## Step 0: Improvement hook check

Before running, retrieve any recurring corrections for design-system, component, Figma-generation, or token-fidelity work (`retrieve_design_corrections` if the design MCP is reachable, or the Sheerline `os/corrections/` registry). Fold a matching correction into the run. Skip silently if none. (On the instance's own proof run this surfaced `contrast-pairing-not-declared-safe`, `hardcoded-hex-bypasses-token`, and `token-missing-semantic-role`; all three were applied: semantic role tokens only, no colour literals, and the near-threshold accent pairing left as a human contrast call.)

## Step 1: Load context, the spec, the engine references, and the served contract

1. **The spec** the human brought, validated against `schemas/component-spec.schema.json`. Stop and report if it fails validation (a VARIANT axis with no values, a missing gate block, an unknown state name).
2. **The engine references (mandatory before any Figma write).** Load `heyhi-figma-ds-generator`'s SKILL.md and `references/generation-method.md` (Phase 3 mechanics, the pre-write gate, the state ledger, the recorded canvas traps) and Figma's own `figma-use` and `figma-code-connect` served skills. This skill assumes them; `references/figma-leg.md` points to them and never restates Phase 3.
3. **The served design-system contract, reached through the MCP boundary** (retrieved, never pasted, never read from a token file on disk; Invariant 4). `retrieve_design_context` for the component spec and the resolved token values; `retrieve_design_relationships` for the tokens a sibling component binds (the dependency order); `retrieve_design_examples` for the nearest existing component; `validate_output` to check the produced code against the served contract. The spec's `tokens{}` names roles; the concrete values and the real CSS variable names come from the served contract, never guessed from the token name.
4. **The states input.** The spec's `states[]` come from an `interaction-inventory` sidecar (`heyhi:interaction-inventory:sidecar:1.0`). The code leg honors the keyboard and role column from `heyhi-a11y-annotation`'s APG pattern map; it never invents an accessible name.
5. **The reuse-or-author check.** Cross-reference `figma-library-census`'s `ds-map.json` if present: if the component already exists in Figma or in code, this is a `ds-component-change` task, not an author task. Route out rather than duplicate.

Echo one line: `Component: <name> · level:<level> · axes:<count> · framework:<framework> · figma:<file_key|LOCAL->refuse> · code_connect:<emit|publish>`.

## Step 2: Spec review (named gate 1, before any write)

Print the resolved spec to chat and get approval before Phase 1 writes anything: the anatomy, the property axes with their values and defaults, the state list and its a11y hooks, the token role map, and the target framework. This is the Earn-the-Room approval artifact; it writes nothing. Surface, do not resolve, any place where the spec's design decisions are ambiguous (an axis with no clear default, a token role the contract is silent on, a state whose a11y hook is unstated). The `gate.spec_review` owner and date stay null until a human signs. Do not proceed to Step 3 on an unapproved spec.

## Step 3: The Figma leg (reuse the generator's Phase 3 by reference)

Build the component into the **library file**: a saved cloud file (the Wave 1 scratch library or a new scratch file created with `create_new_file`), never a production or client file. Run the generator's Phase 3 mechanics; do not copy them. Full detail in `references/figma-leg.md`.

1. **Local-file refusal and capability check first.** `use_figma` needs a saved cloud file. Refuse a `LOCAL_` key and ask for the saved `figma.com/design/<fileKey>` URL. Probe `use_figma` reachability with a read-only call before any write; the Figma MCP has no changelog, so treat the tool list as a hint.
2. **Discovery.** Read the file's variable collections and modes, the existing components (for INSTANCE_SWAP defaults, e.g. an icon), and the variant-naming convention already in the file (`State=Default` vs `state=default`); match it.
3. **Resolve token values before binding.** Read the resolved value of every token the spec names (following alias chains to the primitive), in the mode you will show. You will set each paint's base colour to the resolved value *before* binding the variable.
4. **Base component.** Build one base component with auto-layout and full variable bindings (fills, text colour, padding, gap, radius, all bound; no hardcoded values). Add each region from the anatomy as a child node.
5. **Component properties.** Add each non-variant axis as a component property *before* combining (`addComponentProperty` returns a string key; never guess it), and link it to its child node via `componentPropertyReferences` (`characters` for TEXT, `visible` for BOOLEAN, `mainComponent` for INSTANCE_SWAP). `INSTANCE_SWAP` for icons, never a variant per icon.
6. **The variant matrix.** Clone the base across the VARIANT axes; rename each `Prop=value`; for each clone, set its tone or size specifics by **clearing the fill, setting a fresh paint whose base colour is the resolved value, then binding** (this defeats the recorded rebind-renders-black trap on clones). `combineAsVariants`, then grid-lay-out (children stack at (0,0) until positioned). Cap the matrix at 30 combinations; a matrix near the cap is a scope call for the human.
7. **The probed slot step (new).** If the spec declares a slot, use `component.createSlot()` (it returns a `SLOT` node and auto-wires a `SLOT` property with reference field `slotContentId`). **Probe the slot API on the scratch file first and record the result in `references/probes.md`** (Arc rule 9): `createSlot`, the `'SLOT'` property, and whether `SlotSettings` is available. Slot content is set by appending children, never via `setProperties` (which throws on a slot property); slot nodes cannot use GRID layout.
8. **Verify.** `get_metadata` (design file, not `get_figjam`) plus `get_screenshot`; **screenshot the whole variant grid**, because a per-node binding audit alone reports the black-render trap as bound. Confirm the variant matrix, resolved bindings, and the property set. Save the screenshot to the gitignored proof folder.
9. **Transport discipline (every `use_figma` call), inherited from the generator:**
   - one focused section per call, at most about ten logical operations; batch independent imports in one `Promise.all`.
   - clear the 50,000-char per-call cap (split a dense unit; import a unique SVG once and reuse by instance).
   - never parallelize `use_figma`; Figma state mutations are strictly sequential.
   - font-preflight before any text write: resolve every `(family, style)` against `listAvailableFontsAsync()` and capture the exact style spelling.
   - create-only value writes on a reused canonical Variable; never clobber it.
   - a disk-backed state ledger for `{key -> id}`, re-read every turn; never hallucinate a node id (read it from the ledger or a prior return).

## Step 4: The code leg (React for this arc; Lit and Angular as named stubs)

Emit the code twin from the **same** spec, into the component package. Full detail and the emitter template in `references/code-leg-react.md`; the adapter stubs in `references/code-leg-adapters.md`.

1. **Match the package conventions first.** Read one existing component in the package before emitting; match its idioms (here: `React.forwardRef`, `displayName`, the `heyhi-<name> heyhi-<name>--<variant>` class pattern, types centralized in `types/tokens.ts`, a per-component `index.ts` barrel, and the package's `src/index.ts` export block).
2. **The props interface** is derived from the property axes per the through-line table: each VARIANT becomes a string union of its `values`, each TEXT a `string`, each BOOLEAN a `boolean`, each INSTANCE_SWAP a `ReactNode`, each SLOT the `children`. Add the interaction affordances the states imply (a removable control becomes a real `<button>` with `onRemove` and an `aria-label`).
3. **The CSS** binds every colour, radius, spacing, and duration to the served token names via `var(--token)`; no literals. One modifier class per VARIANT value. Interaction states are real CSS from the spec's `states[]`: `:hover`, `:focus-visible` for the ring (never `:focus`), `:active`, `:disabled`. The focus ring lives in the CSS, bound to the served focus token.
4. **Validate the rendered CSS.** Run `validate_output` (artifact_type `rendered_css`) on the emitted CSS and act on the findings. A true token bypass (a literal where a token exists) is fixed by binding the real served var. A finding that names a token the served CSS does not actually emit is a **served-surface conflict** (Step 6 gate), surfaced with provenance, not silently renamed to a var that would break the render.
5. **One story per variant** (CSF3 shape). If Storybook is not installed in the package, emit the one story file as a convention with local type shims and a note; do not install Storybook.
6. **Typecheck.** Run the package `typecheck`; the emitted component must pass. When the package carries pre-existing type errors in files this skill does not touch, typecheck the new component's closure in isolation and report both results honestly; never claim the whole package is clean when it is not.
7. **Framework order (D5).** Build only the React leg for this arc. Lit and Angular are named stubs (`references/code-leg-adapters.md`): the attribute and slot mapping, `@Input()` and `<ng-content select>`, deferred until an engagement pulls them.

## Accessibility: the states carry the a11y contract into the code leg

The spec's `states[]` are not decoration; each carries the accessible behavior the code leg must honor. This is where the interaction-inventory sidecar and `heyhi-a11y-annotation`'s APG pattern map pay off, and it is a place the skill drafts but never decides.

- **Interactive regions become real controls.** A removable affordance is a native `<button>` with an accessible name (`aria-label`), not a clickable `<span>`; the skill wires the element and the name pattern (`Remove {label}`), and flags any accessible name the spec leaves unstated as ⛔ NEEDS HUMAN, never inventing copy.
- **Focus is visible and keyboard-first.** Every focusable state maps to a CSS `:focus-visible` ring bound to the served focus token, never `:focus` (which fires on mouse click too). The keyboard column comes from the sidecar (`native <button>`, or a named APG pattern); the interaction itself is read from the APG map at build, never copied into the spec.
- **Disabled is programmatic.** A disabled state sets the real `disabled` attribute (or `aria-disabled` on a non-form container) so assistive tech reports it, not a visual dim alone; the remove control is neutralized (`pointer-events` off, `disabled`).
- **Color is never the only signal.** Tone communicates status, but the label text carries the meaning; the skill does not rely on tone alone (the served Badge guidance, applied to Chip).
- **What stays human.** Whether an alt text or accessible name is *correct*, and the reading-order intent, are `heyhi-a11y-annotation` calls at the design gate, surfaced here, decided there.

## Step 5: The Code Connect template (parserless, plan-gated)

Write the parserless template `Component.figma.ts` from the node ids Step 3 returned and the props Step 4 emitted. Full shape and the worked example in `references/code-connect.md`.

- **Always `.figma.ts` with `figma.code`.** Never a `.figma.tsx` file and never the parser-based connect form. The template default-exports `{ example: figma.code\`...\`, imports, id, metadata }`. Map each Figma property per the through-line table's last column: `getEnum` (VARIANT, exhaustive: every value mapped, or an unmapped value renders undefined), `getString` (TEXT), `getBoolean` (BOOLEAN), `getInstanceSwap` (INSTANCE_SWAP, resolved via `executeTemplate()` after a `type === 'INSTANCE'` check), `getSlot` (SLOT).
- **Interpolation.** Strings in quotes (`tone="${tone}"`); instance and slot sections in braces or directly inside the tagged template; booleans as conditionals (`${removable ? 'removable' : ''}`).
- **Publish is plan-gated.** Call `add_code_connect_map` only when `whoami` shows an **Organization or Enterprise** plan AND the plan allowance is set (`code_connect.publish: true`). **Record the `whoami` result.** On a Starter or Pro plan, emit the template to the repo and stop; do not call `add_code_connect_map`.
- **Hermetic seal.** The tracked template redacts the Figma file key and node id (they live in the gitignored proof record); a template is a reusable artifact, so the redaction costs nothing.

## Step 6: Verify and component review (named gate 2, after)

Verify both legs and hand off. The Figma canvas is screenshot-verified (Step 3); the code component typechecks (Step 4); the Code Connect template exists and its publish step is correctly gated (Step 5). Then print the **component review**: the rendered Figma grid, the code twin, and the one-to-one property mapping between them (the through-line table, instantiated), with every empty slot named. The `gate.component_review` owner and date stay null until a human signs. The craft critique is the human's.

## State ledger and idempotent re-run

- **Ledger.** Track `{key -> id}` for the Figma nodes on disk (the generator's `design-system-state-{RUN_ID}.json` convention) and re-read it every turn; a long build truncates context.
- **Figma re-run.** Find-or-create for the component and its properties; a re-run reuses, never duplicates a variant or a property. Create-only value writes on a reused canonical Variable.
- **Code re-run.** A re-run overwrites the emitted files deterministically (the same spec produces the same output) and never edits a sibling component.
- **Resume.** On a fresh session, read the ledger and re-derive node ids from a read-only `use_figma` before any further write.

## Registration (staged, promoted by the convergence pass)

This skill is staged registry-inert. It registers under Sheerline area 7 (Design Systems) and does not open the area-7 foundation. Every shared-anchor edit the promotion needs (both skill registries with verified `not_for` clauses, the coverage map, `CLAUDE.md`'s skills table, both project-state files, the roster) is listed in `NEXT-SESSION.md` for the convergence pass; this lane writes none of them (Arc rule 1). The drafted registry entry for both registries is `registry-entry.yaml`.

---

## Worked example (the instance's own proof run, the Chip)

The proof ran the whole loop on one spec (`references/chip.spec.json`), a **Chip**: the interactive, removable sibling of `Badge`. The served DS names Chip as Badge's interactive counterpart ("if the label is interactive, use Chip"), but the reference package carried only Badge, so this was a real promotion-execution case, not an invented component.

- **Figma leg**: a 10-variant component set (Tone default/success/warning/error/info x Size sm/md) with `Label` (TEXT), `Show Icon` and `Removable` (BOOLEAN), and `Leading Icon` (INSTANCE_SWAP to an existing icon), all fills, text, padding, and radius bound to variables. Screenshot-verified, all ten render.
- **Code leg**: `Chip.tsx` / `Chip.css` / `index.ts` / one story, `ChipTone` and `ChipSize` added to `types/tokens.ts`. The Chip closure typechecks with zero errors; the CSS binds every value to a served token.
- **Code Connect**: `Chip.figma.ts` (parserless, `figma.code`, exhaustive `getEnum` for Tone and Size, `getString` Label, `getBoolean` Removable and Show Icon, `getInstanceSwap` Leading Icon), emitted and **not published** (the plan is Pro).
- **What the proof surfaced for the human gate**: an idiom conflict (Figma's always-present INSTANCE_SWAP plus a `Show Icon` boolean vs the React optional `leadingIcon` prop) and a served-surface conflict (`validate_output` rejects `var(--font-line-height-none)` though the token exists in the built CSS). Neither was resolved by the skill.

The through-line table, instantiated for the Chip, is the join the Code Connect template encodes:

| Chip axis | Figma | React | Code Connect |
|---|---|---|---|
| Tone (VARIANT: default, success, warning, error, info) | 5 variants x Size | `tone?: ChipTone` union | `getEnum('Tone', {default:'default', ...})` (all 5) |
| Size (VARIANT: sm, md) | 2 variants x Tone | `size?: ChipSize` union | `getEnum('Size', {md:'md', sm:'sm'})` |
| Label (TEXT) | `Label` TEXT property | `label: string` | `getString('Label')` |
| Removable (BOOLEAN) | `Removable` BOOLEAN | `removable?: boolean` + `onRemove` | `getBoolean('Removable')` |
| Show Icon (BOOLEAN) | `Show Icon` BOOLEAN | (folds into optional `leadingIcon`) | `getBoolean('Show Icon')` gates the swap |
| Leading Icon (INSTANCE_SWAP) | `Leading Icon` INSTANCE_SWAP | `leadingIcon?: ReactNode` | `getInstanceSwap('Leading Icon')` via `executeTemplate()` |

## How this fits the forward-deployed loop

`ds-component-author` is the **execute** step of pattern promotion, not the discovery step:

- Upstream, `figma-library-census` classifies compositions and the Care cadence's ledger flips a repeating one to a candidate; a human promotes it out of `pattern-intake/`. Only then does this skill run.
- This skill authors the promoted component once, into both the library and the package, from one spec, so the Figma component and the code component share a model from birth (the drift this whole arc exists to prevent).
- Downstream, `ds-component-change` owns every later change to that component (a prop rename, a variant add, a value change) with a deprecation shim, codemod, and changeset. This skill never changes an existing component; it authors a new one.
- The Code Connect template it emits is the durable join: when a team reaches an Organization or Enterprise plan, publishing it wires the Figma instance to the code component with no re-derivation.
- Precedent: `heyhi-figma-ds-generator` proved the whole-system Figma write on the instance's own design system (2026-09-04); this skill narrows that proven write to one component and adds the code twin and the join.

---

## The human-gated slots (charter boundary, enumerated, non-empty)

| Judgment slot (stays human) | Trigger | The gate + provenance rule |
|---|---|---|
| **The anatomy and property axes** | Always (the spec input) | ⛔ **NEEDS HUMAN.** The human authors the anatomy and axes in the spec; the skill never invents a region or an axis. A spec missing them does not proceed. |
| **The spec review** (load-bearing) | Before any write | ⛔ **NEEDS HUMAN.** The resolved spec is printed and approved before Phase 1. `gate.spec_review` stays null until signed. Read-only; writes nothing. |
| **Framework-idiom conflicts** | A code idiom and the Figma structure genuinely disagree | ⛔ **NEEDS HUMAN.** Surface both sides with provenance (the Figma property vs the code convention); the human decides. Named, not silently reconciled. |
| **A served-surface conflict** | `validate_output` names a token the served CSS does not emit, or two served surfaces disagree | ⛔ **NEEDS HUMAN.** Surface the conflict (which surface says what); never rename to a var that breaks the render. |
| **The component review** | After both legs | ⛔ **NEEDS HUMAN.** The rendered Figma grid, the code twin, and the property mapping are printed; `gate.component_review` stays null until signed. |
| **The craft critique** | Always | ⛔ **NEEDS HUMAN.** Whether the component is any good stays human (the `dont-automate` line). The skill produces the substrate, never the grade. |

The generator's floor holds: when exactly one path is clearly correct from the source of truth, take it. The gate fires on genuine ambiguity, not on every mechanical choice.

---

## Provenance and labeling

Sheerline requires provenance on anything synthetic. In this skill:

- Anything the skill must infer to complete the structure (a default the spec omitted, a token role the contract is silent on) is **flagged as inferred**, never asserted as decided, and routed to the spec-review gate.
- Retrieved facts (token values, the nearest component spec) carry their source (the served instance), never a guessed value.
- The Code Connect template records the `whoami` plan and whether it was published, so a later reader knows the template is emitted-but-inert on a Pro plan rather than mistaking it for a live mapping.
- The proof record (gitignored) holds the real Figma file key, node ids, screenshots, and the raw `validate_output` and typecheck output, so the tracked artifacts stay hermetic while the evidence stays inspectable.

## The multi-framework contract (React built, Lit and Angular stubbed)

The spec's `framework` field selects the emitter. For this arc only React is built (D5); Lit and Angular are **named stubs**, not silent gaps:

- The through-line table is framework-neutral: the same axes drive every emitter, so a future Lit or Angular leg reads the same spec.
- `references/code-leg-adapters.md` names the mapping each stub will implement: for Lit, VARIANT and BOOLEAN axes become reflected attributes and a SLOT becomes a named `<slot>`; for Angular, axes become `@Input()`s and a SLOT becomes `<ng-content select>`.
- A request for Lit or Angular today stops at the stub and reports, rather than half-emitting an untested framework. The extension point is declared so the next author has a contract, not a blank page.

## What is explicitly out of scope

- **The design truth**: the anatomy, the axes, an idiom conflict, a served-surface conflict, whether the component is any good. Empty slots by construction.
- **A whole design system** (`heyhi-figma-ds-generator`). **A component change** with a shim, codemod, and changeset (`ds-component-change`). **Translating** a prototype or raster (`heyhi-design-bridge`). **Repairing** drift (`heyhi-drift-repair`). **Extracting** tokens from Figma (`ui-studio-onboard`). **A library census** (`figma-library-census`).
- **The Lit and Angular emitters** (named stubs only for this arc, D5).
- **Storybook installation** (emit the one story file as a convention; do not install Storybook).
- **Publishing Code Connect** on a Starter or Pro plan (emit the template regardless; publish only on Organization or Enterprise with the plan allowance set).
- **Editing a sibling component or fixing pre-existing package errors** (out of scope; report them, do not fold them into the component's change set).

---

## Common failure modes this skill guards against

Each was hit or anticipated on the instance's own proof run; the guard is baked into the steps above.

| Failure mode | The guard |
|---|---|
| A cloned variant renders its base colour black although the binding reads as present | Set each paint's base colour to the resolved token value *before* binding, on every clone (Step 3.6); screenshot the whole grid, never trust a per-node binding audit alone. |
| `resize()` on an auto-layout frame silently resets sizing to FIXED | Set `layoutSizing`/`HUG` after any resize (inherited generator trap). |
| Reaching for the familiar `.figma.tsx` / parser-based connect form from memory | The Code Connect leg is `.figma.ts` with `figma.code` only; a `.figma.tsx` output is rejected (Step 5). |
| A VARIANT `getEnum` that omits a value renders `undefined` | The mapping is exhaustive: every VARIANT value is listed (Step 5, through-line table). |
| `SlotSettings` assumed available because the developer docs list it | Probe first; it is NOT exposed in the `use_figma` sandbox (see `references/probes.md`), while `createSlot` and the `'SLOT'` property are. |
| Claiming the code leg is clean when the package has pre-existing errors | Typecheck the new component's closure in isolation and report both the isolated result and the full-package result honestly (Step 4.6). |
| A served-surface conflict silently "fixed" by renaming to a token that does not render | Surface it to the human gate; never bind a var the served CSS does not emit (Step 4.4). |
| The Figma file key leaking into a tracked Code Connect template | Redact the key and node id in the tracked template; the real values live in the gitignored proof record (Step 5). |
| A `LOCAL_` (unsaved) Figma file refused mid-write | Refuse up front and ask for the saved cloud URL; do not loop on the failing write (Step 3.1). |

## Definition of done

- The spec validates against `schemas/component-spec.schema.json` and the spec-review gate is printed (its sign-off stays the human's).
- The Figma component exists in a saved cloud library file with the full variant matrix and the TEXT / BOOLEAN / INSTANCE_SWAP properties bound, screenshot-verified.
- The slot step is probed on the scratch file and the result recorded in `references/probes.md`.
- The code twin typechecks (the component's closure at minimum, reported honestly against the package state) and its CSS binds to served tokens; `validate_output` was run and its findings acted on or surfaced.
- The parserless Code Connect template exists; `whoami` is recorded; `add_code_connect_map` was called only on an Organization or Enterprise plan.
- The component-review gate is printed with every empty slot named; no judgment slot is filled by the skill.
- The memory saves ran; the lane PR is open; the proof branch PR is open and unmerged.

## Exit Gate Required Headers (bottom-of-skill bracket)

This skill closes through Exit Gate Flavor A (`CLAUDE-SESSION-RULES.md § Exit Gate`). Before declaring done, confirm every header carries real content:

- `## Fixes Applied` (or the delivered component): the Figma component with its node ids and property set, the code twin with its files and typecheck result, and the Code Connect template with its plan-gating recorded.
- `## Smoke Test`: the Step 6 verification (Figma grid screenshot-verified; code component typechecks; template exists and is correctly plan-gated; the slot step probed and recorded).
- `## Next Session Prompt`: the empty slots still open (the spec-review and component-review sign-offs, any idiom or served-surface conflict, the craft critique), and the framework legs deferred past this arc.

If a judgment slot is filled by the skill rather than a human, the gate has **not** been satisfied.

---

*HeyHi Confidential. Sheerline area 7 (Design Systems), build class N. v0.1.0 staged 2026-09-07 for DISPATCH-08, Lane G of `plans/plan-sheerline-fdde-loop-2026-09-07.md`. Engine: `heyhi-figma-ds-generator` Phase 3 (by reference) plus Figma's `figma-use` and `figma-code-connect`. Live proof on the instance's own design system: recorded in the instance's engagement folder (Chip; proof PR #822). Boundary: the Sheerline judgment charter.*
