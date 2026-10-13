---
classification: confidential
title: "Module 1.2 — What loads (four-class loading)"
track: 1
module: "1.2"
level: foundational
prereqs: ["1.1"]
est_minutes: 25
teaches: keel
opens_files:
  - releases/open-source/keel/os/operating-principles.template.md
  - releases/open-source/keel/docs/diagrams/what-loads.svg
  - releases/open-source/keel/docs/architecture.md
---

# Module 1.2 — What loads (four-class loading)

## You are here

You have the three layers. This module opens Layer 2's central discipline: how keel decides what enters a session's context and what stays on disk. Track 0 gave you Earn the Room as an invariant; here it becomes a rule you can apply to any file in the tree. Previous: [`module-1-1.md`](module-1-1.md). Next: [`module-1-3.md`](module-1-3.md).

## Learning objectives

After this you can:

- Name the four load classes and the "load when" condition for each.
- Apply the fewer-than-half rule to decide whether a file loads by default.
- Explain why the most firm-specific file in keel never loads at all.
- Classify a real keel file into a load class and defend the call.

## Concept

Track 0 gave you Earn the Room with two faces: authority (minimum permissions) and context (minimum information, loaded on discovery). This module is the context face turned into a working rule. The question it answers is blunt: for each thing keel owns, does it load into this session, and if so, when?

The answer is a four-way sort. Every piece of content, whether a context file, a principle set, a reference, or a skill, gets classified into exactly one load class.

**always.** Every session needs it, so it loads at session start with no condition. This is a short list on purpose: the firm's identity and voice, the operating principles, and the active corrections. Three files, not thirty. If the always list grows, the starting context grows with it, and that cost is paid on every session whether the task touches the content or not.

**conditional.** Load it when the session type matches. A plan file loads for a planning session; a client-build context loads for a client build. The trigger is the shape of the work, decided near the start, not the individual step.

**on-demand.** Load it when the task explicitly calls for it: a specific reference, the session-rules file at close, the decision log when you are appending to it. The agent reaches for these the way you reach for a manual, when the immediate step needs them and not before.

**searchable.** Retrievable from a registry, never pre-loaded. This is where the skills live. Forty skills would drown a session if they all loaded, so the registry finds the one the task needs and only that one enters context. Module 1.3 is this class made mechanical.

Under the four classes sits one rule of thumb that decides the hard cases: if content is relevant to fewer than half of sessions, it must not load by default. Measure the token cost rather than guessing at it. The rule is deliberately strict, because the failure it prevents is quiet. Context that loads and is never used does not announce itself. It fills the window with procedures the task will never touch, and the work gets a little worse for reasons no error message will name.

The sharpest illustration in the whole scaffold is the company profile, and it repays sitting with, because it looks like an oversight until you see it. The profile is the most firm-specific file keel has. It captures your identity, your voice, your services. And it never loads into a session at all. Its job is not to sit in context; its job is to fill the other files. Voice rules get written from it once, into the always-loaded context; services get written into the skills that need them. After that the profile is a source document, read by a human during setup, not by an agent doing the work. A file being important is not the same as a file needing to load. That distinction is Earn the Room in one example.

You will see this sort applied for the rest of the seminar. The registry in 1.3 is the searchable class. The corrections in 1.4 are always-loaded, but only in their active form. Memory in 1.5 is on-demand recall, retrieved by meaning rather than pre-loaded. Each is a decision about when something earns the room.

## Walkthrough

Open `releases/open-source/keel/os/operating-principles.template.md` and find invariant 2, Earn the Room. Read the four-row load-class table: always, conditional, on-demand, searchable, each with its "load when" condition. Directly under it is the fewer-than-half rule and the instruction to measure the token cost. Notice the closing line: this four-way split is the mechanism, not a suggestion.

Now open `releases/open-source/keel/docs/diagrams/what-loads.svg` and read the load class stamped on every entry of a real file tree. Three files load always; a handful load on demand; the skills are searchable; and the company profile is marked not loaded at all. The figure is the rule applied to an actual scaffold, and the profile's tag is the part to stare at. keel's architecture doc frames the same picture in one line: most of the scaffold never enters a session.

## Lab

Classify a real keel file. Take these four and assign each to one load class, with a one-line reason grounded in the fewer-than-half rule: `releases/open-source/keel/os/agent-context.template.md`, `releases/open-source/keel/os/project-state.template.yaml`, `releases/open-source/keel/os/session-rules.template.md`, and `releases/open-source/keel/skills/registry/skill-registry.template.yaml`. Then answer the trap question about a fifth file, `releases/open-source/keel/profile/company-profile.template.yaml`: which load class does it belong to, and why is "none of them" the correct answer rather than a bug?

**Success looks like:** four defensible class assignments, each with a reason, and the company profile correctly identified as not-loaded because its job is to fill the other files rather than to sit in context.

## Common misreads

- *"Earn the Room is about permissions."* Only half. It governs context as hard as it governs authority: load less, not only allow less.
- *"Important files should always load."* No. The profile is the most firm-specific file keel has, and it never loads. Importance is not a load trigger; relevance to this session is.
- *"Searchable means slower."* No. Searchable means the registry surfaces the one skill the task needs so the other thirty-nine stay out of context. What it removes is the context it never loads.
- *"Conditional and on-demand are the same."* Close, not equal. Conditional keys on the session type, decided near the start. On-demand keys on the specific task step, decided in the moment.

## Self-check

1. Name the four load classes and the "load when" condition for each.
2. State the fewer-than-half rule, and the quiet failure it prevents.
3. Why does the company profile never load, and what does it do instead?
4. From the Lab: your four class assignments, and the one file that does not load.

## Go deeper

- `releases/open-source/keel/os/operating-principles.template.md`: invariant 2 and the load-class table in full.
- `releases/open-source/keel/docs/diagrams/what-loads.svg`: the classes stamped on a real tree.
- `releases/open-source/keel/docs/architecture.md`, figure 2, is that tree in one frame; it draws what this module sorts.
- The searchable class becomes mechanical in module 1.3; the always class, in its active-only form, is the corrections registry in module 1.4.

---

*HeyHi Confidential*
