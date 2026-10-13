# ds-component-author: the Figma leg

*Loaded before the Figma write (Step 3). This leg REUSES `heyhi-figma-ds-generator`'s Phase 3 by reference; it does not restate or copy the Plugin-API mechanics. The only new material here is the slot step and the component-scoped narrowing. Read the generator's method spine first.*

*classification: HeyHi Confidential*

---

## Reuse by reference, do not copy

The component build is the generator's Phase 3, scoped to one component instead of a whole library. Load and follow, do not paste:

- `heyhi-skills/heyhi-figma-ds-generator/references/generation-method.md` § 3 (the phase order), § 5.2 (variables, styles, components), and § 4 (the transport constraints and the three recorded canvas traps).
- Figma's served `figma-use` skill, `references/component-patterns.md` (creating components, `combineAsVariants`, laying out variants, `addComponentProperty`, linking via `componentPropertyReferences`, INSTANCE_SWAP to avoid variant explosion, and the slot API) and `references/variable-patterns.md` (`setBoundVariableForPaint`, `setBoundVariable`).

This skill supplies only the component-scoped overlay: the pre-write spec gate, the slot step, and the join to the code leg. It never reimplements the Plugin API. The smoke test greps this folder for any copied Phase 3 script longer than ten lines and expects none: the mechanics live in the generator; the spec-to-build mapping lives in the SKILL.md through-line table.

## What the generator's Phase 3 gives this leg (summary, not a copy)

- Base component with auto-layout and full variable bindings, no hardcoded fills, strokes, spacing, or radius.
- Variant sets via `combineAsVariants`, then grid-laid-out (children stack at (0,0) until positioned); the 30-combination cap.
- Component properties (`TEXT` / `BOOLEAN` / `INSTANCE_SWAP`) added to each variant before combining and linked to child nodes; `INSTANCE_SWAP` for icons, never a variant per icon.
- The three recorded canvas traps: the rebind-renders-black trap on clones (clear the fill, set the resolved base colour, then bind), `resize()` resetting sizing to FIXED, and stroke-weight bindings reading back per side.
- The transport discipline (one section per call, the 50k cap, never parallelize, font preflight, create-only writes, the disk ledger, never hallucinate a node id).

## The component-scoped narrowing

The generator runs Phase 0 through Phase 4 for a whole system. This leg runs only the parts a single component needs:

1. Capability check and local-file refusal (Step 3.1).
2. Discovery scoped to what this component binds: the variable collections and modes it references, the existing components it swaps in (an icon), and the file's variant-naming convention.
3. Resolve the token values the spec names (follow alias chains to the primitive), in the mode you will show, so clone paints get a correct base colour before binding.
4. Build the base, add the properties, clone the matrix, combine, position, verify. One component, one page.

## The slot step (new; not in the generator)

Slots reached GA in the 2026-06-10 Plugin API. This leg exercises them; `references/probes.md` carries the observed results. Follow the probe, not the docs.

- **Prefer `component.createSlot()`.** It returns a `SLOT` node and auto-wires a `SLOT` component property (reference field `slotContentId`). No manual wiring.
- **Or manual:** `const key = component.addComponentProperty('Content', 'SLOT', '')`, then a frame with `frame.componentPropertyReferences = { slotContentId: key }`.
- **Restrictions (from the probe and the served reference):** slot content is set by appending children in an instance, never via `setProperties` (which throws on a slot property); slot nodes cannot use GRID layout; a frame nested inside another slot cannot itself be bound to a slot property.
- **`SlotSettings` is NOT available** in the `use_figma` sandbox (probed; accessing `figma.SlotSettings` throws). Do not depend on it.
- **When the component uses a slot vs a TEXT/INSTANCE_SWAP:** a slot is for arbitrary nested content (the React `children`); a TEXT property is for a string label; an INSTANCE_SWAP is for a swappable fixed instance (an icon). The Chip worked example uses a TEXT label, so it does not carry a slot; the slot step is still probed and documented as a capability.

## Verify (screenshot the grid, not just the audit)

`get_metadata` (design file) plus `get_screenshot` on the whole component set. **Screenshot the grid**, because the rebind-renders-black trap passes a per-node binding audit. Save the screenshot to the gitignored proof folder. Confirm: the variant matrix is complete, every binding resolves, and the property set matches the spec's axes.

## Where the file goes

A saved cloud library file only: the Wave 1 scratch library, or a new scratch file created with `create_new_file` (load `figma-create-new-file` first). Never a production or client file. The file key stays out of every tracked file (hermetic seal); it lives in the gitignored proof record.

---

*HeyHi Confidential. The Figma leg of `ds-component-author`. Engine: `heyhi-figma-ds-generator` Phase 3 (by reference) + Figma's `figma-use`. Probe records: `references/probes.md`.*
