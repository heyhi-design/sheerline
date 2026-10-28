#!/usr/bin/env python3
"""Sheerline seminar — curriculum structural smoke test.

Checks every module (track-*/module-*.md) against the module template contract:
frontmatter completeness, the exact eight sections, real paths (opens_files, backticked
repo paths, AND inter-module links resolved against the module's own directory), a valid
acyclic prereq DAG, the voice rules, and the keel/Sheerline separability line (body +
opens_files).

Run from anywhere:  python3 sheerline/seminar/smoke_test.py
Exit 0 = clean · exit 1 = one or more failures printed.

Pointers. In the monorepo every path is checked. In an exported copy (EXPORT.json at the
root), a repo-root path outside the shipped roots is a pointer back to the HeyHi monorepo.
When the export also carries PROVENANCE.json (the provenance map export.py writes), every
such pointer must carry a class from it: an unclassified pointer fails, and an `instance`
pointer fails (instance data never ships). Without PROVENANCE.json, pointers are counted and
reported, as before. A link into a published repo (keel, agent-corrections) must be pinned
to a release tag in either mode, and the path it names must exist in that tag: the check reads
public-tag-files.json beside this script (the tag's own file list, fetched once with `gh api`
and committed), never the staged tree, which moves past the tag; a #fragment or ?query is
dropped first. A `gitignored` pointer fails like an `instance` one. The map's instance rules
arrive as digests (16 hex of SHA-256 of the lowercased path), so it names no instance or client
root in clear text; rule_digest() below computes the same digest.

No external dependencies — a tiny frontmatter parser handles the flat frontmatter these
modules use.
"""
import glob, hashlib, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))

REQUIRED_SECTIONS = [
    "You are here", "Learning objectives", "Concept", "Walkthrough",
    "Lab", "Common misreads", "Self-check", "Go deeper",
]
# No `classification`: the seminar is public (MIT, 2026-10-27) and its files carry no mark.
REQUIRED_FM = ["title", "track", "module", "level",
               "prereqs", "est_minutes", "teaches", "opens_files"]
# Whole-word banned terms that never have a legitimate technical sense here.
# (solution / deliverable / ecosystem / paradigm are context-dependent — human review, not here.)
BANNED = ["leverage", "unlock", "supercharge", "disrupt", "synergy", "cutting-edge",
          "next-gen", "revolutionary", "game-changing", "empower", "holistic", "seamless",
          "best-in-class", "world-class", "transformative", "innovative", "10x", "full-service"]
BANNED_PHRASES = ["digital experiences", "stakeholder alignment"]
# A teaches:keel module may not lean on a Sheerline internal (body or opens_files).
SHEERLINE_INTERNAL = ["sheerline/os/", "sheerline/skills/", "sheerline/profile/", "heyhi-mcp/",
                      "ai-services/"]
FILE_EXT = re.compile(r"\.[A-Za-z0-9]{1,5}$")

# An exported copy (the private sheerline repo) carries EXPORT.json at its root listing the
# roots it ships. There, a repo-root path outside those roots is a pointer back to the HeyHi
# monorepo: counted and reported, not checked. A path INSIDE a shipped root must still resolve.
# In the monorepo every path is checked, exactly as before: the marker is ignored wherever
# ai-services/ exists, so a stray EXPORT.json cannot switch the monorepo into skip mode.
SHIPPED_ROOTS = None
PROVENANCE = None
_marker = os.path.join(REPO_ROOT, "EXPORT.json")
if os.path.isfile(_marker) and not os.path.isdir(os.path.join(REPO_ROOT, "ai-services")):
    import json
    SHIPPED_ROOTS = [r.rstrip("/") for r in json.load(open(_marker, encoding="utf-8"))["roots"]]
    _prov = os.path.join(REPO_ROOT, "PROVENANCE.json")
    if os.path.isfile(_prov):
        PROVENANCE = json.load(open(_prov, encoding="utf-8"))
EXTERNAL_POINTERS = {}          # pointer -> set of citing modules
_CURRENT = [None]               # the module being checked (for pointer attribution)

# A link into a published repo must name a release tag, never a branch. The org and repo
# match in any case and with `www.` (GitHub resolves both); a private-repo link is caught on
# the raw host and with a `.git` suffix too.
PINNED_URL = re.compile(r"^https://(?:www\.)?github\.com/heyhi-design/([A-Za-z0-9_.-]+)/(blob|tree)/"
                        r"(v\d+\.\d+\.\d+)(?:/(\S*))?$", re.IGNORECASE)
HEYHI_URL = re.compile(r"^(?:https?|ssh|git)://(?:[^/@\s]+@)?(?:(?:www|codeload)\.)?"
                       r"(?:github\.com|raw\.githubusercontent\.com|api\.github\.com/repos)/"
                       r"heyhi-design/([A-Za-z0-9_.-]+)(/.*)?$", re.IGNORECASE)
PRIVATE_REPOS = ("heyhi-main",)
# Pointer classes that never ship (provenance.py's fail-hard classes).
FAIL_CLASSES = ("instance", "gitignored")
# The file and folder lists of each pinned public tag (regenerate when a pin moves). Paths
# are recorded as digests (16 hex of SHA-256), so the list itself carries no file names.
TAG_FILES_PATH = os.path.join(HERE, "public-tag-files.json")
TAG_FILES = None
if os.path.isfile(TAG_FILES_PATH):
    import json as _json
    TAG_FILES = (_json.load(open(TAG_FILES_PATH, encoding="utf-8")).get("repos") or {})


def is_external(p):
    """True when p is a repo-root path the exported copy deliberately does not ship."""
    if SHIPPED_ROOTS is None:
        return False
    p = os.path.normpath(p)
    if any(p == r or p.startswith(r + "/") for r in SHIPPED_ROOTS):
        return False
    EXTERNAL_POINTERS.setdefault(p, set()).add(_CURRENT[0])
    return True


def rule_digest(text):
    """The monorepo provenance script's rule digest, computed the same way."""
    return hashlib.sha256(text.strip("/").lower().encode("utf-8")).hexdigest()[:16]


def pointer_class(p):
    """The provenance class of an external pointer, from PROVENANCE.json; None = unclassified."""
    if PROVENANCE is None:
        return None
    p = os.path.normpath(p)
    pointers = PROVENANCE.get("pointers") or {}
    for key in (p, p + "/"):
        if key in pointers:
            return pointers[key]
    segs = [s for s in p.lower().split("/") if s]
    for pattern, kind, cls in PROVENANCE.get("rules") or []:
        # The fail-hard instance rules ship as digests (16 hex of SHA-256 of the lowercased
        # path), so the map names no instance or client root in clear text: `digest-prefix`
        # matches a leading run of segments, `digest-segment` any one folder name (not one
        # followed by a bare number, which is a schema id such as `.../1`).
        if kind == "digest-prefix":
            if any(rule_digest("/".join(segs[:i])) == pattern for i in range(1, len(segs) + 1)):
                return cls
        elif kind == "digest-segment":
            for i, s in enumerate(segs):
                if rule_digest(s) == pattern and not (i + 1 < len(segs) and segs[i + 1].isdigit()):
                    return cls
        elif kind == "regex":
            if re.search(pattern, p):
                return cls
        elif pattern.endswith("/"):
            if p.startswith(pattern) or p + "/" == pattern:
                return cls
        elif p == pattern or p.startswith(pattern + "/"):
            return cls
    return None


def check_url(url, rel, fails):
    """A heyhi-design URL must point at a published repo, pinned to a release tag."""
    # A #fragment or ?query names a place in the file, not the file: drop it before the path
    # is checked against the tag's file list (an anchored keel link is a valid pin).
    clean = re.split(r"[?#]", url, maxsplit=1)[0]
    m = HEYHI_URL.match(clean)
    if not m:
        return
    repo, rest = m.group(1).lower(), m.group(2) or ""
    if repo.endswith(".git"):
        repo = repo[:-4]
    if repo in PRIVATE_REPOS:
        fails.append(f"{rel}: link into the private monorepo: {url}")
        return
    if rest.strip("/") == "":
        return                                   # a repo home page, not a file pointer
    pin = PINNED_URL.match(clean)
    if not pin:
        fails.append(f"{rel}: public URL not pinned to a release tag: {url}")
        return
    kind, tag, path = pin.group(2), pin.group(3), (pin.group(4) or "").strip("/")
    if PROVENANCE is not None:
        known = (PROVENANCE.get("public_repos") or {}).get(repo)
        if not known or tag not in known.get("tags", [known.get("tag")]):
            fails.append(f"{rel}: URL not in the provenance map's published repos/tags: {url}")
    # The tag's own file list, in both modes (the staged tree has moved past the tag).
    listing = ((TAG_FILES or {}).get(repo) or {}).get(tag)
    if listing is None:
        fails.append(f"{rel}: no cached file list for {repo}@{tag} in public-tag-files.json: {url}")
    elif path:
        names = listing.get("dirs" if kind == "tree" else "files") or []
        if hashlib.sha256(path.encode("utf-8")).hexdigest()[:16] not in names:
            fails.append(f"{rel}: pinned URL names a path {repo}@{tag} does not have: {url}")


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
    _CURRENT[0] = rel
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
        if p.startswith(("http://", "https://")):
            check_url(p, rel, fails)
            continue
        if p and not is_external(p) and not os.path.exists(os.path.join(REPO_ROOT, p)):
            fails.append(f"{rel}: opens_files path does not exist: {p}")
    for url in re.findall(r"\]\((https?://[^)\s]+)\)", body):
        check_url(url, rel, fails)

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
    if EXTERNAL_POINTERS and PROVENANCE is None:
        print(f"exported copy: {len(EXTERNAL_POINTERS)} pointer(s) back to the HeyHi monorepo "
              f"not checked (not shipped; see EXPORT.json; no PROVENANCE.json to classify them)")
    elif EXTERNAL_POINTERS:
        by_class = {}
        for p, cited in sorted(EXTERNAL_POINTERS.items()):
            cls = pointer_class(p)
            by_class[str(cls)] = by_class.get(str(cls), 0) + 1
            where = ", ".join(sorted(c for c in cited if c))
            if cls is None:
                fails.append(f"unclassified pointer (not in PROVENANCE.json): {p} (cited by {where})")
            elif cls in FAIL_CLASSES:
                fails.append(f"{cls} pointer in a shipped module: {p} (cited by {where})")
        summary = ", ".join(f"{k} {v}" for k, v in sorted(by_class.items()))
        print(f"exported copy: {len(EXTERNAL_POINTERS)} pointer(s) back to the HeyHi monorepo, "
              f"by class: {summary}")
    if fails:
        print(f"\nFAIL — {len(fails)} issue(s):")
        for f in fails:
            print("  - " + f)
        return 1
    print("PASS — structure, paths, links, prereq DAG, voice, and separability clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())

