---
classification: confidential
title: "States-copy canon — the per-state writing discipline"
skill: microcopy-states-writer
loaded_by: "SKILL.md Step 1 (the method spine)"
---

# States-copy canon — the per-state writing discipline

The layer a per-state writer needs *around* the canon `voice-system-author` already carries. Held as read-and-apply reference. On-demand: load when running the writer.

*Internal operational reference. This skill is about copy, so this reference is written to its own read-aloud and plain-punctuation discipline.*

**What this file does not carry, on purpose.** The voice block and the calibration axis (`voice-system-template.md` Parts 1–2), the taxonomy's slot list and per-slot pattern (Part 3), the two doctrine rules (Part 4: an error with no next step is a dead end; a loading state prefers a content skeleton), the claim guardrail (Part 5), and the four lint families (`flattening-lint-checklist.md`) are the canon of record in `heyhi-skills/voice-system-author/references/`. This file cites them and restates none. The slot names appear here only as the state → slot map's right-hand column (§ 1) and, in `microcopy-schema.json`, as an enum copied from the deployed inventory schema as a validation guard.

---

## 1. The state → slot map (co-owned with area 4; the byte-identical line)

The taxonomy is organized by content type, not by state, so the map from a contract state to a slot is fixed once and carried in three places with the same wording: the area-4 spec § 4 on `main` (`plans/plan-sheerline-p3-interaction-design-2026-09-04.md`, the contract of record), the area-3 foundation, and this file. The area-4 canon (`heyhi-skills/interaction-inventory/references/state-applicability-canon.md` § 8) carries the same map as a six-row table, and its foundation states it by pointer. The line:

`loading` → Loading; `error` → Error; `success` → Success (an *extended* slot, which is why the vocabulary is 8+2); a data view's `empty` → Empty; `populated` → none (its copy is content, not a state string). **hover, focus-visible, active, disabled, selected carry no slot** (`copy_slot: null`): they are visual and programmatic changes, not strings. A `disabled` control's *reason*, where one is shown, is Tooltip or Form-label copy on the element, not a state slot.

The deployed inventory schema spells the slot names as its enum does (`Form label`, with a space). The writer **copies the inventory's spelling** into its own sidecar and never renames a slot.

## 2. The per-slot anatomy (pointed at, with two additions)

Each slot's parts are the "pattern to draft" column of `voice-system-template.md` Part 3; the writer drafts against that column and does not carry a second copy of it. Two additions the writer applies on top, because they are checkable per string and Part 3 states them as intent:

- **Error** — the "what went wrong" half must be *specific to the condition* and the "next step" half must be a *typed* next step (§ 3), so completeness can be judged before quality.
- **Loading** — the "what is coming" half names the object, not "data"; and Part 4's skeleton rule applies where the view has structure (cited, not restated).

A string missing a Part 3 part is incomplete, not wrong; the writer completes it or flags what it cannot complete.

## 3. The next-step anatomy, the specificity rule, and the loading rules

**The next-step anatomy.** "Carries a next step" is checkable, not felt. Every Error string names at least one of:

| Type | The shape | Example |
|---|---|---|
| `retry` | the same action, again | "Try again." |
| `edit` | change the input named | "Use a file under 25 MB." |
| `alternative` | a different path to the same end | "Or split it into two uploads." |
| `wait` | with the expected duration | "It should be back in a few minutes." (the duration is a claim; § 5) |
| `contact` | with the channel | "Write to support@…" |

A next step the writer cannot supply because the recovery path is undecided is a **`next-step-unsupplied` flag**, never filler. "Please try again later" with no reason is a dead end wearing a next step. **An undecided recovery path is always a flag, never a typed step:** typing `retry` asserts that retrying recovers, which the structure has not decided. When the inventory row already carries area 4's `error-no-recovery` flag, the writer inherits it as the reason for its own flag and drafts no next step the structure cannot support.

**The specificity rule.** An error names the *condition* the person can act on (the 25 MB limit), not the *category* ("a validation error"). **The condition is an input.** It is read from the state row's transition `trigger` (the inventory's `transitions[].trigger`, or the fallback list's trigger field) or from the source's existing string. A condition the writer was not given is a **`condition-unsupplied` flag** carrying a `{condition}` variable, held. A writer that supplies "check your connection" for a save it knows nothing about has asserted a product fact.

**The loading rules.** A Loading string states what is coming, never "please wait." A *duration* in a Loading string is a timeframe claim under § 5 and ships only as `{claim}` unless the state row supplies a measured value. When the source shows a bare spinner on a structured view, flag **`spinner-where-skeleton`** (Part 4's rule; the writer flags, the design decides).

**The data-view floor** (A.2 in `ai-services/design-intelligence/design-fundamentals.md`). A view bound to async data carries Empty / Loading / Error copy; a static view carries none. When the supplied list omits a copy-bearing state the floor requires, record it under the sidecar's top-level **`missing_states`** (element, view state, reason), a copy-side cross-check of the inventory's own `MISSING` cell; it lives outside `strings[]` because an omitted state is, by definition, not one of the list's rows. The writer never adds the state and never drafts a string for a state the list does not carry.

## 4. String constraints (fields, not prose)

Every drafted string carries:

- **placement** — inline / toast / banner / dialog / panel;
- **length budget** (`max_chars`) where the surface has one (a toast, a button, a table cell; a config's `ux_writing` block may name one, as HeyHi's does for tooltips);
- **variables** — every `{name}` in the string, each with its **plural forms** where a count can vary (`{count}` → "1 file" / "{count} files"), and `held: true` for `{claim}` and `{condition}`.

A string with an unfilled variable or an unstated plural is incomplete. Localization is out of scope in v1; the fields exist so a later locale pass has something to read.

## 5. The claim hold (Part 5, extended)

Any drafted string that asserts an SLA, guarantee, timeframe, uptime, security posture, compliance status, or performance number is not shippable copy until the client confirms it (Part 5; lint Family 2). **Extended here:** a **price or rate** in a string is the same hold (HeyHi's pricing rule generalized to the client's copy). The string keeps the *shape* with a `{claim}` variable; the assertion moves to the guardrail as `NEEDS CLIENT CONFIRMATION`.

## 6. The candidate glossary

A product says one thing by one name. Per run the writer keeps a candidate glossary: term · where it appears · candidate definition · conflicts seen (the same thing named two ways, or one name used for two things). The writer flags the conflict and never rules on it. When Information Architecture is in scope, the source of terms is real user vocabulary (the User Research → IA dependency in `sheerline/os/foundations/user-research/FOUNDATION.md`), not designer coinage.

## 7. The fallback list (one schema, two producers)

Until an inventory exists for a screen, the writer takes a **human-written** state list **in the inventory's own sidecar shape** (`heyhi-skills/interaction-inventory/inventory-schema.json`), with `source.kind: list` and each element `provenance: from-list`. The four minimal fields a human writes map onto it:

| Human field | Sidecar location |
|---|---|
| `element` | `elements[].id` (kebab-case) and `elements[].name` |
| `state` | `elements[].states[].name`, with `status: shown` or `missing` and `source` per the inventory's rule |
| `trigger` | `elements[].transitions[].trigger` (the writer reads it as the error *condition*; absent → `condition-unsupplied`) |
| `exit` | `elements[].transitions[].to` (absent or unknown on an `error` row → `next-step-unsupplied` by default) |

Where a list row carries no `copy_slot`, the writer applies § 1 to derive it. A fallback list is the human's enumeration; the writer never extends it. `heyhi-prototype-audit`'s Step 2 scope count is a number the human may use to cross-check the list's completeness; it never produces a row.

## 8. The write-back rule

The writer's sidecar (`microcopy-schema.json`) keys each string by (`element_id`, `state`), which map to the inventory's `elements[].id` and `states[].name`; `missing_states` sits beside `strings[]` and is never merged (nothing in the inventory corresponds to it). A consumer merging it into the inventory sidecar sets only `elements[].states[].copy_slot.string` on matching rows, copies `taxonomy_slot` in the inventory's spelling, and touches nothing else; the inventory's `judgment` and `gate` stay the inventory's. **As of interaction-inventory v0.1.2 (2026-09-07), the inventory schema types `copy_slot.string` as `string | null`**, so a merged document validates against it: the writer's sidecar is validated against `microcopy-schema.json` on its own, and the merge into the inventory sidecar is a *proposal* the inventory's owner applies. The widening was a convergence agreement item for area 4 (decision-log 2026-09-05 seam agreement item 4), never this skill's edit.

## 9. Provenance and the empathy check

Every string is `[candidate — agent-drafted]` with lineage (`new`, or `revised-from` with the source string). The voice reference and its `confirmed` state, and the state list's source, sit once at the top of the sidecar. A string that names what the user feels ("we know this is frustrating") is cognitive-empathy simulation (`sheerline/os/operating-principles.md` § The zero-cost operating invariants) and is tagged **`empathy-simulated`** for the human's ruling on whether the product may say it.

---

*HeyHi Confidential. Reference for `microcopy-states-writer`. Spec source: `plans/plan-sheerline-p3-content-design-2026-09-05.md` § 2.2 F / § 3 / § 4. Canon of record for the voice model, the taxonomy, the doctrine, the guardrail, and the lint: `heyhi-skills/voice-system-author/references/`. The seam's structural contract: `plans/plan-sheerline-p3-interaction-design-2026-09-04.md` § 3.5 / § 4.*
