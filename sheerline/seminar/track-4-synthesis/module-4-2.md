---
classification: confidential
title: "Module 4.2 — Running a loop end to end"
track: 4
module: "4.2"
level: expert
prereqs: ["4.1"]
est_minutes: 35
teaches: sheerline
opens_files:
  - sheerline/profile/intake-conversation.md
  - sheerline/profile/engagement-intake.yaml
  - sheerline/os/session-rules.md
---

# Module 4.2 — Running a loop end to end

## You are here

Module 4.1 drew the boundary. Now run a full loop inside it. The harness is general; an engagement makes it specific, and a design session has to close in a way source inspection cannot. The question this module answers: how does an engagement parameterize the harness, and how do you close a design session honestly? Previous: [`module-4-1.md`](module-4-1.md). Next: [`module-4-3.md`](module-4-3.md).

## Learning objectives

After this you can:

- Scope an engagement through the intake without naming a client.
- Explain the hermetic seal and why the practice's own system is the default substrate.
- Name the render-and-look design smoke test and say why source inspection alone is not enough.
- Close a session through the Exit Gate with concrete artifacts, not claims.

## Concept

The harness is general; an engagement makes it specific, and the intake is that parameterization. It is a guided self-interview: the engagement in one line, the substrate, the design system and its suspected drift, which of the thirteen practice areas are in scope, and the boundaries. Its answers fill an intake file, and only the in-scope area foundations then load, conditionally, which is Earn the Room applied to a whole engagement.

Two rules keep this safe, and both are hard. The **hermetic seal**: never write a client name into a tracked file. Use a non-identifying label; a real engagement is filled in a gitignored folder in the main workspace, never in the tracked template, which stays blank. And **own practice first**: the practice's own system (substrate `self`) is the default substrate, so the loop can be built, taught, and tested without any client at all. The filled intake is pointed at a path at run time, passed in explicitly, never auto-discovered by scanning the tree, which is why the tracked template can stay blank and still be useful. This is the same discipline the seminar runs on: every example in this curriculum runs on the practice's own system.

Inside those boundaries the loop runs, retrieve then validate then grade, three of Track 3's four verbs. Then the session closes two ways that matter for design specifically. The first is the **render-and-look design smoke test**. Design has a failure mode source inspection cannot catch: output that passes every automated check and still looks wrong. So the smoke test for a visual artifact is to render it and look, to drive a real generation or open the rendered surface, view it, and test one specific observation against the system's intent, a control shipped with all its states, a coherent type ratio, the reference honored. Retrieve the system through the MCP and validate the emitted output, not the self-reported manifest. This is the standing form of grades inform and the human reads, the rule you met in 3.3.

The second is the **Exit Gate**. Every session that produces an artifact exits through named headers, Fixes Applied, Smoke Test, and Next Session Prompt, each a concrete artifact rather than a claim that the work was done. An empty header is a visible failure. The Exit Gate is also where the correction is captured so it loads before the same mistake can happen again, which is the quality loop from 3.4 closing back on itself: this session's record becomes the next session's starting context.

## Walkthrough

Open `sheerline/profile/intake-conversation.md`. Read the hermetic-seal line at the top, then the four question groups. Notice question 2, which asks whether the substrate is the practice's own system or a client's, and question 6, which asks which of the thirteen areas the engagement touches. Now open `sheerline/profile/engagement-intake.yaml` and see that every identifying field is blank in the tracked template, and read the `boundary` block at the bottom: `retained_moat_touched` and `hermetic_seal_confirmed`. Then open `sheerline/os/session-rules.md` and read "The design smoke test" and "The Exit Gate", the render-and-look rule and the three required headers.

## Lab

Dry-run the intake on your own practice's system. Work the intake questions with the substrate set to `self`, and for a design-system audit name which of the thirteen practice areas load in scope.

**Success looks like:** an intake you have filled in your head with a non-identifying label, the substrate set to `self`, and the in-scope area named (for a design-system audit, area 7, Design Systems), plus one sentence stating why the tracked template stays blank, which is the hermetic seal.

## Common misreads

- *"The intake is auto-discovered from the tree."* No. The filled intake is pointed at a path at run time, passed in explicitly; the tracked template stays blank.
- *"The `self` substrate is a placeholder."* No. It is the practice's own system, the real default substrate the whole loop is built and taught on.
- *"Render-and-look is optional polish."* No. It catches the one failure mode automated checks cannot: output that passes every check and still looks wrong.
- *"The Exit Gate is a summary."* No. Each header is a concrete artifact; an empty header is a visible failure, not a formality.

## Self-check

1. What does the intake parameterize, and what loads conditionally as a result?
2. State the hermetic seal and what the `self` substrate is.
3. Why is render-and-look necessary when every automated check has passed?
4. From the Lab: your `self` intake, the in-scope area, and the blank-template reason.

## Go deeper

- `sheerline/profile/intake-conversation.md` and `sheerline/profile/engagement-intake.yaml`: the self-interview and the blank template it fills.
- `sheerline/os/session-rules.md`: the design smoke test and the Exit Gate in full.
- Architecture figure 6, [`../../docs/architecture.md`](../../docs/architecture.md), draws the six-stage session lifecycle from intake to Exit Gate.
- The render-and-look rule is grades-inform-the-human-reads from 3.3; the captured correction that loads next session is 3.4. Extending the system is 4.3.

---

*HeyHi Confidential*
