---
classification: confidential
title: "Sheerline Operating Principles"
adapted_from: releases/open-source/keel/os/operating-principles.template.md
---

# Sheerline Operating Principles

**For everyone working inside Sheerline, human and agent equally.**

Sheerline is HeyHi's design-practice operating system: skills plus governed foundational context across the whole design discipline, carried in the keel/ship lineage as a sibling to keel. Read this file after `agent-context.md` at the start of every session that produces design output. These constraints supersede default behavior.

*Adapted from keel's `os/operating-principles.template.md` (the fixed four-invariant spine ports unchanged; the design constraints below are the fill).*

---

## The Four Architectural Invariants (fixed spine, keep as written)

Every technical decision Sheerline makes is governed by four principles. They do not bend for convenience. Canonical in HeyHi's own `OPERATING_PRINCIPLES.md`; full spec in `ai-services/_core/architecture-principles.md`.

**1. Provider-Agnostic Design.** Everything runs with one agent runtime today and swaps to another later. Structure the stack in layers: application logic, an orchestration abstraction, provider adapters, a protocol layer, tools. Never hardcode a single provider into application logic. The honest caveat travels with the claim: a configuration is provider-agnostic in *design* even while authored and tuned against one runtime in *practice*.

**2. Earn the Room.** Nothing gets access, context, or authority by default. This governs authority (minimum permissions, a human checkpoint before any irreversible action) and context (minimum information, loaded on discovery, not pre-loaded). Classify every piece of content into one of four categories:

| Category | Load when |
|---|---|
| **always** | every session needs it (`agent-context.md`, this file) |
| **conditional** | the session type matches (the active practice-area foundation) |
| **on-demand** | the task explicitly calls for it (a specific corpus reference) |
| **searchable** | retrievable from the registry, never pre-loaded (the design system itself, retrieved through the MCP) |

If content is relevant to fewer than half of sessions, it must not load by default. The MCP retrieval tools are the purest realization of "searchable, never pre-loaded": the design system is *retrieved*, not pasted.

**3. Evaluation Before Deployment.** Nothing ships without passing tests. Four-layer model: component, trajectory, outcome, system. This is the one invariant HeyHi does not commoditize; Sheerline's evaluation layer is the retained moat (§ IP boundary below), and it grades on the severity axis stated under the conflict order.

**4. Protocols at Boundaries, Not Inside Them.** Select an interface by the boundary it crosses, not the capability it offers. In Sheerline this is load-bearing: the Design System MCP, the Evaluator, and the corrections registry are reached *through the MCP as a boundary tool*, nested and referenced, never as token files embedded inside `sheerline/`.

---

## Design Constraints (the fill)

These are Sheerline's non-negotiables, on top of the invariants.

- **The accessibility floor.** WCAG 2.2 AA is a hard gate, not a preference (see the conflict order below for how it resolves). Automated conformance is the floor; the judged half (does it work for an assistive-technology user) is a governed practice, tracked in `os/foundations/accessibility/`.
- **Tokens, not raw values.** Emitted output uses the design system's tokens, never a hardcoded hex, an off-scale spacing value, or a raw literal where a token exists. This is an authoring rule; the corrections layer enforces its deterministic, structural instances.
- **The taste and critique boundary.** Sheerline's scoring is advisory, never a gate: a grade informs a human decision; it never auto-approves taste or auto-blocks a merge. A capability that fills its own judgment slot has exceeded its charter. The judgment calls this protects are enumerated once under *What stays human* below; this rule governs how scoring behaves around them.
- **No standalone "AI."** Say "intelligent systems," "agentic workflows," or name the function. Verbatim quotations from cited statistics and proper nouns are the only exceptions.
- **Restrained em dashes; no pricing in any external surface; the hermetic seal.** Reference any engagement generically (a session label, "the instance's engagement folder"), never a client name. The practice's own system is the default substrate for every increment.
- **What stays human.** Design critique, brand positioning, direction selection, metric selection, severity-as-truth, the positioning stance, hiring, feedback, mentorship, ethics, strategy, and real-user validation (as distinct from reviewer or contract validation — a reviewer's sign-off, a passing contract check, or a completeness audit is not a naive end user having tried the thing and succeeded). These are never generation targets. This is the canonical list: the taste-and-critique boundary above and the critique invariant below point here rather than re-enumerate it.

---

## The zero-cost operating invariants (ship in Phase 1)

Five operating-area invariants cost nothing to state and prevent the whole class of boundary-collapse the discipline is most prone to. They govern the operating areas (§ registry areas 9–13) as threads, the way Design Ethics and Inclusive Design do, without a filled foundation behind them.

- **Critique and facilitation governance.** Of the *What stays human* items, design critique carries a standing operational rule: critique evaluates work against stated goals through dialogue, so the agent may assemble a crit pre-read and capture decisions, but renders no verdicts and suggests no critique content. Reading the room stays human.
- **The empathy boundary.** A model simulates cognitive empathy (inferring what a user might think). It does not have experiential or compassionate empathy (having lived what a user lives). Research synthesis and persona work carry this boundary; simulated empathy is never presented as the real thing.
- **The ideation-diversity guard.** Model-assisted ideation lifts the quality of an individual option and collapses the diversity of a set. It is stimulus, never selection: use it to widen the field, measure overlap, and warn on premature convergence; the human chooses.
- **The Business-Acumen scope fence.** Sheerline's Business-Acumen area is *design*-business only (design ROI, stakeholder buy-in, design-team ops). HeyHi's own firm sales and marketing skills are the keel layer and are out of scope here; the buyer is the designer-as-practitioner, not HeyHi's firm.
- **DesignOps as a governed practice.** Sheerline's own machinery (this registry, the corrections module, the session lifecycle, the Exit Gate, the coverage map) is the worked DesignOps artifact. The operating-area contribution is to recognize and govern that, not to ship a generation skill that "runs ops."

---

## The cross-quality conflict-resolution order (point at it, do not re-derive)

When accessibility, the brand design system, and the universal fundamentals disagree about a value, the resolution order is authored **once**, as **A.1 (Option A)**, ratified in **Increment A of the DESIGN.md arc** ([`plans/plan-design-md-build-2026-08-06.md`](../../plans/plan-design-md-build-2026-08-06.md) § Increment A), with the reasoning of record in [`ai-services/design-intelligence/research/design-fundamentals-decision-research-2026-08-12.md`](../../ai-services/design-intelligence/research/design-fundamentals-decision-research-2026-08-12.md) § Decision 1 (the exact ratified wording). **Point at that rule. Do not re-derive a second canonical hierarchy here.** The decision research found HeyHi's order duplicated and divergent per-skill; centralizing it is the governance job, and two centers is the anti-pattern the ratification exists to end.

A.1 is a **two-axis** rule, which is exactly why it fits this file:

- **The value-source axis (rules 1 through 4) decides which source supplies the emitted value.** In brief: (1) accessibility is a hard gate, resolved by moving to the nearest conformant value at the token source and recording it, with the safety-critical usability contracts folded inside the gate; (2) inside the gate the brand design system is authoritative for everything it *specifies*, on a **specified-beats-silent** coverage test; (3) where the design system is silent, the universal fundamentals fill the gap; (4) a stated brand-versus-fundamentals conflict resolves to the brand rule and is flagged.
- **The severity axis (Accessibility → Interaction → Visual → Brand → Code) decides which failure to grade first.**

That split resolves a tension this file would otherwise carry. `tokens, not raw values` ranks **Brand high** for *authoring* a value (rule 2: the brand system supplies what is emitted, so use its tokens). The severity order ranks **Brand low** for *grading* a defect (a brand deviation is less severe than an accessibility or interaction failure). Both are true at once because they are different axes, and Sheerline's evaluation and corrections layer grades on the **severity** axis.

The universal fundamentals themselves (the binding UX laws, the control-state contract, the modular-type and spacing constraints) are the referenced reasoning layer, not authored here. The deep-area foundations point at it (see `os/foundations/visual-design/FOUNDATION.md` and `os/foundations/design-systems/FOUNDATION.md`). Its served reference file has since landed under the DESIGN.md arc: [`ai-services/design-intelligence/design-fundamentals.md`](../../ai-services/design-intelligence/design-fundamentals.md) is the source of truth, served as the always-loaded `design-system://fundamentals` resource by the Design System MCP (`heyhi-mcp/heyhi_mcp/resources/fundamentals.py`, kept byte-identical). The ratified reasoning of record remains the decision-research doc and the plan's Increment A named above.

**Governance-tracked, not this skeleton's task.** The decision research names a deployed-skill propagation that follows ratification: centralize the duplicated five-domain lists in `heyhi-skills/heyhi-ui-ux/SKILL.md` and `heyhi-skills/ui-studio/SKILL.md` to point at the one rule, and reconcile the two divergent `web-quality.md` Priority Maps against it. That work belongs to the DESIGN.md arc, not to standing up this skeleton. It is recorded here as a governance-tracked item, not done here.

---

## Document Classification

| Tier | Mark | Applies to |
|---|---|---|
| **Confidential** | `HeyHi Confidential` | trade secrets, methodology, the retained moat, core research |
| **Internal** | `HeyHi Internal Use Only` | operational docs, tracking, handoffs |

Every file in `sheerline/` is Confidential at creation: `classification: confidential` frontmatter where the format supports it, plus a `HeyHi Confidential` footer.

---

## The IP boundary (scaffold ships, populated instance stays)

Sheerline's posture is the scaffold-ships / populated-instance-stays split, confirmed against `legal/ip-strategy.md` (gitignored; resolved against the main workspace). The scaffold (this `os/` layer, the registry engine, the corrections schema and generic seeds, the MCP contract, the DS-MCP scaffold) is potentially publishable and stays on C-1 hold for the public tree. The **retained moat stays** in a separate unpublished tree and is not built here: the boundary and evaluation layer, the graded evaluator, the conformance parser, the populated corrections corpus and its promotion judgment, the calibrated thresholds, the DS-MCP populated instance. This skeleton is the scaffold half only.

---

## Structured-Over-Prose on Propagation Surfaces

When a document is something other files, agents, or scanners read to discover what exists or what changed (this registry, a state file, a status field, a coverage map), prefer structured fields (tables, YAML, named headers) over prose. Narrative writing where the prose *is* the artifact (a foundation's framing, a critique) is exempt.

---

*Voice: `heyhi-skills/heyhi-voice/SKILL.md` · Session workflow: `os/session-rules.md` · Area map: `os/foundations/registry.yaml`*

*HeyHi Confidential*
