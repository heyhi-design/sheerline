// mock-run-components.mjs — headless proof of the WS5 component path through the REAL
// interpreter (the three live JS handlers have no other automated coverage). Runs a
// generated plugin code.js (emit_plugin.py over the staged cards golden chunks) against a
// mock Figma API that ACTUALLY implements the component surface — createComponentFromNode
// preserving children, addComponentProperty, componentPropertyReferences, setPluginData/
// getPluginData, createInstance, setProperties, loadFontAsync ordering — and asserts the
// master/instance/property behaviour. This de-risks the one human-initiated live Figma run
// (WS6); real Figma component fidelity is still confirmed live.
//
// Usage: node mock-run-components.mjs <plugin-dir>/code.js
//
// HeyHi Confidential.
import vm from "node:vm";
import fs from "node:fs";

const codePath = process.argv[2];
if (!codePath) { console.error("usage: node mock-run-components.mjs <code.js>"); process.exit(2); }
const code = fs.readFileSync(codePath, "utf8");

let ID = 0, PID = 0;
const registry = {};
const components = [];   // every createComponentFromNode result (the masters)
const instances = [];    // every createInstance result
const fontsLoaded = [];  // ordered loadFontAsync calls (to prove font-before-setProperties)

function makeNode(type) {
  const store = {
    id: "n" + (++ID), type, name: "", children: [], width: 100, height: 100,
    x: 0, y: 0, fills: [], strokes: [], effects: [], opacity: 1, visible: true, parent: null,
    characters: "", fontName: { family: "Sora", style: "Regular" }, fontSize: 16, layoutMode: "NONE",
    componentPropertyReferences: null, componentPropertyDefinitions: {}, _plugin: {}, _setProps: null, __master: null,
  };
  const methods = {
    appendChild: (c) => { store.children.push(c); if (c) { try { c.parent = proxy; } catch (e) {} } },
    insertChild: (i, c) => { store.children.splice(i, 0, c); },
    resize: (w, h) => { store.width = w; store.height = h; },
    resizeWithoutConstraints: (w, h) => { store.width = w; store.height = h; },
    rescale: (s) => { store.width *= s; store.height *= s; },
    remove: () => {},
    clone: () => makeNode(type),
    // Component master surface
    addComponentProperty: (name, ptype, def) => {
      const key = name + "#" + (++PID);                  // Figma returns "<name>#<suffix>"
      store.componentPropertyDefinitions[key] = { type: ptype, defaultValue: def, name };
      return key;
    },
    createInstance: () => {
      const inst = makeNode("INSTANCE");
      inst.__master = proxy;                              // remember which master (for assertions)
      instances.push(inst);
      return inst;
    },
    setProperties: (obj) => { store._setProps = Object.assign({}, store._setProps || {}, obj); },
    setPluginData: (k, v) => { store._plugin[k] = v; },
    getPluginData: (k) => (k in store._plugin ? store._plugin[k] : ""),
    setRangeFills: () => {}, setRangeFontName: () => {}, setRangeFontSize: () => {},
    setRangeLetterSpacing: () => {}, setRangeLineHeight: () => {}, setRangeTextDecoration: () => {},
    setRangeTextCase: () => {}, setBoundVariable: () => {}, setValueForMode: () => {},
  };
  const handler = {
    get(t, p) {
      if (typeof p === "symbol") return store[p];
      if (p in methods) return methods[p];
      if (p in store) return store[p];
      return undefined;
    },
    set(t, p, v) { store[p] = v; return true; },
    has(t, p) { return (p in store) || (p in methods); },
  };
  const proxy = new Proxy(store, handler);
  registry[store.id] = proxy;
  return proxy;
}

function makeCollection(name) {
  const c = { id: "col" + (++ID), name, defaultModeId: "mode1", modes: [{ modeId: "mode1", name: "Mode 1" }], variableIds: [] };
  registry[c.id] = c; return c;
}
function makeVariable(name, col, vtype) {
  const v = { id: "var" + (++ID), name, resolvedType: vtype, setValueForMode: () => {} };
  if (col && col.variableIds) col.variableIds.push(v.id);
  registry[v.id] = v; return v;
}

const messages = [];
const page0 = makeNode("PAGE"); page0.name = "Page 1";
const figma = {
  editorType: "figma",
  mixed: Symbol("figma.mixed"),
  root: { children: [page0] },
  currentPage: page0,
  createPage: () => { const p = makeNode("PAGE"); figma.root.children.push(p); return p; },
  createFrame: () => makeNode("FRAME"),
  createText: () => makeNode("TEXT"),
  createRectangle: () => makeNode("RECTANGLE"),
  // createComponentFromNode must PRESERVE the node's children (the built master subtree),
  // so the WS5 path navigation `comp.children[ix]` reaches the real slot text nodes.
  createComponentFromNode: (n) => {
    const comp = makeNode("COMPONENT");
    if (n) { comp.children = n.children; comp.name = n.name; comp.width = n.width; comp.height = n.height; }
    components.push(comp);
    return comp;
  },
  createNodeFromSvg: (svg) => { const f = makeNode("FRAME"); f.appendChild(makeNode("VECTOR")); f.resize(64, 64); return f; },
  createImage: (bytes) => ({ hash: "img" + (++ID), getSizeAsync: async () => ({ width: 1200, height: 800 }) }),
  base64Decode: (b64) => new Uint8Array(Buffer.from(b64, "base64")),
  getNodeByIdAsync: async (id) => registry[id] || null,
  loadFontAsync: async (fn) => { fontsLoaded.push(fn); },
  listAvailableFontsAsync: async () => [
    { fontName: { family: "Sora", style: "Regular" } }, { fontName: { family: "Sora", style: "Bold" } },
    { fontName: { family: "Sora", style: "SemiBold" } }, { fontName: { family: "Lora", style: "Regular" } },
    { fontName: { family: "Inter", style: "Regular" } },
  ],
  setCurrentPageAsync: async (p) => { figma.currentPage = p; },
  notify: () => {}, showUI: () => {},
  ui: { postMessage: (m) => { messages.push(m); }, onmessage: null },
  variables: {
    createVariableCollection: (name) => makeCollection(name),
    createVariable: (name, col, vtype) => makeVariable(name, col, vtype),
    getLocalVariableCollectionsAsync: async () => [],
    getVariableByIdAsync: async (id) => registry[id] || null,
    setBoundVariableForPaint: (paint) => paint,
  },
};

const sandbox = { figma, __html__: "<ui/>", console };
vm.createContext(sandbox);
vm.runInContext(code, sandbox, { filename: "code.js" });
if (typeof figma.ui.onmessage !== "function") { console.error("FAIL: code.js did not register figma.ui.onmessage"); process.exit(1); }
await figma.ui.onmessage({ type: "run" });

const summary = (messages.filter((m) => m.type === "summary").pop() || {}).summary;
if (!summary) { console.error("FAIL: no summary message emitted"); process.exit(1); }

// ---- assertions on the WS5 component path ----
let pass = 0, fail = 0;
function ok(c, m) { if (c) { pass++; console.log("  PASS " + m); } else { fail++; console.log("  FAIL " + m); } }

const expectTitles = ["Strategy Sprint", "Systems Audit", "Build Partnership", "Care Retainer", "Workshop Series", "Theme Studio"];
const expectKickers = ["01", "02", "03", "04", "05", "06"];

console.log("MOCK-RUN (WS5 component path through the real interpreter):");
ok(summary.errors.length === 0, "the plugin run produced 0 errors (" + summary.errors.length + ")");

// The CARD master is the component that declared properties; svg dedup masters (the C2 swap
// targets) declare none — so this harness works for BOTH the cards golden (1 component, baked
// icon) and the icon-swap golden (N svg masters + 1 card master).
const cardMasters = components.filter((c) => Object.keys(c.componentPropertyDefinitions).length > 0);
ok(cardMasters.length === 1, "exactly 1 CARD master declared properties (createComponentFromNode): " + cardMasters.length);
const master = cardMasters[0] || components[0];
const defs = master ? master.componentPropertyDefinitions : {};
const defList = Object.values(defs);
const textDefs = defList.filter((d) => d.type === "TEXT");
const swapDefs = defList.filter((d) => d.type === "INSTANCE_SWAP");
const defNames = defList.map((d) => d.name);
ok(textDefs.length === 3, "the master declared 3 TEXT component properties: " + JSON.stringify(textDefs.map((d) => d.name)));
ok(defNames.includes("Title") && defNames.includes("Kicker") && defNames.includes("Summary"), "TEXT properties include Kicker/Title/Summary");

// componentPropertyReferences.characters wired onto 3 slot text nodes (navigated by path)
function slots(n, acc) { if (n && n.componentPropertyReferences && n.componentPropertyReferences.characters) acc.push(n); (n && n.children || []).forEach((c) => slots(c, acc)); }
const wired = []; if (master) slots(master, wired);
ok(wired.length === 3, "3 slot text nodes carry componentPropertyReferences.characters: " + wired.length);
ok(wired.every((n) => n.type === "TEXT"), "every wired text slot is a TEXT node");

// plugin-data round-trip the instances rely on (cross-chunk safe)
const propMap = master ? JSON.parse(master.getPluginData("heyhiCompProps") || "{}") : {};
const fontList = master ? JSON.parse(master.getPluginData("heyhiCompFonts") || "[]") : [];
ok(Object.keys(propMap).length === defList.length, "master persisted heyhiCompProps (prop_id -> Figma key) for all " + defList.length + " props");
ok(fontList.length >= 1, "master persisted heyhiCompFonts so an instance can load fonts before setProperties: " + JSON.stringify(fontList));

// CARD instances = those whose master is the card master (excludes the master's own baked/
// swap icon-slot instance). Each is setProperties'd with that card's values.
const cardInstances = instances.filter((i) => i.__master === master);
ok(cardInstances.length === 6, "exactly 6 CARD instances created (createInstance): " + cardInstances.length);
const keyToName = {}; for (const [k, d] of Object.entries(defs)) keyToName[k] = d.name;
const gotTitles = [], gotKickers = [];
for (const inst of cardInstances) {
  const sp = inst._setProps || {};
  for (const [pkey, val] of Object.entries(sp)) {
    if (keyToName[pkey] === "Title") gotTitles.push(val);
    if (keyToName[pkey] === "Kicker") gotKickers.push(val);
  }
}
ok(cardInstances.every((i) => i._setProps && Object.keys(i._setProps).length === defList.length), "every instance received " + defList.length + " property values via setProperties");
ok(JSON.stringify(gotTitles) === JSON.stringify(expectTitles), "the 6 instances' Title values equal the 6 card titles, in order");
ok(JSON.stringify(gotKickers) === JSON.stringify(expectKickers), "the 6 instances' Kicker values equal 01..06, in order");
ok(fontsLoaded.length > 0, "fonts were loaded during the run (ensureFont path exercised)");

// ---- C2: INSTANCE_SWAP path (only when the golden carries a swap prop) ----
if (swapDefs.length > 0) {
  console.log("MOCK-RUN (C2 INSTANCE_SWAP path through the real interpreter):");
  ok(swapDefs.length === 1, "the master declared exactly 1 INSTANCE_SWAP property (the icon)");
  const swapKey = Object.keys(defs).find((k) => defs[k].type === "INSTANCE_SWAP");
  const swapSlots = []; (function find(n) { if (n && n.componentPropertyReferences && n.componentPropertyReferences.mainComponent) swapSlots.push(n); (n && n.children || []).forEach(find); })(master);
  ok(swapSlots.length === 1 && swapSlots[0].type === "INSTANCE", "the master's icon slot is an INSTANCE bound via componentPropertyReferences.mainComponent");
  ok(swapSlots[0] && swapSlots[0].componentPropertyReferences.mainComponent === swapKey, "the icon slot's mainComponent points at the swap property key");
  // svg dedup masters (0-prop components) are the swap targets; each card instance swapped
  // its icon to a REAL svg component node id, resolved from the comp_ key by the interpreter.
  const svgCompIds = new Set(components.filter((c) => Object.keys(c.componentPropertyDefinitions).length === 0).map((c) => c.id));
  const swapVals = cardInstances.map((i) => (i._setProps || {})[swapKey]);
  ok(swapVals.every((v) => svgCompIds.has(v)), "every instance swapped its icon to a real svg component node id (comp_ key resolved to a node id)");
  ok(new Set(swapVals).size === 6, "the 6 instances swapped to 6 DISTINCT svg components: " + new Set(swapVals).size);
}

console.log("\n" + (fail === 0 ? "MOCK-RUN: PASS" : "MOCK-RUN: FAIL") + " — " + pass + " passed, " + fail + " failed");
console.log("  plugin summary: created " + summary.created + ", reused " + summary.reused + ", flags " + summary.flags.length + ", errors " + summary.errors.length);
process.exit(fail === 0 ? 0 : 1);
