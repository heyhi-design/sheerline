---
title: "Module 0.1 — The harness thesis"
track: 0
module: "0.1"
level: novice
prereqs: []
est_minutes: 20
teaches: keel
opens_files:
  - https://github.com/heyhi-design/keel/blob/v0.1.0/README.md
  - https://github.com/heyhi-design/keel/blob/v0.1.0/docs/three-layer-model.md
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

The evidence is public and easy to check. On SWE-Bench Pro, one model scores well apart in [its maker's own setup](https://openai.com/index/introducing-gpt-5-2-codex/) and on [Scale's standardized leaderboard](https://labs.scale.com/leaderboard/swe_bench_pro_public), and the difference is everything around the model. Those two runs vary more than the harness, so the cleaner evidence is a [controlled study](https://arxiv.org/abs/2608.26218) that held the weights fixed and changed one harness behavior: fully solved tasks rose sharply when the context window was tight and barely moved when it was roomy. Both halves of that result matter. The harness changes what the same engine can do, and how much it changes depends on the conditions the harness is built for.

Why should that be true? Because a model reasons well in general but knows nothing about *your* firm in particular. It does not know your voice, your constraints, the four mistakes you keep making, or the order you do things in. The harness is where all of that lives. Hand the same model a harness that carries a firm's identity and its accumulated corrections, and it operates like someone who has worked there for a year. Hand it an empty prompt, and it operates like a stranger who is very good at reasoning.

That has a consequence worth sitting with. The model is rented and swappable; a better one ships every few months. The harness is owned, and it *accumulates*. A model upgrade does not carry your voice, your corrections, or your procedures forward. Your harness does. So the durable value of running a practice on agents is not in the weights you rent this quarter. It is in the configuration you own and keep improving. That is the whole reason keel and Sheerline exist as things you build rather than things you buy.

Hold this as the load-bearing frame for the rest of the seminar. keel is a harness you fill in. Sheerline (Track 2) aims the same idea at design output. Both are bets that the configuration layer is where the reliability, and the value, actually live.

## Walkthrough

Open [keel's README.md](https://github.com/heyhi-design/keel/blob/v0.1.0/README.md). Read the opening framing: keel is a fillable scaffold that turns a general-purpose coding agent into an operator that already knows one firm's identity, voice, constraints, and procedures. Notice what it deliberately is *not*: not a hosted product, not the judgment itself, and not the runtime. It ships no model and no agent loop. It is configuration and deployment, waiting to be filled.

Now open [keel's docs/three-layer-model.md](https://github.com/heyhi-design/keel/blob/v0.1.0/docs/three-layer-model.md). You do not need to master the three layers yet (Track 1 does that). For now, notice only the ownership language: you *rent* the runtime, *own* the configuration once you fill it in, and *extend* the deployment. The sentence about the runtime being swappable is the harness/model boundary made explicit. Everything above that line is the harness. The model runs below it.

## Lab

Open [keel's README.md](https://github.com/heyhi-design/keel/blob/v0.1.0/README.md) and find where it states what keel is not. Write down, in one line each, three things keel is explicitly not.

**Success looks like:** three "keel is not …" statements, each traceable to a specific claim in the README (for example, that it is not a hosted product with a login and a subscription).

## Common misreads

- *"A stronger model makes the harness unnecessary."* No. The controlled result held the weights fixed and still moved the outcome. The harness shapes what any model you drop in can reach.
- *"The harness is just a big system prompt."* No. It is context plus tools plus memory plus session discipline plus corrections, most of which never sits in the prompt at the same time.
- *"A harness is a framework I import."* No. It is a specification the runtime honors, not a library the model calls. The runtime enforces none of it; the configuration does.

## Self-check

1. In one sentence, what is an agent harness, and what is it not?
2. In the controlled study, what was held constant, what was varied, and under which condition did the change matter?
3. Why does upgrading the model not carry a firm's accumulated value forward?
4. From the Lab: name the three things keel is not.

## Go deeper

- [keel's README.md](https://github.com/heyhi-design/keel/blob/v0.1.0/README.md) and [keel's docs/three-layer-model.md](https://github.com/heyhi-design/keel/blob/v0.1.0/docs/three-layer-model.md): the source of this module's frame.
- Architecture figure 2, [`../../docs/architecture.md`](../../docs/architecture.md), draws the layers you just met in words.
- Track 1 opens the harness up one layer at a time.
