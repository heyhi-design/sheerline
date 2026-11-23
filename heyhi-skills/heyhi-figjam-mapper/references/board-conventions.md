# Board conventions (targeted FigJam builds)

How `heyhi-figjam-mapper` writes into a FigJam board that already exists, when the artifact must land on a named page or inside or beside a named node. `generate_diagram` places a new diagram where it chooses and cannot target a page or a node, so a targeted build goes through `use_figma` on FigJam (load `figma-use` and `figma-use-figjam` first). These conventions keep a scripted board legible to the people who work on it, and keep a re-run from piling up copies.

## The target is explicit

- The human names it: a FigJam file key plus an exact page name, or a node id (a section or a frame) from a link they share (the `node-id=` part of the URL, `12-34` in a URL is node `12:34`) or from `get_figjam`.
- A page name that matches no page, or more than one, is a question for the human. Never pick the closest match.
- Read the target first (`get_figjam` on the node) so the build knows what is already there.

## One section per artifact, stamped

- Every artifact lives in one FigJam section named `<artifact title> [sheerline:<type>:<slug>]`, for example `Checkout flow [sheerline:flow:checkout]`. The bracketed stamp is the artifact's identity.
- A re-run finds the section by its stamp and updates it in place. It never adds a second section for the same stamp. Two sections carrying one stamp is a finding to report, not something to merge silently.
- The section carries one small provenance note: the source the structure came from, the date, and "structure generated; judgment slots empty".

## Place beside, never on top

- A new section goes inside the target node when the target is a section the human named for it; otherwise beside it, in empty space to the right of the target's bounds (the target's x plus its width plus a clear gap), aligned to its top.
- Never move, resize, restyle or delete a node the build did not create. A person's stickies, comments and connectors stay where they are.

## Content

- Load fonts before setting any text (the `figma-use-figjam` recipe).
- Judgment slots (pain points, emotions, opportunities, the taxonomy call) are labeled, empty stickies in one distinct color, the same on every artifact, so the room can see at a glance what is theirs to fill.
- Anything the build inferred carries the prefix `inferred:` in its text.
- No client name on a shared board when the engagement intake's `boundary.hermetic_seal_confirmed` is true.

## Return and verify

- Return the section's node id, every node id the build created, and a link that opens on the section (`?node-id=<id with - for :>`).
- Verify with `get_figjam` on the section and `get_screenshot` on its node id: the artifact sits on the named page, inside or beside the named node, the stamp is unique, and the judgment slots are empty.

## A sketch of the targeting step (check names against `figma-use-figjam` before running)

```js
const pages = figma.root.children.filter((p) => p.name === TARGET_PAGE);  // exact name only
if (pages.length !== 1) throw new Error(`page "${TARGET_PAGE}" matched ${pages.length}: ask the human`);
const page = pages[0];
await figma.setCurrentPageAsync(page);
const anchor = TARGET_NODE_ID ? await figma.getNodeByIdAsync(TARGET_NODE_ID) : null;
if (TARGET_NODE_ID && !anchor) throw new Error(`node ${TARGET_NODE_ID} not found: ask the human`);
const stamped = page.findAll((n) => n.type === "SECTION" && n.name.endsWith(STAMP));
if (stamped.length > 1) throw new Error(`${stamped.length} sections carry ${STAMP}: report it, do not merge`);
let section = stamped[0];
if (!section) {
  section = figma.createSection();
  section.name = `${TITLE} ${STAMP}`;
  if (anchor) { section.x = anchor.x + anchor.width + GAP; section.y = anchor.y; }
}
// build the artifact's nodes inside `section`, then return [section.id, ...createdIds]
```

