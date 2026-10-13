---
name: heyhi-pipeline-validator
description: >-
  Validates a named style entry through the full Layer 0 pipeline and returns a structured pass/fail report per stage. Four pipeline stages: style entry field completeness → style-to-token translation reasoning → Mode D active-brand.json field population → style-to-token-reviewer warning sign checks. Turns a one-time smoke test into a repeatable regression check before any client engagement or skill update. Includes a 68-point Component Layer test scaffold derived from Entry 10 (Neo-Industrial, 37 checks) and Entry 16 (Civic Modern, 31 checks) — the library's two most demanding cluster-level validation cases. Three modes: Mode A (full pipeline run from a style name), Mode B (config validation only — stages 3–4 on an existing active-brand.json), Mode C (regression test against the 68-point reference scaffold). Not for: authoring new style entries (use heyhi-style-entry-author), reviewing visual fidelity of rendered output (use design-system-review), validating one config's token-set coherence on its own (use heyhi-style-to-token-reviewer — Stage 4 here delegates to it), auditing inherited token systems with no claimed style (use heyhi-token-audit when built), or running a monthly care check (use design-system-care-monthly).
---

# Layer 0 Pipeline Validator

Structural validation that the full Layer 0 pipeline — from style entry through active-brand.json — produces coherent, schema-valid, and cluster-accurate output before any client engagement begins.

---

> **Exit Gate (Flavor A).** This skill closes through the canonical Exit Gate — see `CLAUDE-SESSION-RULES.md § Exit Gate`. Required headers, in order: `## Fixes Applied`, `## Smoke Test`, `## Next Session Prompt`. Empty headers are visible failures.


## Pipeline Architecture

```
[Style Library Entry]
        ↓
  Stage 1: Entry Field Completeness
  (schema, vocabulary, token_implications)
        ↓
  Stage 2: Translation Reasoning
  (heyhi-style-selection Mode B output)
        ↓
  ── HUMAN GATE: Direction Lock ──
        ↓
  Stage 3: Mode D Config Population
  (design-system-onboard output — 12 required fields + ADR-007 extensions)
        ↓
  Stage 4: Warning Sign Checks
  (heyhi-style-to-token-reviewer — its full current check set)
        ↓
  ── HUMAN GATE: Promotion Decision ──
        ↓
  [Config declared ready for design-system-review]
```

This skill validates the pipeline — it does not run it. Each stage checks the output of a pipeline skill against documented criteria. A failing stage is a repair signal, not a blocker: document the finding, fix it in the source skill or config, and rerun the stage.

---

## What You Need Before Starting

**Required for Mode A (Full Pipeline):**
1. A named style entry from `ai-services/design-intelligence/style-reference-library.md`
2. A completed `active-brand.json` config (produced by `design-system-onboard` Mode D) — or run Mode D first
3. The style pre-classification (Mode B output from `heyhi-style-selection`) if available

**Required for Mode B (Config Validation Only):**
1. A completed or near-complete `active-brand.json` config
2. The claimed style name or cluster designation

**Required for Mode C (Regression Test):**
1. Both reference configs:
   - `ai-services/design-intelligence/test-fixtures/neo-industrial-active-brand.json` (Entry 10 — 37 checks)
   - `ai-services/design-intelligence/test-fixtures/civic-modern-v0.2.0-active-brand.json` (Entry 16 — 31 checks; v0.2.1 internally)
2. No other input needed — the 68-point scaffold is self-contained

**Reference files to load:**
- `ai-services/design-intelligence/style-reference-library.md` — required for Stages 1 and 2
- `ai-services/design-intelligence/style-to-token-translation.md` — Parts 5 and 6 required for Stage 4
- `heyhi-skills/heyhi-style-to-token-reviewer/SKILL.md` — Stage 4 procedure

Do not load `moodboard-to-brand-json.md` unless Stage 3 needs correction depth. Load `heyhi-skills/heyhi-style-entry-author/SKILL.md` only if Stage 1 finds field violations that need the entry-author repair process.

---

## Mode Selector

| Mode | Input | Stages run | Use when |
|------|-------|-----------|----------|
| **A (Full Pipeline)** | Style name + active-brand.json | 1 → 2 → Gate → 3 → 4 → Gate | New style entry, first engagement, skill update |
| **B (Config Validation)** | active-brand.json + claimed style | 3 → 4 → Gate | Config was onboarded through Mode A/B/C; validate before design-system-review |
| **C (Regression Test)** | None — uses reference configs | All 68 points against Entry 10 + 16 | Pipeline regression after any skill update; pre-release check |

---

## Stage 1: Style Entry Field Completeness

**Purpose:** Confirm the style library entry has all required fields before any downstream pipeline work depends on it. Structural errors here propagate to every stage.

**What to load:** The named entry from `style-reference-library.md`.

**Checks — run each independently:**

| # | Check | Criteria | Result |
|---|-------|----------|--------|
| S1.1 | Required schema fields present | entry_id, name, cluster (A–E), descriptors.mood (array, 3+ terms), descriptors.anti_mood (array, 1+ terms) | PASS / FAIL |
| S1.2 | token_implications complete | All 7 fields present and non-empty: color_temperature, spacing_density, border_radius_range, shadow_depth, type_scale_ratio, type_personality, motion_personality | PASS / FAIL |
| S1.3 | Enum values valid | token_implications fields match valid enum values per heyhi-style-entry-author Mode B schema | PASS / FAIL |
| S1.4 | Industry fit documented | industry_fit.natural array non-empty; avoid array present (even if empty) | PASS / FAIL |
| S1.5 | agent_context_snippet present | Non-empty string; references the entry's most distinctive cluster signal (not just the name) | PASS / FAIL |

**If any check FAILS:** Stop and repair the entry using `heyhi-style-entry-author` Mode B before proceeding. Do not advance to Stage 2 with a failing Stage 1 — translation errors will be untraceable.

**Stage 1 Verdict:** PASS (all 5 checks) / FAIL (any check fails)

---

## Stage 2: Style-to-Token Translation Reasoning

**Purpose:** Confirm the style-to-token pre-classification is valid before Mode D uses it as a token extraction guide. A bad pre-classification produces a config that is internally consistent but cluster-wrong.

**What to load:** The `heyhi-style-selection` Mode B output YAML for this entry (if available). If no Mode B output exists, run `heyhi-style-selection` Mode B against the entry's moodboard description to generate it.

**Checks:**

| # | Check | Criteria | Result |
|---|-------|----------|--------|
| S2.1 | matched_style field | Equals the entry name exactly (string match) | PASS / FAIL |
| S2.2 | cluster field | Matches the entry's declared cluster letter | PASS / FAIL |
| S2.3 | token_implications coherence | 7 token_implications fields in Mode B output match the entry's token_implications within acceptable variance (see S2.3 note) | PASS / PARTIAL / FAIL |
| S2.4 | confidence calibration | high (5+ signal matches, no conflicts); medium (3–4 matches); low (2–3 matches or conflicts) — verify confidence matches evidence | PASS / FAIL |
| S2.5 | designer_confirmation_needed populated | Non-empty when any token_implications field is inferred or when typography family is unresolved | PASS / FAIL |
| S2.6 | Cluster-specific hazards flagged | Dark-native entries (Cluster C default_scheme dark): default_scheme = dark documented. Organic modifier (Cluster D): modifier named. ISA-101 context (Neo-Industrial): flagged in designer_confirmation_needed. | PASS / PARTIAL |
| S2.7 | No invented styles | matched_style references a real entry name from style-reference-library.md; no composite names invented | PASS / FAIL |

**S2.3 note:** "Acceptable variance" means the pre-classification uses the same enum values as the library entry. A mismatch in `color_temperature` or `spacing_density` between Mode B output and the entry's token_implications is a Stage 2 FAIL — Mode D will extract tokens from the wrong cluster prior.

**HUMAN GATE: Direction Lock**

After Stage 2 passes, present a brief to the human reviewer before proceeding to Stage 3:

```
Stage 2 — Translation Reasoning: [PASS / PARTIAL]

Style: [entry name] | Cluster: [letter] | Confidence: [high/medium/low]
Key token priors: [color_temperature] / [spacing_density] / [type_personality]
[If PARTIAL: what needs confirmation before Mode D runs]

Confirm direction lock to proceed to Mode D config population?
```

Wait for explicit confirmation. Do not proceed to Stage 3 without it.

---

## Stage 3: Mode D Config Population

**Purpose:** Verify the active-brand.json output has all required fields populated, no schema violations, and correct handling of ADR-007 extension fields.

**What to load:** The completed `active-brand.json` config.

**Check groups:**

### 3A: Required Fields (from layer-0-evaluation-specs.md L1.2)

| # | Field path | Criteria | Result |
|---|-----------|----------|--------|
| S3.1 | brand.name | Non-empty string | PASS / FAIL |
| S3.2 | brand.description | Non-empty string, prose | PASS / FAIL |
| S3.3 | brand.temperature | One of: warm / cool / neutral / mixed | PASS / FAIL |
| S3.4 | brand.personality | Non-empty prose string | PASS / FAIL |
| S3.5 | tokens.typography.families | Object with at least one family defined; non-empty | PASS / FAIL |
| S3.6 | tokens.typography.scale | Object with defined scale values (h1–h4 at minimum) | PASS / FAIL |
| S3.7 | tokens.color.backgrounds | Object with primary; non-empty | PASS / FAIL |
| S3.8 | tokens.color.text | Object with primary; non-empty | PASS / FAIL |
| S3.9 | tokens.color.structural | Object with border-default; non-empty | PASS / FAIL |
| S3.10 | tokens.color.accent | Object with primary; non-empty | PASS / FAIL |
| S3.11 | tokens.color.semantic | Object with success, warning, error, info; non-empty (info added March 25, 2026 — Step 2D.2a now generates all four) | PASS / FAIL |
| S3.12 | tokens.spacing.base | Non-empty string (valid CSS: px, rem, etc.) | PASS / FAIL |

### 3B: PROVISIONAL Prefix Protocol (ADR-005)

| # | Check | Criteria | Result |
|---|-------|----------|--------|
| S3.13 | PROVISIONAL: syntax | Where present, uses exact format "PROVISIONAL: " (colon + space) | PASS / FAIL |
| S3.14 | provisional_fields[] accuracy | meta.provisional_fields[] lists every path with a PROVISIONAL: prefix; no paths are missing or invented | PASS / PARTIAL / FAIL |
| S3.15 | provisional_fields[] structure | Each entry has: path (dot-notation string), reason (human-readable), confidence (inferred or pending) | PASS / FAIL |

### 3C: Meta Fields

| # | Check | Criteria | Result |
|---|-------|----------|--------|
| S3.16 | meta.generated_by | Equals "mode-d" | PASS / FAIL |
| S3.17 | meta.direction_lock_confirmed | true (not false, not null) | PASS / FAIL |
| S3.18 | meta.locked_direction_label | Non-empty string matching the style entry name | PASS / FAIL |
| S3.19 | meta.generated_at | Valid ISO 8601 timestamp (parseable) | PASS / FAIL |

### 3D: ADR-007 Extension Fields

| # | Check | Criteria | Result |
|---|-------|----------|--------|
| S3.20 | tokens.focus.outline | Present when entry cluster is C, D, or when meta.accessibility.contrast_target is AA or AAA; has width, color, offset, style | PASS / FAIL / N/A |
| S3.21 | tokens.spacing.touch-target | Present; has min and comfortable values in px | PASS / FAIL |
| S3.22 | meta.accessibility | Present when meta.accessibility.contrast_target is set; has contrast_target and standard fields | PASS / FAIL / N/A |
| S3.23 | meta.internationalization | Present for Cluster D entries and any entry whose industry_fit.natural includes public sector or civic; has text_expansion_budget, direction_support, logical_properties_required | PASS / FAIL / N/A |

### 3E: Token Namespace Integrity

| # | Check | Criteria | Result |
|---|-------|----------|--------|
| S3.24 | No _note keys in tokens.* namespace | Scan all keys under tokens.*; any key beginning with _ is a violation (corrections-registry: design-note-fields-in-token-namespace). Rationale belongs in meta.implementation_notes, not the token namespace | PASS / FAIL |
| S3.25 | tokens.color.structural vs. tokens.color.border | Does not mix structural and border naming conventions within the same entry (pick one and stay consistent) | PASS / PARTIAL |

### 3F: Cluster-Specific Requirements

Run only the checks that apply to the entry's cluster.

**Cluster C (e.g., Neo-Industrial):**

| # | Check | Criteria | Result |
|---|-------|----------|--------|
| S3.26 | Dark-native config | meta.default_scheme = "dark" | PASS / FAIL |
| S3.27 | tokens.color.schemes.dark | Present; parallel scheme structure per ADR-006 Option C | PASS / FAIL |
| S3.28 | ISA-101 semantic encoding | tokens.color.semantic includes alarm_high_priority (orange) and nominal (gray) | PASS / FAIL |
| S3.29 | ISA-101 exception documented | brand.style_notes documents WS6 ISA-101 exception — ISA-101 high-contrast chromatic signals against achromatic foundation, secondary indicator requirement | PASS / FAIL |
| S3.30 | Dual-family typography | tokens.typography.families.body.body_register = "monospace-primary" (or equivalent monospace declaration); display family is heavy grotesque | PASS / FAIL |

**Cluster D (e.g., Civic Modern):**

| # | Check | Criteria | Result |
|---|-------|----------|--------|
| S3.31 | Light-default config | meta.default_scheme = "light" | PASS / FAIL |
| S3.32 | AAA contrast target | meta.accessibility.contrast_target = "AAA" | PASS / FAIL |
| S3.33 | Organic modifier reflected | tokens.radius.sm in range 2–4px (slight); humanist body typeface | PASS / FAIL |
| S3.34 | Touch target ≥ 48px | tokens.spacing.touch-target.min = "48px" or greater | PASS / FAIL |
| S3.35 | i18n fields complete | meta.internationalization.text_expansion_budget present; direction_support includes "rtl"; logical_properties_required = true | PASS / FAIL |

*Note: S3.26–S3.35 are cluster-specific. Mark N/A for clusters where the check does not apply. Do not fail a non-Cluster-C entry for lacking a dark scheme.*

---

## Stage 4: Warning Sign Checks

**Purpose:** Run the reviewer's full current check set against the config. This stage is pure delegation: `heyhi-style-to-token-reviewer` owns the check definitions, the check count, and the expected-PASS criteria. Do not maintain a copy of its check list here — a copied list drifts the moment the reviewer gains or changes a check (as happened when Checks 9/10 were grafted on 2026-06-02 while this stage still said "9 warning signs").

**Procedure:** Load `heyhi-skills/heyhi-style-to-token-reviewer/SKILL.md` and execute Steps 0–2 in full — every check the reviewer currently defines, at its current criteria. Record each check result independently.

**Valid check results:** PASS / PARTIAL / FAIL / CONSIDERED_DEPARTURE. `CONSIDERED_DEPARTURE` is a resolved status reachable only from PARTIAL. It requires: (a) the style entry has a `taste_profile` with a `boundary_behavior` whose `trigger` maps to the check that fired, and (b) the reviewer has populated all required fields in a `meta.taste_departures[]` entry in the config. For configs without a `taste_profile`, `CONSIDERED_DEPARTURE` is not reachable — PARTIALs fire at full weight.

**Expected results for passing configs:** the reviewer's own per-check PASS criteria are authoritative — read them from its SKILL.md at run time rather than from a table here.

**Critical correction for WS6:** If the config is ISA-101 (Neo-Industrial or similar operational context) and brand.style_notes documents the ISA-101 exception, the result is PASS — not PARTIAL. The test is whether the departure is documented, not whether the saturation delta looks large. See corrections-registry.yaml: design-ws6-documented-exception-pass.

**Stage 4 Verdict:** PASS (0 FAILs, 0 unreviewed PARTIALs — CONSIDERED_DEPARTUREs permitted) / CONDITIONAL PASS (1 FAIL, or 2+ unreviewed PARTIALs — CONSIDERED_DEPARTUREs do not count toward this threshold) / FAIL (2+ FAILs)

An *unreviewed PARTIAL* is a PARTIAL with no corresponding entry in `meta.taste_departures[]`. A PARTIAL with a fully populated `meta.taste_departures[]` entry and the check result updated to CONSIDERED_DEPARTURE is a resolved finding and does not count toward the CONDITIONAL PASS threshold.

---

## Step 5: Produce the Validation Report

After all four stages are complete, produce a structured report.

```markdown
## Layer 0 Pipeline Validation — [Entry Name]
Date: [date]
Mode: [A / B / C]
Config: [file path or "provided conversationally"]
Cluster: [A / B / C / D / E]

---

### Stage Results Summary

| Stage | Checks | Result | Notes |
|-------|--------|--------|-------|
| Stage 1: Entry Field Completeness | 5 | PASS / FAIL | [key finding if any] |
| Stage 2: Translation Reasoning | 7 | PASS / PARTIAL / FAIL | [key finding if any] |
| Stage 3: Mode D Config Population | N | PASS / PARTIAL / FAIL | [N = varies by cluster] |
| Stage 4: Warning Sign Checks | 9 | PASS / CONDITIONAL PASS / FAIL | [checks with findings] |

---

### Overall Verdict

[PIPELINE PASS / CONDITIONAL PASS / FAIL]

- PIPELINE PASS: All stages PASS or CONDITIONAL PASS with documented findings only. Config is ready for design-system-review.
- CONDITIONAL PASS: One FAIL in Stage 3 or 4 that can be corrected in-config. Listed below with correction path.
- FAIL: Stage 1 or 2 FAIL, or 2+ FAILs in Stage 4. Root-skill or entry repair required before config is usable.

---

### Findings by Stage

#### Stage 1: Entry Field Completeness — [PASS / FAIL]
[List any failing checks with field names and correction instructions]

#### Stage 2: Translation Reasoning — [PASS / PARTIAL / FAIL]
[List any failing checks. Note if Mode B output was generated for this run or provided]

#### Stage 3: Mode D Config Population — [PASS / PARTIAL / FAIL]
[List each failing check with field path, found value, expected value]
[Flag any ADR-007 extension fields missing for the entry's cluster]

#### Stage 4: Warning Sign Checks — [PASS / CONDITIONAL PASS / FAIL]
[Reproduce the full Style-to-Token Review table from heyhi-style-to-token-reviewer]
[Document any PARTIAL results with correction options]

---

### Priority Corrections
[Only present if Verdict is Conditional Pass or Fail. Ordered by impact.]

1. [Most critical — affects multiple stages or downstream skills]
2. [...]

### Recommended Next Step
[PIPELINE PASS:] Proceed to `design-system-review` Mode A (v0 → v1 visual fidelity review).
[CONDITIONAL PASS:] Address listed corrections in the config, then rerun Stage 3 and 4 only (Mode B).
[FAIL:] Address the Stage 1 or 2 finding first. Re-run the full pipeline (Mode A) after repair.
```

---

## HUMAN GATE: Promotion Decision

After delivering the report, present the overall verdict to the human reviewer before declaring the config ready:

```
Pipeline Validation: [Entry Name] — [PIPELINE PASS / CONDITIONAL PASS / FAIL]

Stages: 1 [result] | 2 [result] | 3 [result] | 4 [result]
Total checks: [N]

[If any FAIL or PARTIAL:] Priority corrections are listed in the report above.

Confirm to proceed to design-system-review, or return for corrections first?
```

Wait for the human reviewer's explicit confirmation before the config moves forward to `design-system-review`.

---

## Mode C: 68-Point Component Layer Regression Test

Run this mode after any update to the Layer 0 pipeline skills (heyhi-style-selection, design-system-onboard, heyhi-style-to-token-reviewer, heyhi-style-entry-author). Confirms the reference configs still pass all checks — catching regressions before they reach client work.

**Known coverage gap (stated, not silent):** the 68-point scaffold below predates the reviewer's 2026-06-02 graft of Check 9 (accent saturation and count ceiling) and Check 10 (typography intent). Rows R29–R36 and R59–R66 cover the original WS1–WS9 only; the scaffold has NO expected-result rows for Checks 9/10 on either reference entry. A Mode C run therefore under-covers the reviewer's current check set by two checks per entry. Extending the scaffold requires re-deriving Check 9/10 expected results for Entry 10 and Entry 16 against their fixtures — a deliberate session, not a drive-by. Until then, a full-coverage regression signal for Checks 9/10 comes only from running the reviewer directly (Stage 4 in Mode A/B).

### What counts as a regression

A check that previously passed now FAILs or degrades to PARTIAL, with no documented change to the entry or config explaining the change. A PARTIAL that was present in the prior run and remains PARTIAL is not a regression — it is a known documented condition.

### Entry 10 (Neo-Industrial) — 37 Checks

Load: `ai-services/design-intelligence/test-fixtures/neo-industrial-active-brand.json`

**Stage 1 — Entry Field Completeness (5 checks)**

| # | Check | Expected | Pass if |
|---|-------|----------|---------|
| R1 | Required schema fields present | entry_id, name, cluster: C, descriptors.mood ≥3 terms, descriptors.anti_mood ≥1 term | All present |
| R2 | token_implications: 7 fields | color_temperature, spacing_density, border_radius_range, shadow_depth, type_scale_ratio, type_personality, motion_personality all present and non-empty | All 7 present |
| R3 | Enum values valid per heyhi-style-entry-author Mode B schema | color_temperature: cool; spacing_density: dense; border_radius_range: sharp; motion_personality: minimal | All match |
| R4 | industry_fit.natural includes industrial/operational sector | manufacturing, industrial IoT, construction tech, or equivalent | Present |
| R5 | agent_context_snippet references dual-family typography or ISA-101 | Non-empty; distinguishes Neo-Industrial from sibling entries | Present |

**Stage 2 — Translation Reasoning (7 checks)**

| # | Check | Expected | Pass if |
|---|-------|----------|---------|
| R6 | matched_style | "Neo-Industrial" | Exact match |
| R7 | cluster | "C" | Exact match |
| R8 | color_temperature in translation output | "cool" | Matches entry |
| R9 | spacing_density in translation output | "dense" | Matches entry |
| R10 | border_radius_range in translation output | "sharp" | Matches entry |
| R11 | type_personality in translation output | "grotesque" (display) or dual-family noted | Matches entry |
| R12 | motion_personality in translation output | "minimal" | Matches entry |

**Stage 3 — Mode D Config Population (16 checks)**

| # | Check | Expected | Pass if |
|---|-------|----------|---------|
| R13 | brand.temperature | "cool" | Exact match |
| R14 | brand.style_notes | Documents ISA-101 exception for WS6 + WS3 PARTIAL zone separation rationale | Non-empty; ISA-101 referenced |
| R15 | meta.generated_by | "mode-d" | Exact match |
| R16 | meta.direction_lock_confirmed | true | true |
| R17 | meta.default_scheme | "dark" | "dark" |
| R18 | tokens.typography.families.body.body_register | "monospace-primary" | Exact match |
| R19 | tokens.typography.scale.ratio | "Augmented Fourth 1.414x" or equivalent | Contains "Augmented Fourth" |
| R20 | tokens.color.backgrounds.primary | Dark value: hex ≤ #333333 luminance | Dark range verified |
| R21 | tokens.color.semantic.alarm_high_priority | Present and non-empty orange value (ADR-007 Extension 3) | Present |
| R22 | tokens.color.semantic.nominal | Present and non-empty gray value (ISA-101 nominal state) | Present |
| R23 | tokens.color.schemes.dark | Present (ADR-006 Option C scheme namespacing) | Present |
| R24 | tokens.color.schemes.light | Present, marked PROVISIONAL (dark-native) | Present |
| R25 | tokens.spacing.base | "4px" | Exact match |
| R26 | tokens.spacing.touch-target | Present with min and comfortable keys (ADR-007 Extension 2) | Both keys present |
| R27 | tokens.focus.outline | Present with width, color, offset, style (ADR-007 Extension 1) | All 4 keys present |
| R28 | No _note keys in tokens.* namespace | Scan all keys under tokens.*; zero underscore-prefixed keys | Zero violations |

**Stage 4 — Warning Sign Checks (9 checks)**

| # | Warning Sign | Expected | Pass if |
|---|-------------|----------|---------|
| R29 | WS1 Contrast Problem | PASS | PASS |
| R30 | WS2 Performed Translation | PASS | PASS |
| R31 | WS3 Density Drift | PARTIAL (intentional — zone separation documented in brand.style_notes and meta.scale_reasoning) | PARTIAL with documentation |
| R32 | WS4 Scale Inversion | PASS | PASS |
| R33 | WS5 Grey-Default Trap | PASS | PASS |
| R34 | WS6 Semantic Orphan | PASS (ISA-101 documented exception — NOT PARTIAL; see corrections-registry design-ws6-documented-exception-pass) | PASS only; PARTIAL is a regression |
| R34b | WS9 Brand-Utility Collision | PASS (ISA-101 alarm palette uses fully saturated chromatic signals clearly distinct from any achromatic or dark accent) | PASS |
| R35 | WS7 Incoherent Hybrid | PASS | PASS |
| R36 | WS8 Scale-Density Incoherence | PASS (Augmented Fourth 1.414x exceeds Major Third threshold) | PASS |

---

### Entry 16 (Civic Modern) — 31 Checks

Load: `ai-services/design-intelligence/test-fixtures/civic-modern-v0.2.0-active-brand.json` (internal version 0.2.1 — T1.PVC-002 baseline)

**Stage 1 — Entry Field Completeness (4 checks)**

| # | Check | Expected | Pass if |
|---|-------|----------|---------|
| R37 | Required schema fields present | entry_id, name, cluster: D, descriptors.mood ≥3 terms, descriptors.anti_mood ≥1 term | All present |
| R38 | token_implications: 7 fields | All 7 fields present and non-empty | All 7 present |
| R39 | industry_fit.natural includes civic/government/public sector | civic tech, government services, public institutions, or equivalent | Present |
| R40 | Organic modifier documented | brand.personality or agent_context_snippet references the Organic modifier (humanist warmth expressed through typeface, not palette temperature) | Referenced |

**Stage 2 — Translation Reasoning (6 checks)**

| # | Check | Expected | Pass if |
|---|-------|----------|---------|
| R41 | matched_style | "Civic Modern" | Exact match |
| R42 | cluster | "D" | Exact match |
| R43 | color_temperature in translation output | "cool" | Matches entry |
| R44 | spacing_density in translation output | "spacious" | Matches entry |
| R45 | border_radius_range in translation output | "slight" (Organic modifier — 2–4px) | "slight" |
| R46 | motion_personality in translation output | "minimal" | Matches entry |

**Stage 3 — Mode D Config Population (12 checks)**

| # | Check | Expected | Pass if |
|---|-------|----------|---------|
| R47 | brand.temperature | "cool" | Exact match |
| R48 | meta.default_scheme | "light" | "light" |
| R49 | meta.accessibility.contrast_target | "AAA" | "AAA" |
| R50 | meta.internationalization.text_expansion_budget | "35-40%" or equivalent | Present |
| R51 | meta.internationalization.direction_support | Includes "rtl" | "rtl" in array |
| R52 | meta.internationalization.logical_properties_required | true | true |
| R53 | tokens.typography.families.display.family | Humanist or geometric OFL typeface (IBM Plex Sans or equivalent) | Non-empty; OFL or equivalent noted |
| R54 | tokens.typography.scale.ratio | "Major Third 1.25x" | Contains "Major Third" |
| R55 | tokens.typography.scale.h1 | ≈ 44.0px (from 18px × 1.25^4 — corrected from v0 arithmetic error of 44.6) | 44.0px ± 0.5px |
| R56 | tokens.radius.sm | In range 2–4px (Organic modifier — slight) | 2–4px range |
| R57 | tokens.spacing.touch-target.min | "48px" (exceeds WCAG 2.2 SC 2.5.8 — ADR-007 Extension 2) | "48px" |
| R58 | tokens.focus.outline.color | Derived from accent.primary and listed in meta.provisional_fields[] | Present in both locations |

**Stage 4 — Warning Sign Checks (9 checks)**

| # | Warning Sign | Expected | Pass if |
|---|-------------|----------|---------|
| R59 | WS1 Contrast Problem | PASS | PASS |
| R60 | WS2 Performed Translation | PASS | PASS |
| R61 | WS3 Density Drift | PASS (spacious spacing + Major Third — coherent) | PASS |
| R62 | WS4 Scale Inversion | PASS | PASS |
| R63 | WS5 Grey-Default Trap | PASS | PASS |
| R64 | WS6 Semantic Orphan | PASS (AAA contrast target calibrates semantic saturation; cool register maintained) | PASS |
| R64b | WS9 Brand-Utility Collision | PASS (cool-neutral accent palette maintains 20°+ hue distance to all semantic utility colors; no collision) | PASS |
| R65 | WS7 Incoherent Hybrid | PASS (Organic modifier documented in brand.personality and brand.style_notes if present) | PASS |
| R66 | WS8 Scale-Density Incoherence | PASS (Major Third 1.25x exceeds the Minor Third threshold; no ambiguous heading steps) | PASS |

---

### Regression Test Report Format

```markdown
## 68-Point Regression Test — Layer 0 Pipeline
Date: [date]
Trigger: [reason for regression run — e.g., heyhi-style-to-token-reviewer promoted v1.1]

---

### Entry 10 (Neo-Industrial) — 37/37 expected

| Stage | Checks | Result | Regressions |
|-------|--------|--------|-------------|
| Stage 1 | 5 | PASS / FAIL | [list check # if FAIL] |
| Stage 2 | 7 | PASS / FAIL | [...] |
| Stage 3 | 16 | PASS / PARTIAL / FAIL | [...] |
| Stage 4 | 9 | PASS / CONDITIONAL PASS / FAIL | [...] |
| **Total** | **37** | | |

### Entry 16 (Civic Modern) — 31/31 expected

| Stage | Checks | Result | Regressions |
|-------|--------|--------|-------------|
| Stage 1 | 4 | PASS / FAIL | [...] |
| Stage 2 | 6 | PASS / FAIL | [...] |
| Stage 3 | 12 | PASS / PARTIAL / FAIL | [...] |
| Stage 4 | 9 | PASS / CONDITIONAL PASS / FAIL | [...] |
| **Total** | **31** | | |

---

### Regression Verdict: [CLEAN / REGRESSIONS FOUND]

[CLEAN:] All 68 checks at expected results. Pipeline is stable for production use.
[REGRESSIONS FOUND:] [N] checks degraded from expected. Repair required before promotion.

### Regression Details
[Only present if REGRESSIONS FOUND. List check #, check description, prior result, current result, probable cause.]

### Recommended Action
[CLEAN:] Proceed with the update that triggered this regression test.
[REGRESSIONS FOUND:] Do not promote the triggering update until listed regressions are resolved.
```

---

## Consistency Checks and Logical Fallacy Guards

The following checks catch validation errors internal to this skill — cases where the validator itself could produce misleading results.

**Guard 1: WS6 classification error.** If WS6 result is PARTIAL but brand.style_notes or meta.style_notes documents a saturation departure as intentional, the result must be PASS, not PARTIAL. The criterion in heyhi-style-to-token-reviewer SKILL.md is explicit: documented intentional departure = PASS. Classifying it PARTIAL is a false positive. See corrections-registry.yaml: design-ws6-documented-exception-pass.

**Guard 2: Cluster-specific Stage 3 checks applied to wrong clusters.** S3.26–S3.30 are Cluster C checks. S3.31–S3.35 are Cluster D checks. Never fail a Cluster B or E config for missing a dark scheme (S3.26) or AAA contrast target (S3.32) unless that entry explicitly claims those characteristics.

**Guard 3: PROVISIONAL fields penalized as missing.** A field marked "PROVISIONAL: [value]" is present — it has a value, even if inferred. Check S3.14 concerns whether the provisional_fields[] inventory is accurate, not whether provisional values count as populated. S3.1–S3.12 pass when the field has a PROVISIONAL: value.

**Guard 4: WS3 PARTIAL vs. FAIL distinction.** For Neo-Industrial and similar zone-separation architectures, WS3 PARTIAL is the correct result when body/data zones intentionally use a fixed register outside the scale system. This is a documented architectural decision, not a density drift error. Escalating to FAIL incorrectly blocks a valid config.

**Guard 5: Stage ordering enforced.** Stage 1 must pass before Stage 2. Stage 2 must pass and the direction lock gate must be confirmed before Stage 3. A pipeline that skips Stage 1 and fails at Stage 4 may be tracing a symptom rather than the root cause (entry field error propagated downstream).

**Guard 6: CONSIDERED_DEPARTURE without complete documentation.** If a Stage 4 check result is recorded as `CONSIDERED_DEPARTURE` but the corresponding `meta.taste_departures[]` entry is absent or missing any of the five required fields (maps_to_bb, check_fired, alternative_carrier, not_a_departure_verified, revert_condition), this is a documentation violation. Revert the result to PARTIAL and require documentation completion before validation proceeds. `CONSIDERED_DEPARTURE` is not an override label — the documentation is the status change.

---

## Smoke Test Checklist

Before delivering any validation output from this skill, verify:

- [ ] All four stages run and documented (no stage skipped; cluster-specific checks noted as N/A rather than omitted)
- [ ] Each check result states PASS / FAIL / PARTIAL / N/A with specific evidence (not "looks correct")
- [ ] WS6 result is PASS for any config where the saturation departure is documented in style_notes (not PARTIAL — see Guard 1)
- [ ] Cluster-specific Stage 3 checks marked N/A for non-applicable clusters (not FAIL — see Guard 2)
- [ ] PROVISIONAL: fields counted as present for S3.1–S3.12 purposes (see Guard 3)
- [ ] WS3 PARTIAL accepted for documented zone-separation architectures (not escalated to FAIL — see Guard 4)
- [ ] Stage ordering respected — Stage 1 verified before Stage 2, direction lock confirmed before Stage 3 (see Guard 5)
- [ ] HUMAN GATE blocks present at Stage 2 completion and after Stage 4 (not skipped)
- [ ] Overall verdict follows the three-tier rubric (PIPELINE PASS / CONDITIONAL PASS / FAIL)
- [ ] Regression mode (Mode C): checks R1–R66 run against reference configs; any result departing from expected noted as potential regression
- [ ] Any CONSIDERED_DEPARTURE result in Stage 4 has a corresponding entry in meta.taste_departures[] with all five required fields populated (maps_to_bb, check_fired, alternative_carrier, not_a_departure_verified, revert_condition) — Guard 6
- [ ] Regression mode (Mode C): CONSIDERED_DEPARTURE does not appear in either reference config report — Entry 10 and Entry 16 have no taste_profile, so Criterion 1 (Boundary Map Gate) cannot be satisfied and all PARTIALs fire at full weight
- [ ] No standalone "AI" in validation output
- [ ] No banned words in output (leverage, unlock, seamless, etc.)
- [ ] Em dashes: maximum 2 in any client-facing output generated by this skill
- [ ] No pricing in output

---

## Reference Files

Load when relevant, not by default:

- `ai-services/design-intelligence/style-reference-library.md` — Stage 1 and 2 (entry field checks and translation reasoning)
- `ai-services/design-intelligence/style-to-token-translation.md` Parts 5 and 6 — Stage 4 (cluster priors and the warning signs; the reviewer's current check set is authoritative)
- `heyhi-skills/heyhi-style-to-token-reviewer/SKILL.md` — Stage 4 procedure (always load for Stage 4)
- `heyhi-skills/heyhi-style-entry-author/SKILL.md` Mode B — Stage 1 repair path (load only if Stage 1 FAIL)
- `heyhi-skills/design-system-onboard/SKILL.md` — Stage 3 repair path (load only if Stage 3 FAIL requires understanding the extraction procedure)
- `ai-services/design-intelligence/layer-0-evaluation-specs.md` — Full evaluation spec (load for Mode C deep review or when a test result needs spec-level justification)
- `ai-services/design-intelligence/test-fixtures/neo-industrial-active-brand.json` — Mode C Entry 10 reference
- `ai-services/design-intelligence/test-fixtures/civic-modern-v0.2.0-active-brand.json` — Mode C Entry 16 reference (v0.2.1 internally — T1.PVC-002 baseline)

---

## Exit Gate Required Headers (bottom-of-skill bracket)

This skill closes through the Exit Gate Flavor A (`CLAUDE-SESSION-RULES.md § Exit Gate`). Before declaring done, confirm every required header below contains real content, not a claim:

- `## Fixes Applied`
- `## Smoke Test`
- `## Next Session Prompt`

If any header is empty or contains advisory prose ("I checked for bugs") instead of a concrete artifact, the gate has not been satisfied. Apply fixes until clean — then emit.

---

*HeyHi Confidential — Skill internal methodology. Not for client distribution.*

*Layer 0 pipeline skill. Sits after design-system-onboard and validates the full pipeline before design-system-review.*

*Bay Design LLC d/b/a HeyHi · Built March 2026 · Updated 2026-04-05 (WS9 Brand-Utility Collision added; 8 → 9 warning signs; regression scaffold 66 → 68 points)*
