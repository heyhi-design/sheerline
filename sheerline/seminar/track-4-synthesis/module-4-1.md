---
classification: confidential
title: "Module 4.1 — The boundary and the retained moat"
track: 4
module: "4.1"
level: expert
prereqs: ["3.4"]
est_minutes: 30
teaches: sheerline
opens_files:
  - sheerline/os/operating-principles.md
  - sheerline/docs/architecture.md
---

# Module 4.1 — The boundary and the retained moat

## You are here

Track 3 walked the four verbs of the quality loop. Track 4 turns a reader into a subject-matter expert: the boundary that protects the system, running it end to end, extending it, and the capstone. This module opens the boundary. The question it answers: where is the line between the scaffold HeyHi can publish and the calibrated instance it keeps? Previous: [module 3.4 in Track 3](../track-3-quality-loop/module-3-4.md). Next: [`module-4-2.md`](module-4-2.md).

## Learning objectives

After this you can:

- Name the three tiers of the boundary: public keel, Confidential Sheerline, and the retained moat.
- State the scaffold-ships / populated-instance-stays split and the one rule behind it.
- Sort an artifact across the moat wall and defend it in a line.
- Say why evaluation is the one invariant HeyHi does not commoditize.

## Concept

The whole loop you learned is valuable, so the boundary that decides what leaves the building is load-bearing. It has three tiers. **Public keel** is the general harness scaffold, publishable openly. **Confidential Sheerline** is the design instance built on it, on a hold for the public tree until its gate opens. The **retained moat** is the calibrated instance behind both, and it never ships. The seminar itself has been drawing this line the whole way: keel-tagged modules are written to lift into public documentation, Sheerline-tagged modules stay internal, and the calibrated content is taught as architecture only, never reproduced.

The operative rule across the tiers is the **scaffold-ships / populated-instance-stays** split. The scaffold, the `os/` layer, the registry engine, the corrections schema and its generic seeds, the MCP contract, and the Design System MCP scaffold, is potentially publishable. The retained moat stays in a separate unpublished tree and is not built into the shipped scaffold: the boundary and evaluation layer, the graded evaluator, the conformance parser, the populated corrections corpus and its promotion judgment, the calibrated thresholds, and the populated MCP instance. The one line that makes this operational is worth holding onto: what ships is the empty structure with its generic seeds, and what stays is the populated, calibrated instance that fills it. A competitor can rebuild the scaffold; it cannot rebuild what fills it.

This is why the third invariant, evaluation before deployment, is the one HeyHi does not commoditize. A checking layer that has been calibrated on real work is the hard-to-copy asset, so the evaluation layer sits on the retained side of the wall, not the shippable scaffold. It is also the reason the whole seminar refused to print a tuned number: teaching the evaluator and corrections as architecture, and withholding their calibrated content, is this boundary observed in the curriculum. The legal grounding sits underneath and is a separate track: copyright attaches automatically to all the written work, trade secret protects the populated combination that is the moat, and one architectural combination may be patentable, pursued with counsel. HeyHi's IP strategy, a gitignored legal document read outside the tracked tree, is the authoritative record; this module teaches the boundary, not the filing.

One client-facing consequence follows and is worth stating plainly, because it comes up in every engagement. A system built for a client is client-owned: the implementation belongs to them. The methodologies, the platform, and the architectural patterns that produced it remain HeyHi's. The boundary is not a wall against the client; it is the line that lets HeyHi hand over what it built for them and keep the machine that made it.

## Walkthrough

Open `sheerline/os/operating-principles.md` and find "The IP boundary (scaffold ships, populated instance stays)". Read the two lists: the scaffold that is potentially publishable, and the retained moat that stays in a separate unpublished tree. Notice the section says the split is confirmed against a gitignored legal document resolved outside the tracked tree, so the authoritative source lives off the tracked tree and is referenced, never quoted in. Then open `sheerline/docs/architecture.md` and read figure 5: the crimson wall divides the scaffold that ships from the retained moat that stays, with the two-axis conflict order and what stays human beneath it.

## Lab

From figure 5 in `sheerline/docs/architecture.md` and the IP-boundary section of `sheerline/os/operating-principles.md`, sort these five artifacts across the moat wall, ships or stays, each with a one-line reason: (1) the corrections schema and its generic seeds, (2) the populated corrections corpus and its promotion judgment, (3) the MCP contract and scaffold, (4) the calibrated evaluator thresholds, (5) the registry engine.

**Success looks like:** schema-and-seeds ships, corpus-and-judgment stays, MCP scaffold ships, calibrated thresholds stay, registry engine ships, each justified by the one rule, the empty vessel ships and the filled instance stays.

## Common misreads

- *"Publishing the scaffold gives away the moat."* No. The empty schema and engine ship; the populated, tuned instance stays. That split is the entire point of the boundary.
- *"The moat is the code."* No. The moat is the calibrated content: the corpus, the thresholds, the promotion judgment. The code around it is the shippable vessel.
- *"A system built for a client is HeyHi's IP."* No. The client owns the implementation built for them; HeyHi retains the platform, patterns, and methods.
- *"Evaluation is a commodity checker."* No. It is the one invariant HeyHi does not commoditize, because a checking layer calibrated on real work is the hardest asset to copy.

## Self-check

1. Name the three tiers of the boundary and what each one is.
2. State the scaffold-ships / populated-instance-stays split and the rule behind it.
3. Why is evaluation the invariant HeyHi does not give away?
4. From the Lab: your five-artifact sort across the moat wall, each with its reason.

## Go deeper

- `sheerline/os/operating-principles.md`, the IP-boundary section: the scaffold and retained-moat lists in full.
- Architecture figure 5, [`../../docs/architecture.md`](../../docs/architecture.md), draws the boundary wall, the moat, and what stays human.
- The seminar's own moat line (README, "what this seminar does not do") is this boundary applied to the curriculum.
- The calibrated content the corpus and evaluator hold is taught as architecture in Track 3.3 and 3.4; running a loop inside this boundary is 4.2.

---

*HeyHi Confidential*
