---
name: design-system-care-monthly
description: >-
  Execute the monthly Design System Care retainer deliverable for a client.
  Use when the user says "run the monthly care," "Design System Care for [client],"
  "monthly audit for [client]," "token drift check," "component audit,"
  "monthly report," "care cycle for [client]," or any reference to executing the
  recurring monthly Design System Care work. This skill produces a consistent
  monthly deliverable: token drift check, component audit, documentation review,
  and a monthly report stored in the client's workspace. Works for both Care and
  Care+ tiers. NOT for a one-time Design Intelligence Audit (use
  heyhi-design-intelligence-audit for that) and NOT for building or rebuilding a
  design system (use ui-studio or a Build engagement for that).
version: "1.7.1"
updated: "2026-10-13"
changes: "1.7.1 (2026-10-13): Generalized for the Sheerline scaffold: instance data (brand defaults, client/engagement history, owner names, ratified values) moved to instance-only files or neutral wording; method unchanged. The G-W4 adoption contract stays the instance's ratified record at its canonical path; a scaffold export ships an unratified slot in its place. 1.7.0 (2026-09-14): Added Step 5i — Production-Code Adoption Scan (Care+ tier), promoting Sheerline W4 sub-spec (a) from skill-updates/ per PROMOTION.md. Wraps the Tier-1 static adoption scanner (heyhi-mcp/heyhi_mcp/adoption/) in the Care cadence: reads a client frontend repo, records an immutable dated read, computes the month-over-month '% on system' delta with its mandatory override counter-metric and drift concentration. Ships NO default drift threshold (grades never gates); a client-facing figure is gated on the G-W4 metric-definitions contract once an instance ratifies it (references/adoption-definitions-contract.md, v1.0.0). Step 0 gains an adoption_scan intake question + flag paragraph; Care+ tier table + Integration Points updated. Scanner, schema, and self-test live in heyhi-mcp. Skill count unchanged (a step within an existing skill). Source: plans/plan-sheerline-adoption-and-reach-2026-09-12.md; G-W4 approved by the instance owner 2026-09-14. 1.6.0 (2026-09-07): Added the forward-deployed-loop Care steps (Lane I / DISPATCH-10). Step 1b (recon delta) runs the deployed app-recon in delta mode against a stored baseline commit to detect what changed in an application in loop scope, without re-reading unchanged surfaces. Step 3b (pattern ledger review) reads retrieve_application_context scope patterns and files a pattern-intake/ candidate for each local pattern whose promotion_signal is true; it flips no ledger status (the human does, through the promotion pass). Step 5e rewritten from the Tier 3 bidirectional canvas loop to a concrete artifact re-sync through the promoted feature-increment in update mode (dependency-gated on Lane F). Step 7 baseline now also stores the application manifest snapshot, the pattern-ledger snapshot, and the ds-map coverage snapshot. Step 6 gains a Per application report section. Step 0 gains an application_loop intake question, flag paragraph, and Care+ tier-table row that gate steps 1b, 3b, and 5e. The pattern-intake/ convention (README + candidate template) is created alongside this update. Source: plans/plan-sheerline-fdde-loop-2026-09-07.md § 3.1 Care row. 1.5.0 (2026-09-01): Added Step 5h — Agent Conformance Audit (Care+ tier). Wraps the per-sample conformance engine (heyhi-mcp/heyhi_mcp/conformance/) in the Care cadence: reads an agent-authored output corpus, records an immutable dated conformance read, and computes the month-over-month delta (trajectory, top drifting classes, regressed samples). Ships NO default drift threshold — the load-bearing call is authored per engagement (grades never gates). Step 0 gains an agent_conformance intake question + flag paragraph; Care+ tier table and Integration Points updated. Engine, schema, and self-test fixture live in heyhi-mcp. Source: plans/plan-agent-conformance-care-surface-2026-08-30.md. 1.4.0 (2026-06-16): Token drift check now runs scripts/compute_drift.py for a deterministic numeric manifest diff (changed/added/removed/total schema); only the structured diff is passed to the model for interpretation — never both full manifests in context. Changelog line reconstructed 2026-07-04 from git history (the bump shipped without one). 1.2.0: Added search_design_system to Step 3 (component audit — cross-library discovery, Care+ path). Added Step 5e: Bidirectional Canvas Loop (use_figma write operations, Care+ Tier 3). Added Step 5f: Figma Skills Maintenance (monthly Skill file review, Care+ deliverable). Updated Step 6 report to include Skills maintenance section. 1.3.0: Added Step 5g — Prototype Health Audit (Care+ tier). Loads heyhi-prototype-audit Layer 3 for monthly delta audits when prototypes are in engagement scope. Step 0 updated with prototype_audit flag check and intake discovery question; Care+ tier table updated with Step 5g entry; Integration Points table now references heyhi-prototype-audit. Source: plans/track-b-prototype-audit-buildable-2026-05-06.md."
---

# Design System Care: Monthly Cycle

This skill runs the monthly Design System Care retainer deliverable. It produces a consistent, compounding monthly cycle: check what drifted, audit what changed, update what's stale, and report what matters.

The monthly cycle is lighter than a full Design Intelligence Audit. It examines the same six dimensions from the maturity model, but at a monitoring cadence, not a diagnostic one. The full audit finds the problems. The monthly cycle keeps them from coming back.

For report templates, checklist details, and month-over-month comparison format, see [reference.md](reference.md).

---

> **Exit Gate (Flavor A).** This skill closes through the canonical Exit Gate — see `CLAUDE-SESSION-RULES.md § Exit Gate`. Required headers, in order: `## Fixes Applied`, `## Smoke Test`, `## Next Session Prompt`. Empty headers are visible failures.


## Step 0: Determine Context

Before starting, establish:

**Client identity.** Which client? Check the instance's engagement folder for this client (written `<engagement folder>/` below) for the engagement brief, contract, or kickoff notes. If the client workspace doesn't exist yet, ask the instance owner: "Do we have a workspace set up for this client?" The engagement brief is helpful context but not required to start the monthly cycle.

**Tier.** Care or Care+? This determines scope. If unknown, ask: "Is this a Care or Care+ engagement?" Also ask: "Does the engagement include prototype maintenance? If yes, list the prototypes in `care-config.yaml` under `prototype_audit.prototypes`." This intake question covers the Prototype Health Audit (Care+) add-on. Also ask: "Does the engagement include an agent-authored output stream — generated components, MCP-App bundles, or PRs from agents building against the system? If yes, name the corpus in `care-config.yaml` under `agent_conformance.corpus`." This intake question covers the Agent Conformance Audit (Care+) add-on. Also ask: "Is an application in the forward-deployed loop part of this engagement, so the design system is read from and built into a live application and its Figma artifact each cycle? If yes, set `application_loop.enabled: true` in `care-config.yaml` and record the frontend repositories and the last recon baseline commit under it." This intake question covers the forward-deployed-loop steps (1b, 3b, 5e), a Care+ add-on. Also ask: "Does the engagement include codebase access for an adoption reading — can we scan the frontend repo? If yes, set `adoption_scan.enabled: true` in `care-config.yaml` and name the codebase, the config, and a stable `corpus_id` under it." This intake question covers the Production-Code Adoption Scan (Step 5i), a Care+ add-on.

| Tier | Monthly scope |
|------|--------------|
| **Care** | Token drift check, component audit, documentation review, monthly report |
| **Care+** | Everything in Care, plus: new component needs scan (with `search_design_system` cross-library discovery), Figma sync status, accessibility regression check, Code Connect gap detection and maintenance, maturity dimension tracking, Figma Skills Maintenance, Bidirectional Canvas Loop (Tier 3, if in scope), Prototype Health Audit (Step 5g, when `prototype_audit.enabled: true`), Agent Conformance Audit (Step 5h, when `agent_conformance.enabled: true`), Forward-Deployed Loop steps (1b recon delta, 3b pattern ledger review, 5e artifact re-sync, when `application_loop.enabled: true`), Production-Code Adoption Scan (Step 5i, when `adoption_scan.enabled: true`) |

**Prototype Health Audit add-on (Care+, conditional).** If `prototype_audit.enabled: true` is present in `<engagement folder>/care-config.yaml`, Step 5g runs as part of the cycle. If absent or false, Step 5g is skipped. The flag is set during engagement intake when the discovery question above is answered yes; do not infer the flag from the presence of HTML files in the client workspace. See `heyhi-prototype-audit/SKILL.md` Layer 3 for the full execution model.

**Agent Conformance Audit add-on (Care+, conditional).** If `agent_conformance.enabled: true` is present in `<engagement folder>/care-config.yaml`, Step 5h runs as part of the cycle. If absent or false, Step 5h is skipped. The flag is set during engagement intake when the discovery question above is answered yes; do not infer it from the presence of generated CSS or MCP-App bundles in the workspace. See Step 5h and `heyhi-mcp/heyhi_mcp/conformance/trend.py` for the full execution model.

**Production-Code Adoption Scan add-on (Care+, conditional).** If `adoption_scan.enabled: true` is present in `<engagement folder>/care-config.yaml`, Step 5i runs as part of the cycle. If absent or false, Step 5i is skipped. The flag is set during engagement intake when the discovery question above is answered yes; do not infer it from the presence of a frontend repo in the workspace. A "% on system" figure reaches a client-facing report only after the G-W4 metric-definitions contract is ratified. See Step 5i and `heyhi-mcp/heyhi_mcp/adoption/trend.py` for the full execution model.

**Forward-Deployed Loop add-on (Care+, conditional).** If `application_loop.enabled: true` is present in `<engagement folder>/care-config.yaml`, Steps 1b (recon delta), 3b (pattern ledger review), and 5e (artifact re-sync) run as part of the cycle. If absent or false, all three are skipped and the standard Care flow is unaffected. The flag is set during engagement intake when the discovery question above is answered yes; do not infer it from the presence of a repository or a Figma file in the workspace. The block records only what the loop steps need to locate the application; the artifact file key and the served application context stay in the per-system instance and the gitignored engagement folder, never in `care-config.yaml`:

```yaml
application_loop:
  enabled: true
  repos:
    - path-or-name-of-frontend-repo       # app-recon delta reads these (Step 1b)
  baseline_commit: <sha>                  # last cycle's recon baseline; Step 1b runs app-recon --since this
```

These three steps read the application through the per-system heyhi-mcp instance (`retrieve_application_context`) and the deployed `app-recon` skill, never a manifest, contract, or DESIGN.md file loaded from disk as a spec. See Steps 1b, 3b, and 5e for the execution model.

**Month number.** Is this Month 1 (first cycle) or a subsequent month? Month 1 establishes the baseline. Every month after compares against it.

**Previous baseline.** If Month 2+, load the previous month's baseline from `<engagement folder>/deliverables/care/baseline-[YYYY-MM].json`. If no baseline exists, this is effectively Month 1 regardless of what the calendar says.

**Figma MCP availability.** Confirm whether a Figma MCP server connection is active in this session (tools present: `get_variable_defs`, `get_design_context`, `get_code_connect_map`, `get_code_connect_suggestions`). Note the client's Figma plan tier: Professional plan + Developer seat required for `get_variable_defs`; Enterprise/Org plan + Developer seat required for Code Connect tools. MCP availability determines which path runs in Steps 1, 2, 3, 5a, and 5d.

---

## Step 1M: Mode D Provisional Config Check

*Runs before any other step. Skip this if the config is from any other source (existing system, Mode A/B/C).*

When the client's brand config was generated via Mode D (moodboard-driven), check before running the monthly cycle:

**1. Read `meta.generated_by`.** If it contains "mode-d" but NOT "mode-d-v1", this is a provisional config.

**2. If provisional (mode-d, not mode-d-v1):**
   - Do NOT run the standard monthly drift check. There is no baseline to drift from yet.
   - Instead, check: is the designer review protocol complete? (Look for `meta.provisional_fields` — if empty and `meta.generated_by` is "mode-d-v1", proceed normally to Step 1.)
   - If provisional fields remain in `meta.provisional_fields`: stop and ask the instance owner:

     > "The brand config for [client] is still in Mode D v0 (provisional). The designer review protocol needs to complete before we can run the monthly care cycle. Should we trigger the designer review now?"

   - If yes: generate the designer handoff artifact using the template at `heyhi-skills/ui-studio-onboard/templates/designer-handoff-artifact.md`. Auto-generate if `confidence: failing` fields exist; offer for provisional/inferred only. Write as `[client-name]-token-review-[date].md`.
   - Do not proceed past this point until the config is promoted to v1.

**3. If the config is "mode-d-v1":**
   - This is the first monthly cycle. There is no previous baseline to compare against.
   - Proceed to Step 1 (load config normally).
   - Note in the monthly report (Step 6): "First cycle. Baseline established from Mode D v1 config dated [date]."

**What provisional means for care:**
A Mode D v0 config is a design intent document, not a validated system. Running drift detection against it would flag legitimate design exploration as drift. The designer review protocol ensures that v0 fields are confirmed before care begins. Wait for v1.

**If `meta.generated_by` is NOT "mode-d" or "mode-d-v1":**
   - This is not a Mode D config. Proceed normally to Step 1.

---

## Step 1: Load the Client's Brand Config

Load the client's brand configuration from `active-brand.json`. If no config exists, run `ui-studio-onboard` to generate one first — the monthly care cycle cannot run without a configured brand.

**Live refresh (Figma MCP available):** Use `get_variable_defs` against the token library `file_key` to refresh token state before proceeding. Gives you the freshest data.

**Cached:** Read the client's `active-brand.json` directly. Use this path when MCP is not available.

**Which mode?** Ask: "Is there a Figma MCP connection available for this client?" If yes, refresh live. If no, use the cached config. If no config exists at all, stop and run `ui-studio-onboard` to generate one. Ask the instance owner: "The brand config isn't set up for this client. Should we run ui-studio-onboard first?"

Extract and hold:
- Current token set (all categories: color, spacing, typography, elevation, motion)
- Component inventory (what exists, what props and variants)
- Voice rules (for the report)
- Repository URLs (token repo, component repo)

**If Figma MCP is available (Professional plan + Developer seat):** After loading the brand config, extract the current variable manifest via `get_variable_defs`. Store as `figma-manifest-[YYYY-MM].json` in `<engagement folder>/deliverables/care/`. This becomes the source of truth for the MCP drift path in Step 2. For Month 1, this file establishes the Figma-side baseline. For Month 2+, diff against the previous month's `figma-manifest-[YYYY-MM-1].json`.

---

## Step 1b: Recon Delta (Care+, when the application loop is in scope)

*Skip this step unless `application_loop.enabled: true` is set in `<engagement folder>/care-config.yaml`. This is the read half of Care's forward-deployed loop: it detects what changed in the application since last cycle so Steps 3b and 5e act on real deltas, not on what someone remembers changed.*

When an application is in the forward-deployed loop, the design system is read from and built into a live application each cycle. Before the token and component work below, run the recon delta so the cycle knows which application surfaces moved. This step calls the deployed `app-recon` skill; it does not re-implement the read.

**Execution.** For each repository in `application_loop.repos`:

1. **Locate the baseline.** Read `application_loop.baseline_commit` from `care-config.yaml` (the recon baseline stored at the end of last cycle, Step 7). For Month 1, or when no baseline commit exists, there is no delta to compute: run the full `app-recon` read instead and store its manifest as the first baseline. Do not compute a delta against a baseline that does not exist.

2. **Run the delta read.** Run `app-recon` in delta mode: `app-recon --since <application_loop.baseline_commit>`. Per that skill, delta mode runs `git diff --stat <baseline>..HEAD` read-only, re-recons only the surfaces that changed, and emits an `app-manifest.json` with `source_commit` bumped to the new HEAD and the baseline recorded in the brief. It never re-reads unchanged surfaces and never mutates any repository.

3. **Read the result through the instance.** The manifest is served through the per-system heyhi-mcp instance (`retrieve_application_context` scope `manifest`). `app-recon` writes it to the served data dir or the gitignored engagement folder, never a tracked file. Do not load a manifest file from disk as a spec.

4. **Honor the app-recon gate.** `app-recon`'s own named gate is the brief review: no downstream Care step consumes the delta manifest until a human has signed the brief. Carry forward the changed surfaces, the `unverified[]` list, and the new HEAD commit (the next baseline) for the report and for Step 5e.

5. **Merge across repositories.** When `application_loop.repos` names more than one repository, run the delta per repository and keep each repo's changed surfaces separate in the report; the manifest is per repository, so do not conflate two repositories' surfaces under one id. A monorepo with several app roots is one repository with several `container_dir` roots, still one manifest.

**The quiet cycle.** If `app-recon` reports no changed surfaces since the baseline, that is a real result, not a gap: record "no application change this cycle" in the per-application report, still advance the baseline commit (Step 7), and let Step 5e skip this application (nothing landed to re-sync). Do not force a full re-read to manufacture findings.

**Empty slots (human):** which changed surfaces are in scope for this cycle's artifact re-sync (Step 5e); the recon tier when `app-recon`'s precedence rule does not decide it; every `unverified[]` item app-recon could not ground. **Named gate:** the `app-recon` brief review.

**Output:** the delta manifest (served, not tracked) and a recon-delta summary line for the per-application report section (Step 6): surfaces changed, endpoints changed, `unverified[]` count, new baseline commit. Advisory; renders no verdict.

**Reference:** `heyhi-skills/app-recon/SKILL.md` (delta mode, `--since <commit>`, the brief-review gate).

---

## Step 2: Token Drift Check

Compare the current token state against last month's baseline.

**Path selection:**
- **MCP path (Figma MCP available), preferred when a code-execution layer is present:** Extract the current variable state via `get_variable_defs` and write it to `figma-manifest-[YYYY-MM].json`. Then run the deterministic diff in code rather than comparing two full manifests in context:
  ```
  python3 scripts/compute_drift.py figma-manifest-[YYYY-MM].json figma-manifest-[YYYY-MM-1].json
  ```
  (For Month 2+ the baseline may be `baseline-[YYYY-MM].json → figma_variable_manifest`.) `compute_drift()` returns a structured diff: `changed` (key, previous, current), `added`, `removed`, `total_current`, `total_baseline`, `drift_detected`. Pass only that diff to the model for interpretation and the report section. Do **not** load both full manifests into context; the diff is the payload. A numeric diff is deterministic: it catches small, precise value changes that an in-context comparison of two large manifests can miss, and it collapses the both-datasets-in-context cost to the size of the delta. See [reference.md](reference.md) § Drift Log Format for the `compute_drift.py` output schema.
- **MCP path, fallback (no code-execution layer):** Diff the variable manifest against `figma-manifest-[YYYY-MM-1].json` in context. Changes are exact: specific variable names, old values, new values, and which direction drifted (Figma vs. code). Example output format:
  ```
  CHANGED: color/brand/primary
    Figma: oklch(65% 0.22 250)  →  oklch(60% 0.25 240)
    Code:  oklch(65% 0.22 250)  (unchanged — Figma drifted, code didn't)

  ADDED in Figma: spacing/component/card-padding-compact
    Code: not found

  REMOVED from Figma: color/feedback/warning-subtle
    Code: still present
  ```
  This transforms the drift check from "we believe tokens drifted" to "here are the specific variables that changed." The monthly report becomes machine-verifiable.
- **Standard path (Mode A/B, no MCP):** Proceed with the existing token comparison against the code repository, as described below.

**What to check (standard path):**

- **Added tokens.** New tokens that weren't in last month's set. Are they named semantically? Do they follow the existing hierarchy?
- **Removed tokens.** Tokens that existed last month but are gone. Were they deprecated properly or just deleted?
- **Changed values.** Tokens whose resolved values changed. Determine intent by: (1) checking Git commit history for the change, (2) asking the team if unclear, or (3) noting "intent unclear" when neither source is available. This helps distinguish accidental drift from intentional brand updates.
- **Naming violations.** Run the naming convention check against any new or changed tokens. Pattern: `{category}-{role}-{modifier}`. Examples of passing names: `color-action-primary`, `spacing-layout-md`, `font-size-body`. Examples of violations: `blue-500`, `lg-margin`, `#222222`. Group violations by category (color, spacing, typography, etc.) and note patterns. For instance: "Color tokens follow semantic naming, but spacing tokens use numeric appearance-based names."
- **Hardcoded values.** Sample 15-20 components in the codebase (or audit all if fewer than 20 exist). Prioritize: recently modified, commonly used, and any flagged as new in Step 3. Are there new hardcoded values that should be token references?

**For Month 1:** There is no previous baseline. Run the full check as an initial inventory. Document the current state as the first baseline. Note any existing naming violations or hardcoded values as inherited issues (not new drift).

**Output:** A structured diff. What changed, what's new, what's gone, what violates conventions. See [reference.md](reference.md) for the diff format.

---

## Step 3: Component Audit

Walk through the component library. This is lighter than the full Design Intelligence Audit. Focus on what changed since last month.

**If Figma MCP is available:** Run `get_design_context` across the component library file. This produces a structured component inventory per cycle: component hierarchy, library vs. local components, prop and variant details. Compare to `component-inventory-[YYYY-MM-1].json` (previous month) or the component baseline. New components, removed components, and components whose props changed all surface automatically. Store the current output as `component-inventory-[YYYY-MM].json` in `<engagement folder>/deliverables/care/`.

**What to check:**

- **New components.** Were any components added to Figma or code since last month? Do they exist in both places?
- **Modified components.** Did any component's props, variants, or states change? Does the change exist in both Figma and code?
- **Figma-code alignment.** For the components that changed, check: do Figma props match code props? Do variant names match? Are default values consistent?
- **Shadow components.** Scan for components built outside the system in the last month's feature work. These are candidates for promotion into the library.
- **Deprecated components.** Were any marked for deprecation? Are they still in use?

**For Care+ tier, also check:**

- **New component needs.** Based on recent feature work or roadmap, are there components the team is likely to need in the next month? Flag them early.
  - **With `search_design_system` (all plans, when MCP is active):** Query connected design libraries using likely component names for anticipated needs. If the component already exists in a connected library but hasn't been adopted, that's a faster path than building new. Surface it: "The [component name] you'll need next month exists in [library] — consider adopting it rather than building from scratch." This converts a future-cost finding into a concrete recommendation with a specific next step.
- **Usage patterns.** If usage data is available (analytics, import counts), identify: most-used components (these need the most care), least-used components (candidates for deprecation review), most-forked components (the system is failing to serve the need).

**For Month 1:** Document the full component inventory as the initial baseline. Note the current Figma-code alignment status for each component.

**Output:** Component change log. What was added, modified, or deprecated. Alignment status for changed components. See [reference.md](reference.md) for format.

---

## Step 3b: Pattern Ledger Review (Care+, when the application loop is in scope)

*Skip this step unless `application_loop.enabled: true` is set in `<engagement folder>/care-config.yaml`. This is the cadence's human decision surface for pattern promotion: it reads the ledger, and for each repeated composition the ledger flags, it files a candidate for the design-system owner to review. It promotes nothing and changes no ledger row.*

The pattern ledger records repeated compositions of design-system components and where each sits in its lifecycle (`local`, `candidate`, `promoted`, `retired`). It lives as the `usage` extension on `type: pattern` entries in the served `components.json`, and is read through the instance, never from disk.

**Execution.**

1. **Read the ledger through the instance.** Call `retrieve_application_context(query="", scope="patterns")`. Each returned row is `{name, purpose, usage, promotion_signal}`. If the result is `status: absent`, there is no ledger for this engagement yet; note that in the report and skip the rest of this step. (The served HeyHi data carries zero patterns by design; a real engagement's instance carries the rows.)

2. **Read the advisory signal.** The `promotion_signal` boolean is computed by the tool from the § 5 D4 defaults (three surfaces within one application, or two applications, or a second intent-journey-map origin), overridable per client via the profile's `promotion_thresholds`. It is advisory: the tool records no field named gate, blocked, or the like, and raising the signal decides nothing.

3. **File a candidate for each flagged local pattern.** For every row where `promotion_signal` is `true` **and** `usage.status == "local"`:
   - Write `pattern-intake/YYYY-MM-DD-<pattern-slug>.md` from [`pattern-intake/_template.md`](../../pattern-intake/_template.md), filling the candidate fields from the row: `name`, `usage.signature`, the usage evidence per application and per surface (`usage.applications`, `usage.surfaces`, `usage.figma_nodes`, `usage.code_paths`), `usage.origin`, a drafted proposed API, and the reason the signal tripped (which of the three D4 conditions held). The composition `level` is not carried on the pattern-ledger row (only the `ds-map` crosswalk carries `level`): read it from the served `ds-map` (scope `ds-map`) if the pattern maps to a row there, otherwise leave it for the owner to confirm.
   - Leave the template's `## Decision` block empty. This step files a candidate; the owner decides.
   - **The slug and idempotency.** Derive `<pattern-slug>` by kebab-casing the pattern `name`. Before writing, glob `pattern-intake/*-<pattern-slug>.md` and read any match's signature: if a file already carries this pattern's `usage.signature`, the candidate is already open, so append this cycle's fresh usage evidence under a dated note in that file rather than filing a second candidate for the same composition. A `usage.signature` that has changed since the open candidate means the composition itself changed: file that as a new candidate.
   - **Filling `level`, concretely.** Call `retrieve_application_context(scope="ds-map")` and find the `ds-map` row whose `figma_key` (or component set) matches this pattern; use that row's candidate `level` (itself `level_confirmed: false`). If no `ds-map` row matches, leave `level` blank for the owner. Never invent a level.

4. **Never touch the ledger.** Do not change `usage.status`, and do not write to `components.json` or the served ledger from this step. A `local` row stays `local`. Moving a row toward `candidate` or `promoted` is the human promotion pass's action (through the arc's `ds-component-author` and `ds-component-change`, Lanes G and H, once they are built and promoted, per `pattern-intake/README.md`), never this Care step's. The filer writes only into `pattern-intake/`.

**Empty slots (human):** whether a filed candidate is promoted, the level it is promoted at, and the proposed API. **Named gate:** the `pattern-intake/` review by the design-system owner, out of session.

**Output:** for the per-application report section (Step 6), the count of candidates filed this cycle and the names of the patterns that tripped the signal. Report the signal and the candidate as advisory only, never as a verdict or a grade.

**Reference:** `pattern-intake/README.md` (the firewall and lifecycle), the served tool `retrieve_application_context` scope `patterns`, and `ai-services/agentic-infrastructure/research/components-schema.json` `PatternDefinition.usage` (the ledger shape; the lifecycle value lives at `usage.status`).

---

## Step 4: Documentation Review

Check whether documentation kept pace with the changes found in Steps 2 and 3.

**What to check:**

- **Stale docs.** For each token or component that changed, does the documentation reflect the current state?
- **Missing docs.** For new components, does documentation exist? At minimum: when to use, when not to use, available props and variants.
- **Storybook or equivalent.** If the client uses Storybook, are stories current? Do they render correctly? Do they show all variants?
- **Governance adherence.** Were the documented processes (contribution, review, deprecation) followed for last month's changes? If not, note the deviation.
- **Descriptor vocabulary consistency.** If any `descriptors.mood`, `descriptors.anti_mood`, or `descriptors.keywords` fields were added or changed this month, verify the terms are drawn from the canonical Style Descriptor Vocabulary (`ai-services/design-intelligence/style-descriptor-vocabulary.md`). Ad hoc terms that overlap with canonical ones fragment retrieval and break style comparisons. Flag any non-canonical terms and propose the canonical equivalent. Load the summary keyword list (~60 tokens) — no need for the full vocabulary unless proposing a new addition.

**For Month 1:** Perform a complete documentation baseline. For each component and token category, note: coverage percentage, what's documented, what's missing, what's stale. This establishes the metric that future months track. For governance, document the current process (or note its absence) as the starting point.

**Output:** Documentation gap list. What's stale, what's missing, what was bypassed. See [reference.md](reference.md) for format.

---

## Step 4b: Layer 0 Intent Check (when applicable)

*Run only when a Layer 0 style entry was recorded at onboarding — i.e., when `meta.style_notes` in the client's `active-brand.json` references a named style from `style-reference-library.md`. If no Layer 0 style source was recorded at onboarding, skip to Step 5.*

This check detects **intent drift**: the case where token values have evolved through normal care cycles but have drifted away from the aesthetic intent documented when the system was built. Token drift (Step 2) catches changed values; intent drift catches changed character. These are different failure modes.

**What to check:**

1. **Load the style entry.** Read the `meta.style_notes` field from the client's `active-brand.json`. Identify the claimed style name (e.g., "Warm Technical Precision"). Load that entry from `ai-services/design-intelligence/style-reference-library.md` — the `token_implications` block only.

2. **Compare temperature register.** Does the current `brand.temperature` value match the style entry's `color_temperature` prior? Drift signal: a style that onboarded as "warm" now declares "neutral."

3. **Compare type scale.** Does the current `tokens.typography.scale.ratio` fall within the style entry's expected range? Drift signal: an entry that specified "Major Third 1.25x" now runs a "Minor Second 1.125x" — the type hierarchy has collapsed.

4. **Compare spacing density.** Does the current `tokens.spacing.density` (or inferred density from base unit and section values) match the style entry's `spacing_density` prior? Drift signal: a "spacious" style has accumulated dense spacing through component additions.

5. **Check the grey-default trap.** For warm-temperature styles: are `text-secondary`, `surface-secondary`, and `border-default` still warm-grey (hue angle 20–40°) or have they migrated toward neutral/cool defaults (`#6B7280` class)? This is the single most common intent drift pattern.

**Scoring intent drift:**

- 0 drifted dimensions: No intent drift. Note confirmation in the monthly report.
- 1 drifted dimension: Flag as **Low**. Mention in the monthly report as "minor drift noted." No correction required.
- 2 drifted dimensions: Flag as **Medium**. Include in Priority items. Recommend a brief correction pass.
- 3+ drifted dimensions: Flag as **High**. The system is diverging from its style origin. Recommend a structured correction pass and flag to the instance owner as a potential Layer 0 re-alignment session.

**Output:** Intent Drift section in the monthly report (Step 6). Dimensions checked, any drift found, severity, and recommended action.

**Reference:** `ai-services/design-intelligence/style-to-token-translation.md` Parts 1 and 5 for cluster priors. `ai-services/design-intelligence/style-reference-library.md` for the specific style entry.

---

## Step 5: Care+ Extended Checks

*Skip this step for Care tier. Proceed to Step 6.*

### 5a: Figma Sync Status

**With Figma MCP (deterministic):** Sync status is machine-verifiable rather than manual.
- Run `get_variable_defs` and compare Figma variable values against the token pipeline output. Any variable whose Figma value and code value differ is a sync gap.
- Run `get_code_connect_map` to verify Code Connect mappings are current (Enterprise/Org plan + Developer seat required). Stale mappings (pointing to deleted or renamed code files) surface immediately. Components with no mapping appear as gaps.
- Run `get_metadata` to confirm the last library publish date — if the published library is behind the working file, changes haven't propagated to consumers.

**Without Figma MCP (manual):**
- Is the Figma-to-code pipeline running? Check the last successful sync.
- Are there Figma changes that haven't propagated to code?
- Are there code changes that haven't been reflected in Figma?
- If Code Connect is configured, verify mappings are current.

### 5b: Accessibility Regression

Spot-check three to five components that changed since last month:
- Contrast ratios on new or modified color tokens (4.5:1 body text, 3:1 large text)
- Touch target sizes on new or modified interactive components (44x44px minimum)
- Focus states on new interactive components
- Label presence on form inputs

This is a spot-check, not a full accessibility audit. If significant regressions are found, recommend a dedicated accessibility review as a separate engagement.

### 5c: Maturity Dimension Tracking

Score the six maturity model dimensions for this month. Compare against last month's scores. For the full dimension definitions and level descriptions, see [design-system-maturity-model.md](../../ai-services/design-intelligence/design-system-maturity-model.md).

| Dimension | Last month | This month | Direction |
|-----------|-----------|------------|-----------|
| Token Architecture | | | |
| Component Coverage | | | |
| Documentation & Governance | | | |
| Figma-Code Sync | | | |
| Accessibility | | | |
| Team Relationship | | | |

**For Month 1 (Care+):** Score each dimension based on current state only. Mark "Last month" as "N/A" (first cycle). The "Direction" column will populate starting Month 2. Treat Month 1 scores as calibration, not judgment.

Note: Team Relationship is scored based on observations from the monthly work, not a formal interview. If the score seems to be declining, flag it for a deeper conversation with the client.

If any advisory warning combination is detected, cross-check against the "When to Escalate" section. Some warnings (e.g., strong infrastructure at Level 3+ with team relationship at Level 1-2) are escalation triggers.

Check for advisory warning combinations per the maturity model:
- Generation without governance
- Automation without accessibility
- Intelligent tooling without measurement
- Strong infrastructure, weak team relationship

### 5d: Code Connect Gap Detection and Maintenance (Care+ only, Enterprise/Org plan required)

*Requires Enterprise/Org Figma plan + Developer seat. Skip if plan tier doesn't support Code Connect.*

Run `get_code_connect_suggestions`. This returns components the Figma MCP has identified as Code Connect candidates not yet mapped to code. Review the list:

- **Map now:** For components with a clear, stable code counterpart, create the mapping using `add_code_connect_map` and commit via `send_code_connect_mappings`. This converts a gap finding into a delivered fix in the same cycle.
- **Flag for next cycle:** For components where the code counterpart is uncertain or the component is in active development, document the gap and revisit next month.
- **Stale mappings:** Also run `get_code_connect_map` and identify any mappings pointing to deleted or renamed code files. Remove or update these.

This is a named Care+ deliverable: Code Connect gap detection and maintenance. Unmapped components mean engineers don't get design context in their code generation flow. Closing that gap has compounding value each month.

**Monthly report for this step:**
- Number of Code Connect mappings active at cycle start and end
- New mappings added this cycle (list them)
- Gaps remaining and why (component unstable, code counterpart unclear, deferred)
- Stale mappings removed or updated

---

### 5e: Artifact Re-Sync (Care+, Tier 3, when the application loop is in scope)

*Skip this step unless `application_loop.enabled: true` is set in `care-config.yaml`. This step replaces the earlier Tier 3 bidirectional canvas loop with a concrete re-sync: when features landed in the application this cycle (found by Step 1b), the Figma artifact, the living prototype, and the frontend repo are re-synced so the artifact stays current with the application rather than drifting from it.*

**Dependency (name it, do not fake it).** This step runs through the promoted `feature-increment` skill in update mode (Lane F of the forward-deployed-loop arc, DISPATCH-07). Until `feature-increment` is promoted to `heyhi-skills/feature-increment/`, this step is inert: record in the report that artifact re-sync is pending the `feature-increment` promotion, name the deltas that would re-sync (from Step 1b), and skip the write. Do not re-implement `feature-increment`'s build inline.

**What to run (once `feature-increment` is promoted):**

1. From Step 1b's recon delta, take the changed surfaces the human marked in scope for re-sync. The `app-recon` brief gate (Step 1b) must be signed before any re-sync runs.
2. For each in-scope feature, run `feature-increment` in update mode. It produces its three targets from one contract: the Figma artifact increment through `app-to-figma` in update mode, the prototype increment through `ui-studio` Mode A with the instance's `validate_output` as a blocking gate, and the frontend repo increment propose-first, plus the three-way coverage table (every contract row present in Figma, the prototype, and code).
3. The Figma leg edits only the engagement's artifact file (its key lives in the served instance and the gitignored engagement folder, never in `care-config.yaml`). The prototype conformance gate is blocking (D9): a `validate_output` error fails the step. The repo increment is propose-first; Care never merges it and never pushes to a main branch.
4. When `feature-increment` builds a NEW composition because the library lacked the component, it emits a pattern-ledger row (the § 3.3 ledger shape) into the engagement folder. That write is `feature-increment`'s, not Care's. Step 3b reads those rows next cycle. This step writes no ledger row itself.
5. **When nothing in scope re-synced.** If Step 1b reported a quiet cycle, or the human marked no changed surface in scope for re-sync, there is nothing to re-sync: record "artifact current, no re-sync this cycle" and skip. Do not re-sync a surface that did not change.

**A coverage miss is a finding, not a silent gap.** The three-way coverage table carries one row per contract row from the feature's intent-journey map. A contract row absent from any of the three columns (not present in Figma as a property, text, or bound variable; not a prototype data binding; not a code prop or hook field) is a coverage finding, named by the contract row and the column it is missing from, never smoothed over.

**Empty slots (human):** which changed surfaces re-sync this cycle (inherited from Step 1b's brief gate); deviations from the library; the merge of any proposed repo increment. **Named gate:** `feature-increment`'s delta-plan review, and the prototype `validate_output` gate (blocking, D9).

**Monthly report for this step (per application):**
- Features re-synced this cycle (or the pending-dependency note if `feature-increment` is not yet promoted)
- The three-way coverage table result: contract rows present in Figma, in the prototype, and in code; any coverage miss as a finding
- Prototype conformance gate result: passed or blocked (with the blocking finding if blocked)

---

### 5f: Figma Skills Maintenance (Care+ only)

*Runs every cycle. 15–20 minutes. The Skill is part of the design system — it needs the same care.*

The client's Figma Skill file (`<engagement folder>/figma-skills/[client-slug]-figma-skill.md`) teaches agents how to use the design system. As the system evolves, the Skill must stay current. An outdated Skill produces agents that follow yesterday's rules.

**Checklist — work through this against the changes found in Steps 2–3:**

- [ ] **New tokens this cycle:** If Step 2 found new tokens, do they appear in the Skill's Token Conventions section? Add naming guidance for any new token categories.
- [ ] **Changed naming patterns:** If token or component naming conventions changed, update the corresponding Skill section. Don't leave old conventions — they'll produce incorrect agent behavior.
- [ ] **New components:** If Step 3 found new components promoted into the library, add component guidance to the Skill's Component Conventions section.
- [ ] **Direction changes:** If `active-brand.json` was updated (e.g., a new Gate 0 ran or descriptors evolved), check whether the Design System Identity, vocabulary, or composition sections need updating.
- [ ] **New Code Connect mappings (from 5d):** If new mappings were added this cycle, update the Agent Tool Guidance section with any new component usage notes.
- [ ] **Motion or SENSITIVE_CONTEXT changes:** If motion tokens changed or a new sensitive-context scope condition was identified, update the Motion section and Conditional Override block if present.
- [ ] **Version bump:** If any section changed, increment the Skill version and add a row to the Version history table.
- [ ] **No changes:** If nothing in Steps 2–3 affects the Skill, note "Skill reviewed — no updates required" in the report. Still counts as maintenance.

**Escalation trigger:** If the design direction changed significantly (new moodboard delivered, new Gate 0 run, locked direction label changed), do not patch. Stop and re-author the Skill from scratch using the `figma-skills-authoring.md` workflow. Log the re-authoring as a separate deliverable in the engagement record.

**Monthly report for this step:**
- Skill version at cycle start and end
- What was updated (list changed sections)
- Whether re-authoring was triggered and why

**Reference:** `../../ai-services/design-intelligence/figma-skills-authoring.md` — the full five-step authoring workflow, Layer 0 injection process, Skill file structure template, and monthly maintenance checklist.

---

### Step 5g: Prototype Health Audit (Care+, when prototypes are in scope)

*Skip this step unless `prototype_audit.enabled: true` is set in `<engagement folder>/care-config.yaml` and at least one prototype is listed under `prototype_audit.prototypes`.*

When the client's engagement includes a prototype layer — interactive HTML prototypes for new feature concepts, demo prototypes for stakeholder review, or onboarding flow prototypes — run a monthly delta audit against the prior month's baseline. The full framework lives in `heyhi-prototype-audit/SKILL.md` Layer 3; this step orchestrates the call from the Care monthly cycle.

**Scope determination.** At engagement kickoff (asked in Step 0 above), the discovery question is: "Does the engagement include prototype maintenance — onboarding flows, demo prototypes, or feature concepts in HTML — alongside the design system itself?" If yes, populate `<engagement folder>/care-config.yaml`:

```yaml
prototype_audit:
  enabled: true
  prototypes:
    - path: <engagement folder>/prototypes/[name].html
      purpose: "[What this prototype demonstrates]"
```

If `prototype_audit.enabled: false` or the section is absent, skip this step.

**Execution.** Load `heyhi-prototype-audit/SKILL.md` Layer 3. For each prototype listed in `care-config.yaml`:

1. **Locate the prior baseline.** Read `<engagement folder>/deliverables/care/prototype-audit-baseline-[YYYY-MM-1].md` and the matched JSON sidecar `prototype-audit-baseline-[YYYY-MM-1].json`. For Month 1 (no prior baseline), run the full Layer 1 + Layer 2 audit and store as `prototype-audit-baseline-[YYYY-MM].md` plus the matched `.json` sidecar. The first cycle establishes the baseline; do not compute a delta against a baseline that does not exist.

2. **Run the audit.** Layer 1 (six steps) and Layer 2 (config-aware checks if a brand config is present) execute against the current state of each prototype. Validate the resulting JSON sidecar against `heyhi-skills/heyhi-prototype-audit/baseline-schema.json` before writing.

3. **Produce the delta narrative.** Write to `<engagement folder>/deliverables/care/prototype-audit-[YYYY-MM].md` with sections: Gaps closed since last cycle, New gaps surfaced this cycle, Severity-bucket movement (Critical→High, etc.), Stakeholder-readiness threshold movement. The matched JSON sidecar at `prototype-audit-[YYYY-MM].json` becomes the next month's baseline.

4. **Roll up to the Care report.** Add a single summary line to the monthly Care report (Step 6 output): "Prototype audit ([prototype name]): [N gaps closed], [M new gaps surfaced], [readiness threshold position]." If multiple prototypes are in scope, one summary line per prototype.

**Care+ tier note.** Prototype Health Audit is Care+ only because it requires sustained baseline maintenance (Layer 3 depends on the prior month's sidecar to compute deltas). Care tier engagements that need prototype audits get them as standalone Layer 1 + Layer 2 runs — handled directly via `heyhi-prototype-audit`, not as a recurring Care cadence.

**Output paths summary:**
- `<engagement folder>/deliverables/care/prototype-audit-baseline-[YYYY-MM].md` (Month 1 only)
- `<engagement folder>/deliverables/care/prototype-audit-baseline-[YYYY-MM].json` (Month 1 only)
- `<engagement folder>/deliverables/care/prototype-audit-[YYYY-MM].md` (Month 2+ delta narrative)
- `<engagement folder>/deliverables/care/prototype-audit-[YYYY-MM].json` (Month 2+ structured sidecar — becomes next month's baseline)

**Reference:** `heyhi-skills/heyhi-prototype-audit/SKILL.md` Layer 3 — full delta-format spec, baseline preservation rules, schema location.

---

### Step 5h: Agent Conformance Audit (Care+, when agent-authored output is in scope)

*Skip this step unless `agent_conformance.enabled: true` is set in `<engagement folder>/care-config.yaml` and a corpus is named under `agent_conformance.corpus`.*

The longitudinal read no vendor ships: do the agents building against this design system actually comply with it, and is that trending up or down? Token drift (Step 2) measures whether the *system* moved; this measures whether the *agent-authored output* built against it conforms, tracked over the Care cadence. The per-sample engine already exists in `heyhi-mcp/heyhi_mcp/conformance/` (the deterministic CSS/token checks and the MCP-App conformance gate); this step wraps it in time and computes the delta. It adds no new detection.

**Scope determination.** At engagement kickoff (asked in Step 0), the discovery question is: "Does the engagement include an agent-authored output stream — generated components, MCP-App bundles, or PRs from agents building against the system?" If yes, populate `<engagement folder>/care-config.yaml`:

```yaml
agent_conformance:
  enabled: true
  corpus: <engagement folder>/agent-output/        # dir of samples; manifest.json preferred
  tokens: <engagement folder>/tokens.dtcg.json     # the client's token registry (css samples)
  threshold: {}   # AUTHORED PER ENGAGEMENT. Empty = no alert; the drift call stays human.
```

If `agent_conformance.enabled: false` or the section is absent, skip this step.

**Execution.** For the named corpus:

1. **Locate the prior read.** The prior cycle's read is `<engagement folder>/deliverables/care/conformance-read-[YYYY-MM-1].json`. On the first cycle there is no prior read — the cycle is a baseline snapshot; do not compute a delta against a read that does not exist.

2. **Run the read.** From `heyhi-mcp/`:

   ```
   PYTHONPATH=. python -m heyhi_mcp.conformance.trend \
     --corpus <agent_conformance.corpus> \
     --tokens <agent_conformance.tokens> \
     --prev <engagement folder>/deliverables/care/conformance-read-[YYYY-MM-1].json \
     --store <engagement folder>/deliverables/care/ \
     --report-out <engagement folder>/deliverables/care/conformance-report-[YYYY-MM].md \
     --client [client-name] --cycle [YYYY-MM] --tier care+ \
     [--threshold metric:direction:limit ...]   # ONLY if the engagement authored one
   ```

   The read is written as an immutable dated file (a same-cycle re-run is refused, not silently overwritten) and validated against `heyhi_mcp/conformance/conformance-read-schema.json` before write when `jsonschema` is available in the runtime (it is in the standard heyhi-mcp venv and CI). Omit the `--prev` flag on the first cycle. The wrap refuses a `--prev` from a different corpus, theme, or token set, so a mis-pointed prior read fails loud rather than producing a meaningless delta. Never pass `--threshold` unless the engagement has authored the rule (see the threshold note below).

3. **Record provenance.** Each sample carries which agent, prompt, and commit produced it (the corpus `manifest.json` `provenance` field). A conformance figure is never reported without it — the read stamps `tokens_source` too, since output scored against the wrong token set reads as all-unknown.

4. **Roll up to the Care report.** Add a single summary line to the monthly Care report (Step 6 output): "Agent conformance ([corpus]): [N of M samples conform], [trajectory], [K regressed]." The full delta section — trajectory, top drifting classes, regressed samples, and the human load-bearing judgment — is written to `conformance-report-[YYYY-MM].md` and linked from the Care report.

**Threshold note — no default.** The instrument ships no default drift threshold. Which conformance-trend drop is load-bearing is authored per engagement, not by HeyHi: a default threshold is a decision made for the client by a vendor who has not met their team, which is the failure mode HeyHi exists to name. Absent an authored `threshold`, the read reports the trend and leaves the alert null — and whether the movement matters is a Care judgment recorded in the report, not an automated verdict. Grades never gates.

**Care+ tier note.** Agent Conformance Audit is Care+ only because the value is the time-series — it depends on the prior cycle's stored read to compute a delta. A one-off point-in-time conformance check on a single sample is the per-sample engine run directly, outside the Care cadence.

**Output paths summary:**
- `<engagement folder>/deliverables/care/conformance-read-[YYYY-MM].json` (every cycle — the immutable dated read; becomes next month's prior read)
- `<engagement folder>/deliverables/care/conformance-report-[YYYY-MM].md` (the rendered delta section; linked from the Care report)

**Reference:** `heyhi-mcp/heyhi_mcp/conformance/trend.py` (the time-series wrap), `heyhi-mcp/heyhi_mcp/conformance/conformance-read-schema.json` (the read schema), and the per-sample engine in `heyhi-mcp/heyhi_mcp/conformance/`. Plan: `plans/plan-agent-conformance-care-surface-2026-08-30.md`.

---

### Step 5i: Production-Code Adoption Scan (Care+, when the engagement grants codebase access)

*Skip this step unless `adoption_scan.enabled: true` is set in `<engagement folder>/care-config.yaml` and a codebase path is named under `adoption_scan.codebase`.*

The read a Care retainer needs to make itself measurable: **how much of the client's production UI is actually built on the design system, and is that trending?** Token drift (Step 2) measures whether the *system* moved; agent conformance (Step 5h) measures whether *agent-authored output* complies; this measures whether the *client's own production code* adopts the system, tracked over the Care cadence. It generalizes Step 6's "shadow components identified" spot-check from a sample to a full-repo scan. It adds no new detection — the scanner in `heyhi-mcp/heyhi_mcp/adoption/` is authoritative for one snapshot; this step wraps it in time.

**Scope determination.** At engagement kickoff (asked in Step 0), the discovery question is: "Does the engagement include codebase access for an adoption reading — can we scan the frontend repo?" If yes, populate `<engagement folder>/care-config.yaml`:

```yaml
adoption_scan:
  enabled: true
  codebase: /path/to/client/frontend          # the repo (or subdir) to scan
  config: <engagement folder>/adoption-config.json   # what counts as on-system (below)
  corpus_id: [client-name]   # REQUIRED, stable across cycles. Never the dir name: two client
                             # repos both named "frontend" would silently merge into one series.
  threshold: {}   # AUTHORED PER ENGAGEMENT. Empty = no alert; the drift call stays human.
```

The `adoption-config.json` names, for this engagement, `system_import_sources` (import specifiers that mark a component as on-system), an optional `system_components` allowlist, `deprecated_components` (from the client's registry deprecation tags), and `served_component_names` (for one-off detection). The client's engineering lead confirms these before the first read. If `adoption_scan.enabled: false` or the section is absent, skip this step.

**Ratification gate (G-W4) — before any client report.** A "% on system" figure does not go into a client-facing report until the adoption metric-definitions contract is ratified: definition, formula, source, exclusions, refresh, owner, gaming path, counter-metric, effective date, versioned. The contract lives at `references/adoption-definitions-contract.md`; ratification is the instance owner's call, once per definition (the shipped contract is an unratified slot; an instance records its own ratification), per `design-system-roi-storytelling-research-2026-09-01.md` § 6.3. An internal read may run before ratification; a client deliverable may not.

**Execution.** For the named codebase:

1. **Locate the prior read.** The prior cycle's read is `<engagement folder>/deliverables/care/adoption-read-[YYYY-MM-1].json`. On the first cycle there is no prior read — the cycle is a baseline snapshot; do not compute a delta against a read that does not exist.

2. **Run the read.** From `heyhi-mcp/`:

   ```
   PYTHONPATH=. python -m heyhi_mcp.adoption.trend \
     --codebase <adoption_scan.codebase> \
     --config <adoption_scan.config> \
     --corpus-id <adoption_scan.corpus_id> \
     --prev <engagement folder>/deliverables/care/adoption-read-[YYYY-MM-1].json \
     --store <engagement folder>/deliverables/care/ \
     --report-out <engagement folder>/deliverables/care/adoption-report-[YYYY-MM].md \
     --client [client-name] --cycle [YYYY-MM] --tier care+ \
     [--threshold metric:direction:limit ...]   # ONLY if the engagement authored one
   ```

   `--corpus-id` is required for `--tier care+` (the run refuses without it): it is the stable stream identity across cycles, so it must be the engagement's own id, never the scanned directory's name. The read is written as an immutable dated file (a same-cycle re-run is refused unless you pass `--overwrite`) and validated against `heyhi_mcp/adoption/adoption-read-schema.json` when `jsonschema` is available. Omit `--prev` on the first cycle. The wrap refuses a `--prev` from a different corpus id, so a mis-pointed prior read fails loud. Never pass `--threshold` unless the engagement authored the rule.

3. **Read the headline with its counter-metric — always.** The rendered section reports `on_system_rate` beside `override_rate`. Never quote the coverage number alone: a coverage percentage with no counter-metric is gameable (a team can hit 100% on-system while hardcoding every value). The scan is Tier-1 static — blind to whether a call site renders, stated as a labelled limitation on every read.

4. **Roll up to the Care report.** Add a single summary line to the monthly Care report (Step 6 output): "Production-code adoption ([codebase]): [X% on system], override rate [Y%], [trajectory], [K files regressed]." The full delta section — trajectory, drift concentration (which files lost coverage), deprecated usage, one-offs, and the human load-bearing judgment — is written to `adoption-report-[YYYY-MM].md` and linked from the Care report.

**Threshold note — no default.** The instrument ships no default drift threshold. Which coverage drop is load-bearing is authored per engagement, not by HeyHi. Absent an authored `threshold`, the read reports the trend and leaves the alert null; whether the movement matters is a Care judgment recorded in the report, not an automated verdict. Grades never gates.

**Care+ tier note.** The Production-Code Adoption Scan is Care+ only because the value is the time-series — it depends on the prior cycle's stored read to compute a delta and its drift concentration. A one-off point-in-time scan is the scanner run directly, outside the Care cadence.

**Output paths summary:**
- `<engagement folder>/deliverables/care/adoption-read-[YYYY-MM].json` (every cycle — the immutable dated read; becomes next month's prior read)
- `<engagement folder>/deliverables/care/adoption-report-[YYYY-MM].md` (the rendered delta section; linked from the Care report)
- `<engagement folder>/deliverables/care/adoption-definitions-contract.md` (the per-engagement instance of the ratified contract, attached to any report that quotes a number)

**Reference:** `heyhi-mcp/heyhi_mcp/adoption/trend.py` (the time-series wrap), `heyhi-mcp/heyhi_mcp/adoption/static_scan.py` (the Tier-1 scanner), `heyhi-mcp/heyhi_mcp/adoption/adoption-read-schema.json` (the read schema), and `references/adoption-definitions-contract.md` (the G-W4 metric-definitions contract). Plan: `plans/plan-sheerline-adoption-and-reach-2026-09-12.md`.

---

## Step 6: Generate the Monthly Report

Produce the report using HeyHi voice (invoke `heyhi-voice` rules). The report goes to the client. It should be specific, honest, and useful.

**Report structure:** See [reference.md](reference.md) for the full template.

Summary:
- Month number and date range
- One-paragraph executive summary: what happened, what's healthy, what needs attention
- Overall trajectory: improving, stable, or declining (with evidence)

Token health:
- Drift summary (added/removed/changed/violations)
- If MCP path was used: note "Token drift verified via Figma variable extraction" — this is a credibility signal
- Trend: is drift increasing, decreasing, or stable month-over-month?

Component health:
- Changes summary (added/modified/deprecated)
- Alignment status
- Shadow components identified

Documentation status:
- Gaps identified
- Governance adherence

Care+ sections (if applicable):
- Figma sync status (deterministic if MCP was used)
- Accessibility spot-check results
- Maturity dimension scores and trend
- Code Connect status: new mappings added, gaps remaining, trend in coverage
- Artifact re-sync (if the application loop is in scope, Step 5e): features re-synced this cycle, the three-way coverage table result, the prototype conformance gate result
- Figma Skills: Skill version, what changed, whether re-authoring was triggered

**Per application** (only when `application_loop.enabled: true`): one sub-section per application in the forward-deployed loop, rolling up the loop steps for that application. Omit this whole section for engagements with no application loop. For each application:

- **Recon delta** (from Step 1b): surfaces changed this cycle, endpoints changed, the `unverified[]` count from the `app-recon` brief, and the new baseline commit. For Month 1, note that the baseline was established this cycle.
- **Pattern candidates** (from Step 3b): the count of `pattern-intake/` candidates filed this cycle and the names of the patterns that tripped the promotion signal. State plainly that these are candidates for the owner's review, not promotions, and that no ledger row was changed.
- **Artifact re-sync** (from Step 5e): features re-synced through `feature-increment`, the three-way coverage table (contract rows present in Figma, the prototype, and code) with any miss called out as a finding, and the prototype gate result. If `feature-increment` is not yet promoted, state that re-sync is pending that dependency and name the deltas that would re-sync.
- **Coverage snapshot** (from the served `ds-map`): the count of rows in each coverage state (both, code-only, figma-only, divergent), so cross-surface coverage is trackable month over month. Report the counts; the coverage call itself stays a human read.

Keep this section advisory: it reports signals, deltas, and candidates, never a verdict on the application.

Example shape for one application in an ordinary cycle:

> **Application: [app].** Recon delta: 3 surfaces changed (checkout, cart, order-confirm), 1 endpoint changed, 0 unverified, baseline advanced to `a1b2c3d`. Pattern candidates: 1 filed (`filter-bar`) for the owner to review, not a promotion, no ledger row changed. Artifact re-sync: 2 features re-synced, coverage table clean (18 of 18 contract rows in all three columns), prototype gate passed. Coverage snapshot: both 42, code-only 3, figma-only 1, divergent 0.

Repeat the sub-section per application when more than one is in the loop.

Recommendations:
- What to prioritize this month (no more than three items)
- What's coming next month (anticipated needs based on the client's roadmap)
- Any escalations: issues that exceed monthly care scope and warrant a separate engagement

**Voice rules for the report:**
- Write for the audience. If leadership reads it: outcomes and cost. If the team reads it: specifics and actions.
- Be specific. "The Button component's loading state variant exists in Figma but not in code" beats "there are some alignment issues."
- No scores or grades. Describe what's happening and what it means.
- Use the findings language guide from the audit reference for translating technical findings.

**Output format:**
Save as `care-report-[YYYY-MM].md` in `<engagement folder>/deliverables/care/`.

If the client prefers a Word document, also generate `care-report-[YYYY-MM].docx` using standard document generation (the platform `docx` skill or python-docx).

---

## Step 7: Update the Baseline

After the report is complete, generate the updated baseline for next month's comparison.

**Baseline file:** `baseline-[YYYY-MM].json` in `<engagement folder>/deliverables/care/`.

The baseline captures:
- Full token inventory (names, values, hierarchy)
- `figma_variable_manifest` (if Figma MCP was used this cycle): the full variable state extracted from Figma via `get_variable_defs`, for deterministic diff comparison next month. This field does not overwrite the token inventory — it adds the Figma-side source of truth alongside it.
- Component inventory (names, props, variants, Figma-code alignment status)
- Documentation status per component
- Maturity dimension scores (Care+ only)
- Date generated

**Forward-deployed loop additions (when `application_loop.enabled: true`).** So next cycle's Steps 1b, 3b, and 5e act on a real baseline rather than a fresh read, the baseline also captures:

- **Application manifest snapshot:** the `app-manifest.json` from Step 1b, referenced by its served path (not inlined), together with the new baseline commit (the manifest's `source_commit`). Write that commit back to `care-config.yaml` under `application_loop.baseline_commit` so next cycle's Step 1b runs `app-recon --since` the right commit. `care-config.yaml application_loop.baseline_commit` is the authoritative cursor Step 1b reads; the copy recorded in this baseline snapshot is the historical record for the cycle, not a second source Step 1b consults.
- **Pattern-ledger snapshot:** the ledger rows read through `retrieve_application_context` scope `patterns` this cycle (`name`, `usage.signature`, `usage.status`, `promotion_signal`), so next cycle's Step 3b can tell which candidates were already filed and which patterns changed lifecycle since. This is a read snapshot for trend, not a write to the ledger.
- **Coverage snapshot:** the `ds-map` coverage counts (both, code-only, figma-only, divergent), so cross-surface coverage is trackable month over month alongside token and component drift.

These land under an `application_loop` block in `baseline-[YYYY-MM].json`, alongside the existing fields:

```json
"application_loop": {
  "baseline_commit": "<new HEAD sha>",
  "manifest_ref": "<engagement folder>/deliverables/care/app-manifest-[YYYY-MM].json",
  "pattern_ledger": [ {"name": "...", "signature": "...", "status": "local", "promotion_signal": true} ],
  "coverage": {"both": 0, "code_only": 0, "figma_only": 0, "divergent": 0},
  "candidates_filed": ["pattern-intake/YYYY-MM-DD-<slug>.md"]
}
```

`candidates_filed` records which `pattern-intake/` files this cycle wrote, so next cycle's Step 3b idempotency check has a fast index of the open candidates.

Do not overwrite previous baselines. Each month's baseline is a separate file. The history enables trend analysis.

---

## Step 8: File and Confirm

Store all outputs:
- `<engagement folder>/deliverables/care/care-report-[YYYY-MM].md` (or `.docx`)
- `<engagement folder>/deliverables/care/baseline-[YYYY-MM].json`
- `<engagement folder>/deliverables/care/drift-log-[YYYY-MM].json` (the raw diff from Step 2)
- `<engagement folder>/deliverables/care/figma-manifest-[YYYY-MM].json` (if MCP was used)
- `<engagement folder>/deliverables/care/component-inventory-[YYYY-MM].json` (if MCP was used)

Confirm with the instance owner:
- Report is ready for review
- Any escalations that need discussion before sending to the client
- Any items that should be added to the client's next sprint or roadmap

---

## Month 1 vs. Subsequent Months

| Aspect | Month 1 | Month 2+ |
|--------|---------|----------|
| Token check | Full inventory, establish baseline | Compare against previous baseline |
| Component audit | Full inventory, document alignment | Focus on changes since last month |
| Documentation | Full gap analysis | Check whether last month's gaps were closed |
| Report tone | "Here's where your system stands" | "Here's what changed and what it means" |
| Baseline | Create first baseline | Update baseline, preserve history |
| Care+ maturity | Initial scoring (calibration) | Trend comparison |
| MCP Figma manifest | First extraction — no previous to diff against | Diff against previous month's manifest |
| MCP component inventory | First extraction — establishes the baseline | Diff against previous month's inventory |
| Recon delta (1b, loop) | Full `app-recon` read; store the first baseline commit | `app-recon --since` the stored baseline; only changed surfaces |
| Pattern ledger (3b, loop) | Read the ledger; file candidates for local rows already over signal | Read again; file candidates for newly-flagged rows, skip open candidates |
| Artifact re-sync (5e, loop) | Sync the artifact to the first read (or note the pending `feature-increment` dependency) | Re-sync only the features that landed since the baseline |

---

## Integration Points

This skill works alongside:

| Skill | Relationship |
|-------|-------------|
| `ui-studio` | Downstream consumer of the brand config. Monthly care validates that the config used in builds still reflects the live system state. |
| `ui-studio-onboard` | First-time brand config setup for new clients. Run before the first monthly care cycle. Produces active-brand.json. |
| `heyhi-design-intelligence-audit` | The full audit methodology. Monthly care uses a lighter version of the six examination areas. If the monthly cycle uncovers something that needs the full audit treatment, escalate. |
| `heyhi-prototype-audit` | Prototype Health Audit on a recurring cadence (Step 5g) calls Layer 3 of this skill. Standalone (one-off) prototype audits also live here, invoked directly outside the Care cycle. |
| `heyhi-mcp` conformance engine | Agent Conformance Audit on a recurring cadence (Step 5h) wraps the per-sample conformance floor (`heyhi_mcp/conformance/`, `trend.py`) in the Care time-series. One-off point-in-time conformance checks run the engine directly, outside the Care cycle. |
| `heyhi-mcp` adoption engine | Production-Code Adoption Scan on a recurring cadence (Step 5i) wraps the Tier-1 static scanner (`heyhi_mcp/adoption/`, `trend.py`) in the Care time-series (the "% on system" + override counter-metric). One-off point-in-time adoption scans run the scanner directly, outside the Care cycle. |
| `app-recon` | Read half of the forward-deployed loop. Step 1b runs it in delta mode (`--since <commit>`) to find what changed in an application in loop scope. Its brief-review gate must be signed before Step 5e re-syncs. |
| `feature-increment` | Build half of the loop. Step 5e runs it in update mode to re-sync the Figma artifact, the prototype, and the repo from one contract when features land. Consumed as a promoted skill; until Lane F promotes it, Step 5e names the dependency and stays inert. |
| `retrieve_application_context` (heyhi-mcp) | The served application-context boundary. Step 3b reads scope `patterns` for the advisory `promotion_signal`; Steps 1b and 5e read the served manifest and context. No loop step loads a manifest or contract file from disk as a spec. |
| `pattern-intake/` | The human decision surface for pattern promotion. Step 3b files a candidate there for each `local` pattern the ledger flags; the design-system owner promotes, out of session. The firewall twin of `corrections-intake/`. |
| `heyhi-voice` | Report voice. All client-facing content passes through voice rules. |
| `heyhi-proposal` | If the monthly cycle identifies work that exceeds care scope, generate a proposal for a Build engagement. |
| `design-system-onboard` | Legacy onboarding skill. For new clients, use `ui-studio-onboard` instead. |

---

## When to Escalate

The monthly cycle has a defined scope. Some findings exceed it. Escalate when:

- A dimension on the maturity model drops two or more levels in a single month
- The token architecture needs structural rebuilding (not just maintenance)
- More than 30% of components are shadow components (the system isn't serving the team's needs)
- Team relationship signals suggest the system is being actively worked around
- Accessibility findings suggest a full audit is needed (3+ regressions in one month)
- Figma-code sync has been broken for two or more consecutive months
- Any maturity model advisory warning combination is active (see Step 5c)

Escalation means: flag to the instance owner, discuss with the client, and potentially scope a Build engagement or a dedicated audit.

---

See [reference.md](reference.md) for:
- Monthly report template (full)
- Baseline JSON schema (updated with `figma_variable_manifest` field)
- Drift log format
- Component change log format
- Month-over-month comparison template
- Maturity dimension scoring quick reference

---

## Exit Gate Required Headers (bottom-of-skill bracket)

This skill closes through the Exit Gate Flavor A (`CLAUDE-SESSION-RULES.md § Exit Gate`). Before declaring done, confirm every required header below contains real content, not a claim:

- `## Fixes Applied`
- `## Smoke Test`
- `## Next Session Prompt`

If any header is empty or contains advisory prose ("I checked for bugs") instead of a concrete artifact, the gate has not been satisfied. Apply fixes until clean — then emit.

*HeyHi Confidential*
