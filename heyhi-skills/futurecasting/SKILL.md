---
name: futurecasting
description: "Runs a strategic foresight or futurecasting engagement. Use for futurecasting sessions, preferred future design, divergent scenario mapping, organizational signal reading, pre-mortems, Working Canvas or Decision Register creation, The Letter exercise, horizon scanning, field reading, weak signal detection, or applying HeyHi's seven generative tools to an organizational context. Also trigger when the user asks where their team or org is headed, wants to stress-test a decision, or needs to understand the gap between current trajectory and preferred future. Produces named artifacts: Working Canvas, Decision Register, Preferred Future Map, Divergent Futures Summary, Signal Map. Works for client engagements, internal HeyHi strategy, workshop design, thought leadership, or anywhere strategic direction needs to be designed rather than drifted into. NOT for facilitating a full client workshop session with pre-session materials, facilitation support, timing guides, and post-session conversion (use heyhi-workshop, which delegates generative workshops back to this skill for the strategic content). NOT for diagnostic workshops like Human-in-the-Loop, Anti-Slop, Adaptive Organizations, Craft at Scale, or Living Systems (use heyhi-workshop)."
---

# Futurecasting: Practitioner Skill

A full strategic foresight engagement from start to artifact. The methodology is generative — it helps organizations design toward futures rather than drift into them. The output is always actionable: not "here's what might happen" but "here are the decisions your team needs to make, and here's who needs to make them."

Use HeyHi language throughout. Never name the methodology frameworks to clients. Participants don't need to know the method has a name. They just need to do the work.

See [references/methodology.md](references/methodology.md) for full tool details and key questions.
See [references/predictive-layer.md](references/predictive-layer.md) for how to activate predictive intelligence in each phase.

---

> **Exit Gate (Flavor B).** This skill closes through the canonical Exit Gate — see `CLAUDE-SESSION-RULES.md § Exit Gate`. Required headers, in order: `## Findings Integration`, `## Session Integrity`, `## Fixes Applied`, `## Smoke Test`, `## Next Session Prompt`. Empty headers are visible failures.


## Step 0: Qualification Gate

Before running any exercise, route correctly.

Ask: **Is the primary goal generative (designing toward a future) or diagnostic (naming what went wrong)?**

- **Generative** → continue to Step 1.
- **Diagnostic** (naming burnout, broken trust, skill erosion, accountability gaps) → route to the `heyhi-workshop` skill, which owns diagnostic workshop delivery (Human-in-the-Loop, Anti-Slop, Adaptive Organizations, Craft at Scale, Living Systems, Signal Readers) — matching this skill's own frontmatter. [references/diagnostic-workshops.md](references/diagnostic-workshops.md) remains available as methodology background; it is not the delivery route (curriculum-home consolidation is a deferred decision, audit M5).
- **Mixed** → run a generative session, but open with the Signal Readers workshop to name what's already off before designing forward.
- **Unclear** → ask: "Is the team trying to figure out what they want, or trying to name what's already wrong?" Use the answer to route.

---

## Step 1: User Gates

Ask these in sequence. Do not skip or assume. Each answer shapes what comes next.

**Gate 1 — Client context:**
> "Who is this for? Tell me about the organization: what they do, how large they are, and what's happening for them right now."

Capture:
- Organization name/type, industry, approximate size
- Current inflection point: pre-decision, strategic crossroads, leadership transition, sensing drift, post-diagnostic work

After capturing context: **activate the Predictive Layer (Step 1a)** before proceeding to Gate 2.

**Gate 2 — Situation type:**
> "What's the situation that's bringing them here? Are they about to make a big decision and want to think it through first? Do they sense something is changing and don't know what to do about it? Have they just done diagnostic work and they're ready to design toward something better?"

Use the answer to recommend a tool (see Tool Selection below), or confirm the user's preferred tool.

**Gate 3 — Time available:**
> "How much time is there for this work?"
- Async/single session with Claude → generate the artifact collaboratively; full interactive mode
- Half-day → one primary tool, one artifact
- Full-day → one or two tools, full artifact set
- Multi-session → map the arc across sessions, connect each session's output to the next

**Gate 4 — Tool selection:**
Based on Gates 2 and 3, recommend the best tool from the seven. Present the recommendation with one sentence of rationale and confirm before proceeding.

---

## Step 1a: Predictive Layer — Context Intelligence

After Gate 1, before selecting a tool, activate the predictive intelligence layer. Read [references/predictive-layer.md](references/predictive-layer.md) for the full protocol. Summary:

1. **Signal Pre-Assessment** — Based on the organizational context provided, make an initial read on which of the four signal categories (Meaning Erosion, Skill Atrophy, Trust Collapse, Accountability Void) may be present. Surface this to the practitioner as a hypothesis, not a diagnosis. Ask a clarifying question to test each category you flag.

2. **Horizon Scan** (if web search is available) — For the organization's industry and stated inflection point, run a targeted external scan. Surface 2–3 relevant forces from outside the organization that may be shaping the context. Present these as Field Reading inputs before the session begins.

3. **Trajectory Modeling** — Based on the situation type (Gate 2 answer), sketch the probable current trajectory in one sentence. Ask the user to confirm or correct it. This becomes the "current trajectory" input for the Working Canvas.

4. **Scenario Seed** — For Divergent Futures work, pre-generate the 2–3 driving forces most likely to determine which future arrives, based on the organizational context. Present as a starting framework for the session.

---

## Step 2: Tool Selection

Match situation to tool using HeyHi language only:

| Situation | Recommended Tool | HeyHi Name |
|---|---|---|
| Team stuck in problem mode, needs direction | Backcasting | The Preferred Future method |
| Something feels off, can't name it yet | Signals mapping | Organizational early warning |
| Choosing between paths before a major decision | Scenario planning | Divergent futures mapping |
| About to build something; want to stress-test it | Pre-mortem | Before You Build analysis |
| Team needs to articulate a vivid preferred future | Letter exercise | The Letter |
| Capturing the full picture in one working artifact | Canvas | The Working Canvas |
| What's coming from outside that will matter inside | Horizon scanning | Field reading |

For the full facilitation sequence per tool, see [references/methodology.md](references/methodology.md).

---

## Step 3: Run the Exercise

Use only HeyHi language throughout. Never name the methodology.

1. **Set the frame.** Tell the participant what you're doing and why, in plain language.
2. **Ask the tool's key questions** from [references/methodology.md](references/methodology.md) in sequence.
3. **Build the artifact collaboratively.** Push for specificity — not abstract ("we work meaningfully") but concrete ("what does your team do on a Tuesday, specifically?").
4. **Read it back.** When the artifact is substantially complete: "Does this accurately reflect where you are, where you're headed, and where you want to be?"
5. **Note gaps and tensions.** These become the Decision Register entries.

### Predictive layer: mid-exercise

During the exercise, activate the predictive layer at three points:

- **After current state is established:** Use the Signal Severity Protocol (see [references/predictive-layer.md](references/predictive-layer.md)) to score which signal categories are present and how urgent.
- **After preferred future is articulated:** Generate a counter-scenario — the most plausible way this preferred future doesn't arrive. Surface it as a question, not a warning: "What would need to be true about [force] for this future to become harder to reach?"
- **Before artifact is finalized:** Run a rapid pre-mortem on the gap between current trajectory and preferred future. "If we're looking back from three years from now and the gap closed — what made the difference? And what would have prevented it?"

---

## Step 4: Generate the Artifact

Save completed artifacts to the instance's engagement folder for this client: `<engagement folder>/deliverables/`

Create the folder if it doesn't exist. Artifacts are saved relative to the current working directory.

**Naming convention:**
- Working Canvas → `working-canvas-[client]-[YYYY-MM-DD].md`
- Decision Register → `decision-register-[client]-[YYYY-MM-DD].md`
- Preferred Future Map → `preferred-future-map-[client]-[YYYY-MM-DD].md`
- Divergent Futures Summary → `divergent-futures-[client]-[YYYY-MM-DD].md`
- Signal Map → `signal-map-[client]-[YYYY-MM-DD].md`

For all artifact templates, see [references/voice-and-artifacts.md](references/voice-and-artifacts.md).

---

## Dependency Map: Tools → Artifacts → Deliverable Layer

The dependency map shows the full chain from situation type through tool selection to produced artifact, and how each artifact feeds into or closes the engagement.

```
SITUATION                   TOOL                        ARTIFACT                 DELIVERABLE LAYER
─────────────────────────   ─────────────────────────   ──────────────────────   ──────────────────────────────────────────────
Something feels off    ──→  Organizational Early    ──→  Signal Map           ──→  Feeds into Working Canvas (current signals)
                             Warning                                                 Quarterly living document / retainer anchor

External forces scan   ──→  Field Reading           ──→  Signal Map           ──→  Feeds into Working Canvas (current signals,
                                                          (external section)         external layer)

Need direction         ──→  The Preferred Future    ──→  Preferred Future     ──→  Feeds into Working Canvas (preferred future
  + The Letter as             Method                       Map                        + gap sections)
    anchor exercise

Multiple paths         ──→  Divergent Futures       ──→  Divergent Futures    ──→  Feeds into Decision Register
                             Mapping                       Summary                   (scenario-contingent decisions)

Pre-build stress-test  ──→  Before You Build        ──→  Decision Register    ──→  Terminal artifact; closes to named owners,
                             Analysis                                                dates, and reversibility checkpoints

Full strategic picture ──→  The Working Canvas      ──→  Working Canvas       ──→  Terminal artifact for Consult engagements;
  (all inputs collected)                                  + Decision Register        revisited quarterly; anchors next session
```

**How artifacts connect to each other:**

```
Signal Map (internal)  ─┐
                         ├──→  Working Canvas (current signals)
Signal Map (external)  ─┘             │
                                       ├──→  Working Canvas (complete)  ──→  Decision Register
Preferred Future Map   ──→  Working Canvas (preferred future + gap)
                                       │
Divergent Futures      ──→  Decision Register (scenario-contingent decisions)
Summary
```

**What each terminal artifact closes:**

| Terminal artifact | Closes when | What it produces for the client |
|---|---|---|
| Signal Map | Signals are identified, scored, and a Keeper is named | Organizational early warning capability; quarterly monitoring instrument |
| Decision Register | Every key decision has a name, an owner, and a date | Accountability structure for the preferred future |
| Working Canvas | Current signals, trajectory, preferred future, gap, and key decisions are all agreed | Strategic direction document; input for next engagement session |

**Engagement completeness check:** A full engagement produces a Working Canvas and a Decision Register. The Working Canvas captures where the organization is going and why. The Decision Register captures who is accountable for getting it there and by when. Neither alone is complete.

---

## Step 5: Close Protocol

Every engagement ends with three questions:

1. **"What did we build today that we didn't have before?"** (Not what we learned. What we built: the Letter, the Map, the Canvas, the Register.)
2. **"What decision is now yours?"** A specific decision. Named. With a date.
3. **"What signal will tell you, in three months, whether you're on the right track?"** The early indicator of progress — not the outcome, the signal.

---

## Voice

- HeyHi language only. See full translation guide in [references/voice-and-artifacts.md](references/voice-and-artifacts.md).
- Warm, direct, specific. Not academic. Not corporate.
- Push for specificity. "In practice" over "in theory."
- Name the gap without catastrophizing. "This is the work" — not "you've been doing it wrong."
- Never use "AI" as a standalone word. Describe what the system does.

---

## Reference Index

| File | Read when |
|---|---|
| [references/methodology.md](references/methodology.md) | Running any tool — key questions, facilitation notes, the seven tools in depth |
| [references/signal-categories.md](references/signal-categories.md) | Assessing organizational signals, building a Signal Map |
| [references/predictive-layer.md](references/predictive-layer.md) | Activating intelligence layer: horizon scans, signal scoring, probabilistic scenarios |
| [references/workshop-facilitation.md](references/workshop-facilitation.md) | Running full workshops (The Preferred Future, Before You Build, Signal Readers) |
| [references/diagnostic-workshops.md](references/diagnostic-workshops.md) | Running diagnostic workshops when the situation is primarily naming what went wrong |
| [references/research-foundations.md](references/research-foundations.md) | Background on the methodological underpinning — use for thought leadership, talks, or when a client asks about the research basis |
| [references/voice-and-artifacts.md](references/voice-and-artifacts.md) | HeyHi voice standards, translation guide, all artifact templates |

---

## Exit Gate Required Headers (bottom-of-skill bracket)

This skill closes through the Exit Gate Flavor B (`CLAUDE-SESSION-RULES.md § Exit Gate`). Before declaring done, confirm every required header below contains real content, not a claim:

- `## Findings Integration`
- `## Session Integrity`
- `## Fixes Applied`
- `## Smoke Test`
- `## Next Session Prompt`

If any header is empty or contains advisory prose ("I checked for bugs") instead of a concrete artifact, the gate has not been satisfied. Apply fixes until clean — then emit.

*HeyHi Confidential*
