#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI Studio — Brand Config Validator

Computes completeness_score for active-brand.json and reports provisional fields,
missing sections, and mode unlock status.

Algorithm (deterministic, per build plan):
  Required blocks present and non-empty    40 pts  (5 pts × 8 blocks)
  No provisional fields                    20 pts  (proportionally deducted)
  Component inventory populated            15 pts
  UX writing slots populated               15 pts  (~1.875 pts × 8 slots)
  Layout block with named patterns         10 pts

Mode unlock thresholds:
  90–100: All confirmed. Mode A fully unlocked.
  70–89:  Minor gaps. Mode A with documented approximations.
  50–69:  Significant gaps. Mode B recommended. Mode A requires explicit override.
  <50:    Hard stop for all modes. Re-run onboarding.

Usage:
  python3 scripts/validate.py [--config PATH] [--verbose]
  python3 scripts/validate.py --config brand-config/active-brand.json
  python3 scripts/validate.py --config brand-config/example.json --verbose
"""

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DEFAULT_CONFIG = SCRIPT_DIR.parent / "brand-config" / "active-brand.json"

# The 8 required blocks for the 40-point required-blocks score
REQUIRED_BLOCKS = [
    ("brand.name",                         lambda c: bool(c.get("brand", {}).get("name", ""))),
    ("tokens.typography.families.display", lambda c: bool(c.get("tokens", {}).get("typography", {}).get("families", {}).get("display", {}).get("family", ""))),
    ("tokens.typography.families.body",    lambda c: bool(c.get("tokens", {}).get("typography", {}).get("families", {}).get("body", {}).get("family", ""))),
    ("tokens.color.backgrounds",           lambda c: bool(c.get("tokens", {}).get("color", {}).get("backgrounds", {}))),
    ("tokens.color.text",                  lambda c: bool(c.get("tokens", {}).get("color", {}).get("text", {}))),
    ("tokens.color.accent",                lambda c: bool(c.get("tokens", {}).get("color", {}).get("accent", {}))),
    ("tokens.spacing.base",                lambda c: bool(c.get("tokens", {}).get("spacing", {}).get("base", ""))),
    ("tokens.motion.easing",               lambda c: bool(c.get("tokens", {}).get("motion", {}).get("easing", {}))),
]

# The 8 standard ux_writing slots
UX_WRITING_SLOTS = [
    "empty_states", "error_messages", "tooltips", "buttons_ctas",
    "form_labels", "notifications", "loading_states", "onboarding"
]

PROVISIONAL_PREFIX = "PROVISIONAL:"


def has_provisional_values(config: dict) -> list[str]:
    """Walk the config and find all paths containing PROVISIONAL: prefix."""
    provisional_paths = []

    def walk(obj, path=""):
        if isinstance(obj, str) and obj.startswith(PROVISIONAL_PREFIX):
            provisional_paths.append(path)
        elif isinstance(obj, dict):
            for k, v in obj.items():
                walk(v, f"{path}.{k}" if path else k)
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                walk(v, f"{path}[{i}]")

    walk(config)
    return provisional_paths


def score_required_blocks(config: dict, verbose: bool = False) -> tuple[int, list[str]]:
    """Score the 8 required blocks: 5 pts each = 40 pts max."""
    score = 0
    missing = []
    for label, check in REQUIRED_BLOCKS:
        if check(config):
            score += 5
        else:
            missing.append(label)
    if verbose and missing:
        print(f"  Missing required blocks: {', '.join(missing)}")
    return score, missing


def score_provisional_fields(config: dict, verbose: bool = False) -> tuple[int, list[str]]:
    """Score provisional field penalty: 20 pts max, deducted proportionally."""
    # Collect from meta.provisional_fields array
    declared = [f.get("path", "") for f in config.get("meta", {}).get("provisional_fields", [])]

    # Also detect any PROVISIONAL: prefixed values in the wild
    detected = has_provisional_values(config.get("tokens", {}))
    all_provisional = list(set(declared + detected))

    if not all_provisional:
        return 20, []

    # Deduct proportionally: each provisional field costs 20/total-possible-provisional pts
    # Cap deductions at 20 (lose all 20 if there are many provisional fields)
    # We use a decay model: first 5 cost 4 pts each, beyond 5 cost 0 (already 0)
    pts_per_field = 20 / max(len(all_provisional), 1)
    deduction = min(20, round(len(all_provisional) * pts_per_field))
    score = max(0, 20 - deduction)

    if verbose:
        print(f"  Provisional fields ({len(all_provisional)}): {', '.join(all_provisional[:5])}"
              + (f"... +{len(all_provisional)-5} more" if len(all_provisional) > 5 else ""))
    return score, all_provisional


def score_component_inventory(config: dict, verbose: bool = False) -> int:
    """Score component inventory: 15 pts if ≥1 entry + drift checked, 7 if present but drift unchecked."""
    inventory = config.get("components", {}).get("inventory", [])
    drift = config.get("components", {}).get("drift", {})

    if not inventory:
        if verbose:
            print("  Component inventory: empty (0 pts)")
        return 0

    drift_checked = any([
        drift.get("token_drift") is not None,
        drift.get("pattern_drift") is not None,
        drift.get("api_drift") is not None,
    ])

    if drift_checked:
        if verbose:
            print(f"  Component inventory: {len(inventory)} components, drift checked (15 pts)")
        return 15
    else:
        if verbose:
            print(f"  Component inventory: {len(inventory)} components, drift NOT checked (7 pts)")
        return 7


def score_ux_writing(config: dict, verbose: bool = False) -> int:
    """Score UX writing slots: ~1.875 pts × 8 slots = 15 pts max."""
    ux = config.get("ux_writing", {})
    if not ux:
        if verbose:
            print("  UX writing block: absent (0 pts)")
        return 0

    pts_per_slot = 15 / len(UX_WRITING_SLOTS)  # 1.875 pts each
    score = 0
    populated = []
    missing = []

    for slot in UX_WRITING_SLOTS:
        slot_data = ux.get(slot, {})
        if slot_data and slot_data.get("pattern", ""):
            score += pts_per_slot
            populated.append(slot)
        else:
            missing.append(slot)

    score = round(score)
    if verbose:
        print(f"  UX writing slots populated: {len(populated)}/8 ({score} pts)")
        if missing:
            print(f"    Missing: {', '.join(missing)}")
    return score


def score_layout_block(config: dict, verbose: bool = False) -> int:
    """Score layout block: 10 pts if preferred_patterns ≥ 2, 5 if spacing_density only."""
    layout = config.get("layout", {})
    if not layout:
        if verbose:
            print("  Layout block: absent (0 pts)")
        return 0

    patterns = layout.get("preferred_patterns", [])
    spacing = layout.get("spacing_density", "")

    if len(patterns) >= 2:
        if verbose:
            print(f"  Layout block: {len(patterns)} preferred patterns (10 pts)")
        return 10
    elif spacing:
        if verbose:
            print("  Layout block: spacing_density only (5 pts)")
        return 5
    else:
        if verbose:
            print("  Layout block: present but incomplete (0 pts)")
        return 0


def compute_completeness_score(config: dict, verbose: bool = False) -> dict:
    """Compute and return full completeness score breakdown."""
    s_required, missing_blocks = score_required_blocks(config, verbose)
    s_provisional, provisional_list = score_provisional_fields(config, verbose)
    s_components = score_component_inventory(config, verbose)
    s_ux = score_ux_writing(config, verbose)
    s_layout = score_layout_block(config, verbose)

    total = s_required + s_provisional + s_components + s_ux + s_layout

    return {
        "total": total,
        "breakdown": {
            "required_blocks": s_required,
            "no_provisional_fields": s_provisional,
            "component_inventory": s_components,
            "ux_writing_slots": s_ux,
            "layout_block": s_layout,
        },
        "missing_blocks": missing_blocks,
        "provisional_fields": provisional_list,
    }


def unlock_status(score: int) -> tuple[str, str]:
    """Return (unlock_level, message) for a given completeness score."""
    if score >= 90:
        return "FULL", "Mode A, B, C fully unlocked."
    elif score >= 70:
        return "PARTIAL_A", "Mode A with documented approximations. Modes B and C unlocked."
    elif score >= 50:
        return "MODE_B", "Significant gaps. Mode B recommended. Mode A requires explicit override."
    else:
        return "HARD_STOP", "Hard stop: completeness too low for any mode. Re-run ui-studio-onboard."


def main():
    parser = argparse.ArgumentParser(description="UI Studio — Brand Config Validator")
    parser.add_argument("--config", "-c", type=str, default=str(DEFAULT_CONFIG),
                        help="Path to the config file to validate")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Show detailed breakdown per scoring category")
    parser.add_argument("--update", action="store_true",
                        help="Write the computed completeness_score back to the config file")
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = SCRIPT_DIR.parent / args.config

    if not config_path.exists():
        print(f"Error: Config not found: {config_path}")
        sys.exit(1)

    with open(config_path, "r") as f:
        config = json.load(f)

    brand_name = config.get("brand", {}).get("name", "Unknown")
    version = config.get("meta", {}).get("version", "unknown")
    last_refreshed = config.get("meta", {}).get("last_refreshed", "unknown")

    print(f"\n{'='*60}")
    print("  UI Studio — Config Validator")
    print(f"  Brand: {brand_name} (v{version})")
    print(f"  Config: {config_path.name}")
    print(f"  Last refreshed: {last_refreshed}")
    print(f"{'='*60}\n")

    if args.verbose:
        print("Scoring:\n")

    result = compute_completeness_score(config, verbose=args.verbose)
    score = result["total"]
    unlock_level, unlock_msg = unlock_status(score)

    print(f"\n  Completeness score: {score}/100")
    print("  Breakdown:")
    for k, v in result["breakdown"].items():
        print(f"    {k}: {v}")

    print(f"\n  Unlock status: {unlock_level}")
    print(f"  {unlock_msg}")

    if result["provisional_fields"]:
        print(f"\n  Provisional fields ({len(result['provisional_fields'])}):")
        for f in result["provisional_fields"][:10]:
            print(f"    - {f}")
        if len(result["provisional_fields"]) > 10:
            print(f"    ... and {len(result['provisional_fields'])-10} more")

    if result["missing_blocks"]:
        print("\n  Missing required blocks:")
        for b in result["missing_blocks"]:
            print(f"    - {b}")

    if args.update:
        config.setdefault("meta", {})["completeness_score"] = score
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"\n  ✓ completeness_score updated to {score} in {config_path.name}")

    print(f"\n{'='*60}\n")

    # Exit code signals unlock status to callers
    if unlock_level == "HARD_STOP":
        sys.exit(2)
    elif unlock_level == "MODE_B":
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
