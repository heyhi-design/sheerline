---
classification: confidential
title: "feature-increment: the three-way contract coverage table"
---

# The three-way contract coverage table

The coverage table is the step no existing pipeline has: the reconciliation that shows one feature's contract present in all three targets, or names the miss. This reference defines the exact columns, what counts as evidence in each, and the miss rules that decide pass or fail. It is emitted every run, pass or miss, into the proof record.

## The unit: one contract element per row

A row is one element of the feature's contract: a prop, an interaction state, or a component. The rows come from the served contract (the `intent-journey-map` output), not from any one target. This is the discipline that keeps the table honest: the rows are fixed by the contract before any target is read, so a target cannot define away a row by omitting it. A contract with N elements produces a table with N rows, every run.

## The columns

| Column | What counts as evidence of presence | What a miss looks like |
|---|---|---|
| **Contract element** | the row label: the prop name and type, the state, or the component, copied from the contract | (never blank; the rows are the contract) |
| **In Figma** | a property set on the artifact node, a text value, or a bound variable that renders the element (read back through `app-to-figma`'s validation: `mainComponent.key` in the library map, a bound variable `remote: true`) | the element has no node, property, or binding on the artifact frame |
| **In prototype** | a rendered state or a data binding in the `ui-studio` Mode A prototype, present after the `validate_output` gate passed | the element is absent from the prototype section |
| **In code** | a prop on the scaffolded component, a hook field, or a route stub in the repo increment, typed from the contract row | the element has no prop, field, or stub in the repo increment |
| **Verdict** | `pass` when all three columns carry evidence | a finding id when any column is a miss |

## The miss rules (the pass/fail logic)

A contract row absent from a target is one of two things, and the table must say which:

1. **An explained miss**: a finding id and a stated reason. Three legitimate reasons:
   - **operator-gated**: the target cannot be built without a human action outside the agent's reach (the proof library being published is the standing example; a Figma UI action with no Plugin-API path). The finding names the action.
   - **deferred**: the human, at the delta-plan gate, ruled this element out of this increment's scope. The finding cites the ruling.
   - **genuine gap**: the element should be in the target and is not, and closing it is real work the human must schedule. The finding says so plainly; this is the honest failure the table exists to surface.
2. **An unexplained miss**: a target cell is blank and there is no finding. This is a hard failure of the run. There is no "close enough" and no silent omission: a row is present with evidence, or it is a finding with a reason.

The read-out line reports `Unexplained misses: [n]`, and a run is not done until it reads `0`. The smoke test asserts `grep -c "unexplained miss" PROOF.md` is `0`, which holds when every non-pass row carries a finding id and the read-out reads zero.

## The verdict is mechanical, not a judgment

The verdict column is computed, not judged: `pass` when all three columns carry evidence, otherwise the finding id that explains the miss. The table never rules whether the feature is *good* (that is the surface verdict, the human's, `app-to-figma`'s inherited empty slot). It rules only whether the contract is *present in all three places*. A feature can have a fully green coverage table and still be the wrong feature; the table does not claim otherwise.

## Worked shape (illustrative)

This is a teaching example of the table's shape and the pass / finding / `n/a` mechanics, drawn on a category-filter-style feature. It shows a *partially* published library (only the focus-visible variant missing) and an interactive prototype, so most Figma cells pass and one is a finding, which is the useful shape to learn from. The **actual proof run** ran a fully unpublished library and a static rendered_css prototype, so its real table (all nine Figma cells operator-gated, `onSelect` prototype `n/a`) looks different; that honest result lives in the gitignored proof record (`<engagement folder>/feature-increment-proof/PROOF.md`), not here.

```
# Contract coverage: category filter (illustrative)
Contract: <ijm id>     Reconciled: <date>     Unexplained misses: 0

| Contract element | In Figma | In prototype | In code | Verdict |
|------------------|----------|--------------|---------|---------|
| CategoryFilter.categories: string[] (derived) | chip-row instances | rendered chip row | prop categories: string[] | pass |
| CategoryFilter.selected: string (state) | Selected variant on chip | .is-selected class | useState<string> selected | pass |
| CategoryFilter.onSelect (callback) | n/a (Figma has no behavior) | click handler wired | onSelect prop | pass |
| chip state: hover | Hover variant | :hover style | :hover style | pass |
| chip state: focus-visible | (F-01) | :focus-visible ring | :focus-visible ring | F-01 |
| list state: empty-result | frame present | empty-state block | conditional render | pass |
| copy: "All" + category labels | text on chips | rendered labels | label strings (area-3 slot) | pass |

## Findings
- F-01 [operator-gated]: the Figma focus-visible variant is blocked on the proof
  library being published (a Figma UI action, no Plugin-API path). Named operator step, not an
  unexplained miss. When the library is published, the Figma column re-runs through app-to-figma
  update mode and the finding closes.

## Read-out
Rows: 7     Pass: 6     Findings: 1     Unexplained misses: 0
```

Note the `onSelect` row: a callback is a code and prototype concern with no Figma equivalent (Figma has no behavior), so `n/a` in the Figma column is evidence of a correct absence, not a miss. `n/a` is used only where a column genuinely cannot carry the element (behavior in Figma, a derived-not-fetched prop's endpoint); it is never a way to hide a real gap. When in doubt, a finding is the honest choice, not `n/a`.

## Why the table is emitted even when every row passes

A clean table (all `pass`, `Unexplained misses: 0`) is the proof that the join held: the same contract landed in all three targets. Suppressing the table on a clean run would remove the evidence the increment is complete. The table is the artifact that says the loop closed for this feature, so it is emitted every run.

*HeyHi Confidential. `skill-updates/feature-increment/references/`. The coverage-table columns and miss rules. The reconciliation the loop's Care/increment verb owns.*
