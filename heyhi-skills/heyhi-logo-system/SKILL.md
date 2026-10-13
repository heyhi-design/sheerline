---
name: heyhi-logo-system
description: >-
  Asset-level logo work across three modes: concept direction generation,
  rigorous mark critique, and production logo system specification. Use when the user
  says "logo concept", "logo directions", "critique this logo", "review the logo",
  "logo refinement", "logo spec", "logo system spec", "wordmark", or "favicon
  guidance". Builds on Layer 0 Design Intelligence foundations rather than a cold
  brief, and emits a human spec plus a machine logo-namespace JSON companion. For a
  whole-visual-language direction brief use heyhi-style-brief; for system-level
  health use heyhi-design-intelligence-audit; for style classification use
  heyhi-style-selection. This skill designs and specifies a single mark or mark
  system, not a token system or a whole aesthetic.
version: "0.3.2"
updated: "2026-10-13"
changes: "v0.3.2 (2026-10-13): Generalized for the Sheerline scaffold: instance data (brand defaults, client/engagement history, owner names, ratified values) moved to instance-only files or neutral wording; method unchanged. v0.3.1 (2026-06-12): Added a Mode 3 return-path note: resolving a provisional spec field later (favicon, leading option, palette) is a propagation task across the json, the human spec, the guidelines, the in-artifact specimen, and the dev-handoff, closed by a grep-verify for the old term. Origin: a client's favicon-of-record resolution, where a from-memory propagation missed three refs that the grep caught. Source: skill-updates/heyhi-logo-system/resolved-provisional-field-propagation-2026-06-12.md (owner-gated promotion 2026-06-12). v0.3.0 (2026-06-10): Reconciled three un-promoted streams into the deployed skill in one owner-gated pass. Made the v0.2.0 mechanics the base; layered Session 2A refinements R1-R4 (chained-run artifact routing to working/; projected-vs-measured axis honesty with a mandatory second critique; recompute-and-diff in the smoke test; credibility-calibration for playful marks in high-trust categories); added four on-demand research-richness reference modules (references/logo-typology.md, references/render-brief-template.md, references/scale-degradation-matrix.md, references/mark-failure-modes.md) distilled from an external ckm:logo-design review. Modules are pointer-linked from this SKILL.md per Earn the Room, not registry dependencies; no schema change, no registry version or capability-count change. Resolved the unverifiable style-vocabulary term-count to a point-to-file reference. Source: skill-updates/heyhi-logo-system/{promotion-and-reconciliation-spec.md, ckm-distillation-and-gap-analysis.md}. v0.2.0: Integrated the 2026-06-04 live stress-test findings (NEW-1, NEW-2, F1-F7). Added a required render-and-verify loop on any rendering path (NEW-1) plus real-brand-typeface rendering (NEW-2); added a comparative Select lane to Critique (F1); expanded the standalone-Critique input checklist and pointed self-application at a canonical brand-intent source (F2); path-anchored the eight research dependencies and fixed the inconsistent research/ prefix (F3); reclassified the research loads as on-demand enrichment per Earn the Room (F4); added a raster-input fidelity rule on the Legibility/Scalability axes (F5); noted worked-example co-location (F6) and that an empty diary wing is normal on first run (F7). Source: skill-updates/heyhi-logo-system/v0.2.0-edits.md + handoff Section A (2026-06-04). Drafted in skill-updates/; promotion owner-gated. v0.1.0: Initial build. Three modes (Concept, Critique, Spec) modeled on the audit skill's mode structure and the photography-style identity-system convention. Mode-chaining contract, logo-namespace dual artifact, six-axis critique with Logo Readiness Profile, tokenization-boundary spec split. Source: plans/plan-heyhi-logo-system-2026-05-28.md. Owner sign-off on namespace field set and Concept generation boundary, 2026-05-29."
classification: HeyHi Confidential
---

# HeyHi Logo System

This skill runs the full logo lifecycle as one skill with three modes: **Concept** (generate mark directions), **Critique** (review a proposed mark), and **Spec** (produce a production logo system). It is asset-level. It designs and specifies a single mark or mark system. It is not the system-level `heyhi-design-intelligence-audit` and not the style-direction `heyhi-style-brief`.

The skill loads the interrogation, vocabulary, and tokenization-boundary research HeyHi has already built, rather than generating from a cold brief. Every mode produces a dual artifact: a human-readable document and a machine-readable `logo`-namespace JSON companion.

For all rubrics, templates, the six-axis scoring, the readiness profile, the spec template, and the JSON shape, see [reference.md](reference.md).

---

> **Exit Gate (Flavor A).** This skill closes through the canonical Exit Gate — see `CLAUDE-SESSION-RULES.md § Exit Gate`. Required headers, in order: `## Fixes Applied`, `## Smoke Test`, `## Next Session Prompt`. Empty headers are visible failures. Conversational carve-out: the facilitation parts of Concept (interrogation) and Critique (the refinement conversation) run as dialogue and are exempt from the gate until a document artifact is produced.

---

## Step 0: Route to a Mode

- **Concept** — produce N distinct mark directions for client iteration. Trigger words: "logo concept", "logo directions", "explore marks", "we need a logo".
- **Critique** — rigorous review of a proposed mark. Trigger words: "critique this logo", "review the logo", "is this mark working", "logo refinement".
- **Spec** — production logo system specification. Trigger words: "logo spec", "logo system spec", "build out the logo guidelines", "favicon guidance".

**Select (comparative path within Critique).** When several candidate marks arrive together — the common designer hand-off, an N-up with no Concept records — run Critique in its comparative lane (Mode 2 below): score each candidate on the six axes, then close by recommending one with reasoning and a do-not-do list, borrowing Concept's recommendation shape. This is not a fourth mode; it is the form Critique takes when input is N candidates rather than one. Trigger words: "which of these", "pick a direction", "compare these marks".

Modes can chain (Concept → Critique → Spec). If the intent is ambiguous, ask one question: "Are we generating directions, reviewing a mark or comparing several, or specifying the production system?"

**Boundary check before loading.** If the request is about the whole visual language (color feel, type behavior, imagery, sector fit) rather than a mark, this is `heyhi-style-brief`, not this skill. If it is about a design system's health or drift, it is `heyhi-design-intelligence-audit`. Hold the boundary.

**Voice.** All client-facing copy in any mode passes `brand/voice-system.md` and `brand/writing-rules.md`. Load `heyhi-voice` for any output the skill produces. Never "AI" as a standalone word. Maximum two em dashes per output document. Full banned-word list applies.

---

## Research dependencies (on-demand enrichment, not required)

Per Earn the Room, `reference.md` alone is sufficient for a defensible run — it inlines the six-axis methods, the severity rubric, the readiness scale, and the tokenization split. The eight research files below are **enriching, load on demand**, not required imperatives (F4). Reserve "load" for what a run cannot proceed without. All paths are resolved from the project root (F3); the inconsistent bare `research/` prefix from v0.1.0 is corrected here.

| File | Resolved path |
|---|---|
| design-intent-document-template.md | `ai-services/design-intelligence/design-intent-document-template.md` |
| style-descriptor-vocabulary.md | `ai-services/design-intelligence/style-descriptor-vocabulary.md` |
| style-reference-library.md | `ai-services/design-intelligence/style-reference-library.md` |
| gate0-facilitation-guide.md | `ai-services/design-intelligence/gate0-facilitation-guide.md` |
| figma-mcp-integration-plan.md | `ai-services/design-intelligence/figma-mcp-integration-plan.md` |
| designer-questioning-methodology.md | `ai-services/design-intelligence/research/designer-questioning-methodology.md` |
| visual-language-theory.md | `ai-services/design-intelligence/research/visual-language-theory.md` |
| tokenization-boundary.md | `ai-services/design-intelligence/research/tokenization-boundary.md` |

If any single file stays effectively load-bearing in practice, it is `style-descriptor-vocabulary.md` (Concept's moodboard language); promote only that one to required if a run repeatedly needs it.

---

## Research-richness modules (on-demand)

Four reference modules carry the construction-level depth. Load the one the mode needs; none load by default (Earn the Room). They are pointer-linked from this SKILL.md, not registry dependencies.

| Module | File | Load in |
|---|---|---|
| Logo construction typology | `references/logo-typology.md` | Concept, Spec |
| Render-brief template | `references/render-brief-template.md` | Concept (opt-in render only) |
| Scale-degradation matrix | `references/scale-degradation-matrix.md` | Spec, Critique |
| Mark failure-mode catalog | `references/mark-failure-modes.md` | Critique |

---

## Mode 1 — Concept

Purpose: produce N distinct mark directions (default 3, configurable) for client iteration.

**1. Interrogate first.** Before generating anything, surface hard constraints (not preferences), anti-descriptors (what the mark must never be mistaken for), and the emotional target. Do not accept the brief at face value. This is Earn the Room: the directions are only as good as the questions asked before them. Name what the mark must communicate — the upstream, non-tokenizable question. The interrogation method in reference.md is sufficient; for the deep methodology load `ai-services/design-intelligence/research/designer-questioning-methodology.md` on demand (enriching, not required — see "Research dependencies").

**2. Map, do not invent.** Pull moodboard language from `ai-services/design-intelligence/style-descriptor-vocabulary.md` (see the file for the current descriptor set) and align each direction to one or more clusters in `ai-services/design-intelligence/style-reference-library.md`. Do not invent keywords from scratch. Choose the *construction typology* here too (the seven typologies in `references/logo-typology.md`), and state it alongside the cluster. Construction and aesthetic are separate axes; name both.

**3. Generate directions.** For each direction, produce the full Concept Direction Record from reference.md: concept name, strategic idea, symbol direction, wordmark style, composition variants, color direction, cluster alignment, tokenization preview, risks and misreads (grounded in `ai-services/design-intelligence/research/visual-language-theory.md`), best-fit use cases.

> **Generation boundary (instance-owner sign-off, 2026-05-29).** Concept specifies directions in words and structured attributes by default. Rendering candidate marks — image generation or Figma — is an optional step the operator invokes explicitly. It is never the default. Mark direction is HeyHi judgment under the don't-automate-this line; the skill makes the directions legible, it does not auto-produce the marks. When rendering is requested, say so in the output and treat the rendered marks as illustrations of the specified direction, not as the decision.
>
> **Render-and-verify is mandatory when rendering (NEW-1, v0.2.0).** Whenever a mark is actually rendered — image generation, SVG, or Figma — render it to a viewable image and inspect it before scoring or presenting. Generating geometry "by spec" without looking is the defect that produced the sloppy rounds in the 2026-06-04 stress test. Iterate against the rendered result, not against the code. Render on the real brand typeface (NEW-2), never a stand-in face. If the medium cannot be previewed (CSS/JS motion), render a representative proxy — a single still filmstrip of the key beats (rest → mid → overshoot → settle) — and state that timing and easing cannot be felt from stills. Full method: reference.md "Rendering and Verification."

**Render brief (opt-in).** If the operator invokes the opt-in render step, build the generation brief from `references/render-brief-template.md` (provider-agnostic; symbol only; negatives from the do-not-do list), then run the render-and-verify loop above.

**4. Tokenization preview.** For each direction, flag how cleanly it will translate to a token system. This keeps Concept forward-compatible with a later Build engagement.

**5. Recommend one.** One recommended direction with reasoning, the moodboard keyword set (sourced from the vocabulary), and a do-not-do list (the anti-descriptors from step 1).

**Chaining.** The recommended direction's record is the artifact Critique consumes. See the Mode-Chaining Contract in reference.md.

---

## Mode 2 — Critique

Purpose: rigorous, defensible review of a proposed mark.

**1. Score the six axes.** Brand fit, distinctiveness, legibility, scalability, system readiness, risk of misinterpretation. Each is operationalized in reference.md — use those methods, not impressions. Legibility uses the 16px test from `ai-services/design-intelligence/gate0-facilitation-guide.md`. Scalability uses the scale-degradation logic from `ai-services/design-intelligence/design-intent-document-template.md`. If the mark is being rendered for the score (rather than scored from an existing asset), the render-and-verify loop applies — render it, on the real brand typeface, and look at it before scoring (NEW-1/NEW-2; reference.md "Rendering and Verification"). When only raster input is available, the Legibility and Scalability scores are estimates — mark them "estimated (raster)" and lower go/no-go confidence per the raster-input rule in reference.md (F5). On each axis, scan `references/mark-failure-modes.md` for the typology in hand: it lists what usually breaks for this construction type, with default severities. Score Scalability against the defined reduction path in `references/scale-degradation-matrix.md`, not an impression.

**Comparative (Select) lane.** When the input is N candidate marks rather than one (no Concept records), score each candidate on all six axes, then close by recommending one — reasoning plus a do-not-do list, borrowing Concept's recommendation shape. If two candidates land on the same readiness shape, break the tie on the highest-stakes axis for the engagement (usually Legibility at the primary digital surface, or Distinctiveness against the competitive set), and name the tie-break you used.

**Credibility calibration (high-trust categories, R4).** When a playful or illustrative style is applied to a high-trust, high-consideration category (trade, property, financial, health), run a credibility-calibration check on the Brand-fit and Risk-of-misinterpretation axes: does the mark read competent as well as characterful, and does the recommended system pair the character with proof (a formal badge or seal, the trust line, real photography) rather than standing on personality alone? Weight the recommendation toward the emblem form (see `references/logo-typology.md` and the R4 row in `references/mark-failure-modes.md`) if the character skews too playful for the stakes. Exception: in luxury or entertainment, a literal proof-badge can instead undercut the brand, so calibrate to the category.

**2. Run a real contrast pass.** WCAG numbers against each colorway, evaluated against the engagement's brand config (the client's `active-brand.json` when one exists; HeyHi's when self-applied). State AA/AAA targets and computed ratios.

**3. Apply the severity taxonomy.** Critical / High / Medium / Low, defined in reference.md. The source prompt asks for severity ranking but never defines it; this does.

**4. Produce the Logo Readiness Profile.** Score each of the six axes on the readiness scale (Not ready / Emerging / Ready / Reference-grade). Report the radar shape, not a single averaged grade.

**5. Close with the three refinement closers.** A before/after refinement table; three fast A/B tests; a final go/no-go with confidence level (high / medium / low).

**Chaining.** The readiness profile, the resolved severity list, and the final colorways with contrast results carry into Spec. Standalone Critique with no Concept record must request its full input set before proceeding (F2): a brand-fit point-of-view statement, the anti-descriptors / do-not-do list, the competitive set, the intended colorways, and the source assets (vector preferred). For self-application, source the point-of-view and anti-descriptors from a canonical brand-intent file — a section of `heyhi-agent-context.md` or a dedicated brand-intent doc — not from this skill's worked example.

---

## Mode 3 — Spec

Purpose: production logo system specification, dual artifact.

**1. Write the human document.** Use the spec template in reference.md: the seven-section production skeleton plus a design-intent section and an explicit motion section (design intent, core marks, clear space and sizing, color rules, responsive and scale use, motion, file and export, misuse, implementation checklist).

**2. Split by the tokenization boundary.** Measurable rules become tokens and carry a pointer to their `logo`-namespace field. The reasoning (typology, metaphoric weight, mark-to-type relationship, the scale-degradation judgment) goes to the design-intent section, sourced from `ai-services/design-intelligence/design-intent-document-template.md` Section 1. Do not tokenize a judgment; do not leave a rule to prose. Record the typology and its strategic bet from `references/logo-typology.md` in the design-intent section (non-tokenizable). Fill `logo.scale_degradation` from the per-typology path in `references/scale-degradation-matrix.md`.

**3. Add what the source prompt omits.** Favicon and scale-degradation decision; motion behavior; dark-mode token pairing; contrast ratios as numbers; provenance and version metadata.

**4. Emit the machine companion.** Produce the `logo`-namespace JSON alongside the human spec, authored with `$description` fields per `heyhi-token-description-author`. The namespace is added to the brand-config schema through `heyhi-schema-extension-author`, with a numbered ADR filed in `ai-services/_core/architecture-decisions/` and a pointer entry in `ai-services/_core/decision-log.md` (see Phase 3 below). Check the structural-growth early-warning signals in `project-state.yaml` when adding a namespace.

**5. Align export structure.** Component variants and export specs per `ai-services/design-intelligence/figma-mcp-integration-plan.md`, not a generic file list.

**Chaining.** Spec must not introduce a colorway or size that Critique never evaluated. Standalone Spec with no Critique asks for the readiness sign-off, or runs an inline mini-critique gate first.

**Resolving a provisional field later (return path).** When a client decision later resolves a `provisional_fields` / "Open" item (the favicon mark, the leading option, the palette lock), the resolution is a propagation task, not a one-line edit. Propagate in one pass across: the machine JSON (set the value, remove it from `provisional_fields`, update dependent `scale_degradation` / `min_sizes` / gate language, bump the spec version), the human spec, the client guidelines, any in-artifact specimen (proposal/prototype mock plus its casing), and the dev-handoff / content-architecture references. Then grep the whole deliverable tree for the *old* term to prove nothing stale remains — this is what catches the refs you forgot. Distinguish "the mark is decided" (resolve everywhere) from "the export is still pending" (raster/print sizes stay pending). Source: `skill-updates/heyhi-logo-system/resolved-provisional-field-propagation-2026-06-12.md`.

---

## Chained-run artifact routing (R1)

When the modes chain (Concept → Critique → Spec), route the intermediate-mode artifacts to a `working/` scratch area for provenance, and make the final deliverable self-contained: embed the distilled upstream summaries (the recommended direction, the readiness profile, the contrast results) into the deliverable so it stands alone for the client-approval gate and downstream brand-book assembly, without depending on the scratch files. If an embedded summary and its scratch source later diverge, the deliverable's embedded copy is canonical at the approval gate; reconcile from `working/` only when the chain is re-opened.

---

## Schema, Validation, and Promotion (build-time, not per-run)

These steps apply when building or extending the skill itself, not on every client run.

- **Phase 3 — Schema + ADR.** Run `heyhi-schema-extension-author` for the `logo` namespace (`heyhi-skills/ui-studio/brand-config/schema.json` and the `active-brand.json` shape). File a numbered ADR in `ai-services/_core/architecture-decisions/` (matching the schema-decision precedent of ADR-004 / ADR-006 / ADR-007) and add a pointer entry to `ai-services/_core/decision-log.md` (append-only).
- **Phase 5 — Validate + register.** Run `heyhi-pipeline-validator` / `heyhi-session-validator` against a worked example. Add the registry entry to `ai-services/agentic-infrastructure/skill-registry.yaml`. Run the collision check against `heyhi-style-brief`, `heyhi-design-intelligence-audit`, and `heyhi-style-selection`.
- **Phase 6 — Promote.** Only after human review. Move from `skill-updates/` to `heyhi-skills/heyhi-logo-system/`, bump the deployed skill count and registry version, mark the CANDIDATES.md entry promoted.

---

## Skill Diary

This skill maintains a memory diary wing (through the `memory` shim): `heyhi-logo-system-diary`. It captures recurring critique patterns, mark typology decisions, and client mark characteristics that should persist across engagements.

**Read trigger:** at session start, before any logo task, query both wing name forms:

```
memory_search(query="[mark type, critique axis, or client characteristic]", wing="heyhi-logo-system-diary")
memory_search(query="[mark type, critique axis, or client characteristic]", wing="wing_heyhi-logo-system-diary")
```

An empty or absent `heyhi-logo-system-diary` wing is normal on the first run and must not block the work (F7).

**Write trigger:** at the end of any session where a correction is issued or a recurring pattern is noticed, draft an entry and stage it at `.auto-memory/diary-staging/heyhi-logo-system-[YYYY-MM-DD].md` for the instance owner's review. The agent drafts; the instance owner reviews.

**Worked example location (F6).** The worked example and the `heyhi-logo.json` companion live in `skill-updates/heyhi-logo-system/` by build-artifact convention. The skill IS formally promoted (Phase 6, 2026-06-02 — registry v2.20.0 / 39 deployed *at promotion time*; both figures have moved since, run `python skill-registry.py --stats` for current) — this is a discoverability pointer, not an incomplete promotion. Load them from there when a worked reference is needed; if they should ship beside the deployed skill, co-locate them on the next promotion.

---

## Exit Gate Required Headers (bottom-of-skill bracket)

This skill closes through the Exit Gate Flavor A (`CLAUDE-SESSION-RULES.md § Exit Gate`). Before declaring done, confirm every required header below contains real content, not a claim:

- `## Fixes Applied`
- `## Smoke Test`
- `## Next Session Prompt`

The facilitation dialogue of Concept and Critique is exempt until a document artifact is produced. Once any mode emits a document, the gate applies.

---

See [reference.md](reference.md) for:
- The identity-system convention and the fixed / adjustable / open parameter classes
- The tokenization split for marks
- The Concept Direction Record template
- The six-axis critique scoring methods
- The severity rubric with language examples
- The Logo Readiness Profile scale
- The spec template (nine sections: design intent, the seven-section skeleton, and motion)
- The `logo` namespace JSON shape
- The mode-chaining contract
- The output smoke tests

And the on-demand research-richness modules (pointer-linked, load per mode):
- `references/logo-typology.md`: the seven construction typologies (Concept, Spec)
- `references/render-brief-template.md`: the opt-in, provider-agnostic generation brief (Concept)
- `references/scale-degradation-matrix.md`: per-typology reduction paths for `logo.scale_degradation` (Spec, Critique)
- `references/mark-failure-modes.md`: the six-axis by typology failure catalog (Critique)

---

*HeyHi Confidential*
