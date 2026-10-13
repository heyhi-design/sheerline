---
classification: confidential
title: "Module 2.1 — Sheerline as a keel instance"
track: 2
module: "2.1"
level: intermediate
prereqs: ["1.6"]
est_minutes: 30
teaches: sheerline
opens_files:
  - sheerline/README.md
  - sheerline/os/agent-context.md
  - sheerline/os/operating-principles.md
---

# Module 2.1 — Sheerline as a keel instance

## You are here

Track 1 taught keel, the general firm-of-one harness, end to end. Track 2 opens the design instance built on it. This module places Sheerline in that lineage and answers three questions at once: what does Sheerline reuse from keel unchanged, what single structural thing does it add, and what five rules govern the design-specific areas from day one at no build cost? Previous: [module 1.6 in Track 1](../track-1-keel/module-1-6.md). Next: [`module-2-2.md`](module-2-2.md).

## Learning objectives

After this you can:

- State what Sheerline reuses from keel and the one structural slot it adds.
- Explain why "instance, not fork" is the load-bearing choice.
- Name the five zero-cost operating invariants and the boundary each one fences.
- Hold the three-way naming caution without collapsing the design-systems module into "Sheerline."

## Concept

You met the naming lineage in Track 0: keel is the structural line below the waterline, Sheerline the visible design line above it. Now make it concrete. Sheerline is keel re-instantiated for design. It rents the same runtime, owns the same configuration in `os/`, and extends the same deployment layer in `skills/` and `profile/`. It reuses keel's engine, its four-class loading, its corrections mechanism, its session lifecycle, and its dispatch anatomy, all by adaptation rather than by copying. Everything you learned in Track 1 is still true here.

What Sheerline adds is exactly one structural slot keel has no room for: `os/foundations/<practice-area>/`, per-area governed design context that loads conditionally when a session's task calls for it. That single slot is the whole design-specific surface. Everything else is keel.

The choice of *instance* over *fork* is the load-bearing decision, and it is worth saying why. A fork would let the two codebases drift apart until nobody could say which idea was whose. An instance shares the spine and layers design content on top, so a fix to keel's engine is a fix to Sheerline's, and the separation the seminar teaches stays legible. This is also why Track 1 was not a detour on the way here: Track 1 is most of Sheerline's machinery, taught once, cleanly.

Hold the three-way naming caution from module 0.2, because this track will pressure it. keel is the general harness. Sheerline is the whole design-practice operating system, thirteen practice areas wide. The Design System MCP, the evaluator, and the corrections registry together are *one module* of Sheerline, its most-built one, which is exactly why it gets mistaken for the whole thing. Someone who says "Sheerline is the design-system linter" has collapsed a thirteen-area practice into one tool inside one area. Track 3 opens that module; this track keeps it in its place.

Now the part that ships in Phase 1 at no build cost: the **five zero-cost operating invariants**. They cost nothing to state, carry no filled foundation behind them, and prevent the whole class of boundary-collapse the discipline is most prone to. They govern the operating and conditional areas (registry areas 9 through 13) as threads:

- **Critique and facilitation governance.** Design critique evaluates work against stated goals through dialogue. It is never a generation target: the agent may assemble a critique pre-read and capture decisions, but renders no verdicts and suggests no critique content. Reading the room stays human.
- **The empathy boundary.** A model simulates cognitive empathy (inferring what a user might think). It does not have experiential empathy (having lived what a user lives). Research synthesis carries this boundary; simulated empathy is never presented as the real thing.
- **The ideation-diversity guard.** Model-assisted ideation lifts the quality of a single option and collapses the diversity of a set. It is stimulus, never selection: widen the field, measure overlap, warn on premature convergence, and let the human choose.
- **The Business-Acumen scope fence.** Sheerline's Business-Acumen area is design-business only: design ROI, stakeholder buy-in, design-team operations. HeyHi's own firm sales and marketing skills are the keel layer, out of scope here. The buyer is the designer as practitioner.
- **DesignOps as a governed practice.** Sheerline's own machinery, this registry and the corrections module and the session lifecycle, is the worked DesignOps artifact. The job is to govern that, not to ship a skill that "runs ops."

These five are the don't-automate line from module 0.3 made structural for the operating areas. Each names one specific thing the system does not do. The IP boundary that keeps the calibrated half unpublished (scaffold ships, populated instance stays) returns in Track 4.

## Walkthrough

Open `sheerline/README.md`. Read "the one frame" and the three-way naming caution, then "Architecture: a keel instance with one net-new slot". Notice the exact reuse language: keel's engine, loading taxonomy, corrections mechanism, session lifecycle, and dispatch anatomy are reused "by adaptation," plus the one net-new `os/foundations/<practice-area>/` slot.

Now open `sheerline/os/agent-context.md` for the through-line ("extend what a design team can do; never replace how it decides") and the same naming caution restated. Then open `sheerline/os/operating-principles.md`: the four architectural invariants port from keel unchanged, and the section "The zero-cost operating invariants" states the five you just met, each with the boundary it fences.

## Lab

From `sheerline/README.md`, write the reuse ledger: list what Sheerline reuses from keel (the three layers, the four-class loading, the corrections mechanism, the session lifecycle, the dispatch anatomy) and the one thing it adds (the `os/foundations/<practice-area>/` slot). Then open `sheerline/os/operating-principles.md` and, for each of the five zero-cost operating invariants, write the single thing it forbids the system from doing.

**Success looks like:** a reused-versus-net-new split every line of which traces to the README, plus five one-line "does not" statements, one per invariant (for example, the empathy boundary: does not present simulated empathy as the real thing).

## Common misreads

- *"Sheerline is a fork of keel."* No. It is an instance: it reuses keel's engine and adds one slot. Nothing structural diverges, which is the point.
- *"Sheerline is the Design System MCP."* No. That is one module, area 7, the most-built one, inside a thirteen-area practice. Track 3 opens it; do not let it stand in for the whole.
- *"Zero-cost means unimportant."* No. Zero-cost means they cost nothing to state and need no foundation built, yet they prevent the boundary-collapse the operating areas are most prone to.
- *"The five invariants are aspirations."* No. Each is a fence naming one thing the system does not do: render a critique verdict, present simulated empathy as real, select from an ideated set, sell the firm, or run ops as a skill.

## Self-check

1. What does Sheerline reuse from keel, and what one slot does it add?
2. Why is "instance, not fork" the load-bearing choice?
3. Name the five zero-cost operating invariants and the boundary each fences.
4. From the Lab: your reused-versus-net-new split, traceable to the README.

## Go deeper

- `sheerline/README.md`: the frame, the naming caution, and the instance-plus-one-slot shape.
- `sheerline/os/operating-principles.md`: the four invariants, the five zero-cost operating invariants, and the IP boundary.
- Architecture figure 2, [`../../docs/architecture.md`](../../docs/architecture.md), draws the three layers with the foundations slot added for design.
- The net-new slot is module 2.3; the thirteen-area registry is 2.2; the conflict order is 2.4; the retained moat returns in Track 4.

---

*HeyHi Confidential*
