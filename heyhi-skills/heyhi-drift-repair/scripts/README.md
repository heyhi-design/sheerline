# `scripts/` — the repair engine

*HeyHi Confidential. The engine behind `heyhi-drift-repair/SKILL.md` Step 3.*

## What is here

- `repair_engine.py` — the per-finding engine: `run(findings, artifacts, library, *, auto_apply=False)` → a `RunResult` of `applied` (deterministic, re-validated, with deviation records), `proposals` (human-confirm), and `learn_candidates` (authored, unfiled). Plus `load_library`, `value_delta`, and the deployment-only `write_learn_candidate`.

## Run it

The acceptance harness drives the engine on fixtures and proves the spec's §8 criteria:

```bash
python3 heyhi-skills/heyhi-drift-repair/evals/run.py
```

It reads the **live** seed library (`heyhi-mcp/heyhi_mcp/corrections/seed-corrections.yaml`), so the repair transforms cannot drift from a stale copy. Needs PyYAML (the same interpreter that runs `heyhi-mcp`).

**Runtime requirement.** `evals/run.py` loads the seed repair library from `heyhi-mcp/heyhi_mcp/corrections/seed-corrections.yaml`, a retained runtime that lives in the HeyHi monorepo and does not ship with the Sheerline scaffold export. Run the harness from a monorepo checkout (or any checkout that carries that runtime at the same repo-relative path); in a standalone scaffold checkout it cannot load the seed library and will not run.

## The delegation boundary (what is stubbed vs. the real wire)

The spec's rule is *never re-implement detection* and *do not invent a second matcher*. This staged engine honors that by taking findings **pre-located** (matching is upstream) and stubbing only the two calls that need the full MCP, with the deployment wire named at each site:

| Step | Staged engine (self-contained) | At deployment |
|---|---|---|
| `match_correction` | findings arrive with `matched_correction` resolved (the spec: findings arrive located) | `heyhi_mcp.corrections.predicates.evaluate_predicate` over the instance's live registry |
| the ambiguity guard (precondition 1: does the literal resolve to exactly one token?) | the correction carries a single `expected` (→ 1 candidate) or an explicit `candidates` list (>1 → downgrade to `[inferred]`) | the instance's token resolver decides against the canonical set (fixtures excluded) |
| re-validation (Step 4) | a focused conformance re-scan of the repaired declaration (originating literal gone + no new literal) | `heyhi_mcp.core.validator.validate_output(..., constraints=<instance known_tokens / legal_contrast_pairs>)` |
| the repair itself | value → token-reference substitution from the `known_bad`/`expected` pair | **identical** — the transform is the same in both modes |

The stub is the seed-substrate stand-in the seed library itself describes: "the fallback substrate the readers fall back to when no live registry is present" (`seed-corrections.yaml:6-11`). No `heyhi_mcp` import — the staged artifact runs in isolation.

## What the engine never does

- Writes anything for a `detection: judged` finding, or a hybrid's judged half (the never-auto invariant — structural, not a confidence threshold).
- Auto-writes the token source (target A) or the Figma canvas (target C) — both are propose/deferred in v1.
- Files a learn candidate to the live registry. `write_learn_candidate` targets `corrections-intake/` only, is a deployment helper, and is never called by the eval.
- Carries anyone's tokens — a tenant run is judged by the tenant registry passed to `run`.
