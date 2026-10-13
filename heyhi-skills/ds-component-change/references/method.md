# DS Component Change: method spine

*Reference for `ds-component-change` (Sheerline area 7, the change verb). The classification rubric, the change-set shape, the swap discipline, the re-validation rule, and an end-to-end worked example. Load on demand; not in the always-loaded block.*

---

## 1. What a "change" is here, and what it is not

A change is a **confirmed, intended edit to the spec of a component that already exists** in Figma and in code. The intent is settled before this skill runs; the skill lands it, it does not decide it. Five change types are in scope:

| `change_type` | Example |
|---|---|
| `variable_value` | a spacing token moves from `12px` to `10px`; an accent color shifts one step |
| `prop_rename` | `fullWidth` becomes `block` |
| `prop_type_change` | `size?: number` becomes `size?: 'sm' \| 'md' \| 'lg'` |
| `variant_add` | a `danger` variant is added to Button |
| `variant_remove` | a deprecated `ghost` variant is dropped |

Out of scope, by design: discovering that something drifted (that is `heyhi-drift-repair`, which acts on unintended drift), authoring a component that does not exist yet (`ds-component-author`), and generating a whole system (`heyhi-figma-ds-generator`). The verb here is *change an existing thing on purpose*.

## 2. The classification rubric (a candidate, never final)

The rubric maps `change_type` to a default `classification_candidate`. It is mechanical, and it is only a candidate. The human confirms at the classification gate, because the rubric cannot see blast radius.

| `change_type` | Default candidate | Semantic-versioning basis | Why a person still rules |
|---|---|---|---|
| `variable_value` | **patch** | no public interface changes | a value others alias or compute against is a structural break |
| `variant_add`, `prop_add` (optional), `enum_value_add` | **minor** | additive, backward compatible | a new variant can collide; a new required prop is breaking; a widened union can break exhaustive switches |
| `prop_rename`, `prop_remove`, `variant_remove`, `enum_value_remove` | **breaking** | removes or renames public surface | the surface is gone; downstream must migrate |
| `prop_type_change` (incompatible) | **breaking** | old call sites may not typecheck | a *widening* type change (e.g. `'sm'` to `string`) can be minor |
| `default_change` | **breaking** | changing behavior for callers who relied on the old default | whether the old default was load-bearing is a judgment |

Two rules make the rubric safe:

- **Precedence.** When more than one row applies, take the more severe candidate. Breaking beats minor beats patch. The skill never softens; the human may.
- **Re-classification is one-way at run time.** A minor change discovered mid-run to need a call-site migration is promoted to breaking (Step 4 to Step 5). The skill never demotes a breaking candidate to minor on its own; only the human does that, at the gate.

The field is named `classification_candidate` on purpose. Nothing downstream reads it as an approval, and the change set does not merge on it (see `heyhi-drift-repair`'s identical discipline: a `candidate` is never an approval).

## 3. The change-set shape

Whatever the classification, the outputs land as **one reviewable set** so the whole change is seen at once:

```
change set
├── Figma change log        (proposed node edits with ids; NOTHING written)
├── code diff               (the prop or token edit at its source)
└── (breaking only)
    ├── deprecation shim     (old surface accepted + mapped + warned + @deprecated)
    ├── ESLint entry         (flags the deprecated usage)
    ├── codemod              (rewrites downstream call sites; fixture pair)
    ├── migration note       (what, why, window, command)
    └── changeset            (major)
```

The Figma log and the code diff **describe the same change on two surfaces**, so they must agree: the same rename, the same component. A set whose two legs disagree is a defect the gate catches. The set is a single propose-first pull request (the code legs) plus the Figma log; nothing merges.

## 4. The re-validation rule (non-breaking path)

For a patch or minor change, after the source edit:

1. **Typecheck.** The package must typecheck. A change that does not compile is not landed. (In the worked example the package carries pre-existing typecheck debt in unrelated files; the discipline is that *the changed files* introduce zero new errors, verified with a scoped typecheck. See `shim-and-codemod-react.md § typecheck`.)
2. **Re-validate through `validate_output`.** Run the instance's validator on the component's real CSS. It checks **conformance, not intent**: it confirms the edit did not introduce drift (an off-scale value, a broken token reference), the same guarantee `heyhi-drift-repair` Step 4 relies on. It does not confirm the change is *right*; that is the human's call.

Re-validation is a safety net, not a judge. A change that clears the validator but is the wrong change still stops at the classification gate.

## 5. The swap discipline

When a change retargets downstream Figma instances (a removed variant, a replaced master), retarget **per instance** with `instance.swapComponent(newComponent)` or `instance.setProperties(...)`. Figma's native swap-libraries feature only matches assets that originate from another published library; a local master is silently skipped, so a swap-libraries retarget of a local master quietly does nothing (plan ground-truth correction; `figma-leg.md § swap`). The skill's SKILL.md states this once, to forbid it.

## 6. Worked example, end to end (the instance's own proof run)

**Spec.** `component: Button`, `change_type: prop_rename`, `target: fullWidth`, `from: fullWidth`, `to: block`, `reason: "align the layout boolean with sibling primitives that already take block"`.

**Step 2, classify.** `prop_rename` to candidate **breaking**. The candidate does not assert the change is right, or set the window; it asserts that *if* it ships, it ships with the breaking kit.

**Step 3, Figma leg (proposed, nothing written).**

| Change | Node id | Proposed operation | Old to New |
|---|---|---|---|
| prop rename | `<COMPONENT_SET id>` | `editComponentProperty('fullWidth', { name: 'block' })` | fullWidth to block |

`editComponentProperty` is a documented Plugin API method not covered by the served `figma-use` reference, so it is cited from the developer docs and probed before any real use; here it is only logged (`probes.md`). No Figma node is written.

**Step 5, code leg (breaking kit).** The actual shim, codemod, migration note, changeset, and ESLint entry are in `shim-and-codemod-react.md`, landed on the proof branch (`ds-component-change-proof-2026-09-07`) as one propose-first change set. The codemod rewrote a three-call-site fixture (shorthand, `={true}`, expression) and left a non-Button `fullWidth` decoy untouched; the changed files typecheck clean.

**The three empty slots.** The proof records the classification as *confirmed breaking by the owner*, the window as *accepted through the current major, removed in the next*, and the merge as *not done* (propose-first). In a live run those three are blank until a person signs. The worked example fills them only so the kit can run end to end, and it labels them as the human's calls.

---

## 7. Provenance and the empty slots

- Every classification the skill writes is `classification_candidate`. The confirmed `classification` exists only after the gate.
- The Figma leg is `proposed`, never `applied`. The word `applied` appears on a Figma edit only after a human runs the log (or a future gated increment does).
- The deprecation window and the merge are unrecorded until signed.

If any of these is filled by the skill on its own, the boundary is broken and the run is rejected at review.

---

*HeyHi Confidential. Reference for `ds-component-change` (Sheerline area 7). Method spine; load on demand.*
