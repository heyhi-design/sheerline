---
name: heyhi-design-intelligence-audit
description: >-
  Run a HeyHi Design Intelligence Audit on a client's design system. Use when the user
  says "audit this client's design system", "assess design-code drift", "run a design
  audit", "what's the health of their system", "review their tokens and components",
  or when preparing for or executing a Design System Care engagement. Also triggers
  when a client asks what's wrong with their design system, when evaluating a system
  before a Build engagement, or when producing an audit report. Works in three core
  modes (Planning, Audit, Report). Also covers DESIGN.md conformance — whether a
  generated UI honors its intent-rich DESIGN.md (an Area 7 capability sub-area, run
  when a generation is in hand). For interaction completeness checks on HTML
  prototypes — gap analysis, readiness assessment — use heyhi-prototype-audit. For a
  config fidelity review of generated output against design intent, use
  design-system-review.
version: "1.11.1"
updated: "2026-10-13"
changes: "v1.11.1 (2026-10-13): Generalized for the Sheerline scaffold: instance data (brand defaults, client/engagement history, owner names, ratified values) moved to instance-only files or neutral wording; method unchanged. v1.11.0: Area 7 gained a DESIGN.md-conformance sub-area — a dual-checking capability (mechanical floor via validate_output + intent / anti-tell / fundamentals judgment axes) that audits a generation against its intent-rich DESIGN.md and the design-fundamentals reference. Capability sub-area, not a fifth ARI axis; the ARI formula is unchanged. Instance-keyed: the floor reads the client's own token set + out-of-palette feature-styling declaration (via validate_output's constraints param) and Axis 3 reads the instance's own DESIGN.md anti-tell list, not HeyHi's — HeyHi's visual-anti-tells.md is HeyHi's instance list, not the universal set (flexibility-ledger H1a/H1b/H4). Calibrated on a known-good/known-bad pair with zero false positive on the reference instance's documented signatures (Gate G2). Full rubric + calibration proof + report template: references/conformance-sub-area.md, references/conformance-calibration.md. Source: DISPATCH-C, plan-design-md-build § Phase 2. v1.10.0: Area 7 sub-area 7.2 gained the adopted-third-party-agent-UI diagnostic — does the organization know which of its adopted MCP Apps honour its design tokens, and does anything check? Covers the hostContext.styles.variables contract, which goes Final in the 2026-07-28 MCP specification and which nothing verifies. Feeds the existing 7.2 1–4 score; no new sub-area, ARI formula unchanged; clients with no adopted views are marked not-applicable rather than penalised. Explicitly framed as a gap-naming question, not a HeyHi capability claim — no conformance checker exists, from HeyHi or anyone. Source: explorations/verification-loops/runtime-surface-and-the-token-contract.md §§ 2-3; dispatch-prompts-2026-07-19-design-system-native-generation.md DISPATCH-00. v1.9.3: Routing precision batch (setup-grade 2026-07-04 DISPATCH-02) — description gained the design-system-review deferral; Area 1 line no longer cites archived design-system-ux as a live consumer; the Memory Hygiene pointer names the current module (memory-mcp/hygiene_extractor.py) instead of the retired general_extractor name. v1.9.2: Memory Hygiene Diagnostic add-on UNBLOCKED — five-category extractor ported verbatim into memory-mcp/hygiene_extractor.py (patterns unchanged for benchmark comparability; differential-tested byte-identical vs the archived original; smoke 20/20). Reference How-to-Run now points at the in-house module; no mempalace install involved. v1.9.1: Memory architecture alignment — Memory Hygiene Diagnostic add-on marked BLOCKED pending a port of the five-category extractor into memory-mcp/ (its original tooling was MemPalace's general_extractor; MemPalace decommissioned 2026-06-28, and pip-installing mempalace is forbidden per OPERATING_PRINCIPLES Plugin install hygiene). Diary-wing recall section reattributed from MemPalace to the memory shim (mechanics unchanged; the wing_ prefix behavior persists in the Postgres backend). v1.9.0: Folded Work Block 5 Workstream A findings (T2.1–T2.4) into reference.md as the new 'Figma Professional Integration' section — Professional vs. Enterprise capability table, Check Designs pre-audit differential matrix, 200/day MCP call budget (~150 components/day), and the Code Connect Professional workaround (T2.4 confirmed Enterprise-only). Step 3 Figma MCP check + Area 4 Code Connect fallback now point at it. Closes Work Block 5 gateway G5.2. Source: ai-services/design-intelligence/work-block-5-figma-integration-plan.md, test-system.md T2.x results. v1.5.0: Area 1 alpha token check, Area 2 composite dependency check, Maturity Radar required, Organizational Commitment add-on (Area 8), run order updated. v1.6.0: Organizational Commitment add-on fully integrated into Step 0/1/3/5; Area 8 report section. v1.7.0: Added Prototype Mode section (Steps 0–6) and routing rule in Step 0. Source: prototype-audit-extension-spec.md. v1.7.1: Area 5 dark mode token propagation check added to 'What to examine' list; Area 5 drift signals section added (dark mode propagation gaps, focus ring regression). Source: a client-engagement Phase 3 codification — dispatch-prompts-ds-codification-2026-04-27.md Prompt C. v1.8.0: Prototype Mode (Steps 0–6) replaced with one-paragraph redirect to heyhi-prototype-audit; description block trigger phrases for prototype-style audit invocations dropped per Track B buildable plan §5 Option A. Source: plans/track-b-prototype-audit-buildable-2026-05-06.md."
---

# HeyHi Design Intelligence Audit

This skill runs a structured audit of a client's design system — examining the gap between what's in Figma and what's in code, where the documentation breaks down, and what the team's current relationship to the system actually is. The output is an honest assessment that tells the client something they can act on.

The audit is not a scorecard. It's a diagnosis. The goal is to name what's actually happening, not rank the client against an ideal.

For audit report templates, examination checklists, severity rubric, and findings language, see [reference.md](reference.md).

---

> **Exit Gate (Flavor A).** This skill closes through the canonical Exit Gate — see `CLAUDE-SESSION-RULES.md § Exit Gate`. Required headers, in order: `## Fixes Applied`, `## Smoke Test`, `## Next Session Prompt`. Empty headers are visible failures.


## Step 0: Determine Mode

**Planning mode** — the auditor is preparing for an audit engagement. No client materials available yet. Produce: engagement structure, session plan, materials to request from client, and what to examine.

**Audit mode** — Materials are available (Figma access, codebase, documentation, or some combination). Run the six examination areas (seven if `agent_readiness_add_on: true`). Produce findings.

**Report mode** — Findings are complete. Produce the formatted audit report for delivery.

**Agent Interface Readiness add-on:** Before proceeding, check whether `agent_readiness_add_on` is set. This flag is established in Step 1 Intake (Engagement Context). If entering a session mid-stream, ask: "Should we include the Agent Interface Readiness area?" Set `agent_readiness_add_on: true` if yes. Carry the flag through all subsequent steps — it controls whether Area 7 runs in Step 3 and whether the Area 7 section appears in the Step 5 report. Area 7 is also the diagnostic entry point for the **Agent-Readable Design Systems** service line (`ai-services/_core/ai-service-offerings.md`, Consult layer, named 2026-07-02): the ARI score names where the system stands, and that line is the path from the score to agent-deploy-ready. When presenting Area 7 findings, organize them under the frame the service line uses: Context (can an agent read the system), Skills (do agents know how to use it), Agents (is generation governed).

**Memory Hygiene Diagnostic add-on:** Check whether `memory_hygiene_add_on` is set. Relevant when the client's agents are operating against their design system in production — maintaining session summaries, correction histories, or context bundles. If yes, run the diagnostic after Step 3 (Audit Mode) using the in-house five-category extractor (`memory-mcp/hygiene_extractor.py` — self-contained, no LLM, no install; never `pip install mempalace`) against the client's agent memory corpus. The diagnostic template, benchmark ranges, and interpretation guide are in [`references/memory-hygiene-diagnostic.md`](references/memory-hygiene-diagnostic.md). Discovery question: "Do your agents maintain memory across sessions?" If yes and the client is running agents against their design system, set `memory_hygiene_add_on: true`.

**Organizational Commitment add-on (conditional — not optional for mid-market/enterprise):** This dimension is scored by default for organizations with a dedicated design system team or a federated model in a product org of 20+ people. For startup or single-product teams under ~20 people, it is not applicable — set `organizational_commitment_add_on: false` and note it in the report as "not applicable at current scale." For all other engagements, set `organizational_commitment_add_on: true`. This add-on runs after Area 6 and before Area 7 (if ARI is active). It does not require separate pre-work — the intake questions in Step 1 collect what's needed. If team size is unclear from intake, ask: "How many people work on the product, and is there a dedicated team or named owner for the design system?"

**Prototype audits → use `heyhi-prototype-audit`.** If the subject is an HTML prototype, interactive mockup, or behavioral simulation — not a design system — load `heyhi-prototype-audit` instead. The framework is identical (three-pass severity, Foundation/Critical/High/Polish phases, pre-flight, dispatch template); the entry point moved to the standalone skill in v1.8.0. Stay in this skill for system-level audits — design system health, token drift, component coverage, Figma file health, organizational commitment.

If mode is unclear, ask one question: "Do you have access to the client's materials, or are we planning the engagement first?"

---

## Step 1: Intake

Collect these if not already known. Ask as a single set — not one at a time.

**Client context**
- Company name and rough size (startup / mid-market / enterprise)
- What does their product do? (One sentence)
- How many designers and engineers work with the design system?
- How long has the design system existed?

**System context**
- What's the primary design tool? (Figma assumed unless otherwise stated)
- What's the primary frontend stack? (React / Angular / Vue / native / other)
- Does a token architecture exist? (If yes: is it in code, in Figma, or both?)
- Is there a component library? (Storybook, internal docs, or undocumented?)
- Is there a documented governance process for the system?

**Access context**
- Figma file URL or file key available?
- Figma plan tier? (Professional plan required for MCP variable resolution via `get_variable_defs`; Enterprise/Org plan + Developer seat required for Code Connect and Code Connect MCP tools)
- Codebase accessible? (Local filesystem, GitHub, or provided as files)
- Documentation accessible? (Storybook, Confluence, Notion, etc.)
- Any prior audit or assessment the client has already done?

**Engagement context**
- Is this a standalone audit or the first phase of a Build or Sustain engagement?
- Who will receive the report? (Designers / engineers / leadership / all three)
- Any known pain points the client has already named?

**Agent interface readiness add-on (optional)**
- Is the client deploying or planning to deploy agent-generated UI against this design system?
  - If yes → set `agent_readiness_add_on: true` and include Area 7 in scope
  - If no or unsure → mention briefly: "We also offer an Agent Interface Readiness assessment for teams deploying conversational or generative interfaces against their design system. It's an optional add-on — worth including?"
  - If the client mentions agents, copilots, LLM-generated UI, or "our product has a chat/AI interface" at any point in intake: that's the trigger. Flag it and confirm.

**Memory Hygiene Diagnostic add-on (optional)**
- Do agents operating in this client's environment maintain memory across sessions — session summaries, correction histories, context bundles, or always-loaded files?
  - If yes and the client is running agents against their design system → set `memory_hygiene_add_on: true`; run the diagnostic after Step 3 using the template at `references/memory-hygiene-diagnostic.md`
  - If no → skip; note that memory hygiene becomes relevant when they deploy agents against the system
  - If the client mentions "our agents get confused between sessions," "we keep re-explaining the same things," or "our context files keep growing" at any point: those are the trigger phrases. Flag and confirm.

**Organizational Commitment add-on (conditional)**
- How large is the organization (roughly) and what is the team model?
  - Dedicated DS team, or federated model, in a product org of 20+ people → `organizational_commitment_add_on: true` (default on for this scale)
  - Startup or single-product team under ~20 people → `organizational_commitment_add_on: false` (not applicable at current scale; note in report)
  - Unclear → ask "How many people work on the product, and is there a dedicated team or named owner for the design system?"
- Two questions to hold for the designer/lead interview (Area 8 will use the full interview guide):
  1. "How much of your (or your team's) time is officially protected for design system work, versus borrowed for product delivery?"
  2. "What happens to the design system if you leave?"

---

## Step 2: Planning Mode Output

If in Planning mode, produce:

**Engagement structure** — half-day vs. full-day, async vs. facilitated, who needs to be in the room.

**Pre-work request list** — what to ask the client to prepare before the audit session:
- Figma file access (view rights minimum; edit not required)
- Codebase access or component exports
- Any existing documentation
- A 15-minute interview with the lead designer and lead engineer (separately if possible)

**Area 7 pre-work (when `agent_readiness_add_on: true`):**
- Token file (JSON or equivalent) — to check `$description` field coverage before the audit session
- Component inventory in any format (Figma component page export, Storybook index, internal documentation) — to assess naming consistency and catalog structure
- Any brand brief, creative direction document, or moodboard — to assess Layer 0 artifacts
- A yes/no from the client: are they currently deploying or planning to deploy agent-generated UI against this design system?

**Interview guide** — 5–7 questions for the designer interview and 5–7 for the engineer interview. See [reference.md](reference.md) for the full question sets.

**Area 7 interview time additions:** Add 10 minutes to the designer interview. Add 5 minutes to the engineer interview. The interview questions for Area 7 are in the Area 7 block in Step 3.

**Session agenda** — time-blocked plan for the audit day.

**Planning mode output — Area 7:** If `agent_readiness_add_on: true`, include a section in the engagement structure document that describes the seventh area and what will be examined, so the client knows what to prepare. Use the opening framing from the ARI findings language section below.

---

## Step 3: Audit Mode — Six Examination Areas (Seven with Agent Readiness Add-on)

**Figma MCP availability check:** Before beginning, confirm whether a Figma MCP server connection is active in this session. Relevant tools: `get_variable_defs`, `get_design_context`, `get_code_connect_map`, `search_design_system`. If MCP access is available and the client's plan tier supports it (Professional+ for variable resolution; Enterprise/Org for Code Connect tools), use the MCP paths documented in Areas 1, 2, and 4. `search_design_system` is available on all plans — use it whenever MCP is active. If MCP is not available, all areas fall back to manual methods. Note which path was used in the report — clients with Professional or Enterprise plans will see the difference in coverage depth.

**Professional vs. Enterprise capability line, the call budget, and the Code Connect workaround:** Most clients run Figma Professional, and the audit runs fully on Professional. Before scoping the Figma-dependent areas, read the **Figma Professional Integration** section in [reference.md](reference.md). It carries the per-tier capability table (what Professional gives you vs. Enterprise), the Check Designs pre-audit differential method, the 200 calls/day MCP budget (sufficient for up to ~150 components/day; Enterprise's 600/day only matters for larger sweeps), and the Code Connect workaround. Do not scope a deliverable that depends on a tier the client does not have — the honest capability line is the deliverable.

Work through all six areas (seven if `agent_readiness_add_on: true`). Document findings as you go using the format in reference.md.

**Required: Maturity Radar Profile.** Score each dimension (1–5) as you work through the areas below. The radar profile produced from these scores is a required deliverable of every audit. It replaces a single overall grade and is included in the Step 5 report. See reference.md for the maturity model assessment section and scoring template.

**Run order:** Areas 1–6 (standard, always) → Area 8 (Organizational Commitment, if `organizational_commitment_add_on: true`) → Area 7 (Agent Interface Readiness, if `agent_readiness_add_on: true`). Area 8 maps to Dimension 8 of the maturity model. Area 7 maps to Dimension 7. Both are conditional; either or both may be active in a given engagement. See the ARI composite section within Area 7 for the sub-area-to-maturity-level mapping.

**Memory Hygiene Diagnostic (when `memory_hygiene_add_on: true`):** Run after completing all areas (after Area 7 if ARI is active). Use the template at `references/memory-hygiene-diagnostic.md`. Run `memory-mcp/hygiene_extractor.py` against the client's agent memory corpus (session summaries, correction histories, context bundles), record the classification distribution and gap analysis. Output becomes the Memory Hygiene Diagnostic section in Step 5.

### Area 1: Token Architecture

What to examine:
- Does a token hierarchy exist? (global → semantic → component-level)
- Are tokens in the W3C DTCG format or a proprietary format?
- Do token names reflect semantic roles or raw values? ("color-text-primary" vs. "#222222")
- Is there bidirectional sync between Figma and code, or one-direction only?
- Do tokens in Figma match tokens in code?
  - **If Figma MCP access is available (Professional plan + Developer seat):** Run `get_variable_defs` sweep across the design system's primary Figma file. This returns all variables in scope with their resolved values per mode and code syntax (if configured). Compare the full extraction against the client's token file from the codebase. A token present in Figma but absent from code is a gap finding. A token whose value differs between Figma and code is a drift finding. Coverage is comprehensive rather than spot-check.
  - **If Figma MCP is not available:** Sample 10–20 token values across color, spacing, and type.

- **Alpha token handling.** When comparing Figma tokens to code tokens, check specifically for color tokens that carry opacity/alpha values in Figma. Figma strips the alpha channel during variable exports — a token defined as `rgba(55, 198, 222, 0.3)` in Figma will export as the base hex value with no opacity information. The correct representation target is [W3C DTCG v1 format](https://tr.designtokens.org/format/#alpha) using `{colorSpace, components, alpha, hex}` composite notation. Acceptable workarounds: manually encode as `rgba()` in the token file, or use a Tokens Studio + sd-transforms pipeline which handles alpha-channel preservation natively. A code token that uses a plain hex value where a Figma token carries alpha is not a match — it is a data loss finding, not a value mismatch.

- **Layer 0 pipeline presence.** Does the client have a documented style source for their token decisions — a moodboard, a named style entry, or a structured translation rationale? A token system without a documented style origin can be validated for structural correctness but not for intent alignment. Check `meta.style_notes` in the `active-brand.json` config if one exists, or ask directly: "Do you have documentation of the aesthetic intent behind your token choices?" Absent = enrichment opportunity (note as a finding; this is a direct HeyHi Layer 0 onboarding candidate). Present = note the style source in findings for use in intent validation.

Drift signals to look for:
- Hardcoded values in components instead of token references
- Token names that describe appearance, not role ("blue-500" instead of "color-action-primary")
- More tokens in Figma than in code, or vice versa
- No semantic layer (raw values only, no meaningful names)
- No documented style origin for the token system (token values present with no rationale for why they were chosen)
- **Underscore-prefixed keys inside the `tokens.*` namespace** (e.g., `_note`, `_rationale`, `_context` adjacent to token values). These are documentation embedded inside a delivery surface — any standard token consumer (Style Dictionary; the now-archived design-system-ux behaved the same way) will treat every key in `tokens.*` as a token to deliver, including underscore-prefixed ones. Correct location: `meta.implementation_notes` (keyed dict) or `brand.style_notes`. Flag as a structural defect if found.
- **Alpha channel loss** — color tokens that carry opacity in Figma appear as solid hex values in code (Figma strips alpha during variable export). Correct form is DTCG v1 composite notation or manually-encoded `rgba()`. A hex value where opacity was intended is a silent data loss finding, not a drift finding. Correct with a Tokens Studio + sd-transforms pipeline or manual `rgba()` encoding in the token file.

### Area 2: Component Coverage

What to examine:
- What components exist in Figma?
  - **If Figma MCP access is available:** Run `get_design_context` sweep across the component library file. This returns the component hierarchy, including which components are from the published library vs. locally defined. Combined with a codebase component inventory (directory scan or Storybook manifest), this produces a coverage matrix: in Figma not in code, in code not in Figma, in both with divergence. Coverage is systematic rather than sampled.
  - **Additionally (all plans, when MCP is active):** Run `search_design_system` with relevant component category terms (e.g., "button", "form", "navigation", "card", "modal"). This queries all connected design libraries — not just the primary file — and surfaces components from shared or external libraries the team may be consuming. Findings here reveal: (a) whether the client is using components from multiple libraries with potential naming collisions, (b) whether needed components exist in a connected library but haven't been adopted, (c) whether shadow components exist that duplicate what's already in a shared library. This is the cross-library gap that a single-file scan can't detect.
  - **If Figma MCP is not available:** List components manually by reviewing the Figma file.
- What components exist in code? List them.
- Where are the gaps? (In Figma not in code; in code not in Figma; in connected library not adopted)
- For components that exist in both: do they match? Check props, variants, and edge cases.
- **Composite component dependencies.** For each component that internally consumes other design system components (e.g., a TrialBanner that renders a Button and an InlineAlert), verify that all consumed components are declared as explicit prerequisites — in the component's documentation, in acceptance criteria for related implementation stories, and in any PR or migration dependency graph. There is no formal industry standard for composite dependency declaration; best practice is a `composedOf` array in the component's spec (e.g., `composedOf: [Button, InlineAlert]`). Absent this, composite dependencies are invisible to planners and engineers. Check for: (a) components labeled "simple" that silently consume 2+ system components, (b) implementation plans or PRs that declare a prerequisite on one composed component but not all of them, (c) any composite component with no `composedOf` documentation.

Drift signals to look for:
- Shadow components — components built outside the system for one-off uses that should be in the system
- Variant drift — Figma has 4 button variants, code has 3 (or 7)
- Documentation lag — component exists in code but hasn't been updated in Figma in 6+ months
- Library redundancy — the same component exists in two connected libraries with different naming, causing inconsistency depending on which one engineers reference
- **Silent composite dependencies** — components that consume other design system components internally but declare no `composedOf` documentation. These cause prerequisite omissions in implementation plans and PR dependency graphs, surfacing as ordering bugs only after work begins.

### Area 3: Documentation and Governance

What to examine:
- Is there documented usage guidance for components? (When to use, when not to)
- Is there a token usage guide?
- Is there a contribution process for adding new components?
- Is there a deprecation process for removing old ones?
- Is there a named owner of the design system?
- When was documentation last updated? Does it reflect the current state of the system?

Drift signals to look for:
- No governance document or process
- Documentation exists but is acknowledged by the team as out of date
- Multiple owners with no clear decision-maker
- Contribution happens informally (Slack threads, tribal knowledge)

### Area 4: Figma File Health

What to examine:
- Is there one source-of-truth Figma file, or multiple competing files?
- Are components using Figma variables (linked to tokens) or hardcoded styles?
- Are layers named meaningfully or using default names ("Frame 47", "Rectangle 3")?
- Is there a published component library, or are components duplicated across files?
- Are Code Connect mappings in place?
  - **Figma MCP check (Enterprise/Org plan + Developer seat required for Code Connect tools):** Run `get_code_connect_map` to retrieve all active Code Connect mappings. This confirms coverage, identifies components with no mapping, and flags mappings pointing to deleted or renamed code files (stale mappings). Run `get_code_connect_suggestions` to surface components Figma has identified as Code Connect candidates not yet mapped. Both outputs become audit findings.
  - **If client is not on Enterprise/Org plan or Figma MCP is not available:** Review Code Connect status manually in the Figma Dev Mode panel. If Code Connect is not configured at all, flag as a finding — not a plan tier gap. On Professional (the common case), Code Connect and its MCP tools are unavailable; see the **Code Connect: the Professional workaround** subsection in [reference.md](reference.md) for how to handle this without promising an Enterprise capability HeyHi cannot deliver on the client's plan (T2.4, confirmed Enterprise-only).

Drift signals to look for:
- Detached components in design files (instances that have been broken from the library)
- Multiple versions of the same component across different files
- Hardcoded color/spacing in Figma components instead of variable references
- No Code Connect — Figma and codebase are not semantically linked

### Area 5: Accessibility Baseline

What to examine:
- Do text/background color combinations meet WCAG 2.1 AA (4.5:1 for normal text, 3:1 for large)?
- Do interactive elements meet minimum touch target size (44×44px)?
- Do form inputs have visible labels?
- Do focus states exist and are they visible?
- Is there keyboard navigation support in interactive components?
- **Dark mode token propagation.** When the client has implemented dark mode via a CSS class strategy (e.g., `.dark` on the root element with CSS custom property overrides), verify that recently migrated components have explicitly defined dark mode token values — not just inherited or fallen back to light mode values. Token migration moves a component from hardcoded values to token references; it does not automatically populate the dark mode tier. A component that correctly uses semantic tokens in light mode but has no `.dark` overrides for those tokens is partially migrated. Check: (a) sample 3–5 recently migrated components; (b) inspect the token file's dark mode section for each component's relevant tokens; (c) if a token has a light mode value but no dark mode value, it is a propagation gap. Note in findings as a medium severity — it is an accessibility concern (contrast in dark mode is unknown or inherited from default) and a token architecture gap simultaneously. Note: this check is distinct from the alpha token export limitation in Area 1; both concern token completeness for non-default states but address different failure modes.

**W3 — Brand color WCAG compliance check.** Run: `grep -rn "text-accent\|text-brand-primary\|text-cerulean\|text-sunshine" src/`. For any hit where the parent surface is white, light gray, or near-white, verify the contrast ratio. Brand accent colors typically fail WCAG AA as foreground text on light surfaces (cerulean-class colors compute ~2.01:1; sunshine-class colors compute ~2.4:1 — both fail the 4.5:1 threshold for normal text). Flag each violation by file and line. The correct use of brand accent colors is as **background surfaces with dark foreground text**, not as text on white. This is a systematic audit pattern: the failure is predictable in any design system that uses a cerulean or yellow brand accent color.
*Maturity signal: A system with no `text-accent` violations on light surfaces is actively enforcing token semantics. A system with 5+ violations is operating on implicit convention, not explicit governance.*

**W4 — CVA focus ring migration check (if codebase uses CVA).** When auditing components built with class-variance-authority: confirm that every interactive component's focus ring is defined in the CVA **base string**, not in a companion `.scss` or `.module.css` file. The failure mode: SCSS focus rings are silently dropped when a component is migrated to CVA because CSS specificity no longer reliably targets CVA-generated class strings. A component with a SCSS focus ring rule and no corresponding `focus-visible:ring-*` in the CVA base string will render without a focus ring after any CVA update. Audit method: `grep -rn "focus" src/components/[Name]/*.scss` for SCSS focus rules, then verify each has a corresponding `focus-visible` in the CVA base string. Components that use keyboard input (buttons, inputs, tabs, checkboxes) are highest priority. Missing focus rings on these components are a Critical a11y severity finding.
*Maturity signal: If no CVA base strings contain `focus-visible:ring-*`, the codebase is operating with inherited or browser-default focus styles — usually missing entirely on `preflight: false` Tailwind configs.*

Note: This is a spot-check, not a full accessibility audit. Flag what you find and note that a full audit should be a separate engagement if significant issues are identified.

**Area 5 drift signals:**
- **Dark mode propagation gaps** — components using semantic tokens in light mode with no corresponding dark mode token values. These appear correct in light mode and break silently in dark mode. They are the most common output of a partial migration.
- **Focus ring regression** — interactive components with no visible focus ring after a recent refactor. The most common cause: focus ring defined in SCSS lost when component migrated to CVA (see W4).

### Area 6: Team Relationship to the System

This is qualitative — based on the intake interviews. What you're listening for:

- Do designers trust the system, or do they work around it?
- Do engineers know the system exists and know how to use it?
- Is there shared ownership, or is it one person's project?
- What's the team's stated reason for the system not being used more?
- What does a "good week" with the design system look like to them?

This area often surfaces the real issue. A technically sound system that nobody trusts is a different problem than a technically unsound system the team wants to use. The fix is different in each case.

### Area 8: Organizational Commitment *(Conditional — run when `organizational_commitment_add_on: true`; default on for mid-market and enterprise engagements)*

This area examines the institutional conditions that determine whether the design system is funded, sponsored, staffed, and sustained over time. It measures what is upstream of governance effectiveness — not whether governance artifacts exist (that is Area 3), but whether the organization has made the commitments required to make those artifacts function.

**Why this is distinct from Area 3:** Area 3 scores the existence and quality of governance processes. Organizational Commitment scores whether those processes are actually resourced and protected. A team can have a documented contribution process (Area 3 = Level 3) and have the reviewer's time cut 50% last quarter, with no authority to restore it. Area 3 would not catch this. Area 8 does. The gap between a client's Area 3 score and their Area 8 score is itself a finding.

**Why this precedes Area 7 in the run order:** Organizational Commitment is upstream of agent deployment decisions. A team considering ARI investment needs organizational commitment first — infrastructure improvements require sustained maintenance.

**Data sources:** Primarily qualitative. Use the designer/lead interview and, separately, a product or engineering leader interview. Divergence between what the design system owner says and what their manager or a consuming team lead says is the most diagnostic signal in this area. Score the lower answer.

What to examine:
- Is there protected, funded time for design system work — or is it borrowed from product delivery and reclaimed whenever a sprint is under pressure?
- Does leadership understand what the design system is and why it requires ongoing investment (not just initial build)?
- Is there a defined contribution model, and do consuming teams actually participate under it?
- Is budget for the system explicit and visible — or embedded inside another team's budget where it can disappear without a decision?
- What is the succession plan if the design system owner leaves? Is there one?

Drift signals to look for:
- "We built the design system last year, but nobody really maintains it anymore" — maintenance velocity collapse; the classic organizational commitment failure
- "I contribute to it when I have spare capacity" — contribution culture is voluntary and therefore absent under pressure
- "The system is great but leadership doesn't really fund it" — the explicit version; Area 3 may score high, Area 8 scores low
- The design system lead cannot answer "what happens when you leave" — no succession structure
- The product/engineering leader cannot name the contribution model or estimate how often teams contribute back

**Interview questions:**

*For the design system lead (add 15 minutes to the designer interview):*
1. "How much of your time (or your team's time) is officially protected for design system work, versus borrowed for product delivery?" — *Most diagnostic for scoring; 0% = Level 1, informal/untracked = Level 2, formally protected = Level 3+*
2. "When has the design system budget been cut, and what happened? Who made the call to restore it?" — *Level 3+ orgs have a story where leadership defended or restored resources. Level 1–2 orgs say "it never recovered" or have no budget story at all.*
3. "How does a consuming team contribute a new component today? What's the expected turnaround from submission to decision?" — *Level 2: vague, informal. Level 3: defined SLA. Level 4: SLA is tracked and reported.*
4. "What happens to the design system if you leave?" — *The single most diagnostic question. Level 1–2: "It probably struggles." Level 3+: a succession structure or team exists.*

*For a product or engineering leader (not the design system owner; add 10 minutes):*
1. "What would have to happen for you to reduce investment in the design system?" — *Level 3+: no plausible scenario. Level 1–2: they name a very plausible one.*
2. "Do your teams contribute back to the design system? How often, and is it expected or voluntary?" — *Level 3: expected. Level 2: voluntary. Level 1: not considered.*
3. "When was the last time you discussed the design system in a planning or roadmap meeting?" — *Level 3+: regularly. Level 1–2: "I'm not sure I have."*

**Scoring rubric:**

| Score | Criteria |
|-------|---------|
| 5 | The system is a recognized strategic organizational asset. Leadership defends its value in terms the rest of the product org understands. Contribution culture is self-sustaining — consuming teams contribute back as part of normal delivery, not as heroics. Organizational commitment survives leadership changes and team reorganizations. The system has a product roadmap that receives the same investment process as other product areas. |
| 4 | Organizational commitment is quantifiable: headcount is tracked, budget is explicitly allocated, contribution velocity is measured. Leadership receives periodic health reports and acts on them. Attrition of system team members triggers a replacement process. There is a documented SLA for contribution review and it is tracked. |
| 3 | A named owner or small team has protected, funded time for system work. Leadership can articulate why the system exists and shields it from arbitrary reprioritization. There is a formal contribution expectation with a documented process. Budget is explicitly allocated and visible. Contribution review has a defined SLA even if not yet measured. |
| 2 | At least one named person has some protected time for the design system. Leadership is aware the system exists and broadly supportive. Consuming teams occasionally contribute but without structure or expectation. Budget is informal or embedded in another team's budget without visibility. |
| 1 | No organizational support structure. The system is a side project of whoever built it, with no dedicated time, no leadership sponsorship, and no contribution model. The system exists because one person cares about it. Budget is zero or unclear. |

**Scoring heuristic:** If the design system lead and a product/engineering leader give significantly different answers to the same question, score the lower answer. Organizational commitment is as strong as its least informed stakeholder with budget authority.

**Findings language:**

*Score 1–2:*
> "The design system is technically [describe state] but organizationally unsupported. The most common reason technically sound design systems fail is not a token architecture problem or a component coverage gap — it is organizational. When maintenance velocity drops because the owner's time is borrowed, contribution dries up because no one is reviewing, and adoption degrades because teams stop trusting a system that doesn't respond. The engineering work in this engagement is only durable if the organizational conditions improve alongside it."

*Score 3:*
> "Organizational commitment is systematic — the system has a protected owner, a defined contribution model, and visible budget. The next investment is making that commitment measurable: tracking contribution velocity, SLA adherence, and maintenance throughput. When those become numbers on a report, leadership can act on them rather than operating by feel."

*Score 4–5:*
> "Organizational commitment is one of the strongest factors in this system's health. The institutional conditions are in place. The maintenance work here is staying deliberate — commitment at scale can drift into process for its own sake. Keep the metrics tied to outcomes the product org recognizes."

**Retainer pivot:**
> "Your system scores [N] on Organizational Commitment. The technical infrastructure work we're scoping will last as long as the organizational conditions support it. A Care retainer includes a quarterly commitment health check alongside the technical monitoring — making sure both stay current."

### Phase: Variant Naming Audit

**Trigger:** Any component set containing auto-generated variant names (`VariantN`, `TypeN`, `Property 1=X`) or unnamed property dimensions (`Property 1`, `Property 2`).

**Steps:**

1. **Screenshot every unnamed variant individually.** Call `get_screenshot` on each variant node ID. Do not attempt to identify variants from metadata or design context alone — visual inspection is required.

2. **Build a rename map.** For each variant, assign a descriptive name in `Dimension=Value` format (e.g., `State=Color-Picker-Open`, `Type=Icon-Selected`). Naming rules:
   - Dimension name: describes the axis of variation (State, Type, Mode, Size)
   - Value name: describes the visual/interaction state in plain terms
   - Spell out state labels completely: `Selected` not `Sel`, `Disabled` not `Dis`, `Icon-Only` not `Icon`. Exception: abbreviations already established as convention in the existing design system (e.g., `MD` for Medium if already present throughout) may be preserved for consistency
   - Flag duplicate names at the same dimension — these indicate variants merged from separately-created components and each needs a unique name

3. **Check both hierarchy levels.** If the product has both a Design System file (sub-component masters) and an Application file (full panel interaction states), both may have naming debt at different hierarchy levels. Audit and rename separately — they are not duplicates.

4. **Execute via `use_figma`.** Iterate component set children, match by node ID, set `node.name`. For variants not in the explicit rename map: only apply a fallback `Property 1=X` → `State=X` substitution if `State` has already been established as the correct dimension name for this component set (i.e., at least one variant in the rename map uses `State=`). Do not apply a blanket `Property 1` → `State` conversion if the dimension has not been identified — leave those unmatched entries as-is and flag them in the log for manual review. If the script encounters an error mid-execution, surface it via `figma.notify('[Variant Rename] failed at step N: [description]', { error: true })` before returning — do not continue after failure. Return a full log of before/after names including any skipped variants.

5. **Verify.** Screenshot the full component set after rename to confirm the property dimension name updated correctly in the Figma properties panel.

**Output:** A complete rename log with node IDs, old names, and new names — filed in session handoff.

**Improvement hook:** Were there variants that needed both a name correction AND a visual content correction (wrong content in the variant)? If so, batch those together rather than running separate scripts.

### Area 7: Agent Interface Readiness *(Add-on — run only if `agent_readiness_add_on: true`)*

This area examines how prepared the design system is to serve as the constraint surface for agent-generated UI — the layer that keeps automatically generated interfaces on-brand, structurally valid, and consistent with design intent. Produces an **Agent Readiness Index (ARI)**: a composite score across four sub-areas, each scored 1–4.

**Opening framing (use in reports and planning documents):**
> "Agent Interface Readiness examines how prepared this design system is to serve as the constraint surface for agent-generated UI — the layer that keeps automatically generated interfaces on-brand, structurally valid, and consistent with design intent. Most design systems aren't here yet, which is why we're looking at it now rather than when your team is three months into deploying it."

**Figma MCP note for Area 7:** MCP paths are documented for 7.1 and 7.2. Follow the same availability check as Step 3 header — if MCP is active and the client is on Professional plan or above, use the MCP path. Otherwise use the manual fallback. Note which path was used.

---

#### 7.1 — Semantic Token Depth

Agents reasoning against a design system need to understand not just what tokens *are* but when to use them and why. Empty `$description` fields are structurally invisible to agents.

**What to examine:**
- What percentage of tokens have `$description` fields populated beyond empty or physical-property-only values?
- Do descriptions convey design intent ("use when the primary action must be unambiguous to the user") or only physical properties ("#1A73E8, 4px border-radius")?
- Are contextual constraints encoded — which tokens belong to which surfaces, which combinations are intentional, which are prohibited?
- Does description coverage extend across all semantic tiers, or only at the primitive level where reasoning doesn't happen?

**MCP examination path (when Figma MCP is active):**
Run `get_variable_defs` across the client's primary design system file. The returned variables include their `description` field values where populated. To assess coverage: count variables with a non-empty `description` vs. total variables. To assess quality: read 5–10 sampled descriptions across color, spacing, and typography tokens. Descriptions that contain only hex values, pixel values, or names that repeat the token name are physical-property descriptions — not intent descriptions.

**If Figma MCP is not available:** Request the client's token file (JSON or YAML). Check `$description` population manually across a sample of 20+ tokens spanning all semantic tiers.

**Scoring rubric:**

| Score | Criteria |
|-------|---------|
| 4 | ≥75% of semantic tokens have `$description` fields. Descriptions convey design intent, not just physical properties. Contextual constraints are encoded for at least core tokens (color.action.*, spacing.component.*, etc.). |
| 3 | 40–74% description coverage. Intent-level descriptions present but incomplete — core tokens described, component-specific tokens largely empty. No contextual constraint encoding. |
| 2 | <40% coverage and/or descriptions describe only physical properties. The agent can read token values but not reason about when to use them. |
| 1 | Fewer than 10% of tokens have descriptions, or descriptions are entirely absent. The token system cannot serve as a constraint surface for agent reasoning in any meaningful way. |

**Provisional threshold note:** The 40% threshold is a structural benchmark, not an empirically calibrated threshold. It represents the point at which coverage is sparse enough that agents cannot reliably find relevant descriptions even for common semantic categories. Flag as provisional in any report that cites it. Revisit after five completed audits.

---

#### 7.2 — Component Catalog Structure

A2UI's security model rests on a component whitelist — agents can only request components from a pre-approved catalog. If no coherent catalog exists, agents can't reason against it.

**What to examine:**
- Is there a formal component inventory (a unified manifest), or do components live only in Figma and the codebase without a single source?
- Are component names consistent across Figma, code, and documentation? Agents reason against names — "Button" in Figma, "Btn" in code, "PrimaryButton" in docs means the catalog is fragmented.
- Are component props available in a static machine-readable format (JSON Schema, TypeScript interface exports, a props specification file)? Note: Storybook exposes props machine-readably via CSF args and TypeScript types, but requires a running server — a static props schema file is more reliable as a constraint artifact.
- Could a subset of components be identified from a task intent description without loading the full catalog? That's the difference between a flat list and a structured catalog with categories, use-case tags, or semantic groupings.
- **Adopted third-party agent UI.** Has the organization adopted any MCP Apps, and if so, does it know which of them honour its design tokens? Is anything checking? See the diagnostic block below before asking this one.

**Adopted third-party agent UI — the diagnostic question**

The MCP Apps extension went `Final` and ships in the 2026-07-28 MCP specification. When a host application loads an MCP App, it passes the view a `hostContext.styles.variables` object carrying its own CSS custom properties for colour, font and border radius. The view is invited to use them. Nothing requires it to, and nothing verifies whether it did. A view that ignores the host's variables entirely and hardcodes its own colours is fully spec-compliant.

So the question for a client that has adopted any of these is simply:

> "Which of the agent-facing views you've adopted actually honour your tokens, and what tells you when one stops?"

**Ask it as a diagnostic, not as a pitch.** Most teams will not have an answer, and the honest reason is that no tooling exists to produce one — not from HeyHi, not from the host vendors, not from anywhere as of 2026-07-19. The finding is the gap itself, and naming it early is the value. Do not imply that HeyHi ships a conformance checker for this. If the client asks what would answer the question, the accurate response is that it is deterministically answerable in principle by reading each view's CSS against the host's published variable set, and that nobody has built it yet.

**How it scores:** this question feeds the existing 7.2 score on the same 1–4 scale — it does not add a sub-area, and the ARI formula is unchanged. Read it as evidence about how far the catalog extends beyond first-party components:
- A client with adopted third-party views, a record of which ones they are, and any check on token conformance is showing catalog structure that reaches past its own codebase (supports 3–4).
- A client with adopted views and no record of which honour its tokens has a catalog boundary it cannot see past (supports 2).
- A client that has adopted none is **not penalised** — mark the question not applicable and score 7.2 on the other bullets. Score the system in front of you, not the one that hasn't arrived.

**MCP examination path (when Figma MCP is active):**
Run `search_design_system` with broad categorical terms ("button", "form", "input", "card", "navigation", "modal", "table"). This queries across all connected design libraries. Look for: naming collisions across libraries (same concept, different names), naming instability (same component named differently in different files), whether the catalog has semantic groupings or is a flat list.

If `get_design_context` is available: run it across the component library file to retrieve the full component hierarchy. Check for: consistent naming conventions, published library components vs. local/one-off components, and whether the component organization gives structural hints about when to use what.

**If Figma MCP is not available:** Request a component list from the client (Storybook index, Figma component page, or internal documentation). Assess naming consistency by scanning for synonyms, abbreviations, and version suffixes in simultaneous use.

**Scoring rubric:**

| Score | Criteria |
|-------|---------|
| 4 | A unified component manifest exists independently of Figma and Storybook. Names are stable and consistent across all surfaces. Props are available in a static machine-readable format. Components have categorical or semantic groupings sufficient for discovery-aware loading. |
| 3 | Components are well-documented in at least one surface (Figma or Storybook) with consistent naming. No unified manifest, but names are stable enough that one could be generated. Props are accessible through Storybook (requires render context). No semantic groupings or discovery structure yet. |
| 2 | Components exist in both Figma and code but with naming inconsistencies across surfaces. No unified manifest. Props exist in code but are undocumented or inconsistently documented. A catalog would require significant naming reconciliation before it could serve as a constraint surface. |
| 1 | No component inventory exists. Components are scattered across Figma files and the codebase with no consistent naming or organizational structure. Building an A2UI catalog from this state requires a full component audit first. |

---

#### 7.3 — HITL Checkpoint Coverage

When agents generate UI, decisions have different reversibility profiles: draft layouts are reversible; publishing to production, modifying the component catalog, or changing brand tokens are not. This sub-area examines whether the team has thought through which agent actions need human review.

**Scope distinction from Area 3:** Area 3 examines governance of *human* contributions. This sub-area examines governance of *agent-generated* output specifically. The failure modes are different: human contributions are slow and intentional; agent contributions can be fast and accumulative.

**What to examine:**
- Does the team have any explicit policies about which agent actions require human review before taking effect? Even informal ("we always review before publishing") counts at score 2.
- If an agent generates something off-brand or outside the constraint surface, is there a review step before it reaches production?
- Who has authority to modify the component catalog? Is agent-generated catalog extension treated differently from human-proposed extension?
- Does the team know the HITL question is coming? Teams that haven't begun to think about agent-generated UI won't have policies — this sub-area surfaces the gap and seeds the conversation.

**Interview questions for the designer and engineer interviews (Area 7.3):**
- "If an agent generated a new page layout using your design system components, who would review it before it went live? Is that in anyone's job description?"
- "If an agent proposed adding a new component to your library, what would have to happen before it was accepted?"
- "Do you have any situations today where automated tools generate output that has to be reviewed before shipping? How does that work?"

**Scoring rubric:**

| Score | Criteria |
|-------|---------|
| 4 | Reversibility is explicitly mapped — the team can list which agent actions require review, which can proceed autonomously, and why. Escalation path is documented with a named reviewer. Catalog modification by agents has its own governance process, separate from human contribution. |
| 3 | Informal HITL exists — agents' output is reviewed before publishing but the process is undocumented, relying on whoever happens to be doing the work. Catalog governance exists for humans but hasn't been extended to cover agent-generated entries. |
| 2 | The team is aware that agent-generated output needs review but hasn't formalized anything. No escalation path beyond "ask someone." Catalog governance applies to humans; agent entries are a new concept. |
| 1 | No HITL awareness specific to agent-generated output. The team hasn't considered how agent generation changes their review process. Score 1 is normal for teams not yet deploying agent-generated UI — this sub-area identifies the gap, not a failure. Do not remove the add-on scope because of a score-1 here; the finding is the value. |

---

#### 7.4 — Layer 0 Signal (Taste Infrastructure)

This is the most frequently absent element and the hardest to remediate quickly. A system can have perfect token descriptions and a machine-readable catalog and still produce aesthetically incoherent output if the agent has no access to why the visual decisions were made. Tokens encode what the system contains; Layer 0 encodes what the system is trying to express.

**What to examine:**
- Does the design system have any record of why the visual decisions were made? Moodboard references, aesthetic rationale, named style clusters, or documented design philosophy all count.
- Is there a translation layer that explains how the aesthetic intent became specific token values? "We chose this text color because the brand reads as grounded and serious, not clinical" is Layer 0. A hex value is not.
- Could someone reading the design intent documentation understand what the system is trying to express — well enough to evaluate whether generated output is on-brand?
- Are Layer 0 artifacts (moodboards, creative briefs, brand manifestos, named style entries) connected to the design system, or floating independently?

**Scoring rubric:**

| Score | Criteria |
|-------|---------|
| 4 | Layer 0 documentation is structured and connected to the token system. Style rationale explains specific token decisions. A named style entry or equivalent design philosophy document exists and references the visual language the tokens encode. An agent given this documentation could meaningfully distinguish on-brand from off-brand output. |
| 3 | A moodboard, brand brief, or creative direction document exists and is accessible — but it's not formally connected to the token system. The aesthetic intent is documentable; it's just not documented *in* the design system. Style rationale exists informally in the heads of the original designers. |
| 2 | Some aesthetic documentation exists (a style guide with color names and type specimens) but it describes what exists rather than why. No connection between visual decisions and the intent behind them. |
| 1 | No aesthetic documentation exists, or what exists has been lost. Most design systems score 1 or 2 here. Score 1 is not a failure — it's the entry point for HeyHi's Layer 0 enrichment work. Name the gap and use it to open the conversation. |

---

#### Interview Guide — Area 7

Add these to the designer and engineer interviews. They can be asked regardless of whether the client has expressed interest in agent-generated UI — the answers are diagnostic even when the client hasn't thought about it yet.

**For the designer interview (add 10 minutes):**
1. "When you created the token system — what was the thinking behind the naming? Were there aesthetic principles or design intent behind specific decisions, or did the naming emerge more practically?"
2. "Do you have a brand brief, moodboard, or creative direction document that describes what the design system is *trying to say* visually — not just what it contains?"
3. "If someone new joined the design team today, what would they read to understand the aesthetic intent of the system?"

**For the engineer interview (add 5 minutes):**
1. "Are your component props documented anywhere in a format that doesn't require running Storybook — like a JSON schema or a static manifest file?"
2. "If a tool generated a new component using your design system tokens, who would have to sign off before it shipped?"
3. "Is there anything in your component library right now that constrains which components can be used on which surfaces — or is it up to the designer's judgment?"

---

#### Conformance sub-area — DESIGN.md Conformance *(capability sub-area — produces a conformance verdict, NOT a fifth ARI axis; the ARI composite stays the 7.1–7.4 average, unchanged)*

7.1–7.4 ask whether the *system* is ready to constrain agent-generated UI. This sub-area asks the closing question: **did a *generated output* actually honor the system it was generated against?** It reads one generation produced against the client's own intent-rich DESIGN.md and returns a **conformance verdict** — the loop that 7.1–7.4 open, closed. It rides the existing `agent_readiness_add_on` flag (no separate flag) and runs when a generation *and* its DESIGN.md are in hand: at audit-time to make the readiness score concrete, or generation-time as the check an agent runs on its own output. Full rubric and report template: [`references/conformance-sub-area.md`](references/conformance-sub-area.md); Gate G2 calibration proof: the instance's own calibration record, `references/conformance-calibration.md` (instance-only: one instance's run against its own DESIGN.md, not shipped with the scaffold; a new instance records its own).

**Gate (G1 + G1B):** it audits *against* two surfaces, so both must exist — the system's intent-rich DESIGN.md and the `design-fundamentals` reference. If either is absent, it does not run; there is nothing to conform *to*.

**Four axes** (the first blocks; the other three are judgment rubrics — a finding is a *flag*, never an automatic failure, because the carve-out is where judgment lives):

1. **Functional floor (mechanical, automated, blocking).** Reuse `heyhi-mcp` `validate_output`; do not reimplement hex / scale / contrast / state detection. Feed the generation's *declared structured output* (components with `states` + `tokens_used`), not compiled CSS — a browser resolves tokens to hex, so a stylesheet false-fails every real page on Rule 1. Use `full_page` / `component` mode; never a flat `token_usage` bag for a page. **Instance-keyed:** pass the client's own token set, legal-pair set, and any out-of-palette feature-styling declaration via the tool's `constraints` param — the floor reads the *instance*, not HeyHi's tokens. A floor failure is a fail regardless of how the output looks.
2. **Intent adherence (judgment).** Does the output honor the DESIGN.md's `## Intent` and `## Composition` — the reference feel, the sanctioned layout patterns, the right component for the intent — and the taste boundary (`not_a_departure_if`: restraint vs. incoherence)?
3. **Anti-tell scan (judgment, carve-out-gated, instance-keyed).** Scan the rendered output against **the instance's own DESIGN.md anti-tell list**, cited by ID. HeyHi's `visual-anti-tells.md` (AT-1…AT-10 + carve-outs) is *HeyHi's* instance list, not a universal catalog — a tell for one house is a signature for another. A match is a finding only when no carve-out applies. No declared list → no instance-specific findings (Axis 4 still covers the brand-agnostic build tells).
4. **Fundamentals adherence (brand-agnostic, from `design-fundamentals.md`).** The additive check the floor structurally cannot make: the full control-state contract (A.3 — `default / hover / focus / active / disabled / loading / error`), the binding UX laws (A.2), the A.1 hierarchy. A component that passes `validate_output` at 1.0 can still be missing `active` / `loading` / `error` — a clean floor is not "states complete."

**The visual loop (axes 2 and 3 need the *rendered* output).** Render the generation (browser-preview tooling), screenshot the surface plus the interaction-state views (forms, buttons, empty / loading / error), and critique specifically — name the element, the observed value, and the reference it violates or honors. Record which surfaces were captured; a verdict from the hero alone is a partial audit and says so.

---

#### ARI Composite

**Formula:**

```
ARI = (score_7.1 + score_7.2 + score_7.3 + score_7.4) / 4
```

**⚠️ Do not round the ARI composite.** Because sub-area scores are integers 1–4, the composite is always an exact multiple of 0.25 (i.e., 1.0, 1.25, 1.5, 1.75 ... 3.75, 4.0). Report the exact fraction. If implementing in code, use the raw result of `sum / 4` without a `round()` call — Python's banker's rounding converts 3.25 to 3.2, which would incorrectly map scores of [3,3,3,4] to Level 3 instead of Level 4.

**ARI → Maturity Level mapping:**

| ARI Composite | Maturity Level | One-sentence interpretation |
|---------------|---------------|-----------------------------|
| 1.0 – 1.74 | Level 1 — Not ready | System cannot serve as a meaningful constraint surface for agents in its current state. |
| 1.75 – 2.49 | Level 2 — Foundational gaps | Structural gaps exist. Targeted enrichment required before agent deployment. |
| 2.50 – 3.24 | Level 3 — Partially ready | Meaningful constraint surface with focused investment. Agent-generated output would be partially constrained; human review required for consistency. |
| 3.25 – 3.74 | Level 4 — Substantially ready | HITL still required for edge cases and catalog modifications, but infrastructure is substantially in place. |
| 3.75 – 4.0 | Level 5 — Agent-deploy ready | Agent-deploy ready for most use cases at scale. |

**Weighting note:** All four sub-areas are load-bearing — absence of any one creates a qualitatively different failure mode. Simple average is used until calibration data from real audits is available. Revisit weighting at the first five audit completions.

---

#### ARI Findings Language

The ARI should be introduced in the report before the sub-area breakdown. The framing matters: most clients score 1–2, and that's normal.

**Opening framing (use for any ARI score):**
> "Agent Interface Readiness examines how prepared this design system is to serve as the constraint surface for agent-generated UI — the layer that keeps automatically generated interfaces on-brand, structurally valid, and consistent with design intent. Most design systems aren't here yet, which is why we're looking at it now rather than when your team is three months into deploying it."

**Score-specific framing:**

*ARI 1.0–1.74 (Level 1):*
> "Your system scores [X] on Agent Interface Readiness. This means the current infrastructure — token descriptions, component catalog structure, HITL policies, and design intent documentation — isn't in place to meaningfully constrain agent-generated output. That's the starting point for most organizations. The audit identified the specific gaps; here's what investment looks like to reach Level 3, which is the threshold for meaningful agent deployment."

*ARI 1.75–2.49 (Level 2):*
> "Your system scores [X] on Agent Interface Readiness. Foundational elements are present — there's something to work with — but specific structural investments are needed before agent-generated UI would be consistently on-brand. The sub-area breakdown below shows where the return is highest."

*ARI 2.50–3.24 (Level 3):*
> "Your system scores [X] on Agent Interface Readiness. It's a meaningful constraint surface today — an agent reasoning against it would produce output that's partially guided by the system's intent. With targeted investment in [the weakest sub-area], it's ready for bounded agent-generated UI with human review in the loop."

*ARI 3.25–4.0 (Level 4–5):*
> "Your system scores [X] on Agent Interface Readiness. The infrastructure for agent-generated UI is substantially in place. The remaining work is operational — HITL policies, catalog governance at scale, and ongoing enrichment — rather than structural."

**Retainer conversation pivot:**
> "Your system scores [ARI] today. Here's what it needs to reach [target] — which is the threshold for [use case, e.g., agent-generated UI with meaningful design constraint]. That's a Design System Care engagement, not a rebuild."

---

## Step 4: Severity Scoring

For each finding, assign a severity level. See [reference.md](reference.md) for the full rubric and language.

| Level | Meaning |
|---|---|
| **Critical** | Causing active harm — inconsistency shipping to production, accessibility failures, team working around the system entirely |
| **High** | Significant drift that will compound — token gaps, major coverage holes, no governance |
| **Medium** | Real problems that are manageable now but will get expensive — documentation lag, Figma file health issues |
| **Low** | Best-practice gaps that aren't causing immediate pain — naming conventions, minor coverage mismatches |

---

## Step 5: Report Mode — Produce the Audit Report

Structure: see [reference.md](reference.md) for the full template.

Summary section first: what's the overall picture in 3-5 sentences. Not a score. A diagnosis.

**Maturity radar profile:** Include the six-dimension radar profile scored during the audit (seven dimensions if `agent_readiness_add_on: true` — add Dimension 7 as the seventh axis at the ARI composite score mapped to its maturity level). This replaces a single overall grade. The radar shape tells the story: balanced systems need care, spiked systems need specific investment, flat systems need foundational work. See `design-system-maturity-model.md` for the full framework, advisory warnings, and how dimension scores map to recommended engagements.

Then findings by area, each with: what was found, severity, why it matters, and one concrete next step.

End with: the recommended path forward, informed by both the severity findings and the maturity radar profile. The maturity model maps dimension advancement to specific HeyHi engagement types.

**Coverage note in report:** If the audit used Figma MCP paths for Areas 1 and/or 2, include a brief note in the methodology section: "Token extraction and component inventory were performed via automated scan of the client's Figma file rather than manual sampling. Coverage is comprehensive." This is a credibility signal with engineering audiences.

**Area 8 report section (when `organizational_commitment_add_on: true`):** Include after the Area 6 findings section, before Area 7. Use the template below.

### Area 8: Organizational Commitment *(Step 5 Report Section)*

**Score: [N / 5] — Dimension 8: Level [N]**

| Factor | Observation |
|--------|-------------|
| Protected time / headcount | |
| Leadership sponsorship | |
| Contribution model | |
| Budget visibility | |
| Succession / resilience | |

**[Score-specific findings language — use the Area 8 block above]**

**Gap to Area 3:** If the score here is meaningfully lower than the Area 3 (Documentation and Governance) score, name the gap explicitly: "The governance processes are documented but not resourced. The organizational conditions needed to run them are at Level [N]; the processes themselves are at Level [M]. Closing that gap is the first priority — infrastructure investment on top of it will not stick."

**Area 7 report section (when `agent_readiness_add_on: true`):** Include after the Area 8 section (or after Area 6 if Area 8 is not active).

**Memory Hygiene Diagnostic section (when `memory_hygiene_add_on: true`):** Include after Area 6 findings (or after Area 7 if ARI is active). Use the five-component structure from `references/memory-hygiene-diagnostic.md`: classification distribution table with benchmark ranges, capture-vs-load gap analysis, over-weighting signals (>40% in one category), two or three behavioral implications, one recommended action.

### Area 7: Agent Interface Readiness

**ARI Score: [X.XX / 4.0] — Dimension 7: Level [N]**

| Sub-area | Score | Notes |
|----------|-------|-------|
| 7.1 Semantic Token Depth | [1–4] | |
| 7.2 Component Catalog Structure | [1–4] | |
| 7.3 HITL Checkpoint Coverage | [1–4] | |
| 7.4 Layer 0 Signal | [1–4] | |

**[Opening framing paragraph — use the standard framing from Area 7 block]**

**[Score-specific framing — match to ARI composite level]**

**Path to Level [N+1]:** [Specific steps ordered by impact, grounded in the sub-area findings]

**DESIGN.md Conformance verdict** *(separate capability verdict — include only if the conformance sub-area ran; not an ARI row, the ARI composite is unchanged)*

Report the per-axis result, then the overall verdict. Full template and finding shape: [`references/conformance-sub-area.md`](references/conformance-sub-area.md) § 2.4.

| Axis | Verdict | Notes |
|------|---------|-------|
| Functional floor (blocking) | PASS / **FAIL** | `validate_output` result; cite the failing rule numbers. A FAIL caps the overall at FAIL. |
| Intent adherence | PASS / FLAG | vs. the reference feel, composition, right-component-for-intent, and the taste boundary |
| Anti-tell scan | PASS / FLAG | the instance's tell IDs, each with the carve-out judgment (fired / carved-out and why) |
| Fundamentals adherence | PASS / FLAG | A.3 control-state contract, A.2 binding laws, A.1 hierarchy |
| **Overall** | **CONFORMS / DRIFTS** | + a confidence read; DRIFTS if the floor fails or a judgment axis carries material, non-carved-out findings |

Then, per axis with a finding: **What we found** (the specific element, observed value, and reference it violates) · **Severity** (graded by the A.1 order: Accessibility → Interaction → Visual → Brand → Code) · **Why it matters** (the concrete cost) · **Next step** (one concrete fix).

**Coverage note:** If Area 7 ran the `get_variable_defs` MCP path for 7.1 or the `search_design_system` path for 7.2, note it in the methodology section: "Agent Interface Readiness token assessment was performed via automated scan of the client's Figma variable definitions." This is a credibility signal with engineering audiences.

**Voice rules for the report:**
- Write for the audience receiving it. If it goes to leadership: outcomes and cost of drift. If it goes to the design/engineering team: specific findings and concrete actions.
- No rankings against an ideal. Name what's happening, not how far they are from perfect.
- Technical findings in plain language. "The token architecture doesn't have a semantic layer" not "the token system lacks abstraction."
- Specific is kind. Vague findings don't help anyone. Name the specific component, the specific gap, the specific mismatch.

**Output format:**
Save as `audit-[client-slug]-[YYYY-MM-DD].docx` using the `docx` skill.
Save to the instance's engagement folder for the client (`<engagement folder>/deliverables/`)

---

## Step 6: The Path Forward

Every audit ends with a recommended engagement. Name it clearly.

| Audit finding pattern | Recommended next step |
|---|---|
| System exists, has good bones, needs ongoing care | Design System Care retainer |
| System exists but has significant structural issues | Build engagement — Design Systems — with audit as the foundation |
| System is so far from current product it needs a rebuild | Build engagement scoped as a new design system |
| Governance and team relationship are the core problem | Org Consulting engagement before any system work |
| Everything is on fire and they need to triage | Strategy Audit first — understand priorities before committing |

**Skills Authoring note:** If the audit ran MCP paths (Area 1, 2, or 4) and the client is on Professional plan or above, note in the recommendations that a Figma Skill can be authored for their system — a client-specific instruction file that defines how agents use their design system. This is a named deliverable in the Design Systems (Build) engagement and a Care+ maintenance item. If the client is evaluating a Build engagement anyway, it's the same session. If they're staying at Care, it's a one-time authoring add-on.

If it's appropriate, offer to produce a proposal using the `heyhi-proposal` skill.

---

## Skill Diary

This skill maintains a memory diary wing (through the `memory` shim): `heyhi-design-intelligence-audit-diary`. The diary captures token pipeline corrections, recurring audit gap types, WS scoring patterns, and client system characteristics that should persist across engagements.

**Read trigger:** At session start, before beginning any audit task, query both wing name forms to surface relevant corrections and client system patterns:

```
memory_search(query="[audit topic, token type, or client system characteristic relevant to the task]", wing="heyhi-design-intelligence-audit-diary")
memory_search(query="[audit topic, token type, or client system characteristic relevant to the task]", wing="wing_heyhi-design-intelligence-audit-diary")
```

*Note: The memory shim's `memory_diary_write` creates wings with a `wing_` prefix; `memory_write` uses the unprefixed form. Both must be queried to ensure complete retrieval.*

**Write trigger:** At the end of any session where a correction is issued or a recurring audit pattern is noticed while running this skill, draft a diary entry and stage it at `.auto-memory/diary-staging/heyhi-design-intelligence-audit-[YYYY-MM-DD].md` for the instance owner's review before committing. The agent drafts; the human reviews.

**Entry format:**
```
skill: heyhi-design-intelligence-audit
pattern_type: correction | preference | recurring-issue | client-specific
observed_in_session: YYYY-MM-DD
valid_from: YYYY-MM-DD
entry: [body — what happened, what the correct behavior is, why it matters]
```

Entries older than 90 days without a `valid_to` are flagged during session integrity.

---

See [reference.md](reference.md) for:
- Interview question sets (designer and engineer)
- Audit session agenda template
- Pre-work request template
- Full severity rubric with language examples
- Audit report template
- Findings language guide
- Maturity model assessment guidance and scoring template

See [`../../ai-services/design-intelligence/design-system-maturity-model.md`](../../ai-services/design-intelligence/design-system-maturity-model.md) for the full maturity framework, dimension definitions, level descriptions, and advisory warnings.

See [`../../ai-services/agentic-infrastructure/research/a2ui-d2-seventh-area-plan.md`](../../ai-services/agentic-infrastructure/research/a2ui-d2-seventh-area-plan.md) for the full Area 7 specification: complete sub-area definitions, worked scoring example, add-on framing rationale, and v2 upgrade path trigger conditions.

See [`../../ai-services/agentic-infrastructure/research/a2ui-architecture-research-plan.md`](../../ai-services/agentic-infrastructure/research/a2ui-architecture-research-plan.md) for the A2UI architecture research context that Area 7 draws from.

See [`references/memory-hygiene-diagnostic.md`](references/memory-hygiene-diagnostic.md) for the Memory Hygiene Diagnostic add-on: how to run the hygiene extractor (`memory-mcp/hygiene_extractor.py`, the in-house port of the retired general_extractor), classification distribution benchmarks, capture-vs-load gap analysis template, over-weighting signal interpretation, and the HeyHi empirical baseline run (2026-04-20).

See [`references/engagement-plan-template.md`](references/engagement-plan-template.md) for the reusable engagement plan template: DoD-as-phase-start structure, Phase Gate PASS/OPEN/FAIL format with state definitions and rules, standard gate conditions for Design Discovery → Implementation and Implementation → Validation transitions, kickoff checklist with baseline measurement commands, and scope item block format. Use when structuring a Design System Build or Care engagement that follows an audit.

---

## Prototype Mode → see heyhi-prototype-audit

Prototype audits — interaction completeness, gap analysis, build plans for HTML prototypes — are handled by the standalone `heyhi-prototype-audit` skill. This block previously contained the Prototype Mode framework; it has been superseded.

Routing: if the audit subject is an HTML prototype, interactive mockup, or behavioral simulation — load `heyhi-prototype-audit` instead. The framework is identical (three-pass severity, Foundation/Critical/High/Polish phases, pre-flight, dispatch template); the entry point is now the prototype-audit skill rather than this skill's Prototype Mode.

For prototype audits, use `heyhi-prototype-audit`. For system-level audits — design system health, token drift, component coverage, Figma file health, organizational commitment — stay here.

The prior Prototype Mode (Steps 0 through 6) is preserved historically in the v1.7.x changes log and in the source plan at `plans/track-b-prototype-audit-buildable-2026-05-06.md` §5 Option A. The supersedence is bounded — only the architectural decision to embed Prototype Mode here is reversed; the severity taxonomy, phase model, and dispatch template are preserved verbatim in `heyhi-prototype-audit` Layer 1.

---

## Exit Gate Required Headers (bottom-of-skill bracket)

This skill closes through the Exit Gate Flavor A (`CLAUDE-SESSION-RULES.md § Exit Gate`). Before declaring done, confirm every required header below contains real content, not a claim:

- `## Fixes Applied`
- `## Smoke Test`
- `## Next Session Prompt`

If any header is empty or contains advisory prose ("I checked for bugs") instead of a concrete artifact, the gate has not been satisfied. Apply fixes until clean — then emit.

---

*HeyHi Confidential*
