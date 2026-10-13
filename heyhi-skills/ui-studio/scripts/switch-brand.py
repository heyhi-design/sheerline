#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI Studio — Brand Config Switcher

Activates a named brand config by copying it to active-brand.json,
then regenerates .cursor/rules/ui-studio.mdc.

Named configs live in brand-config/. active-brand.json is what ui-studio reads.
This script is the only mechanism for switching configs — do not manually copy.

Usage:
  python3 scripts/switch-brand.py --config acme
  python3 scripts/switch-brand.py --config acme-corp
  python3 scripts/switch-brand.py --list
  python3 scripts/switch-brand.py --status

  # Write generated Cursor rule to a project root instead of the skill directory:
  python3 scripts/switch-brand.py --config acme --cursor-project /path/to/project

  # Switch without regenerating Cursor rules (regenerate manually after):
  python3 scripts/switch-brand.py --config acme --no-cursor
"""

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone

SCRIPT_DIR = Path(__file__).parent
SKILL_ROOT = SCRIPT_DIR.parent
CONFIG_DIR = SKILL_ROOT / "brand-config"
ACTIVE_CONFIG = CONFIG_DIR / "active-brand.json"
CURSOR_EXPORT_SCRIPT = SCRIPT_DIR / "cursor-export.py"


def list_available_configs() -> list[Path]:
    """Return all named configs in brand-config/, excluding schema and example files."""
    exclude = {"active-brand.json", "schema.json", "example.json"}
    return sorted([
        p for p in CONFIG_DIR.glob("*.json")
        if p.name not in exclude
    ])


def get_config_summary(config_path: Path) -> dict:
    """Load a config and return key summary fields."""
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        return {
            "name": config.get("brand", {}).get("name", "Unknown"),
            "version": config.get("meta", {}).get("version", "unknown"),
            "completeness": config.get("meta", {}).get("completeness_score", "not computed"),
            "last_refreshed": config.get("meta", {}).get("last_refreshed", "never"),
        }
    except (json.JSONDecodeError, IOError):
        return {"name": "Error reading config", "version": "?", "completeness": "?", "last_refreshed": "?"}


def main():
    parser = argparse.ArgumentParser(description="UI Studio — Brand Config Switcher")
    parser.add_argument("--config", "-c", type=str,
                        help="Config name to activate (without .json extension). E.g., 'acme' for acme.json.")
    parser.add_argument("--list", "-l", action="store_true",
                        help="List all available named configs")
    parser.add_argument("--status", "-s", action="store_true",
                        help="Show the currently active config")
    parser.add_argument("--no-cursor", action="store_true",
                        help="Skip regenerating .cursor/rules/ui-studio.mdc after switching")
    parser.add_argument("--cursor-project", type=str, default=None,
                        help="Path to the project root where .cursor/rules/ui-studio.mdc should be written. "
                             "When set, the generated rule is written to [cursor-project]/.cursor/rules/ "
                             "instead of inside the skill directory. Use this when working in Cursor IDE.")
    args = parser.parse_args()

    print(f"\n{'='*60}")
    print(f"  UI Studio — Brand Config Switcher")
    print(f"{'='*60}\n")

    if args.status:
        if ACTIVE_CONFIG.exists():
            summary = get_config_summary(ACTIVE_CONFIG)
            print(f"  Active config: {summary['name']}")
            print(f"  Version: {summary['version']}")
            print(f"  Completeness: {summary['completeness']}/100")
            print(f"  Last refreshed: {summary['last_refreshed']}")
        else:
            print("  No active config. Run ui-studio-onboard or switch-brand.py --config [name].")
        print(f"\n{'='*60}\n")
        return

    if args.list:
        configs = list_available_configs()
        if not configs:
            print("  No named configs found in brand-config/.")
            print("  Run ui-studio-onboard to create one.")
        else:
            print("  Available configs:\n")
            for config_path in configs:
                summary = get_config_summary(config_path)
                active_marker = " ← ACTIVE" if ACTIVE_CONFIG.exists() and _is_same_config(config_path) else ""
                print(f"  {config_path.stem}")
                print(f"    Brand:  {summary['name']}")
                print(f"    v{summary['version']} · completeness: {summary['completeness']}/100{active_marker}")
                print()
        print(f"{'='*60}\n")
        return

    if not args.config:
        parser.print_help()
        print(f"\n{'='*60}\n")
        sys.exit(1)

    # Resolve the named config
    config_name = args.config.removesuffix(".json")
    source_path = CONFIG_DIR / f"{config_name}.json"

    if not source_path.exists():
        available = [p.stem for p in list_available_configs()]
        print(f"  Error: Config '{config_name}.json' not found in brand-config/.")
        if available:
            print(f"  Available: {', '.join(available)}")
        else:
            print("  No named configs available. Run ui-studio-onboard to create one.")
        print(f"\n{'='*60}\n")
        sys.exit(1)

    # Load and display summary before switching
    summary = get_config_summary(source_path)
    print(f"  Activating: {source_path.name}")
    print(f"  Brand: {summary['name']}")
    print(f"  Version: {summary['version']}")
    print(f"  Completeness: {summary['completeness']}/100")

    # Check for provisional warning
    if str(summary["version"]).startswith("0."):
        print(f"\n  ⚠  PROVISIONAL CONFIG (v{summary['version']})")
        print("     Token values are directional estimates pending designer confirmation.")
        print("     Mode A builds will be marked provisional.")
        print("     Run `ui-studio-onboard --refresh " + config_name + "` after designer confirms values.")

    # Perform the copy
    shutil.copy2(source_path, ACTIVE_CONFIG)
    print(f"\n  ✓ Copied {source_path.name} → active-brand.json")

    # Regenerate Cursor rules
    if not args.no_cursor and CURSOR_EXPORT_SCRIPT.exists():
        # Determine output path: project root (--cursor-project) or skill directory (default)
        if args.cursor_project:
            cursor_output = Path(args.cursor_project).resolve() / ".cursor" / "rules" / "ui-studio.mdc"
            print(f"  Regenerating .cursor/rules/ui-studio.mdc → {cursor_output.parent} ...")
        else:
            cursor_output = SKILL_ROOT / ".cursor" / "rules" / "ui-studio.mdc"
            print("  Regenerating .cursor/rules/ui-studio.mdc...")

        result = subprocess.run(
            [sys.executable, str(CURSOR_EXPORT_SCRIPT),
             "--config", str(ACTIVE_CONFIG),
             "--output", str(cursor_output)],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print("  ✓ Cursor rules regenerated")
        else:
            print(f"  ⚠  Cursor rules generation failed: {result.stderr.strip()}")
    elif args.no_cursor:
        print("  Cursor rules regeneration skipped (--no-cursor)")
    else:
        print("  ⚠  cursor-export.py not found — Cursor rules not regenerated")

    print(f"\n  Active config is now: {summary['name']} v{summary['version']}")
    print(f"\n{'='*60}\n")


def _config_hash(config_path: Path) -> str:
    """Return an MD5 hash of the config file contents for identity comparison.

    DE-03: Using a content hash instead of name+version comparison prevents false
    positives when two configs share a name or when a config is edited in-place
    without bumping the version string.
    """
    with open(config_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def _is_same_config(named_config: Path) -> bool:
    """Check if a named config is the currently active one (by content hash, not name+version).

    DE-03: Content hash comparison is reliable where name+version was not:
    - Two different clients could share the same brand.name value during early development
    - A config edited in-place (version not bumped) would falsely match its prior state
    A content hash catches both cases.
    """
    if not ACTIVE_CONFIG.exists():
        return False
    try:
        return _config_hash(named_config) == _config_hash(ACTIVE_CONFIG)
    except IOError:
        return False


if __name__ == "__main__":
    main()
