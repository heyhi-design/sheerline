---
classification: confidential
title: "Foundation: Visual Design (area 6, DEEP)"
area: 6
nature: craft
coverage: deep
phase: P1
kind: deep-manifest
---

# Foundation: Visual Design (area 6)

**Coverage: DEEP. This is a governance manifest, not new capability.** Visual Design is one of the two areas the whole Sheerline concept is proof of. Phase 1 brings it under governance: register its skills, seed corrections generic-factual, and point this foundation at HeyHi's existing corpus in place. It authors **zero net-new skills** and **copies nothing**.

*Paths below are repo-root-relative. This manifest is a pointer plus loading rules. It never byte-copies the corpus into `sheerline/` (the byte-identical-copy trap: a duplicated corpus that silently drifts from its source is out of scope by construction).*

---

## What this foundation references (in place, never copied)

| Corpus reference | What it supplies |
|---|---|
| `ai-services/design-intelligence/style-reference-library.md` | The curated style library: the taste corpus behind direction selection. |
| `ai-services/design-intelligence/style-descriptor-vocabulary.md` | The descriptor vocabulary: how a visual direction is named and matched. |
| `ai-services/design-intelligence/research/visual-language-anatomy.md` | The anatomy layer: the structural vocabulary of a visual language. |
| `ai-services/design-intelligence/visual-anti-tells.md` | The anti-tells: what makes generated visual output read as generated. |
| `ai-services/design-intelligence/taste-evaluation-research.md` | The taste-thread: how taste is evaluated and projected, not generated. |
| `ai-services/design-intelligence/research/tokenization-boundary.md` | The non-tokenizable layer: where taste stops being a token and starts being a judgment. |

**Registered skills (area 6):** `heyhi-logo-system`, `heyhi-style-brief`, `heyhi-style-selection`, `heyhi-style-entry-author`, `design-system-onboard` (moodboard to config). These are the foundation; no skill is missing. Watch-items (not gaps): the never-promoted designer-position drafts and the `heyhi-illustration` / `heyhi-visual-exploration` candidates are visual-adjacent *extensions*, folded in as candidates, not treated as under-coverage.

---

## The fundamentals reasoning layer (referenced, not authored here)

Alongside the taste and token corpus, this foundation references the layer above it: the universal UI/UX principles stated as build constraints, plus the cross-quality conflict order. That layer is authored **once**, as **Increment A of the DESIGN.md arc**, ratified. Point at it; do not re-author it here (the reference-not-copy rule applies to the reasoning layer exactly as to the style library).

| Reasoning reference | What it supplies | State |
|---|---|---|
| `plans/plan-design-md-build-2026-08-06.md` § Increment A | The ratified spec: A.1 (the conflict hierarchy, Option A), A.2 (the binding UX law set), A.3 (the control-state contract). | Ratified, landed. |
| `ai-services/design-intelligence/research/design-fundamentals-decision-research-2026-08-12.md` | The reasoning of record: the exact ratified wording for A.1 / A.2 / A.3 and why. | Ratified, landed. |
| `ai-services/design-intelligence/design-fundamentals.md` | The served reference: A.1 the conflict hierarchy, A.2 the Tier-1 ten as build constraints, A.3 the control-state contract, A.4 the rest by reference. | Authored, landed. |

The **served `design-fundamentals` reference file** (`ai-services/design-intelligence/design-fundamentals.md`) is authored and landed; serving it as the second always-loaded surface after the design system is the remaining step (A.5, gate G1B). It, together with the two ratified decision documents above, is the statement of record this foundation points at. The conflict order itself lives in `os/operating-principles.md`, which points at A.1; this foundation does not restate it.

### The Gestalt / Von Restorff bridge (one HeyHi source, two registers)

A.2 promotes the **Gestalt grouping laws** and the **Von Restorff (isolation) effect** into the binding constraint set. These are **not a cold import**. They *re-register* from HeyHi's own visual-language corpus, where they already live filed as brand-perception theory:

| Constraint (A.2) | HeyHi source (brand-perception register) |
|---|---|
| Gestalt grouping | `ai-services/design-intelligence/research/visual-language-theory.md`, `ai-services/design-intelligence/research/visual-language-reference.md` |
| Von Restorff / isolation | `ai-services/design-intelligence/research/visual-language-functions.md` |

The buildout research's § 2.1 corpus list names `visual-language-anatomy.md`, which carries **no** Gestalt material, so this manifest wires to the Gestalt-bearing siblings above as well. Present them as **one HeyHi source in two registers** (brand-perception theory in the corpus; build-constraint via Increment A A.2), not as two separate sources.

---

## Loading rules (Earn the Room, four-class)

- **always:** nothing from this foundation loads by default. Area 6 is the active-area foundation, loaded *conditionally* when a session's task is visual-direction work.
- **conditional:** this manifest, when the session is direction selection, logo/mark work, style-brief authoring, or a visual build that needs the taste corpus.
- **on-demand:** a specific corpus file (a style-library entry, an anti-tell, a Gestalt reference) when the task explicitly calls for it.
- **searchable:** the design system's own token and component data, retrieved through the MCP, never pasted.

---

## The boundary

Direction selection, art direction, and "which deviation matters" stay human. Visual is the area where advisory-never-gate is most load-bearing: infrastructure holds taste, it does not generate it. Start from a visual reference target, not from tokens (the token-driven-taste-gap correction). A grade informs the human read; it never selects the direction.

---

*Area map: `os/foundations/registry.yaml` · Conflict order: `os/operating-principles.md` · Corrections: `os/corrections/`*

*HeyHi Confidential*
