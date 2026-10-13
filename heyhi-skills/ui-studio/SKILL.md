---
name: ui-studio
description: |
  Build web interfaces grounded in a real design system — not generic defaults. Three modes: Mode A (Brand-Compliant, production-ready), Mode B (Creative-Exploratory, marketing/editorial), Mode C (Futurecasting, speculative concept work). Use for any client design system work in any mode, and for HeyHi marketing/editorial/concept work when Mode B or C is needed. Reads active-brand.json for tokens; when the matched brand.style_entry has an authored taste_profile, also projects that entry's taste (aesthetic_principles, restraint_notes, exemplars) into the build as brand-specific steering via the taste_projection toggle (default on), with a generic-cluster fallback. Requires a brand config — run ui-studio-onboard to generate one. Triggers: "build a page for [client]", "create a prototype using their design system", "Mode A build", "Mode B marketing page", "Mode C concept", "futurecasting UI", "identity proposal", "build the stylescape", "render the visual direction for approval", or any design system-constrained interface build. Also renders the Identity Proposal — a constrained Mode B artifact-type that shows a decided visual direction (the rendered companion to a heyhi-style-brief prose brief) for client approval; see references/stylescape-patterns.md. NOT for HeyHi production pages (use heyhi-ui-ux). NOT for generic UI without a design system constraint. NOT for onboarding a new design system (use ui-studio-onboard). Route: client work of any mode → this skill + client config. HeyHi Mode B/C → this skill + heyhi.json active. HeyHi Mode A → heyhi-ui-ux.
version: "1.6.0"
---

# UI Studio

Build web interfaces grounded in a real design system — not generic defaults.

---

> **Exit Gate (Flavor A).** This skill closes through the canonical Exit Gate — see `CLAUDE-SESSION-RULES.md § Exit Gate`. Required headers, in order: `## Fixes Applied`, `## Smoke Test`, `## Next Session Prompt`. Empty headers are visible failures.


## ZONE 1 — Always Loaded

*The complete operating contract for every ui-studio session. ~7,600 tokens (Zone 1 trim pass pending — exceeds ≤2,200 target; see decision-log 2026-03-26).*

---

### Hard Stop: No Config

If `brand-config/active-brand.json` does not exist:

**Stop. Do not build.** Say exactly:

> "No brand config found. Run `ui-studio-onboard` to generate one, or activate an existing config with `python3 scripts/switch-brand.py --config [name]`. Build cannot proceed without a config."

> **Activating a *client* config without breaching the hermetic seal.** `brand-config/active-brand.json` is gitignored, so activation produces no tracked change; but a *named* client config in `brand-config/` (e.g. `acme.json`) is tracked, and both its filename and its `brand.name` leak the client. For client work, do not leave a client-named config in `brand-config/`: copy the reconciled config to a temporary, non-client-named file there (e.g. `_tmp-active.json`), run `python3 scripts/switch-brand.py --config _tmp-active --no-cursor`, then immediately `rm` it (never `git add` it). Confirm `git status --short brand-config/` is clean and no client-named file remains. The client config's canonical home stays in the instance's gitignored engagement folder (`<engagement folder>/working/`).

---

### Config Validation

On every session start, read `active-brand.json` and check in this order:

1. **Gate 0 — direction lock (G2):** If `meta.gate_status.direction_lock_confirmed` is `false` — **hard stop for Mode A.** Say exactly: *"Gate 0 not confirmed: direction_lock_confirmed is false. Mode A builds are blocked. Run ui-studio-onboard to confirm the style cluster and primary direction, then set gate_status.direction_lock_confirmed: true."* Mode B and C may proceed with a warning. If `gate_status` block is absent (pre-G2 config), surface a warning but do not hard stop.

2. **Designer review (G2):** If `meta.gate_status.designer_review_complete` is `false` — surface a warning for Mode A: *"Designer review not complete. Token values have not been verified against the source design file. Mode A output may not match the actual design."* Not a hard stop, but must be documented in any handoff.

3. **Version:** If `0.x.y` (provisional) — surface this warning once: *"Config is provisional (v[version]). Mode A output will be built on unconfirmed tokens. Run `ui-studio-onboard --refresh [config-name]` after the designer confirms values to promote to v1."* Then continue.

4. **`meta.last_refreshed`:** If > 30 days ago — surface a warning (not a blocker): *"Config was last refreshed [date]. Consider running a refresh if the design system has changed."*

5. **Dual-score mode unlock (G5):** Read both `meta.completeness_score` and `meta.fidelity_score` and apply this matrix:

| Completeness | Fidelity | Unlock level | Action |
|---|---|---|---|
| < 30 | any | HARD_STOP | Block all modes. Insufficient data for any meaningful build. Re-run onboarding. |
| 30–49 | any | PARTIAL_STOP | Block Mode A. Mode B and C are allowed, but must open with a capability-degradation notice listing which config blocks are missing and which capabilities are unavailable. Re-run onboarding to fill gaps before attempting Mode A. |
| 50–69 | any | MODE_B | Recommend Mode B. Mode A requires explicit user confirmation — see behavioral gate below. |
| ≥ 70 | < 60 | FIDELITY_WARN | Completeness passes; fidelity too low. Mode A blocked. Designer review needed. |
| ≥ 70 | ≥ 60 | PARTIAL_A | Mode A with documented approximations. Modes B and C unlocked. |
| ≥ 90 | ≥ 60 | FULL | Mode A, B, C fully unlocked. |

**SI-03 — Mode A override gate (50–69):** When completeness is in the 50–69 range and the user has selected or implied Mode A, do not proceed silently. Surface the score and ask:

> "Completeness score is [N]/100. Mode A at this score produces approximated output — token values are directional estimates that may not match the actual design. Would you like to proceed with Mode A (and document this as provisional output), or switch to Mode B?"

Only proceed with Mode A if the user explicitly confirms. On confirmation, set `gate_status.mode_override_acknowledged: true` and record the override score in `gate_status.mode_override_score`. If the user does not respond, default to Mode B.

**LF-02 — PARTIAL_STOP (30–49):** The hard stop at < 50 has been replaced by two thresholds. Scores 30–49 indicate a partially populated config — color and typography tokens may be complete even if layout, voice, and motion are not. Do not block Mode B/C for a 30–49 score; instead, list which capabilities are unavailable (e.g., "voice enforcement skipped — voice block missing") and proceed with available constraints. Score < 30 is an unconditional stop for all modes.

*Note: GATE_STOP (direction_lock_confirmed: false) takes precedence over all score-based checks — step 1 above.*

*Version promotion (`--promote`) is a separate gate from FULL unlock. It additionally requires: fidelity ≥ 80, direction_lock_confirmed: true, designer_review_complete: true, and no provisional fields remaining. A config can be FULL unlock but not yet promotion-eligible if fidelity is 60–79.*

6. **Scheme detection:** Read `meta.default_scheme`. Log the result before proceeding. `"dark"` → dark-native build — apply the Dark-Native Config Handling rules throughout the session. `"light"` or absent → light-baseline build — standard flow. This check is informational, not a gate; it sets the build foundation for all downstream steps.

**Capability unlock matrix** (what the config enables):

| Blocks present | Capabilities |
|---|---|
| `tokens` only | Token-driven build. No voice enforcement. |
| + `voice` | Copy enforcement added. |
| + `components` | Component inventory check + drift detection. |
| + `layout` | Layout Declaration with named patterns + spacing derivation. |
| + `ux_writing` | Per-slot copy patterns for all interface text. |
| All, v1.0.0+ | Full Mode A with developer handoff. |

---

### Three Modes

**Mode A — Brand-Compliant**
Production-ready. All design system rules enforced without exception.
- Components: existing library only
- Tokens: config only — no arbitrary values
- Layouts: named patterns from `config.layout.preferred_patterns`
- Copy: voice rules + `ux_writing` slots enforced
- WCAG AA: hard gate — delivery blocked until passing
- Requires: completeness_score ≥ 70 AND fidelity_score ≥ 60 (recommended: completeness ≥ 90 AND fidelity ≥ 80)
- Outputs: HTML/CSS prototype + developer handoff (includes Component Implementation Map when target framework is known) + `.cursor/rules/ui-studio.mdc`

**Mode B — Creative-Exploratory**
Pushes layouts while staying within the design system.
- Components: existing library — creative application permitted
- Tokens: config only — no extension
- Layouts: asymmetric, novel arrangements; named patterns as starting points with documented modifications (`Derivation: modified: [description]` required)
- Copy: voice rules + `ux_writing` slots enforced
- WCAG AA: hard gate — same as Mode A
- Outputs: HTML/CSS prototype; optional Figma frames tagged `[exploratory]`; no developer handoff, no Cursor rules
- Best for: marketing pages, editorial content, brand campaigns
- Review question: "Does this feel right and push the right way?" — not "Does this match the spec?"

**Mode B Creative Compass** *(pick 2–3 that fit the brief — not a checklist)*

1. **Oversized type anchor** — Break the type scale ceiling on one heading; it becomes the entry point everything else responds to.
2. **Section rhythm variation** — Alternate tight and spacious sections; the contrast makes each section feel distinct without breaking coherence.
3. **Asymmetric content axis** — Commit content to an edge, column offset, or diagonal pull; asymmetry reads as editorial intent, not error.
4. **Grid-breaking inline element** — One element crosses the grid boundary, isolated, to signal content importance — not to create noise.
5. **Negative space as content** — Generous padding and minimal content carry communicative weight; the emptiness is deliberate, not empty.
6. **Typography-led hierarchy** — Type scale contrast alone creates section separation — no dividers or background color changes needed.

**Mode C — Futurecasting**
Speculative aesthetic mode for concept work.
- Components: custom allowed
- Tokens: config as baseline; extended palette permitted — **every invented color MUST be contrast-verified before use** (4.5:1 body text, 3:1 large text — no exceptions)
- Layouts: named patterns as departure point; derivation must be documented
- Copy: concept narrative language; prohibited words may be used if concept demands it, with documentation
- WCAG AA: hard gate — applies to ALL output regardless of how speculative; custom components require semantic HTML, visible focus states, `prefers-reduced-motion` compliance
- Outputs (choose): interactive prototype OR composition blueprint + concept narrative (standalone `.md` with YAML frontmatter — NOT a heyhi-deck input; when a deck is needed, summarize the narrative conversationally to heyhi-deck)

**Mode A vs Mode B — What Changes**

| | Mode A | Mode B |
|---|---|---|
| Layout declaration | Named pattern, `Derivation: exact` | Named pattern as starting point, `Derivation: modified: [description]` required |
| Type scale | Config tokens only, no ceiling breaks | Oversized anchor elements permitted |
| Spacing | Config density applied consistently | Section rhythm variation encouraged |
| Grid alignment | Strict adherence | Intentional grid breaks allowed, isolated to one element |
| Developer handoff | Required | Not included |
| Cursor rules | Generated | Not generated |
| Figma output | Production frames | Optional frames tagged `[exploratory]` |
| Review question | "Does this match the spec?" | "Does this feel right and push the right way?" |

Tokens, WCAG AA, voice rules, and prohibited words are identical in both modes. Mode B is not permission to ignore the design system; it is permission to push within it.

---

### Identity Proposal — a constrained Mode B artifact-type

A client-facing **stylescape**: one self-contained HTML file that *shows* a decided visual direction (type in use, color in use, a composed section, logo zones, in-context mockups) and carries a decision gate. It is the rendered companion to the `heyhi-style-brief` prose brief — the brief is the voice, the proposal is the eye, and they ship as one approval moment. It is a **constrained profile of Mode B**, not a new top-level mode (the A/B/C triad stays intact) and **never** "Mode D" (that string belongs to `design-system-onboard`'s moodboard-to-config extraction). The full fixed template — section anatomy §0–10, grid, input-precedence, provisional convention — is `references/stylescape-patterns.md`; load it when the request is an Identity Proposal.

**Triggers:** "identity proposal," "build the stylescape," "render the visual direction for approval," "show the client the direction," "the visual half of the brief."

**Gate — runs at Config Validation, in addition to the standard checks:**

- **Require `meta.gate_status.direction_lock_confirmed: true`.** This is the gate, a boolean, not a score, and it overrides the Mode B "proceed with a warning" allowance: an Identity Proposal renders a *decided* direction. If false, hard stop. Say exactly: *"Direction not locked: direction_lock_confirmed is false. An Identity Proposal renders a decided direction — run heyhi-style-selection or Gate 0 to lock it first."*
- **Require an approved brief as input.** The render *holds* the brief's decided taste; it never generates taste from a bare config (`corrections-registry.yaml → token-driven-taste-gap`). No brief → stop and ask for it; do not render from the config alone.
- **Do NOT gate on fidelity.** The fidelity floor is a Mode A gate; the proposal is pre-token-lock by design, so gating it on fidelity is self-defeating. Low fidelity is *degradation input* for the legend, not a stop.
- **Inherit the `completeness < 30` all-mode hard stop** (step 5 matrix) and the **WCAG AA hard gate** — verified against every rendered text/background pair, not against provenance metadata.
- **Strict jsonschema pass on the input config** (Draft 2020-12 against `brand-config/schema.json` — see § Config schema-conformance below). Fail loudly on a malformed config rather than rendering from it (`config-schema-validation-gap`).

**Provisional-marking pass (before emit).** Mark every rendered value by confidence so inferred values never launder into decided ones. Source of truth: `meta.field_provenance[].confidence` — `extracted` renders plainly, `inferred` renders visibly banded "direction, not decided," `provisional` appears only as an open decision, `failing` is excluded. **Fallback when provenance is sparse or absent** (real `manual` configs are low-fidelity and usually carry no rich provenance map): use `meta.provisional_fields[]` (confidence enum `[inferred, pending]`) + `meta.version` (`0.x` = provisional) + the score band. Carry the quiet legend: *solid = from your assets · marked = direction we'll confirm.* `geographic-inference-palette-temperature` is load-bearing here: an inferred color temperature renders banded, never as a decided one.

**Anti-tell emit gate (before emit).** Scan the render against `ai-services/design-intelligence/visual-anti-tells.md` (AT-1 through AT-10), reusing the scan pattern `heyhi-prototype-audit` Layer 2 already runs. **High severity on the hero / cover frame**, Medium elsewhere. Highest-risk tells for a stylescape: AT-2 (gradient cover headline), AT-1 (chromatic glow), AT-4 (three-equal-column card row standing in for "color" or "type"), AT-7/8/10 (placeholder or fabricated content in the mockups). A matched tell with no documented carve-out is a defect; fix it before emit.

**Decision register → Mode D handoff.** The §10 gate surfaces locked vs. open decisions read from `meta.gate_status` and the provisional signals; each locked row maps 1:1 to a `design-system-onboard` Mode D precondition (`heyhi-style-brief § Handoff to Mode D`). No row may be left open after approval. The register's output *is* the Mode D handoff manifest.

**Output:** one portable, print-clean HTML file to the instance's gitignored engagement folder, `<engagement folder>/deliverables/identity-proposal/` (main workspace, never a worktree copy).

---

### WCAG AA — Non-Negotiable in All Modes

**Scope:** WCAG AA compliance is verified against all explicitly documented text/background token combinations in the config. This covers the documented pairs — it does not and cannot cover every interactive state, gradient overlay, opacity stack, image background, or browser rendering variation in the final deployment. Verify compliance in-browser before client delivery.

- 4.5:1 contrast ratio for body text — verified against all documented token pairs
- 3:1 for large text and UI components — verified against all documented token pairs
- Visible focus states on all interactive elements
- `prefers-reduced-motion` respected in all animations
- Semantic HTML in all output
- Mode C extended palette: contrast verified for each invented color **before use in CSS**

---

### Real-HTML Rendering — Enforced for Content Builds

**Content pages render server-side (SSR), at build time (SSG/prerender), or via incremental static regeneration. CSR is permitted only for non-essential enhancements** (view counters, chat widgets, live feeds, real-time data overlays).

Default ui-studio templates ship with prerender or SSR enabled. A bare client-rendered SPA is not an acceptable delivery for any content-bearing page. Verification of this rule lives in the GEO Readiness Gate (`references/geo-readiness.md`), invoked before delivery handoff.

This rule applies to client deliverables; internal admin UIs, single-page tools, and pure prototypes that will never be public are exempt. When in doubt, treat the page as content-bearing.

Rationale: the major generative-engine crawlers (GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, PerplexityBot, CCBot) do not execute JavaScript. A client-rendered content page is invisible to the systems that feed generative answers — and switching to SSR after launch is a rewrite, not a patch. See `engineering-handoff/geo-ui-studio-integration-2026-06-02.md` § B1 ("Renders real HTML" as a build invariant).

---

### Responsive Behavior — Enforced in All Modes

Every build targets three canonical breakpoints from `layout.grid.breakpoints`. If absent, apply these defaults:

| Breakpoint | Default size | Config key |
|------------|-------------|------------|
| `sm` | 375px | `layout.grid.breakpoints.sm` |
| `md` | 768px | `layout.grid.breakpoints.md` |
| `lg` | 1440px | `layout.grid.breakpoints.lg` |

**Build rules:**
- Mobile-first: write all styles for `sm`, then scale up with `@media (min-width: …)` for `md` and `lg`.
- **Pattern rethinking:** For components with more than 3 items or complex vertical structure, evaluate whether the desktop pattern can remain functional at `sm` breakpoint. If it cannot, replace the pattern rather than restacking it. Document the change in the Layout Declaration as `Derivation: mobile-rethink: [description of pattern replacement]`.
- Fluid typography: `clamp()` between mobile and desktop sizes. No fixed `px` font sizes.
- Touch targets: minimum `tokens.spacing.touch-target.min` (default: 44px) on every interactive element — buttons, links, form controls.
- Reading column: constrain to `layout.content_max_width` (default: 780px). Never hardcode a max-width value not sourced from the config.
- Page margins: use `layout.page_padding` (default: `clamp(1.5rem, 5vw, 2.5rem)`). Never invent margin values.

Responsive behavior is a constraint class, not a build step. It applies in every mode and cannot be deferred to post-delivery. Same enforcement weight as WCAG.

---

### Dark-Native Config Handling

**Detecting the scheme:** Read `meta.default_scheme` from the config during Config Validation (step 6). Log the detected scheme before proceeding to any build step.

- `"light"` or absent → **light-baseline build.** Standard flow applies.
- `"dark"` → **dark-native build.** Different build foundation — apply all rules below.

**Dark-native build rules:**
1. **Primary foundation:** If `tokens.color.schemes.dark` block is present (ADR-006 Option C), use its values as the build foundation, not the top-level `tokens.color` values.
2. **Contrast surface:** All WCAG checks run against dark background tokens, not white. 4.5:1 for body text is measured against the dark background.
3. **Shadows:** `tokens.shadow` may be absent or inverted on dark-native configs (Cluster C is typically flat). Do not add box-shadows if the shadow block is empty.
4. **No light-value guessing:** Never construct a light-scheme page by inverting dark token values. That is a provisional adaptation — surface the warning below.

**Light-scheme adaptation warning** (required when `meta.default_scheme: "dark"` and output is light-scheme):

Include this note in the delivery output:

> ⚠ Provisional: color values checked against light backgrounds only. This config is dark-native (`meta.default_scheme: dark`). The canonical build for this design system is dark-scheme. Light-scheme output is an adaptation and has not been verified against the source design.

---

### Spec Intake — Build Signal Extraction

Two paths. Choose before proceeding to brand system loading.

**Lightweight path — skip intake:**
Go directly to Step 4 (Load brand system) if ALL three conditions are true:
- Request specifies a single atomic component (button, badge, input, label, card, tooltip, tag, icon)
- Config is at FULL unlock (completeness ≥ 90, fidelity ≥ 60)
- No layout context is required (no section placement, no page structure, no multi-component composition)

Target framework (signal #7) is not required for atomic component builds — no rendering strategy is needed for a single button or card. Record it if known; do not block on it.

**Full intake path — extract these seven categories:**

1. **Page type** — landing, product, editorial, dashboard, form flow, campaign, concept, identity proposal (the constrained Mode B stylescape — see § Identity Proposal)
2. **Primary goal** — what this page must accomplish for the user
3. **Audience** — who will see this and what they bring to the interaction
4. **Content inventory** — what exists (provided text, existing components, images) vs. what needs to be created
5. **Interaction level** — static, lightly animated, interactive (form and state), immersive
6. **Design context** — extending prior work, greenfield from config, or provisional config constraints
7. **Target framework** — Astro / Next.js / TanStack Start / SvelteKit / Hydrogen / unknown.
   If unknown, default to framework-agnostic output. If Astro or Next.js, the Component
   Implementation Map (see Layout Declaration) will include framework-specific rendering
   strategy per component. If SvelteKit, surface the G-7 path decision before proceeding
   (see engineering-handoff/ui-studio-framework-compatibility.md).

**Component communication pattern** (interactive and immersive builds only — record alongside the numbered signals)

Will multiple components need to share state or trigger each other?

If yes, decide upfront:
- (a) Unified state: React Context, or a lightweight store (Zustand, etc.) if the dependency tree warrants it
- (b) Custom DOM events: `window.dispatchEvent` for loose coupling between components that should not know about each other
- (c) Mixed: both patterns, with a documented boundary (e.g., "Context for data; DOM events for cross-tree triggers")

Mixed patterns are valid. Undocumented mixing is not. Record the decision before Layout Declaration. Do not let the pattern emerge from the build.

*Mode B addition:* When Mode B is active, extract one more signal before building: "What should this page feel different from?" This captures the creative departure intent and sets the compass for heuristic application.

Record all extracted signals before proceeding. The build is only traceable if the intake trace exists.

**Complexity Tier Detection (full intake builds only)**

After extracting intake signals, classify the build:

**Simple:** Static components, single interaction surface, no cross-component state. Proceed directly through the workflow skeleton.

**Complex:** Global state, custom events, multi-component interaction, or interactive proofs of system capability. Use the 4-phase structure below and run a verification pass between phases, not just at the end.

| Phase | Scope | Gate before next phase |
|-------|-------|------------------------|
| Phase 1 — Aesthetic Intent | Lock typography, CSS variables, color tokens. No components. | Tokens verified against config. CSS custom properties defined. |
| Phase 2 — Static Structure | Routing, component scaffolding, layout. No interactivity. | All components render without errors. Layout Declaration matches built structure. WCAG AA checked for colors used. |
| Phase 3 — Interactive Proofs | State, contexts, event listeners, simulated data. | State management pattern documented and consistent (no undocumented mixing of patterns). Key interactions functional. |
| Phase 4 — Narrative Polish | Cross-component dialogue, mobile adaptation, UX refinement. | Mobile patterns validated. Reduced motion respected. Full quality gate runs here. |

Note: The final quality gate (step 12 in the workflow skeleton) always runs regardless of tier. The phase gates are stability checkpoints, not substitutes.

**Full intake triggers** (override the lightweight skip if any apply):
- Mode B or C active
- Config at PARTIAL_A unlock or lower
- Page-level or multi-section scope
- Audience, goal, or content inventory is ambiguous from the request

---

### Page Plan + Human Gate

*Applies to full intake builds only. Skip for lightweight-path requests.*

After intake, produce a page plan before writing any CSS. Keep it inline — this is a planning artifact, not a client deliverable.

Format: `Page Plan — [page name]` header, then one block per section:

```
Section: [name]
Purpose: [what this section does for the page structure]
Message: [what this section must communicate — one sentence]
User goal served: [what the user needs at this point in the flow]
Content status: exists / needs writing / partial — [what specifically is missing]
Interaction notes: [state, animation, event triggers]
```

Then three footer lines: `Hierarchy notes:`, `Content gaps:`, `Config constraints:`.

Before moving to Layout Declaration, every section must have a defined Message. Building a component without a locked message produces structural work that gets overwritten. The Message field is the gate.

Present the plan and wait for confirmation before moving to Layout Declaration. Say exactly:

> "Here's the page structure I'm planning — confirm or redirect before I start building."

**Gate skip:** Skip the wait (but not the plan itself) when the user has given explicit build permission ("just build it," "go ahead," "don't wait for confirmation"). The page plan is always produced on full-intake builds — only the confirmation pause is optional.

---

### Layout Declaration — Enforced Before Every Build

Every build begins with a Layout Declaration before any CSS is written. No exceptions.

**Format:**
```
Section: [name]
Pattern: [named pattern from layout-patterns.md]
Derivation: exact (Mode A) | modified: [description] (Mode B) | derived-from: [pattern] (Mode C)
Rationale: [why this pattern fits this content + brand cluster]
Spacing tier: [generous/standard/tight] — from config.layout.spacing_density
```

**Hybrid patterns:** Use derived notation when content crosses patterns — e.g., `Hero-First derived with embedded Dashboard Split in right column`.

**Post-build verification (quality gate):** After CSS is written, verify each declared section's grid properties, spacing values, and structural HTML match the named pattern's specification. Flag divergences. This makes the declaration a constraint, not documentation.

**Spacing is derived, not guessed:** `config.layout.spacing_density` (spacious/balanced/dense) drives section padding tier values. Never invent padding values.

---

### Component Implementation Map (Mode A only)

After the Layout Declaration is complete and before CSS is written, produce a Component Implementation Map. This maps each declared component to its rendering strategy in the target framework.

**When to produce:** Mode A builds where target framework (intake signal #7) is known. Skip for Mode B/C (no developer handoff) and for unknown frameworks (the map cannot be framework-specific without a target).

**How it works:** The information needed is already captured:
- Interaction level (intake signal #5) tells you whether the page has interactive components at all.
- The Page Plan's "Interaction notes" field tells you which sections have state, event triggers, or dynamic behavior.
- The Layout Declaration tells you every component that will be built.

The Component Implementation Map synthesizes these into a framework-actionable table.

**Format:**

```
### Component Implementation Map

Target framework: [from intake signal #7]

| Component | Rendering | Directive / Annotation | Rationale |
|-----------|-----------|----------------------|-----------|
| [Nav]     | Interactive | Astro: `client:load` / Next.js: `"use client"` | Mobile menu state requires client JS |
| [Hero]    | Static | Astro: `.astro` / Next.js: server component | No client JS — static content |
| [Feature grid] | Static | — | No client JS |
| [Contact form] | Interactive | Astro: `client:load` / Next.js: `"use client"` | Form validation + submit handler |
| [Footer]  | Static | — | No client JS |
```

**Rendering classification rules:**

- **Static:** No JavaScript required. No state, no event listeners beyond standard links. In Astro: implement as `.astro` file. In Next.js: server component (default, no annotation needed).
- **Interactive:** Requires client-side JavaScript. State, form handling, dynamic data, or browser APIs. In Astro: React Island with `client:*` directive. In Next.js: `"use client"` directive.
- **Deferred Interactive:** Interactive but below the fold or not immediately needed. In Astro: `client:idle` or `client:visible`. In Next.js: dynamic import with `{ ssr: false }` or React.lazy.

**Astro directive selection (when target is Astro):**

| Component characteristic | Directive |
|-------------------------|-----------|
| Must be interactive on first paint (nav, hero with animation state) | `client:load` |
| Interactive but can wait for idle (below-fold accordions, non-critical widgets) | `client:idle` |
| Interactive and below the viewport (carousels, lazy-loaded sections) | `client:visible` |
| Uses browser-only APIs (canvas, WebGL, clipboard) | `client:only="react"` |

**Default rule:** If a component has no interactive behavior documented in the Page Plan's interaction notes, classify it as Static. Do not add rendering overhead to static content.

---

### Cluster-Derived Design Principles

After loading the brand config, read `brand.style_cluster` and apply the corresponding design heuristics to every layout and composition decision. These are not token lookups — they are higher-order craft directives that shape how the config's values are expressed.

| Cluster | Character | Active principles |
|---------|-----------|-------------------|
| **A — Minimal/Refined** | Restraint as craft | Negative space as signal · Precision typography · Monochromatic depth |
| **B — Warm/Human** | Breathing room | Generous section spacing · Organic rhythm · Editorial warmth in hierarchy |
| **C — Bold/Distinctive** | Contrast-forward | Type as architecture · Graphic decisiveness · Section drama over uniformity |
| **D — Technical/Precision** | Grid as system | Density hierarchy · Functional clarity over decoration · Structured information |
| **E — Organic/Natural** | Material honesty | Textural depth · Asymmetric rhythm · Layered foreground/background |

For any cluster not listed, derive two principles from `brand.personality` and one from `config.layout.spacing_density` (spacious → breathing room; dense → hierarchy-through-proximity; balanced → neither dominates).

For full principle descriptions with worked examples per cluster, read `references/cluster-design-principles.md` (Zone 2 — load when a build requires design direction beyond token application).

---

### Taste Projection — Brand-Specific Steering

When `taste_projection` is on (default) AND `brand.style_entry` names a `style-reference-library.md` entry with an authored `taste_profile`, load that entry's taste as build directives at Workflow step 4.5 — *after* the brand system, *before* Layout Declaration. These **specialize** the generic Cluster-Derived Design Principles above: on any conflict the entry's principles win; the cluster row stays the character backdrop. This replaces the same-recipe-per-cluster default with brand-specific steering (the Convergence-Trap fix). Selection + plumbing, not authoring — the data (`taste_profile`), the link (`brand.style_entry`), and the eval half (`boundary_behaviors` → validator Guard 6) already exist.

- **Load as build directives:** `aesthetic_principles` (apply each principle's boundary *test*), `restraint_notes` (refusal + consequence, checked before emit), `reference_examples` (carry as a visual where an asset exists; else `what_to_take` prose).
- **Do NOT load for the build:** `boundary_behaviors` — eval-shaped; they steer the output judge, not the build. Keep the split clean.
- **Fallback:** the matched entry has no authored `taste_profile` (most entries today) → use the generic Cluster-Derived Design Principles unchanged. Purely additive; no existing build changes behavior unless an authored profile is present.
- **`taste_projection: off`** → skip projection; generic cluster principles only. This is the control path (the build reads tokens + generic cluster only, as before).
- **Provenance:** record the resolved `taste_projection` value, the matched `style_entry`, and whether its profile was authored or fell back, in build output (and the Mode A developer handoff).

---

### Build Resources — Resource-to-Job Assignment

Every build has a small, explicit set of resources, each with one job. Assign the resource to the job — do not improvise a truth source. ui-studio builds *client* interfaces, so the client's config is the build-time truth; the Design System MCP tools are the same pattern pointed at a per-client instance.

| Resource | Job in the build | When |
|---|---|---|
| **Figma MCP** (`get_variable_defs`, `get_design_context`) | Extract the client's tokens + component specs *into* the config | Onboarding / refresh (via `ui-studio-onboard`), before any build |
| **`active-brand.json`** (the client config) | The build-time source of truth — tokens, voice, layout, `components` | Step 1 (validate) and step 4 (load) |
| **`components.inventory`** in the config — or **`retrieve_design_examples(task_type=…)`** from a per-client design-system MCP when one is deployed | Match an existing component (props, variants, do/don't) *before* building a new one | Step 10 (Component check), mandatory |
| **`validate_output`** rendered path against the config's tokens — or the local conformance lane (`conformance/css_check.py`) when no per-client MCP is deployed | Pre-delivery truth-read of the *emitted* CSS — flags hardcoded values outside the config's tokens | Step 12.5 (Rendered-read gate), before Deliver |

**Data isolation (Protocols at Boundaries).** The `heyhi-mcp` server (`retrieve_design_context`, `retrieve_design_examples`, `validate_output`) is the **HeyHi-brand instance** of this pattern — it reads HeyHi's *own* design system. For client work the correct data-isolation path is a **per-client design-system MCP** pointed at that client's tokens and components; never validate a client build against HeyHi's design system. Until a per-client MCP is deployed, the config JSON is the truth source and the same reads run locally against it (the config's `components.inventory`, the `conformance/css_check.py` lane). HeyHi's own pages take the other route — `heyhi-ui-ux` points directly at the `heyhi-mcp` server (`design-system://summary` + `retrieve_design_context`), because there the design system *is* HeyHi's.

---

### Workflow Skeleton

> **Architectural Honesty.** For builds that call for system concepts (data sync, telemetry, observability), the first question is not how to represent the concept visually. It is whether a lightweight simulation is achievable (React Context, custom event listener, CSS variable read/write). A site that demonstrates a capability is more credible than one that describes it. This applies in all three modes.

1. **Validate config** — version, completeness, last_refreshed (above), plus a strict schema-conformance check (`validate.py` scores but does **not** enforce `brand-config/schema.json` — see § Config schema-conformance below)
2. **Mode selection** — confirm with user or infer from request
3. **Spec Intake** — two paths (see Spec Intake section above):
   - *Lightweight:* atomic component + FULL unlock + no layout context → skip directly to step 4
   - *Full intake:* extract seven categories (page type, primary goal, audience, content inventory, interaction level, design context, target framework); interactive/immersive builds add a component communication pattern decision; Mode B adds "What should this feel different from?" Record all signals. Run Complexity Tier Detection to classify Simple vs. Complex before proceeding.
4. **Load brand system** — extract key decisions from config (typography, palette, spacing, motion, voice). If `brand.seed_color` is present, `tokens.color` may be generated accessible-by-construction (light + dark schemes, semantic roles) via `scripts/palette_gen.py` — see `references/color-generation.md`. Generated values carry `source: palette_gen` in `field_provenance`.
   - **4.5 Load taste projection** — if `taste_projection` is on (default) and `brand.style_entry` has an authored `taste_profile`, load its `aesthetic_principles` + `restraint_notes` + `reference_examples` as build directives (see § Taste Projection). Specializes the generic cluster principles; falls back to them when no profile exists. `off` → skip (control path).
5. **Page Plan + human gate** — full intake builds only; skip for lightweight-path requests (see Page Plan section above). Produce the page plan, present it, and wait for confirmation before proceeding to Layout Declaration.
6. **Load Pattern Summary Index** — from `references/layout-patterns.md` (~300 tokens); load full specs on demand
7. **Layout Declaration** — declare every section before writing CSS
8. **Write copy** — apply voice rules + ux_writing slots from config
9. **Build implementation** — token-driven CSS, semantic HTML, interaction patterns from config motion tokens
10. **Component check (mandatory exemplar match)** — reuse before rebuild. Before finalizing any component, consult existing exemplars: read the config's `components.inventory` (or call `retrieve_design_examples(task_type=<component>)` when a per-client design-system MCP is deployed — see the Build Resources table) and match on props, variants, and do/don't guidance. A component that duplicates an existing inventory entry is a defect. Load `references/component-analysis.md` for the drift-detection procedure. This step is not optional; when the config has no `components` block, state that the inventory check is unavailable and proceed (do not skip it silently).
11. **Post-build verification** — grid/spacing/HTML matches declared patterns; flag divergences
12. **Quality gate** — Five-domain check before delivery. Work through each domain in order. The Accessibility domain is a hard gate — delivery is blocked until all contrast checks pass.

   **Severity order when multiple domains fail:** (1) Accessibility (hard gate, delivery blocked) → (2) Interaction → (3) Visual → (4) Brand → (5) Code. Fix top-down.

   **Brand:** Typography matches config font stack. All colors use config tokens — no arbitrary hex values. Zero em dashes in any copy. Zero banned words from `voice.prohibited_words`. CTAs match voice rules. Visual direction is consistent with `brand.personality` and active cluster principles. When `taste_projection` is on, also consistent with the matched entry's `aesthetic_principles` (apply each principle's boundary *test*), and no `restraint_note` is violated — a violated restraint with no documented carve-out is a defect.

   **Interaction:** Every animation has a communicative purpose — remove any motion that cannot be described as "this tells the user X." `prefers-reduced-motion` respected in all animations. Hover states on all interactive elements. Touch targets meet `tokens.spacing.touch-target.min` (default 44px) on all interactive elements.

   **Visual:** No two adjacent sections share the same layout pattern. Clear type hierarchy is established. At least one layout break per page. Spacing rhythm varies across sections — no uniform padding throughout. Tested visually at `sm` (`layout.grid.breakpoints.sm`, default 375px), `md` (`layout.grid.breakpoints.md`, default 768px), and `lg` (`layout.grid.breakpoints.lg`, default 1440px).

   **Accessibility (hard gate — delivery blocked until passing):** WCAG AA contrast: 4.5:1 for body text, 3:1 for large text and UI components — verified against all explicitly documented token pairs (not all possible rendering contexts; verify in-browser before client delivery). Alt text on all images. Visible focus states on all interactive elements. Sequential heading hierarchy. Keyboard navigable. Mode C extended palette: each invented color contrast-verified before use. Dark-native (`meta.default_scheme: dark`): all contrast checks run against dark background tokens — not white. Light-scheme adaptation from a dark-native config: light-scheme adaptation warning included in delivery output. **Interactive component hard block:** For Dialog, Dropdown, Tooltip, Select, Accordion, Tabs, Combobox, and DatePicker — the component must be built on a headless primitive (Radix Primitives, React Aria, or Ariakit) OR must pass manual WAI-ARIA Authoring Practices verification before the component is marked complete. A custom implementation of any of these components is a defect unless explicitly verified. No exceptions.

   **Code:** CSS custom properties throughout — no inline values. Semantic HTML: `<nav>`, `<section>`, `<footer>`, `<article>` — no `<div>` soup. No console errors. Fonts load with fallbacks. `IntersectionObserver` for scroll animations. `requestAnimationFrame` for parallax. `{ passive: true }` on scroll listeners.

   Mode A: run developer handoff after all five domains pass.
12.5. **Rendered-read validation gate (mandatory, fail-loud)** — the step-12 Brand check ("no arbitrary hex values") is a self-check; this is the on-path truth-read that enforces it mechanically. Before Deliver, run `validate_output` on the *emitted* CSS/HTML via its `rendered_css` path against the active config's tokens (per-client design-system MCP when deployed; otherwise the local `conformance/css_check.py` lane against the config). It parses the stylesheet and flags any hardcoded color, dimension, or typed value (font-weight, line-height, z-index, border-width, motion duration/easing) outside the config's tokens — reading the emitted stylesheet, not the self-reported `tokens_used` manifest. **Fail loud:** if the rendered-read is unavailable (no per-client MCP and the conformance package absent), say so and fall back to the local conformance run — never a silent pass. A Mode A rendered-read failure blocks delivery (it is a Brand-domain defect under the severity order); Mode B/C surface the flags in the delivery notes.
13. **Deliver — as a scaffold, not a finished build.** The output is scaffolding: a strong, system-grounded starting point, not a shippable final. Deliver the prototype + handoff + Component Implementation Map (Mode A) / prototype (Mode B) / prototype or blueprint + concept narrative (Mode C), and include an explicit **Human-verify checklist** naming what the build cannot self-certify:
    - Real content replacing every placeholder — copy, images, data
    - Every component *state* in context — loading, empty, error, focus, disabled; the build shows the happy path
    - Interactive-component accessibility confirmed against the WAI-ARIA APG with a keyboard + screen-reader pass (the five-domain gate checks structure, not lived assistive-technology behavior)
    - Component registration / exports / routing wired into the real codebase
    - Responsive + dark-scheme behavior confirmed in the target environment, not only the prototype
    - The step-12.5 rendered-read reviewed — every surfaced token-fidelity flag resolved or consciously accepted

    Frame it to the client or engineer as scaffolding they finish, never a build they ship.

> **Config schema-conformance — run with `validate.py`, not instead of it.** `validate.py` scores completeness/fidelity and enforces gates; it does **not** validate the config against `brand-config/schema.json`, so invalid enum values and wrong-typed fields pass silently. Before treating any config as validated, also run a strict JSON Schema pass (jsonschema Draft 2020-12) and require zero errors:
>
> ```bash
> CONFIG=<config-path>
> python3 - "$CONFIG" <<'PY'
> import json, sys
> from jsonschema import Draft202012Validator
> cfg = json.load(open(sys.argv[1]))
> sch = json.load(open("heyhi-skills/ui-studio/brand-config/schema.json"))
> errs = list(Draft202012Validator(sch).iter_errors(cfg))
> print("VALID" if not errs else [f"{'.'.join(map(str, e.path))}: {e.message}" for e in errs])
> PY
> ```
>
> The two `confidence` enums differ — `meta.provisional_fields[].confidence` is `[inferred, pending]`; `meta.field_provenance[].confidence` is `[extracted, inferred, provisional, failing]`. See `corrections-registry.yaml → config-schema-validation-gap`.

> **Content-architecture-only delivery (when website copy is client-provided).** When the engagement scope puts body and SEO copy with the client or a third-party copywriter, deliver the *content architecture*, not the copy: per page, the H1/H2/H3 hierarchy, route-specific title-tag and meta-description templates, per-section word-count targets, and the schema type. Render the prototype on clearly-marked representative placeholder (bracketed text plus a visible "prototype" banner) so a reviewer never mistakes placeholder for final. State the copy boundary in the developer handoff. If the client wants HeyHi to own the SEO copy, scope and price it as a separate add-on before the build, not after.

> **Serving a prototype for browser review.** The in-app preview panel does not load a prototype's relative stylesheet, so a multi-file static prototype renders unstyled. To let a user review it in their own browser, serve it over a local HTTP server rooted at the folder that contains every referenced asset: `python3 -m http.server <port> --bind 127.0.0.1 --directory <root>`, then give them `http://localhost:<port>/`. To make Markdown deliverables reviewable too, render them client-side with a CDN Markdown library (marked.js) in a small viewer page that falls back to raw text if the CDN is unreachable; do not pip-install a renderer into system Python. Verify endpoints before sending the URL (use `urllib` if `curl` is absent from PATH). The packaged, reusable version is the `heyhi-review-hub` candidate in `CANDIDATES.md`.

---

### Connecting to Other Skills

| Concern | Skill | When |
|---------|-------|------|
| Voice enforcement — client work | Voice rules from `active-brand.json` → `voice.*` block | Any visible copy written for the client |
| Voice enforcement — HeyHi Mode B/C | `heyhi-voice` | Building HeyHi marketing or concept pages via ui-studio |
| Design system audit (pre-build) | `heyhi-design-intelligence-audit` | Before first build against an unfamiliar client config; trust but verify |
| Token config onboarding | `ui-studio-onboard` | No config exists, or config needs a full refresh |
| Design critique | `design:design-critique` | Evaluating build quality or presenting output for review |
| Accessibility audit | `design:accessibility-review` | Full WCAG compliance check beyond the five-domain quality gate |
| UX copy review | `design:ux-writing` | Microcopy, error messages, slot copy, empty states |
| Config promotion | `validate.py --promote` | After designer review with fidelity ≥ 80 — promotes config from 0.x to 1.0 |
| Monthly design system care | `design-system-care-monthly` | Recurring engagement on a live client system |

---

## ZONE 2 — Context Loading

*Load only what the task requires. Not every build needs every file.*

### Quasi-Mandatory (loads on every Mode A/B/C build)

| Reference | Load when |
|---|---|
| `references/layout-patterns.md` Pattern Summary Index (~300 tokens) | **Start of every Layout Declaration** — required for pattern name lookup before any layout section is declared. Loads on every Mode A/B/C build. Not a conditional load despite Zone 2 classification — the Layout Declaration step cannot complete without it. Load full specs on demand when implementation detail for a specific pattern is needed. |

### Task-Conditional (load when condition is met)

| Reference | Load when |
|---|---|
| `references/interactive-build-protocol.md` | Build is rated "interactive" or "immersive" in Spec Intake, or Complexity Tier Detection activates the phased structure |
| `references/brand-integration.md` | Setting up a new project's design foundation — token mapping, type scale, spacing derivation |
| `references/interaction-patterns.md` | Building interactive elements — loading states, scroll reveals, parallax, hover effects, nav transitions |
| `references/cluster-design-principles.md` | Build requires design direction beyond token application — new client engagement, Mode B/C compass, section rhythm decisions not obvious from config alone |
| `ai-services/design-intelligence/style-reference-library.md` (matched entry's `taste_profile` block) | `taste_projection` is on AND `brand.style_entry` names an entry with an authored `taste_profile` — the Item 4 build directives (`aesthetic_principles`/`restraint_notes`/`reference_examples`). Falls back to § Cluster-Derived Design Principles when absent. |
| `references/futurecasting-ui.md` | Mode C active — speculative aesthetic rules, extended palette logic, contrast verification, composition blueprint schema |
| `references/stylescape-patterns.md` | Identity Proposal requested — the fixed stylescape template: section anatomy §0–10, grid, input-precedence, provisional convention, the AT emit gate, decision register to Mode D handoff |
| `references/build-and-preview.md` | Build produces 3+ structurally similar pages (generate from the approved exemplar, never hand-copy), or a coded multi-page prototype is being handed to the user for browser review (serve the folder) |
| `references/figma-mcp-integration.md` | Figma output requested — frame tagging by mode, multi-library extraction, token-to-variable mapping |
| `references/ux-writing-guidelines.md` | Writing component-level copy — slot lookup, gap handling, source attribution |
| Voice rules from `active-brand.json` | Writing any visible copy — load `voice.*` and `ux_writing.*` blocks |

### On-Demand (load when explicitly needed or before delivery)

| Reference | Load when |
|---|---|
| `references/web-quality.md` | Before final delivery — full QA checklist |
| `references/geo-readiness.md` | Before final delivery on any content-bearing build — eight-item pre-handoff gate (real HTML, robots.txt, schema, sitemap, WAF, heading hierarchy) |
| `references/component-analysis.md` | Component inventory check or drift detection |
| `references/layout-patterns.md` full specs | Implementation detail needed for a specific pattern |
| Mode C composition blueprint schema | Mode C, blueprint output path |
| Developer handoff format | Mode A, before writing handoff document |
| `references/color-generation.md` + `scripts/palette_gen.py` | Generating `tokens.color` from a `brand.seed_color` — the accessible seed-to-palette capability (light/dark, semantic roles, WCAG by construction) |

### Searchable (query; never load wholesale)

```bash
python3 scripts/search.py "<query>" --domain <domain>
```

Domains: `style`, `color`, `typography`, `landing`, `product`, `ux`, `animation`, `google-fonts`, `chart`, `mobile`

Results are supplementary. The brand config takes precedence.

---

## Exit Gate Required Headers (bottom-of-skill bracket)

This skill closes through the Exit Gate Flavor A (`CLAUDE-SESSION-RULES.md § Exit Gate`). Before declaring done, confirm every required header below contains real content, not a claim:

- `## Fixes Applied`
- `## Smoke Test`
- `## Next Session Prompt`

If any header is empty or contains advisory prose ("I checked for bugs") instead of a concrete artifact, the gate has not been satisfied. Apply fixes until clean — then emit.

---

*HeyHi Internal Use Only. Created 2026-03-25.*
