---
title: "Reference: the widget → ARIA APG pattern map"
classification: confidential
skill: heyhi-a11y-annotation
status: staged
---

# Widget → ARIA APG pattern map

**HeyHi Confidential.** The mapping Step 2.7 uses to attach an accessibility contract to each composite widget it detects. For each pattern: the **detection heuristic** (what design pattern maps to it), whether a **native element** carries the role, the **name/role/value** the build must expose, and the **keyboard interaction** the build must implement. Source: the W3C ARIA Authoring Practices Guide (APG) patterns and WCAG 2.2. This is a reference for the human-confirmed role call, not an assertion: the role always ships `[candidate: needs confirmation]`.

## The first rule of ARIA (the gate on this whole reference)

**Prefer native HTML. No ARIA is better than bad ARIA.** Use an APG pattern only where a native element cannot carry the role and state. A native `<button>`, `<a href>`, `<input type=checkbox>`, `<select>`, `<dialog>`, or `<details>/<summary>` is more robust than a `<div>` with roles bolted on, and it brings its keyboard behavior for free. Every row below names the native element first; reach for the ARIA pattern only when the "Native" column says none exists or the design genuinely cannot use it. A `<div>` acting as a control is a **missing-by-construction flag** (Step 2.8), not a pattern to spec around.

## The map (common web patterns)

| Widget (detection heuristic) | Native element | Role(s) | Name / value / state | Keyboard interaction |
|---|---|---|---|---|
| **Button** (clickable, performs an action) | `<button>` | `button` | name from text or `aria-label`; toggle exposes `aria-pressed` | Enter and Space activate |
| **Link** (navigates to a URL/anchor) | `<a href>` | `link` | name from link text | Enter activates |
| **Disclosure** (show/hide one region: FAQ item, "more") | `<details>/<summary>` | `button` + `aria-expanded` | `aria-expanded` true/false; `aria-controls` the region | Enter/Space toggle |
| **Accordion** (stacked disclosures) | `<details>` ×N | each header `button` + `aria-expanded` | per-panel expanded state; `aria-controls` | Enter/Space toggle; optional Up/Down between headers |
| **Tabs** (one panel visible, tab strip switches) | none | `tablist` / `tab` / `tabpanel` | selected tab `aria-selected`; `aria-controls` → panel; panel `aria-labelledby` → tab | Arrow keys move between tabs; Enter/Space (or auto) select; Home/End |
| **Checkbox** (on/off, independent) | `<input type=checkbox>` | `checkbox` | `aria-checked` true/false/mixed | Space toggles |
| **Radio group** (one of many) | `<input type=radio name=…>` | `radiogroup` / `radio` | group name; `aria-checked`; roving tabindex | Arrow keys move + select within group; Tab enters/leaves the group |
| **Switch** (on/off toggle, distinct from checkbox) | `<button aria-pressed>` or `<input type=checkbox role=switch>` | `switch` | `aria-checked` true/false | Space (and Enter) toggle |
| **Combobox** (text input + popup list; autocomplete/search) | `<input>` + listbox | `combobox` / `listbox` / `option` | `aria-expanded`; `aria-controls`; `aria-activedescendant`; selected `option` | Down opens/moves; Arrow keys navigate; Enter selects; Esc closes |
| **Listbox / Select** (choose from a fixed list) | `<select>` | `listbox` / `option` | selected `option` `aria-selected` | Arrow keys move; Enter/Space select; Home/End; type-ahead |
| **Menu / Menu button** (actions popup) | none | `button` + `menu` / `menuitem` | button `aria-haspopup` + `aria-expanded`; `menuitem`s | Enter/Space/Down open; Arrow keys navigate; Esc closes; Tab closes |
| **Modal dialog** (blocks the page) | `<dialog>` | `dialog` (`aria-modal=true`) | `aria-labelledby` (title) / `aria-describedby` | focus moves in on open, is **trapped**, returns to trigger on close; Esc closes |
| **Alert dialog** (confirm/destructive) | `<dialog>` | `alertdialog` | `aria-labelledby` / `aria-describedby` | as dialog; initial focus on the least destructive action |
| **Tooltip** (supplemental text on hover/focus) | none | `tooltip` | trigger `aria-describedby` → tooltip; must be hoverable + dismissable (SC 1.4.13) | Esc dismisses; appears on focus, not hover-only |
| **Slider** (pick a value on a range) | `<input type=range>` | `slider` | `aria-valuenow` / `aria-valuemin` / `aria-valuemax` / `aria-valuetext` | Arrow keys step; Home/End; PageUp/PageDown |
| **Spinbutton** (numeric stepper) | `<input type=number>` | `spinbutton` | `aria-valuenow/min/max` | Up/Down step; Home/End |
| **Data table** (rows × columns of data) | `<table>` | `table` + `<th scope>` | column/row headers associated via `scope` or `headers` | native table navigation |
| **Toast / status message** (transient, non-blocking) | none | `status` / `alert` (live region) | `aria-live` polite/assertive; not focus-stealing | none (announced, not focused) |
| **Breadcrumb** (path trail) | `<nav>` + `<ol>` | `navigation` + list | `aria-label="Breadcrumb"`; current `aria-current=page` | native link nav |
| **Carousel** (rotating content) | none | group + controls | prev/next `button`s named; rotation pausable (SC 2.2.2); slides labelled | button activation; pause control reachable |
| **Tree view** (expandable hierarchy) | none | `tree` / `treeitem` / `group` | `aria-expanded` on parents; `aria-selected`; level via `aria-level` | Arrow keys navigate + expand/collapse; type-ahead |

## Cross-cutting contracts every interactive element inherits (the A.1 gate)

Independent of the specific pattern, the annotation specs these because the Sheerline A.1 accessibility gate folds them in (`sheerline/os/operating-principles.md`):

- **Visible focus.** Every interactive element has a visible focus indicator (WCAG 2.2 SC 2.4.7, 2.4.11 Focus Not Obscured, 2.4.13 Focus Appearance). The design must show the focus state, not leave it to the browser default alone.
- **Minimum target size.** 24×24 CSS px (SC 2.5.8), specced in Step 2.6.
- **A distinct state per control.** Default, hover, focus, active, disabled, and the widget's own state (pressed/expanded/checked/selected) each visually distinct (the A.3 control-state contract) and machine-readable (the name/role/value exposes it).
- **Keyboard reachable and operable.** Every control in the pattern reachable in a logical order, operable by keyboard, with no trap (except the deliberate, escapable dialog trap).

## Using this map (what it does and does not decide)

- **It decides the *spec*** — given a widget type, the name/role/value and keyboard contract are mechanical, pulled straight from the pattern. Step 2 attaches them.
- **It does not decide the *role call*** — whether the design's "tab-looking thing" is really a Tabs widget, a set of links, or a segmented button is a design decision. The map offers the pattern as a `[candidate: needs confirmation]`; the ⛔ role-calls slot is where the designer confirms it.
- **A native element beats a spec.** When the "Native" column names an element, the annotation's first recommendation is to use it and drop the ARIA. The ARIA columns are the fallback contract for when native cannot be used.

---

*HeyHi Confidential. Reference for `heyhi-a11y-annotation` (staged, `skill-updates/`). Patterns per the W3C ARIA APG; criteria per `sheerline/os/foundations/accessibility/FOUNDATION.md` and the A.1 gate in `sheerline/os/operating-principles.md`. No client content.*
