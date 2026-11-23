---
title: "Sheerline Session Workflow Rules"
adapted_from: releases/open-source/keel/os/session-rules.template.md
---

# Sheerline Session Workflow Rules

Operational patterns that complement `os/operating-principles.md`. Those govern *what* to produce; these govern *how*. Adapted from keel's `os/session-rules.template.md` (the mechanisms port unchanged; the design smoke test is the design-scoped addition).

The Framing and Entry gates below, plus the go/kill/hold verdict in the Planning Artifact Convention, are the outer lifecycle around the four verbs: Framing and Entry open a scoped piece of work, the Exit Gate closes it, and the verdict says whether it keeps going. The inner loop (retrieve → validate → grade → learn) and the Exit Gate are untouched. These gates, and every sign-off an output waits on, carry the gate fields below: an owner, an age, an escalation path and a proxy-aware signature.

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

## Gate fields: owner, age, escalation, signature

A named gate is any point where a Sheerline artifact waits on a person: the Framing and Entry gates and the go/kill/hold verdict above, an Approver's sign-off on a decision record, a presenter's sign-off on a pre-read, a designer's sign-off on an annotation, a cross-owner confirmation on a blueprint. A gate that names nobody, never ages and escalates to no one is limbo with a heading. So every gate records the same fields. In a planning artifact's frontmatter they sit under one `gates:` key, one entry per gate, so the three-line `framing:` and `entry_gate:` blocks stay three lines; a markdown output carries the same fields as labeled lines in its named-gate section (`Owner: … Opened: … Max age (days): … Escalate to: …`, then the signature line with `Proxy:` and `Where:`), which is the form the Sheerline skills' scaffolds use.

```yaml
gates:
  <gate name>:                  # framing | entry | verdict | the output's own sign-off (e.g. approver)
    owner: "<the one named person who must act; never a role, a team, or 'the room'>"
    opened: "YYYY-MM-DD"        # the day the gate was handed to the owner
    max_age_days: <days>        # an integer the engagement sets; how long the gate may stay open
    escalate_to: "<a named person, not the owner, who hears when the gate ages out>"
    signature:
      by: ""                    # who signed; blank until someone signs
      proxy: ""                 # "no" when the owner signs; "yes" when someone signs on the owner's behalf (false and true read the same)
      date: ""                  # YYYY-MM-DD
      where: ""                 # a link to the signing surface: the Figma comment, the PR review, the record line
```

For the outer lifecycle: the `framing` and `entry` gates are owned by whoever must fill the block before retrieve or execution starts. They pass on their own machine-checkable condition (the three fields non-empty), not on a signature; the signature there records who filled the block; the `verdict` gate is owned by whoever sets go/kill/hold, so an unset verdict past its window reads `aged` and escalates, which is the circuit-break default in the Planning Artifact Convention given an owner and a person to hear about it.

**Pass condition:** `owner`, `opened`, `max_age_days` and `escalate_to` present and non-empty, and `signature` present (its sub-fields stay blank until someone signs). A missing field is the defect, as in the Entry Gate. A gate with no `max_age_days` reads as aged from the day it opened, never as unbounded. The engagement intake may carry defaults (`review.gate_max_age_days`, `review.gate_escalate_to`) that a skill copies into each new gate; the per-gate value wins. A scaffold ships `proxy` blank, never pre-filled: the person who signs states it.

**The state is derived, never stated.** A gate's state is read from its fields, not written as a separate flag, so one artifact cannot read signed and unsigned at once. Closed is decided first; every other state is a way of not being closed:

| State | Reads when |
|---|---|
| `closed` | `signature.by` is the owner, `signature.proxy` is `no`, and every drawn-by-default register row (below) is walked. Nothing else closes a gate |
| `open` | not closed, and today is on or before `opened + max_age_days` |
| `aged` | not closed, and today is past `opened + max_age_days`. Surfaced to `escalate_to`, and left out of every "done" count, the way an unset verdict is left out of ranking |

A gate that is not closed may also read `fired (proxy)`: `signature.by` is filled and `signature.proxy` is `yes`. That is a note on `open` or `aged`, never a third way to close. A signature by anyone other than the owner, or with `proxy` left blank, closes nothing either: the gate stays `open` or `aged` until the owner signs and says so.

**A proxy signature is proof, never a close.** When someone signs for the owner (the operator recording an approval heard in a meeting, a lead signing for an absent reviewer), record it with `proxy: yes`. That records `fired (proxy)`: evidence the artifact reached a reviewer, which a grade may count as proof of use. It never closes the gate, never moves a record to `accepted`, and never counts as the owner's affirmation.

**Escalation is a notice, not a decision.** An aged gate goes to `escalate_to` as a question: this has waited past its window; does it still need the owner, or should it be re-scoped or dropped? The escalation owner decides. The run that surfaced the age decides nothing, and never signs, re-scopes or drops a gate itself.

**Where the signature lives.** With the engagement's review surface on Figma (`review.review_surface: figma`, the default), the owner usually signs in a comment thread on the frame, and `signature.where` links that comment. With `html` or `room`, `where` links the record line or the meeting capture. Whatever the surface, the fields above are the record.

### Uncertain calls

Every gated output carries an `## Uncertain calls` section beside its named gate: the drafts in the output that the run itself is least sure of (an inferred node, a borderline tier, a settlement phrase that may be a hypothetical, a binding that resolved but reads wrong). It is a list, unordered and unscored. It never ranks the calls or names the one that matters most. An output with none writes the literal `none`, as the Entry Gate does for `blocking_unknowns`, so a missing section is a visible defect rather than an implied "all sure". The section points the owner's attention; it does not replace reading the rest of the output.

### The drawn-by-default register (opt-in, off by default)

The standing rule is that a judgment slot ships empty. Under deadline a team may choose to have the run draw its recommended answer into each slot and walk the drawn calls with the owner afterward. That inverts the empty-slot rule, so it is a disposition the human opts into per engagement (`review.drawn_by_default: true` in the engagement intake). It is never the default and never a skill's own choice: a design call drawn by default sits on the don't-automate line, so the opt-in is the human's.

With the opt-in on, a gated skill may draw a recommended answer only into a register row, never silently into the slot:

```yaml
drawn_by_default_register:
  - slot: "<the judgment slot the answer was drawn into>"
    drawn: "<the recommended answer, as drawn>"
    alternative: "<the other answer considered>"
    redraw_cost: "<what changing course costs if the owner picks the alternative>"
    walked_by: ""               # the owner, once the row is walked with them; blank until then
    walk_by: "YYYY-MM-DD"       # the date the row must be walked by
```

The gate stays open until every row is walked: a row with a blank `walked_by`, or one walked by proxy, keeps the gate from closing (it reads `open` or `aged` by the table above, and a row past its `walk_by` date is flagged as overdue), whatever the signature says. A drawn answer the owner never walked was never decided. With the opt-in off, the register is absent and the slots ship empty as always.

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

