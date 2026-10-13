#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tokens.py — the DTCG-native authoring shim for ui-studio brand configs (W5 / audit G7).

A brand config's ``tokens.*`` leaves may be authored in EITHER of two shapes:

    "accent": { "primary": "#2563EB" }                          # legacy bare scalar
    "accent": { "primary": { "$value": "#2563EB",               # DTCG-native
                             "$type": "color",
                             "$description": "Primary CTA." } }

Every reader that pulls a token *value* out of the config must go through
``resolve_token_value`` so both shapes resolve identically and NO reader recurses
into a DTCG object's ``$value``/``$type``/``$description`` keys as if they were
nested tokens. This is the decoupling layer: the storage shape can change without
touching the readers. Backward-compatible by construction — every config onboarded
today is untouched (bare scalars resolve to themselves).

The ``$type`` vocabulary and the category→type inference are reused verbatim from
``heyhi-schema-extension-author`` Step 2 (color, dimension, fontFamily, fontWeight,
duration, cubicBezier, boolean, string). No new mapping is invented here; a token
category the vocabulary cannot type (e.g. a composite box-shadow) is left a scalar
rather than mistyped.

This module is import-safe from the sibling scripts (cursor-export.py, validate.py,
dtcg-codemod.py) via ``sys.path.insert(0, str(Path(__file__).parent))``.
"""

from __future__ import annotations

import re
from typing import Any

# --------------------------------------------------------------------------- #
# The shim
# --------------------------------------------------------------------------- #

# DTCG reserved keys a token object may carry. A dict is a DTCG token iff it has
# "$value"; the others are optional companions.
_DTCG_KEYS = frozenset({"$value", "$type", "$description", "$extensions", "$deprecated"})


def is_dtcg_token(node: Any) -> bool:
    """True iff ``node`` is a DTCG token object (a dict carrying ``$value``)."""
    return isinstance(node, dict) and "$value" in node


def resolve_token_value(node: Any) -> Any:
    """Return the concrete value of a token leaf, whatever shape it was authored in.

    - bare scalar (str/int/float/bool/list) -> returned unchanged (legacy configs)
    - DTCG object ``{"$value": v, ...}``     -> ``v``
    - a nested group (a dict WITHOUT ``$value``) -> ``None``, the signal to the
      caller that this is not a leaf and it should recurse.

    The ``None`` return is the recurse/leaf discriminator: readers that walk the
    token tree call this first and only descend when it returns ``None``.
    """
    if is_dtcg_token(node):
        return node["$value"]
    if isinstance(node, dict):
        return None  # a group, not a leaf — caller should recurse
    return node  # a bare scalar leaf (legacy)


def is_token_group(node: Any) -> bool:
    """True iff ``node`` is a nested group to recurse into (a dict that is NOT a
    DTCG token object). The exact inverse of "is this a resolvable leaf"."""
    return isinstance(node, dict) and not is_dtcg_token(node)


# --------------------------------------------------------------------------- #
# The $type vocabulary + value-shape inference (heyhi-schema-extension-author Step 2)
# --------------------------------------------------------------------------- #

# Category-path prefix -> DTCG $type. Only the token-value *maps* are listed; a
# category absent here (elevation/shadow — a composite the Step-2 vocabulary has no
# scalar type for) is deliberately not codemod-wrapped and stays a scalar.
CATEGORY_TYPE = {
    "color": "color",
    "typography.scale": "dimension",
    "spacing.tiers": "dimension",
    "motion.easing": "cubicBezier",
    "motion.durations": "duration",
    "radius": "dimension",
}

# Shape validators, so the codemod never mistakes a prose note ("hierarchy_note",
# "rhythm") for a value of the target $type. A scalar is wrapped only if BOTH its
# category maps to a $type AND its value matches that type's shape.
_HEX = re.compile(r"^#[0-9a-fA-F]{3,8}$")
_COLOR_FN = re.compile(r"^(rgb|rgba|hsl|hsla|oklch|oklab|lab|lch|color)\(", re.I)
_NAMED_COLOR = frozenset({"transparent", "currentcolor", "inherit", "white", "black"})
_LENGTH = re.compile(
    r"^-?\d*\.?\d+(px|rem|em|%|vw|vh|vmin|vmax|ch|ex|pt|cm|mm|in|fr)?$|"
    r"^(clamp|calc|min|max)\(", re.I
)
_DURATION = re.compile(r"^\d*\.?\d+(ms|s)$", re.I)
_BEZIER = re.compile(r"^(cubic-bezier\(|linear$|ease(-in|-out|-in-out)?$|steps\()", re.I)


def value_matches_type(value: Any, dtcg_type: str) -> bool:
    """True iff ``value`` looks like a legitimate value of ``dtcg_type``. Used by the
    codemod to skip prose notes and non-value scalars sharing a token map."""
    if not isinstance(value, str):
        return False
    v = value.strip()
    if dtcg_type == "color":
        return bool(_HEX.match(v) or _COLOR_FN.match(v) or v.lower() in _NAMED_COLOR)
    if dtcg_type == "dimension":
        return bool(_LENGTH.match(v))
    if dtcg_type == "duration":
        return bool(_DURATION.match(v))
    if dtcg_type == "cubicBezier":
        return bool(_BEZIER.match(v))
    return False


def type_for_path(dotted_path: str) -> str | None:
    """DTCG ``$type`` for a token's dotted path (longest-prefix match), or ``None``
    if the category is not codemod-typable (leave those scalars alone)."""
    best = None
    for prefix, ttype in CATEGORY_TYPE.items():
        if (dotted_path == prefix or dotted_path.startswith(prefix + ".")) and (
            best is None or len(prefix) > len(best[0])
        ):
            best = (prefix, ttype)
    return best[1] if best else None
