---
classification: confidential
title: "Foundation: Design Systems (area 7, DEEP)"
area: 7
nature: craft
coverage: deep
phase: P1
kind: deep-manifest
---

# Foundation: Design Systems (area 7)

**Coverage: DEEP. The most-built area, and one module of Sheerline, not the whole thing.** This is the Design-Systems quality loop: the Design System MCP, the Evaluator, and the corrections registry, plus the 11-skill cluster. Phase 1 governs it (register the skills, seed corrections, point this manifest at the corpus and the nested subsystem). The *advance* of this area is not new skills; it is Phase 2 (the R1 corrections registry per DISPATCH-02, and the evaluator's I2 trend series), planned and dispatched elsewhere.

*Paths below are repo-root-relative. This manifest is a pointer plus loading rules. It copies nothing, and it embeds no token files (Invariant 4).*

---

## The nested subsystem, reached through the MCP boundary (Invariant 4)

The DS-MCP + Evaluator + corrections quality loop is a **nested, referenced subsystem**, reached **through the MCP as a boundary tool**, never as token files embedded inside `sheerline/`. The MCP retrieval tools are the realization of "searchable, never pre-loaded": the design system is *retrieved*, not pasted.

| Reference | What it supplies |
|---|---|
| `ai-services/design-intelligence/agent-summary.md` | The always-loaded meaning layer over the token/component set: a copy of the served `design-system://summary`. Since 2026-10-06 (DESIGN.md Open Decision 2 = Option A) it is generated from the data contract plus two authored layers (`heyhi-mcp/data/authored/`: the guidance residue and the Confidential intent overlay), and the internal `ai-services/design-intelligence/DESIGN.md` is a sibling rendering of the same sources. Edit the data or the authored layers, never the rendered files. |
| `heyhi-website/public/DESIGN.md` | The structurally-conformant, token-only DESIGN.md base (DTCG registry with resolved `$value`s and descriptions). The public exporter reads an explicit allowlist and never the intent overlay. |
| The Design System MCP + Evaluator | The retrieval, validation, and grading loop, reached through the MCP boundary. The populated instance and the graded evaluator are the retained moat (`os/operating-principles.md` § IP boundary); they are referenced here, not built. |

**The corrections runtime ("learn" verb)** lands in the internal `heyhi-mcp` (Phase 2 / DISPATCH-02), not here. `os/corrections/` is the convention slot; it references that runtime by name and builds no runtime.

**Registered skills (area 7):** `heyhi-design-intelligence-audit`, `design-system-review`, `design-system-care-monthly`, `heyhi-token-description-author`, `heyhi-schema-extension-author`, `heyhi-pipeline-validator`, `heyhi-theme-validator`, `heyhi-style-to-token-reviewer`, `ui-studio-onboard`, `heyhi-shopify-theme`, `heyhi-audit-campaign`, `heyhi-figma-ds-generator` (the write verb, 2026-09-04), `heyhi-drift-repair` (the act verb, cross-cutting area 8, 2026-09-04), `figma-library-census` (the forward-deployed loop read/serve census + code crosswalk, 2026-09-07), `ds-component-author` (the promotion-execution author verb, 2026-09-08), `ds-component-change` (the change verb, 2026-09-08).

---

## The fundamentals reasoning layer (referenced, not authored here)

This foundation references the same universal reasoning layer the Visual foundation does: the binding UX laws, the control-state contract, and the type/spacing constraints, plus the conflict order. Authored **once**, as **Increment A of the DESIGN.md arc**, ratified. Point at it; do not re-author it here.

| Reasoning reference | What it supplies | State |
|---|---|---|
| `plans/plan-design-md-build-2026-08-06.md` § Increment A | The ratified spec: A.1 (Option A hierarchy), A.2 (binding UX laws), A.3 (control-state contract). | Ratified, landed. |
| `ai-services/design-intelligence/research/design-fundamentals-decision-research-2026-08-12.md` | The reasoning of record: exact ratified wording. | Ratified, landed. |
| `ai-services/design-intelligence/design-fundamentals.md` | The served reference: A.1 hierarchy, A.2 the Tier-1 ten as constraints, A.3 control-state contract, A.4 by reference. | Authored, landed. |

The served `design-fundamentals` reference file (`ai-services/design-intelligence/design-fundamentals.md`) is authored and landed and is now served as the second always-loaded surface (`design-system://fundamentals`, `heyhi-mcp/heyhi_mcp/server.py`; A.5 / gate G1B satisfied). The conflict order lives in `os/operating-principles.md` (which points at A.1); this foundation does not restate it. A.3's canonical control-state contract is the substrate the Interaction Design foundation (area 4, `os/foundations/interaction-design/FOUNDATION.md`, filled 2026-09-05) references.

---

## Loading rules (Earn the Room, four-class)

- **always:** nothing from this foundation loads by default.
- **conditional:** this manifest, when the session is a design-system audit, review, care pass, token/schema work, or a build that must honor a token/component set.
- **on-demand:** a specific skill's reference, a specific correction, a specific evaluator rubric.
- **searchable:** the token/component data itself, retrieved through the MCP, never pasted.

---

## The boundary and the corpus-thickness watch

Grades inform the evaluator score; they never auto-block a merge (whether a score gates is authored client policy). The moat here runs on compounding assets (the golden set, the corrections corpus); a skill build cannot fix a curation gap. **Ownership resolved**: the instance owner curates via the intake-ratify loop; the thick-corpus moat skills are unblocked, the thin held on a thickness bar. The remaining watch is *thickness* (sustained curation), not ownership.

---

*Area map: `os/foundations/registry.yaml` · Conflict order: `os/operating-principles.md` · Corrections convention: `os/corrections/`*

*HeyHi Confidential*
