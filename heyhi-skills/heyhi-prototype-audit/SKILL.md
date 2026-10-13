---
name: heyhi-prototype-audit
description: >-
  Audit any HTML prototype for interaction completeness. Stack-agnostic by
  default; layers brand-config-aware checks when active-brand.json is present.
  Triggers: audit this prototype, what interactions are missing, is this ready
  for review, prototype readiness check, interaction gap analysis. Use for any
  prototype regardless of stack — HeyHi-built (ui-studio output, heyhi-ui-ux
  output), client-built, or external. NOT for system-level health checks, token
  drift, or component-code drift — those go to heyhi-design-intelligence-audit.
  NOT for building prototypes (use heyhi-ui-ux for HeyHi production, ui-studio
  Mode A/B/C for client work).
version: "1.1.1"
updated: "2026-10-13"
changes: "v1.1.1 (2026-10-13): Generalized for the Sheerline scaffold: instance data (brand defaults, client/engagement history, owner names, ratified values) moved to instance-only files or neutral wording; method unchanged. v1.1.0 (2026-06-02): Added sixth Layer 2 check — Visual-tell scan (references ai-services/design-intelligence/visual-anti-tells.md AT-1..AT-10); inherits existing PARTIAL_A/FULL gating, additive, never blocks. Source: plans/plan-taste-design-graft.md Graft C. v1.0.0: Initial canonical extraction from a client-engagement prototype-audit skill v1.0 (April 28, 2026) and heyhi-design-intelligence-audit v1.7.0 Prototype Mode (May 1, 2026). Three-layer architecture: Layer 1 stack-agnostic core (six steps), Layer 2 brand-config-aware additive checks (token-fidelity, voice-rule, prohibited-word, layout-pattern, dark-native), Layer 3 Care retainer monthly delta cadence with paired markdown narrative + JSON sidecar baseline. Source plan: plans/track-b-prototype-audit-buildable-2026-05-06.md."
classification: HeyHi Confidential
---

# HeyHi Prototype Audit

This skill audits any HTML prototype for interaction completeness. The output is an honest, sequenced gap analysis that names what works, what does not, and what needs to be built before the prototype meets a stated readiness threshold (stakeholder review, design review, or dev handoff).

The audit is not a scorecard. It diagnoses. The substance is interaction fidelity — what the prototype lets a reviewer do — and the framework is identical for every stack: HeyHi-built (`heyhi-ui-ux` or `ui-studio` output), client-built, or external.

The skill operates in three layers. Each is independently runnable; the layered combination is the full audit.

| Layer | Activation | What it adds |
|---|---|---|
| **Layer 1 — Core** | Always active | Stack-agnostic six-step audit (severity matrix, phased build plan, pre-flight, dispatch template) |
| **Layer 2 — Brand-config aware** | When `active-brand.json` is present at PARTIAL_A or higher | Token-fidelity, voice-rule, prohibited-word, layout-pattern, dark-native, visual-tell scan checks |
| **Layer 3 — Care retainer cadence** | When invoked from `design-system-care-monthly` Step 5g | Monthly delta against prior baseline (paired markdown + JSON sidecar) |

For schema, JSON sidecar shape, and validation rules used by Layer 3, see [`baseline-schema.json`](baseline-schema.json).

---

> **Exit Gate (Flavor A).** This skill closes through the canonical Exit Gate — see `CLAUDE-SESSION-RULES.md § Exit Gate`. Required headers, in order: `## Fixes Applied`, `## Smoke Test`, `## Next Session Prompt`. Empty headers are visible failures.

---

## Routing — disambiguation with sibling skills

Two audit traditions, named entry points. Same severity matrix, same phase model, different subjects.

| Audit question | Skill | Why |
|---|---|---|
| Is this prototype ready to show? What interactions are missing? | `heyhi-prototype-audit` | Interaction completeness — Layer 1/2/3 |
| Is the design system healthy? Where's the drift between Figma and code? | `heyhi-design-intelligence-audit` | System-level health — six examination areas |
| Has anything drifted since last month? Is the system being maintained? | `design-system-care-monthly` | Recurring monitoring cadence |
| Does this Care client's prototype need a delta audit this month? | `design-system-care-monthly` Step 5g → calls `heyhi-prototype-audit` Layer 3 | Care+ extension |

Two skills, one shared origin. Each can call the other when a finding crosses the boundary — system-level findings inside a prototype audit call into design-intelligence-audit; system audits that surface a prototype as the next investigation route into Layer 3.

---

# Layer 1 — Core

*Stack-agnostic. Always active. Lifted substantively from a client-engagement prototype-audit skill v1.0 (April 28, 2026) and heyhi-design-intelligence-audit v1.7.0 Prototype Mode.*

This layer is the audit framework on its own. If `active-brand.json` is absent and no Care cadence is in scope, Layer 1 alone produces a complete audit.

## Step 0: Improvement hook check

Before auditing, if Prototype Mode has been run on this prototype before — or if a prior baseline exists for this prototype family — check: did the severity classification match actual review priorities in the last run? Did any "Medium" item turn out to block the stakeholder decision? Did any "Critical" turn out to be cosmetic?

If the calibration reveals a classification gap, adjust the severity definitions for this run before proceeding. Note the adjustment in the audit output.

Skip this step on the first-ever run against a given prototype.

## Step 1: Load context

Confirm what materials are available before auditing:

- The prototype file (HTML or interactive bundle) — absolute path or URL
- The prototype's functional purpose: what should a reviewer be able to do? What demonstration is the prototype attempting?
- Any prior version, reference implementation, or baseline JSON sidecar for comparison (Layer 3 uses the prior sidecar; Layer 1 alone may use a prior markdown report)
- If a brand config is present in the prototype directory or specified via `--config [path]`, note its location for Layer 2 activation

Do not begin auditing without these four items confirmed. An audit without a stated purpose ranks every gap equally; an audit with a stated purpose surfaces the gaps that block that purpose.

## Step 2: Planning pass

Produce these four outputs before the audit pass:

1. **Scope count** — how many distinct interaction points exist? (Navigable states × directions × row types × action triggers per section.) This is the denominator for the readiness estimate.
2. **Qualitative readiness read** — does the prototype have enough functional interaction to serve its current review purpose? A short paragraph, not a number. Quantitative readiness scoring is deferred.
3. **Priority areas** — which tabs, sections, directions, or interaction surfaces have the highest gap density? Where does an experienced reviewer look first?
4. **Session scope** — which audit phases can complete in one working session? If the prototype is large, scope to one phase per session and name the others as follow-up.

## Step 3: Audit pass — three-pass severity framework

For each gap, document in this exact format:

```
### [Gap ID] — [Short title]
**Severity:** Critical / High / Medium
**Type:** Cross-cutting / Direction-specific / Component-specific
**Current:** [What exists — specific to the prototype source]
**Required:** [What it should do — written from the user/reviewer perspective]
**Implementation:** [Concrete code or pseudocode — verified against actual selectors and identifiers in Step 5]
```

**Severity definitions:**

| Tier | Prototype meaning |
|------|-------------------|
| Critical | Core workflow cannot be demonstrated. The prototype fails at its primary job. |
| High | Mechanical step works but produces no feedback. Reviewer guesses whether the action was accepted. |
| Medium | Visible only under scrutiny or edge cases. Does not block stakeholder understanding. |

**Classification:**

- **Cross-cutting** — Same gap appears across multiple components, tabs, or directions. Fix once, apply everywhere.
- **Direction-specific** — Affects one direction or flow but multiple components within it.
- **Component-specific** — Isolated to one component, direction, or tab. Document per location.

**Sequence:** Cross-cutting before direction-specific before component-specific. Critical before High before Medium. The audit pass is not finished until every gap carries severity, classification, and the five-field block above.

## Step 4: Build plan output

Output file: `[workspace]/research/prototype-audit-[name]-[YYYY-MM-DD].md` for one-off audits. For Care engagements, see Layer 3 output paths.

| Phase | Tier | Contents |
|-------|------|----------|
| 1 — Foundation | Cross-cutting Critical | Shared architecture, delegated handlers, global state, foundational selectors |
| 2 — Critical | Direction-specific or component-specific Critical | Core workflow demonstration per direction |
| 3 — High | High severity (any classification) | Feedback states, selection indicators, auto-checks |
| 4 — Polish | Medium | Animation, edge cases, empty states |

**Readiness thresholds:**

- Phases 1–2 complete → Stakeholder-ready (concept can be evaluated)
- Phases 1–3 complete → Design review-ready (full feedback cycle)
- All four phases complete → Handoff-ready spec

These thresholds are calibrated against reference implementations (a client-engagement prototype, April 27–28, 2026 — 21 items, 41/41 smoke test, 1 pre-flight defect caught). Validate the thresholds against the current prototype's review purpose; refine the calibration after each run via Step 0.

## Real-user validation — NEEDS HUMAN

A readiness threshold above is an interaction-completeness state, not a user-validated one. This output reflects the interaction-completeness and readiness review this audit performs, not a test with a real, naive end user: "Design review-ready" and "Handoff-ready spec" mean the prototype demonstrates its interactions, not that a real user has tried it and succeeded. Whether that gap matters for this review, and who would run a Sponsor-User check-in or a small moderated test (the Design Sprint Friday-test shape) if it does, is not this skill's call — see operating-principles.md "What stays human."

```
Real-user validation run?  yes / no / not-applicable: ____________________
If yes, by whom and how:   ____________________
```

## Step 5: Pre-flight verification

Before dispatching or executing the build plan: verify every CSS selector, JS identifier, DOM traversal path, and file path against the actual prototype source.

For each item in the plan:

1. Open the prototype source file at the cited path. Confirm the file exists.
2. For every selector in the implementation block, run a search on the source and confirm the selector matches actual elements.
3. For every JS identifier (event handler, function name, state key), confirm the identifier exists or that the plan correctly creates it.
4. For every DOM traversal path (`closest()`, `querySelector` chains, parent/child walks), confirm the path resolves against the actual DOM structure.

Document corrections in the audit output: "Plan contained X; correct form is Y; reason: Z."

A plan with an unverified code element is not yet a plan — it is a draft. Do not dispatch a draft.

## Step 6: Dispatch prompt template

If the build will happen in a future session — by another agent, by the human owner, or by an engineering handoff — produce a self-contained dispatch prompt using this template:

```
MISSION: [Goal in one sentence — what should be built, not what was reviewed]
PROTOTYPE FILE: [absolute workspace path]
PLAN FILE: [absolute workspace path to the audit output from Step 4]
PRE-FLIGHT RESOLUTIONS: [list every ambiguity resolved in Step 5 — selectors corrected, paths verified, identifiers confirmed]
BUILD SEQUENCE: Phase 1 (Foundation) → Phase 2 (Critical) → Phase 3 (High) → Phase 4 (Polish)
  See plan file for phase contents.
FIRST ACTION: [exact instruction — which file to open, which phase to start, which item is first]
SMOKE TEST: [one check per Critical item minimum — expected DOM state or output condition; structural and string-presence tests preferred]
```

The dispatch prompt is the third artifact of the audit. The audit produces three things: the audit report (Steps 3–4), the improvement plan (Step 4 output), and this dispatch prompt (Step 6). Together they let any agent or operator pick up the work without reconstructing the audit context.

---

# Layer 2 — Brand-config aware

*Activates as additional checks when a brand config exists at PARTIAL_A capability tier or higher. Mirrors the MCP-available / MCP-not-available branching pattern already in `heyhi-design-intelligence-audit` and `design-system-care-monthly`.*

## Activation rule

Layer 2 runs when **either** condition holds:

1. The audit is invoked with a config path argument (`--config [path]`)
2. The prototype's directory or any ancestor directory contains a `brand-config/active-brand.json`

Before running any Layer 2 check, call:

```bash
python3 heyhi-skills/ui-studio/scripts/validate.py --config [path] --status
```

Inspect the return:

- **Validation passes, completeness ≥ 70 and fidelity ≥ 60 (PARTIAL_A or FULL):** All six checks run.
- **Validation passes, completeness 50–69 (MODE_B):** Token-fidelity, voice-rule, prohibited-word, and dark-native run. Layout-pattern and visual-tell scan defer with logged reason ("config below PARTIAL_A; layout pattern and visual-tell scan require fidelity ≥ 60").
- **Validation passes, completeness 30–49:** Token-fidelity (best-effort) and voice/prohibited-word checks run; layout-pattern, dark-native, and visual-tell scan defer.
- **Validation fails for any reason — file missing, malformed YAML/JSON, schema violation, completeness < 30 (HARD_STOP):** Layer 2 is skipped entirely. Audit continues with Layer 1 only. Add a logged reason to the audit output: `Layer 2 skipped: [validation failure detail]`.

The audit is not blocked by Layer 2 unavailability; Layer 2 is additive. Never invent config values to make a check run.

## Layer 2 checks

**Token-fidelity check.** For each color, spacing, typography, and motion value used in the prototype source: is the value within the config's palette/scale, or is it a hardcoded literal where a config token exists? Hardcoded hex values, magic-number paddings, or off-scale font sizes where a config token is available become findings (severity: Medium for cosmetic; High when the literal undermines a design intent named in the config).

**Voice rule check.** Does prototype copy follow `voice.tone` from the config? If the prototype is audience-facing, em-dash count check applies (the config carries the per-document budget — usually 2 per document, but config-determined). Tone deviations (e.g., config says "grounded, precise" but prototype copy reads as "playful, exclamatory") become findings at severity Medium unless they actively confuse the reviewer.

**Prohibited-word scan.** Direct application of `voice.prohibited_words` against any visible copy in the prototype (button labels, headings, tooltips, microcopy, error states). Each occurrence is a finding at severity High when the word is in a primary CTA or heading; Medium otherwise. The check runs against rendered text, not raw HTML — comments and inline notes are excluded.

**Layout pattern compliance.** Are layout patterns used in the prototype drawn from `layout.preferred_patterns`? Departures noted as findings; classification depends on Mode (Mode A departures are defects, Mode B/C departures are intentional and logged for review without severity escalation). The check inspects grid systems, section spacing density, and component arrangement — not pixel values.

**Dark-native handling.** When `meta.default_scheme` is `dark`:

- Contrast checks run against dark background tokens, not white. Use the config's specified dark surface tokens as the contrast denominator.
- Light-scheme adaptation warning included if the prototype provides no light-scheme alternative and the engagement scope includes both schemes.
- Default colorway in copy and visuals matches the config's `default_scheme`. A prototype with `meta.default_scheme: dark` that shows a light hero is a finding at severity High.

**Visual-tell scan.** Scans the rendered prototype for the visual anti-tells catalogued in [`ai-services/design-intelligence/visual-anti-tells.md`](../../ai-services/design-intelligence/visual-anti-tells.md) (AT-1 through AT-10): neon / outer-glow shadows (AT-1), gradient text on large headers (AT-2), oversaturated accents (AT-3), three-equal-column card rows (AT-4), decorative overlapping elements (AT-5), custom cursors (AT-6), fabricated metrics / fake system data (AT-7), broken image links (AT-8), filler prompt copy (AT-9), generic placeholder names (AT-10). Each catalog entry carries a carve-out: a finding fires only when the pattern matches **and** no documented carve-out applies — a deliberately electric brand accent documented in the config (a brand's own documented saturated accents must not trip AT-3), or obvious WIP placeholders in an interaction-only prototype (AT-7, AT-8, AT-10). Severity mirrors the existing Layer 2 scheme: High when the tell appears in a primary hero or CTA surface, Medium otherwise. Cite each finding by catalog ID (AT-n) so it traces to a named rule and its carve-out, not a copy-pasted description. This check is config-coupled (the carve-outs need the config to tell an intentional electric accent from a generated oversaturated one), so it runs at PARTIAL_A / FULL alongside the layout-pattern check and defers below threshold with a logged reason. Like every Layer 2 check, it is additive — it never blocks the audit.

**Component vocabulary check (Layer 2.5, optional).** When a component inventory exists in the config, check whether prototype elements reference real components from the inventory or invent equivalents (e.g., a custom card that duplicates `card-medium` from the inventory). This bridges toward repository-aware territory but stays a flag, not a refusal — the prototype audit does not validate against a live component registry. Severity: Medium. Findings here often surface the question "should this be promoted to the inventory?" — note that question alongside the finding.

## Layer 2 output integration

Layer 2 findings join the Layer 1 audit output under their corresponding severity tier in Step 3. The Step 4 build plan includes Layer 2 findings in the same phased structure (Foundation/Critical/High/Polish). The audit output explicitly notes which findings came from Layer 2 ("Layer 2 finding — token-fidelity"; visual-tell findings are labeled "Layer 2 finding — visual-tell AT-n"); a reader skimming the report can see how much of the gap density is config-coupled versus framework-level.

---

# Layer 3 — Care retainer cadence

*Activates as a Care+ tier dimension when invoked from `design-system-care-monthly` Step 5g. Output structure follows the existing Care monthly conventions (paired markdown narrative + JSON sidecar at `<engagement folder>/deliverables/care/`).*

## Baseline preservation

Month 1 establishes two paired files:

- `<engagement folder>/deliverables/care/prototype-audit-baseline-[YYYY-MM].md` — human-readable narrative report
- `<engagement folder>/deliverables/care/prototype-audit-baseline-[YYYY-MM].json` — structured sidecar

The JSON sidecar is the machine-comparable input for Month 2+ delta detection. It carries gap IDs, severities, classifications, and phase assignments in a flat schema (see `baseline-schema.json`). The markdown is what a human reads; the JSON is what the next month's audit diffs against.

This is the same dual-artifact pattern as the Care monthly cycle's `figma-manifest-[YYYY-MM].json` plus its narrative report, and the same pattern as `baseline-[YYYY-MM].json` for token drift.

## Delta audit format

For Month 2 onward, the audit produces:

- `<engagement folder>/deliverables/care/prototype-audit-[YYYY-MM].md` — narrative
- `<engagement folder>/deliverables/care/prototype-audit-[YYYY-MM].json` — structured sidecar (becomes next month's baseline)

The narrative includes these sections:

1. **Gaps closed since last cycle** — Gap IDs from the prior baseline that are no longer present in the current audit, with one-line confirmation of how each was resolved.
2. **New gaps surfaced this cycle** — Gap IDs present in the current audit but not in the prior baseline.
3. **Severity-bucket movement** — Counts of items that moved tiers (Critical→High, High→Medium, etc.). Aggregated and itemized.
4. **Stakeholder-readiness threshold movement** — Position relative to Phase 1–2, Phase 1–3, all-four thresholds. Did the prototype move closer to or further from stakeholder-ready / design-review-ready / handoff-ready?

Computed by diffing the current month's gap-list JSON against the prior month's sidecar JSON. The diff is structural, not textual — gap IDs are stable across cycles.

## First-cycle handling

If no prior baseline exists, run the full Layer 1 + Layer 2 audit and store as the baseline. Note in the monthly report:

> *First prototype audit cycle. Baseline established from current prototype state. Subsequent cycles will report deltas against this baseline.*

Do not attempt to compute a delta against a baseline that does not exist. The first cycle is always a snapshot.

## Schema and validation

Every Layer 3 output (both first-cycle baseline and subsequent monthly deltas) writes a JSON sidecar that conforms to `baseline-schema.json`. Before writing, validate:

```bash
python3 -c "import json, jsonschema; jsonschema.validate(json.load(open('[output-path].json')), json.load(open('heyhi-skills/heyhi-prototype-audit/baseline-schema.json')))"
```

A sidecar that fails validation is not written. The schema is versioned (`schema_version: "1.0"`); future audits can extend it (adding fields is non-breaking; renaming is breaking).

## Integration into Care report

Layer 3 contributes a single summary line to the monthly Care report (`design-system-care-monthly` Step 6 output):

> *Prototype audit ([prototype name]): [N gaps closed], [M new gaps], [readiness threshold: e.g., "now stakeholder-ready" or "still design-review pending"].*

The full delta narrative lives in its own file (`prototype-audit-[YYYY-MM].md`) and is linked from the Care report.

---

## What stays specific to a calling skill (does not move into Layer 1)

The following elements remain in the calling skill's wrapper or overlay because they encode caller-specific conventions:

- Default prototype paths (e.g., a client wrapper names its product's prototype file; HeyHi uses prior `heyhi-ui-ux` outputs)
- Caller-specific context files (a client wrapper: the product's context and product-intelligence files; HeyHi: HeyHi brand context)
- Stakeholder-readiness language tuned to the engagement (a client wrapper: the client's named reviewers; HeyHi engagements: per-client review chain)
- Reference implementation calibration baselines (a client wrapper: its own reference implementation; HeyHi: per-engagement reference)

These elements live in the wrapper. Layer 1 carries the framework; the wrapper carries the engagement-specific overlay.

---

## What is explicitly out of scope

To keep the audit cohesive:

- **Prototype building.** Use `heyhi-ui-ux` for HeyHi production pages, `ui-studio` Mode A/B/C for client work, a client's own prototype-authoring wrapper where one exists, or a Track A skill if and when one ships.
- **System-level token health, component coverage, or Figma file health.** Use `heyhi-design-intelligence-audit`.
- **Design system monthly maintenance.** Use `design-system-care-monthly` directly.
- **Repository-aware component validation.** Track A territory. This skill may flag low-confidence component references as findings (Layer 2.5) but does not validate against a live component registry.

---

## Smoke tests for the audit output

When this skill produces an audit, the output should pass these self-checks before being declared complete:

- The audit file exists at the expected path (`research/prototype-audit-[name]-[YYYY-MM-DD].md` for one-off; `<engagement folder>/deliverables/care/...` for Layer 3).
- Every gap carries severity, classification, current/required/implementation, and is sequenced by Cross-cutting → Direction-specific → Component-specific within each severity tier.
- The phased build plan has at least one item in Phase 1 (Foundation) when any cross-cutting Critical exists.
- Step 5 pre-flight section enumerates every selector, JS identifier, and DOM path with a Verified/Corrected status.
- The dispatch prompt template (Step 6) is filled out with concrete first-action and at least one smoke test per Critical.
- Layer 2 status block names which checks ran and which were skipped with reason (the six checks: token-fidelity, voice-rule, prohibited-word, layout-pattern, dark-native, visual-tell scan).
- Layer 3 (when applicable) writes both the markdown narrative and the JSON sidecar; the sidecar validates against `baseline-schema.json` before write.
- The real-user-validation slot is present with its run-line blank — the readiness threshold is an interaction-completeness state, never a claim that a real user tried it.

---

## Exit Gate Required Headers (bottom-of-skill bracket)

This skill closes through the Exit Gate Flavor A (`CLAUDE-SESSION-RULES.md § Exit Gate`). Before declaring done, confirm every required header below contains real content, not a claim:

- `## Fixes Applied`
- `## Smoke Test`
- `## Next Session Prompt`

If any header is empty or contains advisory prose ("I checked for bugs") instead of a concrete artifact, the gate has not been satisfied. Apply fixes until clean — then emit.

---

*HeyHi Confidential.*
*Canonical prototype audit skill. Source plan: `plans/track-b-prototype-audit-buildable-2026-05-06.md`. Generalized from a client-engagement prototype-audit skill v1.0 (April 28, 2026) and `heyhi-design-intelligence-audit` v1.7.0 Prototype Mode (May 1, 2026).*
*v1.1.0 (2026-06-02): Visual-tell scan added to Layer 2 per `plans/plan-taste-design-graft.md`.*
