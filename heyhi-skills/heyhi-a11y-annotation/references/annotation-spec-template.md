---
title: "Reference: the accessibility annotation-spec template"
classification: confidential
skill: heyhi-a11y-annotation
status: staged
---

# Annotation-spec template

**HeyHi Confidential.** This is the exact output structure `heyhi-a11y-annotation` produces. Copy the structure into a real spec; **never copy the example rows** below into a client deliverable, they exist only to show the shape and the provenance labels. Every judged slot is pre-marked empty by construction (§ 9). The example content is invented, no client material.

**Provenance labels** (Step 3) sit in a `prov` column on every scaffolded row:

- `[scaffold: from structure]` — derived mechanically from the source (a heading level, a landmark region, a measured box).
- `[candidate: needs confirmation]` — a role call or an order the skill proposes for the human to confirm.
- `[inferred]` — read from a silent source (a Figma design has no DOM, so a landmark or level read from layer naming is inferred).

---

## The template

```
# Accessibility Annotation Spec — [design / prototype name]
Source: [path or Figma file]     Input mode: [prototype | design]     Annotated: [date]
Target: WCAG 2.2 AA (audit-to standard).  Claim standard is the audit's job, not this spec's.

## 1. Heading outline
| Level | Text (from source) | prov | Flag |
|-------|--------------------|------|------|
| h1    | "Page title"       | [scaffold: from structure] | — |
| h2    | "Section A"        | [scaffold: from structure] | — |
| h4    | "Subsection"       | [scaffold: from structure] | SKIPPED-LEVEL (h2 → h4; designer picks the real level) |
Flags: [no h1 | multiple h1 | skipped level | heading used for styling only]

## 2. Landmark map
| Region | Landmark role | Native element to prefer | prov | Flag |
|--------|---------------|--------------------------|------|------|
| top bar   | banner       | <header>  | [scaffold: from structure] | — |
| main nav  | navigation   | <nav>     | [scaffold: from structure] | — |
| body      | main (×1)    | <main>    | [scaffold: from structure] | — |
| side rail | complementary| <aside>   | [inferred] (Figma: read from layer name) | — |
| footer    | contentinfo  | <footer>  | [scaffold: from structure] | — |
Flags: [content in no landmark | more than one main | landmark via ARIA where native exists]

## 3. Reading / focus order (CANDIDATE — source order, not intent)
Emitted order (interactive + landmark stops), labeled candidate:
1. [skip link]            [candidate: needs confirmation]
2. nav: link, link, link  [candidate: needs confirmation]
3. main: h1, CTA button   [candidate: needs confirmation]
...
Divergence flags: [visual order ≠ DOM order at: <where>]
> The INTENDED reading/focus order is a judged slot. See ⛔ below. This list is source order only.

## 4. Name / role / value (WCAG 4.1.2)
| Element | Role (candidate) | Accessible name | Value / state to expose | prov |
|---------|------------------|-----------------|-------------------------|------|
| primary CTA | button        | ____________ (EMPTY) | — | [candidate: needs confirmation] |
| menu toggle | button        | ____________ (EMPTY) | expanded (true/false) | [candidate: needs confirmation] |
| "Remember me" | checkbox    | ____________ (EMPTY) | checked (true/false)  | [candidate: needs confirmation] |
| plan tab set | tab / tablist| ____________ (EMPTY) | selected; aria-controls | [candidate: needs confirmation] |
> The role is a candidate. The accessible NAME is a judged slot (see ⛔). The state spec is mechanical.

## 5. Alt text (every image / icon / meaningful media)
| Image | Decorative or meaningful? | Alt text | prov |
|-------|---------------------------|----------|------|
| hero photo    | ____________ (EMPTY) | ____________ (EMPTY) | [scaffold: from structure] |
| logo          | ____________ (EMPTY) | ____________ (EMPTY) | [scaffold: from structure] |
| icon-in-button| name lives on the control (row 4) | (cross-linked) | [scaffold: from structure] |
> Both columns are judged slots (see ⛔). The skill lists every image; it writes no alt text.

## 6. Target size (WCAG 2.2 SC 2.5.8 — 24×24 CSS px minimum)
| Target | Measured box | Meets 24×24? | prov | Flag |
|--------|--------------|--------------|------|------|
| close (×) icon | 18×18 px | NO  | [scaffold: from structure] | BELOW MINIMUM — enlarge before handoff |
| primary CTA    | 44×48 px | YES | [scaffold: from structure] | — |
Spacing flag: [close-packed targets under the exception threshold at: <where>]
> AAA aspiration (SC 2.5.5, 44×44) noted only where the engagement profile asks for it.

## 7. APG pattern specs (per composite widget)
### [widget name] → [APG pattern]  (role call is a candidate — see ⛔)
- Prefer native: [native element, or "no native equivalent — ARIA pattern required"]
- Required name/role/value: [from apg-pattern-map.md]
- Required keyboard interaction: [from apg-pattern-map.md]
- prov: [candidate: needs confirmation]

## 8. Missing-by-construction flags
- [ ] <element>: no accessible-name source (icon-only, no text/aria-label/labelled child) — designer supplies a name path.
- [ ] <control>: no associated label — designer supplies a label.
- [ ] <div-as-button>: non-native element carrying an interactive role — prefer a native <button>/<a>.
- [ ] <widget>: exposes no state it needs (<which state>).
> Each is a flag for the designer to resolve. The skill invents no name, role, or label to close it.

## ⛔ Alt text: NEEDS DESIGNER
Per image (section 5): decorative or meaningful? If meaningful, the words.
Intentionally empty. The skill lists every image and its slot; it writes no alt text.

## ⛔ Reading-order intent: NEEDS DESIGNER
The candidate order (section 3) is source order, labeled. The INTENDED reading/focus
order is a design decision. Intentionally empty.

## ⛔ Role calls: NEEDS DESIGNER
Each widget (sections 4, 7) carries a candidate role + its APG spec. Whether the role
is correct (and whether native HTML should replace the ARIA) is confirmed here.
Intentionally empty.

## Named gate (annotation sign-off)
Sign-off owner (the designer): ____________________     Date: ______
No accessibility annotation is handed to engineering until this line is signed by a human.
The sign-off attests: alt-text decisions made, reading-order intent set, role calls confirmed,
every missing-by-construction flag resolved.
```

---

## How the template maps to the SKILL.md steps

| Template section | Built in Step 2 by | Judged slot? |
|------------------|--------------------|--------------|
| 1. Heading outline | outline + skipped-level flags | no (level fix is the designer's, flagged) |
| 2. Landmark map | region → landmark, native-first | no |
| 3. Reading / focus order | source-order candidate + divergence flags | **intent is ⛔** |
| 4. Name / role / value | role candidate + state spec + empty name | **name is ⛔; role is candidate** |
| 5. Alt text | one row per image, two empty columns | **both columns ⛔** |
| 6. Target size | measured box vs 24×24 | no (mechanical flag) |
| 7. APG pattern specs | pattern spec per widget (apg-pattern-map.md) | **role call is ⛔** |
| 8. Missing-by-construction | structural gaps flagged, not filled | no (flags only) |

The mechanical floor (sections 1, 2, 6, the role/state and APG specs, the flags) is what makes the accessibility contract legible to engineering. The three ⛔ slots and the sign-off are what keep the design truth with the designer.

---

*HeyHi Confidential. Reference for `heyhi-a11y-annotation` (staged, `skill-updates/`). Example rows are invented; no client content. WCAG criteria per `sheerline/os/foundations/accessibility/FOUNDATION.md`.*
