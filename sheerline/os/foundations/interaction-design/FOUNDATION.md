---
classification: confidential
title: "Foundation: Interaction Design (area 4, PARTIAL / filled / governed practice)"
area: 4
nature: craft
coverage: partial
phase: P3
kind: governance
status: filled
---

# Foundation: Interaction Design (area 4)

**Coverage: PARTIAL, governed — the foundation was authored at the P3 fill (`foundation: deferred → governance`, a new folder rather than a stub elevation) behind one already-deployed skill, `motion-system-author` (the motion facet, Wave G-4). The area moves `partial → covered` when `interaction-inventory` promotes, which closes the non-motion interaction gap the buildout research named.** Interaction Design sits at the `(Interaction ‖ Content)` slot of the dependency spine (User Research → Information Architecture → (Interaction ‖ Content) → Visual → Design Systems): it specifies **behavior** — what states an element has, what moves it between them, what the user sees and a machine can read at each, and how a keyboard or a finger drives it — after structure is settled and before visual treatment is applied. The automatable core here (enumerating states) is not hard and is not the value. The governed value is that the enumeration runs **against a ratified, served contract** (A.3) and hands the human the calls that are genuinely theirs: which interactions matter, whether a flagged absence is deliberate, and whether the behavior is right. No variant matrix or component library does that.

This foundation inherits a pointer, not a blank. The control-state contract was ratified as Increment A of the DESIGN.md arc (A.3) and is served today as the second always-loaded Design System MCP surface (`design-system://fundamentals`). The foundation **points at it and authors only what sits around it**: which states apply to which element class, how states connect, what a missing state looks like. A fill that re-authored the state list would create the second canonical hierarchy the ratification exists to end.

## What already exists (do not re-stub as absent)

Area 4 is a gap in the *upstream structural spec*, not in all interaction capability. The foundation **references these in place, copying nothing**:

| Surface | What it already covers | Why it is not the gap |
|---|---|---|
| **A.3, the control-state contract** ([`ai-services/design-intelligence/design-fundamentals.md`](../../../../ai-services/design-intelligence/design-fundamentals.md) § A.3; served as `design-system://fundamentals`) | The canonical state set and each state's visual change, trigger, and accessibility hook | It is the *contract*; the area lacked the *inventory* against it |
| `motion-system-author` (deployed, area 4) | How each state transition *moves*: springs, the duration + easing fallback, stagger, the mandatory `prefers-reduced-motion` variant, the DTCG motion-gap note; component motion specs keyed to the A.3 set | Names the motion of a transition; does not enumerate which transitions exist |
| `ux-guidelines.csv` rows 28–35 (Interaction) and 26–27 (Touch), in `heyhi-skills/ui-studio/data/` and `heyhi-skills/heyhi-ui-ux/data/` | The build-time checklist (focus, hover, active, disabled, loading, error, success, confirmation; pull-to-refresh, haptics) | A per-build checklist, one of the three sources A.3 reconciled; not a per-element inventory |
| The `heyhi-mcp` validator (Rule 3 touch target ≥ 44 px; Rule 5 a focus slot on every interactive component) | The deterministic floor, enforced at validation | Checks a built component's manifest; cannot say which states a *design* is silent on |
| `heyhi-prototype-audit` (area 5) | Interaction completeness of a **built** prototype: the severity matrix and the phased build plan | Downstream: finds the missing state after the build; the inventory specs it before |
| `heyhi-a11y-annotation` (area 8) | Name / role / value, the APG keyboard-interaction spec per widget, the candidate focus / reading order | The *accessibility* contract for the same elements; the inventory consumes its APG map for the keyboard column and re-emits none of it |
| `heyhi-figma-ds-generator` (area 7) | Writes variant sets into Figma (the self-engagement proof: a 27-variant Button, Style × Size × State) | Consumes a state axis; does not decide it |
| `voice-system-author` + `microcopy-states-writer` (area 3, both deployed) | The UX-writing taxonomy (eight core slots plus two extended) and the states-copy doctrine; the per-state strings against a confirmed voice | The *copy* half of the states seam; the inventory names the slot, `microcopy-states-writer` fills it |

## Points at the invariant, does not restate it

The always-loaded behavioral guardrails that govern this area are authored **once** in [`os/operating-principles.md`](../../operating-principles.md); this foundation cites them by path and re-derives none:

- **What stays human** and **the taste-and-critique boundary** (`operating-principles.md` § Design Constraints): scoring is advisory, never a gate; "a capability that fills its own judgment slot has exceeded its charter." A `MISSING` state is a finding for a human, never a merge block.
- **The accessibility gate** (`operating-principles.md` § The cross-quality conflict-resolution order → A.1 rule 1): the safety-critical usability contracts — visible focus, minimum target size, **a distinct state for each interactive control**, machine-readable feedback — live *inside* the hard gate. The inventory is the artifact that makes the third of those checkable before the build; it does not re-author the gate.
- **The severity axis** (the same section): Accessibility → **Interaction** → Visual → Brand → Code. An interaction failure outranks a visual or brand one when a defect is graded. This foundation points at that order; the evaluator grades on it.
- **Structured-over-prose** (`operating-principles.md` § Structured-Over-Prose on Propagation Surfaces): the inventory is a surface other skills read, so it ships as a table plus a machine-readable sidecar, never as prose alone.
- **The ideation-diversity guard** (`operating-principles.md` § The zero-cost operating invariants): where the inventory offers alternative interaction patterns for an element, they are stimulus, never selection.
- **The empathy boundary** (same section), cited for completeness: a gesture or feedback choice that leans on assumed user experience carries simulated, not lived, empathy, and is labeled as such.

## The judged layer (what stays human)

The tracked shortfall the mechanical layer cannot reach. Every area-4 skill ships these as empty slots behind a named gate:

- **which interactions matter** (buildout research § 4.2: *"Human: which interactions matter"*): of the full enumeration, which elements and transitions deserve design attention on this screen;
- **the interaction verdict**: does the behavior serve the task; does it feel right — judged in motion, by a human who has seen it run (the rule `motion-system-author` already carries);
- **deliberate-absence rulings**: the inventory flags an applicable state the source does not show as `MISSING`; only a human may rule it *deliberately absent* (a synchronous control with no loading state; a read-only view with no error state). The flag stays a flag until ruled;
- **pattern choice where conventions compete**: a *stated* brand departure from a convention (A.2 Jakob's Law) is honored under A.1 rule 2 (specified beats silent) and is not a defect; an *unstated* novelty is a fundamentals miss under rule 3, and only a collision with a stated brand rule inside the gate resolves to brand-and-flag under rule 4. The inventory records which case it is; the human rules on it;
- **the gesture vocabulary** on touch (what a swipe *means* on this surface) and **the motion personality** (already `motion-system-author`'s slot; the inventory never fills it).

## The knowledge canon (authored here — the skills' reference)

The craft this foundation genuinely authors, the analogue of the accessibility WCAG canon and the User Research Faulkner standard. Each row either points at a ratified source or authors the inventory discipline *around* it. The full applicability matrix, the transition rules, and the flag taxonomy live in the deployed skill's method reference (`heyhi-skills/interaction-inventory/references/state-applicability-canon.md`); this table is the canon at foundation depth.

| Topic | The canon (authored here, or pointed at) |
|---|---|
| **The control-state contract** | **Pointed at, not authored:** A.3 in `design-fundamentals.md` (default / hover / focus-visible / active / disabled / loading / error, plus success and selected where the control's function calls for them); reasoning of record `ai-services/design-intelligence/research/design-fundamentals-decision-research-2026-08-12.md` (the three-source divergence it resolved). The foundation adds one rule: **a control that omits an applicable state is incomplete even when it validates** (the A.5 / G1B finding: a Button with four states passes the token validator at confidence 1.0), and the inventory is where "applicable" is decided. |
| **The data-view state set** | **Pointed at:** A.2's assumed floor names it (every data view ships empty / loading / error / populated). Authored here, the **applicability rule**: a view bound to async data carries all four; a static view carries populated only, and the other three are `n/a` by class, never silently omitted. |
| **Element-class applicability** *(authored)* | The matrix the inventory enumerates against. Classes: **action** (button, icon button), **link**, **text input**, **selection control** (checkbox / radio / switch), **composite** (tabs, menu, combobox, dialog, disclosure — the APG set), **data view** (list, table, card grid), **static** (no states; a `readonly` flag only). A *link* carries default / hover / focus-visible / active and not loading or error; a *text input* carries error and never hover-only signaling; a *composite* carries selected / expanded per its APG pattern; an *action* bound to an async operation carries loading with both exits. The full matrix, labeled `authored`, is the method reference § 2. |
| **Transition rules** *(authored)* | Every non-default state has a **named entry trigger** and an **exit path**. **loading** requires an async trigger and both a success exit and an error exit (A.2 law 8). **error** requires an inline recovery path, never a dead end (A.2 law 9; area 3's "an error with no next step is a dead end" is the copy-side twin). **disabled** is communicated programmatically (`disabled` / `aria-disabled`) and is out of scope for contrast (A.3); a disabled control whose *reason* is shown nowhere is flagged as a design question, not a contract failure. **hover** is never the sole signal (A.3; touch has no hover). **selected** contrasts against the component's own surface (A.3; the `ds-active-ring-invisible-on-component-bg` correction is the recorded failure). An **unreachable state** and a **dead-end state** are flags, never silent omissions. |
| **The microinteraction structural model** *(authored)* | Microinteractions are **structural, not decorative** (buildout research § 4.2: they clarify hierarchy and preserve continuity). Per element the inventory reads **trigger → rules → feedback → loops and modes**, the standard microinteraction anatomy, named without re-deriving it. Feedback is a state change the user can perceive *and* a machine can read (A.3's accessibility-hook column), never one without the other. |
| **Timing** | **Pointed at:** the Doherty threshold (~400 ms) and visibility of system status (A.2 law 8): a loading affordance appears immediately past the threshold; a terminal state is always shown. This foundation adds no numbers of its own. |
| **Focus and keyboard** | **Pointed at, consumed in place:** [`heyhi-skills/heyhi-a11y-annotation/references/apg-pattern-map.md`](../../../../heyhi-skills/heyhi-a11y-annotation/references/apg-pattern-map.md) (the required keyboard interaction per ARIA APG pattern, native element first). The inventory's keyboard column is filled from that map by pattern; the foundation does not copy the map. Visible focus on every focusable is A.1 rule 1 (the gate), cited. |
| **Gesture floor** *(authored, thin)* | Touch: tap / long-press / swipe / drag / pinch, each a *trigger* in the model above. The **44 × 44 px floor** across every state (validator Rule 3; A.3) is HeyHi's served floor; WCAG 2.2 SC 2.5.8's legal minimum is 24 × 24, which `heyhi-a11y-annotation` flags at, so the inventory flags at 44 and labels it as the served floor rather than a conformance claim. No hover on touch. The `ux-guidelines.csv` Touch rows (26 pull-to-refresh, 27 haptics) are cited by row. What a gesture *means* on a given surface is the human's (§ The judged layer). |
| **The states seam** | The inventory emits, for every copy-bearing state row (loading / error / success / a data view's empty; the other states carry `no copy`), an **empty copy slot** keyed to the UX-writing taxonomy in [`heyhi-skills/voice-system-author/references/voice-system-template.md`](../../../../heyhi-skills/voice-system-author/references/voice-system-template.md) Part 3 (eight core slots plus two extended). Area 3's `microcopy-states-writer` fills the string; area 4 never writes it. The contract of record for the seam's structure is the area-4 spec § 3.5 / § 4; the area-3 spec owns the copy-side terms. |
| **Motion** | **Pointed at, a deliberate deviation from the research:** buildout research § 4.2 wrote the motion-token model, the DTCG standards-gap note, `prefers-reduced-motion`, and the Figma Motion / Rive substrate into the *foundation's* content list. That research predates `motion-system-author`, which now authors all four in its SKILL.md and `references/motion-token-schema.md`. Re-authoring them here would create the second center the reference-not-restate rule forbids, so this foundation points at the deployed skill. The inventory names the transition; it emits no spring, duration, or easing. |

## Registered skills (area 4)

| Skill | Class | State / gate tier | Judgment that stays human |
|---|---|---|---|
| `motion-system-author` | G+X (built net-new from the § 4.2 spec, Wave G-4) | **deployed** (v0.1.0); registered in both registries; its SKILL.md "Foundation note" is re-pointed at this manifest by the convergence pass (staged edit in `skill-updates/motion-system-author/`) | the motion personality; the restraint call; "does it feel right" |
| `interaction-inventory` | N | Tier 1 — buildable now, proved first on the instance's own practice; **deployed** at `heyhi-skills/interaction-inventory/`; the area flipped `partial → covered` on that promotion (spec § 9 D2) | which interactions matter; the interaction verdict; deliberate-absence rulings |

`heyhi-prototype-audit` stays registered under area 5 (it is the completeness audit of a built prototype, the consumer of this area's spec); this table cross-links it and does not claim it.

---

*Area map: [`os/foundations/registry.yaml`](../registry.yaml) · Always-loaded invariants: [`os/operating-principles.md`](../../operating-principles.md) · The control-state contract (A.3): `ai-services/design-intelligence/design-fundamentals.md` + `research/design-fundamentals-decision-research-2026-08-12.md` · Spec source: [`plans/plan-sheerline-p3-interaction-design-2026-09-04.md`](../../../../plans/plan-sheerline-p3-interaction-design-2026-09-04.md) · Research of record: `ai-services/design-intelligence/research/sheerline-skill-buildout-research-2026-08-09.md` § 4.2 / § 7b*

*HeyHi Confidential*
