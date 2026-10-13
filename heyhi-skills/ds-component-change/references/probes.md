# Plugin API grounding (probe log)

*Reference for `ds-component-change`. Which Plugin API calls the Figma leg cites, where each is grounded, and the plan-tier check. This skill's Figma leg is **propose-only** and writes nothing, so no live write was run; the calls are grounded in the served `figma-use` references (read through `get_figma_skill` on 2026-09-07) and, for one call, the Figma developer docs. A future gated canvas-apply increment (the OQ-1 lift) would probe the write calls on the Wave 1 scratch library before applying. Load on demand.*

Arc rule 9 requires a probe before *building on* a Plugin API call. This lane builds on no call at write time (it logs proposed edits and writes nothing), so grounding is by reference read, with the one docs-only call flagged for a live probe before any real apply.

---

## Grounded in the served references (read 2026-09-07)

| Call | Source (served) | Observed shape / rule | Used for |
|---|---|---|---|
| `variable.setValueForMode(modeId, value)` | `figma-use/references/variable-patterns.md` | value is a primitive, RGBA, or `{type:'VARIABLE_ALIAS', id}`; run in the file the variable is defined in | `variable_value` |
| `variable.setVariableCodeSyntax(platform, syntax)` | `variable-patterns.md` | `'WEB' | 'ANDROID' | 'iOS'`; "must be executed in the file the variable is defined in" | code-syntax move on a `variable_value` |
| `combineAsVariants(components, parent)` + layout | `figma-use/references/component-patterns.md` | variant names use `Property=Value`; children stack at (0,0) until positioned | `variant_add` |
| `instance.swapComponent(newComponent)` | `component-patterns.md` (instances) | per-instance retarget | `variant_remove` retarget |
| `instance.setProperties({...})` | `component-patterns.md` | sets VARIANT / TEXT / BOOLEAN / INSTANCE_SWAP; **throws on a SLOT property** | prop-value retarget |
| `componentPropertyDefinitions` owner narrowing | `component-patterns.md` | **throws** when read from a variant `COMPONENT`, including through optional chaining; resolve the `COMPONENT_SET` owner first | resolving the property owner for `prop_rename` |

## Cited from the developer docs, not the served reference (probe before any real use)

| Call | Source | Status |
|---|---|---|
| `component.editComponentProperty(oldName, { name, defaultValue?, preferredValues? })` | Figma Plugin API developer docs | **Docs-cited; not covered by the served `figma-use` reference.** The Figma leg only *logs* it as the proposed `prop_rename` operation. Before any real apply (the OQ-1 lift increment), probe it in a scratch file on the Wave 1 scratch library, exactly as the plan quarantines `SlotSettings` for Lane G. Not probed in this lane (no Figma write). |

## Plan tier (`whoami`, 2026-09-07)

`whoami` on the Figma MCP shows every accessible plan is **Starter or Pro**; there is no Organization or Enterprise plan. Consequence for this skill: **Code Connect cannot be published** (Org/Enterprise only), so a `Component.figma.ts` template updated by a rename is emitted to the repo, not published (plan D1). Team and file keys are deliberately not recorded here (hermetic seal); only the tier fact is.

## Posture

- **No live write in this lane.** The Figma leg produces a change log; the pre-flight asserts no node, variable, or style was created, mutated, or deleted.
- **No scratch demonstration was required** for the propose-only method. If one is ever run to confirm an API shape, it runs on the Wave 1 scratch library (key in the gitignored proof record only, never here) and is labeled a demonstration, not the default.
- **The write calls above are the OQ-1 increment's to probe**, one confirmed edit at a time behind the shared gated path proposed in `figma-leg.md § 6` and `NEXT-SESSION.md`.

---

*HeyHi Confidential. Reference for `ds-component-change` (Sheerline area 7). Probe log; load on demand.*
