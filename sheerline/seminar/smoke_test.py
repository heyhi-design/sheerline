#!/usr/bin/env python3
"""Sheerline seminar — curriculum structural smoke test.

Checks every module (track-*/module-*.md) against the module template contract:
frontmatter completeness, the exact eight sections, real paths (opens_files, backticked
repo paths, AND inter-module links resolved against the module's own directory), a valid
acyclic prereq DAG, the voice rules, and the keel/Sheerline separability line (body +
opens_files).

Run from anywhere:  python3 sheerline/seminar/smoke_test.py
Exit 0 = clean · exit 1 = one or more failures printed.

No external dependencies — a tiny frontmatter parser handles the flat frontmatter these
modules use.
"""
import os, re, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))

REQUIRED_SECTIONS = [
    "You are here", "Learning objectives", "Concept", "Walkthrough",
    "Lab", "Common misreads", "Self-check", "Go deeper",
]
REQUIRED_FM = ["classification", "title", "track", "module", "level",
               "prereqs", "est_minutes", "teaches", "opens_files"]
# Whole-word banned terms that never have a legitimate technical sense here.
# (solution / deliverable / ecosystem / paradigm are context-dependent — human review, not here.)
BANNED = ["leverage", "unlock", "supercharge", "disrupt", "synergy", "cutting-edge",
          "next-gen", "revolutionary", "game-changing", "empower", "holistic", "seamless",
          "best-in-class", "world-class", "transformative", "innovative", "10x", "full-service"]
BANNED_PHRASES = ["digital experiences", "stakeholder alignment"]
# A teaches:keel module may not lean on a Confidential Sheerline internal (body or opens_files).
SHEERLINE_INTERNAL = ["sheerline/os/", "sheerline/skills/", "sheerline/profile/", "heyhi-mcp/",
                      "ai-services/"]
FILE_EXT = re.compile(r"\.[A-Za-z0-9]{1,5}$")

# An exported copy (the private sheerline repo) carries EXPORT.json at its root listing the
# roots it ships. There, a repo-root path outside those roots is a pointer back to the HeyHi
# monorepo: counted and reported, not checked. A path INSIDE a shipped root must still resolve.
# In the monorepo every path is checked, exactly as before: the marker is ignored wherever
# ai-services/ exists, so a stray EXPORT.json cannot switch the monorepo into skip mode.
SHIPPED_ROOTS = None
_marker = os.path.join(REPO_ROOT, "EXPORT.json")
if os.path.isfile(_marker) and not os.path.isdir(os.path.join(REPO_ROOT, "ai-services")):
    import json
    SHIPPED_ROOTS = [r.rstrip("/") for r in json.load(open(_marker, encoding="utf-8"))["roots"]]
EXTERNAL_POINTERS = set()


def is_external(p):
    """True when p is a repo-root path the exported copy deliberately does not ship."""
    if SHIPPED_ROOTS is None:
        return False
    p = os.path.normpath(p)
    if any(p == r or p.startswith(r + "/") for r in SHIPPED_ROOTS):
        return False
    EXTERNAL_POINTERS.add(p)
    return True


def split_frontmatter(text):
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    raw, body = text[3:end], text[end + 4:]
    fm = {}
    key = None
    for line in raw.splitlines():
        if not line.strip():
            continue
        if re.match(r"^\s+-\s", line) and key:            # list item under last key
            fm.setdefault(key, [])
            if isinstance(fm[key], list):
                fm[key].append(line.strip()[1:].strip())
            continue
        m = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            if val.startswith("[") and val.endswith("]"):      # inline array: ["0.1"] or []
                inner = val[1:-1].strip()
                fm[key] = [x.strip().strip('"').strip("'") for x in inner.split(",") if x.strip()] if inner else []
            else:
                fm[key] = (val.strip('"').strip("'") if val else [])
    return fm, body


def sections(body):
    return [m.group(1).strip() for m in re.finditer(r"^##\s+(.+)$", body, re.M)]


def resolve_ref(p, module_dir):
    """True/False if p is a checkable local file ref, None if not checkable.
    Repo-root paths (contain '/', no leading '.') resolve at REPO_ROOT; relative paths
    ('.'-prefixed) and bare filenames-with-extension resolve against the module's dir."""
    p = p.split("#")[0].strip().strip('"').strip("'")
    if not p or p.startswith(("http://", "https://", "mailto:")):
        return None
    if "/" not in p and not FILE_EXT.search(p):        # a bare word, not a path
        return None
    base = module_dir if (p.startswith(".") or "/" not in p) else REPO_ROOT
    full = os.path.normpath(os.path.join(base, p))
    if is_external(os.path.relpath(full, REPO_ROOT)):
        return None
    return os.path.exists(os.path.normpath(os.path.join(base, p)))


def check(path, fails):
    rel = os.path.relpath(path, REPO_ROOT)
    module_dir = os.path.dirname(path)
    text = open(path, encoding="utf-8").read()
    fm, body = split_frontmatter(text)

    for k in REQUIRED_FM:
        if k not in fm:
            fails.append(f"{rel}: missing frontmatter key '{k}'")

    secs = sections(body)
    top = [s for s in secs if not s.startswith("#")]
    if top != REQUIRED_SECTIONS:
        fails.append(f"{rel}: sections {top} != required {REQUIRED_SECTIONS}")

    opens = [str(p).strip().strip('"').strip("'") for p in (fm.get("opens_files") or [])]
    for p in opens:
        if p and not is_external(p) and not os.path.exists(os.path.join(REPO_ROOT, p)):
            fails.append(f"{rel}: opens_files path does not exist: {p}")

    # backticked file refs AND markdown link targets must resolve
    refs = re.findall(r"`([A-Za-z0-9_./~-]+\.[A-Za-z]{1,5})`", body)
    refs += re.findall(r"\]\(([^)]+)\)", body)
    for p in refs:
        r = resolve_ref(p, module_dir)
        if r is False:
            fails.append(f"{rel}: unresolved path/link: {p}")

    if re.search(r"\bAI\b", body):
        fails.append(f"{rel}: standalone 'AI' present (say 'agentic systems' / 'models' / name the function)")
    for w in BANNED:
        if re.search(r"\b" + re.escape(w) + r"\b", body, re.I):
            fails.append(f"{rel}: banned word '{w}'")
    for ph in BANNED_PHRASES:
        if ph in body.lower():
            fails.append(f"{rel}: banned phrase '{ph}'")
    if body.count("—") > 2:
        fails.append(f"{rel}: {body.count(chr(0x2014))} em dashes (max 2)")

    if str(fm.get("teaches", "")).strip() == "keel":
        for needle in SHEERLINE_INTERNAL:
            if needle in body or any(needle in o for o in opens):
                fails.append(f"{rel}: teaches:keel module references Sheerline internal '{needle}' (separability)")

    return fm.get("module"), (fm.get("prereqs") or [])


def find_cycle(prereqs):
    """Return a node on a cycle in the depends-on graph, or None. Full DFS, not self-loop only."""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {n: WHITE for n in prereqs}

    def dfs(n):
        color[n] = GRAY
        for m in prereqs.get(n, []):
            if m not in color:
                continue                       # missing prereq reported elsewhere
            if color[m] == GRAY or (color[m] == WHITE and dfs(m)):
                return True
        color[n] = BLACK
        return False

    return next((n for n in list(color) if color[n] == WHITE and dfs(n)), None)


def main():
    modules = sorted(glob.glob(os.path.join(HERE, "track-*", "module-*.md")))
    if not modules:
        print("no modules found (track-*/module-*.md) — nothing to check")
        return 0
    fails, ids, prereqs = [], set(), {}
    for path in modules:
        mid, pre = check(path, fails)
        if mid:
            ids.add(mid)
            prereqs[mid] = [p.strip().strip('"').strip("'") for p in pre]
    for mid, pre in prereqs.items():
        for p in pre:
            if p and p not in ids:
                fails.append(f"module {mid}: prereq '{p}' is not an authored module")
    cyc = find_cycle(prereqs)
    if cyc:
        fails.append(f"prereq DAG has a cycle through module '{cyc}'")

    print(f"checked {len(modules)} module(s)")
    if EXTERNAL_POINTERS:
        print(f"exported copy: {len(EXTERNAL_POINTERS)} pointer(s) back to the HeyHi monorepo "
              f"not checked (not shipped; see EXPORT.json)")
    if fails:
        print(f"\nFAIL — {len(fails)} issue(s):")
        for f in fails:
            print("  - " + f)
        return 1
    print("PASS — structure, paths, links, prereq DAG, voice, and separability clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())

# HeyHi Confidential
