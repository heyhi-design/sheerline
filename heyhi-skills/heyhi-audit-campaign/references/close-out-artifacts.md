---
classification: internal
title: Close-Out Artifacts
purpose: Wrapper for the close-stage artifacts of an audit campaign — the synthesis brief and the fix specification. Points at the synthesis-brief structure (canonical in heyhi-voice) and adds the fix-specification template. Loaded by heyhi-audit-campaign at Step 5 (Close stage).
created: 2026-05-21
loaded_by: heyhi-audit-campaign
canonical_sources:
  - heyhi-skills/heyhi-voice/references/synthesis-brief-structure.md (synthesis-brief three-level structure)
  - ai-services/_core/service-readiness-brief-2026-05-21.md (synthesis brief worked example)
  - ai-services/_core/integrity-mechanism-fix-spec-2026-05-21.md (fix specification worked example)
---

# Close-Out Artifacts

The campaign's close-stage outputs. Two artifact types: the **synthesis brief** (every campaign produces one) and the **fix specification** (some campaigns produce one).

This reference is a wrapper. The synthesis brief's structure is canonical in [heyhi-skills/heyhi-voice/references/synthesis-brief-structure.md](../../heyhi-voice/references/synthesis-brief-structure.md) — do not duplicate it here. Load that file at Step 5. The fix specification template lives here in §3 below because the audit-campaign domain is its only known consumer.

---

## 1. When each artifact is produced

**Synthesis brief — always.** Every campaign produces one. The brief is the campaign's central deliverable: one document a reader can open to see where things stand on the campaign's subject, today.

**Fix specification — conditionally.** Produced when the audit surfaced a structural failure pattern that a per-finding follow-on cannot repair. The conditions:

- A pattern recurs across multiple areas in the audit (not just one).
- The pattern points to a structural mechanism — a tool, a skill, a rule, a schema — not a per-area gap.
- A repair beyond per-finding follow-ons is needed; the fix changes the mechanism, not a single file.

The ai-services campaign produced one because the audit surfaced the synthesis-vs-bucket drift archetype across multiple buckets, and the repair was a four-part structural change to `state-sync.py` + `heyhi-session-integrity` + `corrections-registry.yaml` + `CLAUDE-SESSION-RULES.md`. If a campaign surfaces only per-area gaps, the brief alone is the close.

---

## 2. Synthesis brief

**Structure source:** [heyhi-skills/heyhi-voice/references/synthesis-brief-structure.md](../../heyhi-voice/references/synthesis-brief-structure.md).

**Three-level structure (canonical):**

1. **Headline.** One paragraph or one short table that fits on one screen. Lead with the number, the verdict, or the named state. Decompose into 3–6 supporting bullets.
2. **Per-layer detail.** Tables grouped by the natural categories of the subject. Same column shape across sections. For capability audits: Consult / Build / Sustain / Products / Workshops. For design system audits at scale: tokens / components / documentation / governance / Figma.
3. **Cited evidence.** Every claim in levels 1 and 2 grounded in a ledger row, finding ID, or downstream surface. Inline short codes (`area_id`, `DF-N`, `PL-N`) and file-path citations.

**Closing section.** A "What 'today' means" or "Carry-forward" block that names what is dated about the snapshot, what produced it, and what the next brief should re-verify.

**Worked example:** [ai-services/_core/service-readiness-brief-2026-05-21.md](../../../ai-services/_core/service-readiness-brief-2026-05-21.md).

**Anti-patterns to reject** (per the synthesis-brief reference):

- The narrative campaign retrospective. The reader of a synthesis brief needs the state, not the story.
- The methodology-first explainer. The methodology earns its place at the bottom, not the top.

---

## 3. Fix specification

The fix spec is a four-part structural fix proposal. The canonical worked example is [ai-services/_core/integrity-mechanism-fix-spec-2026-05-21.md](../../../ai-services/_core/integrity-mechanism-fix-spec-2026-05-21.md). Verified against that file's actual structure.

### Skeleton

```
Frontmatter
1. The hypotheses (or finding clusters) the campaign confirmed
2. The N-part structural fix
   - Part A
   - Part B
   - Part C (etc.)
3. Implementation order and ownership
4. What this fix is not (negative space)
5. Carry-forward
```

### Frontmatter

```yaml
---
classification: internal
created: YYYY-MM-DD
status: ready-to-work
campaign: <path to the campaign plan>
session: <N of N>
supersedes: <null or path to predecessor fix spec>
linear_issues: []
---
```

### Section 1: The hypotheses (or finding clusters) the campaign confirmed

When the campaign opened with named hypotheses (the ai-services campaign opened with seven), Section 1 is a table re-verifying each. Each row carries:

| ID | Hypothesis | Initial verdict | New evidence | Final verdict |
|----|------------|-----------------|--------------|---------------|

When the campaign opened without named hypotheses (more common for first-time campaigns), Section 1 instead enumerates the cross-bucket finding clusters. Same evidence discipline; the units are clusters, not hypotheses.

The section closes with a headline statement: which hypotheses or clusters are load-bearing for the fix, which are confirmed but secondary.

### Section 2: The N-part structural fix

The fix is broken into N independent-but-coordinated parts. Each part follows the same five-field shape:

```
### Part <letter>. <Part name>

**Closes:** <which hypotheses or finding clusters this part addresses>

**What it does.** <One paragraph: the concrete change>

**Where it lives.** <File paths; specific sections>

**Why it works.** <One paragraph: the mechanism>

**How it gets verified.** <The smoke test or unit tests that confirm the part works>

**Scope discipline.** <What this part deliberately does not do>
```

The "how it gets verified" field is non-optional and must name a runnable test, not a claim that the part is correct. Per Q3 (verify-before-claim).

The "scope discipline" field is the part's negative space — what the part does not claim to do. Without this field, parts drift toward over-promising.

**How many parts?** Aim for 3–5. Fewer is rare; the structural problems audits surface usually have multiple coupled surfaces (tooling change, skill change, rule change, data change). More than 5 suggests the fix is actually two fixes; consider splitting into two specs.

### Section 3: Implementation order and ownership

A table mapping each part to:

| Part | Owner | Lands in | Status after this session |
|------|-------|----------|---------------------------|

Common owner patterns:

- **Owner-reviewed skill edit.** Lands in a skill SKILL.md. Requires the instance owner's review before merge.
- **Direct edit, isolated.** Lands in a script, a test file, a state file. Small enough to ship in the close-stage session.
- **Direct edit, doc + data.** Lands in a rule file (`CLAUDE-SESSION-RULES.md`, `OPERATING_PRINCIPLES.md`) or a data file (`corrections-registry.yaml`). Small enough to ship; coordinated through the close-stage session.

The status column says either *Built in this session* (the part landed) or *Queued for [build plan path]* (the part is specified, build plan elsewhere).

Not every part has to land in the close-stage session. The ai-services fix spec landed Part C and Part D.2 in the close-stage session; Parts A, B, and D.1 were specified and queued for a separate owner-reviewed build session via [plans/plan-session-integrity-backward-reconciliation-2026-05-21.md](../../../plans/plan-session-integrity-backward-reconciliation-2026-05-21.md).

### Section 4: What this fix is not (negative space)

The fix spec carries an explicit negative-space section. Restraint is the fix's discipline; the negative section makes the restraint visible.

Common statements in this section:

- **Not a new skill or framework.** The fix uses existing surfaces.
- **Not a generic abstraction.** Curated and short; new entries require evidence.
- **Not a hook.** Per project rules, hooks belong to the harness, not Claude.
- **Not a retroactive cleanup.** The structural fix prevents the next round; per-finding follow-ons repair the current backlog.
- **Not a closure of all hypotheses.** Some hypotheses' remaining surface is human-operational, not mechanism-fixable.

Five is a typical count. The discipline is the same as the per-part scope discipline (§2): name what the fix does not claim to do, so scope does not drift on the next pass.

### Section 5: Carry-forward

What the next session inherits after the close-stage session lands. Concrete:

- Which parts are live.
- Which parts are queued (with the build plan path).
- The hypotheses' final verdicts recorded.
- The decision-log entry appended.
- The campaign closed as a unit.

The section ends with a one-line note: *the next natural test of the structural fix is X*. (X is the kind of work the fix exists to support.)

---

## 4. Voice and Pre-Output Gate

Both close-out artifacts pass through the instance voice skill's Pre-Output Gate (in HeyHi, `heyhi-voice`) before publication:

- **Em dash scan.** Internal operational documents are exempt from the 2-per-document limit, but the gate's scan still runs. Document the em-dash count in the session's `## Smoke Test` slot.
- **Banned word scan.** Synthesis briefs and fix specs are not client-facing, but the banned vocabulary still degrades signal. Apply the full list.
- **"AI" standalone scan.** Same. Internal-only doesn't excuse the standalone use.
- **Critical AI tell scan.** Reframe constructions, kicker patterns, "X, same Y:" frames. Audit close-outs are particularly vulnerable to these because the writer is summarizing under time pressure.

The voice gate is the last check before the artifact is committed. Run it. Empty `## Smoke Test` slots that say "voice gate passed" without naming the scan run are advisory prose, not verification.

---

## 5. Propagation pass (Tier 1, in-task at Step 5)

After the synthesis brief and fix spec are published, the close-stage session updates dependent surfaces per `CLAUDE-SESSION-RULES.md § Propagation tier discipline`. Common Tier 1 targets for capability audits:

- `ai-services/_core/synthesis.md` — downstream summary surface that paraphrases the audit's findings.
- `ai-services/_core/ai-service-offerings.md` — canonical service definitions; updates if the audit changed what is sellable.
- `recurring-revenue/productized-services.md` — productized service docs; updates if the audit changed scope claims.
- `marketing/competitive-brief.md` — competitive positioning; updates if the audit changed capability claims used in positioning.
- `project-state.yaml` — `capability_readiness` rollup, `last_verified` dates.
- `ai-services/_core/decision-log.md` — append the campaign's consolidated decision-log entry.

The propagation pass is in-task work for the close-stage session. It is not deferred to session integrity.

---

## 6. Quick checklist before declaring close-out done

Synthesis brief:

- [ ] Three-level structure present (headline / per-layer detail / cited evidence).
- [ ] Headline fits on one screen and leads with a number or verdict.
- [ ] Per-layer detail uses tables with stable column shapes.
- [ ] Every claim cites a ledger row, finding ID, or downstream surface.
- [ ] Closing section names dated context and carry-forward.
- [ ] Voice gate passed.

Fix specification (when produced):

- [ ] All five sections present.
- [ ] Section 2's parts each have all five fields (closes / what / where / why / how-verified / scope-discipline).
- [ ] At least one part's "how verified" names a runnable test.
- [ ] Implementation table names owner and lands-in for every part.
- [ ] Negative-space section (Section 4) names at least three things the fix does not do.
- [ ] Carry-forward names what the next session inherits.
- [ ] Voice gate passed.

Propagation:

- [ ] Decision-log entry appended.
- [ ] Tier 1 dependent surfaces updated.
- [ ] Campaign plan status flipped to `executed`; `executed_date` set.

---

*HeyHi Internal Use Only. heyhi-skills/heyhi-audit-campaign/references/. Loaded by SKILL.md Step 5 (Close stage).*
