---
name: app-to-figma
description: >-
  Build an application's surfaces into a target Figma app file from the client's
  own PUBLISHED library instances and variables, not drawn primitives. For each
  in-scope surface it identifies the libraries on the target file, imports
  component sets, variables, and styles by key, instances components and sets
  their props to the application's needs, applies library text and effect styles,
  binds fills and spacing to imported variables, sets the theme mode, builds a
  local pattern component only where the library has no match, imports images
  through upload_assets, validates structurally, and renders and looks. The reverse of the DS generator: that one writes the library, this
  one consumes it to write the screens. Triggers: "build this surface in Figma
  from the library", "write the app screens to Figma", "rebuild this page from
  the design system". Leaves the judgment (the component match when inexact, a
  deliberate deviation from the library, layout where the library is silent, the
  surface verdict) as labeled empty slots behind a named human gate. NOT for
  translating a built HTML prototype or vectorizing a raster into Figma, which
  mints local tokens (use heyhi-design-bridge); NOT for generating the design
  system library itself into Figma from the contract (use
  heyhi-figma-ds-generator); NOT for building an HTML/code prototype or interface
  (use ui-studio for client UI, heyhi-ui-ux for HeyHi pages, per CLAUDE.md
  ui-studio routing); NOT for reading the application into a manifest (use
  app-recon); NOT for auditing a built prototype (use heyhi-prototype-audit).
version: "0.1.0"
updated: "2026-09-07"
status: "deployed 2026-09-07 (Sheerline fdde-loop convergence pass 1, DISPATCH-06; promoted from skill-updates/app-to-figma/). Built from plans/plan-sheerline-fdde-loop-2026-09-07.md (DISPATCH-02, Lane B, Wave 1). Sheerline area 5 (Wireframing & Prototyping), build class N (net-new), the loop's build verb. The §8 kill-condition probe ran green on 2026-09-07 (import-by-key and teamLibrary access work on a Figma Pro plan; log in the instance's engagement folder). Release tier: buildable-now-internal-first; any designer-facing external surface is D-3-gated (2026-10-09), and D10 keeps this arc inside that hold."
review_by: "2026-09-21"
classification: confidential
---

# app-to-figma

**Sheerline area 5 (Wireframing & Prototyping) · build class N · Figma-live build skill.** It writes an application's surfaces into a **saved cloud** Figma app file by importing the client's own **published** library component sets, variables, and styles **by key**, instancing them, and binding them, so every frame stays linked to the library instead of being redrawn as primitives. It is the second half of the loop the DS generator opened. `heyhi-figma-ds-generator` writes the design-system *library* from the served contract; this skill *consumes* a published library to build the *screens*. Two verbs sit in front of retrieve, validate, grade, learn. This is **build**; its input is **read** (`app-recon`).

**What this is.** A per-surface, library-aware build: import the real component sets and variables the client already published, instance them, set their props to what the application actually renders, bind and theme them, and validate that nothing was redrawn or minted. **What this is not.** Not a token minter (that is `heyhi-design-bridge`, and the difference is load-bearing here). Not the library build (`heyhi-figma-ds-generator`, the reverse verb). Not a code or HTML prototype (`ui-studio` / `heyhi-ui-ux`). Not the application read (`app-recon`). Not a judge of the result.

**The boundary this skill obeys (Sheerline § 9, absolute).** A structured build with explicit empty judgment slots, a named human gate, and provenance labels on anything synthetic. The charter is one sentence: *a capability that fills its own judgment slot has exceeded its charter* (`sheerline/os/operating-principles.md` § Design Constraints). The empty slots here are the **component match when inexact**, a **deliberate deviation** from the library, **layout judgment** where the library is silent, and the **surface verdict**. The skill builds the frames and hands those calls back. A version that decides which library component "is close enough", or rules a surface done, has overstepped. Applied as a build-time test: *does any step below fill one of the slots in [§ The human-gated slots]?* If so, stop.

> **This skill closes through the Exit Gate (`CLAUDE-SESSION-RULES.md § Exit Gate`), Flavor A.** See the bottom-of-skill bracket.

---

## Prerequisites

- The Figma MCP is connected, and `use_figma` is reachable (probe it, do not trust the tool list; the MCP has no changelog).
- The target app file exists and is a **saved cloud** file (`figma.com/design/<fileKey>`), not a local/unsaved file. If none exists, create one with `create_new_file` (after loading `figma-create-new-file`) and reuse its key.
- The surface's library is **published**. Import-by-key resolves nothing from an unpublished source; publishing is a Figma UI action with no Plugin-API path, so an unpublished library is a human step named at the gate, not a thing the skill can do.
- The served library and variable maps are reachable (through the instance, or passed by path). Without them the skill has no keys to import by, and it does not run the census to make them.

---

## Routing: the cell this occupies, and its siblings

| If the task is… | Use |
|---|---|
| **Build** an application's surfaces into a Figma **app file** from the client's **published library** (import by key, instance, bind) | **this skill** |
| **Generate** the design-system library (variables + token styles + component library) into a Figma design file from the served contract | `heyhi-figma-ds-generator`. That **writes** the library; this **consumes** it |
| Translate a built HTML prototype, or vectorize a raster, into a Figma file (mints local tokens) | `heyhi-design-bridge`. The local-token minting this skill must NOT reproduce |
| Build an HTML / code prototype or interface | `ui-studio` (client) / `heyhi-ui-ux` (HeyHi), per CLAUDE.md § ui-studio routing |
| Read the application into a manifest (surfaces, components, endpoints, copy) | `app-recon`. This skill's input |
| Add a feature across the artifact, the prototype, and the repo from one contract | `feature-increment` (Care). This skill is its Figma leg |
| Audit a built prototype's interaction completeness | `heyhi-prototype-audit` |
| Decide the match, the deviation, the layout, the verdict | **the human** (this skill's named gate) |

This skill orchestrates Figma's own `figma-generate-design` (the screen-building workflow) over `figma-use` (the Plugin-API HOW). It never reimplements the Plugin API, and it never runs the census that produces its library map (`figma-library-census`, Lane A); it consumes the map.

---

## Inputs (retrieved through the instance, never pasted as a spec)

The source of truth is the per-system heyhi-mcp instance (Sheerline area-7 FOUNDATION, Invariant 4: *retrieved, never pasted*). This skill loads no contract file, token file, brand config, or DESIGN.md from disk as its spec.

1. **The surface list** is an `app-manifest.json` in the plan § 3.3 shape: `surfaces[]` with `id`, `route`, `container_dir`, `entry_component`, `breakpoints[]`, `theme`, `architecture_target`, `components_used[]` (each `name`, `props_passed{}`, `defaults{}`, `source`), `copy[]` (`text`, `role`, `file`, `line`), and `endpoints[]`. Produced by `app-recon` (Lane C) and served through `retrieve_application_context(scope: manifest)` when present, passed by path otherwise. Until Lane C lands, a hand-written surface list in the same shape is the input, and that is how the instance's own proof run ran.
2. **`figma_app_file_key`** is the **target** app file. It must be a **saved cloud** key. A `figma.com/design/new?…&localFileKey=LOCAL_…` URL is refused (Step 2). This is the app/screens file, distinct from the DS library file the generator writes.
3. **The served library and variable maps** are `figma-library-map.json`, `figma-variable-map.json`, and `ds-map.json` (plan § 3.3, emitted by `figma-library-census`, Lane A). Retrieved through `retrieve_application_context(scope: ds-map)` when present, passed by path otherwise. They carry, per row, the published `key` this skill imports by, the property axes, the coverage state, and the composition level. This skill reads those maps; it does not build them.

**How the manifest maps to import keys.** For each `surfaces[].components_used[]` entry, the component `name` joins to a `figma-library-map.json` `components[]` row (the `figma_key` and its `properties[]`); `props_passed{}` selects the VARIANT/TEXT/BOOLEAN/INSTANCE_SWAP values; `defaults{}` fills any prop the source did not pass. Each bound value (a fill, a padding, a radius) joins to a `figma-variable-map.json` `variables[]` row (its `key`). A `components_used[]` entry with no exact library row is an **unresolved** element for the gate, never a silent best-guess match.

Echo one line before any write: `App file:<key|LOCAL→refuse> · surfaces:<n in scope> · library map:<served|by-path> · theme:<mode> · seal:<bool>`.

Full input/output contract, the exact call order, and the recorded Plugin-API traps live in **[references/build-method.md](references/build-method.md)**; the structural checks live in **[references/validation.md](references/validation.md)**; the probe log (the API calls this skill depends on, with observed results and the plan tier) lives in **[references/probes.md](references/probes.md)**. All three load on demand, not at session start.

---

## Step 0: Improvement hook check

Before running, retrieve any recurring corrections for Figma-build / import-by-key / instance-and-bind work (`retrieve_design_corrections` if the instance is reachable, or the Sheerline `os/corrections/` registry). Fold a matching recurring correction into the run. Skip silently if none.

## Step 1: Load context, the engine skills, and the maps

1. **The Figma engine skills (mandatory before any write).** Load `figma-generate-design` (the screen workflow: discovery order, wrapper-first, import-by-key in one `Promise.all`, `setProperties`, componentize repeats, icons via SVG, validate, image transfer, update mode) **and** `figma-use` (the Plugin-API rules: the return pattern, page-reset-once-per-call, ID return, font loading, the 0-to-1 color range, the ≤10-operations rule). This skill assumes them; it does not restate them. Include the engine skill in `skillNames` on every `use_figma` call (prefixed `resource:` when loaded via the MCP resource).
2. **The served application and design-system context** through the instance: `retrieve_application_context` (manifest, intent, ds-map, ijm) when present; `retrieve_design_context` / `retrieve_design_relationships` / `retrieve_design_examples` for the component specs the maps point at. Never inline a file as the spec.
3. **The surface list and the maps** (§ Inputs). Resolve `figma_app_file_key`, the in-scope surfaces, the theme mode, and the hermetic-seal flag.

## Step 2: Phase 0, the pre-write gate (the load-bearing human gate, no writes)

Phase 0 writes nothing to the canvas. It is the Earn-the-Room approval artifact.

- **Capability check first.** Probe the surface, do not trust the tool list (`whoami` plus a read-only `use_figma`). The §8 import-by-key probe is a prerequisite of this skill and is recorded in `references/probes.md`; a run on a new plan re-probes before building. If any in-scope surface carries images, probe `generate_figma_design` too (it is advertised but has been absent from the callable manifest; Step 5), so the pre-write plan states whether images will be captured or flagged for the human.
- **Refuse a local file.** `use_figma` needs a saved cloud file. If `figma_app_file_key` resolves to an unsaved/local key, `use_figma`/`get_metadata` return "don't have edit access". Refuse to write; ask for the saved `figma.com/design/<fileKey>` URL. Do not loop on the failing write.
- **Confirm the library is importable.** `get_libraries` on the target file lists what is added and available. Import-by-key does not require the library to be added first, but the library **must be published**: an unpublished source returns `Component set with key "…" not found` on import (recorded 2026-09-07). If the surface's library is unpublished, stop and name the publish step for the human.
- **Resolve every needed key.** For each `components_used[]` entry on each in-scope surface, resolve its published component key and variant from `figma-library-map.json`; for each bound value, resolve the variable key from `figma-variable-map.json`; for each text run, resolve the library text style key. Build the resolution table.
- **List the unresolved.** Every surface element with no exact library match goes on the unresolved list with its `props_passed` and the nearest candidate from the map, for the human's **reuse / wrap / local-pattern** ruling. Do not pick the match yourself when it is inexact.
- **Print the pre-write plan** to chat and get approval: the resolution table, the unresolved list, the per-surface wrapper plan, the theme mode, and every deviation the human must rule. Surface every live fork; do not resolve one to keep moving.

The pre-write plan is read-only. Phase 1 (Step 3) does not begin until it is approved.

## Step 3: Per surface, the wrapper then the sections

Follow `figma-generate-design` Steps 3 and 4, one **major section per `use_figma` call**, at most **ten logical operations** per call, **never two `use_figma` calls in parallel** (state mutations are strictly sequential). Return every created node ID and write it to the disk-backed state ledger in the proof folder (`app-to-figma-state-{RUN_ID}.json`), re-read each turn.

1. **Wrapper first** (its own call): `figma.createAutoLayout('VERTICAL')`, sized to the surface's breakpoint from the manifest, positioned clear of existing content, name from the surface `id`. Return its ID.
2. **Each section inside the wrapper** (its own call): resolve the wrapper by ID and import every dependency for that section in **one `Promise.all`** (`importComponentSetByKeyAsync`, `importVariableByKeyAsync`, `importStyleByKeyAsync`). Then, in the order below.

The canonical section shape (the full recipe, with the trap notes, is in build-method.md):

```js
const createdNodeIds = [];
// import every dependency for THIS section in one Promise.all
const [wrapper, buttonSet, bgVar, gapVar, headingStyle] = await Promise.all([
  figma.getNodeByIdAsync("WRAPPER_ID"),
  figma.importComponentSetByKeyAsync("BUTTON_SET_KEY"),
  figma.variables.importVariableByKeyAsync("BG_VAR_KEY"),
  figma.variables.importVariableByKeyAsync("GAP_VAR_KEY"),
  figma.importStyleByKeyAsync("HEADING_STYLE_KEY"),
]);
const section = figma.createAutoLayout("VERTICAL");
section.name = "Header";
// bind (never hardcode): setBoundVariableForPaint returns a NEW paint, capture it
section.fills = [figma.variables.setBoundVariableForPaint(
  { type: "SOLID", color: { r: 0, g: 0, b: 0 } }, "color", bgVar)];
section.setBoundVariable("itemSpacing", gapVar);
// instance the resolved variant, set its props
const variant = buttonSet.children.find(c => c.name.includes("Style=primary")) || buttonSet.defaultVariant;
const btn = variant.createInstance();
btn.setProperties({ "Label#4:0": "Read the log", "Show Icon#4:28": true });
section.appendChild(btn);
createdNodeIds.push(btn.id);
// append THEN fill; the theme mode is set once per wrapper (see Theme mode), not per section
wrapper.appendChild(section);
section.layoutSizingHorizontal = "FILL";
createdNodeIds.push(section.id);
return { createdNodeIds };
```

Within a section, in order: build the section frame; bind its fills and spacing to the imported variables; apply the imported text style with `setTextStyleIdAsync` and the effect style with `effectStyleId`; instance each component (the resolved variant, or `set.defaultVariant`); set its props with `setProperties` for VARIANT / TEXT / BOOLEAN / INSTANCE_SWAP, reading the app's `props_passed` and honoring source `defaults`; for a `SLOT` property, **append children to the slot node** (never `setProperties` on a slot, it throws); `appendChild` the section to the wrapper, then set `layoutSizingHorizontal = 'FILL'` (after appending, never before); set the theme mode once on the wrapper with `setExplicitVariableModeForCollection` so bound children resolve to the surface's mode.

3. **Override copy** with `setProperties` on the TEXT property keys from the resolution table (more reliable than direct `characters`); fall back to the canonical font-load recipe only for unmanaged text.
4. **Icons** via imported SVG (`createNodeFromSvg` with explicit width/height/viewBox), or an INSTANCE_SWAP when the library exposes the icon; never reconstruct from rotated primitives.

## Step 4: Local pattern components (only where the library has no match)

When a surface composition has no library component and the human ruled "local pattern" at the gate: build the pattern as a **component** once with `figma.createComponent()`, place instances, name it from `ds-map.json`, and emit a **pattern ledger row** in the plan § 3.3 shape (`name`, `signature`, `level`, `status: local`, `usage.applications/surfaces/figma_nodes`, `origin`) into the **proof folder**, not the served data. The served ledger is written only by the convergence pass or a Care run under the human's clearance. A local pattern mints a **component**; it never mints a variable, a style, or a token (§ Hard constraints).

## Step 5: Images (only when the surface carries them)

`use_figma` cannot fetch external image URLs (`fetch` is `undefined` in the sandbox) and `createImageAsync` is blocked, so an image comes in through one of these paths, in order of preference (all verified 2026-09-07 on the Pro scratch file, see `references/probes.md`):

1. **`upload_assets` (the primary path).** Build the image node as a placeholder, then call `upload_assets(fileKey, count, nodeIds: [placeholder ids])` for single-use submit URLs, and POST each image's bytes to its URL (multipart `file`, whose filename becomes the layer name, or raw bytes with the Content-Type). The image is set as a fill on the target node and the response returns the `imageHash`. The bytes come from the running dev server or the live site, fetched **out of the sandbox** (the agent environment has network; the sandbox does not). PNG / JPG / GIF / WebP / SVG, up to 10MB; an SVG imports as an editable vector tree. This is a separate MCP tool, so it does not count against the `use_figma` operation limit.
2. **`download_assets` then `upload_assets`** when the image already lives in another Figma file (the documented cross-file transfer): `download_assets` returns the raw image, `upload_assets` places it.
3. **`figma.createImage(bytes)` inline** for a small image that fits the 50,000-char `use_figma` payload as base64 (`atob` is available): decode to a `Uint8Array`, `figma.createImage(bytes)`, then set `{ type: 'IMAGE', imageHash: img.hash }` as the fill.
4. **`generate_figma_design`** stays an optional pixel-reference capture *if* a Phase 0 probe finds it callable; it was absent from the live manifest on 2026-09-01 and 2026-09-07, and it is not required because paths 1 to 3 cover image import.

Only when an asset is genuinely unreachable (no URL, no source file) is it a flagged gap for the human. The built frames stay library-linked in every case; images are fills, never a substitute for the library instances.

## Step 6: Structural validation, then render-and-look

Run the checks in **[references/validation.md](references/validation.md)** with a read-only `use_figma`:

- every instance's `mainComponent.key` is present in `figma-library-map.json`;
- every bound variable resolves to `remote: true`;
- every text node carries a library text style;
- **zero local variables and zero local styles were created** (the anti-minting invariant).

Then the design smoke test (V9, `sheerline/os/session-rules.md`): a `get_screenshot` per built section, compared against the source surface, asserting the font family, no clipped text, no placeholder text, and the theme mode. A structural pass with a wrong render is still a failure; look.

## Step 7: Update mode (re-runs and feature increments)

For a surface already built (a re-run, or `feature-increment`'s Figma leg): `get_metadata` the existing frames, then update only what changed. `swapComponent` for a changed variant, `setProperties` for changed props, add or remove sections. Idempotent: find-or-update by the ledger ID, never duplicate a section; never clobber a human-ruled deviation on a re-run. `feature-increment` consumes this skill in update mode as a promoted skill; it does not re-implement the build inline.

---

## Theme mode

The manifest's `surfaces[].theme` names the mode a surface renders in (the worked example's served Color collection, for example, carries Light and Dark). Set it once per surface on the wrapper with `frame.setExplicitVariableModeForCollection(collection, modeId)` after the bound children exist, so every bound fill and border resolves to that mode. A surface that renders in both modes is two wrappers, one per mode, not two mode-sets on one frame. The mode is read from the manifest, never guessed; a surface with no stated theme is an unresolved item for the gate, not a default the skill picks.

## Idempotency and the state ledger

Every created node ID is written to `app-to-figma-state-{RUN_ID}.json` in the proof folder, shaped `{ wrappers: {surface→id}, sections: {name→id}, instances: {key→[ids]}, patterns: {name→id} }`, and re-read at the start of each `use_figma` call. Context truncates across a long build; the ledger is the durable memory, the same convention the generator uses. A re-run reads the ledger first and updates by ID (find-or-update), so it never duplicates a wrapper or a section and never re-imports a component already present. Cleanup, when needed, identifies nodes by their ledger ID or name convention, never by prefix-guessing.

## Worked example: the instance's own proof run (the Log index page)

The proof (plan § 5 D2) rebuilds the heyhi.design Log index page into a new scratch app file from the 2026-09-04 generated library. The surface list is hand-written in the `app-manifest.json` shape (Lane C runs in parallel), the library and variable maps are read from the source library file, and the build imports the library's Button and its Color / Spacing / Typography variables by key, instances them, and binds them. The proof record, the file keys, the acceptance table, and the per-section screenshots live in the instance's engagement folder (gitignored). The full worked build, with the exact call sequence, is in [references/build-method.md](references/build-method.md).

## Failure modes and recovery

| Symptom | Cause | Recovery |
|---|---|---|
| `Component set with key "…" not found` on import | the source library is not published | name the publish step for the human (a Figma UI action, no Plugin-API path); do not fall back to drawing the component |
| `use_figma` / `get_metadata` return "don't have edit access" | the target file key is a local/unsaved key | refuse; ask for the saved `figma.com/design/<fileKey>` URL |
| a `use_figma` payload exceeds the 50,000-char cap | too much in one call, or a large inline SVG | split the section; import a unique SVG once as a component and reuse by instance |
| an instance renders the wrong color though the binding reads present | the black-rebind trap (a clone rebound to the same variable over a black base) | clear `fills = []`, then bind a paint whose base is the resolved value; screenshot to confirm |
| a section renders 1px tall | `resize()` reset the sizing to FIXED | set `layoutSizingVertical = 'HUG'` (or FILL) after the resize |
| the structural check passes but the render is wrong | a per-node audit is a false clean | the render-and-look (V9) is not optional; a screenshot per section is the real gate |

---

## The human-gated slots (§ 9 boundary, enumerated and non-empty)

Each row below is a **NEEDS HUMAN** slot: the skill leaves it empty and names the gate; a version that fills one has overstepped. The load-bearing gate is the **pre-write plan** (Step 2), a **NEEDS HUMAN** approval before any canvas write.

| Judgment slot (NEEDS HUMAN, stays human) | Trigger | The gate + provenance rule |
|---|---|---|
| **The pre-write plan** (load-bearing) | Before any canvas write | The resolution table + the unresolved list + the per-surface plan are printed and **approved** before Step 3. Read-only; writes nothing. |
| **The component match when inexact** | A surface element has no exact library match | Surface the element's `props_passed` and the nearest candidate from the map; the human chooses reuse / wrap / local-pattern. Never pick the inexact match yourself. |
| **A deliberate deviation from the library** | The surface intentionally departs from the library component | Record it as a labeled deviation for the human to rule; a re-run never silently reverts it. |
| **Layout judgment where the library is silent** | The library specifies the parts, not the arrangement | The arrangement is the designer's; the skill places what the manifest and library specify and flags the rest. |
| **The surface verdict** | Always | Whether a rebuilt surface is right is the human's call (the `dont-automate` line). The skill builds and validates; it never rules the surface done. |

`figma-generate-design`'s own floor holds: when exactly one path is clearly correct from the map, take it. The gate fires on genuine ambiguity, not on every mechanical choice.

---

## Hard constraints (every call)

- **Mint nothing local except an approved pattern component.** The new file creates **no variables and no styles**. This is the line that separates this skill from `heyhi-design-bridge`, which mints local tokens for its translate model. Every color, spacing, radius, and type value comes from an **imported** library variable or style. A local pattern (Step 4) mints a component only, and only at the human's ruling.
- **Import by key; instance; bind.** Never draw a primitive where a library component, variable, or style exists. `mainComponent.remote` must read `true` on every instance.
- **One major section per `use_figma` call; at most ten logical operations; never parallelize `use_figma`.** Independent imports batch into one `Promise.all` inside a single call.
- **Ledger every node ID.** Write `{key → id}` and `{section → id}` to the disk-backed state file in the proof folder; re-read it each turn; never hallucinate a node ID.
- **Refuse a local/unsaved file.** A saved cloud key only.
- **Never use Figma's native swap-libraries** to retarget a local master (it only matches assets from another *published* library); a local pattern is placed by instance, retargeted by `swapComponent`.
- **Never detach an instance.** Detaching breaks the library link and invalidates ancestor node IDs.
- **Carry the recorded traps** (build-method.md § 5, the recorded-traps table, all from the 2026-09-04 live proof): `resize()` resets sizing to FIXED (set HUG/FILL after); a rebind-to-the-same-variable over a black base renders black (clear fills, rebind from the resolved value); a `strokeWeight` binding reads back per side. Screenshot every section; a per-node binding audit alone is a false clean.
- **Prose and seal.** No em dashes, no banned words, no pricing; no client name, file key, or engagement detail in a tracked file. Proof records and every file key go to the instance's engagement folder (gitignored).

## What is explicitly out of scope

- **The design truth**: which library component fits, whether to deviate, the arrangement where the library is silent, whether the surface is right. Empty slots by construction (§ 9).
- **Building the library**: `heyhi-figma-ds-generator` (the reverse verb). **Running the census** that produces the library map: `figma-library-census` (Lane A). This skill consumes the map, never rebuilds it, and never reads Lane A's folder.
- **Translating a prototype or vectorizing a raster**: `heyhi-design-bridge` (and its local-token minting, which this skill must not reproduce). **Building an HTML / code prototype**: `ui-studio` / `heyhi-ui-ux` (CLAUDE.md § ui-studio routing).
- **Reading the application**: `app-recon`. **The feature increment across all three targets**: `feature-increment` (this skill is its Figma leg, consumed as a promoted skill, never re-implemented inline).
- **Writing pattern rows into the served `components.json`**: the convergence pass or a cleared Care run only. **Creating `pattern-intake/`**: Lane I. **Editing any shared anchor**: the convergence pass.
- **Writing to any HeyHi production Figma file or any client file**: the instance's own proof run uses a new scratch file in the instance's own Figma team only.

---

## Exit Gate Required Headers (bottom-of-skill bracket)

This skill closes through the Exit Gate Flavor A (`CLAUDE-SESSION-RULES.md § Exit Gate`). Before declaring done, confirm every header carries real content, not a claim:

- `## Fixes Applied`: the surfaces built, with the Figma link, the sections created, the instances resolved to library keys (N of N), the variables bound remote (N of N), local variables and styles created (0 / 0), and where the proof is filed.
- `## Smoke Test`: the Step 6 structural checks (every instance on a library key, every variable remote, every text node on a library style, zero local variables or styles) and the render-and-look (a screenshot per section, font family asserted, no clipped or placeholder text).
- `## Next Session Prompt`: the human-gated slots still open (the inexact matches, the deviations, the layout calls, the surface verdicts), and any surface deferred.

---

*HeyHi Confidential. Sheerline area 5 (Wireframing & Prototyping), build class N. v0.1.0 staged 2026-09-07 from `plans/plan-sheerline-fdde-loop-2026-09-07.md` (DISPATCH-02, Lane B). Engine: Figma's `figma-generate-design` + `figma-use`. Reverse verb: `heyhi-figma-ds-generator` (writes the library this consumes). Live-write lessons: `heyhi-skills/heyhi-design-bridge/` and the 2026-09-04 generator proof. Boundary: § 9.*
