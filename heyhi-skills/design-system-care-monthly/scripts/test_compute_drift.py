#!/usr/bin/env python3
"""
Unit tests for compute_drift.py (Plan 3A). Run: python3 test_compute_drift.py

The canonical case is the one the plan names: a synthetic token set with
5 changed / 2 added / 1 removed.
"""

from compute_drift import compute_drift, flatten_variables


def _assert(cond, msg):
    if not cond:
        raise AssertionError(msg)


def test_canonical_5_changed_2_added_1_removed():
    baseline = {
        "color": {
            "brand": {
                "primary": {"light": "A1", "dark": "A2"},
                "secondary": {"light": "B1", "dark": "B2"},
            },
            "feedback": {"warning": {"light": "C1"}},
        },
        "spacing": {
            "card": {"default": "8px", "compact": "4px"},
            "page": {"default": "16px", "wide": "24px"},
        },
    }
    current = {
        "color": {
            "brand": {
                "primary": {"light": "A1x", "dark": "A2x"},     # 2 changed
                "secondary": {"light": "B1x", "dark": "B2"},     # 1 changed (B1)
            },
            "feedback": {},                                       # warning/light removed (1)
        },
        "spacing": {
            "card": {"default": "8pxX", "compact": "4px", "tight": "2px"},   # 1 changed + 1 added
            "page": {"default": "16pxX", "wide": "24px", "narrow": "12px"},  # 1 changed + 1 added
        },
    }
    # changed = primary/light, primary/dark, secondary/light, card/default, page/default = 5
    # added   = card/tight, page/narrow = 2
    # removed = feedback/warning/light = 1

    diff = compute_drift(current, baseline)
    _assert(diff["drift_detected"] is True, "drift should be detected")
    _assert(len(diff["changed"]) == 5, f"expected 5 changed, got {len(diff['changed'])}: {diff['changed']}")
    _assert(len(diff["added"]) == 2, f"expected 2 added, got {len(diff['added'])}: {diff['added']}")
    _assert(len(diff["removed"]) == 1, f"expected 1 removed, got {len(diff['removed'])}: {diff['removed']}")
    _assert(diff["total_baseline"] == 9, f"expected 9 baseline leaves, got {diff['total_baseline']}")
    _assert(diff["total_current"] == 10, f"expected 10 current leaves, got {diff['total_current']}")

    prim = next(c for c in diff["changed"] if c["key"] == "color/brand/primary/light")
    _assert(prim["previous"] == "A1" and prim["current"] == "A1x", f"changed record values: {prim}")
    _assert(diff["removed"][0]["key"] == "color/feedback/warning/light", f"removed key: {diff['removed']}")
    _assert(diff["added"][0]["key"] in {"spacing/card/tight", "spacing/page/narrow"}, "added key")
    print("PASS test_canonical_5_changed_2_added_1_removed")


def test_no_drift():
    m = {"color": {"x": {"light": "1"}}}
    diff = compute_drift(m, m)  # compute_drift does not mutate its inputs
    _assert(diff["drift_detected"] is False, "no drift expected")
    _assert(diff["changed"] == [] and diff["added"] == [] and diff["removed"] == [], "all empty")
    _assert(diff["total_current"] == diff["total_baseline"] == 1, "counts")
    print("PASS test_no_drift")


def test_deterministic_ordering():
    baseline = {"b": "1", "a": "1", "c": "1"}
    current = {"b": "2", "a": "2", "c": "2"}
    diff = compute_drift(current, baseline)
    keys = [c["key"] for c in diff["changed"]]
    _assert(keys == sorted(keys), f"changed should be sorted, got {keys}")
    print("PASS test_deterministic_ordering")


def test_flatten_handles_lists_and_empty():
    flat = flatten_variables({"a": {"modes": ["x", "y"]}, "b": {}})
    _assert(flat == {"a/modes[0]": "x", "a/modes[1]": "y"}, f"list/empty flatten: {flat}")
    print("PASS test_flatten_handles_lists_and_empty")


if __name__ == "__main__":
    test_canonical_5_changed_2_added_1_removed()
    test_no_drift()
    test_deterministic_ordering()
    test_flatten_handles_lists_and_empty()
    print("\nAll tests passed.")
