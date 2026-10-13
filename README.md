---
classification: confidential
---

# Sheerline

**HeyHi's design-practice operating system.** Skills plus governed foundational context across the whole design discipline: 13 practice areas, a design-scoped skill registry, the seminar that teaches it, and the Studio prototype that shows it. Four verbs run through it: **retrieve** the system, **validate** against it, **grade** the result over time, **learn** from correction.

This is a **private export**. The canonical tree lives in HeyHi's monorepo; this repository is regenerated from it on every export (see `EXPORT.json` for the source commit and date). Treat a change made here as a proposal: open it as an issue or pull request, and it gets folded into the source and re-exported. A re-export overwrites this tree.

## What is in this repository

| Path | What it is |
|------|------------|
| `sheerline/` | The whole Sheerline tree. Start at [`sheerline/README.md`](sheerline/README.md). |
| `heyhi-skills/<id>/` | Every skill the Sheerline registry governs, at the same paths the registry's `location` fields use, so routing and the eval meters run unchanged. The list is derived from the registry at export time; `EXPORT.json` names each one. |
| `sheerline/os/project-state.yaml`, `sheerline/os/decision-log.md` | Scaffold copies: the same structure an instance keeps, without any instance's build history. |
| `EXPORT.json` | Provenance: source commit, export date, the shipped roots, the governed skills. |

## What is deliberately not here

- **The retained moat.** The Design System MCP runtime and its evaluator, the live corrections corpus, and the calibration stay in the unpublished monorepo. Sheerline reaches them through the MCP boundary; it never embeds them.
- **Instance data.** A skill that an instance calibrates ships the slot with generic defaults; the instance's own values (brand configs, palettes, ratified thresholds) live in instance files that stay with the instance. Client and engagement history is not here.
- **HeyHi's own-method skills** (its voice, pages, decks, and workshops) and HeyHi's skills outside Sheerline (sales, content, operations). They are filtered out of this copy's registry; the generic equivalents (for example `voice-system-author`) carry the method.
- **Build history and runtime internals.** Plans, research, decision records, dispatch prompts, the MCP runtime, and the public keel tree live elsewhere. Many Sheerline files cite them, as provenance or as seminar lab material (`opens_files`); those links point back to the monorepo and do not resolve here. The checks below know this and report them as pointers instead of failures. A few skill-local scripts that read the corrections corpus (for example `heyhi-skills/heyhi-drift-repair/evals/run.py`) only run in the monorepo.

## Run the checks

Python 3.9 or newer and PyYAML (`pip install pyyaml`). From the repository root:

```bash
python3 sheerline/skills/registry/skill-registry.py "confirm the backstage of this service blueprint" --confidence
python3 sheerline/seminar/smoke_test.py
python3 sheerline/skills/evals/measure_coverage.py
python3 sheerline/skills/evals/routing-battery/run_battery.py
python3 sheerline/studio/scripts/link-check.py
```

The routing battery skips the cases written against HeyHi's full registry (not shipped) and says how many it skipped. `measure_maturity.py` runs too, but its indirect-evidence column reads the corrections corpus, which is not shipped, so that column prints `n/m` (not measured) and the script warns on stderr. The Studio snapshot (`sheerline/studio/data/snapshot.js`) is regenerated from this tree at export time; open `sheerline/studio/index.html` directly to view it.

CI runs the same checks on pushes to `main`, on pull requests, and on demand.

---

*Copyright 2026 Bay Design LLC d/b/a HeyHi. All rights reserved. See [LICENSE](LICENSE).*

*HeyHi Confidential*
