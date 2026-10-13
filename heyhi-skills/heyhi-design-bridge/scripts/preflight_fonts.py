#!/usr/bin/env python3
"""preflight_fonts.py: HeyHi Design Bridge Translate font preflight (defect I3).

Resolve every font face a scene-graph IR will ask Figma to load, BEFORE the build
runs, against the live Figma catalogue, and fail loudly on any face the catalogue
lacks. The builder (build_figma.py `ensureFont`) falls back silently: a missing
family becomes Inter Regular, a missing style becomes the family's Regular. Those
substitutions render as a broken typeface and the mock transport cannot see them
(the mock's registry disagrees with real Figma in both directions). This preflight
is the check that would have caught the D-09 miss.

The miss it exists for is an INLINE RUN, which a per-node scan cannot see: a
`DM Mono` run that inherits weight 600 from a `Sora` parent resolves to
"DM Mono SemiBold". The parent's own face ("Sora SemiBold") exists, so scanning
node styles alone passes; only expanding each run against its inherited base
surfaces the gap. This tool expands runs (families, weights, italic) exactly the
way the builder does at write time.

Style names come from the builder's own WEIGHT_TO_STYLE table (kept verbatim in
sync with build_figma.py) so the preflight requests precisely what the builder
requests, with no second opinion that could drift.

    usage:
      preflight_fonts.py --available <catalogue.json> <ir.json> [ir.json ...]
      preflight_fonts.py --selftest        # embedded, catalogue-free regression proof

    --available   JSON dump of the target workspace's fonts (see below). Required
                  outside --selftest.
    --json        machine-readable report on stdout instead of the human table.
    --check-generic  also check generic CSS families (system-ui, monospace, ...);
                  off by default because Figma substitutes those by design, not by gap.

Exit status: 0 when every requested face resolves; 1 when any face is unresolvable
(the build would silently substitute it); 2 on a usage/IO error.

--- producing the catalogue (one line, in Figma via use_figma / the plugin console) ---
    figma.listAvailableFontsAsync().then(f => console.log(JSON.stringify(f)))
Save that output to a file and pass it as --available. The dump is an array of
{ fontName: { family, style } }; this tool also accepts a plain [{family, style}]
list or a { fonts: [...] } wrapper.

HeyHi Internal Use Only.
"""

import argparse
import json
import sys
from pathlib import Path

# The builder's own weight -> Figma style-name table. Verbatim from
# build_figma.py (WEIGHT_TO_STYLE / weight_to_style) so this preflight resolves
# exactly what the builder will. If the builder's table changes, change this too.
WEIGHT_TO_STYLE = {
    100: "Thin", 200: "ExtraLight", 300: "Light", 400: "Regular",
    500: "Medium", 600: "SemiBold", 700: "Bold", 800: "ExtraBold", 900: "Black",
}

# CSS generic keywords are not real Figma faces; the builder resolves them by
# substitution as a matter of course, not because the catalogue has a gap. Skipped
# unless --check-generic is passed. Mirrors build-ir's GENERIC_FAMILIES set.
GENERIC_FAMILIES = {
    "serif", "sans-serif", "monospace", "system-ui", "ui-sans-serif",
    "ui-serif", "ui-monospace", "cursive", "fantasy", "inherit", "initial",
    "-apple-system", "blinkmacsystemfont",
}

# The face the builder substitutes to when a family is absent (ensureFont).
FALLBACK_FAMILY = "Inter"


def _die(msg):
    """Exit 2: the preflight could not run (usage or IO). Distinct from exit 1 (ran,
    found unresolvable faces) and exit 0 (ran, all faces resolve)."""
    print(msg, file=sys.stderr)
    sys.exit(2)


def weight_to_style(weight):
    """Verbatim from build_figma.py.weight_to_style."""
    if weight is None:
        return "Regular"
    try:
        w = int(round(float(weight) / 100.0)) * 100
    except (TypeError, ValueError):
        return "Regular"
    w = max(100, min(900, w))
    return WEIGHT_TO_STYLE.get(w, "Regular")


def figma_style_name(weight, italic, base):
    """Mirror build_figma.py.figmaStyleName (the JS run resolver): an explicit
    numeric weight wins; otherwise the run keeps the base style; italic composes on
    top ('Regular'+italic -> 'Italic', else '<name> Italic'). weight_to_style rounds
    with Python round(); the builder's JS run path uses Math.round, so the two agree on
    every real font weight and can differ only at an exact half-hundred (450, 550, ...),
    which standard weights never use."""
    name = base or "Regular"
    if isinstance(weight, (int, float)):
        name = weight_to_style(weight)
    if italic:
        name = "Italic" if name == "Regular" else name + " Italic"
    return name


def load_catalogue(path):
    """Read a listAvailableFontsAsync dump. Returns (pairs, families) where pairs is
    a set of (family, style) and families is a set of family names. Accepts the Figma
    native shape [{fontName:{family,style}}], a plain [{family,style}] list, or a
    {fonts:[...]} wrapper."""
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        _die(f"preflight_fonts: cannot read catalogue {path}: {e}")
    if isinstance(data, dict) and "fonts" in data:
        data = data["fonts"]
    if not isinstance(data, list):
        _die(f"preflight_fonts: catalogue {path} is not a list of fonts")
    pairs, families = set(), set()
    for entry in data:
        if not isinstance(entry, dict):
            continue
        fn = entry.get("fontName") if isinstance(entry.get("fontName"), dict) else entry
        fam = (fn.get("family") or "").strip()
        sty = (fn.get("style") or "").strip()
        if fam:
            families.add(fam)
            if sty:
                pairs.add((fam, sty))
    if not pairs:
        _die(f"preflight_fonts: catalogue {path} named no (family, style) faces")
    return pairs, families


def collect_requests(node, ir_label, parent_name, out):
    """Walk an IR node, appending every font face the build will request. Each item
    is {family, style, source, ir, node, text}. TEXT nodes contribute a base face and
    one face per inline run (families/weights/italic expanded the way the builder
    does), matching build_figma.py's ensureFont call sites."""
    name = node.get("name") or parent_name or "?"
    if node.get("type") == "TEXT":
        ts = node.get("type_style") or {}
        base_family = (ts.get("family") or FALLBACK_FAMILY).strip()
        base_weight = ts.get("weight")
        base_style = weight_to_style(base_weight)
        snippet = (node.get("characters") or "").strip().replace("\n", " ")[:32]
        out.append({"family": base_family, "style": base_style, "source": "base",
                    "ir": ir_label, "node": name, "text": snippet})
        for run in node.get("runs") or []:
            st = run.get("style") or {}
            if not st:
                continue  # a fill-only run requests no new face
            run_family = (st.get("family") or base_family).strip()
            # weight absent on the run -> the run keeps the base style (inheritance);
            # this is the inline-run trap the per-node scan misses.
            run_style = figma_style_name(st.get("weight"), st.get("italic"), base_style)
            out.append({"family": run_family, "style": run_style, "source": "run",
                        "ir": ir_label, "node": name, "text": snippet})
    for child in node.get("children") or []:
        collect_requests(child, ir_label, name, out)
    return out


def classify(requests, pairs, families, check_generic=False):
    """Bucket unique (family, style) requests into resolvable / style-missing /
    family-missing. Returns (results, skipped) where results is an ordered list of
    dicts with verdict + provenance and skipped is the set of generic families not
    checked."""
    seen = {}
    skipped = set()
    order = []
    for req in requests:
        fam, sty = req["family"], req["style"]
        if fam.lower() in GENERIC_FAMILIES and not check_generic:
            skipped.add(fam)
            continue
        key = (fam, sty)
        if key not in seen:
            if key in pairs:
                verdict = "OK"
            elif fam in families:
                verdict = "STYLE_MISSING"
            else:
                verdict = "FAMILY_MISSING"
            seen[key] = {"family": fam, "style": sty, "verdict": verdict,
                         "count": 0, "sources": set(), "example": req}
            order.append(key)
        rec = seen[key]
        rec["count"] += 1
        rec["sources"].add(req["source"])
    return [seen[k] for k in order], skipped


def _fallback_note(rec):
    if rec["verdict"] == "STYLE_MISSING":
        return f'{rec["family"]} exists but "{rec["style"]}" does not -> builder falls back to {rec["family"]} Regular'
    return f'{rec["family"]} absent from the catalogue -> builder falls back to {FALLBACK_FAMILY} Regular'


def report_human(results, skipped, catalogue_size, ir_count):
    fails = [r for r in results if r["verdict"] != "OK"]
    print(f"font preflight: {ir_count} IR(s), {len(results)} unique (family, style) "
          f"requested, catalogue of {catalogue_size} faces")
    for r in results:
        tag = "OK  " if r["verdict"] == "OK" else "FAIL"
        run_marker = " (inline run)" if r["sources"] == {"run"} else \
                     " (run+base)" if "run" in r["sources"] and "base" in r["sources"] else ""
        line = f"  {tag}  {r['family']} {r['style']}{run_marker}  x{r['count']}"
        if r["verdict"] != "OK":
            ex = r["example"]
            line += f"\n         {_fallback_note(r)}\n         first seen: {ex['ir']} :: {ex['node']}"
            if ex["text"]:
                line += f'  "{ex["text"]}"'
        print(line)
    if skipped:
        print(f"  (skipped {len(skipped)} generic families: {', '.join(sorted(skipped))}; pass --check-generic to include)")
    if fails:
        print(f"\nFAIL: {len(fails)} unresolvable face(s). The builder would silently "
              f"substitute these at write time.")
    else:
        print("\nPASS: every requested face resolves in the catalogue.")
    return 1 if fails else 0


def report_json(results, skipped, catalogue_size, ir_count):
    fails = [r for r in results if r["verdict"] != "OK"]
    payload = {
        "ir_count": ir_count,
        "catalogue_size": catalogue_size,
        "unique_faces": len(results),
        "skipped_generic": sorted(skipped),
        "faces": [
            {"family": r["family"], "style": r["style"], "verdict": r["verdict"],
             "count": r["count"], "sources": sorted(r["sources"]),
             "example": {"ir": r["example"]["ir"], "node": r["example"]["node"]}}
            for r in results
        ],
        "unresolvable": [f'{r["family"]} {r["style"]}' for r in fails],
        "ok": not fails,
    }
    print(json.dumps(payload, indent=2))
    return 1 if fails else 0


def run(ir_paths, catalogue_path, as_json=False, check_generic=False):
    pairs, families = load_catalogue(catalogue_path)
    requests = []
    for p in ir_paths:
        try:
            ir = json.loads(Path(p).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            _die(f"preflight_fonts: cannot read IR {p}: {e}")
        root = ir.get("root", ir)
        collect_requests(root, Path(p).name, None, requests)
    results, skipped = classify(requests, pairs, families, check_generic)
    reporter = report_json if as_json else report_human
    return reporter(results, skipped, len(pairs), len(ir_paths))


# --- embedded regression proof (batch rule 6: the check must be shown able to fail) ---
# A real Figma catalogue that carries the two documented gaps: Sora has no Medium
# (studio.css imports Sora 500), and DM Mono has no SemiBold (it ships 400/500 only,
# but an inline run inherits weight 600 -> "DM Mono SemiBold").
_SELFTEST_CATALOGUE = [
    {"fontName": {"family": "Sora", "style": s}} for s in
    ["Thin", "ExtraLight", "Light", "Regular", "SemiBold", "Bold", "ExtraBold"]
] + [
    {"fontName": {"family": "Lora", "style": s}} for s in ["Regular", "Medium", "SemiBold", "Italic"]
] + [
    {"fontName": {"family": "DM Mono", "style": s}} for s in ["Light", "Regular", "Medium"]
] + [
    {"fontName": {"family": "Inter", "style": s}} for s in ["Regular", "Medium", "SemiBold", "Bold"]
]

# fixture A: a node that asks for Sora 500 -> "Sora Medium" (a node-level miss).
_FIXTURE_SORA_MEDIUM = {"root": {"type": "FRAME", "name": "A", "children": [
    {"type": "TEXT", "name": ".nav-label", "characters": "Areas",
     "type_style": {"family": "Sora", "weight": 500}},
]}}

# fixture B: base Sora 600 ("Sora SemiBold", which EXISTS) with a DM Mono run that
# inherits that 600 -> "DM Mono SemiBold" (which does not). The base resolves fine;
# only expanding the run finds the gap. This is the D-09 miss in miniature.
_FIXTURE_INLINE_RUN = {"root": {"type": "FRAME", "name": "B", "children": [
    {"type": "TEXT", "name": ".session-line", "characters": "session live · SESS-01",
     "type_style": {"family": "Sora", "weight": 600},
     "runs": [{"start": 15, "end": 22, "style": {"family": "DM Mono"}}]},
]}}

# fixture C: an all-resolvable control (Lora 500 -> "Lora Medium", which exists) so
# the selftest also proves the instrument can PASS, not only fail.
_FIXTURE_GOOD = {"root": {"type": "FRAME", "name": "C", "children": [
    {"type": "TEXT", "name": ".body", "characters": "A paragraph.",
     "type_style": {"family": "Lora", "weight": 500}},
]}}


def selftest():
    pairs, families = _catalogue_sets(_SELFTEST_CATALOGUE)

    def faces(fixture):
        reqs = collect_requests(fixture["root"], "selftest", None, [])
        results, _ = classify(reqs, pairs, families)
        return {(r["family"], r["style"]): r["verdict"] for r in results}

    ok = True

    a = faces(_FIXTURE_SORA_MEDIUM)
    cond = a.get(("Sora", "Medium")) == "STYLE_MISSING"
    print(f"  [{'PASS' if cond else 'FAIL'}] fixture A: Sora 500 -> 'Sora Medium' flagged STYLE_MISSING")
    ok &= cond

    b = faces(_FIXTURE_INLINE_RUN)
    cond_run = b.get(("DM Mono", "SemiBold")) == "STYLE_MISSING"
    cond_base = b.get(("Sora", "SemiBold")) == "OK"
    print(f"  [{'PASS' if cond_run else 'FAIL'}] fixture B: inline DM Mono run inheriting 600 -> 'DM Mono SemiBold' flagged")
    print(f"  [{'PASS' if cond_base else 'FAIL'}] fixture B: base 'Sora SemiBold' resolves OK (a per-node scan would pass; the run is the only gap)")
    ok &= cond_run and cond_base

    c = faces(_FIXTURE_GOOD)
    cond = c.get(("Lora", "Medium")) == "OK" and all(v == "OK" for v in c.values())
    print(f"  [{'PASS' if cond else 'FAIL'}] fixture C: all-resolvable IR reports no failure (instrument can pass, not only fail)")
    ok &= cond

    print("selftest: PASS. The preflight fires on both the node-level and the inline-run gap, and clears a good IR."
          if ok else "selftest: FAIL. The detector did not behave as specified.")
    return 0 if ok else 1


def _catalogue_sets(entries):
    pairs, families = set(), set()
    for e in entries:
        fn = e.get("fontName", e)
        fam, sty = fn.get("family", "").strip(), fn.get("style", "").strip()
        if fam:
            families.add(fam)
            if sty:
                pairs.add((fam, sty))
    return pairs, families


def main(argv=None):
    ap = argparse.ArgumentParser(description="Translate font preflight (I3): resolve every "
                                 "requested Figma face against the live catalogue; fail on any gap.")
    ap.add_argument("irs", nargs="*", help="scene-graph IR json file(s)")
    ap.add_argument("--available", help="listAvailableFontsAsync() JSON dump (the target catalogue)")
    ap.add_argument("--json", action="store_true", help="machine-readable report")
    ap.add_argument("--check-generic", action="store_true", help="also check generic CSS families")
    ap.add_argument("--selftest", action="store_true", help="run the embedded regression proof")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()
    if not args.available:
        ap.error("--available <catalogue.json> is required (or use --selftest)")
    if not args.irs:
        ap.error("at least one IR file is required")
    return run(args.irs, args.available, as_json=args.json, check_generic=args.check_generic)


if __name__ == "__main__":
    sys.exit(main())
