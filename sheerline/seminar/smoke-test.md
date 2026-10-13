---
classification: confidential
title: "Seminar smoke test"
status: done
---

# The curriculum smoke test

Design-teaching has the same failure mode design work does: a module can read fine and still be structurally broken. A dangling file path, a missing section, a prereq that points nowhere, a keel-track module that quietly leans on a Confidential internal. The smoke test catches the structural half so review can spend its attention on the teaching.

Run it after authoring any module or track:

```bash
python3 sheerline/seminar/smoke_test.py
```

Exit 0 is clean. Exit 1 prints one line per issue.

## What it checks

| Check | Rule |
|-------|------|
| **Frontmatter** | all nine keys present (`classification, title, track, module, level, prereqs, est_minutes, teaches, opens_files`) |
| **Sections** | exactly the eight template headers, in order, nothing added or dropped |
| **Real paths** | every `opens_files` entry, every backticked repo path, and every inter-module link resolves. Repo-root paths (with a slash, no leading dot) resolve at the repo root; `.`-relative paths and bare `*.md` sibling links resolve against the module's own directory |
| **Prereq DAG** | every `prereqs` id is an authored module, and the depends-on graph is acyclic (full cycle detection, not just self-loops) |
| **Voice** | no standalone "AI", no whole-word banned terms, no banned phrases, at most two em dashes |
| **Separability** | a `teaches: keel` module never names a Sheerline internal (`sheerline/os/`, `sheerline/skills/`, `sheerline/profile/`, `heyhi-mcp/`, `ai-services/`) in its body or its `opens_files`, so the keel half stays liftable to keel's public docs |

## What it does not check

The smoke test is structural. It cannot tell you whether the Concept actually teaches, whether the Lab's "success looks like" is real, or whether the module lands novice-to-expert. That is the human read, the render-and-look of teaching. Four context-dependent banned words (`solution`, `deliverable`, `ecosystem`, `paradigm`) are left to that human read rather than flagged mechanically, because each has a legitimate technical sense.

A module that passes the smoke test is *ready to review*, not *done*.

---

*The contract it enforces: [`_module-template.md`](_module-template.md) · Curriculum map: [`README.md`](README.md)*

*HeyHi Confidential*
