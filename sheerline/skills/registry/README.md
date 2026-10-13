---
classification: confidential
title: "Sheerline Registry"
adapted_from: releases/open-source/keel/skills/registry/README.md
---

# Sheerline Registry

The discovery-aware capability index for Sheerline. It is how an agent finds the right area or skill for a task instead of loading everything every session (Earn the Room applied to context). Adapted from keel's registry README; the engine (`skill-registry.py`) is reused unmodified (R2).

## Files

- **`skill-registry.py`**: the reused keel engine: keyword + tag search with a confidence gate. Requires PyYAML and nothing else. Provenance note at the top of the file.
- **`skill-registry.yaml`**: the design-scoped registry: the 13 practice areas (as references pointing at their foundations) and the deployed design-practice skills.
- **`coverage_guard.py`**: a rendering-layer wrapper (R-5) that runs the same routed search, then flags an *empty-room* route — a confident win into an area **reference** whose coverage is a gap or whose foundation is a stub. It imports the engine read-only; the confidence-gate engine is not modified.

## Commands

```bash
python3 skill-registry.py "<task>" --confidence   # route a task (the production path)
python3 coverage_guard.py "<task>"                # same route, plus a gap/stub empty-room warning
python3 skill-registry.py --stats                 # registry size + token savings
python3 skill-registry.py --list                  # everything registered
python3 ../evals/routing-battery/run_battery.py   # regression guard — run after ANY registry edit
```

## The confidence gate (honest abstention)

The gate returns one of three verdicts:

| Verdict | Meaning | Do |
|---|---|---|
| **confident** | the top result scores well and pulls ahead of #2 | load it |
| **ambiguous** | the top result clears the floor but the gap to #2 is narrow | surface both, ask the human |
| **insufficient** | nothing cleared the score floor | abstain: no capability clearly matches |

`insufficient` is the point of the gate. Sheerline routes design work and declines everything else; a query that is not design work should return `insufficient`, not a forced match.

## The `not_for` field (disambiguation)

Two similar capabilities disambiguate with `not_for` clauses: a query that matches a clause is steered away from that capability (negative scoring). A clause may end with a routing hint, `(use other-skill)`.

**A clause can read as correct and do nothing.** The penalty keys off the clause's *first meaningful word* prefix-matching a query term, then requires two meaningful term matches. Before trusting a new clause, verify it actually fires: query the phrase it is meant to suppress and confirm the score drops. The reciprocal collisions to watch in this registry are visual-design vs. design-systems, heyhi-voice vs. area-content-design, and heyhi-design-intelligence-audit vs. heyhi-prototype-audit vs. area-accessibility. Added 2026-08-23 (upgrade-plan R-4): **heyhi-design-intelligence-audit vs. area-collaboration-facilitation** for critique queries — a `not_for` on the audit skill keyed on *critique* (a term absent from its own audit triggers, so it does not self-penalize) steers "run a design critique session" to the area-11 don't-automate facilitation surface. Verify with the routing battery (`../evals/routing-battery/`), which pins every collision above.

## Tuning

The scoring weights and the confidence thresholds live in the `TUNING` block at the top of `skill-registry.py`. They are starting defaults for a generic registry, not calibrated values. Re-tune them against a small eval set as the registry grows. One known property of the partial-trigger substring match: a short trigger word can match inside a longer unrelated word (for example `voice` inside `invoices`); the confidence gate still surfaces such a match for the human to reject, and tightening is a tuning task, not an engine change.

---

*Skills overview: `skills/README.md` · Area map: `os/foundations/registry.yaml`*

*HeyHi Confidential*
