#!/usr/bin/env python3
"""
Skill Registry - keyword + tag search over a capability registry.

SHEERLINE PROVENANCE: reused unmodified (R2) from
releases/open-source/keel/skills/registry/skill-registry.py — the registry engine ports as a
keel mechanism, not a parallel one. Only this provenance note is added; the engine, the
confidence gate (the "insufficient" verdict is honest abstention), and the TUNING block are
keel's. Sheerline's design-scoped registry is the sibling skill-registry.yaml.

Part of the Keel scaffold; discovery-search pattern authored by HeyHi
(heyhi.design), released under MIT. Reads a YAML capability registry and returns the
capabilities most relevant to a natural-language query, so an agent loads only what a
task needs instead of every skill every session.

Requires PyYAML and nothing else. If PyYAML is missing, the tool exits with a clear
install message rather than half-parsing the registry itself.

By default it reads `skill-registry.yaml` in the same directory as this script. This
scaffold ships that registry as `skill-registry.template.yaml`; either rename it to
`skill-registry.yaml`, or point `--registry` at the template by its path (it lives next
to this script, not necessarily in your current directory).

Usage (from the skills/registry/ directory):
    python3 skill-registry.py "write this week's report"
    python3 skill-registry.py "review this pull request" --type skill
    python3 skill-registry.py "route this query" --confidence
    python3 skill-registry.py "route this query" --confidence --log-gaps
    python3 skill-registry.py --registry skill-registry.template.yaml --stats
    python3 skill-registry.py --list

A semantic-embedding backend can replace the keyword scorer later without changing this
CLI or the registry schema.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ─────────────────────────────────────────────────────────────────────────────
# TUNING — scoring weights and classification thresholds.
#
# These are STARTING DEFAULTS for a generic registry, not calibrated values.
# The right numbers depend on how many skills you have and how you write your
# triggers, tags, and not_for clauses. Once you have a handful of skills
# registered, adjust them against a small set of known query -> expected-skill
# cases (your own eval set). Nothing here is a magic constant — treat every
# value as a knob and re-tune as your registry grows.
#
# Signal hierarchy (strongest to weakest): an exact trigger-phrase match should
# outweigh a tag match, which should outweigh a loose description-word overlap.
WEIGHT_TRIGGER_PHRASE: float = 1.0   # query contains a skill's full trigger phrase
WEIGHT_TRIGGER_WORD: float = 0.4     # per meaningful trigger word present (capped)
TRIGGER_WORD_CAP: int = 3            # max partial-trigger words counted per skill
WEIGHT_TAG_PHRASE: float = 0.3       # query contains a skill's full tag phrase
WEIGHT_TAG_TERM: float = 0.2         # a meaningful query term overlaps a tag term
WEIGHT_DESC_OVERLAP: float = 0.3     # scaled by the fraction of query terms in the description
NOT_FOR_PENALTY: float = 1.5         # subtracted when a not_for clause matches the query
NOT_FOR_MATCH_THRESHOLD: int = 2     # meaningful term matches needed to trigger the penalty

# ── Classification thresholds (the confidence gate) ──────────────────────────
# What separates "load this skill" from "ask the operator which one" from "say that
# nothing matched." Re-tune these against your own eval set exactly like the weights
# above; a good moment to revisit is when routing starts to misfire, which usually shows
# up as frequent trigger collisions or a narrow score gap on many queries.

# A lone top result must clear this to be "confident" outright. With two or more results
# the GAP below decides instead: a clear winner routes even on a moderate score.
CONFIDENCE_SCORE_THRESHOLD: float = 1.0

# A "confident" result must lead the runner-up by at least this much.
# Below it -> "ambiguous", however high the top score.
CONFIDENCE_GAP_THRESHOLD: float = 0.4

# The floor a match must clear to be worth surfacing at all. Below it -> "insufficient".
AMBIGUOUS_MIN_SCORE: float = 0.4

# The default min_score for search_with_confidence(), where a weak match is worse than an
# honest "nothing matched" (raw search() defaults to 0.0 and filters nothing).
#
# Keep this equal to AMBIGUOUS_MIN_SCORE. They are two names for one idea, and if the
# filter sits ABOVE the gate's floor, matches the gate would have called "ambiguous" get
# discarded before it ever sees them: the search reports "insufficient" for a match that
# cleared its own documented bar. tests/test_tuning.py asserts the two stay in step.
DEFAULT_MIN_SCORE: float = 0.4
# ─────────────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────
# YAML loading - PyYAML is required; a clear, actionable error if it is missing
# ─────────────────────────────────────────────────────────────────────────────

try:
    import yaml as _yaml

    # libyaml's C loader parses 12-31x faster than the pure-Python path, with
    # byte-identical output -- but not every PyYAML install has it (an sdist build
    # without the libyaml headers lacks the class entirely), so resolve once here and
    # fall back to the pure-Python loader when absent. Its YAMLError subclasses still
    # carry problem_mark, so the line-numbered error message below is unaffected.
    _YAML_LOADER = getattr(_yaml, "CSafeLoader", _yaml.SafeLoader)

    def _load_yaml(path: Path) -> dict:
        try:
            with open(path, encoding="utf-8") as f:
                return _yaml.load(f, Loader=_YAML_LOADER)
        except _yaml.YAMLError as exc:
            # A hand-edited registry with a syntax slip -- an unclosed bracket, a bad
            # indent -- should say so with a line number, not dump a parser traceback.
            # RegistryError is what cli() already catches and reports as a clean exit-1;
            # it is defined below and resolved when this runs, not at def time.
            mark = getattr(exc, "problem_mark", None)
            location = f" near line {mark.line + 1}" if mark is not None else ""
            raise RegistryError(
                f"{path}: the registry has a YAML syntax error{location}."
            ) from exc
        except UnicodeDecodeError as exc:
            # The registry is read as UTF-8. A file saved in another encoding, or a binary
            # file pointed at by mistake, raises this mid-read; name it instead of letting
            # the raw decode error escape.
            raise RegistryError(
                f"{path}: the registry is not valid UTF-8. Re-save it as UTF-8."
            ) from exc

except ImportError:
    # No fallback parser: PyYAML is a hard requirement. A hand-rolled reader for a
    # hand-edited registry is exactly the "sufficient for the common case" shortcut that
    # fails silently on the first edge case (multi-line strings, anchors, quoting), so
    # this raises a clear, actionable error instead of half-parsing.
    def _load_yaml(path: Path) -> dict:  # type: ignore[misc]
        raise ImportError(
            "PyYAML is required. The recommended install is in a virtual environment:\n"
            "    python3 -m venv .venv && source .venv/bin/activate\n"
            "    python3 -m pip install pyyaml"
        )


# ─────────────────────────────────────────────────────────────────────────────
# Data model
# ─────────────────────────────────────────────────────────────────────────────


@dataclass
class Capability:
    """A single registered capability - skill, reference, or tool."""

    id: str
    name: str
    type: str  # "skill" | "reference" | "tool"
    description: str
    semantic_tags: list[str] = field(default_factory=list)
    trigger_patterns: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    not_for: list[str] = field(default_factory=list)
    load_cost_tokens: int = 0
    location: str = ""

    def __repr__(self) -> str:
        return f"Capability(id={self.id!r}, type={self.type!r}, tokens={self.load_cost_tokens})"


@dataclass
class CapabilityMatch:
    """A registry match with its relevance score.

    A flat dataclass (not a wrapper around Capability) so it composes cleanly with any
    orchestration layer that consumes search results. The Capability dataclass above
    retains semantic_tags and trigger_patterns for internal search use; they are not
    exposed here because consumers of search results do not need them.
    """

    id: str
    name: str
    type: str
    description: str
    relevance_score: float
    load_cost_tokens: int
    location: str
    dependencies: list[str]

    def __repr__(self) -> str:
        return f"CapabilityMatch(id={self.id!r}, score={self.relevance_score:.3f})"


@dataclass
class SearchResponse:
    """
    Output of search_with_confidence().

    Wraps the standard search results with a confidence gate classification
    and score-gap metadata for monitoring registry health over time.

    confidence values:
        "confident"    - top result scores well and pulls ahead of #2.
                         Proceed: load the skill and execute.
        "ambiguous"    - top result scores above the minimum but the gap
                         to #2 is narrow. Surface both candidates to the
                         user; ask to disambiguate before loading.
        "insufficient" - no results cleared the minimum score threshold.
                         Abstain: tell the user no skill clearly matches.

    score_gap is None when fewer than 2 results were returned.

    When max_tokens is set, confidence/top_score/score_gap are assessed against the full
    ranked candidate list, not the budget-filtered one: an unaffordable runner-up that is
    genuinely close to #1 must still make this call "ambiguous," even though it will
    never appear in `results`. This can leave top_score higher than
    results[0].relevance_score -- that gap is the budget's own signal that the true best
    match did not fit.
    """

    results: list[CapabilityMatch]
    confidence: str  # "confident" | "ambiguous" | "insufficient"
    top_score: float
    score_gap: Optional[float]  # gap between #1 and #2; None if <2 results

    def __repr__(self) -> str:
        return (
            f"SearchResponse(confidence={self.confidence!r}, "
            f"top_score={self.top_score:.3f}, "
            f"results={len(self.results)})"
        )


# ─────────────────────────────────────────────────────────────────────────────
# Registry loading
# ─────────────────────────────────────────────────────────────────────────────


class RegistryError(ValueError):
    """
    A registry file that cannot be trusted to mean what it says.

    Raised instead of letting a malformed entry through to the scorer. This registry is a
    file you write by hand, and the failure modes of hand-written YAML are quiet ones: a
    forgotten pair of brackets turns a list into a string, and a string is iterable, so
    nothing crashes. It just scores wrong, forever, and you have no reason to look.
    """


def _list_field(entry: dict, field_name: str, entry_id: str) -> list[str]:
    """
    Read a list-valued field, refusing a bare string.

    `semantic_tags: invoicing` (no brackets) is valid YAML and gives you the *string*
    "invoicing", not a one-item list. Python will happily iterate it character by
    character, so every letter gets scored as its own tag: the entry quietly out-scores a
    real trigger-phrase match on queries it has nothing to do with. The same slip on
    `not_for` disables the clause instead, because no single character ever matches a whole
    query term. Both are silent. Both are the exact typo a person makes filling in a
    template, so both are refused here, by name, with the fix in the message.
    """
    value = entry.get(field_name)
    if value is None:
        return []
    if isinstance(value, str):
        raise RegistryError(
            f"{entry_id}: {field_name} is a string, but it has to be a list. "
            f"Write `{field_name}: [{value!r}]` (or a `- ` item per line). As written, it "
            f"would be read one character at a time."
        )
    if not isinstance(value, list):
        raise RegistryError(
            f"{entry_id}: {field_name} must be a list, got {type(value).__name__}."
        )
    return value


VALID_TYPES = ("skill", "reference", "tool")


def load_registry(path: str | Path | None = None) -> list[Capability]:
    """
    Load capabilities from a YAML registry file.

    Defaults to skill-registry.yaml in the same directory as this script.

    Raises FileNotFoundError if the file is missing, and RegistryError if the file parses
    as YAML but is not a registry. An empty registry is not an error: it is where you start.
    """
    if path is None:
        path = Path(__file__).parent / "skill-registry.yaml"

    path = Path(path)
    if not path.exists():
        # Point at the template by its script-anchored path, not the bare relative name:
        # the documented commands run from the repo root, where `skill-registry.template.yaml`
        # would resolve against the wrong directory and loop the operator straight back here.
        template = Path(__file__).parent / "skill-registry.template.yaml"
        raise FileNotFoundError(
            f"Registry not found: {path}. If you haven't set one up yet, this scaffold "
            f"ships its starter registry alongside this script as skill-registry.template.yaml. "
            f"Rename it to skill-registry.yaml, or point at it directly with "
            f"--registry {template}."
        )

    # An empty registry file parses to None, and a `capabilities:` key with nothing under
    # it parses to None rather than []. Both are ordinary states for this scaffold -- the
    # second one is exactly what you get the moment you delete the shipped example entries
    # to start filling in your own -- so both have to load as "empty", not raise.
    data = _load_yaml(path) or {}
    if not isinstance(data, dict):
        raise RegistryError(
            f"{path}: the top level of a registry must be a mapping with a `capabilities:` "
            f"key, got {type(data).__name__}."
        )

    # `data.get(...) or []` would coerce a *present but wrong-type falsy* value ({}, false,
    # 0, "") to an empty list, and a malformed registry would then audit as a clean, empty
    # one. Absent or null is the legitimate "just deleted the examples" state and loads as
    # empty; present-but-wrong-type is refused by name.
    raw_entries = data.get("capabilities")
    if raw_entries is None:
        raw_entries = []
    if not isinstance(raw_entries, list):
        raise RegistryError(
            f"{path}: `capabilities:` must be a list of entries, got "
            f"{type(raw_entries).__name__}."
        )

    capabilities: list[Capability] = []
    seen_ids: set[str] = set()

    for i, entry in enumerate(raw_entries):
        if not isinstance(entry, dict):
            raise RegistryError(
                f"{path}: capability #{i + 1} is a {type(entry).__name__}, not a mapping. "
                f"Every entry needs at least an id, a name, and a type."
            )

        entry_id = entry.get("id") or f"capability #{i + 1}"
        for required in ("id", "name", "type"):
            if not entry.get(required):
                raise RegistryError(f"{entry_id}: missing required field: {required}")

        # id/name/type have to be text. A list or dict `id:` satisfies the truthy check
        # above and then reaches the duplicate-id lookup below, where an unhashable key
        # raises a raw TypeError -- the one outcome this validation exists to prevent.
        # Checked here, before that lookup runs, so the error names the field instead.
        for required in ("id", "name", "type"):
            if not isinstance(entry[required], str):
                raise RegistryError(
                    f"{entry_id}: {required} must be text, got "
                    f"{type(entry[required]).__name__}."
                )

        if entry_id in seen_ids:
            raise RegistryError(
                f"{entry_id}: duplicate id -- another capability earlier in this registry "
                f"already uses {entry_id!r}. Two entries competing under one id can never "
                f"be told apart; with --confidence they permanently tie, producing an "
                f"unexplained gap-0.000 'ambiguous' verdict. Give each capability a unique id."
            )
        seen_ids.add(entry_id)

        if entry["type"] not in VALID_TYPES:
            raise RegistryError(
                f"{entry_id}: type must be one of {VALID_TYPES}, got {entry['type']!r}."
            )

        # Same "key present, value forgotten" slip as `capabilities:` above -- a bare
        # `load_cost_tokens:` parses to None and would otherwise poison every sum it
        # lands in. Absent or null reads as zero, which is the honest reading of "not
        # stated," not an error.
        #
        # Written as an explicit None check rather than `... or 0`: `or` cannot tell
        # null from a present-but-wrong-type falsy value, so `load_cost_tokens: false`
        # (or {}, or "") would collapse to a legitimate-looking 0 -- and an entry that
        # costs nothing survives every --max-tokens budget, out-competing the honestly
        # priced entries it should have been weighed against.
        tokens = entry.get("load_cost_tokens")
        if tokens is None:
            tokens = 0
        if not isinstance(tokens, int) or isinstance(tokens, bool):
            raise RegistryError(
                f"{entry_id}: load_cost_tokens must be a whole number, got {tokens!r}."
            )
        if tokens < 0:
            raise RegistryError(
                f"{entry_id}: load_cost_tokens must not be negative, got {tokens!r}. A "
                f"negative cost would inflate every --max-tokens budget it's summed into."
            )

        capabilities.append(
            Capability(
                id=entry["id"],
                name=entry["name"],
                type=entry["type"],
                description=entry.get("description") or "",
                semantic_tags=_list_field(entry, "semantic_tags", entry_id),
                trigger_patterns=_list_field(entry, "trigger_patterns", entry_id),
                dependencies=_list_field(entry, "dependencies", entry_id),
                not_for=_list_field(entry, "not_for", entry_id),
                load_cost_tokens=tokens,
                location=entry.get("location") or "",
            )
        )

    return capabilities


# ─────────────────────────────────────────────────────────────────────────────
# Text normalization
# ─────────────────────────────────────────────────────────────────────────────


def normalize(text: str) -> str:
    """
    Lowercase, strip punctuation, collapse whitespace.

    Used consistently for both query and indexed text so scoring is symmetric.
    """
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# Compiled trigger-phrase patterns, cached at module scope and keyed by the (already
# lowercased) phrase text. Every search() call re-checks every trigger pattern of every
# capability, so a registry of any real size recompiles the same handful of hundreds of
# patterns over and over; past ~170 capabilities that churn starts evicting entries from
# Python's own 512-slot regex cache, so calls even within one process stop benefiting
# from it. Caching the compiled Pattern object here, rather than relying on that
# built-in cache, means a phrase is compiled once for the life of the process no matter
# how many searches run -- eval loops, --max-tokens' double search, and any library
# consumer calling search() repeatedly all benefit. Cache-safe: a Pattern object is a
# pure function of its phrase text, and no code here ever mutates a cached entry.
_TRIGGER_RE_CACHE: dict[str, "re.Pattern[str]"] = {}


def _trigger_phrase_matches(pattern_lower: str, query_lower: str) -> bool:
    """
    True when `query_lower` contains `pattern_lower` at a word boundary on both sides.

    Both arguments are expected pre-lowercased. This keeps this scaffold's existing
    anchoring exactly as it was (word-boundary on both sides of the phrase) -- only the
    compiled Pattern object is cached, not the matching semantics.
    """
    compiled = _TRIGGER_RE_CACHE.get(pattern_lower)
    if compiled is None:
        compiled = re.compile(r"\b" + re.escape(pattern_lower) + r"\b")
        _TRIGGER_RE_CACHE[pattern_lower] = compiled
    return bool(compiled.search(query_lower))


# ─────────────────────────────────────────────────────────────────────────────
# Search - keyword + tag matching
# ─────────────────────────────────────────────────────────────────────────────


def search(
    query: str,
    registry: list[Capability],
    top_k: int = 3,
    capability_type: Optional[str] = None,
    max_tokens: Optional[int] = None,
    min_score: float = 0.0,
) -> list[CapabilityMatch]:
    """
    Keyword + tag matching search over the capability registry.

    Returns top_k matches ranked by relevance score (descending).
    Returns an empty list if nothing scores above zero (or above min_score).

    Scoring is additive. Every weight below is a knob in the TUNING block at the top of
    this module. They are cited here by NAME, never by value, so that re-tuning a weight
    cannot leave this docstring quietly describing numbers the code no longer uses:

        + WEIGHT_TRIGGER_PHRASE  the query contains a capability's full trigger phrase.
                                 The strongest signal in the model.
        + WEIGHT_TRIGGER_WORD    per meaningful trigger word present, counted at most
                                 TRIGGER_WORD_CAP times for any one capability.
        + WEIGHT_TAG_PHRASE      the query contains a capability's full semantic tag.
        + WEIGHT_TAG_TERM        a meaningful query term overlaps a tag's term set.
        + WEIGHT_DESC_OVERLAP    scaled by the overlap ratio
                                 |q_terms ∩ desc_terms| / |q_terms|.
        - NOT_FOR_PENALTY        per not_for clause that matches the query, applied when
                                 NOT_FOR_MATCH_THRESHOLD or more meaningful query terms
                                 prefix-match the clause (which catches stemming variants
                                 like "build/building" and "write/writing"). Signals that
                                 the query is explicitly out-of-scope for this capability.
                                 At most one penalty per clause; multiple clauses compound.

    Args:
        query          : Natural language description of what the agent needs.
        registry       : List of Capability entries to search.
        top_k          : Maximum results to return.
        capability_type: Optional filter - "skill", "reference", or "tool".
        max_tokens     : If set, returned matches fit within this token budget
                         (greedily fills from highest-score down).
        min_score      : Minimum relevance score to include in results. Defaults to 0.0
                         (no filtering) for raw search. Pass DEFAULT_MIN_SCORE to suppress
                         low-signal noise while keeping genuine secondary matches; that is
                         what search_with_confidence() does.
                         Does not affect which result is ranked #1 - only trims the tail.

    Returns:
        List of CapabilityMatch ordered by relevance_score descending.
    """
    if not query.strip():
        return []

    q_raw = query.strip()
    q_lower = q_raw.lower()
    q_normalized = normalize(q_raw)
    q_terms = set(q_normalized.split())
    # Pre-compute meaningful query terms (len > 3) once per query.
    # Used by tag overlap, description overlap, and not_for matching to
    # exclude single-character and 2-3 char stop word tokens that inflate
    # scores without carrying semantic signal.
    meaningful_q = {t for t in q_terms if len(t) > 3}

    scored: list[CapabilityMatch] = []

    def _terms_match(t1: str, t2: str) -> bool:
        # Refinement: prefix-4 matching is
        # too coarse for longer words ("comp" matches component/composition;
        # "desi" matches design/designer). Use prefix-6 when both terms are
        # >=7 chars to preserve genuine stemming (evaluate/evaluating share
        # "evalua"; design/designer share "design") while separating
        # semantically distinct roots (component/composition diverge after
        # "compo"). Keep prefix-4 for shorter words (build/builds, audit/
        # auditing, write/writing).
        if min(len(t1), len(t2)) >= 7:
            return t1[:6] == t2[:6]
        return t1[:4] == t2[:4]

    for cap in registry:
        # ── Type filter ────────────────────────────────────────────────────
        if capability_type and cap.type != capability_type:
            continue

        score = 0.0

        # ── Trigger pattern matching (highest signal) ──────────────────────
        # Partial trigger matches are capped per skill: a skill with N
        # "build"-containing triggers should not score N * the per-word weight on
        # any "build" query. Cap the partial bonus at
        # TRIGGER_WORD_CAP * WEIGHT_TRIGGER_WORD, applied once after the loop.
        partial_trigger_hits = 0
        for pattern in cap.trigger_patterns:
            p_lower = pattern.lower()
            if _trigger_phrase_matches(p_lower, q_lower):
                # Full trigger phrase found in query, word-boundary anchored -- aligned
                # with the sibling repo's equivalent check, so a short trigger phrase
                # cannot match as a substring of an unrelated longer word (e.g. "cat"
                # inside "concatenate").
                score += WEIGHT_TRIGGER_PHRASE
            elif any(term in q_lower for term in p_lower.split() if len(term) > 4):
                # At least one meaningful trigger word present (>4 chars filters
                # common 4-char stop words: "this", "that", "from", "like", "what",
                # "your", "make", "have", "will", "with" etc. that inflate scores
                # on unrelated queries)
                partial_trigger_hits += 1
        score += min(partial_trigger_hits, TRIGGER_WORD_CAP) * WEIGHT_TRIGGER_WORD

        # ── Semantic tag matching ──────────────────────────────────────────
        # Refinement: tag intersection
        # previously used raw q_terms, so single-char and 2-3 char stop
        # words ("a", "to", "in") counted as overlap with any multi-word
        # tag containing them. Use meaningful_q (len > 3) instead.
        for tag in cap.semantic_tags:
            tag_lower = tag.lower()
            tag_normalized = normalize(tag)
            tag_terms = {t for t in tag_normalized.split() if len(t) > 3}

            if tag_lower in q_lower:
                # Full tag phrase is a substring of the query
                score += WEIGHT_TAG_PHRASE
            elif meaningful_q & tag_terms:
                # Any meaningful query term overlaps with any meaningful tag term
                score += WEIGHT_TAG_TERM

        # ── Description term overlap ───────────────────────────────────────
        desc_terms = set(normalize(cap.description).split())
        # Exclude very short/common words to reduce noise
        meaningful_desc = {t for t in desc_terms if len(t) > 3}

        if meaningful_q:
            overlap = len(meaningful_q & meaningful_desc) / len(meaningful_q)
            score += overlap * WEIGHT_DESC_OVERLAP

        # ── Not-for negative scoring ───────────────────────────────────────
        # Penalize capabilities whose not_for clauses closely match the query.
        # Term comparison goes through _terms_match (above), which prefix-matches
        # to catch stemming variants (build/building, write/writing, audit/auditing).
        # Requires NOT_FOR_MATCH_THRESHOLD meaningful term matches per clause to
        # avoid false negatives. Both knobs live in the TUNING block up top.
        #
        # Before you ship a new clause: a clause can read as correct English and still
        # never fire, because the guard below keys off its leading word. See
        # README.md's "A clause can read as correct and do nothing" section for the
        # three-step way to verify a clause actually works before trusting it.
        for clause in cap.not_for:
            # Strip the trailing "(use ...)" hint from the RAW clause BEFORE normalize().
            # normalize() removes parentheses, turning "(use other-skill instead)" into
            # "use other skill instead". The old single-step regex then matched \buse\b
            # anywhere in the clause - including mid-clause - and wiped everything from
            # that point onward, silently disabling the not_for penalty.
            # Fix: strip the parenthetical pattern from raw
            # text first; normalize() runs on the already-cleaned string.
            clause_raw = re.sub(r'\s*\(use\b[^)]*\)', '', clause).strip()
            clause_clean = normalize(clause_raw)
            clause_words = [t for t in clause_clean.split() if len(t) > 3]
            clause_terms = set(clause_words)

            # Guard: the first meaningful word of the clause must prefix-match a query term.
            # This prevents penalizing on shared domain terms alone (e.g. "design system"
            # in both an audit query and an audit skill's not_for clause about "Building
            # UI in a client's design system"). The action verb / primary noun discriminates.
            first_clause_term = clause_words[0] if clause_words else None
            if not first_clause_term:
                continue
            # Refinement: both the guard
            # and penalty loop previously used raw prefix-4 comparison.
            # _terms_match uses a 6-char prefix for >=7-char terms (long enough to
            # separate distinct roots like component/composition), falling back to a
            # 4-char prefix for shorter stemming variants.
            first_term_present = any(_terms_match(q_term, first_clause_term) for q_term in meaningful_q)
            if not first_term_present:
                continue

            matches = 0
            for q_term in meaningful_q:
                for c_term in clause_terms:
                    if _terms_match(q_term, c_term):
                        matches += 1
                        break  # Only count each query term once per clause

            if matches >= NOT_FOR_MATCH_THRESHOLD:
                score -= NOT_FOR_PENALTY

        if score > 0:
            # build flat CapabilityMatch from Capability fields
            scored.append(CapabilityMatch(
                id=cap.id,
                name=cap.name,
                type=cap.type,
                description=cap.description,
                relevance_score=round(score, 3),
                load_cost_tokens=cap.load_cost_tokens,
                location=cap.location,
                dependencies=cap.dependencies,
            ))

    # ── Sort by score descending ───────────────────────────────────────────
    scored.sort(key=lambda m: m.relevance_score, reverse=True)

    # ── Minimum score filter ───────────────────────────────────────────────
    if min_score > 0.0:
        scored = [m for m in scored if m.relevance_score >= min_score]

    # ── Token budget filter (greedy from highest score) ────────────────────
    if max_tokens is not None:
        budget_filtered: list[CapabilityMatch] = []
        remaining = max_tokens
        for match in scored:
            if match.load_cost_tokens <= remaining:
                budget_filtered.append(match)
                remaining -= match.load_cost_tokens
        scored = budget_filtered

    return scored[:top_k]


# ─────────────────────────────────────────────────────────────────────────────
# The confidence gate
# Emits a 3-way classification (confident / ambiguous / insufficient) for routing
# decisions. Its three thresholds live in the TUNING block at the top of this file,
# alongside the scoring weights, because they are knobs of the same kind.
# ─────────────────────────────────────────────────────────────────────────────


def assess_confidence(results: list[CapabilityMatch]) -> str:
    """
    Classify a search result list as "confident", "ambiguous", or "insufficient".

    Rules (in order):
      1. No results, or top score < AMBIGUOUS_MIN_SCORE  → "insufficient"
      2. Only one result, top score ≥ CONFIDENCE_SCORE_THRESHOLD  → "confident"
      3. Only one result, top score < CONFIDENCE_SCORE_THRESHOLD  → "ambiguous"
      4. gap ≥ CONFIDENCE_GAP_THRESHOLD and score ≥ CONFIDENCE_SCORE_THRESHOLD
            → "confident"
      5. gap < CONFIDENCE_GAP_THRESHOLD  → "ambiguous"
      6. gap is sufficient but score is moderate  → "confident"

    Called by search_with_confidence(). Can also be called standalone when
    results come from a raw search() call.
    """
    if not results or results[0].relevance_score < AMBIGUOUS_MIN_SCORE:
        return "insufficient"

    top_score = results[0].relevance_score

    if len(results) < 2:
        # Single result - confident only if it clearly clears the score bar
        return "confident" if top_score >= CONFIDENCE_SCORE_THRESHOLD else "ambiguous"

    gap = top_score - results[1].relevance_score

    if gap < CONFIDENCE_GAP_THRESHOLD:
        return "ambiguous"

    if top_score >= CONFIDENCE_SCORE_THRESHOLD:
        return "confident"

    # Gap is sufficient but score is moderate - still route, but cautiously
    return "confident"


# ─────────────────────────────────────────────────────────────────────────────
# Score-gap distribution logging
# Appends one record per search call to a JSONL file, so that "is keyword matching
# still good enough for the size this registry has grown to?" becomes a question you
# can answer from data instead of from a hunch. When a large share of your queries
# come back with the top two capabilities nearly tied, keyword scoring has stopped
# discriminating and a semantic-embedding backend starts to earn its cost. What counts
# as "a large share" and "nearly tied" depends on your registry; watch the distribution
# and pick your own line.
# Log is best-effort - logging failures are silently swallowed so they never
# interrupt the routing path.
# ─────────────────────────────────────────────────────────────────────────────

GAP_LOG_PATH: Path = Path(__file__).parent / "score-gap-log.jsonl"


def log_score_gap(
    query: str,
    results: list[CapabilityMatch],
    confidence: str,
    log_path: Optional[Path] = None,
) -> None:
    """
    Append a score-gap record to the distribution log (JSONL).

    Each record captures the timestamp, query, confidence classification,
    top score, gap to #2, and the IDs of the top two candidates.

    Use `log_gaps=True` in search_with_confidence() to activate logging.
    To analyse: read score-gap-log.jsonl and look at the distribution of the
    `gap` field. A healthy registry mostly produces a clear winner. When a
    large share of queries come back with the top two nearly tied, keyword
    scoring has stopped discriminating at the size your registry has reached,
    and a semantic-embedding backend starts to earn its cost (it can replace
    this scorer behind the same interface). Where exactly you draw that line
    is yours to pick, from your own distribution.

    Logging is best-effort. Any OS or encoding error is silently ignored
    so that a logging failure can never interrupt the search path.
    """
    if log_path is None:
        log_path = GAP_LOG_PATH

    record: dict = {
        "ts": datetime.now(tz=timezone.utc).isoformat(),
        "query": query,
        "confidence": confidence,
        "top_score": results[0].relevance_score if results else 0.0,
        "gap": (
            round(results[0].relevance_score - results[1].relevance_score, 3)
            if len(results) >= 2 else None
        ),
        "top_id": results[0].id if results else None,
        "second_id": results[1].id if len(results) >= 2 else None,
    }

    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
    except OSError:
        pass  # Best-effort - never raise from logging path


def _confidence_basis(
    query: str,
    registry: list[Capability],
    top_k: int,
    capability_type: Optional[str],
    max_tokens: Optional[int],
    min_score: float,
    budgeted_results: list[CapabilityMatch],
) -> list[CapabilityMatch]:
    """
    The ranked list the confidence gate should judge, as distinct from the list a caller
    can afford to load.

    With no token budget, that is simply budgeted_results -- every existing caller's
    shape is unchanged. When max_tokens narrowed the field, re-run unbudgeted instead: a
    runner-up that is a genuine near-tie with #1 must still make the gate say
    "ambiguous," even when it does not fit the budget and will never appear in the
    caller's results. Re-querying is cheap at the registry sizes this scaffold targets,
    and it leaves search()'s own contract -- its return value is exactly what you can
    afford, in rank order -- untouched.
    """
    if max_tokens is None:
        return budgeted_results
    return search(
        query=query,
        registry=registry,
        top_k=top_k,
        capability_type=capability_type,
        max_tokens=None,
        min_score=min_score,
    )


def search_with_confidence(
    query: str,
    registry: list[Capability],
    top_k: int = 3,
    capability_type: Optional[str] = None,
    max_tokens: Optional[int] = None,
    min_score: float = DEFAULT_MIN_SCORE,
    log_gaps: bool = False,
    log_path: Optional[Path] = None,
) -> SearchResponse:
    """
    search() + confidence gate (A1) + optional score-gap logging (A2).

    Prefer this over search() for production routing decisions.
    Use search() directly for listing, --stats, exploratory queries, and
    contexts where the caller wants raw results without a confidence wrapper.

    Args:
        query, registry, top_k, capability_type, max_tokens:
            Passed through to search() unchanged.
        min_score:
            Defaults to DEFAULT_MIN_SCORE rather than search()'s 0.0. This
            suppresses low-signal noise at routing time, where a weak match is
            worse than "insufficient" (the fallback path is explicit abstention).
        log_gaps:
            If True, appends a score-gap record to score-gap-log.jsonl. Turn it on
            once you want evidence about whether keyword matching is still
            discriminating well at the size your registry has reached. See
            log_score_gap() for how to read the distribution.
        log_path:
            Override the default log file path (default: score-gap-log.jsonl
            in the same directory as this script). Useful for tests.

    Returns:
        SearchResponse with results, confidence, top_score, and score_gap. When
        max_tokens is set, the latter three are assessed against the unbudgeted
        ranking (see _confidence_basis and SearchResponse's own docstring) so that
        budget filtering cannot flip "ambiguous" to "confident" by pricing out the
        true runner-up.
    """
    results = search(
        query=query,
        registry=registry,
        top_k=top_k,
        capability_type=capability_type,
        max_tokens=max_tokens,
        min_score=min_score,
    )

    confidence_basis = _confidence_basis(
        query, registry, top_k, capability_type, max_tokens, min_score, results
    )
    confidence = assess_confidence(confidence_basis)
    top_score = confidence_basis[0].relevance_score if confidence_basis else 0.0
    score_gap = (
        round(confidence_basis[0].relevance_score - confidence_basis[1].relevance_score, 3)
        if len(confidence_basis) >= 2 else None
    )

    if log_gaps:
        log_score_gap(query, confidence_basis, confidence, log_path)

    return SearchResponse(
        results=results,
        confidence=confidence,
        top_score=top_score,
        score_gap=score_gap,
    )


# ─────────────────────────────────────────────────────────────────────────────
# A3 - Session skill-utilization tracking (stub)
# Full implementation belongs in your session-integrity routine.
# This function provides the supporting interface: given a session log of
# which skills were loaded, it separates "central" from "loaded-but-unused"
# entries and returns a utilization report dict.
#
# Status: stub - the session-integrity skill does not yet call this.
# Next step: extend your session-integrity routine to:
#   1. Log every skill loaded during the session as a structured list.
#   2. At session end, call track_skill_usage() with that list.
#   3. Surface the utilization report in the Phase 5 (final report) output.
# ─────────────────────────────────────────────────────────────────────────────


def track_skill_usage(
    loaded_skills: list[str],
    central_skills: list[str],
) -> dict:
    """
    Produce a skill-utilization report for session-integrity Phase 5.

    Args:
        loaded_skills:  IDs of every skill/reference loaded during the session.
        central_skills: IDs the agent used as the primary source for work output.
                        Typically a subset of loaded_skills. The caller (session-
                        integrity skill) determines centrality by checking which
                        skills were explicitly cited in session artifacts.

    Returns a dict with:
        central       - list of skill IDs that drove the work
        loaded_unused - loaded but never cited in output (waste candidates)
        not_loaded    - skills mentioned in output but not loaded (gap candidates)
        utilization   - fraction of loaded skills that were central (0.0–1.0)

    This function is pure (no I/O). The session-integrity skill is responsible
    for collecting the inputs and rendering the report into its Phase 5 output.
    """
    central_set = set(central_skills)
    loaded_set = set(loaded_skills)

    loaded_unused = sorted(loaded_set - central_set)
    not_loaded = sorted(central_set - loaded_set)
    utilization = len(central_set & loaded_set) / len(loaded_set) if loaded_set else 0.0

    return {
        "central": sorted(central_set & loaded_set),
        "loaded_unused": loaded_unused,
        "not_loaded": not_loaded,
        "utilization": round(utilization, 3),
        "loaded_count": len(loaded_set),
        "central_count": len(central_set & loaded_set),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Token savings measurement
# ─────────────────────────────────────────────────────────────────────────────

# Approximate token cost for the discovery meta-tool schema itself when loaded
# as a tool definition in the system prompt.
DISCOVERY_TOOL_TOKENS = 200


def measure_token_savings(registry: list[Capability]) -> dict:
    """
    Compare static loading (all capabilities upfront) vs. dynamic discovery.

    Static cost  : every capability description loaded every session.
    Dynamic cost : meta-tool schema (fixed ~200 tokens) + top-3 matched capabilities.
                   Estimated using the median token cost of the registry.

    Returns a dict of metrics suitable for logging or reporting.
    """
    if not registry:
        return {}

    static_total = sum(cap.load_cost_tokens for cap in registry)

    # Representative typical session: discovery returns top-3 matches.
    # Estimate their combined cost using a middle-range sample.
    costs = sorted(cap.load_cost_tokens for cap in registry)
    mid = len(costs) // 2
    # Take 3 costs from around the median to represent a typical session load
    sample_slice = costs[max(0, mid - 1) : min(len(costs), mid + 2)]
    typical_matched_tokens = sum(sample_slice)

    dynamic_typical = DISCOVERY_TOOL_TOKENS + typical_matched_tokens
    reduction_abs = static_total - dynamic_typical
    reduction_pct = round((1 - dynamic_typical / static_total) * 100, 1) if static_total else 0

    return {
        "static_total_tokens": static_total,
        "dynamic_meta_tool_tokens": DISCOVERY_TOOL_TOKENS,
        "dynamic_typical_session_tokens": dynamic_typical,
        "reduction_absolute": reduction_abs,
        "reduction_percent": reduction_pct,
        "capabilities_indexed": len(registry),
        "skills": len([c for c in registry if c.type == "skill"]),
        "references": len([c for c in registry if c.type == "reference"]),
        "tools": len([c for c in registry if c.type == "tool"]),
    }


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────


def _print_separator(label: str = "", width: int = 60) -> None:
    if label:
        pad = width - len(label) - 2
        print(f"\n─── {label} {'─' * max(0, pad)}")
    else:
        print("─" * width)


def _positive_int(value: str) -> int:
    """
    argparse type= for --top-k and --max-tokens. A silent 0 (or negative) used to slice
    every result list down to nothing (--top-k), or price out every match (--max-tokens),
    so a query that matched perfectly still printed "No matches" -- a usage mistake in the
    shape of a real search failure. Reject it at the parser instead.

    Both the non-integer and the non-positive case raise ArgumentTypeError, not a bare
    ValueError, so argparse prints the message as written instead of leaking this helper's
    name ("invalid _positive_int value: 'abc'") into the error a user sees.
    """
    import argparse

    try:
        ivalue = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"must be a whole number, got {value!r}")
    if ivalue < 1:
        raise argparse.ArgumentTypeError(f"must be at least 1, got {value!r}")
    return ivalue


# Human-readable confidence-gate labels, shared by the has-results and the no-results
# output paths so the two can never drift apart.
CONFIDENCE_LABELS: dict[str, str] = {
    "confident": "✓ confident",
    "ambiguous": "~ ambiguous - surface both to user before loading",
    "insufficient": "✗ insufficient - no capability clearly matches; abstain",
}


def cli() -> None:
    import argparse

    # Windows terminals often default stdout to a legacy code page (e.g. cp1252) that
    # cannot encode this module's box-drawing separators or confidence icons, raising a
    # hard UnicodeEncodeError as soon as output is redirected or piped. Reconfiguring to
    # UTF-8 with a replace fallback avoids the crash. Guarded like the sibling repo's CLI:
    # some runtimes swap in a stdout with no reconfigure() (certain captured-output test
    # harnesses -> AttributeError) or one already detached (-> ValueError).
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

    parser = argparse.ArgumentParser(
        prog="skill-registry",
        description="Skill Registry - keyword + tag search",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples (from the skills/registry/ directory):
  python3 skill-registry.py "write this week's report"
  python3 skill-registry.py "review this pull request" --type skill
  python3 skill-registry.py "route this query" --top-k 5
  python3 skill-registry.py "route this query" --confidence
  python3 skill-registry.py "route this query" --confidence --log-gaps
  python3 skill-registry.py --registry skill-registry.template.yaml --stats
  python3 skill-registry.py --list
        """,
    )
    parser.add_argument(
        "query",
        nargs="?",
        help="Natural language search query (what capability do you need?)",
    )
    parser.add_argument(
        "--registry",
        default=None,
        help="Path to skill-registry.yaml (default: same directory as this script)",
    )
    parser.add_argument(
        "--top-k",
        type=_positive_int,
        default=3,
        metavar="N",
        help="Maximum number of results to return (default: 3; must be at least 1)",
    )
    parser.add_argument(
        "--type",
        choices=["skill", "reference", "tool"],
        default=None,
        metavar="TYPE",
        help="Filter results by capability type: skill | reference | tool",
    )
    parser.add_argument(
        "--max-tokens",
        type=_positive_int,
        default=None,
        metavar="N",
        help="Token budget: only return capabilities that fit within N tokens combined (at least 1)",
    )
    parser.add_argument(
        "--min-score",
        type=float,
        default=None,
        metavar="N",
        help=(
            "Minimum relevance score to include in results (default: 0.0 for plain "
            f"search, {DEFAULT_MIN_SCORE} under --confidence, which is what suppresses "
            "low-signal noise there). Pass explicitly to override either default -- "
            "including --min-score 0 to disable filtering even under --confidence. "
            "Does not affect which result is #1."
        ),
    )
    parser.add_argument(
        "--confidence",
        action="store_true",
        help=(
            "Use search_with_confidence() and show the confidence gate "
            "classification (confident / ambiguous / insufficient) with each result."
        ),
    )
    parser.add_argument(
        "--log-gaps",
        action="store_true",
        help=(
            "Append a score-gap record to score-gap-log.jsonl. "
            "Activates A2 monitoring. Use to detect when transition to "
            "a semantic-embedding backend is warranted."
        ),
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show registry statistics and token savings estimate",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all capabilities in the registry",
    )

    args = parser.parse_args()

    # ── Load registry ──────────────────────────────────────────────────────
    try:
        registry = load_registry(args.registry)
    except (FileNotFoundError, ImportError, RegistryError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # ── --stats ────────────────────────────────────────────────────────────
    if args.stats:
        stats = measure_token_savings(registry)
        if not stats:
            print("\n  The registry is empty, so there is nothing to measure yet.")
            print("  Register a capability, then run --stats again.\n")
            return
        _print_separator("Registry Statistics")
        print(f"  Capabilities indexed : {stats['capabilities_indexed']}")
        print(f"    Skills             : {stats['skills']}")
        print(f"    References         : {stats['references']}")
        print(f"    Tools              : {stats['tools']}")
        _print_separator("Token Cost Comparison")
        print(f"  Static loading (all) : {stats['static_total_tokens']:,} tokens")
        print(f"  Dynamic meta-tool    : {stats['dynamic_meta_tool_tokens']} tokens")
        print(f"  Dynamic typical (×3) : {stats['dynamic_typical_session_tokens']:,} tokens")
        print(
            f"  Savings              : {stats['reduction_absolute']:,} tokens "
            f"({stats['reduction_percent']}% reduction)"
        )
        print()
        return

    # ── --list ─────────────────────────────────────────────────────────────
    if args.list:
        skills = [c for c in registry if c.type == "skill"]
        refs = [c for c in registry if c.type == "reference"]
        tools = [c for c in registry if c.type == "tool"]

        _print_separator(f"Skills ({len(skills)})")
        for cap in sorted(skills, key=lambda c: c.name):
            print(f"  {cap.id:<42} {cap.load_cost_tokens:>5} tokens")

        _print_separator(f"References ({len(refs)})")
        for cap in sorted(refs, key=lambda c: c.name):
            print(f"  {cap.id:<42} {cap.load_cost_tokens:>5} tokens")

        if tools:
            _print_separator(f"Tools ({len(tools)})")
            for cap in sorted(tools, key=lambda c: c.name):
                print(f"  {cap.id:<42} {cap.load_cost_tokens:>5} tokens")

        total = sum(c.load_cost_tokens for c in registry)
        print()
        _print_separator()
        print(f"  Total static load : {total:,} tokens across {len(registry)} capabilities")
        print(f"  Discovery meta    : ~{DISCOVERY_TOOL_TOKENS} tokens (flat, regardless of registry size)")
        print()
        return

    # ── Search ─────────────────────────────────────────────────────────────
    if not args.query:
        parser.print_help()
        return

    if args.confidence:
        # A1: use search_with_confidence() for routing decisions. args.min_score is
        # None only when --min-score was never passed -- an explicit --min-score 0 must
        # win here, not be silently promoted to DEFAULT_MIN_SCORE alongside it.
        min_score = DEFAULT_MIN_SCORE if args.min_score is None else args.min_score
        response = search_with_confidence(
            args.query,
            registry,
            top_k=args.top_k,
            capability_type=args.type,
            max_tokens=args.max_tokens,
            min_score=min_score,
            log_gaps=args.log_gaps,
        )
        results = response.results
    else:
        min_score = 0.0 if args.min_score is None else args.min_score
        results = search(
            args.query,
            registry,
            top_k=args.top_k,
            capability_type=args.type,
            max_tokens=args.max_tokens,
            min_score=min_score,
        )
        if args.log_gaps:
            # Log gaps even without --confidence. Same reasoning as
            # search_with_confidence(): assess against the unbudgeted ranking so an
            # unaffordable runner-up still counts against "confident" in the logged
            # record.
            confidence_basis = _confidence_basis(
                args.query, registry, args.top_k, args.type, args.max_tokens, min_score, results
            )
            confidence_for_log = assess_confidence(confidence_basis)
            log_score_gap(args.query, confidence_basis, confidence_for_log)
        response = None

    if not results:
        # An empty result list is not always "insufficient". When --max-tokens priced out
        # the field, the confidence basis (assessed UNBUDGETED -- see _confidence_basis)
        # can still hold a match that cleared the score bar. Hardcoding "insufficient" here
        # would make the CLI contradict its own gate and hand out the wrong next step:
        # "broaden the query" when the query was fine and only the budget was too small.
        if response is not None:
            confidence = response.confidence
            top_score = response.top_score
        else:
            # No --confidence, but a budget can still price out every match on this path.
            # Re-derive the unbudgeted top score so the advice below is honest either way.
            basis = _confidence_basis(
                args.query, registry, args.top_k, args.type, args.max_tokens, min_score, results
            )
            confidence = assess_confidence(basis)
            top_score = basis[0].relevance_score if basis else 0.0

        # --confidence promised a classification: print the real one, not a fixed string.
        if response is not None:
            print(f"\n  Confidence  : {CONFIDENCE_LABELS.get(confidence, confidence)}")

        if top_score > 0:
            # A match cleared the floor; only --max-tokens kept it out of the results, so
            # "broaden the query" would be the wrong advice -- the query matched.
            print(f'\nThe best match for "{args.query}" did not fit --max-tokens {args.max_tokens}.')
            print("  Raise --max-tokens, or drop it, to load that match.")
            return

        print(f'\nNo matches for: "{args.query}"')
        print("  Try broadening the query or removing the --type filter.")
        return

    filter_note = f" [{args.type}]" if args.type else ""
    _print_separator(f'Results for "{args.query}"{filter_note}')

    # Show the confidence banner when --confidence is active
    if response is not None:
        print(f"\n  Confidence  : {CONFIDENCE_LABELS.get(response.confidence, response.confidence)}")
        if response.score_gap is not None:
            print(f"  Score gap   : {response.score_gap:.3f}  (threshold: {CONFIDENCE_GAP_THRESHOLD})")

    for i, match in enumerate(results, 1):
        desc_preview = match.description.strip().replace("\n", " ")
        if len(desc_preview) > 130:
            desc_preview = desc_preview[:130] + "…"

        print(f"\n  {i}. {match.name}  [{match.type}]")
        print(f"     Score     : {match.relevance_score}")
        print(f"     Tokens    : {match.load_cost_tokens:,}")
        print(f"     Location  : {match.location}")
        if match.dependencies:
            print(f"     Co-load   : {', '.join(match.dependencies)}")
        print(f"     {desc_preview}")

    total_loaded = sum(m.load_cost_tokens for m in results)
    print()
    _print_separator()
    print(
        f"  {len(results)} result(s) · {total_loaded:,} tokens to load"
        f"  (vs. {sum(c.load_cost_tokens for c in registry):,} static)"
    )
    if args.log_gaps:
        print("  Gap logged  : score-gap-log.jsonl")
    print()


# ─────────────────────────────────────────────────────────────────────────────
# Public API surface
# (import this module to use search() and load_registry() programmatically)
# ─────────────────────────────────────────────────────────────────────────────

__all__ = [
    "Capability",
    "CapabilityMatch",
    "SearchResponse",
    "RegistryError",
    "load_registry",
    "normalize",
    "search",
    "search_with_confidence",
    "assess_confidence",
    "log_score_gap",
    "track_skill_usage",
    "measure_token_savings",
    "DISCOVERY_TOOL_TOKENS",
    "DEFAULT_MIN_SCORE",
    "CONFIDENCE_SCORE_THRESHOLD",
    "CONFIDENCE_GAP_THRESHOLD",
    "AMBIGUOUS_MIN_SCORE",
    "GAP_LOG_PATH",
]

if __name__ == "__main__":
    cli()
