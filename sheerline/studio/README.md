---
classification: confidential
title: "Sheerline Studio"
status: partial
---

# Sheerline Studio

Sheerline Studio is a Replit-inspired workspace UI around the Sheerline design-practice harness: the thirteen YAML-and-markdown surfaces an operator otherwise holds in their head, made visible. It shows what the practice governs, what is a tracked gap, what loaded into a session, and what the quality loop found. The full specification is [`plans/plan-sheerline-studio-ui-2026-08-21.md`](../../plans/plan-sheerline-studio-ui-2026-08-21.md); this folder executes it.

HeyHi runs every loop on its own practice first, and the Studio is that own-practice surface for the harness itself. It is not a runtime. The prototype simulates sessions and routing against a real data snapshot; nothing in it executes skills, calls the Design System MCP, or writes state. Everything lands here under `sheerline/studio/`, classified Confidential, with no publish flip in scope (plan § 1).

## How to view

Open [`index.html`](index.html) in any browser. The screens are plain HTML, CSS, and a little inline JavaScript, with no build step and no server, so `file://` works. To serve them over HTTP instead, run a static server from the repo root and open `http://localhost:8000/`:

```bash
python3 -m http.server --directory sheerline/studio 8000
```

The screens are authored across the build waves in [`plans/plan-sheerline-studio-ui-2026-08-21.md`](../../plans/plan-sheerline-studio-ui-2026-08-21.md) § 7. The data layer below is the foundation every screen reads from.

## How to refresh the data

Every screen renders from [`data/snapshot.js`](data/snapshot.js), a single `window.SHEERLINE_DATA` global generated from the live `sheerline/` tree by the exporter. It is generated, never hand-edited. To regenerate it after the harness changes, run from the repo root:

```bash
python3 sheerline/studio/scripts/export-snapshot.py
```

Add `--check` to run every assertion and print the counts without writing the file:

```bash
python3 sheerline/studio/scripts/export-snapshot.py --check
```

The exporter is read-only over every source; the only file it writes is `data/snapshot.js`. `generated_at` in the snapshot is the source commit's date rather than the wall-clock time, so re-running at the same commit produces a byte-identical file. The exporter fails loudly (a nonzero exit and a named assertion) rather than emit a partial snapshot: it verifies that the capability counts match the registry, that the area count matches the registry, that every dispatch batch yields at least one prompt, that every referenced artifact exists on disk, and that the emitted data round-trips through a JSON parse.

## Simulation honesty

The prototype simulates; it never pretends to run (plan § 6.1). Every page carries the footer `Prototype — simulated interactions over a real data snapshot (<source_commit>) · HeyHi Confidential`, and anything that appears to execute (the Home-screen router, the session replay) is labeled simulated at the point of interaction. The snapshot is real data read from the `sheerline/` tree; the interactions staged over it are not.

---

*HeyHi Confidential*
