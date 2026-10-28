---
title: "Conformance sub-area: calibration record (blank slot)"
status: unrecorded
recorded_by: null
recorded_on: null
gate: G2
sub_area_spec: heyhi-skills/heyhi-design-intelligence-audit/references/conformance-sub-area.md
fixtures: []
---

# Conformance sub-area: calibration record (blank slot)

This is the generic default for the `audit.conformance-calibration` slot. It holds no
calibration. An instance records its own here, in its instance root, before it treats a
conformance verdict as calibrated.

**What the record proves (Gate G2).** The audit's conformance sub-area produces a correct,
discriminating verdict on a known-good and known-bad pair authored against the instance's own
DESIGN.md, with zero false positives on the instance's documented signatures.

## How an instance fills this slot

1. Author two fixtures against the instance's own DESIGN.md: a known-good generation that
   honors it, and a known-bad generation that carries the anti-tells the audit reads (visual,
   structural, token-level, and state-level tells; keep it free of banned words and client
   names so it still passes the voice and hermetic scans).
2. Run the four axes from `conformance-sub-area.md` on each: the functional floor through
   `validate_output` against the instance's own token set, then intent adherence, the
   anti-tell scan, and fundamentals adherence, each rendered and read.
3. Record every `validate_output` result verbatim, every rendered observation, and the verdict
   for each fixture. G2 is met only when the known-good conforms, the known-bad drifts, and no
   documented signature of the instance fires.
4. Fill `status`, `recorded_by`, `recorded_on`, and `fixtures` in this frontmatter, and point
   the instance's `instance.yaml` at the filled record.

## Record

| Fixture | File | Verdict | Evidence |
|---|---|---|---|
| Known-good | | | |
| Known-bad | | | |

---

*The blank G2 calibration slot; an instance records its own run.*
