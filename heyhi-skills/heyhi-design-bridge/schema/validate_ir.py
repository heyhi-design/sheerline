#!/usr/bin/env python3
"""Validate a scene-graph IR file against the v0.1 schema. Phase-0 smoke test.

Usage:
    python3 validate_ir.py [ir_file ...]

With no arguments it validates the bundled golden IR. Exits non-zero on any
validation failure so it can gate a build step.
"""
import json
import pathlib
import sys

from jsonschema import Draft202012Validator

HERE = pathlib.Path(__file__).resolve().parent
SCHEMA = HERE / "scene-graph.schema.json"
DEFAULT_IR = HERE.parent / "examples" / "atlas-hero.lg.ir.json"


def main(argv):
    schema = json.loads(SCHEMA.read_text())
    Draft202012Validator.check_schema(schema)  # the schema itself must be valid
    validator = Draft202012Validator(schema)

    targets = argv[1:] or [str(DEFAULT_IR)]
    ok = True
    for target in targets:
        ir = json.loads(pathlib.Path(target).read_text())
        errors = sorted(validator.iter_errors(ir), key=lambda e: list(e.path))
        if errors:
            ok = False
            print(f"FAIL {target}")
            for err in errors:
                print(f"  - {list(err.path)}: {err.message}")
        else:
            print(f"PASS {target}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
