---
name: microcopy-states-writer
description: >-
  Write the microcopy for every state of a screen — the per-state strings,
  drafted against a voice system a human has already confirmed, into the slot
  each state actually carries. Runs the mechanical work: read the confirmed
  voice block, read the state list (the interaction-inventory sidecar's
  copy_slot rows, or a human-written list in the same shape), map each state
  to its UX-writing slot, draft one candidate string per slot row against the
  voice and the per-slot anatomy, attach constraints (length, variables,
  plurals, placement), run the states-copy doctrine per string (a typed next
  step or a flag; the condition from the row's trigger or a flag; a real
  loading expectation; the data-view floor), hold every claim, log terms to a
  candidate glossary, and flag dead-end errors, unsupplied conditions, and
  missing strings. Triggers: "write the microcopy for every state", "microcopy
  for each state on this screen", "draft the strings for the loading and error
  states", "the copy for every state in this inventory", "write the empty,
  loading, and error copy", "microcopy set for this screen". Produces a
  Microcopy Set where which copy ships, the tone call on a flagged string, and
  the terminology ruling ship EMPTY behind a named human gate, and every string
  is a labeled candidate. NOT for deriving or authoring a voice system, or
  linting copy for flattening (use voice-system-author — that defines the voice
  and runs the lint; this drafts the strings against a voice already
  confirmed). NOT for HeyHi's own fixed brand voice — drafting the about
  page, an email, a proposal (use heyhi-voice; this writes a client's
  product strings, never HeyHi's prose). NOT for another owned brand's in-product
  prose that has its own dedicated voice skill (use that skill). NOT for enumerating, inventorying, or mapping the
  state machine a screen has (use interaction-inventory — that lists the
  states; this fills the strings the list carries; with no list, supply one).
  NOT for auditing a built prototype for readiness or missing interactions
  (use heyhi-prototype-audit — is the copy on-config, are the states wired;
  this drafts the strings before the build). NOT for content for this week's
  calendar — the essay, a Note, or a LinkedIn post (use heyhi-content-writer).
  NOT for
  building the page, the interface, or the interaction itself (use heyhi-ui-ux
  for HeyHi pages, ui-studio for client UI — they consume the strings; this
  drafts them). NOT for alt text or accessible names for images and controls
  (use heyhi-a11y-annotation — designer-judged accessibility text, not state
  strings). NOT for deciding which candidate ships, ruling a flagged line
  on-voice, or ruling on a term (the human's, at the named gate).
version: "0.1.0"
updated: "2026-09-05"
status: "deployed 2026-09-05 — heyhi-skills/microcopy-states-writer/ (Tier 1, buildable-now, self-application-first); registered in the main registry and the Sheerline area-3 subset registry, promoted in the second Bucket B convergence + promotion pass (staged #787, cleared by the instance owner 2026-09-05). Area 3 coverage partial -> covered. Sheerline area 3 (Content Design / UX Writing), P3, build class N. Spec: plans/plan-sheerline-p3-content-design-2026-09-05.md § 3 / § 4 / § 5. Foundation: sheerline/os/foundations/content-design/FOUNDATION.md."
classification: HeyHi Confidential
---

# Microcopy States Writer

**Sheerline area 3 (Content Design / UX Writing) · P3 · Tier 1 buildable-now, self-application-first · build class N · the copy half of the states seam.** A team has a screen with a real state list and a voice they have confirmed, and forty strings to write. This skill does the chartered drafting job: it reads the confirmed voice block and the state list, maps each copy-bearing state to the slot it carries in the UX-writing taxonomy, drafts one candidate string per slot row against the voice and the per-slot anatomy, attaches each string's constraints, runs the states-copy doctrine on each string (a typed next step or a flag; the condition from the row's trigger or a flag; a real loading expectation; the data-view floor), holds every claim behind confirmation, logs every product term to a candidate glossary, and flags every dead end, unsupplied condition, and missing string. It stops where a human must choose which string ships, resolve a flagged tone call, rule on a term, or confirm a claim.

The skill is a **consumer three times over**. It consumes the **voice** (`voice-system-author` derives it; this skill never re-derives a voice and never runs the flattening lint). It consumes the **state list** (`interaction-inventory` enumerates it; this skill never enumerates the interaction structure). And it consumes the **taxonomy** (the eight core slots plus two extended in `voice-system-author/references/voice-system-template.md` Part 3; this skill names the slot, it does not invent one). What it adds is the mechanical middle: per state, which slot; per slot, a candidate string; per string, the doctrine.

**The boundary this skill obeys (Sheerline, absolute).** A structured artifact with explicit empty judgment slots, a named human gate, and provenance labels on anything synthetic. *Which copy ships (accept, rewrite, or ask for alternates), the tone call on a flagged string, the terminology ruling, and whether a feeling may be named are the empty slots*, and the two the voice gate already holds (the voice definition; "does this sound like them") are inherited: this skill refuses to certify a string on-voice. Drafting a candidate against a stated voice is mechanical; deciding it ships is judgment. A version of this skill that picks the string, certifies a string as on-voice, derives the voice or the state list because none was supplied, supplies a failure cause the inputs never carried, or ships a claim the client has not confirmed has exceeded its charter. Flags inform; they never gate.

> **This skill closes through the Exit Gate (`CLAUDE-SESSION-RULES.md § Exit Gate`).** See the bottom-of-skill bracket.

---

## Routing — disambiguation with sibling skills

| If the task is… | Use |
|---|---|
| "Write the microcopy / the strings for every state of this screen" | **this skill** |
| "Derive this client's voice; build a voice and tone system; audit this copy for flattening" | `voice-system-author` (the seam is **layer**: it derives the voice and one pattern per slot, and owns the lint; this drafts the strings for a screen's states against that voice) |
| "Inventory / enumerate the states this screen has" | `interaction-inventory` (the seam is **layer**: it lists the states and leaves each copy slot empty; this fills the string) |
| "Write HeyHi's about page / this email / this proposal" | `heyhi-voice` (the seam is **ownership**: HeyHi's fixed voice; this skill consumes an owned voice only as a *supplied* system when the instance runs it on its own work) |
| "Write the onboarding modal" for another owned brand with its own voice skill | that brand's voice skill (ownership: an owned second voice) |
| "Audit this built prototype; is the copy on-config; what interactions are missing" | `heyhi-prototype-audit` (the seam is **temporal**: it audits what got built; this drafts before the build) |
| "Write this week's content / the essay / a Note" | `heyhi-content-writer` (HeyHi's calendar, not product strings) |
| "Build the page / the loading state / the interface" | `heyhi-ui-ux` (HeyHi pages) / `ui-studio` (client UI); they consume the strings |
| "Write the alt text / the accessible names" | `heyhi-a11y-annotation` (the seam is **object**: designer-judged accessibility text, not state strings) |
| Which string ships, whether a flagged string is on-voice, what the product calls a thing | **the human** (this skill's named gate) |

**When a request is actually for an incumbent, route away.** "Derive their voice" is `voice-system-author`. "Enumerate the states" is `interaction-inventory`. "Draft copy for the about page" is `heyhi-voice`. This skill activates only when there is a confirmed voice to write against and a state list to write into.

---

## Step 0: Improvement hook check

Retrieve any recurring corrections for content / copy work (`retrieve_design_corrections`, or the Sheerline `os/corrections/` registry). Fold a match into the pass. **This starts empty for area 3:** the served corrections carry no `content`, `copy`, or `voice` category, so this normally finds nothing. The hook is wired from day one so `insight-activation` can file the first content correction from this skill's own runs; skip silently until then.

## Step 1: Load context

Load only what the task needs (Earn the Room).

1. **The voice block** — `voice-system-author`'s Author-mode artifact with its **confirmed** slots filled (the one-line voice, the confirmed attributes, the calibration axis and where it sits for in-product and error copy). When the instance runs this skill on its own work, the supplied system is the instance's own voice file, consumed exactly as a client's confirmed block would be. **If the confirmed slots are empty, proceed only in doubly-candidate mode**, stated in the artifact header: every string is `[candidate — voice unconfirmed]`. Never promote a candidate voice to confirmed.
2. **The state list**, in the inventory's sidecar shape (`heyhi-skills/interaction-inventory/inventory-schema.json`): either the deployed `interaction-inventory`'s sidecar for the screen (its `copy_slot` rows are the rows this skill writes), or a **human-written** fallback list in the same shape (`source.kind: list`; each element `provenance: from-list`; the four minimal fields map as `references/states-copy-canon.md` § 7 says). If neither exists, **ask for one**. Never enumerate the screen's states, even when they are obvious. When a built prototype exists, the human may cross-check the list's completeness against `heyhi-prototype-audit`'s Step 2 scope count; the count is a number and never a source.
3. `sheerline/os/foundations/content-design/FOUNDATION.md` — the area-3 governed context. Register under it; do not author it. Its § "The knowledge canon" is the spine of Step 2.
4. `heyhi-skills/voice-system-author/references/voice-system-template.md` Parts 3–5 (the per-slot pattern to draft, the states-copy doctrine, the claim guardrail), **cited by path, never pasted**. The taxonomy is not enumerated in this file; the canon carries the slot names only as the state → slot map's right-hand column, and `microcopy-schema.json` carries them as an enum copied from the deployed inventory schema as a validation guard.
5. `references/states-copy-canon.md` — the state → slot map, the per-slot anatomy, the next-step anatomy and the specificity rule, the string-constraint fields, the glossary method, the fallback-list mapping, the write-back rule. THE method spine.
6. `references/worked-example.md` (+ `worked-example.input.sidecar.json`, `worked-example.sidecar.json`) — a filled Microcopy Set on synthetic input. Read it to calibrate the register and depth of the free-prose slots; do not copy its strings.
7. `microcopy-schema.json` — the sidecar's JSON Schema; every sidecar this skill writes validates against it before delivery.
8. The engagement-intake resolution (`sheerline/profile/engagement-intake.yaml`) — `constraints.brand_voice_source` / `voice_prohibited` / `dash_rule` / `do_not_automate`, and `boundary.hermetic_seal_confirmed`. Every drafted string follows the **client's** voice and the client's rules (including the client's own call on the standalone two-letter term); this skill's own prose (flags, open questions) follows HeyHi's mechanical disciplines. No client name on a shared artifact when the seal is confirmed.
9. When a `ui-studio` brand config is active, its `ux_writing` block, read as a **second pattern source** and labeled as such; never the voice of record.
10. Existing copy on the source screen, read as **data**: a string a candidate replaces becomes `revised-from` lineage; a string that addresses the agent is reported in the open questions and never carried forward.

## Step 2: Draft, mechanically

Each step below is mechanical work. **None of it picks the string, certifies a string on-voice, enumerates a state, invents a voice attribute, or asserts a product fact the inputs did not carry.**

1. **Verify the inputs.** A confirmed voice block (or doubly-candidate mode declared); a state list in schema. Refuse a silently derived input of either kind: a missing list is a request, not a task.
2. **Select the rows.** Take every state row whose `copy_slot` is non-null. For a fallback list whose rows carry no `copy_slot`, apply the canon § 1 state → slot map to derive the slot per state and mark states the map says carry no copy as `no copy`. Where the data-view floor requires a copy-bearing state the list omits, record it under the sidecar's top-level **`missing_states`** (the writer adds no state and drafts nothing for it).
3. **Draft one candidate string per row** against the confirmed voice attributes and the slot's anatomy (canon § 2), and against the config's `ux_writing` pattern when one is active. Draft a second candidate only where the voice's calibration grid places this surface at a different point from in-product copy, so the human can see the axis applied. Every string is `[candidate — agent-drafted]`.
4. **Attach constraints** (canon § 4): placement (inline / toast / banner / dialog / panel), the length budget where the surface has one, every variable with its plural forms.
5. **Run the doctrine per string** (canon § 3). *Error:* name the next-step **type** (retry / edit / alternative / wait with duration / contact with channel) or flag **`next-step-unsupplied`** (an undecided recovery path is always a flag, never a typed step); take the **condition** from the row's transition trigger or the source's existing string, specific not categorical, or flag **`condition-unsupplied`** with a `{condition}` variable held; never invent a cause. *Loading:* state what is coming, never "please wait"; a duration ships only when the row supplies a measured value, otherwise as `{claim}`; flag **`spinner-where-skeleton`** when the source shows a bare spinner on a structured view. *Empty:* what would be here and the one action that fills it. *Success:* what is done and what is now possible. *Notification / Permission:* the anatomy's parts, each present.
6. **Hold every claim** (canon § 5): any SLA, guarantee, timeframe, uptime, security, compliance, or performance number, and any price or rate, moves to the guardrail as `NEEDS CLIENT CONFIRMATION`; the string keeps the *shape* with a `{claim}` variable.
7. **Log terms** (canon § 6): every product term to the candidate glossary; flag a term the source uses two ways. No ruling.
8. **Feeling check:** a string that names what the user feels is tagged **`empathy-simulated`** for the human's ruling.
9. **Open questions + near-misses.** What the inputs do not answer and what you would ask the content lead (each a question); the strings considered and set aside. Traces and questions, never verdicts.

## Step 3: Produce the Microcopy Set (+ the sidecar)

Output this exact structure, and write the sidecar (`microcopy-schema.json` shape) beside it. The three judgment slots stay empty by construction.

```
# Microcopy Set — [screen / component set]
Voice: [voice-system ref · confirmed: yes | CANDIDATE-ONLY (doubly-candidate mode)]
States: [inventory sidecar ref | fallback list: from-human, inventory-shaped (source.kind: list)]
Drafted: [date]   Intake: [brand_voice_source · dash_rule · sealed: yes/no]

## Strings (one row per copy-bearing state; every string a candidate)
| Element | State | Slot | Candidate string [candidate — agent-drafted] | Constraints | Doctrine | Lineage |
| Save    | loading | Loading | "Saving your changes." | inline · ≤40ch · none | expectation: set ✓ | new |
| Save    | error   | Error   | "The save timed out. Try again." | inline · ≤80ch · none | next-step: retry ✓ · condition: from trigger ("request timed out") ✓ | revised-from: "Error" |
| Results | empty   | Empty   | "No results yet. Add your first {item}." | panel · ≤60ch · {item}: sing/pl | action: named ✓ | new |
| Results | error   | Error   | ⚠ FLAG next-step-unsupplied — recovery path undecided (see open questions) | | | |
| Export  | error   | Error   | "The export failed: {condition}. Try again." ⚠ condition-unsupplied | inline · {condition}: held | next-step: retry ✓ · condition: NOT in row | new |
Legend: ✓ = doctrine part met · ⚠ = a flag for the human · rows the state list marks `no copy` are omitted, not invented

## Flags (findings for the human, never verdicts)
- next-step-unsupplied: [element/state] — the recovery path is a product decision, not a copy one
- condition-unsupplied: [element/state] — no trigger on the row and no cause in the source; {condition} held, not invented
- spinner-where-skeleton: [element/state] — the source shows a bare spinner on a structured view
- missing-string: [element/state] — a copy-bearing state the list carries with no source string and no draftable slot
- empathy-simulated: [element/state] — the string names a feeling; ruling needed on whether the product may say it

## Missing states (the data-view floor's cross-check; nothing added, nothing drafted)
- [element / view state] — the floor requires this copy-bearing state and the supplied list omits it (sidecar `missing_states`)

## Claim / SLA guardrail (held for confirmation; nothing here is copy)
- "{claim}" in [element/state]: [the held assertion]   status: NEEDS CLIENT CONFIRMATION

## Candidate glossary (terms and conflicts; no rulings)
| Term | Where | Candidate definition | Conflict seen |

## Open questions for the team (questions, not judgments)
## Near-misses and unchecked territory (traces, no verdicts)

## ⛔ Which copy ships — NEEDS HUMAN
   Per row: accept the candidate / rewrite it / ask for alternates. Nothing above is final until marked here: ____________________

## ⛔ Tone calls on flagged strings — NEEDS HUMAN
   Each ⚠ above resolved, in the client's voice: ____________________

## ⛔ Terminology rulings — NEEDS HUMAN
   Each glossary conflict resolved: ____________________

## Named gate
Sign-off owner (content lead / brand owner): ____________________  Date: ______
No string ships, and no flagged string is resolved, until this line is signed by a human.
Voice-definition sign-off is inherited from the voice system's own gate; if that line is unsigned, this set is candidate-only twice over.
```

**The set is done when** every copy-bearing state in the supplied list has a row (a string or a flag, never an omission), every string carries a slot, constraints, a doctrine result, and lineage, every claim sits in the guardrail, every term is in the glossary, the sidecar validates against `microcopy-schema.json` and its `judgment` / `gate` blocks are null, and the three ⛔ slots plus the gate are still blank.

**The sidecar and the write-back.** The sidecar keys each string by (`element_id`, `state`), which map to the inventory's `elements[].id` and `states[].name`; `missing_states` sits beside `strings[]` and is never merged. A consumer merging the sidecar into the inventory sidecar sets only `copy_slot.string` on matching rows and copies `taxonomy_slot` in the inventory's spelling. The merged document is a **proposal** the inventory's owner applies; as of interaction-inventory v0.1.2 the inventory schema types `copy_slot.string` as `string | null`, so a merged document validates against it (the writer's sidecar is still validated against `microcopy-schema.json`; canon § 8).

## Step 4: Pre-flight verification

Confirm: no string was promoted from candidate to chosen and no flagged string was silently rewritten to pass; no state was enumerated by the writer (every `strings[]` (`element_id`, `state`) pair is a member of the supplied list's non-null `copy_slot` rows); no voice attribute was invented and no candidate voice was promoted; no cause, duration, or fact appears in a string that the row's trigger, the source, or the client did not supply; every claim is in the guardrail, none in a string; every variable has its plural forms; every string carries `[candidate — agent-drafted]` plus lineage; an undecided recovery path is a `next-step-unsupplied` flag, not a typed step; the ⛔ slots are empty and the gate unsigned; the sidecar validates (`python3 -c "import json, jsonschema; jsonschema.validate(json.load(open('<run>.json')), json.load(open('microcopy-schema.json')))"`) and its `judgment` / `gate` are null; the client's voice per intake, `dash_rule` honored, no client name when sealed; this skill's own prose passes the mechanical scan (no standalone two-letter term, no banned words, read-aloud clean).

---

## What is explicitly out of scope

- **Which copy ships, the tone call on a flagged string, the terminology ruling, whether a feeling may be named.** Empty by construction. The set lays out candidates and flags; the human chooses and signs.
- **Deriving the voice, or certifying a string on-voice.** `voice-system-author` derives; its Audit mode lints on request; the "does this sound like them" call is the human's. This skill writes against a voice already confirmed and never runs the lint.
- **Enumerating the states.** `interaction-inventory` (deployed) lists them; a human writes a fallback list in the same shape. This skill never adds a state, even when the floor says one is missing (that is the `missing-state` flag).
- **HeyHi's own prose** — `heyhi-voice`; **another owned brand's** — that brand's voice skill; **HeyHi's calendar** — `heyhi-content-writer`.
- **The accessibility text** (alt text, accessible names, ARIA) — `heyhi-a11y-annotation`; this skill writes the string into the slot A.3's hook names and emits no ARIA.
- **Auditing the built prototype** — `heyhi-prototype-audit`. **Building the screen** — `heyhi-ui-ux` / `ui-studio`.
- **Localization** (v1): the constraint fields exist so a later locale pass has something to read; this skill drafts in the engagement's one language and says so in the header.

---

## Exit Gate Required Headers (bottom-of-skill bracket)

This skill closes through Exit Gate Flavor A (`CLAUDE-SESSION-RULES.md § Exit Gate`). Before declaring done, confirm every required header holds real content:

- `## Fixes Applied` (or the delivered Microcopy Set + its sidecar)
- `## Smoke Test` (the Step 4 pre-flight checks, pasted)
- `## Next Session Prompt`

If a string was marked final, a flagged string was certified on-voice, a state was enumerated by the skill, a cause was invented, or any ⛔ slot is filled, the gate has **not** been satisfied.

---

*HeyHi Confidential. Sheerline area 3 (Content Design / UX Writing), P3, build class N. Tier 1 (buildable-now, self-application-first) — deployed 2026-09-05 (v0.1.0, the second Bucket B convergence + promotion pass; staged #787), registered in both registries. Spec source: `plans/plan-sheerline-p3-content-design-2026-09-05.md` § 3 / § 4 / § 5. Foundation: `sheerline/os/foundations/content-design/FOUNDATION.md`. The seam's structural contract: `plans/plan-sheerline-p3-interaction-design-2026-09-04.md` § 3.5 / § 4. Boundary: `sheerline/os/operating-principles.md`.*
