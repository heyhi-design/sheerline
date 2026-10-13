---
classification: confidential
title: "Module 1.6 — Session lifecycle, Exit Gate, dispatch"
track: 1
module: "1.6"
level: foundational
prereqs: ["1.5"]
est_minutes: 30
teaches: keel
opens_files:
  - releases/open-source/keel/os/session-rules.template.md
  - releases/open-source/keel/os/dispatch/README.md
---

# Module 1.6 — Session lifecycle, Exit Gate, dispatch

## You are here

Module 1.5 handed you the memory contract. This module closes Track 1 with the motion that runs all the parts: how a session opens, works, and closes, and how you delegate a bounded piece of it to an unattended agent. Previous: [`module-1-5.md`](module-1-5.md). Next: Track 2, which shows how keel becomes a design harness (authored in the seminar's dispatch batch).

## Learning objectives

After this you can:

- Apply the one-edit-undo test to decide when to act versus ask.
- Explain verify-before-claim and the two propagation tiers.
- Name the Exit Gate headers for both flavors and say why the gate is structural.
- Name the six sections of a dispatch prompt and why the ENV CHECK runs first.

## Concept

The last four modules were the parts. This one is the motion: how a keel session runs from start to close, and how you hand a bounded piece of it to an unattended agent. Where the operating principles govern *what* to produce, the session rules govern *how* to produce it.

Start with the default that removes most of the friction. Reversible changes get applied directly. When the operator asks for work that ends in file changes, the request is the permission, and you report what was done, not what you propose to do. The test is one question: can this be undone with one edit? If yes, do it. You ask first only for the things that fail that test: irreversible actions (deleting files, pushing, sending an external message), genuinely ambiguous scope, or a single instruction that admits more than one materially different reading on a client-facing artifact. This is Earn the Room on its authority face: minimum ceremony for what is safe, a checkpoint for what is not.

Two disciplines keep the work honest inside a session. Verify-before-claim: every claim in a handoff that asserts a checkable state (tests pass, the file was created, the count reconciles) must either name the exact command that ran and quote its result, or be marked as a judgment call so the next reader knows it was not verified mechanically. A bare assertion is a defect, because the handoff is the contract and an unverified claim propagates as truth into the next session. Propagation, in turn, has two tiers. When you create a new thing, the index that should point to it is wrong until you update it, so that update happens in the same task, not at session end (Tier 1). When you modify an existing file, the documents that merely reference it may go slightly stale, and those can wait for an end-of-session integrity pass (Tier 2). Creating makes an index wrong now; modifying makes references stale later.

The close is structural, and it is the piece to keep. The Exit Gate is the gate every session that produces a document, artifact, plan, or decision passes through before it emits a handoff. Each item is a concrete artifact under a named header, not a claim that the work was done. There are two flavors. Flavor A, the default, has three required headers: `Fixes Applied` (the defect sweep, one line per fix), `Smoke Test` (verification actually ran, with what was run and the result stated), and `Next Session Prompt` (a copy-pasteable paragraph a fresh agent with no memory of this session could resume from). Flavor B, used when the session reads or advances a planning artifact, adds two more: `Findings Integration` and `Session Integrity`. The reason it is headers-with-artifacts rather than a closing checklist is the whole point: advisory closing language gets skipped under pressure, and an empty `Fixes Applied` block is a finding the next reader catches, while a missing "I checked for bugs" is invisible. Structure makes the gate visible.

Dispatch is the same discipline aimed outward: a self-contained work order an agent can complete in a fresh session with no prior conversation. It fits tasks whose output is a document or a decision, whose source already exists in the workspace, and whose constraints are fully knowable from files, so no mid-run judgment call is needed. It is not for sending messages, scheduling, or anything needing credentials. Every prompt carries six sections in order: MISSION (the one thing to produce), CONTEXT LOAD (what to read, and what to extract from each), OUTPUT SPEC (the exact delivery), CRITICAL CONSTRAINTS (the non-negotiables), SMOKE TESTS (binary checks the agent runs before calling it done), and QUALITY GATE (what "done" looks like as a checklist). An ENV CHECK sits above all six, because a fresh session may not have the workspace connected, and a standing directive tells the agent to glob a path before declaring it missing. This seminar's own tracks were written from prompts shaped exactly this way.

## Walkthrough

Open `releases/open-source/keel/os/session-rules.template.md`. Read "Task Execution" and the one-edit-undo test, then "Verify-Before-Claim" and "Propagation Tier Discipline". Then read "The Exit Gate" closely: the three Flavor A headers, the two Flavor B additions, and the paragraph on why it is structural rather than advisory. That paragraph is the argument for the whole gate.

Now open `releases/open-source/keel/os/dispatch/README.md`. Read "What dispatch is for" and its exclusions, the ENV CHECK block that goes at the very top, and "Prompt anatomy" with its six sections in order. Notice the standing directive to glob a path before declaring it missing, and the reason: a fresh sub-agent should not falsely report a file gone on a partial inference.

## Lab

Read a real dispatch prompt's anatomy and name its parts. Open `releases/open-source/keel/os/dispatch/README.md` and work through "Prompt anatomy". Write down the six required sections in order, and for each, one line on what it contributes: MISSION, CONTEXT LOAD, OUTPUT SPEC, CRITICAL CONSTRAINTS, SMOKE TESTS, and QUALITY GATE. Then answer why the ENV CHECK sits above all six rather than inside MISSION.

**Success looks like:** the six sections named in order with a one-line purpose each, and a one-sentence reason the ENV CHECK runs first: a fresh session must confirm the workspace is reachable before it does any work, or every later step fails for the same avoidable cause.

## Common misreads

- *"Every change needs approval."* No. Reversible changes get applied directly; the request is the permission. You ask only for irreversible actions, ambiguous scope, or a genuinely two-reading instruction on a client-facing artifact.
- *"The Exit Gate is a closing summary."* No. It is required headers with required artifacts. An empty header is a visible failure, which is exactly the point.
- *"Dispatch is for any task you want to hand off."* No. It fits document-or-decision output with source already in the workspace and no mid-run judgment. Sends, schedules, and credentialed actions are out.
- *"Verify-before-claim means verify everything."* No. It means either verify a checkable claim and quote the result, or mark it a judgment call. A taste call is not a verifiable claim; a passing test is.

## Self-check

1. What is the one-edit-undo test, and what does it decide?
2. Name the three Flavor A Exit Gate headers and the two Flavor B additions.
3. Why is the Exit Gate structural (headers-with-artifacts) rather than advisory?
4. From the Lab: the six dispatch sections in order, and why the ENV CHECK runs first.

## Go deeper

- `releases/open-source/keel/os/session-rules.template.md`: task execution, verify-before-claim, propagation tiers, and the Exit Gate in full.
- `releases/open-source/keel/os/dispatch/README.md`: the six-section anatomy, the ENV CHECK, and the glob directive.
- `releases/open-source/keel/docs/architecture.md`, figure 3, draws the session as start, route, work, close, and capture, the loop this module runs end to end.
- Track 1 ends here. Track 2 shows how keel becomes a design harness, and what the one net-new slot buys.

---

*HeyHi Confidential*
