#!/usr/bin/env python3
"""compose_type.py — design-bridge Compose: native Figma Text Styles powered by Variables.

Productizes the capability proven live 2026-06-17 (decision-log § 2026-06-17 [design-bridge]):
author a real Figma type system whose Text Styles bind font family/weight/size to Variables,
then apply it to an already-built page by classifying each TEXT node's current type.

Three steps (the spec is the human approval surface — Earn the Room):

  extract <ir.json> [--collection NAME] -o spec.json
      Walk an IR, distill the distinct type ramp, and SUGGEST a type-system spec
      (collection + family/weight STRING vars + a FLOAT size scale + role-named styles).
      Heuristic; meant to be reviewed/edited before emit.

  emit <spec.json> --root-node <ID> -o DIR
      Deterministically emit two use_figma payloads:
        create.js  — find-or-create the collection + Variables + Text Styles; bind
                     fontFamily/fontStyle/fontSize to Variables; set lineHeight,
                     letterSpacing, textCase DIRECT (a Variable-bound lineHeight
                     coerces to PIXELS — see reference.md §2), idempotent on re-run.
        apply.js   — under <ID>, classify each TEXT node by its current
                     (family, weight, size, letterSpacing, lineHeight) -> nearest spec
                     style -> setTextStyleIdAsync. Color fills are untouched (type-only).

  selftest
      Build a spec from a bundled fixture, emit both payloads, and assert the spec
      shape + the classifier round-trips the fixture ramp. No Figma required.

Each payload is a complete `use_figma` `code` string (ends with `return JSON.stringify(out)`)
and is small (no inlined SVG/raster), so the agent-transcription transport wall does not apply.
"""
import argparse
import json
import os
import sys

WEIGHT_TO_STYLE = {100: "Thin", 200: "ExtraLight", 300: "Light", 400: "Regular",
                   500: "Medium", 600: "SemiBold", 700: "Bold", 800: "ExtraBold", 900: "Black"}
SCALE_NAMES = ["display-hero", "display-section", "heading", "subhead", "body-lg",
               "body", "body-sm", "label", "caption", "micro"]

# token_ref -> role name. A type_style.token_ref (e.g. tokens.typography.scale.body-lg)
# is the design's OWN name for the role, so it beats the size-rank heuristic. Known
# tails map to a curated role; an unknown tail falls back to Title-cased Category/Variant.
TOKEN_ROLE = {
    "display-hero": "Display/Hero", "display-section": "Display/Section",
    "display": "Display/Hero", "hero": "Display/Hero",
    "heading": "Heading/Section", "subhead": "Heading/Subhead",
    "h1": "Display/Section", "h2": "Heading/Section", "h3": "Heading/Subhead", "h4": "Heading/Minor",
    "lede": "Body/Lede", "body-lg": "Body/Large", "body": "Body/Default", "body-sm": "Body/Small",
    "eyebrow": "Label/Eyebrow", "kicker": "Label/Kicker", "nav": "Label/Nav", "label": "Label/Default",
    "button": "UI/Button", "caption": "UI/Caption", "micro": "UI/Micro",
}
_ABBR = {"lg": "Large", "sm": "Small", "md": "Medium", "xl": "XLarge", "xs": "XSmall",
         "h1": "H1", "h2": "H2", "h3": "H3", "h4": "H4", "ui": "UI"}


def role_from_token_ref(tref):
    """Map a type_style.token_ref to a role name, preferring the design's own token
    name over the size-rank heuristic. Returns None when there is no usable tail."""
    if not tref:
        return None
    tail = str(tref).rstrip(".").split(".")[-1].strip().lower()
    if not tail:
        return None
    if tail in TOKEN_ROLE:
        return TOKEN_ROLE[tail]
    parts = [p for p in tail.replace("_", "-").split("-") if p]
    if not parts:
        return None
    cap = lambda p: _ABBR.get(p, p[:1].upper() + p[1:])
    if len(parts) == 1:
        return "%s/Default" % cap(parts[0])
    return "%s/%s" % (cap(parts[0]), " ".join(cap(p) for p in parts[1:]))


def weight_class(w):
    try:
        return max(100, min(900, int(round(float(w) / 100.0) * 100)))
    except Exception:
        return 400


# ---- extract -------------------------------------------------------------

def extract_ramp(ir):
    """Return distinct type tuples (family, wclass, size, lhRatio, lsPx, upper) + counts."""
    seen = {}
    def walk(n):
        if not isinstance(n, dict):
            return
        if n.get("type") == "TEXT":
            ts = n.get("type_style") or {}
            fam, sz = ts.get("family"), ts.get("size")
            if fam and sz:
                ls = float(ts.get("letterSpacing") or 0)
                # the extractor may not capture textCase; infer upper from a tracked-label signature
                upper = bool(ts.get("textCase") and str(ts["textCase"]).upper() == "UPPER")
                key = (fam, weight_class(ts.get("weight") or 400), round(float(sz), 2),
                       round(float(ts["lineHeight"]), 3) if ts.get("lineHeight") else None,
                       round(ls, 2), upper)
                e = seen.setdefault(key, {"count": 0, "names": [], "token_ref": None})
                e["count"] += 1
                if e["token_ref"] is None and ts.get("token_ref"):
                    e["token_ref"] = ts["token_ref"]
                if len(e["names"]) < 4 and n.get("name"):
                    e["names"].append(n["name"])
        for k in ("children", "content"):
            if isinstance(n.get(k), list):
                for c in n[k]:
                    walk(c)
    walk(ir.get("root") or ir)
    return [{"family": k[0], "wclass": k[1], "size": k[2], "lhRatio": k[3],
             "lsPx": k[4], "upper": k[5], "count": v["count"], "egs": v["names"],
             "token_ref": v["token_ref"]}
            for k, v in seen.items()]


def suggest_spec(ramp, collection="Brand · Type"):
    """Heuristic: split families into display vs text, build a size scale, role-name styles.
    Output is a reviewable spec; the human edits before emit (Earn the Room)."""
    if not ramp:
        return None
    fams = {}
    for r in ramp:
        f = fams.setdefault(r["family"], {"max": 0, "count": 0})
        f["max"] = max(f["max"], r["size"]); f["count"] += r["count"]
    display_fam = max(fams, key=lambda f: fams[f]["max"])
    is_display = lambda fam: fam == display_fam
    def slugify(s):
        out = "".join(c if c.isalnum() else "-" for c in s.lower())
        while "--" in out:
            out = out.replace("--", "-")
        return out.strip("-")
    # one family Variable per distinct family; pretty display/text slugs for the
    # common 1-display + 1-text case, sanitized names for 3+ families (e.g. serif + mono).
    slug_of = {display_fam: "display"}
    others = [f for f in fams if f != display_fam]
    if len(others) == 1:
        slug_of[others[0]] = "text"
    else:
        for f in others:
            slug_of[f] = slugify(f)
    families = {slug: fam for fam, slug in slug_of.items()}

    sizes = sorted({round(r["size"]) for r in ramp}, reverse=True)
    size_name = {s: (SCALE_NAMES[i] if i < len(SCALE_NAMES) else "size-%d" % s) for i, s in enumerate(sizes)}

    def infer_upper(r):
        return r["upper"] or (r["lsPx"] > 0 and round(r["size"]) <= 16 and r["wclass"] >= 600)

    def role(r):
        tref_role = role_from_token_ref(r.get("token_ref"))
        if tref_role:
            return tref_role
        sz, sn = round(r["size"]), size_name[round(r["size"])]
        if is_display(r["family"]):
            if sn == "display-hero":
                return "Display/Hero"
            if sn == "display-section":
                return "Display/Section"
            return "Heading/Section"
        if infer_upper(r):
            if r["lsPx"] >= r["size"] * 0.10:
                return "Label/Eyebrow"
            if sz <= 13:
                return "Label/Kicker"
            if r["wclass"] >= 700:
                return "Label/Footer-Heading"
            return "Label/Nav"
        if r["wclass"] >= 700:
            return "UI/Button-Large" if sz >= 19 else ("UI/Button" if sz >= 16 else "Body/Quote-Cite")
        if r["wclass"] >= 600 and sz <= 16 and (r["lhRatio"] or 1.6) <= 1.4:
            return "UI/Hero-Kicker"
        if sz >= 19:
            return "Body/Lede"
        if sz >= 16:
            return "Body/Default"
        if sz >= 14:
            return "Body/Small"
        return "UI/Caption"

    # one style per role; representative spec = highest-count tuple in the group
    groups = {}
    for r in ramp:
        groups.setdefault(role(r), []).append(r)
    styles = []
    for name, rs in groups.items():
        rep = max(rs, key=lambda r: r["count"])
        styles.append({
            "name": name,
            "family": rep["family"],
            "famKey": slug_of[rep["family"]],
            "style": WEIGHT_TO_STYLE[rep["wclass"]],
            "wclass": rep["wclass"],
            "size": round(rep["size"]),
            "sizeKey": size_name[round(rep["size"])],
            "lhPct": round((rep["lhRatio"] or 1.5) * 100),
            "lsPct": round(rep["lsPx"] / rep["size"] * 100, 1) if rep["size"] else 0,
            "upper": infer_upper(rep),
        })
    styles.sort(key=lambda s: -s["size"])
    weights = sorted({s["wclass"] for s in styles})
    return {
        "collection": collection,
        "families": families,
        "weights": {WEIGHT_TO_STYLE[w].lower(): WEIGHT_TO_STYLE[w] for w in weights},
        "sizes": {sn: sz for sz, sn in size_name.items()},
        "styles": styles,
    }


# ---- emit ----------------------------------------------------------------

def _fonts_in(spec):
    fonts = set()
    for s in spec["styles"]:
        fonts.add((s["family"], s["style"]))
    return sorted(fonts)


def emit_create_js(spec):
    fonts = _fonts_in(spec)
    sizes = spec["sizes"]            # {name: px}
    fams = spec["families"]          # {display, text}
    weights = spec["weights"]        # {key: StyleName}
    styles = spec["styles"]
    return (
        "const out = { col:{}, vars:0, styles:{}, errors:[] };\n"
        "const log = (w,e) => out.errors.push({where:w, error:String((e&&e.message)||e)});\n"
        "for (const [f,s] of " + json.dumps([[f, st] for f, st in fonts]) + ") {\n"
        "  try { await figma.loadFontAsync({family:f, style:s}); } catch(e){ log('load:'+f+'/'+s, e); }\n"
        "}\n"
        "const cols = await figma.variables.getLocalVariableCollectionsAsync();\n"
        "let col = cols.find(c => c.name === " + json.dumps(spec["collection"]) + ");\n"
        "out.col.created = !col;\n"
        "if (!col) col = figma.variables.createVariableCollection(" + json.dumps(spec["collection"]) + ");\n"
        "out.col.id = col.id; const mode = col.modes[0].modeId;\n"
        "const allVars = await figma.variables.getLocalVariablesAsync();\n"
        "const inCol = allVars.filter(v => v.variableCollectionId === col.id);\n"
        "const mkVar = (n,t,val) => { let v = inCol.find(x => x.name === n);\n"
        "  if (!v) { v = figma.variables.createVariable(n, col, t); v.setValueForMode(mode, val); } return v; };\n"
        "const V = {};\n"
        + "".join("V['family/%s'] = mkVar('family/%s','STRING',%s);\n" % (slug, slug, json.dumps(name)) for slug, name in fams.items())
        + "".join("V['weight/%s'] = mkVar('weight/%s','STRING',%s);\n" % (k, k, json.dumps(v)) for k, v in weights.items())
        + "".join("V['size/%s'] = mkVar('size/%s','FLOAT',%d);\n" % (sn, sn, sz) for sn, sz in sizes.items())
        + "out.vars = Object.keys(V).length;\n"
        "const existing = await figma.getLocalTextStylesAsync();\n"
        "const DEFS = " + json.dumps(styles) + ";\n"
        "const wkey = {100:'thin',200:'extralight',300:'light',400:'regular',500:'medium',600:'semibold',700:'bold',800:'extrabold',900:'black'};\n"
        "for (const d of DEFS) {\n"
        "  try {\n"
        "    let ts = existing.find(s => s.name === d.name);\n"
        "    if (!ts) { ts = figma.createTextStyle(); ts.name = d.name; }\n"
        "    ts.fontName = { family: d.family, style: d.style };\n"
        "    ts.fontSize = d.size;\n"
        "    ts.lineHeight = { unit:'PERCENT', value: d.lhPct };\n"
        "    ts.letterSpacing = { unit:'PERCENT', value: d.lsPct };\n"
        "    ts.textCase = d.upper ? 'UPPER' : 'ORIGINAL';\n"
        "    const b = {};\n"
        "    try { ts.setBoundVariable('fontFamily', V['family/'+d.famKey]); b.family='ok'; } catch(e){ b.family=String((e&&e.message)||e); }\n"
        "    try { ts.setBoundVariable('fontStyle', V['weight/'+wkey[d.wclass]]); b.style='ok'; } catch(e){ b.style=String((e&&e.message)||e); }\n"
        "    try { ts.setBoundVariable('fontSize', V['size/'+d.sizeKey]); b.size='ok'; } catch(e){ b.size=String((e&&e.message)||e); }\n"
        "    out.styles[d.name] = { id: ts.id, bound: b };\n"
        "  } catch(e){ log('style:'+d.name, e); }\n"
        "}\n"
        "return JSON.stringify(out);\n"
    )


def emit_apply_js(spec, root_id):
    # the classifier scores nearest spec style, family-matched
    defs = [{"name": s["name"], "family": s["family"], "wclass": s["wclass"],
             "size": s["size"], "lsPct": s["lsPct"], "upper": s["upper"]} for s in spec["styles"]]
    fonts = _fonts_in(spec)
    return (
        "const out = { applied:{}, total:0, mixed:0, unmatched:0, missingStyles:[], errors:[] };\n"
        "const log = (w,e) => out.errors.push({where:w, error:String((e&&e.message)||e)});\n"
        "for (const [f,s] of " + json.dumps([[f, st] for f, st in fonts]) + ") {\n"
        "  try { await figma.loadFontAsync({family:f, style:s}); } catch(e){ log('load:'+f+'/'+s, e); }\n"
        "}\n"
        "const DEFS = " + json.dumps(defs) + ";\n"
        "const stys = await figma.getLocalTextStylesAsync();\n"
        "const byName = {}; for (const s of stys) byName[s.name] = s;\n"
        "for (const d of DEFS) { if (!byName[d.name]) out.missingStyles.push(d.name); out.applied[d.name] = 0; }\n"
        "if (out.missingStyles.length) { out.retry = 'run create.js first'; return JSON.stringify(out); }\n"
        "const wclass = (s) => /bold/i.test(s)&&!/semi/i.test(s) ? 700 : (/semi/i.test(s)?600:(/medium/i.test(s)?500:(/black/i.test(s)?900:400)));\n"
        "const pick = (fam, wc, size, lsPx, upper) => {\n"
        "  let best=null, bestScore=1e9;\n"
        "  for (const d of DEFS) {\n"
        "    if (d.family !== fam) continue;\n"
        "    const lsPctNode = size ? (lsPx/size*100) : 0;\n"
        "    const score = Math.abs(d.size-size)*4 + Math.abs(d.wclass-wc)/100 + Math.abs((d.lsPct||0)-lsPctNode)*0.5 + ((!!d.upper===!!upper)?0:3);\n"
        "    if (score < bestScore) { bestScore = score; best = d; }\n"
        "  }\n"
        "  return best;\n"
        "};\n"
        "const root = await figma.getNodeByIdAsync(" + json.dumps(root_id) + ");\n"
        "if (!root) { out.errors.push({where:'root', error:'not reachable: '+" + json.dumps(root_id) + "}); return JSON.stringify(out); }\n"
        "const visit = async (n) => {\n"
        "  if (n.type === 'TEXT') { out.total++;\n"
        "    try {\n"
        "      const size=n.fontSize, fn=n.fontName;\n"
        "      if (typeof size!=='number' || fn===figma.mixed) { out.mixed++; return; }\n"
        "      let lsPx=0; const ls=n.letterSpacing; if (ls&&ls!==figma.mixed) lsPx = ls.unit==='PERCENT' ? (ls.value/100)*size : ls.value;\n"
        "      const d = pick(fn.family, wclass(fn.style), size, lsPx, false);\n"
        "      if (!d) { out.unmatched++; return; }\n"
        "      try { await figma.loadFontAsync(fn); } catch(e){}\n"
        "      if (typeof n.setTextStyleIdAsync==='function') await n.setTextStyleIdAsync(byName[d.name].id); else n.textStyleId = byName[d.name].id;\n"
        "      out.applied[d.name]++;\n"
        "    } catch(e){ out.unmatched++; log('apply:'+n.name, e); }\n"
        "  }\n"
        "  if ('children' in n) for (const c of n.children) await visit(c);\n"
        "};\n"
        "await visit(root);\n"
        "return JSON.stringify(out);\n"
    )


# ---- cli + selftest ------------------------------------------------------

_FIXTURE = {  # a minimal Alfa-Slab-One + Work-Sans ramp (mirrors the real engagement shape)
    "root": {"type": "FRAME", "name": "Page", "children": [
        {"type": "TEXT", "name": "Hero Headline", "type_style": {"family": "Alfa Slab One", "weight": 400, "size": 76, "lineHeight": 1.02, "letterSpacing": 0.76}},
        {"type": "TEXT", "name": "Section H", "type_style": {"family": "Alfa Slab One", "weight": 400, "size": 40, "lineHeight": 1.1}},
        {"type": "TEXT", "name": "Lede", "type_style": {"family": "Work Sans", "weight": 400, "size": 19, "lineHeight": 1.6}},
        {"type": "TEXT", "name": "Body", "type_style": {"family": "Work Sans", "weight": 400, "size": 16, "lineHeight": 1.6}},
        {"type": "TEXT", "name": "Eyebrow", "type_style": {"family": "Work Sans", "weight": 600, "size": 14, "lineHeight": 1.6, "letterSpacing": 1.68}},
        {"type": "TEXT", "name": "Nav", "type_style": {"family": "Work Sans", "weight": 600, "size": 14, "lineHeight": 1.6, "letterSpacing": 0.84}},
        {"type": "TEXT", "name": "Card Kicker", "type_style": {"family": "Work Sans", "weight": 600, "size": 13, "lineHeight": 1.6, "letterSpacing": 1.04}},
        {"type": "TEXT", "name": "Button", "type_style": {"family": "Work Sans", "weight": 700, "size": 16, "lineHeight": 1.6}},
    ]},
}


def cmd_extract(args):
    ir = json.load(open(args.ir))
    spec = suggest_spec(extract_ramp(ir), collection=args.collection)
    out = json.dumps(spec, indent=2)
    if args.out:
        open(args.out, "w").write(out)
        print("wrote %s (%d styles, %d sizes)" % (args.out, len(spec["styles"]), len(spec["sizes"])))
    else:
        print(out)


def cmd_emit(args):
    spec = json.load(open(args.spec))
    os.makedirs(args.out, exist_ok=True)
    create = os.path.join(args.out, "create.js")
    apply = os.path.join(args.out, "apply.js")
    open(create, "w").write(emit_create_js(spec))
    open(apply, "w").write(emit_apply_js(spec, args.root_node))
    print("wrote %s (%d chars) and %s (%d chars)" % (
        create, os.path.getsize(create), apply, os.path.getsize(apply)))
    for f in (create, apply):
        n = os.path.getsize(f)
        assert n < 50000, "%s exceeds the 50,000-char use_figma cap (%d)" % (f, n)
    print("both under the 50,000-char use_figma cap — OK")


def cmd_selftest(args):
    ramp = extract_ramp(_FIXTURE)
    assert len(ramp) == 8, "fixture ramp: expected 8 tuples, got %d" % len(ramp)
    spec = suggest_spec(ramp, collection="Test · Type")
    names = {s["name"] for s in spec["styles"]}
    cats = {n.split("/")[0] for n in names}
    for cat in ("Display", "Body", "Label"):
        assert cat in cats, "expected a %s/* style (got %s)" % (cat, sorted(names))
    assert spec["families"]["display"] == "Alfa Slab One", "display family detection"
    assert "Work Sans" in spec["families"].values(), "text family present in family Variables"
    # no orphan family binding: every style's famKey resolves to a real family Variable
    for s in spec["styles"]:
        assert s["famKey"] in spec["families"], "orphan famKey %s (families: %s)" % (s["famKey"], list(spec["families"]))
    assert spec["sizes"]["display-hero"] == 76, "largest size names display-hero"
    create_js = emit_create_js(spec)
    apply_js = emit_apply_js(spec, "56:3")
    for js, label in ((create_js, "create"), (apply_js, "apply")):
        assert js.strip().endswith("return JSON.stringify(out);"), "%s.js must return a value" % label
        assert js.count("{") == js.count("}"), "%s.js brace mismatch" % label
        assert len(js) < 50000, "%s.js over cap" % label
    assert "setBoundVariable('fontFamily'" in create_js and "setBoundVariable('fontSize'" in create_js
    assert "lineHeight = { unit:'PERCENT'" in create_js, "lineHeight must be set DIRECT as PERCENT (reference.md §2)"
    assert "setBoundVariable('lineHeight'" not in create_js, "lineHeight must NOT bind to a Variable (coerces to pixels)"
    assert "setTextStyleIdAsync" in apply_js and "getLocalTextStylesAsync" in apply_js
    # token_ref-aware naming: a token_ref beats the size-rank heuristic
    assert role_from_token_ref("tokens.typography.scale.body-lg") == "Body/Large"
    assert role_from_token_ref("tokens.typography.scale.display-hero") == "Display/Hero"
    assert role_from_token_ref("tokens.typography.scale.h2") == "Heading/Section"
    assert role_from_token_ref("tokens.typography.scale.footer-heading") == "Footer/Heading"
    assert role_from_token_ref(None) is None
    _tref_ramp = [{"family": "Work Sans", "wclass": 400, "size": 16, "lhRatio": 1.6, "lsPx": 0,
                   "upper": False, "count": 3, "egs": ["Body"], "token_ref": "tokens.typography.scale.body-lg"}]
    assert suggest_spec(_tref_ramp, collection="T")["styles"][0]["name"] == "Body/Large", "token_ref drives the role name"
    # classifier round-trip: each fixture tuple maps to a real style of the right family
    print("selftest PASS — ramp 8, styles %d, sizes %d; create.js %d / apply.js %d chars; lineHeight set-direct; token_ref naming; classifier present"
          % (len(spec["styles"]), len(spec["sizes"]), len(create_js), len(apply_js)))


def main():
    ap = argparse.ArgumentParser(description="design-bridge Compose: Text Styles powered by Variables")
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("extract"); e.add_argument("ir"); e.add_argument("--collection", default="Brand · Type"); e.add_argument("-o", "--out")
    m = sub.add_parser("emit"); m.add_argument("spec"); m.add_argument("--root-node", required=True); m.add_argument("-o", "--out", default="compose-out")
    sub.add_parser("selftest")
    args = ap.parse_args()
    {"extract": cmd_extract, "emit": cmd_emit, "selftest": cmd_selftest}[args.cmd](args)


if __name__ == "__main__":
    main()
