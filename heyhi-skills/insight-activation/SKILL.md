---
name: insight-activation
description: >-
  Turn a recurring finding — from a Sheerline audit skill's report, an
  self-application harvest, or a research synthesis — into a properly-shaped
  CANDIDATE correction routed to the human-only corrections-intake, classified
  factual vs behavioral, so the next session's Step-0 improvement hook can
  retrieve it once a human has curated it. It is the "learn" verb: the bridge
  that makes findings compound into institutional memory instead of evaporating
  at session end. As of 2026-09-13 it is dual-routed: a correction-shaped finding (a recurring process mistake) becomes a correction candidate, and an insight-shaped finding (a recurring opinion-free observation about a user, domain, or product) becomes an insight (nugget) candidate for the insight registry; both go to the same human-only corrections-intake, promotion the curator's. Triggers: "activate this insight", "turn this finding into a
  correction", "file this as a correction candidate", "this keeps happening —
  capture it", "bridge this finding to the corrections registry", "make this
  finding retrievable next time". Produces a corrections-intake candidate whose
  severity classification and the decide-to-adopt ship EMPTY behind the human
  curator — it proposes and steps back. It NEVER writes the live corrections
  registry, auto-injects a correction into generation, or promotes anything to a
  hard rule. NOT for running an audit (use the area audit skills:
  experiment-readout-linter, design-measurability-mapper,
  strategy-integrity-warden, design-rationale-decision-record). NOT for editing the live
  human-curated corrections registry directly. NOT for HeyHi's own by-hand
  session corrections-intake filing.
version: "0.2.0"
updated: "2026-09-13"
status: "deployed — heyhi-skills/; promoted 2026-08-23 (Sheerline Wave G-1, plans/plan-sheerline-skills-upgrade-2026-08-22.md). Findings→corrections bridge built on the R1 corrections runtime. v0.2.0 (2026-09-13, insight-registry build): dual-routed — Step 2b/5b now also route an insight-shaped finding to the insight registry (plans/plan-sheerline-insight-registry-2026-09-12.md; plans/decision-register-sheerline-insight-registry-2026-09-13.md). Registered in skill-registry.yaml + sheerline/skills/registry/skill-registry.yaml (entry descriptions to sync with the routing battery next pass). Spec: sheerline-skill-buildout-research-2026-08-09.md § 7c use case #11; closes the 2026-08-22 skills audit § 2.5."
classification: HeyHi Confidential
---

# Insight Activation

**Sheerline connective skill · built on the R1 corrections runtime · P2.** The four Sheerline audit skills produce findings — a FLAG in a Readout Integrity Report, an unmeasurable-as-designed flag, a warden's near-miss, a self-application surprise. Today those findings evaporate at session end: the corrections loop cannot turn because areas 9/10/11 hold zero corrections, so every audit skill's Step-0 "retrieve any recurring corrections" is a structural no-op (2026-08-22 audit § 2.5). This skill is the missing bridge. It takes a *recurring* finding and turns it into a **candidate correction** — properly shaped for the corrections registry, classified factual vs behavioral — and routes it to the human-only intake, so that once a human curates it, the next session's improvement hook has something real to retrieve. It is the "learn" verb, and it is the skeptic's own escape hatch: the mechanism by which the audit skills' skepticism compounds instead of resetting.

**The boundary this skill obeys (Sheerline § 9, absolute).** A structured artifact with explicit empty judgment slots, a named human gate, and provenance labels on anything synthetic. *The decide-to-adopt is the empty slot, and the human curator is the named gate.* This skill **proposes and steps back**. It never writes the live corrections registry (that is human-curated — the firewall in `OPERATING_PRINCIPLES.md § Corrections Intake Protocol`), never auto-injects a correction into generation, and never promotes a pattern to a hard rule. The severity classification it assigns (factual / behavioral) is itself a *candidate* the curator confirms. A version of this skill that files straight into the live registry, or promotes on its own, has collapsed the exact boundary it exists to serve. And it honors the corrections lifecycle's tightening: a **behavioral** correction surfaces to the human as a reminder to decide and is **never** auto-injected or promotable — so this skill never flags a behavioral pattern as promotion-eligible. The same boundary holds for an **insight** candidate (the insight-shaped route, Step 2b / Step 5b): it is filed as a proposal only, never written to a live insight registry, never injected into generation, and never enforced — an insight's decide-to-adopt slot is exactly as empty as a correction's, behind the same human curator.

> **This skill closes through the Exit Gate (`CLAUDE-SESSION-RULES.md § Exit Gate`).** See the bottom-of-skill bracket.

---

## Routing — disambiguation with sibling skills

| If the task is… | Use |
|---|---|
| Turning a *recurring* finding into a tracked candidate correction (the learn verb) | **this skill** |
| Running the audit that produces the finding | the area audit skills (`experiment-readout-linter`, `design-measurability-mapper`, `strategy-integrity-warden`, `design-rationale-decision-record`) |
| Editing the live, human-curated corrections registry | a direct human edit — never through a skill (the firewall) |
| HeyHi's own by-hand session intake filing (`corrections-intake/YYYY-MM-DD-*.md`) | done by hand per `corrections-intake/README.md` — this skill systematizes the *design-finding* case of that |
| Deciding whether a candidate becomes a correction, its severity, or promotion | **the human curator** (this skill's named gate) |

The seam with the audit skills is directional: they *find*, this *activates*. An audit skill's Step-0 hook is the *read* side of the corrections loop; this skill is the *write-candidate* side. One retrieves what was learned; this proposes what to learn. Neither decides — the audit skills leave the ship/select slots empty, and this leaves the adopt/promote slots empty.

---

## Step 0: Scope check — is this a recurring pattern, or a one-off?

The corrections registry is for *patterns*, not one-off errors (`corrections-intake/README.md`, `LIFECYCLE.md`). Before activating anything, confirm the finding is a candidate *pattern*: it has recurred across separate tasks/sessions, or it is a structural gap that *will* recur by construction (a method that misfires on a whole class of inputs). A genuinely one-off slip is noted, not activated — filing one-offs floods the intake and degrades the signal. If uncertain, the intake README's own rule applies (write it down anyway; the curator decides) — but say explicitly, in the candidate, that recurrence is unconfirmed.

## Step 1: Load context

1. The **finding(s)** to activate — an audit skill's report (its FLAGs / near-misses / open questions), a self-application harvest, a research synthesis insight, or a plainly-stated recurring observation.
2. `references/corrections-bridge-method.md` — the schema mapping, the factual/behavioral classification rubric, the dedup + promotion-threshold method, and the intake-routing rule. THE method spine.
3. The corrections convention and lifecycle: `sheerline/os/corrections/README.md`, `LIFECYCLE.md`, and `seed-corrections.yaml` (the per-entry schema and the factual/behavioral boundary). Read-only — you register under this convention; you do not author the registry.
4. The **existing corrections**, for dedup: `retrieve_design_corrections` if the design MCP is reachable (read-only), or the seed/live registry. You are checking whether this pattern is already tracked.
5. `corrections-intake/README.md` — the human-only intake route and its file template. This is where the candidate goes.

## Step 2b: Classify — correction-shaped or insight-shaped (the routing fork; runs before the Step 2 mapping)

Before mapping, decide which registry the finding belongs to, using the disambiguator:
- **Correction-shaped** — a recurring *mistake* in agent output or process; the test is *"does this change what the agent does next time?"* Route it through Steps 2–5 (the correction path: filing to `corrections-intake/` for the root / method / design corrections registries).
- **Insight-shaped** — a recurring *observation* about a user, domain, or product; the test is *"does this add to what we know about the user or domain?"* It is descriptive, opinion-free, never a verdict, and never enforced. Route it through the insight path: map to the **insight** schema (below), SKIP Step 3 (an insight has no severity — it is never enforced), and file via **Step 5b**.

If genuinely ambiguous, classify **correction-shaped** only when the finding prescribes a change to agent behavior; otherwise it is an insight. State the classification and the reason in the candidate.

## Step 2: Normalize the finding into its schema (correction OR insight)

**Correction-shaped** — map onto the corrections schema (from `seed-corrections.yaml`): `id · category · severity · status · trigger_context · correction · times_fired · last_fired · origin_date`. Mechanically:
- **`id`** — a kebab-slug naming the pattern (`srm-check-assumes-randomized-assignment`).
- **`category`** — the design/practice taxonomy bucket (token-fidelity, spacing-scale, semantic-role, accessibility, and — for the audit-skill areas — a method/area tag like `experiment-integrity`, `measurability`, `strategy-reasoning`, `decision-hygiene`).
- **`trigger_context`** — *when* the pattern fires, specifically enough that a future session recognizes it.
- **`correction`** — what to do instead, stated as guidance (for behavioral) or a structural rule (for factual).
- `status: active`, `times_fired`, `last_fired`, `origin_date` are the curator's to set on adoption — leave `times_fired: 0` / nulls in the candidate unless dedup (Step 4) found real fires.

**Insight-shaped** — map onto the insight (nugget) schema (`heyhi-mcp/heyhi_mcp/corrections/insight-schema.yaml`): `id · observation · evidence · tags{domain, topic, method_of_origin} · provenance{source_type, pii_redacted, consent_scope, origin_ref} · status`, plus the recommended `confidence{level, reason}` · `scope` · `date` · `owner` · `review_by` · `corroborated_by` · `contradicted_by`. Mechanically:
- **`observation`** — the opinion-free fact; a description, never a verdict (the verdict stays human).
- **`evidence`** — a POINTER to the source (a run id / doc section / transcript line-range), never a copy or summary. A quantitative finding lives here, by its pointer, never atomized into `observation`.
- **`tags`** — `domain` (the subject), `topic` (a Sheerline area id 1-13, the routing lens), `method_of_origin` (fieldwork | audit-finding | synthesis | competitive-research | industry-research). A new tag value is itself a candidate, never agent-added.
- **`provenance`** — stamp `source_type`, `pii_redacted` (was untrusted source content de-identified on ingest?), `consent_scope` (what it is cleared for), and `origin_ref` (which run/session produced it).
- **`confidence`** — a coarse candidate `low | medium | high` + one-line reason; the curator confirms it. An insight carries **no** severity, trigger condition, correction rule, or predicate — it is never enforced.

Every field you fill is a **candidate** value, labeled so. Nothing here is an adopted correction or insight.

## Step 3: Classify severity — factual vs behavioral (the load-bearing call)

**Correction path only — an insight-shaped candidate skips this step entirely** (an insight has no severity; it is never enforced or injected, so there is nothing to gate). For a correction:

Assign a *candidate* severity, with the reasoning, per the rubric in the reference. The two values are exact (`LIFECYCLE.md`):
- **`factual`** — a deterministic, structural fact: a hardcoded hex where a token exists, an off-scale value, a method that mechanically misfires on a whole input class. Factual corrections *can* be injected/enforced and *can* be promoted once they cross the threshold.
- **`behavioral`** — a taste read, a critique tendency, a judgment call (restraint vs incoherence; a warden's ranking temptation). Behavioral corrections **surface to the human as a reminder to decide, are never auto-injected into generation, and are never promotable to an enforced rule.**

State *why* the classification holds. When it is genuinely ambiguous, default to **behavioral** and say so — the cost of mis-classifying a taste call as an enforceable fact (a rule that auto-fires on a judgment) is higher than the reverse. The curator confirms the classification; this skill proposes it.

## Step 4: Dedup and check the promotion threshold (read-only)

- **Dedup against the existing corrections.** If a matching pattern is already tracked, this finding is a **fire-count increment candidate** (propose incrementing `times_fired` and refreshing `last_fired`), not a new entry. Say which existing correction it matches. Within a batch of findings, collapse duplicates to one candidate.
- **Promotion-threshold check (factual only).** The lifecycle promotes at **5+ total fires OR the same pattern across 3+ separate sessions**. If dedup shows a **factual** pattern at or near the threshold, FLAG it as *promotion-eligible* — a candidate for the curator to promote into a hard rule (`os/session-rules.md` / `os/operating-principles.md`) and supersede. **Never flag a behavioral pattern as promotion-eligible** — behavioral patterns are non-promotable by construction; doing so is the boundary collapsing.

## Step 5: Route the candidate to the human-only intake

Write a `corrections-intake/YYYY-MM-DD-<slug>.md` candidate per the intake template (`corrections-intake/README.md`), carrying: what happened, how often (the recurrence/dedup finding), expected behavior, the schema-shaped correction proposal (Step 2), the **candidate severity + reasoning** (Step 3), and any promotion-threshold flag (Step 4). Mark `Status: proposed`. **The file goes to `corrections-intake/` — never to `sheerline/os/corrections/` or the live heyhi-mcp registry.** Then hand off with the decide slot explicitly empty.

```
# [Pattern name] — insight-activation candidate

**Date:** YYYY-MM-DD   **Observed by:** [agent/session]   **Status:** proposed
**Source finding:** [audit report / self-application harvest / research insight — cite it]

## What happened
[the recurring pattern, specific]

## How often (recurrence / dedup)
[recurred across N tasks/sessions, OR structural-will-recur, OR recurrence UNCONFIRMED —
 say which. If it matches an existing correction, name it and propose a fire-count increment.]

## Candidate correction (schema-shaped — a proposal, not an adopted entry)
  id: <kebab-slug>
  category: <taxonomy bucket>
  severity: factual | behavioral   ← CANDIDATE — reasoning below; curator confirms
  trigger_context: <when it fires>
  correction: <what to do instead>
  times_fired: <0, or the dedup count>   last_fired / origin_date: <null / date>

## Severity reasoning
[why factual or behavioral; if ambiguous, defaulted to behavioral and said so]

## Promotion note (factual only)
[promotion-eligible if a factual pattern is at/near 5 fires / 3 sessions — a candidate for the
 curator to promote to a hard rule; OR "not at threshold"; OR "behavioral — non-promotable".]

## ⛔ Decide-to-adopt — NEEDS THE HUMAN CURATOR
This is intentionally empty. Whether this enters the registry, its confirmed severity, and any
promotion are the curator's calls. This skill proposed a candidate and stepped back.
   Curator decision (adopt / adjust severity / reject / promote): ____________________
```

## Step 5b: Route an insight candidate to the human-only intake

Mirror Step 5, filing to the SAME human-only intake with an **`insight-` filename prefix** so the curator tells the two apart at a glance: `corrections-intake/YYYY-MM-DD-insight-<slug>.md`. **The file goes to `corrections-intake/` — never to a live insight registry (`design-insights.yaml` / `practice-insights.yaml`), never to `sheerline/os/insights/`.** Carry the insight-schema mapping (Step 2), the `confidence` candidate, and the recurrence/dedup finding; then hand off with the decide slot empty. There is no severity line (an insight has none) and no promotion-eligible flag (an insight is retrieval-only — it never hardens into an enforced rule).

```
# [Observation name] — insight-activation candidate (INSIGHT)

**Date:** YYYY-MM-DD   **Observed by:** [agent/session]   **Status:** proposed
**Source finding:** [audit report / self-application harvest / research synthesis — cite it]

## What was observed
[the recurring, opinion-free observation — a fact, not a verdict]

## How often (recurrence / dedup)
[recurred across N runs, OR structural-will-recur, OR recurrence UNCONFIRMED — say which.
 If it matches an existing nugget, name it and propose corroborated_by / contradicted_by.]

## Candidate nugget (schema-shaped — a proposal, not an adopted entry)
  id: <kebab-slug naming the observation>
  observation: <opinion-free fact>
  evidence: <POINTER — run id / doc section / transcript range; never a copy>
  tags: { domain: <subject>, topic: <1-13>, method_of_origin: <fieldwork|audit-finding|synthesis|competitive-research|industry-research> }
  provenance: { source_type: <...>, pii_redacted: <bool>, consent_scope: <...>, origin_ref: <run/session> }
  confidence: { level: low|medium|high, reason: <one line> }   ← CANDIDATE — curator confirms
  scope: <population/context the observation held for>   status: active

## ⛔ Decide-to-adopt — NEEDS THE HUMAN CURATOR
Intentionally empty. Whether this enters an insight registry, its confidence, and its
tags are the curator's calls. This skill proposed a candidate and stepped back.
   Curator decision (adopt / adjust tags / reject): ____________________
```

## Step 6: Pre-flight verification

Confirm: the candidate went to `corrections-intake/` and NOT the live registry; the decide-to-adopt slot is empty; every filled schema field is labeled a candidate; the severity carries reasoning and ambiguous cases defaulted to behavioral; any behavioral candidate is NOT flagged promotion-eligible; a one-off (not a pattern) was noted rather than filed, or its recurrence is explicitly marked unconfirmed; nothing was auto-injected or auto-promoted.

---

## What is explicitly out of scope

- **Writing the live corrections registry, auto-injecting, or promoting.** Empty by construction (§ 9 + the firewall). This skill only ever produces a `corrections-intake/` candidate; the curator decides everything downstream.
- **Running the audit.** This skill activates a finding that already exists; it does not produce the finding. Producing it is the area audit skills' job.
- **Filing one-offs.** A single non-recurring slip is noted, not activated — the registry is for patterns.
- **Deciding a behavioral pattern is enforceable.** Behavioral corrections never auto-inject and never promote; this skill honors that and never proposes otherwise.

---

## Exit Gate Required Headers (bottom-of-skill bracket)

This skill closes through Exit Gate Flavor A (`CLAUDE-SESSION-RULES.md § Exit Gate`). Before declaring done, confirm every required header holds real content:

- `## Fixes Applied` (the corrections-intake candidate(s) produced, with paths)
- `## Smoke Test` (the Step 6 pre-flight checks, pasted)
- `## Next Session Prompt` (what the curator still needs to decide)

If any candidate landed in the live registry, if the decide-to-adopt slot is filled, or if a behavioral pattern was flagged promotion-eligible, the gate has **not** been satisfied.

---

*HeyHi Confidential. Sheerline Wave G-1 (findings→corrections bridge), the highest-value in-Sheerline research capability per `sheerline-skill-buildout-research-2026-08-09.md` § 7c / § 8. Built on the R1 corrections runtime (`heyhi-mcp/heyhi_mcp/corrections/`), not as a research tool. Closes the 2026-08-22 skills audit § 2.5 (the corrections loop cannot turn). Boundary: § 9.*
