#!/usr/bin/env python3
"""figma_readback.py: HeyHi Design Bridge Translate — the LIVE geometry instrument (I2).

The reason this file exists: three instruments reported PASS on the D-09 build and the
result could not be reviewed. `GEOMETRY CHECK` reasoned about the IR's own numbers;
`mock-run.mjs` proved the ops execute but never computed layout; the mock's font
registry disagreed with real Figma. This is the one instrument that reads back what
Figma actually computed. It reconstructs a named IR into a SCRATCH Figma page with real
auto-layout, reads back the root frame's computed height plus a named set of node
dimensions, compares them to the extractor's captured values, FAILS on drift beyond a
stated tolerance, and removes the scratch page on both success AND failure.

Why a focused reconstruction, not the production `code.js`. Only the agent (MCP client)
can call `use_figma`, and its `code` argument is inline text capped at 50,000 chars. The
production interpreter alone is ~30k of dense JS across every chunk — the exact
transcription hazard the plugin transport (scripts/transport/) was built to avoid. So
this tool authors ONE compact, self-contained `use_figma` payload that rebuilds the
frame tree with the SAME axis resolution the builder uses (`frameAxisAuto`, ported
verbatim below and in build_figma.py) and lets Figma's real layout engine compute the
result — which is the whole point: the circular constraint and the 100px fallback are
Figma behaviors the IR-only checks cannot see. Geometry (frames, auto-layout, sizing,
text-for-hug) is reconstructed faithfully; fills / SVG / variables are not, because they
do not move a frame's box.

A Python script cannot call `use_figma`. So this tool authors the payload and judges the
return; the agent issues the one call:

    1. figma_readback.py emit <ir> --out-dir D [--pre-d1] [--nodes "A,B"]
    2. <agent runs D/readback.use_figma.js via use_figma(fileKey, <contents>)>
    3. figma_readback.py verdict D <<< '<the use_figma return JSON>'   # exit 1 on drift

The scratch file is any throwaway Figma design file (create one with the Figma MCP
`create_new_file`); pass its fileKey to `use_figma`. The payload builds a uniquely-named
page, measures it, and removes it — never a review or client file.

Two builder eras drive the two failure fixtures the batch is proven against:
  post-fix (default): the current builder's axis resolution — the golden reads 52x8.
  --pre-d1          : the pre-D1 "never resize a HUG axis" rule — the token-sized leaves
                      keep Figma's 100px createFrame default, so the readback is shown
                      FAILING on the drift it must catch (the D-09-class collapse).

This file also hosts the runner for the sibling `GEOMETRY CHECK` (assert_geometry in
build_figma.py), so that check can be exercised — and witnessed failing — in isolation:
    figma_readback.py geometry-check <ir> [--pre-d1]
    figma_readback.py geometry-selftest

HeyHi Confidential.
"""
import argparse
import json
import os
import sys
import time

STATE = "readback-state.json"


def _here():
    return os.path.dirname(os.path.abspath(__file__))


# ----------------------------------------------------------------------------------
# the GEOMETRY CHECK runner (I1) — exercise assert_geometry in isolation
# ----------------------------------------------------------------------------------
def _load_assert_geometry():
    """Import assert_geometry from the sibling build_figma.py (the GEOMETRY CHECK)."""
    sys.path.insert(0, _here())
    import build_figma  # noqa: E402
    return build_figma.assert_geometry


def _run_geometry_check(root, pre_d1=False):
    ag = _load_assert_geometry()
    semantics = "pre-d1" if pre_d1 else "post-d1"
    findings = ag(root, sizing_semantics=semantics)
    errors = [g for g in findings if g.get("severity", "error") == "error"]
    return findings, errors


def cmd_geometry_check(args):
    try:
        ir = json.loads(open(args.ir, encoding="utf-8").read())
    except (OSError, json.JSONDecodeError) as e:
        print("geometry-check: cannot read IR %s: %s" % (args.ir, e), file=sys.stderr)
        return 2
    root = ir.get("root", ir)
    # D-05 convergence: the builder rewrites css-grid containers (D-03 `preprocess_flags`)
    # BEFORE it emits, and its own in-builder GEOMETRY CHECK reasons about that rewritten
    # tree. Run the same pre-pass here so the check predicts EMITTED geometry, not the raw
    # IR. Without it, every css-grid page (a full-span `grid-column: 1/-1` child) false-
    # FAILs on the pre-rebuild `v:FILL`-in-`v:HUG` circular constraint the builder resolves
    # (studio-index/session: raw 1 circular error -> 0 after the rebuild). A no-op on every
    # non-grid golden (verified: geometry-defects, atlas-*, cards, controls, logo-wall, ...).
    sys.path.insert(0, _here())
    import build_figma  # noqa: E402
    build_figma.preprocess_flags(root)
    findings, errors = _run_geometry_check(root, pre_d1=args.pre_d1)
    era = "pre-d1 (the pre-fix builder)" if args.pre_d1 else "post-d1 (the current builder)"
    if args.json:
        print(json.dumps({"era": era, "errors": len(errors),
                          "findings": findings, "ok": not errors}, indent=2))
    else:
        print("GEOMETRY CHECK :: %s :: %s" % (os.path.basename(args.ir), era))
        if not findings:
            print("  PASS — no overflow, white-space, circular constraint, or fallback size.")
        for g in findings:
            print("  [%s/%s]  %s :: %s" % (g.get("severity", "error"), g["kind"],
                                           g.get("node", ""), g["detail"]))
        print("  %s (%d error(s))" % ("FAIL" if errors else "PASS", len(errors)))
    return 1 if errors else 0


# --- embedded regression proof (batch rule 6: the check must be shown able to fail) ---
# A leaf whose vertical axis is a genuine content-hug with a captured height: the pre-D1
# builder discards the 8 and Figma keeps its 100px createFrame default; the current
# builder FIXes it. The same IR must FAIL under pre-d1 and PASS under post-d1.
_FIXTURE_FALLBACK = {"root": {"type": "FRAME", "name": "Root", "layout": {"mode": "VERTICAL"},
    "size": {"w": 200, "h": None, "sizing": {"h": "FIXED", "v": "HUG"}}, "children": [
        {"type": "FRAME", "name": "Bar", "layout": {"mode": "VERTICAL"},
         "size": {"w": 52, "h": 8, "sizing": {"h": "FILL", "v": "HUG"}}}]}}

# A `v: FILL` child inside a VERTICAL parent whose vertical (primary) axis HUGs: the
# circular constraint Figma collapses. Must FAIL under both eras (it is a shape defect,
# not a builder-era one). The child carries no fixed height, so only `circular` fires.
_FIXTURE_CIRCULAR = {"root": {"type": "FRAME", "name": "Root", "layout": {"mode": "VERTICAL"},
    "size": {"w": 1440, "h": None, "sizing": {"h": "FIXED", "v": "HUG"}}, "children": [
        {"type": "FRAME", "name": "Section", "layout": {"mode": "VERTICAL"},
         "size": {"w": 1440, "h": None, "sizing": {"h": "FILL", "v": "FILL"}}, "children": [
             {"type": "TEXT", "name": "Body", "size": {"w": 400, "h": 40, "sizing": {"h": "HUG", "v": "HUG"}}}]}]}}

# An all-resolvable control (a leaf with a captured height, a HUG stack of real content)
# so the runner is proven able to PASS, not only fail — under BOTH eras.
_FIXTURE_GOOD = {"root": {"type": "FRAME", "name": "Root", "layout": {"mode": "VERTICAL"},
    "size": {"w": 200, "h": None, "sizing": {"h": "FIXED", "v": "HUG"}}, "children": [
        {"type": "TEXT", "name": "Body", "size": {"w": 180, "h": 40, "sizing": {"h": "HUG", "v": "HUG"}}}]}}


def cmd_geometry_selftest(args):
    """Prove the GEOMETRY CHECK can express the failures it was blind to (I1)."""
    ok = True

    def has(kind, errs):
        return any(g["kind"] == kind for g in errs)

    _, pre_err = _run_geometry_check(_FIXTURE_FALLBACK["root"], pre_d1=True)
    _, post_err = _run_geometry_check(_FIXTURE_FALLBACK["root"], pre_d1=False)
    c1 = has("fallback", pre_err) and not post_err
    print("  [%s] fallback: a token-sized leaf collapses to Figma's 100px default under the "
          "pre-fix builder, resolves under the fix" % ("PASS" if c1 else "FAIL"))
    ok &= c1

    _, circ_err = _run_geometry_check(_FIXTURE_CIRCULAR["root"], pre_d1=False)
    c2 = has("circular", circ_err)
    print("  [%s] circular: a v:FILL child inside a vertical-HUG parent is flagged "
          "(the D-09 root-collapse shape)" % ("PASS" if c2 else "FAIL"))
    ok &= c2

    _, g_pre = _run_geometry_check(_FIXTURE_GOOD["root"], pre_d1=True)
    _, g_post = _run_geometry_check(_FIXTURE_GOOD["root"], pre_d1=False)
    c3 = not g_pre and not g_post
    print("  [%s] control: an all-resolvable IR reports no error under either builder era"
          % ("PASS" if c3 else "FAIL"))
    ok &= c3

    print("geometry-selftest: %s. The GEOMETRY CHECK now sees the circular constraint and "
          "the height fallback it was blind to." % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


# ----------------------------------------------------------------------------------
# the LIVE readback (I2): author one use_figma payload, judge its return
# ----------------------------------------------------------------------------------
def _num(x):
    return x if isinstance(x, (int, float)) and not isinstance(x, bool) else None


def _minify(node):
    """Strip an IR node to the fields that move a frame's box, so the embedded payload
    stays well under the 50k use_figma cap. Fills / strokes / tokens / SVG do not affect
    geometry and are dropped."""
    lay = node.get("layout") or {}
    out = {"type": node.get("type"), "name": node.get("name")}
    keep_layout = {k: lay[k] for k in ("mode", "padding", "itemSpacing", "layoutWrap",
                                       "counterAxisSpacing") if k in lay}
    if keep_layout:
        out["layout"] = keep_layout
    if node.get("size") is not None:
        sz = node["size"]
        out["size"] = {k: sz.get(k) for k in ("w", "h", "sizing") if k in sz}
    if node.get("type") == "TEXT" and node.get("characters"):
        out["characters"] = node["characters"]
    kids = node.get("children") or []
    if kids:
        out["children"] = [_minify(k) for k in kids]
    return out


def _collect_targets(node, names, out):
    """Every FRAME whose name is in `names` (or, if `names` is None, every leaf FRAME
    that carries BOTH a captured width and height — the token-sized frames the D1
    collapse hit) -> its expected {w, h} from the IR, grouped by name."""
    if not isinstance(node, dict):
        return out
    if node.get("type") == "FRAME":
        sz = node.get("size") or {}
        w, h = _num(sz.get("w")), _num(sz.get("h"))
        is_leaf = not (node.get("children") or [])
        take = (node.get("name") in names) if names is not None else (is_leaf and w is not None and h is not None)
        if take:
            out.setdefault(node.get("name", "?"), []).append({"w": w, "h": h})
    for c in node.get("children") or []:
        _collect_targets(c, names, out)
    return out


# The one use_figma payload: reconstruct the IR with real auto-layout, measure the root
# and every target node, then remove the scratch page in a `finally` (cleanup on success
# AND failure). `axisPlan` is the frameAxisAuto port — kept in sync with build_figma.py's
# interpreter (~L334) and predict_frame_axes. `builtCount` is a transcription-fidelity
# check: it must equal the IR's node count.
_PROBE_JS = r"""
const IR = %(ir)s;
const PAGE_NAME = %(page_name)s;
const ERA = %(era)s;
const TARGETS = %(targets)s;

function axisPlan(mode, size, isLeaf, axis) {
  const sh = (size && size.sizing) || {};
  const declaredHug = (axis === 'w') ? (sh.h === 'HUG') : (sh.v === 'HUG');
  const cap = (axis === 'w') ? size.w : size.h;
  const capNum = (typeof cap === 'number');
  const isPrimary = (mode === 'HORIZONTAL') ? (axis === 'w') : (axis === 'h');
  if (ERA === 'pre-d1') {
    // "never resize a HUG axis": a declared-HUG axis keeps Figma's createFrame default;
    // a dimensionless axis hugs; everything else takes its captured value.
    if (declaredHug) return { mode: 'FIXED', resize: null };
    if (!capNum) return { mode: 'AUTO', resize: null };
    return { mode: 'FIXED', resize: cap };
  }
  // post-d1 (frameAxisAuto): a HUG axis is a genuine content-hug only as a non-leaf
  // container's primary axis, or a dimensionless axis; else the captured value is FIXED.
  if (isPrimary && declaredHug && !isLeaf) return { mode: 'AUTO', resize: null };
  if (!capNum) return { mode: 'AUTO', resize: null };
  return { mode: 'FIXED', resize: cap };
}

const built = [];
async function build(node, parent) {
  const type = node.type;
  const size = node.size || {};
  const layout = node.layout || {};
  const mode = layout.mode || 'NONE';
  const kids = node.children || [];
  const nm = node.name || type;
  if (type === 'TEXT') {
    const t = figma.createText();
    await figma.loadFontAsync({ family: 'Inter', style: 'Regular' });
    t.fontName = { family: 'Inter', style: 'Regular' };
    t.name = nm;
    t.characters = (node.characters != null ? String(node.characters) : nm) || ' ';
    parent.appendChild(t);
    const sh = size.sizing || {};
    try {
      if (parent.layoutMode === 'VERTICAL' && sh.h === 'FILL') { t.layoutSizingHorizontal = 'FILL'; t.textAutoResize = 'HEIGHT'; }
      else if (parent.layoutMode === 'HORIZONTAL' && sh.h === 'FILL') { t.layoutGrow = 1; t.textAutoResize = 'HEIGHT'; }
      else if (typeof size.w === 'number') { t.resize(Math.max(size.w, 1), t.height); t.textAutoResize = 'HEIGHT'; }
    } catch (e) {}
    built.push({ name: nm, node: t });
    return t;
  }
  // FRAME / GROUP -> a frame
  const f = figma.createFrame();
  f.name = nm;
  f.fills = [];
  if (mode === 'VERTICAL' || mode === 'HORIZONTAL') {
    f.layoutMode = mode;
    const p = layout.padding || {};
    f.paddingTop = p.t || 0; f.paddingRight = p.r || 0; f.paddingBottom = p.b || 0; f.paddingLeft = p.l || 0;
    if (typeof layout.itemSpacing === 'number') f.itemSpacing = layout.itemSpacing;
    if (layout.layoutWrap === 'WRAP') {
      try { f.layoutWrap = 'WRAP'; if (typeof layout.counterAxisSpacing === 'number') f.counterAxisSpacing = layout.counterAxisSpacing; } catch (e) {}
    }
  }
  parent.appendChild(f);
  built.push({ name: nm, node: f });
  for (const k of kids) await build(k, f);
  const isLeaf = kids.length === 0;
  if (mode === 'VERTICAL' || mode === 'HORIZONTAL') {
    const wp = axisPlan(mode, size, isLeaf, 'w');
    const hp = axisPlan(mode, size, isLeaf, 'h');
    const primIsW = (mode === 'HORIZONTAL');
    const primPlan = primIsW ? wp : hp;
    const cntPlan = primIsW ? hp : wp;
    f.primaryAxisSizingMode = (primPlan.mode === 'AUTO') ? 'AUTO' : 'FIXED';
    f.counterAxisSizingMode = (cntPlan.mode === 'AUTO') ? 'AUTO' : 'FIXED';
    const wArg = (wp.resize != null) ? Math.max(wp.resize, 0.01) : f.width;
    const hArg = (hp.resize != null) ? Math.max(hp.resize, 0.01) : f.height;
    if (wp.resize != null || hp.resize != null) { try { f.resize(wArg, hArg); } catch (e) {} }
    // re-assert AUTO last (resize silently flips a sized axis to FIXED)
    try { if (primPlan.mode === 'AUTO') f.primaryAxisSizingMode = 'AUTO'; if (cntPlan.mode === 'AUTO') f.counterAxisSizingMode = 'AUTO'; } catch (e) {}
  } else {
    // NONE / GROUP: literal captured box (a captured 0 is real; floor at 0.01)
    const w = (typeof size.w === 'number') ? size.w : null;
    const h = (typeof size.h === 'number') ? size.h : null;
    if (w !== null || h !== null) { try { f.resize(Math.max(w !== null ? w : f.width, 0.01), Math.max(h !== null ? h : f.height, 0.01)); } catch (e) {} }
  }
  return f;
}

let result = { ok: false, removed: false };
let page = null;
try {
  page = figma.createPage();
  page.name = PAGE_NAME;
  await figma.setCurrentPageAsync(page);
  const rootNode = await build(IR, page);
  const r2 = (n) => Math.round(n * 100) / 100;
  const nodes = {};
  for (const b of built) {
    if (TARGETS.indexOf(b.name) >= 0) {
      (nodes[b.name] = nodes[b.name] || []).push({ w: r2(b.node.width), h: r2(b.node.height) });
    }
  }
  result = { ok: true, pageName: page.name, rootName: rootNode.name,
             root: { w: r2(rootNode.width), h: r2(rootNode.height) },
             nodes: nodes, builtCount: built.length, removed: false };
} catch (e) {
  result = { ok: false, error: String((e && e.message) || e), removed: false };
} finally {
  // cleanup on BOTH paths. Figma forbids removing the CURRENT page and requires >= 1
  // page, so switch to another page first, then remove the scratch page.
  try {
    if (page && figma.root.children.length > 1) {
      const other = figma.root.children.find(p => p.id !== page.id);
      if (other) await figma.setCurrentPageAsync(other);
      page.remove();
      result.removed = true;
    }
  } catch (ce) { result.cleanupError = String((ce && ce.message) || ce); }
}
return JSON.stringify(result);
"""


def _count_nodes(node):
    return 1 + sum(_count_nodes(k) for k in (node.get("children") or []))


def cmd_emit(args):
    out_dir = os.path.abspath(args.out_dir)
    os.makedirs(out_dir, exist_ok=True)
    try:
        ir = json.loads(open(args.ir, encoding="utf-8").read())
    except (OSError, json.JSONDecodeError) as e:
        print("emit: cannot read IR %s: %s" % (args.ir, e), file=sys.stderr)
        return 2
    root = ir.get("root", ir)
    era = "pre-d1" if args.pre_d1 else "post-d1"
    stem = os.path.splitext(os.path.basename(args.ir))[0]
    page_name = args.page_name or ("HeyHi Readback · %s · %s · %d" % (stem, era, int(time.time())))
    names = [s.strip() for s in args.nodes.split(",")] if args.nodes else None
    targets = _collect_targets(root, set(names) if names else None, {})

    payload = _PROBE_JS % {
        "ir": json.dumps(_minify(root), ensure_ascii=False),
        "page_name": json.dumps(page_name, ensure_ascii=False),
        "era": json.dumps(era),
        "targets": json.dumps(sorted(targets.keys()), ensure_ascii=False),
    }
    js_path = os.path.join(out_dir, "readback.use_figma.js")
    with open(js_path, "w", encoding="utf-8") as fh:
        fh.write(payload)

    st = {"ir": os.path.abspath(args.ir), "era": era, "page_name": page_name,
          "targets": targets, "root_captured_h": _num((root.get("size") or {}).get("h")),
          "node_count": _count_nodes(root), "tol": args.tol}
    with open(os.path.join(out_dir, STATE), "w", encoding="utf-8") as fh:
        json.dump(st, fh, indent=2, ensure_ascii=False)

    USE_FIGMA_CAP = 50000
    over = len(payload) - USE_FIGMA_CAP
    print("READBACK emit :: %s :: %s" % (stem, era))
    print("  scratch page: %s" % page_name)
    print("  payload: %s   (%d chars, cap %d%s)"
          % (js_path, len(payload), USE_FIGMA_CAP,
             "" if over < 0 else "  OVER by %d" % over))
    if over >= 0:
        print("  ERROR: the payload exceeds the use_figma inline-code cap; a single-call "
              "readback cannot carry this IR. Narrow it with --nodes on a section, or read "
              "back a sub-tree; the golden and per-section fixtures fit comfortably.")
    print("  reconstructs %d node(s); reads back the root + %d target name(s), removes the page."
          % (st["node_count"], len(targets)))
    if not targets:
        print("  WARNING: 0 node targets selected — the readback will verify only the root, "
              "not any node geometry. Pass --nodes to name targets. verdict will report "
              "INCONCLUSIVE, not PASS.")
    print("  expected (captured) target geometry:")
    for name, lst in sorted(targets.items()):
        exp = lst[0]
        print("    %-16s %sx%s  (x%d)" % (name, exp["w"], exp["h"], len(lst)))
    print("  Next: run %s via use_figma(fileKey, <contents>) on a SCRATCH file, then:" % os.path.basename(js_path))
    print("        figma_readback.py verdict %s  (pipe the use_figma return on stdin)" % out_dir)
    return 0


def _read_stdin_or_arg(args):
    if getattr(args, "result_file", None):
        return open(args.result_file, encoding="utf-8").read()
    if getattr(args, "result", None):
        return args.result
    return sys.stdin.read()


def _parse_return(text):
    """Parse a use_figma return: JSON, or the first balanced object if wrapped in prose."""
    text = (text or "").strip()
    try:
        return json.loads(text)
    except Exception:
        pass
    start = text.find("{")
    if start < 0:
        raise ValueError("no JSON object in the use_figma return")
    depth, in_str, esc = 0, False, False
    for i in range(start, len(text)):
        c = text[i]
        if in_str:
            esc = (c == "\\") and not esc
            if c == '"' and not esc:
                in_str = False
            continue
        if c == '"':
            in_str = True
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return json.loads(text[start:i + 1])
    raise ValueError("unbalanced JSON in the use_figma return")


def cmd_verdict(args):
    out_dir = os.path.abspath(args.out_dir)
    with open(os.path.join(out_dir, STATE), encoding="utf-8") as fh:
        st = json.load(fh)
    res = _parse_return(_read_stdin_or_arg(args))
    tol = args.tol if args.tol is not None else st.get("tol", 2.0)

    print("READBACK VERDICT :: %s :: %s" % (st["page_name"], st["era"]))
    if not res.get("ok"):
        print("  MEASURE FAILED: %s" % res.get("error", "(no error given)"))
    # An incomplete/mis-transcribed build must not be able to pass: if fewer nodes were
    # built than the IR carries, the measurements do not describe the whole build.
    bc = res.get("builtCount")
    incomplete = (bc is not None and bc != st.get("node_count"))
    if incomplete:
        print("  INCOMPLETE: builtCount %s != IR node count %s — the payload built fewer "
              "nodes than the IR carries (a mis-transcribed or partial run); this readback "
              "cannot vouch for the build." % (bc, st.get("node_count")))
    # A readback with no node targets verified only the root; it must not masquerade as a
    # clean geometry pass (the false-clean this batch exists to kill). Name targets with
    # --nodes, or accept the default leaf-frame selection produced some.
    no_targets = not st.get("targets")
    if no_targets:
        print("  INCONCLUSIVE: 0 node targets — the readback checked only the root frame, "
              "not any node geometry. Re-run emit with --nodes, or against an IR that has "
              "leaf frames with captured dimensions.")
    measured = res.get("nodes", {}) or {}
    drifts = []

    def close(a, b):
        return a is not None and b is not None and abs(a - b) <= tol

    # per-target-node drift: the extractor's captured (w, h) vs what Figma computed. The
    # captured value is the target for BOTH eras — the pre-d1 build drifts, the post-d1
    # build lands on it.
    for name, expected_list in sorted(st["targets"].items()):
        got_list = measured.get(name, [])
        exp_w = expected_list[0]["w"] if expected_list else None
        exp_h = expected_list[0]["h"] if expected_list else None
        if not got_list:
            drifts.append("%s: expected %sx%s, NOT FOUND in Figma" % (name, exp_w, exp_h))
            print("  [MISS] %-16s expected %sx%s — not found" % (name, exp_w, exp_h))
            continue
        for g in got_list:
            okw, okh = close(g["w"], exp_w), close(g["h"], exp_h)
            tag = "ok   " if (okw and okh) else "DRIFT"
            print("  [%s] %-16s Figma %sx%s  vs captured %sx%s" % (tag, name, g["w"], g["h"], exp_w, exp_h))
            if not (okw and okh):
                dh = "n/a" if (g["h"] is None or exp_h is None) else round(abs(g["h"] - exp_h), 2)
                drifts.append("%s: Figma %sx%s vs captured %sx%s (h drift %s)"
                              % (name, g["w"], g["h"], exp_w, exp_h, dh))

    # root frame: compare to the captured page height when the IR carries one; otherwise
    # (a HUG root) report it and guard against a collapse below the tallest measured child.
    root = res.get("root") or {}
    root_h = root.get("h")
    cap = st.get("root_captured_h")
    tallest = max([g["h"] for lst in measured.values() for g in lst if g.get("h") is not None] or [0])
    print("  root frame '%s': Figma height %s" % (res.get("rootName", "?"), root_h))
    if cap is not None:
        if not close(root_h, cap):
            drifts.append("root height Figma %s vs captured page height %s" % (root_h, cap))
            print("        DRIFT vs captured page height %s (tol %s)" % (cap, tol))
        else:
            print("        matches captured page height %s (tol %s)" % (cap, tol))
    else:
        print("        (root HUGs; no captured page height in the IR — collapse guard: "
              "root height must be >= tallest child %s)" % tallest)
        if root_h is not None and tallest and root_h + tol < tallest:
            drifts.append("root collapsed to %s, below the tallest child %s" % (root_h, tallest))

    # cleanup MUST have happened (scratch page removed on success AND failure).
    if not res.get("removed"):
        print("  CLEANUP: scratch page NOT removed%s"
              % (" (%s)" % res["cleanupError"] if res.get("cleanupError") else ""))
    else:
        print("  cleanup: scratch page removed.")

    failed = bool(drifts) or not res.get("ok") or not res.get("removed") or incomplete or no_targets
    if no_targets and not (drifts or not res.get("ok") or not res.get("removed") or incomplete):
        status = "INCONCLUSIVE (no node targets)"
    else:
        status = "FAIL" if failed else "PASS"
    print("  %s%s" % (status, " — %d drift(s)/issue(s)" % len(drifts) if drifts else ""))
    for d in drifts:
        print("    drift: %s" % d)
    return 1 if failed else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="HeyHi Design Bridge — live Figma geometry readback (I2) "
                                             "and the GEOMETRY CHECK runner (I1).")
    sub = ap.add_subparsers(dest="cmd", required=True)

    gc = sub.add_parser("geometry-check", help="run assert_geometry on an IR; exit 1 on any error")
    gc.add_argument("ir")
    gc.add_argument("--pre-d1", action="store_true", help="reproduce the pre-fix builder era (the 100px collapse)")
    gc.add_argument("--json", action="store_true")

    sub.add_parser("geometry-selftest", help="embedded proof the GEOMETRY CHECK can fail and pass")

    em = sub.add_parser("emit", help="author one use_figma payload that builds + measures + cleans up")
    em.add_argument("ir")
    em.add_argument("--out-dir", required=True)
    em.add_argument("--pre-d1", action="store_true", help="reconstruct the pre-fix era (the 100px collapse)")
    em.add_argument("--page-name", default=None)
    em.add_argument("--nodes", default=None, help="comma-separated node names to read back "
                                                  "(default: every leaf FRAME with a captured w and h)")
    em.add_argument("--tol", type=float, default=2.0)

    vp = sub.add_parser("verdict", help="judge a measure return; exit 1 on drift")
    vp.add_argument("out_dir")
    vp.add_argument("--result-file", dest="result_file", default=None)
    vp.add_argument("--result", default=None)
    vp.add_argument("--tol", type=float, default=None)

    args = ap.parse_args(argv)
    return {
        "geometry-check": cmd_geometry_check,
        "geometry-selftest": cmd_geometry_selftest,
        "emit": cmd_emit, "verdict": cmd_verdict,
    }[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
