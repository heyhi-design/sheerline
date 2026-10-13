---
classification: confidential
title: "feature-increment: Plugin-API probe log"
---

# Probe log

Arc rule 9: a lane that depends on a Plugin-API call probes it in a scratch file before building on it and records the result here. This skill's Figma leg consumes `app-to-figma` in update mode, so most of the calls it depends on are `app-to-figma`'s and were already probed green on a Figma Pro plan on 2026-09-07 (`heyhi-skills/app-to-figma/references/probes.md` and the gitignored `<engagement folder>/app-to-figma-proof/probe-log-2026-09-07.md`). This log records which of those this skill relies on and probes the update-mode-specific calls that `app-to-figma`'s initial build did not exercise.

## Calls this skill depends on

| Call | Where used | Provenance |
|---|---|---|
| `figma.importComponentSetByKeyAsync` | Figma leg, `library` rows | `app-to-figma` probe C, green 2026-09-07 (Pro, control library) |
| `figma.variables.importVariableByKeyAsync` | Figma leg, bound values | `app-to-figma` probe, green 2026-09-07 |
| `figma.importStyleByKeyAsync` | Figma leg, text/effect styles | `app-to-figma` probe, green 2026-09-07 |
| `node.setProperties` (VARIANT/TEXT/BOOLEAN/INSTANCE_SWAP) | Figma leg, changed props | `app-to-figma` probe, green 2026-09-07 |
| `frame.setExplicitVariableModeForCollection` | Figma leg, theme mode | `app-to-figma` probe, green 2026-09-07 |
| `get_metadata` (MCP tool) | Figma leg, update mode: read existing frames | probed here |
| `instance.swapComponent` | Figma leg, update mode: a changed variant | probed here |
| `validate_output` (MCP tool, `rendered_css`) | prototype gate (blocking) + repo conformance read | probed here |
| `retrieve_application_context` (MCP tool) | contract + manifest + ds-map retrieval | probed here |

## Update-mode probes (this skill's own)

The update-mode calls `app-to-figma`'s initial build did not exercise: `get_metadata` (read the existing frame set before updating) and `instance.swapComponent` (retarget a changed variant on an existing instance without detaching). These are the two calls that distinguish an increment from a first build.

**Probe plan (run during the Figma-leg attempt, against a published control library so it does not depend on the proof library being published):**

1. `get_metadata` on the scratch artifact file returns the existing node tree (the frames `app-to-figma` built, or an empty file if the first build was operator-gated). Read-only; no write.
2. Import a control component set by key (`Simple Design System` Button, key on record in the gitignored app-to-figma proof log), instance a variant, then `instance.swapComponent(otherVariant.mainComponent)` to a different variant, and read back `mainComponent.remote === true` and the new variant name. Remove the probe node.

**Observed result (2026-09-07, Pro plan, published control library):** `get_metadata` on the scratch artifact returned its node tree (an empty page: the Wave 1 base build was itself operator-gated). Import-by-key of the control Button set succeeded (18 variants), an instance was created, and `swapComponent` retargeted it from one variant to another with `mainComponent.remote === true` on both before and after; the probe node was removed. So the two update-mode calls that distinguish an increment from a first build both execute on the Pro plan. The file keys and the full run stay in the gitignored proof log `<engagement folder>/feature-increment-proof/probe-log-2026-09-07.md` per the hermetic seal; this reference records the calls and their observed outcome without the keys.

## Non-Figma tool probes

- **`validate_output(artifact, artifact_type: "rendered_css")`** returns a `ValidationResult` with `valid: bool`, `errors`, `warnings`, `suggestions`, `confidence_score`. The prototype gate reads `valid`. Observed shape verified against `heyhi-mcp/heyhi_mcp/core/validator.py` (the `ValidationResult` model) and exercised live in the prototype-leg proof; the run output is pasted into the proof record.
- **`retrieve_application_context(query, scope)`** returns `{scope, status, result, total_items, truncated}`; an absent data file degrades to `{status: "absent", scope, expected_path}` rather than raising (Lane E, on `origin/main`). The skill reads `status` and falls back to a passed contract path when `absent`.

## The operator gate (inherited from Wave 1)

The Figma leg's live rebuild against the proof library is blocked on that library being published, the same operator step recorded in the Wave 1 `app-to-figma` proof (`probe-log-2026-09-07.md`: import-by-key resolves nothing from an unpublished source; publishing is a Figma UI action with no Plugin-API path). This is not a kill condition (import-by-key itself works on the Pro plan, proven green) and not a defect in this skill; it is a named human step. The proof records the Figma column as an operator-gated finding, not an unexplained miss, and the coverage table stays honest.

*HeyHi Confidential. `skill-updates/feature-increment/references/`. Probe log. Shared Figma calls proven in `app-to-figma`'s probe (2026-09-07); update-mode and tool probes recorded here and in the gitignored proof log.*
