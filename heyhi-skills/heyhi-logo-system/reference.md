---
title: "heyhi-logo-system — Reference"
classification: HeyHi Confidential
version: "0.3.0"
updated: "2026-06-10"
---

# heyhi-logo-system: Reference

**HeyHi Confidential**

*Companion to `SKILL.md`. Pull this when running any of the three modes. SKILL.md orchestrates; this file holds the rubrics, templates, and the JSON shape the work produces. Detail lives here so the procedure stays readable.*

This skill is part of the **Identity System** family within Design Intelligence (photography, logo, and later motion and iconography). The family convention: a human-readable narrative artifact plus a tool-agnostic machine artifact, a generation step that stays opt-in for the parts that are HeyHi judgment, and a review step. The structural twin is the `heyhi-photography-style` candidate; its conventions are extracted into this file rather than inherited from a deployed skill.

---

## The Identity-System Convention (shared family shape)

Every Identity System deliverable separates three parameter classes. A logo brief, like the photography brief it is modeled on, names which is which so a future reader does not re-litigate a settled decision or freeze a deliberately open one.

| Parameter class | What it means for a logo system | Where it lives |
|---|---|---|
| **Fixed** | Holds across every adaptation of this identity. Changing it changes the brand. (e.g., "wordmark-led, never a standalone symbol.") | Design-intent section + `logo.meta` |
| **Adjustable** | Derived from the brand, varies per engagement. (e.g., clear-space ratio, colorway set, minimum sizes.) | `logo` namespace token fields |
| **Open** | Requires a named decision that has not been made. (e.g., an unresolved favicon reduction.) | Flagged in `meta.provisional_fields` and named in the human spec |

The dual artifact in every mode:

- **Layer 1 — human document.** What a client or a new designer reads. Concept directions, a critique narrative, or a spec with its reasoning. Passes `heyhi-voice`.
- **Layer 2 — machine companion.** The `logo`-namespace JSON. What the Figma pipeline and downstream agents consume. Authored with `$description` fields per the `heyhi-token-description-author` philosophy.

The upstream question (carried from the photography brief's "what the photograph needs to communicate"): **before any direction is generated, name what the mark must communicate and what it must never be mistaken for.** That answer is non-tokenizable and governs everything downstream.

---

## Rendering and Verification (NEW-1, NEW-2 — v0.2.0)

This section is the heart of the v0.2.0 change. It applies whenever a mark is actually rendered, in any mode — Concept's opt-in render step, a Critique that renders to score, or a Spec proof.

**Render and look before you score or present (NEW-1).** Whenever a mark is rendered — image generation, SVG, or Figma — render it to a viewable image and inspect it before scoring or presenting. Generating geometry "by spec" without looking is the defect: in the 2026-06-04 stress test the first two render rounds were sloppy precisely because the output was never viewed. Iterate against the rendered result, not against the code. The loop is: render → view → judge against your own eyes → iterate → only then present.

**Render on the real brand typeface (NEW-2).** When rendering brand type for verification, load the actual brand display or body font — for self-application, the instance's own display, body, and utility faces as named in its brand config — via an npm font package plus a rasterizer (e.g., fontkit + resvg). Never judge weight, fit, or legibility on a stand-in geometric face; doing so produced "unfinished"-looking marks in the stress test. This is required for self-application and for any brand with a known display token. Fallback when the brand font is not open-licensed or package-available: render on the nearest licensed match in the same classification and state explicitly that the face is a proxy, so weight and fit are not certified.

**Motion that cannot be previewed live (NEW-1b).** For motion that cannot be previewed (CSS/JS animation, scroll-driven behavior), render the key beats — rest → mid → overshoot → settle — as a single still filmstrip to verify the choreography and to show the user. State that timing and easing cannot be felt from stills; a four-frame strip can misrepresent a spring, so name what the proxy does and does not show.

**Proxies for media that resist a static render.** Live animation, 3D, scroll-driven, and video each need a faithful proxy: a keyframe filmstrip for motion, near-target-size screenshots for scale, a turntable or fixed set of views for 3D. Choose the proxy that least misrepresents the medium and say what it omits.

---

## The Tokenization Split for Marks

This is the spine of Spec mode and the reason the output is two artifacts, not one. Source: `ai-services/design-intelligence/research/tokenization-boundary.md` Element 1. Rules and measurable values become tokens; the reasoning becomes design-intent prose. (All research-dependency paths are resolved from the project root; the full resolved-path table is in `SKILL.md` § "Research dependencies.")

| Mark attribute | Category | Artifact |
|---|---|---|
| Mark file (SVG path data) | Fully tokenizable | `logo.marks` asset ref |
| Mark color (fill value) | Fully tokenizable | `logo.colorways` |
| Minimum size (px threshold) | Fully tokenizable | `logo.min_sizes` |
| Clear space (ratio to mark width) | Fully tokenizable | `logo.clearspace` |
| Mark typology choice (wordmark / abstract / combination) | Non-tokenizable | Design-intent prose |
| Metaphoric weight of the form | Non-tokenizable | Design-intent prose |
| Scale degradation (when and how the mark simplifies) | Partially tokenizable | Threshold in `logo.scale_degradation`; the judgment in prose |
| Mark-to-type relationship in a lockup | Non-tokenizable | Design-intent prose |
| Dynamic identity transformation rules | Non-tokenizable | Design-intent prose |

**The rule:** if a machine can verify it is applied correctly, it is a token. If verifying it requires taste, it is design intent. A spec that tokenizes "why a wordmark" has made a category error; a spec that leaves clear-space to prose has under-specified the build.

---

## Concept Direction Record (Concept mode output, per direction)

The default Concept output specifies directions in words and structured attributes. Rendering candidate marks (image generation or Figma) is an opt-in step the operator invokes explicitly; it is never the default, because mark direction is HeyHi judgment under the don't-automate-this line. (Instance-owner sign-off, 2026-05-29.)

Each direction carries:

- **Concept name** — a memorable handle, not a description.
- **Strategic idea** — the bet this direction makes about the brand. One sentence a competitor could not have written about a different brand.
- **Symbol direction** — shape, motif, or metaphor. For wordmark-led directions, the letterform treatment.
- **Wordmark style** — typographic character and the reason.
- **Composition variants** — horizontal, stacked, icon-only. Which leads.
- **Color direction** — the role color plays; whether the direction reads in one color.
- **Cluster alignment** — one or more clusters from `ai-services/design-intelligence/style-reference-library.md`. Moodboard language pulled from `ai-services/design-intelligence/style-descriptor-vocabulary.md`, not invented.
- **Tokenization preview** — how cleanly this direction will translate to a token system. Forward-compatibility signal for a later Build engagement.
- **Risks and misreads** — grounded in the semiotics and Gestalt material in `ai-services/design-intelligence/research/visual-language-theory.md`. What could this be mistaken for; where does the metaphor over-reach.
- **Best-fit use cases** — where this direction is strongest.

Close Concept with: **one recommended direction and the reasoning**, the moodboard keyword set (sourced from the vocabulary), and a **do-not-do list** (anti-descriptors surfaced during interrogation, per `ai-services/design-intelligence/research/designer-questioning-methodology.md`).

Number of directions is configurable; default is 3.

---

## Six-Axis Critique Scoring (Critique mode)

The six axes from the source prompt, each operationalized so the score is defensible rather than asserted. Score every axis on the readiness scale below; the radar across all six is the **Logo Readiness Profile**, which replaces a single go/no-go grade (mirroring the audit skill's radar-over-grade approach).

| Axis | What it measures | How it is operationalized |
|---|---|---|
| **Brand fit** | Does the mark express the brand's point of view? | Checked against the design-intent point-of-view statement (or the engagement's brand config). Performed vs. present test from `ai-services/design-intelligence/research/tokenization-boundary.md`. |
| **Distinctiveness** | Could this be mistaken for a competitor? | Compared against the named competitive set and the do-not-do list. |
| **Legibility** | Does it read at the sizes it must work at? | The **16px test** from `ai-services/design-intelligence/gate0-facilitation-guide.md`: render the mark at 16×16px. For a wordmark, which letters survive. For a symbol, is it recognizable. |
| **Scalability** | Does the mark have a defined reduction path? | Scale-degradation logic from `ai-services/design-intelligence/design-intent-document-template.md` Section 1: is there a stated threshold and a reduced form, or does it just shrink until it fails. |
| **System readiness** | Will this translate to a token system and a component set? | Tokenization preview maturity; export structure aligned to `ai-services/design-intelligence/figma-mcp-integration-plan.md`. |
| **Risk of misinterpretation** | What unintended reading does the form carry? | Semiotics and Gestalt grounding from `ai-services/design-intelligence/research/visual-language-theory.md`. Cultural and contextual misreads named, not hand-waved. |

**Raster-input fidelity rule (F5).** The 16px test (Legibility) and the scale-degradation check (Scalability) assume vector input. When only a raster is available — a FigJam screenshot, a flattened PNG — both axes are estimates: render-at-size shows blur and resampling artifacts, not the letterform's true behavior. In that case, mark Legibility and Scalability **"estimated (raster)"** and lower the go/no-go confidence by one level. Prefer pulling vectors via the Figma MCP from a `/design/` file (a FigJam `/board/` does not expose letterform vectors), or render near-target sizes with `get_screenshot` at a small `maxDimension`. The skill does not certify Legibility above "estimated" until vectors are in hand.

**Projected vs. measured axes (R2).** When critiquing a concept that is specified but intentionally unrendered (rendering is a later human or gated step), mark the rendering-dependent axes (Legibility, Scalability) as **"projected from structure, not measured"**: score them from the typology's structure (the per-typology reduction path in `references/scale-degradation-matrix.md` is the projection), cap the go/no-go at medium confidence, and schedule a mandatory second critique — a render-and-verify pass at 16px and one color on the rendered artifact — before finalizing. Never let a projected score read as measured, and flag projected axes visibly in the Logo Readiness Profile so a reader never mistakes them for measured.

**Required contrast pass.** Run a real WCAG contrast check with numbers against each colorway, evaluated against the engagement's brand config (the client's `active-brand.json` when one exists; HeyHi's when the work is self-applied). State AA/AAA targets and the computed ratios. A colorway that fails its target is a finding, not a footnote.

**Critique closers (keep all three from the source prompt):**
1. A before/after refinement table — the issue, the proposed change, the expected effect.
2. Three fast A/B tests the team can run to resolve open questions cheaply.
3. A final go / no-go with a confidence level (high / medium / low), aligned with the Evaluation-Before-Deployment invariant.

---

## Severity Rubric (Critique findings)

Borrowed from `heyhi-design-intelligence-audit` and `heyhi-prototype-audit` and adapted to mark work. The source prompt asks for severity ranking but never defines it; this defines it.

### Critical
The mark fails at a job it must do, and shipping it does active harm. The failure is visible in use.
- "At 16px the wordmark collapses into an unreadable smear. The favicon and the app icon are both unusable; this is the primary digital surface."
- "The symbol reads as a near-duplicate of [competitor]'s mark. Adopting it invites confusion and a possible trademark conflict."
- "The only approved colorway computes 2.1:1 against its specified background. It fails WCAG AA and is illegible for low-vision users."

### High
Significant weakness that will compound or that blocks a major use. Not yet causing visible harm, but it will.
- "There is no reduction path. The mark is specified at one size and shrinks until it breaks; small-scale use is undefined."
- "Distinctiveness is thin. The form is competent but generic for the category; it will not be remembered or owned."
- "The lockup has no defined mark-to-type relationship, so every application will reinvent the spacing."

### Medium
A real problem, manageable now, that should be resolved before the system is built out.
- "Clear space is implied but not specified as a ratio, so it will drift across applications."
- "The dark-mode colorway exists but its contrast was never evaluated."
- "Motion behavior is undefined; the mark's first animated use will set an unreviewed precedent."

### Low
A best-practice gap worth addressing but not urgent.
- "Export structure is functional but not aligned to the component-variant convention, which will slow the Figma handoff."
- "The monochrome variant is present but its provenance metadata is incomplete."

---

## Logo Readiness Profile (the readiness-scale rubric)

Each of the six axes is scored on this named scale. The profile is a small maturity radar, not a single grade. (Modeled on the ARI level bands in `heyhi-design-intelligence-audit`.)

| Level | Name | Meaning |
|---|---|---|
| 1 | **Not ready** | The axis fails. The mark cannot do this job in its current form. |
| 2 | **Emerging** | Partial. The intent is visible but the execution or specification has gaps that block confident use. |
| 3 | **Ready** | The axis holds for the intended uses. Edge cases may need attention, but the mark works. |
| 4 | **Reference-grade** | The axis is a strength. The mark sets a standard others in the system can be measured against. |

**Profile reading:** a balanced profile near 3 across all axes is a ship-ready mark needing light polish. A spiked profile (4 on distinctiveness, 1 on legibility) is a mark with a strong idea and a specific, nameable problem. A flat profile near 1–2 is a direction that is not ready and needs to return to Concept. The shape tells the story; report it, do not average it into one number.

---

## Spec Template (Spec mode, Layer 1 human document)

The source prompt's seven-section production skeleton, plus a design-intent section (0) and an explicit motion section (5): nine sections in all. Each is split by the tokenization boundary. Measurable rules carry a pointer to their `logo`-namespace field; reasoning stays in prose. The favicon/scale-degradation decision, motion behavior, dark-mode pairing, contrast numbers, and provenance are required; the source prompt omits all five.

**0. Design intent (non-tokenizable).** Sourced from `ai-services/design-intelligence/design-intent-document-template.md` Section 1. Mark typology and the bet behind it; metaphoric weight; mark-to-type relationship; transformation rules; the scale-degradation judgment. This is what the config cannot hold.

**1. Core marks.** Primary, secondary, icon, and monochrome forms. Each with its asset reference. → `logo.marks`

**2. Clear space and sizing.** Clear-space formula (as a ratio to mark width). Minimum sizes for digital and print. → `logo.clearspace`, `logo.min_sizes`

**3. Color rules.** Approved colorways, each with its contrast result against the surfaces it is used on, AA/AAA target stated. Dark-mode pairing explicit. → `logo.colorways`

**4. Responsive and scale use.** The reduction path: thresholds and the reduced form at each. What "degraded but still recognizable" means for this mark. → `logo.scale_degradation`

**5. Motion behavior.** Entrance and state behavior. What the mark's motion never does (anti-descriptors). → `logo.motion`

**6. File and export.** Component-variant structure and export specs aligned to `ai-services/design-intelligence/figma-mcp-integration-plan.md`, not a generic file list.

**7. Misuse.** The do-not-do list, shown not just stated where possible.

**8. Implementation checklist.** What an engineer or a Figma operator confirms before the mark is considered deployed.

Close with provenance: who generated the spec, version, gate status, and any provisional fields, matching the `active-brand.json` meta pattern.

---

## The `logo` Namespace (Spec mode, Layer 2 machine companion)

Seven top-level fields (instance-owner sign-off, 2026-05-29). A new top-level namespace in the brand config, sibling to `tokens`, carrying asset references and provenance rather than pure token values. Full schema shape and the ADR are produced by `heyhi-schema-extension-author` (see SKILL.md Phase 3).

```json
{
  "logo": {
    "marks": {
      "primary":    { "asset": "path|ref", "format": "svg", "$description": "Primary lockup. Default for all standard uses above min size." },
      "secondary":  { "asset": "path|ref", "format": "svg", "$description": "Alternate composition (e.g., stacked) for constrained ratios." },
      "icon":       { "asset": "path|ref", "format": "svg", "$description": "Symbol or reduced form for square contexts." },
      "monochrome": { "asset": "path|ref", "format": "svg", "$description": "Single-color form for one-color reproduction and engraving." }
    },
    "clearspace": {
      "formula": "Nx",
      "basis": "cap-height|mark-width|x-height",
      "$description": "Minimum clear space as a multiple of the named basis. Applies to all marks unless overridden."
    },
    "min_sizes": {
      "digital_px": 0,
      "print_mm": 0,
      "$description": "Smallest size at which the primary mark may be used before switching to the reduced form."
    },
    "colorways": [
      {
        "name": "string",
        "mark_color": "#hex",
        "background": "#hex",
        "contrast_ratio": 0.0,
        "wcag_target": "AA|AAA",
        "wcag_result": "pass|fail",
        "scheme": "light|dark",
        "$description": "Approved mark-on-background pairing with its evaluated contrast result."
      }
    ],
    "scale_degradation": {
      "thresholds": [
        { "below_px": 0, "use_mark": "icon|monochrome|simplified", "$description": "Reduction step: at this size and below, switch to the named form." }
      ],
      "reduction_path": "string",
      "$description": "Ordered reduction path from full lockup to smallest recognizable form."
    },
    "motion": {
      "entrance": "string",
      "state": "string",
      "never": ["string"],
      "$description": "Entrance and state behavior; the never-list carries motion anti-descriptors."
    },
    "meta": {
      "generated_by": "heyhi-logo-system",
      "version": "0.x.y",
      "gate_status": "draft|reviewed|locked",
      "provisional_fields": [
        { "path": "logo.scale_degradation.thresholds[0]", "reason": "string", "confidence": "inferred|pending" }
      ],
      "$description": "Provenance and confidence, matching the active-brand.json meta convention."
    }
  }
}
```

`$description` authoring follows `heyhi-token-description-author`: describe purpose and usage constraint, not the value. "Primary lockup; default above min size" is a description; "an SVG" is not.

---

## Mode-Chaining Contract (carried artifacts)

When modes chain, each passes a defined artifact forward so a chained run is not three cold starts. Standalone runs declare the missing upstream input as a required question before proceeding (Earn the Room).

- **Concept → Critique.** The recommended direction's record (name, symbol/wordmark direction, composition variants, colorways, tokenization preview, do-not-do list) is the critique's input. Critique treats the recommendation as the proposed mark.
- **Critique → Spec.** The readiness profile, the severity-ranked issue list (each resolved to "addressed" or "accepted"), and the final colorways with their contrast results carry into Spec. Spec must not introduce a colorway or size that Critique never evaluated.
- **Standalone Critique** with no Concept record asks for its full input set before proceeding (F2): a brand-fit point-of-view statement, the anti-descriptors / do-not-do list, the competitive set, the intended colorways, and source assets (vector preferred). For self-application, source the point-of-view and anti-descriptors from a canonical brand-intent file (a section of `heyhi-agent-context.md` or a dedicated brand-intent doc), not from the worked example.
- **Comparative (Select) lane.** When several candidate marks arrive together with no Concept records — the common designer hand-off — Critique scores each candidate on the six axes and closes by recommending one, borrowing Concept's "recommend one + reasoning + do-not-do list" shape. Tie-break when two candidates share a readiness shape: decide on the highest-stakes axis for the engagement and name the tie-break used.
- **Standalone Spec** with no Critique asks for the readiness sign-off, or runs an inline mini-critique gate first.
- **Chained-run artifact routing (R1).** Intermediate-mode artifacts route to a `working/` scratch area for provenance; the final deliverable embeds the distilled upstream summaries (recommended direction, readiness profile, contrast results) so it stands alone for the client gate. The embedded copy is canonical at the approval gate. Full statement in `SKILL.md` § "Chained-run artifact routing."

---

## Output Smoke Tests (run before promotion)

- Concept produces N genuinely distinct directions, each mapped to a named cluster, with a do-not-do list.
- Critique returns a severity-ranked issue list and a Logo Readiness Profile across all six axes, with a confidence-rated go/no-go and a real contrast pass. When the input is N candidates, the comparative lane scores each and recommends one with a named tie-break.
- When a mark is rendered, it is rendered to a viewable image on the real brand typeface and inspected before scoring or presenting (NEW-1/NEW-2); raster-only input marks the Legibility/Scalability axes "estimated (raster)" (F5).
- Spec emits both a human document and valid `logo`-namespace JSON; the tokenization split is honored (no reasoning in tokens, no rules left to prose).
- Recompute-and-diff (R3): any value the spec or JSON hard-codes from a computation (contrast ratios, type-scale steps, spacing multiples) is recomputed from source and diffed against the stored value, not sanity-checked by eye. A stored number that matches a fresh recompute is verified; one that only looks plausible is not.
- No banned words; never "AI" as a standalone word; two or fewer em dashes per output document.
- Registry search routes the trigger phrases to `heyhi-logo-system` and not to `heyhi-style-brief`, `heyhi-design-intelligence-audit`, or `heyhi-style-selection`.

---

*Companion to `heyhi-logo-system/SKILL.md`. Cross-reference: `ai-services/design-intelligence/`, `ai-services/_core/decision-log.md` (logo namespace ADR).*

*HeyHi Confidential*
