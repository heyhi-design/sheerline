# Design Bridge — Plugin Transport (Mode 1 live write)

**HeyHi Confidential.** Staged in `skill-updates/` for review; promote to the deployed
skill (`heyhi-skills/heyhi-design-bridge/scripts/`) on a clean live acceptance.

## Why this exists

The builder (v0.8.0) turns a prototype into 10 sub-50k `use_figma` chunks. The blocker
was never the builder — it was the **transport** to a write-capable `use_figma`:

- **No scriptable `use_figma` endpoint.** The local Figma MCP (`127.0.0.1:3845`) is
  read-only (5 get_* tools). The write-capable connector is the app-brokered
  "claude.ai Figma" — no replayable URL/token, and `claude mcp` has no `call`. A
  standalone script (runbook option a) has nothing to call. *(Verified 2026-06-17.)*
- **The `use_figma` sandbox has no network** — `fetch` and `XMLHttpRequest` are both
  `undefined` (probed live). So no agent-side shim can stream a chunk in either. The
  only bytes that enter `use_figma` are the `code` param the agent generates — i.e. the
  44k-of-dense-SVG transcription that silently drops masters.
- **A Figma plugin's main thread blocks `eval`/`new Function`** — so fetch-then-eval
  inside a plugin is also out.

So the transport **bundles**: `emit_plugin.py` writes each chunk as a real `async`
function into a generated `code.js` (no eval, no network). Each chunk runs in its own
function scope — exactly `use_figma`'s per-call semantics (fresh `made`/`out`; ids
threaded via the `IDMAP` parameter, merged in memory between chunks). Rasters embed via
`figma.createImage` (bytes bundled as base64). The agent is fully out of the transport.

## Files

| File | Role | Tracked? |
|------|------|----------|
| `emit_plugin.py` | Assembles a runnable plugin dir (`code.js` + manifest + ui) from a `build_figma.py --out-dir` | yes |
| `plugin/manifest.json` | Static manifest (`networkAccess: none`) | yes |
| `plugin/ui.html` | Static UI — a Build button + result readout | yes |
| `mock-run.mjs` | Headless proof: runs `code.js` against a Node mock of the Figma API | yes |
| `<plugin-out>/code.js` | GENERATED — embeds chunk + raster data | **NO — gitignored** for client builds |

## Pipeline

```bash
SK=heyhi-skills/heyhi-design-bridge
T=$SK/scripts            # deployed build_figma.py / run_build.py
TR=skill-updates/heyhi-design-bridge/transport

# 1. Build the plan (svgo on; client IR + out-dir resolve to a gitignored path)
python3 $T/build_figma.py <IR> --svgo --out-dir <BUILD_DIR>

# 2. Assemble the runnable plugin (client builds: <PLUGIN_DIR> must be gitignored)
python3 $TR/emit_plugin.py --out-dir <BUILD_DIR> --plugin-out <PLUGIN_DIR>

# 3. Headless proof (optional but recommended) — expect MOCK-RUN: PASS, 0 errors
node $TR/mock-run.mjs <PLUGIN_DIR>/code.js
```

## The one human-initiated step (Earn the Room — a write into the client's own file)

1. Open the **target Figma file** in the Figma **desktop** app (the client's own
   identity file for a client deliverable; a HeyHi scratch file for a proof).
2. **Import once:** Plugins → Development → *Import plugin from manifest…* → pick
   `<PLUGIN_DIR>/manifest.json`. (Re-running a new build only needs *Run* again —
   Figma re-reads `code.js` from disk each run; no re-import.)
3. **Run:** Plugins → Development → *HeyHi Design Bridge Runner* → click
   **Build into this file**. The page (`HeyHi Bridge · …`) builds with `--rerun replace`
   semantics on that named page only; identity pages are untouched.
4. Read the result readout (created / reused / rasters / flags / errors).

## Hermetic seal

A client build's generated `code.js` embeds the client's SVG paths, raster bytes, and
page name. Always emit `--plugin-out` to a **gitignored** path (under `clients/<eng>/…`).
Never commit a generated `code.js`. The tracked files here carry no build data.
