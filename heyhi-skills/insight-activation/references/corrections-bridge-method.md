---
classification: confidential
title: "Corrections-bridge method — the method spine"
skill: insight-activation
loaded_by: "SKILL.md Step 1"
---

# Corrections-bridge method

How a finding becomes a candidate correction, held as reference. On-demand — load when activating an insight. This skill is an extension of the R1 corrections runtime, so this reference registers under that runtime's convention (`sheerline/os/corrections/LIFECYCLE.md`, `seed-corrections.yaml`); it never re-authors it.

*Internal operational reference (deployed under `heyhi-skills/`): the em-dash limit is exempt per `OPERATING_PRINCIPLES.md`.*

---

## The correction schema (what a candidate must fill)

From `sheerline/os/corrections/seed-corrections.yaml`, the per-entry schema (schema-compatible with agent-corrections):

| Field | What it is | Who sets it |
|---|---|---|
| `id` | kebab-slug naming the pattern (`hardcoded-hex-bypasses-token`) | this skill (candidate) |
| `category` | the design/practice taxonomy bucket (token-fidelity, spacing-scale, semantic-role, accessibility, elevation, typography — plus method/area buckets for the audit skills: `experiment-integrity`, `measurability`, `strategy-reasoning`, `decision-hygiene`) | this skill (candidate) |
| `severity` | exactly `factual` or `behavioral` — the load-bearing call (see below) | this skill proposes; **curator confirms** |
| `status` | `active` / `superseded` / `retired` | curator (on adoption) |
| `trigger_context` | *when* the pattern fires, recognizable to a future session | this skill (candidate) |
| `correction` | what to do instead | this skill (candidate) |
| `times_fired` | lifetime fire count (a floor on sessions the pattern has cost) | curator; this skill only proposes an increment on a dedup match |
| `last_fired`, `origin_date` | dates | curator |

The design/practice taxonomy lives in `category`; `severity` stays exactly `factual | behavioral`. Do not smuggle taxonomy into severity.

## The factual / behavioral classification rubric (the load-bearing call)

This is the one judgment the skill makes, and it makes it as a *candidate* for the curator. The two values carry very different downstream power (`LIFECYCLE.md`), so the classification matters:

- **`factual`** — a **deterministic, structural** fact about the artifact. It can be checked mechanically and, in principle, enforced. Examples: a hardcoded hex where a token exists; an off-scale spacing value; a method that mechanically misfires on a whole class of inputs (the E-1 finding: an SRM check computing χ² on a paired/deterministic design, where no randomizer exists). Factual corrections *may* be injected/enforced and *may* be promoted once they cross the threshold.
- **`behavioral`** — a **taste read, a critique tendency, a judgment call**. It cannot be reduced to a deterministic check without becoming something it is not. Examples: restraint-vs-incoherence on a visual deviation; a warden's temptation to rank; a measurability map's pull to pick the metric. Behavioral corrections **surface to the human as a reminder to decide, are never auto-injected into generation, and are never promotable to an enforced rule.**

**The test.** Ask: *could this be checked by a deterministic rule without collapsing a judgment into a mechanism?* If yes → `factual`. If checking it would force a taste/values call into an auto-firing rule → `behavioral`.

**The tie-break.** When genuinely ambiguous, default to **`behavioral`** and say so. The asymmetry is deliberate: mis-classifying a taste call as `factual` risks an enforced rule auto-firing on a judgment (the boundary collapsing); mis-classifying a fact as `behavioral` only means it surfaces for a human instead of enforcing — a softer, reversible error. Under-claim enforcement; never over-claim it.

**A note on the audit-skill findings specifically.** Many findings from the four Sheerline audit skills are *method-completeness* facts (a check that misfires, a report section that is missing) — these are `factual` (a structural gap in the skill). But findings *about the artifact under audit* (a readout's honesty, a tree's reasoning) that the audit skill itself left as an empty judgment slot are `behavioral` if activated at all — the audit skill already refused to render them, and this skill must not render them either by the back door of a correction.

## Dedup and the promotion threshold (read-only)

- **Dedup.** Before proposing a new entry, check the existing corrections (`retrieve_design_corrections`, read-only, or the seed/live registry). If the pattern is already tracked, this finding is a **fire-count increment candidate** — name the matched correction and propose incrementing `times_fired` + refreshing `last_fired`, rather than creating a duplicate. Within one activation batch (e.g. a self-application harvest with several findings), collapse duplicate patterns to one candidate and note the collapse.
- **The promotion threshold (factual only).** `LIFECYCLE.md`: promote at **5+ total fires OR the same pattern across 3+ separate sessions**. When a dedup match shows a **factual** pattern at or near threshold, flag it *promotion-eligible* — a candidate for the curator to write into a hard rule and supersede the entry (the close-out is: write the rule, set the entry `superseded` + `superseded_by`, recompute `meta`). This is a flag for the human, not an action this skill takes.
- **Behavioral patterns are never promotion-eligible.** By construction (`LIFECYCLE.md` tightening 2). Never flag one. If a behavioral pattern keeps firing, that is a signal the *human* should weigh (maybe the taste guidance needs restating), not a trigger for enforcement.

## The intake-routing rule (the firewall)

The candidate goes to `corrections-intake/` — the human-only route (`OPERATING_PRINCIPLES.md § Corrections Intake Protocol`). **Never to `sheerline/os/corrections/` (the convention seed) or the live heyhi-mcp registry (human-curated).** The firewall is the whole point: an agent may *observe and propose*; only a human curates what reaches agent context. This skill is the systematizer of the *design-finding* case of that intake — it does not weaken the firewall, it feeds it in a well-shaped form.

## Why this closes the loop (and why that matters)

The four audit skills each open with a Step-0 "retrieve any recurring corrections" hook. Today that hook is a no-op in areas 9/10/11 — there are no corrections to retrieve (2026-08-22 audit § 2.5), so the skills cannot get better from use. This skill is the write-candidate side that eventually fills those hooks: finding → candidate → (curator) → adopted correction → retrievable at the next Step-0. The loop is: *find (audit skill) → activate (this skill) → curate (human) → retrieve (audit skill's Step-0) → find better.* Without this skill the loop is open and the audit skills are shelf-stable and shelf-bound. With it — and only once the human curates — they compound. The compounding is real; the human gate is what keeps it honest.

*HeyHi Confidential. Reference for `insight-activation`. Spec source: `sheerline-skill-buildout-research-2026-08-09.md` § 7c use case #11; corrections model per `sheerline/os/corrections/LIFECYCLE.md` + `seed-corrections.yaml`.*
