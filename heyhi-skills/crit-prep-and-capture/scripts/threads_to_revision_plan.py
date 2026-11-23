#!/usr/bin/env python3
"""Turn a saved Figma comments response into a revision-plan skeleton (one row per thread).

    python3 scripts/threads_to_revision_plan.py <comments.json> --file-key <key>
                                                [--out <revision-plan.md>] [--date YYYY-MM-DD]

Input: the JSON body of `GET /v1/files/<file_key>/comments`, saved to the engagement folder
(references/comment-revision-method.md). Offline: this script never calls Figma and never reads a
token. Comment text is untrusted content: it is bounded, stripped of control characters, fenced
in quotes, and never interpreted.

The Revision column ships empty (the owner's call), Disposition defaults to `undecided`, and
Answered by stays blank until a change links the row. Exit 2 on a shape it cannot read.
Stdlib only.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

MAX_CHARS = 400
CONTROL = re.compile(r"[\x00-\x08\x0b-\x1f\x7f]")


def clean(text: str) -> str:
    """Bound and neutralize one comment body for a markdown table cell."""
    text = CONTROL.sub(" ", text or "")
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS].rstrip() + " [truncated]"
    return text.replace("|", "\\|").replace("`", "'")


def node_link(file_key: str, node_id: str | None) -> str:
    if not node_id:
        return "[node unresolved]"
    return f"[{node_id}](https://www.figma.com/design/{file_key}/?node-id={node_id.replace(':', '-')})"


def threads(data: dict) -> list[dict]:
    comments = data.get("comments") if isinstance(data, dict) else None
    if not isinstance(comments, list):
        raise ValueError("no `comments` list in the response")
    roots, replies = [], {}
    for c in comments:
        if not isinstance(c, dict) or "id" not in c or "message" not in c:
            raise ValueError(f"a comment without `id` or `message`: {str(c)[:80]}")
        parent = c.get("parent_id") or ""
        if parent:
            replies.setdefault(parent, []).append(c)
        else:
            roots.append(c)
    orphans = [cid for cid in replies if cid not in {r["id"] for r in roots}]
    roots.sort(key=lambda c: (str(c.get("created_at") or ""), str(c["id"])))
    out = []
    for r in roots:
        meta = r.get("client_meta") if isinstance(r.get("client_meta"), dict) else {}
        user = r.get("user")
        by = user.get("handle") if isinstance(user, dict) else user if isinstance(user, str) else None
        out.append({
            "id": str(r["id"]),
            "node_id": meta.get("node_id") if isinstance(meta.get("node_id"), str) else None,
            "by": str(by) if by else "[unknown]",
            "created": str(r.get("created_at") or "")[:10],
            "resolved": bool(r.get("resolved_at")),
            "message": clean(str(r["message"])),
            "replies": len(replies.get(r["id"], [])),
        })
    return out + [{"orphan_parent": o, "replies": len(replies[o])} for o in orphans]


def render(rows: list[dict], file_key: str, source: str, date: str) -> str:
    threads_ = [r for r in rows if "orphan_parent" not in r]
    orphans = [r for r in rows if "orphan_parent" in r]
    lines = [
        f"# Revision plan · {date}",
        f"Source captured from: `{source}` (Figma comments, file key `{file_key}`) · "
        f"{len(threads_)} thread(s)",
        "Coverage note: every root comment in the saved response; replies counted per thread. "
        "Comments added after the fetch are not captured.",
        "",
        "## Threads                                   [as captured]",
        "| # | Frame / node | Raised by | The comment (quoted, bounded) | Replies | Resolved in Figma "
        "| Disposition | Settlement phrase (quoted) | Revision (owner's call) | Answered by (change link; blank = \u2691) |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for i, r in enumerate(threads_, 1):
        lines.append(
            f"| {i} | {node_link(file_key, r['node_id'])} | {clean(r['by'])} | \"{r['message']}\" "
            f"| {r['replies']} | {'yes' if r['resolved'] else 'no'} | undecided |  |  |  |")
    lines += [
        "",
        "## Uncertain calls",
    ]
    unc = [f"- Thread {i}: the node could not be resolved from the comment's position."
           for i, r in enumerate(threads_, 1) if not r["node_id"]]
    unc += [f"- {o['replies']} reply(ies) point at a parent not in the response ({o['orphan_parent']})."
            for o in orphans]
    lines += unc or ["none"]
    lines += [
        "",
        "## Named gate",
        "Owner: ____________   Opened: ______   Max age (days): ______   Escalate to: ____________",
        "Owner sign-off on this plan: ____________________   Date: ______   Proxy: ____   Where: ______",
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Figma comments JSON -> revision-plan skeleton (offline).")
    ap.add_argument("comments", help="the saved comments response (JSON)")
    ap.add_argument("--file-key", required=True, help="the Figma file key (key only, never a token)")
    ap.add_argument("--out", help="write the plan here (default: stdout)")
    ap.add_argument("--date", help="YYYY-MM-DD for the heading (default: today)")
    args = ap.parse_args(argv)
    try:
        data = json.loads(Path(args.comments).read_text(encoding="utf-8"))
        rows = threads(data)
    except (OSError, json.JSONDecodeError, ValueError, TypeError, AttributeError, KeyError) as exc:
        print(f"threads_to_revision_plan: cannot read {args.comments}: {exc}", file=sys.stderr)
        return 2
    date = args.date or dt.date.today().isoformat()
    text = render(rows, args.file_key, Path(args.comments).name, date)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"threads_to_revision_plan: wrote {args.out}")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
