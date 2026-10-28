#!/usr/bin/env python3
"""Sheerline slot resolver: a skill asks for a slot and gets the instance's value or the
generic default, and fails loudly when neither exists. Standard library only.

    python3 sheerline/os/instance/resolve.py --list
    python3 sheerline/os/instance/resolve.py --slot ui-studio.default-brand
    python3 sheerline/os/instance/resolve.py --write                  # resolved-slots.json
    python3 sheerline/os/instance/resolve.py --check --blank          # blank-instance check
    python3 sheerline/os/instance/resolve.py --check --expect <fixture.json>

From Python:

    spec = importlib.util.spec_from_file_location("sheerline_resolve", <root>/sheerline/os/instance/resolve.py)
    ...; rec = mod.consumer_slot("vectorize.calibration")   # {"path", "source", "ratified", ...}

A skill's code calls consumer_slot (selection by $SHEERLINE_INSTANCE only, plus the stale
resolved-slots.json check); slot()/resolve_slot() take an explicit instance= for tools and tests.

Which instance (first match wins; the resolver takes a path, it never scans for one):
  1. --instance <root>  (or instance=<root> from Python). Resolve-only: it applies to this
     resolve.py run (for example `--write` for a named instance) and to nothing it does not
     run itself. Consumers never see it.
  2. $SHEERLINE_INSTANCE (the value `none` means a blank instance, skipping the pointer). The
     one selector every consumer honors, Python and Node alike (consumer_slot below, and
     resolved-slot.mjs).
  3. the default-instance pointer file, releases/private/sheerline/default-instance, when the
     checkout carries it (the monorepo does; an export does not)
  4. none: every slot resolves to its generic default
A relative instance path resolves against the repo root, never the current directory, and a
leading `~` or `~/` is the home directory (Node expands it the same way). `~name` is refused.

Rules it enforces (taken from the practice's own registered instances, never from the manifest
being read):
  - an instance's value, else the generic default (or the source slot of a derived slot), else
    an error naming the slot and the instance.yaml key that fills it;
  - `kind: self` and `mode: pointer` are allowed only for an instance registered in the
    checkout's instances directory (INSTANCES_DIR, a direct child folder holding
    instance.yaml); a manifest elsewhere that claims either is refused;
  - it never reads a value from one instance on behalf of another: a rooted instance's fills
    must sit under its own root; no fill may sit under any other folder that holds an
    instance.yaml (registered or not); and a pointer fill may not sit under a client root the
    practice declares (the union of every registered self instance's instance.client_roots;
    pointer mode with no declared client root anywhere is refused, fail closed);
  - it refuses a client instance root placed under a .claude/worktrees/ checkout (that copy
    is orphaned when the worktree is reaped); the practice's own registered instance is fine
    there;
  - a consumer reading resolved-slots.json (or consumer_slot from Python) checks that the file
    was written for the selected instance (same id, same root); a file left over from another
    instance is an error, never a value;
  - a slot that needs ratification reports `ratified: false` until its owner ratifies it.

"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import posixpath
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_ROOT = HERE.parents[2]
SLOTS_FILE = "sheerline/os/instance/slots.yaml"
DEFAULT_POINTER = "releases/private/sheerline/default-instance"
# Built from parts so this shipped file cites no instance-root path (only the declared
# default-pointer exemption above). The registered instances sit one level below it.
INSTANCES_DIR = "/".join(("releases", "private", "sheerline", "instances"))
RESOLVED_FILE = "resolved-slots.json"
RESOLVED_SCHEMA = "sheerline-resolved-slots/1"
ENV_VAR = "SHEERLINE_INSTANCE"
BLANK_VALUE = "none"  # $SHEERLINE_INSTANCE=none: resolve as a blank instance (no pointer)
SCHEMA = "sheerline-instance/1"
KINDS = ("self", "client")
MODES = ("pointer", "rooted")
FORMATS = ("python-module", "json", "markdown", "generated", "paths")
SLOT_KINDS = ("calibration", "brand", "ratified", "contract", "history")


class SlotError(Exception):
    """A slot cannot be resolved. The message names the slot and the key that fills it."""


class InstanceError(Exception):
    """The selected instance root is unusable (missing, malformed, or refused)."""


# ── a restricted YAML loader (stdlib only) ────────────────────────────────────
# slots.yaml and instance.yaml keep to block mappings, block sequences, plain or quoted
# scalars, flow lists of scalars, `{}`, and folded (`>` / `>-`) scalars. Anything else is an
# error, never a guess. tests/test_resolve.py checks it agrees with PyYAML on every file.

_INT = re.compile(r"^-?\d+$")


def _strip_comment(line: str) -> str:
    out, q = [], None
    for i, ch in enumerate(line):
        if q:
            if ch == q:
                q = None
        elif ch in ("'", '"') and (i == 0 or line[i - 1] in " [,:"):
            q = ch
        elif ch == "#" and (i == 0 or line[i - 1] in " \t"):
            break
        out.append(ch)
    return "".join(out).rstrip()


def _scalar(tok: str):
    tok = tok.strip()
    if tok == "":
        return None
    if tok[0] == tok[-1] and tok[0] in ("'", '"') and len(tok) >= 2:
        body = tok[1:-1]
        return body.replace("''", "'") if tok[0] == "'" else body.replace('\\"', '"')
    if tok in ("null", "~", "Null", "NULL"):
        return None
    if tok in ("true", "True", "TRUE"):
        return True
    if tok in ("false", "False", "FALSE"):
        return False
    if _INT.match(tok):
        return int(tok)
    if tok == "{}":
        return {}
    if tok.startswith("[") and tok.endswith("]"):
        inner = tok[1:-1].strip()
        return [] if not inner else [_scalar(x) for x in _split_flow(inner)]
    if tok[0] in "{&*!|>%@`":
        raise ValueError(f"unsupported YAML in a Sheerline instance file: {tok!r}")
    return tok


def _split_flow(s: str):
    parts, cur, q = [], [], None
    for ch in s:
        if q:
            cur.append(ch)
            if ch == q:
                q = None
        elif ch in ("'", '"'):
            q = ch
            cur.append(ch)
        elif ch == ",":
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    parts.append("".join(cur))
    return [p for p in (x.strip() for x in parts)]


def load_yaml(text: str):
    raw = text.splitlines()
    lines = []  # (indent, content, raw_index)
    for i, l in enumerate(raw):
        if "\t" in l[: len(l) - len(l.lstrip())]:
            raise ValueError(f"line {i + 1}: tab indentation")
        c = _strip_comment(l)
        if c.strip():
            lines.append((len(c) - len(c.lstrip()), c.strip(), i))
    pos = 0

    def folded(indent_floor: int, keep_newline: bool) -> str:
        nonlocal pos
        parts = []
        while pos < len(lines) and lines[pos][0] > indent_floor:
            parts.append(raw[lines[pos][2]].strip())
            pos += 1
        s = " ".join(parts)
        return s + ("\n" if keep_newline and s else "")

    def value_after(rest: str, indent: int):
        nonlocal pos
        if rest in (">", ">-"):
            return folded(indent, rest == ">")
        if rest == "":
            if pos < len(lines) and (lines[pos][0] > indent or
                                     (lines[pos][0] == indent and lines[pos][1].startswith("- "))):
                return block(lines[pos][0])
            return None
        return _scalar(rest)

    def block(indent: int):
        nonlocal pos
        if lines[pos][1].startswith("- ") or lines[pos][1] == "-":
            seq = []
            while pos < len(lines) and lines[pos][0] == indent and (
                    lines[pos][1].startswith("- ") or lines[pos][1] == "-"):
                item = lines[pos][1][2:].strip() if lines[pos][1] != "-" else ""
                pos += 1
                if item == "":
                    seq.append(block(lines[pos][0]) if pos < len(lines) and lines[pos][0] > indent else None)
                elif _is_key(item):
                    # an inline mapping start: re-read it as a mapping at the item's column
                    child = indent + 2
                    lines.insert(pos, (child, item, lines[pos - 1][2]))
                    seq.append(block(child))
                else:
                    seq.append(_scalar(item))
            return seq
        mapping = {}
        while pos < len(lines) and lines[pos][0] == indent:
            content = lines[pos][1]
            if not _is_key(content):
                raise ValueError(f"line {lines[pos][2] + 1}: expected `key: value`, got {content!r}")
            key, rest = _split_key(content)
            pos += 1
            if key in mapping:
                raise ValueError(f"line {lines[pos - 1][2] + 1}: duplicate key {key!r}")
            mapping[key] = value_after(rest, indent)
        if pos < len(lines) and lines[pos][0] > indent:
            raise ValueError(f"line {lines[pos][2] + 1}: unexpected indentation")
        return mapping

    if not lines:
        return None
    result = block(lines[0][0])
    if pos != len(lines):
        raise ValueError(f"line {lines[pos][2] + 1}: unparsed content")
    return result


def _is_key(content: str) -> bool:
    if content[0] in ("'", '"'):
        return False
    return bool(re.match(r"^[^\s:][^:]*:(\s|$)", content))


def _split_key(content: str):
    key, _, rest = content.partition(":")
    return key.strip(), rest.strip()


# ── registry and instance ─────────────────────────────────────────────────────

def _root(root=None) -> Path:
    return Path(root).resolve() if root else DEFAULT_ROOT


def load_slots(root=None) -> dict:
    root = _root(root)
    path = root / SLOTS_FILE
    data = load_yaml(path.read_text(encoding="utf-8")) or {}
    slots = {}
    for s in data.get("slots") or []:
        sid = s.get("id")
        if not sid or sid in slots:
            raise SlotError(f"slots.yaml: missing or duplicate slot id {sid!r}")
        if s.get("kind") not in SLOT_KINDS:
            raise SlotError(f"slots.yaml: slot {sid} has unknown kind {s.get('kind')!r}")
        if s.get("format") not in FORMATS:
            raise SlotError(f"slots.yaml: slot {sid} has unknown format {s.get('format')!r}")
        s.setdefault("in_tree", [])
        s.setdefault("values", [])
        slots[sid] = s
    for sid, s in slots.items():
        src = s.get("derived_from")
        if src and src not in slots:
            raise SlotError(f"slots.yaml: slot {sid} is derived from unknown slot {src}")
    return slots


def instance_path(value, root=None) -> Path:
    """An instance root as the resolver and every consumer read it: `~` or `~/...` is the home
    directory, a relative path is relative to the repo root (never the current directory).
    resolved-slot.mjs applies the same rule."""
    root = _root(root)
    v = str(value).strip()
    if v.startswith("~"):
        if v != "~" and not v.startswith("~/"):
            raise InstanceError(f"instance path {value!r}: `~name` is not supported "
                                "(use `~/...`, an absolute path, or a repo-relative path)")
        v = str(Path.home()) + v[1:]
    p = Path(v)
    return (p if p.is_absolute() else root / p).resolve()


def default_pointer(root=None):
    """The instance root the checkout's default pointer names, or None (an export has none)."""
    root = _root(root)
    p = root / DEFAULT_POINTER
    if not p.is_file():
        return None
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            return instance_path(line, root)
    return None


def select_instance(root=None, instance=None, blank=False):
    """(instance_root or None, how it was selected)."""
    root = _root(root)
    if blank:
        return None, "blank"
    if instance:
        return instance_path(instance, root), "--instance"
    env = os.environ.get(ENV_VAR, "").strip()
    if env == BLANK_VALUE:
        return None, f"${ENV_VAR}={BLANK_VALUE}"
    if env:
        return instance_path(env, root), f"${ENV_VAR}"
    ptr = default_pointer(root)
    if ptr is not None:
        return ptr, DEFAULT_POINTER
    return None, "none"


def registered_instances(root=None):
    """The practice's own instances: direct child folders of INSTANCES_DIR holding instance.yaml."""
    root = _root(root)
    d = root / INSTANCES_DIR
    if not d.is_dir():
        return []
    return sorted(p.resolve() for p in d.iterdir() if (p / "instance.yaml").is_file())


def _is_registered(instance_root: Path, root: Path) -> bool:
    return instance_root.resolve() in registered_instances(root)


def practice_client_roots(root=None) -> list:
    """Client roots the practice declares: the union of instance.client_roots over every
    registered `kind: self` instance. Read from the practice's manifests, never from the
    manifest whose fill is being checked (that one could simply leave the list empty)."""
    root = _root(root)
    out = set()
    for inst in registered_instances(root):
        mf = inst / "instance.yaml"
        try:
            data = load_yaml(mf.read_text(encoding="utf-8")) or {}
        except ValueError:
            continue
        meta = data.get("instance") or {}
        if meta.get("kind") != "self":
            continue
        roots = meta.get("client_roots")
        if roots is None:
            continue
        if not isinstance(roots, list):
            # a bare string would iterate character by character and look non-empty
            raise InstanceError(f"{mf}: instance.client_roots must be a list of folders, got {roots!r}")
        for c in roots:
            out.add(_normal_client_root(c, mf))
    return sorted(out)


def _normal_client_root(c, where) -> str:
    """A declared client root as a normalized repo-relative folder with one trailing slash."""
    if not isinstance(c, str) or not c.strip():
        raise InstanceError(f"{where}: a client root must be a non-empty string, got {c!r}")
    n = posixpath.normpath(c.strip().replace("\\", "/"))
    if n in (".", "") or n.startswith(("/", "../")) or n == "..":
        raise InstanceError(f"{where}: client root {c!r} must be a folder inside the checkout")
    return n + "/"


def _under_client_root(rel: str, client_roots) -> str:
    """The client root `rel` (repo-relative POSIX) sits in or equals, case-insensitively, or ''."""
    low = rel.lower().rstrip("/") + "/"
    for c in client_roots:
        if low.startswith(c.lower()):
            return c
    return ""


def load_instance(instance_root: Path, root=None) -> dict:
    root = _root(root)
    mf = instance_root / "instance.yaml"
    if not mf.is_file():
        raise InstanceError(f"instance root has no instance.yaml: {instance_root}")
    try:
        data = load_yaml(mf.read_text(encoding="utf-8")) or {}
    except ValueError as e:
        raise InstanceError(f"{mf}: {e}")
    if data.get("schema") != SCHEMA:
        raise InstanceError(f"{mf}: schema must be {SCHEMA!r}")
    inst = data.get("instance") or {}
    kind, mode = inst.get("kind"), inst.get("mode")
    if not isinstance(inst.get("id"), str) or not inst.get("id").strip():
        # an unquoted numeric id (007) reads as an int here and as text in Node: refuse both
        raise InstanceError(f"{mf}: instance.id must be a non-empty string (quote a numeric id), "
                            f"got {inst.get('id')!r}")
    if kind not in KINDS:
        raise InstanceError(f"{mf}: instance.kind must be one of {KINDS}, got {kind!r}")
    if mode not in MODES:
        raise InstanceError(f"{mf}: instance.mode must be one of {MODES}, got {mode!r}")
    if kind == "client" and mode == "pointer":
        raise InstanceError(f"{mf}: a client instance is rooted; pointer mode is for the practice's own instance")
    if (kind == "self" or mode == "pointer") and not _is_registered(instance_root, root):
        raise InstanceError(
            f"{mf}: `kind: self` and pointer mode are allowed only for an instance registered in "
            f"{INSTANCES_DIR}/<id>/ of the checkout {root}; this manifest is not one (a client "
            "instance is `kind: client`, `mode: rooted`)")
    if kind == "client" and _is_registered(instance_root, root):
        raise InstanceError(f"{mf}: a client instance root never sits in the tracked {INSTANCES_DIR}/ "
                            "folder; keep it in the practice's gitignored engagement folder")
    if kind == "client" and "/.claude/worktrees/" in (instance_root.as_posix() + "/").lower():
        raise InstanceError(
            f"refusing a client instance root under a .claude/worktrees/ checkout: {instance_root} "
            "(the worktree is reaped and the instance data with it; keep client roots in the "
            "main workspace's gitignored engagement folder)")
    if kind == "client":
        _check_client_root_placement(instance_root.resolve(), root, mf)
    slots = data.get("slots") or {}
    if not isinstance(slots, dict):
        raise InstanceError(f"{mf}: slots must be a mapping keyed by slot id")
    data["slots"] = slots
    data["_root"] = instance_root
    return data


def _check_client_root_placement(inst_root: Path, root: Path, mf) -> None:
    """A client root may not enclose the checkout or any registered instance (it would then
    read the practice's own files as its fills), and inside the checkout it must sit in a client
    root the practice declares (never in a shipped or tracked folder)."""
    if _within(root, inst_root):
        raise InstanceError(f"{mf}: a client instance root may not be the checkout or enclose it "
                            f"({inst_root} contains {root})")
    for reg in registered_instances(root):
        if _within(reg, inst_root):
            raise InstanceError(f"{mf}: a client instance root may not enclose the practice's "
                                f"registered instance {reg}")
    if _within(inst_root, root):
        rel = _rel(inst_root, root)
        if not _under_client_root(rel, practice_client_roots(root)):
            raise InstanceError(
                f"{mf}: a client instance root inside the checkout must sit in a client root the "
                f"practice declares (instance.client_roots of a registered self instance); {rel}/ "
                "is not in one")


def _rel(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def _within(path: Path, base: Path) -> bool:
    try:
        path.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False


def _foreign_instance_dir(full: Path, inst_root: Path, stop: Path):
    """The nearest folder above `full` (up to and including `stop`) that holds an instance.yaml
    and is not `inst_root`, or None. Any such folder is an instance root, registered or not."""
    inst_root = inst_root.resolve()
    stop = stop.resolve()
    cur = full if full.is_dir() else full.parent
    while True:
        cur = cur.resolve()
        if cur == inst_root:
            return None
        if (cur / "instance.yaml").is_file():
            return cur
        if cur == stop or cur.parent == cur:
            return None
        cur = cur.parent


def _fill_path(p: str, manifest: dict, root: Path, sid: str) -> Path:
    inst_root = manifest["_root"].resolve()
    mode = manifest["instance"]["mode"]
    raw = Path(p)
    if mode == "rooted":
        full = (raw if raw.is_absolute() else inst_root / raw).resolve()
        if not _within(full, inst_root):
            raise SlotError(f"slot {sid}: fill {p!r} is outside its instance root {inst_root} "
                            "(an instance never reads another's value)")
        stop = inst_root
    else:
        full = (raw if raw.is_absolute() else root / raw).resolve()
        if not _within(full, root):
            raise SlotError(f"slot {sid}: pointer fill {p!r} is outside the checkout {root}")
        client_roots = practice_client_roots(root)
        if not client_roots:
            raise SlotError(f"slot {sid}: pointer fill {p!r} refused: no registered self instance "
                            f"in {INSTANCES_DIR}/ declares instance.client_roots, so a client's "
                            "folder cannot be told apart (declare the practice's client roots)")
        hit = _under_client_root(_rel(full, root), client_roots)
        if hit:
            raise SlotError(f"slot {sid}: pointer fill {p!r} sits in the client root {hit} "
                            "(the practice's own instance never reads a client's value)")
        stop = root
    for other in registered_instances(root):
        if other != inst_root and _within(full, other):
            raise SlotError(f"slot {sid}: fill {p!r} sits under another instance root {other}")
    foreign = _foreign_instance_dir(full, inst_root, stop)
    if foreign is not None:
        raise SlotError(f"slot {sid}: fill {p!r} sits under {foreign}, which holds an instance.yaml "
                        "(any folder holding one is an instance root; an instance never reads "
                        "another's value)")
    if not full.exists():
        raise SlotError(f"slot {sid}: fill {p!r} does not exist (fix slots.{sid} in "
                        f"{inst_root / 'instance.yaml'})")
    return full


# ── value extraction (what --check --expect compares) ─────────────────────────

def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _frontmatter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    out = {}
    for line in (m.group(1).splitlines() if m else []):
        k, sep, v = line.partition(":")
        if sep and not line.startswith((" ", "\t")):
            v = v.strip()
            out[k.strip()] = None if v in ("null", "~", "") else v.strip('"').strip("'")
    return out


def _frontmatter_lines(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    out = {}
    for line in (m.group(1).splitlines() if m else []):
        k, sep, _ = line.partition(":")
        if sep and not line.startswith((" ", "\t")):
            out[k.strip()] = line
    return out


def _module_literals(path: Path, names) -> dict:
    """Top-level literal assignments of a Python module, read with ast (never executed)."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    found = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id in names:
                    try:
                        found[t.id] = ast.literal_eval(node.value)
                    except ValueError:
                        found[t.id] = None
    return found


def _values(slot_def: dict, path: Path) -> dict:
    fmt, keys = slot_def["format"], list(slot_def.get("values") or [])
    if not keys or path is None or not path.is_file():
        return {}
    if fmt == "python-module":
        lit = _module_literals(path, set(keys))
        out = {}
        for k in keys:
            v = lit.get(k)
            out[k] = list(v) if isinstance(v, tuple) else v
        return out
    if fmt == "json":
        data = json.loads(path.read_text(encoding="utf-8"))
        out = {}
        for k in keys:
            node = data
            for part in k.split("."):
                node = node.get(part) if isinstance(node, dict) else None
            out[k] = node
        return out
    text = path.read_text(encoding="utf-8")
    fm = _frontmatter_lines(text) if fmt == "generated" else _frontmatter(text)
    return {k: fm.get(k) for k in keys}


def _ratified(slot_def: dict, path: Path, values: dict):
    if not slot_def.get("requires_ratification"):
        return None
    if path is None or not path.is_file():
        return False
    if slot_def["format"] == "python-module":
        ceilings = values.get("CEILINGS")
        if ceilings is None:
            ceilings = _module_literals(path, {"CEILINGS"}).get("CEILINGS")
        return bool(isinstance(ceilings, dict) and ceilings.get("ratified"))
    if slot_def["format"] == "markdown":
        return _frontmatter(path.read_text(encoding="utf-8")).get("status") == "ratified"
    return False


# ── resolution ────────────────────────────────────────────────────────────────

def _record(sid, slot_def, path, source, root, extra=None) -> dict:
    vals = _values(slot_def, path)
    rec = {
        "slot": sid,
        "source": source,
        "path": _rel(path, root) if path is not None else None,
        "sha256": _sha(path) if path is not None and path.is_file() else None,
        "values": vals,
        "requires_ratification": bool(slot_def.get("requires_ratification")),
    }
    rat = _ratified(slot_def, path, vals)
    if rat is not None:
        rec["ratified"] = rat
    if extra:
        rec.update(extra)
    return rec


def resolve_slot(sid: str, root=None, instance=None, blank=False, _manifest=None, _slots=None):
    """Resolve one slot. Raises SlotError (no value, no default) or InstanceError."""
    root = _root(root)
    slots = _slots if _slots is not None else load_slots(root)
    if sid not in slots:
        raise SlotError(f"unknown slot {sid!r} (not in {SLOTS_FILE})")
    slot_def = slots[sid]
    manifest = _manifest
    if manifest is None:
        inst_root, _how = select_instance(root, instance, blank)
        manifest = load_instance(inst_root, root) if inst_root is not None else None
    if manifest is not None:
        fill = manifest["slots"].get(sid)
        if fill:
            if not isinstance(fill, dict):
                raise SlotError(f"slot {sid}: slots.{sid} must be a mapping with `value` or `paths`")
            evidence = {}
            for e in fill.get("evidence") or []:
                ep = _fill_path(e, manifest, root, sid)
                evidence[_rel(ep, root)] = _sha(ep) if ep.is_file() else None
            extra = {"instance": manifest["instance"].get("id")}
            if evidence:
                extra["evidence"] = evidence
            if slot_def["format"] == "paths":
                ps = [_fill_path(p, manifest, root, sid) for p in fill.get("paths") or []]
                if not ps:
                    raise SlotError(f"slot {sid}: slots.{sid}.paths is empty")
                extra["paths"] = [_rel(p, root) for p in ps]
                return _record(sid, slot_def, None, "instance", root, extra)
            if fill.get("value"):
                return _record(sid, slot_def, _fill_path(fill["value"], manifest, root, sid),
                               "instance", root, extra)
            raise SlotError(f"slot {sid}: slots.{sid} in "
                            f"{manifest['_root'] / 'instance.yaml'} has no `value`")
    src = slot_def.get("derived_from")
    if src:
        base = resolve_slot(src, root, _manifest=manifest, _slots=slots,
                            blank=manifest is None)
        rec = _record(sid, slot_def, (root / base["path"]) if base.get("path") else None,
                      "derived", root, {"derived_from": src, "generator": slot_def.get("generator")})
        rec["values"] = {}
        return rec
    if slot_def.get("default"):
        dp = (root / slot_def["default"]).resolve()
        if not dp.exists():
            raise SlotError(f"slot {sid}: generic default {slot_def['default']} is missing")
        return _record(sid, slot_def, dp, "default", root)
    where = (f"slots.{sid}.value in {manifest['_root'] / 'instance.yaml'}" if manifest is not None
             else f"slots.{sid}.value in an instance.yaml (no instance is selected)")
    raise SlotError(f"slot {sid} has no generic default and no instance value: fill {where}")


slot = resolve_slot


def resolve_all(root=None, instance=None, blank=False) -> dict:
    """Every slot: {"instance", "selected_by", "slots": {id: record or {"error": ...}}}."""
    root = _root(root)
    slots = load_slots(root)
    inst_root, how = select_instance(root, instance, blank)
    manifest = load_instance(inst_root, root) if inst_root is not None else None
    out = {}
    for sid in slots:
        try:
            out[sid] = resolve_slot(sid, root, _manifest=manifest, _slots=slots,
                                    blank=manifest is None)
        except SlotError as e:
            out[sid] = {"slot": sid, "error": str(e), "optional": bool(slots[sid].get("optional"))}
    return {
        "instance": manifest["instance"].get("id") if manifest else None,
        "instance_root": _rel(inst_root, root) if inst_root is not None else None,
        "selected_by": how,
        "slots": out,
    }


# ── checks ────────────────────────────────────────────────────────────────────

def instance_paths(root=None) -> set:
    """Every in_tree path class entry plus every path a registered instance fills, repo-relative."""
    root = _root(root)
    slots = load_slots(root)
    paths = {p for s in slots.values() for p in s.get("in_tree") or []}
    for inst in registered_instances(root):
        try:
            m = load_instance(inst, root)
        except InstanceError:
            continue
        for fill in m["slots"].values():
            if not isinstance(fill, dict):
                continue
            for p in [fill.get("value")] + list(fill.get("paths") or []) + list(fill.get("evidence") or []):
                if p:
                    full = (inst / p) if m["instance"]["mode"] == "rooted" else (root / p)
                    paths.add(_rel(full, root) + ("/" if p.endswith("/") else ""))
    return paths


def _matches(path: str, classes) -> bool:
    for c in classes:
        if c.endswith("/") and (path + "/").startswith(c):
            return True
        if path == c.rstrip("/"):
            return True
    return False


def check_blank(root=None) -> list:
    """Problems with a blank instance: no instance value may reach it, every default must exist."""
    root = _root(root)
    slots = load_slots(root)
    problems = []
    classes = instance_paths(root)
    res = resolve_all(root, blank=True)
    for sid, rec in res["slots"].items():
        sd = slots[sid]
        if "error" in rec:
            if not sd.get("optional"):
                problems.append(f"{sid}: {rec['error']}")
            continue
        if rec["source"] not in ("default", "derived"):
            problems.append(f"{sid}: blank instance resolved from {rec['source']!r}")
        p = rec.get("path")
        if p is None:
            problems.append(f"{sid}: blank instance resolved to no path")
            continue
        if _matches(p, classes):
            problems.append(f"{sid}: generic default {p} is an instance path")
        if rec.get("ratified"):
            problems.append(f"{sid}: generic default {p} reads as ratified")
    return problems


def check_expect(fixture: dict, root=None, instance=None) -> list:
    root = _root(root)
    res = resolve_all(root, instance)
    problems = []
    if res["instance"] is None:
        problems.append(f"no instance selected ({res['selected_by']}); the fixture is an instance's values")
    for sid, want in (fixture.get("slots") or {}).items():
        got = res["slots"].get(sid)
        if got is None:
            problems.append(f"{sid}: not in the slot registry")
            continue
        if "error" in got:
            problems.append(f"{sid}: {got['error']}")
            continue
        for key, wv in want.items():
            if got.get(key) != wv:
                problems.append(f"{sid}.{key}: expected {json.dumps(wv, sort_keys=True)[:200]}, "
                                f"got {json.dumps(got.get(key), sort_keys=True)[:200]}")
    return problems


def resolved_text(root=None, instance=None):
    """(instance root, the resolved-slots.json text --write would emit)."""
    root = _root(root)
    res = resolve_all(root, instance)
    if res["instance_root"] is None:
        raise InstanceError("--write needs an instance root (none selected)")
    inst_root = Path(res["instance_root"])
    inst_root = inst_root if inst_root.is_absolute() else root / inst_root
    body = {
        "schema": RESOLVED_SCHEMA,
        "generated_by": "sheerline/os/instance/resolve.py --write",
        "instance": res["instance"],
        # A consumer compares this (and the id) with the instance it selected, so a file copied
        # along with another instance's folder is refused instead of read. A registered
        # (tracked) instance records its repo-relative root: every checkout carries its own
        # copy. Any other instance records its absolute root, so a client root in the main
        # workspace reads the same from the main checkout and from any worktree.
        "instance_root": (_rel(inst_root, root) if _is_registered(inst_root, root)
                          else inst_root.resolve().as_posix()),
        "slots": {sid: {k: rec.get(k) for k in ("source", "path", "paths", "derived_from",
                                                "requires_ratification", "ratified", "error")
                        if rec.get(k) is not None}
                  for sid, rec in res["slots"].items()},
    }
    return inst_root, json.dumps(body, indent=2, sort_keys=True) + "\n"


def write_resolved(root=None, instance=None) -> Path:
    inst_root, text = resolved_text(root, instance)
    out = inst_root / RESOLVED_FILE
    out.write_text(text, encoding="utf-8")
    return out


def check_resolved_file(inst_root: Path, instance_id, root=None, required=False):
    """Raise InstanceError unless <inst_root>/resolved-slots.json was written for this instance
    (same schema, same id, same root). With required=False a missing file is fine (a Python
    consumer resolves directly); a file present but written for another instance never is.
    Returns the parsed body, or None when the file is absent and not required."""
    root = _root(root)
    f = Path(inst_root) / RESOLVED_FILE
    if not f.is_file():
        if required:
            raise InstanceError(f"{f} is missing: run resolve.py --write with "
                                f"${ENV_VAR} set to this instance")
        return None
    try:
        body = json.loads(f.read_text(encoding="utf-8"))
    except ValueError as e:
        raise InstanceError(f"{f}: not valid JSON ({e}); rerun resolve.py --write")
    if not isinstance(body, dict) or body.get("schema") != RESOLVED_SCHEMA:
        raise InstanceError(f"{f}: schema must be {RESOLVED_SCHEMA!r}; rerun resolve.py --write")
    if body.get("instance") != instance_id:
        raise InstanceError(f"{f} was written for instance {body.get('instance')!r}, but the "
                            f"selected instance is {instance_id!r}: rerun resolve.py --write "
                            "for this instance (a stale file is never read as a value)")
    recorded = body.get("instance_root")
    if not recorded or instance_path(recorded, root) != Path(inst_root).resolve():
        raise InstanceError(f"{f} was written for the instance root {recorded!r}, not "
                            f"{Path(inst_root).resolve()}: rerun resolve.py --write for this instance")
    return body


def consumer_slot(sid: str, root=None) -> dict:
    """The entry point for a skill's Python code: resolve `sid` from the instance the consumer
    selection picks ($SHEERLINE_INSTANCE, else the default pointer, else none; never a flag),
    and refuse a resolved-slots.json in that root that was written for another instance, so
    Python and Node consumers stand on the same instance or both fail."""
    root = _root(root)
    inst_root, _how = select_instance(root)
    manifest = load_instance(inst_root, root) if inst_root is not None else None
    rec = resolve_slot(sid, root, _manifest=manifest, blank=manifest is None)
    if manifest is not None:
        iid = manifest["instance"].get("id")
        check_resolved_file(inst_root, iid, root)
        if rec.get("source") == "instance" and rec.get("instance") != iid:
            raise InstanceError(f"slot {sid}: resolved for instance {rec.get('instance')!r}, "
                                f"selected {iid!r}")
    return rec


# ── CLI ───────────────────────────────────────────────────────────────────────

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", help="repo root (default: the checkout this file sits in)")
    ap.add_argument("--instance", help="instance root for this resolve.py run only (overrides "
                    "$SHEERLINE_INSTANCE and the default pointer here; consumers select with "
                    "$SHEERLINE_INSTANCE, never this flag)")
    ap.add_argument("--slot", help="resolve one slot and print its record as JSON")
    ap.add_argument("--list", action="store_true", help="every slot and where it resolves")
    ap.add_argument("--write", action="store_true", help=f"write {RESOLVED_FILE} into the instance root")
    ap.add_argument("--check", action="store_true", help="run a check (with --blank or --expect)")
    ap.add_argument("--blank", action="store_true", help="resolve as a blank instance (no instance at all)")
    ap.add_argument("--expect", help="with --check: compare the instance's values with a fixture JSON")
    a = ap.parse_args(argv)
    try:
        if a.instance and not a.check:
            picked = instance_path(a.instance, a.root)
            env_root, _ = select_instance(a.root)
            if env_root != picked:
                print(f"note: --instance applies to this resolve.py run only; consumers (Python and "
                      f"Node) read ${ENV_VAR}. To have them use this instance: "
                      f"export {ENV_VAR}={picked}", file=sys.stderr)
        if a.check:
            if a.blank == bool(a.expect):
                ap.error("--check needs exactly one of --blank or --expect <fixture>")
            if a.blank:
                problems = check_blank(a.root)
                label = "blank-instance check"
            else:
                fixture = json.loads(Path(a.expect).read_text(encoding="utf-8"))
                problems = check_expect(fixture, a.root, a.instance)
                label = f"expect check against {a.expect}"
            if problems:
                print(f"{label}: FAILED ({len(problems)})")
                for p in problems:
                    print("  - " + p)
                return 1
            res = resolve_all(a.root, a.instance, blank=a.blank)
            print(f"{label}: clean ({len(res['slots'])} slots; instance "
                  f"{res['instance'] or 'none'} via {res['selected_by']})")
            return 0
        if a.write:
            out = write_resolved(a.root, a.instance)
            print(out)
            body = json.loads(out.read_text(encoding="utf-8"))
            slots = load_slots(a.root)
            bad = [sid for sid, rec in body["slots"].items()
                   if "error" in rec and not slots.get(sid, {}).get("optional")]
            if bad:
                # written anyway: a reader of an ERROR slot fails loudly on that slot
                print(f"resolve: wrote {len(bad)} required slot(s) in ERROR: {', '.join(bad)}",
                      file=sys.stderr)
                return 1
            return 0
        if a.slot:
            print(json.dumps(resolve_slot(a.slot, a.root, a.instance, a.blank), indent=2, sort_keys=True))
            return 0
        res = resolve_all(a.root, a.instance, a.blank)
        print(f"instance: {res['instance'] or 'none'} (selected by {res['selected_by']})")
        errors = 0
        for sid, rec in res["slots"].items():
            if "error" in rec:
                if rec.get("optional"):
                    state = "unfilled (optional)"
                else:
                    state = "ERROR " + rec["error"]
                    errors += 1
                print(f"  {sid:32} {state}")
                continue
            flag = ""
            if rec.get("requires_ratification"):
                flag = "  ratified" if rec.get("ratified") else "  UNRATIFIED"
            where = rec.get("path") or ", ".join(rec.get("paths") or [])
            print(f"  {sid:32} {rec['source']:8} {where}{flag}")
        if errors:
            print(f"resolve: {errors} slot(s) in ERROR", file=sys.stderr)
            return 1
        return 0
    except (SlotError, InstanceError) as e:
        print(f"resolve: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
