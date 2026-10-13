---
name: heyhi-a11y-annotation
description: >-
  Design-side accessibility prevention: annotate a design or prototype with the
  accessibility spec for engineering handoff, so accessibility is designed in, not
  audited after. Reads the design's structure (a ui-studio HTML prototype via the
  heyhi-design-bridge extractor, or a Figma design via get_design_context) and
  produces an annotation scaffold: a heading outline, a landmark map, a candidate
  focus/reading order, alt-text slots, name/role/value triples, and target-size
  checks, mapping each interactive element to its ARIA APG pattern and flagging what
  is missing by construction (an interactive element with no accessible-name source,
  a control with no associated label). Triggers include "annotate this design for
  accessibility", "a11y handoff spec", "accessibility redlines", "mark up headings
  and landmarks for handoff", "accessibility annotation for the engineers". The
  judged calls ship EMPTY behind a named designer sign-off: which alt text is
  actually correct, the reading-order INTENT, and the role calls. NOT a post-hoc
  WCAG conformance audit or a VPAT/ACR on a shipped build (use heyhi-a11y-audit).
  NOT translating a prototype into a Figma design file or vectorizing a raster (use
  heyhi-design-bridge). NOT a prototype interaction-completeness / readiness check
  (use heyhi-prototype-audit).
version: "0.1.1"
updated: "2026-09-12"
status: "Deployed — heyhi-skills/heyhi-a11y-annotation/; registered in the main + Sheerline subset registries (Sheerline Wave G-2, 2026-08-28). Sheerline area 8 (Accessibility), P2. Class X (extends heyhi-design-bridge): the accessibility-annotation sibling of design-bridge's Translate."
classification: HeyHi Confidential
---

# HeyHi Accessibility Annotation

**Sheerline area 8 (Accessibility) · P2 · class X (extends `heyhi-design-bridge`).** A designer has a design or a built prototype and is about to hand it to engineering. This skill reads that source's structure and produces the **accessibility spec for the handoff**: the heading outline, the landmark regions, a proposed reading order, the alt-text slots, the name/role/value triples for every control, the target-size checks, and the ARIA APG pattern each widget must implement. It is **design-side prevention**, the accessibility-annotation sibling of `heyhi-design-bridge`'s Translate: where Translate lands a prototype as Figma design layers, this lands the accessibility contract engineering builds against, so accessibility is designed in, not audited after.

**It never renders a conformance verdict.** That is the seam with `heyhi-a11y-audit`, which runs *after* the build and produces the ACR/VPAT. Annotation runs *before* the build, on the design, and produces the spec. Prevention, not conformance. (§ Routing.)

**The boundary this skill obeys (Sheerline § 9, absolute).** A structured artifact with explicit empty judgment slots, a named human gate, and provenance labels on anything the skill inferred or scaffolded. *The empty slots are the designer's calls:* which alt text is actually correct (decorative vs meaningful, and the words themselves), the reading-order **intent** (the skill proposes DOM/visual order as a labeled candidate; the intended order is a design decision), and the **role calls** (the skill maps a widget to an APG pattern and offers the role as a candidate; whether it really is a tab or a link, and whether the ARIA is right, is confirmed by a human). The skill scaffolds the slots and fills none of them. A version of this skill that writes the alt text, asserts the reading order as truth, or declares the role correct has exceeded its charter.

**It consumes structure; it does not re-read it from scratch.** Mirroring how `heyhi-a11y-audit` consumes the deterministic contrast floor rather than re-implementing contrast math, this skill consumes `heyhi-design-bridge`'s structure read: the Scene-Graph IR from its Playwright extractor for a prototype, or the Figma MCP `get_design_context` / `get_metadata` for a design. It adds the accessibility annotation layer on top; it re-implements no extraction.

> **This skill closes through the Exit Gate (`CLAUDE-SESSION-RULES.md § Exit Gate`).** See the bottom-of-skill bracket.

---

## Routing — disambiguation with sibling skills

| If the task is… | Use |
|---|---|
| Annotating a design/prototype with the a11y spec for engineering handoff (before build) | **this skill** |
| A WCAG-conformance verdict / ACR / VPAT on a *built* thing (after build) | `heyhi-a11y-audit` |
| Translating a built HTML prototype into a Figma **design** file (or vectorizing a raster) | `heyhi-design-bridge` |
| A prototype interaction-completeness / readiness check (are the states wired) | `heyhi-prototype-audit` |
| Headless render-and-verify of a prototype's deterministic checks (incl. the contrast floor) | `heyhi-prototype-verify` (staged, not yet deployed) |
| A flow / journey / IA artifact live in FigJam | `heyhi-figjam-mapper` |
| Whether the alt text is right, the reading order intended, the role correct | **the human** (this skill's named gate) |

The seam with `heyhi-a11y-audit` is **temporal and evidentiary**: annotation is design-side and produces a *spec to build to*; the audit is post-build and produces a *conformance claim*. Annotation never asserts conformance. The seam with `heyhi-design-bridge` is **object**: design-bridge produces the design artifact (mockup + doc frame); this produces the accessibility contract for it. `heyhi-a11y-audit`'s own scope line ("a full accessibility audit is a separate engagement") points back here for the prevention half.

---

## Step 0: Improvement hook check

Retrieve any recurring corrections for accessibility / annotation / handoff work (`retrieve_design_corrections` if the design MCP is reachable, or the Sheerline `os/corrections/` registry, `category: accessibility`). Fold a matching recurring correction into the pass. Skip silently if none.

## Step 1: Load context and route the input mode

1. **The source the human brought.** One of two input modes:
   - **Prototype (HTML).** A `ui-studio` / `heyhi-ui-ux` prototype. Read its structure through `heyhi-design-bridge`'s extractor (the Scene-Graph IR carries the DOM tree, tags, roles, `href`, images, and computed box sizes). Do not re-parse the HTML by hand when the IR is available.
   - **Design (Figma).** A Figma design file. Read layer structure and component types with the Figma MCP `get_design_context` / `get_metadata`. A design has no DOM, so heading level, landmark role, and accessible name are *intent to be declared*, which is exactly what the annotation captures.
2. **[references/annotation-spec-template.md](references/annotation-spec-template.md)**: the exact output structure, with every judged slot pre-marked empty. The artifact spine. Copy the structure; never copy example content into a real spec.
3. **[references/apg-pattern-map.md](references/apg-pattern-map.md)**. The widget → ARIA APG pattern map: the detection heuristic, the required name/role/value, the required keyboard interaction, and the first-rule-of-ARIA native-first note per pattern. The method reference for Step 2's mapping.
4. **The area-8 foundation** (`sheerline/os/foundations/accessibility/FOUNDATION.md`): WCAG 2.2 on POUR, the nine 2.2 criteria (incl. Target Size 24×24, Focus Not Obscured, Focus Appearance), ARIA APG + the first rule of ARIA, and the A.1 accessibility gate (visible focus, minimum target size, distinct state per control, machine-readable feedback). Register under it; do not author it. The **A.1 gate** in `sheerline/os/operating-principles.md` is the authority for the target-size and focus contracts this skill specs; point at it, do not re-derive it.

## Step 2: Build the annotation scaffold, mechanically

Every item below is mechanical work derived from the source structure. **None of it decides the alt text, the reading order, or whether a role is correct.**

1. **Heading outline.** Extract the heading structure (h1–h6 for a prototype; the intended heading levels for a Figma design, read from type-scale and layer naming as *candidates*). Emit the nesting as an outline and **flag skipped levels** (an h2 → h4 jump) and any page with no h1 or more than one. Skipped-level flags are mechanical; the fix (which level a heading should be) is the designer's.
2. **Landmark map.** Map the top-level regions to landmark roles: `banner` (header), `navigation`, `main` (exactly one), `complementary` (aside), `contentinfo` (footer), `search`, `region` (named). Prefer the native element (`<header>`/`<nav>`/`<main>`/`<aside>`/`<footer>`) over an ARIA role attribute (the first rule of ARIA). Flag content that sits in no landmark and any duplicate `main`.
3. **Reading / focus order (candidate).** Emit the source order (DOM order for a prototype, top-to-bottom / left-to-right visual order for a design) as a **labeled candidate** sequence of the interactive and landmark stops. Flag any place where visual order and DOM order diverge (a common tab-order trap). **The intended reading order is a judged slot, leave it empty** (§ Step 3); the candidate widens the designer's view, it does not decide the order.
4. **Alt-text slots.** For every image, icon, media, and background image carrying meaning, emit an **empty alt slot** plus a **decorative-vs-meaningful decision slot** (both judged). Never write the alt text. For an icon that is the only content of a control, cross-link it to that control's accessible-name slot (the name usually lives on the control, not a nested `alt`).
5. **Name / role / value triples.** For every interactive element, emit a row with: **role** (a *candidate* from the APG map or the native element), **accessible name** (an **empty slot**, the judged call), and **value / state** spec (the states the element must expose: `pressed` for a toggle, `expanded` for a disclosure, `checked` for a checkbox, `selected` / `current` where relevant). Role and name are per WCAG 4.1.2. The state spec is mechanical (it follows from the widget type); the *name* is the designer's.
6. **Target size checks.** Measure each interactive target's box. Flag any below the WCAG 2.2 SC 2.5.8 **24×24 CSS px** minimum (note SC 2.5.5 Enhanced 44×44 as the AAA aspiration where the profile asks for it), and check spacing where targets are close-packed. This is a mechanical measurement and a design-side fix *before* handoff: it is a flag, not a severity grade.
7. **APG pattern mapping.** For each composite widget detected (tabs, disclosure/accordion, combobox, dialog, menu, listbox, switch, slider, tooltip, and the rest of `references/apg-pattern-map.md`), attach the pattern's required name/role/value and keyboard-interaction spec as the build contract, with the **native-first note** (prefer a native element where one carries the role). The **role call ships as a candidate**: whether this really is a Tabs widget or a set of links is confirmed by a human.

   > Where a `role="dialog"` container is required, its build contract is the full set: `role="dialog"` + `aria-modal="true"` + a labelling attribute (`aria-labelledby` / `aria-label`) + focus moved into the dialog on open + a focus trap while open + Escape to close + focus returned to the invoker on close. Flag any modal container that lacks `role="dialog"` or any part of this contract; the container being a styled `div` shown by a class toggle is the common miss.
8. **Missing-by-construction flags.** Flag what the structure makes impossible to satisfy as-designed, without inventing the fix:
   - an interactive element with **no accessible-name source** (an icon-only button with no text, no `aria-label`, no labelled child),
   - a form control with **no associated label**,
   - a native control replaced by a role attribute on a non-interactive element — a `div`/`span` carrying `role=checkbox|radio|switch|button` where the native element (`input type=checkbox|radio`, `button`) would give state, keyboard behavior, and name for free (first rule of ARIA); note the read-only/disabled variant, which a role-div typically fakes with `tabindex=-1` and no `aria-disabled`,
   - a modal / dialog container lacking the Step 2.7 dialog contract (no `role="dialog"`, no `aria-modal`, no labelling attribute, or no focus management — focus not moved in on open, no trap, no return on close, Escape not handled or closing more than the dialog),
   - a heading level with no place in the outline, a control that exposes no state it needs.

   A missing-by-construction flag is a finding handed to the designer, never a fabricated name or role that papers over the gap.

## Step 3: Produce the Annotation Spec

Output the structure in `references/annotation-spec-template.md` exactly. Every scaffolded item carries a **provenance label** so a never-confirmed slot cannot roll into the handoff as if it were designed:

- `[scaffold: from structure]` — derived mechanically from the source (a heading level, a landmark, a target-size measurement).
- `[candidate: needs confirmation]` — a role call or a reading-order sequence the skill proposes for the human to confirm.
- `[inferred]` — anything the skill had to infer because the source was silent (a Figma design has no DOM, so a landmark or heading level read from layer naming is inferred).

The three judged slots stay empty by construction:

```
## ⛔ Alt text: NEEDS DESIGNER
Per image: decorative or meaningful? If meaningful, the alt text itself.
This slot is intentionally empty. The skill lists every image and its slot; it writes no alt text.

## ⛔ Reading-order intent: NEEDS DESIGNER
The candidate order (below) is source order, labeled. The INTENDED reading/focus order
is a design decision. This slot is intentionally empty.

## ⛔ Role calls: NEEDS DESIGNER
Each widget carries a candidate role + its APG spec. Whether the role is correct
(and whether native HTML should replace the ARIA) is confirmed here. Intentionally empty.

## Named gate (annotation sign-off)
Sign-off owner (the designer): ____________________   Date: ______
No accessibility annotation is handed to engineering until this line is signed by a human.
The sign-off attests: alt-text decisions made, reading-order intent set, role calls confirmed,
every missing-by-construction flag resolved.
```

**The spec is done when** every heading/landmark/target-size finding is a `[scaffold]` row, every interactive element has a name/role/value row (role candidate, name slot empty), every image has an alt slot and a decorative/meaningful slot (both empty), every composite widget carries its APG pattern spec, every missing-by-construction gap is flagged, and the three ⛔ slots plus the sign-off line are still blank.

## Step 4: Pre-flight verification

Confirm, before handing the spec back:

- No alt text was written and no image's decorative/meaningful call was made; every alt slot is empty.
- No reading order was asserted as intended; the emitted order is labeled `[candidate: needs confirmation]`, and the intent slot is empty.
- No role was asserted as correct; every role is `[candidate: needs confirmation]`, and the role-calls slot is empty.
- Every scaffolded item carries a provenance label; nothing inferred is presented as declared.
- At least the mechanical floor is complete: heading outline (with skipped-level flags), landmark map, target-size flags, name/role/value rows, APG specs, and missing-by-construction flags.
- Every missing-by-construction gap is a *flag*, not a fabricated name/role/label.
- The named sign-off line is present and unsigned.
- If any client asset or name is in play, the hermetic-seal / classification rules of the engagement profile hold (no client name on a shared Figma annotation layer).

---

## Optional: land the annotations as a Figma layer (extends design-bridge)

When the deliverable is a Figma annotation layer rather than a markdown spec, reuse `heyhi-design-bridge`'s `use_figma` write path and its Earn-the-Room gate: the human opens/points at the file, approves the spec (Step 3) as the approval surface, and the write is a faithful render of the approved spec, not a free generation. Land the annotations as callouts/redline stickies anchored to the corresponding layers (heading levels, landmark boundaries, the candidate focus-order path, name/role/value badges, target-size flags), with the empty judged slots rendered as visibly-blank labeled callouts. Do not re-implement the write transport; call design-bridge's. This is the class-X extension in practice.

---

## What is explicitly out of scope

- **The judged calls.** Alt-text content and decorative/meaningful decisions, the reading-order intent, and whether a role is correct: empty slots by construction (§ 9). The skill specs the contract; the designer fills the meaning.
- **A conformance verdict.** No pass/fail, no severity grade, no ACR/VPAT, no "this meets AA." That is `heyhi-a11y-audit`, post-build. Annotation is prevention and never claims conformance.
- **Fabricating a name, role, or label** to close a missing-by-construction gap. A gap is a flag, not an invitation to invent.
- **Building the prototype or the design**: `heyhi-ui-ux` / `ui-studio` / `heyhi-design-bridge`. **Interaction-completeness readiness**: `heyhi-prototype-audit`. **The deterministic render-and-verify pass**: `heyhi-prototype-verify`.

---

## Exit Gate Required Headers (bottom-of-skill bracket)

This skill closes through the Exit Gate Flavor A (`CLAUDE-SESSION-RULES.md § Exit Gate`). Before declaring done, confirm every header below carries real content, not a claim:

- `## Fixes Applied`: the Annotation Spec produced (or the Figma annotation layer landed), with the source and input mode named.
- `## Smoke Test`: the Step 4 pre-flight checks, pasted: judged slots empty, provenance labels present, mechanical floor complete, sign-off line unsigned.
- `## Next Session Prompt`: the judged slots the designer still owns (alt text, reading-order intent, role calls) and every missing-by-construction flag still to resolve.

If any alt slot, the reading-order intent slot, the role-calls slot, or the sign-off line is filled by the skill, the gate has **not** been satisfied.

---

*HeyHi Confidential. Sheerline area 8 (Accessibility), P2, class X (extends `heyhi-design-bridge`). v0.1.0 deployed 2026-08-28 (Sheerline Wave G-2), registered in both registries. v0.1.1 (2026-09-12): Step 2.7 gains the full dialog build contract, and Step 2.8's native-substitution flag is generalized from a `<div>`-as-button to the `role=checkbox|radio|switch|button` set, plus a modal-without-dialog-semantics flag; one eval added (a11a-08). From a client-engagement `heyhi-a11y-annotation` finding (a skill-layer fix locked by an eval, erl-SRM; not a registry entry). Spec source: `ai-services/design-intelligence/research/sheerline-skill-buildout-research-2026-08-09.md` § 5.1 (the `heyhi-a11y-annotation` row) + § 9 (boundary + IP posture). Foundation: `sheerline/os/foundations/accessibility/FOUNDATION.md`. Boundary: § 9.*
