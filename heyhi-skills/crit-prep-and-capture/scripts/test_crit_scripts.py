"""Tests for threads_to_revision_plan.py and uptake_count.py. Stdlib only.
Run: python3 -m pytest -q scripts/test_crit_scripts.py"""
from __future__ import annotations

import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import threads_to_revision_plan as trp  # noqa: E402
import uptake_count as uc  # noqa: E402

FIX = HERE / "fixtures"


class RevisionPlan(unittest.TestCase):
    def setUp(self):
        self.rows = trp.threads(json.loads((FIX / "comments.json").read_text(encoding="utf-8")))
        self.text = trp.render(self.rows, "FILEKEY", "comments.json", "2026-11-22")

    def test_one_row_per_root_thread(self):
        roots = [r for r in self.rows if "orphan_parent" not in r]
        self.assertEqual([r["id"] for r in roots], ["101", "103"])
        self.assertEqual(roots[0]["replies"], 1)

    def test_comment_text_is_neutralized(self):
        self.assertNotIn("\x07", self.text)
        self.assertIn("\\|", self.text)  # a pipe cannot break the table

    def test_every_disposition_starts_undecided_and_revision_is_empty(self):
        rows = [ln for ln in self.text.splitlines() if ln.startswith("| 1 ") or ln.startswith("| 2 ")]
        self.assertEqual(len(rows), 2)
        for ln in rows:
            cells = [c.strip() for c in re.split(r"(?<!\\)\|", ln.strip().strip("|"))]
            self.assertEqual(cells[6], "undecided")
            self.assertEqual(cells[8], "")  # Revision: the owner's call
            self.assertEqual(cells[9], "")  # Answered by: blank until a change links it

    def test_resolved_is_data_not_a_disposition(self):
        row2 = next(ln for ln in self.text.splitlines() if ln.startswith("| 2 "))
        self.assertIn("| yes | undecided |", row2)

    def test_unresolved_node_and_orphan_reply_are_uncertain_calls(self):
        tail = self.text.split("## Uncertain calls", 1)[1]
        self.assertIn("node could not be resolved", tail)
        self.assertIn("999", tail)

    def test_bad_shape_fails_loud(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "bad.json"
            p.write_text('{"nope": []}', encoding="utf-8")
            self.assertEqual(trp.main([str(p), "--file-key", "K"]), 2)


    def test_string_user_and_odd_meta_do_not_crash(self):
        data = {"comments": [{"id": "1", "parent_id": "", "message": "m", "user": "Reviewer A",
                              "client_meta": {"node_id": 5}}]}
        rows = trp.threads(data)
        self.assertEqual(rows[0]["by"], "Reviewer A")
        self.assertIsNone(rows[0]["node_id"])

    def test_proxy_ships_blank_in_the_plan_gate(self):
        self.assertIn("Proxy: ____", self.text)


class Uptake(unittest.TestCase):
    def test_counts_and_both_rates(self):
        r = uc.count((FIX / "capture.md").read_text(encoding="utf-8"))
        self.assertEqual((r["items"], r["answered"], r["deferred"], r["dropped"], r["unanswered"]),
                         (5, 1, 1, 1, 2))
        self.assertEqual(r["unanswered_rows"], ["2", "5"])
        self.assertEqual(r["rate_all"], 0.2)
        self.assertEqual(r["rate_open"], 0.333)

    def test_escaped_pipe_and_placeholders_from_a_generated_plan(self):
        plan = trp.render(trp.threads(json.loads((FIX / "comments.json").read_text(encoding="utf-8"))),
                          "K", "comments.json", "2026-11-22")
        lines = plan.splitlines()
        i = next(n for n, ln in enumerate(lines) if ln.startswith("| 2 "))
        lines[i] = lines[i].replace("| undecided |", "| deferred |")
        j = next(n for n, ln in enumerate(lines) if ln.startswith("| 1 "))
        lines[j] = lines[j].rstrip().rstrip("|").rstrip() + " TBD |"
        r = uc.count("\n".join(lines))
        self.assertEqual((r["items"], r["answered"], r["deferred"], r["unanswered"]), (2, 0, 1, 1))

    def test_partial_window_is_flagged(self):
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            uc.main([str(FIX / "capture.md"), "--review-date", "2026-11-10", "--window-days", "7",
                     "--today", "2026-11-12"])
        self.assertIn("PARTIAL", buf.getvalue())

    def test_no_matching_table_fails_loud(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "c.md"
            p.write_text("| a | b |\n|---|---|\n| 1 | 2 |\n", encoding="utf-8")
            self.assertEqual(uc.main([str(p), "--review-date", "2026-11-10", "--window-days", "7"]), 2)

    def test_series_outside_git_is_written(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "grades" / "uptake-audit.csv"
            rc = uc.main([str(FIX / "capture.md"), "--review-date", "2026-11-10",
                          "--window-days", "7", "--append-csv", str(out)])
            self.assertEqual(rc, 0)
            self.assertEqual(len(out.read_text(encoding="utf-8").splitlines()), 2)

    def test_series_refuses_a_tracked_path(self):
        tracked = HERE / "uptake-series-must-not-land-here.csv"
        rc = uc.main([str(FIX / "capture.md"), "--review-date", "2026-11-10",
                      "--window-days", "7", "--append-csv", str(tracked)])
        if uc.git_would_track(tracked):
            self.assertEqual(rc, 2)
            self.assertFalse(tracked.exists())
        else:  # an export or a checkout where this folder is ignored: nothing to assert
            tracked.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
