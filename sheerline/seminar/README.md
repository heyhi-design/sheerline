---
classification: confidential
title: "Sheerline + keel: the seminar"
status: done
---

# Sheerline + keel — the seminar

**A self-paced curriculum that takes you from novice to subject-matter expert on how keel and Sheerline actually work.**

You already know what an agent is: a model in a loop, calling tools, carrying context. This seminar is about the *layer around the model*, the harness, where most of the reliability is actually won. It teaches keel (the general firm-of-one harness) and Sheerline (the design-practice harness built on top of it) from first principles, through the real files, to the point where you could stand up, extend, or teach the system yourself.

## Who this is for

You are fluent in agentic systems at a high level. You have built with agents and models, you understand tool-calling and context, and you can read Python and YAML. You have **not** worked inside keel or Sheerline before. By the end you will have.

No prior design-systems knowledge is assumed. Where the design module needs a concept (tokens, WCAG, drift), the module teaches it.

## How the curriculum works

The seminar is a **track ladder**. Each track is a coherent level; later tracks assume the earlier ones without re-teaching them. Progression is by track, not by difficulty labels inside a page.

Each **module** is one self-contained reading unit built from the same eight parts (see [`_module-template.md`](_module-template.md)):

1. **You are here**: where this module sits in the arc.
2. **Learning objectives**: what you will be able to *do* after it.
3. **Concept**: the teaching exposition. Read this.
4. **Walkthrough**: a guided read of the real tree and code. Open the files named.
5. **Lab**: do it yourself against the real repo, with a "success looks like".
6. **Common misreads**: the traps, named so you skip them.
7. **Self-check**: questions that confirm you actually own the idea.
8. **Go deeper**: the canonical files and the architecture-doc figure behind the module.

Work a module by reading the Concept, doing the Walkthrough with the files open, then the Lab. Do not skip the Lab. The harness is a *practice*, and the labs are where the practice lands.

The figures the modules reference are Sheerline's architecture set at [`../docs/architecture.md`](../docs/architecture.md). The seminar teaches the system; the architecture doc is its map.

## The curriculum map

| Track | Level | What you leave with | Modules |
|-------|-------|---------------------|---------|
| **0 · Orientation** | novice entry | Why a harness exists at all, and the mental model that holds the whole system together | 0.1 The harness thesis · 0.2 The ship lineage and the naming discipline · 0.3 The four invariants, Earn the Room, and the don't-automate line |
| **1 · keel** | foundational | You can read, stand up, and reason about the general harness end to end | 1.1 The three-layer model · 1.2 What loads (four-class loading) · 1.3 The registry engine and the confidence gate · 1.4 Corrections: compounding memory · 1.5 The memory contract · 1.6 Session lifecycle, Exit Gate, dispatch |
| **2 · Sheerline** | intermediate | You understand how keel becomes a design harness, and what the one net-new slot buys | 2.1 Sheerline as a keel instance · 2.2 The 13-area practice registry · 2.3 The foundations slot (reference, never copy) · 2.4 The two-axis conflict order and the fundamentals layer |
| **3 · The quality loop** | advanced | You can trace retrieve → validate → grade → learn through the real subsystems | 3.1 RETRIEVE: the Design System MCP · 3.2 VALIDATE: the validator · 3.3 GRADE: the evaluator · 3.4 LEARN: the corrections registry |
| **4 · SME synthesis** | expert | You can run a full loop, extend the system, and defend where judgment stays human | 4.1 The boundary and the retained moat · 4.2 Running a loop end to end · 4.3 Extending the system · 4.4 Capstone: the compounding argument |

**All five tracks are built and pass the smoke test** (21 modules): the spine (this file, the module template, the smoke test), **Track 0** (orientation, three modules), **Track 1** (keel end to end, six modules), **Track 2** (Sheerline, the design instance, four modules), **Track 3** (the quality loop, four modules), and **Track 4** (SME synthesis, four modules). Tracks 1 through 4 landed as the sequential dispatch batch under [`../../dispatch/`](../../dispatch/); `smoke_test.py` passes over all 21 modules (structure, paths, links, prereq DAG, voice, separability clean).

## The separability line (why the tracks split where they do)

Separability is per module, carried by the `teaches:` tag, not strictly per track. The `teaches: keel` modules (0.1, 0.3, and all of Track 1) teach the general harness and are written to lift cleanly into keel's own public documentation later without a rewrite. The `teaches: sheerline` modules (0.2, and Tracks 2 through 4) teach Sheerline, which is Confidential and gated (C-1 for any publish, D-3 for any offering), and stay internal until those gates open. Track 0 is deliberately mixed: its orientation includes the keel/Sheerline lineage (module 0.2), which is Sheerline-specific. When you author a `teaches: keel` module, keep it self-contained. It may never depend on a Confidential Sheerline internal to make sense, and the smoke test enforces that.

This is Sheerline's own Build → Abstract → Content model applied to the seminar itself: build it internal-first on the real system, abstract the public half after the gate.

## What this seminar does not do

It teaches the moat *as architecture* (the shape of the evaluator, the corrections corpus, the calibration), never the calibrated content itself. The populated corpus, the golden set, and the tuned thresholds are the retained moat; they are named and located, never reproduced. This is the same line the architecture doc's figure 5 draws.

---

*Start at [`track-0-orientation/module-0-1.md`](track-0-orientation/module-0-1.md). Architecture map: [`../docs/architecture.md`](../docs/architecture.md). Frame and naming: [`../README.md`](../README.md).*

*HeyHi Confidential*
