---
classification: confidential
title: "Sheerline Session Workflow Rules"
adapted_from: releases/open-source/keel/os/session-rules.template.md
---

# Sheerline Session Workflow Rules

Operational patterns that complement `os/operating-principles.md`. Those govern *what* to produce; these govern *how*. Adapted from keel's `os/session-rules.template.md` (the mechanisms port unchanged; the design smoke test is the design-scoped addition).

The Framing and Entry gates below, plus the go/kill/hold verdict in the Planning Artifact Convention, are the outer lifecycle around the four verbs: Framing and Entry open a scoped piece of work, the Exit Gate closes it, and the verdict says whether it keeps going. The inner loop (retrieve → validate → grade → learn) and the Exit Gate are untouched.

---

## The Framing Gate

The first bracket around the inner loop. Before any retrieve call on a new piece of design work, commit to the outcome. A build or execution planning artifact whose work items run one or more of the four verbs (retrieve → validate → grade → learn) against a design output carries a `framing:` block in its frontmatter — three lines, never more (IBM's Hills, capped at three; Lean UX's falsifiable hypothesis, so "did it work" stops being a subjective debate):

```yaml
framing:
  who: "<the practice or user segment this output serves>"
  what: "<the capability or behavior sought>"
  signal: "<a falsifiable 'we will know we are right when…' sentence, OR a path to a
            design-measurability-mapper Measurability Map for anything past a one-line hypothesis>"
```

**Pass condition** (machine-checkable, not "someone approves"): all three sub-fields non-empty. A one-line frontmatter parse resolves it; a `state-sync.py` check may enforce it later under the existing Check-N numbering, but none is stood up here. **Scope:** a pure research or audit spec does not trigger its own gate — it produces no design output for the inner loop to run against. When `signal` needs more than one falsifiable sentence, escalate it to a `design-measurability-mapper` Measurability Map rather than overloading the line.

---

## The Entry Gate

The second bracket. Before execution starts on a scoped piece of work, file a three-line `entry_gate:` block once (Shape Up's shaping, sized — not a Scrum checklist run per item):

```yaml
entry_gate:
  scope: "<a named appetite/effort size — 'a session,' 'a dispatch,' 'a multi-session arc' — never 'TBD'>"
  consumer: "<who or what consumes the finished work — the Phase-B-consumer naming this program already requires at spec review, pulled forward to fire before execution too>"
  blocking_unknowns: "<named, or the literal string 'none'>"
```

**Pass condition:** all three sub-fields present and non-empty (the literal `none` counts). This stays a guideline fired once per scoped chunk, never a per-item checklist. The Definition of Ready never entered the Scrum Guide, and every primary source carries the same caution: a readiness check that blocks a work item until every box is ticked becomes a waterfall gate in agile's clothing. So `shaping incomplete` is itself a valid, recorded value for `blocking_unknowns`, not a hard stop — the failure mode is the missing field, not the unknown.

---

## Task Execution

Apply reversible changes directly. When a request ends in file changes, the request is the permission. Report what was done, not what you propose to do. Ask first only for irreversible actions (deleting, pushing, sending), genuinely ambiguous scope, or a single instruction that admits more than one materially different reading of a client-facing artifact.

---

## Task-Level Verification

Before marking any non-trivial task complete, verify three things: (1) the output matches the stated intent, not just the literal instruction; (2) no applicable constraint or correction was violated; (3) the work propagated to everything it affects. Creating a new file makes an index wrong (fix it in-task); modifying a file makes references stale (catch at integrity).

**Recompute computable values.** Any count, ratio, version, or derived value a machine could recompute is verified by running the computation, not asserted. A count that describes a set is computable: count the set. The skill count is derived from `skill-registry.py --stats` or the canonical skills table, never hardcoded from prose.

---

## Verify-Before-Claim

Every claim that asserts a verifiable state ("the tree matches the spec," "all references resolve," "the registry abstains cleanly") either names the exact command run and quotes its result, or is marked `[judgment]`. A bare assertion without either is a defect. Taste calls, positioning, and design critique are `[judgment]` by nature; anything a glob, grep, or one-line script could resolve is not.

A finding returned by a sub-agent, or an operator's report of an action ("I merged it"), is a lead, not a fact. When the effect is mechanically checkable, confirm it against ground truth before building on it.

**Scale verification to blast radius (the new-tooling ladder).** A passing seeded smoke on a script or tool you just built is the first rung, not done. Second: run it against real registry or corpus data and read the output for junk, since seeded tests prove the logic you imagined and real data reveals the cases you did not. Third: an adversarial pass (malformed input, empty input, an idempotent re-run), where every probe failure becomes a permanent assertion, not just a fix. Fourth, for multi-file infrastructure: a fresh-context check that reproduces every numeric claim from its own run before the work is called done. A one-line mechanical edit needs none of this; a coverage meter or a routing guard needs all four.

**Report the harness, not just the number.** Sheerline authors eval and coverage claims, so when a claim is a metric (a coverage ratio, a routing-battery score, a case count) name the instrument that produced it, for example `measure_coverage.py` for the eval-home count, not the bare figure. A number without its harness cannot be checked and reads as false precision; naming the meter is what turns it from an assertion into a verifiable claim.

---

## The design smoke test

Design work has a failure mode that source inspection cannot catch: output that passes every automated check and still looks wrong. So the smoke test for any visual artifact is **render it and look**, not inspect the source only. Drive a real generation or open the rendered surface, view it, and test one specific observation against the design system's intent (a control shipped with all its states; a coherent type ratio; the reference honored). Retrieve the system through the MCP; validate the emitted output, not the self-reported manifest. This is the standing form of "grades inform, the human reads."

---

## Commit Envelope Convention

Every Sheerline commit carries a structured footer so history reads without cross-referencing two systems.

```
[sheerline] Verb + subject line

Decision-log: YYYY-MM-DD · Entry title   (omit if none)
Files: key files changed                 (omit if obvious)
Notes: anything that does not fit above   (omit if none)
```

---

## Planning Artifact Convention

Every planning artifact (`*-plan.md`, `*-spec.md`, `*-brief.md`, a next-session prompt) carries a `status:` frontmatter field (`pending | partial | done | archived`). Flipping it when work completes is a required close-out action. An unflipped status is a stale trigger the next session re-fires on.

A build or execution artifact also carries a **go/kill/hold verdict** beside `status:` — the third bracket of the outer lifecycle:

```
verdict: go | kill | hold | unset      # default: unset
```

The two fields answer different questions and neither overrides the other: `status:` records how far the work got; `verdict:` records whether it should keep going. Set the verdict at the points the practice already has — a workstream's own G-gate (the Phase A→B review), a plan's dated kill-condition check, or the Shape Up circuit-break default: a plan still at an incomplete status (anything but `done`/`archived`, in whichever status vocabulary the artifact uses) past its own cited re-check date with `verdict: unset` is not "still viable, rank it," it is a circuit left open, surfaced for a decision. That default is what keeps the field from being ceremony — silence now has a consequence (excluded from ranking, flagged) instead of indefinite limbo. The readers that act on it are named in `heyhi-plan-survey` and `session-run`; a verdict with no reader is exactly the ceremony this field exists to avoid.

---

## The Exit Gate

Every session that produces a document, artifact, plan, or decision record exits through this gate. The handoff cannot be emitted without it. Each item requires a concrete artifact under a named header, not a claim that the work was done. An empty header is a visible failure; advisory prose is not.

**Flavor A (default), three required headers:**

- `## Fixes Applied`: defect sweep, one line per fix, applied until clean.
- `## Smoke Test`: verification ran. For a visual artifact: render it and view it (see above), do not inspect source only. State what was run and the result.
- `## Next Session Prompt`: a copy-pasteable paragraph a fresh agent with no memory can resume from.

**Flavor B (when the session reads, writes, or advances a plan), five headers.** The three above plus:

- `## Findings Integration`: every finding integrated into the active plan, not just noted.
- `## Session Integrity`: a lightweight check that the integrated plan still holds against its original intent and that new entries propagated to the plan's index.

**Facilitation carve-out.** A purely conversational session (a critique conversation, a facilitation debrief) that produces no tracked artifact closes with a proportional record, not empty gate headers.

---

## Craft Check

Before finalizing any technical output (a schema, an architecture decision, a script), ask: is this the minimal, clear implementation, or a shortcut? If an approach feels like a workaround, build the proper one. This is the technical sibling of the voice rules: the voice rules force a better word; the craft check forces a better structure.

---

*Operating principles: `os/operating-principles.md` · Decision log: `os/decision-log.md` · Integrity: the `heyhi-session-integrity` skill, design-scoped.*

*HeyHi Confidential*
