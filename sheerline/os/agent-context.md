---
classification: confidential
title: "Sheerline: Agent Context"
adapted_from: releases/open-source/keel/os/agent-context.template.md
---

# Sheerline: Agent Context

*Always-loaded. Present in every session that produces design output through Sheerline. Keep it thin: the four-class loading discipline (`os/operating-principles.md`, Invariant 2) applies to this file's own token budget.*

*Adapted from keel's `os/agent-context.template.md`, design-scoped.*

---

## What Sheerline is

Sheerline is HeyHi's design-practice operating system: skills plus governed foundational context across the whole design discipline. The one frame: **keel is the firm-of-one harness; Sheerline is the same idea aimed at design output.** Four verbs run through it: **retrieve** the system, **validate** against it, **grade** the result over time, **learn** from correction.

**Keep three things separate** (the naming trap this OS exists to avoid):
- **keel** is the general firm-of-one harness.
- **Sheerline** is the whole design-practice OS (this tree).
- **The Design System MCP + Evaluator + corrections registry** is *one module* of Sheerline, its most-built one, not the whole thing.

---

## The design through-line

Extend what a design team can do; never replace how it decides. Automate the plumbing, the surfacing, the structuring, the enforcement. Keep the verdict, the read, and the taste call human. Craft is a decision, made every time or lost.

---

## The 13 practice areas

A flat, tagged capability registry (full states, tags, and phasing in `os/foundations/registry.yaml`). HeyHi's capability is deep but lopsided (strong in Visual and Design Systems, thin upstream); governance turns the gaps into *tracked states*, not invisible absences.

| Craft (8) | Operating (4) | Conditional (1) |
|---|---|---|
| 1 User Research · 2 Information Architecture · 3 Content Design · 4 Interaction Design · 5 Wireframing & Prototyping · 6 Visual Design · 7 Design Systems · 8 Accessibility | 9 Design Strategy · 10 Business Acumen · 11 Collaboration & Facilitation · 12 DesignOps | 13 Service Design |

Two areas are **deep** (6 Visual, 7 Design Systems) and carry governed foundations. Seven are **covered**: Prototyping (5), User Research (1), Interaction Design (4), Business Acumen (10), Content Design (3), and Information Architecture (2) + Service Design (13) (both at the D-3 open on a client-engagement pull, when taxonomy-labeling-auditor + heyhi-service-blueprint deployed). Five areas shipped as first-class tracked-state stubs in Phase 1; **all have since been filled** — Service Design (13), the last stub and the last gap, closed at the D-3 open. Four areas are **partial** (8, 9, 11, 12); 8, 11, and 12 are terminal partials by construction. **Zero gaps and zero stubs remain.** The rest are registered with their coverage states in the registry.

---

## The don't-automate line

Design critique, brand positioning, direction selection, taste, hiring, performance feedback, mentorship, ethics, and strategic judgment are not automation candidates. Sheerline builds the infrastructure so a team has more room for exactly these. This line is enforced structurally: the operating invariants in `os/operating-principles.md` (critique-as-governance, the empathy boundary, the ideation-diversity guard) are its standing form.

---

## How to work here

- **Retrieve, do not paste.** The design system is reached through the MCP retrieval tools, not dumped into context. Foundations reference the corpus in place; they never byte-copy it.
- **Grades inform, never gate.** A score routes a human decision. It never auto-approves taste or auto-blocks a merge.
- **Render and look.** For any visual artifact, the smoke test is to render it and view it, not to inspect source only (`os/session-rules.md`).
- **Own practice first.** The instance runs every loop on its own practice before anything is abstracted for sale. Hermetic seal always: no client name in any tracked file.

---

*Operating principles: `os/operating-principles.md` · Session rules: `os/session-rules.md` · Skill routing: `skills/registry/skill-registry.py` (run `python3 skill-registry.py "<task>" --confidence`, load only the top skill, ask when it reports two close matches).*

*HeyHi Confidential*
