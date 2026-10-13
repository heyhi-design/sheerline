---
title: "Stylescape / Identity Proposal Reference"
classification: internal
status: active
scope: ui-studio reference — the fixed template for the Identity Proposal artifact-type
loaded_by:
  - ui-studio (Identity Proposal artifact-type — a constrained profile of Mode B)
precedent:
  - heyhi-skills/ui-studio/references/futurecasting-ui.md (Composition Blueprint schema — structural precedent for a fixed-template artifact)
  - on-disk worked reference — the hand-built consolidation hub a live engagement produced before this capability existed
created: 2026-06-10
---

# Stylescape / Identity Proposal Reference

**`ui-studio/references` · Load when the request is an Identity Proposal · June 2026**

*The fixed template for the Identity Proposal: a single, self-contained, client-facing stylescape that shows a decided visual direction and carries a decision gate. This is the rendered companion to the prose direction brief. The brief is the voice; the proposal is the eye. They ship as one approval moment.*

---

## What the Identity Proposal Is

The pipeline's only client-facing visual-identity approval artifact has been the `heyhi-style-brief` output: 400–550 words of prose a client reads and approves before any tokens are built. The brief is deliberately visuals-free. The foundational research that governs all of this says taste must be *seen*: a design can pass every automated check and still feel assembled rather than designed. The proposal stage was showing the client nothing. The Identity Proposal closes that gap by rendering the decided direction at real scale: type in use, color in use, a composed section, logo zones, the system in context, and a decision register the client signs.

It is a **constrained profile of Mode B**, not a new top-level mode. The A/B/C triad stays intact. Client-facing label: "Identity Proposal." It is **never** called "Mode D" (that string belongs to `design-system-onboard`'s moodboard-to-config extraction; ui-studio has only Modes A/B/C).

**The boundary, stated once.** Three nearby artifacts are not this one:

| Artifact | Owner | Relationship |
|----------|-------|--------------|
| Prose direction brief | `heyhi-style-brief` | The *input*. The voice half of the same approval moment. The proposal renders what the brief describes. |
| Visual exploration | `heyhi-visual-exploration` (candidate) | Runs *before* the direction lock: divergent, "not a deliverable." The proposal runs *after* the lock: convergent, *is* the deliverable. They bracket the lock; they do not compete. |
| v0→v1 fidelity review | `design-system-review` | An *internal* check of a *built* system against design intent. The proposal is *client-facing* and *pre-token-lock*. One reviews a build; the other proposes a direction. Do not conflate the two renders. |

---

## When It Runs — the Contract

The authoritative gate wiring lives in `ui-studio/SKILL.md § Identity Proposal`. In brief, an Identity Proposal renders only when:

1. **`meta.gate_status.direction_lock_confirmed` is `true`.** This is the gate, a boolean, not a score. A proposal renders a *decided* direction; if the direction is not locked, route back to `heyhi-style-selection` / Gate 0. The render does not invent a direction to render around.
2. **An approved brief is present.** The render *holds* the brief's decided taste; it never generates taste from a bare config (`corrections-registry.yaml → token-driven-taste-gap`). No brief, no proposal.
3. **Fidelity is *not* gated.** The fidelity floor is a Mode A gate. The proposal is pre-token-lock by design; gating it on fidelity is a self-defeating gate. Low fidelity becomes *degradation input* (it tells the legend "these are directional"), never a stop.
4. **The `completeness < 30` all-mode hard stop still applies.** Below 30 there is not enough to render anything meaningful.
5. **WCAG AA is a hard gate** on every rendered text/background pair, same weight as any Mode A/B/C build.
6. **Three passes run before emit:** the provisional-marking pass, the AT-1..AT-10 anti-tell scan, and a strict jsonschema pass on the input config.

---

## Inputs and Precedence

The render consumes up to three inputs and **invents nothing absent from them**.

| Input | Required | Supplies | Source |
|-------|----------|----------|--------|
| Approved direction brief | **Yes** | The voice, the felt qualities, the rationale, the sector calibration, the "what we're not doing" contrasts | `heyhi-style-brief` output |
| Brand config | **Yes** | The token values that *hold* the taste; the provenance and provisional signals; the WCAG-verified pairs | a `manual` provisional config or a `design-system-onboard` Mode D config |
| Logo concept | Optional | The mark direction and the "Logo Logic" strategic idea (§1); **wins on palette** | `heyhi-logo-system` Concept output + `logo`-namespace JSON |

**Precedence — "logo wins" on palette.** When the config and the logo concept disagree on a color value, the **logo wins**: the mark is the more-resolved taste decision, and the config should already carry the reconciled values. This is the canonical `token-driven-taste-gap` example: the render reads the reconciled config but attributes the palette *direction* to the logo. The brief supplies the feeling; the config holds the values; the logo settles the palette. The render is the place all three meet, and it changes none of them.

**Graceful degradation when an input is thin:**

- **No logo concept** → §1 renders the concept line as a typographic statement only; §6 renders clear-space *placement zones*, not marks.
- **No photography direction** → §7 renders the system on labeled neutral surfaces (card, sign, screen) rather than over real imagery; samples are marked illustrative.
- **All-inferred color** → §4 renders the palette fully banded as direction (see the Provisional Convention).

A missing input degrades a section; it never fabricates content to fill one. A fabricated mockup is an anti-tell (AT-7/8/10) and fails the emit gate.

---

## The Section Anatomy — the Fixed Template

The value of this artifact over a plain Mode B page is the *fixed* template. The Layout Declaration names the Stylescape pattern with `Derivation: exact`. Section-level creativity is allowed *inside* a vignette, never in the section order or the gate. Every section maps to a brief section and a config source, and every section degrades gracefully.

| # | Section | Shows (not just tells) | Brief / config source |
|---|---------|------------------------|------------------------|
| 0 | Cover / one-line direction | The concept line set in the chosen display face at real scale, on the real page background | Brief §1 "the direction, in one line" · `tokens.typography.display` · `backgrounds.primary` |
| 1 | Concept line / "Logo Logic" | The `[attribute] + [visual concept] = solution` idea as a typographic statement. *A beat the prose brief lacks.* | Logo-system strategic idea (if Concept ran) · brief §1 |
| 2 | What this will feel like | The mood prose *set* in the real body face, measure, and line-height on the real surface | Brief §2 · `tokens.typography.body` · `spacing.content_max_width` |
| 3 | Type in use | The real pairing rendered live at display / body / label scale: a real headline, a paragraph, a caption | `tokens.typography.*` · `scale.*` |
| 4 | Color in use | The palette as *applied surfaces* (page background + text, a card, an accent doing one job), each with one line of rationale. **Inferred / provisional values marked.** | `tokens.color.*` · brief §3 · provenance |
| 5 | Composed hero / section | One real layout from a named compositional pattern, editorial and asymmetric by default | `layout.preferred_patterns` · `compositional-layout-patterns.md` |
| 6 | Logo-direction zones | Clear-space placement zones (default), or rendered marks **labeled "illustrations of the direction, not the decision"** | `heyhi-logo-system` output (logo-system boundary) |
| 7 | In real-world application | The system on 2–3 sector-plausible surfaces (a card, a sign, a screen, a header) | brief §5 imagery · `layout.*` |
| 8 | Why this fits you | The sector intersection and the sector-stretch credibility calibration | Brief §6 |
| 9 | What we're not doing | One or two anti-style contrasts, ideally a visual "not this" | Brief §7 · `tokens.color.prohibited` |
| 10 | Decision / approval gate | The decision register: locked vs. open decisions, each tied to `gate_status` / provenance | `meta.gate_status` · `meta.provisional_fields` |

Optionally, after §10, a short **links section** (the only nod to the older consolidation-hub pattern) pointing to the full brief and any prototype. Keep it to a quiet footer; the proposal *shows* the direction, it does not link to it.

---

## Grid and Structural Spec

- **One portable HTML file.** No asset server, no build step, no external stylesheet the in-app preview will drop. Everything inline so the file renders standalone and prints clean to PDF. (The older hand-built hub failed exactly here: a multi-file prototype with a relative stylesheet renders unstyled in the preview panel.)
- **Long-scroll with a sticky decision rail.** The §10 gate stays reachable from any scroll position so the client can act on it without scrolling back.
- **Real type at real scale.** Render from the config's `clamp()` scale and token values natively. The credibility move is that the client sees the *real thing* rendering, not a screenshot of design.
- **Layout Declaration.** Name the Stylescape pattern, `Derivation: exact`. Inside each vignette (§3–§7) a named compositional pattern from `compositional-layout-patterns.md` may be applied; declare it. The section order is not a creative variable.
- **Responsive and accessible** to the same standard as any ui-studio build: three breakpoints, 44px touch targets, semantic HTML, visible focus states, `prefers-reduced-motion`.

---

## The Provisional Convention — the Credibility Mechanism

Marking inferred values as *direction, not decided* is what makes the artifact read as candor rather than a defect list. It is the mechanism that earns trust before a token is locked.

**Source of truth: `meta.field_provenance[].confidence`.** Render by state:

| `confidence` | Render as |
|--------------|-----------|
| `extracted` | Plainly. This value came from the client's own assets. No marking. |
| `inferred` | **Visibly banded** "direction, not decided." A value we proposed, not one we pulled from an asset. |
| `provisional` | Appears *only* as an open decision in §10. Never shown as a finished value. |
| `failing` | Excluded from the render entirely. |

**Critical fallback — sparse or absent provenance.** Real `manual` configs are low-fidelity and do not carry a richly-populated `field_provenance` map (a Mode D config does; a hand-authored one usually does not). When provenance is sparse or absent, fall back to:

1. **`meta.provisional_fields[]`** — every path listed here is provisional. Its `confidence` enum is `[inferred, pending]` (note: this is a *different* enum from `field_provenance`'s four-value set; see `config-schema-validation-gap`). `inferred` → band as "direction, not decided." `pending` → band as "direction we'll confirm with you" (it is reconciled enough to show, but a specific lock is still open — e.g. a client palette sign-off).
2. **`meta.version`** — `0.x` means the whole config is provisional. Carry a single global note to that effect.
3. **The score band** — low `fidelity_score` is degradation input: it tells the legend these are directional estimates, not measured values.

**A quiet legend, stated once on the artifact:** *solid = from your assets · marked = direction we'll confirm.* That sentence reframes every marked value as a question the client gets to answer, not a flaw.

**`geographic-inference-palette-temperature` is load-bearing here.** A color temperature inferred from a description (a "coastal" or "warm-climate" guess) is `inferred`, and an inferred temperature **must never launder into a decided one**. The same location photographs differently across season, weather, and time of day. If color came from a description rather than an asset, it renders banded. If it came from the logo or extracted photography, it renders plainly. The marking is the difference between honesty and a guess wearing a suit.

**Visual treatment.** Banding should read as deliberate, not broken: a thin marker on a swatch, a small "direction" tag, a one-line note. Not a red error state, not a strikethrough. The goal is "we are being straight with you about what is settled," not "here is a list of what is wrong."

---

## One Direction Led, Multi-Direction Capable

**Default: render *one* fully-built direction.** Three near-identical options read as lazy, and multiple live options invite a stitched-together "Frankendesign" where the client picks a nose from A and eyes from B. Leading with one well-resolved direction converges with HeyHi's "take a position / earn the room" ethos.

Render a **second** direction only when `heyhi-style-selection` produced a genuinely distinct alternate. The distinctness guard is hard: the alternate must differ on **≥2 of {concept line, type personality, color temperature, compositional pattern}**, or it is rejected as a non-distinct variant and the artifact reverts to a single direction. Two directions are insurance, never a feature-comparison grid; a side-by-side spec table invites the small-tweaks trap and is not produced.

**Scoring the guard (operational).** Read each dimension from a fixed field, so two agents score the same pair the same way:

| Dimension | Source (per direction) | "Differs" when |
|-----------|------------------------|----------------|
| Concept line | style entry `descriptors.mood` + `imagery_approach` + `agent_context_snippet`; the logo strategic idea (§1) | the organizing idea is categorically different |
| Type personality | `token_implications.type_personality` (`slab` / `humanist` / `grotesque` / `geometric` / `serif`) | the enum value differs, or the pairing register is categorically different |
| Color temperature | `token_implications.color_temperature` (`warm` / `cool` / `neutral`) | the enum value differs (coarse; see below) |
| Compositional pattern | `layout_patterns.compositional_patterns` / `grid_preference`; config `layout.preferred_patterns` | the named compositional family differs |

`count` is the number of dimensions that differ. `count ≥ 2` renders two directions; `count ≤ 1` reverts to one with a stated reason ("alternate differs on only {dimension}; below the ≥2 threshold; reverting to a single direction"). **Precondition:** the alternate must be a genuine `heyhi-style-selection` match for the *same* brief. Distinctness is the second filter, not the first. A maximally-distinct entry that does not fit the brief never reaches the guard.

**Color temperature is a coarse axis.** Two entries can share a `color_temperature` enum value while their palettes feel completely different: a limited saturated earthy poster set and a near-achromatic ground with one rare accent are both `warm`. Read the dimension off the enum for a crisp, repeatable count. But when `count == 1` and the lone matching axis is `color_temperature` while the palette *character* is categorically different (achromatic vs chromatic, or a large saturation delta), surface the pair to the human as a judgment call rather than auto-reverting. The count stays deterministic; the override is human, never a silent count change. (`geographic-inference-palette-temperature` is the cousin rule, for where the temperature itself is an inference.)

**The two-direction layout.** When the guard renders two, the section order and the gate stay fixed; the per-direction vignettes double:

- A shared **cover**, then a **"two directions at a glance"** beat (concept line A │ B, one line each).
- **Per-direction panels** (feel, type-in-use, color-in-use, composed vignette), each rendered from *its own scoped token set*, so the two read as two systems rather than two themes.
- **Shared** §8 "why each fits" and §9 "what neither does": the brief framing, and the anti-style both directions refuse.
- A §10 register whose **lead row is "choose A or B" (the lock)**, the downstream rows (palette, type, mark, sign-off) confirmed after the choice.

Pick one direction whole; never graft one direction's type onto the other's color. No side-by-side spec-comparison table: it invites the small-tweaks trap the single-direction default exists to prevent. Worked reference render: `skill-updates/ui-studio/two-direction-stylescape-proof.html`.

---

## The Anti-Tell Emit Gate

This is the one artifact that most needs to *look designed* and is *generated*. If it trips a visual anti-tell, the pitch dies on contact. Scan the render against `ai-services/design-intelligence/visual-anti-tells.md` (AT-1 through AT-10) **before emit**, reusing the scan pattern `heyhi-prototype-audit` Layer 2 already runs. Severity is **High on the hero / cover frame**, Medium elsewhere.

Highest-risk tells for a stylescape specifically:

- **AT-2** gradient text on the cover headline (use a solid display face in a brand color).
- **AT-1** chromatic glow shadows (the config is flat; honor it).
- **AT-4** a three-equal-column card row standing in for "color" or "type" (compose, do not template-fill).
- **AT-7 / AT-8 / AT-10** placeholder or fabricated content in the §7 mockups — invented metrics, broken images, "Acme Inc." A mockup must use real, labeled-illustrative content or a clearly-marked placeholder, never fabricated data presented as real.

A matched tell with no documented carve-out is a defect; fix it before the artifact leaves. The artifact that sells taste has to have taste.

---

## The Decision Register → Mode D Handoff

The §10 gate is not decoration. It surfaces the locked and open decisions, read from `meta.gate_status` and the provisional signals, and **its output *is* the `design-system-onboard` Mode D handoff manifest.**

Each *locked* row maps 1:1 to a Mode D precondition (`heyhi-style-brief § Handoff to Mode D`):

| Decision register row | Mode D precondition |
|-----------------------|---------------------|
| Direction locked? | The direction lock itself (`direction_lock_confirmed`) |
| Named display + body faces? | Typography confirmed, or deferred to a typeface-selection step |
| Color asset-derived vs inferred vs pending? | Color source settled (asset values, or extraction scheduled) |
| Logo direction chosen? | The mark direction (feeds the logo build, not Mode D token extraction directly) |
| Sector-stretch calibration agreed? | Sector adaptation recorded |

**No row may be left open after approval.** An open row that survives "yes" is a token build running on an unresolved input. The register makes "looks nice" into signed, answerable decisions; that is the whole reason the proposal exists.

---

## Definition of Done

- A client can *approve or redirect* the direction in one read. The proposal makes the decision easy, not the deck long.
- Every *locked* row in the register maps 1:1 to a Mode D precondition; no open row survives approval.
- The render passes the AT-1..AT-10 scan and WCAG AA on every rendered pair. The artifact that sells taste has taste.
- Inferred and provisional values are unmistakably distinct from decided ones (the honesty test), with graceful degradation: no logo concept renders placement zones; no photography renders labeled samples; all-inferred color renders fully banded.
- It renders from a live provisional config with no hand-fixups. The output is a *generated* artifact, not a hand-assembled one.

---

## Output

The rendered artifact and any companion notes land in the instance's gitignored engagement folder, in the **main workspace**, never a worktree copy:

```
<workspace root>/<engagement folder>/deliverables/identity-proposal/
```

One self-contained `index.html` that opens in any browser and prints clean to PDF. Reference the engagement generically in every tracked artifact and commit message (the hermetic seal); the client name lives only in the gitignored output and in `project-state.yaml`.

---

*HeyHi Internal Use Only. Bay Design `heyhi-skills/ui-studio/references/`. Created 2026-06-10. Updated 2026-06-11: § One Direction Led gained the operational guard scoring (dimension→field table, selection-match precondition, color-temperature coarseness tie-breaker, and the two-direction layout), promoted from the distinctness-guard validation (skill-updates/ui-studio/).*
