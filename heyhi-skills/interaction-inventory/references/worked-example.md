---
classification: confidential
title: "Worked example — a filled Interaction Inventory"
skill: interaction-inventory
loaded_by: "SKILL.md Step 1 (calibration)"
---

# Worked example — a filled Interaction Inventory

**Synthetic input, invented product. No client content.** Read this to calibrate the register and depth of the free-prose slots; do not copy its findings. The empty slots are shown empty on purpose: that is the output shape, not an omission. The matching sidecar is `worked-example.sidecar.json` (validates against `../inventory-schema.json`).

**Synthetic source brought by the (invented) team:** a Figma frame for the *Notification settings* screen of a note-taking app — a tab strip (Email / Push / Digest), a form with a toggle switch and a text input for a digest hour, a **Save** button that posts to an API, and a list of recently sent digests fetched on load. Only the default, hover, and focus states of the Save button are drawn; the list is drawn populated.

---

```
# Interaction Inventory — Notification settings (NoteNest, synthetic)
Source: figma · file SYNTH-0001 · node 12:340   Inventoried: 2026-09-05   Contract: A.3 (design-system://fundamentals)

## Element census
| # | Element | Class | Provenance | APG pattern (if composite) |
| 1 | Channel tabs (Email / Push / Digest) | composite | from-source | Tabs |
| 2 | "Send a daily digest" switch | selection control | from-source | Switch |
| 3 | Digest hour input | text input | from-source | — |
| 4 | Save button | action (async submit) | from-source | Button |
| 5 | Recent digests list | data view (async) | from-source | — |
| 6 | Section heading "Notifications" | static | from-source | — |

## State matrix (contract states × element; data-view states × view)
| Element | default | hover | focus-visible | active | disabled | loading | error | success | selected |
| 1 Channel tabs | shown | shown | shown | MISSING | n/a | n/a | n/a | n/a | shown (aria-selected) |
| 2 Digest switch | shown | shown | MISSING | MISSING | n/a | n/a | n/a | n/a | shown (aria-checked) |
| 3 Digest hour input | shown | n/a | shown | n/a | n/a | n/a | MISSING | n/a | n/a |
| 4 Save button | shown | shown | shown | MISSING | MISSING | MISSING | MISSING | MISSING | n/a |
| 5 Recent digests list | — | data-view states: empty MISSING · loading MISSING · error MISSING · populated shown |
| 6 Heading | n/a (readonly) |
Legend: shown = in the source · MISSING = applicable by class, not shown · n/a = not applicable by class
[Every MISSING is a flag for the human, never a defect verdict. Twelve MISSING cells on this
 screen plus four named flags; the Save button carries five of the cells because it is an async
 action drawn as if it were synchronous.]

## Transitions (per element — candidate state machines)   [all rows: candidate — agent-drafted]
| Element | From → To | Trigger | Exit path | Flag |
| 4 Save | default → loading | click / Enter / Space (async POST) | → success on 2xx; → error on failure | loading-no-error-exit (only the 2xx path is implied by the design) |
| 4 Save | loading → success | response 2xx | → default after the confirmation | — |
| 4 Save | loading → error | response non-2xx / network | → default via retry (no inline retry drawn) | error-no-recovery |
| 4 Save | default → disabled | form unchanged since last save (a candidate rule; no disabled state is drawn) | → default on any edit | disabled-reason-unshown (nothing on the surface would say why) |
| 3 Hour input | default → error | blur with a value outside 0–23 | → default on a valid edit | — (an inline message is required; see copy slot) |
| 2 Switch | off → on / on → off | click / Space | — (toggle) | — |
| 1 Tabs | selected(Email) → selected(Push) | click / Arrow keys | — | — |
| 5 List | loading → populated / empty / error | fetch resolves | populated → (none: terminal); error → loading on retry | — (no retry affordance drawn: flagged above as error MISSING)

## Focus, keyboard, gesture
| Element | Focusable | Keyboard (APG map, by pattern) | Touch triggers | ≥ 44 px (served floor) |
| 1 Tabs | yes | per APG "Tabs": Arrow keys move, Enter/Space select, Home/End | tap | tab targets 40 px high → below-44px |
| 2 Switch | yes | per APG "Switch": Space / Enter toggle | tap | ok |
| 3 Hour input | yes | native text input | tap | ok |
| 4 Save | yes | per APG "Button": Enter / Space activate | tap | ok |
| 5 List rows | no (not selectable) | — | swipe? (undrawn; a question below) | — |

## Accessibility hooks per state
| 4 Save | loading: aria-busy=true, non-interactive to block double submit · error: aria-invalid on the form + aria-describedby → message · success: a polite live region · disabled: disabled attribute
| 3 Hour input | error: aria-invalid + aria-describedby → inline message · focus-visible: 2px ring at 2px offset (non-color-only)
| 1 Tabs | selected: aria-selected on the tab, aria-controls → panel · focus-visible on the active tab only (roving tabindex)
| 2 Switch | selected: aria-checked · focus-visible ring
| 5 List | loading: aria-busy on the region · empty / error: announced in a status region

## Copy slots (EMPTY — area 3 fills them; only the states that carry copy)
| Element | State | Taxonomy slot | String |
| 4 Save | loading | Loading | ______ |
| 4 Save | error | Error | ______ |
| 4 Save | success | Success | ______ |
| 3 Hour input | error | Error | ______ |
| 5 List | empty | Empty | ______ |
| 5 List | loading | Loading | ______ |
| 5 List | error | Error | ______ |
(All other state rows: no copy.)

## Open questions for the team (questions, not judgments)
- Is Save synchronous in practice (a local settings write) or an API round-trip? The whole
  loading / error / success column on row 4 turns on that answer.
- Should the digest list support swipe-to-delete on touch, or is it read-only history? Nothing
  is drawn either way, and the answer decides whether rows are focusable and selectable.
- Should "Save" be disabled until a change is made (no disabled state is drawn, so the rule is
  a guess), and if so, should the surface say why?

## Near-misses and unchecked territory (traces, no verdicts)
- Considered flagging the tab strip's `active` (pressed) state as n/a — kept as MISSING because
  A.3 lists active for every pointer-activated control and the tabs are click targets.
- The hour input's `success` (inline "looks good") was almost added as `if-validated`; left n/a
  because the form has no per-field validation pattern elsewhere. A question for the lead, not
  a ruling.
- Could not check: whether the list is paginated (the frame shows three rows and no control) —
  a pagination control would add its own composite element and states.

## ⛔ Which interactions matter — NEEDS HUMAN
   Elements / transitions that get design attention on this screen: ____________________

## ⛔ Deliberate-absence rulings — NEEDS HUMAN
   Each MISSING flag above is either a gap to design or a deliberate absence. Rule on each:
   ____________________

## ⛔ Interaction verdict — NEEDS HUMAN
   Does the behavior serve the task; does it feel right (judged in motion): ____________________

## Named gate
Sign-off owner (design lead / interaction owner): ____________________  Date: ______
No state is declared complete or deliberately absent until this line is signed by a human.
```

---

## What to notice (calibration notes, not findings)

- The **Save button** is the archetypal case this skill exists for: an async action drawn with three states validates as a Button and ships without loading, error, or success. The inventory does not say the design is wrong; it says five applicable states are not shown and hands the ruling to a human.
- The **list** shows how a data view's four states are read: drawn populated, the other three `MISSING` because the source is async (fetched on load). Had the list been static history compiled in, empty / loading / error would be `n/a`.
- The **copy slots** stop at the slot name. "Saving…", "Couldn't save your settings", "Nothing sent yet" are obvious strings and the skill still does not write them — that is area 3's, in the client's voice. Area 3's `microcopy-states-writer` merges its candidate strings back into these `copy_slot.string` fields; the schema types the field `string | null` as of v0.1.2, so that merged sidecar validates. This worked example shows the empty slots this skill writes (every `copy_slot.string` here is `null`).
- The **keyboard column** cites the APG pattern per row and copies nothing else from the map; whether the tab strip *is* a Tabs widget rather than three links is `heyhi-a11y-annotation`'s role call.
- The **below-44px** flag on the tabs is the served floor, not a conformance claim: WCAG's minimum is 24 px, and the accessibility audit is the place that claim is made.
- The **disabled-reason-unshown** flag on Save sits on a state that is itself MISSING: it flags a *candidate rule* ("disabled until a change is made"), so if the human rules the disabled state deliberately absent the flag falls with it. A flag on an inference is still a flag, never a verdict.

*HeyHi Confidential. Synthetic throughout.*
