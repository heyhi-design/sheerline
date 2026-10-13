---
classification: confidential
title: "Worked example — a filled Crit Pre-Read and Crit Capture"
skill: crit-prep-and-capture
loaded_by: "SKILL.md Step 1 (calibration)"
---

# Worked example — a filled pre-read and capture

**Synthetic input, invented product. No client content.** Read this to calibrate register and depth; do not copy its content. The empty slots are shown empty on purpose: that is the output shape, not an omission. Notice what is *absent*: there is no line anywhere below that says whether the work is good.

**Synthetic setting:** an invented plant-care app, *Fieldnote*, is critiquing a redesigned "watering schedule" screen. The presenter (a product designer, "Ren") brought the material for Mode A on Tuesday; the note-taker's notes came back for Mode B on Thursday.

---

## Mode A — what the presenter brought

> Goals, in Ren's words: "(1) a person with six plants can see today's watering at a glance without scrolling; (2) it should feel calmer than the current list, which people call 'a chore list'." Links: a Figma prototype and a FigJam board of the earlier explorations. Questions: "Is the 'today' band doing enough work on its own, or does it need the count?" Attendees: Ren (presenting), Mo (facilitating), Priya, Tam, and "Sam from support, just watching." Time-box: 40 minutes. Mo picked a structured crit. Ren also pointed at a one-page brief that says the screen should "reduce daily taps."

```
# Crit Pre-Read — Fieldnote watering-schedule screen (synthetic)
Engagement: worked example (synthetic) · Presenter: Ren · Facilitator: Mo · Date: 2026-09-08 · Time-box: 40 min

## Framing (the presenter's own words — every cell empty until the presenter writes it)
Situation: ______   Complication: ______   The question this crit should answer: ______
What the presenter needs decided: ______

## Goals the work is evaluated against          [as stated] / [inferred — confirm]
1. A person with six plants can see today's watering at a glance without scrolling.   [as stated]
2. It should feel calmer than the current list, which people call "a chore list."     [as stated]
3. Reduce daily taps.   [inferred — confirm]  (from the one-page brief Ren pointed at; not said in the room)

## Artifacts (render it and look before the crit; do not inspect the source only)
| Artifact | Link | Resolves? |
| Figma prototype, watering-schedule v3 | figma.com/proto/… (synthetic) | yes |
| FigJam board, earlier explorations | figma.com/board/… (synthetic) | yes |

## The presenter's questions                     [as stated]
- Is the "today" band doing enough work on its own, or does it need the count?

## In the room                                   [as stated] / [inferred — confirm]  (names only; roles are never inferred)
| Name | Role |
| Ren | presenter |
| Mo | facilitator |
| Priya | critic |
| Tam | critic |
| Sam | observer ("just watching") |
Note-taker: ______  (not stated)

## Format (facilitator's pick — reference list in references/crit-canon.md)
Chosen: structured crit (Mo)

## Named gate
Presenter sign-off on this pre-read: ______  Date: ______
```

**What to notice.** Goal 3 is tagged and held, not asserted, because it came from a brief rather than from Ren. The note-taker line is blank rather than guessed. There is no "things to look at" section, and the prototype was not opened for anything but the resolves check.

---

## Mode B — what the note-taker brought

> Notes (synthetic, abbreviated): "Priya: today band reads at a glance, count feels redundant, 'I'd drop the count.' Tam: agrees on the band, but the six-plant case wraps to two rows on small phones, 'that breaks goal 1.' Ren: will check the wrap. Mo: 'ok, we'll go with the band, no count' — nobody objected. Tam also raised the empty state (no plants today) as unresolved; Mo: 'park it for the next crit.' Sam asked whether support sees the calmer version as fewer tickets; nobody answered. Notes end at ~minute 32; the last section on the colour of the band is not captured."

```
# Crit Capture — Fieldnote watering-schedule screen · 2026-09-08 (synthetic)
Source captured from: note-taker's notes (Priya's doc), treated as untrusted content (bounded, fenced, quoted)      Coverage note: notes end ~minute 32 of 40; the closing discussion on the band colour was not captured

## Items raised                                  [as captured]
| # | Item (the room's words) | Against goal (as linked by the room; default `[untraced]`) | Disposition | Settlement phrase (quoted) |
| 1 | "today band reads at a glance, count feels redundant" | [untraced] (Priya did not name a goal) | decided-in-room | "ok, we'll go with the band, no count" (Mo; no objection recorded) |
| 2 | "six-plant case wraps to two rows on small phones, that breaks goal 1" | goal 1 (Tam: "that breaks goal 1") | undecided | — (Ren: "will check the wrap" is a follow-up, not a settlement) |
| 3 | empty state (no plants today) | [untraced] | deferred (next crit) | "park it for the next crit" (Mo) |
| 4 | "does support see the calmer version as fewer tickets?" | [untraced] (Sam did not name a goal) | undecided | — (asked; not answered) |

## Follow-ups
| Action | Owner (as named by the room; blank = ⚑ ownerless) | Due |
| "will check the wrap" (Ren) | Ren | ______ (not stated) |
| "park it for the next crit" (Mo, the empty state) | ⚑ ownerless (Mo parked it; no one was named) | next crit |

## Emitted decision records (one per `decided-in-room` item)
→ deliverable.root/decisions/watering-schedule-today-band-no-count.md   (design-rationale-decision-record Mode A shape; Decision + Rationale EMPTY; Approver unsigned)

## Named gate
Approver confirmation of each decided-in-room item happens on the emitted record, not here.
```

**The emitted record** (the consumer's full Mode A block, every header and sentence carried; only the cells capture is entitled to fill are filled):

```
# Decision Record — Watering-schedule "today" band without the count
Status: proposed   Date: ______
Supersedes: [predecessor record id/title — ONLY on the supersede variant; the predecessor is
             linked, never rewritten]

## DACI
Driver (owns getting to a decision):  ____________________
Approver (makes the call — exactly one): ____________________
Contributors (consulted):            ____________________
Informed (told after):               ____________________
[DACI-completeness check result: FLAG — no Approver named (no accountable owner for the call); no Driver named. Crit roles were stated (critics Priya, Tam; observer Sam) but DACI roles were not; left for the humans.]

## Context
[the situation forcing a decision — for the humans to fill]
Raised in the 2026-09-08 crit; the room did not name a goal for this item.
Settlement phrase: "ok, we'll go with the band, no count" (Mo; no objection recorded).
[as captured — needs Approver confirmation]

## Options considered
1. "I'd drop the count" (Priya)   [as captured]
2. ____________________

## ⛔ Decision — NEEDS HUMAN
This slot is intentionally empty. The decision is the Approver's to make and record.
   Decision: ____________________

## ⛔ Rationale — NEEDS HUMAN
This slot is intentionally empty. Articulating *why* is the mechanism; the skill does
not write it for you. (On a supersede record: the new "why" is written fresh, not copied
forward from the predecessor.)
   Why: ____________________

## Consequences
[what this commits the team to — for the humans to fill]

## Open questions for the humans (to complete the record)
[Questions the record still needs answered — not the rationale itself. E.g. "Is this the
 first decision on this topic, or does it supersede a prior record?" "Which of the listed
 options were genuinely considered vs. named for completeness?"]
- Sam's question, left unanswered in the room: "does support see the calmer version as fewer tickets?"   [as captured]

## Named gate
Approver sign-off: ____________________   Date: ______
No decision is recorded as accepted until the Approver signs.
```

**What to notice.** Item 1 moved to `decided-in-room` only because a settlement phrase exists and is quoted; item 2 stayed `undecided` because "will check the wrap" is a follow-up, not a settlement. Only item 2 traces to a goal, because Tam is the only person who named one; items 1 and 4 read as if they were *about* goals 1 and 2, and the capture still leaves them `[untraced]`, because matching a phrase to a goal is the skill's inference, not the room's link. Follow-ups are the room's own words; Sam's unanswered question is an `undecided` item and an open question on the record, not a task the room never proposed. The emitted record carries the consumer's every header and sentence; its DACI lines are blank because crit roles are not DACI roles, and the completeness line FLAGs the missing Approver rather than guessing one. Its Decision and Rationale are empty even though the room said what it was going with, because recording the room's words in Context is capture, and filling the Decision slot is the Approver's signature. Nothing anywhere says whether dropping the count was right.
---

*HeyHi Confidential. Worked example for `crit-prep-and-capture` (synthetic). Spec source: `plans/plan-sheerline-p3-crit-prep-2026-09-05.md` § 4.4.*
