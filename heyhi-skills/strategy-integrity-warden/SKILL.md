---
name: strategy-integrity-warden
description: >-
  Audit an opportunity, JTBD, or prioritization artifact for reasoning
  integrity — before the team commits to it. Runs the mechanical checks: restate
  the Opportunity Solution Tree or JTBD in its canonical shape so gaps show,
  check the tree's top node is a team-influenceable product outcome (not a
  lagging business metric), enforce evidence-linkage-or-assumption-flag on every
  node, detect solutions dressed as opportunities, flag stale evidence, and
  detect back-solved RICE / prioritization scores. Triggers: "audit this
  opportunity tree", "is this JTBD sound", "check the reasoning on this
  prioritization", "did we back-solve these scores", "stress-test this strategy
  artifact", "opportunity integrity check". Produces a Reasoning Integrity
  Report; which opportunity to pursue and what to build ship EMPTY behind a named
  human gate. It is a WARDEN: it audits the reasoning, it never picks the
  opportunity or renders the strategy verdict. NOT for org foresight,
  preferred-future, or scenario work (use futurecasting). NOT for building a
  Goals→Signals→Metrics measurability map (use design-measurability-mapper). NOT
  for auditing an experiment readout (use experiment-readout-linter).
version: "0.2.0"
updated: "2026-08-23"
status: "deployed — heyhi-skills/; v0.2.0 promoted 2026-08-23 (Gate G-C, plans/plan-sheerline-skills-upgrade-2026-08-22.md) — adds check 6 outcome-quality (structural, no re-rank), a staleness heuristic band, open-questions + near-misses surfaces, a worked example, 2 eval cases (5→7). v0.1.0 promoted 2026-08-15 (DISPATCH-D). Sheerline area 9 (Design Strategy), P1.5. Registered in skill-registry.yaml v2.35.0."
classification: HeyHi Confidential
---

# Strategy Integrity Warden

**Sheerline area 9 (Design Strategy & Product Thinking) · P1.5 · pure validate/audit skill.** A team brings an opportunity solution tree, a JTBD map, or a RICE-scored prioritization sheet and wants to commit. This skill is the warden at the gate: it checks the *reasoning* — is the tree rooted in an outcome the team can actually influence, is every opportunity evidence-linked or honestly flagged as an assumption, is anything here a solution wearing an opportunity's clothes, is the evidence still current, were the scores back-solved to justify a foregone conclusion. It restructures the artifact so the gaps are visible and hands the *which-opportunity* and *what-to-build* calls back to the humans. It is warden-shaped by design: it guards the integrity of the thinking; it does not do the thinking.

**The boundary this skill obeys (Sheerline § 9, absolute).** A structured artifact with explicit empty judgment slots, a named human gate, and provenance labels on anything synthetic. *Which opportunity to pursue and what to build are the empty slots.* Auditing the reasoning is mechanical; choosing the opportunity is the team's strategy call. **Keep it warden-shaped: the moment it ranks the opportunities or names the one to pursue, it has stopped being a warden and started being the strategist — the exact overreach this skill is specified against.** The new outcome-quality check (v0.2.0) is a *structural type-check on the top node*, not an opportunity ranking and not a rewrite of the outcome: it can say "this top node is a lagging business metric, not a product outcome the team can move," and it must stop there — it never supplies the "right" outcome. Grades never gates; mechanics never taste.

> **This skill closes through the Exit Gate (`CLAUDE-SESSION-RULES.md § Exit Gate`).** See the bottom-of-skill bracket.

---

## Routing — disambiguation with sibling skills

| If the task is… | Use |
|---|---|
| Audit an opportunity / JTBD / prioritization artifact's *reasoning integrity* | **this skill** |
| Generate org foresight, a preferred future, scenarios, or a Decision Register | `futurecasting` |
| Build a Goals→Signals→Metrics measurability map for a goal | `design-measurability-mapper` |
| Audit a completed A/B / experiment readout | `experiment-readout-linter` |
| Choose the opportunity, or decide what to build | **the human** (this skill's named gate) |

The reciprocal with `futurecasting` is directional: futurecasting *generates* strategy (org-level foresight, the Decision Register); this warden *audits* a product-opportunity artifact's reasoning. One makes the map, the other checks the map holds — and neither picks the destination.

---

## Step 0: Improvement hook check

Retrieve any recurring corrections for strategy / opportunity work (`retrieve_design_corrections` or the Sheerline `os/corrections/` registry). Fold a match in. Skip silently if none.

## Step 1: Load context

1. The **artifact under audit** — the opportunity solution tree, JTBD map, or prioritization sheet the team brought.
2. `references/reasoning-integrity-checks.md` — the OST/JTBD canon with its 2026 failure modes, the outcome-quality (top-node influenceability) test, the evidence-linkage rule, the solution-in-disguise test, the staleness rule and its heuristic band, and the back-solved-score detector. THE method spine.
3. `references/worked-example.md` — a filled Reasoning Integrity Report on synthetic input. Read it to calibrate register and depth on the free-prose slots (open questions, near-misses, the restatement); do not copy its findings.
4. The Sheerline area-9 governed context (`sheerline/os/foundations/registry.yaml` area-design-strategy; foundation deferred to P3, manifest-grade foundation under consideration in Wave G). Register under it; do not author it.

## Step 2: Run the integrity checks

Each check is a mechanical audit of the reasoning. None ranks or selects an opportunity, and none authors a replacement outcome or node.

1. **Canonical restatement.** Restate the artifact in its proper shape — an OST as outcome → opportunities → solutions → experiments; a JTBD as job → forces / desired outcomes; a prioritization as the scored factors laid bare. Restructuring makes the gaps visible (a starved tree, a job with no outcome, a factor with no basis). Any node the warden infers or reshapes is labeled `[agent-restructured — verify]` (provenance).
2. **Evidence-linkage-or-assumption-flag.** Every opportunity/need node must either link to evidence (research, data, a cited signal) **or** be flagged an assumption. An unlinked node presented as fact is the finding. (The dominant 2026 OST failure is a *starved* tree — opportunities with no research under them — not a mis-drawn one; this check is aimed there.)
3. **Solutions-dressed-as-opportunities.** Detect nodes in the opportunity space that are really pre-baked solutions. "Add a dashboard" is a solution; the opportunity is the unmet need it claims to serve. A tree full of solutions-as-opportunities has skipped the problem space entirely — flag each.
4. **Evidence staleness.** Flag cited evidence that is old enough to be suspect, references a since-changed product, or leans on a source the team no longer trusts. Use the **staleness heuristic band** in the reference — which leads with *what changed*, not calendar age (a 3-month-old finding about a rebuilt flow is stale; a 3-year-old finding about a stable human behavior may not be). It is a flag-not-gate band: it says "verify this still holds," it never blocks.
5. **Back-solved scores.** In a RICE (or similar) sheet, detect scores that appear reverse-engineered to produce a predetermined ranking — suspiciously round numbers, confidence set to justify a favorite, effort shaved on the pet project. RICE is a *read-and-challenge* instrument, never a truth oracle; back-solved scores are its defining anti-pattern.
6. **Outcome-quality (top-node influenceability).** Examined at the tree's root, alongside the canonical restatement (numbered 6 to keep checks 1–5 stable). Is the top node a **team-influenceable product outcome** (a user behavior the team's work can move — activation, adoption, task completion, frequency), or a **lagging business/financial metric** (revenue, ARR, churn dollars, LTV) the team cannot run discovery against, or an **output/solution masquerading as an outcome** ("ship the redesign")? PASS a genuine product outcome; FLAG a lagging business metric or an output-as-outcome, and state *why* it breaks the tree (a team cannot run opportunity discovery against a number it does not control; the whole tree beneath a lagging metric inherits the confusion). **Structural, never a re-rank and never a rewrite:** name the type-mismatch and stop — do not supply the "correct" product outcome (that is the team's articulation work, exactly as with solutions-dressed-as-opportunities). This is the standard Torres business-vs-product-outcome critique, made structurally checkable.

## Step 3: Produce the Reasoning Integrity Report

Output this exact structure. The selection slots stay empty by construction; the open-questions and near-misses surfaces carry questions and traces, never a ranking or a recommendation.

```
# Reasoning Integrity Report — [artifact name]
Source: [artifact]        Audited: [date]        Type: OST / JTBD / prioritization

## Canonical restatement
[the artifact in its proper shape; inferred/reshaped nodes tagged [agent-restructured — verify]]

## Integrity checks (check 1 is the Canonical restatement section above)
| # | Check | Verdict | What triggered it (node-specific) |
|---|-------|---------|-----------------------------------|
| 6 | Outcome-quality (top-node influenceable) | PASS / FLAG | root is "increase revenue" — a lagging business metric, not a product outcome |
| 2 | Evidence-linkage / assumption-flag | PASS / FLAG | "opportunity: users want X" — no evidence linked |
| 3 | Solutions-dressed-as-opportunities | PASS / FLAG | "add a dashboard" sits in the opportunity space |
| 4 | Evidence staleness                 | PASS / FLAG | cites a 2024 study of a since-rebuilt flow |
| 5 | Back-solved scores                 | PASS / FLAG | confidence = 100% on the sponsor's favorite |

## Open questions for the team (questions, not judgments)
[What the artifact does not resolve and what you would ask its authors. Each is a question
 that, answered, would firm up the reasoning. No ranking, no recommendation.]
- [e.g. "The top outcome is 'increase revenue' — is there a product outcome your team owns
   that ladders up to it, that the tree could be rooted in instead?"]
- [e.g. "Opportunity 2 cites a Q1-2024 study — is the flow it studied still the current one?"]

## Near-misses and unchecked territory (the audit journey, made inspectable)
[Nodes considered and passed, checks that almost fired, what could not be verified. Traces,
 no verdicts, no ranking.]
- Considered, did not flag: [e.g. "'improve reliability' read like a solution at first;
   it is a genuine unmet-need opportunity — no FLAG."]
- Almost flagged: [e.g. "opportunity 3's evidence is 20 months old, but it is about a
   navigation habit the product hasn't changed — noted under staleness, held at PASS."]
- Could not check: [e.g. "the two evidence links point to an internal research repo not in
   the artifact — linkage present but the content is unverified from here."]

## ⛔ Which opportunity to pursue — NEEDS HUMAN
This slot is intentionally empty. Ranking and selecting the opportunity is the team's
strategy call. The warden guards the reasoning; it does not choose.
   Selected opportunity: ____________________

## ⛔ What to build — NEEDS HUMAN
   Decision: ____________________

## Named gate
Sign-off owner (product / design lead): ____________________   Date: ______
No opportunity is selected until a human signs.
```

**Done when:** the top node carries an outcome-quality verdict, every node carries an evidence-linkage verdict, every FLAG cites a specific node, restructured nodes are tagged, the open-questions and near-misses surfaces carry questions/traces (no ranking), and the two selection slots are still blank. A report that ranks the opportunities — even "informally," and even inside an open question — has broken warden shape.

## Step 4: Pre-flight verification

Confirm: the which-opportunity and what-to-build slots are empty; the report contains no ranking, score, or recommendation of *which* opportunity to pursue; every FLAG is node-specific (not a generic "add more evidence"); every inferred/reshaped node is tagged `[agent-restructured — verify]`; the skill has not itself authored a new opportunity. New in v0.2.0: confirm the outcome-quality check named the top-node *type-mismatch* without supplying a replacement outcome; confirm the staleness verdicts led with *what changed* rather than calendar age alone; confirm every open question is a question (no smuggled ranking — "isn't opportunity 2 the strongest?" is a ranking in a question's clothes and is out) and every near-miss is a trace.

---

## What is explicitly out of scope

- **Selecting or ranking the opportunity; deciding what to build.** Empty by construction (§ 9). The warden audits; it never picks. This is the line the skill is specified against — hold it, including inside the open-questions surface.
- **Authoring the "correct" outcome or opportunity.** The outcome-quality check flags a top-node type-mismatch; it does not write the product outcome that should replace it. Naming the replacement is the team's articulation work (same discipline as solutions-dressed-as-opportunities).
- **Generating strategy.** The warden does not add opportunities, write the JTBD, or propose solutions. It checks what the team brought. Generating org-level foresight is `futurecasting`.
- **Building the measurability map** — `design-measurability-mapper`. **Auditing an experiment readout** — `experiment-readout-linter`.

---

## Exit Gate Required Headers (bottom-of-skill bracket)

This skill closes through Exit Gate Flavor A (`CLAUDE-SESSION-RULES.md § Exit Gate`). Before declaring done, confirm every required header holds real content:

- `## Fixes Applied` (or the delivered Reasoning Integrity Report)
- `## Smoke Test` (the Step 4 pre-flight checks, pasted)
- `## Next Session Prompt`

If the report ranks or selects an opportunity, fills the what-to-build slot, or supplies a replacement outcome for the outcome-quality flag, the gate has **not** been satisfied — warden shape is broken.

---

*HeyHi Confidential. Sheerline area 9 (Design Strategy & Product Thinking), P1.5 net-new. v0.1.0 deployed 2026-08-15 (DISPATCH-D); registered in `skill-registry.yaml` v2.32.0. v0.2.0 staged 2026-08-23 (Wave D, `plans/plan-sheerline-skills-upgrade-2026-08-22.md`). Spec source: `ai-services/design-intelligence/research/sheerline-skill-buildout-research-2026-08-09.md` § 6.1 / § 8; outcome-quality, staleness band, and curiosity surfaces from the 2026-08-22 skills audit § 2.4 / § 5. Boundary: § 9. Kept warden-shaped per the dispatch's standing constraint.*
