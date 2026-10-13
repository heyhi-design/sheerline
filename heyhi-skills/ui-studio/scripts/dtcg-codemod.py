#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dtcg-codemod.py — migrate a ui-studio brand config's token *maps* from bare scalars
to DTCG-native objects (W5 / audit G7), backward-compatibly.

Walks the config's ``tokens.*`` value maps (the categories ``tokens.py``'s
``CATEGORY_TYPE`` can type: color, typography.scale, spacing.tiers, motion.easing,
motion.durations, radius) and wraps each scalar whose *shape* matches the target
``$type`` into ``{"$value": <original>, "$type": <inferred>, "$description": <...>}``.
Descriptions are lifted from ``meta.field_provenance[path].description`` when present,
so the migration carries existing engineer context forward rather than dropping it.

Deliberately conservative — it does NOT touch:
  - prose notes / non-value scalars sharing a map (``hierarchy_note``, ``rhythm``) —
    the value-shape check skips them;
  - singleton scalar properties outside the typed maps (``spacing.base``,
    ``focus.outline.color``) — the shim reads those either shape at runtime anyway;
  - composite categories with no Step-2 scalar ``$type`` (``elevation`` box-shadows);
  - anything already in DTCG shape (idempotent).

Safety: writes a SIBLING ``<name>.dtcg.json`` by default (zero risk to the live
config). ``--in-place`` requires ``--dry-run`` to have been reviewed first and is
gated behind an explicit confirmation. A round-trip check asserts every wrapped
``$value`` equals the original scalar before anything is written.

Usage:
    python3 scripts/dtcg-codemod.py --config brand-config/example.json
    python3 scripts/dtcg-codemod.py --config brand-config/example.json --dry-run
    python3 scripts/dtcg-codemod.py --config brand-config/example.json --in-place --yes
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tokens import is_dtcg_token, resolve_token_value, type_for_path, value_matches_type  # noqa: E402


def _walk_and_wrap(node, path, prov, stats):
    """Recursively return a wrapped copy of ``node``. ``path`` is the dotted token
    path (rooted at the first key under ``tokens``). Mutates ``stats`` in place."""
    if is_dtcg_token(node):
        stats["already_dtcg"] += 1
        return node  # idempotent: leave existing DTCG objects untouched
    if isinstance(node, dict):
        return {k: _walk_and_wrap(v, f"{path}.{k}" if path else k, prov, stats)
                for k, v in node.items()}
    if isinstance(node, list):
        stats["skipped_list"] += 1
        return node  # arrays (prohibited[], contrast_notes[]) are never tokens
    # scalar leaf
    dtcg_type = type_for_path(path)
    if dtcg_type is None:
        stats["skipped_untyped"].append(path)
        return node  # category not codemod-typable — leave scalar (shim reads it)
    if not value_matches_type(node, dtcg_type):
        stats["skipped_shape"].append(path)  # a note or non-value scalar in a map
        return node
    desc = prov.get(path, {}).get("description", "")
    wrapped = {"$value": node, "$type": dtcg_type}
    if desc:
        wrapped["$description"] = desc
    stats["wrapped"].append((path, node, dtcg_type))
    return wrapped


def migrate(config: dict) -> tuple[dict, dict]:
    """Return (migrated_config, stats). Pure — does not mutate ``config``."""
    stats = {"wrapped": [], "already_dtcg": 0, "skipped_untyped": [],
             "skipped_shape": [], "skipped_list": 0}
    prov = config.get("meta", {}).get("field_provenance", {})
    # Provenance keys are "tokens.<path>"; the walker roots at the first key under
    # tokens, so normalise the provenance map to that same rooting.
    prov_rooted = {k[len("tokens."):]: v for k, v in prov.items() if k.startswith("tokens.")}
    out = dict(config)
    out["tokens"] = _walk_and_wrap(config.get("tokens", {}), "", prov_rooted, stats)
    return out, stats


def _navigate(tokens_root: dict, dotted_path: str):
    """Return the node at ``dotted_path`` under the migrated tokens tree, or None."""
    node = tokens_root
    for seg in dotted_path.split("."):
        if not isinstance(node, dict) or seg not in node:
            return None
        node = node[seg]
    return node


def round_trip_ok(migrated: dict, stats: dict) -> list[str]:
    """Real round-trip: for every wrapped leaf, resolve the value back out of the
    MIGRATED config through the shim and confirm it equals the original scalar.
    Tests the migration output and the shim together (not a self-comparison)."""
    fails = []
    tokens_root = migrated.get("tokens", {})
    for path, original, _ in stats["wrapped"]:
        node = _navigate(tokens_root, path)
        if resolve_token_value(node) != original:
            fails.append(path)
    return fails


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="dtcg-codemod",
                                 description="Migrate a brand config's token maps to DTCG-native.")
    ap.add_argument("--config", type=Path, required=True, help="path to the brand config JSON")
    ap.add_argument("--dry-run", action="store_true", help="report only; write nothing")
    ap.add_argument("--in-place", action="store_true",
                    help="overwrite the config in place (requires --yes)")
    ap.add_argument("--yes", action="store_true", help="confirm an --in-place write")
    args = ap.parse_args(argv)

    if not args.config.exists():
        print(f"error: {args.config} not found", file=sys.stderr)
        return 1
    config = json.loads(args.config.read_text(encoding="utf-8"))
    migrated, stats = migrate(config)

    fails = round_trip_ok(migrated, stats)
    if fails:
        print("error: round-trip check FAILED — refusing to write. Paths:", file=sys.stderr)
        for p in fails:
            print(f"  - {p}", file=sys.stderr)
        return 1

    # Report
    print(f"DTCG codemod — {args.config.name}")
    print(f"  wrapped:       {len(stats['wrapped'])} scalars -> DTCG objects")
    print(f"  already DTCG:  {stats['already_dtcg']}")
    print(f"  skipped (untyped category): {len(stats['skipped_untyped'])}")
    print(f"  skipped (non-value shape):  {len(stats['skipped_shape'])}")
    print(f"  skipped (arrays):           {stats['skipped_list']}")
    by_type: dict[str, int] = {}
    for _, _, t in stats["wrapped"]:
        by_type[t] = by_type.get(t, 0) + 1
    print("  by $type:      " + ", ".join(f"{t}={n}" for t, n in sorted(by_type.items())))
    if stats["skipped_shape"]:
        print("  note-like/non-value scalars left untouched: "
              + ", ".join(stats["skipped_shape"][:8])
              + (" …" if len(stats["skipped_shape"]) > 8 else ""))

    payload = json.dumps(migrated, indent=2, ensure_ascii=False) + "\n"

    if args.dry_run:
        print("\n--dry-run: no file written.")
        return 0
    if args.in_place:
        if not args.yes:
            print("\nrefusing --in-place without --yes (review a --dry-run first).",
                  file=sys.stderr)
            return 1
        args.config.write_text(payload, encoding="utf-8")
        print(f"\nwrote (in place): {args.config}")
        return 0
    sibling = args.config.with_suffix(".dtcg.json")
    sibling.write_text(payload, encoding="utf-8")
    print(f"\nwrote sibling: {sibling} (live config untouched)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
