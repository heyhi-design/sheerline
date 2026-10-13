---
classification: confidential
title: "Sheerline Eval Cases"
adapted_from: releases/open-source/keel/skills/evals/README.md
---

# Sheerline Eval Cases

Each governed capability ships a small set of eval cases, one `cases.yaml` per capability. A case is a known input paired with the result a working capability should produce. Adapted from keel's `skills/evals/` (the R4 pattern). In Phase 1 the cases probe **governance** (does the discipline hold), since P1 authors no new skills; from P1.5 each net-new skill ships its own cases before it is trusted.

## What a case is

| Field | What it is |
|---|---|
| `id` | A unique name (unique across every capability's cases). |
| `description` | The specific behavior the case is meant to catch. |
| `input` | The material handed to the capability. |
| `expected_findings` | What a working capability should report. An empty list is a real expectation: a correct capability finds nothing wrong here. |
| `pass_criteria` | The bar the result must clear, stated specifically. |

An optional `fixture` field sets up a case whose input needs something first.

## How to run a case

These cases are run by hand or by the agent, not by an automated harness (a design capability's output is prose to be judged, not a value compared byte for byte). Read the input, apply the capability's own procedure, compare against `expected_findings`, decide pass or fail by `pass_criteria`. Run a capability's cases when you first govern or fill it, and again whenever it changes.

The provided scaffold, `visual-design-governance/cases.yaml`, is a worked example: it probes the Phase-1 governance of the Visual Design foundation (reference-not-copy, advisory-never-gate, the fundamentals-fold wiring). Copy its shape for each new capability.

`INDEX.md` lists every governed capability and its eval home, and `python3 measure_coverage.py` re-measures the `eval-coverage` signal from those homes (exit 1 if any governed skill has none; `--emit-index` regenerates the index).

A sibling meter, `python3 measure_maturity.py`, reports the practice-**capability** instrument rather than eval coverage: it reads the per-area `maturity` blocks in `os/foundations/registry.yaml` and prints the achievement / target / delta profile (`--emit-profile`), plus advisory `NEEDS-REGRADE` / `POSSIBLE-REGRESSION` flags. It is advisory by construction (zero gate rules, always exits 0 on a successful read) and read-only on the registry. The scale and evidence classes it reports live in `os/foundations/maturity/`.

---

*Skills overview: `skills/README.md` · The R4 pattern source: `releases/open-source/keel/skills/evals/`*

*HeyHi Confidential*
