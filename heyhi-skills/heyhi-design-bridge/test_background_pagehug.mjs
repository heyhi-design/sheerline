// test_background_pagehug.mjs — unit tests for the background-and-pagehug packet
// (WS-A backgrounds + WS-B page-hug; no Playwright, no Figma). Exercises the
// Node-side IR logic + the Python op-builder + the severity-tiered geometry gate:
//   WS-A — a section that inherits the body background (own bg transparent) emits NO
//          fills; the builder op carries no fills, so doFrame sets fills=[] (the painted
//          page shows through), never Figma's default white. A section with its own bg
//          is painted. An unpainted document body raises a root-background-unresolved flag.
//   WS-B — the document body is forced to a hugging VERTICAL stack (mode=VERTICAL,
//          sizing.v=HUG, h=null) even when it would otherwise be a GROUP (abs child),
//          so the footer cannot float below a stale fixed height.
//   Gate — assert_geometry returns severity-tiered findings: a compliant page is clean;
//          a NONE/unpainted root yields advisory 'warn' root guards (not self-test-fatal).
//
//   node test_background_pagehug.mjs
//
// buildIR is imported from the staged packet copy (deployed skill untouched).
// The rich() factory follows test_wrap.mjs.

import { buildIR } from "./scripts/extract_scene_graph/lib/build-ir.mjs";
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";

let pass = 0, fail = 0;
function ok(cond, msg) { if (cond) { pass++; console.log("  PASS " + msg); } else { fail++; console.log("  FAIL " + msg); } }

const here = dirname(fileURLToPath(import.meta.url));
const brandMap = { lookupVar: () => null, nearestColor: () => null, nearestSpacing: () => null };

function rich(over = {}) {
  const c = {
    display: "block", position: "static", overflowX: "visible", overflowY: "visible",
    flexDirection: "row", justifyContent: "flex-start", alignItems: "normal", alignContent: "normal", flexWrap: "nowrap",
    rowGap: "0px", columnGap: "0px", gridTemplateColumns: "none", transform: "none", boxShadow: "none",
    borderTopWidth: "0px", borderRightWidth: "0px", borderBottomWidth: "0px", borderLeftWidth: "0px",
    borderTopStyle: "none", borderTopColor: "rgba(0, 0, 0, 0)",
    borderTopLeftRadius: "0px", borderTopRightRadius: "0px", borderBottomRightRadius: "0px", borderBottomLeftRadius: "0px",
    opacity: "1", animationName: "none", transitionDuration: "0s",
    backgroundColor: "rgba(0, 0, 0, 0)", backgroundImage: "none", backgroundSize: "auto", color: "rgb(0, 0, 0)",
    fontFamily: "Inter", fontWeight: "400", fontSize: "16px", lineHeight: "normal", letterSpacing: "normal",
    paddingTop: "0px", paddingRight: "0px", paddingBottom: "0px", paddingLeft: "0px",
    ...(over.computed || {}),
  };
  return {
    tag: over.tag || "div", id: over.id || null, classes: over.classes || [], dataAudit: null,
    bbox: over.bbox || { x: 0, y: 0, w: 100, h: 20 }, computed: c,
    declared: { color: null, backgroundColor: null, fontSize: null, padding: null, gap: null, borderColor: null, animation: null },
    pseudo: { before: null, after: null },
    font: { family: "Inter", generic: false, brand: true, loaded: true },
    svgOuter: over.svgOuter || null, imgSrc: over.imgSrc || null, text: over.text || null,
    isFlexOrGrid: false, hasAbsChild: over.hasAbsChild || false, children: over.children || [],
  };
}

const meta = { viewport: { w: 1440, h: 2000 }, rootSelector: "body", fontsReady: "loaded", ruleCount: 0 };
const flagsOf = (ir, feature) => (ir.root.flags || []).filter((f) => f.feature === feature);

function txt(label, w = 400, h = 24) {
  return rich({ tag: "p", text: label, bbox: { x: 0, y: 0, w, h }, computed: { display: "block" } });
}
// A section; bg null => inherits the body background (computed stays transparent).
function section(cls, bg, label, h = 300) {
  return rich({
    tag: "section", classes: [cls], bbox: { x: 0, y: 0, w: 1440, h },
    computed: { display: "block", paddingTop: "96px", paddingBottom: "96px", ...(bg ? { backgroundColor: bg } : {}) },
    children: [txt(label)],
  });
}

// ---- GOLDEN: a painted body with a painted hero, a TRANSPARENT (inheriting) section, a painted footer ----
const bodyCapture = {
  meta,
  root: rich({
    tag: "body", bbox: { x: 0, y: 0, w: 1440, h: 2000 },
    computed: { display: "block", backgroundColor: "rgb(246, 244, 238)" }, // painted page base
    children: [
      section("hero", "rgb(18, 26, 21)", "Clear the wild", 666),  // own dark bg -> painted
      section("services", null, "Services", 904),                  // transparent -> inherits page
      section("footer", "rgb(18, 26, 21)", "Footer", 300),         // own dark bg -> painted
    ],
  }),
};
const { ir } = buildIR(bodyCapture, brandMap, { source: "prototypes/inherited-bg.html", breakpoint: "lg", brandConfig: "example" });
const hero = ir.root.children[0];
const services = ir.root.children[1];

console.log("WS-B — the document body is forced to a hugging VERTICAL stack:");
ok(ir.root.layout.mode === "VERTICAL", "root.layout.mode === VERTICAL");
ok(ir.root.size.sizing.v === "HUG", "root.size.sizing.v === HUG");
ok(ir.root.size.h === null, "root.size.h === null (hugs content; footer cannot float below a stale height)");

console.log("WS-A — a painted body + painted section carry fills; a transparent section does not:");
ok(Array.isArray(ir.root.fills) && ir.root.fills.length > 0, "root (body) is painted (has fills)");
ok(Array.isArray(hero.fills) && hero.fills.length > 0, "hero section with own bg is painted (has fills)");
ok(!("fills" in services), "transparent 'services' section has NO fills key (inherits — builder will set fills=[])");
ok(flagsOf(ir, "root-background-unresolved").length === 0, "painted body -> no root-background-unresolved flag");

// ---- a body with NO background raises the root-background-unresolved flag ----
const { ir: bareBody } = buildIR({
  meta, root: rich({
    tag: "body", bbox: { x: 0, y: 0, w: 1440, h: 1200 }, computed: { display: "block" }, // transparent body
    children: [section("services", null, "Services")],
  }),
}, brandMap, { source: "x", breakpoint: "lg", brandConfig: "example" });
console.log("WS-A — an unpainted body is flagged (page would render white behind inheriting sections):");
ok(flagsOf(bareBody, "root-background-unresolved").length === 1, "transparent body -> root-background-unresolved flag (needs human)");
ok(bareBody.root.layout.mode === "VERTICAL" && bareBody.root.size.sizing.v === "HUG", "bare body still forced VERTICAL + HUG");

// ---- a body with an absolutely-positioned child still hugs VERTICAL (not a NONE GROUP) ----
const { ir: absBody } = buildIR({
  meta, root: rich({
    tag: "body", bbox: { x: 0, y: 0, w: 1440, h: 1500 },
    computed: { display: "block", backgroundColor: "rgb(246, 244, 238)" }, hasAbsChild: true,
    children: [section("hero", "rgb(18, 26, 21)", "Hero"), section("main", null, "Main")],
  }),
}, brandMap, { source: "x", breakpoint: "lg", brandConfig: "example" });
console.log("WS-B — a body with an abs child is coerced to a VERTICAL FRAME (not a NONE GROUP):");
ok(absBody.root.type === "FRAME", "root.type === FRAME (coerced from GROUP)");
ok(absBody.root.layout.mode === "VERTICAL" && absBody.root.size.sizing.v === "HUG", "root forced VERTICAL + HUG despite abs child");

// ---- write the golden + schema-validate under v0.4 (no schema change this phase) ----
console.log("Schema — the produced golden declares v0.4 and validates:");
ok(ir.$schema === "heyhi-scene-graph/v0.4", "$schema === heyhi-scene-graph/v0.4");
mkdirSync(resolve(here, "examples"), { recursive: true });
const goldenPath = resolve(here, "examples/inherited-bg.lg.ir.json");
writeFileSync(goldenPath, JSON.stringify(ir, null, 2) + "\n");
const validator = resolve(here, "schema/validate_ir.py");
function py(scriptArgs, label, { wantExit0 = true } = {}) {
  try {
    execFileSync("python3", scriptArgs, { encoding: "utf8", cwd: here });
    ok(wantExit0, label);
  } catch (e) {
    const combined = String((e.stdout || "") + (e.stderr || "") + (e.message || ""));
    if (/No module named ['"]?jsonschema|command not found|ENOENT/.test(combined)) { console.log("  SKIP " + label + " (python3/jsonschema unavailable)"); }
    else ok(!wantExit0, label + (wantExit0 ? " — got:\n" + combined : ""));
  }
}
py([validator, goldenPath], "validate_ir.py PASS on inherited-bg.lg.ir.json (v0.4)");

// ---- builder — the transparent section's frame op carries NO fills; the painted one does ----
console.log("Builder — the op-plan distinguishes painted vs transparent frames:");
try {
  const outDir = "/tmp/bg-pagehug-build";
  execFileSync("python3", [resolve(here, "scripts/build_figma.py"), goldenPath, "--out-dir", outDir], { encoding: "utf8", cwd: here });
  const plan = JSON.parse(readFileSync(resolve(outDir, "plan.json"), "utf8"));
  const ops = plan.chunks.flatMap((c) => c.ops);
  const svcOp = ops.find((o) => o.op === "frame" && o.name === "Services");
  const heroOp = ops.find((o) => o.op === "frame" && o.name === "Hero");
  ok(svcOp && (!svcOp.fills || svcOp.fills.length === 0), "transparent 'Services' frame op has no fills (doFrame -> fills=[], shows the page through)");
  ok(heroOp && Array.isArray(heroOp.fills) && heroOp.fills.length > 0, "painted 'Hero' frame op carries fills");
} catch (e) {
  const combined = String((e.stdout || "") + (e.stderr || "") + (e.message || ""));
  if (/command not found|ENOENT/.test(combined)) console.log("  SKIP builder check (python3 unavailable)");
  else ok(false, "build_figma.py op-plan check — got:\n" + combined);
}

// ---- gate — severity-tiered assert_geometry: golden clean (no errors); a NONE/unpainted root warns ----
console.log("Gate — assert_geometry severity tiers (errors hard-fail; root guards advise):");
const gateClean = [
  "import sys,json;sys.path.insert(0,'scripts');import build_figma as b;",
  "v=b.assert_geometry(json.load(open('examples/inherited-bg.lg.ir.json'))['root']);",
  "errs=[x for x in v if x.get('severity','error')=='error'];",
  "sys.exit(0 if not errs and not v else 1)",
].join("");
py(["-c", gateClean], "compliant golden -> assert_geometry returns zero findings (no errors, no warns)");
const gateBad = [
  "import sys;sys.path.insert(0,'scripts');import build_figma as b;",
  "bad={'name':'Page','layout':{'mode':'NONE'},'size':{'w':1440,'h':6000,'sizing':{}},'fills':[],",
  "'children':[{'name':'a','size':{'w':1440,'h':500}},{'name':'b','size':{'w':1440,'h':500}}]};",
  "v=b.assert_geometry(bad);k=set(x['kind'] for x in v);w=[x for x in v if x.get('severity')=='warn'];",
  "sys.exit(0 if ('root-not-hugging' in k and 'root-no-background' in k and len(w)==2) else 1)",
].join("");
py(["-c", gateBad], "NONE/unpainted root -> root-not-hugging + root-no-background warns (severity 'warn')");

console.log("\n" + (fail === 0 ? "ALL PASS" : "FAILURES") + ` — ${pass} passed, ${fail} failed`);
process.exit(fail === 0 ? 0 : 1);
