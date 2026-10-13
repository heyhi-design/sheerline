---
classification: confidential
title: "Sheerline Dispatch: Reference"
adapted_from: releases/open-source/keel/os/dispatch/README.md
---

# Sheerline Dispatch: Reference

A dispatch prompt is a self-contained work order: everything an agent needs to complete a defined design-practice task in a fresh session with no prior context. Adapted from keel's `os/dispatch/README.md` (the anatomy ports unchanged).

---

## What dispatch is for

Dispatch fits tasks where the output is a document or a decision record (not a send, a schedule, or a live action), the source material already exists in the workspace, the constraints are fully knowable from files, and the work can run asynchronously. It is not for sending messages, scheduling, financial inputs, or anything needing credentials.

---

## ENV CHECK: required at the top of every dispatch prompt

```
─── ENV CHECK (complete before anything else) ────────────────────────────────
Read the file at: <absolute path to the instance's root agent guide>

IF it loads (its first line matches the title the instance records for it):
  proceed to MISSION.

IF you get any error:
  STOP. Report: "ENV ERROR: cannot read <path>. Confirm the workspace is mounted,
  then run this prompt again." Do not proceed.
──────────────────────────────────────────────────────────────────────────────
```

The instance fills the two placeholders once, in its own batch files. A fresh session does not inherit the workspace, so the check proves the session can see the files before it acts on them.

---

## Prompt anatomy: all six sections required

- **MISSION**: one directive. What the agent must produce, specific, not aspirational.
- **CONTEXT LOAD**: an ordered file list: path, what to extract, how to interpret. Source files before derivative files, constraint files before content files. Include the standing directive once, after the list:

  > Before declaring any cited path missing or unreadable, run a glob against the canonical path and report the result. The glob is the source of truth, not partial inferences from earlier reads.

- **OUTPUT SPEC**: the exact delivery: file path, format, frontmatter, classification mark, an honest length range, section structure.
- **CRITICAL CONSTRAINTS**: the non-negotiables: the standing voice and classification constraints, then the task-specific ones. For a design task, include: grades inform never gate; the taste boundary; foundations reference the corpus, never byte-copy; the retained moat is not built.
- **SMOKE TESTS**: specific, binary, verifiable checks. Include a **day-0 self-review** (adversarial re-read; glob every cited path; fix every MISS) and, for a visual artifact, a render-and-look check. Aim for at least four; six to eight for high-stakes output.
- **QUALITY GATE**: a single paragraph stating what "done" looks like, as a checklist.

---

## Where batch files live

`os/dispatch/batches/dispatch-prompts-<date>-<slug>.md`, one file per generation session, several prompts per file. The Studio dispatch board renders this folder. It ships seeded with two worked examples (`example: true` in frontmatter) that show the convention; an instance adds its own batches beside them. An instance that already keeps batches elsewhere (HeyHi keeps its in the monorepo's root `dispatch/`) can leave this folder at the examples.

---

## Execution status: frontmatter convention

Every dispatch file carries a `status:` field (`pending | partial | done | archived`). Update it when a prompt runs. An unflipped status is a stale trigger the next scan re-fires on.

---

*Session rules: `os/session-rules.md` · Operating principles: `os/operating-principles.md`*

*HeyHi Confidential*
