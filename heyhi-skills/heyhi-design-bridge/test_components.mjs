// test_components.mjs — unit tests for design-bridge packet components-path (WS5 C0; no
// Playwright, no Figma). Exercises the builder-side componentization in build_figma.py:
//   A grid of 6 identical-signature cards (icon + kicker + title + summary, varying text)
//   collapses to ONE frame_component master + 6 instance_component instances carrying each
//   card's TEXT property values; a 7th card with an extra badge has a different signature,
//   so it stays an independent frame (never dropped). A 4-item Values group collapses the
//   same way (1 master + 4 instances). A 2-item run is below the >=3 group threshold and
//   builds as 2 independent frames.
//
//   node test_components.mjs
//
// buildIR is imported from the staged components-path copy (deployed skill untouched). The
// IR stays plain frames — componentization is builder-only (plan.json), so the golden
// validates under the UNCHANGED v0.4 schema. The rich() factory follows test_controls.mjs.
// Labels are neutral fixtures (no client name, no geography) per the hermetic seal.

import { buildIR } from "./scripts/extract_scene_graph/lib/build-ir.mjs";
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";

let pass = 0, fail = 0;
function ok(cond, msg) { if (cond) { pass++; console.log("  PASS " + msg); } else { fail++; console.log("  FAIL " + msg); } }

const here = dirname(fileURLToPath(import.meta.url));
// A neutral brandMap: no token binds (the golden carries literal colours). The card
// title's heading token_ref comes from the clamp() font-size recovery in build-ir, not
// from the brand map, so the role-gate still fires.
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
    backgroundColor: "rgba(0, 0, 0, 0)", backgroundImage: "none", backgroundSize: "auto", color: "rgb(35, 40, 38)",
    fontFamily: "Sora", fontWeight: "400", fontSize: "16px", lineHeight: "normal", letterSpacing: "normal",
    paddingTop: "0px", paddingRight: "0px", paddingBottom: "0px", paddingLeft: "0px",
    ...(over.computed || {}),
  };
  return {
    tag: over.tag || "div", id: over.id || null, classes: over.classes || [], dataAudit: null,
    role: over.role || null, href: over.href || null,
    bbox: over.bbox || { x: 0, y: 0, w: 100, h: 20 }, computed: c,
    declared: { color: null, backgroundColor: null, fontSize: null, padding: null, gap: null, borderColor: null, animation: null, ...(over.declared || {}) },
    pseudo: { before: null, after: null },
    font: { family: "Sora", generic: false, brand: true, loaded: true },
    svgOuter: over.svgOuter || null, imgSrc: over.imgSrc || null, text: over.text || null,
    isFlexOrGrid: false, hasAbsChild: over.hasAbsChild || false, children: over.children || [],
  };
}
const meta = { viewport: { w: 1440, h: 1100 }, rootSelector: "body", fontsReady: "loaded", ruleCount: 0 };
const ICON = "<svg viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M4 4h16v16H4z\"/></svg>";

// one content card: icon (VECTOR) + kicker + title (h3 + clamp -> heading token_ref) + summary.
// `extra` adds a child so the varied card breaks the run's signature.
function card(kicker, title, summary, extra) {
  const kids = [
    rich({ tag: "svg", classes: ["icon"], svgOuter: ICON, bbox: { x: 0, y: 0, w: 40, h: 40 } }),
    rich({ tag: "span", classes: ["kicker"], text: kicker, bbox: { x: 0, y: 0, w: 48, h: 16 },
           computed: { fontSize: "13px", color: "rgb(120, 120, 120)" } }),
    rich({ tag: "h3", classes: ["title"], text: title, bbox: { x: 0, y: 0, w: 288, h: 30 },
           computed: { fontSize: "24px", fontWeight: "600", color: "rgb(35, 40, 38)" },
           declared: { fontSize: "clamp(1.25rem, 2vw, 1.5rem)" } }),
    rich({ tag: "p", classes: ["summary"], text: summary, bbox: { x: 0, y: 0, w: 288, h: 60 },
           computed: { fontSize: "15px", color: "rgb(70, 70, 70)" } }),
  ];
  if (extra) kids.push(extra);
  return rich({
    tag: "article", classes: ["card"], bbox: { x: 0, y: 0, w: 336, h: 232 },
    computed: { display: "flex", flexDirection: "column", backgroundColor: "rgb(255, 255, 255)", rowGap: "12px",
                paddingTop: "24px", paddingRight: "24px", paddingBottom: "24px", paddingLeft: "24px",
                borderTopLeftRadius: "12px", borderTopRightRadius: "12px", borderBottomRightRadius: "12px", borderBottomLeftRadius: "12px" },
    children: kids,
  });
}
function grid(cards, w = 1072, h = 760) {
  return rich({
    tag: "div", classes: ["grid"], bbox: { x: 120, y: 96, w, h },
    computed: { display: "grid", gridTemplateColumns: "341.33px 341.33px 341.33px", columnGap: "24px", rowGap: "32px" },
    children: cards,
  });
}

// Build the IR, run the staged builder, return the parsed op-plan (no Figma).
function buildPlan(rootNode, name, source, maxNodes) {
  const ir = buildIR({ meta, root: rootNode }, brandMap, { source, breakpoint: "lg", brandConfig: "example" }).ir;
  const outDir = "/tmp/cards-component-" + name;
  mkdirSync(outDir, { recursive: true });
  const irPath = resolve(outDir, name + ".ir.json");
  writeFileSync(irPath, JSON.stringify(ir, null, 2) + "\n");
  const argv = [resolve(here, "scripts/build_figma.py"), irPath, "--out-dir", outDir];
  if (maxNodes) argv.push("--max-nodes", String(maxNodes));
  execFileSync("python3", argv, { encoding: "utf8" });
  const plan = JSON.parse(readFileSync(resolve(outDir, "plan.json"), "utf8"));
  return { ir, irPath, outDir, plan, ops: plan.chunks.flatMap((c) => c.ops) };
}
function py(args, label, testOut) {
  try { ok(testOut(execFileSync("python3", args, { encoding: "utf8" })), label); }
  catch (e) {
    const combined = String((e.stdout || "") + (e.stderr || "") + (e.message || ""));
    if (/No module named ['"]?jsonschema|command not found|ENOENT/.test(combined)) console.log("  SKIP " + label + " (python3/jsonschema unavailable)");
    else ok(false, label + " — got:\n" + combined);
  }
}

// ---------- GOLDEN: a 6-card grid + a 7th varied card (extra badge) ----------
const titles = ["Strategy Sprint", "Systems Audit", "Build Partnership", "Care Retainer", "Workshop Series", "Theme Studio"];
const kickers = ["01", "02", "03", "04", "05", "06"];
const summaries = [
  "Map the system before a line of code is written.",
  "A structured read of design-code drift and token health.",
  "Build the infrastructure your team owns and extends.",
  "Ongoing iteration, monitoring, and monthly care.",
  "Hands-on sessions that leave the craft with the team.",
  "Marketplace-ready themes from the design pipeline.",
];
const sixCards = titles.map((t, i) => card(kickers[i], t, summaries[i]));
const varied = card("07", "Discovery Call", "A short call to see whether the fit is real.",
  rich({ tag: "span", classes: ["badge"], text: "New", bbox: { x: 0, y: 0, w: 40, h: 18 }, computed: { fontSize: "12px", color: "rgb(43, 95, 42)" } }));
const goldenRoot = rich({
  tag: "section", classes: ["services"], bbox: { x: 0, y: 0, w: 1312, h: 952 },
  computed: { display: "block", paddingTop: "96px", paddingRight: "120px", paddingBottom: "96px", paddingLeft: "120px" },
  children: [grid([...sixCards, varied])],
});

const g = buildPlan(goldenRoot, "cards-component", "prototypes/cards-component.html");
const frameComps = g.ops.filter((o) => o.op === "frame_component");
const instComps = g.ops.filter((o) => o.op === "instance_component");
const independentCards = g.ops.filter((o) => o.op === "frame" && o.name === "Card");

console.log("WS5 — a 6-card repeat-run collapses to 1 master + 6 instances; the varied card stays independent:");
ok(frameComps.length === 1, "exactly 1 frame_component master emitted");
ok(instComps.length === 6, "exactly 6 instance_component instances emitted");
ok(independentCards.length === 1, "the varied (extra-badge) card stays 1 independent frame (not dropped, not componentized)");

console.log("WS5 — the master carries 3 TEXT props (kicker, title, summary); the icon is baked (C2 swaps it):");
const props = (frameComps[0] || {}).props || [];
ok(props.length === 3, "frame_component carries exactly 3 TEXT props");
ok(props.every((p) => p.type === "TEXT"), "every prop is type TEXT");
ok(props.some((p) => p.name === "Title"), "a heading prop is named 'Title'");
ok(props.some((p) => p.name === "Kicker"), "the kicker is a prop named 'Kicker'");
ok(props.some((p) => p.name === "Summary"), "the summary is a prop named 'Summary'");

console.log("WS5 — each prop slot has a path into the master subtree, and a default = the first card's text:");
ok(props.every((p) => Array.isArray(p.path) && p.path.length >= 1), "every prop carries a non-empty path into the master subtree");
const titleProp = props.find((p) => p.name === "Title");
ok(titleProp && titleProp.default === "Strategy Sprint", "the Title prop default is the first card's title");

console.log("WS5 — each instance's values carry that card's kicker/title/summary:");
ok(instComps.every((i) => i.values && Object.keys(i.values).length === 3), "every instance carries 3 property values");
const instanceTitles = instComps.map((i) => (titleProp ? i.values[titleProp.id] : null));
ok(JSON.stringify(instanceTitles) === JSON.stringify(titles), "the 6 instances' Title values equal the 6 card titles, in order");
ok(instComps[0].values[titleProp.id] === "Strategy Sprint" && Object.values(instComps[0].values).includes("01"),
   "instance 0 carries its own title + kicker");

console.log("WS5 — instances reference the master by key (compute_needs can thread it across chunks):");
ok(instComps.every((i) => i.component === (frameComps[0] || {}).key), "every instance references the master component key");

// ---------- flags: a component master's baked content must not silently drop review flags ----------
// buildPlan() writes the IR to a fresh tmp dir with no materialized svg assets, so the
// grouped cards' icon (baked from member 0 into the master template) is genuinely
// unresolvable in this build context, same as the varied (ungrouped) card's own icon --
// the flat path has always flagged that one correctly, so a naive "does the flag string
// appear at all" check can't tell a fixed extract_component from a broken one (the varied
// card's flag alone makes it appear). collapse_flags groups same-feature flags into ONE
// display row with an "xN" count suffix, so the real signal is the FLAGS total: 2 (one
// clamp-calc-derived + one missing-vector-asset) if the master's flag is dropped, 3 if
// both the varied card's AND the master's missing-vector-asset flags survive.
console.log("WS5 — a component master's baked content (e.g. the group's icon) surfaces its build_node_op flag, not silently:");
{
  const summary = execFileSync("python3", [resolve(here, "scripts/build_figma.py"), g.irPath, "--summary"], { encoding: "utf8" });
  const totalMatch = summary.match(/^FLAGS \((\d+) total, (\d+) distinct\)/m);
  ok(totalMatch !== null, "the --summary output has a FLAGS (N total, M distinct) header");
  const total = totalMatch ? Number(totalMatch[1]) : -1;
  ok(total === 3, `FLAGS total is 3 (1 clamp-calc-derived + 2 missing-vector-asset: varied card + group master), got ${total}`);
  ok(/missing-vector-asset\]\s+x2\b/.test(summary), "missing-vector-asset is reported x2 (collapsed from the varied card's flat flag + the group master's baked-content flag), not silently dropped for the componentized one");
}

// ---------- schema: the plain-frame golden validates under the UNCHANGED v0.4 schema ----------
console.log("Schema — the components golden is plain frames and validates under v0.4 (no schema change):");
ok(g.ir.$schema === "heyhi-scene-graph/v0.4", "$schema === heyhi-scene-graph/v0.4");
mkdirSync(resolve(here, "examples"), { recursive: true });
const goldenPath = resolve(here, "examples/cards-component.lg.ir.json");
writeFileSync(goldenPath, JSON.stringify(g.ir, null, 2) + "\n");
py([resolve(here, "schema/validate_ir.py"), goldenPath], "validate_ir.py PASS on cards-component.lg.ir.json (v0.4)", (o) => /^PASS /m.test(o));

// ---------- self-test: ordering, threading, pruning-safety, geometry (default + forced multi-chunk) ----------
console.log("WS5 — run_build.py self-test PASS (dedup-integrity + pruning + geometry), incl. forced multi-chunk:");
const runner = resolve(here, "scripts/run_build.py");
py([runner, "self-test", goldenPath], "self-test PASS (default chunking)", (o) => /SELF-TEST: PASS/.test(o) && /geometry: PASS/.test(o));
py([runner, "self-test", goldenPath, "--max-nodes", "3"], "self-test PASS (--max-nodes 3 forces master/instances across chunks)", (o) => /SELF-TEST: PASS/.test(o));

// ---------- Values group: 4 identical-structure values -> 1 master + 4 instances ----------
console.log("WS5 — a 4-item Values group collapses to 1 master + 4 instances (2 TEXT props):");
function value(heading, body) {
  return rich({
    tag: "li", classes: ["value"], bbox: { x: 0, y: 0, w: 280, h: 160 },
    computed: { display: "flex", flexDirection: "column", rowGap: "8px" },
    children: [
      rich({ tag: "svg", classes: ["mark"], svgOuter: ICON, bbox: { x: 0, y: 0, w: 32, h: 32 } }),
      rich({ tag: "h4", classes: ["heading"], text: heading, bbox: { x: 0, y: 0, w: 240, h: 26 },
             computed: { fontSize: "20px", fontWeight: "600" }, declared: { fontSize: "clamp(1.1rem, 1.6vw, 1.25rem)" } }),
      rich({ tag: "p", classes: ["body"], text: body, bbox: { x: 0, y: 0, w: 240, h: 60 }, computed: { fontSize: "15px", color: "rgb(70, 70, 70)" } }),
    ],
  });
}
const valuesRoot = rich({
  tag: "ul", classes: ["values"], bbox: { x: 0, y: 0, w: 280, h: 700 },
  computed: { display: "flex", flexDirection: "column", rowGap: "24px" },
  children: [
    value("Provider-agnostic", "Built to run with Claude today and swap any provider later."),
    value("Earn the room", "Nothing gets access, context, or authority by default."),
    value("Evaluate first", "No agent ships without passing trajectory and outcome tests."),
    value("Protocols at boundaries", "An interface earns its cost only when it crosses one."),
  ],
});
const v = buildPlan(valuesRoot, "values-group", "prototypes/values.html");
ok(v.ops.filter((o) => o.op === "frame_component").length === 1, "1 frame_component master for the 4 values");
ok(v.ops.filter((o) => o.op === "instance_component").length === 4, "4 instance_component instances for the 4 values");
const vMaster = v.ops.find((o) => o.op === "frame_component");
ok(vMaster && vMaster.props && vMaster.props.length === 2, "the values master carries 2 TEXT props (heading + body)");

// ---------- below threshold: a 2-item run stays 2 independent frames (no component) ----------
console.log("WS5 — a 2-card run is below the >=3 threshold and stays 2 independent frames:");
const twoRoot = rich({
  tag: "div", classes: ["pair"], bbox: { x: 0, y: 0, w: 696, h: 232 },
  computed: { display: "flex", flexDirection: "row", columnGap: "24px" },
  children: [card("01", "First", "Only two of these."), card("02", "Second", "Below the threshold.")],
});
const two = buildPlan(twoRoot, "two-cards", "prototypes/two.html");
ok(two.ops.filter((o) => o.op === "frame_component").length === 0, "no frame_component master for a 2-item run");
ok(two.ops.filter((o) => o.op === "instance_component").length === 0, "no instance_component instances for a 2-item run");
ok(two.ops.filter((o) => o.op === "frame" && o.name === "Card").length === 2, "both cards build as independent frames");

// ---------- duplicate property display-names get uniquified (Figma requires unique) ----------
console.log("WS5 — two same-named varying slots get unique property names (no silent slot drop):");
function dupCard(a, b, c) {
  return rich({
    tag: "article", classes: ["card"], bbox: { x: 0, y: 0, w: 336, h: 200 },
    computed: { display: "flex", flexDirection: "column", backgroundColor: "rgb(255, 255, 255)", rowGap: "12px",
                paddingTop: "24px", paddingRight: "24px", paddingBottom: "24px", paddingLeft: "24px" },
    children: [
      rich({ tag: "h3", classes: ["title"], text: a, bbox: { x: 0, y: 0, w: 288, h: 30 },
             computed: { fontSize: "24px", fontWeight: "600" }, declared: { fontSize: "clamp(1.25rem, 2vw, 1.5rem)" } }),
      rich({ tag: "p", classes: ["note"], text: b, bbox: { x: 0, y: 0, w: 288, h: 20 }, computed: { fontSize: "14px" } }),
      rich({ tag: "p", classes: ["note"], text: c, bbox: { x: 0, y: 0, w: 288, h: 20 }, computed: { fontSize: "14px" } }),
    ],
  });
}
const dupRoot = rich({
  tag: "div", classes: ["grid"], bbox: { x: 0, y: 0, w: 1072, h: 300 },
  computed: { display: "grid", gridTemplateColumns: "341.33px 341.33px 341.33px", columnGap: "24px", rowGap: "24px" },
  children: [dupCard("Alpha", "a1", "a2"), dupCard("Beta", "b1", "b2"), dupCard("Gamma", "c1", "c2")],
});
const dup = buildPlan(dupRoot, "dup-names", "prototypes/dup.html");
const dupMaster = dup.ops.find((o) => o.op === "frame_component");
const dupNames = (dupMaster ? dupMaster.props : []).map((p) => p.name);
ok(dupMaster && dupMaster.props.length === 3, "3 props (title + two same-class notes)");
ok(new Set(dupNames).size === dupNames.length, "all property display names are unique: " + JSON.stringify(dupNames));

// ====================================================================================
// C1 — broaden the role-gate beyond heading cards: chips/tags (pill shape), interactive
// controls (button/cta labels), and reviews/FAQ (heading-bearing). A boxless wrapper row
// stays independent (the conservative line).
// ====================================================================================

// ---------- C1: a chip/tag row (pill shape, no heading) componentizes ----------
console.log("C1 — a >=3 chip row collapses to 1 master + N instances (1 TEXT prop):");
function chip(label) {
  return rich({
    tag: "span", classes: ["chip"], text: label, bbox: { x: 0, y: 0, w: 128, h: 36 },
    computed: { display: "inline-flex", backgroundColor: "rgb(240, 240, 240)", color: "rgb(40, 40, 40)",
                paddingTop: "8px", paddingBottom: "8px", paddingLeft: "16px", paddingRight: "16px",
                borderTopLeftRadius: "18px", borderTopRightRadius: "18px", borderBottomRightRadius: "18px", borderBottomLeftRadius: "18px" },
  });
}
const chipsRoot = rich({
  tag: "div", classes: ["chips"], bbox: { x: 0, y: 0, w: 600, h: 96 },
  computed: { display: "flex", flexWrap: "wrap", columnGap: "8px", rowGap: "8px" },
  children: ["Provider-agnostic", "Earn the room", "Evaluate first", "Protocols at boundaries"].map(chip),
});
const cr = buildPlan(chipsRoot, "chips-row", "prototypes/chips.html");
ok(cr.ops.filter((o) => o.op === "frame_component").length === 1, "1 frame_component master for the chip row (pill gate)");
ok(cr.ops.filter((o) => o.op === "instance_component").length === 4, "4 instance_component instances for the 4 chips");
const crMaster = cr.ops.find((o) => o.op === "frame_component");
ok(crMaster && crMaster.props.length === 1, "the chip master carries 1 TEXT prop (the label)");

// ---------- C1: a button row (interactive control label) componentizes ----------
console.log("C1 — a >=3 button row collapses to 1 master + N instances (Label prop):");
function button(label) {
  return rich({
    tag: "a", classes: ["btn", "btn--primary"], href: "#", text: label, bbox: { x: 0, y: 0, w: 200, h: 48 },
    computed: { display: "inline-flex", backgroundColor: "rgb(43, 95, 42)", color: "rgb(255, 255, 255)",
                paddingTop: "12px", paddingBottom: "12px", paddingLeft: "24px", paddingRight: "24px",
                borderTopLeftRadius: "8px", borderTopRightRadius: "8px", borderBottomRightRadius: "8px", borderBottomLeftRadius: "8px" },
  });
}
const btnRoot = rich({
  tag: "div", classes: ["actions"], bbox: { x: 0, y: 0, w: 680, h: 48 },
  computed: { display: "flex", columnGap: "16px" },
  children: ["Get started", "Learn more", "Book a call"].map(button),
});
const br = buildPlan(btnRoot, "button-row", "prototypes/buttons.html");
ok(br.ops.filter((o) => o.op === "frame_component").length === 1, "1 frame_component master for the button row (control gate)");
ok(br.ops.filter((o) => o.op === "instance_component").length === 3, "3 instance_component instances for the 3 buttons");
const brMaster = br.ops.find((o) => o.op === "frame_component");
ok(brMaster && brMaster.props.some((p) => p.name === "Label"), "the button label prop is named 'Label'");

// ---------- C1: a FAQ/review list (heading-bearing) componentizes ----------
console.log("C1 — a >=3 FAQ list (heading question + answer) collapses to 1 master + N instances:");
function faq(q, a) {
  return rich({
    tag: "div", classes: ["faq-item"], bbox: { x: 0, y: 0, w: 640, h: 120 },
    computed: { display: "flex", flexDirection: "column", rowGap: "8px",
                borderTopWidth: "1px", borderTopStyle: "solid", borderTopColor: "rgb(220, 220, 220)" },
    children: [
      rich({ tag: "h3", classes: ["question"], text: q, bbox: { x: 0, y: 0, w: 640, h: 28 },
             computed: { fontSize: "20px", fontWeight: "600" }, declared: { fontSize: "clamp(1.1rem, 1.5vw, 1.25rem)" } }),
      rich({ tag: "p", classes: ["answer"], text: a, bbox: { x: 0, y: 0, w: 640, h: 60 }, computed: { fontSize: "15px" } }),
    ],
  });
}
const faqRoot = rich({
  tag: "div", classes: ["faq"], bbox: { x: 0, y: 0, w: 640, h: 400 },
  computed: { display: "flex", flexDirection: "column", rowGap: "0px" },
  children: [
    faq("What does Consult cover?", "Workshops, audits, and strategy."),
    faq("What does Build cover?", "MCP servers and design-system infrastructure."),
    faq("What does Sustain cover?", "Recurring retainers, monitoring, iteration."),
  ],
});
const fq = buildPlan(faqRoot, "faq-list", "prototypes/faq.html");
ok(fq.ops.filter((o) => o.op === "frame_component").length === 1, "1 frame_component master for the FAQ list");
ok(fq.ops.filter((o) => o.op === "instance_component").length === 3, "3 instance_component instances for the 3 FAQ items");
ok((fq.ops.find((o) => o.op === "frame_component") || {}).props.length === 2, "the FAQ master carries 2 TEXT props (question + answer)");

// ---------- C1: conservative — a boxless wrapper row is NOT componentized ----------
console.log("C1 — a >=3 boxless wrapper row stays independent frames (conservative gate):");
const boxlessRoot = rich({
  tag: "div", classes: ["rows"], bbox: { x: 0, y: 0, w: 400, h: 160 },
  computed: { display: "flex", flexDirection: "column", rowGap: "8px" },
  children: [["a", "Alpha"], ["b", "Bravo"], ["c", "Charlie"]].map(([cls, t]) =>
    rich({ tag: "div", classes: [cls], bbox: { x: 0, y: 0, w: 400, h: 40 }, computed: { display: "flex" },
           children: [rich({ tag: "span", text: t, bbox: { x: 0, y: 0, w: 120, h: 20 } })] })),
});
const bl = buildPlan(boxlessRoot, "boxless-rows", "prototypes/rows.html");
ok(bl.ops.filter((o) => o.op === "frame_component").length === 0, "no frame_component master for boxless (no fill/stroke/radius) wrapper frames");
ok(bl.ops.filter((o) => o.op === "instance_component").length === 0, "no instances for boxless wrapper frames (not a pill, not a card)");

// ====================================================================================
// C2 — INSTANCE_SWAP icons: a card run whose per-card ICON svg varies becomes an
// INSTANCE_SWAP component property (the icon swaps per instance) while the TEXT still
// flows as TEXT props. This path MATERIALIZES the extractor's svg asset files so svgRef
// resolves (unlike buildPlan above, which leaves them missing to exercise the baked-flag
// path). Identical icons stay baked inline — no swap prop.
// ====================================================================================
function buildPlanMaterialized(rootNode, name, source) {
  const built = buildIR({ meta, root: rootNode }, brandMap, { source, breakpoint: "lg", brandConfig: "example" });
  const ir = built.ir;
  const outDir = "/tmp/cards-component-" + name;
  mkdirSync(outDir, { recursive: true });
  for (const a of built.assets || []) {              // materialize each VECTOR svg on disk
    const p = resolve(outDir, a.file);
    mkdirSync(dirname(p), { recursive: true });
    writeFileSync(p, a.content);
  }
  const irPath = resolve(outDir, name + ".ir.json");
  writeFileSync(irPath, JSON.stringify(ir, null, 2) + "\n");
  execFileSync("python3", [resolve(here, "scripts/build_figma.py"), irPath, "--out-dir", outDir], { encoding: "utf8" });
  const plan = JSON.parse(readFileSync(resolve(outDir, "plan.json"), "utf8"));
  return { ir, irPath, outDir, assets: built.assets || [], plan, ops: plan.chunks.flatMap((c) => c.ops) };
}
function iconSvg(d) { return `<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="${d}"/></svg>`; }
function cardIcon(icon, kicker, title, summary) {
  return rich({
    tag: "article", classes: ["card"], bbox: { x: 0, y: 0, w: 336, h: 232 },
    computed: { display: "flex", flexDirection: "column", backgroundColor: "rgb(255, 255, 255)", rowGap: "12px",
                paddingTop: "24px", paddingRight: "24px", paddingBottom: "24px", paddingLeft: "24px",
                borderTopLeftRadius: "12px", borderTopRightRadius: "12px", borderBottomRightRadius: "12px", borderBottomLeftRadius: "12px" },
    children: [
      rich({ tag: "svg", classes: ["icon"], svgOuter: icon, bbox: { x: 0, y: 0, w: 40, h: 40 } }),
      rich({ tag: "span", classes: ["kicker"], text: kicker, bbox: { x: 0, y: 0, w: 48, h: 16 }, computed: { fontSize: "13px", color: "rgb(120, 120, 120)" } }),
      rich({ tag: "h3", classes: ["title"], text: title, bbox: { x: 0, y: 0, w: 288, h: 30 },
             computed: { fontSize: "24px", fontWeight: "600", color: "rgb(35, 40, 38)" }, declared: { fontSize: "clamp(1.25rem, 2vw, 1.5rem)" } }),
      rich({ tag: "p", classes: ["summary"], text: summary, bbox: { x: 0, y: 0, w: 288, h: 60 }, computed: { fontSize: "15px", color: "rgb(70, 70, 70)" } }),
    ],
  });
}

console.log("C2 — 6 cards with VARYING icons: the icon becomes an INSTANCE_SWAP prop (TEXT stays TEXT):");
const iconPaths = ["M4 4h16v16H4z", "M12 2l10 20H2z", "M12 2a10 10 0 100 20 10 10 0 000-20z",
                   "M3 12h18M12 3v18", "M4 20L20 4M4 4l16 16", "M12 2l3 7h7l-6 4 2 7-6-4-6 4 2-7-6-4h7z"];
const swapCards = titles.map((t, i) => cardIcon(iconSvg(iconPaths[i]), kickers[i], t, summaries[i]));
const swapRoot = rich({
  tag: "section", classes: ["services"], bbox: { x: 0, y: 0, w: 1312, h: 952 },
  computed: { display: "block", paddingTop: "96px", paddingRight: "120px", paddingBottom: "96px", paddingLeft: "120px" },
  children: [grid(swapCards)],
});
const sw = buildPlanMaterialized(swapRoot, "cards-icon-swap", "prototypes/cards-icon-swap.html");
const swMaster = sw.ops.find((o) => o.op === "frame_component");
const swInst = sw.ops.filter((o) => o.op === "instance_component");
const svgMasters = sw.ops.filter((o) => o.op === "component");
ok(swMaster != null, "a frame_component master is emitted for the 6 varying-icon cards");
ok(swInst.length === 6, "6 instance_component instances emitted");
const swProps = (swMaster || {}).props || [];
const swapProps = swProps.filter((p) => p.type === "INSTANCE_SWAP");
const textProps = swProps.filter((p) => p.type === "TEXT");
ok(swapProps.length === 1, "the master carries exactly 1 INSTANCE_SWAP prop (the icon): " + swapProps.length);
ok(textProps.length === 3, "the master still carries 3 TEXT props (kicker/title/summary): " + textProps.length);
ok(svgMasters.length === 6, "6 distinct svg component masters emitted (one per distinct icon): " + svgMasters.length);
const iconProp = swapProps[0] || {};
ok(/^comp_/.test(String(iconProp.default)), "the INSTANCE_SWAP default is an svg component key: " + iconProp.default);
ok(swInst.every((i) => Array.isArray(i.swaps) && i.swaps.includes(iconProp.id)), "every instance names the icon prop id in its `swaps` list");
const swapVals = swInst.map((i) => i.values[iconProp.id]);
ok(swapVals.every((v) => /^comp_/.test(String(v))), "every instance's swap value is an svg component key");
ok(new Set(swapVals).size === 6, "the 6 instances swap to 6 DISTINCT svg components (icons vary): " + new Set(swapVals).size);
const svgKeys = new Set(svgMasters.map((m) => m.key));
ok(swapVals.every((v) => svgKeys.has(v)) && svgKeys.has(iconProp.default), "every swap value + the default reference a real emitted svg master (dedup-integrity)");

console.log("C2 — 6 cards with the SAME icon stay baked (no INSTANCE_SWAP prop even when the svg resolves):");
const sameCards = titles.map((t, i) => cardIcon(ICON, kickers[i], t, summaries[i]));
const sameRoot = rich({
  tag: "section", classes: ["services"], bbox: { x: 0, y: 0, w: 1312, h: 952 },
  computed: { display: "block", paddingTop: "96px", paddingRight: "120px", paddingBottom: "96px", paddingLeft: "120px" },
  children: [grid(sameCards)],
});
const same = buildPlanMaterialized(sameRoot, "cards-same-icon", "prototypes/cards-same-icon.html");
const sameMaster = same.ops.find((o) => o.op === "frame_component");
ok(sameMaster != null, "a frame_component master is emitted for the identical-icon cards");
ok(((sameMaster || {}).props || []).every((p) => p.type === "TEXT"), "no INSTANCE_SWAP prop — the shared icon is baked into the master");
ok(same.ops.filter((o) => o.op === "component").length === 0, "the shared icon is baked inline in the master (0 separate svg component ops — it rides the master's single copy)");

// ---------- golden + self-test for the swap path (committed, real assets) ----------
console.log("C2 — the swap golden validates (v0.4) and run_build self-test passes (swap threading + integrity + geometry):");
ok(sw.ir.$schema === "heyhi-scene-graph/v0.4", "$schema === heyhi-scene-graph/v0.4 (builder-only; no schema change)");
const swapGoldenPath = resolve(here, "examples/cards-icon-swap.lg.ir.json");
writeFileSync(swapGoldenPath, JSON.stringify(sw.ir, null, 2) + "\n");
for (const a of sw.assets) {              // commit the icon svgs so the self-test resolves them (real swap path)
  const p = resolve(here, "examples", a.file);
  mkdirSync(dirname(p), { recursive: true });
  writeFileSync(p, a.content.endsWith("\n") ? a.content : a.content + "\n");  // newline-terminated (end-of-file-fixer hook)
}
py([resolve(here, "schema/validate_ir.py"), swapGoldenPath], "validate_ir.py PASS on cards-icon-swap.lg.ir.json (v0.4)", (o) => /^PASS /m.test(o));
py([resolve(here, "scripts/run_build.py"), "self-test", swapGoldenPath], "self-test PASS on the swap golden (default chunking)", (o) => /SELF-TEST: PASS/.test(o) && /geometry: PASS/.test(o));
py([resolve(here, "scripts/run_build.py"), "self-test", swapGoldenPath, "--max-nodes", "3"], "self-test PASS (--max-nodes 3 threads svg masters/card master/instances + swap refs across chunks)", (o) => /SELF-TEST: PASS/.test(o));

// ---------- C2 edge: dedup WITHIN a varying swap group (two cards share an icon) ----------
console.log("C2 — a varying-icon group where two cards share an icon dedups the shared svg, swap stays correct:");
const dupIcons = [iconPaths[0], iconPaths[1], iconPaths[0], iconPaths[2], iconPaths[3], iconPaths[4]]; // cards 0 & 2 share
const dupIconCards = titles.map((t, i) => cardIcon(iconSvg(dupIcons[i]), kickers[i], t, summaries[i]));
const dupIconRoot = rich({
  tag: "section", classes: ["services"], bbox: { x: 0, y: 0, w: 1312, h: 952 },
  computed: { display: "block", paddingTop: "96px", paddingRight: "120px", paddingBottom: "96px", paddingLeft: "120px" },
  children: [grid(dupIconCards)],
});
const di = buildPlanMaterialized(dupIconRoot, "cards-dup-icon", "prototypes/cards-dup-icon.html");
const diMaster = di.ops.find((o) => o.op === "frame_component");
const diSwapProp = ((diMaster || {}).props || []).find((p) => p.type === "INSTANCE_SWAP") || {};
const diVals = di.ops.filter((o) => o.op === "instance_component").map((i) => i.values[diSwapProp.id]);
ok(diSwapProp.id != null, "an INSTANCE_SWAP prop exists for the varying group");
ok(di.ops.filter((o) => o.op === "component").length === 5, "5 svg masters for 6 cards (the shared icon dedups once): " + di.ops.filter((o) => o.op === "component").length);
ok(diVals[0] === diVals[2] && diVals[0] !== diVals[1], "cards 0 & 2 swap to the SAME svg component; card 1 differs");
ok(new Set(diVals).size === 5, "5 distinct swap values across 6 instances: " + new Set(diVals).size);

console.log("\n" + (fail === 0 ? "ALL PASS" : "FAILURES") + ` — ${pass} passed, ${fail} failed`);
process.exit(fail === 0 ? 0 : 1);
