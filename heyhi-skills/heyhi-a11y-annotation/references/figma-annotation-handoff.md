# The Figma annotation handoff (and the reconciliation ledger)

Under Figma-first review (`review.review_surface: figma`, the default), signed Sheerline outputs reach the work through the frames. This reference is the handoff path for three of them: the **interaction inventory** (`interaction-inventory`), the **microcopy set** (`microcopy-states-writer`) and the **accessibility annotation** (this skill). It writes each signed row as a native Figma annotation on the node it describes, then reads every annotation back and compares. Its companion, the **reconciliation ledger**, records later where the final frame and the source output disagree.

## When it runs

Only after the source output's gate is closed (`sheerline/os/session-rules.md` § Gate fields): the owner signed, not by proxy. An unsigned output is not handed off, because the annotation would read as designed when it was only drafted. Judged slots that are still empty by construction (alt text, reading-order intent, a copy string not yet chosen) are written as visibly blank annotations labeled with the slot, never filled.

## 1. The targets file

One JSON file in the engagement folder, `annotation-targets.json`, one entry per annotation to write:

```json
{
  "file_key": "<the Figma file key>",
  "categories": {"interaction": "<category id>", "microcopy": "<category id>", "accessibility": "<category id>"},
  "targets": [
    {"id": "inv-3", "source": "interaction-inventory", "source_row": "3", "node_id": "12:34",
     "category": "interaction", "label": "Save button: default, hover, focus-visible, disabled, loading. Enter and Space activate."}
  ],
  "unmapped": [{"source": "microcopy-states-writer", "source_row": "7", "reason": "no frame shows the error state"}]
}
```

- `id` is stable across runs (source plus row), so a re-run replaces its own annotation instead of adding a second.
- `node_id` comes from reading the file (`get_metadata`, `get_design_context`). A row with no matching node goes to `unmapped` with the reason. It is never pinned to a guessed node; an unmapped row is a GAP for the ledger.
- `label` is the signed row as text, bounded to what a developer reads in Dev Mode. The write appends the target's `id` in brackets (for example `[inv-3]`), so anyone can trace the annotation to its source row and a re-run can find its own annotations.

## 2. Categories

One annotation category per source kind (interaction, microcopy, accessibility). The instance names them; read the file's existing categories first and reuse a matching one, and create a missing one once. Record the ids in the targets file so the write and the read-back agree on them.

## 3. Write

Through `use_figma` (load `figma-use` first, as for every `use_figma` call). For each target: find the node and keep every annotation on it that this pipeline did not write. An annotation carrying this target's `id` is replaced only when it still reads exactly what the last run wrote (the previous targets file is the record of that). If a person has edited it in Figma, leave it as it is: the read-back reports it `CHANGED`, and the reconciliation ledger records the delta for the owner. One script per file, batched; return the node ids written. Never delete or rewrite an annotation a person wrote or edited.

## 4. Read back

A second `use_figma` call reads the annotations on every target node and returns them as JSON (`{"<node_id>": [{"label": "...", "categoryId": "..."}]}`), saved as `annotation-readback.json`. Then:

```
python3 scripts/check_annotation_readback.py annotation-targets.json annotation-readback.json
```

It reports each target as `MATCH` (the label, with the `[id]` removed, equals the target's label, and the category matches), `MISSING` (no annotation carries the id), `CHANGED` (the id is there with any other label or category, an appended edit included) or `DUPLICATE` (the id appears more than once), and lists the unmapped rows. It exits 1 on anything but all `MATCH`, and 2 on a targets file with no targets or an empty label. The read-back is the verification, not the write's return value; then render the frames and look (the design smoke test).

**Open question (vendor fact, check before the first live run):** this method assumes the Plugin API's node `annotations` property (entries with a label or markdown label, optional properties and a category id) and the file-level annotation-category calls. Confirm both against the `figma-use` skill's API reference; the read-back fails loud if the shape differs.

## The reconciliation ledger (a grade instrument)

After the designer finalizes the frames, the final frame can overrule the source output: a string reworded in the frame, a state dropped, a role changed. The ledger records each disagreement instead of letting the two drift apart silently. One row per source row and per frame element with no source row:

| Source | Row | Node | The source says | The frame says | Class | Basis |
|---|---|---|---|---|---|---|

- **MATCH**: the frame agrees with the source row.
- **DELTA-FIGMA-WINS**: they differ and the frame is the record. Recorded only against a frame whose review gate is closed (Basis links the owner's signature); then the owner updates the source output to match. A delta against an unsigned frame is held with Basis `unsigned frame` and counted only once the frame is signed.
- **GAP**: a source row with no counterpart in the frame (an unmapped target, a missing annotation), or a frame element no source row covers.

The comparison is mechanical; deciding that the frame's version is the right one is the owner's signature, which is why a delta needs a closed gate before it counts.

**The grade series.** Each handoff appends one row of counts (MATCH, DELTA-FIGMA-WINS, GAP, held deltas) to the engagement's own series file in its gitignored engagement folder. The method ships; what a healthy ratio is stays with the instance as calibration and never ships. The ledger reports counts, not a verdict.

