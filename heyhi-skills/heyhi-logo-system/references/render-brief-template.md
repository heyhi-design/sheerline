---
title: "heyhi-logo-system — Render-Brief Template"
classification: HeyHi Confidential
module: C
loads_in: [Concept]
trigger: "operator-invoked render step only — never the default"
version: "0.1.0"
created: "2026-06-10"
grounding: ["SKILL.md:79 (generation boundary)", "reference.md v0.2.0 (Rendering and Verification, NEW-1/NEW-2)", "Concept Direction Record"]
---

# Render-Brief Template

**HeyHi Confidential**

*On-demand reference module for `heyhi-logo-system`. Loads only when the operator has explicitly invoked the opt-in render step in Concept. It is the structured brief that turns a Concept Direction Record into a tool-agnostic generation instruction. It does not change the default behavior of any mode.*

---

## The boundary comes first (restated verbatim, not softened)

> **Generation boundary (instance-owner sign-off, 2026-05-29).** Concept specifies directions in words and structured attributes by default. Rendering candidate marks — image generation or Figma — is an optional step the operator invokes explicitly. It is never the default. Mark direction is HeyHi judgment under the don't-automate-this line; the skill makes the directions legible, it does not auto-produce the marks. When rendering is requested, say so in the output and treat the rendered marks as illustrations of the specified direction, not as the decision.

This module exists *inside* that boundary. It never makes rendering the default, and the marks it helps produce are illustrations of a direction, not a chosen mark. A rendered image is evidence in the conversation, not the decision.

---

## Provider-agnostic by construction (Invariant 1)

The brief describes the *mark*, never the *tool*. It names no generation product and no model. The operator routes the same brief to whatever surface they use — an image-generation model, a vector tool, or Figma — and the brief reads the same. Hardcoding a generator would violate Provider-Agnostic Design and would date the module the moment a tool changes. If a downstream operator needs tool-specific syntax, they adapt the brief at the surface; the brief itself stays neutral.

---

## When there is nothing to generate

Check the typology first (Module A). A **wordmark** or **lettermark** *is* type — there is no symbol to image-generate, and image-generation surfaces cannot draw reliable letterforms anyway. For those typologies, the "render" is **setting the real brand typeface** (NEW-2), not a generation call. This module's template applies to the symbol-bearing typologies: pictorial, abstract, the icon of a combination mark, emblem, and a dynamic system's anchor.

This is also the home of ckm's most useful troubleshooting insight, generalized: **render the symbol only; set the wordmark separately from the real font.** Generation surfaces garble letterforms, so a combination mark is rendered as its symbol, and the wordmark is composed from the brand display token afterward.

---

## The render brief (fields mapped from the Concept Direction Record)

Each field is sourced from the direction's record, so the brief is grounded in the interrogation, not improvised. Fill every line from the record; do not invent attributes the direction did not specify.

| Brief field | Sourced from (Concept Direction Record) | Note |
|---|---|---|
| **Subject + typology** | Symbol direction + the typology from Module A | "an abstract symbol," "a pictorial mark of X." Symbol only — no text. |
| **Form descriptors** | Cluster alignment + moodboard keywords (from `style-descriptor-vocabulary.md`) | Mapped, not invented. The same words the direction already names. |
| **Construction directive** | Typology | "vector, single weight, flat, scalable, geometric construction." |
| **Color** | Color direction | State the role; include the one-color test ("must also read in a single color"). |
| **Background + format** | Standing | "transparent or plain background, no scene, no environment." |
| **Brand negatives** | The do-not-do list / anti-descriptors (from interrogation) | This is where HeyHi's anti-descriptors *become* the negative prompt. |
| **Technical negatives** | Standing hygiene | "no photorealism, no drop shadows, no gradients, no 3D bevel, no fine internal detail that fails at small size." |
| **Variants** | Operator's exploration count | Request several exploratory variants of the *one* direction; this is exploration within a direction, not a spray across directions. |

### The negative prompt, done the HeyHi way

ckm's template carries a single generic negative line. HeyHi's negative has **two** sources, and the first is the differentiator:

1. **Brand negatives** — the anti-descriptors surfaced in interrogation (the do-not-do list). "Never ornate," "never literal," "never corporate-generic." These make the negative prompt specific to *this* brand, which is the whole point of having run the interrogation.
2. **Technical negatives** — the standing hygiene list that keeps output vector-clean: no photorealism, shadows, gradients, bevels, or small-size-fragile detail.

A negative prompt built only from technical hygiene wastes the interrogation. Build it from both.

---

## Worked shape (illustrative, generic)

From a direction whose record reads *Concept name: "Keystone"; typology: abstract; cluster: A (Clean and Structured); moodboard: precise, structural, quiet; color: monochrome-first with a single accent; do-not-do: ornate, literal, playful*:

```
Subject + typology: an abstract symbol, single mark, no text.
Form: precise, structural, quiet; geometric construction; one clear idea
      that survives the squint test.
Construction: vector, flat, single weight, scalable, high contrast.
Color: render in one color first; the accent is added later, not load-bearing.
Background: transparent, no scene.
Brand negatives: not ornate, not literal, not playful.
Technical negatives: no photorealism, no shadows, no gradients, no 3D,
      no fine detail that fails below 32px.
Variants: 6 explorations of this one direction.
```

The wordmark is **not** in the brief; it is set afterward from the brand display font.

---

## Then hand to the render-and-verify loop (do not skip, do not duplicate)

This module produces the brief. The moment a mark is actually rendered, the **render-and-verify loop owns the rest** — render to a viewable image, render the wordmark on the **real brand typeface** (never a stand-in), look at it, judge against your own eyes, iterate, and only then present. The full method is `reference.md` § "Rendering and Verification" (NEW-1 / NEW-2); this module does not restate it. Generating geometry "by spec" and presenting it unseen is the defect the loop exists to prevent.

**Coordination:**
- **NEW-1 / NEW-2** — the loop and the real-typeface rule run after this brief; this module feeds them.
- **R2** — a rendered, verified mark moves the Legibility and Scalability axes from "projected from structure" toward "measured." The brief plus the loop is what makes the mandatory second critique possible.
- **Module A** — typology decides whether this module is even used (a wordmark sets type, it does not generate).

---

*Companion module to `heyhi-logo-system`, loaded only on the opt-in render step in Concept. Cross-references: [`logo-typology.md`](logo-typology.md). Grounding: `heyhi-skills/heyhi-logo-system/SKILL.md` (generation boundary), `reference.md` § "Rendering and Verification."*

*HeyHi Confidential*
