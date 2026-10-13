#!/usr/bin/env python3
"""
heyhi-drift-repair — runnable eval harness.

Proves the spec's §8 acceptance criteria (plans/plan-drift-repair-loop-2026-08-29.md)
on fixtures, using the LIVE seed repair library so the transforms cannot drift from a
stale copy. Run:

    python3 heyhi-skills/heyhi-drift-repair/evals/run.py

Exit 0 iff every check passes; prints a PASS/FAIL table. This is the mechanical
half of the acceptance set; evals/cases.yaml carries the same criteria in the
Sheerline agent-judged format.

classification: HeyHi Confidential
"""
from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve()
_SKILL = _HERE.parents[1]
_REPO = _HERE.parents[3]
sys.path.insert(0, str(_SKILL / "scripts"))

import repair_engine as E  # noqa: E402

try:
    import yaml
except ModuleNotFoundError:
    print("FAIL: PyYAML not importable. Run under the project venv "
          "(the one that runs heyhi-mcp).")
    sys.exit(2)

SEED = _REPO / "heyhi-mcp/heyhi_mcp/corrections/seed-corrections.yaml"
FIX = _SKILL / "evals/fixtures"

_results: list[tuple[str, bool, str]] = []


def check(name: str, passed: bool, detail: str = "") -> None:
    _results.append((name, bool(passed), detail))


def load_text(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def main() -> int:
    seed_lib = E.load_library(str(SEED))
    drifted = load_text(FIX / "drifted.css")
    clean = load_text(FIX / "clean.css")
    findings = yaml.safe_load(load_text(FIX / "findings.yaml"))["findings"]
    det9 = [f for f in findings if f["id"] in {f"F{i}" for i in range(1, 10)}]

    # sanity: the live seed carries the 9 deterministic + the judged/hybrid block
    check(
        "seed library loaded (9 deterministic transforms present)",
        all(
            seed_lib.get(i, {}).get("detection") == "deterministic"
            and seed_lib[i].get("known_bad")
            for i in (
                "hardcoded-hex-bypasses-token",
                "off-scale-spacing-value",
                "raw-zindex-bypasses-elevation-token",
                "hardcoded-font-size-bypasses-type-token",
                "hardcoded-font-weight-bypasses-type-token",
                "hardcoded-line-height-bypasses-type-token",
                "hardcoded-duration-bypasses-motion-token",
                "hardcoded-easing-bypasses-motion-token",
                "hardcoded-border-width-bypasses-token",
            )
        ),
        f"loaded {len(seed_lib)} entries from the live seed registry",
    )

    # ── main run: all 12 findings, auto-apply ────────────────────────────────
    M = E.run(findings, {"drifted.css": drifted, "artifact.json": '{"states":{}}'},
              seed_lib, auto_apply=True, now="2026-09-01T00:00:00Z")

    # C1 — round-trip discrimination -----------------------------------------
    c1 = (
        len(M.applied) == 9
        and M.artifacts["drifted.css"] == clean          # aggregate byte-equal
        and "padding: 16px" in drifted                    # finding fires on known_bad
        and "padding: 16px" not in M.artifacts["drifted.css"]  # gone after repair
    )
    # per-finding: each applied `after` equals the seed's expected fragment
    per = all(
        E._decl_fragments(seed_lib[a.matched_correction]["known_bad"],
                          seed_lib[a.matched_correction]["expected"])[1] == a.after
        for a in M.applied
    )
    check("C1 round-trip discrimination (known_bad→expected, revert re-fires)",
          c1 and per, f"{len(M.applied)}/9 applied; drifted repaired == clean.css")

    # C2 — false-repair floor -------------------------------------------------
    empty = E.run([], {"clean.css": clean}, seed_lib, auto_apply=True)
    mispointed = E.run(
        [dict(f, surface="clean.css") for f in det9],
        {"clean.css": clean}, seed_lib, auto_apply=True,
    )
    check("C2 false-repair floor (clean input → zero repairs, zero proposals)",
          len(empty.applied) == 0 and len(empty.proposals) == 0
          and empty.artifacts["clean.css"] == clean
          and len(mispointed.applied) == 0 and len(mispointed.proposals) == 0,
          "empty-findings run and 9-findings-on-clean run both produce 0/0")

    # C3 — boundary assertion (judged writes NOTHING) -------------------------
    judged = next(f for f in findings if f["id"] == "F10")
    before = {"drifted.css": drifted}
    B = E.run([judged], dict(before), seed_lib, auto_apply=True)
    check("C3 boundary assertion (detection:judged → propose, no write)",
          len(B.applied) == 0 and len(B.proposals) == 1
          and B.proposals[0].provenance == "[candidate: needs confirmation]"
          and B.proposals[0].needs_human_confirm is True
          and B.artifacts == before,
          "contrast finding proposed with human-confirm flag; no file changed")

    # C4 — idempotence --------------------------------------------------------
    r1 = E.run(det9, {"drifted.css": drifted}, seed_lib, auto_apply=True)
    r2 = E.run(det9, r1.artifacts, seed_lib, auto_apply=True)
    check("C4 idempotence (second auto-apply run → zero new auto-applies)",
          len(r1.applied) == 9 and len(r2.applied) == 0
          and r2.artifacts == r1.artifacts,
          f"run1={len(r1.applied)} applied, run2={len(r2.applied)} applied")

    # C5 — token-source propagation -------------------------------------------
    td_lib = dict(seed_lib)
    td_lib["brand-color-off-system"] = {
        "id": "brand-color-off-system", "category": "token-fidelity",
        "severity": "factual", "detection": "judged",
        "predicate": {"type": "contrast_pairing", "surface": "json_artifact"},
    }
    td_finding = {"id": "TD1", "surface": "tokens.dtcg.json",
                  "location": "color.brand.accent", "drift_kind": "color",
                  "drift_class": "token-definition",
                  "matched_correction": "brand-color-off-system"}
    src = {"tokens.dtcg.json": '{"color":{"brand":{"accent":{"$value":"#3A5FCD"}}}}',
           "drifted.css": drifted}
    TD = E.run([td_finding], dict(src), td_lib, auto_apply=True)
    callsite_targets_code = all(a.surface.endswith(".css") for a in M.applied)
    check("C5 token-source propagation (value drift → single-source diff, not N sites)",
          len(TD.applied) == 0 and len(TD.proposals) == 1
          and TD.proposals[0].target == "token-source"
          and TD.artifacts == src            # neither the source nor call-sites touched
          and callsite_targets_code,          # call-site fixes write code, not the source
          "token-definition proposed against the source (v1 does not auto-write A)")

    # C6 — post-repair re-validation / rollback -------------------------------
    br_lib = {"broken-zindex": {
        "id": "broken-zindex", "category": "elevation", "severity": "factual",
        "detection": "deterministic",
        "predicate": {"type": "off_token_number", "surface": "emitted_css"},
        "known_bad": ".x { z-index: 400; }", "expected": ".x { z-index: 401; }"}}
    br_finding = {"id": "BR1", "surface": "x.css", "location": ".x / z-index",
                  "drift_kind": "number", "drift_class": "call-site",
                  "matched_correction": "broken-zindex"}
    br_art = {"x.css": ".x { z-index: 400; }"}
    BR = E.run([br_finding], dict(br_art), br_lib, auto_apply=True)
    goodpath = all(a.revalidated for a in M.applied)  # the 9 real repairs re-validated
    check("C6 post-repair re-validation (bad transform rolled back; good lands)",
          len(BR.applied) == 0 and len(BR.proposals) == 1
          and "rolled back" in BR.proposals[0].reason
          and BR.artifacts == br_art          # rolled back → file unchanged
          and goodpath,
          "a transform that leaves a literal is rolled back; the 9 clean ones held")

    # C7 — instance isolation --------------------------------------------------
    tenant_lib = {"tenant-hex": {
        "id": "tenant-hex", "category": "token-fidelity", "severity": "factual",
        "detection": "deterministic",
        "predicate": {"type": "literal_color", "surface": "emitted_css"},
        "known_bad": ".t { color: #000000; }",
        "expected": ".t { color: var(--tenant-ink); }"}}
    t_finding = {"id": "T1", "surface": "tenant.css", "location": ".t / color",
                 "drift_kind": "color", "drift_class": "call-site",
                 "matched_correction": "tenant-hex"}
    T = E.run([t_finding], {"tenant.css": ".t { color: #000000; }"},
              tenant_lib, auto_apply=True)
    blob = " ".join(a.after for a in T.applied) + " ".join(
        f"{p.reason}{p.ready_transform}" for p in T.proposals)
    no_heyhi = not any(name in blob for name in E.HEYHI_TOKEN_NAMES)
    check("C7 instance isolation (no HeyHi token name in a tenant repair)",
          len(T.applied) == 1 and "--tenant-ink" in T.applied[0].after and no_heyhi,
          "tenant run uses the tenant registry only; no HeyHi token leaked")

    # C8 — provenance + deviation present -------------------------------------
    dev_ok = all(
        a.provenance == "automated" and a.revalidated and a.confirmed is False
        and all(a.deviation_record().get(k) for k in
                ("finding", "matched_correction", "surface", "before", "after", "timestamp"))
        for a in M.applied
    )
    prop_ok = all(
        p.provenance in ("[candidate: needs confirmation]", "[inferred]")
        for p in M.proposals
    )
    check("C8 provenance + deviation present (applied=automated+record; proposals labeled)",
          dev_ok and prop_ok and len(M.proposals) == 3,
          f"{len(M.applied)} deviation records complete; {len(M.proposals)} proposals labeled")

    # bonus — learn candidate authored with the design-extension fields (OQ-3) -
    lc = next((c for c in M.learn_candidates if c.id == "hardcoded-hex-bypasses-token"), None)
    check("OQ-3 learn candidate authored (detection/known_bad/expected, decide slot empty)",
          lc is not None and lc.detection == "deterministic"
          and bool(lc.known_bad) and bool(lc.expected)
          and lc.status == "proposed" and lc.decide_to_adopt == "",
          "recurring finding authored a schema-superset intake candidate, unfiled")

    # bonus — OQ-4 over-threshold contrast surfaced (never taken) --------------
    contrast_prop = next((p for p in B.proposals
                          if p.matched_correction == "contrast-pairing-not-declared-safe"), None)
    check("OQ-4 over-threshold contrast surfaced as promotion-eligible (not taken)",
          contrast_prop is not None and contrast_prop.promotion_eligible is True,
          "contrast seed at times_fired 6 flagged for the curator, not promoted")

    # C9 — proposal-first DEFAULT (OQ-2 safe default) writes nothing ----------
    PF = E.run(det9, {"drifted.css": drifted}, seed_lib)  # auto_apply defaults to False
    check("C9 proposal-first default (OQ-2 safe default → propose all, write nothing)",
          PF.mode == "proposal-first" and len(PF.applied) == 0 and len(PF.proposals) == 9
          and all(p.ready_transform for p in PF.proposals)
          and all(p.provenance == "[candidate: needs confirmation]" for p in PF.proposals)
          and PF.artifacts["drifted.css"] == drifted,
          "9 deterministic findings proposed with ready transforms; file byte-unchanged")

    # C10 — precondition 1: value resolving to >1 canonical token → [inferred] -
    amb_lib = {"ambiguous-spacing": {
        "id": "ambiguous-spacing", "category": "spacing-scale", "severity": "factual",
        "detection": "deterministic",
        "predicate": {"type": "off_scale_dimension", "surface": "emitted_css"},
        "known_bad": ".x { gap: 8px; }", "expected": ".x { gap: var(--space-2); }",
        "candidates": ["var(--space-2)", "var(--space-2-alt)"]}}
    amb_finding = {"id": "AMB1", "surface": "x.css", "location": ".x / gap",
                   "drift_kind": "dimension", "drift_class": "call-site",
                   "matched_correction": "ambiguous-spacing"}
    amb_art = {"x.css": ".x { gap: 8px; }"}
    AMB = E.run([amb_finding], dict(amb_art), amb_lib, auto_apply=True)
    check("C10 ambiguity guard (deterministic but value→>1 token → [inferred], no write)",
          len(AMB.applied) == 0 and len(AMB.proposals) == 1
          and AMB.proposals[0].provenance == "[inferred]"
          and AMB.artifacts == amb_art,
          "which token the site intended is a human call, not an auto-apply (precondition 1)")

    # C11 — spec §5.1: a warning/suggestion-tier finding NEVER auto-applies -----
    warn_f = [{"id": "W1", "surface": "w.css", "location": ".card / padding",
               "drift_kind": "dimension", "drift_class": "call-site",
               "matched_correction": "off-scale-spacing-value", "source_tier": "warning"}]
    warn_art = {"w.css": ".card { padding: 16px; }"}
    W = E.run(warn_f, dict(warn_art), seed_lib, auto_apply=True)
    check("C11 warning-tier never auto-applies (spec §5.1: advisory → propose only)",
          len(W.applied) == 0 and len(W.proposals) == 1
          and W.artifacts == warn_art
          and "advisory" in W.proposals[0].reason,
          "a deterministic finding tagged source_tier=warning is proposed, not written")

    # C12 — a malformed finding (no surface) degrades to a proposal, not a crash --
    try:
        NS = E.run([{"id": "NS1", "location": "x", "drift_class": "call-site",
                     "matched_correction": "off-scale-spacing-value"}],
                   {"x.css": ".card { padding: 16px; }"}, seed_lib, auto_apply=True)
        ns_ok = len(NS.applied) == 0 and len(NS.proposals) == 1 and NS.artifacts == {
            "x.css": ".card { padding: 16px; }"}
    except Exception:
        ns_ok = False
    check("C12 robustness (finding missing 'surface' → proposed, no crash, no write)",
          ns_ok, "a malformed finding degrades to a proposal instead of raising KeyError")

    # ── report ────────────────────────────────────────────────────────────────
    width = max(len(n) for n, _, _ in _results)
    print("\n  heyhi-drift-repair · acceptance harness\n  " + "─" * (width + 10))
    passed = 0
    for name, ok, detail in _results:
        mark = "PASS" if ok else "FAIL"
        passed += ok
        print(f"  [{mark}] {name.ljust(width)}   {detail}")
    print("  " + "─" * (width + 10))
    print(f"  {passed}/{len(_results)} checks passed\n")
    return 0 if passed == len(_results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
