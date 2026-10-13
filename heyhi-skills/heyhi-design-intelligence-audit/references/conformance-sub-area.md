---
classification: confidential
promoted: 2026-08-17
status: active — deployed reference of heyhi-design-intelligence-audit (Area 7 conformance sub-area)
target_skill: heyhi-design-intelligence-audit
homes_into: "Area 7 (Agent Interface Readiness) — as a conformance sub-area"
source_plan: plans/plan-design-md-build-2026-08-06.md  # § Phase 2 (2.1–2.5, Gate G2) + § Increment A
dispatch: dispatch/dispatch-prompts-2026-08-15-design-arc-wave-builds.md  # DISPATCH-C
gate: G2
reuses:
  - heyhi-mcp validate_output (the 9-rule mechanical floor, instance-keyed via its constraints param — reused, not reimplemented)
  - ai-services/design-intelligence/design-fundamentals.md (the A.1/A.2/A.3 fundamentals axis — DISPATCH-A)
  - ai-services/design-intelligence/visual-anti-tells.md (HeyHi's instance anti-tell list, AT-1…AT-10 + carve-outs — one instance's list, not the universal set)
  - ai-services/design-intelligence/style-reference-library.md (taste_profile / not_a_departure_if)
---

# Area 7 — DESIGN.md Conformance (a conformance sub-area)

*Deployed reference for `heyhi-design-intelligence-audit` (Area 7 conformance sub-area). The SKILL.md Step 3 Area 7 block carries the operative summary; this is the full rubric it points to. Calibration evidence and the Gate G2 result live in the instance's calibration record, `conformance-calibration.md` (instance-only; not shipped with the scaffold).*

**Retained IP — Confidential, not for publish.** The conformance-audit *method* is the moat three independent 2026 sources name (see the plan). The publish path is Phase 4 and gated on counsel; this capability is internal.

---

## What this is, and where it homes

The four existing Area 7 sub-areas ask a readiness question: **is the *system* ready to serve as a constraint surface for agent-generated UI?** (7.1 token depth, 7.2 catalog structure, 7.3 HITL coverage, 7.4 Layer 0 signal.) They score the system 1–4 and compose the ARI.

This sub-area asks the closing question: **did a *generated output* actually honor the system it was generated against?** It reads a rendered generation and returns a **conformance verdict** — the loop that 7.1–7.4 open, closed.

**It is a capability sub-area, not a fifth ARI axis.** The ARI composite stays the 7.1–7.4 average; this sub-area's verdict is separate and does not fold into that score. This is the same discipline the 7.2 adopted-third-party diagnostic used ("does not add a sub-area, ARI formula unchanged") — a capability can extend Area 7 without disturbing the readiness index.

**Distinct from the 7.2 adopted-third-party-view gap.** Sub-area 7.2's diagnostic names a gap nobody has built a checker for: do *adopted third-party MCP-App views* honor a *host's* `hostContext.styles.variables`? That stays an honest, unbuilt gap; do not imply HeyHi ships a checker for it. This sub-area is a *different target* — a generation (HeyHi's own, or an agent's, against a known DESIGN.md) versus *its own governing DESIGN.md*. Building this one does not contradict 7.2's framing; keep the two questions separate in any report.

**When it runs.**
- **Audit-time (demonstration).** In an audit or Care engagement, run it on one generation produced against the client's own system to make the readiness score concrete: "here is what an agent generated against your system, and here is exactly how far it honored it."
- **Generation-time (the loop).** As the optional thin companion the plan names — the check an agent runs on its own output before returning it. Same rubric, same four axes; the difference is only when it fires.

**Gate for this sub-area to run at all (G1 + G1B).** It audits *against* two surfaces, so both must exist: (a) an intent-rich DESIGN.md for the system under audit (HeyHi's is `ai-services/design-intelligence/DESIGN.md`; a client's is authored in the engagement), and (b) the `design-fundamentals` reference (`ai-services/design-intelligence/design-fundamentals.md`). If either is absent, the sub-area does not run — there is nothing to conform *to*.

The instance's DESIGN.md is also the source that keys the audit to the instance: the floor's token set and out-of-palette feature-styling declaration (Axis 1) and the anti-tell list (Axis 3) all read from it. The richer that DESIGN.md, the more of the audit reads the instance rather than HeyHi's defaults. Only Axis 4 (fundamentals) is brand-agnostic and runs the same on every system.

---

## 2.1 · The dual-checking rubric

Four axes. The first is automated and blocking; the other three are human-authored rubrics the agent executes with judgment. A finding on any judgment axis is a *flag*, never an automatic failure — the carve-out is where judgment lives (see the anti-tell and intent axes).

### Axis 1 — Functional floor (mechanical, automated, blocking)

Reuse the `heyhi-mcp` **`validate_output`** tool. Do **not** reimplement hex, scale, contrast, or state detection — the tool is deterministic, runs outside the model at no token cost, and is the single source of truth for the 9 rules. Read `valid`, `errors[].rule`, and `confidence_score`.

**Feed the declared structured output, not the compiled CSS.** The floor scores what the generation *declares* it used — the structured artifact a real HeyHi generation emits (per the pipeline's worked example): components with `states` and a `tokens_used` list. It does not parse rendered CSS. Resolved hex in a rendered page is the expected form of a token (a browser cannot resolve token names), so extracting compiled CSS and feeding it would false-fail every real page on Rule 1. For an HTML surface, read its declared token usage (or the emitted structured output), not its stylesheet.

**Mode: use `full_page` (or per-`component`) for a page.** `full_page` validates each component's own token pairs in context. Do **not** use a flat `artifact_type: "token_usage"` bag for a whole page: that mode pairs every text token against every background cartesian-style and false-fails a legitimate multi-surface palette on Rule 2 (contrast). Reserve `token_usage` for a single component's own already-legal pair set.

**Run the floor against the instance, not HeyHi (ledger H1a).** `validate_output` takes a `constraints` argument that keys the floor to the system under audit. Without it, Rule 1 checks tokens against HeyHi's own vocabulary — which false-fails every other client's output. Pass the instance's token set and legal-contrast-pair set:

```
constraints = {
  "known_tokens": [ ...the instance's token names... ],
  "legal_contrast_pairs": [ ["text-token", "bg-token"], ... ]
}
```

An injected `known_tokens` set is the tenant's whole vocabulary, so it also switches off HeyHi's dotted-DTCG resolver **and** clears HeyHi's legal contrast pairs — all three are HeyHi's own and must not govern another tenant. Pass `legal_contrast_pairs` alongside `known_tokens`; if you omit it, contrast degrades to unverified warnings (the safe direction) rather than being judged by HeyHi's pairs. The floor already accepts this injection; full per-client token ingestion from the instance's DESIGN.md is #643 P3-03. When the system under audit *is* HeyHi, omit `constraints` and the floor reads HeyHi's registry exactly as before.

**The out-of-palette-by-design escape (ledger H1b).** A data-driven instance paints features off the chrome palette on purpose — a data-visualization instance's attribute-driven colors are the worked case, where a naive floor false-flags all 13 as raw-hex Rule-1 violations. The floor honors an out-of-palette declaration read from the instance's DESIGN.md `## Colors` data-driven feature-styling section:

```
constraints["out_of_palette"] = {
  "feature_colors": [ "#2E7D32", ... ],   # the declared feature palette
  "allow_user_colors": false,             # true if the surface takes arbitrary user colors
  "chrome_context": false                 # true when auditing a chrome surface
}
```

A raw hex that traces to the declared feature palette (or is an explicit user color) is **not** a Rule-1 violation. An undeclared hardcoded hex still fails. Feature colors **must not appear on chrome**: audit a chrome surface with `chrome_context: true` and the escape switches off, so a feature color laundered onto the shell fails exactly as an undeclared hex would. Every color that is *not* data-conditional stays governed by the palette.

The 9 rules (`ai-services/design-intelligence/agent-summary.md` § Validation Rules; implemented in `heyhi-mcp/heyhi_mcp/core/validator.py`):

| # | Rule | Catches |
|---|------|---------|
| 1 | Token compliance | raw hex, arbitrary px outside the scale, off-system token names |
| 2 | Contrast | text/bg pairs below WCAG AA 4.5:1 (checked against the legal-pair registry) |
| 3 | Touch target | interactive elements under 44×44px |
| 4 | Label coverage | form inputs without a matching visible `<label>` |
| 5 | Focus state | interactive elements with no visible, non-color-only focus indicator |
| 6 | Variant legality | prop values not in the component schema |
| 7 | Component scope | improvised component types outside the catalog |
| 8 | Copy constraints | standalone acronym for artificial intelligence; more than 2 em dashes per artifact |
| 9 | Output format | non-structured output |

**This axis blocks.** A functional-floor failure is a fail regardless of how the output looks — it is the top of the A.1 severity order (Accessibility → Interaction → Visual → Brand → Code). A gorgeous page that fails contrast has not conformed.

**Boundary — the floor covers what it covers.** `validate_output` checks *focus* (Rule 5) and *label* (Rule 4) but has **no rule for the full control-state contract**. A component that carries a focus state passes Rule 5 while still missing `active` / `loading` / `error`. That gap is caught by Axis 4, not here. Do not read a clean `validate_output` as "states complete."

### Axis 2 — Intent adherence (judgment)

Does the output honor the DESIGN.md's **intent**, not just its tokens? Read the system's intent-rich DESIGN.md — its `## Intent`, `## Composition`, and the functional-first order (Accessibility → Interaction → Visual → Brand) — and ask:

- **The reference.** Does the output feel like what the DESIGN.md says it should feel like? (For HeyHi: "a studio's own working surface, not a storefront" — warm paper, near-black ink, one confident type moment, energy in one accent, not in effects.)
- **The composition.** Does it use the system's documented layout patterns, or a generic template the DESIGN.md's `## Composition` does not sanction?
- **Right component for the intent.** Was the component chosen the one the intent calls for, or a default? (A `link` where the intent wants a primary `Button`; a data table where a reader wants prose.)
- **The taste boundary.** This is where `taste_profile` / `not_a_departure_if` (`style-reference-library.md`) applies as an audit. The discrimination is **restraint versus incoherence**: an intentional, documented departure that satisfies its `not_a_departure_if` condition is a *considered departure*, not a finding. An undocumented one with no coherence test behind it is drift.

### Axis 3 — Anti-tell scan (judgment, carve-out-gated, instance-keyed)

Scan the rendered output against **the instance's own anti-tell list**, read from its DESIGN.md and cited **by ID**. The list is instance-keyed: each system declares the generated-design tells it departs from, along with its own carve-outs, because a tell for one house is a signature for another. There is no universal catalog this axis applies to everyone; the axis reads the instance.

- **The instance's DESIGN.md is the source.** Read the system's declared anti-tell list and cite its IDs, never a copy-pasted description. The instance's list is the single source, and its carve-outs move.
- **HeyHi is one instance, not the universal set (ledger H4).** HeyHi's anti-tell list is the catalog in `visual-anti-tells.md` (AT-1 … AT-10 plus the house carve-outs). It is *HeyHi's* list. When the system under audit is HeyHi, that catalog is the instance list. For any other client, that client's DESIGN.md carries the list, and `visual-anti-tells.md` is a reference example of the shape, not a rule to apply to their system.
- **A different instance declares different tells.** A data-visualization product's departures are its own: chrome competing with the map, padding chosen over density, feature color crossing into chrome, drift hexes, sunlight-blind contrast. None of those map onto AT-1 … AT-10, and none of HeyHi's tells govern that instance. The mechanism is shared; the list is the instance's.
- **No declared list, no instance findings.** If the instance's DESIGN.md carries no anti-tell list, Axis 3 does not fire on instance-specific tells; it degrades to silence, never to HeyHi's tells applied to someone else's system. The brand-agnostic build tells still live in Axis 4 (fundamentals).

**HeyHi's instance anti-tell list** is the worked example below; the source is `visual-anti-tells.md`, cited by ID.

| ID | Tell |
|----|------|
| AT-1 | Neon / outer-glow shadows |
| AT-2 | Gradient text on large headers |
| AT-3 | Oversaturated accents (>80% saturation, non-electric, undocumented) |
| AT-4 | Three-equal-column card rows (unconsidered, repeated, equal-everything) |
| AT-5 | Overlapping elements (decorative collision) |
| AT-6 | Custom cursors |
| AT-7 | Fabricated metrics / fake "system data" |
| AT-8 | Broken image links |
| AT-9 | Filler prompt copy |
| AT-10 | Generic placeholder names |

**The carve-out is the judgment boundary, and it is load-bearing.** A pattern match is a finding only when no carve-out applies. Every entry in an instance's list names the condition under which the pattern is a *deliberate house choice*. For the reference instance, the house carve-out is stated once in the catalog and is the reason this axis does **not** fire on that instance's own signatures. The two shapes it covers:

- **A documented electric accent.** A signature accent near 100% HSL saturation (and a supporting accent near it) sits *above the AT-3 ceiling by design*, is documented in the instance's brand config, and carries passing WCAG results at the sizes it is used. **Any saturation rule that flags it is mis-scoped — the rule is wrong, not the brand.**
- **A documented serif body.** A serif reading face under a geometric display face inverts the classical serif-headline order on purpose and is a documented signature, not a tell.

Firing on either of these is a false positive, and preventing it is Gate G2's whole point. The same discipline applies to every instance: judge each declared tell against that instance's own carve-outs, never against another instance's.

### Axis 4 — Fundamentals adherence (brand-agnostic, from DISPATCH-A)

Does the output honor the universal build constraints in `design-fundamentals.md`? This axis is **brand-agnostic** — it applies on any client's system, so the audit sharpens even where the brand intent is thin. Reference the axis; do not re-author it (it lives in `design-fundamentals.md`).

- **The control-state contract (A.3).** Does every interactive element ship its full state set — `default / hover / focus-visible / active / disabled / loading / error` (+ `success` / `selected` where the function calls for them)? This is the additive check the functional floor structurally cannot make: a component that passes `validate_output` at confidence 1.0 can still be missing `active`, `loading`, and `error`. Missing `loading` on an async submit permits a double-submit; missing `error` denies a machine-readable failure signal.
- **The binding UX laws (A.2).** The Tier-1 ten as checkable constraints — one primary action per view (Von Restorff), option count capped and grouped (Hick's + Gestalt), recognition over recall, chunking, visibility-of-status. Flag a law that the output violates.
- **The A.1 hierarchy.** When a finding on this axis collides with a stated brand rule, resolve per A.1 rule 4 (brand-and-flag) and grade the flag by the severity order — an interaction or visual failure ranks above a brand-convention departure.

---

## 2.2 · Home and integration

**Home:** a conformance sub-area of **Area 7 (Agent Interface Readiness)**, so it rides the existing audit funnel and the Design System Care / Agent-Readable Design Systems service lines. It runs only when `agent_readiness_add_on: true` (the Area 7 flag) *and* a generation plus its DESIGN.md are in hand.

**ARI composite:** unchanged. The conformance verdict is reported alongside the 7.1–7.4 ARI table, not inside it.

**Optional generation-time companion.** The same rubric can run as the check an agent applies to its own output before returning it (the "loop"). If the instance owner wants that as a thin standalone skill later, it reuses this rubric verbatim; nothing here needs to change to support it.

---

## 2.3 · The visual feedback loop

The judgment axes (2 and 3) need the *rendered* output, not the source. Specificity is what makes the critique worth anything — "headline too large for the reference," not "typography could be improved."

**Procedure:**

1. **Render.** Open the generation in the browser-preview tooling (`mcp__Claude_Browser__navigate` to the file or a preview URL; `preview_start` for a dev server).
2. **Screenshot.** Capture the rendered surface (`mcp__Claude_Browser__computer` `screenshot`); scroll and capture the interaction-state surfaces (forms, buttons, empty/loading/error views) so Axis 4 has something to read.
3. **Critique against the DESIGN.md intent, specifically.** Name the element, the observed value, and the reference it violates or honors. Examples of the register:
   - "The hero headline is a three-stop purple-to-blue gradient — AT-2, and it contradicts the DESIGN.md's 'solid display in near-black ink, energy in one accent.'"
   - "Three equal feature cards, equal everything — AT-4; the DESIGN.md's `## Composition` calls for editorial, asymmetric layouts."
   - "The primary button ships only a default state — the A.3 contract's `active`/`loading`/`error` are absent, so an async submit can double-fire."
4. **Verdict.** Per-axis, then overall (see 2.4).

Record which surfaces were captured. A conformance verdict rendered from the hero alone, with the interaction states never screenshotted, is a partial audit and says so.

---

## 2.4 · The conformance report

Shaped like the DI Audit report (`reference.md` § Audit Report Template) so it plugs into audit and Care engagements: a short diagnosis first, then per-axis findings, then the verdict.

> **[System] — DESIGN.md Conformance**
> *HeyHi · [Month Year]*

**The short version.** *3–5 sentences: does this generation honor its DESIGN.md, and what is the one thing that most decides the verdict.*

**Conformance verdict**

| Axis | Verdict | Notes |
|------|---------|-------|
| Functional floor (blocking) | PASS / **FAIL** | `validate_output` result; cite the failing rule numbers. A FAIL here caps the overall verdict at FAIL regardless of the other axes. |
| Intent adherence | PASS / FLAG | findings vs. the reference, composition, right-component-for-intent, and the taste boundary |
| Anti-tell scan | PASS / FLAG | the instance's tell IDs, each with the carve-out judgment (fired / carved-out and why) |
| Fundamentals adherence | PASS / FLAG | A.3 control-state contract, A.2 binding laws, A.1 hierarchy |
| **Overall** | **CONFORMS / DRIFTS** | + a confidence read; DRIFTS if the floor fails or the judgment axes carry material, non-carved-out findings |

Then, per axis with a finding, the DI Audit finding shape:

- **What we found:** [the specific element, observed value, and the reference it violates — plain language]
- **Severity:** Critical / High / Medium / Low, graded by the A.1 severity order (Accessibility → Interaction → Visual → Brand → Code)
- **Why it matters:** [the concrete cost — a double-submit, an unreadable contrast, an off-brand first impression]
- **Next step:** [one concrete fix]

**Grading rule (A.1 severity order).** Accessibility and interaction failures (floor, control-state completeness) outrank visual and brand-convention departures. A brand choice that forces a functional failure is a high-priority flag; a brand choice that only departs from convention with no functional cost is not a defect and is not flagged (A.1 rule 4).

---

## What is reused, not rebuilt

| Need | Reused from | Do not |
|------|-------------|--------|
| Mechanical floor (9 rules) | `heyhi-mcp` `validate_output` (instance-keyed via `constraints`) | reimplement hex/scale/contrast/focus detection, or run HeyHi's token set against another client |
| Fundamentals axis (A.1/A.2/A.3) | `ai-services/design-intelligence/design-fundamentals.md` | re-author the hierarchy, laws, or state contract |
| Anti-tell list (instance-keyed) | the instance's DESIGN.md; `visual-anti-tells.md` is HeyHi's own list (cite by ID) | treat HeyHi's AT-1…AT-10 as universal, or copy-paste descriptions that drift from the source |
| Taste / false-positive gate | `ai-services/design-intelligence/style-reference-library.md` (`not_a_departure_if`) | invent a coherence test the library does not carry |
| Intent surface | the system's intent-rich DESIGN.md | audit against a token-only DESIGN.md (nothing to conform to) |

---

## Increment record — instance-aware floor + anti-tell axis (folded 2026-08-17)

A second-instance flexibility run (the instance's flexibility ledger) found the conformance capability was single-tenant: it assumed HeyHi. Three of its filed harness changes are folded into this reference, all making the capability read the *instance* instead.

| Ledger row | Fix | Where |
|---|---|---|
| **H1a** | `validate_output` accepts an injected instance token set + legal-pair set via its `constraints` param (it no longer hardwires HeyHi's `KNOWN_TOKENS`). | Axis 1 (this doc); `heyhi-mcp/heyhi_mcp/core/validator.py` `constraints={"known_tokens", "legal_contrast_pairs"}` |
| **H1b** | Out-of-palette-by-design escape: a raw hex declared in the DESIGN.md `## Colors` feature-styling section is not a Rule-1 violation, and must not appear on chrome. | Axis 1 (this doc); `validator.py` `constraints["out_of_palette"]` |
| **H4** | Axis 3 reads the instance's DESIGN.md anti-tell list; HeyHi's `visual-anti-tells.md` becomes HeyHi's instance list, not the universal catalog. | Axis 3 (this doc) |

**Scope of the code layer.** `validate_output` now *accepts* the injection; full per-client token ingestion from the instance's DESIGN.md is #643 P3-03 (unbuilt). Tests: `heyhi-mcp/tests/test_instance_aware.py`. With no `constraints`, the floor is byte-identical to the pre-injection HeyHi floor (the whole `test_stream_c.py` set still passes).

**Flexibility roadmap — updated 2026-08-17.** Two of the three items open at this increment have since landed: the one intake-location rule (H6) in #658, and the instance-keyed taste store (H7) as the spec-layer keying in [`layer-0-evaluation-specs.md` § Instance-keyed taste store](../../../ai-services/design-intelligence/layer-0-evaluation-specs.md#instance-keyed-taste-store-flexibility-ledger-h7) (the taste-review gate reads the instance's `taste_profile`, with `style-reference-library.md` as HeyHi's own instance store). **Still open:** the per-client served DESIGN.md (ledger H5), gated on the #643 Phase-2 image-per-client serving.

---

*HeyHi Confidential.*
