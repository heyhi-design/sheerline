#!/usr/bin/env python3
"""Validate Intent-Journey Map contracts against schemas/ijm-contract.schema.json.

    python3 scripts/validate_contracts.py <contract.json | folder> [...] [--schema <path>] [--json]

For each contract it reports, by name, the three fields that drift loses first between runs
(`schema_version`, `tier`, `research_question`), then every other schema error. A folder is read
for `*ijm-contract*.json` (all `*.json` when none match). Full validation uses the `jsonschema`
package when it is installed; without it, only the schema's required top-level keys and the
three named fields are checked, and the report says so. Exit 1 when any contract fails, 2 when
there is nothing to read. Read-only.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_SCHEMA = HERE.parent / "schemas" / "ijm-contract.schema.json"
NAMED = ("schema_version", "tier", "research_question")


def find_schema(path: str | None) -> Path:
    if path:
        return Path(path)
    if DEFAULT_SCHEMA.is_file():
        return DEFAULT_SCHEMA
    for parent in HERE.parents:  # a draft run outside the deployed skill folder
        cand = parent / "heyhi-skills" / "intent-journey-map" / "schemas" / "ijm-contract.schema.json"
        if cand.is_file():
            return cand
    return DEFAULT_SCHEMA


def collect(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for p in map(Path, paths):
        if p.is_dir():
            found = sorted(p.glob("*ijm-contract*.json")) or sorted(p.glob("*.json"))
            files.extend(found)
        elif p.is_file():
            files.append(p)
        else:
            raise FileNotFoundError(str(p))
    return files


def check(doc, schema: dict, validator) -> dict:
    missing = [k for k in NAMED if not isinstance(doc, dict) or k not in doc]
    problems = []
    if isinstance(doc, dict):
        if "research_question" in doc and doc["research_question"] is not None:
            problems.append("research_question is not null (it is an empty slot by construction)")
        if "tier" in doc and doc["tier"] not in (1, 2):
            problems.append(f"tier is {doc['tier']!r} (a contract is Tier 1 or 2)")
    if validator is not None:
        for err in sorted(validator.iter_errors(doc), key=lambda e: list(e.absolute_path)):
            msg = err.message
            if any(f"'{k}' is a required property" == msg for k in NAMED):
                continue  # already reported by name
            where = "/".join(str(x) for x in err.absolute_path) or "(top)"
            problems.append(f"{where}: {msg}")
        mode = "jsonschema"
    else:
        req = [k for k in schema.get("required", []) if k not in NAMED]
        problems += [f"(top): '{k}' is a required property" for k in req
                     if not isinstance(doc, dict) or k not in doc]
        mode = "required-keys only (jsonschema not installed)"
    return {"missing": missing, "problems": problems, "mode": mode,
            "ok": not missing and not problems}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Validate IJM contracts (read-only).")
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--schema")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    schema_path = find_schema(args.schema)
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        files = collect(args.paths)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"validate_contracts: cannot read input: {exc}", file=sys.stderr)
        return 2
    if not files:
        print("validate_contracts: no contracts found", file=sys.stderr)
        return 2
    try:
        import jsonschema  # optional
        validator = jsonschema.Draft202012Validator(schema)
    except ImportError:
        validator = None

    results = []
    for f in files:
        try:
            doc = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            results.append({"path": str(f), "missing": list(NAMED), "ok": False,
                            "problems": [f"unreadable: {exc}"], "mode": "unreadable"})
            continue
        results.append({"path": str(f), **check(doc, schema, validator)})

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            print(f"{'PASS' if r['ok'] else 'FAIL'} {r['path']}")
            if r["missing"]:
                print(f"  missing: {', '.join(r['missing'])}")
            for p in r["problems"]:
                print(f"  {p}")
        failed = sum(not r["ok"] for r in results)
        print(f"validate_contracts: {len(results)} contract(s), {failed} failed "
              f"[{results[0]['mode'] if results else 'n/a'}; schema {schema_path.name}]")
    return 1 if any(not r["ok"] for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
