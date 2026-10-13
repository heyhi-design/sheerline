---
name: voice-system-author
description: >-
  Derive a client's voice-and-tone system, and audit copy against it. Dual-mode.
  Author mode produces a voice block (the voice-definition scaffold with an
  ELICITED calibration axis, not a fixed pair), an 8-slot UX-writing taxonomy
  drafted against that voice (empty / error / tooltip / CTA / form-label /
  notification / loading / onboarding, plus success / permission), and the
  states-copy doctrine baked in (an error with no next step is a dead end;
  skeleton over spinner). Audit mode runs the flattening lint: mechanical checks
  only (banned words, claim/SLA-leak held until client-confirmed, read-aloud,
  distinctiveness / sea-of-sameness / anti-tell). The lint is advisory, never a
  gate. The client's voice is an elicited INPUT, not read from any brand config;
  the voice DEFINITION and the "does this sound like them" call ship to the human.
  Triggers: "build a voice and tone system", "derive this client's voice",
  "author a UX-writing voice system", "audit this copy for voice flattening".
  NOT for writing in HeyHi's own fixed brand voice (use heyhi-voice). NOT for
  writing in another owned brand's voice that has its own dedicated voice skill
  (use that skill). NOT for a visual /
  design-direction brief (use heyhi-style-brief, which owns the eye; this owns the
  verbal voice). NOT for writing the microcopy for each state of a specific
  screen — the strings, not the voice or the slot patterns (use
  microcopy-states-writer; this derives the voice and lints).
version: "0.1.1"
updated: "2026-09-05"
status: "Deployed — heyhi-skills/voice-system-author/; registered in the main + Sheerline subset registries (Sheerline Wave G-4, 2026-08-28). v0.1.1 (2026-09-05, the second Bucket B pass): re-pointed at the area-3 foundation (sheerline/os/foundations/content-design/FOUNDATION.md) and given the microcopy-states-writer reciprocal at that skill's promotion. Sheerline area 3 (Content Design / UX Writing), P3. Built as the generalization of the owned-voice pattern (heyhi-voice plus one bespoke second-brand voice skill; no heyhi-client-voice candidate exists in the tree). Spec: sheerline-skill-buildout-research-2026-08-09.md § 4.1; boundary § 9."
classification: confidential
---

# Voice System Author

**Sheerline area 3 (Content Design / UX Writing) · dual-mode Author + Audit.** A client team knows how it wants to sound but has never written it down, or has a voice on paper and copy drifting away from it. This skill structures the first and lints the second. In **Author** mode it assembles a voice-and-tone system: a voice block whose calibration axis is elicited for this client (not HeyHi's fixed pair), an 8-slot UX-writing taxonomy drafted against that voice, and the states-copy doctrine baked in. In **Audit** mode it runs the flattening lint, a set of mechanical checks that flag where copy has gone off-voice, generic, or made a claim it cannot back. The lint advises; it never blocks a ship.

The move that makes this a generalization: an owned voice skill carries one fixed voice (`heyhi-voice` is HeyHi's own; an instance may also run a bespoke voice skill for a second brand it writes for). This skill is the pattern under those, decoupled from any single brand. The client's voice is an input the human defines. The skill drafts candidates, structures the system, and audits the output. It never decides "this is their voice."

**The boundary this skill obeys (Sheerline § 9, absolute).** A structured artifact with explicit empty judgment slots, a named human gate, and provenance labels on anything synthetic or unconfirmed. The **voice definition** and the **"does this sound like them"** call are the empty slots. Drafting candidate attributes, structuring the calibration axis, and drafting slot copy against a stated voice is mechanical. Deciding which attributes are true, where the voice lands on its axis, and whether the copy sounds like the client is judgment. A version of this skill that fills its own voice definition, or signs off that copy is on-voice, has exceeded its charter. The skill drafts and flags; the human decides.

> **This skill closes through the Exit Gate (`CLAUDE-SESSION-RULES.md § Exit Gate`).** See the bottom-of-skill bracket.

---

## Routing: disambiguation with sibling skills

| If the task is… | Use |
|---|---|
| Derive a NEW client's voice system, or audit a client's copy for voice drift | **this skill** |
| Write in HeyHi's own fixed brand voice (HeyHi copy, essays, proposals) | `heyhi-voice` |
| Write in another owned brand's voice that already has its own dedicated voice skill | that brand's voice skill |
| Turn a chosen VISUAL direction into a client-approvable brief (the eye, not the verbal voice) | `heyhi-style-brief` |
| Write the microcopy / the strings for every state of a specific screen, against a voice already confirmed | `microcopy-states-writer` (this skill derives the voice and one pattern per slot, and owns the lint; that skill drafts the strings into the slots a screen's states carry) |
| Decide the voice definition, or judge whether copy sounds like the client | **the human** (this skill's named gate) |

The seam with `heyhi-voice` and any other owned voice skill is ownership: each carries one fixed, owned voice and writes in it. This skill carries no voice of its own. It derives a client's voice as an elicited variable and hands the definition back to the human. The seam with `heyhi-style-brief` is sense: that skill describes what a design will look and feel like (color, type, imagery); this skill governs what the product says and how it says it. A single engagement often needs both, in parallel.

**When a request is actually for an incumbent, route away.** "Write HeyHi's about page" is `heyhi-voice`. "Draft the onboarding modal" for an owned second brand with its own voice skill is that skill. "Write the design-direction brief for sign-off" is `heyhi-style-brief`. This skill activates only when the voice being derived or audited belongs to a client and is not already an owned instance voice (HeyHi's or another owned brand's).

---

## Step 0: Improvement hook check

Retrieve any recurring corrections for voice / content-design work (`retrieve_design_corrections`, or the Sheerline `os/corrections/` registry when running inside a Sheerline engagement). Fold a match into the pass. Skip silently if none.

## Step 1: Load context and pick the mode

Load only what the task needs (Earn the Room).

1. **The engagement inputs** the human brought. For Author mode: whatever names the client's voice today, in any form (a discovery-call note, an existing copy sample, a competitor set to sound unlike, a "we want to feel X but not Y" line, a brand adjective list). For Audit mode: the copy to lint, plus the voice system to lint it against if one exists.
2. `references/voice-system-template.md`: the voice-block structure, the elicited-calibration-axis method, the 8-slot taxonomy with the states-copy doctrine, and the claim/SLA guardrail. The Author-mode spine.
3. `references/flattening-lint-checklist.md`: the four mechanical lint families and how each is run and reported. The Audit-mode spine.
4. `sheerline/os/foundations/content-design/FOUNDATION.md`: the area-3 governed context. Register under it; do not author it. It points at this skill's two references as the canon of record for the voice model, the taxonomy, the doctrine, the lint, and the guardrail, and authors only the per-state layer around them (the state → slot map, the next-step anatomy, string constraints) that `microcopy-states-writer` consumes.
5. The instance's own voice skill (in HeyHi, `heyhi-skills/heyhi-voice/SKILL.md`), loaded for its **mechanical** disciplines only: the banned-word list, the anti-tell patterns, the read-aloud test, the em-dash and standalone-word rules. Borrow the machinery, not HeyHi's voice. This skill derives the client's voice, which is usually nothing like HeyHi's.

**Mode selection.** If the task is "build / derive / author a voice system," run **Author** mode (Step A). If the task is "audit / lint / check this copy for voice drift or flattening," run **Audit** mode (Step B). If both are asked for in one session, run Author first, then Audit against the system it produced.

---

## Author mode: derive the voice system

Every step below is mechanical scaffolding. None of it decides the voice.

### Step A1: Frame the voice definition as the human's, and draft candidates

The voice definition is the empty judgment slot. Do not fill it. Instead:

- Draft **candidate voice attributes** from the inputs (three to five is the working range). Each candidate carries a *sounds-like / doesn't-sound-like* pair so the human has something concrete to accept, reject, or rewrite. Label every candidate `[candidate — agent-drafted]`.
- Draft a **candidate one-line voice statement**, also labeled a candidate.
- Leave the confirmed definition blank. The human chooses which attributes are true and writes the one-liner that survives.

Drafting a candidate widens the human's options. It does not narrow them to a choice. A skill that returns "your voice is warm, direct, and playful" as settled fact has made the call the human owns.

### Step A2: Structure the calibration axis (elicited, not fixed)

HeyHi's own voice runs on a fixed dial (polished studio voice at one end, a more unfiltered energy at the other). A client's axis is not that dial. It must be elicited for this client.

- Propose one or two **candidate axes** the client's voice appears to move along (for example: *authoritative ←→ approachable*, or *playful ←→ precise*), each drafted from the inputs and labeled a candidate.
- Structure the *where does it sit by context* question as an empty grid: marketing surface, in-product copy, error and failure states, legal and account moments. The client's voice usually sits at different points on the axis in each.
- The human confirms the axis and where the voice sits. The skill provides the frame and the candidates, never the settled position.

### Step A3: Draft the 8-slot UX-writing taxonomy against the voice

Draft candidate copy patterns for each of the eight core content slots, written against the *candidate* voice so the human can see the voice applied and react to it. The eight, plus the two extended slots:

| Slot | What it governs |
|---|---|
| Empty | First-run and no-data states: what the screen says when there is nothing to show yet |
| Error | Failure, validation, and blocked states |
| Tooltip | Inline help and hover hints |
| CTA | Buttons and primary actions |
| Form label | Field labels, placeholders, helper text |
| Notification | Toasts, banners, system messages |
| Loading | Waiting and in-progress states |
| Onboarding | First-use guidance and setup flows |
| Success *(extended)* | Confirmation and completion states |
| Permission *(extended)* | Consent, access, and privacy prompts |

All drafted strings are candidates pending the human's voice definition. Mark them so.

### Step A4: Bake in the states-copy doctrine

The taxonomy is not just voice applied; it carries two non-negotiable content rules, wired into the relevant slots:

- **An error with no next step is a dead end.** Every error-slot pattern must carry a next action: what the person can do now. An error string that only names the failure fails the doctrine.
- **Skeleton over spinner.** Loading-slot patterns default to a content skeleton (structure the person will see) rather than an undifferentiated spinner, and any loading copy sets a real expectation, not "please wait."

Flag any slot copy that violates the doctrine rather than silently shipping it.

### Step A5: Hold every claim behind provenance

Any drafted string that asserts an **SLA, guarantee, timeframe, uptime, security posture, compliance status, or performance number** is not shippable copy until the client confirms it is true. Do not write it into the taxonomy as final. Move it to the **claim guardrail** with a `NEEDS CLIENT CONFIRMATION` flag. The skill can draft the *shape* of the sentence; it cannot assert the *fact*. A voice system that ships "resolved within 24 hours" as confirmed copy has laundered an unverified claim into the product.

### Step A6: Produce the Voice System artifact

Output this exact structure. The voice-definition slot and the named gate stay empty by construction.

```
# Voice System: [engagement label]
Source: [inputs]        Authored: [date]        Mode: Author

## ⛔ Voice definition — NEEDS HUMAN
This slot is intentionally empty. Which attributes are true, and whether the
result sounds like the client, is the human's call.
   Voice in one line (human-confirmed):        ____________________
   Confirmed voice attributes (3–5):           ____________________

### Candidate voice attributes  [candidate — agent-drafted]
- [attribute] (sounds like: [...]; doesn't sound like: [...])
- [attribute] (sounds like: [...]; doesn't sound like: [...])

## Calibration axis (elicited, not a fixed pair)
   Candidate axis:  [pole A] ←→ [pole B]        [candidate — agent-drafted]
   ⛔ Where it sits by context — NEEDS HUMAN:
      marketing surface:  ____   in-product:  ____
      error states:  ____        legal / account:  ____

## 8-slot UX-writing taxonomy (drafted against the candidate voice)
| Slot | Pattern | States-copy rule | Draft copy [candidate] |
|------|---------|------------------|------------------------|
| Empty        | ... |                              | ... |
| Error        | ... | must carry a next step       | ... |
| Tooltip      | ... |                              | ... |
| CTA          | ... |                              | ... |
| Form label   | ... |                              | ... |
| Notification | ... |                              | ... |
| Loading      | ... | skeleton over spinner        | ... |
| Onboarding   | ... |                              | ... |
| Success      | ... |                              | ... |
| Permission   | ... |                              | ... |

All draft copy above is AGENT-DRAFTED CANDIDATE, pending the human's voice definition.

## Claim / SLA guardrail (held for confirmation)
[Any string asserting an SLA, guarantee, timeframe, security, compliance, or
 performance claim, held until the client confirms it. Not shipped as copy.]
- [held string], status: NEEDS CLIENT CONFIRMATION
[Empty if the drafted copy makes no such claim.]

## Named gate
Voice-definition sign-off owner (client / brand lead): ____________  Date: ______
No voice system is adopted, and no candidate copy ships, until this line is signed.
```

**The system is done when every candidate is labeled, the calibration axis is elicited (not a fixed pair), every error slot carries a next step and every loading slot honors skeleton-over-spinner, every claim is held behind confirmation, and the voice-definition slot plus the named gate are still blank.**

---

## Audit mode: the flattening lint

The lint is four families of **mechanical** checks. It flags; it never gates. There is no "this copy is on-voice" verdict in this skill: that judgment is the human's.

### Step B1: Load the copy and the reference

Take the copy to lint. If a voice system exists (from Author mode or the client's own), load it as the reference the lint measures against. If none exists, the distinctiveness and read-aloud checks still run; the off-voice-term check runs against the client's banned list if provided, otherwise it reports what it can and names what it could not check.

### Step B2: Run the four lint families

Full checklist in `references/flattening-lint-checklist.md`. The families:

1. **Banned-word / off-voice term flags.** Scan for the client's own banned list (if supplied) and for the generic-filler set the checklist carries. Report each hit with its location. This is a scan, not a rewrite.
2. **Claim / SLA-leak flags.** Flag every SLA, guarantee, timeframe, security, compliance, or performance claim in the copy. Each is held with a `NEEDS CLIENT CONFIRMATION` note. The lint does not decide whether the claim is true; it surfaces that a claim was made and must be backed.
3. **Read-aloud flags.** Flag sentences that do not survive being read aloud: the ones that stall, that no person would say out loud, that carry two ideas in one breath. Report the sentence and why it stalls.
4. **Distinctiveness / sea-of-sameness / anti-tell flags.** Flag copy that reads as generic product boilerplate (the "sea of sameness": interchangeable with any competitor) and copy carrying the known machine-generated tells (the reframe construction, the one-sentence reveal, the section-ending kicker, the tricolon-as-drama). This family names *where* the copy is undifferentiated; it does not decide whether the distinct alternative sounds like the client.

### Step B3: Produce the lint report

Output this exact structure. Advisory throughout.

```
# Voice Flattening Lint: [artifact]
Source: [copy]   Voice reference: [system ref / "none provided"]   Linted: [date]
ADVISORY ONLY. This lint flags; it does not block, gate, or approve a ship.

## Banned-word / off-voice term flags
- "[term]" at [location]: [why flagged]

## Claim / SLA-leak flags (held for client confirmation)
- "[claim]" at [location], status: NEEDS CLIENT CONFIRMATION

## Read-aloud flags
- "[sentence]": [why it stalls]

## Distinctiveness / sea-of-sameness / anti-tell flags
- "[passage]": [generic boilerplate / named tell]; [note]

## What the lint could NOT check (needs the human)
- Whether the flagged passages, once revised, sound like the client (the voice call).
- [Anything the lint had no reference for, stated plainly.]
```

**The lint is done when every family has run, every flag carries a location and a reason, no flag is phrased as an approval or a block, and the "could not check" section names the on-voice judgment as the human's.**

---

## Step 2: Pre-flight verification

Before presenting either mode's output, confirm:

- **Author mode:** the voice-definition slot is empty and the named gate is unsigned; every drafted attribute, axis, and string is labeled `[candidate — agent-drafted]`; the calibration axis is elicited for this client, not HeyHi's fixed pair and not read from a brand config; every error slot carries a next step; every loading slot honors skeleton-over-spinner; every SLA / guarantee / claim is held behind confirmation, not shipped as fact.
- **Audit mode:** every flag carries a location and a reason; no flag reads as "this is on-voice" or "this is safe to ship" (advisory only); the report never blocks a ship; the "could not check" section states the on-voice judgment is the human's.
- **Both modes:** this skill's own output honors its own doctrine. Run the mechanical scan on the SKILL output itself: no standalone "AI", no banned words, read-aloud clean, em dashes minimal.

---

## What is explicitly out of scope

- **Deciding the voice.** The voice definition and the "does this sound like them" call are empty by construction (§ 9). The skill drafts candidates and structures the system; the human decides.
- **Approving copy as on-voice.** The Audit lint flags; it never certifies. No "on-brand, ship it" verdict exists in this skill.
- **Writing in HeyHi's or another owned brand's voice.** Those are owned, fixed voices with their own skills (`heyhi-voice`, or that brand's dedicated voice skill). This skill derives a *client's* voice as a variable.
- **Visual / design direction.** Color, type, imagery, and the look-and-feel brief belong to `heyhi-style-brief`. This skill owns the verbal voice only.
- **Asserting an unconfirmed claim.** Every SLA, guarantee, and performance number is held behind client confirmation, never shipped as fact.

---

## After delivering

- Present the output in conversation first. Create a file only when asked to save it.
- On save: `voice-system-[label].md` in the instance's engagement folder for this client (the engagement intake's `deliverable.root`). If that folder is gitignored and the session runs in a git worktree, write to the main workspace copy (`<workspace root>/<engagement folder>/...`), never the worktree's copy.
- If the engagement's NDA or contract is not yet signed, the voice system is a **draft**, not a delivery. Producing the internal draft is allowed; shipping it to the client is gated on signatures (the standing pre-signature rule at `OPERATING_PRINCIPLES.md` § Document classification). Mark the working file `status: draft` and `classification: confidential`; the client-facing body becomes unclassified on delivery.

---

## Exit Gate Required Headers (bottom-of-skill bracket)

This skill closes through Exit Gate Flavor A (`CLAUDE-SESSION-RULES.md § Exit Gate`). Before declaring done, confirm every required header holds real content:

- `## Fixes Applied` (or the delivered Voice System / Lint report)
- `## Smoke Test` (the Step 2 pre-flight checks, pasted)
- `## Next Session Prompt`

If the voice-definition slot is filled, or an Audit flag reads as an approval, the gate has **not** been satisfied.

---

*HeyHi Confidential. Sheerline area 3 (Content Design / UX Writing), P3. Deployed — `heyhi-skills/voice-system-author/`; registered in the main + Sheerline subset registries (Sheerline Wave G-4, 2026-08-28). Built as the generalization of the owned-voice pattern (`heyhi-voice` plus one bespoke second-brand voice skill; no `heyhi-client-voice` candidate exists in the tree). Spec source: `ai-services/design-intelligence/research/sheerline-skill-buildout-research-2026-08-09.md` § 4.1. Boundary: § 9. Foundation: `sheerline/os/foundations/content-design/FOUNDATION.md` (filled 2026-09-05).*
