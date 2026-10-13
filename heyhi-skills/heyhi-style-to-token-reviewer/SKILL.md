---
name: heyhi-style-to-token-reviewer
description: >-
  Validates whether a completed token set matches its claimed style cluster. Runs the 9 warning signs from the style-to-token translation protocol plus two grafted checks (Check 9 accent saturation and count ceiling, Check 10 typography intent) against an active-brand.json config and returns a structured PASS / FAIL / PARTIAL per check with specific evidence and correction instructions. Answers the question: does this token set actually produce the visual system it claimed to target? Use after design-system-onboard completes a config and before design-system-review runs visual fidelity checks. Triggers: "does this token set match the style," "validate this config against the cluster," "run the warning signs on this," "does the token set hold together," "is this coherent," "token set review," "check this config before we build," "does this honor the style," "validate the token decisions." Not for: visual fidelity review against rendered output (use design-system-review), full-pipeline regression testing across all Layer 0 stages (use heyhi-pipeline-validator, which delegates its Stage 4 back to this skill), style entry validation before writing to the library (use heyhi-style-entry-author Mode B), or auditing an inherited token system with no claimed style (use heyhi-token-audit when built).
---

# Style-to-Token Reviewer

Structural validation that a completed token set honors the style cluster it was built from. Runs between `design-system-onboard` (which produces the config) and `design-system-review` (which validates visual fidelity against generated output).

---

> **Exit Gate (Flavor A).** This skill closes through the canonical Exit Gate — see `CLAUDE-SESSION-RULES.md § Exit Gate`. Required headers, in order: `## Fixes Applied`, `## Smoke Test`, `## Next Session Prompt`. Empty headers are visible failures.


## Pipeline Position

```
design-system-onboard → [heyhi-style-to-token-reviewer] → design-system-review
     Produces config               This skill                 Validates visual output
```

This skill answers a different question than `design-system-review`. The review skill asks: *does the rendered output look right?* This skill asks: *are the token values themselves coherent with the style they claim?* A config can produce plausible-looking output while still containing structural errors that will degrade at scale — wrong temperature on secondary tokens, a grey-default trap, a density drift that doesn't show up in a single component but breaks a full page.

Run this before generation, not after.

---

## What You Need Before Starting

**Required:**

1. A completed or near-complete `active-brand.json` config (produced by `design-system-onboard` Modes A–D). The config does not need to be a v1 promotion — a Mode D provisional config is valid input.
2. The claimed style: either a named style from `style-reference-library.md` (e.g., "Warm Technical") or a cluster designation (A, B, C, D, or E) with brief descriptor notes.

**Reference files to load:**

- `ai-services/design-intelligence/style-to-token-translation.md` — **Always load.** Parts 5 (cluster priors) and 6 (9 warning signs) are required for every review. Part 1–4 may be needed for correction guidance on complex findings.
- `ai-services/design-intelligence/style-reference-library.md` — Load when the claimed style is a named entry (not just a cluster). The `token_implications` fields per entry provide the specific priors for that style within its cluster.
- `ai-services/design-intelligence/visual-anti-tells.md` — Load for Checks 9 and 10. Carries the saturation/count ceilings (AT-3, "The ceilings") and the provenance for the Typography Intent Rule that replaced the source skill's serif ban.

Do not load `moodboard-to-brand-json.md` or `designer-review-protocol.md` for this skill. Those govern extraction and visual fidelity respectively. This skill governs token-level structural coherence.

---

## Step 0: Identify the Claimed Style and Cluster

Before running any checks, establish what this config claims to be.

**Extract from the config:**

1. Read `meta.style_notes` — this field should contain the claimed style name or cluster designation. If it references a hybrid (e.g., "Hybrid B/C: C-cluster editorial type on B-cluster spatial foundation"), note the dominant and modifying clusters separately.
2. Read `brand.temperature` — this is the declared temperature register. It must be consistent with the claimed cluster.
3. Read `meta.generated_by` — a Mode D config (`"mode-d"`) is a provisional translation from a moodboard. A `"mode-d-v1"` config has passed designer review. Both are valid inputs; note the generation mode in the review report.

**If the claimed style is a named entry:** Load the matching entry from `style-reference-library.md`. Pull the `token_implications` block — these are the specific priors for that style, one level more specific than the cluster prior tables.

**If only a cluster is known:** Pull the cluster prior table from Part 5 of `style-to-token-translation.md`.

**Build a quick prior reference table** before running checks. This is the baseline each check will compare against.

| Token category | Claimed style prior | Source |
|----------------|--------------------|----|
| Color temperature | [warm / cool / neutral] | meta.style_notes + Part 5 |
| Spacing density | [spacious / balanced / dense] | token_implications or Part 5 |
| Border radius | [sharp / slight / rounded / pill] | token_implications or Part 5 |
| Shadow depth | [flat / subtle / material] | token_implications or Part 5 |
| Type scale ratio | [e.g., Major Third 1.25x] | token_implications or Part 5 |
| Type personality | [humanist / geometric / etc.] | token_implications or Part 5 |
| Motion personality | [minimal / purposeful / expressive] | token_implications or Part 5 |

---

## Step 1: Extract Key Token Values

Pull these values from the config before running the 11 checks (9 warning signs plus Checks 9 and 10, the grafted ceiling and typography-intent checks). Having them in front of you prevents re-reading the config mid-check.

**Color layer:**
- `tokens.color.backgrounds.primary` — background hex
- `tokens.color.backgrounds.secondary` — surface secondary hex
- `tokens.color.text.primary` — primary text hex
- `tokens.color.text.secondary` — secondary text hex (grey-default trap check target)
- `tokens.color.accent.primary` — primary brand accent hex
- `tokens.color.action.primary` — CTA / interactive element color
- `tokens.color.border.default` — default border hex
- `tokens.color.feedback.success`, `.warning`, `.error` — semantic color hexes

**Typography layer:**
- `tokens.typography.families.display.family` — display/heading typeface
- `tokens.typography.families.body.family` — body typeface
- `tokens.typography.scale.ratio` — the scale ratio name or value
- `tokens.typography.weights.heading` — heading weight
- `tokens.typography.weights.body` — body weight

**Spacing layer:**
- `tokens.spacing.base` — base spacing unit (px)
- `tokens.spacing.density` — if present, the declared density
- `tokens.spacing.section` (or equivalent tier names) — section-level spacing values

**Shape layer:**
- `tokens.radius.sm`, `.md`, `.lg` — border radius values
- `tokens.elevation.sm`, `.md` — shadow values

**Meta:**
- `meta.style_notes` — hybrid documentation, deviations from cluster prior
- `brand.temperature` — declared temperature

---

## Step 2: Run the Checks (9 Warning Signs + 2 Grafted)

Run each check independently. Record a result and evidence before moving to the next.

Results are: **PASS** / **FAIL** / **PARTIAL** (partial = the check reveals a concern that is not a definitive failure but requires attention).

---

### Check 1: The Contrast Problem

**What this catches:** A token set where foundational values (background, typography, spacing) belong to one cluster while the interactive layer (action colors, semantic colors, focus/hover states) belongs to a different one. The user does not experience this as "mostly X with a Y accent." They experience it as inconsistent.

**What to examine:**
- `brand.temperature` vs. `tokens.color.action.primary` — does the action color match the temperature register? (A warm-declared config with a cool blue CTA is the canonical failure.)
- `tokens.color.feedback.success/warning/error` — are semantic hues calibrated to the cluster's temperature? (Reference: Part 1.3, semantic role mapping by cluster)
- Cross-check action color against the cluster's expected action-primary behavior from Part 1.3.

**PASS criteria:** Action color and semantic colors are in the same temperature register as the foundational palette. No interactive token reads as imported from a different cluster without documentation.

**FAIL criteria:** Cool interactive layer on a warm foundational palette (or reverse), with no hybrid documentation in `meta.style_notes`.

**PARTIAL criteria:** Action color is slightly mismatched but semantic colors are correct, or the deviation is minor enough to be a stylistic choice rather than a structural error. Flag for confirmation.

---

### Check 2: The Performed Translation

**What this catches:** Token values chosen to look like the style family rather than function like it. The most common manifestation: a "warm" background that measures as neutral or cool, or a "spacious" layout with a base unit that cannot produce spacious section padding at standard multipliers.

**What to examine:**

**Color performance:**
- Measure `tokens.color.backgrounds.primary` against the warmth test:
  - True warm off-white: hex in the range `#FAF7F2`–`#F5EFE4` (has a warm yellow-red hue shift)
  - Neutral: `#F8F8F6`–`#FAFAFA` (no meaningful hue shift)
  - Cool: `#F8F9FA`–`#F0F1F2` (slight blue shift)
  - Claimed warm + neutral-measuring background = performed translation
- Check `tokens.color.text.secondary`: does it match the palette's temperature register? (A warm config with `#6B7280` text-secondary is neutral-leaning, not warm.)

**Spacing performance:**
- If claimed density is "spacious" (Cluster B, E), verify that `tokens.spacing.base` × reasonable multipliers can produce section-level padding of 64px+.
  - Base 4px: standard spacious section = 4 × 16 = 64px. Valid.
  - Base 8px: standard spacious section = 8 × 8 = 64px. Valid.
  - If base is set to 4px but no multiplier reaches 16+, the spaciousness is unearned.

**Typography performance:**
- If claimed style is editorial or expressive (Cluster C, some B), check that heading weight creates actual visual emphasis over body.
  - Display 900 weight + body 400 weight = genuine emphasis. Valid.
  - Display 500 weight + body 400 weight = one-step weight map. Editorial claim is performed.

**PASS criteria:** Key token values measure correctly against their claimed character.

**FAIL criteria:** One or more values claim a quality (warm, spacious, editorial) that contradicts their actual measured value.

---

### Check 3: Density Drift

**What this catches:** Spacing and typography working against each other, producing incoherence through mismatched density signals.

**The rule from Part 6.3:** Tight type scale pairs with dense spatial density. Dramatic type scale pairs with spacious layout. Mixed-density systems require explicit documentation of which zones follow which rules.

**What to examine:**
- Map `tokens.typography.scale.ratio` to a density category:
  - Major Second (1.125x) = tight scale (dense-appropriate)
  - Major Third (1.25x) = moderate scale (balanced-appropriate)
  - Perfect Fourth (1.333x) = expansive scale (spacious-appropriate)
  - Augmented Fourth (1.414x) = dramatic scale (spacious-required)
- Map `tokens.spacing.density` (or infer from base unit and section values) to a density category: dense / balanced / spacious.
- Compare: are type scale and spatial density in the same density family, or are they pulling in opposite directions?

**Common failure pairs:**
- Augmented Fourth scale + dense spacing: display headings overwhelm data tables
- Major Second scale + spacious spacing: tiny type hierarchy in vast white space

**PASS criteria:** Type scale ratio and spacing density are in the same density family, or a hybrid is explicitly documented in `meta.style_notes` with zone-level rules.

**FAIL criteria:** Type scale and spacing density are in opposing density families with no documentation.

---

### Check 4: Scale Inversion

**What this catches:** The type scale ratio implies one level of visual authority; the weight map implies another. They contradict each other.

**What to examine:**
- Map `tokens.typography.scale.ratio` to its authority level:
  - Major Second / Minor Third = understated, data-appropriate
  - Major Third = balanced, professional
  - Perfect Fourth / Augmented Fourth = expressive, editorial authority
- Map `tokens.typography.weights.heading` to its emphasis level:
  - 400–500 = restrained
  - 600–700 = standard emphasis
  - 800–900 = heavy/aggressive emphasis

**Check the pairing:**
- Augmented Fourth scale + 900 weight: both are aggressive. Coherent, but only valid in Cluster C. Verify the cluster claim matches.
- Major Second scale + 900 weight: understated scale + aggressive weight. The heading looks important but the size difference says otherwise. This is inversion.
- Augmented Fourth scale + 400 weight: dramatic size differences + light weight. Headings arrive at scale but without presence. Inversion in the opposite direction.

**PASS criteria:** Scale ratio and heading weight belong to the same cluster's authority register, or an intentional tension is documented in `meta.style_notes` (Studio Craft uses this deliberately).

**FAIL criteria:** Scale and weight are from different cluster registers with no documentation of intent.

---

### Check 5: The Grey-Default Trap

**What this catches:** `tokens.color.text.secondary`, `tokens.color.backgrounds.secondary`, and `tokens.color.border.default` defaulting to neutral grey regardless of the palette's temperature register. These supporting tokens are the most frequently left at CSS-reset defaults. The result: a primary brand layer that reads with character, and a supporting token layer that reads neutral-cold.

**What to examine:**

For each of these three token values, classify the temperature:
- Warm grey: hue angle approximately 20–40° (yellow-orange undertone). Example: `#78716C`, `#8A7A6A`.
- Cool grey: hue angle approximately 200–230° (blue undertone). Example: `#6B7280`, `#94A3B8`.
- Neutral grey: hue angle 0° or near-zero saturation. Example: `#9CA3AF`, `#D1D5DB`.

**Cross-check against `brand.temperature`:**
- Warm declared temperature: all three supporting tokens should be warm-grey or warm-tinted.
- Cool declared temperature: cool-grey or blue-grey supporting tokens are correct.
- Neutral declared temperature: true neutral greys are acceptable; slight warm or cool lean is acceptable if consistent.

**PASS criteria:** Supporting token temperature matches the declared palette temperature.

**FAIL criteria:** Warm palette with neutral-to-cool supporting tokens (or cool palette with warm supporting tokens). This is the most common single failure in configs translated from warm or cool moodboards.

**Correction shortcut:** For warm palettes — shift `text-secondary`, `surface-secondary`, and `border-default` toward the warm-grey range. Use `#78716C` (warm mid-grey) as a reference point rather than `#6B7280` (neutral mid-grey). For cool palettes, the inverse: `#6B7280` or `#94A3B8` are appropriate; `#78716C` reads inconsistently warm.

---

### Check 6: The Semantic Orphan

**What this catches:** Semantic colors (success, warning, error, info) that are correct in hue category but feel imported from a different design system because their saturation or lightness is mismatched to the palette's saturation register.

**The rule from Part 6.6:** Semantic colors should be within ±15% saturation of the palette's primary accent, unless high-contrast semantics are intentionally required (Cluster D in operations contexts — document this if so).

**What to examine:**
- Measure the saturation value of `tokens.color.accent.primary`.
- Measure the saturation value of each semantic color: `tokens.color.feedback.success`, `.warning`, `.error`.
- Calculate the saturation difference.
- Flag any semantic color that exceeds ±15% saturation from the primary accent without documentation.

**Quick heuristic (when exact measurement isn't available):**
- Bright, fully saturated Tailwind-default greens (`#22c55e`) and reds (`#ef4444`) read as orphaned in any palette with saturation below 50% on the primary accent. These are the two most common imported defaults.
- Earth-tone palettes, muted palettes, and any Cluster E or Cluster B config are especially vulnerable.

**PASS criteria:** Semantic colors are within ±15% saturation of the primary accent, or intentional high-contrast departures are documented in `brand.style_notes` or `meta.style_notes`. Either location satisfies this criterion — the test is whether the departure is documented and intentional, not which field holds the documentation. ISA-101 industrial/SCADA contexts are an established exception class: mandatory high-contrast chromatic signals against an achromatic foundation are sector-required, not errors.

**FAIL criteria:** Semantic colors are clearly from a different saturation register than the palette they live in, with no documentation in either brand.style_notes or meta.style_notes.

**Provenance shortcut (2026-06-10):** When `meta.field_provenance` marks `tokens.color` with `source: palette_gen`, the semantic colors were generated harmonized to the palette chroma and accessible by construction (see `heyhi-skills/ui-studio/references/color-generation.md`). For such configs Check 6 is confirmation, not repair — verify the provenance, spot-check one semantic against the primary accent, and PASS unless the provenance is absent or stale.

---

### Check 6b: Brand-Utility Collision (WS9)

**What this catches:** Semantic colors that are too *close* to brand accent colors — the inverse failure mode of Check 6. When a CTA button and a form error are the same red, or a warm decorative accent and a caution signal are the same orange, users cannot distinguish invitation from warning. Check 6 catches orphaned semantics (too far from the palette). Check 6b catches colliding semantics (too close to brand accents).

**The rule (added 2026-04-05, derived from Phase C semantic color specimen):** For each brand accent, compute hue distance and lightness distance to each semantic utility color. Flag a collision if any pair is within 15 degrees hue AND 15% lightness simultaneously.

**What to examine:**
- For each accent color (`tokens.color.accent.primary`, `.secondary`, `.tertiary`), compute HSL hue and lightness.
- For each semantic color (`tokens.color.feedback.error`, `.warning`, `.success`, `.info`), compute HSL hue and lightness.
- Compare every accent-semantic pair. If hue distance < 15° AND lightness distance < 15%, flag.
- Common collisions: bright red accents vs. error, orange/copper accents vs. warning, sky-blue accents vs. info.

**Correction protocol (three levers):**
1. **Deeper value** — shift the semantic color darker than the brand accent.
2. **Reduced energy** — lower saturation or lightness so the semantic reads as system furniture, not brand expression.
3. **Hue shift** — nudge the semantic color's hue away from the accent (e.g., shift warning from orange toward gold, shift info from sky-blue toward indigo).

**PASS criteria:** No brand accent is within 15° hue AND 15% lightness of any semantic color, OR intentional collisions are documented in `meta.style_notes` with a rationale (rare — most collisions are unintentional).

**FAIL criteria:** One or more brand accents are perceptually indistinguishable from a semantic utility color at UI scale (alerts, badges, buttons), with no documentation.

**Reference:** `brand/phase-c-semantic-color.html` — the instance's own specimen that resolved an accent/error and an accent/warning collision.

---

### Check 7: The Incoherent Hybrid

**What this catches:** Token decisions that combine signals from two different clusters without a documented hybrid strategy. The result tends toward neither cluster: not distinctive enough to read as the bold cluster, not warm enough to read as the human cluster.

**What to examine:**
- Does `meta.style_notes` reference a hybrid? If yes: confirm a dominant cluster and modifying cluster are named, and that foundational decisions (temperature, scale, shadow) follow the dominant cluster's prior while the modifying cluster only appears in specific named dimensions.
- If no hybrid is documented: check whether any token decision contradicts the claimed cluster prior in a way that suggests accidental cluster crossing.

**Hybrid detection heuristic (when not documented):**
- If `border_radius` prior is "sharp" (Cluster C) but the config has rounded corners (8–12px, Cluster B) with no note — potential undocumented hybrid.
- If `shadow_depth` prior is "flat" (Cluster C) but the config has material shadows — potential undocumented hybrid.
- If `color_temperature` prior is "warm" (Cluster B) but `brand.temperature` is "cool" — potential cluster misidentification.

**PASS criteria:** No hybrid present and all token decisions align with the claimed cluster, OR a hybrid is present with explicit dominant/modifying cluster documentation.

**FAIL criteria:** Contradictions between token decisions and the claimed cluster prior are present with no documentation.

**PARTIAL criteria:** Minor deviations from the cluster prior that may be intentional stylistic choices. Flag for confirmation — ask whether the deviation is intentional before calling it a failure.

---

### Check 8: Scale-Density Incoherence

**What this catches:** A type scale ratio and spacing density that produce ambiguous visual hierarchy because they sit at opposing ends of the density spectrum. Specifically: a Minor Third (1.2x) scale paired with balanced or dense spacing, where the tight heading steps may fall within 3–4px of each other in effective rendered height once line-height is factored in.

**What to examine:**

- Map `tokens.typography.scale.ratio` — flag if it is Minor Third (1.2x) or Major Second (1.125x).
- Map `tokens.spacing.density` — if `"balanced"` or `"dense"`, cross-check against the scale ratio.
- Calculate or estimate the effective rendered size difference between heading levels at the declared base size (e.g., 16px base × 1.2x = 16 → 19.2 → 23 → 27.6px across four heading steps).
- With dense or balanced layout, these 3–4px differences become ambiguous at display sizes: viewers may not clearly distinguish H3 from body at a glance.

**Reference:** Part 6.8 of `style-to-token-translation.md`.

**Resolution options (if flagged):**

1. Increase scale ratio to Perfect Fourth (1.333x) for more visual separation between heading levels.
2. Accept Minor Third + **spacious** density — this is the Studio Craft pattern, where breathing room substitutes for dramatic size jumps. Only valid when spacing density is spacious, not balanced or dense.
3. Compensate with weight contrast: heading at Bold/700 or Heavy/800, body at Regular/400. Size steps are close, but weight difference produces hierarchy.

**PASS criteria:** Minor Third scale is paired with spacious spacing density, or a heavier heading weight (700+) compensates for tight size steps. Alternatively, scale is Major Third (1.25x) or wider — no incoherence risk.

**FAIL criteria:** Minor Third scale paired with balanced or dense spacing and no weight compensation — heading hierarchy will be ambiguous at rendered size.

**PARTIAL criteria:** Minor Third scale paired with balanced spacing where heading weight is 600 (semi-bold). Some compensation present but marginal. Flag for designer confirmation: "Is the tight heading hierarchy intentional for a data-dense context?"

---

### Grafted Checks (taste-design, 2026-06-02)

Checks 9 and 10 are grafted from the visual anti-tell catalog (`ai-services/design-intelligence/visual-anti-tells.md`), not Part 6 of the translation protocol. They run in the same pass as the 9 warning signs and report on the same PASS / FAIL / PARTIAL scale. Their numbering is plain (9, 10), not `6.x`, precisely because they do not derive from Part 6.

### Check 9: Accent Saturation & Count Ceiling

**What this catches:** Accent colors that exceed the saturation ceiling, and configs declaring more than one *primary* accent. Oversaturated accents are the single most common generated-design tell; multiple primaries signal a palette that never made a choice. This check is a graft from the visual anti-tell catalog (`visual-anti-tells.md` — "The ceilings" and AT-3), not a Part 6 warning sign.

**What to examine:**
- For each accent in `tokens.color.accent.*` (primary, secondary, tertiary), compute HSL saturation.
- Flag any accent at **≥ 80% saturation** *unless* it is documented as an intentional electric brand color **with a passing WCAG result.** The documentation can live in `meta.field_provenance.<path>`, `meta.color_strategy`, `brand.style_notes`, or `meta.implementation_notes`; the passing contrast evidence in `tokens.color.contrast_notes` or the provenance `notes`/`usage_notes`. Both halves are required — intent *and* a passing contrast result.
- Count primary accents. Exactly one accent may be designated primary. Supporting / secondary / tertiary accents are not primaries. Flag if more than one accent is named primary.

**The carve-out, worked (verify the check is correctly scoped):** a config declares one primary (an electric red at ~100% saturation) and two supporting accents (a deep blue-violet at ~99% saturation, a warm olive at ~18%). *Both* the red and the blue-violet exceed the 80% ceiling, and *both* are carve-out cases: each is documented in `meta.field_provenance` and `meta.color_strategy` as a deliberate electric decision, and each carries a passing WCAG result (the red AA at display scale, the blue-violet AAA at any size). The ceiling is per-accent and the carve-out is per-accent — a check that flags either accent on this config is mis-scoped. One-primary ceiling: the red is the sole primary, the blue-violet and olive are supporting. PASS.

**PASS criteria:** Every accent is below 80% saturation, OR each ≥ 80% accent is documented as an intentional electric color with a passing WCAG result; AND exactly one primary accent is declared.

**FAIL criteria:** An accent at ≥ 80% saturation with no intentional-electric documentation or no passing-contrast evidence; OR more than one accent designated primary.

**PARTIAL criteria:** An accent at ≥ 80% saturation documented as intentional but with no recorded WCAG result (intent present, contrast evidence missing). Flag for confirmation rather than failing outright.

---

### Check 10: Typography Intent

**What this catches:** Type choices that are unconsidered defaults rather than deliberate, context-matched decisions. This check **replaces the source skill's blanket serif ban** (see `visual-anti-tells.md` provenance note and the graft plan §2). The tell being caught is *unconsidered* type, never serif as such. A deliberately chosen, reading-tuned serif is the opposite of a tell.

**The rule (Typography Intent Rule):** Type choices must be deliberate and context-matched, never a fallback default.
- **Long-form / editorial / sustained-reading surfaces:** serif body copy is *encouraged* when set for reading — body size ≥ 1rem, generous leading (~1.5–1.7), measure ≤ ~75ch, and a reading-optimized face (Lora, Fraunces, Source Serif, and the like), not a lazy system serif dropped in as a fallback.
- **High-density / dashboard / data-table / UI-chrome surfaces:** serif body is discouraged at small sizes where legibility-per-pixel dominates; reserve serif for display, use mono for dense numerics.
- **The actual tell being banned:** *unconsidered* type — a default system stack (`Inter`-by-default, `Times`/`Georgia` as an unstyled fallback) shipped because no choice was made.

**What to examine:**
- Read `tokens.typography.families.display.family`, `.body.family`, `.utility.family`, and any `body.body_register` (ADR-004).
- Determine the reading context from `layout.spacing_density`, `brand.cluster`, `brand.style_entry`, and `layout.preferred_patterns`: editorial / long-form, or high-density / dashboard?
- If a serif body is set on an editorial / long-form surface, confirm it is a reading-optimized face and the body scale is ≥ 1rem with generous leading. **PASS — encouraged.**
- If a serif body is set on a high-density / dashboard surface at small sizes with no documented intent (`body_register` or provenance), flag **PARTIAL** (legibility-per-pixel concern), not FAIL.
- Look for evidence of an *unconsidered default stack*: a bare system fallback as the primary body, or a known default face (`Inter`, `Times`, `Georgia`) used as primary body with no provenance or decision record. That is the FAIL condition.

**The carve-out, worked:** a config runs a reading-optimized serif (e.g. Lora) as body, a geometric sans as display, and a mono as utility, on an editorial cluster (e.g. Cluster E / Studio Craft) whose editorial `preferred_patterns` make it a long-form reading context. The serif is documented in `meta.field_provenance.tokens.typography.families.body.family` and `meta.scale_reasoning` (a deliberate "editorial inversion"). Body scale is `clamp(1rem, 1.3vw, 1.125rem)` — ≥ 1rem. PASS — a deliberately chosen, reading-tuned serif body. Any check that flags that serif body is mis-scoped.

**PASS criteria:** Type roles are deliberate and reading-context-matched. Serif body on an editorial surface with reading-tuned settings passes. Family choices carry provenance or documented intent.

**FAIL criteria:** Evidence of a default / unconsidered stack — a bare system fallback as primary body, or a known default face used as primary body with no provenance or decision record. **Never FAIL on serif body alone**, and never FAIL on a dashboard serif (that case is PARTIAL, below).

**PARTIAL criteria:** Serif body on a high-density / dashboard surface at small sizes with no documented reading-context justification. Flag for confirmation rather than failing.

---

## Step 3: Produce the Review Report

After all 11 checks are complete, produce a structured report.

```markdown
## Style-to-Token Review — [Config Name / Client Name]
Date: [date]
Claimed style: [Style Name or Cluster A/B/C/D/E]
Config: [file path or "provided conversationally"]
Generation mode: [mode-d provisional / mode-d-v1 / mode-a / mode-b / mode-c]

---

### Cluster Prior Summary

| Token category | Expected (prior) | Config value | Match |
|----------------|-----------------|--------------|-------|
| Color temperature | [prior] | [config value] | Yes / No |
| Spacing density | [prior] | [config value] | Yes / No |
| Border radius | [prior] | [config value] | Yes / No |
| Shadow depth | [prior] | [config value] | Yes / No |
| Type scale ratio | [prior] | [config value] | Yes / No |
| Type personality | [prior] | [config value] | Yes / No |
| Motion personality | [prior] | [config value] | Yes / No |

---

### Check Results

Rows 6.1–6.8 (with 6.6b) are the Part 6 warning signs; rows 9 and 10 are the grafted checks.

| # | Check | Result | Summary |
|---|-------------|--------|---------|
| 6.1 | Contrast Problem | PASS / FAIL / PARTIAL | [one sentence] |
| 6.2 | Performed Translation | PASS / FAIL / PARTIAL | [one sentence] |
| 6.3 | Density Drift | PASS / FAIL / PARTIAL | [one sentence] |
| 6.4 | Scale Inversion | PASS / FAIL / PARTIAL | [one sentence] |
| 6.5 | Grey-Default Trap | PASS / FAIL / PARTIAL | [one sentence] |
| 6.6 | Semantic Orphan | PASS / FAIL / PARTIAL | [one sentence] |
| 6.6b | Brand-Utility Collision | PASS / FAIL / PARTIAL | [one sentence] |
| 6.7 | Incoherent Hybrid | PASS / FAIL / PARTIAL | [one sentence] |
| 6.8 | Scale-Density Incoherence | PASS / FAIL / PARTIAL | [one sentence] |
| 9 | Accent Saturation & Count Ceiling | PASS / FAIL / PARTIAL | [one sentence] |
| 10 | Typography Intent | PASS / FAIL / PARTIAL | [one sentence] |

---

### Detailed Findings

#### 6.1 Contrast Problem — [PASS / FAIL / PARTIAL]

[Specific token paths and values examined. What you found. Why it passes or fails.]
[If FAIL: correction instruction referencing Part 6.1 of style-to-token-translation.md]

#### 6.2 Performed Translation — [PASS / FAIL / PARTIAL]

[...]

#### 6.3 Density Drift — [PASS / FAIL / PARTIAL]

[...]

#### 6.4 Scale Inversion — [PASS / FAIL / PARTIAL]

[...]

#### 6.5 Grey-Default Trap — [PASS / FAIL / PARTIAL]

[...]

#### 6.6 Semantic Orphan — [PASS / FAIL / PARTIAL]

[...]

#### 6.6b Brand-Utility Collision — [PASS / FAIL / PARTIAL]

[For each accent-semantic pair: hue distance computed, lightness distance computed. Whether any pair falls within 15° hue AND 15% lightness simultaneously. If FAIL: which correction lever is recommended — deeper value, reduced energy, or hue shift.]

#### 6.7 Incoherent Hybrid — [PASS / FAIL / PARTIAL]

[...]

#### 6.8 Scale-Density Incoherence — [PASS / FAIL / PARTIAL]

[Scale ratio mapped. Spacing density mapped. Whether tight scale steps are compensated by spacing or weight. If FAIL: which resolution option is recommended — increase ratio, accept with spacious density only, or add weight contrast.]

---

#### Check 9 Accent Saturation & Count Ceiling — [PASS / FAIL / PARTIAL]

[Per accent: HSL saturation computed. For any accent ≥ 80%, whether intentional-electric documentation AND a passing WCAG result are both present. Count of primary accents. If FAIL: which accent and which half of the carve-out is missing, or which extra primary to demote. Reference `visual-anti-tells.md` AT-3 / "The ceilings".]

#### Check 10 Typography Intent — [PASS / FAIL / PARTIAL]

[Reading context determined (editorial vs. high-density). Family roles and provenance examined. Whether any family is an unconsidered default stack. If FAIL: which family is the default and what documentation or deliberate choice is missing. Never fails on serif body alone. Reference the Typography Intent Rule.]

### Overall Verdict

[PASS / CONDITIONAL PASS / FAIL]

- PASS: 0 FAILs. Proceed to design-system-review.
- CONDITIONAL PASS: 1 FAIL or 2+ PARTIALs. Corrections listed below; review may proceed in parallel.
- FAIL: 2+ FAILs. Corrections must be made before visual generation produces reliable output.

*Note on CONSIDERED_DEPARTURE: When this skill is run as Stage 4 of `heyhi-pipeline-validator` and the style entry has a `taste_profile`, PARTIAL results may be resolvable as `CONSIDERED_DEPARTURE` via the taste review path — meaning a CONDITIONAL PASS from this skill may yield a Stage 4 PASS at the pipeline level once taste review is complete. See `heyhi-pipeline-validator/SKILL.md` Stage 4 for the three criteria and documentation requirements. For configs without a taste_profile, all PARTIALs fire at full weight and this note does not apply.*

### Priority Corrections
[Only present if Verdict is Conditional Pass or Fail. Ordered by impact.]

1. [Most structurally important correction — affects rendering most broadly]
2. [...]

### Recommended Next Step
[PASS / Conditional Pass:] Proceed to `design-system-review`. Present this report alongside the generated output.
[FAIL:] Address priority corrections in the config, then re-run this skill before proceeding.
```

---

## HUMAN GATE: Review Confirmation

After delivering the report, present the verdict to the human reviewer before proceeding:

```
Style-to-Token Review: [Style Name] — [PASS / CONDITIONAL PASS / FAIL]

Checks passed: N/11
Checks with findings: [list check names, if any]

[If any FAIL or PARTIAL:] Priority corrections are listed in the report above.

Confirm to proceed to design-system-review, or return to the config for corrections first?
```

Wait for the human reviewer's explicit confirmation before declaring the config ready for visual generation.

---

## Reference Files

Load when relevant, not by default:

- `ai-services/design-intelligence/style-to-token-translation.md` — Parts 5 and 6 are required for every review. Parts 1–4 provide correction depth when a FAIL requires explanation beyond the summary.
- `ai-services/design-intelligence/style-reference-library.md` — Load when the claimed style is a named entry. The `token_implications` block is the style-specific prior.
- `ai-services/design-intelligence/visual-anti-tells.md` — Required for Checks 9 and 10. Saturation/count ceilings and the Typography Intent Rule, each with a worked carve-out (documented electric accents; a deliberate reading serif body).
- `heyhi-skills/design-system-onboard/SKILL.md` — Reference if the config requires corrections and you need to understand what Mode produced it.
- `heyhi-skills/design-system-review/SKILL.md` — The next step after this skill passes. Mode A (v0 → v1 visual fidelity review).

---

## Smoke Test Checklist

Before delivering any review output, check:

- [ ] All 11 checks run and documented (9 warning signs + Check 9 saturation/count ceiling + Check 10 typography intent; no checks skipped)
- [ ] Each check result states PASS / FAIL / PARTIAL with specific token path evidence (not just "looks correct")
- [ ] Corrections for any FAIL reference the specific Part 6 section of `style-to-token-translation.md`
- [ ] HUMAN GATE block is present before declaring config ready
- [ ] Cluster Prior Summary table populated from actual config values (not estimated)
- [ ] No standalone "AI" in review output
- [ ] No pricing in review output
- [ ] Em dashes: maximum 2 per client-facing output generated by this skill (the 2-em-dash rule applies to output, not to this procedural SKILL.md document itself)
- [ ] If config is Mode D provisional, that is noted in the report header — a provisional config can pass this review and still have unresolved fields for the designer to confirm
- [ ] No banned words in review output copy (leverage, unlock, seamless, etc.)

---

## Exit Gate Required Headers (bottom-of-skill bracket)

This skill closes through the Exit Gate Flavor A (`CLAUDE-SESSION-RULES.md § Exit Gate`). Before declaring done, confirm every required header below contains real content, not a claim:

- `## Fixes Applied`
- `## Smoke Test`
- `## Next Session Prompt`

If any header is empty or contains advisory prose ("I checked for bugs") instead of a concrete artifact, the gate has not been satisfied. Apply fixes until clean — then emit.

---

*HeyHi Confidential — Skill internal methodology. Not for client distribution.*

*Layer 0 pipeline skill. Sits between design-system-onboard and design-system-review.*

*Bay Design LLC d/b/a HeyHi · Built March 2026 · Updated 2026-04-05 (Check 6b: Brand-Utility Collision added; 8 → 9 warning signs) · Updated 2026-06-02 (taste-design graft: Check 9 Accent Saturation & Count Ceiling + Check 10 Typography Intent added; 9 → 11 checks; references visual-anti-tells.md)*
