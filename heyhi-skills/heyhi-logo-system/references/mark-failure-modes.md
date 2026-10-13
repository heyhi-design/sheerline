---
title: "heyhi-logo-system — Mark Failure-Mode Catalog"
classification: HeyHi Confidential
module: E
loads_in: [Critique]
version: "0.1.0"
created: "2026-06-10"
grounding: ["reference.md (six axes, severity rubric)", "research/visual-language-theory.md (semiotics, Gestalt)", "SKILL.md (Mode 2 Critique, R4 credibility-calibration)"]
---

# Mark Failure-Mode Catalog

**HeyHi Confidential**

*On-demand reference module for `heyhi-logo-system`, loaded in **Critique**. It upgrades the external `ckm:logo-design` skill's two-item troubleshooting into a catalog keyed to the skill's **own six axes** and the seven typologies, so a critique asks "what usually breaks for *this* construction type on *this* axis" instead of relying on memory. It invents no new axis and no new severity tier — every entry maps to one of the six axes in `reference.md` and uses the existing Critical/High/Medium/Low rubric.*

---

## How to use it

During Critique, after scoring an axis, scan that axis's failure list below for the typology in hand. A listed failure that is present is a finding; assign it the rubric severity (adjusting for the engagement's stakes), and carry the refinement direction into the before/after table. The catalog is a checklist for consistency, not a verdict — the six-axis score and the Logo Readiness Profile remain the judgment.

Severity in the **default** column is the typical floor; raise it when the failing surface is the primary one (a Legibility failure at the favicon, the primary digital surface, is Critical, not High).

---

## By axis

### 1. Brand fit — does the mark express *this* brand's point of view?
| Failure | Typology | Default | Refinement direction |
|---|---|---|---|
| **Generic to the category** — expresses the sector, not the brand; a competitor could own it unchanged | any | High | Return to Concept; sharpen the strategic idea (the sentence a competitor could not have written). |
| **Performed, not present** — the mark *performs* a quality (warmth, innovation) rather than embodying it (the performed-vs-present test, `tokenization-boundary.md`) | any | Medium | Trace the quality to a structural choice, not a decorative one. |
| **Aesthetic ↔ typology mismatch** — the construction type fights the intended feel (a gravitas brand on a casual wordmark) | any | Medium | Re-pair typology (Module A) and cluster; state both. |
| **Credibility miscalibration (R4)** — a playful or illustrative style applied to a high-trust, high-consideration category (trade, property, financial, health): the mark reads characterful but not competent | pictorial, dynamic, playful wordmark | **High** in high-trust categories | Weight toward the **emblem** form (Module A); pair the character with proof (a formal badge/seal, a trust line, real photography). Do not let personality stand alone where the stakes are high. *Exception:* in luxury or entertainment, pairing with a literal proof-badge can instead undercut the brand — calibrate to the category. |

### 2. Distinctiveness — could this be mistaken for a competitor?
| Failure | Typology | Default | Refinement direction |
|---|---|---|---|
| **Literal cliché** — the obvious object for the category (a camera for photography); immediately legible, instantly shared (`visual-language-theory.md:58`) | pictorial | High | Move toward abstract or an unexpected angle on the object. |
| **Crowded initials** — three-letter marks collide across industries | lettermark | Medium | Add a distinguishing letterform move, or reconsider typology. |
| **Perceptual flattening** — a fussy abstract mark the eye reduces to "some swoosh" (fails Prägnanz, `visual-language-theory.md:188`) | abstract, dynamic | High | Simplify to one memorable idea; pass the squint test. |
| **Trademark-collision risk** — reads as a near-duplicate of a named competitor's mark | any | **Critical** | Stop; redesign. Confusion and possible legal conflict. |

### 3. Legibility — does it read at the sizes it must work at? (the 16px test)
| Failure | Typology | Default | Refinement direction |
|---|---|---|---|
| **Favicon collapse** — the wordmark turns to a smear below ~24px | wordmark, combination | **Critical** at the primary digital surface | Define the reduced form (Module D); the favicon is not optional. |
| **Emblem mud** — detail-dense emblem unreadable when scaled down | emblem | High | A *separately drawn* simplified small form (Module D), never a scaled emblem. |
| **Vanishing detail** — thin strokes / fine counters disappear at scale or in low contrast | any | Medium | Thicken; reserve detail for sizes that hold it. |
| **Rendered letterform artifacts** — if the mark was rendered, the type is broken or garbled | wordmark, combination | finding, not ship | The render path renders the **symbol only**; set type from the real font (Module C). |

### 4. Scalability — is there a defined reduction path?
| Failure | Typology | Default | Refinement direction |
|---|---|---|---|
| **No reduction path** — specified at one size, shrinks until it breaks | any | High | Author the per-typology path (Module D) into `logo.scale_degradation`. |
| **Emblem with no small form** — inseparable, detail-dense, undefined below the detail floor | emblem | High | Draw the simplified/monochrome small form explicitly (Module D). Until it exists, the Scalability axis scores Not ready (1). |
| **Undefined mark-to-type spacing** — the combination lockup has no stated mark-to-type relationship, so it breaks on mobile and every application reinvents it | combination | Medium | Specify the relationship in design intent; it is non-tokenizable but it must be *stated*. |

### 5. System readiness — will it translate to tokens and components?
| Failure | Typology | Default | Refinement direction |
|---|---|---|---|
| **Mark-to-type left to prose only** — no stated lockup logic | combination | Medium | State the relationship and the clear-space ratio. |
| **No transformation rule** — a dynamic identity with no rule is chaos, not flexibility | dynamic | High | Define the bounded variation set, or change typology. |
| **Missing core variants** — no monochrome or no dark-mode pairing defined | any | Medium | Add `marks.monochrome` and the dark colorway with its contrast result. |
| **Export not component-aligned** — functional but not variant-structured | any | Low | Align export to the component-variant convention. |

### 6. Risk of misinterpretation — what unintended reading does the form carry?
| Failure | Typology | Default | Refinement direction |
|---|---|---|---|
| **Metaphor over-reach** — the form says more, or other, than intended | pictorial, abstract | Medium | Run the connotation audit (`visual-language-theory.md`); name and bound the reading. |
| **Accidental negative-space reveal** — Gestalt closure or figure-ground makes the gaps spell or show something unintended | any | High if the reveal is unfortunate | Re-balance figure-ground; the eye completes forms involuntarily. |
| **Cultural / contextual misread** — color symbolism, gesture, or form carrying a negative reading in a target market | any | High in affected markets | Name the market and the misread; do not hand-wave. |
| **Connotation contradicting the descriptors** — a "warm" direction that reads cold (or the reverse) | any | Medium | Surface the contradiction; align denotation to the intended connotation. |

---

## Typology × axis quick map (where each type most often breaks)

| Typology | Most common failure (axis) |
|---|---|
| Wordmark | Favicon collapse (**Legibility**) |
| Lettermark | Crowded initials (**Distinctiveness**) |
| Pictorial | Literal cliché (**Distinctiveness**) / metaphor over-reach (**Risk**) |
| Abstract | Perceptual flattening (**Distinctiveness**) / meaningless early (**Brand fit**) |
| Combination | Undefined mark-to-type spacing (**Scalability / System readiness**) |
| Emblem | No small form (**Scalability**) / emblem mud (**Legibility**) |
| Dynamic | No transformation rule (**System readiness**) / recognition tax (**Distinctiveness**) |

---

## Comparative use (Select lane)

If the engagement is an N-up comparison, use the **Select lane** (Mode 2, deployed since v0.2.0) and this catalog to score each candidate consistently against the same per-typology failure list, then recommend one. For single-mark Critique the catalog applies exactly as above — this comparative note is additive, not a dependency.

---

*Companion module to `heyhi-logo-system`, loaded in Critique. Cross-references: [`logo-typology.md`](logo-typology.md), [`scale-degradation-matrix.md`](scale-degradation-matrix.md) (the fix-side for Scalability findings), [`render-brief-template.md`](render-brief-template.md). Grounding: `heyhi-skills/heyhi-logo-system/reference.md` (six axes + severity rubric), `ai-services/design-intelligence/research/visual-language-theory.md`.*

*HeyHi Confidential*
