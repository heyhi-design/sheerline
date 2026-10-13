#!/usr/bin/env python3
"""
compute_drift.py — deterministic token-drift diff for Design System Care monthly.

Plan 3A of the Tool Search / Programmatic Tool Calling plan
(ai-services/agentic-infrastructure/tool-search-programmatic-tc-plans.md), promoted
to a build by the 2026-06-13 scope-check
(ai-services/agentic-infrastructure/tool-search-scope-check-2026-06-13.md).

Why: the monthly token-drift check (design-system-care-monthly SKILL.md § Step 2)
was an agent-interpreted comparison of two full token manifests held in context
(~3,600 tokens for a 200-variable client). A numeric diff is deterministic — run it
in code (Programmatic Tool Calling), pass only the structured delta to the model for
interpretation and report-writing. More correct (catches small/precise value changes
a model comparison can miss) and far cheaper in context, on any runtime.

Pure stdlib. No Figma/MCP dependency — operates on already-extracted manifests
(current = get_variable_defs output; baseline = baseline-[YYYY-MM].json).

STAGED in skill-updates/ pending the instance owner's review; promote to
heyhi-skills/design-system-care-monthly/scripts/ on approval.
"""

from __future__ import annotations

import json
import sys


def flatten_variables(manifest, _prefix=""):
    """
    Flatten a nested variable manifest into {flat_key: scalar_value}.

    A manifest from get_variable_defs (or a stored baseline) is nested by
    collection / name / mode. Flatten any nested dict into slash-joined keys so two
    manifests compare key-for-key regardless of nesting depth. Lists are indexed.
    Scalars (str/int/float/bool/None) are leaves. An empty dict/list yields no keys,
    so a collection emptied between cycles surfaces correctly as removed leaves.
    """
    flat = {}
    if isinstance(manifest, dict):
        for k, v in manifest.items():
            key = f"{_prefix}/{k}" if _prefix else str(k)
            flat.update(flatten_variables(v, key))
    elif isinstance(manifest, list):
        for i, v in enumerate(manifest):
            flat.update(flatten_variables(v, f"{_prefix}[{i}]"))
    else:
        flat[_prefix] = manifest
    return flat


def compute_drift(current: dict, baseline: dict) -> dict:
    """
    Deterministic token drift computation. Returns a structured diff — no inference.

    current:  variable manifest from get_variable_defs (this cycle)
    baseline: variable manifest from baseline-[YYYY-MM].json (previous cycle)
    """
    diff = {
        "changed": [],
        "added": [],
        "removed": [],
        "total_current": 0,
        "total_baseline": 0,
        "drift_detected": False,
    }

    current_flat = flatten_variables(current)
    baseline_flat = flatten_variables(baseline)

    diff["total_current"] = len(current_flat)
    diff["total_baseline"] = len(baseline_flat)

    for key, current_val in current_flat.items():
        if key not in baseline_flat:
            diff["added"].append({"key": key, "value": current_val})
        elif current_val != baseline_flat[key]:
            diff["changed"].append({
                "key": key,
                "previous": baseline_flat[key],
                "current": current_val,
            })

    for key, prev_val in baseline_flat.items():
        if key not in current_flat:
            diff["removed"].append({"key": key, "previous": prev_val})

    # Deterministic ordering so month-over-month diff reports are stable and diffable.
    diff["changed"].sort(key=lambda d: d["key"])
    diff["added"].sort(key=lambda d: d["key"])
    diff["removed"].sort(key=lambda d: d["key"])

    diff["drift_detected"] = bool(diff["changed"] or diff["added"] or diff["removed"])
    return diff


def _main(argv):
    """CLI: compute_drift.py <current.json> <baseline.json> — prints the diff as JSON."""
    if len(argv) != 3:
        print(
            "usage: compute_drift.py <current-manifest.json> <baseline-manifest.json>",
            file=sys.stderr,
        )
        return 2
    with open(argv[1]) as f:
        current = json.load(f)
    with open(argv[2]) as f:
        baseline = json.load(f)
    print(json.dumps(compute_drift(current, baseline), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
