# app-to-figma: build method

*The method spine. Loaded on demand, not at session start (Earn the Room). SKILL.md is the procedure; this file carries the mechanism, the input/output contract, the exact per-section call order, the recorded Plugin-API traps, and the worked build from the instance's own proof run.*

*classification: HeyHi Confidential*

---

## 1. The mechanism

The write path is `use_figma`, and the skill orchestrates Figma's own two skills: `figma-generate-design` (the WHAT and in WHAT ORDER a screen is built) over `figma-use` (the Plugin-API HOW). Both load before any write. This skill supplies only the Sheerline overlay: the manifest-and-map resolution, the § 9 human-gate and provenance boundary, the anti-minting invariant, and the Exit Gate close. It never re-implements the Plugin API.

**Images do not depend on `generate_figma_design` here.** That MCP tool (a web-view capture) is absent from the live callable manifest (2026-09-01 and 2026-09-07), and it is not needed: image import has three working paths (Step 5), verified 2026-09-07 on the Pro scratch file. The primary path is `upload_assets` (POST image bytes to a single-use URL; the image is set as a fill on a target node and an `imageHash` is returned); `download_assets` then `upload_assets` covers a cross-Figma-file image; and `figma.createImage(bytes)` handles a small inline base64 image within the 50k `use_figma` cap. `generate_figma_design` is retained only as an optional pixel-reference capture if a probe ever finds it callable. Screens are always built by `use_figma` from imported library instances, so they stay linked and updatable; images are fills, never screens.

**Runtime-verify, do not trust the tool list.** The Figma MCP has no changelog. Phase 0 confirms `use_figma` is reachable and re-runs the §8 import-by-key probe on a new plan before building (`references/probes.md`).

---

## 2. The input contract

### 2.1 The surface list (`app-manifest.json`, plan § 3.3)

Retrieved through `retrieve_application_context(scope: manifest)` when the instance serves it, passed by path otherwise, or hand-written in the same shape until `app-recon` (Lane C) lands. The fields this skill reads:

| Field | Used for |
|---|---|
| `surfaces[].id` | wrapper name, ledger key |
| `surfaces[].route` / `container_dir` / `entry_component` | which source view a surface is |
| `surfaces[].breakpoints[]` | the wrapper width |
| `surfaces[].theme` | the mode set with `setExplicitVariableModeForCollection` |
| `surfaces[].components_used[]` (`name`, `props_passed{}`, `defaults{}`, `source`) | the component key to import and the props to set |
| `surfaces[].copy[]` (`text`, `role`, `file`, `line`) | the TEXT overrides |
| `surfaces[].endpoints[]` | context only in this skill (data binding is the prototype leg, not the Figma leg) |

### 2.2 The library and variable maps (plan § 3.3, emitted by `figma-library-census`, Lane A)

Retrieved through `retrieve_application_context(scope: ds-map)` when served, passed by path otherwise. This skill reads them; it does not build them.

- **`figma-library-map.json`** `components[]`: `name`, `key`, `library_key`, `type` (COMPONENT / COMPONENT_SET), `properties[]` (`name`, `type` in TEXT/BOOLEAN/VARIANT/INSTANCE_SWAP/SLOT, `values[]`), `default_variant`; `styles[]`: `name`, `key`, `kind` (text / effect).
- **`figma-variable-map.json`** `collections[]`: `key`, `name`, `modes[]`, `variables[]` (`name`, `key`, `resolved_type`, `code_syntax`).
- **`ds-map.json`** `rows[]`: `code_component`, `figma_key`, `token_refs[]`, `coverage`, `level`, `level_confirmed`. Used to name a local pattern and to know a composition's level.

### 2.3 The join (the resolution table, built at the gate)

For each `components_used[]` entry: `name` joins to a `figma-library-map.json` row for the `figma_key`; `props_passed{}` selects the variant and sets TEXT/BOOLEAN/INSTANCE_SWAP; `defaults{}` fills unspecified props. Each bound value joins to a `figma-variable-map.json` row for the variable `key`. Each text run joins to a `styles[]` row of `kind: text`. An entry with no exact row is **unresolved**, surfaced for the human's reuse / wrap / local-pattern ruling, never silently matched.

---

## 3. The output contract (real Figma constructs, nothing minted)

- **Per surface:** one wrapper auto-layout frame, sized to the breakpoint, named from `surfaces[].id`.
- **Per section:** an auto-layout frame whose fills/spacing/radii are **bound to imported variables**, whose text carries **imported text styles**, holding **instances of imported component sets** with their props set.
- **Local pattern components:** only where the library has no match and the human ruled "local pattern"; a component (never a variable, style, or token), plus a ledger row in the proof folder.
- **Zero local variables and zero local styles.** This is the invariant that separates this skill from `heyhi-design-bridge`.

---

## 4. The exact per-section call order

One major section per `use_figma` call, at most ten logical operations, never two `use_figma` calls in parallel. The order inside a section:

1. **Resolve the wrapper and import every dependency in one `Promise.all`.** `getNodeByIdAsync(wrapperId)`, `importComponentSetByKeyAsync(key)`, `importVariableByKeyAsync(key)`, `importStyleByKeyAsync(key)`, batched. Sequential awaits multiply IPC latency for no benefit.
2. **Build the section frame** with `figma.createAutoLayout(direction)`.
3. **Bind fills and spacing.** `figma.variables.setBoundVariableForPaint(basePaint, "color", var)` returns a NEW paint; capture it and assign `section.fills = [boundPaint]`. `section.setBoundVariable("itemSpacing" | "paddingLeft" | "topLeftRadius" | …, var)`.
4. **Apply styles.** `await node.setTextStyleIdAsync(textStyle.id)` for text; `node.effectStyleId = effectStyle.id` for shadows.
5. **Instance components.** Find the resolved variant in `set.children` by its `Property=Value` name, or `set.defaultVariant`; `variant.createInstance()`.
6. **Set props.** `instance.setProperties({ "VariantProp": "value", "Label#…": "text", "Show Icon#…": true, "Icon#…": iconComponentId })` for VARIANT / TEXT / BOOLEAN / INSTANCE_SWAP. Read `props_passed`, fall back to `defaults`.
7. **Slot content by append, never by setProperties.** For a `SLOT` property, `instance.findAllWithCriteria({types:["SLOT"]}).find(byName)` then `slot.appendChild(child)`. `setProperties` on a slot throws (Ground-truth correction).
8. **Append, then FILL.** `wrapper.appendChild(section)`, then `section.layoutSizingHorizontal = "FILL"`. Never before the append.
9. **Set the theme mode once on the wrapper.** Resolve the collection from an imported variable's `variableCollectionId` (`await figma.variables.getVariableCollectionByIdAsync(v.variableCollectionId)`), pick the mode by name from `collection.modes`, then `wrapper.setExplicitVariableModeForCollection(collection, modeId)` so bound children resolve to the surface's mode. This is once per wrapper, not per section.
10. **Return every created/mutated node ID** and write it to the disk ledger.

Copy overrides use `setProperties` on the TEXT property keys (more reliable than direct `characters`); the canonical font-load recipe (`loadFontAsync` for the node's current fonts, `await`, mutate, return IDs) is the fallback for unmanaged text only. Icons import as SVG (`createNodeFromSvg` with explicit width/height/viewBox) or an INSTANCE_SWAP; never reconstructed from rotated primitives.

---

## 5. Transport constraints and the recorded traps (hard, every call)

The native transport is the engine's many-small-sequential-calls pattern, not `heyhi-design-bridge`'s bundled-plugin transport (which exists because Translate lands a whole page in a few large chunks). The live-write lessons still bind. Attribution is exact so the next author can trace each rule.

| Constraint | Source | The rule |
|---|---|---|
| 50,000-char per-call cap | `figma-use` § 1, `heyhi-design-bridge` v0.8.0 | Each `use_figma` payload clears 50k. Split a dense section; import a unique SVG once as a component and reuse by instance. |
| Never parallelize `use_figma` | `figma-use` § 2, `figma-generate-library` rule 13 | Figma state mutations are strictly sequential. Independent imports batch into one `Promise.all` inside a single call. |
| Font preflight before any text write | `heyhi-design-bridge` v0.14.0 | Resolve every `(family, style)` against `listAvailableFontsAsync()` first; capture the exact Figma style spelling (they differ per family). A silent substitution is invisible until the render. |
| Rebind on a clone renders black | Live proof, 2026-09-04 | A node whose fill is already bound to variable X, re-assigned a paint bound to the same X over a black base, reads as bound but renders black. Set `fills = []`, then bind a paint whose base is the resolved value. Screenshot; the per-node binding audit alone is a false clean. |
| `resize()` resets sizing to FIXED | Live proof, 2026-09-04 | An auto-layout frame sized with `resize(w, 1)` renders 1px tall until `layoutSizingVertical = 'HUG'` (or FILL) is set after the resize. |
| Stroke-weight binding reads per side | Live proof, 2026-09-04 | `setBoundVariable('strokeWeight', v)` stores as `strokeTop/Bottom/Left/RightWeight`; an audit that checks the `strokeWeight` key reports a false unbound. |
| `setProperties` on a SLOT throws | `figma-use` component-patterns | Slot content is set by appending children to the slot node, not by `setProperties`. |
| Native swap-libraries cannot retarget a local master | plan Ground-truth corrections | It only matches assets from another published library; a local pattern is placed by instance, retargeted by `swapComponent`. |
| Never hallucinate a node ID | `figma-generate-library` rule 14 | Read every ID from the disk ledger or a prior return, never from memory. |

**On the bundled-plugin transport.** `heyhi-design-bridge` built a bundled-plugin transport out of necessity for its whole-page write model. This skill's v1 uses the engine's native per-section `use_figma` calls, human-initiated at the gate. A bundled-replay transport so a whole surface set builds unattended is a v2 direction, and it also has to clear the Earn-the-Room human-initiation gate; it is not merely a transport swap.

---

## 6. The worked build (the instance's own proof run, the Log index page)

**Substrate (plan § 5 D2):** rebuild the heyhi.design Log index page into a new scratch app file in the instance's own Figma team, from the 2026-09-04 generated library. The library and variable maps are read directly from the source library file (Lane A runs in parallel), and the surface list is hand-written in the `app-manifest.json` shape (Lane C runs in parallel).

**Prerequisite:** the source library must be **published**, or its keys resolve to "not found" on import. Publishing is a Figma UI action with no Plugin-API path (recorded 2026-09-07); it is a human step, named at the gate.

**Sketch of the build:**

1. Phase 0: `get_libraries` on the new app file; read the source library's component and variable keys; build the resolution table for the Log index surface (the header/nav, the log-entry list rows, the footer, the type ramp, the theme mode); print the pre-write plan.
2. Wrapper: one `VERTICAL` auto-layout at the Log index breakpoint.
3. Sections, one `use_figma` call each: the header (imported nav/logo instances, bound background, applied heading style); the entry list (a row composition, likely a local pattern if the library has no "log row", built once and instanced per entry); the footer (imported instances). Each section binds color and spacing to imported variables and applies imported text styles.
4. Images (if any on the Log index): build a placeholder node per image, fetch each image's bytes from the running `heyhi-website` dev server or the live site (out of the sandbox), and `upload_assets` them onto the placeholders (or `figma.createImage` for a tiny inline one). The Log index is largely text and type, so this step may be a no-op.
5. Validate (§ references/validation.md): every instance on a library key, every variable remote, every text node on a library style, zero local variables or styles.
6. Render-and-look: a `get_screenshot` per section against the live Log index page; assert the font family matches the library's text styles (display, body, utility), no clipped or placeholder text, the theme mode.

The proof record, the file keys, the acceptance table, and the per-section screenshots are filed in the instance's engagement folder (gitignored). No file key appears in any tracked file.

---

## 7. Re-run / idempotency

- Read the disk ledger first; find-or-update every wrapper, section, and instance by ID; never duplicate.
- A re-run never re-imports a component already present, and never clobbers a human-ruled deviation.
- Update mode (SKILL.md Step 7): `get_metadata` the existing frames, `swapComponent` a changed variant, `setProperties` changed props, add or remove sections. This is the path `feature-increment` drives.

---

*HeyHi Confidential. Reference for `app-to-figma` (Sheerline area 5). Engine: Figma's `figma-generate-design` + `figma-use`. Reverse verb: `heyhi-figma-ds-generator`. Live-write lessons: `heyhi-skills/heyhi-design-bridge/` and the 2026-09-04 generator proof. Spec source: `plans/plan-sheerline-fdde-loop-2026-09-07.md` (DISPATCH-02).*
