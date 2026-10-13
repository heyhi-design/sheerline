---
name: ui-studio-onboard
description: |
  Onboard a new design system into ui-studio. Extracts tokens, layout patterns, components, and voice guidelines from a client's connected sources and writes active-brand.json. The only way to activate ui-studio for a new design system. Nine phases plus persona routing. Triggers: "onboard a new design system", "set up the brand config", "extract design tokens from Figma", "create a design system config", "run onboarding for [client]", "refresh the config", or any setup work that precedes a ui-studio build. NOT for running builds (use ui-studio). NOT for switching between already-configured brands (use `python3 scripts/switch-brand.py`). NOT for design system audits (use heyhi-design-intelligence-audit). NOT for moodboard-driven Mode D onboarding from aesthetic intent (use design-system-onboard).
version: "1.0.0"
---

# UI Studio Onboard

Extract a client's design system and write `active-brand.json`. The only gateway to `ui-studio`.

---

> **Exit Gate (Flavor A).** This skill closes through the canonical Exit Gate — see `CLAUDE-SESSION-RULES.md § Exit Gate`. Required headers, in order: `## Fixes Applied`, `## Smoke Test`, `## Next Session Prompt`. Empty headers are visible failures.


## ZONE 1 — Always Loaded

*Complete onboarding contract. ≤2,000 tokens.*

---

### Nine-Phase Overview

| Phase | What happens |
|---|---|
| 0: Access verification | Confirm Figma MCP account can access the file before touching anything |
| 0.5: Persona routing | Route to the right access modes for Phases 2–4 |
| 1: Library discovery | Find and classify all connected design system libraries |
| 2: Token extraction | Extract tokens by persona route |
| 3: Layout extraction | Map brand to style cluster; derive layout block |
| 4: Component extraction | Build component inventory from connected sources |
| 5: Guidelines extraction | Pull UX writing patterns and voice rules |
| 6: Voice rules intake | Capture or confirm voice rules for the voice block |
| 7: Interaction patterns | Capture motion and interaction vocabulary |
| 8: Repository connections | Store all source strings in the repository block |
| 9: Completeness review | Compute completeness_score; confirm mode unlock status |

---

### Phase 0: Access Verification

Run before anything else. Fail fast.

```
whoami() → confirm connected Figma account email
search_design_system(query="test") → confirm library access
```

**If access fails — STOP:**
> "Account [email] cannot access this file. Share the file with that account and try again. Onboarding cannot proceed without library access."

Do not attempt to continue with partial access.

---

### Phase 0.5: Persona Routing

Ask: "Which describes your situation?"

- **Designer** — I work in Figma, Supernova, or can export files
- **Developer** — I have git/GitHub access to the token and component repositories
- **Enterprise** — We're behind a company firewall with a private npm registry

The route determines which access modes are used in Phases 2–4. Record the persona in `meta.generated_by`.

---

### Phase 1: Library Discovery

Ask for the PRIMARY DESIGN SYSTEM FILE specifically — the component library master or token foundation, not a working prototype.

1. `search_design_system` → enumerate connected libraries + capture library_keys
2. Classify each library: `token_foundation / atomic / molecular / layout_template / icon / documentation / other`
3. Confirm: "We found N libraries. Are there token or component libraries not in this list?" Allow additional file keys.
4. Store all `file_keys`, `library_keys`, and classifications in `repository.figma`

**Critical:** Identify which library is the token foundation before Phase 2. Token extraction must use the token library's `file_key`, not the component library's.

---

### Phase 2: Token Extraction

Route by persona:

| Persona | Method |
|---|---|
| Designer | `get_variable_defs(file_key=TOKEN_LIBRARY_FILE_KEY)` + token file upload if provided |
| Developer | GitHub API fetch (`GITHUB_TOKEN` env var) OR git clone (`GIT_TOKEN`) — scan token files |
| Enterprise | npm package extraction with `.npmrc` + internal registry (`NPM_TOKEN` env var) |

**Unresolved variable references:** If a component references a token not found in the token library:
- Do NOT null the field
- Add to `meta.provisional_fields` with reason `unresolved_variable_reference`
- Add to `components.drift.token_drift`

**Storybook fallback (Level 1):** If available: `GET {storybook_url}/stories.json` → component name inventory without requiring source access.

**Provenance write requirement (G3 — mandatory):** Every extracted token must have a corresponding entry in `meta.field_provenance` at extraction time. Do not defer this to post-extraction cleanup. The minimum required fields are `source`, `confidence`, and `extracted_at`. See `moodboard-to-brand-json.md` Part 4.7 for the full provenance spec.

Confidence levels:
- `extracted` — value came from a reliable structured source (Figma variables, CSS file, labeled PDF). Production-ready.
- `inferred` — estimated from visual inspection or qualitative description. Directional. Needs designer confirmation before v1.
- `provisional` — known to be approximate or incomplete; origin tracked. Requires designer replacement.
- `failing` — known to violate a hard constraint (WCAG, brand restriction). Must not emit to CSS.

---

### Phase 3: Layout Extraction + Layer 0 Pipeline

For layout_template libraries: `search_design_system` + `get_design_context` on layout frames.

**Layer 0 pipeline:**
1. Match brand to style cluster (A–E) using personality, temperature, and visual descriptors
   - **First-pass signal from `data/ui-reasoning.csv`:** Before inferring the cluster from brand materials alone, read `data/ui-reasoning.csv` directly (procedural read, no search command) and find the row whose `UI_Category` best matches the client's product type. Read its `Style_Priority` and look it up in `references/cluster-crosswalk.md` to get a suggested HeyHi cluster. Surface the suggestion and confirm before writing to `brand.style_cluster`. Do not auto-assign.
2. Pull cluster-fit named patterns from the Pattern Summary Index in `ui-studio/references/layout-patterns.md`
3. Derive `spacing_density` from cluster fit and brand descriptors
4. Populate the `layout` block in the config:
   - `grid.*` from the layout template frames
   - `spacing_density`: spacious/balanced/dense
   - `section_padding_tiers`: derived from density (spacious: 8-12rem generous, 5-8rem standard; balanced: 6-9rem generous, 4-6rem standard; dense: 4-6rem generous, 2.5-4rem standard)
   - `preferred_patterns`: 2–5 patterns from cluster cross-reference
   - `style_cluster`: confirmed cluster letter

**Gate 0 confirmation (G2 — required before Phase 4):** After presenting the style cluster match and primary direction to the user or designer and receiving confirmation, write it to the config immediately:

```json
"gate_status": {
  "direction_lock_confirmed": true,
  "direction_lock_date": "YYYY-MM-DD"
}
```

This is a required write step, not prose documentation. validate.py enforces `direction_lock_confirmed: false` as a hard stop for Mode A. The date should be today's ISO date. If the user or designer cannot confirm direction during this session, leave `direction_lock_confirmed: false` and proceed to Phase 4 — but document the gap in `meta.implementation_notes` and set a clear expectation that Mode A is blocked until Gate 0 is confirmed.

**Designer review confirmation (G2 — written after Figma review, not during onboarding):** When a designer has reviewed the extracted token values against the source Figma file and confirmed them, write this to the config:

```json
"gate_status": {
  "designer_review_complete": true,
  "designer_review_date": "YYYY-MM-DD",
  "designer_reviewer": "Name or identifier (e.g., 'Sarah M.', 'studio lead designer')"
}
```

This gate is typically confirmed in a separate session after onboarding, when the designer has the Figma file in front of them. Do not set it true during initial onboarding unless the designer is actively verifying values in real time. validate.py will surface a warning (not a hard stop) for Mode A builds until this is true, and will hard stop `--promote`.

---

### Phase 4: Component Extraction

Per component library, filtered by `library_key`.

- Cross-reference: fuzzy-match component variable references to token library
- Unresolved → `meta.provisional_fields` with `unresolved_variable_reference`
- Storybook URL: fetch `{url}/stories.json` for Level 1 inventory
- Deep analysis (Level 2–3) is on-demand only — load the component analysis reference if requested

---

### Phase 5: Guidelines Extraction

Priority order:
1. Supernova MCP (if connected) → guidelines, component docs, voice rules, UX writing patterns
2. `get_design_context` on documentation library frames (text extraction)
3. Guided manual Q&A per `ux_writing` slot (use `templates/ux-writing-intake.md`)

For each slot, store: `pattern`, `source`, `source_url`, `last_verified`.

---

### Phase 6: Voice Rules Intake

If voice rules not captured in Phase 5:
- Ask for the brand's style guide or voice document
- Extract: tone, prohibited words, prohibited patterns, CTA style, formatting, terminology
- If nothing exists: flag it. Do not invent voice rules. Populate with blanks and note in `meta.implementation_notes`.

---

### Phase 7: Interaction Patterns

Capture:
- Motion easing curves (named CSS cubic-bezier values)
- Duration ranges by interaction type
- Stagger timing
- Brand motion principles (e.g., "subtle and purposeful", "energetic and expressive")

Source: brand guidelines, Supernova if connected, or elicit from the designer.

---

### Phase 8: Repository Connections

Store all source strings in the `repository` block. Env var names only — never auth tokens. Document all env var names needed in `.env.example`.

---

### Phase 9: Completeness Review

```bash
# Working directory: heyhi-skills/ui-studio-onboard/
# validate.py lives in ui-studio, not ui-studio-onboard. LE-05.
python3 ../ui-studio/scripts/validate.py --config ../ui-studio/brand-config/[name].json --verbose --status
```

The `--verbose --status` flags show the full breakdown: completeness score, fidelity score, gate status, and any stale provenance entries. Display all of these to the user.

**Two scores, two questions — present them distinctly (LF-01, LF-05):**

- **Completeness score** (0–100): Is the config fully populated? Governs mode unlock. A high completeness score means all fields have values — it does not mean those values are correct. A score of 95 with approximate hex values still produces confidently wrong output. **Completeness measures data presence, not brand accuracy.**
- **Fidelity score** (0–100): How much has been confirmed against its source? Governs build trustworthiness. This is the substantive quality signal. Low fidelity means provisional or inferred values — the build may look brand-compliant by the numbers but not match actual design intent.

Always surface both scores with their labels. Do not present completeness as a summary of config quality. The failure mode: "Your config is 95% complete" implies readiness when fidelity may still be 40. Correct form: "Completeness: 95/100 (all fields populated). Fidelity: 40/100 (most values inferred — designer review required to confirm accuracy before Mode A delivery)."

**Unlock matrix:**
| Completeness | Fidelity | Status |
|---|---|---|
| ≥ 90 | ≥ 80 | Mode A fully unlocked. Eligible for version promotion via `--promote`. |
| ≥ 90 | 60–79 | Mode A fully unlocked. Promotion blocked — fidelity ≥ 80 required. Run designer review to qualify. |
| ≥ 70 | ≥ 60 | Mode A with documented approximations. |
| ≥ 70 | < 60 | Completeness passes; fidelity too low. Designer review needed before Mode A. |
| 50–69 | any | Mode B recommended. Mode A requires explicit user confirmation in ui-studio (score surfaces as override gate). |
| 30–49 | any | Mode B/C allowed with capability-degradation notice. Mode A blocked. Re-run onboarding to fill gaps. |
| < 30 | any | Hard stop. Insufficient data for any meaningful build. Re-run onboarding. |

**Gate status check:** Report whether `direction_lock_confirmed` and `designer_review_complete` are true. If direction lock is false, Mode A is blocked regardless of scores. Tell the user exactly what needs to happen to unblock it.

**Version promotion path (G1):** If completeness ≥ 90 AND fidelity ≥ 80 AND both gate fields are true AND no provisional fields remain, the config is eligible for promotion to v1.0.0:

```bash
python3 ../ui-studio/scripts/validate.py --config ../ui-studio/brand-config/[name].json --promote
```

Tell the user whether their config is promotion-eligible. If it is, offer to run `--promote`. If not, list exactly which gates are blocking.

Confirm the scores with the user. If completeness is below 50 (PARTIAL_STOP at 30–49, or HARD_STOP below 30), identify the highest-impact gaps and offer to fill them before writing the config.

---

**Designer Handoff Artifact (Phase 9 output):**

After completeness review, check `meta.field_provenance` for fields with `confidence: failing`, `confidence: provisional`, or `confidence: inferred`.

- **If any `confidence: failing` fields exist:** Generate the designer handoff artifact automatically, without asking. Failing fields block version promotion — designer action is required before Mode A delivery is safe. State clearly: "Config contains failing fields. A designer review document has been generated — the designer must confirm replacements before this config can be promoted."
- **If only `confidence: inferred` or `confidence: provisional` fields exist (no failing):** Offer to generate the handoff artifact: "The config has [N] approximate values. Would you like a designer review document to confirm them before the first build?"

**Generating the artifact:**

Use the template in `templates/designer-handoff-artifact.md`. Populate the table rows from `meta.field_provenance` — one row per failing/provisional/inferred field. The table columns are: field path, current value, confidence level, basis for estimate (the provenance `reason` field), and an empty "Designer confirms:" column for the designer to fill in.

Write the artifact as `[client-name]-token-review-[date].md` in the same working directory as the config. Tell the user the filename and what to do with it: fill in the "Designer confirms:" column and return it. When they return it, read the completed table and update the config and provenance entries accordingly.

---

### After Writing the Config

1. **Save the config** as `../ui-studio/brand-config/[client-name].json`
2. **Activate it:** `python3 ../ui-studio/scripts/switch-brand.py --config [client-name]`
   *(Working directory: heyhi-skills/ui-studio-onboard/ — same anchor as Phase 9. LE-06.)*
3. **State the result:** Config name, version, completeness score, unlock status, any provisional field warnings
4. **Tell the user what to do next** if score is provisional — e.g., "Run `--refresh [name]` after the designer confirms the accent color"
5. **Offer G6 description backfill (engineer context — mandatory offer):** Ask: "The config is written. Would you like me to add token descriptions so engineers reading the generated Cursor rules file understand what each CSS variable is for?" If yes: load `heyhi-skills/heyhi-token-description-author/SKILL.md` and run Target B mode on the new config. If the config has inferred or provisional fields, prioritize those first — they are the most likely to be misused without a warning comment. Without this step, the generated `.mdc` file delivers CSS variables with no context. Not a blocking step for build readiness, but strongly recommended before first handoff to an engineer.

---

## ZONE 2 — Context Loading

**Task-conditional:**
- `ui-studio/references/figma-mcp-integration.md` — Figma MCP tool calls and multi-library extraction routing
- Supernova extraction procedures — if Supernova workspace is provided
- Git repo analysis guide — if Developer persona and repo URL is provided
- UX writing intake guide (`templates/ux-writing-intake.md`) — Phase 5 reached and guidelines not in Supernova/Figma
- Designer handoff artifact template (`templates/designer-handoff-artifact.md`) — Phase 9 reached and `meta.field_provenance` contains inferred, provisional, or failing fields

**On-demand:**
- Full cross-reference resolution algorithm — token-component mismatch detected
- Schema documentation — user asks about a specific field in `brand-config/schema.json`
- Deep component analysis (Level 2–3) — explicit depth requested

**Searchable:**
- `python3 ui-studio/scripts/search.py "<query>" --domain <domain>` — style, color, typography, landing, product, ux, animation
- Style reference library — cluster matching during Phase 3

---

## Exit Gate Required Headers (bottom-of-skill bracket)

This skill closes through the Exit Gate Flavor A (`CLAUDE-SESSION-RULES.md § Exit Gate`). Before declaring done, confirm every required header below contains real content, not a claim:

- `## Fixes Applied`
- `## Smoke Test`
- `## Next Session Prompt`

If any header is empty or contains advisory prose ("I checked for bugs") instead of a concrete artifact, the gate has not been satisfied. Apply fixes until clean — then emit.

---

*HeyHi Internal Use Only. Created 2026-03-25.*
