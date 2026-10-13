---
name: heyhi-style-selection
description: >-
  Match a completed moodboard to 1–3 named styles from the Style Reference Library. Two modes: Mode A (client-facing, conversational) and Mode B (agent-internal, structured lookup for Mode D handoff). Use when a designer or account lead needs to translate client direction into a named, system-ready style choice. Triggers: "recommend a style for [client]," "which style fits this moodboard," "style selection for [client]," "which named style," "Gate 0 style match," "classify this moodboard," "does this moodboard match a named style." Mode A runs first during any design engagement direction phase. Mode B runs when design-system-onboard needs a pre-classification before Mode D token extraction begins. Do not use this skill to extract tokens (that is design-system-onboard), to build style entries (that is heyhi-style-entry-author), or to validate entries (use Mode B of heyhi-style-entry-author). Style selection happens before tokens exist, during the direction phase.
---

# Style Selection

Match a moodboard to a named style. One invocation = one selection session, producing 1–3 recommendations with full rationale, imagery direction, and layout guidance.

**Mode A** — client-facing, conversational. Used by designers and account leads during Gate 0 or any direction-phase conversation. Output is readable prose with vocabulary-backed rationale, imagery direction, grid layout recommendations, and anti-style contrasts.

**Mode B** — agent-internal, structured. Used when `design-system-onboard` needs a pre-classification before Mode D runs. Output is structured YAML. Not for client delivery.

---

> **Exit Gate (Flavor A).** This skill closes through the canonical Exit Gate — see `CLAUDE-SESSION-RULES.md § Exit Gate`. Required headers, in order: `## Fixes Applied`, `## Smoke Test`, `## Next Session Prompt`. Empty headers are visible failures.


## Before You Start

Load these files before beginning any matching work. Load in order.

1. **`ai-services/design-intelligence/style-reference-library.md`** — load the proposed styles table and the YAML entries for plausible clusters only. The table (~500 tokens) tells you the full candidate set across all 20 styles. After Step 2 (cluster pre-filter) identifies 1–2 plausible clusters, load only those cluster entries for scoring. Do not load all entries by default — the file is at or near the token read limit as the library grows. Loading the full file when you only need Cluster B and D entries is a resource violation of the Earn the Room principle. Both the table and the filtered YAML entries are needed for scoring.

2. **`ai-services/design-intelligence/style-descriptor-vocabulary.md`** — load the summary keyword list section (approximately 100 tokens) unless you are doing fine-grained comparison across three or more candidates with similar descriptors. Full load only when term-level disambiguation is needed. The summary keyword list gives you cluster affinity for all 141 terms.

3. **`ai-services/design-intelligence/compositional-layout-patterns.md`** — load the Pattern Summary Index only (approximately 380 tokens) unless compositional rationale for a specific pattern is needed in the client deliverable. Full pattern detail is on-demand. This is the primary reference for Component 4 compositional layout output.

4. **`ai-services/design-intelligence/grid-layout-examples.md`** — load the Pattern Summary Index only (approximately 300 tokens) unless a specific grid pattern's spatial logic is needed for rationale. Full pattern detail is on-demand. This is the secondary structural reference for Component 4 grid scaffolding output.

Do not speculatively load `moodboard-template.md`, `anti-descriptor-method.md`, or `gate0-facilitation-guide.md`. Load if the moodboard is incomplete, multi-directional, or if brand fit analysis is needed before style matching can proceed.

---

## Input Formats

This skill accepts moodboard input in any of these states. Assess the input format before starting — it determines which sub-process to follow.

**Resolved moodboard (preferred):** A completed `moodboard-template.md` with at minimum Sections 1 (Style Identity), 2 (Color Direction), 3 (Typography Direction), 4 (Spatial Direction), and 7 (Photography and Illustration) populated. Token Translation Notes (Section 9) not required.

**Partial moodboard:** One or more sections missing. Proceed with available signals; name which sections are missing in the output and flag what additional input would sharpen the recommendation.

**Verbal brief:** No template — just client-provided description, reference URLs, mood words, or a designer's notes. Extract signals using the same categories as the moodboard template before matching.

**Gate 0 multi-direction scenario:** Multiple directions delivered by a designer. If direction lock has not been confirmed, stop and route through `gate0-facilitation-guide.md` before style selection runs. Style selection requires a single resolved direction as input. If the directions are similar enough that one can reasonably serve as primary with a modifier from another, note this in the output and recommend the hybrid approach.

---

## Mode A: Client-Facing Style Matching

### Step 1: Extract Signals

Pull these six signal types from the moodboard input. Record them before matching — this is the evidence layer the recommendation must be traceable to.

**Mood signal:** The 5–7 mood descriptors from Section 1.3. If verbal only, infer 4–6 terms from the reference descriptions and brief. Translate non-vocabulary language to nearest vocabulary terms (use summary keyword list for cluster affinity).

**Color signal:** Palette temperature (warm / cool / neutral / mixed), palette character, any stated restrictions. From Section 2.

**Typography signal:** Type personality (humanist / geometric / grotesque / slab / serif / transitional / display / monospace) and scale feeling (compact / balanced / dramatic). From Section 3.

**Spatial signal:** Content density (spacious / balanced / dense) and grid intent. From Section 4.

**Imagery signal:** Photography direction, illustration direction, iconography style. From Section 7. Map to vocabulary Category 8 terms (documentary, reportage, constructed, editorial, cinematic, spatial, process, data-visual, abstracted, line-driven, diagrammatic, geometric-illustration, textured-hand, outlined, filled, custom-mark). This signal drives the imagery direction output.

**Industry signal:** Primary sector from Section 8. Cross-reference against each candidate style's `industry_fit` (natural / stretch / avoid) to surface sector tension early.

Record the extracted signals before moving to Step 2. The recommendation is only as defensible as the signal trace.

---

### Step 2: Run Cluster Pre-Filter

Before scoring individual entries, identify which cluster(s) are plausible given the mood and industry signals. This narrows the candidate set to the entries most worth scoring against.

**Cluster reference:**
- **A** — Clean and Structured: SaaS, infrastructure, financial services, technical precision. Mood: quiet, austere, considered, declarative, precise.
- **B** — Warm and Human: healthcare, education, care, community. Mood: generous, earnest, grounded, inviting, reassuring.
- **C** — Bold and Distinctive: media, fashion, cultural institutions, brand-forward. Mood: urgent, alive, restless, expressive, declarative.
- **D** — Sustainable and Infrastructure: energy, utilities, civic, environmental, systems work, municipal, public works, policy. Mood: austere, grounded, earnest, durable, civic.
- **E** — Craft and Studio: design agencies, artisan, publishing, portfolio. Mood: generous, considered, expressive, restrained, refined.

Cross-reference mood signal against each cluster's vocabulary affinity. Flag the 1–2 most plausible clusters before scoring library entries. If imagery signals include `documentary` or `reportage`, those have affinity for B and D. `Constructed` or `editorial` for C and E. `Data-visual` or `diagrammatic` for A and D. `Textured-hand` or `custom-mark` for E. `Spatial` for D and E. These cluster-to-imagery-term affinities are a secondary filter — they should confirm or complicate the mood-based cluster assessment, not override it.

For hybrid mood signals spanning two clusters — record both and check whether a hybrid-style entry (one with a `modifier` field) exists in the library that covers the combination.

If no hybrid entry exists, do not invent a hybrid name. Instead, score both clusters' entries independently. If a clear primary emerges from one cluster but 2–3 signals strongly favor the other, name both styles in the output as a composite direction with explicit guidance on which style governs which design decisions (for example: spatial and color logic from Style A, typography and imagery register from Style B). Label this as a "composite direction" — not a library match. In Mode B, set `confidence: medium` and add a `designer_confirmation_needed` item noting that the hybrid needs design confirmation before Mode D proceeds.

---

### Step 3: Score Library Entries

For each entry in the plausible cluster(s), score against the six extracted signals. Use the entry's schema fields directly — do not summarize or paraphrase. Score as: **strong match / partial match / weak match / conflict**.

| Signal | Entry field to check | What counts as a match |
|--------|---------------------|------------------------|
| Mood | `descriptors.mood` | 3+ extracted terms match or are close synonyms |
| Anti-mood alignment | `descriptors.anti_mood` | None of the client's stated mood terms appear as anti-moods |
| Color | `token_implications.color_temperature` | Same thermal direction as moodboard palette |
| Typography | `token_implications.type_personality` | Same personality category as moodboard Section 3 |
| Spatial | `token_implications.spacing_density` | Same density intent as moodboard Section 4 |
| Imagery | `visual_characteristics.imagery_approach` | Category 8 terms in the entry match or share cluster affinity with moodboard Section 7 |
| Industry | `industry_fit.natural` or `stretch` | Client sector appears in natural (strong), stretch (partial), or avoid (conflict) |

The scoring table has 7 rows, but not all rows are graduated signals. **Anti-mood alignment** and **Industry fit** are disqualifiers, not scored matches — they flag conflicts or confirm sector fit, but a "pass" on either does not count toward the match threshold. The 5+ threshold counts only the 5 graduated signals: Mood, Color, Typography, Spatial, and Imagery.

An entry with 5+ strong matches across those five signals and no disqualifying conflicts is a primary recommendation. 3–4 strong matches across those five signals with no conflicts is a secondary recommendation. A conflict on anti-mood alignment or industry_fit.avoid is disqualifying regardless of graduated match count, unless there is an explicit sector adaptation rationale.

**Note on field format:** Library entries may contain descriptive prose in `token_implications.type_personality` (e.g., "geometric sans" or "humanist sans-serif for UI") and `visual_characteristics.imagery_approach` rather than exact vocabulary terms. When prose is present, map to the nearest enum value or Category 8 term before scoring. Do not fail to score simply because the field uses prose rather than a single keyword.

If fewer than 2 entries from the current library score well, note this explicitly — the recommendation is based on the entries currently in the library, which expands over time (count the entries in `style-reference-library.md` at load time; do not rely on a number pinned in this file). Do not force a recommendation that doesn't hold.

If zero entries score at 3+ strong matches, this is a library coverage gap, not a client direction problem. Stop matching. Name the dominant signals — which cluster the moodboard most likely points toward, which mood terms have no library equivalent — and route to Gate 0 to confirm direction before attempting a low-confidence match. State explicitly: "The current library does not have an entry that covers this signal profile. Direction confirmation is recommended before proceeding." Do not invent a style name or fabricate a match to fill the gap.

---

### Step 4: Select 1–3 Styles

Rank scored entries. Select 1 primary + up to 2 alternates. Criteria:

**Primary:** Highest match count with no conflicts. If two entries tie, prefer the one whose `agent_context_snippet` better describes what the client brief is reaching for.

**Alternates:** Next 1–2 entries with 3+ strong matches. Alternates should differ meaningfully from the primary — a second Cluster A entry is only useful if it represents a genuine variant, not a near-duplicate. If all viable candidates are in the same cluster, present them with explicit contrast between what they do differently, not just what they share.

**Anti-style contrasts:** Identify 1–2 entries that were considered but excluded. For each, state which signal created the conflict. These are the entries the client did *not* reach for — naming them sharpens the recommendation and preempts "but what about..." conversations.

---

### Step 5: Build the Output Package

For each recommended style, produce all five components. Do not omit any. The output package is not a summary — it is a decision document that a designer can work from.

**Component 1 — Style identification**

State the style name, cluster, and family. If hybrid, name the modifier and what it contributes. Use the `agent_context_snippet` as the anchor sentence — it should appear verbatim or near-verbatim as the opening line. Then add one sentence of connection to the moodboard: what specifically in the client's brief or references points toward this style.

**Component 2 — Vocabulary-backed match rationale**

State the 3–5 mood terms that aligned between the moodboard and the library entry. Quote them as terms — they are vocabulary, not paraphrase. Then name which signals from the moodboard drove the cluster selection (color temperature, spatial density, typography personality). Keep this to 3–5 sentences. The rationale should be traceable: a designer should be able to look at the moodboard and see exactly where each point came from.

**Component 3 — Imagery direction**

This is the component the vocabulary expansion enables. Provide three layers:

*Primary imagery vocabulary:* State the Category 8 term(s) from the matched style entry's `imagery_approach` field. Quote the term and its implication directly. Example: "The style calls for **spatial** photography — wide-format site and environment images that establish physical scale and consequence, not people or product shots."

*Cross-reference to client brief:* Connect the vocabulary term to what appeared in the moodboard's Section 7. If the client's photography direction was "Documentary / Authentic" and the matched style calls for `documentary` imagery — confirm the alignment explicitly. If there is a vocabulary mismatch, name it: the client reached for X, the style's primary imagery register is Y, and here is what that means in practice.

*Iconography and illustration note:* If the style entry specifies iconography or illustration terms (outlined, filled, custom-mark, line-driven, etc.) and the moodboard has a corresponding preference, confirm or note the tension. If neither the entry nor the moodboard specifies, say so — this is not a gap, it is a decision for the designer.

*Typography resolution status:* If the moodboard's Section 3 specified only a type personality category (e.g., "geometric sans") without naming specific typefaces, note this explicitly. The `type_personality` field is inferred, not confirmed. State it as an open question: "Typography direction is based on personality category only — named typefaces have not been selected. Resolve before Mode D runs." In Mode B, this becomes a `designer_confirmation_needed` item.

**Component 4 — Compositional and grid layout patterns**

Name 2–3 compositional layout patterns from `compositional-layout-patterns.md` that are natural fits for this style. Use pattern names exactly as they appear in the Pattern Summary Index (e.g., "Momentum Hero," "Editorial Anchor," "Documentary Opener," "Dashboard Preview"). For each, one sentence of rationale: why this pattern fits this style's composition, cluster character, and spatial logic.

Then name 1–2 structural grid patterns from `grid-layout-examples.md` that provide the column scaffold for those sections. Compositional patterns describe *how* sections are composed; grid patterns describe the underlying structure they sit within.

If the moodboard's Section 4.2 already named a grid preference, confirm whether the recommended patterns are consistent with it. If there is a tension, name it.

**Component 5 — Sector intersection note**

If the client's sector appears in the style's `industry_fit.natural` list — confirm cleanly. One sentence.

If the sector appears in `industry_fit.stretch` — name the adaptation required. What specifically needs to shift for this style to work in this sector? This is where the sector intersection guidance in the library entries earns its keep.

If the sector appears in `industry_fit.avoid` — this is a disqualifying condition unless there is a strong justification. State it directly: "This style is listed as an avoid for [sector] because [reason from anti-mood or visual characteristic that conflicts]. If you want to pursue it anyway, here is what needs to change."

---

### Step 6: Present and Offer Next Steps

Deliver the output package in plain prose. Not a YAML block. Not a table. Readable by a client in a workshop and by a designer working from notes.

**Before writing the first sentence: count your available em dashes.** The full Mode A output package may contain no more than 2 em dashes total. This is a hard voice constraint — not a style preference. If you plan to use em dashes in your draft, allocate them deliberately before writing: 2 total, across all sections, primary + alternates + anti-style + next steps combined. Em dashes are persuasive at one or two; they become habitual noise at three or more. If you cannot fit the sentence without a third em dash, rewrite the sentence — a comma, colon, or period will serve. The Smoke Test checks this item last; catch it here first.

Structure:
1. **Primary recommendation** — all five components
2. **Alternate(s)** — abbreviated; components 1, 2, and 3 (imagery direction) in brief; components 4 and 5 only if they differ materially from the primary
3. **Anti-style contrasts** — 1–2 excluded styles with brief conflict rationale
4. **What this enables next** — one paragraph on what the recommendation unlocks:
   - If direction is confirmed: `design-system-onboard` Mode D can run with the named style as reference
   - If typography candidates are not yet resolved: named typefaces need to be selected before `design-system-onboard` Mode D runs — reference `typography-lockup-specimens.md` for the specimens catalog, or confirm typeface choices through the design direction process first
   - If imagery direction is provisional: imagery confidence is low when (a) the moodboard's Section 7 was not populated, (b) Category 8 terms had to be inferred from prose rather than matched directly, or (c) the matched style's imagery_approach field used descriptive prose without explicit vocabulary terms. In any of these cases, flag which Category 8 terms are inferred and note that photography/illustration direction needs design confirmation before Mode D
   - If sector tension exists in the selected style: surface it as an open question before locking direction

---

## Mode B: Agent-Internal Style Pre-Classification

Mode B is the agent-facing version of Mode A. It runs when `design-system-onboard` needs to pre-classify a moodboard against the library before Mode D token extraction begins. Output is structured YAML for internal consumption, not client delivery.

### When to Use Mode B

Mode B runs when the orchestrating agent (typically `design-system-onboard`) calls for a style pre-classification as part of its Mode D intake. The trigger condition: a moodboard is provided to `design-system-onboard` and no named style has been confirmed yet. Mode B runs first, classifies the moodboard, and passes a structured result back before token extraction begins.

### Mode B Procedure

**Step 1: Extract signals (same as Mode A Step 1)** — Pull all six signal types from the moodboard. Record them.

**Step 2: Score entries (same as Mode A Step 3)** — Score against the library. Identify the highest-scoring entry and confidence level.

**Confidence levels:**
- `high` — 5+ strong matches, no conflicts
- `medium` — 3–4 strong matches, no disqualifying conflicts
- `low` — 2–3 matches, potential conflicts present or library coverage is insufficient for the style territory

**Step 3: Output structured result**

```yaml
style_pre_classification:
  matched_style: "Style name from library — for composite directions, use 'Composite: [Style A] + [Style B]'"
  cluster: "A | B | C | D | E — for composite, list both clusters"
  confidence: "high | medium | low"
  match_evidence:
    mood_alignment: ["term1", "term2", "term3"]  # terms that matched
    color_temperature: "warm | cool | neutral"
    spacing_density: "spacious | balanced | dense"
    type_personality: "humanist | geometric | grotesque | serif | transitional | slab | display | monospace"
    imagery_register: ["category8_term1", "category8_term2"]  # from imagery_approach field — map prose descriptions to nearest Category 8 terms
  token_implications:
    color_temperature: "warm | cool | neutral | cool-neutral | warm-neutral"
    # If color values are asset-derived, add these extended fields:
    color_palette_source: "asset-derived | inferred | pending"  # required when palette was extracted from photography/video
    color_primary_hex: "#000000"     # asset-derived primary brand color
    color_surface_primary_hex: "#000000"  # asset-derived primary page background
    color_surface_secondary_hex: "#000000"  # asset-derived secondary/tinted surface
    color_accent_warm_hex: "#000000"  # asset-derived warm accent (if any)
    color_dark_hex: "#000000"         # asset-derived near-black / text primary
    # Extended fields are optional when palette is inferred; required when asset-derived
    spacing_density: "spacious | balanced | dense"
    border_radius_range: "sharp | slight | rounded | pill"
    shadow_depth: "flat | subtle | material | dramatic"
    type_scale_ratio: "e.g., Major Third 1.25x"
    type_personality: "humanist | geometric | grotesque | serif | transitional | slab | display | monospace"
    # If typefaces have been confirmed, add these fields:
    type_display_face: "Typeface name (weight) — Google Fonts / commercial"  # confirmed display face
    type_body_face: "Typeface name — Google Fonts / commercial"              # confirmed body face
    # These replace 'designer_confirmation_needed' typography entries when confirmed
    motion_personality: "minimal | purposeful | expressive"
  layout_patterns:
    recommended: ["Pattern Name 1", "Pattern Name 2"]
    grid_preference: "From matched entry's grid_preference field"
    content_width: "narrow | standard | wide | full"
  sector_fit: "natural | stretch | avoid"
  sector_note: "One sentence if stretch or avoid; omit if natural"
  designer_confirmation_needed:
    - "Field or decision that requires designer input before Mode D proceeds"
    - "e.g., typography candidates not yet specified — token_personality is inferred"
    # When a decision is resolved, replace the item text with 'RESOLVED: [what was decided]'
    # rather than deleting the item — preserves the decision record
  alternate_style: "Style name if confidence is medium or low — the next best match"
  # Optional: library gap fields (add when Phase 2 identifies a gap)
  library_gap_flag: false  # set to true when no single entry covers the signal profile
  library_gap_new_entry_name: ""  # confirmed name for the new entry; use heyhi-style-entry-author post-Phase 4
  gate_2_cleared: false
  gate_2_date: ""
```

Pass this result to `design-system-onboard`. Mode D proceeds with the pre-classification as context. If confidence is `low`, Mode D should surface the classification to a human before proceeding — do not run token extraction on a weak match without confirmation.

---

## Smoke Test

Before delivering any Mode A output, verify:

- [ ] Signal extraction is documented — rationale is traceable to moodboard fields
- [ ] Cluster pre-filter ran before scoring — candidate set was not scored exhaustively without narrowing
- [ ] Anti-mood check ran — no client mood terms appear in the recommended style's `anti_mood` list
- [ ] Industry fit was checked — sector appears in `natural` or `stretch` (if `avoid`, it's flagged)
- [ ] Imagery direction output has four layers: vocabulary term, cross-reference to moodboard, iconography/illustration note, typography resolution status
- [ ] Compositional layout patterns are named exactly as they appear in the `compositional-layout-patterns.md` Pattern Summary Index
- [ ] Grid layout patterns are named exactly as they appear in `grid-layout-examples.md`
- [ ] 2–3 compositional patterns + 1–2 grid patterns provided per Component 4
- [ ] Anti-style contrasts include at least 1 excluded style with conflict rationale
- [ ] "What this enables next" paragraph names the specific skill or session to run after direction lock
- [ ] No HeyHi banned words (leverage, unlock, seamless, holistic, empower, supercharge, disrupt, 10x, etc.)
- [ ] No "AI" as a standalone word in any client-facing output
- [ ] Em dashes: maximum 2 across the full Mode A output package

For Mode B:
- [ ] All YAML fields populated — no omissions
- [ ] `imagery_register` uses only Category 8 vocabulary terms
- [ ] All enum values are valid: `confidence` is one of `high | medium | low`; `color_temperature` is one of `warm | cool | neutral`; `spacing_density` is one of `spacious | balanced | dense`; `border_radius_range` is one of `sharp | slight | rounded | pill`; `shadow_depth` is one of `flat | subtle | material | dramatic`; `motion_personality` is one of `minimal | purposeful | expressive`; `sector_fit` is one of `natural | stretch | avoid`; `type_personality` is one of `humanist | geometric | grotesque | serif | transitional | slab | display | monospace`
- [ ] `confidence` is calibrated against actual evidence — fewer than 5 strong matches disqualifies `high`; any conflict disqualifies above `medium`
- [ ] `designer_confirmation_needed` is populated — any field inferred rather than read directly from the moodboard appears here; at minimum, unresolved typography (no named typefaces) is listed
- [ ] `alternate_style` is present when `confidence` is `medium` or `low`
- [ ] `sector_note` is present when `sector_fit` is `stretch` or `avoid`; omitted when `natural`
- [ ] If a composite direction was used (no library hybrid exists), `confidence` is set to `medium` and the hybrid need is documented in `designer_confirmation_needed`
- [ ] **Em dashes: count occurrences in the full Mode B YAML file before saving.** OPERATING_PRINCIPLES maximum is 2 per document. YAML comments (lines starting with `#`) are part of the document and count toward the limit. If em dash count exceeds 2, replace excess uses with colons, parentheses, or sentence restructuring. This check applies to the `.yaml` file as a whole, not just the structured fields. Run: `grep -o "—" [file] | wc -l` to verify.
- [ ] **`color_temperature` must match asset-derived values if photography or video assets were reviewed during Phase 1.** "Inferred from geography" is not a valid basis for `color_temperature` when assets exist. If the moodboard's Section 2 color values are marked "Extracted," the `color_temperature` field must reflect what the assets actually show, not what the location description suggests.

---

## Source Material Reference

| File | When to load |
|------|-------------|
| `style-reference-library.md` | Always — proposed styles table first; then cluster entries for plausible clusters only (not full file) |
| `style-descriptor-vocabulary.md` | Always — summary keyword list; full load for fine-grained disambiguation |
| `compositional-layout-patterns.md` | Always — Pattern Summary Index; full load when compositional rationale needs depth |
| `grid-layout-examples.md` | Always — Pattern Summary Index; full load for specific grid pattern spatial logic |
| `moodboard-template.md` | When input is incomplete or non-standard — load to understand what fields are missing |
| `anti-descriptor-method.md` | When anti-style contrast rationale needs depth, or client brief has strong anti-descriptors |
| `gate0-facilitation-guide.md` | When multiple directions are in play and direction lock has not been confirmed |

---

## Exit Gate Required Headers (bottom-of-skill bracket)

This skill closes through the Exit Gate Flavor A (`CLAUDE-SESSION-RULES.md § Exit Gate`). Before declaring done, confirm every required header below contains real content, not a claim:

- `## Fixes Applied`
- `## Smoke Test`
- `## Next Session Prompt`

If any header is empty or contains advisory prose ("I checked for bugs") instead of a concrete artifact, the gate has not been satisfied. Apply fixes until clean — then emit.

---

*HeyHi Internal Use Only. Bay Design LLC. March 2026.*
*Source material: style-reference-library.md · style-descriptor-vocabulary.md · compositional-layout-patterns.md · grid-layout-examples.md · moodboard-template.md · anti-descriptor-method.md · gate0-facilitation-guide.md*
*Classification: internal*
