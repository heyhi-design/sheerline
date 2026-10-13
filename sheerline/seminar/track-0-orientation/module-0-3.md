---
classification: confidential
title: "Module 0.3 — The four invariants, Earn the Room, and the don't-automate line"
track: 0
module: "0.3"
level: novice
prereqs: ["0.2"]
est_minutes: 25
teaches: keel
opens_files:
  - releases/open-source/keel/os/operating-principles.template.md
  - releases/open-source/keel/docs/diagrams/what-loads.svg
---

# Module 0.3 — The four invariants, Earn the Room, and the don't-automate line

## You are here

You have the thesis and the lineage. This is Track 0's last module, and it hands you the rules that govern every harness decision you will meet from here. Read it and Tracks 1 through 4 stop looking like a pile of mechanisms and start reading as applications of four ideas. Previous: [`module-0-2.md`](module-0-2.md). Next: Track 1, which opens keel one layer at a time (authored in the seminar's dispatch batch).

## Learning objectives

After this you can:

- Name the four architectural invariants and state the "never" behind each.
- Explain Earn the Room as both authority and context, and list the four load classes.
- Say why the don't-automate line is a design value rather than a disclaimer.
- Recognize a later mechanism as one of these invariants made concrete.

## Concept

Four principles govern every technical decision in the harness. They do not bend for convenience, and each of them recurs, by name, later in this seminar.

**Provider-agnostic design.** Build to run with one runtime today and swap to another later; never hardcode a single provider into application logic. The honest caveat travels with the claim: a configuration is agnostic in *design* even while it is authored and tuned against one runtime in *practice*. The never: never assume the model you rent this quarter is the model you keep.

**Earn the Room.** Nothing gets access, context, or authority by default. This has two faces. On authority: minimum permissions, and a human checkpoint before any irreversible action. On context: minimum information, loaded on discovery rather than pre-loaded. The never: never load something just in case. Content sorts into four classes: **always** (every session needs it), **conditional** (load when the session type matches), **on-demand** (load when the task explicitly calls for it), and **searchable** (retrievable from a registry, never pre-loaded). The rule of thumb is blunt: if content is relevant to fewer than half of sessions, it does not load by default.

**Evaluation before deployment.** Nothing ships without passing tests, across four layers: component, trajectory, outcome, and system. The never: never trust an agent's self-report over a test. This is also the one invariant a firm does not give away, because a checking layer that has been calibrated on real work is hard to copy. You meet it in Track 3.3.

**Protocols at boundaries, not inside them.** Choose an interface by the boundary it crosses, not the capability it offers. A protocol earns its cost when it crosses a team, a company, or an outside integrator; inside a controlled stack it is overhead. The stock line is "you don't need a courier to send yourself a package." The never: never pay for a boundary you are not crossing. You meet this in Track 3.1 and again in Track 4.1.

Earn the Room deserves a second pass, because it governs the most. It is why a registry exists at all (so an agent discovers the one skill it needs instead of pre-loading fifty), why the company profile never loads (its job is to fill other files, not to sit in context), and why only a handful of files load every session. When you meet the confidence gate in Track 1.3, you are meeting Earn the Room in mechanism form.

Finally, the line that keeps all of this pointed at people rather than away from them: the **don't-automate line**. Design critique, brand positioning, direction selection, hiring, performance feedback, mentorship, ethics, and strategic judgment are not automation candidates. This is a design value, not a disclaimer. The harness earns its keep by building the infrastructure so a team has *more* room for exactly the things that should stay human, not less. People stay in the loop by design; autonomy is earned, not assumed. When you meet "grades inform, never gate" in Track 3.3, that rule is this line made structural.

## Walkthrough

Open `releases/open-source/keel/os/operating-principles.template.md`. Read the four invariants. Notice that each is written with an honest caveat rather than a boast: provider-agnostic "in design, not proven portable," for instance. That restraint is itself a house value, and you will see it again in every figure's footer.

Find the Earn the Room load-class table in the same file, then open `releases/open-source/keel/docs/diagrams/what-loads.svg` to see the classes applied to a real file tree: three files always, a few on demand, skills searchable, and the profile not loaded at all. The figure is the invariant made visible.

## Lab

In `releases/open-source/keel/os/operating-principles.template.md`, find the four invariants and, for each, write the one thing it forbids. Then find the load-class table and assign one file type of your choosing (say, a rarely-needed reference document) to one of the four classes, with a one-line reason.

**Success looks like:** four "never" statements, one per invariant, plus one load-class assignment justified by the fewer-than-half rule.

## Common misreads

- *"Earn the Room is about permissions."* Only half. It governs context just as much as authority: load less, not only allow less.
- *"The don't-automate line is legal cover."* No. It is a design choice that shapes what the harness builds and what it refuses to build.
- *"Provider-agnostic means it runs anywhere today."* No. It is agnostic in design; realized portability is real adaptation work, not a configuration flip.

## Self-check

1. Name the four invariants and one "never" for each.
2. What are the four load classes, and what is the fewer-than-half rule?
3. Why is the don't-automate line a design value rather than a disclaimer?
4. From the Lab: your load-class assignment and the reason behind it.

## Go deeper

- `releases/open-source/keel/os/operating-principles.template.md`: the four invariants and Earn the Room in full.
- `releases/open-source/keel/docs/diagrams/what-loads.svg` — the load classes on a real tree.
- Watch the invariants recur: Track 1.2 (load classes), 1.3 (the confidence gate as Earn the Room), 3.3 (evaluation, and grades-inform-never-gate as the don't-automate line), 4.1 (protocols at the boundary).

---

*HeyHi Confidential*
