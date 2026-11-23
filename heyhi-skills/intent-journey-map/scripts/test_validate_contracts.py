"""Tests for validate_contracts.py. Run: python3 -m pytest -q scripts/test_validate_contracts.py"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import validate_contracts as vc  # noqa: E402

FIX = HERE / "fixtures"


def worked_example() -> Path | None:
    for base in [HERE.parent] + [p / "heyhi-skills" / "intent-journey-map" for p in HERE.parents]:
        cand = base / "references" / "worked-example.ijm-contract.json"
        if cand.is_file():
            return cand
    return None


class Contracts(unittest.TestCase):
    def test_drifted_contract_names_the_three_fields(self):
        schema = json.loads(vc.find_schema(None).read_text(encoding="utf-8"))
        doc = json.loads((FIX / "drifted.ijm-contract.json").read_text(encoding="utf-8"))
        r = vc.check(doc, schema, None)
        self.assertEqual(r["missing"], ["schema_version", "tier", "research_question"])
        self.assertFalse(r["ok"])

    def test_minimal_contract_passes_and_drifted_fails(self):
        self.assertEqual(vc.main([str(FIX / "minimal.ijm-contract.json")]), 0)
        self.assertEqual(vc.main([str(FIX / "drifted.ijm-contract.json")]), 1)

    def test_a_filled_research_question_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "x.ijm-contract.json"
            d = json.loads((FIX / "minimal.ijm-contract.json").read_text(encoding="utf-8"))
            d["research_question"] = "Do users want notes?"
            p.write_text(json.dumps(d), encoding="utf-8")
            self.assertEqual(vc.main([str(p)]), 1)

    def test_folder_mode_and_nothing_to_read(self):
        self.assertEqual(vc.main([str(FIX)]), 1)  # the drifted one fails the folder
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(vc.main([tmp]), 2)

    def test_the_shipped_worked_example_passes(self):
        we = worked_example()
        if we is None:
            self.skipTest("worked example not present in this tree")
        self.assertEqual(vc.main([str(we)]), 0)


if __name__ == "__main__":
    unittest.main()
