# ds-component-author: probe log

*Loaded before relying on any probed API (Arc rule 9: probe the Figma surface, never trust it). Every Plugin API call this skill depends on is probed in a scratch file first and the observed result recorded here. The Figma MCP has no changelog, so the surface must be probed, not read from docs.*

*classification: HeyHi Confidential*

---

## Environment recorded on the proof run (2026-09-07)

- **`whoami`**: plans = one Personal (starter) team and two Pro teams. **No Organization or Enterprise plan.** Consequence: Code Connect is not publishable (`add_code_connect_map` not called); the `.figma.ts` template is emitted regardless.
- **Scratch library**: the instance's own 2026-09-04 generated library (a Pro team, a saved cloud file). File key and node ids live only in the gitignored proof record. 4 collections, 157 variables, an `Icon/ChevronRight` component for INSTANCE_SWAP.

## Slot API (Plugin API 2026-06-10 "Slots GA"): the new surface this skill exercises

Probed on the scratch file with throwaway components, removed after. Each check isolated in its own try/catch so a throw does not short-circuit another flag.

| Call | Probe | Observed result |
|---|---|---|
| `component.createSlot()` | create a component, call `createSlot()`, read the returned node's `type` and the component's `componentPropertyDefinitions` | **AVAILABLE.** Returns a node of `type === 'SLOT'`; auto-wires a `SLOT` component property (key shape `Content#<n>:<n>`); the slot node's `componentPropertyReferences` carries `slotContentId`; `slot.resetSlot` is a function. |
| `'SLOT'` property type | via `createSlot()` (auto) and via `addComponentProperty('Content','SLOT','')` (manual) | **AVAILABLE** both ways. The manual call returns a key (e.g. `Content#20:1`). |
| `figma.SlotSettings` | `typeof figma.SlotSettings` | **NOT AVAILABLE.** Throws `TypeError: figma.SlotSettings: no such property 'SlotSettings' on the figma global object`. The `SlotSettings` type listed on the 2026-06-10 developer docs is not exposed in the `use_figma` sandbox. |

Probe script (throwaway, cleaned up):

```javascript
const r = {};
let probe = null;
try {
  probe = figma.createComponent();
  probe.name = "__slot_probe__";
  probe.layoutMode = "VERTICAL";
  probe.resize(120, 60);
  try {
    const slot = probe.createSlot();
    slot.name = "Content";
    const defs = probe.componentPropertyDefinitions;
    const slotKey = Object.keys(defs).find(k => defs[k].type === "SLOT");
    r.createSlot_available = true;
    r.slot_node_type = slot.type;                 // 'SLOT'
    r.slot_property_type = defs[slotKey].type;     // 'SLOT'
    r.slot_reference_field = Object.keys(slot.componentPropertyReferences || {})[0]; // 'slotContentId'
    r.resetSlot_is_function = (typeof slot.resetSlot === "function"); // true
  } catch (e) { r.createSlot_available = false; r.createSlot_error = String(e); }
  try { r.figma_SlotSettings = typeof figma.SlotSettings; }   // THROWS, isolated
  catch (e) { r.figma_SlotSettings = "THROWS"; r.figma_SlotSettings_error = String(e); }
} finally { try { if (probe) probe.remove(); } catch (e) {} }
return r;
```

**Trap recorded.** A first probe that read `typeof figma.SlotSettings` in the same try block as `createSlot()` reported `createSlot_available:false`, because the `SlotSettings` access threw and jumped to the catch. The returned fields (slot node type, property, references) proved createSlot had already succeeded. Isolate each check in its own try/catch, or a throwing later check falsifies an earlier flag (a false-clean instrument in reverse).

**Consequence for the skill.** Use `createSlot()` (or manual `addComponentProperty(...,'SLOT','')`) for slots; do not depend on `SlotSettings`. Slot content is set by appending children, never via `setProperties` (which throws on a slot property); slot nodes cannot use GRID layout.

## Component + variant API (reused from the generator's Phase 3, re-confirmed here)

| Call | Observed on the proof |
|---|---|
| `figma.createComponent()` + `combineAsVariants([...], page)` | Builds a `COMPONENT_SET`; children stack at (0,0) until positioned; variant names parsed from `Prop=value` into the VARIANT axes. |
| `addComponentProperty(name, type, default)` | Returns a string key (e.g. `Label#24:0`); add to each variant BEFORE combining; the set inherits them. |
| `componentPropertyReferences` | `characters` (TEXT), `visible` (BOOLEAN), `mainComponent` (INSTANCE_SWAP) link a property to a child node. |
| `componentPropertyDefinitions` | Throws when read from a variant `COMPONENT`; resolve to the parent `COMPONENT_SET` owner first. |
| `setBoundVariableForPaint(paint, 'color', variable)` | Binds a fill to a variable. **On a clone, set the paint's base colour to the resolved value first, then bind** (else it can render the base colour, e.g. black, though the binding reads as present, the 2026-09-04 trap). |
| `resize()` on an auto-layout frame | Resets sizing to FIXED; set `HUG`/`layoutSizing` after (the 2026-09-04 trap). |
| stroke-weight binding | Reads back as `strokeTop/Bottom/Left/RightWeight`; an audit on the `strokeWeight` key reports a false unbound (the 2026-09-04 trap). |

## Reachability

Before any write, a read-only `use_figma` (list pages, read collections) confirms the write path is reachable and the file is a saved cloud file. A `LOCAL_` file key is refused up front.

---

*HeyHi Confidential. Probe records for `ds-component-author`. Re-probe on any Figma MCP change; the surface has no changelog.*
