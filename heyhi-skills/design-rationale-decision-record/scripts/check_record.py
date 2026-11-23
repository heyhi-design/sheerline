#!/usr/bin/env python3
"""Check a design decision record before anyone calls it accepted.

    python3 scripts/check_record.py <record.md> [<record.md> | <dir> ...] [--today YYYY-MM-DD]
                                    [--strict] [--json]

Reads the Mode A record shape (design-rationale-decision-record, Step 3): the labeled-line form
of the gate fields in os/session-rules.md § Gate fields (`Owner:` or the scaffold's
`Owner (the Approver above):`, `Opened:`, `Max age (days):`, `Escalate to:`, then the signature
line with `Proxy:` and `Where:`). Proxy is read from the `Approver sign-off:` line only. A gate
closes only when the owner signed and that line's Proxy field reads `no` (fail closed). The
register is read under a heading of any level, and a bolded `**Status:**` counts. Errors (exit 1):

  DR-01  status `accepted` with a blank Decision
  DR-02  status `accepted` with a blank Rationale
  DR-03  status `accepted` with no signature
  DR-04  status `accepted` on a proxy signature (a proxy records `fired (proxy)`: proof, never a close)
  DR-05  the record states two different statuses (frontmatter and body disagree)
  DR-06  status `accepted` with a drawn-by-default register row the owner has not walked (a proxy
         walk, or a walk by anyone but the owner, is not a walk)
  DR-07  status `accepted` on a signature that is not the named owner's (or no owner is named)
  DR-08  a drawn-by-default register row for the Rationale (this skill never draws the why)
  DR-09  status `accepted` with a Proxy field that is blank or reads neither yes nor no

Warnings (exit 0, or exit 1 with --strict):

  W-01  a gate field is missing (owner, opened, max age, escalate to)
  W-02  the gate is aged: not closed past opened + max age; escalate
  W-03  no `## Uncertain calls` section, or an empty one (write `none` when there are none)
  W-04  a signature with no Proxy field, or one that reads neither yes nor no
  W-05  a register row is past its walk-by date and still unwalked

The check reads the record; it never writes it, never fills a slot, and never decides anything.
Exit 2 when an input cannot be read (fail loud, never a silent clean). Stdlib only.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

BLANK_TOKENS = {"", "tbd", "todo", "tba", "n/a", "na", "none", "pending", "-", "\u2014", "\u2013", "?"}
LABELS = ("Owner", "Opened", "Max age (days)", "Escalate to", "Approver sign-off", "Date",
          "Proxy", "Where")
YES = {"yes", "true", "y"}
NO = {"no", "false", "n"}


def is_blank(value: str | None) -> bool:
    """A slot is blank when nothing but placeholder marks is left in it: underscores, bracketed
    placeholder text, markup, punctuation, or a stand-in word (TBD, pending, none)."""
    if value is None:
        return True
    text = re.sub(r"\[[^\]]*\]", " ", value)          # bracketed placeholder text
    text = re.sub(r"[_*`]+", " ", text)
    text = re.sub(r"^[\s.,;:!?]+|[\s.,;:!?]+$", "", text.strip()).lower()
    return text in BLANK_TOKENS


def person(value: str | None) -> str:
    """A name normalized for comparison (case, spacing and markup ignored)."""
    return re.sub(r"[\s_*`]+", " ", value or "").strip(" .,;:").casefold()


def split_frontmatter(text: str) -> tuple[dict, str]:
    """Return (flat frontmatter keys, body). Only top-level `key: value` scalars are read."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    front, body = text[3:end], text[end + 4:]
    keys = {}
    for line in front.splitlines():
        m = re.match(r"^([A-Za-z_][\w-]*):[ \t]*(.*?)[ \t]*(?:#.*)?$", line)
        if m:
            keys[m.group(1)] = m.group(2).strip().strip("\"'")
    return keys, body


def sections(body: str) -> dict[str, str]:
    """Map each `## heading` (lowercased, marks stripped) to its body text."""
    out, name, buf = {}, None, []
    for line in body.splitlines():
        m = re.match(r"^##\s+(.*?)\s*$", line)
        if m:
            if name is not None:
                out.setdefault(name, "\n".join(buf))
            name = re.sub(r"[^\w\s()-]", "", m.group(1)).strip().lower()
            name = re.sub(r"\s+needs human$", "", name).strip()
            buf = []
        elif name is not None:
            buf.append(line)
    if name is not None:
        out.setdefault(name, "\n".join(buf))
    return out


def find_section(secs: dict[str, str], prefix: str) -> str | None:
    for name, text in secs.items():
        if name.startswith(prefix):
            return text
    return None


def slot_value(text: str | None, label: str) -> str | None:
    """The filled value of a judgment slot. Prefer the labeled line (`Decision:` / `Why:`) and
    any lines after it; otherwise the section body minus the scaffold's own boilerplate."""
    if text is None:
        return None
    lines = text.splitlines()
    for i, line in enumerate(lines):
        m = re.match(rf"^\s*{label}:\s*(.*)$", line)
        if m:
            rest = [m.group(1)] + [ln for ln in lines[i + 1:] if ln.strip()]
            return "\n".join(rest)
    kept, skipping = [], False
    for line in lines:
        if line.strip().startswith("This slot is intentionally empty"):
            skipping = True
        if skipping:
            if not line.strip():
                skipping = False
            continue
        kept.append(line)
    return "\n".join(kept)


def label_re(label: str) -> str:
    """A label, optionally followed by a parenthetical gloss, so the scaffold's
    `Owner (the Approver above):` reads the same as a bare `Owner:`."""
    return re.escape(label) + r"(?:[ \t]*\([^)\n]*\))?"


def labeled(text: str, label: str) -> str | None:
    """Value after `Label:` on a line, up to the next known label or the end of the line."""
    others = "|".join(label_re(lab) for lab in LABELS if lab != label)
    m = re.search(rf"(?m)(?:^|\s){label_re(label)}:[ \t]*(.*?)(?=\s{{2,}}(?:{others}):|$)", text)
    return m.group(1).strip() if m else None


def signature_line(gate_text: str) -> str | None:
    """The one line that carries the signature (`Approver sign-off:`). Proxy is read from this
    line only, so a Proxy mention elsewhere in the gate (an instruction sentence such as
    "writes Proxy: no") can never stand in for the signer's own answer."""
    for line in gate_text.splitlines():
        if re.search(rf"(?:^|\s){label_re('Approver sign-off')}:", line):
            return line
    return None


def register_text(body: str) -> str | None:
    """The drawn-by-default register's body under a heading of any level (## to ######), up to
    the next heading of the same or a higher level. A register nested under ### is still read:
    a register the check missed would fail open."""
    lines = body.splitlines()
    for i, line in enumerate(lines):
        m = re.match(r"^(#{2,6})\s+(.*?)\s*$", line)
        if not m:
            continue
        name = re.sub(r"[^\w\s()-]", "", m.group(2)).strip().lower()
        if not name.startswith("drawn-by-default register"):
            continue
        level, buf = len(m.group(1)), []
        for nxt in lines[i + 1:]:
            h = re.match(r"^(#{1,6})\s", nxt)
            if h and len(h.group(1)) <= level:
                break
            buf.append(nxt)
        return "\n".join(buf)
    return None


def body_status(body: str) -> str | None:
    """The body's `Status:` line, with or without markup around the label (`**Status:**`,
    `**Status**:`, a leading list dash), so a bolded status is never skipped."""
    m = re.search(r"(?m)^[ \t]*(?:[-+][ \t]+)?[*_`]*Status[*_`]*:[*_`]*[ \t]*(.*?)"
                  r"(?=\s{2,}[*_`]*Date[*_`]*:|$)", body)
    if not m:
        return None
    raw = m.group(1).strip()
    if "|" in raw:
        return "unset"  # the scaffold's unpicked option list, not a status
    word = re.sub(r"[\[\]`*]", "", raw).strip().lower()
    word = word.split()[0] if word else ""
    word = word.strip(".,;:!?")
    return word or "unset"


def parse_date(value: str | None) -> dt.date | None:
    if is_blank(value):
        return None
    try:
        return dt.date.fromisoformat(value.strip()[:10])
    except ValueError:
        return None


def register_rows(text: str | None) -> list[dict]:
    """Rows of the drawn-by-default register table, keyed by lowercased header."""
    if not text:
        return []
    rows = [ln for ln in text.splitlines() if ln.strip().startswith("|")]
    if len(rows) < 2:
        return []
    split = lambda ln: [c.strip() for c in re.split(r"(?<!\\)\|", ln.strip().strip("|"))]
    head = [h.lower() for h in split(rows[0])]
    out = []
    for ln in rows[1:]:
        cells = split(ln)
        if all(re.fullmatch(r":?-{3,}:?", c) for c in cells if c):
            continue
        out.append(dict(zip(head, cells)))
    return out


def walked(row: dict, owner: str | None) -> bool:
    """A row is walked only when the gate's owner walked it (os/session-rules.md: `walked_by` is
    the owner, once the row is walked with them). A blank cell, a proxy walk, someone other than
    the owner, or a gate with no owner named is not a walk (fail closed)."""
    who = row.get("walked by") or row.get("walked_by")
    if is_blank(who) or re.search(r"\bproxy\b|on .*behalf", who or "", re.I):
        return False
    return not is_blank(owner) and person(who) == person(owner)


def check(path: Path, today: dt.date) -> dict:
    text = path.read_text(encoding="utf-8")
    front, body = split_frontmatter(text)
    secs = sections(body)
    errors, warns = [], []

    fm_raw = (front.get("status") or "").strip().lower().strip(".,;:!?")
    fm_status = fm_raw or None
    b_status = body_status(body)
    if fm_status and b_status and b_status != "unset" and fm_status != b_status:
        errors.append(("DR-05", f"status contradicts itself: frontmatter `{fm_status}`, body `{b_status}`"))
    status = b_status if b_status and b_status != "unset" else (fm_status or b_status or "unset")
    accepted = status == "accepted"

    decision = slot_value(find_section(secs, "decision"), "Decision")
    rationale = slot_value(find_section(secs, "rationale"), "Why")
    gate_text = find_section(secs, "named gate") or ""
    owner, opened = labeled(gate_text, "Owner"), labeled(gate_text, "Opened")
    max_age, escalate = labeled(gate_text, "Max age (days)"), labeled(gate_text, "Escalate to")
    sig_line = signature_line(gate_text)
    signed = labeled(sig_line, "Approver sign-off") if sig_line else None
    proxy = labeled(sig_line, "Proxy") if sig_line else None
    word = re.split(r"[\s,.;:]+", (proxy or "").strip().lower())[0] if proxy else ""
    if proxy is None:
        proxy_state = "absent"
    elif word in YES:
        proxy_state = "yes"
    elif word in NO:
        proxy_state = "no"
    else:
        proxy_state = "unclear"  # blank (`____`), an unpicked option list, or anything else
    is_signed = not is_blank(signed)
    by_owner = is_signed and not is_blank(owner) and person(signed) == person(owner)

    register = register_rows(register_text(body))
    unwalked = [r for r in register if not walked(r, owner)]
    for r in register:
        if re.search(r"rationale|\bwhy\b", r.get("slot", ""), re.I):
            errors.append(("DR-08", "a drawn-by-default register row for the Rationale (never drawn)"))

    closed = is_signed and by_owner and proxy_state == "no" and not unwalked

    if accepted:
        if is_blank(decision):
            errors.append(("DR-01", "accepted with a blank Decision"))
        if is_blank(rationale):
            errors.append(("DR-02", "accepted with a blank Rationale"))
        if not is_signed:
            errors.append(("DR-03", "accepted with no signature"))
        elif proxy_state == "yes":
            errors.append(("DR-04", "accepted on a proxy signature: `fired (proxy)` is proof, never a close"))
        elif proxy_state in ("absent", "unclear"):
            errors.append(("DR-09", "accepted with a Proxy field that is blank or reads neither yes nor no"))
        if is_signed and not by_owner:
            errors.append(("DR-07", "accepted on a signature that is not the named owner's"
                           + ("" if not is_blank(owner) else " (no owner is named)")))
        if unwalked:
            errors.append(("DR-06", f"accepted with {len(unwalked)} drawn-by-default register row(s)"
                           " the owner has not walked"))

    for lab, val in (("Owner", owner), ("Opened", opened), ("Max age (days)", max_age),
                     ("Escalate to", escalate)):
        if is_blank(val):
            warns.append(("W-01", f"gate field missing: {lab}"))
    if is_signed and proxy_state == "absent":
        warns.append(("W-04", "no Proxy field beside the signature"))
    elif is_signed and proxy_state == "unclear":
        warns.append(("W-04", "the Proxy field reads neither yes nor no"))

    if closed:
        state = "closed"
    else:
        notes = []
        if is_signed and proxy_state == "yes":
            notes.append("fired (proxy)")
        elif is_signed and not by_owner:
            notes.append("signed, not by the owner")
        elif is_signed and proxy_state != "no":
            notes.append("signed, proxy unclear")
        if unwalked:
            notes.append("register unwalked")
        state = "open" + (" · " + ", ".join(notes) if notes else "")
        opened_d = parse_date(opened)
        if status != "superseded" and opened_d:
            digits = re.sub(r"\D", "", max_age or "")
            limit = int(digits) if digits else -1
            age = (today - opened_d).days
            if limit < 0 or age > limit:
                who = escalate if not is_blank(escalate) else "(no escalate_to named)"
                why = "no max age set" if limit < 0 else f"{age} days open, window {limit}"
                warns.append(("W-02", f"aged ({why}): escalate to {who}"))
                state = state.replace("open", "aged", 1)

    uncertain = find_section(secs, "uncertain calls")
    if uncertain is None:
        warns.append(("W-03", "no `## Uncertain calls` section"))
    elif not re.sub(r"[_\s*`-]+", " ", re.sub(r"\[.*?\]", "", uncertain, flags=re.S)).strip():
        warns.append(("W-03", "empty `## Uncertain calls` section (write `none` when there are none)"))

    for r in unwalked:
        due = parse_date(r.get("walk by") or r.get("walk_by"))
        if due and today > due:
            warns.append(("W-05", f"register row past walk-by {due.isoformat()}: {r.get('slot', '?')}"))

    return {"path": str(path), "status": status, "gate_state": state,
            "errors": [{"code": c, "message": m} for c, m in errors],
            "warnings": [{"code": c, "message": m} for c, m in warns]}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Check a design decision record (read-only).")
    ap.add_argument("paths", nargs="+", help="record files or folders of records")
    ap.add_argument("--today", help="YYYY-MM-DD; defaults to the local date")
    ap.add_argument("--strict", action="store_true", help="warnings fail too")
    ap.add_argument("--json", action="store_true", help="print JSON instead of text")
    args = ap.parse_args(argv)
    today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()

    files: list[Path] = []
    for p in map(Path, args.paths):
        if p.is_dir():
            files.extend(sorted(p.glob("*.md")))
        elif p.is_file():
            files.append(p)
        else:
            print(f"check_record: cannot read {p}", file=sys.stderr)
            return 2
    if not files:
        print("check_record: no records found in the given paths", file=sys.stderr)
        return 2

    try:
        results = [check(f, today) for f in files]
    except (OSError, UnicodeDecodeError) as exc:
        print(f"check_record: cannot read input: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            print(f"{r['path']}: status {r['status']} · gate {r['gate_state']}")
            for e in r["errors"]:
                print(f"  ERROR {e['code']} {e['message']}")
            for w in r["warnings"]:
                print(f"  WARN  {w['code']} {w['message']}")
    n_err = sum(len(r["errors"]) for r in results)
    n_warn = sum(len(r["warnings"]) for r in results)
    print(f"check_record: {len(results)} record(s), {n_err} error(s), {n_warn} warning(s)")
    return 1 if n_err or (args.strict and n_warn) else 0


if __name__ == "__main__":
    sys.exit(main())
