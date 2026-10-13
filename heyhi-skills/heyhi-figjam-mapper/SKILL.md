---
name: heyhi-figjam-mapper
description: >-
  Turn structured design inputs the human brings into an editable FigJam artifact,
  live in the client's Figma: a flow, journey map, service blueprint, IA sitemap,
  sequence, state machine, ERD, or system architecture diagram. Routes each artifact
  type to the right Figma mechanism (generate_diagram for the types Mermaid supports;
  use_figma on FigJam for journey maps and service blueprints, which it does not) and
  reads the engagement-intake profile for voice, deliverable location, and the
  hermetic boundary. Triggers: "map this journey in FigJam", "build a service
  blueprint", "diagram this flow", "make an IA sitemap", "put this architecture in
  FigJam", "turn the research into a journey map". Produces the structure and leaves
  the design judgment (pain points, opportunities, the correctness of the taxonomy)
  as labeled empty slots behind a named human gate; any inferred node or edge is
  tagged. NOT for translating a built prototype into a Figma design file (use
  heyhi-design-bridge); NOT for building slides (use heyhi-deck); NOT for running the
  workshop itself (use heyhi-workshop); NOT for a diagram inside a Figma DESIGN file
  (call figma-use directly).
version: "0.2.0"
updated: "2026-08-23"
status: "deployed — heyhi-skills/; v0.2.0 promoted 2026-08-23 (Gate G-C, plans/plan-sheerline-skills-upgrade-2026-08-22.md) — authors evals/cases.yaml (the skill shipped with zero cases against Sheerline's own eval policy) and corrects the stale 'Draft' footer in references/artifact-recipes.md; no method change (0→6 cases). v0.1.0 promoted + lifted 2026-08-17 (DISPATCH-01). Registered in skill-registry.yaml v2.35.0 + sheerline/skills/registry/skill-registry.yaml v0.3.0. Sheerline area 11 (Collaboration & Facilitation), P1; serves gated areas 2 (Information Architecture, P3) and 13 (Service Design, D-3 2026-10-09) when those open."
classification: HeyHi Confidential
---

# HeyHi FigJam Mapper

**Sheerline area 11 (Collaboration & Facilitation) · P1 · Figma-live generation skill.** A designer or facilitator brings structured material: a flow they sketched, the stages of a journey, a service's front and back stage, an IA outline, a system's services. This skill renders it as an editable FigJam artifact the room can work on, then hands the design judgment back to the human. It is HeyHi's first skill to *generate* design artifacts (flows, journeys, blueprints, IA maps) live in Figma, as distinct from `heyhi-design-bridge`, which already writes to Figma but *translates* an existing prototype or raster into a Figma design file. It writes into the client's own board; it does not produce a picture of one.

**The boundary this skill obeys (Sheerline § 9, absolute).** A structured artifact with explicit empty judgment slots, a named human gate, and provenance labels on anything synthetic. *The empty slots are the interpretive layers:* the pain points, emotions, opportunities, and "moments that matter" on a journey or blueprint, and the correctness of an IA taxonomy itself. They are placed as labeled-but-blank cells for the human and the room to fill. Any node, edge, or label the skill infers rather than takes from the source is tagged `inferred`. The skill lays out structure; the human owns the design truth. A version of this skill that fills in the pain points or asserts the "right" IA has exceeded its charter.

> **This skill closes through the Exit Gate (`CLAUDE-SESSION-RULES.md § Exit Gate`).** See the bottom-of-skill bracket.

---

## Routing — disambiguation with sibling skills

| If the task is… | Use |
|---|---|
| Rendering a flow / journey / blueprint / IA / architecture into FigJam from known inputs | **this skill** |
| Translating a built HTML prototype into a Figma **design** file (or vectorizing a raster) | `heyhi-design-bridge` |
| Building a slide deck | `heyhi-deck` |
| Running or prepping the workshop the artifact is used in | `heyhi-workshop` |
| Extracting a Figma design system's tokens into a config | `ui-studio-onboard` |
| A diagram inside a Figma **design** file (`figma.com/design/...`) rather than FigJam | `figma-use` directly |
| Deciding what the journey / IA actually *is* | **the human** (this skill's named gate) |

This skill orchestrates Figma's own skills; it never reimplements them. It composes `figma-generate-diagram` and `figma-use` + `figma-use-figjam`.

---

## Step 0: Improvement hook check

Before running, retrieve any recurring corrections for diagramming / FigJam / IA work (`retrieve_design_corrections` if the design MCP is reachable, or the Sheerline `os/corrections/` registry). Fold a matching recurring correction into the run. Skip silently if none.

## Step 1: Load context and the engagement profile

1. **The inputs the human brought** — the flow, the research synthesis, the service description, the IA outline. This is the source of truth. Do not go invent the content.
2. **[references/artifact-recipes.md](references/artifact-recipes.md)** — the per-artifact-type mechanics (which types go through `generate_diagram`, which are built with `use_figma` on FigJam, and the FigJam recipes for blueprints, journeys, and IA trees). The method spine.
3. **The engagement-intake profile** (`sheerline/profile/engagement-intake.yaml`, filled per engagement and passed by path — never auto-discovered). Resolve and hold: `constraints.brand_voice_source` / `voice_prohibited` / `dash_rule` (label the artifact in the engagement's voice, not HeyHi's, for client work); `deliverable.root` + `deliverable.classification` (where the link and any export are filed); `boundary.hermetic_seal_confirmed` (no client name on a shared FigJam); `figma_file_key` (add to an existing file rather than spawning drafts). Echo one line: `Engagement: <label> · voice:<source> · figma:<file_key|new> · areas:<practice_areas_in_scope>`.
4. **Figma prerequisites (mandatory).** Before any `generate_diagram` call, load `figma-generate-diagram`. Before any `use_figma` call on FigJam, load `figma-use` and `figma-use-figjam`. These carry the constraints that keep the write from failing; this skill assumes them, it does not restate them.

## Step 2: Pick the artifact type, then route to the right Figma mechanism

The single technical fact that governs this skill: **`generate_diagram` supports `flowchart`, `sequenceDiagram`, `stateDiagram`, `erDiagram`, `gantt` — and does NOT support journey maps, timelines, or C4.** So journey maps and service blueprints are built with `use_figma`, not `generate_diagram`. Route accordingly:

| Artifact | Mechanism |
|----------|-----------|
| Process / task flow, decision tree, pipeline, dependency graph | `generate_diagram` — flowchart (`architecture.md` route if it is services/datastores/queues) |
| Sequence of interactions over time (API, auth, handoffs) | `generate_diagram` — sequenceDiagram |
| Named states + transitions | `generate_diagram` — stateDiagram |
| Data model / entities / keys | `generate_diagram` — erDiagram |
| **IA sitemap** (hierarchy of pages/sections) | `generate_diagram` — flowchart, top-down; OR the FigJam tree recipe if it needs annotation |
| **Journey map** (stages × dimensions grid) | `use_figma` + FigJam — the journey-grid recipe (a table + labeled empty rows) |
| **Service blueprint** (customer action / frontstage / backstage / support, across time) | `use_figma` + FigJam — the swimlane recipe (sections + stickies + connectors) |

## Step 3: Gather ground truth before drawing — no invented edges

The quality of the artifact is bounded by the quality of the inputs. Pull real names, real steps, real edges from the source the human brought (code, PRD, research synthesis, an existing FigJam via `get_figjam`). **Do not invent nodes, edges, or labels to round out the picture.** A missing step is a gap to flag to the human, not to fill. Anything you must infer to connect the structure is tagged `inferred` on the artifact. This is the provenance half of the § 9 boundary, and it is also `figma-generate-diagram`'s own rule.

## Step 4: Generate, and place the judgment slots empty

- **generate_diagram path.** Write clean Mermaid per the constraints in `figma-generate-diagram` (camelCase node ids, quote any special characters, no emojis / `\n` / HTML, supported types only). Pass `figma_file_key` when the profile names one so the artifact lands in the engagement's file. Reuse the same file when iterating.
- **use_figma + FigJam path.** Build the blueprint or journey per `references/artifact-recipes.md`: the blueprint from FigJam sections + stickies + connectors (lanes, content, wiring), the journey from a table with labeled empty rows. Follow the canonical font-load recipe and return every created node id.
- **Place the empty judgment slots.** On a journey or blueprint, add the pain-points row, the emotion row, and the opportunities row as **labeled, empty** cells or stickies. Do not fill them. They are for the room.
- **Label inference.** Tag any inferred node/edge/label `inferred`.

## Step 5: Verify and hand off

Inspect with `get_figjam` (not `get_metadata`, which is design-only) and `get_screenshot` on a node id. Confirm: the structure matches the source, no invented edges crept in, the judgment slots are empty and labeled, inferred content is tagged, and — if the file is shared — no client name appears on the board (hermetic seal). Return the FigJam link as a markdown link. Note where the deliverable is filed per `deliverable.root`.

---

## What is explicitly out of scope

- **The design truth.** Whether the IA is right, what the real pain points are, which moments matter — empty slots by construction (§ 9). The skill structures what is known; it does not decide what is true.
- **Inventing content** to complete a thin artifact. A gap is a flag, not an invitation to fabricate.
- **Building the prototype or UI** — `heyhi-ui-ux` / `heyhi-design-bridge`. **Running the session** — `heyhi-workshop`. **The deck** — `heyhi-deck`.
- **Design-file diagrams** (`figma.com/design/...`) — `figma-use` directly; this skill is FigJam (`figma.com/board/...`).

---

## Exit Gate Required Headers (bottom-of-skill bracket)

This skill closes through the Exit Gate Flavor A (`CLAUDE-SESSION-RULES.md § Exit Gate`). Before declaring done, confirm every header below carries real content, not a claim:

- `## Fixes Applied` — artifact(s) produced, with the FigJam link and the artifact type.
- `## Smoke Test` — the Step 5 verification: structure matches source, judgment slots empty, inferred labels present, hermetic seal held.
- `## Next Session Prompt` — the judgment slots the room still needs to fill, and any gap flagged in Step 3.

---

*HeyHi Confidential. Sheerline area 11 (Collaboration & Facilitation), P1. v0.1.0 deployed 2026-08-17 (#666/#673). v0.2.0 staged 2026-08-23 (Wave D, `plans/plan-sheerline-skills-upgrade-2026-08-22.md`) — evals authored, footer corrected, no method change. Spec source: `ai-services/design-intelligence/research/sheerline-skill-buildout-research-2026-08-09.md`; eval gap identified in the 2026-08-22 skills audit § 2.3. Boundary: § 9.*
