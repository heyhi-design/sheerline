---
classification: confidential
title: "Module 0.2 — The ship lineage and the naming discipline"
track: 0
module: "0.2"
level: novice
prereqs: ["0.1"]
est_minutes: 20
teaches: sheerline
opens_files:
  - sheerline/README.md
  - sheerline/docs/architecture.md
  - releases/open-source/keel/README.md
---

# Module 0.2 — The ship lineage and the naming discipline

## You are here

You know the harness thesis: the scaffold, not the model, wins the reliability. This seminar teaches two scaffolds, keel and Sheerline, and one distinction you must never blur. This module gives you the mental model that keeps the whole system straight. Previous: [`module-0-1.md`](module-0-1.md). Next: [`module-0-3.md`](module-0-3.md).

## Learning objectives

After this you can:

- Explain the keel and sheer ship metaphor and why each name fits its layer.
- State the three-way separation and name the trap it exists to prevent.
- Place Sheerline as a keel *instance*, not a fork, and say why that choice matters.
- Read architecture figure 1 and locate each named thing on it.

## Concept

A hull has two defining longitudinal lines. The **keel** is the structural line below the waterline. It carries the load and keeps the vessel upright and on course; nobody admires it, and nothing floats straight without it. The **sheer** is the visible line where the deck meets the hull, the curve your eye reads as the boat's grace. One line is structure. The other is the beautiful thing you actually see.

That is the naming logic. **keel** the harness is the structural spine: the general firm-of-one operating layer, the same for any solo practice. **Sheerline** is the line above it: the same harness idea aimed at design output, where the visible craft is the whole point. keel keeps you upright; Sheerline is what people see.

The metaphor carries a discipline, and it is the single most important thing in this module. Three things must stay separate:

1. **keel** is the general harness. It knows nothing about design.
2. **Sheerline** is the whole design-practice operating system: skills plus governed context across the entire design discipline, thirteen practice areas wide.
3. **The Design-Systems quality loop** (the MCP, the validator, the evaluator, the corrections registry) is *one module* of Sheerline. It is the most-built one, which is exactly why it gets mistaken for the whole thing.

Conflating the module with the harness is the trap this operating system exists to avoid. Someone who says "Sheerline is the design-system linter" has collapsed a thirteen-area practice OS into one tool inside one of its areas. Hold the three apart and the rest of the seminar stays legible; blur them and everything downstream gets confused.

One more placement, and it decides how you read Tracks 1 through 4. Sheerline is a keel **instance**, not a fork. It reuses keel's mechanisms directly: the registry engine, the corrections mechanism, the session lifecycle, the memory contract. It adds exactly one structural slot keel does not have, for per-area design context. A fork would let the two codebases drift apart and muddy which ideas are whose. An instance shares the spine and layers design content on top. That is why Track 1 (pure keel) is not wasted time on the way to Sheerline: Track 1 *is* most of Sheerline's machinery, taught once, cleanly.

## Walkthrough

Open `sheerline/README.md`. Read the section titled "the one frame" and the three-way naming caution directly under it. Notice the exact phrasing: keel's engine, loading taxonomy, corrections mechanism, and session lifecycle are reused "by adaptation," and there is one net-new slot. That reuse-plus-one-slot shape is the instance claim made concrete.

Now open architecture figure 1 through `sheerline/docs/architecture.md` (section 1, "Where Sheerline sits"). The figure draws exactly what you just read: the sheer line above the waterline, the keel line below, and the three-card separation of keel, Sheerline, and the quality-loop module, with the naming caution across the bottom. If the words and the figure agree in your head, this module has landed.

## Lab

In `sheerline/README.md`, find the three-way naming caution. For each of the three things it separates, write one sentence naming what it **is** and one naming what it would be wrong to call it.

**Success looks like:** three is/is-not pairs, and you can state in one sentence why calling the quality-loop module "Sheerline" is the specific error the caution warns against.

## Common misreads

- *"Sheerline is the Design System MCP."* No. That is one module inside one of thirteen practice areas. The MCP is a tool Sheerline reaches through a boundary, not Sheerline itself.
- *"Sheerline is a fork of keel."* No. It is an instance: it reuses keel's engine and adds one slot. Nothing structural diverges.
- *"keel is the design harness and Sheerline is the general one."* Backwards. keel is the general spine below the waterline; Sheerline is the design line above it.

## Self-check

1. Why is keel named for the line below the waterline and Sheerline for the line above?
2. Name the three things kept separate, and the trap that follows from blurring them.
3. Instance or fork: which is Sheerline, and what would the other choice have cost?
4. From the Lab: what specific naming error does the caution guard against?

## Go deeper

- `sheerline/README.md` — the frame and the naming caution in full.
- Architecture figure 1, [`../../docs/architecture.md`](../../docs/architecture.md).
- Track 2.1 shows how the instance is wired; Track 3 opens the quality-loop module.

---

*HeyHi Confidential*
