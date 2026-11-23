#!/usr/bin/env python3
"""Compare a Figma annotation read-back against the targets file (references/figma-annotation-handoff.md).

    python3 scripts/check_annotation_readback.py <annotation-targets.json> <annotation-readback.json> [--json]

Each target is MATCH, MISSING, CHANGED or DUPLICATE; unmapped rows are listed as gaps. A
pipeline annotation is recognized by its `[id]` in its label; MATCH means the label, with that
`[id]` removed, equals the target's label exactly (whitespace aside) and the category matches,
so a person's appended edit reads CHANGED. Exit 1 unless every
target is MATCH, exit 2 on an unreadable input, zero targets, or an empty id or label. Offline and read-only. Stdlib only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def label_of(ann: dict) -> str:
    return str(ann.get("labelMarkdown") or ann.get("label") or "")


def compare(targets: dict, readback: dict) -> dict:
    cats = targets.get("categories") or {}
    rows = []
    for t in targets.get("targets") or []:
        tid, node = str(t["id"]), str(t["node_id"])
        mine = [a for a in (readback.get(node) or []) if re.search(rf"(?<![\w-]){re.escape(tid)}(?![\w-])", label_of(a))]
        want_cat = cats.get(t.get("category"), t.get("category"))
        if not mine:
            status = "MISSING"
        elif len(mine) > 1:
            status = "DUPLICATE"
        else:
            got = mine[0]
            without_id = re.sub(rf"\[{re.escape(tid)}\]", " ", label_of(got))
            same_label = norm(without_id) == norm(t.get("label", ""))
            same_cat = want_cat is None or str(got.get("categoryId")) == str(want_cat)
            status = "MATCH" if same_label and same_cat else "CHANGED"
        rows.append({"id": tid, "node_id": node, "status": status})
    unmapped = targets.get("unmapped") or []
    counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("MATCH", "MISSING", "CHANGED", "DUPLICATE")}
    return {"targets": rows, "counts": counts, "unmapped": unmapped}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Annotation read-back check (offline).")
    ap.add_argument("targets")
    ap.add_argument("readback")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    try:
        targets = json.loads(Path(args.targets).read_text(encoding="utf-8"))
        readback = json.loads(Path(args.readback).read_text(encoding="utf-8"))
        if not isinstance(targets.get("targets"), list) or not isinstance(readback, dict):
            raise ValueError("targets needs a `targets` list; the read-back must map node ids to lists")
        if not targets["targets"]:
            raise ValueError("the targets file lists no targets; nothing to check is not a clean result")
        for t in targets["targets"]:
            if not all(k in t for k in ("id", "node_id", "label")):
                raise ValueError(f"target without id, node_id or label: {str(t)[:80]}")
            if not norm(str(t["label"])) or not norm(str(t["id"])):
                raise ValueError(f"target with an empty id or label: {str(t)[:80]}")
        result = compare(targets, readback)
    except (OSError, json.JSONDecodeError, ValueError, AttributeError) as exc:
        print(f"check_annotation_readback: cannot read input: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        for r in result["targets"]:
            print(f"{r['status']:<9} {r['id']} on {r['node_id']}")
        for u in result["unmapped"]:
            print(f"GAP       {u.get('source', '?')} row {u.get('source_row', '?')}: {u.get('reason', 'unmapped')}")
        c = result["counts"]
        print(f"check_annotation_readback: {c['MATCH']} match, {c['MISSING']} missing, "
              f"{c['CHANGED']} changed, {c['DUPLICATE']} duplicate, {len(result['unmapped'])} unmapped")
    ok = result["counts"]["MATCH"] == len(result["targets"])
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
