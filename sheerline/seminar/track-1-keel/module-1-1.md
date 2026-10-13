---
classification: confidential
title: "Module 1.1 — The three-layer model"
track: 1
module: "1.1"
level: foundational
prereqs: ["0.3"]
est_minutes: 25
teaches: keel
opens_files:
  - releases/open-source/keel/docs/three-layer-model.md
  - releases/open-source/keel/README.md
  - releases/open-source/keel/examples/README.md
---

# Module 1.1 — The three-layer model

## You are here

Track 1 opens keel one layer at a time. Track 0 gave you the thesis (the scaffold, not the model, wins the reliability), the lineage (keel below the waterline, the design line above), and the four invariants. This module answers the first structural question: what are the actual layers of a keel instance, who owns each one, and what survives when you change agent tools? Previous: [module 0.3 in Track 0](../track-0-orientation/module-0-3.md). Next: [`module-1-2.md`](module-1-2.md).

## Learning objectives

After this you can:

- Name the three layers of a keel instance and state who owns each.
- Point to the line a change of agent tool has to respect, and say why it holds.
- Explain the `.template` rename rule and what "filling in" a template actually does.
- Read a filled instance and recognize the shape of "done" in each layer.

## Concept

You met the harness and model boundary in Track 0 as a thesis. keel turns it into a structure you can point at. A keel instance is three layers stacked, and the whole design turns on knowing which layer you are looking at, because that tells you who owns it, whether you can edit it safely, and what happens to it when you swap agent tools.

**Layer 1, the runtime, is the agent tool you bring.** It is the loop that reasons and calls tools, the permission system, and the sandbox the agent runs inside. keel implements none of it. Claude Code, Cowork, or any compatible agent runtime supplies this layer, and it is entirely theirs. You do not own it; you rent it. When you switch tools, this is the layer that changes, and the two above it should not have to.

**Layer 2, the configuration, is what turns a general agent into one that knows your firm.** It holds your written identity and voice, your binding operating principles, your session workflow, and your corrections memory. keel ships this layer as fillable templates. Once you fill them in, the content is yours, and a template cannot generate it for you: your voice, your constraints, and your history of corrections have to come from you. This is the layer with the most lasting value, because it is the one that accumulates. Every correction you record makes the next session a little more reliable, which is the compounding you met in the harness thesis.

**Layer 3, the deployment, is how the configuration becomes a working daily system.** It is the intake profile that captures your firm's identity and services, the starter skills that give the agent concrete procedures to run, and the registry that lets the agent find the right skill instead of loading all of them at once. You own this layer too, and it is the one you extend the most: new skills as the practice grows, new profile fields as you learn what you actually need captured.

The load-bearing feature of the whole picture is the line between Layer 1 and the two above it. keel's architecture doc draws it in crimson and names it the owned-versus-rented seam. Everything above the line is the harness you own and carry with you; the runtime below it is swappable. That line is the first invariant from module 0.3, provider-agnostic design, made concrete: change the model or the tool and only Layer 1 changes, because nothing in Layers 2 and 3 names a specific vendor. The honest caveat rides along unchanged. The templates are agnostic in design, and porting them to a different provider in practice is real adaptation work, not a configuration flip.

One mechanic makes the ownership line legible on disk: the `.template` rename rule. Every file keel ships as a fillable template carries a `.template` segment in its name. The operating principles arrive as `releases/open-source/keel/os/operating-principles.template.md`; the skill index arrives as `releases/open-source/keel/skills/registry/skill-registry.template.yaml`. Filling one in does two things at once: you write your firm's content into the bracketed slots, and you drop the `.template` segment so the live file sits beside the blank. The renamed file is what your runtime and scripts load; the template stays as the baseline you can diff against later. A keel repository you have set up therefore reads as pairs, a template you were handed and a filled file you own. When the registry search in module 1.3 looks for a file without the `.template` segment, this rule is why.

Hold the three layers as the frame for the rest of Track 1. Everything ahead lives in Layer 2 or Layer 3: what loads (1.2) is a Layer 2 discipline; the registry (1.3) and corrections (1.4) are Layer 2 and Layer 3 mechanisms; memory (1.5) is this same three-layer model applied one level down; and the session lifecycle (1.6) is how all of it runs.

## Walkthrough

Open `releases/open-source/keel/docs/three-layer-model.md`. Read the three layer headings and, under each, the single bolded ownership sentence: you rent Layer 1, you own Layer 2 once you fill it in, you own and extend Layer 3. Then read the short section "How the layers compose". The runtime loads your configuration at the start of every session, and nothing about the runtime knows it is "your firm" until that configuration arrives. That one sentence is the harness thesis restated as a data flow.

Now open `releases/open-source/keel/README.md` and find "What's inside". Map each folder to a layer: `os/` is Layer 2, the configuration; `profile/` and `skills/` are Layer 3, the deployment. Notice the note that nothing here installs as a package, that you clone the repository and run the scripts in place, so the interpreter version is the only requirement. That is the runtime boundary in miniature: keel is files you own, not a service you log into. The `.template` segment on the files under `os/` is the rename rule waiting for you.

## Lab

Open `releases/open-source/keel/examples/README.md` and read what it says about the worked instance at `releases/open-source/keel/examples/baseline-year/`: a one-person practice, invented, filled end to end. Then open two of its filled files and place each in a layer. Open `releases/open-source/keel/examples/baseline-year/os/agent-context.md` and notice how short it stays, because it loads every session and cutting matters more than covering (Layer 2). Open `releases/open-source/keel/examples/baseline-year/os/decision-log.md` and notice it holds two entries in ten months, because a log that fills up fast is recording activity, not decisions (Layer 2). Then note what the example deliberately does not ship: a filled session-rules file, which the examples README lists among the referenced-but-not-shipped files, because a worked example shows what a filled file says, not a second full copy of the scaffold.

**Success looks like:** you can state which layer `os/`, `profile/`, and `skills/` each belong to, name the owned-versus-rented line, and point to one filled baseline-year file whose shape (short, or sparse) teaches something a blank template could not.

## Common misreads

- *"You own the whole stack."* No. Layer 1 is rented from the agent tool. Only Layers 2 and 3 are yours, and Layer 2 only after you fill it in.
- *"The template is the thing you run."* No. The template is the blank. You fill it and drop the `.template` segment; the renamed file loads, and the template stays as the diff baseline.
- *"Configuration and deployment are the same layer."* No. Configuration is who the firm is (identity, voice, principles, corrections). Deployment is how that becomes daily procedure (profile, skills, registry). The profile feeds the skills, so they are separate on purpose.
- *"Switching agent tools rebuilds everything."* No. Only Layer 1 changes; Layers 2 and 3 carry over, because nothing in them names a vendor. That is the owned-versus-rented line doing its job.

## Self-check

1. Name the three layers and who owns each.
2. Which line does a change of agent tool have to respect, and why does it hold?
3. What does the `.template` rename rule do, and what stays behind after you rename?
4. From the Lab: name one baseline-year file whose shape teaches something a blank template could not, and say what it teaches.

## Go deeper

- `releases/open-source/keel/docs/three-layer-model.md`: the three layers and the ownership line in full.
- `releases/open-source/keel/docs/architecture.md`, figure 1, draws the layers and the crimson owned-versus-rented seam. The seminar's own map redraws the same model for design as figure 2 of [`../../docs/architecture.md`](../../docs/architecture.md).
- `releases/open-source/keel/examples/README.md`: the worked instance, and why the fiction is deliberate.
- The rename rule returns in module 1.3 (the registry loads the renamed file); the ownership line returns one level down in module 1.5 (memory behind a swappable backend).

---

*HeyHi Confidential*
