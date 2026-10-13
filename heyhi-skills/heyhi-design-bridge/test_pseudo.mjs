// test_pseudo.mjs — unit tests for the R-1=D visible-pseudo handling and its non-leaf /
// box-null follow-up (no Playwright, no Figma). Exercises handlePseudo through buildIR:
//   Shape 1 — a resolvable box on a CHILDLESS FRAME host -> the host is flipped to NONE-layout
//             in place with a placeholder child (the coverage-bar leaf pattern; unchanged).
//   Shape 2 — a resolvable box on a NON-leaf host (children) or a non-frame host -> the host is
//             WRAPPED in a NONE-layout [host, placeholder] so its own layout is preserved.
//   Shape 3 — an in-flow `position:static` content-text marker (content:"▸ ", box:null) -> the
//             host is WRAPPED in a HORIZONTAL [placeholder, host] so the marker ships inline.
//   Refuse  — a box-less pseudo with NO visible content (content:"") -> a BLOCKING pseudo-element
//             flag; nothing ships silently.
// Plus a schema check (produced IR validates under v0.4) and an end-to-end builder check
// (build_figma.py SHIPS a shape-3 build exit-0 but REFUSES a dead-pseudo build exit-1).
//
//   node test_pseudo.mjs
//
// The rich() factory follows test_wrap.mjs, extended to accept a `pseudo` override.

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
    pseudo: over.pseudo || { before: null, after: null },
    font: { family: "Inter", generic: false, brand: true, loaded: true },
    svgOuter: over.svgOuter || null, imgSrc: over.imgSrc || null, text: over.text || null,
    isFlexOrGrid: false, hasAbsChild: over.hasAbsChild || false, children: over.children || [],
  };
}

// ---- pseudo-object factories mirroring browser-capture.mjs probePseudo output ----
function pBox(box, over = {}) {
  return { content: over.content ?? '""', position: over.position ?? "absolute",
    color: over.color ?? "rgb(0, 0, 0)", background: over.background ?? "rgb(20, 120, 120)",
    backgroundImage: null, border: null, radius: "0px", box };
}
function pInline(content = '"▸ "') {
  return { content, position: "static", color: "rgb(20, 120, 120)", background: "rgba(0, 0, 0, 0)",
    backgroundImage: null, border: null, radius: "0px", box: null };
}
function pDead() {
  return { content: '""', position: "static", color: "rgb(0, 0, 0)", background: "rgba(0, 0, 0, 0)",
    backgroundImage: null, border: null, radius: "0px", box: null };
}

// a section wrapper so the host is a CHILD (mirrors "Article Head > .eyebrow"), and the transform
// on the child is observable at ir.root.children[0].
function section(children, over = {}) {
  return rich({ tag: "section", classes: ["sec"], bbox: over.bbox || { x: 0, y: 0, w: 400, h: 400 },
    computed: { display: "flex", flexDirection: "column", backgroundColor: "rgb(250, 250, 250)" },
    children });
}
function build(rootRich) {
  return buildIR({ root: rootRich }, brandMap, { source: "test", breakpoint: "lg", brandConfig: "example" }).ir;
}
function flagsOf(ir, feature) { return ((ir.root && ir.root.flags) || []).filter((f) => f.feature === feature); }

// ---------------------------------------------------------------------------
// Shape 1 — leaf FRAME host + resolvable box -> flipped in place (unchanged behavior)
// ---------------------------------------------------------------------------
console.log("Shape 1 — a childless FRAME host with an absolute ::before box flips to NONE in place:");
{
  const cov = rich({ tag: "div", classes: ["cov__bar"], bbox: { x: 100, y: 200, w: 52, h: 8 },
    computed: { position: "relative" },
    pseudo: { before: pBox({ x: 100, y: 200, w: 26, h: 8 }), after: null } });
  const ir = build(section([cov]));
  const host = ir.root.children[0];
  ok(host.layout && host.layout.mode === "NONE", "leaf host layout flipped to NONE (in place, not wrapped)");
  ok(Array.isArray(host.children) && host.children.length === 1, "one placeholder child added");
  ok(host.children[0].name === "⚠ ::before (needs human)", "placeholder is the ⚠ needs-human marker");
  ok(host.children[0].position && host.children[0].position.x === 0 && host.children[0].position.y === 0, "placeholder offset from the host origin (0,0)");
  ok(host.children[0].size.w === 26, "placeholder carries the captured box width (26)");
  ok(flagsOf(ir, "pseudo-placeholder").length === 1, "raises a non-blocking pseudo-placeholder flag");
  ok(flagsOf(ir, "pseudo-element").length === 0, "raises NO blocking pseudo-element flag (it ships)");
}

// ---------------------------------------------------------------------------
// Shape 2 — non-leaf host + resolvable box -> WRAP so the host's own layout survives
// ---------------------------------------------------------------------------
console.log("Shape 2 — a host WITH children + an absolute ::before box is wrapped, layout preserved:");
{
  const label = rich({ tag: "span", text: "New", bbox: { x: 108, y: 206, w: 30, h: 12 } });
  const badge = rich({ tag: "div", classes: ["badge"], bbox: { x: 100, y: 200, w: 80, h: 24 },
    computed: { position: "relative", display: "flex", flexDirection: "row" },
    children: [label],
    pseudo: { before: pBox({ x: 100, y: 200, w: 12, h: 12 }), after: null } });
  const ir = build(section([badge]));
  const wrap = ir.root.children[0];
  ok(wrap.type === "FRAME" && wrap.layout.mode === "NONE", "host wrapped in a NONE-layout container");
  ok(wrap.size.w === 80 && wrap.size.h === 24 && wrap.size.sizing.h === "FIXED", "wrapper takes the host footprint (80x24, FIXED)");
  ok(Array.isArray(wrap.children) && wrap.children.length === 2, "wrapper holds [host, placeholder]");
  const inner = wrap.children[0];
  ok(inner.name === "Badge" && inner.layout && inner.layout.mode === "HORIZONTAL", "inner host keeps its own HORIZONTAL layout");
  ok(inner.children && inner.children.length === 1 && inner.children[0].characters === "New", "inner host keeps its own children");
  ok(inner.position && inner.position.x === 0 && inner.position.y === 0, "inner host pinned at the wrapper origin");
  ok(wrap.children[1].name === "⚠ ::before (needs human)", "placeholder is the second child, at its captured box");
  ok(wrap.children[1].position.x === 0 && wrap.children[1].size.w === 12, "placeholder offset + captured width (12)");
  ok(flagsOf(ir, "pseudo-placeholder").length === 1 && flagsOf(ir, "pseudo-element").length === 0, "ships (pseudo-placeholder, no blocking flag)");
}

// ---------------------------------------------------------------------------
// Shape 3 — the .eyebrow case: an in-flow content-text ::before (box:null) -> inline wrap
// ---------------------------------------------------------------------------
console.log("Shape 3 — a TEXT host with an in-flow content ::before marker ships an inline placeholder:");
{
  const eyebrow = rich({ tag: "p", classes: ["eyebrow"], text: "Field note", bbox: { x: 100, y: 200, w: 60, h: 12 },
    computed: { fontSize: "9.6px", fontFamily: "DM Mono", color: "rgb(20, 120, 120)" },
    pseudo: { before: pInline('"▸ "'), after: null } });
  const ir = build(section([eyebrow]));
  const wrap = ir.root.children[0];
  ok(wrap.type === "FRAME" && wrap.layout.mode === "HORIZONTAL", "host wrapped in a HORIZONTAL row (inline marker + text)");
  ok(wrap.layout.counterAxisAlignItems === "CENTER", "marker is vertically centered against the text");
  ok(wrap.size && wrap.size.w === null && wrap.size.h === null && wrap.size.sizing.h === "HUG" && wrap.size.sizing.v === "HUG",
    "wrapper HUGs both axes (w/h null, NOT the host bbox) so a wider/taller [marker+text] does not false-trip the lost-wrap geometry check");
  ok(wrap.children.length === 2, "wrapper holds [placeholder, host]");
  ok(wrap.children[0].name === "⚠ ::before (needs human)", "the ::before placeholder comes FIRST (inline before the text)");
  ok(wrap.children[0].size.w === 9.6 && wrap.children[0].size.sizing.h === "FIXED", "inline placeholder is a nominal ~1em square from the host font (9.6)");
  ok(wrap.children[1].type === "TEXT" && wrap.children[1].characters === "Field note", "the host TEXT is the second child, intact");
  ok(flagsOf(ir, "pseudo-placeholder").length === 1, "raises a non-blocking pseudo-placeholder flag");
  ok(flagsOf(ir, "pseudo-element").length === 0, "the build SHIPS — no blocking pseudo-element flag (the closed gap)");
}

// ---------------------------------------------------------------------------
// Shape 3 ordering — a content ::after marker ships AFTER the host
// ---------------------------------------------------------------------------
console.log("Shape 3 (order) — a content ::after marker is placed AFTER the host:");
{
  const reqd = rich({ tag: "label", text: "Email", bbox: { x: 100, y: 200, w: 50, h: 16 },
    computed: { fontSize: "14px" },
    pseudo: { before: null, after: pInline('"*"') } });
  const ir = build(section([reqd]));
  const wrap = ir.root.children[0];
  ok(wrap.layout.mode === "HORIZONTAL" && wrap.children.length === 2, "wrapped into a HORIZONTAL row of two");
  ok(wrap.children[0].type === "TEXT" && wrap.children[0].characters === "Email", "the host TEXT comes first");
  ok(wrap.children[1].name === "⚠ ::after (needs human)", "the ::after placeholder comes second");
}

// ---------------------------------------------------------------------------
// Shape 3 (geometry) — a marker taller/wider than the host bbox must not overflow the
// wrapper (regression: the wrapper hugs, so assert_geometry stays clean). A fixed-size
// wrapper at the host bbox false-tripped the lost-wrap overflow error and clipped a tall
// marker; the eyebrow happened to fit, so only a pathological case guards it.
// ---------------------------------------------------------------------------
console.log("Shape 3 (geometry) — a tall/wide marker on a tight-line-height host stays geometry-clean:");
{
  // fontSize 16 -> a 16px placeholder, but a compressed line box (lineHeight 11) -> host bbox.h 11.
  const tight = rich({ tag: "p", classes: ["tight"], text: "NOTE", bbox: { x: 20, y: 20, w: 40, h: 11 },
    computed: { fontSize: "16px", lineHeight: "11px" }, pseudo: { before: pInline('"▸ "'), after: null } });
  const ir = build(section([tight], { bbox: { x: 0, y: 0, w: 400, h: 120 } }));
  const wrap = ir.root.children[0];
  ok(wrap.size.w === null && wrap.size.h === null, "wrapper hugs (w/h null) even though the marker (16) is taller than the host bbox.h (11)");
  const irPath = "/tmp/pseudo-test/tight.ir.json";
  writeFileSync(irPath, JSON.stringify(ir, null, 2) + "\n");
  try {
    const outp = execFileSync("python3", [resolve(here, "scripts/build_figma.py"), irPath, "--summary"], { encoding: "utf8" });
    ok(!/\[error\//.test(outp.slice(outp.indexOf("GEOMETRY CHECK"))), "build_figma GEOMETRY CHECK reports no error (no false lost-wrap overflow)");
  } catch (e) {
    const combined = String((e.stdout || "") + (e.stderr || "") + (e.message || ""));
    if (/command not found|ENOENT|No such file/.test(combined)) console.log("  SKIP geometry check (python3 unavailable)");
    else ok(false, "build_figma --summary geometry check — got:\n" + combined);
  }
}

// ---------------------------------------------------------------------------
// Refuse — a box-less pseudo with NO visible content still blocks
// ---------------------------------------------------------------------------
console.log("Refuse — an empty in-flow ::before (no box, no content) stays a BLOCKING pseudo-element:");
{
  const host = rich({ tag: "div", classes: ["spacer"], bbox: { x: 100, y: 200, w: 40, h: 40 },
    pseudo: { before: pDead(), after: null } });
  const ir = build(section([host]));
  const out = ir.root.children[0];
  ok(!(out.children && out.children.length), "host is NOT wrapped (nothing to place)");
  ok(flagsOf(ir, "pseudo-element").length === 1, "raises a blocking pseudo-element flag");
  ok(flagsOf(ir, "pseudo-placeholder").length === 0, "raises NO pseudo-placeholder (it refuses, does not ship)");
}

// ---------------------------------------------------------------------------
// Passthrough — a node with no pseudo is untouched
// ---------------------------------------------------------------------------
console.log("Passthrough — a node with no pseudo is returned unchanged:");
{
  const plain = rich({ tag: "p", text: "Body", bbox: { x: 100, y: 200, w: 200, h: 40 } });
  const ir = build(section([plain]));
  const out = ir.root.children[0];
  ok(out.type === "TEXT" && out.characters === "Body", "plain node unchanged (still a bare TEXT)");
  ok(flagsOf(ir, "pseudo-placeholder").length === 0 && flagsOf(ir, "pseudo-element").length === 0, "no pseudo flags at all");
}

// ---------------------------------------------------------------------------
// Schema — an IR carrying all three shapes validates under v0.4
// ---------------------------------------------------------------------------
console.log("Schema — an IR carrying shapes 1+2+3 validates under v0.4:");
{
  const leaf = rich({ tag: "div", classes: ["cov__bar"], bbox: { x: 10, y: 10, w: 52, h: 8 },
    computed: { position: "relative" }, pseudo: { before: pBox({ x: 10, y: 10, w: 26, h: 8 }), after: null } });
  const inner = rich({ tag: "span", text: "New", bbox: { x: 18, y: 60, w: 30, h: 12 } });
  const badge = rich({ tag: "div", classes: ["badge"], bbox: { x: 10, y: 50, w: 80, h: 24 },
    computed: { position: "relative", display: "flex" }, children: [inner],
    pseudo: { before: pBox({ x: 10, y: 50, w: 12, h: 12 }), after: null } });
  const eyebrow = rich({ tag: "p", classes: ["eyebrow"], text: "Field note", bbox: { x: 10, y: 100, w: 60, h: 12 },
    computed: { fontSize: "9.6px" }, pseudo: { before: pInline('"▸ "'), after: null } });
  const ir = build(section([leaf, badge, eyebrow]));
  ok(ir.$schema === "heyhi-scene-graph/v0.4", "$schema === heyhi-scene-graph/v0.4");
  mkdirSync(resolve(here, "/tmp/pseudo-test"), { recursive: true });
  const irPath = "/tmp/pseudo-test/shapes.ir.json";
  writeFileSync(irPath, JSON.stringify(ir, null, 2) + "\n");
  const validator = resolve(here, "schema/validate_ir.py");
  try {
    const outp = execFileSync("python3", [validator, irPath], { encoding: "utf8" });
    ok(/^PASS /m.test(outp), "validate_ir.py PASS on the shapes IR (v0.4)");
  } catch (e) {
    const combined = String((e.stdout || "") + (e.stderr || "") + (e.message || ""));
    if (/No module named ['"]?jsonschema|command not found|ENOENT/.test(combined)) console.log("  SKIP validate (python3/jsonschema unavailable)");
    else ok(false, "validate_ir.py — got:\n" + combined);
  }
}

// ---------------------------------------------------------------------------
// Builder — a shape-3 build SHIPS (exit 0); a dead-pseudo build REFUSES (exit 1)
// ---------------------------------------------------------------------------
console.log("Builder — build_figma.py ships a shape-3 build but refuses a dead-pseudo build:");
{
  const builder = resolve(here, "scripts/build_figma.py");
  // shape 3: the eyebrow marker — must SHIP (exit 0) where it used to refuse.
  const eyebrow = rich({ tag: "p", classes: ["eyebrow"], text: "Field note", bbox: { x: 10, y: 10, w: 60, h: 12 },
    computed: { fontSize: "9.6px" }, pseudo: { before: pInline('"▸ "'), after: null } });
  const shipIr = build(section([eyebrow], { bbox: { x: 0, y: 0, w: 200, h: 80 } }));
  const shipPath = "/tmp/pseudo-test/ship.ir.json";
  writeFileSync(shipPath, JSON.stringify(shipIr, null, 2) + "\n");
  // dead pseudo: must REFUSE (exit 1).
  const spacer = rich({ tag: "div", classes: ["spacer"], bbox: { x: 10, y: 10, w: 40, h: 40 }, pseudo: { before: pDead(), after: null } });
  const refuseIr = build(section([spacer], { bbox: { x: 0, y: 0, w: 200, h: 80 } }));
  const refusePath = "/tmp/pseudo-test/refuse.ir.json";
  writeFileSync(refusePath, JSON.stringify(refuseIr, null, 2) + "\n");

  let pythonOk = true;
  // ship: exit 0, the placeholder makes it into the op-plan.
  try {
    execFileSync("python3", [builder, shipPath, "--out-dir", "/tmp/pseudo-test/ship"], { encoding: "utf8" });
    const plan = JSON.parse(readFileSync("/tmp/pseudo-test/ship/plan.json", "utf8"));
    const ops = plan.chunks.flatMap((c) => c.ops);
    ok(ops.some((o) => (o.name || "").includes("needs human")), "shape-3 build SHIPS (exit 0) and the ⚠ placeholder is in the op-plan");
  } catch (e) {
    const combined = String((e.stdout || "") + (e.stderr || "") + (e.message || ""));
    if (/command not found|ENOENT|No such file/.test(combined)) { pythonOk = false; console.log("  SKIP builder ship check (python3 unavailable)"); }
    else ok(false, "shape-3 build should exit 0 — got:\n" + combined);
  }
  // refuse: exit 1 with a BLOCKING banner.
  if (pythonOk) {
    let threw = false, combined = "";
    try {
      execFileSync("python3", [builder, refusePath, "--out-dir", "/tmp/pseudo-test/refuse"], { encoding: "utf8" });
    } catch (e) {
      threw = true;
      combined = String((e.stdout || "") + (e.stderr || "") + (e.message || ""));
    }
    ok(threw && /block|refuse/i.test(combined), "dead-pseudo build REFUSES (exit 1, BUILD BLOCKED banner)");
  }
}

console.log("\n" + (fail === 0 ? "ALL PASS" : "FAILURES") + ` — ${pass} passed, ${fail} failed`);
process.exit(fail === 0 ? 0 : 1);
