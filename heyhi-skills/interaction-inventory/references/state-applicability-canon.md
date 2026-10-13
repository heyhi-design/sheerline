---
classification: confidential
title: "State-applicability canon — the inventory discipline around the control-state contract"
skill: interaction-inventory
loaded_by: "SKILL.md Step 1"
---

# State-applicability canon — the inventory discipline

The method knowledge `interaction-inventory` loads to enumerate a screen. It is authored here as the layer *around* the served control-state contract; the contract itself (A.3 in `ai-services/design-intelligence/design-fundamentals.md`, served as `design-system://fundamentals`) is **retrieved, never restated** — this file names its states only to say which apply where. The always-loaded behavioral invariants the skill obeys live in `sheerline/os/operating-principles.md` and are cited, not restated. Everything here is scaffolding for a human decision: none of it rules an absence deliberate, judges the behavior, or writes copy.

---

## 1. The contract (pointed at)

The state set is A.3's: **default / hover / focus-visible / active / disabled / loading / error**, plus **success** and **selected** where the control's function calls for them. Each state's required visual change, trigger, and accessibility hook are defined there. This canon adds one rule the contract implies and the served token validator cannot check: **a control that omits an applicable state is incomplete even when every token validates** (the A.5 / G1B proof: a four-state Button passed at confidence 1.0). Deciding "applicable" is § 2.

Data views carry a second, smaller set from A.2's assumed floor: **empty / loading / error / populated**.

Naming note: A.3 names the keyboard-focus state `focus-visible` (the CSS `:focus-visible` mechanism; the ring must not fire on a mouse click). The `heyhi-mcp` validator's manifest slot is literally `focus`. The inventory and its sidecar use the contract's name; § 9 gives the mapping for any consumer that feeds the validator.

---

## 2. Element-class applicability matrix (authored)

Applicability is decided by **class**, mechanically, before anyone looks at the design. `applies` = the inventory expects the state and flags it `MISSING` when the source does not show it; `n/a` = the class never carries it; `if-async` / `if-…` = applies only when the named condition holds (state the condition in the row's note).

| Class | Examples | default | hover | focus-visible | active | disabled | loading | error | success | selected |
|---|---|---|---|---|---|---|---|---|---|---|
| **action** | button, icon button, submit, destructive action | applies | applies (web) | applies | applies | if-disable-able | **if-async** | if-async (the action can fail) | if-async (confirmation) | if-toggle (`aria-pressed`) |
| **link** | in-page link, nav link | applies | applies (web) | applies | applies | n/a | n/a | n/a | n/a | if-current (`aria-current`) |
| **text input** | text, email, number, textarea, search | applies | n/a (focus, not hover, is the signal) | applies | n/a | if-disable-able | n/a (validation is sync; async lookups belong to the composite) | **applies** | if-validated (inline confirmation) | n/a |
| **selection control** | checkbox, radio, switch | applies | applies (web) | applies | applies | if-disable-able | n/a | if-validated (a required group) | n/a | **applies** (`aria-checked`) |
| **composite** | tabs, menu, combobox, dialog, disclosure, listbox, slider | applies | applies (web) | applies | applies | if-disable-able | if-async (combobox lookups, lazy panels) | if-async | n/a | **per APG pattern** (`aria-selected` / `aria-expanded` / `aria-checked`) |
| **data view** | list, table, card grid, chart | populated | n/a | applies (if rows are focusable) | n/a | n/a | **if-async** (with empty + error) | **if-async** | n/a | if-selectable rows |
| **static** | heading, paragraph, image, divider | n/a (a `readonly` flag only) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

Reading the matrix for a **data view**: an async-bound view carries **all four** of empty / loading / error / populated; a static view carries populated only and the other three are `n/a by class`. A view whose data source is unknown is flagged `source-unknown` and treated as async (the conservative read) until the human says otherwise.

Two rules that override any cell: **hover is never the sole signal** for a state (A.3; touch has no hover), so a `hover`-only differentiation of any other state is flagged `hover-only`; and **every focusable element carries `focus-visible`** (A.1 rule 1, the accessibility gate), so a focusable element with no focus state is `MISSING`, never `n/a`.

---

## 3. The data-view rule (authored)

| Data source | empty | loading | error | populated |
|---|---|---|---|---|
| async (fetched, searched, filtered, paginated) | applies | applies | applies | applies |
| static (compiled in, never changes at runtime) | n/a | n/a | n/a | applies |
| user-generated but local (a form the user fills, no fetch) | applies (before first entry) | n/a | if-validated | applies |
| unknown | treat as async; flag `source-unknown` | | | |

The **empty** state of a data view is the one copy-bearing state that is most often absent by omission rather than decision; it is always a `MISSING` flag when not shown, and the ruling is the human's.

---

## 4. Transition rules and the flag taxonomy (authored)

Every non-default state has a **named entry trigger** and an **exit path**. The inventory drafts them as candidates; the rules below decide what gets flagged.

| Rule | Flag when violated | Source |
|---|---|---|
| **loading** needs an async trigger and **both** a success exit and an error exit | `loading-no-error-exit` (only the happy path is drawn) | A.2 law 8 (visibility of system status + Doherty); A.3 loading row |
| **error** needs an inline recovery path — never a dead end | `error-no-recovery` | A.2 law 9 (forgiving inputs); the area-3 doctrine "an error with no next step is a dead end" is the copy-side twin |
| every state is reachable (has at least one entry) | `unreachable` | state-machine hygiene |
| every non-terminal state has an exit | `dead-end` | state-machine hygiene |
| **disabled** is communicated programmatically (`disabled` / `aria-disabled`); contrast is out of scope | `disabled-not-programmatic`; and `disabled-reason-unshown` when nothing on the surface says *why* (a design question for the human, not a contract failure) | A.3 disabled row |
| **hover** never the sole signal | `hover-only` | A.3 hover row |
| **selected** indicator contrasts against the component's own surface | `selected-invisible` | A.3 selected row; the `ds-active-ring-invisible-on-component-bg` correction (the recorded failure) |
| **focus-visible** on every focusable, non-color-only | `MISSING` on the focus cell | A.1 rule 1; validator Rule 5 |
| target ≥ 44 × 44 px across every state | `below-44px` | validator Rule 3; A.3 touch floor. **This is the served contract's floor.** WCAG 2.2 SC 2.5.8's legal minimum is 24 × 24 (`heyhi-a11y-annotation` flags at 24); the inventory flags at 44 and labels it as the served floor, not a conformance claim |
| a data view's source is unknown | `source-unknown` | § 3 |

A flag is a finding for the human. **No flag is a verdict, and no flag blocks anything.** The `MISSING` cell and every flag above stay as filed until the named gate rules on them.

---

## 5. The microinteraction structural model (authored)

Microinteractions are **structural, not decorative** (buildout research § 4.2): they clarify hierarchy and preserve continuity. Per element the inventory reads the standard microinteraction anatomy — **trigger → rules → feedback → loops and modes** — and fills each part mechanically:

- **trigger**: what starts it (a pointer event, a key, a gesture, a system event such as a fetch completing);
- **rules**: what happens, expressed as the transition (from → to) and its guard (an async result, a validation result);
- **feedback**: the state change the user perceives *and* a machine can read — A.3's visual-change column paired with its accessibility-hook column, never one without the other;
- **loops and modes**: what changes on repeat (a second submit while loading is blocked; a toggle alternates), and any mode the element has (edit vs. read).

Which of these deserve design attention is the human's slot (⛔ Which interactions matter).

---

## 6. Timing (pointed at)

The Doherty threshold (~400 ms) and visibility of system status are A.2 law 8: a loading affordance appears immediately past the threshold; a terminal state (success or error) is always shown. This canon adds no timing numbers of its own; the numbers a motion system emits are `motion-system-author`'s.

---

## 7. Focus, keyboard, and the gesture floor

**Keyboard (pointed at, consumed in place).** The keyboard column is filled **from `heyhi-skills/heyhi-a11y-annotation/references/apg-pattern-map.md` by APG pattern** (native element first; the first rule of ARIA). The inventory cites the pattern it used per row (`keyboard: per APG "Tabs"`); it copies no row of the map into its own output beyond the interaction it applies. Whether the element really *is* that pattern (a tab vs. a link) is `heyhi-a11y-annotation`'s human-confirmed role call, not this skill's.

**Gesture floor (authored, thin).** On touch surfaces the triggers are tap / long-press / swipe / drag / pinch, each a *trigger* in § 5. No hover exists on touch, so any hover-only signal is flagged. Pull-to-refresh and haptic feedback follow `ux-guidelines.csv` rows 26–27 (in `heyhi-skills/ui-studio/data/`): disable pull-to-refresh where it is not needed; do not vibrate on every tap. What a gesture *means* on this surface (does a swipe delete, archive, or reveal?) is the human's.

---

## 8. The copy-slot map (the states seam with area 3)

The inventory emits an **empty copy slot** on every state that carries a string, keyed to the UX-writing taxonomy in `heyhi-skills/voice-system-author/references/voice-system-template.md` Part 3 (eight core slots plus two extended). The map from contract state to slot is fixed here because the taxonomy is organized by content type, not by state:

| Contract state | Taxonomy slot | Note |
|---|---|---|
| loading | **Loading** (core 7) | skeleton over spinner is the area-3 doctrine; the inventory names the slot only |
| error | **Error** (core 2) | the area-3 doctrine requires a next step; the inventory's `error-no-recovery` flag is the structural twin |
| success | **Success** (extended 9) | an extended slot, which is why the vocabulary is "8 + 2", not "8" |
| a data view's empty | **Empty** (core 1) | the most-omitted copy-bearing state |
| populated | none | its copy is content, not a state string |
| default / hover / focus-visible / active / disabled / selected | **none** (`copy_slot: null`) | visual and programmatic changes, not strings; a disabled control's *reason*, where shown, is Tooltip or Form-label copy on the element, not a state slot |

The sidecar schema enumerates the ten slot names as a validation guard — a deliberate coupling to the template: a rename there must be mirrored in `inventory-schema.json`. The string is always `null` when this skill writes it. Area 3's `microcopy-states-writer` fills it against the client's voice; until it exists, a human does, or `voice-system-author`'s Audit mode lints what someone drafted. The reverse fallback also holds: until this inventory ships for a screen, the writer may take a state list from the human or from `heyhi-prototype-audit`'s scope count, **in the same sidecar shape**, so no second state schema grows.

---

## 9. Provenance labels and the validator-slot mapping

Every element carries one of `from-source` (read from the design or build), `from-list` (named by the human, nothing read), `inferred` (added by the skill to complete the structure). Every transition is `candidate — agent-drafted`. Every state cell is `shown` / `MISSING` / `n/a`. Anything modeled for illustration is `synthetic`.

**State-level source.** A state's `source` says where its status came from: `shown` ⇒ `from-source` (read from the design or build); `MISSING` ⇒ `inferred` (the skill inferred from the element class that the state applies; nothing was read); `n/a` ⇒ `n/a`. A state with `source: inferred` is therefore never `shown` — an inferred state presented as shown is the provenance failure eval `ii-05` guards.

**Markdown → sidecar mapping.** The markdown inventory and the sidecar say the same thing in two registers: matrix cells `shown` / `MISSING` / `n/a` → `status` `shown` / `missing` / `n/a`; class labels `text input` / `selection control` / `data view` → `text-input` / `selection-control` / `data-view`; a data view's four states (`empty` / `loading` / `error` / `populated`) sit in one spanning matrix row in the markdown and as four named states in the sidecar; `n/a` cells may be omitted from the sidecar (a state absent from `states[]` is `n/a` by class), while `shown` and `missing` states are always listed; the keyboard column cites the APG pattern plus the interaction it applies in the markdown, and the pattern name only (or `native <element>`) in the sidecar; **every exit path the markdown states is a sidecar transition whose `from` is that state** (the area-3 seam schema's `exit` field is that transition), and a `dead-end` flag is derived from a non-terminal state with no such transition; a `static` element carries a single `default` state with status `n/a` and the `readonly` flag, nothing else.

**`focus-visible → focus`.** The sidecar uses the contract's state names. A consumer that feeds the `heyhi-mcp` validator (whose Rule 5 checks a manifest slot literally named `focus`) maps `focus-visible` to the `focus` slot, implemented as `:focus-visible` — the reconciliation A.3 itself records as a one-line validator change to schedule, not something this skill resolves.

---

*HeyHi Confidential. `skill-updates/interaction-inventory/references/`. Authored 2026-09-05 from `plans/plan-sheerline-p3-interaction-design-2026-09-04.md` § 2.2 F / § 3 / § 4 and `sheerline/os/foundations/interaction-design/FOUNDATION.md` § The knowledge canon. The contract it enumerates against is retrieved, never restated.*
