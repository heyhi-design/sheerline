#!/usr/bin/env python3
"""Routing fixture for crit-prep-and-capture (staged; registry-inert).

Builds the candidate registry entry the way a real entry is shaped — the SKILL.md
description with its `NOT for …` clauses STRIPPED from the description field and
supplied only as `not_for` (the live registry never double-counts clause terms) —
and scores the spec § 5.3 queries against the live Sheerline subset registry,
with and without the clauses. Read-only: nothing is written to any registry.

Run from the repo root:
    python3 skill-updates/crit-prep-and-capture/scripts/routing-fixture.py

HeyHi Confidential.
"""
from __future__ import annotations

import copy
import importlib.util
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
REG_DIR = ROOT / "sheerline" / "skills" / "registry"
SKILL_MD = ROOT / "skill-updates" / "crit-prep-and-capture" / "SKILL.md"

TAGS = [
    "crit prep", "crit pre-read", "crit capture", "design crit", "pre-read",
    "capture decisions", "dispositions", "follow-ups", "presenter", "facilitator",
]
TRIGGERS = [
    "crit prep", "prep the crit", "crit pre-read", "capture the crit", "crit notes",
    "what did we decide in crit", "design crit capture",
]
QUERIES = [
    "prep the design crit for Thursday", "capture the decisions from today's crit",
    "design crit capture", "crit prep", "critique this design",
    "run a design critique session", "critical path for the launch", "design review prep",
    "record this design decision", "prep the Human-in-the-Loop workshop",
    "map this journey in figjam", "audit this prototype for interaction completeness",
    "build the slides for the crit readout", "critique this logo",
]


def load_engine():
    spec = importlib.util.spec_from_file_location("sr", REG_DIR / "skill-registry.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["sr"] = mod
    spec.loader.exec_module(mod)
    return mod


def split_description(desc: str) -> tuple[str, list[str]]:
    """Return (description without NOT-for clauses, [clauses])."""
    flat = " ".join(desc.split())
    parts = re.split(r"\s*NOT for ", flat)
    body, clauses = parts[0], [p.strip().rstrip(".") for p in parts[1:]]
    return body, clauses


def main() -> int:
    sr = load_engine()
    reg = sr.load_registry(REG_DIR / "skill-registry.yaml")
    fm = re.match(r"^---\n(.*?)\n---\n", SKILL_MD.read_text(), re.S).group(1)
    desc_body, clauses = split_description(yaml.safe_load(fm)["description"])
    template = next(c for c in reg if c.id == "design-rationale-decision-record")

    def entry(not_for: list[str]):
        c = copy.deepcopy(template)
        c.id, c.name, c.description = "crit-prep-and-capture", "Crit Prep & Capture", desc_body
        c.semantic_tags, c.trigger_patterns, c.not_for = TAGS, TRIGGERS, list(not_for)
        return c

    def score(query, registry):
        res = sr.search(query, registry, top_k=5)
        rows = [(getattr(m, "capability", m).id, round(float(getattr(m, "relevance_score", 0) or 0), 3)) for m in res]
        rank = next((i + 1 for i, (cid, _) in enumerate(rows) if cid == "crit-prep-and-capture"), None)
        return rows[:3], rank, sr.assess_confidence(res)

    print(f"clauses parsed from SKILL.md description: {len(clauses)}")
    for c in clauses:
        print(f"  - {c[:80]}")
    for label, nf in (("no clauses", []), ("with clauses", clauses)):
        print(f"\n=== {label} ===")
        for q in QUERIES:
            top, rank, conf = score(q, reg + [entry(nf)])
            print(f"  {q!r}: top={top} | cpc rank={rank} | {conf}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
