---
classification: confidential
title: "Intent-Journey Map, method reference"
skill: intent-journey-map
version: "0.1.0"
---

# Intent-Journey Map, method reference

The method the SKILL.md routes to. It carries four things: the band spine, the tier gate, the 14-column prop-contract, and the adversarial over-claim checklist. The SKILL.md sets the tier and names the empty slots; this reference is the how.

This method is portable methodology. The stack bindings, the job-story library, and any domain band's real contents are engagement knowledge that the engagement supplies; nothing product-specific is baked in here.

---

## The band spine (fixed) plus one pluggable band

A feature is a set of journey steps in narrative order, each a column. The rows are bands. The spine is fixed across engagements; exactly one domain-state band is pluggable and lives in `domain-band-template.md`.

| Band | Name | Runs at | What each cell records |
|---|---|---|---|
| 1 | **Intent** | all tiers | The job story (When / I want / so I can) and the persona-and-surface note (which user, which surface, which viewport). |
| 2 | **Journey** | all tiers | The stage label, the one concrete user action (a single task-analysis leaf), and the emotion / friction / opportunity note. |
| D | **Domain-state** (pluggable) | Tier 2, when the domain needs it | The parts of the domain's state model that change at this step. One band per engagement; see `domain-band-template.md`. Skipped, and said to be skipped, when the feature carries no special domain state. |
| 3 | **System-and-data** | Tier 2 | The service or endpoint that fires when the action crosses the line of visibility; the entities and fields read or written; a frontstage / backstage marker. |
| 4 | **UI-and-component** | all tiers | The screen or component and its state (empty, loading, filled, success, error); the served-library component plus its atomic level, or `NEW:` a proposed name; the layer (container or presentational). |
| 5 | **Acceptance** | all tiers | Given / When / Then: the checkable pre-state, trigger, and post-state for the step. |

The prop-contract (below) is the machine companion to bands 3 and 4 at Tier 2. Bands 1, 2, 4, and 5 are the Tier 1 minimum. A feature is design-complete when every step has bands 1, 2, 4, and 5, and every data prop in the contract has a source and a schema field that is bound or explicitly flagged.

**What stays human across the bands.** The job framing behind band 1 (the research question), the severity of a band-2 friction and whether a band-2 opportunity is real (the theme-and-severity calls), and every open decision the map surfaces. The bands hold observations and candidates; the rulings are the human's, behind the named gate. The domain-state band is not one of these rulings: it is a pluggable slot the engagement supplies (which band, whose state model) and the run then fills mechanically from the grounded model, exactly like the other bands. What is the engagement's is the pluggability, not a withheld judgment.

---

## The tier gate

Run the tier check first (SKILL.md Step 1). The gate exists to keep most changes off this protocol: a copy tweak is Tier 0, a settings reflow is Tier 1, and the full spine plus the bound contract is Tier 2.

- **Tier 0** skips the protocol entirely.
- **Tier 1** runs bands 1, 2, 4, 5. No domain band, no system band, no prop-contract, no adversarial pass, unless a single load-bearing decision needs one lane of a higher tier (add just that lane, and say why).
- **Tier 2** runs every band, builds the prop-contract, and runs the adversarial pass.

**Precedence (binding).** A change that writes data, changes auth or entitlement, or crosses an architecture boundary is Tier 2 no matter how few controls it touches. Control count never demotes such a change. When the precedence rule does not settle a borderline case, the tier is an open decision for the human, not a silent pick.

**Calibration hook.** After three uses, check the gate: did Tier 0 and Tier 1 changes stay light, or did everything land at Tier 2? If everything is Tier 2, the tiers are miscalibrated. If a band is empty on most features, it may belong in a higher tier rather than the default run.

---

## The prop-contract (14 columns, one row per data prop)

The machine half of the map, emitted as `[feature]-ijm-contract.json` and validated against `schemas/ijm-contract.schema.json`. One object per data prop. The enforceable core is the binding (columns 7 through 11 in the table below): a codegen or contract test rejects a prop that references an absent field, and a contract test fails when the provider changes the field under it.

| # | Column | Field | Source of the value |
|---|---|---|---|
| 1 | Step or job | `step` | The map step this prop serves. |
| 2 | Screen state | `screen_state` | The Given/When/Then label: loading, empty, filled, success, error. From band 5. |
| 3 | Component | `component` | Served-library name plus atomic level, or `NEW: name`. From band 4. |
| 4 | Layer | `layer` | container or presentational. From band 4. |
| 5 | Prop | `prop` | The prop name. |
| 6 | Prop role | `prop_role` | data, presentation (a design-token value), or behavior (a callback). |
| 7 | Type | `type` | The type, bound to an OpenAPI component-schema slice when the binding resolves. |
| 8 | Source | `source` | `{hook, endpoint}`: the data hook and endpoint; both null for presentation or behavior props. |
| 9 | Schema field | `json_pointer` + `binding_status` | JSON pointer into the application's OpenAPI. Resolves → `bound`. Absent → `flagged-absent`. No owned spec → `no-spec` (bound to a typed module or external endpoint instead). Human-asserted, unsupported → `assumption`. |
| 10 | Required? | `required` | From the schema `required` array (null when unbound). |
| 11 | Enum values | `enum` | From the schema enum; asserts equality with the token or variant set when the prop drives one. |
| 12 | Default or token | `default_or_token` | The fallback literal, or the design-token role. |
| 13 | Empty or error state | `empty_or_error_state` | What renders on null, missing, or failed. From band 5. |
| 14 | Proof ref | `proof_ref` | The story id or the test assertion that proves the binding (null until it exists). |

Columns 2 and 13 come from band 5. Columns 6 and 12 come from the token-versus-headless split. Columns 8 and 9 anchor the row to the API as the single source of truth. Column 9's `binding_status` is the honesty field: it is never `bound` unless the pointer actually resolved.

**Bind, do not guess (the rule this contract exists for).** Resolve every `json_pointer` against the supplied OpenAPI. A pointer that resolves carries the schema's real `required`, `enum`, and type across. A pointer that does not resolve is `flagged-absent` and surfaced as a finding; it is never silently kept and never filled with an invented shape. Where the application carries no OpenAPI, bind each data prop to its real source (a typed data module by file and symbol, or a named external endpoint) and set `no-spec`; record honestly that no owned contract exists. A field a human asserts that the sources do not support is `assumption`, labeled so.

---

## The adversarial over-claim pass (Tier 2, mandatory)

Before the map is final, one adversarial reading checks the map and the contract against the manifest and the OpenAPI. It is a hunt for over-claim: anything asserted as real that the sources do not support. It does not judge whether the feature is worth building.

Checklist (each item is corrected to the source or re-labeled `unverified` / `assumption`, never left as a bare claim):

1. **Every endpoint** named in band 3 or the contract's `source` resolves in the manifest or the OpenAPI. An endpoint from memory is `unverified`.
2. **Every schema field** with `binding_status: bound` actually resolves at its `json_pointer`. Re-resolve each; a stale pointer is re-flagged.
3. **Every component** named in band 4 is a served-library component (via `retrieve_design_context`) or is explicitly `NEW:`. A component named from memory is `unverified`.
4. **Every capability** implied (a write, a role gate, an offline path) traces to the manifest's `capabilities`. An implied capability with no manifest support is `assumption`.
5. **Every enum equality** claim (a prop enum equals a token or variant set) is checked against both sides. A divergence is a finding, not a silent match.
6. **No screen state** claims to be shown that the brief or the manifest does not evidence; an inferred state is labeled inferred, never presented as drawn.

An over-claim found here is corrected in place. The pass produces a short note (what was checked, what was corrected) that ships with the map. If the pass finds nothing, it says so; a pass that never finds anything across several features is a signal the binding is too shallow.

---

## Reuses (owned elsewhere; not restated here)

- **Ground truth from code:** the `app-recon` skill and the served `app-manifest.json` fill bands 3 and 4 and the component names. This skill consumes the manifest; it does not re-read the codebase.
- **The served design system:** component names, atomic levels, and token roles come through the per-system instance (`retrieve_design_context`, `retrieve_design_relationships`), never a disk file.
- **The application context:** the manifest, and any prior intent map, come through `retrieve_application_context` when the instance serves them.

---

*HeyHi Confidential. `intent-journey-map` method reference v0.1.0. Portable methodology; every stack binding, job-story library, and domain-band fill is engagement knowledge supplied at run time.*
