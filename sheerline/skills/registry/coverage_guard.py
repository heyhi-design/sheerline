#!/usr/bin/env python3
"""Sheerline coverage guard — a rendering-layer wrapper over the reused keel
registry engine (``skill-registry.py``, R2).

Why this exists (upgrade-plan wave R-5, Decision Register Q-1, 2026-08-22):
the confidence gate scores relevance, not destination substance, so it can route
an in-scope query *confidently* into a practice area that is only a tracked stub
("plan a usability study" -> Area 1, a gap-state foundation). That confident
answer lands in an empty room, and nothing said so.

Q-1 chose the rendered-warning fix over an engine change: **the shared keel
confidence-gate engine is not touched.** This wrapper imports that engine
read-only, runs the same routed search, then annotates each result whose
practice area is a gap/stub — reading the coverage/foundation state from
``os/foundations/registry.yaml`` (the single source of truth for area state).

Usage:
    python3 coverage_guard.py "plan a usability study with 5 participants"
    python3 coverage_guard.py "build a service blueprint" --top-k 3

The engine file is never modified; if a future keel-engine update lands, this
wrapper keeps working as long as ``load_registry`` / ``search_with_confidence``
keep their signatures.
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ENGINE_PATH = HERE / "skill-registry.py"
FOUNDATIONS_REGISTRY = HERE.parent.parent / "os" / "foundations" / "registry.yaml"

# Area states that mean "the room this routes into is under-built."
# coverage: design-practice coverage (gap = no deployed skills for the area).
# foundation: the governed-context manifest depth (stub = a tracked placeholder).
# Matches the plan's Q-1/R-5 spec exactly: coverage gap OR foundation stub. A
# 'deferred' foundation is deliberately NOT warned — the state meant "a later phase fills
# this folder" with *partial* coverage and deployed skills behind it, never an empty room.
# As of 2026-09-05 no area carries it (area 3 was the last; areas 3, 4 and 9 were filled
# 2026-09-05, 2026-09-05 and 2026-08-28), but the rule stays so a future deferred fill is
# not mislabeled as a gap.
WARN_COVERAGE = {"gap"}
WARN_FOUNDATION = {"stub"}


_ENGINE = None


def _load_engine():
    """Import skill-registry.py as a module (its filename's hyphen blocks a
    plain import). Runs the engine's module-level code only — main() is guarded
    behind ``if __name__ == "__main__"`` and does not fire on import.

    The module is registered in sys.modules before exec_module: the engine
    defines @dataclass types, and dataclasses resolves annotations via
    sys.modules[cls.__module__], which must exist during class creation.
    Cached so repeated calls do not re-exec the engine."""
    global _ENGINE
    if _ENGINE is not None:
        return _ENGINE
    spec = importlib.util.spec_from_file_location("keel_registry_engine", ENGINE_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    _ENGINE = module
    return module


def _area_state_by_ref_id() -> dict[str, tuple[int, str, str]]:
    """Map each area-reference id (``area-<key>``) -> (area_number, coverage, foundation).

    Only references are mapped, and deliberately so: the audit's concern (§ 2.2)
    is a confident route into an area *pointer* that no deployed skill backs — the
    empty room. A deployed skill winning is never an empty room, even when the
    area's foundation manifest is still thin, so skills are not flagged here.
    (The engine's Capability dataclass does not carry the skill ``area:`` field
    anyway; area references resolve through their ``area-<key>`` id.)
    """
    foundations = yaml.safe_load(FOUNDATIONS_REGISTRY.read_text())
    by_num = {a["id"]: (a.get("coverage"), a.get("foundation")) for a in foundations["areas"]}
    key_to_num = {a["key"]: a["id"] for a in foundations["areas"]}

    out: dict[str, tuple[int, str, str]] = {}
    for key, num in key_to_num.items():
        coverage, foundation = by_num[num]
        out[f"area-{key}"] = (num, coverage, foundation)
    return out


def coverage_note(cap_id: str, cap_type: str, state: dict[str, tuple[int, str, str]]) -> str | None:
    """Return a warning line if this result is an empty-room route, else None.

    An empty-room route is a *reference* (an area pointer, not a deployed skill)
    winning into an area whose coverage is a gap or whose foundation is a stub —
    the exact "confident answer that lands in an empty room" the audit flagged.
    """
    if cap_type != "reference":
        return None
    entry = state.get(cap_id)
    if not entry:
        return None
    area_num, coverage, foundation = entry
    if coverage not in WARN_COVERAGE and foundation not in WARN_FOUNDATION:
        return None
    return (f"WARNING — routed into an under-built area (Area {area_num}: coverage={coverage}, "
            f"foundation={foundation}). This is an area pointer, not a deployed skill, and the "
            f"area's governed context is still a stub/gap — treat it as a pointer to the "
            f"foundation, not a finished capability, and confirm the work is in Sheerline's scope.")


def route(query: str, top_k: int = 3) -> int:
    engine = _load_engine()
    registry = engine.load_registry()
    state = _area_state_by_ref_id()
    resp = engine.search_with_confidence(query, registry, top_k=top_k)

    print(f'\n─── Coverage-guarded route for "{query}" ───')
    print(f"    confidence: {resp.confidence}"
          + (f"   score_gap: {resp.score_gap}" if resp.score_gap is not None else ""))
    if not resp.results:
        print("    (no capability cleared the score floor — honest abstention)\n")
        return 0
    for i, m in enumerate(resp.results, 1):
        print(f"\n  {i}. {m.name}  [{m.type}]   score {m.relevance_score:.3f}")
        print(f"     {m.location}")
        note = coverage_note(m.id, m.type, state)
        if note:
            print(f"     ⚠ {note}")
    print()
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Coverage-guarded routing over the Sheerline subset registry "
                    "(rendering-layer warning for gap/stub destinations; engine untouched).")
    ap.add_argument("query", help="Natural-language routing query")
    ap.add_argument("--top-k", type=int, default=3, help="Max results to show (default 3)")
    args = ap.parse_args(argv)
    return route(args.query, top_k=args.top_k)


if __name__ == "__main__":
    sys.exit(main())
