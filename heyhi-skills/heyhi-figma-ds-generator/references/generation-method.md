# heyhi-figma-ds-generator — generation method

*The method spine. Loaded on demand, not at session start (Earn the Room). SKILL.md is the procedure; this file carries the mechanism decision, the input/output contracts, the engine phase mapping, the transport constraints, and the re-run rules.*

*classification: HeyHi Confidential*

---

## 1. The mechanism — `use_figma`, orchestrating the Figma-native engine

**The write path is `use_figma`**, and the skill orchestrates Figma's own two skills: `figma-generate-library` (the WHAT to build and in WHAT ORDER) over `figma-use` (the Plugin-API HOW). Both are loaded before any write — `figma-generate-library`'s own Prerequisites require `figma-use` for every `use_figma` call. This skill supplies only the Sheerline overlay (the engagement-intake resolution, the § 9 human-gate/provenance boundary, the Exit Gate close); it never re-implements the Plugin API. When a `use_figma` call runs under the engine, include the engine skill in `skillNames`, prefixed `resource:` if it was loaded via the MCP resource (`resource:figma-generate-library`).

**`generate_figma_design` is rejected**, for two independent reasons:
1. **Wrong tool.** It captures an existing *rendered web view* into Figma (code-to-design of a page that already exists). This skill builds a design system from a served token/component contract — there is no rendered view to capture.
2. **Absent from the live manifest.** The Figma MCP *server description* advertises `generate_figma_design`, but no callable tool schema for it appears in the live `mcp__cc3b9073…` manifest (verified this build: the callable set is `use_figma`, `create_new_file`, `generate_diagram`, the `get_*` readers, `upload_assets`, `download_assets`, Code-Connect tools, `whoami` — no `generate_figma_design`). Its schema cannot be loaded here.

**Runtime-verify, do not trust the tool list.** The Figma MCP has no changelog — the surface must be probed. Phase 0 confirms `use_figma` is reachable (`whoami` / a read-only `use_figma`) before any write, and treats CLAUDE.md's tool list as a hint, never ground truth.

---

## 2. The input contract — what is served, and from where

### 2.1 The served design-system surface (reached through the MCP boundary — Invariant 4)

Retrieved, never pasted into context, never embedded in `sheerline/` (`sheerline/os/foundations/design-systems/FOUNDATION.md`: *"the design system is retrieved, not pasted"*). The rows below name the instance's own served DS (the v1 target); for another engagement, `design_system.source` / `serves_via_mcp` (§ 2.3) resolve the equivalent surfaces, retrieved the same way:

| Surface | Tool / path | Supplies |
|---|---|---|
| Always-loaded meaning layer | `design-system://summary` | the intent layer over the token/component set |
| Universal reasoning layer | `design-system://fundamentals` | the binding UX laws, control-state contract, conflict order |
| The token **registry** | `heyhi-website/public/DESIGN.md` | token **names** (kebab), DTCG-style **types**, role/usage descriptions, the **primitive palette (hex)**, and a 31-name **component index** — see 2.2 |
| Concrete values / specs / patterns | `retrieve_design_context` | the resolved values, the primitive→semantic resolution, the CSS variable names, and the component specs to build |
| Impact / dependency | `retrieve_design_relationships` | which tokens a component binds (dependency order for Phase 3) |
| Worked usage examples | `retrieve_design_examples` | do/don't + samples for a component |
| Recurring drift corrections | `retrieve_design_corrections` | what has been learned about a token/component (folds into Step 0) |
| Contract-compliance validation | `validate_output` | validate a produced/exported artifact (not the Figma canvas) against the served contract |

### 2.2 What `DESIGN.md` actually is — and what it is not (verified this build)

`DESIGN.md` declares `token_spec: "DTCG 2025.10"` but is **a flattened human-readable registry, not DTCG token objects.** It has **no** per-token `$value`, `$description`, `$type`, `var(--…)` code-syntax, or `{alias}` edges. Each token is a single string `"<type> — <value/usage prose>"`. Concretely:

- **What it carries:** the ~124 kebab-case token names (semantic + scale) with an embedded type word (`color` / `typography` / `dimension` / `duration` / …) and a usage/role description; for *scale* tokens the value is embedded in prose (`space-1: "dimension — 4px …"`, `body: "typography — 1rem/400 …"`); the **primitive palette** as `path: #HEX` bullets in the body (the only resolved hex present); a bare **component index** (31 names); and Do's/Don'ts constraints.
- **What it does NOT carry:** resolved values for **semantic color** tokens (no hex on `accent-primary`); the alias edges (described in prose, not encoded); the **CSS variable names** for the `var()` code syntax; and **component specs** (prop schemas, variants, sizes, a11y). `DESIGN.md` itself points to the MCP for these: *"Full prop schemas, variants, sizes, accessibility requirements, and usage guidance are served by the heyhi-mcp server (`retrieve_design_context`, `retrieve_design_examples`)."*

**Consequence for the build.** Use `DESIGN.md` for *what exists and what it means* (the registry + the primitive hex + the component index). Use `retrieve_design_context` for *what to build it from* (resolved semantic values, primitive→semantic resolution, component specs, and the CSS variable names). The `var()` code syntax comes from the served CSS / `retrieve_design_context` — **never** guessed from the token name. Where a token→CSS-var mapping cannot be confirmed, it is a Phase-0 gap to flag, not an inference to ship (SKILL.md § human-gated slots).

### 2.3 The engagement-intake resolution (`sheerline/profile/engagement-intake.yaml`)

A **tracked blank template**; the filled instance lives at `engagement-intake.yaml` in the instance's engagement folder (gitignored) and is **passed by path at run time, never auto-discovered**. Field names/nesting as they exist on disk:

| Field (exact path) | Governs |
|---|---|
| `design_system.source` / `.token_spec` / `.serves_via_mcp` | where the DS truth is; whether it is retrieved through the MCP |
| `design_system.figma_file_key` | the **target** DS file (a saved cloud key — see § 3, the local-file refusal) |
| `design_system.figma_app_file_key` | optional separate app/screens file (out of v1 scope) |
| `design_system.component_source` / `.component_format` / `.component_inventory` | the component catalog (`json-manifest \| storybook \| code \| figma \| none`) and the named components in scope |
| `design_system.description_target` | where field/token descriptions get written (`DTCG $description \| a DESIGN.md tokens: block \| field_provenance`) |
| `practice_areas_in_scope` | the area ids this engagement touches (Phase 0d scope input) |
| `deliverable.root` / `.classification` | where the link + any export are filed; the footer scheme |
| `constraints.brand_voice_source` / `.voice_prohibited` / `.dash_rule` | doc-page copy in the **client's** voice, never HeyHi's; the resolved banned-word list; the em-dash policy |
| `constraints.do_not_automate` | engagement-specific judgment that stays human, on top of the standing line |
| `boundary.retained_moat_touched` | flags a run that would touch the evaluator / populated corpus / calibration |
| `boundary.hermetic_seal_confirmed` | no client name on a shared file |

*(Note: `component_inventory` is nested under `design_system`, not top-level; `boundary` lists `retained_moat_touched` before `hermetic_seal_confirmed`. The template also carries `design_system.known_drift`, `constraints.accessibility_target`, and the `engagement` / `remediation` blocks, not used by this skill.)*

**Phase-0 mapping.** The served surface (§ 2.1) is the "codebase" the engine analyzes in **0a**; `figma_file_key` is the file inspected in **0b**; `get_libraries` runs **0c**; `practice_areas_in_scope` + `component_inventory` lock scope in **0d**; served-truth vs. the existing Figma file is the conflict source in **0e**; **0f** prints the gap analysis (the approval surface).

---

## 3. The engine phase order (`figma-generate-library` § 2), and this skill's map onto it

The engine is a **20–100+ sequential `use_figma` call** workflow with a disk-backed state ledger, validate-between-steps, and one focused unit per call. Its five phases map 1:1 onto this skill:

- **Phase 0 — Discovery (no writes).** Capability check + local-file refusal first (SKILL.md Step 2); then 0a analyze the served surface → 0b inspect the target Figma file → 0c `get_libraries` then `search_design_system` → 0d lock v1 scope → 0e map + record every conflict → 0f print the gap analysis. **This whole phase can run unattended** (retrieval, discovery, the plan); the canvas writes cannot.
- **The pre-write gate (Earn the Room).** Print the 0f gap analysis + 0d scope + the collection/variable/style/component plan; get approval before Phase 1. The write path is app-brokered with no replayable config (§ 4), so a human approves the plan and initiates the write.
- **Phase 1 — Foundations (variables first).** Collections + modes (§ 8 token architecture); primitive variables (raw values, 1 mode); semantic variables aliased to primitives and mode-aware; **scopes on every variable, never `ALL_SCOPES`**; **`WEB` code syntax on every variable** = the real CSS variable name in a `var()` wrapper (from the served CSS / `retrieve_design_context`, § 2.2); then effect styles + text styles.
- **Phase 2 — File structure.** Page skeleton `Cover → Getting Started → Foundations → --- → Components → --- → Utilities`; foundations docs (color swatches, type specimens, spacing bars), each `get_screenshot`-verified.
- **Phase 3 — Components, one at a time, dependency order (atoms → molecules).** Base component (auto-layout + full variable bindings, no hardcoded fills/strokes) → all variant combinations (`combineAsVariants`, then grid-laid-out — they stack at (0,0) until positioned) → component properties (`TEXT`/`BOOLEAN`/`INSTANCE_SWAP`) bound to child nodes → page docs → validate (`get_metadata` + `get_screenshot`). `INSTANCE_SWAP` for icons, never a variant per icon; cap a variant matrix at 30 combinations.
- **Phase 4 — Integration + QA.** Code Connect (optional), accessibility spot-check, naming audit, unresolved-bindings audit, final screenshots.

---

## 4. Transport constraints (hard, every call)

The native transport for a DS build is the engine's many-small-sequential-calls pattern — **not** design-bridge's bundled-plugin transport, which exists because Translate lands a whole page in a few large chunks. But the design-bridge live-write lessons still bind every call here. Attribution is exact so the next author can trace each rule:

| Constraint | Where it is authoritative | The rule |
|---|---|---|
| **50,000-char per-call cap** | `heyhi-design-bridge` v0.8.0 (SVG dedup as the primary lever; SVGO `-p 2` complementary); seeded v0.6.0 F3 | Each `use_figma` payload must clear 50k projected chars. The phased unit-per-call structure keeps calls small; if a unit (e.g. a component with a dense embedded SVG) would exceed the cap, import the unique SVG **once** as a component and reuse by instance (dedup), and/or shrink the master — never emit an over-cap chunk. |
| **Never parallelize `use_figma`** | `figma-generate-library` § 3 **rule 13** (literal) | Figma state mutations are strictly sequential. Even a tool that supports parallel calls must issue these one at a time. design-bridge's corollary (v0.6.0 F1): a cross-call read of a just-created node can hit replication lag — `setCurrentPageAsync` first, then read, then guard-and-retry. |
| **Font preflight before any text write** | `heyhi-design-bridge` v0.14.0 (`preflight_fonts.py`); seeded v0.6.0 F4 | Resolve every `(family, weight)` — inline runs included — against `listAvailableFontsAsync()` first; capture the exact Figma style-name spelling (they differ per family). A silent typeface substitution is invisible until the render. |
| **Create-only Variable writes** | `heyhi-design-bridge` v0.6.0 **F2** (`doVariable`) | On a re-run that reuses an existing (possibly canonical) collection, set a Variable's value on **create only** — never clobber a reused canonical Variable with a low-confidence value. A deliberate change to an existing Variable is then an explicit act, not a silent side effect. |
| **Disk-backed state ledger** | `figma-generate-library` § 4 (`/tmp/design-system-state-{RUN_ID}.json`); design-bridge's `run-state.json` is the same idea across sub-agents | Write `{key → id}` to disk and re-read it every turn; conversation context truncates across a long build. |
| **Never hallucinate node IDs** | `figma-generate-library` § 3 **rule 14** (literal) | Read every ID from the ledger / a prior call's return, never from memory. design-bridge threads returned ids via its `__IDMAP__` mechanism. |
| **Rebind on a clone: clear, then bind from the resolved value** | Live proof, 2026-09-04 (the instance's own design system) | A clone whose fill is already bound to variable X, re-assigned a paint bound to the *same* X via `setBoundVariableForPaint` over a black base, reads as bound but renders the base colour. Set `fills = []` first, then bind a paint whose base colour is the resolved value. Screenshot every variant grid; a per-node binding audit alone reported these as bound. |
| **`resize()` resets sizing to FIXED** | Live proof, 2026-09-04 | An auto-layout doc frame sized with `resize(1440, 1)` renders 1px tall until `layoutSizingVertical = 'HUG'` is set *after* the resize. Applies to every nested auto-layout frame built the same way. |
| **Stroke-weight bindings read back per side** | Live proof, 2026-09-04 | `setBoundVariable('strokeWeight', v)` stores as `strokeTopWeight` / `strokeBottomWeight` / `strokeLeftWeight` / `strokeRightWeight` in `boundVariables`; an audit that checks the `strokeWeight` key reports a false unbound. |

**On the bundled-plugin transport.** `heyhi-design-bridge` built a bundled-plugin transport (`scripts/transport/emit_plugin.py`, v0.9.0) **out of necessity** for its whole-page write model: `use_figma` has no scriptable endpoint (the write-capable connector is app-brokered with no replayable config), its sandbox has no network, and a plugin's main thread blocks `eval` — so a bundled plugin was the only faithful path for a whole-page replay. This skill's **v1** deliberately uses the engine's native per-unit `use_figma` calls, human-initiated. Adopting a bundled-replay transport so this skill's **whole DS build** runs unattended is a **v2 direction**, and it also requires clearing the Earn-the-Room human-initiation gate (SKILL.md Step 3 + the human-gated slots) — it is not merely a transport swap.

---

## 5. The output contract — real Figma constructs

### 5.1 Variables (Phase 1)
- **Collections + modes** per § 8 (token architecture): `Primitives` (1 mode) · `Color` (Light / Dark) · `Spacing` (1 mode) · `Typography` (1 mode). Scale to more semantic collections / modes only above the § 8 thresholds.
- **Primitive → semantic aliasing:** semantics are `VARIABLE_ALIAS` to primitives, never duplicated raw values.
- **Scopes on every variable — never `ALL_SCOPES`.** Background `FRAME_FILL, SHAPE_FILL`; text `TEXT_FILL`; border `STROKE_COLOR`; spacing `GAP`; radius `CORNER_RADIUS`; primitives hidden `[]`.
- **`WEB` code syntax on every variable** = the real CSS variable name with the `var()` wrapper (`var(--accent-primary)`), from the served CSS / `retrieve_design_context` — not a guessed name (§ 2.2).

### 5.2 Styles + components
- **Effect styles** (shadows) + **text styles** (typography), named to the file's convention.
- **Components** in dependency order, one per `use_figma` call: base (auto-layout + full variable bindings) → all variant combinations (`combineAsVariants`, then grid-laid-out) → component properties (`TEXT`/`BOOLEAN`/`INSTANCE_SWAP`) linked to child nodes. Variant matrix capped at 30; `INSTANCE_SWAP` for icons.

### 5.3 File structure + docs
- Page skeleton `Cover → Getting Started → Foundations → --- → Components → --- → Utilities`; foundations docs (color swatches, type specimens, spacing bars), each `get_screenshot`-verified.

---

## 6. Token architecture thresholds (`figma-generate-library` § 8)

| Served token count | Pattern |
|---|---|
| < 50 | Single collection, 2 modes (Light/Dark) |
| 50–200 | **Standard**: `Primitives` (1 mode) + `Color` semantic (Light/Dark) + `Spacing` (1 mode) + `Typography` (1 mode) |
| 200+ | **Advanced**: multiple semantic collections, 4–8 modes |

The instance's own served DS in the first live proof (~124 canonical tokens per its `DESIGN.md`) sat in the **Standard** band, so that proof used that pattern.

---

## 7. Re-run / idempotency

- **Idempotency check before every create** (`figma-generate-library` § 4) — query by name + state-ledger ID; if it exists, skip or update, never duplicate.
- **Find-or-create** for collections and Variables so a re-run reuses rather than duplicates; **create-only value writes** on a reused canonical collection (§ 4).
- **Deterministic naming** for idempotent cleanup and resumability; cleanup identifies nodes by returned ID / name convention, never by prefix-guessing (`figma-generate-library` § 3 rules 10–11).
- **Resume protocol:** on a fresh session or after context truncation, run a read-only `use_figma` to reconstruct the `{key → id}` map, then re-read the disk ledger.

---

*HeyHi Confidential. Reference for `heyhi-figma-ds-generator` (Sheerline area 7). Engine: Figma's `figma-generate-library` (§ references above) + `figma-use`. Live-write lessons: `heyhi-skills/heyhi-design-bridge/` (versions cited inline). Spec source: `plans/plan-ds-into-figma-generator-2026-08-29.md`.*
