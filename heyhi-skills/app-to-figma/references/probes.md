# app-to-figma: Figma Plugin-API probe log

*Arc rule 9: a lane that depends on a Plugin-API call probes it in a scratch file before building on it, and records the result here. The Figma MCP has no changelog, so the surface is verified at runtime, never trusted from a tool list. This file carries the calls, the probe shape, the observed result, and the plan tier only. It carries no file key, library key, or engagement detail; those live in the gitignored proof record.*

*classification: HeyHi Confidential*

---

## Context

- **Plan tier probed:** Pro (a personal Pro team), a saved cloud file. This is the tier the § 8 kill condition targets.
- **Method:** each call ran on a fresh scratch file, against a known-published library (a community design system as the positive control, so a "not found" from an unpublished source cannot be confused with a plan-gate refusal). Created nodes were removed after the observation.
- **Date:** 2026-09-07.

## The § 8 kill-condition result

The kill condition (plan § 8) fires only if import-by-key or `teamLibrary.*` are **refused** in the `use_figma` sandbox on a Pro-plan file. Observed: they are not refused. The kill condition is **not triggered**; the build leg is viable on Pro.

An import-by-key against an **unpublished** source returns `Component set with key "…" not found`. That is a deterministic "the source is not published" result, not a refusal, and it does not retry away. Publishing a library is a Figma UI action with no Plugin-API path, so an unpublished source is a human step named at the gate.

## The calls this skill depends on

| Call | Probe shape | Observed result (Pro, saved cloud) |
|---|---|---|
| `figma.teamLibrary.getAvailableLibraryVariableCollectionsAsync()` | call, read the array | returns an array, no error (empty when nothing is enabled for the file); the API is reachable, not refused |
| `figma.importComponentSetByKeyAsync(key)` | import a published component set, read `.children.length` | ok: a component set imported (a multi-variant control set), instance created, `mainComponent.remote === true`, rendered |
| `figma.importVariableByKeyAsync(key)` | import a published COLOR variable, read `.remote`/`.resolvedType` | ok: `remote: true`, `resolvedType: COLOR` |
| `figma.importStyleByKeyAsync(key)` | import a published text style, read `.name`/`.type` | ok: a TEXT style imported |
| `instance.setProperties({ [prop]: value })` | set a VARIANT property on an imported instance | ok: a VARIANT property set to a valid option |
| `frame.setExplicitVariableModeForCollection(collection, modeId)` | bind an imported variable to a fill, then set the collection mode on the frame | ok: a two-mode collection's mode set on the frame with no throw |
| `node.setTextStyleIdAsync(styleId)` | apply the imported text style to a text node | ok: the style applied (the async setter loads the style's font) |

Every call the per-section build depends on (import a component set, a variable, and a style by key; set props; set the theme mode; apply a text style) executes on the Pro plan without refusal or plan-gate.

## Image import: the paths that work, and `generate_figma_design`

`generate_figma_design` (an MCP web-view capture) is **absent from the live callable manifest**: no callable schema resolved on 2026-09-01 (the `heyhi-figma-ds-generator` record) or on 2026-09-07 (this build; a `ToolSearch` for it returned no match). It is not a REST endpoint and has no REST equivalent. It is also **not needed**, because image import has verified working paths (all run on the Pro scratch file, 2026-09-07):

| Path | Probe result |
|---|---|
| `upload_assets` (MCP) | ok end to end: `upload_assets(count:1)` returned a single-use submit URL; a multipart POST of a PNG returned `success:true`, an `imageHash`, and `placedOnNodeId` (the image set as a fill on a new frame). PNG / JPG / GIF / WebP / SVG, 10MB max; an SVG imports as an editable vector tree; `nodeIds` targets existing nodes; a separate MCP tool, so it does not spend the `use_figma` op budget. |
| `download_assets` then `upload_assets` (MCP) | the documented cross-Figma-file image transfer (`download_assets` returns raw image URLs; `upload_assets` places them). |
| `figma.createImage(bytes)` (Plugin API, in `use_figma`) | ok: `createImage` is a function and `atob` is available; a 1x1 base64 PNG decoded to a `Uint8Array` produced a real `imageHash` applied as a fill. Bounded by the 50,000-char `use_figma` payload (small inline images only). |
| `figma.createImageAsync(url)` / `fetch` (in `use_figma`) | NOT usable: `fetch` is `undefined` (no network in the sandbox) and `createImageAsync` is blocked per the figma-use rules. Fetch bytes out of the sandbox, then use a path above. |

The REST API's image endpoints are export-oriented (`GET /v1/images/:key` renders nodes to PNG / SVG / PDF; `GET /v1/files/:key/images` lists existing image fills), useful for getting images OUT of Figma, not a general import path. The image write path is `upload_assets` (or `figma.createImage`). `generate_figma_design` is re-probed per run and used only as an optional pixel-reference capture if it becomes callable.

## What still requires a human, not an API

- **Publishing a library.** No Plugin-API or REST path publishes a library from the agent environment. A source that is not published resolves nothing by key. This is named at the pre-write gate as a human step, never worked around by drawing the component.
- **A local or unsaved file.** `use_figma` / `get_metadata` return "don't have edit access" on a local key. Refuse; ask for the saved `figma.com/design/<fileKey>` URL.

## Re-probe policy

A run on a **new plan** (a different team tier) re-runs the import-by-key probe before building, because the sandbox surface is plan-dependent and unversioned. The kill condition is evaluated per plan, not assumed from this record.

---

*HeyHi Confidential. Reference for `app-to-figma` (Sheerline area 5). The keys and file identifiers for the 2026-09-07 run live only in the gitignored proof record. Spec source: `plans/plan-sheerline-fdde-loop-2026-09-07.md` (DISPATCH-02, Lane B).*
