---
classification: confidential
title: "Module 0.1 — The harness thesis"
track: 0
module: "0.1"
level: novice
prereqs: []
est_minutes: 20
teaches: keel
opens_files:
  - releases/open-source/keel/README.md
  - releases/open-source/keel/docs/three-layer-model.md
---

# Module 0.1 — The harness thesis

## You are here

First module, first track. Before any file, one idea has to land: the scaffold around a model, not the model itself, is where reliability is won. Everything else in this seminar is built on it. Next: [`module-0-2.md`](module-0-2.md), where the scaffold gets a name and a lineage.

## Learning objectives

After this you can:

- Define an agent harness and name its parts without hand-waving.
- Explain the SWE-bench Pro result and say precisely what it held constant.
- Point at the boundary between the harness and the model in a running agent.
- Say why durable value accumulates in the configuration, not the weights.

## Concept

You have built with agents, so you already know the loop: a model reads its context, calls a tool, reads the result, and goes again. The model is the engine. The **harness** is everything around the engine that turns raw capability into reliable operation. That includes the context the agent starts a session with, the tools it can reach, the rules it must follow, the memory of mistakes it has made before, and the discipline of how a session opens and closes. None of that is the model. All of it decides how well the model performs.

The empirical anchor is SWE-bench Pro. The same model weights swung about twenty-two points on the benchmark depending only on the scaffold around them. Same engine. Different harness. Twenty-two points. That is the thesis in one number: the harness, not the model, is where much of the reliability is won.

Why should that be true? Because a model reasons well in general but knows nothing about *your* firm in particular. It does not know your voice, your constraints, the four mistakes you keep making, or the order you do things in. The harness is where all of that lives. Hand the same model a harness that carries a firm's identity and its accumulated corrections, and it operates like someone who has worked there for a year. Hand it an empty prompt, and it operates like a stranger who is very good at reasoning.

That has a consequence worth sitting with. The model is rented and swappable; a better one ships every few months. The harness is owned, and it *accumulates*. A model upgrade does not carry your voice, your corrections, or your procedures forward. Your harness does. So the durable value of running a practice on agents is not in the weights you rent this quarter. It is in the configuration you own and keep improving. That is the whole reason keel and Sheerline exist as things you build rather than things you buy.

Hold this as the load-bearing frame for the rest of the seminar. keel is a harness you fill in. Sheerline (Track 2) aims the same idea at design output. Both are bets that the configuration layer is where the reliability, and the value, actually live.

## Walkthrough

Open `releases/open-source/keel/README.md`. Read the opening framing: keel is a fillable scaffold that turns a general-purpose coding agent into an operator that already knows one firm's identity, voice, constraints, and procedures. Notice what it deliberately is *not*: not a hosted product, not the judgment itself, and not the runtime. It ships no model and no agent loop. It is configuration and deployment, waiting to be filled.

Now open `releases/open-source/keel/docs/three-layer-model.md`. You do not need to master the three layers yet (Track 1 does that). For now, notice only the ownership language: you *rent* the runtime, *own* the configuration once you fill it in, and *extend* the deployment. The sentence about the runtime being swappable is the harness/model boundary made explicit. Everything above that line is the harness. The model runs below it.

## Lab

Open `releases/open-source/keel/README.md` and find where it states what keel is not. Write down, in one line each, three things keel is explicitly not.

**Success looks like:** three "keel is not …" statements, each traceable to a specific claim in the README (for example, that it is not a hosted product with a login and a subscription).

## Common misreads

- *"A stronger model makes the harness unnecessary."* No. The twenty-two-point swing happened at fixed weights. The harness sets the ceiling the model can reach, whatever model you drop in.
- *"The harness is just a big system prompt."* No. It is context plus tools plus memory plus session discipline plus corrections, most of which never sits in the prompt at the same time.
- *"A harness is a framework I import."* No. It is a specification the runtime honors, not a library the model calls. The runtime enforces none of it; the configuration does.

## Self-check

1. In one sentence, what is an agent harness, and what is it not?
2. What did SWE-bench Pro hold constant, and what did it vary?
3. Why does upgrading the model not carry a firm's accumulated value forward?
4. From the Lab: name the three things keel is not.

## Go deeper

- `releases/open-source/keel/README.md` and `releases/open-source/keel/docs/three-layer-model.md` — the source of this module's frame.
- Architecture figure 2, [`../../docs/architecture.md`](../../docs/architecture.md), draws the layers you just met in words.
- Track 1 opens the harness up one layer at a time.

---

*HeyHi Confidential*
