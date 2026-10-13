# Dependency ripple: exercise the graph, don't just model it

*Shared reference for `ds-component-change` and `feature-increment` (Sheerline W7 / G12, the ripple step). Loaded on demand after the skill computes its own change; not in the always-loaded block. Ratified 2026-09-13 (G-W7c; `plans/plan-sheerline-governance-mechanisms-2026-09-12.md` § 0.5).*

*This file is staged byte-identically under both `skill-updates/ds-component-change/references/` and `skill-updates/feature-increment/references/`. On promotion it lands in both deployed skills' `references/` dirs; keep the two copies in sync (or relocate to one shared reference if the skill loader supports it — the instance owner's call at promotion).*

---

## What this step is, and what it is not

Sheerline already MODELS the dependency graph (`retrieve_design_relationships`) and each consuming skill already emits its own change (a shim, a codemod, a coverage table) for its OWN target. The missing step is EXERCISING the graph for every OTHER node the change touches: re-running the same check on each dependent, so a change that is clean on its target but breaks a consumer is caught before the human gate, not after.

This is **not a new graph** (no new node type, edge type, or data), **not a new gate** (both skills are already propose-first; nothing merges without a human), and **never an auto-revert** (nothing was applied, so nothing is reverted — the PR / change-set review is the gate). It adds completeness to the existing human gate.

## When it runs (attachment points)

- **`ds-component-change`:** after the code leg computes its change (Step 4 non-breaking / Step 5 breaking), before Step 6 "Land as one reviewable change set." The dependent rows join the Step 6 change set.
- **`feature-increment`:** inside Step 6 (the three-way contract coverage table). The dependent rows join that table.

## The mechanism

**1. Root the query at the semantically-changed node.** Call:

```
retrieve_design_relationships(
    query_type="impact_analysis",
    target_node=<the changed component or token id>,
    max_hops=4,
)
```

For a **token / variable-value** change, root the call at the changed **token**, not the nominal component target — the token is what changed meaning; the component is one of its dependents. Add `component_uses` / `pattern_application` calls where the change is a token or a promoted pattern.

**Depth: default 4 / full-within-cap.** `max_hops=4` is the tool's enforced maximum (`graph.query` clamps to 1–4), so the default traverses to the leaves of the served graph. Governance is by a dependent-**count** cost cap, not a shallow depth cap: an override NARROWS from full-within-cap, it does not widen from a shallow default. (The spec's first draft proposed `max_hops=2`; § 0.5 supersedes it.)

**2. Re-exercise every dependent the graph returns.** For each dependent, add one row to the skill's existing reconciliation surface (`ds-component-change`'s change set; `feature-increment`'s coverage table) and re-run the SAME check the skill runs on its primary target:
- a code dependent: typecheck + `validate_output` on its real CSS;
- a prototype dependent: re-render + `validate_output(rendered_css)`.

**3. Three-state reconciliation row — never a silent miss.** Every dependent lands in exactly one of:

| State | Meaning |
|---|---|
| `exercised: pass` | re-ran the check, it passed |
| `exercised: FAIL → finding` | re-ran the check, it failed — a hard finding (below) |
| `NOT exercised (beyond horizon / cost cap): N dependents` | the count cap or the hop horizon stopped the traversal here — the N is named, not dropped |

The third row is the load-bearing visibility fix: because there is no gate, "never a silent miss" has to be literal. A dependent that is not exercised is reported as not-exercised with its count, never omitted.

**4. A failed dependent is a hard finding, in the shape both skills already use.** Write it as the reversible-deviation record verbatim:

```
{ finding, matched_correction, before, after, surface, location,
  timestamp, provenance: automated, confirmed: false }
```

(`matched_correction` is `null` for a raw conformance finding with no registry match.) It is a hard fail of the RUN — the same way `feature-increment`'s coverage table already treats an unexplained miss — never an auto-block of a merge that was never automatic, and never an auto-revert.

## Named honestly against today's data

`pattern_application` queries return empty until the pattern ledger (fdde-loop § 3.3, filled by Care / `feature-increment`'s own `local`-row emission) actually holds rows. That is a real limit of today's DATA, not of the graph or this step, and it is not hidden: a pattern-leg row reports `NOT exercised: 0 pattern dependents (ledger empty)` rather than a false pass. The graph is real for tokens / components today; `page` nodes and populated patterns are the graph-completeness question (C1) routed forward in § 0.5, not resolved here.

---

*HeyHi Internal Use Only*
*classification: internal*
