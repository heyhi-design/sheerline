---
classification: confidential
title: "Assistive-technology testing checklist — the Mode B protocol"
skill: heyhi-a11y-audit
loaded_by: "SKILL.md Step 1 / Step 4 (Mode B)"
---

# Assistive-technology (AT) testing checklist

The manual protocol behind Mode B, held as *run-and-record reference*. It is the source of `AT-confirmed` (and much `human-reviewed`) evidence — the half of a conformance audit no scan can reach. This checklist is a **mode of `heyhi-a11y-audit`, not a separate skill.** On-demand: load when running Mode B.

*Internal operational reference (staged under `skill-updates/`): em-dash limit exempt per `OPERATING_PRINCIPLES.md`. The AT-protocol canon and the WebAIM-weighted pairings live in `sheerline/os/foundations/accessibility/FOUNDATION.md` § "The AT-testing protocol"; this file is the operational checklist over that canon.*

---

## The recording rule (so a not-run never reads as a pass)

Every line records exactly one of:

- **`AT-confirmed`** — the check was exercised with assistive technology and passed; note the pairing and what was observed. Writes provenance `AT-confirmed` on the ACR row.
- **defect** — the check was exercised and failed; note what happened and let a human assign severity (severity for a real disabled user is a judgment, per § 9). Writes evidence toward `Does Not Support` / `Partially Supports`, provenance `AT-confirmed`.
- **`not-run`** — not exercised this session. The ACR row stays `NEEDS AT`; it does **not** graduate to a verdict. A `not-run` is a gap in the audit, never a silent pass.

A `human-reviewed` line (code/rendered-output inspection without assistive technology — e.g., reading alt text for meaningfulness) is the other confirmed provenance; note it as such.

## 1. Keyboard traversal

Rendered output required. Unplug the mouse, or commit to not touching it.

- [ ] Every interactive element (links, buttons, form fields, custom widgets, menus, dialogs) is **reachable** by Tab / Shift-Tab.
- [ ] Every reachable element is **operable** by keyboard (Enter/Space activate; arrow keys where the pattern expects them — menus, tabs, radio groups).
- [ ] **Visible focus** at every stop (this is stronger than 2.4.7's "declared" — confirm it is actually visible against the real background, in every state).
- [ ] **Focus order is logical** — it follows reading/meaning order, not DOM accident. (This is the judged half of 2.4.3 the floor cannot reach.)
- [ ] **No keyboard trap** — focus can always move on and out (2.1.2); modals return focus sensibly on close.
- [ ] Focus is **not obscured** by sticky headers/footers or overlays when it lands (2.4.11, new in 2.2).

Feeds: 2.1.1, 2.1.2, 2.4.3, 2.4.7, 2.4.11.

## 2. Screen-reader passes (the WebAIM-survey-weighted pairings)

Rendered output required. Run more than one pairing where feasible — behavior differs across engines. The WebAIM-weighted pairings (foundation canon):

- **JAWS + Chrome** (most common desktop pairing)
- **NVDA + Chrome or Firefox**
- **VoiceOver + Safari** (macOS and iOS)

For each surface, confirm:

- [ ] Every control announces a **correct, meaningful name** (this settles alt-text and label *meaningfulness*, not just presence).
- [ ] Every control announces its **correct role** — and native HTML was preferred over ARIA where it could carry the role (the first rule of ARIA; this is where "whether the ARIA is *right*" is settled, beyond the floor's validity check).
- [ ] **State changes announce** (expanded/collapsed, selected, checked, disabled, error).
- [ ] **Status messages announce** without stealing focus (4.1.3 — live regions actually fire).
- [ ] Headings, landmarks, and lists **navigate correctly** (the structure the floor confirmed *present* is actually usable to move through).
- [ ] Reading order in the accessibility tree matches the visual/intended order.

Feeds: 1.1.1 (meaningfulness), 1.3.1, 2.4.6, 4.1.2, 4.1.3.

## 3. Zoom and reflow

Rendered output + a browser required.

- [ ] **200% text zoom** — content and function survive; nothing is clipped, overlapped, or lost (1.4.4).
- [ ] **400% reflow** — at a 1280px-wide viewport scaled to 400% (≈320 CSS px), content reflows to a single column with **no loss of content or function and no two-dimensional scrolling** of content (1.4.10). (Data tables, and content that inherently needs 2-D, are the named exceptions — judge, do not auto-fail.)
- [ ] Text spacing overrides (line-height, letter/word spacing, paragraph spacing) do not clip content (1.4.12).

Feeds: 1.4.4, 1.4.10, 1.4.12.

## After the pass — write it back

For each line, write the result onto the matching ACR row (`references/acr-vpat-template.md`) with its provenance (`AT-confirmed` / `human-reviewed`) and a one-line observation. Rows you did not exercise stay `NEEDS AT`. Then re-check SKILL.md Step 5 pre-flight: a VPAT verdict may still appear only where provenance is human-reviewed or AT-confirmed, and the overall conformance claim + sign-off line stay blank until the human gate.

*HeyHi Confidential. Reference for `heyhi-a11y-audit` (Mode B). Canon: `sheerline/os/foundations/accessibility/FOUNDATION.md` § "The AT-testing protocol". Spec: `sheerline-skill-buildout-research-2026-08-09.md` § 5.1.*
