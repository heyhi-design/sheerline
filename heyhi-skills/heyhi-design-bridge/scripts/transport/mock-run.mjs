// HeyHi Design Bridge — headless proof of the plugin transport.
//
// Runs a generated plugin code.js (from emit_plugin.py) against a mock of the Figma
// Plugin API in Node's vm. Proves the bundling transform is sound — every chunk
// parses, wraps, and runs as an async function; ids thread across chunks via the
// in-memory idmap; the raster embed path executes — WITHOUT needing Figma desktop.
// This de-risks the one human-initiated Figma run. The real createNodeFromSvg /
// GradientPaint fidelity is proven on the live file; this proves the plumbing.
//
// What this mock CANNOT see (read the README instrument table before trusting a PASS):
//   - LAYOUT. It records resize() but computes no auto-layout: FILL/HUG resolution, the
//     circular constraint, and the createFrame fallback are invisible here. Geometry is
//     proven live by figma_readback.py, not by this mock.
//   - FONTS (defect I3). The built-in registry below disagrees with real Figma in both
//     directions (it lacks e.g. Inter Bold, which exists), so a bare run's
//     missing-font-style flags are NOISE indistinguishable from signal. Pass a real
//     `--fonts` dump to make them trustworthy, or the run reports fonts as NOT CHECKED
//     rather than emitting a verdict it cannot stand behind. The font GATE is
//     preflight_fonts.py; this only surfaces what a judged registry would say.
//
// Usage: node mock-run.mjs <plugin-dir>/code.js [--fonts <listAvailableFontsAsync.json>]
//   --fonts   a JSON dump of the target workspace's fonts (the same shape
//             preflight_fonts.py consumes: [{fontName:{family,style}}], a plain
//             [{family,style}] list, or {fonts:[...]}). Produce it in Figma with:
//               figma.listAvailableFontsAsync().then(f => console.log(JSON.stringify(f)))
//             Also read from the MOCK_FONT_DUMP env var when the flag is absent.
//
// HeyHi Confidential.
import vm from 'node:vm';
import fs from 'node:fs';

const argv = process.argv.slice(2);
let fontDumpPath = null;
const fi = argv.indexOf('--fonts');
if (fi >= 0 && argv[fi + 1]) fontDumpPath = argv[fi + 1];
if (!fontDumpPath && process.env.MOCK_FONT_DUMP) fontDumpPath = process.env.MOCK_FONT_DUMP;
// The code path is the first positional arg that is neither a flag nor the value that
// follows --fonts, so `--fonts dump code.js` and `code.js --fonts dump` both work.
// Guard on fi >= 0: with no --fonts, fi is -1 and fi+1 (0) must NOT exclude arg 0.
const codePath = argv.find((a, i) => !a.startsWith('--') && !(fi >= 0 && i === fi + 1));
if (!codePath) {
  console.error('usage: node mock-run.mjs <code.js> [--fonts <listAvailableFontsAsync.json>]');
  process.exit(2);
}
const code = fs.readFileSync(codePath, 'utf8');

// The mock's built-in registry — kept only as the plumbing default. It is deliberately
// partial (defect I3): it is NOT the real Figma catalogue, so font flags raised against
// it are not judgeable. A `--fonts` dump replaces it with the real catalogue.
const BUILTIN_FONTS = [
  { fontName: { family: 'Sora', style: 'Regular' } }, { fontName: { family: 'Sora', style: 'Bold' } },
  { fontName: { family: 'Sora', style: 'SemiBold' } }, { fontName: { family: 'Lora', style: 'Regular' } },
  { fontName: { family: 'Lora', style: 'Italic' } }, { fontName: { family: 'Lora', style: 'Bold' } },
  { fontName: { family: 'DM Mono', style: 'Regular' } }, { fontName: { family: 'DM Mono', style: 'Medium' } },
  { fontName: { family: 'Inter', style: 'Regular' } },
];
let availableFonts = BUILTIN_FONTS;
let fontsJudged = false;   // true only when a real --fonts dump is loaded
if (fontDumpPath) {
  try {
    let data = JSON.parse(fs.readFileSync(fontDumpPath, 'utf8'));
    if (data && !Array.isArray(data) && Array.isArray(data.fonts)) data = data.fonts;
    if (!Array.isArray(data)) throw new Error('not a list of fonts');
    availableFonts = data
      .map((e) => {
        const fn = (e && e.fontName && typeof e.fontName === 'object') ? e.fontName : e;
        return { fontName: { family: String((fn && fn.family) || '').trim(), style: String((fn && fn.style) || '').trim() } };
      })
      .filter((e) => e.fontName.family);
    if (!availableFonts.length) throw new Error('named no (family, style) faces');
    fontsJudged = true;
  } catch (e) {
    console.error('mock-run: cannot load --fonts ' + fontDumpPath + ': ' + ((e && e.message) || e));
    process.exit(2);
  }
}

let ID = 0;
const registry = {};

function makeNode(type) {
  const store = {
    id: 'n' + (++ID), type, name: '', children: [], width: 100, height: 100,
    x: 0, y: 0, fills: [], strokes: [], effects: [], opacity: 1, visible: true, parent: null,
    characters: '', fontName: { family: 'Sora', style: 'Regular' }, fontSize: 16, layoutMode: 'NONE',
  };
  const methods = {
    appendChild: (c) => { store.children.push(c); if (c) { try { c.parent = proxy; } catch (e) {} } },
    insertChild: (i, c) => { store.children.splice(i, 0, c); },
    resize: (w, h) => { store.width = w; store.height = h; },
    resizeWithoutConstraints: (w, h) => { store.width = w; store.height = h; },
    rescale: (s) => { store.width *= s; store.height *= s; },
    remove: () => {},
    clone: () => makeNode(type),
    createInstance: () => { const inst = makeNode('INSTANCE'); inst.__master = proxy; return inst; },
    setRangeFills: () => {}, setRangeFontName: () => {}, setRangeFontSize: () => {},
    setRangeLetterSpacing: () => {}, setRangeLineHeight: () => {}, setRangeTextDecoration: () => {},
    setRangeTextCase: () => {}, setBoundVariable: () => {}, setValueForMode: () => {},
  };
  const handler = {
    get(t, p) {
      if (typeof p === 'symbol') return store[p];
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
  const c = { id: 'col' + (++ID), name, defaultModeId: 'mode1', modes: [{ modeId: 'mode1', name: 'Mode 1' }], variableIds: [] };
  registry[c.id] = c; return c;
}
function makeVariable(name, col, vtype) {
  const v = { id: 'var' + (++ID), name, resolvedType: vtype, setValueForMode: () => {} };
  if (col && col.variableIds) col.variableIds.push(v.id);
  registry[v.id] = v; return v;
}

const messages = [];
const page0 = makeNode('PAGE'); page0.name = 'Page 1';
const figma = {
  editorType: 'figma',
  mixed: Symbol('figma.mixed'),
  root: { children: [page0] },
  currentPage: page0,
  createPage: () => { const p = makeNode('PAGE'); figma.root.children.push(p); return p; },
  createFrame: () => makeNode('FRAME'),
  createText: () => makeNode('TEXT'),
  createRectangle: () => makeNode('RECTANGLE'),
  createComponentFromNode: (n) => makeNode('COMPONENT'),
  createNodeFromSvg: (svg) => { const f = makeNode('FRAME'); f.appendChild(makeNode('VECTOR')); f.resize(64, 64); return f; },
  createImage: (bytes) => ({ hash: 'img' + (++ID), getSizeAsync: async () => ({ width: 1200, height: 800 }) }),
  base64Decode: (b64) => new Uint8Array(Buffer.from(b64, 'base64')),
  getNodeByIdAsync: async (id) => registry[id] || null,
  loadFontAsync: async () => {},
  listAvailableFontsAsync: async () => availableFonts,
  setCurrentPageAsync: async (p) => { figma.currentPage = p; },
  notify: () => {},
  showUI: () => {},
  ui: { postMessage: (m) => { messages.push(m); }, onmessage: null },
  variables: {
    createVariableCollection: (name) => makeCollection(name),
    createVariable: (name, col, vtype) => makeVariable(name, col, vtype),
    getLocalVariableCollectionsAsync: async () => [],
    getVariableByIdAsync: async (id) => registry[id] || null,
    setBoundVariableForPaint: (paint, field, v) => paint,
  },
};

const sandbox = { figma, __html__: '<ui/>', console };
vm.createContext(sandbox);
vm.runInContext(code, sandbox, { filename: 'code.js' });

if (typeof figma.ui.onmessage !== 'function') { console.error('FAIL: code.js did not register figma.ui.onmessage'); process.exit(1); }
await figma.ui.onmessage({ type: 'run' });

const summary = (messages.filter((m) => m.type === 'summary').pop() || {}).summary;
if (!summary) { console.error('FAIL: no summary message emitted'); process.exit(1); }

// Font-availability flags are only trustworthy when judged against a real catalogue
// (defect I3). Split them out so a bare run never presents noise as a finding.
const FONT_FEATURES = new Set(['missing-font-style', 'missing-font-family']);
const fontFlags = summary.flags.filter((f) => f && FONT_FEATURES.has(f.feature));
const otherFlags = summary.flags.filter((f) => !(f && FONT_FEATURES.has(f.feature)));

const featCount = {};
for (const f of otherFlags) { const k = (f && f.feature) || '?'; featCount[k] = (featCount[k] || 0) + 1; }

const pass = summary.errors.length === 0 && summary.created > 0;
console.log('MOCK-RUN: ' + (pass ? 'PASS' : 'FAIL') + '   (plumbing only: ops execute — NOT a geometry or font gate)');
console.log('  created: ' + summary.created + '   reused: ' + summary.reused + '   rasters: ' + (summary.rasters || 0));
console.log('  flags:   ' + otherFlags.length + '   errors: ' + summary.errors.length);
console.log('  pages:   ' + summary.pages.length + '   registry nodes: ' + Object.keys(registry).length);
for (const [k, n] of Object.entries(featCount)) console.log('    flag ' + n + 'x ' + k);
for (const e of summary.errors.slice(0, 15)) console.log('    ERROR ' + JSON.stringify(e));

// Font availability — reported as a verdict ONLY when judged against a real dump.
if (fontsJudged) {
  const faces = {};
  for (const f of fontFlags) { const k = (f && f.node) || '?'; faces[k] = (faces[k] || 0) + 1; }
  console.log('  fonts:   CHECKED against ' + availableFonts.length + ' real face(s) (--fonts) — ' +
    (fontFlags.length === 0
      ? 'every requested face resolves; no substitution'
      : fontFlags.length + ' substitution(s), ' + Object.keys(faces).length + ' distinct face(s)'));
  for (const [face, cnt] of Object.entries(faces)) {
    console.log('    absent ' + cnt + 'x ' + face + '  (not in the dump — preflight_fonts.py is the loud gate)');
  }
} else {
  console.log('  fonts:   NOT CHECKED — the built-in registry disagrees with real Figma in both directions ' +
    '(it lacks e.g. Inter Bold, which exists), so ' + fontFlags.length + ' missing-font flag(s) are');
  console.log('           unjudgeable and suppressed. Pass --fonts <listAvailableFontsAsync dump> to judge, ' +
    'or run preflight_fonts.py (the gate).');
}

process.exit(pass ? 0 : 1);
