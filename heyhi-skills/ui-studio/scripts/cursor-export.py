#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI Studio — Cursor Rules Exporter

Generates .cursor/rules/ui-studio.mdc from SKILL.md + active-brand.json values.
The .mdc file is the Cursor companion for ui-studio. It is separate from SKILL.md.

This script does NOT rely on create_design_system_rules (Figma MCP tool).
That tool provides supplementary context; this script writes the actual .mdc file.

Usage:
  python3 scripts/cursor-export.py [--config PATH] [--output PATH] [--cursor-project PATH]
  python3 scripts/cursor-export.py
  python3 scripts/cursor-export.py --config brand-config/acme.json --output .cursor/rules/ui-studio.mdc

  # Recommended: use --cursor-project to write directly to a project root (run from project root):
  python3 ui-studio/scripts/cursor-export.py --cursor-project .

  # Equivalent longhand (relative output resolves from cwd):
  python3 ui-studio/scripts/cursor-export.py --output .cursor/rules/ui-studio.mdc

  # Cross-tool: Cowork plugin config → Cursor project (--config accepts any path):
  python3 ui-studio/scripts/cursor-export.py \
    --config /path/to/plugin/active-brand.json \
    --cursor-project /path/to/project
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

# DTCG-native authoring shim (W5 / audit G7): resolve token leaves whether authored
# as a bare scalar (legacy) or a DTCG object ({"$value": ...}). Import-safe from the
# sibling scripts dir regardless of cwd.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from tokens import resolve_token_value, is_token_group  # noqa: E402

SCRIPT_DIR = Path(__file__).parent
SKILL_ROOT = SCRIPT_DIR.parent
DEFAULT_CONFIG = SKILL_ROOT / "brand-config" / "active-brand.json"
DEFAULT_OUTPUT = SKILL_ROOT / ".cursor" / "rules" / "ui-studio.mdc"


def load_config(config_path: Path) -> dict:
    if not config_path.exists():
        print(f"Error: Config not found: {config_path}")
        sys.exit(1)
    with open(config_path, "r") as f:
        return json.load(f)


def extract_font_stack(family_obj: dict) -> str:
    family = resolve_token_value(family_obj.get("family")) or ""
    fallback = resolve_token_value(family_obj.get("fallback")) or "system-ui, sans-serif"
    return f'"{family}", {fallback}' if family else fallback


def build_prov_comment(css_prop: str, full_path: str, provenance: dict) -> str:
    """Return a CSS comment line from provenance description/usage_notes, or empty string.

    G6: Used by all extract_* functions to annotate CSS custom properties with
    engineer-readable context from meta.field_provenance[path].description and .usage_notes.
    Returns empty string (not None) so callers can unconditionally concatenate.
    """
    prov = provenance.get(full_path, {})
    parts = []
    if prov.get("description"):
        parts.append(prov["description"])
    if prov.get("usage_notes"):
        parts.append(prov["usage_notes"])
    if parts:
        return f"  /* {css_prop}: {' '.join(parts)} */"
    return ""


def build_font_families_css(
    display_stack: str,
    body_stack: str,
    utility_stack: str,
    field_provenance: dict,
) -> str:
    """Build the Typography families CSS block with G6 provenance comments.

    Emits description and usage_notes from field_provenance before each
    --font-* custom property, so engineers know when and how to use each family.
    """
    lines = []
    pairs = [
        ("--font-display", "tokens.typography.families.display.family", display_stack),
        ("--font-body",    "tokens.typography.families.body.family",    body_stack),
        ("--font-utility", "tokens.typography.families.utility.family", utility_stack),
    ]
    for css_prop, full_path, stack in pairs:
        comment = build_prov_comment(css_prop, full_path, field_provenance)
        if comment:
            lines.append(comment)
        lines.append(f"  {css_prop}: {stack};")
    return "\n".join(lines)


def extract_colors(color_obj: dict, field_provenance: dict = None) -> str:
    """Recursively extract color tokens to CSS custom properties at any nesting depth.

    Original implementation only handled two levels (category.name). Colors nested
    deeper (e.g. semantic.alarm.high_priority) were silently dropped. Fixed DE-01.

    G3/G4 (added 2026-03-25): Reads field_provenance for each token path and:
    - Filters out confidence=failing and confidence=provisional values (do not emit to CSS)
    - Annotates inferred values with a CSS comment showing confidence and last_verified_at
    - Emits extracted values with optional description/usage_notes comments from provenance
    Falls back to PROVISIONAL: string prefix filtering when no provenance is present.
    """
    lines = []
    provenance = field_provenance or {}

    def recurse(obj: dict, prefix: str, token_path: str) -> None:
        for key, value in obj.items():
            css_prop = f"{prefix}-{key}"
            full_path = f"{token_path}.{key}" if token_path else key

            # A nested group (dict WITHOUT $value) is descended into; a DTCG token
            # object ({"$value": ...}) is a LEAF and must NOT be recursed into (else
            # we'd emit --color-x-$value). resolve_token_value collapses both a DTCG
            # object and a bare scalar to the concrete value.
            if is_token_group(value):
                recurse(value, f"{prefix}-{key}", full_path)
                continue
            value = resolve_token_value(value)

            if isinstance(value, str):
                # Legacy PROVISIONAL: prefix check (for configs without provenance)
                if value.startswith("PROVISIONAL:"):
                    lines.append(f"  /* SKIPPED: {css_prop} — provisional value, not emitted */")
                    return

                # G3/G4: Check provenance confidence level
                prov = provenance.get(full_path, {})
                confidence = prov.get("confidence", None)

                if confidence == "failing":
                    lines.append(f"  /* EXCLUDED: {css_prop} — confidence:failing (hard constraint violation). "
                                 f"Do not use. {prov.get('notes', '')} */")
                    return
                elif confidence == "provisional":
                    lines.append(f"  /* SKIPPED: {css_prop} — confidence:provisional "
                                 f"(requires designer replacement). {prov.get('notes', '')} */")
                    return

                # Emit the value — add provenance comment for non-extracted or annotated tokens
                comment_lines = []

                if prov.get("description"):
                    comment_lines.append(prov["description"])
                if prov.get("usage_notes"):
                    comment_lines.append(prov["usage_notes"])
                if confidence == "inferred":
                    last_verified = prov.get("last_verified_at") or "never"
                    comment_lines.append(f"Confidence: inferred (not designer-confirmed). Last verified: {last_verified}.")
                elif confidence and confidence != "extracted":
                    comment_lines.append(f"Confidence: {confidence}.")

                if comment_lines:
                    comment_body = " ".join(comment_lines)
                    lines.append(f"  /* {css_prop}: {comment_body} */")

                lines.append(f"  {css_prop}: {value};")

    recurse(color_obj, "--color", "tokens.color")
    return "\n".join(lines)


def extract_spacing(spacing_obj: dict, field_provenance: dict = None) -> str:
    """G6: Emit spacing CSS vars with provenance description comments.

    Checks meta.field_provenance['tokens.spacing.*'] for description and usage_notes
    and emits them as CSS comments before each spacing custom property.
    """
    lines = []
    provenance = field_provenance or {}

    def emit(css_prop: str, value: str, full_path: str) -> None:
        comment = build_prov_comment(css_prop, full_path, provenance)
        if comment:
            lines.append(comment)
        lines.append(f"  {css_prop}: {value};")

    base = resolve_token_value(spacing_obj.get("base")) or "8px"
    emit("--spacing-base", base, "tokens.spacing.base")
    for tier, value in spacing_obj.get("tiers", {}).items():
        emit(f"--spacing-{tier}", resolve_token_value(value), f"tokens.spacing.tiers.{tier}")
    if spacing_obj.get("content_max_width"):
        emit("--content-max-width", resolve_token_value(spacing_obj["content_max_width"]), "tokens.spacing.content_max_width")
    if spacing_obj.get("page_padding"):
        emit("--page-padding", resolve_token_value(spacing_obj["page_padding"]), "tokens.spacing.page_padding")
    if spacing_obj.get("grid_gap"):
        emit("--grid-gap", resolve_token_value(spacing_obj["grid_gap"]), "tokens.spacing.grid_gap")
    # DE-02: touch-target is an object with min/comfortable; emit min as
    # --spacing-touch-target with an inline WCAG 2.5.5 comment so Cursor rules
    # document its accessibility purpose (not just its pixel value).
    touch_target = spacing_obj.get("touch-target")
    if touch_target:
        if isinstance(touch_target, dict):
            min_val = touch_target.get("min", "44px")
        else:
            min_val = touch_target  # scalar fallback for older configs
        prov_comment = build_prov_comment("--spacing-touch-target", "tokens.spacing.touch-target", provenance)
        if prov_comment:
            lines.append(prov_comment)
        lines.append(f"  --spacing-touch-target: {min_val}; /* WCAG 2.5.5 minimum touch target size */")
    return "\n".join(lines)


def extract_motion(motion_obj: dict, field_provenance: dict = None) -> str:
    """G6: Emit motion CSS vars with provenance description comments.

    Checks meta.field_provenance['tokens.motion.*'] for description and usage_notes
    and emits them as CSS comments before each easing, duration, and stagger property.
    """
    lines = []
    provenance = field_provenance or {}

    def emit(css_prop: str, value: str, full_path: str) -> None:
        comment = build_prov_comment(css_prop, full_path, provenance)
        if comment:
            lines.append(comment)
        lines.append(f"  {css_prop}: {value};")

    for name, value in motion_obj.get("easing", {}).items():
        emit(f"--easing-{name}", resolve_token_value(value), f"tokens.motion.easing.{name}")
    for name, value in motion_obj.get("durations", {}).items():
        emit(f"--duration-{name}", resolve_token_value(value), f"tokens.motion.durations.{name}")
    if motion_obj.get("stagger"):
        emit("--stagger", resolve_token_value(motion_obj["stagger"]), "tokens.motion.stagger")
    return "\n".join(lines)


def extract_type_scale(scale_obj: dict, field_provenance: dict = None) -> str:
    """G6: Emit type scale CSS vars with provenance description comments.

    Checks meta.field_provenance['tokens.typography.scale.{name}'] for description
    and usage_notes and emits them as CSS comments before each --type-* property.
    """
    lines = []
    provenance = field_provenance or {}
    for name, value in scale_obj.items():
        css_prop = f"--type-{name}"
        comment = build_prov_comment(css_prop, f"tokens.typography.scale.{name}", provenance)
        if comment:
            lines.append(comment)
        lines.append(f"  {css_prop}: {resolve_token_value(value)};")
    return "\n".join(lines)


def format_prohibited_words(words: list) -> str:
    if not words:
        return "None specified."
    return ", ".join(f'"{w}"' for w in words)


def format_preferred_patterns(patterns: list) -> str:
    if not patterns:
        return "No preferred patterns configured."
    return "\n".join(f"- {p}" for p in patterns)


def generate_mdc(config: dict) -> str:
    brand = config.get("brand", {})
    tokens = config.get("tokens", {})
    layout = config.get("layout", {})
    voice = config.get("voice", {})
    meta = config.get("meta", {})
    components = config.get("components", {})
    field_provenance = meta.get("field_provenance", {})

    brand_name = brand.get("name", "Unknown Brand")
    version = meta.get("version", "unknown")
    cluster = brand.get("cluster", layout.get("style_cluster", "?"))
    is_provisional = version.startswith("0.")
    completeness = meta.get("completeness_score", "not computed")
    fidelity = meta.get("fidelity_score", "not computed")
    gate_status = meta.get("gate_status", {})
    direction_locked = gate_status.get("direction_lock_confirmed", False)
    designer_reviewed = gate_status.get("designer_review_complete", False)
    spacing_density = layout.get("spacing_density", "balanced")
    preferred_patterns = layout.get("preferred_patterns", [])

    # Typography — G6: pass field_provenance to scale extractor and font family builder
    typo = tokens.get("typography", {})
    families = typo.get("families", {})
    display_stack = extract_font_stack(families.get("display", {}))
    body_stack = extract_font_stack(families.get("body", {}))
    utility_stack = extract_font_stack(families.get("utility", {}))
    font_families_css = build_font_families_css(display_stack, body_stack, utility_stack, field_provenance)
    scale_css = extract_type_scale(typo.get("scale", {}), field_provenance=field_provenance)

    # Colors — pass field_provenance for G3 confidence annotations
    color = tokens.get("color", {})
    colors_css = extract_colors(color, field_provenance=field_provenance)
    contrast_notes = color.get("contrast_notes", [])
    prohibited_colors = [f"{c.get('value')} ({c.get('reason')})" for c in color.get("prohibited", [])]

    # Spacing + motion — G6: pass field_provenance for description comment emission
    spacing_css = extract_spacing(tokens.get("spacing", {}), field_provenance=field_provenance)
    motion_css = extract_motion(tokens.get("motion", {}), field_provenance=field_provenance)
    motion_principles = tokens.get("motion", {}).get("principles", "")

    # Voice
    prohibited_words = format_prohibited_words(voice.get("prohibited_words", []))
    cta_style = voice.get("cta_style", "Human and specific.")
    tone = voice.get("tone", "Not specified.")

    # Components
    comp_source = components.get("source", "")
    comp_framework = components.get("framework", "")
    comp_inventory_count = len(components.get("inventory", []))

    # Focus — G4: confidence gating; G6: description/usage_notes comment emission
    focus = tokens.get("focus", {}).get("outline", {})
    focus_width = resolve_token_value(focus.get("width")) or "2px"
    focus_color_raw = resolve_token_value(focus.get("color")) or "currentColor"
    focus_offset = resolve_token_value(focus.get("offset")) or "2px"

    focus_prov = field_provenance.get("tokens.focus.outline.color") or {}
    focus_confidence = focus_prov.get("confidence")

    if focus_confidence in ("failing", "provisional"):
        focus_color = f"currentColor  /* focus.outline.color excluded: confidence:{focus_confidence} */"
    elif focus_color_raw.startswith("PROVISIONAL:"):
        focus_color = "currentColor  /* PROVISIONAL: value not emitted — replace with confirmed color */"
    elif focus_confidence == "inferred":
        last_verified = focus_prov.get("last_verified_at") or "never"
        focus_color = f"{focus_color_raw}  /* inferred, not designer-confirmed. Last verified: {last_verified} */"
    else:
        focus_color = focus_color_raw

    # G6: build description comment for the --focus-outline property
    focus_desc_comment = build_prov_comment("--focus-outline", "tokens.focus.outline.color", field_provenance)
    focus_comment_line = f"{focus_desc_comment}\n" if focus_desc_comment else ""

    # Build gate/provenance warnings for the MDC header
    gate_warnings = []
    if is_provisional:
        gate_warnings.append(
            f"⚠️ **PROVISIONAL CONFIG (v{version})** — Token values are directional estimates. "
            f"Any field marked `confidence: inferred` or with a `/* SKIPPED */` comment must NOT be used as a hard constraint. "
            f"Run `ui-studio-onboard --refresh` after designer confirms values."
        )
    if not direction_locked:
        gate_warnings.append(
            "⚠️ **DIRECTION NOT LOCKED** — `gate_status.direction_lock_confirmed` is false. "
            "Style cluster and primary direction have not been confirmed. Mode A builds are blocked."
        )
    if not designer_reviewed:
        gate_warnings.append(
            "⚠️ **DESIGNER REVIEW PENDING** — `gate_status.designer_review_complete` is false. "
            "Token values have not been verified against the source design file. "
            "Inferred values may not match the actual design. Do not deliver to client without review."
        )

    provisional_warning = ""
    if gate_warnings:
        provisional_warning = "\n" + "\n\n".join(f"> {w}" for w in gate_warnings) + "\n"

    section_padding = ""
    padding_tiers = layout.get("section_padding_tiers", {})
    if padding_tiers:
        section_padding = f"""
### Section Padding Tiers (from spacing_density: {spacing_density})
- **generous:** {padding_tiers.get('generous', 'not set')}
- **standard:** {padding_tiers.get('standard', 'not set')}
- **tight:** {padding_tiers.get('tight', 'not set')}
"""

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    return f"""---
description: UI Studio brand rules for {brand_name}. Enforces design system compliance in Cursor. Generated from active-brand.json v{version}.
globs: ["**/*.html", "**/*.css", "**/*.js", "**/*.ts", "**/*.tsx", "**/*.jsx", "**/*.scss"]
alwaysApply: false
---

# UI Studio — {brand_name}

**Config version:** {version} | **Cluster:** {cluster} | **Completeness:** {completeness}/100 | **Fidelity:** {fidelity}/100 | **Generated:** {now}
{provisional_warning}
---

## Design System Identity

**Brand:** {brand_name}
**Temperature:** {brand.get('temperature', 'not set')}
**Personality:** {brand.get('personality', 'not set')}
**Spacing density:** {spacing_density}

---

## Token Reference — CSS Custom Properties

Paste this `:root` block into every new project. All values come from active-brand.json. Do not hardcode.

```css
:root {{
  /* Typography families */
{font_families_css}

  /* Type scale */
{scale_css}

  /* Colors */
{colors_css}

  /* Spacing */
{spacing_css}

  /* Motion */
{motion_css}

  /* Focus */
{focus_comment_line}  --focus-outline: {focus_width} solid {focus_color};
  --focus-offset: {focus_offset};
}}
```

---

## WCAG AA — Non-Negotiable

Every build must pass before delivery.

- Body text: **4.5:1** contrast ratio minimum
- Large text (18px+ regular, 14px+ bold): **3:1** minimum
- UI components and decorative borders: **3:1** minimum
- **Visible focus states** on all interactive elements (`outline: var(--focus-outline); outline-offset: var(--focus-offset)`)
- `prefers-reduced-motion` respected in all animations
- Semantic HTML throughout — no `<div>` soup

### Known contrast constraints
{chr(10).join(f"- {note}" for note in contrast_notes) if contrast_notes else "- No contrast notes in config. Verify all color combinations before delivery."}

### Prohibited colors
{chr(10).join(f"- {c}" for c in prohibited_colors) if prohibited_colors else "- None specified."}

---

## Layout Declaration

**Every build begins with a Layout Declaration before any CSS is written.**

Format for each section:
```
Section: [name]
Pattern: [named pattern]
Derivation: exact | modified: [description] | derived-from: [pattern]
Rationale: [why this pattern + brand cluster]
Spacing tier: [generous/standard/tight]
```

### Preferred patterns for this brand (Cluster {cluster})
{format_preferred_patterns(preferred_patterns)}

### Spacing derivation
Spacing density is **{spacing_density}**. All section padding comes from the tiers below.
{section_padding}
---

## Voice Rules

**Tone:** {tone}

**CTAs:** {cta_style}

**Prohibited words:** {prohibited_words}

{f"**Prohibited patterns:** {chr(10).join(voice.get('prohibited_patterns', []))}" if voice.get('prohibited_patterns') else ""}

---

## Component Library

**Source:** {comp_source if comp_source else "Not configured"}
**Framework:** {comp_framework if comp_framework else "Not detected"}
**Inventory:** {comp_inventory_count} components indexed

Before building any component:
1. Check the component inventory — if it exists, use it or extend it
2. If building new, match existing naming and prop conventions
3. Never rebuild what already exists

---

## Motion Rules

{motion_principles if motion_principles else "Apply brand motion tokens from the token reference above. Prefer purposeful transitions (communicate state change). No decorative animation."}

All animations require `@media (prefers-reduced-motion: reduce)` variants.

---

## Build Checklist

Before delivering any output:

- [ ] Layout Declaration completed for every section before CSS was written
- [ ] Post-build: CSS grid/spacing matches declared patterns
- [ ] All colors come from `--color-*` custom properties (no raw hex in CSS)
- [ ] WCAG AA verified for all text/background combinations
- [ ] Focus states visible on all interactive elements
- [ ] `prefers-reduced-motion` handled in all animations
- [ ] Semantic HTML: `<nav>`, `<section>`, `<footer>`, sequential heading hierarchy
- [ ] Font loading: CDN link + `display=swap` + system fallbacks

---

*Generated by `cursor-export.py` from `active-brand.json` v{version}. Do not edit directly — regenerate with `python3 scripts/cursor-export.py`.*
"""


def main():
    parser = argparse.ArgumentParser(description="UI Studio — Cursor Rules Exporter")
    parser.add_argument("--config", "-c", type=str, default=str(DEFAULT_CONFIG),
                        help="Path to the brand config file. Accepts any absolute or relative path. "
                             "E.g., --config /path/to/plugin/brand-config/active-brand.json for cross-tool usage.")
    parser.add_argument("--output", "-o", type=str, default=str(DEFAULT_OUTPUT),
                        help="Output path for the .mdc file. Relative paths resolve from cwd.")
    parser.add_argument("--cursor-project", "-p", type=str, default=None,
                        help="Path to the project root where .cursor/rules/ui-studio.mdc should be written. "
                             "When set, writes to [cursor-project]/.cursor/rules/ui-studio.mdc. "
                             "Overrides --output. Use this when running from a Cursor project root: "
                             "python3 ui-studio/scripts/cursor-export.py --cursor-project .")
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = SKILL_ROOT / args.config

    if args.cursor_project:
        # --cursor-project is a convenience shorthand: writes to [project]/.cursor/rules/ui-studio.mdc.
        # Resolves relative project paths from cwd (e.g., --cursor-project . means the current directory).
        output_path = Path(args.cursor_project).resolve() / ".cursor" / "rules" / "ui-studio.mdc"
    else:
        output_path = Path(args.output)
        if not output_path.is_absolute():
            # Resolve relative output paths from cwd, not SKILL_ROOT.
            # This allows `--output .cursor/rules/ui-studio.mdc` to write to
            # the user's project root when run from there, rather than inside
            # the skill directory.
            output_path = Path.cwd() / args.output

    print(f"\n{'='*60}")
    print(f"  UI Studio — Cursor Rules Exporter")
    print(f"  Config: {config_path.name}")
    print(f"  Output: {output_path}")
    print(f"{'='*60}\n")

    config = load_config(config_path)
    brand_name = config.get("brand", {}).get("name", "Unknown Brand")

    mdc_content = generate_mdc(config)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        f.write(mdc_content)

    print(f"  Generated Cursor rules for: {brand_name}")
    print(f"  Written to: {output_path}")
    print(f"\n{'='*60}\n")


if __name__ == "__main__":
    main()
