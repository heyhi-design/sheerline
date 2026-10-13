# FigJam Mapper — artifact recipes (load on demand)

> Part of `heyhi-figjam-mapper`. Load per artifact type. Assumes `figma-generate-diagram`
> (for the Mermaid types) and `figma-use` + `figma-use-figjam` (for the FigJam builds) are
> already loaded — this file carries the mapping method, not the Figma API rules.

## Routing recap

| Artifact | Mechanism | Why |
|----------|-----------|-----|
| Flow, decision tree, pipeline, dependency graph | `generate_diagram` flowchart | Native Mermaid |
| Architecture (services/datastores/queues) | `generate_diagram` flowchart + `useArchitectureLayoutCode` | Native, architecture route |
| Sequence of interactions | `generate_diagram` sequenceDiagram | Native |
| States + transitions | `generate_diagram` stateDiagram | Native |
| Data model | `generate_diagram` erDiagram | Native |
| IA sitemap | `generate_diagram` flowchart (top-down) | Hierarchy renders as a tree |
| **Journey map** | `use_figma` FigJam grid | Mermaid `journey` is unsupported by `generate_diagram` |
| **Service blueprint** | `use_figma` FigJam swimlanes | No Mermaid type exists |

---

## The Mermaid types (generate_diagram)

Keep to the constraints in `figma-generate-diagram`: camelCase node ids, quote special characters, no emojis / `\n` / HTML, supported types only. Examples of the shapes this skill emits most:

**IA sitemap** (flowchart, top-down):
```
flowchart TD
  home["Home"] --> products["Products"]
  home --> about["About"]
  products --> detail["Product detail"]
  products --> compare["Compare"]
```

**Process flow with an owner per step** — put the owner in the edge label, not invented:
```
flowchart LR
  lead["Lead captured"] -->|"marketing"| qualify["Qualify"]
  qualify -->|"sales"| discoveryCall["Discovery call"]
```

Do not add a branch the source does not describe. A missing branch is a `Step 3` gap flag.

**Reserved node ids (a live-run catch, 2026-08-17).** Mermaid parses some bare words as keywords, not node ids: `call` (callback directive; fails with `got 'CALLBACKNAME'`), plus `click`, `class`, `style`, and the `end` / `subgraph` / `graph` that figma-generate-diagram already names. Using one as a node id is a hard parse error. Use a distinct camelCase id (`discoveryCall`, not `call`), and prefer camelCase ids everywhere to stay clear of the keyword set.

---

## Journey map (FigJam grid, use_figma)

A journey map is a grid: **stage columns × dimension rows**. The content rows are filled from the
source; the interpretive rows ship **empty and labeled** (the § 9 judgment slots).

Rows, in order: `Stage` · `Doing` (actions, from source) · `Thinking` (from source if given, else empty) ·
**`Feeling` (empty slot)** · **`Pain points` (empty slot)** · **`Opportunities` (empty slot)**.

Build with a FigJam table (one column per stage, one row per dimension), or sections + stickies.
Sketch (table path):
```js
// figma-use-figjam loaded. FigJam file (figma.com/board/...). No figma.createPage().
const stages = ["Discover", "Evaluate", "Adopt"];            // from the source
const rows = ["Stage", "Doing", "Thinking", "Feeling", "Pain points", "Opportunities"];
const table = figma.createTable(rows.length, stages.length + 1);
// load the cell font before writing text (sublayer default varies) — see figma-use-figjam
const font = table.cellAt(0,0).text.fontName;
await figma.loadFontAsync(font);
rows.forEach((r,i) => { table.cellAt(i,0).text.characters = r; });
stages.forEach((s,c) => { table.cellAt(0,c+1).text.characters = s; });
// fill Doing from source; leave Feeling / Pain points / Opportunities blank (judgment slots)
return { createdNodeIds: [table.id] };
```
Mark the three empty rows visibly as slots (a lighter cell fill, or a "for the room" label sticky beside
them). Never fill them. Tag any `Doing` cell you inferred rather than took from the source with `(inferred)`.

---

## Service blueprint (FigJam swimlanes, use_figma)

A blueprint is horizontal lanes across a time axis, separated by three lines. Lanes top to bottom:

1. `Customer Actions`
2. line of interaction
3. `Frontstage` (what the customer sees: staff, UI)
4. line of visibility
5. `Backstage` (staff actions the customer does not see)
6. line of internal interaction
7. `Support Processes` (systems, third parties)

Build each lane as a FigJam **section**, place stickies left-to-right along the time axis inside each lane,
draw the three separator lines, and wire dependencies with connectors. `use_figma` runs code with top-level
`await` and `return` **only**: never emit `figma.closePlugin()` or an async IIFE (the FigJam reference docs
show both in their examples; `use_figma` wraps the code for you, so copying them fails). Lanes first:
```js
// figma-use-figjam loaded. FigJam file (figma.com/board/...). No figma.createPage().
const lanes = ["Customer Actions", "Frontstage", "Backstage", "Support Processes"];
const created = [];
let y = 0;
for (const name of lanes) {
  const sec = figma.createSection();
  sec.name = name;
  sec.x = 0; sec.y = y;
  sec.resize(1600, 320);   // resize() is the preferred method (not resizeWithoutConstraints); 320 tall so a 240px sticky fits
  y += 360;                // lane height + gap
  created.push(sec.id);
}
return { createdNodeIds: created };
```
Then add the stickies (referencing the lane ids returned above). A sticky is a **fixed 240x240 square**:
`width`/`height` are read-only and there is no `resize()` (toggle `isWideWidth` for the 416-wide form), which
is why the lane must be at least ~300 tall. Load the font before any text, append into the lane, then position
in section-local coordinates:
```js
const lane = await figma.getNodeByIdAsync(LANE_ID);
const s = figma.createSticky();
await figma.loadFontAsync(s.text.fontName);   // sticky default is Inter Medium; load from the node, do not hardcode
s.text.characters = "Books a slot";           // a real step from the source
lane.appendChild(s);                          // append FIRST, then position
s.x = 40; s.y = 40;                            // section-local coords (0,0 is the lane top-left)
return { createdNodeIds: [s.id] };            // for a row, use two passes: create all, read each s.height (stickies auto-grow), then set x/y
```
The **three separator lines** have no FigJam line primitive (`figma.createLine()` is Design-mode only). Draw
each as a **floating straight connector** spanning the lane width, with no arrowheads and a text label:
```js
const line = figma.createConnector();
line.connectorStart = { position: { x: 0,    y: 330 } };   // floating endpoints, absolute board coords
line.connectorEnd   = { position: { x: 1600, y: 330 } };
line.connectorLineType = "STRAIGHT";
line.connectorStartStrokeCap = "NONE";
line.connectorEndStrokeCap = "NONE";
const f = { family: "Inter", style: "Medium" };
await figma.loadFontAsync(f);
line.text.fontName = f;                    // a new connector's text.fontName is INVALID by default: set it explicitly
line.text.characters = "line of visibility";
return { createdNodeIds: [line.id] };
```
Wire step-to-step dependencies with attached connectors: `figma.createConnector()`, then `connectorStart` /
`connectorEnd` = `{ endpointNodeId: <sticky id>, magnet: "AUTO" }`.

The **pain points / opportunities** annotations across the blueprint are the empty judgment slots: add a
labeled empty band (a FigJam section titled "Pain points / opportunities (for the room)", or a row of blank
stickies under a text label). Do not fill it.

**Verified against the FigJam API references (2026-08-17):** `figma.createSection` + `section.resize`
(create-section.md, which names `resize()` as preferred over `resizeWithoutConstraints`); `figma.createSticky`
with its fixed 240px size, font-loaded-from-`text.fontName`, and `appendChild`-then-section-local-coords
(create-sticky.md, position-figjam-nodes.md); `figma.createConnector` floating + attached endpoints and the
`text.fontName`-invalid-by-default label gotcha (create-connector.md); and the `use_figma`
top-level-`await` / `return` contract with no `closePlugin` or IIFE (figma-use SKILL.md). Corrections applied:
`resizeWithoutConstraints` to `resize`; lane height 220 to 320 (a sticky is 240 tall, so it could not fit);
and the three separator lines pinned to floating straight connectors, since FigJam has no line node.

---

## IA tree (FigJam, use_figma): when a flowchart is not enough

If the sitemap needs annotation (owners, states, notes per node), build it as **shapes with text + connectors**
so nodes stay individually editable, rather than a flat `generate_diagram` flowchart. Parent shapes on top,
children below, connectors down. Same `use_figma` style (top-level `await`, `return`, no `closePlugin` or IIFE):
```js
// figma-use-figjam loaded. FigJam file (figma.com/board/...).
const node = figma.createShapeWithText();
node.shapeType = "ROUNDED_RECTANGLE";            // set AFTER creation; the default is ELLIPSE
await figma.loadFontAsync(node.text.fontName);   // shape default is Inter Medium; load from the node
node.text.characters = "Products";
// Size to the text. Never hardcode a shape size (the default clips): use the fitShapeToText
// measurer from create-shape-with-text.md, then node.resize(w, h).
return { createdNodeIds: [node.id] };
```
Connect parent to child with `figma.createConnector()` and `connectorStart` / `connectorEnd` =
`{ endpointNodeId: <id>, magnet: "AUTO" }` (end cap `ARROW_LINES`). To label a connector, set
`connector.text.fontName` explicitly first (it is invalid by default), then `connector.text.characters`.

**Verified against the FigJam API references (2026-08-17):** `figma.createShapeWithText` with `shapeType` set
after creation, font-loaded-from-`text.fontName`, and the mandatory `fitShapeToText` sizing
(create-shape-with-text.md); `figma.createConnector` endpoints and the connector-label font gotcha
(create-connector.md). No signature drift: the shapes-plus-connectors approach was correct, now pinned to the
exact FigJam node types and the size-to-text rule.

---

## Provenance and the judgment slots (the § 9 discipline, mechanical)

- **Empty slots:** `Feeling`, `Pain points`, `Opportunities`, and any "moments that matter" / priority call
  ship as labeled blank cells. Visibly mark them "for the room." The skill never fills them.
- **Inferred content:** anything not taken directly from the source carries an `(inferred)` tag on the node.
- **Hermetic seal:** if the FigJam is shared or its key lands in a tracked artifact, no client name appears on
  the board (`boundary.hermetic_seal_confirmed`). Use the engagement label, not the client name.
- **Voice:** stage names, lane labels, and any prose come from the engagement's voice
  (`brand_voice_source` / `voice_prohibited` / `dash_rule`), not HeyHi's, for client work.

---

*HeyHi Confidential. Reference for `heyhi-figjam-mapper` (deployed 2026-08-17, #666/#673; live-verified FigJam API recipes). Eval set added and this footer corrected v0.2.0 (2026-08-23, Wave D, `plans/plan-sheerline-skills-upgrade-2026-08-22.md`).*
