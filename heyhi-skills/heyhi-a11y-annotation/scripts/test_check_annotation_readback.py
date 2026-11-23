"""Tests for check_annotation_readback.py. Run: python3 -m pytest -q scripts/test_check_annotation_readback.py"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import check_annotation_readback as car  # noqa: E402

FIX = HERE / "fixtures"


def load(name: str):
    return json.loads((FIX / name).read_text(encoding="utf-8"))


class Readback(unittest.TestCase):
    def setUp(self):
        self.r = car.compare(load("annotation-targets.json"), load("annotation-readback.json"))
        self.by_id = {t["id"]: t["status"] for t in self.r["targets"]}

    def test_each_status(self):
        self.assertEqual(self.by_id, {"inv-3": "MATCH", "copy-5": "CHANGED",
                                      "a11y-2": "DUPLICATE", "a11y-9": "MISSING"})

    def test_a_hand_written_annotation_is_left_alone(self):
        self.assertEqual(self.r["counts"]["MATCH"], 1)  # the designer's note is not counted as ours

    def test_unmapped_rows_are_gaps(self):
        self.assertEqual(len(self.r["unmapped"]), 1)

    def test_an_appended_edit_reads_changed(self):
        targets = {"categories": {}, "targets": [{"id": "x-1", "node_id": "1:1", "category": None,
                                                  "label": "Landmark: main."}]}
        rb = {"1:1": [{"label": "Landmark: main. Designer edit: actually nav [x-1]", "categoryId": "c"}]}
        self.assertEqual(car.compare(targets, rb)["targets"][0]["status"], "CHANGED")

    def test_zero_targets_and_empty_labels_fail_loud(self):
        with tempfile.TemporaryDirectory() as tmp:
            rb = Path(tmp) / "rb.json"
            rb.write_text("{}", encoding="utf-8")
            for doc in ({"targets": []},
                        {"targets": [{"id": "x-1", "node_id": "1:1", "label": "  "}]}):
                t = Path(tmp) / "t.json"
                t.write_text(json.dumps(doc), encoding="utf-8")
                self.assertEqual(car.main([str(t), str(rb)]), 2)

    def test_exit_codes(self):
        t, rb = str(FIX / "annotation-targets.json"), str(FIX / "annotation-readback.json")
        self.assertEqual(car.main([t, rb]), 1)
        with tempfile.TemporaryDirectory() as tmp:
            good = Path(tmp) / "rb.json"
            good.write_text(json.dumps({"12:34": [{"label": "Save button: default, hover, focus-visible, disabled, loading. [inv-3]", "categoryId": "cat-i"}]}), encoding="utf-8")
            one = Path(tmp) / "t.json"
            data = load("annotation-targets.json")
            data["targets"] = data["targets"][:1]
            one.write_text(json.dumps(data), encoding="utf-8")
            self.assertEqual(car.main([str(one), str(good)]), 0)
            bad = Path(tmp) / "bad.json"
            bad.write_text("[]", encoding="utf-8")
            self.assertEqual(car.main([t, str(bad)]), 2)


if __name__ == "__main__":
    unittest.main()
