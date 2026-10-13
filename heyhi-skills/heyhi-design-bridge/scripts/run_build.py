#!/usr/bin/env python3
"""
HeyHi Design Bridge — Chunk Runner (drives build_figma.py's plan into Figma).

build_figma.py turns a reviewed IR into an ordered set of use_figma chunks, each
carrying an `__IDMAP__` placeholder for the node ids earlier chunks return. This
script productizes the run loop the agent follows to issue those chunks: it fills
`__IDMAP__` from the accumulated returns, threads ids forward, accumulates the
flags/errors/created-vs-reused report, and prints the final landing report. It
replaces the ad-hoc /tmp prep-and-merge pattern used in the T2/T3 spike sessions.

The runner does NOT call use_figma itself — only the agent (MCP client) can. The
agent's loop, per chunk, is:

    1. python3 run_build.py prep   <out-dir>           # fills __IDMAP__, writes chunk_<i>.ready.js
    2. <agent reads chunk_<i>.ready.js, calls use_figma with its contents>
    3. python3 run_build.py record <out-dir> <<'JSON'  # merges the use_figma return
       <the JSON the use_figma call returned>
       JSON
    ... repeat until all chunks are issued ...
    4. python3 run_build.py assets <out-dir>           # raster embeds via upload_assets
    5. python3 run_build.py report <out-dir>           # the landing report

After the chunks land, any raster IMAGE fill is embedded full-res via the Figma MCP
`upload_assets` tool (raw bytes -> cover fill on the node), NOT inline base64. `assets`
lists each one with its resolved node id; the agent calls upload_assets(nodeId) then POSTs
the file bytes to the returned single-use URL. SVGs never take this path (they are deduped
into components by build_figma.py and imported via createNodeFromSvg).

Commands:
    init   <out-dir>                 Start a run from build_figma.py's manifest.json.
    prep   <out-dir> [--chunk N]     Fill __IDMAP__ for the current (or Nth) chunk.
    record <out-dir> [--chunk N]     Merge a use_figma return (stdin, --result-file,
                                     or --result). Advances the cursor.
    status <out-dir>                 Show progress.
    assets <out-dir>                 List raster embeds (node id + path) for upload_assets.
    report <out-dir>                 Final landing report (pages, Variables, flags).
    self-test <ir.json ...>          Headless proof of the loop: build a plan, then
                                     simulate the executor and assert every chunk's
                                     `needs` are satisfied in order (no Figma).

HeyHi Confidential.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

STATE = "run-state.json"
USE_FIGMA_HARD_CAP = 50000  # the use_figma `code` argument is hard-capped at 50,000 chars


# ----------------------------------------------------------------------------------
# state helpers
# ----------------------------------------------------------------------------------
def _state_path(out_dir):
    return os.path.join(out_dir, STATE)


def load_state(out_dir):
    with open(_state_path(out_dir), "r", encoding="utf-8") as fh:
        return json.load(fh)


def save_state(out_dir, st):
    with open(_state_path(out_dir), "w", encoding="utf-8") as fh:
        json.dump(st, fh, indent=2, ensure_ascii=False)


def load_manifest(out_dir):
    with open(os.path.join(out_dir, "manifest.json"), "r", encoding="utf-8") as fh:
        return json.load(fh)


def parse_result(text):
    """Parse a use_figma return. The return is JSON.stringify(out); accept it
    directly, or extract the first balanced JSON object if it arrives wrapped in
    surrounding text. String-aware so braces inside flag text do not fool it."""
    text = (text or "").strip()
    try:
        return json.loads(text)
    except Exception:
        pass
    start = text.find("{")
    if start < 0:
        raise ValueError("no JSON object found in the use_figma result")
    depth, in_str, esc = 0, False, False
    for i in range(start, len(text)):
        c = text[i]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
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
    raise ValueError("unbalanced JSON in the use_figma result")


def categorize(key):
    if key == "__PAGE__":
        return "page"
    if key == "__COL__":
        return "collection"
    if key.startswith("var:type:"):
        return "type_variable"
    if key.startswith("var:"):
        return "color_variable"
    if key.startswith("doc_"):
        return "doc_node"
    return "node"


# ----------------------------------------------------------------------------------
# commands
# ----------------------------------------------------------------------------------
def cmd_init(args):
    man = load_manifest(args.out_dir)
    # D-03/D-05: a manifest.blocked build carries a BLOCKING flag (an unconsumable
    # ::before/::after, or a css grid that cannot be partitioned into grid-column
    # spans) and must NOT be issued to Figma — shipping a blocked build is the D-09
    # failure this batch closes. build_figma.py --allow-blocking downgrades the exit
    # for measurement/inspection only; the run loop refuses it here.
    if man.get("blocked"):
        brows = man.get("blocking_flags", [])
        print("RUN REFUSED: manifest.blocked is true — this build carries %d BLOCKING flag(s)"
              % sum(r.get("count", 1) for r in brows))
        print("  and must NOT be issued to use_figma. Resolve the blocking flag(s) in the")
        print("  source/extractor and rebuild; --allow-blocking is for measurement, not shipping.")
        for r in man.get("blocking_flags", [])[:8]:
            cnt = ("  x%d" % r["count"]) if r.get("count", 1) > 1 else ""
            print("    [%s]%s  %s :: %s" % (r.get("feature", ""), cnt, r.get("node", ""), r.get("action", "")))
        sys.exit(1)
    st = {
        "page_name": man.get("page_name"),
        "type_mode": man.get("type_mode"),
        "rerun": man.get("rerun"),
        "chunk_count": man.get("chunk_count"),
        "ir_flags": man.get("flags", 0),
        "assets": man.get("assets", []),   # raster fills embedded post-write via upload_assets
        "cursor": 0,
        "idmap": {},
        "created": {},     # key -> id (this run created it)
        "reused": {},      # key -> id (already existed; reused)
        "flags": [],
        "errors": [],
        "page_ids": [],
        "page_names": [],
        "history": [],
    }
    save_state(args.out_dir, st)
    print("Run initialized: %s" % man.get("page_name"))
    print("  %d chunk(s) to issue, type_mode=%s, rerun=%s"
          % (man.get("chunk_count"), man.get("type_mode"), man.get("rerun")))
    print("  Next: python3 run_build.py prep %s" % args.out_dir)


def cmd_prep(args):
    st = load_state(args.out_dir)
    man = load_manifest(args.out_dir)
    i = args.chunk if args.chunk is not None else st["cursor"]
    if i >= st["chunk_count"]:
        print("All %d chunk(s) already issued. Next: python3 run_build.py report %s"
              % (st["chunk_count"], args.out_dir))
        return
    ch = man["chunks"][i]
    needs = ch.get("needs", [])
    missing = [n for n in needs if n not in st["idmap"]]

    code_path = ch["code_file"]
    if not os.path.isabs(code_path):
        code_path = os.path.join(args.out_dir, code_path)
    with open(code_path, "r", encoding="utf-8") as fh:
        code = fh.read()
    # Idmap pruning (chunk-budget-fix): inject ONLY this chunk's cross-chunk `needs`, not
    # the whole accumulated map. The full-map dump grew to ~10k chars in late chunks and
    # was the headroom-killer that pushed logo-heavy chunks over the use_figma cap.
    # compute_needs() already identifies exactly the keys the interpreter resolves from
    # IDMAP; everything created in this chunk is local to it (the interpreter's made[]).
    full_n = len(st["idmap"])
    pruned = {k: st["idmap"][k] for k in needs if k in st["idmap"]}
    code = code.replace("__IDMAP__", json.dumps(pruned, ensure_ascii=False))
    ready = os.path.join(args.out_dir, "chunk_%d.ready.js" % i)
    with open(ready, "w", encoding="utf-8") as fh:
        fh.write(code)

    over = len(code) - USE_FIGMA_HARD_CAP
    print("PREP chunk %d/%d  (%s)" % (i, st["chunk_count"] - 1, st["page_name"]))
    print("  node ops: %d   total ops: %d" % (ch.get("node_count", 0), ch.get("op_count", 0)))
    print("  idmap injected: %d key(s)  (pruned from %d accumulated)" % (len(pruned), full_n))
    print("  rendered chars: %d / %d  (%s)"
          % (len(code), USE_FIGMA_HARD_CAP,
             ("headroom %d" % (-over)) if over < 0 else ("OVER CAP by %d" % over)))
    print("  needs from earlier chunks: %s" % (needs or "none"))
    if missing:
        print("  WARNING — %d need(s) NOT in the id map yet: %s" % (len(missing), missing))
        print("  Did the previous chunk record its returned ids? Run record before prep.")
    else:
        print("  all needs satisfied by the id map.")
    if over >= 0:
        print("  ERROR — this chunk exceeds the %d-char use_figma cap; do NOT send it as-is."
              % USE_FIGMA_HARD_CAP)
        print("          Rebuild with char-budget chunking (build_figma.py) or lower --max-nodes.")
    print("  ready file: %s" % ready)
    print("  Next: read that file, issue it via use_figma(fileKey, <contents>), then:")
    print("        python3 run_build.py record %s  (pipe the use_figma return on stdin)" % args.out_dir)


def _read_result_text(args):
    if args.result_file:
        with open(args.result_file, "r", encoding="utf-8") as fh:
            return fh.read()
    if args.result:
        return args.result
    return sys.stdin.read()


def cmd_record(args):
    st = load_state(args.out_dir)
    i = args.chunk if args.chunk is not None else st["cursor"]
    res = parse_result(_read_result_text(args))

    created = res.get("created", {}) or {}
    reused = res.get("reused", {}) or {}
    flags = res.get("flags", []) or []
    errors = res.get("errors", []) or []

    for k, v in created.items():
        st["idmap"][k] = v
        st["created"][k] = v
    for k, v in reused.items():
        st["idmap"][k] = v
        st["reused"][k] = v
    st["flags"].extend(flags)
    st["errors"].extend(errors)
    if res.get("pageId") and res["pageId"] not in st["page_ids"]:
        st["page_ids"].append(res["pageId"])
    if res.get("pageName") and res["pageName"] not in st["page_names"]:
        st["page_names"].append(res["pageName"])

    st["history"].append({
        "index": i, "created": len(created), "reused": len(reused),
        "flags": len(flags), "errors": len(errors),
    })
    st["cursor"] = i + 1
    save_state(args.out_dir, st)

    done = st["cursor"] >= st["chunk_count"]
    print("RECORD chunk %d/%d : +%d created, +%d reused, %d flags, %d errors"
          % (i, st["chunk_count"] - 1, len(created), len(reused), len(flags), len(errors)))
    if errors:
        for e in errors[:8]:
            print("  ERROR: %s" % json.dumps(e, ensure_ascii=False))
    if done:
        print("  All chunks issued. Next: python3 run_build.py report %s" % args.out_dir)
    else:
        print("  Next: python3 run_build.py prep %s" % args.out_dir)


def cmd_status(args):
    st = load_state(args.out_dir)
    print("%s : chunk %d/%d issued, %d ids threaded, %d flags, %d errors"
          % (st["page_name"], st["cursor"], st["chunk_count"],
             len(st["idmap"]), len(st["flags"]), len(st["errors"])))


def cmd_report(args):
    st = load_state(args.out_dir)
    cats_created, cats_reused = {}, {}
    for k in st["created"]:
        cats_created[categorize(k)] = cats_created.get(categorize(k), 0) + 1
    for k in st["reused"]:
        cats_reused[categorize(k)] = cats_reused.get(categorize(k), 0) + 1

    def cc(cat):
        return cats_created.get(cat, 0)

    def rc(cat):
        return cats_reused.get(cat, 0)

    print("HeyHi Design Bridge :: Translate landing report")
    print("Page: %s" % (", ".join(st["page_names"]) or st["page_name"]))
    print("Chunks issued: %d/%d%s"
          % (st["cursor"], st["chunk_count"],
             "  (INCOMPLETE)" if st["cursor"] < st["chunk_count"] else "  (complete)"))
    print("Type mode: %s" % st["type_mode"])
    print("Mockup nodes created: %d" % cc("node"))
    print("Documentation-frame nodes created: %d" % cc("doc_node"))
    print("Color Variables: %d created, %d reused" % (cc("color_variable"), rc("color_variable")))
    if cc("type_variable") or rc("type_variable"):
        print("Type Variables: %d created, %d reused" % (cc("type_variable"), rc("type_variable")))
    print("Token collection: %d created, %d reused" % (cc("collection"), rc("collection")))
    print("IR does-not-map flags (rendered in the doc frame): %d" % st.get("ir_flags", 0))
    print("Build-time flags returned (font/asset substitutions): %d" % len(st["flags"]))
    feats = {}
    for f in st["flags"]:
        feats[f.get("feature", "?")] = feats.get(f.get("feature", "?"), 0) + 1
    for feat, n in sorted(feats.items(), key=lambda x: -x[1]):
        print("  %2d x %s" % (n, feat))
    print("Errors: %d" % len(st["errors"]))
    for e in st["errors"][:12]:
        print("  %s" % json.dumps(e, ensure_ascii=False))
    if st.get("assets"):
        print("Raster embeds (upload_assets): %d pending  ->  python3 run_build.py assets %s"
              % (len(st["assets"]), args.out_dir))


def cmd_assets(args):
    """List the raster embeds to land via the Figma MCP upload_assets tool. Each raster
    IMAGE fill is embedded AFTER its node's chunk records (so the node id exists), full-res
    and with no base64 transcription. Per asset the agent calls
    upload_assets(fileKey, nodeId=<id>, count=1, scaleMode=<mode>) and POSTs the file's raw
    bytes to the returned single-use URL with the right Content-Type (one image per call)."""
    st = load_state(args.out_dir)
    assets = st.get("assets", []) or []
    if not assets:
        print("No raster embeds: this build has no IMAGE fills (upload_assets not needed).")
        return
    print("Raster embeds via Figma MCP upload_assets (%d):" % len(assets))
    pending = 0
    for a in assets:
        key = a.get("key")
        nid = st["idmap"].get(key)
        path = a.get("imageRef")
        mode = a.get("scaleMode", "FILL")
        ct = a.get("content_type", "application/octet-stream")
        if nid:
            print("  - node %s  (key %s)" % (nid, key))
            print("      upload_assets(fileKey, nodeId=\"%s\", count=1, scaleMode=\"%s\")" % (nid, mode))
            print("      then POST the raw bytes of %s  (Content-Type: %s) to the returned URL" % (path, ct))
        else:
            pending += 1
            print("  - key %s NOT created yet — record its chunk, then re-run `assets`." % key)
            print("      path: %s  (scaleMode %s, %s)" % (path, mode, ct))
    if pending:
        print("  %d embed(s) pending (node id not in the id map yet)." % pending)
    else:
        print("  all %d node id(s) resolved; ready to embed." % len(assets))


def cmd_selftest(args):
    """Headless proof of the run loop: build a plan, then simulate the executor.
    Validates ordering, __IDMAP__ threading, and needs-satisfaction without Figma.
    The JS execution itself is validated by the live run; this proves the plumbing."""
    here = os.path.dirname(os.path.abspath(__file__))
    builder = os.path.join(here, "build_figma.py")
    tmp = tempfile.mkdtemp(prefix="bridge-selftest-")
    # D-03/D-05: forward --allow-blocking so a golden that legitimately BLOCKS (an
    # unconsumable ::before/::after, or a non-partitionable css grid) still writes its
    # plan.json for the plumbing checks below. self-test validates plumbing (ordering,
    # __IDMAP__ threading, needs-satisfaction, geometry), not shippability — a blocked
    # build is refused at the run loop (cmd_init), not here. Without this, a BLOCKING
    # golden makes build_figma.py exit non-zero and check=True aborts the self-test.
    cmd = [sys.executable, builder] + args.ir + ["--out-dir", tmp, "--allow-blocking"]
    if args.max_nodes is not None:
        cmd += ["--max-nodes", str(args.max_nodes)]
    subprocess.run(cmd, check=True, capture_output=True, text=True)
    plan = json.load(open(os.path.join(tmp, "plan.json"), encoding="utf-8"))
    # Surface a blocked build so its self-test PASS is read for what it proves (plumbing),
    # not as shippable — the run loop is where manifest.blocked is refused.
    manifest_blocked = False
    _man_path = os.path.join(tmp, "manifest.json")
    if os.path.isfile(_man_path):
        manifest_blocked = bool(json.load(open(_man_path, encoding="utf-8")).get("blocked"))

    created, idmap = set(), {}
    all_keys = []
    problems = []
    for ch in plan["chunks"]:
        i = ch["index"]
        missing = [n for n in ch.get("needs", []) if n not in created]
        if missing:
            problems.append("chunk %d references unmet keys: %s" % (i, missing))
        # also: every parent/var an op references must resolve by end-of-its-own-chunk
        chunk_created = set()
        for op in ch["ops"]:
            if op.get("key"):
                chunk_created.add(op["key"])
        needs_i = set(ch.get("needs", []))
        for op in ch["ops"]:
            refs = []
            if op.get("parent"):
                refs.append(op["parent"])
            if op.get("component"):
                refs.append(op["component"])
            # C2: INSTANCE_SWAP refs (a frame_component's prop defaults + an
            # instance_component's swap values) are cross-chunk svg-component refs too —
            # mirror build_figma._swap_refs so the pruning-safety check actually covers them
            # (else a dropped swap ref is a false-clean self-test).
            if op.get("op") == "frame_component":
                for p in op.get("props", []) or []:
                    if p.get("type") == "INSTANCE_SWAP" and p.get("default"):
                        refs.append(p["default"])
            elif op.get("op") == "instance_component":
                _vals = op.get("values") or {}
                for pkey in op.get("swaps", []) or []:
                    if _vals.get(pkey):
                        refs.append(_vals[pkey])
            for fl in op.get("fills", []) or []:
                if fl.get("bind"):
                    refs.append("var:" + fl["bind"])
            for r in op.get("runs", []) or []:
                rf = r.get("fill") or {}
                if rf.get("bind"):
                    refs.append("var:" + rf["bind"])
            for st in op.get("strokes", []) or []:
                sc = st.get("color") or {}
                if sc.get("bind"):
                    refs.append("var:" + sc["bind"])
            for vk in (op.get("bindRefs") or {}).values():
                refs.append(vk)
            if op.get("op") == "variable" and op.get("collection"):
                refs.append(op["collection"])
            for r in refs:
                if r != "__PAGE__" and r not in created and r not in chunk_created:
                    problems.append("chunk %d op %s references unresolved %s"
                                    % (i, op.get("key"), r))
                # Pruning-safety (chunk-budget-fix): a cross-chunk ref MUST be in this
                # chunk's needs, or idmap-pruning drops it and resolveVar/resolveNode
                # fails at runtime (the stroke-bind class the live run caught).
                if r in created and r not in chunk_created and r not in needs_i:
                    problems.append("chunk %d op %s cross-chunk ref %s NOT in needs (pruning would drop it)"
                                    % (i, op.get("key"), r))
        # simulate the executor assigning an id to every created key
        for op in ch["ops"]:
            k = op.get("key")
            if k:
                idmap[k] = "sim:" + k
                created.add(k)
                all_keys.append(k)

    dupes = len(all_keys) - len(set(all_keys))

    # SVG-dedup integrity (dedup follow-on): every `instance` op must reference a
    # `component` master created somewhere in the plan, and a reused svg must collapse
    # (masters < uses). Catches a regression that drops the masters or mis-threads the
    # comp_* keys — the logo-heavy golden makes this assertion meaningful.
    comp_keys, inst_refs = set(), []
    for ch in plan["chunks"]:
        for op in ch["ops"]:
            if op.get("op") == "component" and op.get("key"):
                comp_keys.add(op["key"])
            if op.get("op") == "instance" and op.get("component"):
                inst_refs.append(op["component"])
            # C2: an INSTANCE_SWAP master default and each per-instance swap value must also
            # reference a real svg `component` master (the swap targets are dedup'd svgs).
            if op.get("op") == "frame_component":
                for p in op.get("props", []) or []:
                    if p.get("type") == "INSTANCE_SWAP" and p.get("default"):
                        inst_refs.append(p["default"])
            if op.get("op") == "instance_component":
                _vals = op.get("values") or {}
                for pkey in op.get("swaps", []) or []:
                    if _vals.get(pkey):
                        inst_refs.append(_vals[pkey])
    for cref in inst_refs:
        if cref not in comp_keys:
            problems.append("instance references missing component master: %s" % cref)

    # WS5 component-group integrity (mirrors the SVG dedup-integrity check): every
    # instance_component op must reference a frame_component master created somewhere in
    # the plan. Catches a regression that drops the masters or mis-threads the
    # comp_card_* keys — the cards-component golden makes this assertion meaningful.
    # (Ordering + pruning-safety for the master ref are already covered by the generic
    # op.get("component") checks above, same as SVG instances.)
    fcomp_keys, fcomp_refs = set(), []
    for ch in plan["chunks"]:
        for op in ch["ops"]:
            if op.get("op") == "frame_component" and op.get("key"):
                fcomp_keys.add(op["key"])
            if op.get("op") == "instance_component" and op.get("component"):
                fcomp_refs.append(op["component"])
    for cref in fcomp_refs:
        if cref not in fcomp_keys:
            problems.append("instance_component references missing frame_component master: %s" % cref)

    # Char-budget assertion (chunk-budget-fix): each rendered chunk, with a realistic
    # pruned idmap (only its `needs`), must clear the 50,000-char use_figma cap. This is
    # the regression guard for the logo-heavy page that blocked the live acceptance.
    over_cap = []
    for ch in plan["chunks"]:
        cf = os.path.join(tmp, "chunk_%d.js" % ch["index"])
        if not os.path.isfile(cf):
            continue
        with open(cf, encoding="utf-8") as fh:
            raw = fh.read()
        sim = {k: "12:%07d" % n for n, k in enumerate(ch.get("needs", []))}
        rendered = raw.replace("__IDMAP__", json.dumps(sim, ensure_ascii=False))
        if len(rendered) > USE_FIGMA_HARD_CAP:
            over_cap.append((ch["index"], len(rendered)))

    # WS2 geometry gate: the lost-wrap / over-height-white-space defect class must
    # fail headlessly and geometrically (assert, don't eyeball). assert_geometry lives
    # in build_figma; import it from the same dir the builder was run from.
    geo_problems = []
    try:
        sys.path.insert(0, here)
        import build_figma as _bf
        for ir_path in args.ir:
            _ir = json.load(open(ir_path, encoding="utf-8"))
            # D-05 convergence: apply the builder's own D-03 css-grid/pseudo pre-pass
            # before the geometry gate, so a css-grid page is checked as the builder
            # EMITS it (post-rebuild), not as the raw IR. Without it, studio-index/session
            # false-FAIL the self-test on the pre-rebuild `v:FILL`-in-`v:HUG` circular
            # constraint the grid rebuild resolves; a no-op on every non-grid golden.
            _root = _ir.get("root", {})
            _bf.preprocess_flags(_root)
            for v in _bf.assert_geometry(_root):
                # Only hard geometric contradictions (severity 'error': overflow /
                # white-space) fail the self-test; root guards (severity 'warn') are
                # advisory, surfaced in --summary, and must not break a section-rooted golden.
                if v.get("severity", "error") != "error":
                    continue
                geo_problems.append("%s: [%s] %s — %s"
                                    % (os.path.basename(ir_path), v["kind"], v.get("node", ""), v["detail"]))
    except Exception as e:
        geo_problems.append("geometry check error: %s" % e)

    ok = not problems and dupes == 0 and not over_cap and not geo_problems and st_all_resolved(plan, idmap)
    print("SELF-TEST: %s" % ("PASS" if ok else "FAIL"))
    print("  IRs: %s" % ", ".join(os.path.basename(p) for p in args.ir))
    if manifest_blocked:
        print("  NOTE: build is manifest.blocked — this PASS proves the plumbing only; "
              "the run loop (init) refuses to issue a blocked build to Figma.")
    print("  chunks: %d   keys: %d (unique: %d)   final id map: %d"
          % (len(plan["chunks"]), len(all_keys), len(set(all_keys)), len(idmap)))
    if inst_refs:
        print("  dedup: %d instance use(s) -> %d component master(s)" % (len(inst_refs), len(comp_keys)))
    if fcomp_refs:
        print("  components: %d instance(s) -> %d frame_component master(s)" % (len(fcomp_refs), len(fcomp_keys)))
    if over_cap:
        for i, n in over_cap:
            print("  OVER CAP: chunk %d renders %d chars (> %d)" % (i, n, USE_FIGMA_HARD_CAP))
    else:
        print("  payload: all %d chunk(s) under the %d-char cap" % (len(plan["chunks"]), USE_FIGMA_HARD_CAP))
    if not geo_problems:
        print("  geometry: PASS — no overflow / white-space violations")
    if dupes:
        print("  DUPLICATE KEYS: %d" % dupes)
    for p in (problems + geo_problems)[:20]:
        print("  PROBLEM: %s" % p)
    sys.exit(0 if ok else 1)


def st_all_resolved(plan, idmap):
    for ch in plan["chunks"]:
        for op in ch["ops"]:
            if op.get("key") and op["key"] not in idmap:
                return False
    return True


def main():
    ap = argparse.ArgumentParser(description="HeyHi Design Bridge chunk runner")
    sub = ap.add_subparsers(dest="cmd", required=True)

    for name in ("init", "prep", "record", "status", "report", "assets"):
        sp = sub.add_parser(name)
        sp.add_argument("out_dir")
        if name in ("prep", "record"):
            sp.add_argument("--chunk", type=int, default=None)
        if name == "record":
            sp.add_argument("--result-file", dest="result_file", default=None)
            sp.add_argument("--result", default=None)

    sp = sub.add_parser("self-test")
    sp.add_argument("ir", nargs="+")
    sp.add_argument("--max-nodes", type=int, default=None)

    args = ap.parse_args()
    {
        "init": cmd_init, "prep": cmd_prep, "record": cmd_record,
        "status": cmd_status, "report": cmd_report, "assets": cmd_assets,
        "self-test": cmd_selftest,
    }[args.cmd](args)


if __name__ == "__main__":
    main()
