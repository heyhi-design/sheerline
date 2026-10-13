---
classification: confidential
title: "Sheerline: HeyHi's design-practice harness"
---

# Sheerline

**HeyHi's design-practice operating system.** Skills plus governed foundational context across the whole design discipline, carried in the keel/ship lineage as a sibling to keel.

**The one frame:** keel is the firm-of-one harness; Sheerline is the same idea aimed at design output. Four verbs run through it: **retrieve** the system, **validate** against it, **grade** the result over time, **learn** from correction.

It is a keel-instance hybrid, governance-first. Phase 1 stood up the structure, governed the two deep areas (Visual, Design Systems) and Prototyping, and tracked the gaps as visible states; P1.5 and P2 are complete and P3 (craft foundations) is active, so every area now carries a governed foundation and the registry governs the skills that serve them (`os/project-state.yaml` has the live phase state). It builds no runtime. It is the scaffold half only; the retained moat (the evaluator, the populated corpus, the calibration) stays in a separate unpublished tree.

## The three-way naming caution (keep these separate)

"Harness" is overloaded here. Conflating the module with the harness is the trap this tree exists to avoid.

- **keel**: the *general* firm-of-one harness (public since 2026-07-29). Sheerline reuses its engine, loading taxonomy, corrections mechanism, session lifecycle, and dispatch anatomy by adaptation.
- **Sheerline**: the whole design-practice OS (this tree).
- **The Design System MCP + Evaluator + corrections registry**: the Design-Systems *quality loop*. This is **one module** of Sheerline (its most-built one), not the whole thing. It is reached through the MCP as a boundary tool (Invariant 4), nested and referenced, never embedded here.

## Architecture: a keel instance with one net-new slot

Sheerline is keel re-instantiated for design: the same three layers (Runtime rented, Configuration owned in `os/`, Deployment owned in `skills/` and `profile/`), the same Earn-the-Room four-class loading, plus **one structural slot keel lacks: `os/foundations/<practice-area>/`**, per-area governed context. Foundations *reference* HeyHi's existing corpus in place; they never byte-copy it.

## The tree

```
sheerline/
├── README.md                          this file: the frame, the naming caution, the map
├── os/                                the Configuration layer (owned)
│   ├── agent-context.md               thin always-context: the 13 areas, the through-line, don't-automate
│   ├── operating-principles.md        the four invariants + design constraints + the zero-cost operating invariants + the A.1 conflict-order pointer
│   ├── session-rules.md               the Exit Gate + the design smoke test (render it and look)
│   ├── corrections/                   the corrections CONVENTION slot (runtime is heyhi-mcp, Phase 2)
│   │   ├── README.md                  the convention + the pointer to the runtime
│   │   ├── LIFECYCLE.md               statuses, promotion, close-out, the factual/behavioral boundary
│   │   └── seed-corrections.yaml      generic-factual seed template (not the live registry)
│   ├── foundations/                   THE NET-NEW SLOT
│   │   ├── registry.yaml              the 13-area registry (nature / coverage / phase)
│   │   ├── visual-design/             deep manifest (area 6): references the corpus in place
│   │   ├── design-systems/            deep manifest (area 7): references the DS-MCP through the boundary
│   │   ├── prototyping/               governance manifest (area 5)
│   │   ├── user-research/             governance manifest (area 1, filled P3 2026-09-01; covered 2026-09-04)
│   │   ├── information-architecture/  governance manifest (area 2, filled P3 2026-09-01; taxonomy-labeling-auditor deployed, other 3 IA skills held on pull)
│   │   ├── accessibility/             governance manifest (area 8, filled G-3 2026-08-28)
│   │   ├── design-strategy/           governance manifest (area 9, G-3 2026-08-28)
│   │   ├── collaboration-facilitation/ governance manifest (area 11, G-3 2026-08-28)
│   │   ├── content-design/            governance manifest (area 3, filled P3 2026-09-05; covered 2026-09-05)
│   │   ├── interaction-design/        governance manifest (area 4, filled P3 2026-09-05; covered 2026-09-05)
│   │   ├── business-acumen/           governance manifest (area 10, filled P3 2026-09-05; covered 2026-09-05)
│   │   └── service-design/            governance manifest (area 13, filled + covered 2026-09-07 D-3 open)
│   ├── dispatch/README.md             dispatch anatomy, design-scoped
│   ├── decision-log.md                append-only, seeded with the founding entry
│   ├── dependency-graph.json          the tree's document dependency map
│   └── project-state.yaml             machine-readable ground truth: phases, coverage, early warning signals
├── skills/                            the Deployment layer (owned)
│   ├── README.md                      skills overview + routing
│   ├── registry/                      the reused keel engine (R2) + the design-scoped registry
│   ├── templates/README.md            pointers to HeyHi's deployed design skills (reference, not copy)
│   └── evals/                         the per-capability eval-case scaffold (R4)
├── profile/                           the engagement / design-system intake (parameterizes, never loaded)
│   ├── engagement-intake.yaml
│   └── intake-conversation.md
├── seminar/                           the Learn surface: the novice→SME track ladder (5 tracks, 21 modules)
├── docs/                              the six-figure architecture set (diagrams/ + architecture.md)
└── studio/                            Wheelhouse: the Replit-inspired prototype UI over the harness (simulated; D-08)
```

## The 13 practice areas

The full map with coverage states and phasing is `os/foundations/registry.yaml`. Two areas are **deep** (Visual, Design Systems) and carry governed foundations; Prototyping, User Research, Interaction Design, Business Acumen, Content Design, Information Architecture, and Service Design are **covered**; Accessibility, Design Strategy, and Collaboration/Facilitation carry filled governance manifests at partial coverage, DesignOps is governed by invariant. **Zero gaps and zero stubs remain** — Service Design (13), the last one, was filled and its skill deployed at the early D-3 open, on a client-engagement pull. Phase 1 stood five areas up as stubs; all have since been filled. The gaps were visible states, not invisible absences.

## Distribution

A private export of this tree plus every skill its registry governs lives at `heyhi-design/sheerline` (decided 2026-10-13; `os/decision-log.md`). It is one-way: this tree is canonical, and `releases/private/sheerline/export.py` regenerates the repo. Runbook: `releases/private/sheerline/PUBLISH.md`.

## Start here

1. Read `os/agent-context.md` (always-loaded orientation).
2. Read `os/operating-principles.md` (the constraints, including the conflict order and the IP boundary).
3. Route a task through `skills/registry/skill-registry.py "<task>" --confidence`; load only what it returns.

---

*HeyHi Confidential*
