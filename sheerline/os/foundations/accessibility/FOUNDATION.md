---
classification: confidential
title: "Foundation: Accessibility (area 8, PARTIAL / elevated / governed practice)"
area: 8
nature: craft
coverage: partial
elevated: true
phase: P2
kind: governance
status: filled
---

# Foundation: Accessibility (area 8)

**Coverage: PARTIAL, elevated to a governed practice. This foundation is now filled (skills-upgrade G-2).** Accessibility is cross-cutting: it runs as a thread through every relevant area, not as a stage in the spine. The elevation's net-new work was the *judged/knowledge layer* — authored here, because unlike Visual and Design Systems, accessibility has no existing HeyHi corpus to reference in place — plus the two skills that consume it. Both are now built and promoted:

- **`heyhi-a11y-audit`** (the anchor): the standalone WCAG-conformance audit that produces an ACR/VPAT-shaped per-criterion report at a stated level, with every judged criterion shipped empty until a human or assistive-technology user confirms it.
- **`heyhi-a11y-annotation`** (the design-side extension): annotates a design or prototype with the accessibility spec for handoff (headings, landmarks, focus order, alt, name/role/value, target size).

Coverage stays **partial**, not covered, on purpose: the mechanical floor is deep, but the area's defining feature is that its judged half — does it actually work for an assistive-technology user — stays human. An automated pass is never a conformance claim.

## The mechanical floor already exists (do not re-stub it as absent)

The deterministic accessibility floor is **deep and enforced today**, inside Sheerline's own machinery:

- the `heyhi-mcp` validator's accessibility rules (Rules 2 and 5),
- the `health-check` C4 checks,
- the DS-MCP conformance lane, and the eval harness's dimension 3,
- the corrections registry's `category: accessibility` taxonomy (a seeded slot: `contrast-pairing-not-declared-safe` ships as the one filled example, carrying synthetic `times_fired` demo data — the taxonomy is wired and ready, but has not yet fired on a real field run).

`heyhi-a11y-audit` **consumes this floor generically; it re-implements no contrast math.** It reads the deterministic results (the conformance lane, the validator rules, the contrast checker) as the automated tier and layers the judged tier on top. It does not hard-depend on any single unpromoted skill.

## The A.1 accessibility gate (the safety-critical contracts fold in)

The ratified A.1 (Increment A, Decision 1) folds the safety-critical usability contracts into the accessibility gate: visible focus, minimum target size, a distinct state per control (the A.3 control-state contract), and machine-readable feedback now live *inside* the hard gate, not beside it. So the gate spans those contracts, not contrast alone. The gate itself is stated once in [`os/operating-principles.md`](../../operating-principles.md); this foundation points at it and does not restate it.

## The judged layer (what the audit adds on top of the floor)

The tracked shortfall the mechanical floor cannot reach is the **judged half**: does it actually work for an assistive-technology user? Alt-text meaningfulness, focus-order logic, whether the ARIA is right, severity for real disabled users, the conformance verdict. That is `heyhi-a11y-audit`'s job, and by construction every judged criterion ships empty (`NEEDS HUMAN / AT CONFIRMATION`), every row carries a provenance label (`automated` / `human-reviewed` / `AT-confirmed`) so a never-confirmed row cannot roll into a claim, and the conformance sign-off is a named human gate.

## The knowledge canon (authored here — the judged layer's reference)

| Topic | The canon |
|---|---|
| **WCAG 2.2 on POUR** | The four principles (Perceivable, Operable, Understandable, Robust). The nine criteria new in 2.2 are the audit's freshest surface: Target Size (Minimum) 24×24, Focus Not Obscured (Minimum + Enhanced), Focus Appearance, Dragging Movements, Consistent Help, Redundant Entry, and Accessible Authentication (Minimum + Enhanced). Success Criterion 4.1.1 (Parsing) was removed in 2.2 — do not audit against it. |
| **The AA legal-version fork** | Audit *to* 2.2 AA (the current, strictest baseline), but map conformance *claims* to the version the jurisdiction names — some legal regimes still cite 2.1 AA (or 2.0). Audit to the newer standard; claim to the named one. Never assert a version the law does not require. |
| **ARIA APG + the first rule of ARIA** | Prefer native HTML semantics; no ARIA is better than bad ARIA. Use the ARIA Authoring Practices Guide patterns only where native elements cannot carry the role/state, and verify name/role/value. |
| **The AT-testing protocol** (a *mode* of the audit, not a separate skill) | Keyboard traversal (every interactive element reachable and operable, visible focus, logical order, no traps); screen-reader passes on the WebAIM-survey-weighted pairings (JAWS + Chrome, NVDA + Chrome/Firefox, VoiceOver + Safari on macOS/iOS); 200% zoom and 400% reflow without loss of content or function. |
| **The automated-coverage ceiling (state it honestly)** | Automated tools catch roughly 30–40% of WCAG issues *by criteria type*, but a higher share *by instance count* (Deque reports ~57% of issue instances). Flag both framings; under either, the judged remainder is large. Never position the audit as "we run axe" — the mechanical floor is commoditized (axe/Lighthouse are free). Position on the judged half, the governed ACR/VPAT artifact, and AT confirmation. |
| **Legal context** | The EAA has been in force since 28 June 2025 (extraterritorial, active penalties — the sharpest near-term pull). ADA Title II deadlines slipped roughly a year under an April-2026 rule (now 2027/2028) — **retire any "2026 ADA deadline" framing; treat it as a pipeline builder, not an emergency.** The durable, calendar-independent pull is the model-generated-UI-inaccessible-by-default deficit, which ties accessibility directly to Sheerline's generation-governance thesis. (Legal-timeline facts of record: `ai-services/design-intelligence/research/sheerline-skill-buildout-research-2026-08-09.md` § 5.1.) |
| **WCAG 3.0 (watch-item)** | Still a Working Draft; final not expected before 2028. Anchor on 2.2 AA; treat 3.0 as a horizon-scan item, not a target. |

## Registered skills (area 8)

| Skill | Class | What it does | Judgment that stays human |
|---|---|---|---|
| `heyhi-a11y-audit` | anchor | The WCAG-conformance audit → an ACR/VPAT per-criterion report at a stated level; consumes the deterministic floor, adds the judged tier | Does it work for an AT user; alt-text meaningfulness; focus-order logic; is the ARIA right; severity for real disabled users; the conformance verdict |
| `heyhi-a11y-annotation` | extension | Design-side prevention: annotate a design/prototype with the accessibility spec for handoff | Which alt text is correct; reading-order intent; role calls |

Both register here. The AT-testing protocol is a *mode* of the audit, not a separate skill; the enforcement floor already exists (above).

---

*Area map: `os/foundations/registry.yaml` · The accessibility gate (A.1): `os/operating-principles.md` · Legal-timeline + coverage-ceiling facts: `ai-services/design-intelligence/research/sheerline-skill-buildout-research-2026-08-09.md` § 5.1*

*HeyHi Confidential*
