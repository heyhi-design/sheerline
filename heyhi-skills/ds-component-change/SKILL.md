---
name: ds-component-change
description: >-
  Take one confirmed change to an existing design-system component (a variable
  value, a prop rename, a prop type change, a variant added or removed) and land
  it as a single reviewable change set across Figma and code, with a
  backward-compatible path for the breaking case. Runs the mechanical work:
  classifies the change as patch / minor / breaking (a candidate the human
  confirms), writes a propose-only Figma change log with node ids, edits the
  prop or token in code and re-validates through validate_output for a
  non-breaking change, and for a breaking change emits the deprecation shim (old
  prop accepted and mapped, a development-only warning, an @deprecated JSDoc
  naming the replacement, an ESLint entry), a codemod that rewrites downstream
  call sites, a migration note, and a changeset bumping the major. React is
  built; Lit and Angular are named stubs. Triggers: "update this design system
  component from the spec", "breaking change with a migration path", "rename this
  prop across the system", "change a component's public API", "deprecate a prop",
  "add a variant to this component", "change a token value on a component".
  Produces a change set where the classification, the deprecation window, and the
  merge ship EMPTY behind a named human gate. NOT for repairing located drift or
  accessibility findings (use heyhi-drift-repair; that acts on unintended drift,
  this executes an intended spec change). NOT for authoring a new component from
  scratch (use ds-component-author; that creates, this changes an existing one).
  NOT for generating a whole design system into a Figma file (use
  heyhi-figma-ds-generator). NOT for discovering drift or auditing a system (use
  heyhi-design-intelligence-audit). NOT for building app surfaces from library
  instances (use app-to-figma).
version: "0.2.0"
updated: "2026-09-14"
status: "deployed 2026-09-08: heyhi-skills/ds-component-change/ (promoted at convergence pass 2 / DISPATCH-11). Built from plans/plan-sheerline-fdde-loop-2026-09-07.md (DISPATCH-09, Lane H); Wave 2, depends on convergence 1 (DISPATCH-06, landed). Sheerline area 7 (Design Systems), the 'change' verb. Worked example proved on the instance's own design system (heyhi-design-intelligence-tests @heyhi/components Button, a breaking fullWidth to block rename): proof branch ds-component-change-proof-2026-09-07, propose-first PR (see NEXT-SESSION.md). Figma leg is propose-only (writes nothing); the drift-repair OQ-1 canvas-write lift is proposed in the handoff, not applied. v0.2.0 (2026-09-14): added Step 5c dependency-ripple (W7/G12; CLOSE-03 disposition, owner-approved promotion of the staged skill-updates step) and its references/dependency-ripple.md, loaded in Step 1."
review_by: "2026-09-21"
classification: HeyHi Confidential
---

# DS Component Change

**Sheerline area 7 (Design Systems) · the "change" verb.** A design-system component already exists in Figma and in code, and its spec is changing: a token value moves, a prop is renamed, a prop's type changes, a variant is added or dropped. Today that change is landed by hand across two surfaces and however many downstream call sites, and the backward-compatible path (the shim, the codemod, the migration note, the version bump) is remembered or forgotten one change at a time. This skill takes the confirmed change spec and lands it as **one reviewable change set**: a propose-only Figma change log, the code edit, and for a breaking change the full deprecation kit, versioned together. It sits beside `ds-component-author` (which builds a new component) and downstream of the audit skills (which find drift). It never decides whether the change is worth making, how long the old surface lives, or when the set merges.

**The boundary this skill obeys (Sheerline, absolute).** The work lives inside the roughly forty percent that is safely automatable (`brand/dont-automate-this.md`). The judgment calls are on the other side, each a labeled empty slot behind a named human gate. Three calls stay human, always:

- **The classification.** patch / minor / breaking is proposed as a `classification_candidate` and confirmed by a person. A value change can be a structural break; an additive-looking variant can collide with a name or an implicit default. The rubric proposes; the person rules.
- **The deprecation window.** How long the old surface is accepted before removal is a policy decision about the team's tolerance for churn, not a mechanical one. The skill names the slot and leaves it blank.
- **The merge.** Both legs are propose-first. The Figma leg is a log a person applies; the code leg is a branch a person merges. Nothing lands on `main`.

A version of this skill that records a final classification on its own, sets the deprecation window, or merges the change set has exceeded its charter. Drafting the kit is mechanical; deciding to ship it is not.

> **This skill closes through the Exit Gate (`CLAUDE-SESSION-RULES.md § Exit Gate`).** See the bottom-of-skill bracket.

---

## Where this sits, and the one spec it reads

The forward-deployed loop reads an application, serves its design system, maps its intent, builds its Figma artifact, then validates, grades, repairs, and learns. This skill is the **change** verb in the Care cadence that keeps that loop current: when the served spec of a component moves, this lands the move on both surfaces. It runs after `ds-component-author` has built the component and after the audit skills have found any drift. It is not a detector and not a builder.

It reads the component's current state through the per-system instance, never a contract, token file, or DESIGN.md on disk as its spec (the Sheerline source-of-truth rule, plan Arc rule 4). The Figma node comes from the served library maps; the code source and call sites from the served application context or a passed repo path. The one input a human hands it directly is the change spec, because the intent to change a component is a decision the instance cannot serve.

---

## Routing: disambiguation with sibling skills

| If the task is… | Use |
|---|---|
| Landing a **confirmed change** to an existing component across Figma and code (the change verb) | **this skill** |
| **Repairing** located drift or accessibility findings (unintended drift, the act verb) | `heyhi-drift-repair` |
| **Authoring a new** component in Figma and code from a spec (the build verb) | `ds-component-author` |
| **Generating a whole** design system into a Figma file (the write verb) | `heyhi-figma-ds-generator` |
| **Discovering** drift, or auditing a system's health | `heyhi-design-intelligence-audit`, `validate_output` |
| Building app **surfaces** from library instances | `app-to-figma` |
| Deciding the classification, the deprecation window, or the merge | **the human** (this skill's named gates) |

The seam with `heyhi-drift-repair` is the source of the change. Drift-repair consumes a *finding* (something drifted from intent, unintended) and repairs it back. This skill consumes a *spec* (an intended change to the intent itself) and propagates it forward. The seam with `ds-component-author` is create-versus-change: the author writes a component that does not exist; this changes one that does, and owns the backward-compatibility path the author never needs.

---

## Step 0: Improvement hook check

Retrieve any recurring corrections for component-change, deprecation, or migration work (`retrieve_design_corrections` if the design MCP is reachable, or the Sheerline `sheerline/os/corrections/` registry). Fold a match into the pass. Skip silently if none.

## Step 1: Load context

1. The **change spec**: the confirmed intent, in the `schemas/change-spec.schema.json` shape. It carries `component`, `change_type` (one of `variable_value`, `prop_rename`, `prop_type_change`, `variant_add`, `variant_remove`), a `target`, the `from` and `to` (both for a rename, type, or value change; only the relevant side for a variant add or remove, per the schema), an optional `reason`, and `classification_candidate` left null on intake. Step 2 fills the candidate; a human confirms it. A spec that arrives with a final classification already asserted is treated as a candidate regardless and re-run through Step 2.
2. The component's **current Figma node**: the component or component set node id (and the variable node id for a `variable_value` change), read through the served library maps (`figma-library-map.json`, `figma-variable-map.json`) via the instance, never a file on disk. This skill reads the maps; it does not re-census the library (that is `figma-library-census`).
3. The component's **current code source**: the component file and its props interface, and the downstream call sites (a repo grep). The served application context (`retrieve_application_context`) locates the call sites when present; a passed repo path is the fallback.
4. `references/method.md`: THE method spine. The classification rubric, the change-set shape, the swap discipline, the re-validation rule. Read it before acting.
5. `references/shim-and-codemod-react.md`: the React templates (shim, codemod, migration note, changeset, ESLint entry) plus the worked example's actual artifacts. Read it to calibrate; do not copy its component names.
6. `references/figma-leg.md` (the propose-only Figma change-log method and the drift-repair OQ-1 lift proposal), `references/adapters.md` (the Lit and Angular stubs, named not built, per plan D5), and `references/probes.md` (the Plugin API grounding).
7. `references/dependency-ripple.md`: the ripple step — after this skill computes its own change (Step 4 or Step 5), exercise every dependent the graph returns before landing. Read it before Step 5c.

## Step 2: Classify the change (a candidate, never final)

Map `change_type` to a default `classification_candidate`. The rubric is mechanical; the confirmation is not.

| `change_type` | Default `classification_candidate` | Why | The human confirms because… |
|---|---|---|---|
| `variable_value` | **patch** | no public API changes | a value others compute against (a scale step, a documented constant) can be a structural break |
| `variant_add` | **minor** | additive; existing variants keep working | a new variant can collide with a name or shift an implicit default |
| `prop_add` (optional) | **minor** | additive | a new optional prop is safe; a new required prop is breaking |
| `enum_value_add` | **minor** | widens a union | downstream exhaustive switches may not handle the new case |
| `prop_rename` | **breaking** | removes the old name | rarely anything but breaking, yet the window is still a human call |
| `prop_type_change` (incompatible) | **breaking** | old call sites may not typecheck | a widening change can be minor; a person rules |
| `prop_remove` / `variant_remove` | **breaking** | removes public surface | downstream usage must be migrated first |
| `enum_value_remove` | **breaking** | narrows a union | removes a value consumers may pass |
| `default_change` | **breaking** (candidate) | changing default behavior can break callers relying on the old default | a person rules whether the old default was load-bearing |

**Record the result as `classification_candidate`, never as a final `classification`.** The field name is the discipline. Nothing downstream reads `classification_candidate` as an approval, and the change set does not merge on it. The human confirmation step (the classification review gate) is where a candidate becomes the decision, and it is the only place a decision is recorded.

**Precedence.** When two rows could apply (a `prop_type_change` that also renames, say), take the more severe candidate. Breaking beats minor beats patch. A person may soften it at the gate; the skill never softens it on its own.

**Worked candidate.** For the worked example, `change_type: prop_rename`, `from: fullWidth`, `to: block`: the rubric proposes **breaking** (the old name is removed from the public surface). The candidate does not assert that the change is right, or that it must ship this quarter, or how long `fullWidth` is accepted. Those are the three human slots. What the candidate does assert is that *if* this ships, it ships with the breaking kit (Step 5), not as a quiet patch.

**A candidate the human softens.** A `prop_type_change` from `size?: 'sm' | 'md' | 'lg'` to `size?: string` *widens* the type: every old call site still typechecks. The rubric proposes breaking (its default for `prop_type_change`), and here the human softens it to minor at the gate, because widening breaks no caller. The skill proposes the safe, more severe candidate and lets the person who can see it is a widening soften it. It never widens-and-softens on its own.

## The change-set shape

Whatever the classification, the outputs land as **one reviewable set**, so a reviewer sees the whole change at once rather than a Figma edit here and a code edit there that drift apart. The set is:

- the **Figma change log** (proposed node edits with ids; nothing written),
- the **code diff** (the prop or token edit),
- and, for a breaking change, the **shim**, the **codemod**, the **migration note**, the **major changeset**, and the **ESLint entry**.

The set is a propose-first pull request plus a Figma log. The version bump on the changeset and the deprecation kit belong to the same set as the code diff, so the reviewer cannot approve the breaking edit without also seeing its migration path.

The two legs describe the *same* change on two surfaces, so their contents must agree. The node id in the Figma change log and the prop in the code diff name the same rename; a reviewer can check one against the other. A change set whose Figma log and code diff disagree (a rename proposed in Figma but a different prop touched in code) is a defect the gate should catch, and the pre-flight in Step 7 asserts the two legs are the same change.

## Step 3: The Figma leg (propose-only, always)

The Figma leg **writes nothing**. It produces a change log of the proposed edits with node ids, in the shape of the Design Intelligence Audit variant-rename log (`heyhi-design-intelligence-audit` variant-naming phase: a log with node ids, old, and new). A person applies it, or a later increment applies it behind a gate. See `references/figma-leg.md` for the per-`change_type` proposed operation and its API grounding.

| `change_type` | Proposed Figma operation (logged, not run) | On the node |
|---|---|---|
| `variable_value` | `variable.setValueForMode(modeId, newValue)`, in the variable's **defining file**; if the code syntax moves, `setVariableCodeSyntax` in that same file | the variable node |
| `prop_rename` | `editComponentProperty(oldName, { name: newName })` on the property owner (the `COMPONENT_SET`, resolved by owner-narrowing) | the component set |
| `prop_type_change` | the property-type-appropriate edit (a VARIANT restructure, a BOOLEAN to INSTANCE_SWAP change), each logged with its node id | the component set |
| `variant_add` | add a variant `COMPONENT` with the new `Property=Value` name, then re-lay-out the set | the component set |
| `variant_remove` | remove the variant `COMPONENT`; every downstream instance on it is a retarget proposal | the component set and each instance |

**The swap discipline.** When a change retargets downstream instances (a removed variant, a replaced master), each instance is retargeted per-instance with `instance.swapComponent(newComponent)` or `instance.setProperties(...)`. Do not reach for Figma's native swap libraries feature when the source is a local master: it only matches assets that originate from another published library, so a local master is silently skipped and the retarget quietly does nothing. This SKILL.md names that feature only here, and only to forbid it for local masters.

**Relationship to drift-repair OQ-1.** The propose-only posture mirrors `heyhi-drift-repair`'s OQ-1 (the Figma canvas is not a v1 write target there; even a later increment is a proposed-only canvas edit). This skill does not apply the OQ-1 lift. It proposes the lift in `NEXT-SESSION.md`: a shared, gated increment that would let both skills apply a confirmed Figma-canvas change through the same app-brokered, human-initiated path. If a scratch-file demonstration of an operation is run, it runs on the Wave 1 scratch library only and is recorded as a demonstration in `references/probes.md`, never as the method's default.

## Step 4: The code leg, non-breaking change (patch / minor)

For a `classification_candidate` of patch or minor:

1. **Edit at the source.** A `variable_value` change edits the single token definition (the DTCG source), not N call sites. An additive prop or variant adds the surface without touching existing callers. One edit, one source of truth.
2. **Typecheck.** Run the package typecheck (`npm run typecheck` or the repo's equivalent). A change that does not typecheck is not landed.
3. **Re-validate.** Run the instance's `validate_output` on the component's real CSS. Re-validation checks conformance, not intent: it confirms the change did not introduce drift (an off-scale value, a broken token reference), not that the change is the right one. That is the human's call at the gate.

A minor change that turns out to need a call-site migration (an `enum_value_add` that breaks an exhaustive switch, say) is re-classified as breaking and routed to Step 5. The candidate is a starting point, not a lock.

**Worked non-breaking.** A `variable_value` change (a spacing token moving from `12px` to `10px`) is a candidate **patch**: no prop or variant surface changes. The Figma leg logs one proposed `setValueForMode` on the token node in its defining file. The code leg edits the single DTCG token definition, typechecks, and re-validates the components that bind the token. If the human confirms at the gate that the token is a documented scale step other tokens alias against, the candidate is upgraded to breaking there and the value change ships with a migration note for the aliased consumers. The rubric proposes patch; the person who knows the token's blast radius decides.

## Step 5: The code leg, breaking change (major)

For a `classification_candidate` of breaking, emit the backward-compatible kit as one set. The templates and a full worked example are in `references/shim-and-codemod-react.md`.

1. **Deprecation shim.** The old surface keeps working. The old prop is accepted and mapped to the new one (the new value wins when both are passed). A one-time, development-only warning names the replacement and the codemod, and is suppressed in production. An `@deprecated` JSDoc on the old prop names the replacement. This generalizes the Design Intelligence Audit's Phase 3-to-4 gate (a whole-component `@deprecated`) down to a single prop. No consumer breaks on upgrade to the shim version.
2. **ESLint entry.** A rule flags the deprecated usage, paired with the JSDoc so the enforcement and the documentation agree. A deprecated *prop* is enforced with `no-restricted-syntax` on the JSX attribute; a deprecated *import* (a whole component) with `no-restricted-imports` (the DI-audit gate's named rule); `eslint-plugin-deprecation` reads the JSDoc directly when the plugin is available. Pick the rule that matches what is deprecated.
3. **Codemod.** A jscodeshift (or ts-morph) transform rewrites downstream call sites automatically, scoped to the component and alias-aware (so it does not rewrite a same-named symbol imported from somewhere else), with a fixture pair proving it rewrites every call-site form (shorthand, explicit value, expression) and misses nothing. Run it against a fixture and the real call sites; paste the before-and-after diff into the reference. A codemod that touches a same-named element from another source, or that misses a form, is a defect, not a landing.
4. **Migration note.** What changed, the human's stated reason, the backward-compatibility behavior, the deprecation window (the human's call), and the codemod command. It is written for the consumer, so it names the exact command and the exact removal version.
5. **Changeset.** A Changesets entry bumping the **major**, naming the change and the codemod. The major bump is the machine-readable statement that this is breaking, tied to the same set as the shim that keeps it from breaking anyone yet.
6. **Code Connect.** If the component carries a `Component.figma.ts` Code Connect template, the rename is reflected there too, so the design-to-code mapping stays true. Publishing that mapping is gated on an Organization or Enterprise Figma plan (every current plan is Starter or Pro; `references/probes.md` records the `whoami` check), so the updated template is **emitted to the repo, not published** (plan D1). The emit is not the publish.

**The shim and the codemod are a pair.** The shim keeps the old surface working so no consumer breaks on upgrade; the codemod removes the old usage so the shim is not permanent debt. A shim without a codemod is a deprecation that never completes: the old prop lives forever because nothing migrates the call sites, and the removal at the end of the window has nothing to remove against. Ship both, or the window never closes.

Everything above lands on a branch as one change set. Nothing merges (Step 6).

## Step 5c: Dependency ripple (exercise every dependent)

After the code leg computes its change (Step 4 or Step 5), exercise every dependent of the changed node before landing. Root `retrieve_design_relationships(query_type="impact_analysis", ...)` at the semantically-changed node — the changed **token** for a `variable_value` change, not the component — `max_hops=4` (full-within-cap, narrowed by a dependent-count cap, never widened from a shallow default). Re-run the same re-validation the change leg runs (typecheck + `validate_output`) on each dependent, and add a three-state row to the change set: `exercised: pass` / `exercised: FAIL → finding` / `NOT exercised (beyond horizon / cost cap): N`. A failed dependent is a **hard finding** in the reversible-deviation-record shape — never a silent miss, never an auto-revert; the human gate is Step 6's existing review. Full method: `references/dependency-ripple.md`.

## Step 6: Land as one reviewable change set

The change set is one unit: the Figma change log (node ids, proposed edits), the code diff, and for a breaking change the shim, codemod, migration note, changeset, and ESLint entry. It lands on a branch as a propose-first pull request. **No leg merges; nothing lands on `main` anywhere.** The Figma leg is a log, not a write. The code leg is a branch, not a merge. The reviewer at the gate sees the classification candidate, the migration path, and the version bump in one place, and signs (or does not).

## Step 7: Pre-flight verification

Confirm before declaring done:

1. **Classification is a candidate.** The change set carries `classification_candidate`, never a final `classification`; the classification review gate is present and unsigned.
2. **Figma leg wrote nothing.** The Figma output is a change log with node ids. Assert no `use_figma` call in this pass created, mutated, or deleted a node, variable, or style (a scratch demonstration, if any, is labeled a demonstration on the scratch library).
3. **Non-breaking change re-validated.** A patch or minor change typechecks and clears `validate_output`; a change that fails either is not landed.
4. **Breaking change is complete and reversible.** The shim accepts the old surface and maps it; the `@deprecated` JSDoc names the replacement; the ESLint entry is present; the codemod rewrites a fixture with every call-site form and misses none (diff pasted); the migration note and the major changeset exist.
5. **The swap discipline holds.** Any downstream retarget is per-instance; the native swap-libraries feature is not used for a local master.
6. **Nothing merged.** Both legs are propose-first; no change is on `main`.
7. **The deprecation window and the merge are empty.** The window and the merge decision are the human's, unrecorded until signed.

## Output structure

```
# DS Component Change: [component] · [change_type]
Spec: [from] -> [to]        Classification (candidate): [patch|minor|breaking]        Run: [date]

## Figma change log (PROPOSED, nothing written)
| Change | Node id | Proposed operation | Old -> New |
|--------|---------|--------------------|-----------|
| prop rename | 12:34 (COMPONENT_SET) | editComponentProperty('fullWidth', { name: 'block' }) | fullWidth -> block |

## Code change set (branch: <branch>, PROPOSE-FIRST, not merged)
- Shim: [path] (old prop accepted, mapped, @deprecated JSDoc, dev-only warning)
- ESLint entry: [path] (no-restricted-syntax | no-restricted-imports)
- Codemod: [path] ([N] call sites rewritten in the fixture; diff in references/)
- Migration note: [path]
- Changeset: [path] (major)
- Code Connect template: [emitted | n/a] (publish gated: Org/Enterprise; D1)
- typecheck: [pass] · validate_output: [valid: true | n/a for breaking]

## ⛔ Classification review: NEEDS HUMAN
This slot is intentionally a candidate. patch / minor / breaking is confirmed by a
person, because a value change can be a structural break and an additive change can collide.
   Confirmed classification: ____________________

## ⛔ Deprecation window: NEEDS HUMAN
How long the old surface is accepted before removal is a policy decision.
   Window (accepted through / removed in): ____________________

## ⛔ Merge: NEEDS HUMAN
Both legs are propose-first. The Figma log is applied by a person; the code PR is merged by a person.
   Reviewer: ____________________  Date: ______
No classification, window, or merge is recorded until this line is signed.
```

---

## What is explicitly out of scope

- **The classification, the deprecation window, and the merge.** Empty by construction. The skill proposes a candidate classification and lays out the kit; the human decides all three.
- **Writing to any Figma file.** The Figma leg is a propose-only log. The canvas-write increment (the drift-repair OQ-1 lift) is proposed in the handoff, not applied here.
- **Repairing drift.** Unintended drift is `heyhi-drift-repair`'s job; this skill executes an intended spec change. It never re-runs a detector.
- **Authoring a new component.** `ds-component-author` creates; this changes. The two share the change-set discipline and nothing else.
- **The Lit and Angular emitters.** Named stubs only for this arc (plan D5, React only). The extension points are in `references/adapters.md`.
- **Merging anything.** No leg lands on `main`. The proof branch and the change-set branch are both propose-first.

---

## Exit Gate Required Headers (bottom-of-skill bracket)

This skill closes through Exit Gate Flavor A (`CLAUDE-SESSION-RULES.md § Exit Gate`). Before declaring done, confirm every required header holds real content:

- `## Fixes Applied` (the change set: the Figma change log and the code change-set summary, with paths)
- `## Smoke Test` (the Step 7 pre-flight checks, pasted)
- `## Next Session Prompt` (what the human still needs to confirm: the classification, the window, the merge)

If a final `classification` was recorded without a human signature, if any Figma node was written, if a breaking change shipped without the shim / codemod / migration note / major changeset, or if any leg merged to `main`, the gate has **not** been satisfied.

---

*HeyHi Confidential. Sheerline area 7 (Design Systems), the change verb. Staged 2026-09-07 (v0.1.0), DISPATCH-09 / Lane H of `plans/plan-sheerline-fdde-loop-2026-09-07.md`. Sibling of `ds-component-author` (create) and `heyhi-drift-repair` (repair). Worked example: a breaking `fullWidth` to `block` rename on `@heyhi/components` Button, proof branch `ds-component-change-proof-2026-09-07` (propose-first). Figma leg propose-only; the drift-repair OQ-1 canvas-write lift is proposed in the handoff.*
