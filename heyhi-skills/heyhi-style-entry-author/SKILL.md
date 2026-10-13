---
name: heyhi-style-entry-author
description: >-
  Build or validate a named style entry for the HeyHi Style Reference Library. Two modes: Mode A (build) and Mode B (validate). Mode A — build triggers: "write a style entry," "build the [style name] entry," "add [style] to the style library," "Session B," "Session F," "add a named style," "write [style name] for the style library," "populate the style library." Mode B — validate triggers: "validate this style entry," "check this entry before committing," "quality gate for Session F," "does this entry meet the bar," "run the schema tests on this," "is this entry ready to commit." Always run Mode B after Mode A's Smoke Test passes and before writing any entry to the library. Mode A encodes the full build procedure: vocabulary-sourced descriptor selection, anti-descriptor sharpening with four validity checks, sector intersection logic for hybrid styles, motion schema mapping. Mode B runs four quality tests: token_implications depth (traceable to visual_characteristics), keyword distinctness (no retrieval collision with existing entries), agent_context_snippet differentiation (non-interchangeable avoidance language), and typography pairing actionability (named fonts, not categories). Phase 2 (optional): adds a taste_profile to a committed entry. Triggers: "add a taste profile to [entry]," "document the boundary behaviors for [style]," "entry needs a taste profile," "author the aesthetic principles for [style]," "this entry is going into client work — document the taste." Phase 2 runs after the entry is committed to the library, not before. Mode C (curate an infra reference entry): "add an infra reference," "curate a reference for the infra set," "add [system] to the infra reference set," "infra reference entry for [territory]," "does this reference pass the curation bar," "validate this infra reference." Mode C authors one entry in `ai-services/design-intelligence/infra-reference-set.md` — a real, shipped civic/energy/government/operator UI captured as link + citation + HeyHi annotation, never a stored screenshot. It is a different artifact from a style entry; do not confuse the two. Mode C runs a selection bar (operator-grade and shipped, not a generic SaaS dashboard), an anti-slop annotation check, and a citation-only license discipline. Reference entries are validated by Mode C's own Curation Bar Smoke Test (Step C5), not by Mode B (whose four tests are style-entry-specific). Mode C is NOT for building a style entry (that is Mode A of this skill) — and this skill as a whole is NOT for a whole visual-language brief (use `heyhi-style-brief`).
---

# Style Entry Author

Build one complete, validated YAML style entry for the Style Reference Library. One invocation = one entry. The entry is pasted into `ai-services/design-intelligence/style-reference-library.md` when complete.

**Two artifact types.** Modes A and B build and validate **style entries** in `style-reference-library.md`. **Mode C** (below) curates **infra reference-set entries** in `ai-services/design-intelligence/infra-reference-set.md` — HeyHi's proprietary, human-curated exposure corpus for the civic / energy / government / operator-monitoring territory that no off-the-shelf reference library indexes. Different schema, different file, same disciplines. Read Mode C's own preamble before authoring a reference entry; the style-entry steps (1–10) and Mode B's tests do not apply to it.

---

> **Exit Gate (Flavor A).** This skill closes through the canonical Exit Gate — see `CLAUDE-SESSION-RULES.md § Exit Gate`. Required headers, in order: `## Fixes Applied`, `## Smoke Test`, `## Next Session Prompt`. Empty headers are visible failures.


## Before You Start

Load both files fully before writing a single field:

1. **`ai-services/design-intelligence/style-descriptor-vocabulary.md`** — full load required. Every term used in `mood`, `anti_mood`, and the `visual_characteristics` prose must come from this vocabulary. Do not invent ad hoc descriptors.

2. **`ai-services/design-intelligence/style-reference-library.md`** — load the proposed styles table to identify the style you're building, and load the schema for field reference.

---

## The Schema

Every entry must fill all mandatory fields. Optional enrichment fields are documented below the schema — add them when the entry warrants them (ADR-004).

```yaml
style:
  name: "Working label for the style"
  family: "Primary family — from the five cluster descriptions"
  modifier: "Secondary influence if hybrid — omit field entirely if pure"

  descriptors:
    mood: []       # 5–7 terms; primarily from vocabulary Category 1 (Mood/Tone)
    anti_mood: []  # 3–5 terms; run four validity checks on each before committing
    keywords: []   # noun-heavy searchable terms for agent retrieval

  visual_characteristics:
    color_approach: ""      # ~2 sentences; draw on vocabulary Category 5 (Color)
    typography_approach: "" # ~2 sentences; draw on vocabulary Category 4 (Typographic)
    spatial_approach: ""    # ~2 sentences; draw on vocabulary Category 3 (Spatial)
    surface_treatment: ""   # ~2 sentences; draw on vocabulary Category 2 (Material/Surface)
    motion_approach: ""     # ~1 sentence; name the motion term + its schema mapping
    imagery_approach: ""    # ~1 sentence; photography, illustration, or iconography direction

  token_implications:
    color_temperature: ""    # warm | cool | neutral
    spacing_density: ""      # spacious | balanced | dense
    border_radius_range: ""  # sharp | slight | rounded | pill
    shadow_depth: ""         # flat | subtle | material | dramatic
    type_scale_ratio: ""     # ratio notation + rationale (e.g., "Major Third 1.25x from 18px base")
    type_personality: ""     # humanist | geometric | grotesque | serif | transitional | slab
    motion_personality: ""   # minimal | purposeful | expressive — must match motion_approach

  layout_patterns:
    grid_preference: ""   # grid type + brief rationale
    content_width: ""     # narrow | standard | wide | full
    section_rhythm: ""    # 1 sentence on how vertical sections flow
    hero_approach: ""     # 1 sentence on typical hero treatment
    card_treatment: ""    # 1 sentence on how containers behave

  typography_specimens:
    recommended_pairings: [] # 2 pairings: "Display Font + Body Font (brief rationale)"
    heading_treatment: ""    # weight, case, tracking character (1 sentence)
    body_treatment: ""       # typeface feel, line-height, measure (1 sentence)

  industry_fit:
    natural: [] # 3–5 sectors where this style fits without explanation
    stretch: [] # 2–3 sectors where this works with deliberate adaptation
    avoid: []   # 2–3 sectors where this would actively mislead or fail

  reference_examples:
    - url: ""
      what_to_take: "" # specific element — not "this whole site is good"
    - url: ""
      what_to_take: ""

  agent_context_snippet: >
    Sentence 1: name the style and primary visual character.
    Sentence 2: describe what it produces visually.
    Sentence 3: state what it explicitly avoids.
```

---

## Step 1: Identify the Style

**Gate 0 — classify the label before authoring.** Before authoring an entry for a culturally-derived style, or adding one to the `styles.csv` build catalog, classify the label:

1. **Specific named tradition, craft, or scene** (Gzhel, Visual Kei, Khokhloma, Art Nouveau) → proceed, with a mandatory provenance / attribution note. For pan-regional families ("Slavic folk"), disaggregate by tradition — Russian / Ukrainian / Polish are distinct — rather than collapsing them into one.
2. **Flattening bundle** — a broad or Western-gaze descriptor that collapses multiple distinct cultures into one "look" (Fresh Ethno, Asian Store, Asian Chic) → **HOLD**. Do not author an entry or a build-catalog row until the ethical analysis is done: name the actual tradition, identify who owns the visual language, decide how the system should represent it. This mirrors the TR-2 ethical-use protocol and the `cultural_provenance` schema field.
3. **Scope-ambiguous concept** whose referent is not settled ("Pacific Punk Wave" — Pasifika punk vs. surf-punk-new-wave vs. tropical-vapor) → **HOLD** pending a scope decision from the instance owner.

When a blanket instruction ("add all of these") collides with this gate, apply the gate to the gated items, complete the rest, and surface the held items as a one-line correctable choice — neither silently comply nor silently refuse. Flattening labels and scope-ambiguous concepts must not be operationalized into the automated build catalog (`styles.csv`) even when an instruction says to add them, until their gate clears: operationalizing an unresolved cultural label into an automated pipeline crosses the "don't automate this" line (ethics judgment is not an automation candidate). Open question, not yet resolved: a label that is specific AND contested (a named tradition claimed by more than one nation, or under active ownership dispute) — surface to the instance owner rather than applying the tradition-vs-flattening test. Cross-references: `design-trend-research-plan.md` Sessions TR-2 and TR-9; `heyhi-style-selection` Gate 0 (this gate is canonical here; cross-reference, do not duplicate). Promoted from `skill-updates/` 2026-07-02.

Look up the style in the proposed styles table in `style-reference-library.md`. Note its cluster (A–E), family, modifier if any, key characteristics, and industry fit note. This is your brief. Every field decision must be defensible against it.

For hybrid styles — those with a modifier — the modifier introduces a secondary cluster's sensibility. Both the primary family and the modifier's cluster should inform descriptor and token choices throughout.

**Cluster placement for a gap-filling entry.** When the entry fills a named coverage gap (a family or sector listed in the library's coverage-gaps table with no entry), place it in the nearest existing cluster whose premise fits, following prior gap-fill precedent: Glamour (Desire / Luxury) and Quiet Craft were added to existing Clusters C and A, not to new clusters. Open a new cluster only when no existing cluster's premise fits. State the placement decision and its reversibility in the handoff, since re-clustering an entry is a one-line move.

---

## Step 2: Build Descriptors

### Mood (5–7 terms)

Select from vocabulary Category 1 (Mood/Tone). For hybrid styles, pull terms that represent both the primary family and the modifier — cross-cluster terms (grounded, earnest, considered, austere, restrained) are especially useful here. Each term should add information the others don't. Five near-synonyms is range collapse; cut and replace with distinct qualities.

### Anti-Mood (3–5 terms)

Anti-mood is not the opposite of mood. It is the set of qualities that would break the style's premise if they appeared. For each candidate anti-mood term, run four validity checks before committing:

**1. Specificity** — Is this exclusion specific to this style, or would every design direction exclude it? "Not generic" is noise. "Not warm" for a precision-first style is a real exclusion.

**2. Consequence** — If the style became this thing, would the direction collapse entirely, or just shift slightly? Real anti-moods cause collapse. Preferences cause slight shifts.

**3. Resolution** — Does this create a choice that a designer or client could reasonably make differently? If no one would choose the opposite, it's shared constraint, not a decision point.

**4. Brand alignment** — Can you trace this exclusion back to something the style's premise actually requires? If the only reason is aesthetic preference, it is not a valid anti-mood.

Anti-mood terms that fail checks 1 or 2 should be replaced. "Not generic," "not dated," and "not cheap" fail check 1 for almost every direction.

### Keywords (noun-heavy, searchable)

Keywords enable semantic retrieval when an agent matches a client context to a style. They should be nouns and compound nouns: sector terms, application types, visual register names. Do not repeat mood adjectives here — those are already captured. Aim for 6–10 terms.

---

## Step 3: Write Visual Characteristics

Write each sub-field in prose sentences. Use vocabulary terms when naming qualities — this is what makes entries comparable across the library. Word budgets:

- `color_approach`, `typography_approach`, `spatial_approach`, `surface_treatment`: ~2 sentences each
- `motion_approach`, `imagery_approach`: ~1 sentence each

**color_approach:** Name the palette territory (vocabulary Category 5), then describe how color is deployed — accent strategy, background logic, whether functional color exists in the system.

**typography_approach:** Name the type personality (vocabulary Category 4), then describe the hierarchy approach — scale logic, weight strategy, tracking and leading character.

**spatial_approach:** Name the spatial character (vocabulary Category 3), then describe how sections and components use space — density, breathing intervals, content width preference.

**surface_treatment:** Name the surface quality (vocabulary Category 2), then describe specific treatment decisions — corner radius logic, shadow system, border presence or absence.

**motion_approach:** Name the motion vocabulary term(s) that fit this style, state what they produce, then note the schema value they map to. Format: "Motion is [term] — [description] (schema: `motion_personality: [value]`)."

**imagery_approach:** Name the imagery character using vocabulary Category 8 (Photography/Imagery), then describe the visual register in one sentence. Photography direction: documentary, reportage, constructed, editorial, cinematic, spatial, process, data-visual, abstracted. Illustration: line-driven, diagrammatic, geometric-illustration, textured-hand. Iconography: outlined, filled, custom-mark. Use the vocabulary term first, then describe what it produces in this style.

---

## Step 4: Map Token Implications

Token implications translate style feeling into token-level decisions. Each field has constrained values — use only the options listed. The values here feed directly into Mode D (design-system-onboard) token extraction.

**color_temperature** (`warm | cool | neutral`): Based on the palette's thermal direction. Neutral when the palette is achromatic or deliberately temperature-balanced.

**spacing_density** (`spacious | balanced | dense`): Based on `spatial_approach`. Spacious = generous margins and section intervals. Dense = high information count, compressed spacing. Balanced = neither extreme.

**border_radius_range** (`sharp | slight | rounded | pill`): Based on `surface_treatment`. Sharp = 0px, no softening. Slight = 2–4px. Rounded = 8px or more. Pill = fully rounded elements.

**shadow_depth** (`flat | subtle | material | dramatic`): Based on `surface_treatment`. Flat = no shadow system. Subtle = low-opacity, minimal blur. Material = distinct elevation layers. Dramatic = strong shadow as compositional element.

**type_scale_ratio:** Name the scale (e.g., Major Third 1.25x, Perfect Fourth 1.333x) and give one phrase of rationale tied to the style's reading intent.

**type_personality:** Must align with `typography_approach`. Choices: humanist, geometric, grotesque, serif, transitional, slab.

**motion_personality** (`minimal | purposeful | expressive`): Must match the schema mapping noted in `motion_approach`. If the motion vocabulary terms used map to `purposeful`, this field must say `purposeful`. The vocabulary's schema mapping column is the authority.

**Optional enrichment fields (add when the entry warrants them):**

- `default_scheme: dark` — Add ONLY when the entry is dark-native or dark-viable as its primary baseline. Omit for all light-baseline entries (light is the implicit default). Current dark entries: Entry 2, 3, 10, 15.
- `border_radius_strategy` — Add when the entry requires variable radius logic (e.g., "0px structural, 2–4px interactive") that the single-enum `border_radius_range` field cannot express.
- `shadow_depth` annotation — When an entry's shadow_depth diverges from its modifier's delta table, add an inline comment explaining the intentional override.

---

## Step 5: Document Layout Patterns

**grid_preference:** Name the grid type, then one phrase of rationale. Example: "12-col — professional standard; asymmetric column assignment supports text/image split layouts."

**content_width:** Based on the style's spatial character and reading intent. Narrow (600–720px) = reading-optimized. Standard (~1200px) = general layouts. Wide (1440px+) = visual dominance. Full = edge-to-edge imagery or data.

**section_rhythm:** Describe how vertical sections flow — whether intervals are consistent, whether any sections break the rhythm for emphasis, whether spacing scales as the page develops.

**hero_approach:** One sentence on what a typical hero section looks like in this style — what elements appear, how they're arranged, what the dominant impression is.

**card_treatment:** One sentence on how containers behave — border presence, shadow, background distinction, radius, whether cards feel elevated or flush.

---

## Step 6: Select Typography Specimens

**recommended_pairings:** Two specific pairings. Format: "Display Font + Body Font (brief rationale)." Choose pairings a competent designer would actually specify for this style. Generic utility pairings (Roboto + Open Sans) do not demonstrate craft and should not appear here.

**heading_treatment:** One sentence covering weight, case (title case, all caps, sentence case), and tracking character for headings.

**body_treatment:** One sentence covering typeface feel, line-height, and measure (column width target) for body text.

---

## Step 7: Define Industry Fit

**natural:** Industries where this style would be commissioned without any justification. 3–5 entries. These are sectors where the style's visual language already matches the audience's expectations.

**stretch:** Industries where this style works with deliberate adaptation. 2–3 entries. If the adaptation required is non-obvious, note what it is in a brief parenthetical.

**avoid:** Industries where this style would actively mislead or underperform. 2–3 entries. Be specific — "direct-to-consumer food/beverage" is useful. "Casual contexts" is not.

---

## Step 8: Find Reference Examples

Two examples minimum. These are real websites or products that demonstrate specific aspects of this style well. The `what_to_take` field is mandatory and must name a specific element — a grid system, a shadow treatment, a typography pairing, a spacing convention — not a general endorsement of the site's quality.

Avoid overused design references (Stripe, Apple, Linear) unless the `what_to_take` note is genuinely precise and teaches something about this specific style that isn't already widely known.

---

## Step 9: Write the Agent Context Snippet

This is the field most used in downstream generation. It will be injected as context when an agent applies this style. Write it last, after all other fields are complete — it should summarize the entry, not repeat it.

Structure:
1. **Sentence 1:** Name the style and its primary visual character in one phrase.
2. **Sentence 2:** Describe what it produces — what a piece of work in this style looks and feels like.
3. **Sentence 3:** State what it explicitly avoids, drawn from the anti-mood.

Precision over elegance. The snippet should be readable by an agent that has no other context about this style and still give it enough to make consistent generation decisions.

---

## Step 10: Output

Paste the completed YAML entry into `style-reference-library.md` in the appropriate cluster section (A–E), after the proposed styles table. Use the cluster headings already in the file.

**Propagate in the same change.** A new entry touches more than its own block. In the same edit, update the cluster's row in the proposed-styles table, the `## Proposed Styles — N Entries` header count, and (if the entry fills a documented gap) the coverage-gaps table status for that family. While in the coverage-gaps table, verify the *other* rows are not stale against the current entry set: a prior gap may have been filled without the table being updated. (When Entry 23 was added, both the header count and a coverage-gaps row were already stale by one entry.)

**Verify the insert mechanically.** After writing, confirm with a quick grep rather than by eye: the `entry_id` count incremented by one; the entry name appears in each expected location (cluster table row, coverage-gaps row if applicable, entry header, `name` field, snippet); and an em-dash scan of the entry block returns only the markdown entry-header's em dash.

**Discrimination check for a brief-specific entry.** If the entry was authored to serve a specific client brief rather than as general library coverage, validate that it discriminates before committing: run `heyhi-style-selection` against that brief and confirm the new entry scores a clean high-confidence primary, and that no other entry reaches the secondary threshold. A collision means the entry is not pulling its weight; sharpen it rather than shipping a self-fulfilling entry.

If this is a Session B pilot entry (one of the five: Grounded Modern, Warm Technical, Editorial Bold, Energy Redesign, Studio Craft), record which entries are complete in the Phase 1 Build Plan checkboxes at the end of the file. After all five Session B entries are complete, answer the four schema test questions listed in the execution plan's Session B scope before marking Phase 1 done.

Order of operations: the Smoke Test and Mode B (both below) must pass, and for a brief-specific entry the discrimination check above must clear, before you write and propagate the entry. The output steps are listed first here, but the validations gate them.

---

## Phase 2: Taste Profile (Optional)

**What it is.** The `taste_profile` field extends a committed style entry with documented aesthetic principles, boundary behaviors, restraint notes, and contrast pairs. It is the mechanism that enables the CONSIDERED_DEPARTURE path in `heyhi-style-to-token-reviewer` and `heyhi-pipeline-validator` — a PARTIAL result in a pipeline check can resolve to CONSIDERED_DEPARTURE when the entry's taste_profile documents the departure as intentional. Without a taste_profile, all PARTIALs fire at full weight.

**When to trigger Phase 2.** Author a taste_profile when any of these conditions are true:

- The entry is being used in active client work or pipeline work
- The entry has known modifier-override patterns (e.g., shadow_depth or border_radius_range diverge from the modifier's defaults)
- WS2 (Performed Translation) or WS5 (Supporting Token Temperature) checks are likely to PARTIAL on this entry's token config
- The user explicitly requests it ("document the taste for [style]," "add a taste profile to [entry]," "this entry goes into client work — document the boundary behaviors")

**When NOT to trigger Phase 2.** Do not author a taste_profile as part of Mode A or Mode B during initial entry build. Phase 2 is a distinct activity that runs after the entry has been committed to the library and after at least one pipeline run has identified candidate boundary behaviors. Authoring taste_profiles speculatively for entries not yet in use wastes context and produces weaker content — real boundary behaviors emerge from actual pipeline runs.

**Reference implementation.** Entry 17 (Studio Craft) is the first taste_profile in the library. Load it as the structural template before writing.

---

### Step P2-1: Identify Boundary Trigger Points

Before writing any taste_profile content, scan the entry's `token_implications` and `visual_characteristics` for patterns likely to produce PARTIAL checks in the pipeline. For each pattern, name the check that would fire and the specific token values or conditions involved.

Common trigger patterns to look for:

| Pattern | Check that fires | Why it fires |
|---------|-----------------|-------------|
| Warm temperature declared but palette is muted or near-achromatic | WS2 (Performed Translation) | Reviewer measures background hex against declared warm; muted palette does not register as warm at the hex level |
| Organic modifier declared but shadow_depth: flat | Stage 4 modifier delta check | Organic modifier default is shadow_depth: subtle; flat departs from the table |
| Organic modifier declared but border_radius_range: sharp | Stage 4 modifier delta check | Organic modifier default is slight or rounded; sharp departs from the table |
| Serif body type with humanist type_personality declared | WS3 (Typography Coherence) | humanist type_personality implies sans; serif body is an unusual but valid departure |
| High-contrast semantic utility colors in an earth-tone palette | WS6 (Semantic Orphan) | Saturation gap between natural palette and functional colors triggers orphan check |
| Variable radius strategy (sharp structural, slight interactive) | Stage 3 radius uniformity check | Single enum border_radius_range cannot express variable strategy; 0px structural frames flag as mismatched |

Document each trigger point as a named candidate before writing the boundary_behaviors. Aim for 1–3 that are specific to this entry. Do not write boundary behaviors for generic patterns that apply to every style.

---

### Step P2-2: Author Aesthetic Principles (3–5)

Aesthetic principles are the animating values of the style — the reasons behind the design decisions, stated operationally. They explain how the style's taste operates at boundary cases, not just what it sounds like as a value statement.

For each principle:
- **Name:** A short phrase naming the animating value (not a banned word; not a generic design virtue)
- **Description:** What the principle means operationally. How it guides judgment at the specific boundary cases this style encounters. Not "we value X" but "when X appears, this is why it is present and what breaks if it is absent."

Write 3–5 principles. Each should be specific enough that a reviewer could use it to distinguish CONSIDERED_DEPARTURE from incoherence on a real pipeline check. Generic principles ("craft matters," "less is more") provide no diagnostic value.

**Test:** After writing each principle, ask: could I apply this principle to resolve a PARTIAL on a specific check? If the answer is no for every check in this entry's likely pipeline run, the principle is too abstract.

---

### Step P2-3: Author Boundary Behaviors (1–3)

Each boundary_behavior documents a specific pipeline check that is expected to fire on this entry's token configs, and provides the resolution logic for determining CONSIDERED_DEPARTURE vs. incoherence.

All five subfields are required for every boundary_behavior. A boundary_behavior entry without all five subfields cannot support a CONSIDERED_DEPARTURE resolution — Criterion 3 (Not-a-Departure Conditions Absent) in the taste review gate requires `not_a_departure_if` to be populated.

**ID format:** `BB-[2–3 letter style code]-[nn]` — e.g., BB-SC-01, BB-QC-02, BB-SS-03. The style code should be consistent across all boundary_behaviors for this entry.

For each of the trigger points identified in P2-1, write one boundary_behavior:

```yaml
- id: "BB-[code]-[nn]"
  trigger: >
    Which pipeline check fires. Name the check specifically (WS2, WS6, Stage 4 modifier delta,
    Stage 3 radius uniformity). Describe what the reviewer sees when the check fires.
  situation: >
    The specific token values or configuration conditions that produce the PARTIAL.
    What the check is measuring, what value it expects, what value the config has.
  resolution: >
    How to determine whether this is CONSIDERED_DEPARTURE vs. incoherence.
    What to look for in the composition. What to document in the rationale field
    when recording the departure.
  not_a_departure_if: >
    The condition that distinguishes restraint from error. When the same trigger
    indicates genuine incoherence rather than a documented aesthetic choice.
    This field is the Criterion 3 gate for taste review — if this condition is
    present, the PARTIAL is not a departure; it is a genuine problem.
```

Write boundary behaviors for the 1–3 highest-probability trigger points. Do not write boundary behaviors for hypothetical checks that haven't fired or are unlikely given the entry's token values.

---

### Step P2-4: Author Restraint Notes (3–6)

Restraint notes document what the style refuses and why — written as critical reasoning, not prohibition. Each note should:

1. **Name the refusal** — what the style does not do (no decorative shadows, no competing typefaces, no oversaturated accent)
2. **State the consequence** — what breaks if the refusal is violated, and specifically what it breaks (the type hierarchy competes with elevation; the foundry relationship dissolves; the accent loses its signal weight)

The note should be long enough to explain the reasoning but short enough to be referenced during a review. 2–4 sentences per note. Write 3–6 notes.

**Test:** After writing each restraint note, ask: does this explain *why* the restraint exists and *what collapses* if violated? If the note is only a prohibition without a consequence, rewrite it.

---

### Step P2-5: Author Contrast Pairs (2–3)

Contrast pairs document entries in the library that are easy to confuse with this style, and precisely where the distinction lies. They are the disambiguation layer for agents and reviewers who have seen two near-identical token configs and need to know which style is actually being expressed.

For each contrast pair:

```yaml
- style: "Style Name (Entry N)"
  surface_similarity: >
    What makes these styles easy to confuse at the token level or first-impression level.
    Be specific: same temperature, same spacing density, similar type personality, shared
    industry territory. The confusion must be real — pairs that are obviously different
    at a glance are not useful contrast pairs.
  taste_distinction: >
    What distinguishes them at the taste level. Not token values — what the eye reads
    and what the design is doing for the user. Specific enough to apply to a real layout
    decision. A useful distinction can be stated as a test: "Apply this to [content type].
    If the layout is optimizing for [X], that is [Style A]. If it is optimizing for [Y],
    that is [Style B]."
```

Write 2–3 contrast pairs. Priority: styles in the same cluster or adjacent cluster with overlapping temperature and spacing values. Use the Style Reference Library's keyword and token_implications data to identify candidates.

---

### Step P2-6: Taste Profile Smoke Test

Before inserting the taste_profile block into `style-reference-library.md`, verify:

- [ ] `authored` field set to today's date (YYYY-MM-DD)
- [ ] `aesthetic_principles` count: 3–5
- [ ] Each principle has both `principle` (name) and `description` (operational) fields
- [ ] Each description is specific to this entry — could not appear verbatim in a different style's taste_profile
- [ ] `boundary_behaviors` count: 1–3
- [ ] All five required subfields present in every boundary_behavior entry: `id`, `trigger`, `situation`, `resolution`, `not_a_departure_if`
- [ ] IDs follow BB-[code]-[nn] format and are consistent across all behaviors in this entry
- [ ] `restraint_notes` count: 3–6
- [ ] Each restraint note names the refusal AND states the consequence
- [ ] `contrast_pairs` count: 2–3
- [ ] Each contrast pair has both `surface_similarity` and `taste_distinction`
- [ ] `taste_distinction` for each pair is specific enough to apply to a real layout decision (not just "they feel different")
- [ ] No banned words (leverage, unlock, seamless, holistic, empower, transformative, etc.)
- [ ] No "AI" as a standalone word
- [ ] Em dashes: `style-reference-library.md` is an internal agent-readable document, never audience-facing — the 2-em-dash limit does not apply here (same exemption as internal research documents per OPERATING_PRINCIPLES.md). Em dashes may be used freely in taste_profile prose. If the taste_profile is being extracted into an audience-facing document (e.g., a client brief), apply the standard 2-per-section limit at that stage.
- [ ] "ecosystem" (if used): confirm the use is ecological/biological, not in the business sense. If ambiguous, replace with "ecological system" or "natural system" to avoid scanner false-positives.

After the smoke test passes, insert the `taste_profile` block into the style entry in `style-reference-library.md`, immediately after the `agent_context_snippet` field and before the closing ` ``` ` delimiter.

---

## Supporting References

| Reference | Category | When to Load |
|-----------|----------|--------------|
| `SENSITIVE_CONTEXT_OVERRIDE.md` | Pattern | When an entry's `industry_fit.natural` includes mental health, crisis, trauma, neurodivergent, grief, recovery, or high-stakes decision contexts. Documents the motion override pattern for sensitive-context entries. |
| `ai-services/design-intelligence/infra-reference-set.md` | Corpus | When authoring or validating a Mode C infra reference entry. The owned exposure corpus and its coverage ledger. |
| `plans/plan-infra-reference-set-2026-06-17.md` | Plan | When curating depth (Phase 3) or wiring the corpus into the Audit (Phase 4). Selection bar §6, schema §5, phasing §10, constraints §7. |

---

## Smoke Test (Mode A — Structural)

Before marking the entry complete, verify:

- [ ] All `mood` terms come from the vocabulary (not invented)
- [ ] All `anti_mood` terms come from the vocabulary
- [ ] `mood` count: 5–7
- [ ] `anti_mood` count: 3–5
- [ ] Each `anti_mood` term passed at minimum checks 1 and 2 (specificity + consequence)
- [ ] `motion_personality` value matches the schema mapping declared in `motion_approach`
- [ ] `token_implications` constrained fields use only the enumerated values listed in the schema
- [ ] `keywords` are noun-heavy — not duplicates of `mood` adjectives
- [ ] `recommended_pairings` are real, specific font names — not placeholders
- [ ] `reference_examples` have real URLs and specific `what_to_take` notes
- [ ] `agent_context_snippet` is 2–3 sentences
- [ ] No HeyHi banned words (leverage, unlock, seamless, holistic, empower, supercharge, disrupt, etc.)
- [ ] No "AI" as a standalone word anywhere in the entry
- [ ] Em dashes: none in single-line YAML value annotations (`type_scale_ratio`, `grid_preference`, `what_to_take`, `industry_fit` parentheticals); ≤2 total across all `visual_characteristics` prose blocks and `agent_context_snippet` combined. Em dashes accumulate quickly across a multi-field entry — count them before submitting. Replace extras with colons, semicolons, or restructure the sentence. This per-entry cap governs entry authoring and overrides the document-level internal-doc em-dash exemption in `OPERATING_PRINCIPLES.md`; that exemption applies only to free-prose `taste_profile` blocks (Phase 2), not to the structured entry fields here.
- [ ] If the entry's `industry_fit.natural` includes any sensitive-context scope conditions (mental health, crisis, trauma, neurodivergent, grief, recovery, high-stakes decisions), verify that a `motion_override` block has been added per `SENSITIVE_CONTEXT_OVERRIDE.md`.

If the Smoke Test passes, proceed to Mode B before writing the entry to the library.

---

## Mode B: Validate an Entry

Run after the Smoke Test passes. The Smoke Test checks structure. Mode B checks quality — four semantic tests that determine whether an entry can carry its weight in downstream Mode D token extraction, agent retrieval, and style generation.

**When to trigger:** Any of these: "validate this style entry," "check this entry before committing," "quality gate," "does this entry meet the bar," "run the schema tests on this."

**Load:** The drafted entry + `ai-services/design-intelligence/style-reference-library.md` (for Tests 2 and 3).

---

### Test 1: Token Implications Depth

**Question:** Are the `token_implications` fields specific enough that Mode D can generate a first-pass config from them without needing to re-read `visual_characteristics`?

For each field, verify two things: the enum value is valid, and it is traceable to a specific claim in `visual_characteristics` — not a guess or a default.

- `color_temperature`: Is warm/cool/neutral supported by a specific observation in `color_approach`?
- `spacing_density`: Is spacious/balanced/dense supported by a specific claim in `spatial_approach`?
- `border_radius_range`: Is sharp/slight/rounded/pill supported by a specific statement in `surface_treatment`?
- `shadow_depth`: Is flat/subtle/material/dramatic supported by a specific statement in `surface_treatment`?
- `type_scale_ratio`: Is the ratio + rationale specific to this style's reading intent, or is it a generic default?
- `type_personality`: Does it exactly match the type category named in `typography_approach`?
- `motion_personality`: Does it exactly match the schema mapping declared in `motion_approach`?

**PASS:** All fields present, valid, and traceable.
**FAIL:** List each gap: `"shadow_depth: 'subtle' selected, but surface_treatment says 'no elevation system' — value should be 'flat'."`

---

### Test 2: Keyword Distinctness

**Question:** Do the keywords create retrieval collision with any existing library entry?

For each keyword in the new entry, check whether it appears in 2+ existing entries. **Prefer grep per candidate keyword over loading every entry** (`grep -niE 'keyword1|keyword2' style-reference-library.md`): a clean grep (no hits outside the new entry's own territory) confirms zero collision at a fraction of the token cost the full-file load would burn as the library grows (Earn the Room). Use the same pass to map the insertion point: `grep -nE '^### (Entry|Cluster)'`. Collision threshold: 3 or more keywords shared between the new entry and a single existing entry = retrieval ambiguity risk.

**PASS:** No single existing entry shares 3+ keywords with the new entry.
**FAIL:** Name the colliding entry and list the shared keywords. Recommend: "(a) replace shared keywords with more specific terms, or (b) if the styles are genuinely distinct, the distinguishing characteristics should be in the keywords — add them."

---

### Test 3: Agent Context Snippet Differentiation

**Question:** Is Sentence 3 of the `agent_context_snippet` specific and non-interchangeable — something only this style would generate?

Read Sentence 3. Ask: could this exact sentence appear verbatim in 2+ other style entries without being false? If yes, the avoidance is too generic. "Avoids decoration for its own sake" applies to almost every professional direction. "Avoids warmth that would soften the infrastructure signal" is specific to one cluster.

Also check:
- Sentence 1: Does it name the style's primary visual character specifically, beyond just the style name?
- Sentence 2: Does it describe what a piece of work in this style looks and feels like with enough specificity that a designer could hold it in mind while making decisions?

**PASS:** All three sentences are specific, non-interchangeable, and sufficient for downstream generation.
**FAIL:** Note which sentence and why. Provide a rewrite direction: `"Sentence 3 is too generic — 'avoids visual noise' applies to A, D, and most C entries. Replace with what would actively break this style's premise: [direction specific to this entry]."`

---

### Test 4: Typography Pairing Actionability

**Question:** Are both `recommended_pairings` entries real, named typefaces a designer could license and specify today?

For each pairing:
1. Does it contain actual font names — not categories like "humanist sans" or "transitional serif"?
2. Are both fonts real and commercially available (Google Fonts, Adobe Fonts, or a known foundry)?
3. Does the rationale explain *why* this pairing fits this style specifically — not just that it is a valid pairing in general?

**PASS:** Both pairings have named fonts, both are verifiably real and licensable, both rationales are style-specific.
**FAIL:** Note each failure with a specific correction. For category-only pairings: `"Replace the category description with a specific font name. For a [style description] direction, consider: [2–3 named options with provider notes]."`

---

### Mode B Output Format

Return a structured validation report:

```
## Style Entry Validation Report
Entry: [Style Name]
Validated against: [N] existing entries in style-reference-library.md

Test 1 — Token Implications Depth:     [PASS / FAIL]
[If FAIL: specific field failures with correction instructions]

Test 2 — Keyword Distinctness:          [PASS / FAIL]
[If FAIL: colliding entry name + shared keywords + recommendation]

Test 3 — Agent Context Differentiation: [PASS / FAIL]
[If FAIL: which sentence + why + rewrite direction]

Test 4 — Typography Pairing Actionability: [PASS / FAIL]
[If FAIL: which pairing + correction instruction with named alternatives]

Overall: PASS — ready to commit to style-reference-library.md
     OR: FAIL — [N] issue(s) require correction before committing
```

All-PASS entries are ready to write to `style-reference-library.md`. Any FAIL holds the commit until the issue is corrected and the test re-run.

---

## Mode C: Curate an Infra Reference Set Entry

Curate one entry for `ai-services/design-intelligence/infra-reference-set.md` — HeyHi's owned exposure corpus for the territory no commodity UI-reference library covers (civic, government, energy/grid, industrial-operator monitoring, geospatial operations). The 2026-06-17 reference-corpus probe found the commodity libraries (Mobbin, Refero, Nicelydone) effectively null-to-thin on this territory (Mobbin thin-to-absent); HeyHi curates its own because it cannot license this in. Origin and full rationale: `plans/plan-infra-reference-set-2026-06-17.md`.

**The hard frame — read before curating.**
- **Curation is the product.** The value is taste, not volume. This is a don't-automate-this surface: a human selects the reference and writes the analysis. The set informs judgment; it never authors it. (Ties to the taste-cultivation keystone — exposure plus comparison is the first mechanism, and this corpus *is* HeyHi's structured exposure for the niche.)
- **The annotation is the asset.** Anyone can paste a URL. What makes an entry citable in a client Audit — without exposing third-party copyright — is HeyHi's own written `what_to_take` / `why` / `anti_pattern`. The words are the owned material.
- **Reference by citation only.** Store the URL and the analysis. Never store, embed, or republish a screenshot of the referenced system. A build that reproduces a referenced screen is a defect, not a feature; an Audit deliverable that embeds one re-opens the third-party-copyright wall the whole corpus is designed to avoid.

**When to trigger Mode C:** "add an infra reference," "curate a reference for the infra set," "add [system] to the infra reference set," "infra reference entry for [territory]," "does this reference pass the curation bar," "validate this infra reference."

**Validation.** A reference entry is checked by the Step C5 Curation Bar Smoke Test below. Mode B (Tests 1–4) is style-entry-only — its keyword-distinctness, snippet-differentiation, and typography-actionability tests do not apply to a reference entry. Do not run Mode B on a reference entry.

**Load before authoring:**
1. `ai-services/design-intelligence/infra-reference-set.md` — the corpus (how-to-use header, existing entries to avoid duplicating, the coverage ledger).
2. `ai-services/design-intelligence/compositional-layout-patterns.md` — patterns 19 (Control Center Grid), 20 (Geospatial + Data Panel), 21 (Civic Information Layer), 22 (Timeline Monitor), for the `pattern_ref` mapping.
3. `ai-services/design-intelligence/style-reference-library.md` — Cluster D entries 13 (Energy Redesign), 15 (Invisible Grid), 16 (Civic Modern), for the `pattern_ref` mapping.

### The Mode C schema (extends the `reference_examples` convention)

This reuses the existing `reference_examples` convention in `style-reference-library.md` (the `{url, what_to_take}` shape) and extends it. Schema-compatible with what ui-studio step 4.5 and the style entries already read.

```yaml
- url: "https://… (publicly reachable; the real system)"
  source: "Product / org name (e.g. NESO — National Energy System Operator)"
  territory: "operator-monitoring | energy-grid | civic-gov | geospatial-ops"
  pattern_ref: "<name the actual pattern 19–22 and/or Cluster D entry 13/15/16 — format placeholder; see the worked example>"
  what_to_take: "the specific element to learn from"
  why: "why it works for this territory (the taste reasoning)"
  anti_pattern: "the failure it avoids (what NOT to do)"
  captured_at: "YYYY-MM-DD (recency matters; infra UIs change)"
  curator: "who selected it"
  license_note: "reference-by-citation only; no screenshot stored or reproduced"
```

`captured_at` and `license_note` are the two additions that make this a durable, defensible corpus rather than a frozen prose list.

### The four territories

Every entry belongs to exactly one territory. Use this table to classify and to pick the `pattern_ref`. (Reconciled with the corpus's territory sections and coverage ledger.)

| `territory` | What it covers | Patterns | Cluster D |
|-------------|----------------|----------|-----------|
| `operator-monitoring` | SCADA, NOC, control rooms, observability/incident consoles — dense, at-a-glance system state for trained operators | 19 Control Center Grid, 22 Timeline Monitor | 15 Invisible Grid |
| `energy-grid` | Grid/utility operations, generation/transmission/DERMS, energy status for a mixed operator + regulator + public audience | 20 Geospatial + Data Panel | 13 Energy Redesign |
| `civic-gov` | Government and public-services UIs — task flows, benefits, permitting, public information, transit | 21 Civic Information Layer | 16 Civic Modern |
| `geospatial-ops` | Spatial operations consoles — transit/fleet/emergency-ops, GIS operations where the map is the primary work surface | 20 Geospatial + Data Panel | 13 Energy Redesign, 15 Invisible Grid |

The boundary that matters most: `operator-monitoring` is organized around system state (panels, timelines); `geospatial-ops` is organized around a map as the primary surface. When a system genuinely spans two (e.g. a grid console that is both energy and spatial), pick the primary territory and name the second in `pattern_ref`.

### Step C1: Pass the Selection Bar (gate — before writing anything)

Every candidate clears all five before it earns an entry. This is the bar; a candidate that fails any line is rejected, not softened.

1. **Real and shipped.** A production system that real operators, residents, or staff use — not a concept, a dribbble shot, a redesign-concept, or a vendor's marketing mock. Public, reachable URL.
2. **Operator-grade for its territory.** It must exemplify the *territory's* working pattern, not a generic SaaS dashboard wearing infra clothing. The probe surfaced the exact trap: a search for "monitoring" returns Neon and Vercel (developer-marketing dashboards), not control rooms. A consumer analytics dashboard with hero numbers and generous whitespace is a rejection for operator-monitoring, however polished.
3. **Exemplifies a named pattern.** It maps cleanly to at least one compositional pattern (19–22) and/or a Cluster D entry (13/15/16). If you cannot name the pattern it teaches, it is not a reference — it is a bookmark.
4. **Teaches one specific thing.** There is a single, nameable element worth taking (a panel-grid discipline, a status-vocabulary restraint, a timeline-fusion move). "This whole system is good" is not a selection; it is an endorsement, and endorsements do not earn entries.
5. **Current enough to cite.** The system reflects how the territory ships *now*. An abandoned or visibly dated UI is worse than no reference — it teaches the wrong thing with false authority.

**Record instructive rejections.** When a strong candidate fails the bar (a polished dashboard that is not operator-grade; a striking concept that never shipped), note it once in the curation log or session handoff with the bar line it failed. This sharpens the bar over time and stops the same generic candidate being re-proposed each cycle. Do not store its screenshot either — a rejected reference is still reference-by-citation.

**Worked example — the bar met.** This seed entry clears all five lines; use it to calibrate:

```yaml
- url: https://play.grafana.org
  source: Grafana (official public play instance)
  territory: operator-monitoring
  pattern_ref: "pattern 19 (Control Center Grid); Cluster D entry 15 (Invisible Grid)"
  what_to_take: A panel grid where every tile is one metric with a sparkline, a threshold color, and a fixed position; the time-range control is global to the whole board.
  why: Operators scan by spatial memory; the same panel is always in the same place, so an anomaly registers as a color or shape change, not a reading exercise. Density serves recognition speed.
  anti_pattern: Dressing it as a consumer analytics dashboard with hero numbers and generous whitespace; the operator needs the whole system at a glance, not a curated highlight.
```

Why it passes: **(1) real/shipped** — the official public play instance, reachable; **(2) operator-grade** — a working panel grid for trained operators, not a marketing surface; **(3) named pattern** — Control Center Grid (19) + Invisible Grid (15); **(4) one specific thing** — the fixed-position, one-metric-per-tile grid with a global time control; **(5) current** — Grafana is actively shipped. The annotation passes anti-slop: the `why` (operators scan by spatial memory) is true of this territory and would be false under a consumer-app reference.

### Step C2: Map territory + pattern_ref

- `territory`: exactly one of `operator-monitoring | energy-grid | civic-gov | geospatial-ops` (see the territory table). If a system genuinely spans two, pick the primary and name the second in `pattern_ref`.
- `pattern_ref`: name the compositional pattern (19–22) and/or the Cluster D entry (13/15/16) the reference grounds. Verify the number against the source files (the "Load" list) — do not assert a pattern number from memory. Format mirrors the seed: `"pattern 20 (Geospatial + Data Panel); Cluster D entry 13 (Energy Redesign)"`.

### Step C3: Write the annotation (the anti-slop check)

The three analysis fields are where the entry becomes HeyHi's owned material. Each has a discipline; an annotation that fails it is slop and gets rewritten, not committed.

- **`what_to_take`** — name a *specific element*, not the system. Failing: "great dashboard design." Passing: "a panel grid where every tile is one metric with a sparkline, a threshold color, and a fixed position; the time-range control is global to the whole board."
- **`why`** — the taste reasoning specific to *this territory*. Why does this move work *here*, for *this* audience (operators scanning by spatial memory; a mixed public/regulator audience that needs plain language; an incident responder who only needs chronological truth)? Generic UX praise ("it's clean and intuitive") fails. The `why` must say something that would be false if pasted under a consumer-app reference.
- **`anti_pattern`** — name the concrete failure this choice avoids. Not "bad design" — the specific wrong turn (e.g. "dressing it as a consumer analytics dashboard with hero numbers and generous whitespace; the operator needs the whole system at a glance, not a curated highlight"). The anti_pattern is what keeps the entry usable as a benchmark line in an Audit.

**Anti-slop test (run on every entry):** could `what_to_take` / `why` / `anti_pattern`, as written, appear verbatim under three other systems in the same territory? If yes, the annotation is generic — sharpen it until it is true of *this* reference and few others. (Same discipline as Mode A's keyword-distinctness and snippet-differentiation tests, applied to reference annotations.)

### Step C4: Stamp provenance + license

- `captured_at`: today's date (YYYY-MM-DD). This drives the Care refresh cadence.
- `curator`: who selected it (e.g. "HeyHi" for seed/internal; a named curator for engagement curation).
- `license_note`: verbatim `reference-by-citation only; no screenshot stored or reproduced`. Non-negotiable on every entry.

**License discipline — lockstep (reproduce exactly, do not paraphrase).** The citation-only license language is a cross-artifact invariant: it must stay identical across three places — this mode, the Audit `sector_benchmark` add-on (`skill-updates/heyhi-design-intelligence-audit/sector-benchmark-addon-2026-06-17.md`), and the corpus (`ai-services/design-intelligence/infra-reference-set.md`). Producer (Mode C) and consumer (the add-on) must never drift; if the license language changes in one, it changes in all three. The canonical strings:

> "reference-by-citation only; no screenshot stored or reproduced" — the `license_note` every entry carries.

> "Reference, not reproduction. Each entry is a link + citation + HeyHi's own analysis. The screen is never stored or republished — the URL and the written what_to_take / why / anti_pattern are the asset." — `infra-reference-set.md`, "How to use this set."

> "Exposure for judgment, behind a human gate. It informs taste; it never authors it. A build that reproduces a referenced screen is a defect, not a feature." — `infra-reference-set.md`, "How to use this set."

> "Citation + HeyHi's own words only. Link to publicly-reachable systems; do not store or republish third-party screenshots." — `plan` §7 R1 (Licensing).

This is the R1 moat: it is exactly what lets the corpus ground a client Audit where a republished third-party screenshot could not. A stored screen breaks it.

**On URLs:** entries are **curator-asserted** — selected from HeyHi's knowledge of these systems, not necessarily live-checked at write time. That is acceptable at authoring; Design System Care spot-verifies reachability and refreshes annotations each cycle. Do not block an entry on a live fetch, but do not invent a URL either: if you are not confident the system is publicly reachable at the asserted address, mark it for Care verification in the handoff rather than asserting a guess.

### Step C5: Curation Bar Smoke Test

Before pasting the entry, verify:

- [ ] All ten schema fields present and populated
- [ ] `territory` is exactly one of the four enum values (see the territory table)
- [ ] `pattern_ref` names a pattern (19–22) and/or Cluster D entry (13/15/16) confirmed against the source files — not asserted from memory
- [ ] Selection bar (C1) passes all five lines; the system is real, shipped, operator-grade, pattern-exemplifying, and current
- [ ] `what_to_take` names a specific element, not the whole system
- [ ] `why` is territory-specific taste reasoning, not generic UX praise (anti-slop test passed)
- [ ] `anti_pattern` names a concrete failure mode, not "bad design"
- [ ] `license_note` is present and verbatim; no screenshot is stored, embedded, or linked as an image
- [ ] **Lockstep:** the license language matches the corpus and the `sector_benchmark` add-on byte-for-byte — if you changed it anywhere, change all three (Mode C, the add-on, `infra-reference-set.md`)
- [ ] `captured_at` is today; `curator` is named
- [ ] Not a duplicate of an existing entry in the corpus (check the coverage ledger)
- [ ] No HeyHi banned words; no "AI" as a standalone word
- [ ] Em dashes: none in the single-line annotation fields (`what_to_take`, `why`, `anti_pattern`, `pattern_ref`) — use colons or semicolons, consistent with the Mode A single-line-field rule (`v-next-edits` §6). The corpus file is internal agent-readable, so prose outside the entry blocks follows the internal-doc exemption.

### Step C6: Output + propagate

1. Paste the entry into `ai-services/design-intelligence/infra-reference-set.md` under the correct territory section.
2. **Propagate in the same change** (mirrors Mode A's Step 10 propagation discipline): update the **Coverage ledger** table (the territory's entry count and, if this closes one, its Phase 3 gap note); and the entry-count line beneath it. If the entry fills a territory that was cross-ref-only (e.g. geospatial-ops had 0 dedicated entries at seed), promote it from cross-ref to a real count.
3. If the entry grounds a Cluster D style entry, you may also populate that entry's `reference_examples` slot in `style-reference-library.md` (Cluster D 13/15/16) — this is the Phase-1.5 deferred work; do it only when curating against a live engagement, not speculatively.
4. Verify the insert mechanically: grep the corpus for the new `source` name (one hit), and confirm the coverage-ledger count matches the actual entry count for that territory.

### Recency + the downstream license discipline

- **Recency.** `captured_at` is not decoration. Infra UIs change; a stale infra reference is worse than none. Design System Care spot-verifies reachability and refreshes annotations each cycle. Build the refresh in from the first entry.
- **Audit use (forward note — Phase 4, gated).** If an entry is later cited in a Design Intelligence Audit `sector_benchmark`, the citation-only discipline still governs: the deliverable **describes and links**, it never embeds the screen. That is what makes the benchmark billable where a Mobbin-sourced one was blocked by third-party copyright. This is a discipline that travels with the entry, not an instruction to build the Audit integration now — that is Phase 4 and gated on a live engagement.

**Earn the Room:** reference entries are retrieved by intent (territory / pattern) at design time, never pre-loaded into a build. The corpus informs reasoning at the boundary; it is not generation-runtime context.

---

## Exit Gate Required Headers (bottom-of-skill bracket)

This skill closes through the Exit Gate Flavor A (`CLAUDE-SESSION-RULES.md § Exit Gate`). Before declaring done, confirm every required header below contains real content, not a claim:

- `## Fixes Applied`
- `## Smoke Test`
- `## Next Session Prompt`

If any header is empty or contains advisory prose ("I checked for bugs") instead of a concrete artifact, the gate has not been satisfied. Apply fixes until clean — then emit.

---

*HeyHi Internal Use Only. Style Reference Library procedural skill. Bay Design LLC. March 2026. Phase 2 (Taste Profile) and Mode C (Infra Reference Set Curator) deployed; Mode C promoted 2026-06-17 from the Infra Reference Set thread Phase 2 (corpus at infra-reference-set.md).*
*Source material: style-descriptor-vocabulary.md · style-reference-library.md · anti-descriptor-method.md · layer-0-execution-plan.md § Session B · infra-reference-set.md · plan-infra-reference-set-2026-06-17.md*
