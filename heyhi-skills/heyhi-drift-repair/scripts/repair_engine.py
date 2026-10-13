"""
heyhi-drift-repair — the repair engine (deployed 2026-09-04; seed-substrate self-contained).

The "act" verb of Sheerline's retrieve -> validate -> grade -> learn loop
(plans/plan-drift-repair-loop-2026-08-29.md). Given LOCATED drift/accessibility
findings, per finding it classifies on the `detection` axis and either
auto-applies a pre-registered structural transform (re-validated, with a
reversible deviation record) or proposes a human-confirm candidate — writing
nothing it cannot mechanically verify.

DELEGATION BOUNDARY (read this before trusting the engine)
----------------------------------------------------------
The spec's rule is "never re-implement detection" and "do not invent a second
matcher". At DEPLOYMENT:
  * match_correction  -> heyhi_mcp.corrections.predicates.evaluate_predicate over
                         the instance's live registry.
  * re-validation     -> heyhi_mcp.core.validator.validate_output(..., constraints=
                         <instance known_tokens / legal_contrast_pairs>).
This engine takes findings PRE-LOCATED (matching is upstream, per the spec's
"findings arrive located") and re-validates with a focused conformance re-scan of
the repaired region. That is the seed-substrate stand-in the seed library itself
describes ("the fallback substrate the readers fall back to when no live registry
is present", seed-corrections.yaml:6-11). The apply step — a value -> token-
reference substitution derived from the known_bad/expected pair — is the repair,
not detection, and is identical in both modes.

No heyhi_mcp import: the staged artifact runs in isolation (stdlib + optional
pyyaml). Nothing here writes the live corrections registry; the learn step only
AUTHORS a corrections-intake candidate (write_learn_candidate is a deployment
helper, never called by the eval).

classification: HeyHi Confidential
"""

from __future__ import annotations

import datetime as _dt
import re
from dataclasses import dataclass, field, asdict
from typing import Any, Optional


# ── literal detectors, keyed by drift kind ───────────────────────────────────
# Used ONLY by re-validation to confirm a repaired declaration introduced no new
# raw literal (var(...) references are stripped first). This is a conformance
# re-scan of the repaired span, NOT a from-scratch re-detection.
_LITERAL_PATTERNS: dict[str, str] = {
    "color": r"#[0-9a-fA-F]{3,8}\b|\brgb\(|\bhsl\(",
    "dimension": r"\b\d*\.?\d+(px|rem|em)\b",
    "duration": r"\b\d*\.?\d+(ms|s)\b",
    "easing": r"cubic-bezier\(",
    "number": r"\b\d+\b",
}

#: HeyHi's own seed token names — the isolation test asserts NONE of these leak
#: into a tenant repair. Derived from seed-corrections.yaml's `expected` values.
HEYHI_TOKEN_NAMES: frozenset[str] = frozenset(
    {
        "--text-primary",
        "--space-4",
        "--z-modal",
        "--font-size-base",
        "--font-weight-semibold",
        "--font-lineHeight-relaxed",
        "--motion-duration-200",
        "--motion-easing-ease-in-out",
        "--border-width-thick",
    }
)


# ── result records ────────────────────────────────────────────────────────────
@dataclass
class Applied:
    """A landed, re-validated deterministic repair with its deviation record."""

    finding: str
    matched_correction: str
    surface: str
    location: str
    before: str
    after: str
    provenance: str = "automated"
    revalidated: bool = True
    confirmed: bool = False  # flips only on a human's review, never here
    timestamp: str = ""

    def deviation_record(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Proposal:
    """A human-confirm candidate. Nothing is written for a proposal."""

    finding: str
    matched_correction: Optional[str]
    detection: Optional[str]
    provenance: str  # "[candidate: needs confirmation]" | "[inferred]"
    reason: str
    target: Optional[str] = None  # "code" | "token-source" | None
    ready_transform: Optional[tuple[str, str]] = None  # (old, new) when known
    needs_human_confirm: bool = True
    promotion_eligible: bool = False
    named_gate: str = "Repair-confirmation sign-off"


@dataclass
class LearnCandidate:
    """A schema-shaped corrections-intake candidate. AUTHORED, never filed here.

    Superset of what insight-activation emits: it carries the design-extension
    fields (detection / predicate / known_bad / expected) because the repair loop
    owns the transform it just applied (spec OQ-3 recommendation (a)).
    """

    id: str
    category: str
    severity: str
    detection: str
    trigger_context: str
    correction: str
    predicate: Optional[dict[str, Any]]
    known_bad: Optional[str]
    expected: Optional[str]
    status: str = "proposed"
    decide_to_adopt: str = ""  # EMPTY — the human curator's slot
    times_fired: int = 0


@dataclass
class RunResult:
    mode: str
    findings_in: int
    applied: list[Applied] = field(default_factory=list)
    proposals: list[Proposal] = field(default_factory=list)
    learn_candidates: list[LearnCandidate] = field(default_factory=list)
    artifacts: dict[str, str] = field(default_factory=dict)  # post-run surfaces


# ── library loading ────────────────────────────────────────────────────────────
def load_library(path: str) -> dict[str, dict[str, Any]]:
    """Load a corrections registry (the seed substrate or a live/tenant registry),
    keyed by id. Reads the LIVE file by path so the repair library cannot drift
    from a stale copy."""
    try:
        import yaml  # type: ignore
    except ModuleNotFoundError as exc:  # pragma: no cover
        raise SystemExit(
            "repair_engine needs PyYAML to read a registry file. "
            "Install it, or pass an in-memory library dict to run()."
        ) from exc
    with open(path, encoding="utf-8") as fh:
        doc = yaml.safe_load(fh)
    entries = (doc or {}).get("entries", [])
    return {e["id"]: e for e in entries if isinstance(e, dict) and "id" in e}


# ── the value-level transform ───────────────────────────────────────────────
def value_delta(known_bad: str, expected: str) -> tuple[str, str]:
    """The minimal differing span between the known_bad and expected snippets —
    i.e. the literal-value -> token-reference swap. Selector-agnostic: the pair's
    selector is illustrative, the delta is the fix."""
    i = 0
    while i < len(known_bad) and i < len(expected) and known_bad[i] == expected[i]:
        i += 1
    j = 0
    while (
        j < len(known_bad) - i
        and j < len(expected) - i
        and known_bad[-1 - j] == expected[-1 - j]
    ):
        j += 1
    old = known_bad[i : len(known_bad) - j]
    new = expected[i : len(expected) - j]
    return old, new


def _decl_fragments(known_bad: str, expected: str) -> tuple[str, str]:
    """The property-scoped `prop: value` fragment of each snippet, selector and
    braces stripped. Property-scoping is what keeps the apply LOCATION-faithful:
    two declarations can share a literal (`padding: 16px` and `font-size: 16px`),
    so a bare value-replace would misapply a token — the `prop:` prefix
    disambiguates. In deployment the finding's line/column locates the site;
    here the fragment is the location stand-in."""

    def frag(s: str) -> str:
        m = re.search(r"\{(.*)\}", s, re.S)
        inner = m.group(1) if m else s
        return inner.strip().rstrip(";").strip()

    return frag(known_bad), frag(expected)


def _candidate_tokens(corr: dict[str, Any]) -> list[str]:
    """The canonical token(s) a literal resolves to. A single `expected` -> one
    candidate (the 1:1 case). An explicit `candidates` list of length > 1 is the
    ambiguous instance case that downgrades to a proposal (precondition 1)."""
    cands = corr.get("candidates")
    if isinstance(cands, list) and cands:
        return list(cands)
    if corr.get("expected") and corr.get("known_bad"):
        _, new = value_delta(corr["known_bad"], corr["expected"])
        return [new]
    return []


def _introduces_literal(new_decl: str, drift_kind: str) -> bool:
    """True if the repaired declaration STILL contains a raw literal of its kind
    after var(...) references are stripped. The conformance half of re-validation."""
    stripped = re.sub(r"var\([^)]*\)", "", new_decl)
    pattern = _LITERAL_PATTERNS.get(drift_kind)
    return bool(pattern and re.search(pattern, stripped))


#: LIFECYCLE.md generic promotion floor: 5+ TOTAL fires. (The other arm — the same
#: pattern across 3+ separate sessions — is not visible to a single run, so the
#: fires arm governs here.)
_PROMOTION_FIRE_THRESHOLD = 5


def _promotion_eligible(corr: dict[str, Any]) -> bool:
    """Surface (never take) a promotion. FACTUAL only (LIFECYCLE.md). Heuristic
    stand-in for the curator's call: the generic lifecycle floor of 5+ total fires.
    A per-correction promotion clause (e.g. the contrast seed's own stricter 3-fire
    clause) is read at DEPLOYMENT; here the generic floor governs so the engine
    never over-flags. The contrast seed (factual, times_fired 6) clears it; a fresh
    factual entry at 0-4 fires does not."""
    return (
        corr.get("severity") == "factual"
        and int(corr.get("times_fired", 0) or 0) >= _PROMOTION_FIRE_THRESHOLD
    )


def _drift_kind(corr: dict[str, Any]) -> str:
    """Map a correction's predicate type to a literal-detector key."""
    ptype = (corr.get("predicate") or {}).get("type", "")
    return {
        "literal_color": "color",
        "off_scale_dimension": "dimension",
        "off_token_number": "number",
        "off_token_duration": "duration",
        "off_token_easing": "easing",
    }.get(ptype, "dimension")


# ── the engine ────────────────────────────────────────────────────────────────
def run(
    findings: list[dict[str, Any]],
    artifacts: dict[str, str],
    library: dict[str, dict[str, Any]],
    *,
    auto_apply: bool = False,
    now: str = "1970-01-01T00:00:00Z",
) -> RunResult:
    """Execute the per-finding routing (SKILL.md Steps 2-4, 6).

    `auto_apply=False` is the spec's proposal-first default (OQ-2): even a
    deterministic-unambiguous finding is PROPOSED (transform attached) and nothing
    is written. Auto-apply is the explicit per-engagement opt-in.

    `artifacts` is mutated in place ONLY on an auto-apply that re-validates; the
    same dict is returned as result.artifacts so idempotence can re-run on the
    output.
    """
    work = dict(artifacts)  # copy: only auto-applied, re-validated repairs mutate
    res = RunResult(
        mode="auto-apply" if auto_apply else "proposal-first",
        findings_in=len(findings),
        artifacts=work,
    )

    for f in findings:
        fid = f.get("id", "<finding>")
        corr = library.get(f.get("matched_correction"))
        drift_class = f.get("drift_class", "call-site")

        # No matched correction -> novel drift -> propose with [inferred].
        if corr is None:
            res.proposals.append(
                Proposal(
                    finding=fid,
                    matched_correction=None,
                    detection=None,
                    provenance="[inferred]",
                    reason="novel drift — no registered transform",
                    ready_transform=(f.get("literal"), f.get("suggestion"))
                    if f.get("suggestion")
                    else None,
                )
            )
            continue

        detection = corr.get("detection")

        # Token-definition drift routes to the token source (target A) — PROPOSED
        # as a single-source diff, never a smear of N call-sites. v1 never
        # auto-writes A. Independent of detection.
        if drift_class == "token-definition":
            res.proposals.append(
                Proposal(
                    finding=fid,
                    matched_correction=corr["id"],
                    detection=detection,
                    provenance="[candidate: needs confirmation]",
                    reason="token-definition drift → single-source diff for human "
                    "approval (v1 proposes target A, never auto-writes it)",
                    target="token-source",
                )
            )
            _maybe_learn(res, f, corr)
            continue

        if detection == "deterministic":
            cands = _candidate_tokens(corr)
            # Precondition 1: value must resolve to exactly one canonical token.
            if len(cands) != 1:
                res.proposals.append(
                    Proposal(
                        finding=fid,
                        matched_correction=corr["id"],
                        detection=detection,
                        provenance="[inferred]",
                        reason="value resolves to >1 canonical token — which token "
                        "the site intended is a semantic-role call",
                        target="code",
                    )
                )
                _maybe_learn(res, f, corr)
                continue

            old, new = value_delta(corr["known_bad"], corr["expected"])

            # Spec §5.1: only an `error`-tier finding is auto-apply-eligible. A
            # `warning` / `suggestion` tier is advisory and PROPOSES, never
            # auto-applies, regardless of detection — the guarantee is enforced
            # here, not left to the accident that today's warnings happen to map
            # to judged corrections.
            tier = f.get("source_tier", "error")
            if tier != "error":
                res.proposals.append(
                    Proposal(
                        finding=fid,
                        matched_correction=corr["id"],
                        detection=detection,
                        provenance="[candidate: needs confirmation]",
                        reason=f"{tier}-tier finding is advisory — propose-only, "
                        "never auto-apply (spec §5.1)",
                        target="code",
                        ready_transform=(old, new),
                    )
                )
                _maybe_learn(res, f, corr)
                continue

            # Proposal-first default: propose with the ready transform, write nothing.
            if not auto_apply:
                res.proposals.append(
                    Proposal(
                        finding=fid,
                        matched_correction=corr["id"],
                        detection=detection,
                        provenance="[candidate: needs confirmation]",
                        reason="proposal-first mode (auto-apply is an explicit "
                        "engagement opt-in)",
                        target="code",
                        ready_transform=(old, new),
                    )
                )
                _maybe_learn(res, f, corr)
                continue

            # AUTO-APPLY (opt-in): target B, the call-site. Property-scoped so a
            # shared literal (padding: 16px vs font-size: 16px) can't misapply.
            old_frag, new_frag = _decl_fragments(corr["known_bad"], corr["expected"])
            surface = f.get("surface")
            if not surface:
                # Malformed finding: no located surface. Degrade to a proposal
                # rather than crash the run — nothing is silently dropped.
                res.proposals.append(
                    Proposal(
                        finding=fid,
                        matched_correction=corr["id"],
                        detection=detection,
                        provenance="[candidate: needs confirmation]",
                        reason="no surface located — cannot auto-apply; proposed for manual fix",
                        target="code",
                        ready_transform=(old, new),
                    )
                )
                _maybe_learn(res, f, corr)
                continue
            text = work.get(surface, "")
            if old_frag not in text:
                # Located declaration absent — nothing to apply. Not a false
                # repair; also the idempotence path (a prior run already fixed it).
                continue
            new_text = text.replace(old_frag, new_frag, 1)  # deploy: replace AT location

            # Step 4: re-validate. Originating declaration gone AND no new literal.
            region_clean = old_frag not in new_text
            no_new_literal = not _introduces_literal(new_frag, _drift_kind(corr))
            if region_clean and no_new_literal:
                work[surface] = new_text
                res.applied.append(
                    Applied(
                        finding=fid,
                        matched_correction=corr["id"],
                        surface=surface,
                        location=f.get("location", ""),
                        before=old_frag,
                        after=new_frag,
                        timestamp=now,
                    )
                )
                _maybe_learn(res, f, corr)
            else:
                # Roll back (never wrote work[surface]) + downgrade to a proposal.
                res.proposals.append(
                    Proposal(
                        finding=fid,
                        matched_correction=corr["id"],
                        detection=detection,
                        provenance="[candidate: needs confirmation]",
                        reason="re-validation failed — rolled back, no write",
                        target="code",
                        ready_transform=(old, new),
                    )
                )

        elif detection == "judged":
            res.proposals.append(
                Proposal(
                    finding=fid,
                    matched_correction=corr["id"],
                    detection=detection,
                    provenance="[candidate: needs confirmation]",
                    reason="judged — a human decides (never auto-applied, no "
                    "confidence-threshold override)",
                    promotion_eligible=_promotion_eligible(corr),
                )
            )
            _maybe_learn(res, f, corr)

        elif detection == "hybrid":
            # v1: no seeded hybrid carries an emitted-code structural transform,
            # so propose-both.
            res.proposals.append(
                Proposal(
                    finding=fid,
                    matched_correction=corr["id"],
                    detection=detection,
                    provenance="[candidate: needs confirmation]",
                    reason="hybrid — v1 propose-both (no registered emitted-code "
                    "structural transform to auto-apply)",
                )
            )
            _maybe_learn(res, f, corr)

    return res


def _maybe_learn(res: RunResult, finding: dict[str, Any], corr: dict[str, Any]) -> None:
    """Author a learn candidate when the caller flags the finding as recurring
    (cross-session dedup is upstream; the engine authors when told it recurs).
    Never files it — that is a deployment step behind the human firewall."""
    if not finding.get("recurring"):
        return
    res.learn_candidates.append(
        LearnCandidate(
            id=corr["id"],
            category=corr.get("category", ""),
            severity=corr.get("severity", "factual"),
            detection=corr.get("detection", ""),
            trigger_context=corr.get("trigger_context", ""),
            correction=corr.get("correction", ""),
            predicate=corr.get("predicate"),
            known_bad=corr.get("known_bad"),
            expected=corr.get("expected"),
            times_fired=int(corr.get("times_fired", 0) or 0),
        )
    )


def write_learn_candidate(cand: LearnCandidate, intake_dir: str) -> str:  # pragma: no cover
    """DEPLOYMENT ONLY — write a corrections-intake candidate (never the live
    registry, never sheerline/os/corrections/). Not called by the eval. The
    decide-to-adopt slot is left empty for the human curator."""
    import os

    today = _dt.date.today().isoformat()
    path = os.path.join(intake_dir, f"{today}-{cand.id}.md")
    body = (
        f"# {cand.id} — drift-repair learn candidate\n\n"
        f"**Date:** {today}   **Status:** proposed\n\n"
        f"## Candidate correction (schema-shaped — a proposal, not an adopted entry)\n"
        f"  id: {cand.id}\n  category: {cand.category}\n  severity: {cand.severity}\n"
        f"  detection: {cand.detection}\n  trigger_context: {cand.trigger_context}\n"
        f"  correction: {cand.correction}\n  known_bad: {cand.known_bad}\n"
        f"  expected: {cand.expected}\n  times_fired: {cand.times_fired}\n\n"
        f"## ⛔ Decide-to-adopt — NEEDS THE HUMAN CURATOR\n{cand.decide_to_adopt}\n"
    )
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body)
    return path
