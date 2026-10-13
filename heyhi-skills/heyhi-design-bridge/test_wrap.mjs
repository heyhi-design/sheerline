// test_wrap.mjs — unit tests for design-bridge packet wrap-and-sizing (WS1 / ADR-014;
// no Playwright, no Figma). Exercises the Node-side IR logic directly:
//   WS1 — a multi-row CSS grid / wrapping flex emits layout.layoutWrap:WRAP +
//         counterAxisSpacing (row-gap), and the wrap container is FIXED width +
//         HUG height (h:null) so it auto-heights to the wrapped rows.
//   Edge — a single-row grid does NOT wrap; a wrapping COLUMN flex is flagged, not
//          faked; a non-uniform grid keeps a reduced css-grid flag.
// Plus a schema check (the produced golden validates under the staged v0.4 schema)
// and a builder check (the Python op-builder forwards layoutWrap to the frame op).
//
//   node test_wrap.mjs
//
// buildIR is imported from the staged wrap-and-sizing copy (deployed skill untouched).
// The rich() factory follows p3-position/test_p3.mjs, extended with alignContent.

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

// a card: text + opaque bg + flex (so it hugs its width like a real client services card)
function card(label, w = 336, h = 200) {
  return rich({ tag: "div", classes: ["card"], text: label, bbox: { x: 0, y: 0, w, h },
    computed: { display: "flex", flexDirection: "column", backgroundColor: "rgb(255, 255, 255)",
                paddingTop: "24px", paddingRight: "24px", paddingBottom: "24px", paddingLeft: "24px" } });
}
function chip(label, w = 120, h = 36) {
  return rich({ tag: "span", classes: ["chip"], text: label, bbox: { x: 0, y: 0, w, h },
    computed: { display: "inline-flex", backgroundColor: "rgb(255, 255, 255)" } });
}
const meta = { viewport: { w: 1440, h: 1100 }, rootSelector: "body", fontsReady: "loaded", ruleCount: 0 };
const flagsOf = (ir, feature) => (ir.root.flags || []).filter((f) => f.feature === feature);

// ---- GOLDEN: a section with a 3-col / 10-card grid (4 rows) + a wrapping chip row ----
const gridCards = ["Data Pipeline", "Access Management", "Billing Settings", "Webhook Delivery",
  "Search & Filtering", "Files & Documents", "Alerts / Digests", "Audit Logs", "Workspace Export", "Single Sign-On"];
const goldenCapture = {
  meta,
  root: rich({
    tag: "section", classes: ["section"], bbox: { x: 0, y: 0, w: 1312, h: 1296 },
    computed: { display: "block", paddingTop: "96px", paddingRight: "120px", paddingBottom: "96px", paddingLeft: "120px" },
    children: [
      rich({
        tag: "div", classes: ["grid"], bbox: { x: 120, y: 96, w: 1072, h: 920 },
        // 3 uniform tracks, 10 children -> wraps to 4 rows; column-gap 24, row-gap 40
        computed: { display: "grid", gridTemplateColumns: "341.33px 341.33px 341.33px",
                    columnGap: "24px", rowGap: "40px" },
        children: gridCards.map((l) => card(l)),
      }),
      rich({
        tag: "div", classes: ["chips"], bbox: { x: 120, y: 1056, w: 1072, h: 84 },
        computed: { display: "flex", flexWrap: "wrap", columnGap: "8px", rowGap: "8px" },
        children: ["North County", "West County", "Greater Metro", "River Valley", "Hill County"].map((l) => chip(l)),
      }),
    ],
  }),
};
const { ir } = buildIR(goldenCapture, brandMap, { source: "prototypes/wrapping-grid.html", breakpoint: "lg", brandConfig: "example" });
const grid = ir.root.children[0];
const chips = ir.root.children[1];

console.log("WS1 — a multi-row CSS grid maps to a layoutWrap:WRAP auto-layout:");
ok(grid.layout.mode === "HORIZONTAL", "grid.layout.mode === HORIZONTAL");
ok(grid.layout.layoutWrap === "WRAP", "grid.layout.layoutWrap === WRAP (was a flat single row)");
ok(grid.layout.itemSpacing === 24, "main-axis itemSpacing === column-gap (24)");
ok(grid.layout.counterAxisSpacing === 40, "counterAxisSpacing === row-gap (40)");

console.log("WS1 — the wrap container is FIXED width + HUG height (kills the white space):");
ok(grid.size.sizing.h === "FIXED" && grid.size.sizing.v === "HUG", "grid.size.sizing === {h:FIXED, v:HUG}");
ok(grid.size.w === 1072, "grid.size.w === captured border-box width (1072)");
ok(grid.size.h === null, "grid.size.h === null (does NOT carry the 4-row bbox height of 920)");

console.log("WS1 — a uniform grid is no longer flagged; the old flex-wrap flag is gone:");
ok(flagsOf(ir, "css-grid").length === 0, "no css-grid flag for a uniform repeat(3,1fr) grid");
ok(flagsOf(ir, "flex-wrap").length === 0, "no legacy 'flex-wrap' flag");

console.log("WS1 — a wrapping flex chip row also maps to WRAP:");
ok(chips.layout.layoutWrap === "WRAP" && chips.layout.itemSpacing === 8 && chips.layout.counterAxisSpacing === 8,
   "chip row -> WRAP, itemSpacing 8, counterAxisSpacing 8");
ok(chips.size.sizing.h === "FIXED" && chips.size.h === null, "chip row -> FIXED width + HUG height (h:null)");

// ---- EDGE: single-row grid (children <= tracks) does NOT wrap ----
const { ir: singleRow } = buildIR({ meta, root: rich({
  tag: "div", classes: ["row"], bbox: { x: 0, y: 0, w: 700, h: 200 },
  computed: { display: "grid", gridTemplateColumns: "200px 200px 200px", columnGap: "24px" },
  children: [card("A", 200), card("B", 200), card("C", 200)],
}) }, brandMap, { source: "x", breakpoint: "lg", brandConfig: "example" });
console.log("Edge — a single-row grid (children <= tracks) stays a plain HORIZONTAL row:");
ok(singleRow.root.layout.mode === "HORIZONTAL" && !singleRow.root.layout.layoutWrap, "no layoutWrap when children fit one row");
ok(singleRow.root.size.h !== null, "single-row grid keeps a real height (not pinned to null)");

// ---- EDGE: a wrapping COLUMN flex has no Figma equivalent -> flag, don't fake ----
const { ir: colWrap } = buildIR({ meta, root: rich({
  tag: "div", classes: ["colwrap"], bbox: { x: 0, y: 0, w: 400, h: 600 },
  computed: { display: "flex", flexDirection: "column", flexWrap: "wrap", rowGap: "8px" },
  children: [card("A"), card("B"), card("C")],
}) }, brandMap, { source: "x", breakpoint: "lg", brandConfig: "example" });
console.log("Edge — a wrapping column flex is flagged (no layoutWrap), not silently faked:");
ok(colWrap.root.layout.mode === "VERTICAL" && !colWrap.root.layout.layoutWrap, "column flex stays VERTICAL, no layoutWrap");
ok(flagsOf(colWrap, "flex-wrap-vertical").length === 1, "raises a flex-wrap-vertical flag (needs human)");

// ---- EDGE: a non-uniform grid keeps a reduced css-grid flag (equal-column approx) ----
const { ir: nonUniform } = buildIR({ meta, root: rich({
  tag: "div", classes: ["nu"], bbox: { x: 0, y: 0, w: 1224, h: 400 },
  computed: { display: "grid", gridTemplateColumns: "800px 400px", columnGap: "24px", rowGap: "24px" },
  children: [card("A", 800), card("B", 400), card("C", 800), card("D", 400)],
}) }, brandMap, { source: "x", breakpoint: "lg", brandConfig: "example" });
console.log("Edge — a non-uniform grid wraps but keeps an honest css-grid flag:");
ok(nonUniform.root.layout.layoutWrap === "WRAP", "non-uniform grid still wraps (HORIZONTAL + WRAP)");
ok(flagsOf(nonUniform, "css-grid").length === 1, "raises a css-grid flag (equal-column approximation, review)");

// ---- write the golden + schema-validate under the staged v0.4 schema ----
console.log("Schema — the produced golden declares v0.4 and validates:");
ok(ir.$schema === "heyhi-scene-graph/v0.4", "$schema === heyhi-scene-graph/v0.4");
mkdirSync(resolve(here, "examples"), { recursive: true });
const goldenPath = resolve(here, "examples/wrapping-grid.lg.ir.json");
writeFileSync(goldenPath, JSON.stringify(ir, null, 2) + "\n");
const validator = resolve(here, "schema/validate_ir.py");
function validate(path, label) {
  try {
    const outp = execFileSync("python3", [validator, path], { encoding: "utf8" });
    ok(/^PASS /m.test(outp), label);
  } catch (e) {
    const combined = String((e.stdout || "") + (e.stderr || "") + (e.message || ""));
    if (/No module named ['"]?jsonschema|command not found|ENOENT/.test(combined)) console.log("  SKIP " + label + " (python3/jsonschema unavailable)");
    else ok(false, label + " — got:\n" + combined);
  }
}
validate(goldenPath, "validate_ir.py PASS on wrapping-grid.lg.ir.json (v0.4)");

// ---- builder — the Python op-builder forwards layoutWrap to the frame op ----
console.log("Builder — build_figma.py forwards layoutWrap + counterAxisSpacing to the frame ops:");
try {
  const outDir = "/tmp/wrap-build";
  execFileSync("python3", [resolve(here, "scripts/build_figma.py"), goldenPath, "--out-dir", outDir], { encoding: "utf8" });
  const plan = JSON.parse(readFileSync(resolve(outDir, "plan.json"), "utf8"));
  const ops = plan.chunks.flatMap((c) => c.ops);
  const wrapOps = ops.filter((o) => o.layout && o.layout.layoutWrap === "WRAP");
  ok(wrapOps.length >= 2, "two frame ops carry layout.layoutWrap === WRAP (grid + chip row)");
  ok(wrapOps.some((o) => o.layout.counterAxisSpacing === 40), "the grid op carries counterAxisSpacing === 40 (row-gap)");
} catch (e) {
  const combined = String((e.stdout || "") + (e.stderr || "") + (e.message || ""));
  if (/command not found|ENOENT/.test(combined)) console.log("  SKIP builder check (python3 unavailable)");
  else ok(false, "build_figma.py op-plan check — got:\n" + combined);
}

console.log("\n" + (fail === 0 ? "ALL PASS" : "FAILURES") + ` — ${pass} passed, ${fail} failed`);
process.exit(fail === 0 ? 0 : 1);
