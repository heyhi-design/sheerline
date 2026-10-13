---
name: heyhi-drift-repair
description: >-
  Turn located design-system drift and accessibility findings into APPLIED or
  PROPOSED repairs — the missing "act" step in Sheerline's retrieve → validate →
  grade → learn loop. Consumes findings from validate_output, the conformance
  lane, the Design Intelligence Audit, and the a11y audits; per finding it either
  auto-applies a pre-registered structural transform (a known_bad → expected
  reference-swap, re-validated, with a reversible deviation record) or proposes a
  human-confirm candidate — and writes nothing it cannot mechanically verify. The
  apply/propose decision keys on the `detection` axis (deterministic → auto-apply;
  judged, and the judged half of hybrid → propose-only), NEVER on `severity`.
  Triggers: "repair this drift", "fix the token bypasses", "apply the audit
  findings", "make the audit actionable", "auto-fix the conformance failures",
  "turn these findings into fixes", "drift-repair loop". Every judged call ships
  as a labeled empty slot behind a named human gate. NOT an auditor — it consumes
  findings, it does not discover them (use heyhi-design-intelligence-audit /
  heyhi-a11y-audit / heyhi-a11y-annotation / validate_output). NOT a grader — it
  applies point fixes and assigns no score (the evaluator's moat is untouched).
  NOT heyhi-figma-ds-generator — that writes a system IN; this writes a fix
  BACK. NOT a Figma-canvas writer in v1 (that target is deferred). NOT for
  translating a prototype/raster into a Figma design file (heyhi-design-bridge).
version: "0.1.0"
updated: "2026-09-04"
status: "deployed 2026-09-04 — heyhi-skills/heyhi-drift-repair/; registered in the main registry and the Sheerline area-7 subset registry. Built from plans/plan-drift-repair-loop-2026-08-29.md (DISPATCH-02 decision-ready spec, PR #747), staged PR #750/#751, promoted in the 2026-09-04 promotion pass. Sheerline area 7 (Design Systems), cross-cutting area 8 (Accessibility). Adopts the spec's §10 D-1…D-5 recommendations and the OQ defaults (proposal-first, code + token-source targets; OQ-1 Figma canvas write = planned v2; OQ-3 promotion path documented in corrections-intake/README.md, PR #761)."
classification: HeyHi Confidential
---

# HeyHi Drift-Repair Loop

**Sheerline area 7 (Design Systems) · cross-cutting area 8 (Accessibility) · the "act" verb.** An audit finds drift — a hardcoded hex where a token exists, an off-scale spacing value, a raw z-index, a contrast pair that is not declared safe. Today the finding is true, located, and inert: someone fixes it by hand. This skill is the act step that closes the distance between "we found the drift" and "the drift is fixed, or a fix is on the human's desk." Per located finding it **classifies** the drift on the `detection` axis, **auto-applies** the pre-registered structural transform when the fix is mechanically decidable (re-validating it and recording a reversible deviation), or **proposes** a labeled human-confirm candidate when a person must decide. It sits between validate and learn, disciplined by both.

**The boundary this skill obeys (Sheerline, absolute).** The loop lives entirely inside the ~40% of the work that is safely automatable (`brand/dont-automate-this.md`); every judged call is on the 60% side, and each is a labeled empty slot behind a named human gate. The apply-authority gate is the `detection` field, and it is **structural, not a confidence threshold**: `judged` means propose, always — there is no "high-confidence contrast" path, no "obvious semantic-role" path. A repair *routes a human decision or lands a recorded, reversible structural fix; it never auto-approves taste, and it never auto-blocks a merge* (adopting `sheerline/docs/architecture.md:51` verbatim as the loop's ceiling). A version of this skill that auto-repairs any `detection: judged` finding — even a cheap, obvious one — has exceeded its charter (`sheerline/os/operating-principles.md:46`).

> **This skill closes through the Exit Gate (`CLAUDE-SESSION-RULES.md § Exit Gate`).** See the bottom-of-skill bracket.

---

## Routing — disambiguation with sibling skills

| If the task is… | Use |
|---|---|
| Applying / proposing repairs for **located** drift + a11y findings (the act verb) | **this skill** |
| **Discovering** the findings (drift, token bypasses, contrast) | `heyhi-design-intelligence-audit`, `validate_output` (the conformance lane) |
| A standalone WCAG conformance verdict (ACR/VPAT) | `heyhi-a11y-audit` |
| Annotating a design with the a11y spec before build | `heyhi-a11y-annotation` |
| **Generating** a design system live INTO a Figma file (the write verb) | `heyhi-figma-ds-generator` (spec: `plans/plan-ds-into-figma-generator-2026-08-29.md`) |
| Translating a prototype / raster into a Figma design file | `heyhi-design-bridge` |
| **Grading** output over a release series | the evaluator (`plans/plan-design-output-eval-harness-2026-07-16.md`) |
| Turning a *recurring* repair into a candidate correction (the learn verb) | `insight-activation` — this skill routes its learn step through that discipline (Step 6) |
| Deciding a judged fix, confirming a deviation, promoting a correction | **the human** (this skill's named gates) |

The seam is directional and verb-shaped: the audit skills **find**, the generator **writes a system in**, the evaluator **grades a series**, and this skill **writes a fix back**. It is downstream of every audit skill and never re-runs their detection.

---

## Step 0: Improvement hook check

Retrieve any recurring corrections for repair / token-fidelity / accessibility work (`retrieve_design_corrections` if the design MCP is reachable, or the Sheerline `sheerline/os/corrections/` registry). Fold a match into the pass. Skip silently if none.

## Step 1: Load context

1. The **located findings** to act on — the output of a `validate_output` call (`ValidationResult.errors[]`), a conformance-lane run (`css_check.check_css`), a Design Intelligence Audit (findings with severity + "one concrete next step"), or an a11y audit (per-criterion evidence tagged `automated` / `human-reviewed` / `AT-confirmed`). Normalize each into the located-finding shape in `references/repair-taxonomy.md § Findings in`.
2. `references/repair-taxonomy.md` — THE method spine: the `detection`-keyed taxonomy, the v1 seed repair library (the 9 deterministic transforms), the never-auto set, the write-target decision (code vs token-source vs the deferred Figma canvas), the provenance model, the deviation-record schema, and the learn write-back seam. Read it before acting.
3. `references/worked-example.md` — a filled run on synthetic input. Read it to calibrate the shape of the deviation records, the proposals, and the learn candidate; do not copy its findings.
4. The **repair library**: the instance's own live corrections registry, read at run time (resolved via `sheerline/profile/engagement-intake.yaml → design_system.source`), OR the generic seed substrate (`heyhi-mcp/heyhi_mcp/corrections/seed-corrections.yaml`) when no live registry is present. The 9 `detection: deterministic` seeds each carry the `known_bad` → `expected` transform that *is* the repair.
5. The intake config — `sheerline/profile/engagement-intake.yaml` (pointed at a gitignored filled copy at run time): `design_system.source` / `token_spec` / `serves_via_mcp`; `component_source` / `component_format` / `figma_file_key`; `constraints.do_not_automate` (extra never-auto entries, honored as additional judged slots); `constraints.brand_voice_source` / `voice_prohibited`; `remediation.model` / `remediation.map` (proposals speak the owner's backlog vocabulary, not HeyHi consulting framing); `boundary.hermetic_seal_confirmed` / `deliverable.root`.
6. Read-only convention: `sheerline/os/corrections/README.md`, `LIFECYCLE.md`, and the corrections schema (`heyhi-mcp/heyhi_mcp/corrections/schema.yaml` — the `detection` axis, the `known_bad`/`expected` fields). You register under this convention; you do not author the live registry.

## Step 2: Classify each finding on the `detection` axis (NOT `severity`)

`detection` is a property of a *correction*, not of a raw finding, so it exists only once a finding resolves to a `matched_correction`. Match with the corrections module's own machinery (`heyhi-mcp/heyhi_mcp/corrections/predicates.py`, `evaluate_predicate`) — do not invent a second matcher. Then route:

| `detection` | Action | Write? |
|---|---|---|
| **deterministic** *and* the value resolves to exactly one token in the instance's canonical set | **auto-apply** the `expected` transform at the drift's location, then re-validate | yes → then Step 4 |
| **deterministic** but the value resolves to more than one canonical token | **propose** with the `[inferred]` label — the "which token did this site intend" call is a semantic-role judgment | no |
| **judged** | **propose** with a `needs-human-confirm` flag | no |
| **hybrid** | auto-apply the structural half **only when it carries a registered emitted-code transform**; propose the judged half. In v1 no seeded hybrid carries one (`detached-component-instance` lives on `json_artifact`), so v1 is **propose-both** | structural half only (none in v1) |
| **no matched correction** (novel drift) | **propose** with the `[inferred]` label and the validator's nearest-token hint | no |

**Why `detection`, not `severity`:** `severity` answers "may we *record the rule* without human sign-off" (factual vs behavioral — the registry's write authority). The repair loop asks a different question — "may we *apply the fix without a human*" — which is answered by whether the drift and its fix are mechanically decidable. The proof they must not be conflated is `contrast-pairing-not-declared-safe`: `severity: factual` **and** `detection: judged` (`seed-corrections.yaml:279`). Keying on `severity` would auto-apply a contrast repair — exactly what A.1 says to propose-and-record, never auto-land. Keying on `detection` keeps contrast propose-only.

**Default is proposal-first.** Auto-apply is an explicit per-engagement opt-in (`engagement-intake`), not the default. In proposal-first mode even a deterministic-unambiguous finding is *proposed* (with its ready-to-apply transform attached) and nothing is written until a human turns auto-apply on. This is the spec's OQ-2 safe default.

**Only `error`-tier findings are auto-apply-eligible.** A finding normalized from a `warnings[]` or `suggestions[]` entry (`source_tier` ≠ `error`) is propose-only regardless of `detection` — the engine enforces this at the write decision, so a warning can never auto-apply even if it matched a deterministic correction (spec §5.1). See `references/repair-taxonomy.md § 5`.

## Step 3: Run the repair engine (per finding)

The engine (`scripts/repair_engine.py`) executes the per-finding routing above. It is delegation-shaped: at deployment `match_correction` delegates to `evaluate_predicate` over the live registry and re-validation delegates to `validate_output` with the instance's `constraints`; the staged engine implements a faithful self-contained version over the seed substrate so the acceptance criteria run without the full MCP (mirroring the seed library's own "fallback substrate when no live registry is present" role, `seed-corrections.yaml:6-11`). The apply step for the code target is a **value → token-reference substitution** derived from the `known_bad` / `expected` pair, applied at the finding's location. Run it, or follow its logic by hand; see `scripts/README.md` for the delegation boundary.

## Step 4: Re-validate every applied repair, and roll back on failure

Every applied repair is re-validated before it is considered landed (Evaluation Before Deployment). Re-validation runs the same check that produced the finding — at deployment, `validate_output` with the instance's `constraints`; in the staged engine, a conformance re-scan of the repaired region. It checks **conformance, not intent**: any same-valued token would clear the finding, so a valid-but-wrong substitution would still pass — which is exactly why Step 2 bars an ambiguous auto-apply upstream (re-validation is a safety net against a broken result, not a judge of the *right* token).

- Originating finding no longer fires **and** no new error appeared → the repair holds; the deviation record stands.
- The finding still fires, or a new error appeared → **roll back** the edit and downgrade the finding to a proposal. A deterministic repair that does not re-validate is a defect, not a landing.

## Step 5: The human gate, provenance, and the deviation record

Every applied repair writes a reversible **deviation record**: `{ finding, matched_correction, before, after, surface, location, timestamp, provenance: automated, confirmed: false }`. It is the human-confirmation queue and the audit trail in one; `confirmed` flips only on a human's review, never on the loop's own re-validation.

Provenance labels mirror the a11y model so the surfaces read consistently:
- **Applied deterministic repair → `automated`.** This attaches only to an unambiguous auto-apply. An `automated` repair is never a taste approval — the deviation record says *what changed and why it is conformant*, not that the result is *good*.
- **Proposed judged repair → `[candidate: needs confirmation]`.**
- **Anything inferred (e.g. which token an ambiguous literal intended) → `[inferred]`.** By construction `[inferred]` is always *proposed*, never auto-applied, so `[inferred]` and `automated` never co-occur on one output.

The judgment slots this loop must refuse (each behind its named gate):

| Empty slot | Named gate |
|---|---|
| The contrast "declared-safe" call | Repair-confirmation sign-off |
| Semantic-role correctness (a valid token in the wrong role) | Repair-confirmation sign-off |
| Which token an ambiguous literal intended | Repair-confirmation sign-off |
| Alt text, reading-order intent, ARIA role correctness | Annotation designer sign-off (`heyhi-a11y-annotation`) |
| The conformance verdict (CONFORMS/DRIFTS) | Audit report sign-off |
| Any `constraints.do_not_automate` entry | Per-engagement (intake) |

## Step 6: Learn — route a recurring repair to the human-only intake

When the same finding recurs across sessions, propose a *new correction* so the next session catches it earlier. This reuses the `insight-activation` learn discipline exactly, with one extension: because the repair loop *owns the transform it just applied*, it authors the design-extension fields (`detection`, `predicate`, `known_bad`, `expected`) into the candidate — a superset of what `insight-activation` emits today (spec OQ-3, recommendation (a)).

- Write the candidate to `corrections-intake/YYYY-MM-DD-<slug>.md` with `Status: proposed` and the decide-to-adopt slot empty. **Never** to the live registry, never to `sheerline/os/corrections/` (the firewall, `OPERATING_PRINCIPLES.md § Corrections Intake Protocol`).
- It never auto-injects and never promotes. Promotion is the curator's, on the registry's own threshold.
- Over-threshold surfacing (OQ-4): if a matched factual pattern is at/near its promotion clause (e.g. `contrast-pairing-not-declared-safe` at `times_fired: 6` with a 3-fire clause), FLAG it as promotion-eligible for the curator — surface it, never take it.

*The promotion PATH into the per-DS design registry is open (spec OQ-3): `corrections-intake/README.md` documents promotion only into the root and method registries, not the live-or-seed per-DS design registry that `retrieve_design_corrections` reads (`heyhi-mcp/heyhi_mcp/tools/corrections.py:119-128`). The candidate still lands behind the same human firewall regardless; the path is a promotion-time question, not a blocker on filing the candidate.*

## Step 7: Pre-flight verification

Confirm, before declaring done (these are the spec's §8 acceptance criteria; the eval harness `evals/run.py` asserts them mechanically):

**Runtime requirement.** `evals/run.py` loads the seed repair library from `heyhi-mcp/heyhi_mcp/corrections/seed-corrections.yaml`, a retained runtime that lives in the HeyHi monorepo and does not ship with the Sheerline scaffold export. Run the harness from a monorepo checkout (or any checkout that carries that runtime at the same repo-relative path); in a standalone scaffold checkout it cannot load the seed library and will not run.

1. **Round-trip discrimination** — a deterministic repair applied to a `known_bad` fixture makes the region match `expected`; reverting re-fires the finding.
2. **False-repair floor** — a known-good fixture produces zero repairs and zero proposals.
3. **Boundary assertion** — a `detection: judged` finding produces a proposal with the human-confirm flag and **no write** (assert no file changed).
4. **Idempotence** — a second auto-apply run applies zero new auto-repairs (judged/unmatched re-propose by design; assert zero new *auto-applies*).
5. **Token-source propagation** — a token-definition fix *targets* the single DTCG source (as a proposed diff — v1 does not auto-write target A), not N patched call-sites; a call-site literal writes the site, not the source.
6. **Post-repair re-validation** — every applied repair is followed by a passing re-validation; a repair that fails is rolled back.
7. **Instance isolation** — a tenant run (injected `constraints`) leaks no HeyHi token name into any repair or proposal.
8. **Provenance + deviation present** — every applied repair carries `provenance: automated` and a complete reversible deviation record; every proposal carries `[candidate: needs confirmation]` or `[inferred]`.

## Output structure

```
# Drift-Repair Run — [instance] · [surface]
Mode: proposal-first | auto-apply    Findings in: N    Run: [date]

## Applied repairs (deterministic, re-validated)     [empty in proposal-first mode]
| Finding | Location | before → after | Re-validated | Provenance | Deviation record |
|---------|----------|----------------|--------------|------------|------------------|
| off-scale-spacing-value | card.css:12 | padding: 16px → var(--space-4) | pass | automated | dev-0001 |

## Proposals (human-confirm — NOTHING written)
| Finding | detection | Why propose-only | Ready transform (if any) | Provenance | Named gate |
|---------|-----------|------------------|--------------------------|------------|------------|
| contrast-pairing-not-declared-safe | judged | "declared safe" is a design decision | (none — human call) | [candidate: needs confirmation] | Repair-confirmation sign-off |

## Learn candidates (routed to corrections-intake/, NOT the live registry)
- corrections-intake/YYYY-MM-DD-<slug>.md — [pattern], detection/known_bad/expected authored, decide-to-adopt slot EMPTY

## ⛔ Repair-confirmation — NEEDS HUMAN
Every deviation record above is `confirmed: false` until this line is signed.
   Confirmed by: ____________________  Date: ______
```

---

## What is explicitly out of scope

- **Discovering findings.** This skill consumes located findings; detection stays in `validate_output`, the conformance lane, the DI-audit, and the a11y audits. It never re-implements contrast math or any other detector.
- **Grading.** No score, no series. The evaluator's charter is untouched — the loop never reads a grade to decide whether to repair, and never writes a grade as a result.
- **Repairing a judged finding.** Ever. Not even a cheap, obvious one. `detection: judged` → propose, always (the never-auto invariant).
- **Figma-canvas writes (v1).** The canvas target is app-brokered, human-initiated, and its create-only Variable guard blocks a repair (a change to an existing Variable) — structurally incompatible with an unattended auto-apply. Deferred behind a named gate (spec OQ-1); even in a later increment it is a *proposed*-only canvas edit.
- **Auto-writing the token source (target A) in v1.** Token-definition fixes are proposed as a diff for human approval, not auto-written — their members are `judged` and their blast radius is a shared value.
- **Brand identity.** Brand marks, logos, and disabled controls are out of scope for contrast repair and are not "fixed" (`design-fundamentals.md:37`).

---

## Exit Gate Required Headers (bottom-of-skill bracket)

This skill closes through Exit Gate Flavor A (`CLAUDE-SESSION-RULES.md § Exit Gate`). Before declaring done, confirm every required header holds real content:

- `## Fixes Applied` (the Drift-Repair Run output — applied repairs and/or proposals, with paths)
- `## Smoke Test` (the Step 7 pre-flight checks — paste the `evals/run.py` pass/fail table)
- `## Next Session Prompt` (what the human still needs to confirm; any promotion-eligible flag)

If any `detection: judged` finding was auto-repaired, if any deviation record is `confirmed: true` without a human signature, or if a learn candidate landed in the live registry, the gate has **not** been satisfied.

---

*HeyHi Confidential. Sheerline area 7 (Design Systems), cross-cutting area 8 (Accessibility). Deployed 2026-09-04 (v0.1.0) — registered in both registries. Spec source: `plans/plan-drift-repair-loop-2026-08-29.md` (DISPATCH-02, PR #747). Sibling of the DS-into-Figma generator (`plans/plan-ds-into-figma-generator-2026-08-29.md`, disjoint output — that writes a system in, this writes a fix back). Portfolio use is a separate redaction pass per the spec's §11 (strip the seed transforms, instance internals, intake field names, paths, IP/charter cross-references; keep the problem framing, the detection-vs-severity decision, the write-target trade-off, the never-auto boundary, the provenance model, and the acceptance shape).*
