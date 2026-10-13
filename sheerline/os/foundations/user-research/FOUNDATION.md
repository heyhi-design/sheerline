---
classification: confidential
title: "Foundation: User Research (area 1, COVERED / filled / governed practice)"
area: 1
nature: craft
coverage: covered
phase: P3
kind: governance
status: filled
---

# Foundation: User Research (area 1)

**Coverage: COVERED — filled at the P3 foundation fill, then covered when `research-plan-author` deployed. The foundation was the tracked-gap promise built ahead of the skills; the first dedicated skill has now landed on it.** User Research is the head of the dependency spine (User Research → Information Architecture → (Interaction ‖ Content) → Visual → Design Systems): Information Architecture presupposes it, because labels and taxonomy are sourced from real user vocabulary, which research supplies. The fill authors the **craft canon** the skills consume and **points at** the always-loaded behavioral invariants (it never restates them). Coverage moves `gap → partial` because a filled governance foundation is no longer an empty room; `partial → covered` is earned later, as real UR skills land. The automatable core of research work is already commoditized by category-defining incumbents (Dovetail, Maze, Optimal Workshop); the governed value is the **boundary discipline the incumbents structurally cannot ship** — their incentive is speed, and speed drives the documented failure modes. So almost every skill here is class **N** (nothing to generalize), and that is the strategic tell, not a weakness.

The buyer is not the researcher-with-Dovetail. It is **the design team that no longer has a researcher**, whose designers run model-accelerated studies with no protocol (the "de-researchering" finding). Sheerline is the guardrail that stops a model-accelerated study from laundering synthetic or flattened output into "findings."

## What already exists (do not re-stub as absent)

User Research is a gap in *dedicated* skills, not in all research-adjacent capability. The foundation **references these adjacent HeyHi corpora in place, copying nothing**:

- the **facilitation corpus** (`heyhi-workshop`) for session conduct — how a room is run, not what a study asks;
- the **foresight methodology** (`futurecasting` / the foresight-methodology reference) for reading *organizational* signals — a different object from user evidence;
- `heyhi-discovery-call` as the **sales** discovery it is *not* — the disambiguation the UR skills' `not_for` clauses enforce. Discovery-call qualifies a buyer; research studies a user.

The point: the net-new gap is dedicated research *discipline*, and the canon below is where it is authored.

## Points at the invariant, does not restate it

The always-loaded behavioral guardrails that govern UR are authored **once** in [`os/operating-principles.md`](../../operating-principles.md); this foundation cites them by path and re-derives none:

- **The empathy boundary** (`operating-principles.md` § The empathy boundary) — a model simulates cognitive empathy (inferring what a user might think); it has no experiential empathy (having lived it). Research synthesis and persona work carry this boundary; simulated empathy is never presented as the real thing.
- **What stays human** (`operating-principles.md` § What stays human) — the research *question*, direction selection, severity-as-truth, ethics. The canonical list lives there; this foundation does not re-enumerate it.
- **The ideation-diversity guard** (`operating-principles.md` § The ideation-diversity guard) — generative research widens the field and never selects. Model-assisted ideation lifts an individual option and collapses the diversity of a set; it is stimulus, never the choice.
- **The cross-quality conflict-resolution order** (`operating-principles.md` § The cross-quality conflict-resolution order, which points at A.1) — how research evidence resolves against the other qualities when they disagree.
- **Scoring is advisory, never a gate** (`operating-principles.md` § the taste-and-critique boundary) — a severity score or a confidence figure informs a human; it never auto-approves or auto-blocks.

## The judged layer (what stays human)

The tracked shortfall the mechanical/automatable layer cannot reach. Every UR skill ships these as empty slots behind a named gate, with provenance labels on anything synthetic:

- the research **question** (what are we actually trying to learn);
- the final **method** and the **go** decision;
- **theme verdicts** (is this pattern real, or an artifact of the coding);
- statistical and practical **significance** (does the number mean anything, and does it matter);
- **gold-vs-noise** (which utterance is signal);
- **severity-as-truth** ("does it matter" — the difference between a scored finding and a real one).

A capability that fills its own judgment slot has exceeded its charter.

## The knowledge canon (authored here — the skills' reference)

This is the craft the foundation genuinely authors, the analogue of the accessibility WCAG canon. The UR skills load it; the incumbents do not ship it.

| Topic | The canon (authored here) |
|---|---|
| **Method selection** | Generative vs. evaluative research; the Opportunity-Solution-Tree framing with its failure warnings (a solution dressed as an opportunity). Choosing *which* method a question needs is scaffolded; the final method is the human's. |
| **The Faulkner-corrected sample-size standard** | Bans the folk "5 users = 85%." The corrected floor: **5 for directional, 10 for a reliable mean, 20 for a ≥95% detection floor.** This is the standard `research-plan-author` wires into every plan; a plan under the floor for its stated confidence is flagged, not silently passed. |
| **Usability-evaluation standards** | Nielsen's 10 heuristics; **severity = frequency × impact × persistence**, run **advisory-never-gate** (a severity score informs a human; it never blocks a merge). Faulkner-honest confidence framing on every first-pass score — a first-pass severity is a proposal to a human, labeled as such. |
| **The synthesis method + anti-flattening discipline** | Staged coding; a **mandatory disconfirming pass** (actively seek the evidence against each theme); the **80/20 outlier audit** (the 20% the majority theme buried); **verbatim traceability** (every theme traces to a real utterance, quotable). The discipline exists because model-accelerated synthesis flattens the outlier — the exact failure the incumbents' speed incentive drives. |
| **The synthetic-provenance rule** | **Generate-with-synthetic / validate-with-humans / never the reverse**, labeled on every surface. Synthetic participants may widen a hypothesis set; they may never stand in for validation. Authored here — it is UR craft, not an always-loaded invariant. |
| **Participant-integrity standards** | The model-pollution taxonomy: detecting and resisting fraudulent or model-generated participants; screener fraud-resistance; anti-telegraphing (a question that hands the participant the answer it wants). |
| **Analytics-as-research** | The text-to-SQL trust ceiling; when behavioral analytics is evidence and when it is a leading question. Analytics answers "what"; it rarely answers "why." |
| **Research ethics** | Consent, participant welfare, data handling; the ethics thread that runs through `operating-principles.md`, named here where it bites on UR. Participant data (transcripts, recordings) is untrusted content at the write boundary: neutralize and provenance-stamp on ingest. |

## Registered skills (area 1)

The pipeline. `research-plan-author` is **deployed (v0.1.0)** — the first dedicated User Research skill, registered in both registries; it takes this area from `partial` to `covered`. The other three are **held** behind their gates. Gate tiers and the corpus-thickness dependency: [`plans/plan-sheerline-p3-ur-ia-foundations-2026-08-29.md`](../../../../plans/plan-sheerline-p3-ur-ia-foundations-2026-08-29.md) § 1.2 / § 5.

| Skill | Class | Gate tier | Judgment that stays human |
|---|---|---|---|
| `research-plan-author` | N | Tier 1 — **deployed** (proved first on the instance's own practice) | the question; the final method; the go decision |
| `synthesis-pipeline` | N (flagship) | Tier 2 — held on research-example-corpus thickness | theme verdicts; significance; gold-vs-noise |
| `usability-evaluation` | X (audit family) | Tier 2 — held on research-example-corpus thickness (severity calibration) | severity confirmation; "does it matter" |
| `instrument-smith` | N | Tier 2b — held on engagement pull | which questions matter; in-session probing |

`insight-activation` (the findings → correction learn-verb) is already built and registered under area 1; it is the model the research-example-intake queue reuses (§ 5.3 of the spec), not a UR study skill.

---

*Area map: [`os/foundations/registry.yaml`](../registry.yaml) · Always-loaded invariants: [`os/operating-principles.md`](../../operating-principles.md) · The IP boundary (scaffold ships, populated corpus stays): `operating-principles.md` § The IP boundary · Spec source: [`plans/plan-sheerline-p3-ur-ia-foundations-2026-08-29.md`](../../../../plans/plan-sheerline-p3-ur-ia-foundations-2026-08-29.md) · Research of record: `ai-services/design-intelligence/research/sheerline-skill-buildout-research-2026-08-09.md` § 3.1 / § 7b*

*HeyHi Confidential*
