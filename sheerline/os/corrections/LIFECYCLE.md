---
classification: confidential
title: "Sheerline Corrections Lifecycle"
adapted_from: releases/open-source/keel/os/corrections/LIFECYCLE.md
---

# Sheerline Corrections Lifecycle

How a design correction moves from a one-off note to a hard rule, and how it retires. Adapted from keel's `os/corrections/LIFECYCLE.md` (the mechanism ports unchanged; the factual/behavioral boundary is the design-scoped tightening). This is the convention; the runtime is the internal `heyhi-mcp` (Phase 2 / DISPATCH-02).

The point is compounding institutional memory. A mistake caught once is a note. The same mistake caught a third time is a pattern worth encoding so no future session pays for it again.

---

## The three statuses

A correction is always in exactly one state.

| Status | Meaning |
|---|---|
| **active** | In force. Agents load it at session start and honor it. |
| **superseded** | A stronger mechanism (usually a promoted hard rule) now covers this pattern. Kept for provenance, carries `superseded_by`, no longer loads as active guidance. |
| **retired** | The pattern no longer applies (a tool changed, a workflow is gone). Kept for the record, not loaded. |

`promoted` is an *action*, not a status. When a correction earns a permanent rule, promote it (write the rule into `os/session-rules.md` or `os/operating-principles.md`), then mark the entry `superseded` with `superseded_by` pointing at the rule's home.

---

## The factual / behavioral boundary (the design-scoped tightening)

Sheerline's severity vocabulary is exactly two values, `factual` and `behavioral` (CLI-enforced by the vendored mechanism). The two hard tightenings:

1. **Only `factual` corrections are injected or enforced.** A `factual` correction is a deterministic, structural fact (a hardcoded hex where a token exists; an off-scale spacing value). A `behavioral` correction (a taste read, a critique tendency) surfaces to the human as a reminder to decide; it is never auto-injected into generation.
2. **A `behavioral` correction is never promotable to an auto-enforced rule.** A taste correction hardening into an enforced check is the boundary collapsing. Promotion applies to `factual` patterns only.

The design taxonomy (token-fidelity, spacing-scale, component-integrity, semantic-role, accessibility, escape-hatch, elevation, typography) lives in a `category` field, not in `severity`.

---

## Promotion thresholds

A correction earns promotion when it keeps firing despite being in the registry. A reasonable default:

> **5 or more total fires, OR the same pattern across 3 or more separate sessions.**

`times_fired` is a lifetime count, a floor on the sessions a pattern has already cost. When either trigger fires, the advisory correction is no longer doing its job as a soft note; promote it and supersede the entry.

---

## The close-out protocol

When you promote a correction, do all three in the same pass so the registry never lies:

1. Write the new hard rule into its permanent home.
2. Set the entry's `status` to `superseded` and `superseded_by` to the rule's location.
3. Recompute the registry `meta` counts.

A correction left `active` after its rule shipped keeps firing on something already enforced, so the signal degrades.

---

## The human standard

The registry is curated, not auto-generated. An agent may *observe* a recurring pattern and propose a correction; a human decides what enters and what promotes. Unreviewed entries never reach agent context. The intake and the live registry stay separate.

---

*Seed template: `os/corrections/seed-corrections.yaml` · Runtime: the internal `heyhi-mcp` (Phase 2 / DISPATCH-02) · Convention overview: `os/corrections/README.md`*

*HeyHi Confidential*
