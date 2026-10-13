---
classification: confidential
title: "Production-Code Adoption — metric-definitions contract"
status: unratified
ratified_by: null
version: "1.0.0"
effective_date: null
source: plans/plan-sheerline-adoption-and-reach-2026-09-12.md
---

# Production-Code Adoption — metric-definitions contract

**HeyHi Confidential.** The single page every adoption number ships with. A coverage percentage without its definition is the field's oldest failure: a number nobody can reproduce, argue with, or trust. This contract is the ratification artifact for **G-W4** — no "% on system" figure goes into a client report until this is signed off, and every figure that does carries a link back to it.

> **Ratification slot: unratified in the scaffold (G-W4).** The methodology below is the shipped default. An instance ratifies it once, recording who signed off and the effective date in this file's frontmatter, before any "% on system" figure reaches a client report. Two framing decisions are proposed with it for the instance to ratify: (1) the **denominator** is reported both ways, leading with the on-system rate (host elements in the denominator, the industry default) and carrying named-components-only as context; (2) the **system boundary** is set per engagement (for example, a client's Storybook-documented primitives). A per-engagement instance still records its own boundary, threshold, and the client's confirmation. The reference instance's ratified record is `adoption-definitions-contract.instance.md` (instance-only; not shipped with the scaffold).

Every metric below is stated in the same ten fields, so a client's engineering lead can read one and know exactly what it measures, how it can be gamed, and what is tracked alongside it to keep it honest.

---

## The one rule that governs all four

**The headline is never reported alone.** `on_system_rate` always ships beside `override_rate`. A coverage number with no counter-metric is gameable and misleading in the same move: a team can push "% on system" to 100 while hardcoding every value inside those on-system components. The pair reads together or not at all. This is the value-UI research's own anti-pattern (`design-system-value-ui-inspiration-2026-09-01.md` § 4.5: insertion counts without a denominator; a blended grade with hidden weights) applied as a hard reporting rule.

---

## Metric 1 — On-system rate (the headline)

- **Definition:** the share of UI call sites in the production codebase that use a design-system component rather than a raw host element or a non-system component.
- **Formula:** `system_call_sites / total_ui_call_sites`.
- **Source:** a Tier-1 static scan (`heyhi_mcp.adoption.static_scan`) of the client's frontend at a named commit. A call site is on-system when its component name is imported from a source the engagement names as a system source (`system_import_sources`), or is on the engagement's explicit `system_components` allowlist.
- **Exclusions:** test files, stories, generated output, and vendored code (the scan's `exclude_substrings`); non-UI modules; commented-out call sites.
- **Refresh:** per Care cycle (monthly), trended against the prior cycle's stored read. Care+ tier only — the value is the trend, not the point value.
- **Owner:** the Care lead authors the engagement's `system_import_sources`, deprecated list, and served-component names; the client's engineering lead confirms them before the first read.
- **Gaming path:** wrap a one-off in a thin pass-through of a system component so it registers as an on-system hit without genuine reuse. **Not patched with a detector** (a brittle arms race); countered by the paired counter-metric below, which rises when on-system usage is being locally overridden.
- **Counter-metric:** `override_rate` (Metric 2). Mandatory, never omitted.
- **Effective date:** set at the instance's ratification.
- **Denominator (proposed default, ratified per instance):** report both, lead with this on-system rate (host elements in the denominator, the industry default); carry named-components-only as context. Never a single number in isolation.
- **Version:** 1.0.0. A change to what counts as a call site or a system source bumps this and the `scanner_version` stamped on every read.

---

## Metric 2 — Override rate (the counter-metric)

- **Definition:** the share of on-system call sites that still hardcode a visual override (an inline `style=` or an arbitrary-value className).
- **Formula:** `override_call_sites / system_call_sites`.
- **Source:** the same static scan; an override is a structural marker on an on-system call site.
- **Exclusions:** same as Metric 1; overrides on non-system call sites are not counted (they are already off-system).
- **Refresh:** per Care cycle, trended.
- **Owner:** as Metric 1.
- **Gaming path:** none that helps the vendor — this metric exists to be honest about the headline. A team lowering it genuinely is the intended outcome.
- **Counter-metric:** it *is* the counter-metric. Reported beside `on_system_rate`, always.
- **Effective date:** set at the instance's ratification.
- **Version:** 1.0.0.

---

## Metric 3 — Deprecated-version usage

- **Definition:** on-system call sites that reference a component (or version) the served registry tags deprecated.
- **Formula:** `deprecated_call_sites / system_call_sites` (and the raw count).
- **Source:** the static scan, against the engagement's `deprecated_components` list (sourced from the client's own registry deprecation tags).
- **Exclusions:** as Metric 1.
- **Refresh:** per Care cycle, trended — the number a migration is meant to drive to zero.
- **Owner:** as Metric 1; the deprecated list is confirmed against the client's registry.
- **Gaming path:** none material.
- **Counter-metric:** reported in context of the headline; a deprecated call site is still on-system, so it does not inflate coverage falsely.
- **Effective date:** set at the instance's ratification.
- **Version:** 1.0.0.

---

## Metric 4 — One-off candidates

- **Definition:** locally-defined components whose name shadows a served component — a hand-rolled version of something the system already provides.
- **Formula:** count of call sites of a non-system component whose name is in the engagement's `served_component_names`.
- **Source:** the static scan. This generalizes Care Step 6's existing "shadow components identified" spot-check from a sample to the full repo.
- **Exclusions:** as Metric 1. It is a *candidate* list, not a verdict — a same-named local component may be legitimately different; the Care read flags, the human confirms.
- **Refresh:** per Care cycle.
- **Owner:** as Metric 1.
- **Gaming path:** rename the local component to avoid the name collision. Low value to the client (the duplication remains); flagged as a known limit of name-based detection.
- **Counter-metric:** read beside the nonsystem-component count, so a shrinking one-off list that just moved to differently-named locals is visible.
- **Effective date:** set at the instance's ratification.
- **Version:** 1.0.0.

---

## Fidelity: Tier 1 only

The field measures coverage at three ascending tiers. This contract covers **Tier 1** (static import/dependency scan) — the honest first cut that a codebase read supports. It is **blind to whether an imported call site actually renders**, and says so on every read (`fidelity_limitation`). The scanner walks the source string-, comment-, and brace-aware and rejects TypeScript generics, but it is not a full parser: a relative import of a library component from a sibling file is under-counted, and JSX authored inside a template literal is not counted. Both directions of that residual are disclosed on every read. Tiers 2 (DOM-element ratio in production) and 3 (pixel-weighted visual coverage) are a named follow-on, requiring a build-time marker plus a runtime sampler in the client's live app — a materially larger, more invasive grant, taken only on a client ask for production-runtime access, never assumed.

---

## Per-engagement instantiation (authored, never defaulted)

Each engagement fills these in `care-config.yaml` in the instance's engagement folder for the client, under `adoption_scan`, and the client's engineering lead confirms them before the first read:

- `system_import_sources` — the import specifiers that mark a component as on-system.
- `system_components` — an explicit allowlist, if import-source detection is insufficient.
- `restrict_to_components` — narrows "the system" to a subset (e.g. the Storybook-documented primitives): on-system becomes system-sourced AND in this list.
- `deprecated_components` — from the client's own registry deprecation tags.
- `served_component_names` — for one-off detection.
- `threshold` — **no default.** Which coverage drop is load-bearing is the client's call, authored per engagement. Absent one, the read reports the trend and leaves the alert null; whether the movement matters is a Care judgment recorded in the report, never an automated verdict.

**A default threshold is a decision made for the client by a vendor who has not met their team.** That is the failure mode HeyHi exists to name, so the instrument ships without one.

---

*HeyHi Confidential. Shipped unratified (the G-W4 slot); an instance ratifies its own copy. Source: `plans/plan-sheerline-adoption-and-reach-2026-09-12.md` § 1a.*
