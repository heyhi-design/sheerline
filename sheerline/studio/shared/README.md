---
classification: confidential
created: "2026-08-23"
lane: DISPATCH-03 (SHELL)
source: plans/plan-sheerline-studio-ui-2026-08-21.md
---

# Wheelhouse shared shell (usage contract)

Three files, authored by DISPATCH-03, that every Wheelhouse screen sits on:

| File | What it is |
|---|---|
| `studio.css` | The full token set (palette, type, spacing) + shared components. |
| `shell-snippet.html` | The exact top-bar + 9-item rail + footer, plus the one snapshot include and the self-activating fill JS. |
| `README.md` | This contract. |

## Frozen after DISPATCH-03 merges

Once D-03 lands, `studio/shared/` is **frozen**. Wave-3 lanes (D-04…D-07) do not edit these files. Only **D-08** folds candidates back. This is the parallelism mechanism from plan §6.3: four lanes build four sets of screens without ever touching the same file.

## How a wave-3 page is built

1. **`<head>`**: copy the head from `index.html` (the `charset`/`viewport` meta, the `<title>`, and `<link rel="stylesheet" href="shared/studio.css">`). All pages are flat under `sheerline/studio/`, so `shared/studio.css` and `data/snapshot.js` resolve for every screen.
2. **Paste `shell-snippet.html` verbatim** as the first thing inside `<body>`. Put your screen markup between the two `PAGE CONTENT` markers.
3. **Do not add a second `<script src="data/snapshot.js">`.** The snippet loads the data global first, in the right order. Your page's own `<script>` (filters, tabs, rendering from `SHEERLINE_DATA`) goes after your content and can read the global directly.
4. **Page-scoped styles** go in a page `<style>` block with a `/* candidate for shared */` comment on anything you think belongs in `studio.css`. Do not add it to `studio.css` yourself.

## Conventions the tokens encode (hold these across lanes)

- **Render from the data global, never hardcode counts.** Area chips, cards, capability counts, phase rows: build them by iterating `window.SHEERLINE_DATA`. The snapshot is the single truth; a hardcoded "13" or "42" drifts.
- **Coverage ramp** (`.cov` + `.cov--{deep,covered,partial,gap}`): a 4-step teal→neutral ramp. deep = solid teal, covered = teal outline, partial = half-fill, gap = neutral **dashed** track. Crimson never encodes coverage.
- **Crimson is the human's color** (law L8). Use `--crimson*` / `.human-slot` / `.rule-line` for exactly three things: human-gate and empty-judgment slots (L4), the ownership/moat + hermetic-seal seam, and the "grades inform, never gate" rule line. Never decorative, never a status color.
- **DM Mono is the machine-truth register.** Every value that comes from the snapshot (paths, ids, counts, statuses, load costs) renders in `.mono` / `--font-mono`.
- **Accessibility floor is a hard gate.** The focus ring is defined once in the base (`:focus-visible`); do not remove it. Teal is safe as link text on the field but verify any new text/surface pair at WCAG 2.2 AA. Decorative glyphs get `aria-hidden`; meaning gets `sr-only` text (never `aria-label` as the sole mechanism on a static element). No CSS masks of external SVGs; inline any icon.
- **Honesty labels are load-bearing.** Anything simulated carries a `sim` badge or an inline note at the point of interaction, not only in the footer.

## Palette provenance

Every hex in `studio.css` is lifted verbatim from the Sheerline architecture diagrams' `<style>` blocks (`sheerline/docs/diagrams/*.svg`), named inline in the CSS. The Studio is meant to look like the diagrams grew a workspace (plan §5). Soft/faint neutrals were darkened (light) / lightened (dark) from the diagram values by the minimum needed to clear AA 4.5:1 as text; the comment on each notes the shift.

---

*HeyHi Confidential*
