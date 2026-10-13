---
classification: confidential
title: "Voice-system template: the Author-mode spine"
skill: voice-system-author
loaded_by: "SKILL.md Step 1 (Author mode)"
---

# Voice-system template

The voice-block structure, the elicited-calibration-axis method, the 8-slot UX-writing taxonomy with the states-copy doctrine, and the claim guardrail. Held as read-and-apply reference. On-demand: load when running Author mode.

*Internal operational reference (staged under `skill-updates/`). This skill is about voice, so this reference is written to its own read-aloud and plain-punctuation discipline: em dashes are kept minimal rather than taking the operational exemption.*

---

## The one rule that shapes the whole template

The client defines the voice. The template structures it and drafts candidates against it. Every slot the template fills is a candidate the human accepts, rejects, or rewrites. Two slots the template never fills: the **voice definition** (which attributes are true, the one-line statement) and the **on-voice judgment** ("does this sound like them"). Those are the empty judgment slots (§ 9). A candidate widens the human's options. It never narrows them to a choice.

---

## Part 1: The voice block

The voice block is the definition scaffold. It has three parts, and only the third is agent-drafted.

### 1a. Voice in one line (human-confirmed, ships empty)

One sentence a client reads and says "yes, that is us." The skill may offer a *candidate* one-liner drawn from the inputs, labeled as a candidate. The confirmed line is the human's.

### 1b. Voice attributes (human-confirmed, ships empty; candidates drafted)

Three to five attributes is the working range. Fewer than three is thin; more than five stops being a voice and becomes a wish list. Each attribute the skill drafts is a **candidate**, and each candidate carries a concrete pair so the human has something to react to:

```
[attribute]  [candidate — agent-drafted]
  sounds like:        [a short, specific example line in this attribute]
  doesn't sound like: [the near-miss the attribute rules out]
```

The *sounds-like / doesn't-sound-like* pair is what makes an attribute usable. "Friendly" alone is inert. "Friendly (sounds like: 'Let's get you set up.' / doesn't sound like: 'We are delighted to assist you on your journey.')" gives the human a real edge to confirm or move.

### 1c. Anti-descriptors (what the voice is not)

Draft candidate anti-descriptors from the inputs, especially from any competitor set the client wants to sound *unlike*. Anti-descriptors sharpen a voice faster than descriptors: "not corporate, not cute, not breathless" tells a writer more than three positive adjectives. Candidates only; the human confirms.

---

## Part 2: The calibration axis (elicited, not fixed)

HeyHi's own voice runs on a fixed dial: polished studio voice at one pole, a more unfiltered energy at the other. That dial is HeyHi's. It is not a client's. The generalization that makes this skill work is treating the axis as an **elicited variable**: this client's voice moves between poles that must be discovered, not assumed, and never read from a brand config.

### 2a. Draft candidate axes

Propose one or two axes the client's voice appears to move along, each drafted from the inputs and labeled a candidate. Common axis shapes (draw from these, do not default to them):

- authoritative ←→ approachable
- playful ←→ precise
- warm ←→ efficient
- expert ←→ plainspoken
- calm ←→ energetic

A client may need a two-axis grid rather than one line. Draft what the inputs support; the human confirms whether one axis or two.

### 2b. Structure where it sits by context (ships empty)

A voice is not one point on the axis. It sits at different points in different surfaces. Structure this as an empty grid the human fills:

```
                    [pole A] <---------------------> [pole B]
marketing surface:                    ?
in-product copy:                      ?
error / failure states:               ?
legal / account moments:              ?
```

The pattern most product voices follow: more character on the marketing surface, more restraint in error and legal states. But that is a tendency to prompt with, not a position to assert. The human places the marks.

---

## Part 3: The 8-slot UX-writing taxonomy

Draft candidate copy patterns for each slot, written against the *candidate* voice so the human sees the voice applied. Eight core slots, two extended.

| # | Slot | What it governs | The pattern to draft |
|---|---|---|---|
| 1 | Empty | First-run and no-data states | What the screen says with nothing to show yet, and the one action that fills it |
| 2 | Error | Failure, validation, blocked states | What went wrong, in plain terms, and the next step (see the doctrine below) |
| 3 | Tooltip | Inline help, hover hints | One idea, short, no restating the label it hangs on |
| 4 | CTA | Buttons, primary actions | The verb-first action, sized to the commitment behind it |
| 5 | Form label | Labels, placeholders, helper text | The label as a plain question or noun; placeholder as example, not instruction |
| 6 | Notification | Toasts, banners, system messages | What happened, whether the person must act, and how to act if so |
| 7 | Loading | Waiting, in-progress states | Skeleton over spinner (see the doctrine); copy that sets a real expectation |
| 8 | Onboarding | First-use guidance, setup | One step at a time, in the client's voice, never a wall of tips |
| 9 | Success *(extended)* | Confirmation, completion | What is done and what is now possible, without over-celebrating routine acts |
| 10 | Permission *(extended)* | Consent, access, privacy | What is being asked, why, and what happens either way, in plain language |

Every drafted string is a candidate pending the voice definition. Mark each `[candidate — agent-drafted]`.

---

## Part 4: The states-copy doctrine (baked in, non-negotiable)

Two content rules ride inside the taxonomy. They are not voice preferences; they are content-design floors that hold regardless of voice.

### 4a. An error with no next step is a dead end

Every error-slot pattern must carry a next action: what the person can do now. An error string that only names the failure ("Something went wrong") strands the person. The doctrine requires the next step:

```
Fails the doctrine:   "Upload failed."
Honors the doctrine:  "That file is over 25 MB. Try a smaller file, or split it in two."
```

Flag any error slot that names a failure without a way forward. The voice can be warm or terse; the next step is not optional.

### 4b. Skeleton over spinner

Loading-slot patterns default to a content skeleton (the shape of what is coming) rather than an undifferentiated spinner, and loading copy sets a real expectation rather than "please wait":

```
Weak:    a spinner, "Loading..."
Better:  a skeleton of the results list, "Pulling your last 30 days."
```

Flag loading slots that reach for a bare spinner when a skeleton would tell the person more.

---

## Part 5: The claim / SLA guardrail

Any drafted string that asserts an **SLA, guarantee, timeframe, uptime, security posture, compliance status, or performance number** is not shippable copy until the client confirms it is true. The skill can draft the *shape* of the sentence. It cannot assert the *fact*.

Move every such string out of the taxonomy and into the guardrail with a flag:

```
## Claim / SLA guardrail (held for confirmation)
- "Resolved within 24 hours"           status: NEEDS CLIENT CONFIRMATION
- "Bank-level encryption"              status: NEEDS CLIENT CONFIRMATION
- "99.9% uptime"                       status: NEEDS CLIENT CONFIRMATION
```

A voice system that ships an unconfirmed claim as final copy has laundered a fact the client never verified. The guardrail is empty only when the drafted copy makes no such claim.

---

## Part 6: The provenance discipline for this skill

Every attribute, axis, anti-descriptor, and slot string the skill writes is agent-drafted and labeled `[candidate — agent-drafted]`. It is a proposal, never a confirmed voice or an approved string. Any claim is held behind confirmation. Anything drawn from a real client artifact (an existing copy sample, a stated adjective) carries that source so a candidate can never be mistaken for the client's confirmed word.

---

*HeyHi Confidential. Reference for `voice-system-author`. Spec source: `sheerline-skill-buildout-research-2026-08-09.md` § 4.1 (content-design foundation: voice-and-tone model with the calibration axis as an elicited variable; the 8-slot taxonomy; the states-copy doctrine; claim guardrails). Built as the generalization of the owned-voice pattern (`heyhi-voice` plus one second-brand voice skill).*
