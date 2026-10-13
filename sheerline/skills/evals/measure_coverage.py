#!/usr/bin/env python3
"""measure_coverage.py — the Sheerline eval-coverage meter.

Derives, for every governed capability (``type: skill`` in the Sheerline subset
registry), whether it has an eval-case home and where. Prints the covered /
uncovered counts and the uncovered percentage the ``eval-coverage`` early-warning
signal reads, and exits 1 if any governed skill has no home. This exists so the
signal is re-measured by a script instead of by memory — the 2026-08-22 audit's
"41 of 42 have none" reading went stale because nothing recomputed it.

Two homes count as coverage:

  * in-skill:  ``heyhi-skills/<id>/evals/cases.yaml``  or  ``.../evals/evals.json``
  * harness:   ``sheerline/skills/evals/<id>/cases.yaml``

Coverage is derived purely from file existence, so it cannot drift from reality.
The ``area`` label is a static map sourced from the ``os/foundations/*/FOUNDATION.md``
"Registered skills (area N)" rows and the subset registry's ``area`` field; it is
cosmetic (it labels a row, it never affects the covered/uncovered count).

Run from anywhere — paths resolve against the repo root, four levels up from this
file (evals -> skills -> sheerline -> repo root).

Usage:
    python3 sheerline/skills/evals/measure_coverage.py           # summary + table; exit 1 on any gap
    python3 sheerline/skills/evals/measure_coverage.py --emit-index   # print INDEX.md to stdout
    python3 sheerline/skills/evals/measure_coverage.py --quiet    # summary line + exit code only
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - environment guard
    sys.stderr.write(
        "measure_coverage.py needs PyYAML (the same dependency skill-registry.py uses).\n"
        "Install it (pip install pyyaml) or run in the tooling env.\n"
    )
    raise SystemExit(2)

REPO_ROOT = Path(__file__).resolve().parents[3]
SUBSET_REGISTRY = REPO_ROOT / "sheerline" / "skills" / "registry" / "skill-registry.yaml"
HARNESS_EVALS = REPO_ROOT / "sheerline" / "skills" / "evals"

# The "more than a quarter uncovered" threshold the eval-coverage signal fires on.
# Stated once here so the number the signal reads and the number the script prints agree.
UNCOVERED_FIRE_THRESHOLD = 0.25

# Home area per governed skill for skills the subset registry does not tag with `area`
# (the legacy HeyHi cluster). Sourced from the `Registered skills (area N)` rows in
# os/foundations/*/FOUNDATION.md as of 2026-09-07. A skill the registry DOES tag uses
# that tag; this map fills only the rest. Static label — a re-home is rare and edited here.
HOME_AREA = {
    # area 3 — Content Design
    "heyhi-voice": "3",
    # area 5 — Prototyping (hi-fi build + built-prototype audit)
    "heyhi-ui-ux": "5",
    "ui-studio": "5",
    "heyhi-design-bridge": "5",
    "heyhi-prototype-audit": "5",
    # area 6 — Visual Design
    "heyhi-logo-system": "6",
    "heyhi-style-brief": "6",
    "heyhi-style-selection": "6",
    "heyhi-style-entry-author": "6",
    "design-system-onboard": "6",
    # area 7 — Design Systems
    "heyhi-design-intelligence-audit": "7",
    "design-system-review": "7",
    "design-system-care-monthly": "7",
    "heyhi-token-description-author": "7",
    "heyhi-schema-extension-author": "7",
    "heyhi-pipeline-validator": "7",
    "heyhi-theme-validator": "7",
    "heyhi-style-to-token-reviewer": "7",
    "ui-studio-onboard": "7",
    "heyhi-shopify-theme": "7",
    "heyhi-audit-campaign": "7/8",  # home area 7, cross-cutting area 8 (dispatch names it 7/8)
    # area 9 — Design Strategy
    "futurecasting": "9",
    # area 11 — Collaboration & Facilitation
    "heyhi-deck": "11",
    "heyhi-workshop": "11",
}


def load_governed_skills() -> list[dict]:
    """Every capability of type `skill` in the subset registry — the governed set."""
    reg = yaml.safe_load(SUBSET_REGISTRY.read_text())
    caps = reg.get("capabilities") or []
    return [c for c in caps if c.get("type") == "skill"]


def _count_cases_yaml(path: Path) -> int | None:
    try:
        data = yaml.safe_load(path.read_text()) or {}
    except Exception:
        return None
    cases = data.get("cases")
    return len(cases) if isinstance(cases, list) else None


def _count_evals_json(path: Path) -> tuple[int | None, str]:
    """Best-effort case count + inferred shape ("Prompt" / "Scenario" / "Findings") for the
    skill's PRIMARY corpus.

    Counts the first present primary key only. A nested sibling corpus (e.g. `onboard_evals`,
    which ui-studio carries for ui-studio-onboard) is deliberately excluded so it is never summed
    into the parent skill's count.
    """
    try:
        data = json.loads(path.read_text())
    except Exception:
        return None, "?"
    if not isinstance(data, dict):
        return None, "?"
    for key in ("cases", "evals", "scenarios", "tests"):
        val = data.get(key)
        if isinstance(val, list) and val and isinstance(val[0], dict):
            first = val[0]
            if "scenario" in first or "assertion" in first:
                shape = "Scenario"
            elif "expected_findings" in first:
                shape = "Findings"
            else:
                shape = "Prompt"
            return len(val), shape
    return None, "?"


def resolve_home(skill_id: str) -> tuple[str, int | None, str]:
    """Return (home_kind, case_count, shape) for a governed skill.

    Precedence: in-skill cases.yaml, in-skill evals.json, harness cases.yaml, none.
    """
    in_yaml = REPO_ROOT / "heyhi-skills" / skill_id / "evals" / "cases.yaml"
    in_json = REPO_ROOT / "heyhi-skills" / skill_id / "evals" / "evals.json"
    harness = HARNESS_EVALS / skill_id / "cases.yaml"
    if in_yaml.exists():
        return f"heyhi-skills/{skill_id}/evals/cases.yaml", _count_cases_yaml(in_yaml), "Findings"
    if in_json.exists():
        count, shape = _count_evals_json(in_json)
        return f"heyhi-skills/{skill_id}/evals/evals.json", count, shape
    if harness.exists():
        return f"sheerline/skills/evals/{skill_id}/cases.yaml", _count_cases_yaml(harness), "Findings (governance probe)"
    return "none", None, "—"


def area_for(cap: dict) -> str:
    area = cap.get("area")
    if area is not None:
        return str(area)
    return HOME_AREA.get(cap.get("id", ""), "—")


def build_rows() -> list[dict]:
    rows = []
    for cap in load_governed_skills():
        sid = cap.get("id", "")
        home, count, shape = resolve_home(sid)
        rows.append(
            {
                "id": sid,
                "area": area_for(cap),
                "home": home,
                "count": count,
                "shape": shape,
                "covered": home != "none",
            }
        )
    return rows


def _area_sort_key(area: str) -> tuple[int, str]:
    head = area.split("/")[0]
    try:
        return (int(head), area)
    except ValueError:
        return (999, area)


def emit_index(rows: list[dict]) -> str:
    total = len(rows)
    covered = sum(1 for r in rows if r["covered"])
    uncovered = total - covered
    pct_uncovered = (uncovered / total * 100) if total else 0.0
    ordered = sorted(rows, key=lambda r: (_area_sort_key(r["area"]), r["id"]))
    lines: list[str] = []
    lines.append("---")
    lines.append("classification: confidential")
    lines.append('title: "Sheerline Eval-Home Index"')
    lines.append("generated_by: sheerline/skills/evals/measure_coverage.py")
    lines.append("---")
    lines.append("")
    lines.append("# Sheerline Eval-Home Index")
    lines.append("")
    lines.append(
        "**Generated file — do not hand-edit.** Regenerate with "
        "`python3 sheerline/skills/evals/measure_coverage.py --emit-index > sheerline/skills/evals/INDEX.md`."
    )
    lines.append("")
    lines.append(
        f"One row per governed capability (`type: skill` in the subset registry). "
        f"A capability is covered when it has an eval-case home — in-skill "
        f"(`heyhi-skills/<id>/evals/`) or harness-level (`sheerline/skills/evals/<id>/cases.yaml`). "
        f"The `eval-coverage` early-warning signal fires when more than a quarter are uncovered; "
        f"`measure_coverage.py` is the meter that reads this."
    )
    lines.append("")
    lines.append(
        f"**Coverage: {covered} of {total} governed capabilities have an eval home "
        f"({uncovered} uncovered, {pct_uncovered:.0f}%).**"
    )
    lines.append("")
    lines.append("| Capability | Area | Eval home | Cases | Shape |")
    lines.append("|---|---|---|---|---|")
    for r in ordered:
        count = "—" if r["count"] is None else str(r["count"])
        home = "none" if r["home"] == "none" else f"`{r['home']}`"
        lines.append(f"| `{r['id']}` | {r['area']} | {home} | {count} | {r['shape']} |")
    lines.append("")
    lines.append(
        "Shapes: **Prompt** / **Scenario** (`evals.json`, conversational or build; see "
        "`heyhi-skills/EVALS.md`), **Findings** (`cases.yaml`, audit/validate), "
        "**Findings (governance probe)** (harness-level cases under `sheerline/skills/evals/<id>/`, "
        "which test whether a skill honors its area's invariants rather than whether its prose is good — "
        "the shape of `visual-design-governance/cases.yaml`)."
    )
    lines.append("")
    lines.append("*HeyHi Confidential*")
    lines.append("")
    return "\n".join(lines)


def print_summary(rows: list[dict], quiet: bool) -> int:
    total = len(rows)
    covered = sum(1 for r in rows if r["covered"])
    uncovered = [r for r in rows if not r["covered"]]
    n_unc = len(uncovered)
    pct_unc = (n_unc / total) if total else 0.0
    if not quiet:
        ordered = sorted(rows, key=lambda r: (_area_sort_key(r["area"]), r["id"]))
        width = max((len(r["id"]) for r in rows), default=10)
        print(f"{'capability':<{width}}  area  cases  eval home")
        print(f"{'-' * width}  ----  -----  ---------")
        for r in ordered:
            count = "—" if r["count"] is None else str(r["count"])
            print(f"{r['id']:<{width}}  {r['area']:>4}  {count:>5}  {r['home']}")
        print()
    fires = pct_unc > UNCOVERED_FIRE_THRESHOLD
    print(
        f"eval-coverage: {covered} of {total} governed capabilities have an eval home; "
        f"{n_unc} uncovered ({pct_unc * 100:.0f}%). "
        f"Signal threshold: >{UNCOVERED_FIRE_THRESHOLD * 100:.0f}% uncovered "
        f"=> {'FIRED' if fires else 'clear'}."
    )
    if n_unc:
        print("gap — no eval home:", ", ".join(r["id"] for r in uncovered))
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit-index", action="store_true", help="print INDEX.md to stdout and exit 0")
    parser.add_argument("--quiet", action="store_true", help="print only the summary line + gap")
    args = parser.parse_args(argv)
    rows = build_rows()
    if args.emit_index:
        sys.stdout.write(emit_index(rows))
        return 0
    return print_summary(rows, args.quiet)


if __name__ == "__main__":
    raise SystemExit(main())
