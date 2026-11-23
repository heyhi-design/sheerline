#!/usr/bin/env python3
"""Count feedback uptake from a capture: feedback item against work change (references/uptake-audit.md).

    python3 scripts/uptake_count.py <capture.md> --review-date YYYY-MM-DD --window-days N
                                    [--json] [--append-csv <engagement folder>/grades/uptake-audit.csv]

Reads every markdown table in the capture that has a Disposition column and an Answered by
column (a Mode B Crit Capture, or a revision plan). Prints the counts, both rates and the
unanswered rows. It reports numbers only: no threshold, no grade, no verdict (the calibration
stays with the instance). Capture rows carry no dates, so the window is not a filter: run the
audit at or after the window's end; a run before it is reported PARTIAL. `--append-csv` refuses
a path git would track. Stdlib only.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

BLANK = {"", "tbd", "todo", "tba", "pending", "none", "n/a", "na", "-", "?",
         "\u2014", "\u2013", "\u2691"}
FIELDS = ["audited_on", "review_date", "window_days", "partial", "source", "items", "answered",
          "deferred", "dropped", "unanswered", "rate_all", "rate_open"]
UNESCAPED_PIPE = re.compile(r"(?<!\\)\|")


def is_blank(value: str) -> bool:
    """Blank: nothing but placeholder marks, bracketed placeholder text, or a stand-in word."""
    text = re.sub(r"\[[^\]]*\]", " ", value or "")
    text = re.sub(r"[_*`]+", " ", text)
    text = re.sub(r"^[\s.,;:!?]+|[\s.,;:!?]+$", "", text.strip()).lower()
    return text in BLANK


def split_row(line: str) -> list[str]:
    """Cells of one table row; an escaped pipe (`\\|`) stays inside its cell."""
    return [c.strip().replace("\\|", "|") for c in UNESCAPED_PIPE.split(line.strip().strip("|"))]


def tables(text: str) -> list[tuple[list[str], list[list[str]]]]:
    out, block = [], []
    for line in text.splitlines() + [""]:
        if line.strip().startswith("|"):
            block.append(line)
        elif block:
            cells = [split_row(ln) for ln in block]
            if len(cells) >= 2:
                body = [r for r in cells[1:] if not all(re.fullmatch(r":?-{3,}:?", c) for c in r if c)]
                out.append(([h.lower() for h in cells[0]], body))
            block = []
    return out


def col(head: list[str], word: str) -> int | None:
    for i, h in enumerate(head):
        if h.startswith(word):
            return i
    return None


def count(text: str) -> dict:
    rows = []
    for head, body in tables(text):
        d, a = col(head, "disposition"), col(head, "answered by")
        if d is None or a is None:
            continue
        n = col(head, "#")
        for i, r in enumerate(body, 1):
            r = r + [""] * (len(head) - len(r))
            rows.append({"row": r[n] if n is not None and r[n] else str(i),
                         "disposition": r[d].strip("`* .").lower(),
                         "answered": not is_blank(r[a])})
    if not rows:
        raise ValueError("no table with both a Disposition and an Answered by column")
    items = len(rows)
    answered = sum(r["answered"] for r in rows)
    deferred = sum(1 for r in rows if not r["answered"] and r["disposition"] == "deferred")
    dropped = sum(1 for r in rows if not r["answered"] and r["disposition"] == "dropped")
    unanswered = [r["row"] for r in rows
                  if not r["answered"] and r["disposition"] not in ("deferred", "dropped")]
    open_ = items - deferred - dropped
    return {"items": items, "answered": answered, "deferred": deferred, "dropped": dropped,
            "unanswered": len(unanswered), "unanswered_rows": unanswered,
            "rate_all": round(answered / items, 3),
            "rate_open": round(answered / open_, 3) if open_ else None}


def git_would_track(path: Path) -> bool:
    """True when `path` sits in a git work tree and is not ignored there."""
    where = path.resolve().parent
    while not where.exists():
        where = where.parent
    inside = subprocess.run(["git", "-C", str(where), "rev-parse", "--is-inside-work-tree"],
                            capture_output=True, text=True)
    if inside.returncode != 0:
        return False
    ignored = subprocess.run(["git", "-C", str(where), "check-ignore", "-q", str(path.resolve())],
                             capture_output=True)
    return ignored.returncode != 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Uptake count: feedback item against work change.")
    ap.add_argument("capture")
    ap.add_argument("--review-date", required=True)
    ap.add_argument("--window-days", type=int, required=True)
    ap.add_argument("--today", help="YYYY-MM-DD, read against the window's end (default: local date)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--append-csv", help="the engagement's series file (gitignored path only)")
    args = ap.parse_args(argv)
    try:
        review = dt.date.fromisoformat(args.review_date)
        today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()
        result = count(Path(args.capture).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"uptake_count: cannot read {args.capture}: {exc}", file=sys.stderr)
        return 2
    window_end = review + dt.timedelta(days=args.window_days)
    result.update({"review_date": review.isoformat(), "window_days": args.window_days,
                   "window_end": window_end.isoformat(), "partial": today < window_end,
                   "source": Path(args.capture).name})
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"uptake: {result['answered']}/{result['items']} answered "
              f"(rate {result['rate_all']}; excluding deferred and dropped: {result['rate_open']}) "
              f"· deferred {result['deferred']} · dropped {result['dropped']} "
              f"· unanswered {result['unanswered']} {result['unanswered_rows']} "
              f"· window {result['review_date']} to {result['window_end']}"
              + (" · PARTIAL: the window has not closed, so this is an interim reading"
                 if result["partial"] else ""))
    if args.append_csv:
        target = Path(args.append_csv)
        if git_would_track(target):
            print(f"uptake_count: refusing {target}: git would track it; the series belongs in a "
                  "gitignored engagement folder", file=sys.stderr)
            return 2
        new = not target.exists()
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("a", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=FIELDS)
            if new:
                w.writeheader()
            w.writerow({**{k: result.get(k) for k in FIELDS},
                        "audited_on": dt.date.today().isoformat()})
        print(f"uptake_count: appended one row to {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
