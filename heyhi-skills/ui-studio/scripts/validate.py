#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI Studio — Brand Config Validator

Computes completeness_score and fidelity_score for active-brand.json and reports
provisional fields, missing sections, gate status, provenance freshness, and mode
unlock status.

Completeness algorithm (deterministic, per build plan):
  Required blocks present and non-empty    40 pts  (5 pts × 8 blocks)
  No provisional fields                    20 pts  (proportionally deducted)
  Component inventory populated            15 pts
  UX writing slots populated               15 pts  (~1.875 pts × 8 slots)
  Layout block with named patterns         10 pts

Fidelity algorithm (G5 — added 2026-03-25):
  Token provenance: % tokens with confidence extracted or designer_review_complete  50 pts
  Gate status: direction_lock_confirmed + designer_review_complete                  30 pts
  Freshness: no field_provenance entries older than FRESHNESS_DAYS days             20 pts

Mode unlock matrix (SI-03/LF-02 update — 2026-03-26):
  completeness < 30                        →  HARD_STOP (all modes blocked — insufficient data)
  completeness 30–49                       →  PARTIAL_STOP (Mode B/C allowed; Mode A blocked)
  completeness 50–69                       →  MODE_B (Mode A requires SI-03 explicit override)
  completeness ≥ 70  AND  fidelity ≥ 60   →  PARTIAL_A or FULL (Mode A enabled)
  completeness ≥ 90  AND  fidelity ≥ 80   →  Version promotion (--promote)
  fidelity < 40 at any completeness level  →  Fidelity warning surfaced in all modes

Gate status (G2 — added 2026-03-25):
  direction_lock_confirmed: false  →  Hard stop for Mode A builds
  designer_review_complete: false  →  Warning for Mode A builds; hard stop for --promote

Version promotion (G1 — added 2026-03-25):
  --promote: bumps 0.x.y → 1.0.0 when all gates pass and writes meta.promoted_at

Staleness note (fidelity_score):
  fidelity_score is computed dynamically at runtime from field_provenance and gate_status.
  If a stored fidelity_score field exists in the config JSON, treat it as a snapshot from
  the last validate.py run — not an authoritative current value. Always run validate.py to
  get the current score before making promotion or mode-unlock decisions. The --update flag
  writes the freshly computed score back to the config to keep the stored value current.
  Without --update, the stored score may be stale if field_provenance has changed.

Usage:
  python3 scripts/validate.py [--config PATH] [--verbose] [--update] [--status] [--promote]
  python3 scripts/validate.py --config brand-config/active-brand.json
  python3 scripts/validate.py --config brand-config/example.json --verbose
  python3 scripts/validate.py --config brand-config/example.json --status
  python3 scripts/validate.py --config brand-config/example.json --promote
"""

import argparse
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DEFAULT_CONFIG = SCRIPT_DIR.parent / "brand-config" / "active-brand.json"

# DTCG-native authoring shim (W5 / audit G7): resolve token leaves whether authored
# as a bare scalar or a DTCG object, so provisional detection walks token values
# (not their $type/$description companions).
sys.path.insert(0, str(SCRIPT_DIR))
from tokens import resolve_token_value, is_token_group  # noqa: E402

# Freshness threshold: field_provenance entries with last_verified_at older than this
# are surfaced as staleness warnings. Configurable via --freshness-days flag.
DEFAULT_FRESHNESS_DAYS = 90

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

# Keys present in every ux_writing slot for traceability — not content indicators.
_SLOT_META_KEYS = {"source", "source_url", "last_verified"}

# Confidence levels that are considered fidelity-positive for token scoring
FIDELITY_POSITIVE_CONFIDENCE = {"extracted"}


def _slot_is_populated(slot_data: dict) -> bool:
    """Return True if a ux_writing slot has any meaningful content."""
    if not slot_data:
        return False
    for k, v in slot_data.items():
        if k in _SLOT_META_KEYS:
            continue
        if isinstance(v, str) and v:
            return True
        if isinstance(v, list) and v:
            return True
    return False


def has_provisional_values(config: dict) -> list[str]:
    """Walk the config and find all paths containing PROVISIONAL: prefix."""
    provisional_paths = []

    def walk(obj, path=""):
        # A DTCG token object resolves to its $value here (checked at the token's own
        # path); a bare scalar resolves to itself; a nested group resolves to None and
        # is recursed. This keeps a DTCG-native config's provisional detection clean
        # (path is the token, not token.$value) and never descends into $type/$description.
        resolved = resolve_token_value(obj)
        if isinstance(resolved, str) and resolved.startswith(PROVISIONAL_PREFIX):
            provisional_paths.append(path)
            return
        if is_token_group(obj):
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
    """Score provisional field penalty: 20 pts max, deducted proportionally.

    G4: Confidence-weighted deductions. inferred = 2 pts each; provisional/failing = 4 pts each.
    When field_provenance is present, confidence levels are read from provenance entries.
    Falls back to PROVISIONAL: string prefix detection when provenance is absent.
    """
    # Collect from meta.provisional_fields array (legacy format)
    declared = [f.get("path", "") for f in config.get("meta", {}).get("provisional_fields", [])]

    # Detect any PROVISIONAL: prefixed values in the wild (legacy format)
    detected = ["tokens." + p for p in has_provisional_values(config.get("tokens", {}))]
    legacy_provisional = list(set(declared + detected))

    # Read confidence levels from field_provenance (G4 graduated confidence)
    field_provenance = config.get("meta", {}).get("field_provenance", {})
    provenance_deduction = 0
    provenance_paths = []
    for path, prov in field_provenance.items():
        confidence = prov.get("confidence", "inferred")
        if confidence == "inferred":
            provenance_deduction += 2
            provenance_paths.append(f"{path}[inferred]")
        elif confidence in ("provisional", "failing"):
            provenance_deduction += 4
            provenance_paths.append(f"{path}[{confidence}]")
        # extracted = no deduction

    if field_provenance:
        # Use provenance-based scoring when provenance is present
        deduction = min(20, provenance_deduction)
        score = max(0, 20 - deduction)
        all_non_extracted = provenance_paths
    else:
        # Fall back to legacy count-based scoring
        all_non_extracted = legacy_provisional
        if not all_non_extracted:
            return 20, []
        deduction = min(20, len(all_non_extracted) * 4)
        score = max(0, 20 - deduction)

    if verbose and all_non_extracted:
        print(f"  Non-extracted fields ({len(all_non_extracted)}): "
              + ", ".join(all_non_extracted[:5])
              + (f"... +{len(all_non_extracted)-5} more" if len(all_non_extracted) > 5 else ""))

    return score, all_non_extracted


def score_component_inventory(config: dict, verbose: bool = False) -> int:
    """Score component inventory: 15 pts if ≥1 entry + drift checked, 7 if present but drift unchecked."""
    inventory = config.get("components", {}).get("inventory", [])
    drift = config.get("components", {}).get("drift", {})

    if not inventory:
        if verbose:
            print("  Component inventory: empty (0 pts)")
        return 0

    drift_checked = any([
        len(drift.get("token_drift", [])) > 0,
        len(drift.get("pattern_drift", [])) > 0,
        len(drift.get("api_drift", [])) > 0,
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

    pts_per_slot = 15 / len(UX_WRITING_SLOTS)
    score = 0
    populated = []
    missing = []

    for slot in UX_WRITING_SLOTS:
        slot_data = ux.get(slot, {})
        if _slot_is_populated(slot_data):
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


# ─────────────────────────────────────────────────────────────────────────────
# G5: Fidelity Score (added 2026-03-25)
# ─────────────────────────────────────────────────────────────────────────────

def compute_fidelity_score(config: dict, freshness_days: int = DEFAULT_FRESHNESS_DAYS,
                            verbose: bool = False) -> dict:
    """Compute fidelity score: how much of the config has been confirmed against its source.

    Fidelity is distinct from completeness. Completeness = is it populated?
    Fidelity = is what's populated actually correct and confirmed?

    Components (100 pts total):
      Token provenance (50 pts): % of field_provenance entries with confidence=extracted
                                  OR gate_status.designer_review_complete=true
      Gate status (30 pts):      direction_lock_confirmed (15) + designer_review_complete (15)
      Freshness (20 pts):        No field_provenance entries with last_verified_at > freshness_days ago

    Returns a dict with total, breakdown, stale_fields, and warning messages.
    """
    meta = config.get("meta", {})
    gate_status = meta.get("gate_status", {})
    field_provenance = meta.get("field_provenance", {})

    # ── Gate status score (30 pts) ──────────────────────────────────────────
    direction_lock = bool(gate_status.get("direction_lock_confirmed", False))
    designer_review = bool(gate_status.get("designer_review_complete", False))
    s_gate = (15 if direction_lock else 0) + (15 if designer_review else 0)

    if verbose:
        print(f"  Fidelity — Gate status:")
        print(f"    direction_lock_confirmed: {'✓' if direction_lock else '✗'} ({15 if direction_lock else 0} pts)")
        print(f"    designer_review_complete: {'✓' if designer_review else '✗'} ({15 if designer_review else 0} pts)")

    # ── Token provenance score (50 pts) ────────────────────────────────────
    if not field_provenance:
        # No provenance at all — score 0 unless designer_review_complete is true
        # (which means a designer reviewed the whole config at once)
        if designer_review:
            s_provenance = 50
            if verbose:
                print(f"  Fidelity — Token provenance: designer_review_complete=true, no per-field provenance (50 pts via gate)")
        else:
            s_provenance = 0
            if verbose:
                print(f"  Fidelity — Token provenance: no field_provenance and no designer review (0 pts)")
    else:
        total_fields = len(field_provenance)
        confirmed_fields = sum(
            1 for prov in field_provenance.values()
            if prov.get("confidence") in FIDELITY_POSITIVE_CONFIDENCE or designer_review
        )
        ratio = confirmed_fields / total_fields if total_fields > 0 else 0
        s_provenance = round(50 * ratio)
        if verbose:
            print(f"  Fidelity — Token provenance: {confirmed_fields}/{total_fields} fields extracted/confirmed "
                  f"({s_provenance} pts)")

    # ── Freshness score (20 pts) ────────────────────────────────────────────
    today = date.today()
    stale_fields = []
    if field_provenance:
        for path, prov in field_provenance.items():
            last_verified = prov.get("last_verified_at")
            if last_verified:
                try:
                    verified_date = date.fromisoformat(last_verified)
                    age_days = (today - verified_date).days
                    if age_days > freshness_days:
                        stale_fields.append((path, age_days))
                except ValueError:
                    pass  # Malformed date — skip silently
            # null last_verified_at is not a staleness error (field was never verified,
            # which is already penalized in the provenance score)

    if stale_fields:
        s_freshness = 0
        if verbose:
            print(f"  Fidelity — Freshness: {len(stale_fields)} stale field(s) (>{freshness_days} days, 0 pts)")
            for path, age in stale_fields[:5]:
                print(f"    - {path} ({age} days old)")
    elif not field_provenance:
        s_freshness = 0
        if verbose:
            print(f"  Fidelity — Freshness: no provenance data (0 pts)")
    else:
        s_freshness = 20
        if verbose:
            print(f"  Fidelity — Freshness: all verified within {freshness_days} days (20 pts)")

    total = s_gate + s_provenance + s_freshness

    return {
        "total": total,
        "breakdown": {
            "gate_status": s_gate,
            "token_provenance": s_provenance,
            "freshness": s_freshness,
        },
        "stale_fields": stale_fields,
        "direction_lock_confirmed": direction_lock,
        "designer_review_complete": designer_review,
    }


# ─────────────────────────────────────────────────────────────────────────────
# G2: Gate status checks (added 2026-03-25)
# ─────────────────────────────────────────────────────────────────────────────

def check_gate_status(config: dict) -> dict:
    """Return gate status flags and any blocking conditions.

    Returns a dict with:
      - hard_stop: True if a gate condition blocks Mode A entirely
      - hard_stop_reason: human-readable explanation
      - warnings: list of non-blocking warnings to surface to the operator
      - gate_status: the raw gate_status dict from the config (or empty dict)
    """
    gate_status = config.get("meta", {}).get("gate_status", {})
    hard_stop = False
    hard_stop_reason = None
    warnings = []

    if not gate_status:
        # Config pre-dates G2 — no gate_status block at all. Surface as warning, not hard stop,
        # to preserve backward compatibility with configs generated before 2026-03-25.
        warnings.append(
            "gate_status block absent — this config was generated before G2 was implemented. "
            "Run ui-studio-onboard to refresh and add gate confirmations."
        )
        return {
            "hard_stop": False,
            "hard_stop_reason": None,
            "warnings": warnings,
            "gate_status": {},
        }

    direction_lock = bool(gate_status.get("direction_lock_confirmed", False))
    designer_review = bool(gate_status.get("designer_review_complete", False))
    mode_override = bool(gate_status.get("mode_override_acknowledged", False))
    mode_override_score = gate_status.get("mode_override_score")

    if not direction_lock:
        hard_stop = True
        hard_stop_reason = (
            "Gate 0 not confirmed: gate_status.direction_lock_confirmed is false. "
            "The style cluster, temperature, and primary direction must be locked before a "
            "Mode A build can proceed. Run ui-studio-onboard Gate 0 to confirm direction, "
            "then set gate_status.direction_lock_confirmed: true and gate_status.direction_lock_date."
        )

    if not designer_review:
        warnings.append(
            "Designer review not complete (gate_status.designer_review_complete: false). "
            "Token values have not been verified against the source design file. "
            "Mode A output may not match the actual design. Complete a designer review "
            "and set gate_status.designer_review_complete: true before client delivery."
        )

    if mode_override and mode_override_score is not None and mode_override_score < 30:
        # This shouldn't normally happen — a score < 30 is an unconditional hard stop;
        # mode_override only applies to the 50–69 MODE_B range. Guard against corrupt state.
        warnings.append(
            f"mode_override_acknowledged is true but recorded score ({mode_override_score}) "
            f"is below the unconditional hard-stop threshold (< 30). Override is invalid. Re-run validation."
        )

    return {
        "hard_stop": hard_stop,
        "hard_stop_reason": hard_stop_reason,
        "warnings": warnings,
        "gate_status": gate_status,
    }


# ─────────────────────────────────────────────────────────────────────────────
# G1: Version promotion (added 2026-03-25)
# ─────────────────────────────────────────────────────────────────────────────

def attempt_promotion(config: dict, config_path: Path,
                      completeness: int, fidelity: int) -> tuple[bool, str]:
    """Attempt version promotion from 0.x.y to 1.0.0.

    Gate conditions (all must pass):
      1. completeness_score ≥ 90
      2. meta.provisional_fields is empty (no declared provisionals)
      3. gate_status.direction_lock_confirmed is true (G2)
      4. gate_status.designer_review_complete is true (G2)
      5. fidelity_score ≥ 80 (G5)

    If all pass: bumps version to 1.0.0 and writes meta.promoted_at.
    Returns (success: bool, message: str).
    """
    meta = config.get("meta", {})
    current_version = meta.get("version", "0.1.0")
    gate_status = meta.get("gate_status", {})

    if not current_version.startswith("0."):
        return False, f"Config is already at version {current_version} (not provisional). No promotion needed."

    failures = []

    if completeness < 90:
        failures.append(f"completeness_score is {completeness}/100 (need ≥ 90)")

    provisional_fields = meta.get("provisional_fields", [])
    # Also check for any PROVISIONAL: prefix values in the wild (legacy format)
    detected_provisional = has_provisional_values(config.get("tokens", {}))
    if provisional_fields or detected_provisional:
        count = len(provisional_fields) + len(detected_provisional)
        failures.append(
            f"meta.provisional_fields is not empty ({count} provisional field(s) remain). "
            "All provisional values must be replaced with confirmed values before promotion."
        )

    if not gate_status:
        failures.append(
            "gate_status block absent — cannot verify gate confirmations. "
            "Run ui-studio-onboard to add gate_status."
        )
    else:
        if not gate_status.get("direction_lock_confirmed", False):
            failures.append("gate_status.direction_lock_confirmed is false")
        if not gate_status.get("designer_review_complete", False):
            failures.append("gate_status.designer_review_complete is false")

    if fidelity < 80:
        failures.append(f"fidelity_score is {fidelity}/100 (need ≥ 80)")

    if failures:
        msg = "Promotion blocked. The following gates did not pass:\n"
        for f in failures:
            msg += f"  ✗ {f}\n"
        return False, msg

    # All gates passed — promote
    config["meta"]["version"] = "1.0.0"
    config["meta"]["promoted_at"] = datetime.now(timezone.utc).isoformat()

    with open(config_path, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    return True, (
        f"✓ Promoted to v1.0.0. All gates passed:\n"
        f"  ✓ completeness_score: {completeness}/100\n"
        f"  ✓ no provisional fields\n"
        f"  ✓ direction_lock_confirmed: true (locked {gate_status.get('direction_lock_date', 'date unknown')})\n"
        f"  ✓ designer_review_complete: true (reviewed {gate_status.get('designer_review_date', 'date unknown')} "
        f"by {gate_status.get('designer_reviewer', 'unknown')})\n"
        f"  ✓ fidelity_score: {fidelity}/100\n"
        f"meta.promoted_at written. Config is now production-ready."
    )


# ─────────────────────────────────────────────────────────────────────────────
# Unlock status
# ─────────────────────────────────────────────────────────────────────────────

def unlock_status(completeness: int, fidelity: int, gate_result: dict) -> tuple[str, str]:
    """Return (unlock_level, message) given completeness, fidelity, and gate status.

    G5 update: Mode A now requires completeness ≥ 70 AND fidelity ≥ 60.
    G2 update: Gate 0 (direction_lock_confirmed) is a hard stop for Mode A.
    SI-03/LF-02 update (2026-03-26): Replaced single < 50 hard stop with two thresholds:
      - < 30: HARD_STOP — insufficient data for any meaningful build.
      - 30–49: PARTIAL_STOP — Mode B/C allowed with capability-degradation notice; Mode A blocked.
    """
    # Gate hard stop takes precedence over all score-based checks
    if gate_result.get("hard_stop"):
        return "GATE_STOP", f"Gate hard stop: {gate_result['hard_stop_reason']}"

    if completeness < 30:
        return "HARD_STOP", (
            "Hard stop: completeness too low for any mode. "
            "Insufficient data for a meaningful build. Re-run ui-studio-onboard."
        )

    if completeness < 50:
        return "PARTIAL_STOP", (
            "Config is partially populated. Mode A blocked. "
            "Mode B and C may proceed — open with a capability-degradation notice "
            "listing which config blocks are missing and which capabilities are unavailable."
        )

    if completeness >= 70 and fidelity >= 60:
        if completeness >= 90:
            return "FULL", "Mode A, B, C fully unlocked."
        return "PARTIAL_A", "Mode A with documented approximations. Modes B and C unlocked."
    elif completeness >= 70 and fidelity < 60:
        return "FIDELITY_WARN", (
            f"Completeness passes (≥70) but fidelity is low ({fidelity}/100 — need ≥60 for Mode A). "
            "Token values have not been sufficiently confirmed. Run a designer review "
            "or complete per-field provenance before Mode A builds."
        )
    else:
        return "MODE_B", "Significant gaps. Mode B recommended. Mode A requires explicit override (SI-03 gate)."


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="UI Studio — Brand Config Validator")
    parser.add_argument("--config", "-c", type=str, default=str(DEFAULT_CONFIG),
                        help="Path to the config file to validate")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Show detailed breakdown per scoring category")
    parser.add_argument("--update", action="store_true",
                        help="Write the computed scores back to the config file")
    parser.add_argument("--status", action="store_true",
                        help="Full status output: scores, gate status, provenance freshness, stale fields")
    parser.add_argument("--promote", action="store_true",
                        help="Attempt version promotion from 0.x.y to 1.0.0 (all gates must pass)")
    parser.add_argument("--freshness-days", type=int, default=DEFAULT_FRESHNESS_DAYS,
                        help=f"Days before a provenance entry is considered stale (default: {DEFAULT_FRESHNESS_DAYS})")
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
    print(f"  UI Studio — Config Validator")
    print(f"  Brand: {brand_name} (v{version})")
    print(f"  Config: {config_path.name}")
    print(f"  Last refreshed: {last_refreshed}")
    print(f"{'='*60}\n")

    if args.verbose:
        print("Completeness scoring:\n")

    completeness_result = compute_completeness_score(config, verbose=args.verbose)
    completeness = completeness_result["total"]

    fidelity_result = compute_fidelity_score(
        config, freshness_days=args.freshness_days, verbose=args.verbose
    )
    fidelity = fidelity_result["total"]

    gate_result = check_gate_status(config)

    unlock_level, unlock_msg = unlock_status(completeness, fidelity, gate_result)

    # ── Completeness output ─────────────────────────────────────────────────
    print(f"  Completeness score: {completeness}/100")
    print(f"  Breakdown:")
    for k, v in completeness_result["breakdown"].items():
        print(f"    {k}: {v}")

    # ── Fidelity output ─────────────────────────────────────────────────────
    print(f"\n  Fidelity score: {fidelity}/100")
    print(f"  Breakdown:")
    for k, v in fidelity_result["breakdown"].items():
        print(f"    {k}: {v}")

    if fidelity < 40:
        print(f"\n  ⚠  LOW FIDELITY ({fidelity}/100): Token values are largely unconfirmed.")
        print(f"     Complete a designer review or add per-field provenance before client delivery.")

    # ── Gate status output ──────────────────────────────────────────────────
    print(f"\n  Gate status:")
    gs = gate_result.get("gate_status", {})
    if gs:
        print(f"    direction_lock_confirmed: {'✓ true' if gs.get('direction_lock_confirmed') else '✗ false'}"
              + (f" ({gs.get('direction_lock_date')})" if gs.get('direction_lock_date') else ""))
        print(f"    designer_review_complete: {'✓ true' if gs.get('designer_review_complete') else '✗ false'}"
              + (f" ({gs.get('designer_reviewer')})" if gs.get('designer_reviewer') else ""))
        print(f"    mode_override_acknowledged: {'true' if gs.get('mode_override_acknowledged') else 'false'}")
    else:
        print(f"    (no gate_status block — pre-G2 config)")

    if gate_result.get("warnings"):
        print(f"\n  Gate warnings:")
        for w in gate_result["warnings"]:
            print(f"    ⚠  {w}")

    # ── Unlock status output ────────────────────────────────────────────────
    print(f"\n  Unlock status: {unlock_level}")
    print(f"  {unlock_msg}")

    # ── Gate hard stop output ───────────────────────────────────────────────
    if gate_result.get("hard_stop"):
        print(f"\n  ✗ GATE HARD STOP — Mode A builds blocked.")
        print(f"    {gate_result['hard_stop_reason']}")

    # ── Provisional fields ──────────────────────────────────────────────────
    if completeness_result["provisional_fields"]:
        print(f"\n  Provisional/non-extracted fields ({len(completeness_result['provisional_fields'])}):")
        for f in completeness_result["provisional_fields"][:10]:
            print(f"    - {f}")
        if len(completeness_result["provisional_fields"]) > 10:
            print(f"    ... and {len(completeness_result['provisional_fields'])-10} more")

    if completeness_result["missing_blocks"]:
        print(f"\n  Missing required blocks:")
        for b in completeness_result["missing_blocks"]:
            print(f"    - {b}")

    # ── Stale fields (--status or --verbose) ───────────────────────────────
    if (args.status or args.verbose) and fidelity_result.get("stale_fields"):
        print(f"\n  Stale provenance entries (>{args.freshness_days} days since last_verified_at):")
        for path, age in fidelity_result["stale_fields"][:10]:
            print(f"    - {path} ({age} days)")
        if len(fidelity_result["stale_fields"]) > 10:
            print(f"    ... and {len(fidelity_result['stale_fields'])-10} more")

    # ── --update: write scores back to config ──────────────────────────────
    if args.update:
        config.setdefault("meta", {})["completeness_score"] = completeness
        config["meta"]["fidelity_score"] = fidelity
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"\n  ✓ completeness_score ({completeness}) and fidelity_score ({fidelity}) "
              f"written to {config_path.name}")

    # ── --promote: attempt version promotion ───────────────────────────────
    if args.promote:
        print(f"\n  {'─'*50}")
        print(f"  Promotion attempt: {version} → 1.0.0")
        print(f"  {'─'*50}")
        success, msg = attempt_promotion(config, config_path, completeness, fidelity)
        print(f"\n  {'✓ PROMOTED' if success else '✗ BLOCKED'}")
        print(f"  {msg}")

    print(f"\n{'='*60}\n")

    # Exit codes signal unlock status to callers
    if gate_result.get("hard_stop"):
        sys.exit(3)  # Gate hard stop
    elif unlock_level == "HARD_STOP":
        sys.exit(2)
    elif unlock_level in ("MODE_B", "FIDELITY_WARN"):
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
