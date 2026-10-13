# The Figma leg: propose-only change log, and the OQ-1 lift proposal

*Reference for `ds-component-change`. How the skill describes a Figma-side change without writing it, the per-`change_type` proposed operation with its Plugin API grounding, the swap discipline, and the proposal (for the handoff) to lift `heyhi-drift-repair`'s OQ-1 so a confirmed Figma-canvas change can be applied through a shared gated path. Load on demand.*

---

## 1. Propose-only, always

The Figma leg **writes nothing**. It produces a change log of proposed edits with node ids, in the shape of the Design Intelligence Audit variant-rename log (a log of node ids, old names, and new names, filed in the handoff). A person applies the log, or a future gated increment does. The propose-only posture mirrors `heyhi-drift-repair`'s OQ-1: the Figma canvas is not a v1 write target there, and even a later increment is a proposed-only canvas edit.

The change log is the whole Figma output. The pre-flight (SKILL.md Step 7) asserts no `use_figma` call created, mutated, or deleted a node, variable, or style during the pass. If a demonstration of an operation is run to confirm an API shape, it runs on the Wave 1 scratch library only and is recorded as a demonstration in `probes.md`, never as the method's default.

## 2. The change-log shape

```
## Figma change log (PROPOSED, nothing written)
| Change | Node id | Proposed operation | Old -> New |
|--------|---------|--------------------|-----------|
| prop rename | 12:34 (COMPONENT_SET) | editComponentProperty('fullWidth', { name: 'block' }) | fullWidth -> block |
```

One row per proposed edit. The node id and the operation are precise enough that a person (or a later gated increment) can apply the log without re-deriving anything.

## 3. Per-`change_type` proposed operation (grounded)

Grounding is from the served `figma-use` references (`get_figma_skill`), except where noted. See `probes.md` for the read log.

| `change_type` | Proposed operation | Grounding |
|---|---|---|
| `variable_value` | `variable.setValueForMode(modeId, newValue)`, in the variable's **defining file**; if the code syntax moves, `variable.setVariableCodeSyntax(platform, syntax)` in that same file | `variable-patterns.md` (both are "executed in the file the variable is defined in") |
| `prop_rename` | `editComponentProperty(oldName, { name: newName })` on the property owner (the `COMPONENT_SET`, resolved by owner-narrowing: `componentPropertyDefinitions` throws on a variant component) | **docs-cited**: `editComponentProperty` is a documented Plugin API method not covered by the served reference; probe before any real use (`probes.md`) |
| `prop_type_change` | the property-type-appropriate edit (a VARIANT restructure, a BOOLEAN to INSTANCE_SWAP change), each logged with its node id | `component-patterns.md` (property model, INSTANCE_SWAP) |
| `variant_add` | add a variant `COMPONENT` with the new `Property=Value` name to the set, then re-lay-out (`combineAsVariants` layout rule: children stack at 0,0 until positioned) | `component-patterns.md` (combine + layout) |
| `variant_remove` | remove the variant `COMPONENT`; each downstream instance on it becomes a per-instance retarget row | `component-patterns.md` (instances, `swapComponent`) |

**Owner narrowing (a real trap).** `componentPropertyDefinitions` throws when read from a variant `COMPONENT`, including through optional chaining. Always resolve the property-owning node first: a `COMPONENT_SET` owns its definitions; a variant component delegates to its parent set. A `prop_rename` operates on the set, not on a variant.

## 4. The swap discipline

When a change retargets downstream instances (a removed variant, a replaced master), retarget **per instance** with `instance.swapComponent(newComponent)` or `instance.setProperties(...)`. Do not use Figma's native swap-libraries feature for a local master: it only matches assets that originate from another published library (Figma Help Center, Swap libraries), so a local master is silently skipped and the retarget quietly does nothing. This is the ground-truth correction in the plan; the SKILL.md states it once to forbid it for local masters.

## 5. Code Connect

A `prop_rename` (or a `variant` change) also changes any `Component.figma.ts` Code Connect template that maps the Figma component to code, so the mapping stays true after the rename. Publishing that mapping is gated on an Organization or Enterprise Figma plan. The `whoami` check (recorded in `probes.md`) shows every current plan is Starter or Pro, so Code Connect cannot be published now (plan D1). The updated template is therefore **emitted to the repo, not published**. The emit keeps the mapping correct on disk; the publish waits for a plan that allows it.

## 6. The OQ-1 lift proposal (for the handoff, not applied here)

`heyhi-drift-repair`'s OQ-1 defers the Figma-canvas write: "the canvas target is app-brokered, human-initiated, and its create-only Variable guard blocks a repair (a change to an existing Variable), structurally incompatible with an unattended auto-apply. Deferred behind a named gate; even in a later increment it is a proposed-only canvas edit."

This skill hits the same wall from the change side: it proposes Figma edits it cannot apply. The proposal (recorded in `NEXT-SESSION.md`, **not** applied to `heyhi-drift-repair`) is a **shared, gated, proposed-only canvas-apply increment** that would serve both skills:

- A single app-brokered, human-initiated apply path that takes a proposed change log (this skill's Step 3 output, or drift-repair's proposed diff) and applies it to the canvas behind a named human gate, one confirmed edit at a time.
- It is **proposed-only** even then: the human confirms each edit; nothing auto-applies. This respects drift-repair's OQ-1 wording ("even in a later increment it is a proposed-only canvas edit").
- The create-only Variable guard that blocks drift-repair's *repair* (a change to an existing Variable) is exactly what a `variable_value` change here needs lifted; the increment would allow a confirmed change to an existing Variable through the gated path, not through an unattended auto-apply.

Lifting OQ-1 is `heyhi-drift-repair`'s call and a separate build. This skill only names the shared need in the handoff. It does not edit `heyhi-drift-repair` (out of scope, plan OWNS Lane H).

---

*HeyHi Confidential. Reference for `ds-component-change` (Sheerline area 7). Figma leg and OQ-1 proposal; load on demand.*
