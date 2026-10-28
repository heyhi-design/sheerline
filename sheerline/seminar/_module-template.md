---
title: "Seminar module template"
status: done
---

# The module template

Every seminar module is one markdown file built from the eight sections below, in order. This file is the shell to copy and the contract the [smoke test](smoke-test.md) checks. It is not itself a module (it teaches nothing); it is the mold.

**Copy the frontmatter and the eight `##` headers verbatim.** Fill each section. Do not add top-level sections or reorder them — the smoke test asserts the exact set.

## Frontmatter schema

```yaml
---
title: "Module N.M — <title>"
track: N                              # 0–4
module: "N.M"
level: novice | foundational | intermediate | advanced | expert
prereqs: ["N.M", ...]                 # module ids that must come first ([] for 0.1)
est_minutes: 25                       # honest reading + lab time
teaches: keel | sheerline            # keel-track modules stay publishable; sheerline-track modules are gated
opens_files:                          # the real files the learner will open
  - path/relative/to/repo/root        # or a published repo's URL at a release tag
lab_mode: heyhi-run                   # optional: the lab opens retained code (a HeyHi-run demonstration)
pointer_labels: [moat-runtime]        # optional: the provenance classes this file's pointers carry
---
```

**Pointers out of the tree.** A file from a published repo (keel, agent-corrections) is cited by its public URL pinned to a release tag, never by its monorepo path. A module whose lab opens retained code says so in its first section and sets `lab_mode: heyhi-run`; `pointer_labels` names the class of the retained paths it cites (`moat-runtime`, `oss-staged`, or `reference`), which the export's provenance lint reads. Build history is never cited by path.

`teaches:` is the separability tag. A `teaches: keel` module must be self-contained — it may not depend on a Sheerline internal to make sense, so it can later be lifted into keel's public docs. A `teaches: sheerline` module may use anything.

## The eight sections

### 1. `## You are here`
One short paragraph. Name the track, what the learner just finished, and the single question this module answers. Link the previous and next module.

### 2. `## Learning objectives`
A list of 3–5 items, each phrased "After this you can …" — an ability, not a topic. These are what the Self-check tests. Ladder them to the module's `level`.

### 3. `## Concept`
The teaching exposition — the part the deck-free house format leaves out. Explain the idea from the learner's existing agentic-systems knowledge, then build to the keel/Sheerline specific. Prose, not bullets. This is the longest section. Connect forward: name where the idea reappears later in the arc.

### 4. `## Walkthrough`
A guided read of the real tree and code. Every file named must exist (the smoke test globs them). Quote short excerpts; cite `path:line` where it helps. Tell the learner what to notice, not just what to open. Never paste a whole file — point and narrate.

### 5. `## Lab`
A hands-on task against the real repo: run the registry, trace a correction, call a validator, read a pre-registration. Give the exact command or the exact file to open, and a **Success looks like** line stating the observable result. A lab with no observable result is not a lab.

### 6. `## Common misreads`
2–4 traps, each one line: the wrong mental model, then the correction. These are the module's negative space — what a smart novice gets wrong here.

### 7. `## Self-check`
3–5 questions that a learner who owns the objectives can answer without re-reading. No answer key — the answers are in the Concept and the Lab. At least one question should require having done the Lab.

### 8. `## Go deeper`
Pointers only: the canonical files this module simplifies, and the architecture-doc figure that draws it (`../docs/architecture.md`). This is where a learner who wants the full, un-simplified version goes.

## Constraints (the smoke test enforces these)

- **Voice.** No standalone "AI" (say "agentic systems", "models", "intelligent systems", or name the function). No banned words. At most two em dashes in the module.
- **Real paths.** Every file named in `opens_files`, the Walkthrough, and the Lab must exist at authoring. The smoke test globs them; a dangling path is a failure.
- **Separability.** A `teaches: keel` module cites only keel, through its public repository at a pinned release tag (for example [keel v0.1.0](https://github.com/heyhi-design/keel/tree/v0.1.0)), and general concepts, never a Sheerline internal.
- **Honesty.** The moat is taught as architecture, never reproduced. No calibrated thresholds, no populated-corpus content, no golden-set answers.
- **Prereq DAG.** `prereqs` point only to lower-or-equal modules already authored. No cycles.

---

*Curriculum map: [`README.md`](README.md) · Structural check: [`smoke-test.md`](smoke-test.md)*

