---
classification: confidential
title: "Sheerline Skill Templates: pointers, not copies"
---

# Sheerline Skill Templates: pointers, not copies

Unlike keel, which ships fillable starter skills, Sheerline governs HeyHi's **already-deployed** design skills. This directory is a **pointer index** into `heyhi-skills/`. It copies nothing: the canonical `SKILL.md` for each skill stays in `heyhi-skills/`, and this tree references it (the reference-not-copy rule, `os/operating-principles.md`).

The registry (`skills/registry/skill-registry.yaml`) is the routable index; this table is the human-readable roster of what Sheerline governs, by area (Phase 1 plus the P1.5 operating-area audit skills).

| Area | Skill | Canonical path |
|---|---|---|
| 1 User Research | Research Plan Author | `heyhi-skills/research-plan-author/SKILL.md` |
| 1 User Research | Insight Activation (connective: the learn verb, serves areas 9/10/11) | `heyhi-skills/insight-activation/SKILL.md` |
| 2 Information Architecture | Taxonomy & Labeling Auditor | `heyhi-skills/taxonomy-labeling-auditor/SKILL.md` |
| 6 Visual | Logo System | `heyhi-skills/heyhi-logo-system/SKILL.md` |
| 6 Visual | Style Brief | `heyhi-skills/heyhi-style-brief/SKILL.md` |
| 6 Visual | Style Selection | `heyhi-skills/heyhi-style-selection/SKILL.md` |
| 6 Visual | Style Entry Author | `heyhi-skills/heyhi-style-entry-author/SKILL.md` |
| 6 Visual | Design System Onboard | `heyhi-skills/design-system-onboard/SKILL.md` |
| 7 Design Systems | Design Intelligence Audit | `heyhi-skills/heyhi-design-intelligence-audit/SKILL.md` |
| 7 Design Systems | Design System Review | `heyhi-skills/design-system-review/SKILL.md` |
| 7 Design Systems | Design System Care (monthly) | `heyhi-skills/design-system-care-monthly/SKILL.md` |
| 7 Design Systems | Token Description Author | `heyhi-skills/heyhi-token-description-author/SKILL.md` |
| 7 Design Systems | Schema Extension Author | `heyhi-skills/heyhi-schema-extension-author/SKILL.md` |
| 7 Design Systems | Pipeline Validator | `heyhi-skills/heyhi-pipeline-validator/SKILL.md` |
| 7 Design Systems | Theme Validator | `heyhi-skills/heyhi-theme-validator/SKILL.md` |
| 7 Design Systems | Style-to-Token Reviewer | `heyhi-skills/heyhi-style-to-token-reviewer/SKILL.md` |
| 7 Design Systems | ui-studio Onboard | `heyhi-skills/ui-studio-onboard/SKILL.md` |
| 8 Accessibility | Accessibility Audit (ACR/VPAT anchor) | `heyhi-skills/heyhi-a11y-audit/SKILL.md` |
| 8 Accessibility | Accessibility Annotation (design-side handoff) | `heyhi-skills/heyhi-a11y-annotation/SKILL.md` |
| 7 Design Systems | Shopify Theme | `heyhi-skills/heyhi-shopify-theme/SKILL.md` |
| 7 Design Systems | Audit Campaign | `heyhi-skills/heyhi-audit-campaign/SKILL.md` |
| 7 Design Systems | Figma DS Generator | `heyhi-skills/heyhi-figma-ds-generator/SKILL.md` |
| 7 Design Systems | Drift Repair | `heyhi-skills/heyhi-drift-repair/SKILL.md` |
| 7 Design Systems | Figma Library Census (forward-deployed loop, read/serve census + crosswalk) | `heyhi-skills/figma-library-census/SKILL.md` |
| 7 Design Systems | DS Component Author (forward-deployed loop, promotion-execution author verb) | `heyhi-skills/ds-component-author/SKILL.md` |
| 7 Design Systems | DS Component Change (forward-deployed loop, the change verb) | `heyhi-skills/ds-component-change/SKILL.md` |
| 5 Prototyping | ui-studio | `heyhi-skills/ui-studio/SKILL.md` |
| 5 Prototyping | Prototype Audit | `heyhi-skills/heyhi-prototype-audit/SKILL.md` |
| 5 Prototyping | Design Bridge | `heyhi-skills/heyhi-design-bridge/SKILL.md` |
| 5 Prototyping | Flow & Lo-fi Author | `heyhi-skills/flow-and-lofi-author/SKILL.md` |
| 5 Prototyping | Divergence Guard | `heyhi-skills/divergence-guard/SKILL.md` |
| 5 Prototyping | App to Figma (forward-deployed loop, the build verb) | `heyhi-skills/app-to-figma/SKILL.md` |
| 3 Content | Voice System Author | `heyhi-skills/voice-system-author/SKILL.md` |
| 3 Content | Microcopy States Writer | `heyhi-skills/microcopy-states-writer/SKILL.md` |
| 4 Interaction | Motion System Author | `heyhi-skills/motion-system-author/SKILL.md` |
| 4 Interaction | Interaction Inventory | `heyhi-skills/interaction-inventory/SKILL.md` |
| 9 Strategy | Futurecasting | `heyhi-skills/futurecasting/SKILL.md` |
| 9 Strategy | Design Measurability Mapper | `heyhi-skills/design-measurability-mapper/SKILL.md` |
| 9 Strategy | Strategy Integrity Warden | `heyhi-skills/strategy-integrity-warden/SKILL.md` |
| 9 Strategy | Intent-Journey Map (forward-deployed loop; serves areas 1, 2) | `heyhi-skills/intent-journey-map/SKILL.md` |
| 9 Strategy | Application Intent Map (forward-deployed loop; serves areas 1, 2) | `heyhi-skills/app-intent-map/SKILL.md` |
| 12 DesignOps | App Recon (forward-deployed loop, the read verb; serves areas 5/7/9/2) | `heyhi-skills/app-recon/SKILL.md` |
| 12 DesignOps | Feature Increment (forward-deployed loop, the Care/increment verb; serves areas 5, 7) | `heyhi-skills/feature-increment/SKILL.md` |
| 10 Business Acumen | Experiment Readout Linter | `heyhi-skills/experiment-readout-linter/SKILL.md` |
| 10 Business Acumen | Competitive Teardown Runner | `heyhi-skills/competitive-teardown-runner/SKILL.md` |
| 10 Business Acumen | Design Business Case Drafter | `heyhi-skills/design-business-case-drafter/SKILL.md` |
| 11 Facilitation | Design Rationale Decision Record | `heyhi-skills/design-rationale-decision-record/SKILL.md` |
| 11 Facilitation | FigJam Mapper | `heyhi-skills/heyhi-figjam-mapper/SKILL.md` |
| 11 Facilitation | Crit Prep & Capture | `heyhi-skills/crit-prep-and-capture/SKILL.md` |
| 13 Service Design | Service Blueprint | `heyhi-skills/heyhi-service-blueprint/SKILL.md` |

The canonical full deployed-skill roster (including the keel-layer sales and session-infra skills Sheerline does *not* claim as design coverage) is HeyHi's own `CLAUDE.md` skills table and `ai-services/agentic-infrastructure/skill-registry.yaml`. The skill count is derived from `skill-registry.py --stats`, never hardcoded.

---

*Registry: `skills/registry/skill-registry.yaml` · Area map: `os/foundations/registry.yaml`*

*HeyHi Confidential*
