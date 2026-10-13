---
classification: confidential
title: "Module 4.4 — Capstone: the compounding argument"
track: 4
module: "4.4"
level: expert
prereqs: ["4.3"]
est_minutes: 30
teaches: sheerline
opens_files:
  - sheerline/docs/architecture.md
  - releases/open-source/keel/docs/diagrams/compounding-loops.svg
---

# Module 4.4 — Capstone: the compounding argument

## You are here

This is the last module. You can run the system and extend it; now assemble the argument for why it compounds, and teach it back. Nothing here is new: every claim traces to a module you have already read. The question this module answers: why is session ten more reliable than session one? Previous: [`module-4-3.md`](module-4-3.md). Next: none; this module closes the seminar at 21 modules.

## Learning objectives

After this you can:

- Name the three compounding loops and what each one funnels back.
- Place the phase roadmap as governance, not a backlog.
- State the compounding argument in one breath.
- Teach the whole system to a novice in five sentences, one per track.

## Concept

The whole system rests on one claim: the system's own output is its next input, so each session is cheaper and more reliable than the last. Three loops carry it, and you have met all three in pieces.

**Corrections.** A mistake becomes a correction entry that loads at every session start, keeps firing, and is eventually promoted into a hard rule that joins the always-loaded core while the entry retires. That is Track 3.4 and the corrections lifecycle: institutional memory that a repeated mistake pays into once, so no later session pays again.

**Parameterization.** The engagement intake fills the configuration and the skills, a session runs them, you learn what to change, and the intake is refilled so everything downstream recalibrates. That is module 4.2: the harness is general, and each engagement teaches it how to be specific.

**Orientation.** The work passes the Exit Gate, which forces propagation into the decision log and the project state, which the next session reads to orient. That is the Exit Gate from 4.2 again, seen from the other side: this session's record is the next session's starting context, so nothing gets re-derived.

Above the loops sits the phase roadmap. Every practice area carries a coverage state and a phase, so a gap is a scheduled, visible thing rather than an invisible absence, and the system deepens area by area over phases rather than all at once. That is the governance from module 2.2: the thirteen areas tax maintenance, not the agent.

And the whole machine stays pointed at people. The loops compound the mechanical work precisely so a team has more room for the judgment that was never a generation target, the don't-automate line from module 0.3 restated as the reason the compounding is worth building at all.

Assembled, the argument is the seminar in one breath: a harness exists because reliability lives in the layer around the model; keel is that general harness; Sheerline instances it for design with one net-new foundations slot; the quality loop retrieves, validates, grades, and learns; the boundary keeps the calibrated moat while the scaffold ships; and three compounding loops make session ten cheaper than session one.

## Walkthrough

Open `sheerline/docs/architecture.md` and read figures 4 and 6 together as two halves of one machine: figure 4 is the quality loop that runs inside a session, figure 6 is the session lifecycle that carries one session to the next. Then open `releases/open-source/keel/docs/diagrams/compounding-loops.svg` and read the three loops, corrections, parameterization, and orientation, and the closing line, the system's own output is its next input. The diagram is keel's, so its parameterization loop names the general keel artifact, the company profile, which Sheerline instances as the engagement intake from module 4.2. Notice the phase roadmap is visible in figure 3, the registry, where each area shows a coverage state and the phase that fills it.

## Lab

Teach it back. Explain the whole system to a novice in five sentences, one per track, ending on the compounding claim.

**Success looks like:** five sentences, one mapped to each track, that a novice could follow. For example: **(Track 0)** a harness exists because an agent's reliability is won in the layer around the model, not the model itself; **(Track 1)** keel is that general firm-of-one harness, with a layered structure, four-class loading, a registry and confidence gate, corrections, a memory contract, and a session lifecycle; **(Track 2)** Sheerline instances keel for design, reusing all of it and adding one net-new slot of per-area governed foundations across thirteen practice areas; **(Track 3)** its most-built module is the quality loop, which retrieves the design system through the MCP, validates emitted output deterministically, grades it over time, and learns from correction; **(Track 4)** a boundary keeps the calibrated moat while the scaffold ships, and three compounding loops make session ten cheaper than session one.

## Common misreads

- *"The three loops are separate systems."* No. They are one machine. Each loop funnels a session's output back as the next session's input.
- *"Compounding means more automation."* No. It compounds the mechanical work so more room is left for the human judgment the don't-automate line protects.
- *"The phase roadmap is a backlog."* No. It is governance: a gap is a tracked, scheduled coverage state, not an invisible absence.
- *"The capstone adds new material."* No. Every claim here traces to an earlier module; the capstone only assembles them.

## Self-check

1. Name the three compounding loops and what each funnels back into the next session.
2. Why is the phase roadmap governance rather than a backlog?
3. State the compounding argument in one sentence.
4. From the Lab: your five-sentence teach-back, one sentence per track.

## Go deeper

- Architecture figures 4 and 6, [`../../docs/architecture.md`](../../docs/architecture.md): the quality loop and the session lifecycle as two halves of one machine.
- `releases/open-source/keel/docs/diagrams/compounding-loops.svg`: the three loops and the closing claim.
- The whole seminar, Tracks 0 through 4, is the un-simplified version of the five sentences above. With this module the seminar is complete at 21 modules.

---

*HeyHi Confidential*
