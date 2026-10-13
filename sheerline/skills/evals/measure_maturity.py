#!/usr/bin/env python3
"""measure_maturity.py — the Sheerline practice-capability meter.

The finer-grained sibling of ``measure_coverage.py``. Where coverage answers "does a
practice EXIST" (>=1 skill + a foundation), this reads the ``maturity`` block each area now
carries in ``sheerline/os/foundations/registry.yaml`` and derives, for the 13-area map:

  * the ACHIEVEMENT profile — each area's current practice-capability level (1-5, or
    ``ungraded`` when null);
  * the TARGET profile — each area's owner-set aspiration (or ``unset``);
  * the DELTA between them, which *is* the roadmap (CMMI achievement-vs-target framing);
  * advisory ``indirect``-evidence candidates per area, classified from the corrections
    registry + intake by REUSING ``heyhi-mcp/heyhi_mcp/corrections/search.py``'s
    field-weighted scoring (never a new matcher, never a stored foreign key);
  * two advisory flags: ``NEEDS-REGRADE`` (a graded area whose ``last_graded`` predates a
    passed cadence checkpoint) and ``POSSIBLE-REGRESSION`` (a graded area with a fresh
    corrections incident dated after its grade).

ADVISORY BY CONSTRUCTION. This instrument declares ZERO ``gate_class: deterministic-block``
rules (parent-plan arc rule 4): a practice-capability read is a judgment call. The script
therefore exits 0 on ANY successful read — zero areas graded or all thirteen — and exits
non-zero (2) ONLY on an operational failure (missing/malformed registry, missing PyYAML).
It never exits non-zero on a NEEDS-REGRADE or POSSIBLE-REGRESSION flag, and it never
lowers a stored level (only a human does — the "practice capability can regress" property).

READ-ONLY on the registry. It never rewrites ``registry.yaml``. The stored
``maturity.re_grade_due`` is an inert placeholder; this script computes the authoritative
value at read time and prints it. Rewriting the hand-formatted, comment-bearing registry
programmatically would normalize its bytes and strip its comments (see the corrections-registry
entry ``programmatic-file-edit-normalizes-byte-format``), so re-grades are applied by a human
Edit, never by this tool.

Cadence anchor (B3, NN/g-literal — no invented calendar). ``re_grade_due`` rides the empirical-
moat arc's own dated checkpoints, supplied at run time via ``--checkpoints`` (never hardcoded
here, so this file cannot go stale against the arc). With no checkpoints supplied, no area is
flagged overdue and a one-line note says so.

Run from anywhere — paths resolve against the repo root, four levels up from this file
(evals -> skills -> sheerline -> repo root), exactly like ``measure_coverage.py``.

Usage:
    python3 sheerline/skills/evals/measure_maturity.py                 # table + summary + flags
    python3 sheerline/skills/evals/measure_maturity.py --emit-profile  # the achievement/target/delta table only
    python3 sheerline/skills/evals/measure_maturity.py --quiet         # summary line + exit code only
    python3 sheerline/skills/evals/measure_maturity.py --checkpoints 2026-10-09,2026-11-29 --as-of 2026-11-30
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Optional

try:
    import yaml
except ImportError:  # pragma: no cover - environment guard
    sys.stderr.write(
        "measure_maturity.py needs PyYAML (the same dependency skill-registry.py and\n"
        "measure_coverage.py use). Install it (pip install pyyaml) or run in the tooling env.\n"
    )
    raise SystemExit(2)

REPO_ROOT = Path(__file__).resolve().parents[3]
REGISTRY = REPO_ROOT / "sheerline" / "os" / "foundations" / "registry.yaml"
CORRECTIONS_DIR = REPO_ROOT / "heyhi-mcp" / "heyhi_mcp" / "corrections"
SEARCH_PY = CORRECTIONS_DIR / "search.py"
INTAKE_DIR = REPO_ROOT / "corrections-intake"
# Future input: the I1 / evaluator findings export. I1 is unscheduled per
# plan-design-output-eval-harness-2026-07-16's own status line, so this is a named hook, not a
# dependency: read if present, silently skipped while absent (which is the state today).
EVALUATOR_FINDINGS = REPO_ROOT / "sheerline" / "skills" / "evals" / "evaluator-findings.json"

RUNGS = {1: "Scaffolded", 2: "Situated", 3: "Governed", 4: "Calibrated", 5: "Exemplary"}
# Advisory floor for surfacing a candidate `indirect` hit. Not a gate: it only decides what
# gets shown for a human to confirm. The corrections `search.py` weights it feeds are the
# single source of the scoring mechanism (correction 1.0 / trigger_context 0.8 / ...).
INDIRECT_MIN_SCORE = 0.4


# --- reuse the corrections scoring mechanism, not a second matcher -----------------------

def load_search_module():
    """Load corrections/search.py by file path and return the module (or None if absent).

    By file path, not `import heyhi_mcp...`, so this stays as dependency-light as
    measure_coverage.py (search.py is stdlib-only) and does not drag in heyhi_mcp's package
    __init__ chain. The module MUST be registered in sys.modules before exec_module, or its
    @dataclass fails to resolve __module__ under Python 3.9 (AttributeError on None).
    """
    if not SEARCH_PY.is_file():
        return None
    spec = importlib.util.spec_from_file_location("corrections_search", SEARCH_PY)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


# --- loaders ----------------------------------------------------------------------------

def load_registry() -> dict:
    return yaml.safe_load(REGISTRY.read_text()) or {}


def load_corrections_entries() -> list[dict]:
    """Every corrections entry (seed + method) as a plain dict, plus intake candidates.

    The two YAML registries carry structured entries usable directly by search(). Intake
    markdown files have no structured fields, so each becomes a best-effort pseudo-entry
    {id: <stem>, correction: <full text>, category: "intake", status: <parsed>} — enough for
    search()'s token-overlap scoring on the `correction` field. All of this is advisory: an
    `indirect` hit is a candidate for a human to confirm, never a stored foreign key.
    """
    entries: list[dict] = []
    for name in ("seed-corrections.yaml", "method-corrections.yaml"):
        path = CORRECTIONS_DIR / name
        if not path.is_file():
            continue
        try:
            data = yaml.safe_load(path.read_text()) or {}
        except Exception:
            continue
        rows = data.get("entries") if isinstance(data, dict) else data
        if isinstance(rows, list):
            for row in rows:
                if isinstance(row, dict) and row.get("id"):
                    row = dict(row)
                    row["_source"] = name
                    entries.append(row)
    if INTAKE_DIR.is_dir():
        for md in sorted(INTAKE_DIR.glob("2026-*.md")):
            if md.name.upper().startswith("README"):
                continue
            try:
                text = md.read_text()
            except Exception:
                continue
            status = "proposed"
            for line in text.splitlines():
                if line.strip().lower().startswith("**status:**"):
                    status = line.split("**", 2)[-1].strip().strip("*").strip() or "proposed"
                    break
            entries.append(
                {
                    "id": md.stem,
                    "category": "intake",
                    "correction": text,
                    "status": status,
                    "last_fired": None,
                    "_source": "corrections-intake",
                }
            )
    return entries


def load_evaluator_findings() -> list[dict]:
    """The I1 / evaluator findings export as indirect-candidate pseudo-entries, if present.

    A future input (plan B3): I1 is unscheduled per plan-design-output-eval-harness-2026-07-16,
    so this file does not exist today and this returns []. When it lands, each finding becomes a
    search()-scoreable entry {id, correction, category:"evaluator", status:"active", last_fired}
    so it can surface as an `indirect` candidate and, when dated, contribute to POSSIBLE-
    REGRESSION exactly as a corrections entry does. Best-effort and fully guarded: a missing or
    malformed export is a no-op, never an error.
    """
    if not EVALUATOR_FINDINGS.is_file():
        return []
    try:
        import json
        data = json.loads(EVALUATOR_FINDINGS.read_text())
    except Exception:
        return []
    rows = data.get("findings") if isinstance(data, dict) else data
    if not isinstance(rows, list):
        return []
    out: list[dict] = []
    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            continue
        text = str(row.get("finding") or row.get("summary") or row.get("text") or "")
        if not text:
            continue
        out.append(
            {
                "id": str(row.get("id") or f"evaluator-{i}"),
                "category": "evaluator",
                "correction": text,
                "status": str(row.get("status") or "active"),
                "last_fired": row.get("last_fired") or row.get("date"),
                "_source": "evaluator-findings",
            }
        )
    return out


def area_query(area: dict) -> str:
    """The classification query for an area: its key + name.

    Deliberately key + name, NOT the area's FOUNDATION.md body. The foundation vocabulary was
    tried and dropped: its headers are broad enough that almost every corrections/intake entry
    token-overlaps them (30-37 of 43 per area vs 0-6 for key+name in the Phase-B probe), which
    turns `indirect` into noise rather than a candidate surface. key + name is the discriminating
    vocabulary, and a human confirms every hit anyway (indirect is never auto-filed). The
    plan's B2 named FOUNDATION.md as a vocabulary source; this is the faithful-to-intent
    refinement — a useful candidate surface beats a literal-but-useless one.
    """
    key = str(area.get("key", "")).replace("-", " ")
    name = str(area.get("name", ""))
    return " ".join(p for p in (key, name) if p).strip()


# --- date helpers (None-safe per yaml-null-to-python-none-rendering) ----------------------

def parse_date(value) -> Optional[date]:
    if not value:
        return None
    if isinstance(value, date):
        return value
    try:
        return datetime.strptime(str(value)[:10], "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


# --- derivation -------------------------------------------------------------------------

def classify_indirect(area: dict, entries: list[dict], search_mod, active_only: bool) -> list[dict]:
    """Advisory candidate `indirect` hits for an area, scored by the reused search() mechanism."""
    if search_mod is None:
        return []
    query = area_query(area)
    if not query:
        return []
    status = "active" if active_only else None
    # search.py filters on entry["status"] == status; corrections use "active", intake use
    # "proposed", so an active_only pass over intake naturally returns nothing (intended:
    # POSSIBLE-REGRESSION keys on promoted/active corrections, not unpromoted intake).
    matches = search_mod.search(query, entries, top_k=10, status=status)
    return [
        {"id": m.id, "score": m.score, "entry": m.entry}
        for m in matches
        if m.score >= INDIRECT_MIN_SCORE
    ]


def re_grade_due(area: dict, checkpoints: list[date], as_of: date) -> bool:
    """True when the area is graded and a cadence checkpoint has passed since last_graded."""
    last = parse_date((area.get("maturity") or {}).get("last_graded"))
    if last is None:
        return False  # ungraded -> not "overdue", just not yet graded
    return any(last < cp <= as_of for cp in checkpoints)


def possible_regression(area: dict, entries: list[dict], search_mod) -> list[str]:
    """Ids of fresh corrections incidents (last_fired after the area's grade) — a review flag.

    Never lowers the stored level; surfaces for a human. Only meaningful for a graded area.
    """
    mat = area.get("maturity") or {}
    if mat.get("level") is None:
        return []
    graded = parse_date(mat.get("last_graded"))
    if graded is None:
        return []
    hits = classify_indirect(area, entries, search_mod, active_only=True)
    fresh = []
    for hit in hits:
        fired = parse_date(hit["entry"].get("last_fired"))
        if fired is not None and fired > graded:
            fresh.append(hit["id"])
    return fresh


def build_rows(registry: dict, entries: list[dict], search_mod, checkpoints: list[date], as_of: date) -> list[dict]:
    rows = []
    for area in registry.get("areas", []):
        mat = area.get("maturity") or {}
        level = mat.get("level")
        target = mat.get("target")
        delta = (target - level) if isinstance(level, int) and isinstance(target, int) else None
        indirect = classify_indirect(area, entries, search_mod, active_only=False)
        rows.append(
            {
                "id": area.get("id"),
                "key": area.get("key", ""),
                "name": area.get("name", ""),
                "level": level,
                "target": target,
                "delta": delta,
                "indirect_n": len(indirect),
                "regrade": re_grade_due(area, checkpoints, as_of),
                "regression": possible_regression(area, entries, search_mod),
            }
        )
    return rows


# --- output -----------------------------------------------------------------------------

def _fmt_level(v) -> str:
    if v is None:
        return "ungraded"
    return f"{v} {RUNGS.get(v, '?')}"


def _fmt_target(v) -> str:
    return "unset" if v is None else f"{v} {RUNGS.get(v, '?')}"


# Set in main() when the corrections registry is absent: the indirect column is then printed
# as "n/m" (not measured), never as a 0 that reads like "searched, found nothing".
CORPUS_ABSENT = False


def emit_profile(rows: list[dict]) -> str:
    """The achievement-vs-target delta table (Markdown), for embedding in a report."""
    lines = ["| Area | Level (achievement) | Target | Delta | Indirect candidates |",
             "|---|---|---|---|---|"]
    for r in rows:
        delta = "—" if r["delta"] is None else (f"+{r['delta']}" if r["delta"] > 0 else str(r["delta"]))
        lines.append(
            f"| {r['id']} {r['name']} | {_fmt_level(r['level'])} | {_fmt_target(r['target'])} "
            f"| {delta} | {'n/m' if CORPUS_ABSENT else r['indirect_n']} |"
        )
    if CORPUS_ABSENT:
        lines.append("")
        lines.append("n/m = not measured: the corrections registry is absent (an exported copy).")
    return "\n".join(lines)


def summary_line(rows: list[dict]) -> str:
    total = len(rows)
    graded = sum(1 for r in rows if r["level"] is not None)
    targeted = sum(1 for r in rows if r["target"] is not None)
    needs_regrade = sum(1 for r in rows if r["regrade"])
    regressions = sum(1 for r in rows if r["regression"])
    positive_deltas = [r for r in rows if isinstance(r["delta"], int) and r["delta"] > 0]
    if positive_deltas:
        top = max(positive_deltas, key=lambda r: r["delta"])
        roadmap = f"largest delta +{top['delta']} at area {top['id']} ({top['name']})"
    elif targeted:
        roadmap = "no positive delta (all graded areas meet target)"
    else:
        roadmap = "no targets set"
    return (
        f"maturity: {graded} of {total} areas graded ({total - graded} ungraded); "
        f"{targeted} with a target; {roadmap}; "
        f"{needs_regrade} need re-grade; {regressions} possible regression. "
        f"Advisory only (0 gates)."
    )


def print_report(rows: list[dict], checkpoints: list[date], quiet: bool) -> None:
    if not quiet:
        print(emit_profile(rows))
        print()
        flagged = [r for r in rows if r["regrade"] or r["regression"]]
        for r in flagged:
            notes = []
            if r["regrade"]:
                notes.append("NEEDS-REGRADE (a cadence checkpoint passed since last_graded)")
            if r["regression"]:
                notes.append(f"POSSIBLE-REGRESSION (fresh incidents: {', '.join(r['regression'])})")
            print(f"  area {r['id']} {r['name']}: " + "; ".join(notes))
        if flagged:
            print("  (advisory — surfaced for human review; no level is auto-changed)")
            print()
        if not checkpoints and any(r["level"] is not None for r in rows):
            print("  note: no --checkpoints supplied, so re_grade_due could not be computed "
                  "(pass the empirical-moat arc's current checkpoints to enable it).")
            print()
    print(summary_line(rows))


# --- cli --------------------------------------------------------------------------------

def parse_checkpoints(raw: Optional[str]) -> list[date]:
    if not raw:
        return []
    out = []
    for token in raw.split(","):
        token = token.strip()
        if not token:
            continue
        parsed = parse_date(token)
        if parsed is None:
            sys.stderr.write(f"measure_maturity.py: ignoring un-parseable checkpoint '{token}'\n")
            continue
        out.append(parsed)
    return out


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--emit-profile", action="store_true",
                        help="print the achievement/target/delta table (Markdown) and exit 0")
    parser.add_argument("--quiet", action="store_true", help="print only the summary line + exit code")
    parser.add_argument("--checkpoints", default=None,
                        help="comma-separated ISO dates (the empirical-moat arc's checkpoints); "
                             "the cadence anchor for re_grade_due. Not hardcoded — supplied here.")
    parser.add_argument("--as-of", default=None, help="ISO date to evaluate re_grade_due against (default: today)")
    args = parser.parse_args(argv)

    if not REGISTRY.is_file():
        sys.stderr.write(f"measure_maturity.py: registry not found at {REGISTRY}\n")
        return 2
    try:
        registry = load_registry()
    except Exception as exc:  # a malformed registry is an operational failure, not a finding
        sys.stderr.write(f"measure_maturity.py: could not parse the registry: {exc}\n")
        return 2
    if not registry.get("areas"):
        sys.stderr.write("measure_maturity.py: registry has no areas\n")
        return 2

    as_of = parse_date(args.as_of) or date.today()
    checkpoints = parse_checkpoints(args.checkpoints)
    global CORPUS_ABSENT
    search_mod = load_search_module()
    if search_mod is None or not CORRECTIONS_DIR.is_dir():
        CORPUS_ABSENT = True
        # Say so loudly: without the corrections registry the indirect-evidence column reads 0
        # because nothing was searched, not because nothing matched (expected in an exported copy,
        # where the registry is retained and not shipped).
        sys.stderr.write(
            "measure_maturity.py: corrections registry not found at "
            f"{CORRECTIONS_DIR.relative_to(REPO_ROOT).as_posix()}; the indirect-evidence column "
            "is NOT MEASURED (0 = not searched), and POSSIBLE-REGRESSION cannot fire.\n"
        )
    entries = load_corrections_entries() + load_evaluator_findings()
    rows = build_rows(registry, entries, search_mod, checkpoints, as_of)

    if args.emit_profile:
        sys.stdout.write(emit_profile(rows) + "\n")
        return 0
    print_report(rows, checkpoints, args.quiet)
    return 0  # advisory instrument: success is exit 0 regardless of flags


if __name__ == "__main__":
    raise SystemExit(main())
