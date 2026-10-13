// test_controls.mjs — unit tests for design-bridge packet controls-path (WS4; no Playwright,
// no Figma). Exercises the Node-side IR logic that fixes buttons & links:
//   B — an interactive control with a visible box (<a>/<button>/.btn/.cta + bg|border) becomes
//       a deterministic control FRAME: a ghost button (transparent bg + border) renders as an
//       OUTLINE (carries strokes), never collapses to bare text; a bare nav link stays TEXT.
//   C — a TEXT colour that only resolves via the MATCHED path and is nearest a BACKGROUND-family
//       token is kept literal + UNBOUND (link-color-unsnapped), so a light label never goes
//       invisible; a label that ~matches its control fill raises near-invisible-label.
//   D — loose inline text beside an inline <img> inside a flex span survives as a TEXT run
//       (the "See service" card__more label), instead of being dropped with the non-element
//       content. (The browser-side synthesis is in browser-capture.mjs looseTextNode and is
//       proven end-to-end by the live re-extract; here we assert the build-side contract.)
// Plus a schema check (the produced golden validates under v0.4) and the WS2 geometry gate.
//
//   node test_controls.mjs
//
// buildIR is imported from the staged controls-path copy (deployed skill untouched). The
// rich() factory follows test_wrap.mjs, extended with role/href and a control-aware brandMap.

import { buildIR } from "./scripts/extract_scene_graph/lib/build-ir.mjs";
import { writeFileSync, mkdirSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";

let pass = 0, fail = 0;
function ok(cond, msg) { if (cond) { pass++; console.log("  PASS " + msg); } else { fail++; console.log("  FAIL " + msg); } }

const here = dirname(fileURLToPath(import.meta.url));

// A control-aware brandMap mock. The invisible-label hazard is a near-white TEXT colour
// matching a BACKGROUND-family token; pure white maps to text/inverse (binds cleanly), a
// bg-role colour maps to a background token. Dark text -> a text token.
const brandMap = {
  lookupVar: () => null,
  nearestSpacing: () => null,
  nearestColor: (computed, family) => {
    const m = /rgb\((\d+),\s*(\d+),\s*(\d+)\)/.exec(computed || "");
    if (!m) return null;
    const r = +m[1], g = +m[2], b = +m[3], lum = (r + g + b) / 3;
    if (r === 255 && g === 255 && b === 255) return { token: { token_path: "tokens.color.text.inverse", figma_variable: "color/text/inverse" }, confidence: 1 };
    if (lum >= 235) return { token: { token_path: "tokens.color.backgrounds.surface", figma_variable: "color/backgrounds/surface" }, confidence: 0.94 };
    if (family === "background") return { token: { token_path: "tokens.color.backgrounds.dark-surface", figma_variable: "color/backgrounds/dark-surface" }, confidence: 0.9 };
    return { token: { token_path: "tokens.color.text.body", figma_variable: "color/text/body" }, confidence: 0.9 };
  },
};

function rich(over = {}) {
  const c = {
    display: "block", position: "static", overflowX: "visible", overflowY: "visible",
    flexDirection: "row", justifyContent: "flex-start", alignItems: "normal", alignContent: "normal", flexWrap: "nowrap",
    rowGap: "0px", columnGap: "0px", gridTemplateColumns: "none", transform: "none", boxShadow: "none",
    borderTopWidth: "0px", borderRightWidth: "0px", borderBottomWidth: "0px", borderLeftWidth: "0px",
    borderTopStyle: "none", borderTopColor: "rgba(0, 0, 0, 0)",
    borderTopLeftRadius: "0px", borderTopRightRadius: "0px", borderBottomRightRadius: "0px", borderBottomLeftRadius: "0px",
    opacity: "1", animationName: "none", transitionDuration: "0s",
    backgroundColor: "rgba(0, 0, 0, 0)", backgroundImage: "none", backgroundSize: "auto", color: "rgb(35, 40, 38)",
    fontFamily: "Work Sans", fontWeight: "400", fontSize: "16px", lineHeight: "normal", letterSpacing: "normal",
    paddingTop: "0px", paddingRight: "0px", paddingBottom: "0px", paddingLeft: "0px",
    ...(over.computed || {}),
  };
  return {
    tag: over.tag || "div", id: over.id || null, classes: over.classes || [], dataAudit: null,
    role: over.role || null, href: over.href || null,
    bbox: over.bbox || { x: 0, y: 0, w: 100, h: 20 }, computed: c,
    declared: { color: null, backgroundColor: null, fontSize: null, padding: null, gap: null, borderColor: null, animation: null, ...(over.declared || {}) },
    pseudo: { before: null, after: null },
    font: { family: "Work Sans", generic: false, brand: true, loaded: true },
    svgOuter: over.svgOuter || null, imgSrc: over.imgSrc || null, text: over.text || null,
    isFlexOrGrid: false, hasAbsChild: over.hasAbsChild || false, children: over.children || [],
  };
}
const meta = { viewport: { w: 1440, h: 1100 }, rootSelector: "body", fontsReady: "loaded", ruleCount: 0 };
// flags are attached to the built root node (build-ir: root.flags); these single-node
// builds return that root directly, so read flags off the node.
const flagsOf = (node, feature) => (node.flags || []).filter((f) => f.feature === feature);
const build1 = (node) => buildIR({ meta, root: node }, brandMap, { source: "prototypes/controls.html", breakpoint: "lg", brandConfig: "example" }).ir;

// ---- B: primary button (bg + .btn) -> control FRAME with fills + a Button-tagged label ----
const primary = build1(rich({
  tag: "a", classes: ["btn", "btn--primary"], href: "#estimate", text: "Get a Free Estimate", bbox: { x: 0, y: 0, w: 240, h: 52 },
  computed: { display: "inline-flex", backgroundColor: "rgb(43, 95, 42)", color: "rgb(255, 255, 255)",
              paddingTop: "14px", paddingBottom: "14px", paddingLeft: "28px", paddingRight: "28px",
              borderTopLeftRadius: "8px", borderTopRightRadius: "8px", borderBottomRightRadius: "8px", borderBottomLeftRadius: "8px" },
})).root;
console.log("B — a primary button (bg + .btn) becomes a control FRAME with a fill + a label:");
ok(primary.type === "FRAME", "primary button -> FRAME (not bare TEXT/CHIP)");
ok((primary.fills || []).some((f) => f.type === "SOLID"), "primary FRAME carries a SOLID background fill");
ok(primary.layout && primary.layout.mode === "HORIZONTAL", "control FRAME is HORIZONTAL auto-layout");
const pLabel = (primary.children || []).find((c) => c.type === "TEXT");
ok(pLabel && pLabel.characters === "Get a Free Estimate", "label TEXT present with the button text (no empty pill)");
ok(pLabel && pLabel.type_style && pLabel.type_style.token_ref === "tokens.typography.scale.button", "label tagged token_ref -> UI/Button (WS3 style binding)");

// ---- B: ghost / secondary button (transparent bg + border) -> OUTLINE, never bare text ----
const ghost = build1(rich({
  tag: "a", classes: ["btn", "btn--secondary"], href: "#more", text: "Learn more", bbox: { x: 0, y: 0, w: 180, h: 52 },
  computed: { display: "inline-flex", backgroundColor: "rgba(0, 0, 0, 0)", color: "rgb(35, 40, 38)",
              borderTopWidth: "1px", borderRightWidth: "1px", borderBottomWidth: "1px", borderLeftWidth: "1px",
              borderTopStyle: "solid", borderTopColor: "rgb(35, 40, 38)",
              paddingTop: "14px", paddingBottom: "14px", paddingLeft: "28px", paddingRight: "28px" },
})).root;
console.log("B — a ghost button (transparent bg + border) renders as an OUTLINE, not bare text:");
ok(ghost.type === "FRAME", "ghost button -> FRAME (was misclassified as plain TEXT)");
ok(Array.isArray(ghost.strokes) && ghost.strokes.length === 1 && ghost.strokes[0].weight === 1, "ghost FRAME carries a 1px stroke (the visible outline)");
ok(!ghost.fills || ghost.fills.length === 0, "ghost FRAME has NO solid fill (transparent bg preserved)");
ok((ghost.children || []).some((c) => c.type === "TEXT" && c.characters === "Learn more"), "ghost button keeps its label TEXT");

// ---- B: a bare nav link (no box) stays TEXT — nav links never become pills ----
const nav = build1(rich({ tag: "a", classes: ["nav__link"], href: "/services", text: "Services", bbox: { x: 0, y: 0, w: 80, h: 22 } })).root;
console.log("B — a bare nav link (no bg, no border, no btn class) stays TEXT:");
ok(nav.type === "TEXT" && nav.characters === "Services", "nav link -> TEXT (not turned into a pill/FRAME)");

// ---- C: a light inherited link colour is kept literal + unbound (link-color-unsnapped) ----
const invis = build1(rich({
  tag: "a", classes: ["hero__link"], href: "#", text: "Read more", bbox: { x: 0, y: 0, w: 110, h: 22 },
  // color:inherit resolved to a near-white on a light card -> matched path -> background token
  computed: { color: "rgb(246, 246, 244)" },
})).root;
console.log("C — a near-white link colour is NOT snapped to a background token (stays visible):");
ok(invis.type === "TEXT", "the link is TEXT (link-like, not button-like)");
ok(invis.fills && invis.fills[0] && !invis.fills[0].bind, "link label colour is UNBOUND (not snapped to backgrounds/surface)");
ok(flagsOf(invis, "link-color-unsnapped").length === 1, "raises a link-color-unsnapped flag (needs human)");

// ---- C: near-invisible label (label ~ control fill) raises a contrast flag ----
const lowContrast = build1(rich({
  tag: "button", classes: ["btn"], text: "Submit", bbox: { x: 0, y: 0, w: 140, h: 48 },
  computed: { display: "inline-flex", backgroundColor: "rgb(240, 240, 240)", color: "rgb(255, 255, 255)",
              paddingTop: "12px", paddingBottom: "12px", paddingLeft: "24px", paddingRight: "24px" },
})).root;
console.log("C — a label that ~matches its control fill raises near-invisible-label:");
ok(lowContrast.type === "FRAME", "low-contrast control still builds as a FRAME");
ok(flagsOf(lowContrast, "near-invisible-label").length === 1, "white label on a near-white fill -> near-invisible-label flag");

// ---- D: loose text beside an inline <img> inside a flex span survives ----
// the FIXED capture shape browser-capture.looseTextNode produces: [loose-text leaf, arrow img]
const cardMore = build1(rich({
  tag: "span", classes: ["card__more"], bbox: { x: 0, y: 0, w: 120, h: 20 },
  computed: { display: "inline-flex", color: "rgb(43, 95, 42)", columnGap: "6px" },
  children: [
    rich({ tag: "span", text: "See service", bbox: { x: 0, y: 0, w: 80, h: 20 }, computed: { color: "rgb(43, 95, 42)" } }),
    rich({ tag: "img", imgSrc: "assets/arrow.png", bbox: { x: 86, y: 4, w: 13, h: 13 } }),
  ],
})).root;
console.log("D — loose 'See service' text survives alongside its arrow (card__more, no dropped label):");
ok(cardMore.type === "FRAME", "card__more -> FRAME (it is not a .btn, so not a control box)");
const seeService = (cardMore.children || []).find((c) => c.type === "TEXT" && c.characters === "See service");
ok(!!seeService, "the 'See service' label TEXT is preserved (was dropped with the inline <img>)");
ok((cardMore.children || []).some((c) => c.type === "IMAGE" || c.type === "VECTOR"), "the arrow image still rides alongside the label");

// ---- GOLDEN: a Controls section (column of the cases) that forces the failure path ----
const goldenCapture = { meta, root: rich({
  tag: "section", classes: ["controls"], bbox: { x: 0, y: 0, w: 1312, h: 520 },
  computed: { display: "flex", flexDirection: "column", rowGap: "32px", paddingTop: "96px", paddingRight: "120px", paddingBottom: "96px", paddingLeft: "120px" },
  children: [
    rich({ tag: "a", classes: ["btn", "btn--primary"], href: "#estimate", text: "Get a Free Estimate", bbox: { x: 120, y: 96, w: 240, h: 52 },
      computed: { display: "inline-flex", backgroundColor: "rgb(43, 95, 42)", color: "rgb(255, 255, 255)",
                  paddingTop: "14px", paddingBottom: "14px", paddingLeft: "28px", paddingRight: "28px",
                  borderTopLeftRadius: "8px", borderTopRightRadius: "8px", borderBottomRightRadius: "8px", borderBottomLeftRadius: "8px" } }),
    rich({ tag: "a", classes: ["btn", "btn--secondary"], href: "#more", text: "Learn more", bbox: { x: 120, y: 180, w: 180, h: 52 },
      computed: { display: "inline-flex", backgroundColor: "rgba(0, 0, 0, 0)", color: "rgb(35, 40, 38)",
                  borderTopWidth: "1px", borderRightWidth: "1px", borderBottomWidth: "1px", borderLeftWidth: "1px",
                  borderTopStyle: "solid", borderTopColor: "rgb(35, 40, 38)",
                  paddingTop: "14px", paddingBottom: "14px", paddingLeft: "28px", paddingRight: "28px" } }),
    rich({ tag: "span", classes: ["card__more"], bbox: { x: 120, y: 264, w: 130, h: 20 },
      computed: { display: "inline-flex", color: "rgb(43, 95, 42)", columnGap: "6px" },
      children: [
        rich({ tag: "span", text: "See service", bbox: { x: 120, y: 264, w: 80, h: 20 }, computed: { color: "rgb(43, 95, 42)" } }),
        rich({ tag: "img", imgSrc: "assets/arrow.png", bbox: { x: 206, y: 268, w: 13, h: 13 } }),
      ] }),
    rich({ tag: "a", classes: ["hero__link"], href: "#", text: "Read more", bbox: { x: 120, y: 320, w: 110, h: 22 }, computed: { color: "rgb(246, 246, 244)" } }),
  ],
}) };
const golden = buildIR(goldenCapture, brandMap, { source: "prototypes/controls.html", breakpoint: "lg", brandConfig: "example" }).ir;

console.log("Schema — the produced controls golden declares v0.4 and validates:");
ok(golden.$schema === "heyhi-scene-graph/v0.4", "$schema === heyhi-scene-graph/v0.4");
mkdirSync(resolve(here, "examples"), { recursive: true });
const goldenPath = resolve(here, "examples/controls.lg.ir.json");
writeFileSync(goldenPath, JSON.stringify(golden, null, 2) + "\n");
const validator = resolve(here, "schema/validate_ir.py");
function py(args, label, testOut) {
  try {
    const outp = execFileSync("python3", args, { encoding: "utf8" });
    ok(testOut(outp), label);
  } catch (e) {
    const combined = String((e.stdout || "") + (e.stderr || "") + (e.message || ""));
    if (/No module named ['"]?jsonschema|command not found|ENOENT/.test(combined)) console.log("  SKIP " + label + " (python3/jsonschema unavailable)");
    else ok(false, label + " — got:\n" + combined);
  }
}
py([validator, goldenPath], "validate_ir.py PASS on controls.lg.ir.json (v0.4)", (o) => /^PASS /m.test(o));

// ---- WS2 geometry gate — the controls golden stays clean (no overflow / white space) ----
console.log("WS2 — assert_geometry stays clean on the controls golden:");
py([resolve(here, "scripts/run_build.py"), "self-test", goldenPath], "run_build.py self-test PASS (geometry clean)", (o) => /SELF-TEST: PASS/.test(o) && /geometry: PASS/.test(o));

console.log("\n" + (fail === 0 ? "ALL PASS" : "FAILURES") + ` — ${pass} passed, ${fail} failed`);
process.exit(fail === 0 ? 0 : 1);
