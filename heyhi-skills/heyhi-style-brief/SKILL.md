---
name: heyhi-style-brief
description: >-
  Turn a selected style direction into a client-approvable design direction brief — the
  human-readable artifact a non-designer client reads and approves before any tokens are
  built. Consumes the output of heyhi-style-selection (a Mode A recommendation package or a
  Mode B style_pre_classification YAML) plus the matched style-reference-library entry, and
  produces plain-language prose: what the design will feel like, the color direction in
  non-technical terms, what the typography will do, what imagery to expect, why the style
  fits the client's sector, and what approval unlocks. Triggers: "write a style brief for
  [client]," "turn this style recommendation into a brief," "write up the design direction
  for client approval," "the client needs to approve the direction," "design direction
  brief," "draft the direction for sign-off." Runs after style selection and before
  design-system-onboard Mode D. NOT for matching a moodboard to a style (use
  heyhi-style-selection — that runs first and produces this skill's input). NOT for a single
  logo or wordmark (use heyhi-logo-system — it owns the mark; this skill owns the whole
  visual language). NOT for extracting or validating tokens (use design-system-onboard for
  Mode D extraction, heyhi-style-to-token-reviewer for token-set coherence). The brief is a
  client explanation, not a schema summary and not the token build.
version: "1.2.1"
updated: "2026-10-13"
changes: "v1.2.1 (2026-10-13): Generalized for the Sheerline scaffold: instance data (brand defaults, client/engagement history, owner names, ratified values) moved to instance-only files or neutral wording; method unchanged. v1.2.0: Added a pre-signature gate to After Delivering. If the engagement's NDA or contract is not yet signed, the brief is a draft, not a delivery — producing it internally is allowed, shipping it to the client is gated on signatures. Source: skill-updates/heyhi-style-brief/v-next-edits-2026-06-10-pre-signature.md, promoted per the skill-updates protocol."
---

# Style Direction Brief

Translate a chosen style direction into a brief a client can read and approve. One invocation = one brief, for one named direction, ready to put in front of a non-designer for sign-off.

This skill fills a real gap in the Design Systems Build pipeline. Style selection produces a *designer-facing decision document* — vocabulary-backed, scored, with anti-style contrasts. Token extraction (Mode D) needs an *approved* direction to build against. Between them sits a missing artifact: the thing the client actually reads and reacts to. This skill is that artifact.

```
heyhi-style-selection  →  heyhi-style-brief  →  design-system-onboard (Mode D)
   (which style?)          (client approves)        (build the tokens)
   designer-facing         CLIENT-FACING            agent-facing
```

The brief is an approval gate, not a recap. Its job is to let a client say "yes, that's us" — or "not quite, here's what's off" — before a single token is built. Catching a direction mismatch here costs a conversation. Catching it after Mode D costs a rebuild.

An approved brief can also feed a **ui-studio Identity Proposal** render: the rendered companion to this prose brief, a client-facing stylescape that *shows* the same direction the brief describes. The brief is the voice; the proposal is the eye; they ship as one approval moment. See `heyhi-skills/ui-studio/SKILL.md § Identity Proposal`. It is optional, never a prerequisite for Mode D.

---

> **Exit Gate (Flavor A).** This skill closes through the canonical Exit Gate — see `CLAUDE-SESSION-RULES.md § Exit Gate`. Required headers, in order: `## Fixes Applied`, `## Smoke Test`, `## Next Session Prompt`. Empty headers are visible failures.

---

## Before You Start

Load these in order. Earn the Room applies — load the one matched style entry, not the whole library.

1. **The style-selection output** — the input this skill consumes. One of:
   - A **Mode A recommendation package** (the client-facing prose with five components). Preferred — it already carries the imagery direction, sector note, and anti-style contrasts in close-to-client language.
   - A **Mode B `style_pre_classification` YAML** (structured). Workable — translate the fields to plain language yourself.
   - A **named style handed over directly** by a designer ("we're going with Community Platform"). Workable — read the library entry and the moodboard for the signal trace.

2. **The matched style entry from `ai-services/design-intelligence/style-reference-library.md`** — load only the entry (or entries, for a composite) named by the selection. The entry's `visual_characteristics`, `token_implications`, `industry_fit`, and `agent_context_snippet` are the source you translate from. Do not load the full library.

3. **`ai-services/design-intelligence/style-descriptor-vocabulary.md`** — the summary keyword list (~100 tokens). Use it to translate vocabulary terms into plain client language. Full load only if a descriptor needs careful unpacking.

4. **`ai-services/design-intelligence/research/designer-questioning-methodology.md`** — load when the engagement produced constraint documentation, anti-descriptor lists, or a user emotional-state map. This is what makes a brief land as a *client explanation* rather than a schema summary: it lets the brief speak to what the client said they needed, in their words.

5. **The instance's own voice skill** (in HeyHi, `heyhi-skills/heyhi-voice/SKILL.md`) — every word of the brief is client-facing copy. The voice system governs it. Load before writing, not after.

Do not load `moodboard-template.md`, `compositional-layout-patterns.md`, or `grid-layout-examples.md` by default — composition and grid scaffolding are Mode D and build-phase concerns, not what a client approves in a direction brief. Load only if the client explicitly asked about page structure.

---

## Input Formats

Assess what you were handed before you start.

- **Mode A package (preferred):** Translate its five components into the brief sections below. Most of the work is tone — moving from "vocabulary-backed rationale" register to "here's what this will feel like" register.
- **Mode B YAML:** Each field maps to a brief section (see the translation guide in `reference.md`). Watch the `designer_confirmation_needed` list — every item there becomes an explicit open decision in the brief.
- **Named style only:** Read the library entry and the moodboard. Reconstruct the signal trace before writing, so the "why this fits you" section is grounded, not asserted.
- **Only a client name ("write the brief for [client]"):** Ask exactly one question — *"Which style was selected, or should I pull the style-selection output?"* — then proceed. Do not ask more than one.
- **No style selected yet:** Stop. The brief is an approval artifact and requires a resolved direction. Route back to `heyhi-style-selection` (or `gate0-facilitation-guide.md` if multiple directions are still live). Do not invent a direction to write a brief around.

---

## Procedure

### Step 1: Confirm the direction is locked

A brief approves *one* direction. Confirm you have a single named style, or an explicitly labeled composite (Style A governs X, Style B governs Y). If the selection output still lists alternates as live options, or confidence is `low`, the direction is not ready for a client approval brief — surface that and route back to selection or Gate 0. Writing a brief over an unresolved direction asks the client to approve a coin-flip.

### Step 2: Pull the source signals

From the style entry and selection output, gather the raw material the brief translates:

- **Mood** — the `descriptors.mood` terms (and the `anti_mood` terms, for the "what we're not doing" section).
- **Color** — `token_implications.color_temperature` and `visual_characteristics.color_approach`; note whether color is asset-derived, inferred, or pending.
- **Typography** — `type_personality` and `typography_approach`; note whether named typefaces are confirmed or still personality-only.
- **Imagery** — `visual_characteristics.imagery_approach` (the Category 8 register) and the moodboard's photography direction.
- **Surface and motion** — `surface_treatment` and `motion_approach`, translated to felt qualities (soft and tactile / crisp and immediate), not values.
- **Sector fit** — `industry_fit.natural | stretch | avoid` for the client's sector.
- **Sector of the reference exemplars** — note where the moodboard's reference brands actually come from. If they are all from a different sector than the client (e.g., hospitality / CPG references for a trade-service client), treat it as a **stretch signal even when the `industry_fit` aesthetic match scores clean** — the references prove the *craft*, not the *category fit*.
- **Client's own words** — from the questioning methodology: stated needs, constraints, anti-descriptors, emotional-state notes. These anchor the brief to what the client actually asked for.

### Step 3: Translate to client language

This is the craft of the skill. The client is not a designer. Translate every term:

- **Feeling first, mechanism second.** Lead with what it will feel like; explain the how only as far as it earns the feeling.
- **No jargon.** No "tokens," "humanist grotesque," "Major Third 1.25x," "12-column grid," hex codes, or px values in the brief body. "Warm and grounded" beats "warm color_temperature." "Clear, with a quiet confidence" beats "humanist sans at 1.25x."
- **Describe what they'll see.** A client approves an experience, not a spec. "Rounded cards with a soft shadow, so the interface feels approachable" — not "border-radius 12–20px, shadow_depth: subtle."
- **Keep their words in the room.** Where the client said "we want to feel trustworthy but not corporate," reflect that language back and show how the direction answers it.

The descriptor → plain-language translation table is in `reference.md`. Use it; do not freehand technical terms into client copy.

### Step 4: Write the brief

Use the section structure in `reference.md`. The shape:

1. **The direction, in one line** — the `agent_context_snippet`, rewritten plainspoken. The sentence the client remembers.
2. **What this will feel like** — the mood, in plain terms, tied to what the client said they wanted.
3. **Color** — the temperature and character, described not specified. No hex.
4. **Typography** — what the type will *do* for them (clarity, warmth, authority), not its classification.
5. **Imagery and photography** — what to expect and, where relevant, what to start gathering. Plain translation of the Category 8 register.
6. **Why this fits you** — the sector intersection, in client terms. For a `natural` fit, confirm cleanly. For a `stretch`, name honestly what adapts and why it still works. **When the reference exemplars come from a different sector than the client** (the stretch signal from Step 2), name it explicitly here and in the "what we're not doing" section, and add a calibration guardrail tied to the client's purchase type: a high-consideration, trust-driven purchase (a multi-thousand-dollar service, a regulated product) needs the direction to read credible alongside characterful — not characterful at the expense of credible. State the guardrail as a felt quality the client can react to ("bold and memorable, but unmistakably dependable"), not as a spec.
7. **What we're not doing** — one or two anti-style contrasts in plain language. Naming the road not taken sharpens a "yes" and preempts second-guessing.
8. **What happens when you approve** — the next step (the token build / Mode D), and the specific decisions this approval locks.

**Length.** The brief is short. Default to a **client-facing length of 400–550 words**. Use 250–350 for an internal approval pass (the studio lead or the design team reviewing before the client sees it), and up to 650 only for a standalone written brief appended to a proposal. The detail lives in the build; the brief carries the decision.

**Motion and interaction feel.** For any engagement with a digital touchpoint (website, app, dashboard, prototype), fold the surface and motion qualities into "What this will feel like" or the relevant section — how the interface responds (calm and unhurried, crisp and immediate, responsive with care), translated to feel, never to values. If the engagement is print or brand-only, omit it. When unclear, include it briefly: a client who turns out to need it is better served than one whose brief omitted it.

### Step 5: Surface the open decisions the approval must resolve

The brief is also the moment to make hidden decisions explicit. Anything the selection flagged as unresolved — typography not yet locked to named typefaces, imagery direction provisional, a sector stretch needing a judgment call, color still pending asset extraction — appears in the brief as a clear checkpoint, not buried. These are exactly the items Mode D needs settled before it can run. Frame them as approval questions the client can answer, e.g. "We've set the direction as warm and humanist; the specific typefaces are the next choice — do you want us to bring you two options, or run with our recommendation?"

### Step 6: Voice pass, then present

Run the instance's voice skill (in HeyHi, `heyhi-voice`) over the full brief before presenting. Confirm:
- No banned words; no "AI" as a standalone word.
- No pricing anywhere — the line is "let's talk about what fits."
- Em dashes: maximum 2 per publishable section (the brief is one client-facing document; if it is delivered as a multi-part package, the limit applies per part).
- The brief reads as something a client says yes to, not a schema someone exported.

Deliver as readable prose (or a short formatted document), never as a YAML block or a fields table.

---

## Handoff to Mode D

An approved brief locks the inputs `design-system-onboard` Mode D needs. On approval, confirm these are settled (they map to the Mode B `style_pre_classification` fields):

- **Named style** (or composite split) — confirmed.
- **Color source** — asset-derived (with the extracted values) vs inferred vs pending; if pending, asset extraction precedes Mode D.
- **Typography** — named display and body faces confirmed, or explicitly deferred to a typeface-selection step before Mode D.
- **Imagery register** — the Category 8 terms confirmed, or flagged provisional.
- **Sector adaptation** — if the fit was a stretch, the agreed adaptation is recorded.

If any of these is still open after approval, name it in the handoff — Mode D should not run token extraction on an unresolved input.

---

## After Delivering

- **If the engagement's NDA or contract is not yet signed, the brief is a DRAFT, not a delivery.** Producing the internal draft is allowed; shipping it to the client is gated on signatures. Mark the file `status: draft`, add a release-gate line ("hold for release until NDA + contract SIGNED"), classify the working file `confidential`, and note that the client-facing body becomes unclassified on delivery. Do not present the brief to the client until the gate clears. (This is the style-brief instance of the standing rule at `OPERATING_PRINCIPLES.md` § Document classification, "Pre-signature client deliverables" — the same gate applies to logo concepts, discovery materials, workshop content, and style-selection output.)
- Present the brief in conversation first. Create a file only when asked to save it.
- On save: `<engagement folder>/style-brief-[style-name].md` in the instance's engagement folder (self-engagements and paid engagements may use separate folders). Engagement folders are gitignored — from a worktree, write to the main workspace copy (`<workspace root>/<engagement folder>/...`), never the worktree's copy (see CLAUDE.md § worktree split-routing).
- A routine brief does not warrant a decision-log entry; log only if a new structural or formatting decision was made.

---

## Smoke Test

Before delivering any brief, verify:

- [ ] The direction is a single named style or an explicitly labeled composite — not an unresolved set of alternates
- [ ] Every brief section translates a real signal from the style entry or selection output — nothing asserted without a source
- [ ] No technical vocabulary in the client-facing body: no "token," type-classification jargon, hex codes, px values, grid-column counts, or schema field names
- [ ] The "why this fits you" section reflects the client's sector and, where available, their own stated needs
- [ ] At least one honest "what we're not doing" contrast is included
- [ ] Every unresolved item from the selection (typography, imagery, color source, sector stretch) appears as an explicit approval checkpoint, not omitted
- [ ] The "what happens when you approve" section names the next step (token build / Mode D) and what the approval locks
- [ ] Voice skill run clean: no banned words, no standalone "AI", no pricing
- [ ] Em dashes: maximum 2 per publishable section
- [ ] The brief is prose a non-designer can read and react to — not a YAML block, not a fields table

---

## Source Material Reference

| File | When to load |
|------|-------------|
| The style-selection output (Mode A package / Mode B YAML / named style) | Always — this is the input |
| `ai-services/design-intelligence/style-reference-library.md` | Always — the matched entry only, not the full library |
| `ai-services/design-intelligence/style-descriptor-vocabulary.md` | Always — summary keyword list, for descriptor → plain-language translation |
| `ai-services/design-intelligence/research/designer-questioning-methodology.md` | When the engagement produced constraints, anti-descriptors, or an emotional-state map |
| The instance's voice skill (in HeyHi, `heyhi-skills/heyhi-voice/SKILL.md`) | Always — the brief is client-facing copy |
| `reference.md` (this skill) | Always — brief template + descriptor translation guide |
| `gate0-facilitation-guide.md` | Only when the direction is not locked and must be resolved first |

---

## Exit Gate Required Headers (bottom-of-skill bracket)

This skill closes through the Exit Gate Flavor A (`CLAUDE-SESSION-RULES.md § Exit Gate`). Before declaring done, confirm every required header below contains real content, not a claim:

- `## Fixes Applied`
- `## Smoke Test`
- `## Next Session Prompt`

If any header is empty or contains advisory prose ("I checked the voice") instead of a concrete artifact, the gate has not been satisfied. Apply fixes until clean — then emit.

---

*HeyHi Internal Use Only. Bay Design LLC. July 2026 · v1.2.0 (updated 2026-07-10).*
*Source material: style-reference-library.md · style-descriptor-vocabulary.md · designer-questioning-methodology.md · heyhi-voice/SKILL.md*
*Classification: internal*
