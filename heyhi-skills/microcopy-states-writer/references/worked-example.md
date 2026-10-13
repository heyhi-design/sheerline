---
classification: confidential
title: "Worked example — a filled Microcopy Set"
skill: microcopy-states-writer
loaded_by: "SKILL.md Step 1 (calibration)"
---

# Worked example — a filled Microcopy Set

**Synthetic input, invented product, invented voice. No client content.** Read this to calibrate the register and depth of the free-prose slots; do not copy its strings. The empty slots are shown empty on purpose: that is the output shape.

**Synthetic inputs brought by the (invented) team.** A confirmed voice system for *Ledgerling*, a small-business bookkeeping app (voice in one line: "Plainly, like a bookkeeper who has seen your kind of month before"; confirmed attributes: *plainspoken*, *steady*, *exact*; calibration axis *calm ←→ brisk*, sitting at calm for error states and brisk for in-product copy). And an Interaction Inventory sidecar for its *Receipts settings* screen (`worked-example.input.sidecar.json`): a Save button drawn without its async states, a recent-receipts list drawn populated only (area 4 flagged its error state `error-no-recovery`), and a camera-permission dialog. Seven copy-bearing rows; two flags stand at the end.

---

```
# Microcopy Set — Receipts settings (Ledgerling, synthetic)
Voice: Voice System: Ledgerling (synthetic) · confirmed: yes
States: inventory sidecar worked-example.input.sidecar.json (SYNTH-0002 node 8:120)
Drafted: 2026-09-05   Intake: brand_voice_source = the Ledgerling voice system · dash_rule = zero · sealed: yes (synthetic)

## Strings (one row per copy-bearing state; every string a candidate)
| Element | State | Slot | Candidate string [candidate — agent-drafted] | Constraints | Doctrine | Lineage |
| Save button | loading | Loading | "Saving your settings." | inline · ≤40ch · none | expectation: set | new |
| Save button | error | Error | "The save didn't go through ({condition}). Try again." | inline · ≤80ch · {condition}: held | next-step: retry · condition: from trigger, held as a variable (the trigger is a disjunction, "request timed out or 5xx"; naming one arm would assert a cause the row did not single out) | new |
| Save button | success | Success | "Settings saved." | toast · ≤40ch · none | done + nothing to over-celebrate | new |
| Recent receipts list | empty | Empty | "No receipts yet. Scan your first one to start the list." | panel · ≤80ch · none | action: named (scan) | new |
| Recent receipts list | loading | Loading | "Pulling your recent receipts." ⚠ spinner-where-skeleton | panel · ≤60ch · none | expectation: set | new |
| Recent receipts list | error | Error | ⚠ FLAG next-step-unsupplied — area 4 flagged error-no-recovery on this view; the recovery path (reload the list? fall back to cached rows?) is a product decision | panel · ≤80ch | condition: from trigger ("GET /receipts failed") · next-step: UNSUPPLIED | — |
| Camera permission prompt | success | Success | "Camera on. Point it at a receipt." | inline · ≤60ch · none | what is now possible: named | new |
Legend: ⚠ = a flag for the human · the 7 `no copy` rows in the inventory (the Save button's default, hover, focus-visible, active, disabled; the list's populated; the dialog's default) are omitted, not invented

## Flags (findings for the human, never verdicts)
- next-step-unsupplied: Recent receipts list / error — inherits area 4's error-no-recovery; no next step is drafted until the structure decides one
- spinner-where-skeleton: Recent receipts list / loading — the source shows a bare spinner over a view that has row structure; a skeleton of the rows would say more than the string

## Claim / SLA guardrail (held for confirmation; nothing here is copy)
[Empty — none of the seven candidates asserts a timeframe, guarantee, security, compliance, performance figure, or price.]

## Candidate glossary (terms and conflicts; no rulings)
| Term | Where | Candidate definition | Conflict seen |
| receipt | receipts list; camera prompt | One scanned or imported expense record. | The source's tab label says "Expenses" for the same objects |

## Open questions for the team (questions, not judgments)
- When the receipts list fails to load, is there a cached copy to fall back to, or only a reload? That decides whether the error row gets `alternative` or `retry`.
- Does "Settings saved." need to say *which* settings when several sections save together, or is one confirmation enough?
- Is "receipt" or "expense" the word the product uses everywhere? The list and the tab disagree.

## Near-misses and unchecked territory (traces, no verdicts)
- Considered and set aside: "Saved!" for Save/success — the voice's *steady* attribute rules out the exclamation, and the calibration grid sits at calm for confirmations.
- Considered and set aside: "Something went wrong. Try again." for Save/error — names the category, not the condition; the trigger supplied "timed out", so the specific form won.
- Could not check: whether the camera prompt's *denied* path returns to a state with its own copy — the inventory records the denied transition as closing the dialog, with no copy-bearing state, so nothing was drafted for it.

## ⛔ Which copy ships — NEEDS HUMAN
   Per row: accept the candidate / rewrite it / ask for alternates. Nothing above is final until marked here: ____________________

## ⛔ Tone calls on flagged strings — NEEDS HUMAN
   Each ⚠ above resolved, in the client's voice: ____________________

## ⛔ Terminology rulings — NEEDS HUMAN
   receipt vs expense: ____________________

## Named gate
Sign-off owner (content lead / brand owner): ____________________  Date: ______
No string ships, and no flagged string is resolved, until this line is signed by a human.
Voice-definition sign-off is inherited from the voice system's own gate; if that line is unsigned, this set is candidate-only twice over.
```

**Sidecar.** `worked-example.sidecar.json` is this set's machine-readable half: seven `strings[]` rows keyed by (`element_id`, `state`), the two flags in their rows' `doctrine.flags`, an empty `claims_held`, one glossary entry, and `judgment` / `gate` null. It validates against `microcopy-schema.json`; every (`element_id`, `state`) pair is one of the input sidecar's seven non-null `copy_slot` rows; a merge into the input would change only `copy_slot.string` on those rows (that merged document is a proposal the inventory's owner applies; as of interaction-inventory v0.1.2 the inventory types the string as `string | null`, so the merge validates against `inventory-schema.json`).

**What to notice.** The error row for the receipts list carries **no string** and a flag, not a hopeful "Try again": area 4 said the view has no recovery path, so the writer has nothing to type a next step against. The Save error holds its condition as a variable: the trigger supplied a *disjunction* ("request timed out or 5xx"), so naming "timed out" alone would assert one arm the row did not single out; the shape is drafted, the arm is the human's or the row's to settle (a row with a single trigger gets the specific form, as the Export row in the SKILL.md template shows). The loading rows set an expectation without a duration (a duration is a claim). Nothing in the set decides which candidate ships.

---

*HeyHi Confidential. Reference for `microcopy-states-writer`. Synthetic throughout: Ledgerling, its voice, and its screen are invented for calibration.*
