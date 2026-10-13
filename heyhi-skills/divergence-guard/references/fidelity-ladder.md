---
classification: confidential
title: "Fidelity ladder — what 'right-sized to the test question' means"
skill: divergence-guard
loaded_by: "SKILL.md Step 1"
---

# Fidelity ladder

The comparison basis for the guard's **warn** verb, so the fidelity flag is a comparison and not a vibe. Craft canon adopted 2026-09-05 (spec § 10 D8): the **structure** (question class → sufficient rung) is the adopted recommendation; **the specific rows come from design practice, not from a cited source**, and are a starting point. The ladder describes *sufficiency*; it never prescribes a stop, and it is never a threshold anything can gate on.

*Internal operational reference: em-dash limit exempt per `OPERATING_PRINCIPLES.md`.*

---

## 1. The ladder

The **question class** is the input; the **sufficient fidelity** is the rung the guard compares the artifact against.

| Test-question class | Sufficient fidelity |
|---|---|
| Is the flow right? Are the steps / screens complete? Is the decomposition how the work is done? | **Lo-fi** — inventory + flow map + skeleton |
| Can people find X? Do the labels and hierarchy carry scent? | **Lo-fi with real (provisional) labels** — still no visual language |
| Does the interaction model hold? (states, transitions, error paths, keyboard) | **Mid** — skeleton + state placeholders, or a coded prototype scoped to the one interaction |
| Does it feel like the brand? Is the visual direction right? | **Hi-fi visual** — `ui-studio` Mode B / the Identity Proposal |
| Is it buildable to the system? (tokens, WCAG, responsive) | **Hi-fi coded** — `ui-studio` Mode A + `heyhi-prototype-audit` + `heyhi-prototype-verify` |
| "Convince the stakeholders" | Not a test question. The guard names this plainly and hands it back; what fidelity a room needs is the human's read. |

## 2. Reading an artifact's fidelity

The guard classifies the artifact as lo-fi · mid · hi-fi visual · hi-fi coded from what it can see (a Lo-fi Pack; a skeleton with state placeholders; comps carrying color, type, imagery; running code bound to tokens). The classification is always tagged `[inferred]`. Where the artifact sits above the rung the question needs, the guard says so in prose and names the cost: time spent on polish that the question does not need, the team's attachment to a rendered thing, reviewers reacting to color instead of structure. Where it sits below, it says that too. Where no question was stated, it says that fidelity cannot be right-sized to an unstated question, and still counts the options.

## 3. The divergence axes (pointed at, never copied)

The guard's **measure** verb compares options on the six divergence axes (navigation model · task decomposition · information hierarchy · entry point · disclosure strategy · input model). They are authored **once**, in `flow-and-lofi-author`'s `references/lofi-method.md` § 2 (at staging: `skill-updates/flow-and-lofi-author/references/lofi-method.md`), per the author-once rule; this file carries no second copy. Two options sharing every axis are one option rearranged; hi-fi variants of one structure (three color treatments of one flow) are one structural option, and the guard says so.

## 4. Why nothing here is a threshold

The ladder maps a question to a *sufficient* rung. It does not say "stop at lo-fi," and it does not produce a number. The Divergence Read renders the comparison as one or two prose sentences on purpose: an enumerated fidelity value next to an enumerated rung is exactly what a future hook would diff, and the guard's whole construction (spec § 3.5) is that nothing inside it can be gated on. The one enumerated value the Read carries is `Count:`, because the count *is* the finding; N is echoed beside it as context and never compared as a threshold.

---

*HeyHi Confidential. Reference for `divergence-guard`. Spec source: `plans/plan-sheerline-p3-prototyping-lofi-2026-09-05.md` § 3.3–§ 3.5, § 6.2. Canon adopted 2026-09-05 (§ 10 D8): structure recommended, values from design practice.*
