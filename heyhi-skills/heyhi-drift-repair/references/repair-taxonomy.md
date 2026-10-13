# Repair taxonomy — the method spine

*HeyHi Confidential. Loaded on demand by `heyhi-drift-repair/SKILL.md` Step 1. The `detection`-keyed taxonomy, the v1 seed repair library, the never-auto set, the write-target decision, the findings-in normalization, the provenance model, the deviation-record schema, and the learn write-back seam. Reference, don't restate: the always-loaded invariants are cited by path, never re-authored here. Full derivation: `plans/plan-drift-repair-loop-2026-08-29.md`.*

---

## 1. The two axes, and why the loop keys on the right one

The corrections schema (`heyhi-mcp/heyhi_mcp/corrections/schema.yaml`) carries two orthogonal axes:

- **`severity: factual | behavioral`** (`:35-42`) — write authority for the *registry*: may an agent record this correction without human sign-off. Factual is safe to auto-record; behavioral needs review. **This is the registry's question, not the repair loop's.**
- **`detection: deterministic | judged | hybrid`** (`:109-121`) — mechanical verifiability: can we *mechanically detect and locate* this drift. `deterministic` is licensed **only for structural predicates** (a literal where a token belongs, an unknown token name); a `category: semantic-role` correction is `judged`, never a conformance rule; `hybrid` is partly structural.

**The repair-apply decision keys on `detection`.** `severity` answers "may we *record the rule*"; the repair loop asks "may we *apply the fix without a human*" — answered by whether the drift and its fix are mechanically decidable, which is exactly what `detection` measures. The proof they must not be conflated is already in the seed library: `contrast-pairing-not-declared-safe` is `severity: factual` **and** `detection: judged` (`seed-corrections.yaml:279`). Contrast is cheaply measurable, but "declared safe for this use" is a design decision. Keying on `severity` would auto-apply a contrast repair — precisely the thing `design-fundamentals.md:37` (A.1) says to propose-and-record, never auto-land. Keying on `detection` resolves it: contrast is `judged`, so it is propose-only, full stop.

---

## 2. The taxonomy table

| `detection` | Repair action | Write? | What it records | v1 examples |
|---|---|---|---|---|
| **deterministic** (value → 1 token) | Auto-apply the registered `expected` transform at the drift's location | **Yes**, then re-validate | A reversible **deviation record** (before/after, source finding, timestamp) for human confirmation | the 9 structural seeds in §4 |
| **deterministic** (value → >1 token) | **Propose** with `[inferred]` — which token the site intended is a semantic-role call | No | proposal + `[inferred]` label | an instance whose canonical set genuinely collides |
| **judged** | Emit a labeled **candidate** repair with a human-confirm flag | **No** | `[candidate: needs confirmation]` + the human-gate slot it fills | `contrast-pairing-not-declared-safe`, `token-missing-semantic-role`, `arbitrary-value-escape-hatch` |
| **hybrid** | **Split**: auto-apply the structural half *when it carries a registered emitted-code transform*, propose the judged half | Structural half only | Deviation on the structural half; candidate on the judged half | `detached-component-instance` — **propose-both in v1** |
| **no match** (novel drift) | Propose with `[inferred]` + the validator's nearest-token hint | No | proposal + `[inferred]` label | any finding with no registered transform |

**Two preconditions scope the deterministic auto-apply:**

1. **The value → token map must be unambiguous.** Auto-apply substitutes a literal with the seed's single registered `expected` token — but a raw *value* can resolve to more than one same-class token, and choosing among them is a semantic-role judgment. So the deterministic tier auto-applies **only** when the literal's value resolves to exactly one token in the instance's canonical set; a value with more than one candidate downgrades to a proposal carrying `[inferred]`, and the "which token did this site intend" call becomes a named human slot. On HeyHi's own DTCG the canonical map is currently 1:1 — the apparent collisions (`0.5rem` → three spacing names, `200ms` → two duration names) are all `expectedViolation` fixtures the resolver excludes — so the guard bites only for a client instance whose canonical token set genuinely collides. It is an instance-safety property, not a HeyHi bug.
2. **No v1-seeded `hybrid` carries an emitted-code structural transform.** The one seeded hybrid, `detached-component-instance`, has no `known_bad`/`expected` pair and lives on the `json_artifact` surface, not the emitted-CSS surface v1 writes. So in v1 it is **propose-both**; the structural-half auto-apply is the general rule that activates once a hybrid with a registered emitted-code transform is seeded — none is today.

---

## 3. The never-auto set (the charter)

The loop **must never auto-apply** a fix for any of these, regardless of how mechanical the fix looks. This is not a tuning parameter or a confidence threshold — it is structural.

- **Semantic-role drift** — a valid token used in the wrong role (`color.neutral.900` where `text.primary` belongs). It renders identically, so no literal check can see it; `judged` by construction, "the canonical semantic drift the I1.5 mutation engine proved the deterministic floor is BLIND to" (`seed-corrections.yaml:327-330`).
- **The contrast "declared-safe" call** — measurable, but the safe-for-this-use verdict is a design decision.
- **Alt text, reading-order intent, ARIA role correctness** — the three empty designer slots the a11y-annotation skill names (`heyhi-a11y-annotation/SKILL.md:100-110`). The loop can flag a missing-by-construction gap; it never authors the words, the intended order, or the role call.
- **The conformance verdict itself** — CONFORMS / DRIFTS is a judgment-axis output; a finding on a judgment axis is a *flag*, never an automatic failure (`heyhi-design-intelligence-audit/references/conformance-sub-area.md:47`).
- **The SC 2.5.8 target-size (24×24) verdict** — the floor's Rule 3 warns at the stricter 44×44; the AA 24×24 verdict itself is judged, never an automated pass (`heyhi-a11y-audit/SKILL.md:106`).

This is the 40/60 line: the loop lives entirely inside the ~40% that is safely automatable, and every item above is on the 60% side that `brand/dont-automate-this.md` protects.

---

## 4. The v1 repair library (already seeded)

The deterministic auto-apply tier is already seeded. Nine `detection: deterministic` corrections in `heyhi-mcp/heyhi_mcp/corrections/seed-corrections.yaml` each carry a `predicate` (`surface: emitted_css`) that locates the drift and a `known_bad` → `expected` pair that *is* the repair transform. The pairs below are the live seed values (verbatim from the seed file, rule-wrapped form):

| Seed id | `known_bad` → `expected` |
|---|---|
| `hardcoded-hex-bypasses-token` | `.btn { color: #111827; }` → `.btn { color: var(--text-primary); }` |
| `off-scale-spacing-value` | `.card { padding: 16px; }` → `.card { padding: var(--space-4); }` |
| `raw-zindex-bypasses-elevation-token` | `.modal { z-index: 400; }` → `.modal { z-index: var(--z-modal); }` |
| `hardcoded-font-size-bypasses-type-token` | `.h1 { font-size: 16px; }` → `.h1 { font-size: var(--font-size-base); }` |
| `hardcoded-font-weight-bypasses-type-token` | `.title { font-weight: 600; }` → `.title { font-weight: var(--font-weight-semibold); }` |
| `hardcoded-line-height-bypasses-type-token` | `.body { line-height: 1.6; }` → `.body { line-height: var(--font-lineHeight-relaxed); }` |
| `hardcoded-duration-bypasses-motion-token` | `.fade { transition-duration: 200ms; }` → `.fade { transition-duration: var(--motion-duration-200); }` |
| `hardcoded-easing-bypasses-motion-token` | `.fade { transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1); }` → `.fade { transition-timing-function: var(--motion-easing-ease-in-out); }` |
| `hardcoded-border-width-bypasses-token` | `.card { border-width: 2px; }` → `.card { border-width: var(--border-width-thick); }` |

The repair is a **value → token-reference substitution**: the differing span between `known_bad` and `expected` is the fix (e.g. `#111827` → `var(--text-primary)`), applied at the finding's location. The selector in the pair is illustrative; the transform is selector-agnostic.

The schema already states the discrimination property the smoke tests depend on: "The pair is also the discrimination proof — revert the fix, confirm the conformance-lane finding moves" (`schema.yaml:147-148`). That is round-trip testability built into the data.

**Live-registry note.** These nine are the generic seed layer; the live per-instance registry resolves elsewhere (`seed-corrections.yaml:6-11`) and is never bundled. The repair library for a real engagement is that instance's own registry, read at run time — the seeds are the fallback substrate when no live registry is present.

**The judged / hybrid block (the never-auto set, from the same seed file):** `contrast-pairing-not-declared-safe` (judged, `times_fired: 6`, promotion clause at 3), `token-missing-semantic-role` (judged), `detached-component-instance` (hybrid, `json_artifact`), `arbitrary-value-escape-hatch` (judged). None is auto-applied.

---

## 5. Findings in — the located-finding shape

The loop normalizes every producer into one shape:

```
{ instance, surface, location, drift_kind, drift_class, source_tier, matched_correction?, proposed_transform? }
```

`detection` is deliberately **not** a field of the raw finding — it is a property of a *correction*, so it exists only once `matched_correction` resolves. An unmatched finding carries no `detection` and is proposed. `drift_class ∈ { call-site | token-definition }` routes the write target (§6). `source_tier ∈ { error | warning | suggestion }` (default `error`) records which `ValidationResult` list the finding came from; **only an `error`-tier finding is auto-apply-eligible** — the engine enforces this at the write decision (§5.1, below). `drift_kind` is **informational metadata** carried into the report and the deviation record; the re-validation literal-detector is derived from the *matched correction's* predicate type, not from this field, so a finding's `drift_kind` never has to agree with the resolver for the repair to be correct.

| Producer | Emits | How the loop reads it |
|---|---|---|
| `validate_output` (`heyhi-mcp/heyhi_mcp/core/validator.py`) | `ValidationResult { errors[], warnings[], suggestions[] }` (`:594-596`) over the 9 rules; `artifact_type="rendered_css"` reads emitted CSS via the conformance lane | each `ValidationError` with a `rule` + `location` is a located finding; Rule-1 raw-hex / off-dimension errors match the deterministic seeds; Rule-2 contrast, Rule-5 focus map to judged/gated |
| conformance lane (`heyhi-mcp/heyhi_mcp/conformance/css_check.py`, `check_css`) | `Finding { kind, message, line, column, suggestions }` on emitted CSS | the `_validate_rendered_css` path turns each into a Rule-1 `ValidationError`; the loop reads those |
| DI-audit (`heyhi-design-intelligence-audit/SKILL.md`) | findings with severity + "one concrete next step" (`:581`); the Area-7 conformance sub-area returns a PASS/FAIL floor + CONFORMS/DRIFTS verdict | the sub-area's Axis-1 floor already *is* `validate_output`; its findings arrive pre-located; judgment-axis flags arrive as propose-only |
| a11y audits (`heyhi-a11y-audit/SKILL.md`, `heyhi-a11y-annotation/SKILL.md`) | per-criterion evidence tagged `automated` / `human-reviewed` / `AT-confirmed` (`:71-73`); annotation's three empty designer slots | only `automated`-tier structural defects are repair candidates; everything judged is propose-only or a named-gate slot |

**Intake routing (engine-enforced, not conventional).** Only `errors[]` are auto-apply-eligible. A `warnings[]` entry (Rule 3's sub-44×44 touch-target, "Issues warnings, not errors") is advisory and routes as a **proposal**, never an auto-apply — the engine enforces this via `source_tier`: a `warning`/`suggestion` finding is proposed **regardless of `detection`**, so the guarantee does not depend on the accident that today's warnings happen to map to judged corrections. A `suggestions[]` entry is the validator's own nearest-token hint; it never triggers a repair on its own but supplies the `[inferred]` hint on a proposal. Nothing in `warnings[]` / `suggestions[]` is silently dropped.

**One rule governs intake:** the loop reads the *same deterministic floor* these producers read; it never re-implements detection. In particular it never re-implements contrast math — it reads the floor's contrast result exactly as the a11y-audit does ("Do not re-implement contrast math," `heyhi-a11y-audit/SKILL.md:105`).

---

## 6. The write target (the spec's load-bearing decision)

The write target is chosen **per drift class**, not globally:

| Drift class | Target | Tier | Rationale |
|---|---|---|---|
| Call-site literal (the 9 seeds) | **Code (B)** — the stylesheet/component file where the literal sits | Auto-apply | The `known_bad` → `expected` pair *is* the site-local fix; reversible; unattended-safe |
| Token-definition / value drift (A.1 contrast) | **Token source (A)** — the single DTCG source file | **Propose** (diff for human approval; v1 does not auto-write A) | Propagation-correct (targets one source, not N call-sites), but shared-value blast radius **and** `judged` → human-confirm |
| Anything in Figma | **Canvas (C)** | **Deferred** | App-brokered + human-initiated + create-only Variable guard (`heyhi-design-bridge/SKILL.md`) → cannot host an unattended auto-apply; gated to a later increment |

Two consequences:

- **The token-source path is propose-only in v1 because its members are `judged`, not because A.1 is wrong.** A.1's own contrast fix ends "record the deviation for human confirmation" (`design-fundamentals.md:37`) — A.1 itself proposes-and-records. So v1 auto-applies only where the fix is both mechanical *and* local (target B), and routes the propagation-correct-but-judged fixes to a human (target A, proposed).
- **The "N call-sites vs single source" guard is a correctness rule, not a preference.** When a finding *is* a token-definition problem, the proposed fix targets the one source, never a smear of N patched consumers. When a finding is a call-site literal, the fix is the reference-swap at that site. Targeting a value-fix across N consumers, or a call-site fix into the token source, are both defects.

---

## 7. Provenance and the deviation record

Every loop output carries a provenance label; the vocabulary mirrors the a11y sibling skills so the surfaces read consistently:

- **Applied deterministic repair → `automated`** — attaches only to an *unambiguous* auto-apply. Mirroring `heyhi-a11y-audit/SKILL.md:71`, an automated repair is never a taste approval, exactly as "an automated PASS means 'no automated defect found,' never 'conforms.'"
- **Proposed judged repair → `[candidate: needs confirmation]`** (`heyhi-a11y-annotation/SKILL.md:94`).
- **Anything inferred → `[inferred]`** (`:95`) — never presented as settled. By precondition 1 an inferred token-choice is *proposed*, never auto-applied, so `[inferred]` and `automated` never co-occur on one output.

**The deviation record** (written for every applied repair):

```
{ finding, matched_correction, before, after, surface, location, timestamp,
  provenance: automated, revalidated: true, confirmed: false }
```

It is the human-confirmation queue and the audit trail in one. A.1 requires exactly this for its own contrast case — "record the deviation for human confirmation" — and the loop generalizes it to every applied repair. `confirmed` flips only on a human's review, never on the loop's own re-validation.

---

## 8. The learn write-back seam (spec OQ-3)

When a finding recurs across sessions, the loop's learn step proposes a *new correction* routed to the human-only `corrections-intake/` — never the live registry (`insight-activation/SKILL.md:90`; the firewall is `OPERATING_PRINCIPLES.md § Corrections Intake Protocol`). It never auto-injects and never promotes.

Two things are settled, one is open:

- **Settled — the retrieval home.** These design-drift corrections are *read* from the per-DS design registry, which `retrieve_design_corrections` unions with the audit-method registry (`heyhi-mcp/heyhi_mcp/tools/corrections.py:119-128`; the design corpus is `active_corrections`/enforceable, the method corpus is retrieval-only).
- **Settled for v1 — who authors the repair fields.** The repair loop authors the design-extension fields (`detection`, `predicate`, `known_bad`, `expected`) directly into its intake candidate — a superset of what `insight-activation` emits today (which stops at the base schema `id · category · severity · status · trigger_context · correction · times_fired · last_fired · origin_date`, `insight-activation/SKILL.md:66`). The repair loop is uniquely positioned to know the transform it just applied, so it owns authoring the pair. Recommendation (b) — extending `insight-activation` to carry these fields and routing through it — is the cleaner long-run consolidation, noted, not built.
- **Open — the promotion PATH.** `corrections-intake/README.md` documents promotion only into the root `corrections-registry.yaml` and `method-corrections.yaml`, **neither** the per-DS design registry. How a newly learned areas-7/8 design-drift correction reaches that (live-or-seed, per-deployment) registry is undocumented. This is a promotion-time question behind the human firewall, not a blocker on filing the candidate.

---

## 9. Instance isolation

A tenant repair is judged by the tenant's own system, never HeyHi's. The mechanism exists: `validate_output`'s `constraints` parameter injects the instance's `known_tokens` and `legal_contrast_pairs` via `_build_ctx` → `_ValidationContext` (`validator.py:~756-840`), and an injected instance token set drops HeyHi's legal contrast pairs. The repair loop reads findings produced under the instance's constraints and proposes fixes in the instance's own token vocabulary. No HeyHi token name may appear in a tenant repair. This is Invariant 4 in practice: the design system is reached *through the MCP boundary*, never embedded — the loop calls `validate_output` with the tenant's constraints; it does not carry a copy of anyone's tokens.
