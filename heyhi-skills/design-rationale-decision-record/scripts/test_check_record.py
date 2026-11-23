"""Tests for check_record.py. Run: python3 -m pytest -q scripts/test_check_record.py
(or python3 scripts/test_check_record.py). Stdlib only."""
from __future__ import annotations

import datetime as dt
import re
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import check_record as cr  # noqa: E402

FIX = HERE / "fixtures"
TODAY = dt.date(2026, 11, 22)


def codes(result: dict, kind: str = "errors") -> set[str]:
    return {item["code"] for item in result[kind]}


class Fixtures(unittest.TestCase):
    def test_accepted_with_blank_decision_fails(self):
        self.assertIn("DR-01", codes(cr.check(FIX / "accepted-blank-decision.md", TODAY)))

    def test_same_record_with_a_decision_passes(self):
        r = cr.check(FIX / "accepted-with-decision.md", TODAY)
        self.assertEqual(r["errors"], [])
        self.assertEqual(r["gate_state"], "closed")

    def test_accepted_with_blank_rationale_fails(self):
        self.assertIn("DR-02", codes(cr.check(FIX / "accepted-blank-rationale.md", TODAY)))

    def test_proxy_signature_never_closes(self):
        r = cr.check(FIX / "accepted-proxy-signature.md", TODAY)
        self.assertIn("DR-04", codes(r))
        self.assertIn("fired (proxy)", r["gate_state"])
        self.assertNotEqual(r["gate_state"], "closed")

    def test_unwalked_register_row_keeps_the_gate_open(self):
        r = cr.check(FIX / "accepted-unwalked-register.md", TODAY)
        self.assertIn("DR-06", codes(r))
        self.assertNotEqual(r["gate_state"], "closed")

    def test_two_statuses_is_an_error(self):
        self.assertIn("DR-05", codes(cr.check(FIX / "status-contradiction.md", TODAY)))

    def test_unpicked_scaffold_status_is_not_accepted(self):
        r = cr.check(FIX / "proposed-scaffold.md", TODAY)
        self.assertEqual(r["status"], "unset")
        self.assertEqual(r["errors"], [])

    def test_cli_exit_codes(self):
        self.assertEqual(cr.main([str(FIX / "accepted-with-decision.md"), "--today", "2026-11-22"]), 0)
        self.assertEqual(cr.main([str(FIX / "accepted-blank-decision.md"), "--today", "2026-11-22"]), 1)
        self.assertEqual(cr.main([str(FIX / "does-not-exist.md")]), 2)


class Inline(unittest.TestCase):
    """Records written in the deployed scaffold's own heading form (em dash in the heading)."""

    def run_text(self, text: str, today: dt.date = TODAY) -> dict:
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "r.md"
            p.write_text(text, encoding="utf-8")
            return cr.check(p, today)

    def scaffold(self, decision="______", signed="______", opened="2026-11-01", max_age="7",
                 proxy="no") -> str:
        dash = "\u2014"
        return (
            "# Decision Record " + dash + " t\nStatus: accepted   Date: ______\n\n"
            f"## ⛔ Decision {dash} NEEDS HUMAN\nThis slot is intentionally empty. The decision is"
            f" the Approver's to make and record.\n   Decision: {decision}\n\n"
            f"## ⛔ Rationale {dash} NEEDS HUMAN\nThis slot is intentionally empty. Articulating"
            " *why* is the mechanism; the skill does\nnot write it for you.\n   Why: because\n\n"
            "## Uncertain calls\nnone\n\n"
            f"## Named gate\nOwner: A   Opened: {opened}   Max age (days): {max_age}   Escalate to: E\n"
            f"Approver sign-off: {signed}   Date: ______   Proxy: {proxy}   Where: ______\n")

    def test_em_dash_headings_parse(self):
        self.assertIn("DR-01", codes(self.run_text(self.scaffold())))
        ok = self.run_text(self.scaffold(decision="ship it", signed="A"))
        self.assertEqual(ok["errors"], [])

    def test_unsigned_past_window_is_aged(self):
        r = self.run_text(self.scaffold())
        self.assertIn("W-02", codes(r, "warnings"))
        self.assertTrue(r["gate_state"].startswith("aged"))

    def test_no_max_age_reads_as_aged(self):
        r = self.run_text(self.scaffold(max_age="______"), today=dt.date(2026, 11, 2))
        self.assertIn("W-02", codes(r, "warnings"))

    def test_unclear_proxy_never_closes(self):
        r = self.run_text(self.scaffold(decision="ship it", signed="A", proxy="[ no | yes ]"))
        self.assertNotEqual(r["gate_state"], "closed")
        self.assertIn("W-04", codes(r, "warnings"))

    def test_signature_by_someone_else_never_closes(self):
        r = self.run_text(self.scaffold(decision="ship it", signed="Someone Else"))
        self.assertIn("DR-07", codes(r))
        self.assertNotEqual(r["gate_state"], "closed")

    def test_blank_or_missing_proxy_never_closes(self):
        for proxy in ("____", "maybe"):
            r = self.run_text(self.scaffold(decision="ship it", signed="A", proxy=proxy))
            self.assertIn("DR-09", codes(r), proxy)
        r = self.run_text(self.scaffold(decision="ship it", signed="A").replace("   Proxy: no", ""))
        self.assertIn("DR-09", codes(r))

    def test_placeholder_decisions_are_blank(self):
        for d in ("TBD.", "pending", "[the Approver writes the decision here]", "____."):
            self.assertIn("DR-01", codes(self.run_text(self.scaffold(decision=d, signed="A"))), d)

    def test_status_with_trailing_punctuation_is_still_accepted(self):
        text = self.scaffold(decision="______", signed="A").replace("Status: accepted", "Status: accepted.")
        self.assertIn("DR-01", codes(self.run_text(text)))

    def test_proxy_walk_and_rationale_row(self):
        reg = ("## Drawn-by-default register\n| Slot | Drawn | Alternative | Redraw cost | Walked by | Walk by |\n"
               "|---|---|---|---|---|---|\n| Decision | a | b | c | Ops (proxy) | 2026-11-30 |\n"
               "| Rationale | x | y | z | A | 2026-11-30 |\n\n")
        text = self.scaffold(decision="ship it", signed="A").replace("## Named gate", reg + "## Named gate")
        r = self.run_text(text)
        self.assertIn("DR-06", codes(r))
        self.assertIn("DR-08", codes(r))

    def test_missing_uncertain_calls_warns(self):
        text = self.scaffold(decision="x", signed="A").replace("## Uncertain calls\nnone\n\n", "")
        self.assertIn("W-03", codes(self.run_text(text), "warnings"))

    def test_a_proxy_mention_off_the_signature_line_never_counts(self):
        # G-F-1 F2: with no Proxy on the signature line, a "Proxy: no" anywhere else in the gate
        # (an instruction sentence, a note) must not close the record.
        text = (self.scaffold(decision="ship it", signed="A").replace("   Proxy: no", "")
                + "The Owner signs in person and writes Proxy: no.\n")
        r = self.run_text(text)
        self.assertIn("DR-09", codes(r))
        self.assertNotEqual(r["gate_state"], "closed")

    def test_only_the_owners_walk_closes_a_register_row(self):
        # G-F-1 F3: Walked by must be the gate's owner (os/session-rules.md `walked_by`).
        def reg(who: str) -> str:
            return ("## Drawn-by-default register\n| Slot | Drawn | Alternative | Redraw cost | Walked by | Walk by |\n"
                    f"|---|---|---|---|---|---|\n| Decision | a | b | c | {who} | 2026-11-30 |\n\n")
        base = self.scaffold(decision="ship it", signed="A")
        self.assertIn("DR-06", codes(self.run_text(base.replace("## Named gate", reg("Someone Else") + "## Named gate"))))
        ok = self.run_text(base.replace("## Named gate", reg("A") + "## Named gate"))
        self.assertEqual(ok["errors"], [])
        self.assertEqual(ok["gate_state"], "closed")


def scaffold_gate_lines() -> list[str] | None:
    """The Mode A Named gate's instruction lines as the skill ships them: from the deployed
    SKILL.md once promoted, or from this draft's PATCH.md NEW block while staged."""
    pat = re.compile(r"## Named gate\nOwner \(the Approver above\):[^\n]*\nApprover sign-off:[^\n]*\n"
                     r"(.*?\nBefore marking accepted:[^\n]*)", re.S)
    for cand in (HERE.parent / "SKILL.md", HERE.parents[1] / "PATCH.md"):
        if cand.is_file():
            m = pat.search(cand.read_text(encoding="utf-8"))
            if m:
                return m.group(1).splitlines()
    return None


REAL = sorted(FIX.glob("real-scaffold-*.md"))


class RealScaffold(unittest.TestCase):
    """Fixtures built from the v0.3.0 Mode A scaffold's own text (G-F-1 F1, F2, F3, F6)."""

    def test_fixtures_carry_the_scaffold_gate_verbatim(self):
        lines = scaffold_gate_lines()
        self.assertIsNotNone(lines, "the Mode A scaffold's Named gate was not found")
        self.assertEqual(len(REAL), 5)
        for line in lines:
            # The instruction sentence must not hold a Proxy value the check could read (F2).
            self.assertIsNone(re.search(r"Proxy:\s*(no|yes)\b", line, re.I), line)
        for f in REAL:
            text = f.read_text(encoding="utf-8")
            self.assertIn("Owner (the Approver above): Approver A", text, f.name)
            for line in lines:
                self.assertIn(line, text, f"{f.name}: {line!r}")

    def test_owner_signed_record_in_the_scaffold_labels_closes(self):
        r = cr.check(FIX / "real-scaffold-owner-signed.md", TODAY)
        self.assertEqual(r["errors"], [])
        self.assertEqual(r["warnings"], [])
        self.assertEqual(r["gate_state"], "closed")

    def test_no_proxy_on_the_signature_line_fails_closed(self):
        r = cr.check(FIX / "real-scaffold-no-proxy-on-signature.md", TODAY)
        self.assertIn("DR-09", codes(r))
        self.assertNotIn("DR-07", codes(r))
        self.assertNotEqual(r["gate_state"], "closed")

    def test_a_walk_by_someone_other_than_the_owner_is_not_a_walk(self):
        r = cr.check(FIX / "real-scaffold-walked-by-non-owner.md", TODAY)
        self.assertEqual(codes(r), {"DR-06"})
        self.assertNotEqual(r["gate_state"], "closed")

    def test_a_register_under_a_level_three_heading_is_read(self):
        r = cr.check(FIX / "real-scaffold-register-under-h3.md", TODAY)
        self.assertEqual(codes(r), {"DR-06"})

    def test_a_bolded_body_status_counts(self):
        r = cr.check(FIX / "real-scaffold-bold-status.md", TODAY)
        self.assertEqual(r["status"], "accepted")
        self.assertEqual(codes(r), {"DR-01"})


if __name__ == "__main__":
    unittest.main()
