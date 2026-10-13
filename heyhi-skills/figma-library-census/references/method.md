---
classification: confidential
title: "figma-library-census: crosswalk and classification method"
created: "2026-09-07"
---

# The crosswalk and the classification

The census (SKILL.md steps 1 to 3) produces two join tables and a style list: `figma-library-map.json` (component/style name → published key + property axes) and `figma-variable-map.json` (variable name → key, resolved type, modes, code syntax). This reference covers steps 4 and 5: the crosswalk against the served code manifest (`ds-map.json`), and the candidate atomic classification. The schemas are in `../schemas/`; the worked example is in `worked-example/`.

## Step 4, the crosswalk

The crosswalk joins the Figma component census against the served code component manifest and records a coverage state per component. **The code side is retrieved through the per-system instance, never read from disk** (`retrieve_design_context` for the component list and token maps; `retrieve_design_relationships` with `query_type: component_uses` for containment where it exists). The join key is the component name, reconciled across naming conventions (a `figma-only` or `code-only` row that is really a naming mismatch is surfaced for the human, not silently merged).

Coverage states (the `coverage` enum):

| State | Meaning | How it is detected |
|---|---|---|
| `both` | present in the Figma library and the served manifest | name matches on both sides |
| `code-only` | in the served manifest, no Figma component | name in the manifest, absent from the Figma census |
| `figma-only` | a Figma component with no manifest entry | name in the Figma census, absent from the manifest |
| `divergent` | present in both, but a mechanically detected disagreement | a bound token or a property axis differs between the Figma component and the manifest entry |

`divergent` is a detection, not a verdict. The census flags that Figma and code disagree (for example a variant binds `text-primary` where the manifest's token map says `accent-primary`); **which side is correct is the human's call at the crosswalk-review gate.** `token_refs[]` on each row is copied from the served manifest's token map for that component, so the reviewer sees what the component references without opening the manifest.

## Step 5, the candidate atomic classification

Each row gets a candidate `level` in `token / atom / molecule / organism / template`, with `level_confirmed: false`. The level is derived, in this priority:

1. **Figma composition (primary for a censused library).** Walk the component's variant subtree for nested library-component INSTANCE nodes. A leaf that nests no other library component (only primitives, text, vectors, or an icon swap) is an **atom**. A component that nests atoms is a **molecule**; one that nests molecules is an **organism**; a full screen or page composed of organisms is a **template**. **An `INSTANCE_SWAP` of a leaf or icon component does not promote an atom**, a Button with a swappable Icon is still an atom.
2. **Served-graph containment (refines, where the manifest encodes it).** `retrieve_design_relationships` `component_uses` returns `child_components` with a hop distance and `children_count`; a manifest that encodes `contains` lets the graph confirm or deepen the Figma-derived level.
3. **Cross-surface recurrence (raises toward a pattern).** A composition that recurs across surfaces or pages is a candidate design pattern (it feeds the pattern ledger in Lanes E and I); recurrence raises the candidate level regardless of local nesting depth.

`token` level is for a row that represents a raw token used directly rather than a component.

### Honest limit of the graph signal (2026-09-07)

The reference instance's served graph currently encodes **zero containment**: `heyhi-mcp/data/components.json` has no `contains` field, and the adapter hardcodes `"contains": []` for every component, so `component_uses` returns `children_count: 0` for every production component (containment edges exist only in the built-in Modal/Table/Form fixture, one level deep). On the worked example, therefore, **signal 1 (Figma composition) is authoritative** and signal 2 is empty. The graph `contains_component` route is the path for a client manifest that DOES encode containment; the census does not invent containment the manifest omits. This is why every level is a candidate and the gate is a human's.

## Worked example (the instance's own served system + its 2026-09-04 generated library)

Ran read-only against the scratch library, Figma plan tier Pro, 2026-09-07. Full census and real keys are in the gitignored proof record; the file key and every asset key (component, variable, style) are redacted to name-derived placeholders in the tracked worked example, because the real 40-char hex keys read as high-entropy secrets to the scanner and are engagement-specific. See `worked-example/figma-library-map.json`, `figma-variable-map.json`, `ds-map.json` (all validate against the schemas).

**The Figma side (`figma-library-map.json`).** Two published components, the `Button` COMPONENT_SET (27 variants; Style × Size × State plus Label / Show Icon / Icon) and a standalone `Icon/ChevronRight` COMPONENT, 18 styles (12 text, 6 effect), and 157 variables across 4 collections (`figma-variable-map.json`). Every variable is local (`remote:false`) with a WEB code syntax and explicit scopes.

**The code side (served).** The reference instance's manifest carries 31 components (Button, Input, Card, Alert, Modal, Navigation, Badge, Table, Tooltip, Form, and 21 more), retrieved through the instance.

**The crosswalk (`ds-map.json`), true coverage counts:**

| coverage | count | rows |
|---|---|---|
| `both` | 1 | Button |
| `figma-only` | 1 | Icon/ChevronRight |
| `code-only` | 30 | Input, Card, Alert, Modal, … (the manifest's other 30) |
| `divergent` | 0 | the token-binding sub-check was not run in this read; flagged for the gate (the 2026-09-04 proof recorded a candidate secondary-text token disagreement) |

**The classification.** Button is a candidate **atom**, it nests only a swappable Icon, and an icon swap does not promote an atom (this is smoke-test 5's expected result). Icon is a candidate atom. The code-only rows carry candidate levels read from the served manifest's own structure (Input atom, Card molecule, Alert molecule, Form molecule, Modal organism, …); because the graph encodes no containment (above), those levels rest on the manifest structure and the human's judgment, all `level_confirmed: false`. The worked example lists Button, Icon, and 6 representative code-only rows; the full 32-row crosswalk is in the proof record.

## Empty slots and the gate

The census fills no judgment. It hands the reviewer:

- **Token conflicts (which wins).** A `divergent` row, or a `dtcg_token` candidate that does not match, is flagged; the census does not pick a winner.
- **Naming reconciliation.** A `figma-only` / `code-only` pair that is really one component under two names is surfaced, not merged.
- **The level names the client uses.** `atom / molecule / organism / template` is HeyHi's vocabulary; the client may use another. The candidate level is labeled, never imposed.

**Named gate: the crosswalk review.** A human confirms the coverage reconciliations, adjudicates every `divergent` row and `dtcg_token` mismatch, and sets `level_confirmed: true` per row. No level, no token-conflict resolution, and no naming merge is recorded until that review is signed.

*HeyHi Confidential.*
