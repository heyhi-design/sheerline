---
name: heyhi-figma-ds-generator
description: >-
  Generate a design system live into a Figma design file from HeyHi's served
  design-system contract: variable collections and modes (primitives → aliased,
  mode-aware semantics), token styles (effect + text), and a component/variant
  library with bound properties — scoped by the engagement-intake profile. It
  orchestrates Figma's own figma-generate-library + figma-use skills over
  use_figma; it never reimplements the Plugin API. Triggers: "generate the design
  system into Figma", "build our design system as a Figma library", "create the
  variable collections, token styles, and component library in Figma from our
  tokens", "stand up the design system in a Figma design file", "generate the DS
  variables and components in Figma from the served contract". Produces the
  system substrate and leaves the judgment (value conflicts, reuse-vs-rebuild,
  scope, an inferred taxonomy, and the craft critique of the result) as labeled
  empty slots behind a named human gate; anything inferred is flagged. NOT for
  translating a built HTML prototype or vectorizing a raster into a Figma design
  file (use heyhi-design-bridge); NOT for generating a flow, journey map, service
  blueprint, or IA sitemap into a FigJam board (use heyhi-figjam-mapper); NOT for
  auditing or drift-detecting an existing design system — it reads, never writes
  (use heyhi-design-intelligence-audit); NOT for repairing audit findings back
  into the file (use heyhi-drift-repair — this skill builds, that one repairs);
  NOT for composing a brand book / identity file from finished art — cover, logo
  lockups, illustration (use the heyhi-figma-identity-file candidate — this builds
  the DS substrate, not a book of placed art); NOT for extracting tokens FROM
  Figma into a config, the opposite direction (use ui-studio-onboard); NOT for
  building the interface that consumes the DS (heyhi-ui-ux for HeyHi pages,
  ui-studio for client UI).
version: "0.1.0"
updated: "2026-09-04"
derived_exports:
  - repo: "a private derived repo (named in staged_at's DERIVED_FROM.md)"
    cut_from: "0.1.0"
    exported: "2026-09-09"
    staged_at: "releases/private/figma-ds-generator/"
    rule: "one-way: this file is canonical; changes in the export come back through skill-updates/"
status: "deployed 2026-09-04 — heyhi-skills/heyhi-figma-ds-generator/; registered in the main registry and the Sheerline area-7 subset registry. Built 2026-09-01 from plans/plan-ds-into-figma-generator-2026-08-29.md (DISPATCH-01), staged PR #749, promoted in the 2026-09-04 promotion pass after the spec § 8.1 live proof on the instance's own design system ran green (4 collections / 157 variables / 18 styles / a 27-variant Button, re-run reuse proven; record in the instance's engagement folder). Sheerline area 7 (Design Systems), build class N (net-new). Release tier: buildable-now-internal-first — any designer-facing external surface is D-3-gated (2026-10-09)."
classification: HeyHi Confidential
---

# HeyHi Figma DS Generator

**Sheerline area 7 (Design Systems) · build class N · Figma-live generation skill.** It writes a production-grade design system into a **saved cloud** Figma design file — variable collections (primitives → aliased semantics, mode-aware), token styles, and a component/variant library — from HeyHi's served design-system contract, scoped by the engagement-intake profile. It is area 7's first **write verb**: the eleven existing DS skills all read, audit, validate, or grade a system; none writes one into Figma. It closes the `generate × design-file × design-system` cell that `heyhi-design-bridge` (translate → design file) and `heyhi-figjam-mapper` (generate → FigJam board) leave open.

**The boundary this skill obeys (Sheerline § 9, absolute).** A structured artifact with explicit empty judgment slots, a named human gate, and provenance labels on anything synthetic. The charter is one sentence: *a capability that fills its own judgment slot has exceeded its charter* (`sheerline/os/operating-principles.md` § Design Constraints (the fill); the net-new-skill form is in `sheerline/skills/README.md`). The empty slots here are the **value conflicts** (code ≠ Figma), the **reuse-vs-rebuild** call, the **v1 scope lock**, an **inferred taxonomy** the served contract is silent on, and the **craft critique** of the produced library. The skill builds the substrate and hands those decisions back. A version that resolves a conflict silently, or grades the library, has overstepped. Applied as a build-time test: *does any step below fill one of the slots in [§ The human-gated slots]?* If so, stop.

> **This skill closes through the Exit Gate (`CLAUDE-SESSION-RULES.md § Exit Gate`), Flavor A.** See the bottom-of-skill bracket.

---

## Routing — the cell this occupies, and its siblings

| If the task is… | Use |
|---|---|
| **Generate** the design system (variables + token styles + component library) into a Figma **design file** from the served contract | **this skill** |
| Translate a built HTML prototype, or vectorize a raster, into a Figma design file | `heyhi-design-bridge` |
| Generate a flow / journey / blueprint / IA into a FigJam **board** | `heyhi-figjam-mapper` |
| Audit / drift-detect an existing DS (reads, never writes) | `heyhi-design-intelligence-audit` |
| Repair audit findings back into the file | `heyhi-drift-repair` — this **builds**, that **repairs** |
| Compose a brand book / identity file from finished art (cover, logo, illustration) | `heyhi-figma-identity-file` candidate (Compose) |
| Extract tokens **from** Figma into a config (opposite direction) | `ui-studio-onboard` |
| Build the interface that **consumes** the DS | `heyhi-ui-ux` (HeyHi) / `ui-studio` (client) |
| Decide the taste, the conflict winner, the taxonomy | **the human** (this skill's named gate) |

This skill orchestrates Figma's own skills; it never reimplements them. It composes `figma-generate-library` (the WHAT + the phase order) over `figma-use` (the Plugin-API HOW).

---

## Step 0: Improvement hook check

Before running, retrieve any recurring corrections for design-system / Figma-generation / variable-and-component work (`retrieve_design_corrections` if the design MCP is reachable, or the Sheerline `os/corrections/` registry). Fold a matching recurring correction into the run. Skip silently if none.

## Step 1: Load context, the served contract, and the engagement profile

1. **The Figma engine skills (mandatory before any write).** Load `figma-generate-library` **and** `figma-use` — the generate-library skill's own Prerequisites require both for every `use_figma` call. They carry the Plugin-API constraints (return pattern, page-reset-once-per-call, ID return, font loading, 0–1 color range) and the phase discipline; this skill assumes them, it does not restate them. When a `use_figma` call runs under this skill, include the engine skill in `skillNames`, prefixed `resource:` if it was loaded via the MCP resource (`resource:figma-generate-library`).

2. **The served design-system contract — reached through the MCP boundary** (area-7 FOUNDATION, Invariant 4: *retrieved, never pasted, never embedded in `sheerline/`*). This is the "codebase" the engine analyzes in Phase 0. The surfaces below are the instance's own served DS (the v1 target); for another engagement the same *kinds* of surface resolve from `design_system.source` / `serves_via_mcp` (item 3) and are retrieved the same way. Retrieve, do not inline:
   - `design-system://summary` and `design-system://fundamentals` — the always-loaded meaning + reasoning layers.
   - `retrieve_design_context` — token values, component specs, patterns.
   - `retrieve_design_relationships` — which tokens a component binds (the dependency order for Phase 3).
   - `retrieve_design_examples` — do/don't + worked samples for a component.
   - `heyhi-website/public/DESIGN.md` — the served token **registry**: token names, DTCG-style types, role/usage descriptions, the primitive palette (hex), and a 31-name component index. It is a flattened Markdown registry, **not** DTCG token objects — it carries no per-token `$value`/`$description`/`var()` code-syntax. The concrete values, the primitive→semantic resolution, the component specs, and the real CSS variable names come from `retrieve_design_context` (DESIGN.md itself points there). Use DESIGN.md for *what exists and what it means*; use `retrieve_design_context` for *what to build it from*.
   - `validate_output` — validate a produced/exported artifact (e.g., token descriptions written per `description_target`) against the served contract before hand-off. It checks contract compliance, **not** the Figma canvas (that is `get_metadata` + `get_screenshot`, Step 5).

3. **The engagement-intake profile** (`sheerline/profile/engagement-intake.yaml` is a tracked blank **template**; the filled instance lives in the instance's engagement folder (gitignored) and is **passed by path at run time, never auto-discovered**). Resolve and hold:
   - `design_system.source` / `token_spec` / `serves_via_mcp` — where the DS truth is, and whether it is retrieved through the MCP.
   - `design_system.figma_file_key` — the **target** DS file (must be a **saved cloud** key — see Step 2, the local-file refusal).
   - `design_system.figma_app_file_key` — optional separate app/screens file (out of v1 scope — see § out of scope).
   - `design_system.component_source` / `component_format` / `component_inventory` — the component catalog and the named components in scope.
   - `design_system.description_target` — where token/field descriptions get written (DTCG `$description` | a `DESIGN.md tokens:` block | `field_provenance`).
   - `practice_areas_in_scope` — the areas this engagement touches (Phase 0d scope input).
   - `deliverable.root` / `deliverable.classification` — where the link + any export are filed; the footer scheme.
   - `constraints.brand_voice_source` / `voice_prohibited` / `dash_rule` — doc-page copy in the **client's** voice, never HeyHi's; the resolved banned-word list; the em-dash policy.
   - `constraints.do_not_automate` — engagement-specific judgment that stays human, on top of the standing line.
   - `boundary.hermetic_seal_confirmed` — no client name on a shared file.
   - `boundary.retained_moat_touched` — flags a run that would touch the evaluator / populated corpus / calibration.

   Echo one line: `Engagement: <label> · voice:<source> · figma:<file_key|LOCAL→refuse> · areas:<practice_areas_in_scope> · seal:<bool>`.

Full input/output contract detail, the transport constraints, and the token architecture live in **[references/generation-method.md](references/generation-method.md)** — the method spine, loaded on demand.

## Step 2: Phase 0 — Discovery (no writes yet)

Run the engine's Phase 0 (`figma-generate-library` § 2), which writes nothing:

- **Capability check first.** The Figma MCP has no changelog — the surface must be probed, not trusted. Confirm `use_figma` is reachable (`whoami` / a read-only `use_figma`) before planning any write. Treat CLAUDE.md's tool list as a hint, never as ground truth. Do **not** use `generate_figma_design` — it is for first-time capture of an existing rendered web view, not a DS build from a contract, and it has no callable schema in the live manifest.
- **Refuse a local file.** `use_figma` needs a saved cloud file. If `figma_file_key` resolves to an unsaved/local key (a `figma.com/design/new?…&localFileKey=LOCAL_…` URL), `use_figma`/`get_metadata` return "don't have edit access". Refuse to write; ask for the saved `figma.com/design/<fileKey>` URL. Do not loop on the failing write.
- **0a–0e:** analyze the served surface (the "codebase"); inspect the target Figma file; `get_libraries` then `search_design_system`; lock the v1 scope (`practice_areas_in_scope` + `component_inventory`); map served-truth → Figma and record every conflict.
- **0f:** print the **gap analysis** to chat — what exists in the contract but not Figma, what exists in Figma but not the contract, and every conflict with its (proposed) resolution.

## Step 3: The pre-write gate (the load-bearing human gate)

Before Phase 1 writes anything, print the **pre-write plan** to chat and get approval: the 0f gap analysis + the 0d locked scope + the planned collections / variables / styles / components. This is the Earn-the-Room approval artifact — read-only, it writes nothing. The write path is app-brokered with no replayable config, so a human approves the plan and initiates the write. Surface every § 6 fork that is live (below); do not resolve one to keep moving.

## Step 4: Generate — the engine's phase order, judgment slots left empty

Run the engine phases in order (`figma-generate-library` § 2), one focused unit per `use_figma` call, validating between steps. Carry the transport constraints (full table in the reference; the load-bearing few restated):

- **Phase 1 — Foundations (variables first).** Collections + modes per the § 8 token architecture (`Primitives` 1-mode · `Color` Light/Dark · `Spacing` 1-mode · `Typography` 1-mode; scale up only when the served token count crosses the § 8 thresholds). Semantics are `VARIABLE_ALIAS` to primitives — never duplicated raw values. **Scopes on every variable, never `ALL_SCOPES`.** **WEB code syntax on every variable** = the real CSS variable name wrapped in `var(--…)`, taken from the served CSS / `retrieve_design_context` (DESIGN.md carries the token name, not the CSS-var name) — **never guessed**; if a token→CSS-var mapping can't be confirmed, flag it rather than invent one (rule 6). Then effect styles (shadows) + text styles (typography).
- **Phase 2 — File structure.** Page skeleton `Cover → Getting Started → Foundations → --- → Components → --- → Utilities`, plus foundations docs (color swatches, type specimens, spacing bars), each `get_screenshot`-verified.
- **Phase 3 — Components, one at a time, in dependency order (atoms → molecules).** Base component with auto-layout + full variable bindings (no hardcoded fills/strokes); variant sets via `combineAsVariants` then grid-laid-out (they stack at (0,0) until positioned); component properties (`TEXT`/`BOOLEAN`/`INSTANCE_SWAP`) bound to child nodes. `INSTANCE_SWAP` for icons — never a variant per icon; cap a variant matrix at 30 combinations (v1 covers single-axis and small multi-axis; a matrix near the cap is a v2 scope call).
- **Phase 4 — Integration + QA.** Code Connect (optional), accessibility spot-check, naming audit, unresolved-bindings audit, final screenshots.
- **Transport discipline (hard constraints, every call):** each `use_figma` payload clears the 50,000-char cap (split a dense unit; import a unique SVG once as a component and reuse by instance); **never parallelize `use_figma`** (state mutations are strictly sequential — `figma-generate-library` § 3 rule 13); **font preflight** before any text write (resolve every `(family, weight)` against `listAvailableFontsAsync()` first); **create-only value writes** on a reused canonical Variable (never clobber it); **disk-backed state ledger** (`design-system-state-{RUN_ID}.json`, re-read every turn); **never hallucinate node IDs** (read from the ledger / a prior return — § 3 rule 14).
- **Place the judgment slots empty.** Anything the skill must infer to complete the structure (an unspecified variant axis, a token role the contract is silent on) is **flagged/tagged**, not asserted. Value conflicts, reuse-vs-rebuild, and scope stay with the human (§ The human-gated slots).
- **Idempotency.** Find-or-create for collections and Variables; check by name + state-ledger ID before every create; a re-run reuses, never duplicates.

## Step 5: Verify and hand off

Verify the Figma canvas with `get_metadata` (design-file, not `get_figjam`) + `get_screenshot`; run `validate_output` on any produced/exported artifact (e.g., written token descriptions) to check served-contract compliance. Confirm: collections + primitive/semantic variables exist, mode-aware, scoped (no `ALL_SCOPES`), `var()` code syntax present; at least one component with a correct variant matrix and all bindings resolved (no hardcoded fills/strokes), screenshot-verified; the page skeleton + one foundations doc; a re-run creates zero duplicate collections/Variables and does not overwrite a reused canonical value; and — if the file is shared — no client name appears on it (hermetic seal). Return the Figma link as a markdown link; note where the deliverable is filed per `deliverable.root`.

---

## The human-gated slots (§ 9 boundary — enumerated, non-empty)

| Judgment slot (stays human) | Trigger | The gate + provenance rule |
|---|---|---|
| **The pre-write plan** (load-bearing) | Before any canvas write | The 0f gap analysis + 0d scope + the collection/variable/component plan are printed and **approved** before Phase 1. Read-only; writes nothing. |
| **Value-conflict resolution** (`figma-generate-library` § 6 Fork 1) | Code ≠ Figma on a token/component/value | Surface both sides with provenance (file/line vs node id); the human picks. Never silently default. |
| **Reuse-vs-rebuild** (§ 6 Fork 2 / § 5 reuse matrix) | A subscribed library is a close-but-not-exact match | Surface the component summary + the gap list; the human chooses reuse / wrap / rebuild. |
| **v1 scope lock** (§ 6 Fork 3, Phase 0d) | Scope ambiguity | Surface clearly-in / clearly-out / ambiguous; the human locks scope. |
| **An inferred taxonomy** | An unspecified variant axis or token role | Anything inferred to complete the structure is tagged/flagged; the human confirms the taxonomy. |
| **Craft critique of the produced library** | Always | The verdict stays human (the `dont-automate` line). The skill produces the substrate, never the grade. |

`figma-generate-library` § 6's own floor holds: *when exactly one path is clearly correct from the source of truth, take it.* The gate fires on genuine ambiguity, not on every mechanical choice.

---

## What is explicitly out of scope

- **The design truth** — which value wins, whether to reuse or rebuild, the right scope, the correct taxonomy, whether the library is any good. Empty slots by construction (§ 9).
- **Auditing / drift-detecting** an existing DS — `heyhi-design-intelligence-audit` (reads, never writes). **Repairing** findings back into the file — `heyhi-drift-repair`.
- **Composing a brand book from finished art** — `heyhi-figma-identity-file` candidate. **Translating** a prototype/raster — `heyhi-design-bridge`. **Extracting** tokens from Figma — `ui-studio-onboard`. **A FigJam board** — `heyhi-figjam-mapper`.
- **The app/screens file** (`figma_app_file_key`) — v1 writes only the DS file; consuming the DS to build screens is `ui-studio` / `heyhi-ui-ux`.
- **Raw Storybook/code component-catalog parsing** (`component_format: storybook | code`) — v1 sources components from the served MCP contract (`retrieve_design_context`); other catalog formats are a v2 scope (spec Decision D4).
- **Unattended whole-build replay** via a bundled-plugin transport (the `emit_plugin.py` pattern `heyhi-design-bridge` built, out of necessity, for its whole-page writes) — a **v2 direction** for this skill. v1 writes are human-initiated through the engine's native per-unit `use_figma` calls.

---

## Exit Gate Required Headers (bottom-of-skill bracket)

This skill closes through the Exit Gate Flavor A (`CLAUDE-SESSION-RULES.md § Exit Gate`). Before declaring done, confirm every header carries real content, not a claim:

- `## Fixes Applied` — what was generated, with the Figma link, the collections/variables/styles/components created, and where the deliverable is filed.
- `## Smoke Test` — the Step-5 verification: variables scoped + `var()`-syntaxed + mode-aware; a component with resolved bindings, screenshot-verified; the re-run reuse proof; the hermetic seal held; no write against a local key.
- `## Next Session Prompt` — the judgment slots still open (unresolved conflicts, the reuse/rebuild calls, the scope questions), and the components deferred past v1.

---

*HeyHi Confidential. Sheerline area 7 (Design Systems), build class N. v0.1.0 built 2026-09-01, deployed 2026-09-04 after the live proof on the instance's own design system. Spec source: `plans/plan-ds-into-figma-generator-2026-08-29.md` (DISPATCH-01). Precedent: `heyhi-figjam-mapper` (area 11, the first live-Figma generation skill — into FigJam; design-bridge already *writes* to Figma via Translate). Engine: Figma's `figma-generate-library` + `figma-use`. Boundary: § 9.*
