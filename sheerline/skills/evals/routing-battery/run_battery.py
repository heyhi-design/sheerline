#!/usr/bin/env python3
"""Sheerline routing battery runner.

Runs cases.yaml against both registries and the R-5 coverage guard, reporting
PASS / FAIL / KNOWN_GAP per case. Re-run after ANY registry edit (data or engine):

    python3 sheerline/skills/evals/routing-battery/run_battery.py

Exit code is non-zero iff a hard FAIL occurred (a documented KNOWN_GAP never fails
the run). Imports each engine read-only under a unique module name; the shared keel
engines are not modified. Authored wave R-6, plan-sheerline-skills-upgrade-2026-08-22.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]  # routing-battery -> evals -> skills -> sheerline -> repo root
CASES = HERE / "cases.yaml"
ENGINES = {
    "main": (
        REPO / "ai-services/agentic-infrastructure/skill-registry.py",
        REPO / "ai-services/agentic-infrastructure/skill-registry.yaml",
    ),
    "subset": (
        REPO / "sheerline/skills/registry/skill-registry.py",
        REPO / "sheerline/skills/registry/skill-registry.yaml",
    ),
}
REGISTRY_DIR = REPO / "sheerline/skills/registry"
# An exported copy (the private sheerline repo) carries EXPORT.json at its root and ships only
# the subset registry. There, "main" cases are skipped and counted, never silently passed. In
# the monorepo (ai-services/ present, marker ignored) a missing engine is still a hard error.
EXPORTED = (REPO / "EXPORT.json").is_file() and not (REPO / "ai-services").is_dir()

_loaded: dict[str, object] = {}


# Skills an exported copy deliberately leaves out (instance-only, filtered from its registry):
# a case expecting one of them is skipped and counted there, never silently passed.
DROPPED = (set(json.loads((REPO / "EXPORT.json").read_text())
               .get("instance_only_skills_dropped", [])) if EXPORTED else set())


def _shipped(reg_key: str, case: dict | None = None) -> bool:
    if case is not None and case.get("expect") in DROPPED:
        return False
    return not EXPORTED or all(p.is_file() for p in ENGINES[reg_key])


def _engine(reg_key: str):
    if reg_key in _loaded:
        return _loaded[reg_key]
    path, _ = ENGINES[reg_key]
    modname = f"battery_engine_{reg_key}"
    spec = importlib.util.spec_from_file_location(modname, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[modname] = mod  # dataclass annotation resolution needs it registered
    spec.loader.exec_module(mod)
    _loaded[reg_key] = mod
    return mod


def _resp(reg_key: str, query: str, top_k: int = 3):
    mod = _engine(reg_key)
    _, yaml_path = ENGINES[reg_key]
    registry = mod.load_registry(yaml_path)
    return mod.search_with_confidence(query, registry, top_k=top_k)


def run() -> int:
    data = yaml.safe_load(CASES.read_text())
    passes = fails = gaps = skipped = 0

    print("── Routing ──")
    for c in data.get("routing", []):
        if not _shipped(c["registry"], c):
            skipped += 1
            continue
        r = _resp(c["registry"], c["query"])
        winner = r.results[0].id if r.results else None
        if winner == c["expect"]:
            passes += 1
            print(f"  PASS  [{c['registry']:>6}] {c['query']!r} -> {winner}")
        elif c.get("status") == "known_gap":
            gaps += 1
            print(f"  GAP   [{c['registry']:>6}] {c['query']!r} -> {winner} "
                  f"(expected {c['expect']}; documented residual)")
        else:
            fails += 1
            print(f"  FAIL  [{c['registry']:>6}] {c['query']!r} -> {winner} "
                  f"(expected {c['expect']})")

    print("── Abstention ──")
    for c in data.get("abstention", []):
        if not _shipped(c["registry"], c):
            skipped += 1
            continue
        r = _resp(c["registry"], c["query"])
        if r.confidence == "insufficient":
            passes += 1
            print(f"  PASS  [{c['registry']:>6}] abstain {c['query']!r} -> insufficient")
        else:
            fails += 1
            print(f"  FAIL  [{c['registry']:>6}] abstain {c['query']!r} -> {r.confidence} "
                  f"(expected insufficient)")

    print("── Coverage warnings (R-5) ──")
    sys.path.insert(0, str(REGISTRY_DIR))
    import coverage_guard as cg  # noqa: E402  (path set above)
    state = cg._area_state_by_ref_id()
    for c in data.get("coverage_warnings", []):
        if not _shipped(c["registry"], c):
            skipped += 1
            continue
        r = _resp(c["registry"], c["query"], top_k=1)
        top = r.results[0] if r.results else None
        warned = bool(top and cg.coverage_note(top.id, top.type, state))
        if warned == c["expect_warning"]:
            passes += 1
            print(f"  PASS  [{c['registry']:>6}] warn={warned} {c['query']!r}")
        else:
            fails += 1
            print(f"  FAIL  [{c['registry']:>6}] warn={warned} "
                  f"(expected {c['expect_warning']}) {c['query']!r}")

    if skipped:
        print(f"\n  ({skipped} case(s) skipped: their registry or expected skill is not shipped in this exported copy)")
    print(f"\n{passes} passed · {gaps} known-gap · {fails} failed")
    if passes + gaps + fails == 0:
        print("FAIL: no case ran (every registry skipped), so nothing was verified")
        return 1
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(run())
