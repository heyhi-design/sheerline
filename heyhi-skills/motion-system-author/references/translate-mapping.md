---
classification: confidential
title: "Reference: Translate mapping (Figma Motion / Rive export → token-mapped spec)"
skill: motion-system-author
mode: Translate
---

# Translate mapping

**HeyHi Confidential.** How Translate mode reads a Figma Motion or Rive export, lints it against the motion system, and emits the token-mapped handoff. Load this in Translate mode. The rule that governs the whole mode: **flag off-system values, never silently rewrite the designer's motion.** The skill maps and lints; the human decides snap-versus-keep.

---

## Aug-2026 substrate (stated facts, do not re-verify online)

- **Figma Motion**: a timeline model, Dev-Mode-inspectable, with a CSS / JSON / React export and MCP passthrough. Read it live via the Figma MCP `get_motion_context` tool, or parse a developer-supplied export file.
- **Rive**: state-machine model; the Rive Editor MCP is in **early access**, so a file export is the reliable read path. Parse the state machine's transitions and their timing.

*[Substrate source: `sheerline-skill-buildout-research-2026-08-09.md` § 4.2. Treat these as the stated facts of record; flag, do not silently correct, if a live export contradicts them.]*

---

## Step B1: ingest

### Figma Motion

1. Confirm the connection with `whoami` before any live read. An unsaved / local Figma file is not reachable by the cloud MCP (see HeyHi CLAUDE.md § Figma MCP); ask for a saved `figma.com/design/<fileKey>/…` URL, or parse the exported file.
2. Read motion context with `get_motion_context` on the frame or component. It returns the timeline: which properties animate, their timing, and (where present) spring or easing parameters.
3. If only an exported file is provided (CSS / JSON / React), parse that instead. CSS carries `transition` / `@keyframes` / `animation`; JSON carries the timeline structure; React carries the animation props of whatever library the export targets. Map from whichever is provided.

Translate **does not write to Figma.** It reads motion and emits a spec.

### Rive

1. Parse the Rive export. Read each **state machine**, its states, and the **transitions** between them (the transition carries the duration/interpolation).
2. Rive interpolation is typically a duration + an easing (linear / cubic / custom); a Rive transition rarely carries a spring, so most Rive values map to the **duration+easing fallback** side of the system, and a spring token is proposed only where the motion clearly reads as spring-like. Note this in the spec so the developer knows the source was time-based.

---

## Step B2: off-system lint

Compare each animated value against the target motion system (the Author-mode system if one exists, else the token model's expected shape from `motion-token-schema.md`). Flag, with the source value and the nearest token:

| Off-system finding | What it looks like | Nearest token to offer |
|---|---|---|
| Duration off-scale | 237ms where the scale is 150 / 250 / 400 | `fallback.duration.default` (250ms) |
| Ad-hoc easing | a bespoke `cubic-bezier(...)` matching no named curve | nearest `fallback.easing.*` |
| Unmapped spring | spring params matching no spring token | nearest `spring.spatial|effects.*` |
| Wrong spring category | an overshooting (spatial-style) spring on opacity/color | `spring.effects.*` (no overshoot) |
| No reduced-motion path | an animation with no `prefers-reduced-motion` counterpart | the mandate, flag as a gap |
| Inexpressible value | something the token model cannot represent | none: flag, never drop |

Every finding is `off-system`. The skill records the source value and the nearest token so the human can decide; it does not change the value. A wrong-category spring (spatial overshoot on opacity) is the highest-value catch: it is a flicker bug the designer usually did not intend, but it is still theirs to confirm.

---

## Step B3: the token-mapped handoff

Emit one row per animation:

- **Source value**: verbatim from the export, labeled `from-export`.
- **Resolved token**: the token it maps to, or `off-system (flagged)`.
- **Fallback**: the duration+easing pair for consumers that cannot express the spring.
- **Reduced-motion**: the behavior, or `GAP: none in export`.
- **Provenance**: `from-export` for read values; `agent-derived` for anything the mapping inferred (for example, proposing a spring token for a time-based Rive transition is `agent-derived`).

Then the three closing surfaces: the off-system findings list, the reduced-motion gap list, and the ⛔ snap-vs-keep slot behind the named gate. Whether an off-system value is a bug to snap to the system or an intentional flourish to keep (and add to the system) is a restraint-and-feel call, so it stays the human's.

---

## The seam with heyhi-design-bridge (keep it clean)

Both skills have a Translate mode and both read from Figma, so the seam must be explicit:

- **`heyhi-design-bridge` Translate** turns a whole HTML prototype (or a raster) into a Figma **design file**: layout, color, type, components, the full scene graph. It writes to the canvas.
- **`motion-system-author` Translate** turns the **motion layer only** of a Figma Motion or Rive export into **tokens**. It writes a spec, not a canvas.

If the ask is "recreate this prototype as editable Figma layers," that is design-bridge. If the ask is "turn these animations into our motion tokens," that is this skill. When a single engagement wants both (build the design file, then extract its motion), run design-bridge for the file and this skill for the motion layer; do not absorb one into the other.

---

*HeyHi Confidential. Reference for `motion-system-author` (Translate mode). Spec: `sheerline-skill-buildout-research-2026-08-09.md` § 4.2.*
