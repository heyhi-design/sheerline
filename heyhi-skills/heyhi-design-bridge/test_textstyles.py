#!/usr/bin/env python3
"""test_textstyles.py — unit tests for design-bridge packet text-styles-mode (WS3).
No Figma. Covers:
  - compose_type token_ref-aware role naming (token_ref beats the size-rank heuristic)
  - extract_ramp captures token_ref
  - build_figma --type-mode style: set-direct on first paint (NO bindRefs) + a finish
    instruction in --summary; contrasted with --type-mode bind (which DOES bind).

  python3 test_textstyles.py
"""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(HERE, "scripts")
sys.path.insert(0, SCRIPTS)
import compose_type as ct  # noqa: E402

P = F = 0


def ok(cond, msg):
    global P, F
    if cond:
        P += 1; print("  PASS " + msg)
    else:
        F += 1; print("  FAIL " + msg)


# ---- compose_type: token_ref-aware naming ----
print("compose_type — token_ref beats the size-rank heuristic:")
ok(ct.role_from_token_ref("tokens.typography.scale.body-lg") == "Body/Large", "body-lg -> Body/Large")
ok(ct.role_from_token_ref("tokens.typography.scale.display-hero") == "Display/Hero", "display-hero -> Display/Hero")
ok(ct.role_from_token_ref("tokens.typography.scale.h2") == "Heading/Section", "h2 -> Heading/Section (curated)")
ok(ct.role_from_token_ref("tokens.typography.scale.footer-heading") == "Footer/Heading", "unknown tail -> Title-cased Category/Variant")
ok(ct.role_from_token_ref(None) is None and ct.role_from_token_ref("") is None, "no token_ref -> None (heuristic fallback)")

print("compose_type — extract_ramp captures token_ref; suggest_spec uses it for the role name:")
ir = {"root": {"type": "FRAME", "name": "P", "children": [
    {"type": "TEXT", "name": "Lede", "type_style": {"family": "Work Sans", "weight": 400, "size": 19,
        "lineHeight": 1.6, "token_ref": "tokens.typography.scale.body-lg"}},
    {"type": "TEXT", "name": "Copy", "type_style": {"family": "Work Sans", "weight": 400, "size": 16,
        "lineHeight": 1.6, "token_ref": "tokens.typography.scale.body"}},
]}}
ramp = ct.extract_ramp(ir)
ok(all("token_ref" in r for r in ramp), "ramp entries carry token_ref")
spec = ct.suggest_spec(ramp, collection="T")
names = {s["name"] for s in spec["styles"]}
ok("Body/Large" in names and "Body/Default" in names, "two body sizes -> distinct token-named roles (Body/Large, Body/Default)")

print("compose_type — bundled selftest still green (with the new assertions):")
rc = subprocess.run([sys.executable, os.path.join(SCRIPTS, "compose_type.py"), "selftest"],
                    capture_output=True, text=True)
ok(rc.returncode == 0 and "selftest PASS" in rc.stdout, "compose_type.py selftest PASS")
ok("token_ref naming" in rc.stdout, "selftest reports token_ref naming")

# ---- build_figma --type-mode style ----
IR = {
    "$schema": "heyhi-scene-graph/v0.4",
    "meta": {"source": "fixture.html", "breakpoint": "lg", "brand_config": "example", "generated_by": "test"},
    "tokens_used": [],
    "root": {
        "type": "FRAME", "name": "Page",
        "layout": {"mode": "VERTICAL", "itemSpacing": 16},
        "size": {"w": 1200, "h": 400, "sizing": {"h": "FILL", "v": "HUG"}},
        "children": [
            {"type": "TEXT", "name": "Hero", "characters": "Big", "fills": [{"resolved": "#1C1C1C"}],
             "type_style": {"family": "Alfa Slab One", "weight": 400, "size": 76, "lineHeight": 1.02,
                            "token_ref": "tokens.typography.scale.display-hero"},
             "size": {"w": 400, "h": 80, "sizing": {"h": "HUG", "v": "HUG"}}},
            {"type": "TEXT", "name": "Body", "characters": "Text", "fills": [{"resolved": "#1C1C1C"}],
             "type_style": {"family": "Work Sans", "weight": 400, "size": 16, "lineHeight": 1.6,
                            "token_ref": "tokens.typography.scale.body"},
             "size": {"w": 400, "h": 24, "sizing": {"h": "HUG", "v": "HUG"}}},
        ],
    },
}
tmp = tempfile.mkdtemp(prefix="ts-")
irp = os.path.join(tmp, "fixture.lg.ir.json")
json.dump(IR, open(irp, "w"))
bf = os.path.join(SCRIPTS, "build_figma.py")


def text_ops(out_dir):
    plan = json.load(open(os.path.join(out_dir, "plan.json")))
    return [o for ch in plan["chunks"] for o in ch["ops"] if o.get("op") == "text"]


print("build_figma — --type-mode style is accepted and emits a buildable plan:")
style_dir = os.path.join(tmp, "style")
rc = subprocess.run([sys.executable, bf, irp, "--type-mode", "style", "--out-dir", style_dir],
                    capture_output=True, text=True)
ok(rc.returncode == 0, "build succeeds with --type-mode style")
sops = text_ops(style_dir)
named = {o.get("name") for o in sops}
ok("Hero" in named and "Body" in named, "mockup text ops are present in the plan")
ok(all("bindRefs" not in o for o in sops),
   "style mode writes type set-direct (NO bindRefs on any text op — first paint correct)")

print("build_figma — --summary (style) prints the compose_type finish instruction:")
rc = subprocess.run([sys.executable, bf, irp, "--type-mode", "style", "--summary"],
                    capture_output=True, text=True)
ok("FINISH with compose_type.py" in rc.stdout, "summary names the Text-Styles finish")
ok("compose_type.py emit spec.json --root-node" in rc.stdout, "summary gives the emit command")

print("build_figma — contrast: --type-mode bind DOES bind type to Variables:")
bind_dir = os.path.join(tmp, "bind")
rc = subprocess.run([sys.executable, bf, irp, "--type-mode", "bind", "--out-dir", bind_dir],
                    capture_output=True, text=True)
bops = text_ops(bind_dir)
ok(rc.returncode == 0 and any("bindRefs" in o for o in bops),
   "bind mode emits bindRefs (confirms style != bind)")

print("\n" + ("ALL PASS" if F == 0 else "FAILURES") + " — %d passed, %d failed" % (P, F))
sys.exit(0 if F == 0 else 1)
