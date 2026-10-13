---
classification: confidential
title: "Foundation: Wireframing & Prototyping (area 5, COVERED / governance)"
area: 5
nature: craft
coverage: covered
phase: P1
kind: governance
---

# Foundation: Wireframing & Prototyping (area 5)

**Coverage: COVERED at hi-fi. This is a governance manifest, not a corpus manifest and not a gap stub.** Phase 1 registers the hi-fi skills, adopts the Exit Gate for prototype work, and wires the `ui-studio` routing override. It authors no new build. The early gap (lo-fi wireframing, flow/structure before hi-fi, the divergence discipline) is Phase 3, tracked in `os/foundations/registry.yaml`.

*This is a governance manifest: it registers and routes existing capability. It does not reference a taste corpus (that is Visual, area 6), and it is not a gap stub (the capability exists).*

---

## Registered skills (area 5)

| Skill | State | Action |
|---|---|---|
| `heyhi-ui-ux` | deployed | Governed. HeyHi production pages. |
| `ui-studio` | deployed | Governed. Client / speculative UI builds (Mode A/B/C). |
| `heyhi-prototype-audit` | deployed | Governed. Interaction-completeness audit. |
| `heyhi-design-bridge` | deployed | Governed. Prototype-to-Figma and raster-to-vector. |
| `heyhi-prototype-verify` | in-dev | Finish + govern; the `prototype-hardener` is an extension, not a new build. |
| `flow-and-lofi-author` | deployed | The lo-fi / flow deepen: screen inventory, Mermaid flow map, N structurally distinct skeletons behind the fidelity ceiling; config-free. Spec `plans/plan-sheerline-p3-prototyping-lofi-2026-09-05.md` § 2; the routing override applied in the same promotion. |
| `divergence-guard` | deployed | The ideation-diversity guard made operable: counts structural options, offers unordered stimulus, reads fidelity against the question; advisory by construction, gates nothing. Spec § 3. |

The divergent-visual-boards candidate (`heyhi-visual-exploration`) belongs to Visual Design (it is visual, not structural); cross-link, do not claim it here.

---

## Governance actions (Phase 1)

- **Register** the skills above under area 5.
- **Adopt the Exit Gate** (`os/session-rules.md`) for every prototype session, including the design smoke test: render it and look, do not inspect source only.
- **Wire the `ui-studio` routing override.** Before loading any skill for a UI build, apply the routing table (canonical in HeyHi's `CLAUDE.md` § ui-studio routing):

| Scenario | Skill | Config |
|---|---|---|
| **Lo-fi / wireframe / screen inventory / flow map, any brand — before hi-fi** | `flow-and-lofi-author` | none (config-free) |
| **"Are we converging too early" / "too hi-fi for the question" / alternatives check** | `divergence-guard` | none |
| HeyHi production pages | `heyhi-ui-ux` | HeyHi brand (built-in) |
| The instance's own creative / speculative work | `ui-studio` | the instance's own brand config in `heyhi-skills/ui-studio/brand-config/` |
| Client UI, design system exists | `ui-studio` | client config (onboarded) |
| Client UI, no config yet | `ui-studio-onboard`, then `ui-studio` | generate via onboarding |

**Applied at promotion.** The two lo-fi rows now sit at the top of the routing table (precedence is top-down): a lo-fi or structural ask routes to `flow-and-lofi-author` before any hi-fi builder. The sequencing note read "wire the override at build, not after"; the spec (§ 4.3) moved the wiring to promotion, in the same pass the skills became loadable — a staged skill is registry-inert, so a routing row would have pointed the reader at nothing. "Not after" is honored in the sense that matters (the override and the promotion landed in one PR, never the skills first and the override in a later session); "at build" is the named departure.

---

## The boundary

Prototype fidelity is right-sized to the test question. Which interactions matter, and whether a prototype is ready, are human reads that the audit informs and never decides.

---

*Area map: `os/foundations/registry.yaml` · Session rules: `os/session-rules.md`*

*HeyHi Confidential*
