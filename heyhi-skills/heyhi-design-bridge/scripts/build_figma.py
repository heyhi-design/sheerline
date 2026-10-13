#!/usr/bin/env python3
"""
HeyHi Design Bridge — Builder (IR -> chunked use_figma op-plan).

Reads a scene-graph IR (schema/scene-graph.schema.json) and emits an ordered set
of `use_figma` chunks. Each chunk is a self-contained JavaScript payload: a fixed
interpreter plus a compact OPS array and an __IDMAP__ placeholder the runner fills
with node ids returned by earlier chunks. This is the "compact data array + builder
loop" shape the Phase-T2 spike found necessary (the real per-call ceiling is the
50,000-character code cap, not execution; see spike-T2-findings.md).

The script is the deterministic, testable writer: it transforms a reviewed IR into
a build plan without opening Figma. The runner (the agent) issues each chunk via
use_figma in order, threading the returned id map forward.

Usage:
    python3 build_figma.py <ir.json> [options]

Options:
    --type-mode {set-direct,bind}  Typography handling. set-direct (default) writes
                                   type values directly and annotates token_ref.
                                   bind also binds typography to Figma Variables.
    --rerun {replace,version}      Re-run contract. replace (default) clears and
                                   rebuilds the build page; version writes a new
                                   "<page> vN" page.
    --max-nodes N                  Node ops per chunk (default 60). Lower it to force
                                   multi-chunk builds for cross-call testing.
    --page-name NAME               Override the build page name (the stable re-run key).
    --x N / --y N                  Mockup origin on the page (default 0,0).
    --out-dir DIR                  Where chunk_<n>.js files are written
                                   (default /tmp/heyhi-bridge-build). Throwaway.

Output:
    Writes chunk_<n>.js into --out-dir and prints a compact JSON manifest to stdout:
    { type_mode, rerun, page_name, chunk_count, out_dir,
      chunks: [ {index, description, needs:[keys], node_count, code_file} ] }

HeyHi Confidential.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

# --------------------------------------------------------------------------------------
# The use_figma chunk interpreter (fixed JS, identical in every chunk).
# Reads OPS + IDMAP (both injected above it) and returns JSON.stringify(out).
# --------------------------------------------------------------------------------------
INTERPRETER_JS = r"""
const out = { created: {}, reused: {}, flags: [], errors: [], pageId: null, pageName: null };
const made = {};
let _fontCache = null;

function hexToRgb(hex) {
  hex = String(hex || '#000000').replace('#', '');
  if (hex.length === 3) hex = hex.split('').map(c => c + c).join('');
  return { r: parseInt(hex.slice(0,2),16)/255, g: parseInt(hex.slice(2,4),16)/255, b: parseInt(hex.slice(4,6),16)/255 };
}
async function resolveNode(ref) {
  if (ref in made) return made[ref];
  if (IDMAP[ref]) { const n = await figma.getNodeByIdAsync(IDMAP[ref]); if (n) return n; }
  throw new Error('unresolved node ref: ' + ref);
}
async function resolveVar(key) {
  if (made[key]) return made[key];
  if (IDMAP[key]) return await figma.variables.getVariableByIdAsync(IDMAP[key]);
  throw new Error('unresolved var: ' + key);
}
async function ensureFont(family, style) {
  if (!_fontCache) _fontCache = await figma.listAvailableFontsAsync();
  const fam = _fontCache.filter(f => f.fontName.family === family);
  if (fam.length === 0) {
    out.flags.push({ feature: 'missing-font-family', node: family, action: 'fell back to Inter Regular', needs_human: true });
    await figma.loadFontAsync({ family: 'Inter', style: 'Regular' });
    return { family: 'Inter', style: 'Regular' };
  }
  let hit = fam.find(f => f.fontName.style === style);
  let chosen;
  if (hit) {
    chosen = hit.fontName;
  } else {
    chosen = (fam.find(f => f.fontName.style === 'Regular') || fam[0]).fontName;
    out.flags.push({ feature: 'missing-font-style', node: family + ' ' + style, action: 'used ' + chosen.style, needs_human: true });
  }
  await figma.loadFontAsync(chosen);
  return chosen;
}
// P4 (Gap 4c): the Figma font-style name for an inline run, from its weight/italic
// relative to the run's family. ensureFont falls back gracefully if the exact style
// is absent, so an unusual weight/italic combination degrades rather than throwing.
const _W2S = { 100: 'Thin', 200: 'ExtraLight', 300: 'Light', 400: 'Regular', 500: 'Medium', 600: 'SemiBold', 700: 'Bold', 800: 'ExtraBold', 900: 'Black' };
function figmaStyleName(weight, italic, base) {
  let name = base || 'Regular';
  if (typeof weight === 'number') { const w = Math.max(100, Math.min(900, Math.round(weight / 100) * 100)); name = _W2S[w] || 'Regular'; }
  if (italic) name = (name === 'Regular') ? 'Italic' : name + ' Italic';
  return name;
}
// Apply inline styled ranges over a text node's characters. Each run is
// {start, end, fill?, style?}: fill -> setRangeFills (binds like a fill), style ->
// setRangeFontName (+ optional size). Offsets are clamped to the characters length
// so a stale offset never throws.
async function applyRuns(t, op) {
  if (!op.runs || !op.runs.length) return;
  const len = (op.characters || '').length;
  for (const r of op.runs) {
    const s = Math.max(0, r.start | 0), e = Math.min(len, r.end | 0);
    if (e <= s) continue;
    try {
      if (r.style) {
        const fam = r.style.family || op.family;
        const fn = await ensureFont(fam, figmaStyleName(r.style.weight, r.style.italic, op.style));
        t.setRangeFontName(s, e, fn);
        if (typeof r.style.size === 'number') { try { t.setRangeFontSize(s, e, r.style.size); } catch (e2) {} }
      }
      if (r.fill) {
        let paint = { type: 'SOLID', color: hexToRgb(r.fill.resolved || '#000000') };
        if (r.fill.bind) {
          try { const v = await resolveVar('var:' + r.fill.bind); paint = figma.variables.setBoundVariableForPaint(paint, 'color', v); }
          catch (err) { out.errors.push({ key: op.key, field: 'run-fill:' + r.fill.bind, error: String(err && err.message || err) }); }
        }
        t.setRangeFills(s, e, [paint]);
      }
    } catch (err) { out.errors.push({ key: op.key, field: 'run', error: String(err && err.message || err) }); }
  }
}
// CSS gradient angle -> Figma gradientTransform (a 2x3 affine matrix
// [[a,c,tx],[b,d,ty]]). Figma reads each stop's position along the X axis of
// gradient space, where a point p in the node's normalized UV box (each axis
// 0..1) maps to gradient space via M·[px,py,1]. We want stop value (g.x) to grow
// along the CSS gradient direction.
//   CSS angle: 0deg points UP, increases CLOCKWISE; the canvas is y-DOWN.
//   So the unit direction is d = (sin θ, -cos θ):  90deg->(1,0) right,
//   180deg->(0,1) down, 0deg->(0,-1) up.
// g.x = d·(p - center) + 0.5  centers the gradient line on the box, giving
//   row0 = [dx, dy, 0.5 - 0.5*dx - 0.5*dy].
// row1 is the perpendicular axis (unused for stop reads but needed for a valid
// 2x3): [-dy, dx, 0.5 + 0.5*dy - 0.5*dx].
// Caveat: CSS scales the gradient line so it touches the box corners at off-axis
// angles; this centered unit projection is the faithful, widely-used
// approximation (cardinal angles are exact). Verified against the cardinals in
// the unit test.
function cssAngleToGradientTransform(deg) {
  const t = ((Number(deg) || 0) * Math.PI) / 180;
  const dx = Math.sin(t), dy = -Math.cos(t);
  const r = (n) => Math.round(n * 1e6) / 1e6; // kill float fuzz on the cardinals
  return [
    [r(dx), r(dy), r(0.5 - 0.5 * dx - 0.5 * dy)],
    [r(-dy), r(dx), r(0.5 + 0.5 * dy - 0.5 * dx)],
  ];
}
function gradientStops(stops) {
  // IR stops are {pos:0..1, color:'rgba(..)'|'#..'}; Figma wants
  // {position, color:{r,g,b,a}}. Sort by position so Figma gets monotonic stops.
  const ss = (stops || []).map(s => {
    const c = parseColor(s.color || '#000000');
    return { position: Math.max(0, Math.min(1, (s.pos != null ? s.pos : 0))),
             color: { r: c.r, g: c.g, b: c.b, a: (c.a != null ? c.a : 1) } };
  });
  ss.sort((a, b) => a.position - b.position);
  return ss.length ? ss : [{ position: 0, color: { r: 0, g: 0, b: 0, a: 1 } },
                            { position: 1, color: { r: 0, g: 0, b: 0, a: 1 } }];
}
async function applyFills(node, fills) {
  if (!fills || !fills.length) return;
  const paints = [];
  for (const f of fills) {
    // P3 (ADR-013): an image fill is a first-class f.type === 'IMAGE'. The legacy
    // kind:"IMAGE" (P2's stopgap, when v0.2's fill.type enum was closed) is still
    // accepted so a pre-migration IR keeps building.
    const isImage = f.type === 'IMAGE' || f.kind === 'IMAGE';
    const type = f.type || 'SOLID';
    let paint;
    if (!isImage && (type === 'GRADIENT_LINEAR' || type === 'GRADIENT_RADIAL')) {
      paint = { type, gradientStops: gradientStops(f.stops),
                gradientTransform: cssAngleToGradientTransform(f.angle != null ? f.angle : 180) };
      // A radial gradient ignores the linear angle; the centered transform places
      // it from the box centre, which is the right default.
      if (type === 'GRADIENT_RADIAL') paint.gradientTransform = cssAngleToGradientTransform(0);
    } else if (isImage) {
      // Raster embed path (chunk-budget follow-on): the full-res bytes are landed by
      // the Figma MCP `upload_assets` tool (POST raw bytes; nodeId sets a cover FILL),
      // NOT inline figma.createImage(base64). A base64 data string near the 50k cap is
      // not reliably shuttled by the agent, so the inline embed is retired for rasters.
      // We do NOT stage an IMAGE paint here (a hashless IMAGE paint is invalid); the
      // node keeps a visible placeholder until run_build.py's assets manifest drives the
      // upload_assets call AFTER this chunk records (so the node id exists). Flag it.
      out.flags.push({ feature: 'raster-embed-via-upload_assets', node: node.name,
                       action: 'embed full-res via Figma MCP upload_assets(nodeId, ' + (f.imageRef || '?') + ') — sets a ' + (f.scaleMode || 'FILL') + ' (cover) fill after the chunk records',
                       needs_human: true });
      continue; // image layers are embedded post-write; add no paint for them here
    } else {
      paint = { type, color: hexToRgb(f.resolved || '#000000') };
    }
    if (f.bind && type === 'SOLID' && !isImage) {
      try { const v = await resolveVar('var:' + f.bind); paint = figma.variables.setBoundVariableForPaint(paint, 'color', v); }
      catch (e) { out.errors.push({ key: node.name, field: 'fill:' + f.bind, error: String(e && e.message || e) }); }
    }
    paints.push(paint);
  }
  // Image layers are embedded post-write via upload_assets (the branch above adds no
  // paint), so `paints` holds only ready solid/gradient fills. If filtering left
  // nothing (an image-only node), keep a visible placeholder rather than an empty fill.
  if (paints.length) {
    node.fills = paints;
  } else if (fills.some(f => f.type === 'IMAGE' || f.kind === 'IMAGE')) {
    node.fills = [{ type: 'SOLID', color: { r: 0.85, g: 0.85, b: 0.85 } }];
  }
}
function parseColor(s) {
  s = String(s || '').trim();
  if (s.indexOf('rgb') === 0) {
    const m = s.match(/[\d.]+/g) || [];
    return { r: (+m[0] || 0) / 255, g: (+m[1] || 0) / 255, b: (+m[2] || 0) / 255, a: (m[3] != null ? +m[3] : 1) };
  }
  const h = hexToRgb(s); h.a = 1; return h;
}
async function applyDecorations(node, op) {
  // v0.2 (ADR-010): cornerRadius, strokes, effects, opacity. Each guarded so an
  // unsupported node type degrades quietly rather than killing the chunk.
  if (typeof op.opacity === 'number') { try { node.opacity = op.opacity; } catch (e) {} }
  if (op.cornerRadius != null) {
    try {
      if (typeof op.cornerRadius === 'number') { node.cornerRadius = op.cornerRadius; }
      else { node.topLeftRadius = op.cornerRadius.tl || 0; node.topRightRadius = op.cornerRadius.tr || 0; node.bottomRightRadius = op.cornerRadius.br || 0; node.bottomLeftRadius = op.cornerRadius.bl || 0; }
    } catch (e) {}
  }
  if (op.strokes && op.strokes.length) {
    try {
      const paints = []; let weight = null, align = null;
      for (const s of op.strokes) {
        let paint = { type: 'SOLID', color: parseColor((s.color && s.color.resolved) || '#000000') };
        delete paint.color.a;
        if (s.color && s.color.bind) {
          try { const v = await resolveVar('var:' + s.color.bind); paint = figma.variables.setBoundVariableForPaint(paint, 'color', v); }
          catch (e) { out.errors.push({ key: node.name, field: 'stroke-bind', error: String(e && e.message || e) }); }
        }
        paints.push(paint);
        if (typeof s.weight === 'number') weight = s.weight;
        if (s.align) align = s.align;
      }
      node.strokes = paints;
      if (weight != null) node.strokeWeight = weight;
      if (align) node.strokeAlign = align;
    } catch (e) { out.errors.push({ key: node.name, field: 'strokes', error: String(e && e.message || e) }); }
  }
  if (op.effects && op.effects.length) {
    try {
      node.effects = op.effects.map(e => {
        const c = parseColor((e.color && e.color.resolved) || e.color || 'rgba(0,0,0,0.25)');
        return { type: (e.type === 'INNER_SHADOW' ? 'INNER_SHADOW' : 'DROP_SHADOW'), color: { r: c.r, g: c.g, b: c.b, a: (c.a != null ? c.a : 0.25) }, offset: { x: e.x || 0, y: e.y || 0 }, radius: e.blur || 0, spread: e.spread || 0, visible: true, blendMode: 'NORMAL' };
      });
    } catch (e) { out.errors.push({ key: node.name, field: 'effects', error: String(e && e.message || e) }); }
  }
}

// P3 (ADR-013): apply a child's placement inside a NONE-layout frame — x/y from
// the captured offset, plus stretch constraints for a full-bleed (inset:0) child
// so it fills the parent. In an auto-layout parent, Figma ignores x/y and these
// constraints, so this is safe to call on every node.
function applyPlacement(node, op) {
  if (op.x != null) node.x = op.x;
  if (op.y != null) node.y = op.y;
  if (op.fillParent) {
    try { node.constraints = { horizontal: 'STRETCH', vertical: 'STRETCH' }; } catch (e) {}
  }
}

async function doPage(op) {
  const base = op.name;
  let name = base;
  if (op.rerun === 'version' && figma.root.children.find(p => p.name === base)) {
    let n = 2;
    while (figma.root.children.find(p => p.name === base + ' v' + n)) n++;
    name = base + ' v' + n;
  }
  let page = (op.rerun === 'version') ? null : figma.root.children.find(p => p.name === name);
  if (!page) { page = figma.createPage(); page.name = name; }
  await figma.setCurrentPageAsync(page);
  if (op.rerun === 'replace') { for (const c of [...page.children]) c.remove(); }
  made[op.key] = page; out.created[op.key] = page.id; out.pageId = page.id; out.pageName = name;
}
async function doCollection(op) {
  // Re-run contract (reference.md §5): reuse a collection that already exists by
  // name, else create. Reuse is recorded so the runner can thread its id forward
  // and the report can separate created from reused.
  let col = null;
  try {
    const cols = await figma.variables.getLocalVariableCollectionsAsync();
    col = cols.find(c => c.name === op.name) || null;
  } catch (e) { col = null; }
  if (col) { out.reused[op.key] = col.id; }
  else { col = figma.variables.createVariableCollection(op.name); out.created[op.key] = col.id; }
  made[op.key] = col;
}
async function doVariable(op) {
  const col = made[op.collection];
  let v = null;
  try {
    for (const vid of (col.variableIds || [])) {
      const ex = await figma.variables.getVariableByIdAsync(vid);
      if (ex && ex.name === op.name && ex.resolvedType === op.vtype) { v = ex; break; }
    }
  } catch (e) { v = null; }
  let val = op.value;
  if (op.vtype === 'COLOR') val = hexToRgb(op.value);
  if (v) {
    // Reuse branch: do NOT setValueForMode on a found Variable. A reused canonical
    // Variable (e.g. one authored on a Color foundations page) must not be overwritten
    // by a Translate's low-confidence matched literal (reference.md §5, Canonical-collection
    // reuse hazard). Value is set on create only. Trade-off: a re-run does not auto-update
    // a reused Variable's value — that is now an explicit action, by design.
    out.reused[op.key] = v.id;
  } else {
    v = figma.variables.createVariable(op.name, col, op.vtype);
    out.created[op.key] = v.id;
    try { v.setValueForMode(col.defaultModeId, val); }
    catch (e) { out.errors.push({ key: op.key, field: 'setValue', error: String(e && e.message || e) }); }
  }
  made[op.key] = v;
}
// D1 (plan-design-bridge-geometry-defects-2026-08-24): decide, per real axis
// (width / height), whether it stays AUTO (content-hug) or takes its captured
// dimension (FIXED). The extractor marks sizing.v = "HUG" on EVERY frame, so a blanket
// "never resize a HUG axis" discarded real dimensions and let Figma's 100px createFrame
// default stand (an 8px bar, a 7px dot, a 60px bar all landed 100 tall). A HUG axis is a
// genuine content-hug in exactly two cases: the PRIMARY (main) axis of a container that
// actually has children, and an axis the extractor left dimensionless (w/h null — the
// ADR-014 wrap height). Everywhere else the captured value is authoritative. A leaf hugs
// on neither axis — there is no content to hug to — so its captured box wins outright.
function frameAxisAuto(layoutMode, S, isLeaf) {
  const shug = (S && S.sizing) || {};
  const wIsPrimary = (layoutMode === 'HORIZONTAL');
  const wAuto = wIsPrimary ? (shug.h === 'HUG' && !isLeaf) : (S.w == null);
  const hAuto = wIsPrimary ? (S.h == null) : (shug.v === 'HUG' && !isLeaf);
  return { wAuto: wAuto, hAuto: hAuto };
}
// Apply auto-layout + sizing onto a freshly-created frame from its op. Factored out of
// doFrame so the WS5 component-master builder (buildTemplateNode) applies the identical
// box logic — including the §5a AUTO re-assert that kills over-height white space — to
// every frame in a master subtree. Fills (incl. the WS-A transparent-default) stay in
// each caller: applyFrameBox is box/layout/sizing only.
function applyFrameBox(f, op) {
  const L = op.layout;
  if (L && L.mode && L.mode !== 'NONE') {
    f.layoutMode = L.mode;
    if (L.primaryAxisAlignItems) f.primaryAxisAlignItems = L.primaryAxisAlignItems;
    if (L.counterAxisAlignItems) f.counterAxisAlignItems = L.counterAxisAlignItems;
    if (typeof L.itemSpacing === 'number') f.itemSpacing = L.itemSpacing;
    if (L.padding) { f.paddingTop = L.padding.t || 0; f.paddingRight = L.padding.r || 0; f.paddingBottom = L.padding.b || 0; f.paddingLeft = L.padding.l || 0; }
    // ADR-014: layoutWrap is valid ONLY for HORIZONTAL (Figma throws otherwise).
    // Guarded so an older engine without layoutWrap degrades to a single line
    // rather than killing the chunk.
    if (L.mode === 'HORIZONTAL' && L.layoutWrap) {
      try {
        f.layoutWrap = L.layoutWrap;
        if (L.layoutWrap === 'WRAP') {
          if (typeof L.counterAxisSpacing === 'number') f.counterAxisSpacing = L.counterAxisSpacing;
          if (L.counterAxisAlignContent) f.counterAxisAlignContent = L.counterAxisAlignContent;
        }
      } catch (e) { out.errors.push({ key: op.key, field: 'layoutWrap', error: String(e && e.message || e) }); }
    }
  }
  const S = op.size;
  if (S && (f.layoutMode === 'VERTICAL' || f.layoutMode === 'HORIZONTAL')) {
    // D1 fix: honor a HUG axis as content-hug only where it is genuine (frameAxisAuto);
    // everywhere else the captured dimension is authoritative and the axis is FIXED, so
    // a token-sized leaf no longer inherits Figma's 100px createFrame default.
    const ax = frameAxisAuto(f.layoutMode, S, !!op.leaf);
    const primAuto = (f.layoutMode === 'HORIZONTAL') ? ax.wAuto : ax.hAuto;
    const cntAuto  = (f.layoutMode === 'HORIZONTAL') ? ax.hAuto : ax.wAuto;
    f.primaryAxisSizingMode = primAuto ? 'AUTO' : 'FIXED';
    f.counterAxisSizingMode = cntAuto ? 'AUTO' : 'FIXED';
    // Resize a FIXED axis to its captured dimension (a captured 0 is real, e.g. a flex
    // spacer — Math.max floors it to 0.01, never Figma's default); leave a genuine-hug
    // axis at f.width/height for the AUTO re-assert below to recompute.
    const wArg = (!ax.wAuto && typeof S.w === 'number') ? Math.max(S.w, 0.01) : f.width;
    const hArg = (!ax.hAuto && typeof S.h === 'number') ? Math.max(S.h, 0.01) : f.height;
    if (!ax.wAuto || !ax.hAuto) { try { f.resize(wArg, hArg); } catch (e) {} }
    // The one unresolvable case: a FIXED axis with no captured dimension keeps Figma's
    // default rather than a real value. Never silent — flag it for human review (the
    // plan: "if a genuine fallback is still needed, it must be flagged, not silent").
    if ((!ax.wAuto && typeof S.w !== 'number') || (!ax.hAuto && typeof S.h !== 'number')) {
      out.flags.push({ feature: 'unresolved-frame-size', node: op.name,
        action: 'a sized frame axis had no captured dimension; kept Figma default', needs_human: true });
    }
    // resize() silently flips a sized axis to FIXED (reference.md §5a); re-assert AUTO
    // last so a genuine-hug axis recomputes to its content — this is what kills the
    // over-height white space on every auto-layout container, not just wrap frames.
    try { if (primAuto) f.primaryAxisSizingMode = 'AUTO'; if (cntAuto) f.counterAxisSizingMode = 'AUTO'; } catch (e) {}
  } else if (S) {
    // NONE-layout (absolute) frame: keep the literal captured box. A captured 0 is a real
    // dimension (a zero-height rule/spacer), not "unset" — guard it explicitly so it does
    // not fall through `|| f.width/height` to Figma's 100px default (the same D1 class).
    const w = (typeof S.w === 'number') ? S.w : null;
    const h = (typeof S.h === 'number') ? S.h : null;
    if (w !== null || h !== null) {
      try { f.resize(Math.max(w !== null ? w : f.width, 0.01), Math.max(h !== null ? h : f.height, 0.01)); } catch (e) {}
    }
  }
}
async function doFrame(op) {
  const f = figma.createFrame();
  f.name = op.name;
  applyFrameBox(f, op);
  if (op.fills) await applyFills(f, op.fills);
  else f.fills = []; // WS-A: a frame with no resolved background is transparent (the painted page shows through it), never Figma's default white
  await applyDecorations(f, op);
  applyPlacement(f, op);
  const parent = await resolveNode(op.parent);
  parent.appendChild(f);
  made[op.key] = f; out.created[op.key] = f.id;
}
async function doText(op) {
  const fn = await ensureFont(op.family, op.style);
  const t = figma.createText();
  t.name = op.name;
  t.fontName = fn;
  t.characters = op.characters || '';
  if (typeof op.size === 'number') t.fontSize = op.size;
  if (op.lineHeight) { try { t.lineHeight = op.lineHeight; } catch (e) {} }
  if (op.letterSpacing) { try { t.letterSpacing = op.letterSpacing; } catch (e) {} }
  if (op.fills) await applyFills(t, op.fills);
  await applyDecorations(t, op);
  if (op.bindRefs) {
    for (const field in op.bindRefs) {
      try { const v = await resolveVar(op.bindRefs[field]); t.setBoundVariable(field, v); }
      catch (e) { out.errors.push({ key: op.key, field: field, error: String(e && e.message || e) }); }
    }
  }
  applyPlacement(t, op);
  const parent = await resolveNode(op.parent);
  parent.appendChild(t);
  // Gap 4a: a wrapped text fills its column and auto-heights instead of hugging
  // to one overflowing line. layoutAlign/layoutGrow handle an auto-layout parent;
  // a fixed width handles a non-auto-layout parent.
  if (op.fillH === 'FILL') {
    try {
      if (parent.layoutMode === 'VERTICAL') { t.layoutAlign = 'STRETCH'; t.textAutoResize = 'HEIGHT'; }
      else if (parent.layoutMode === 'HORIZONTAL') { t.layoutGrow = 1; t.textAutoResize = 'HEIGHT'; }
      else if (typeof op.w === 'number') { t.resize(Math.max(op.w, 1), t.height); t.textAutoResize = 'HEIGHT'; }
    } catch (e) { out.errors.push({ key: op.key, field: 'wrap', error: String(e && e.message || e) }); }
  }
  await applyRuns(t, op);
  made[op.key] = t; out.created[op.key] = t.id;
}
async function doVector(op) {
  let node;
  if (!op.svg) {
    out.flags.push({ feature: 'missing-vector-asset', node: op.name, action: 'placeholder rectangle', needs_human: true });
    node = figma.createRectangle();
    node.resize(op.w || 64, op.h || 64);
    node.fills = [{ type: 'SOLID', color: { r: 0.85, g: 0.85, b: 0.85 } }];
  } else {
    try { node = figma.createNodeFromSvg(op.svg); }
    catch (e) { out.errors.push({ key: op.key, error: 'svg import failed: ' + String(e && e.message || e) }); return; }
    // Gap 1: createNodeFromSvg imports at the svg's intrinsic size; scale it to
    // the CSS display width the prototype laid out.
    if (typeof op.w === 'number' && node.width > 0) {
      try { node.rescale(Math.max(op.w, 1) / node.width); } catch (e) {}
    }
  }
  node.name = op.name;
  await applyDecorations(node, op);
  applyPlacement(node, op);
  const parent = await resolveNode(op.parent);
  parent.appendChild(node);
  made[op.key] = node; out.created[op.key] = node.id;
}
async function doImage(op) {
  // A raster image node: a rectangle sized to the image box, carrying an IMAGE
  // fill. applyFills stages the IMAGE paint and flags the embed; the live
  // figma.createImage(bytes) -> imageHash is the gated step (the runner reads the
  // asset and uploads its bytes into the client's own Figma file, then writes the
  // completed paint from the node's heyhiPendingFills plugin data).
  const node = figma.createRectangle();
  node.name = op.name;
  const S = op.size || {};
  const w = (typeof S.w === 'number') ? S.w : 64;
  const h = (typeof S.h === 'number') ? S.h : 64;
  try { node.resize(Math.max(w, 0.01), Math.max(h, 0.01)); } catch (e) {}
  // A visible placeholder fill until the gated embed completes, so the box reads
  // as an image slot rather than vanishing.
  node.fills = [{ type: 'SOLID', color: { r: 0.85, g: 0.85, b: 0.85 } }];
  if (op.fills) await applyFills(node, op.fills);
  await applyDecorations(node, op);
  applyPlacement(node, op);
  const parent = await resolveNode(op.parent);
  parent.appendChild(node);
  made[op.key] = node; out.created[op.key] = node.id;
}
// SVG dedup (chunk-budget follow-on): each UNIQUE svg is imported once as a
// component master (createNodeFromSvg -> createComponentFromNode); every use is a
// lightweight instance referencing it by key. This collapses the payload — a page
// that re-inlined the same ~27KB logo on every use now carries each svg's bytes
// once, so an SVG-heavy page drops from dozens of use_figma chunks to a handful.
async function doComponent(op) {
  let comp;
  try {
    const n = figma.createNodeFromSvg(op.svg);
    comp = figma.createComponentFromNode(n);
  } catch (e) {
    out.flags.push({ feature: 'svg-component-failed', node: op.name, action: 'placeholder component', needs_human: true });
    const r = figma.createRectangle();
    r.resize(op.w || 64, op.h || 64);
    r.fills = [{ type: 'SOLID', color: { r: 0.85, g: 0.85, b: 0.85 } }];
    comp = figma.createComponentFromNode(r);
  }
  comp.name = op.name;
  applyPlacement(comp, op);
  try { const parent = await resolveNode(op.parent); parent.appendChild(comp); } catch (e) {}
  made[op.key] = comp; out.created[op.key] = comp.id;
}
async function doInstance(op) {
  let comp = null;
  try { comp = await resolveNode(op.component); } catch (e) {}
  let node;
  if (comp && typeof comp.createInstance === 'function') {
    node = comp.createInstance();
    // Scale the instance to the CSS display width the prototype laid out. The master
    // is at the svg's intrinsic size; rescale is relative to the instance's current
    // width, so each use can land at its own size from one shared master.
    if (typeof op.w === 'number' && node.width > 0) { try { node.rescale(Math.max(op.w, 1) / node.width); } catch (e) {} }
  } else {
    out.flags.push({ feature: 'instance-component-missing', node: op.name, action: 'placeholder rectangle', needs_human: true });
    node = figma.createRectangle();
    node.resize(op.w || 64, op.h || 64);
    node.fills = [{ type: 'SOLID', color: { r: 0.85, g: 0.85, b: 0.85 } }];
  }
  node.name = op.name;
  await applyDecorations(node, op);
  applyPlacement(node, op);
  const parent = await resolveNode(op.parent);
  parent.appendChild(node);
  made[op.key] = node; out.created[op.key] = node.id;
}
// <WS5-COMPONENT-FUNCS>  (build_figma.py strips this block for component-free chunks
// so an SVG-heavy page keeps the full base-interpreter headroom — Earn the Room.)
// WS5 (components/slots): build one node of a component MASTER's template subtree.
// A template node carries the same op fields doFrame/doText/doVector/doImage read
// (minus key/parent), plus an optional `children` array and a `propId` marker on a
// TEXT slot. Unlike the flat-op path, the master is built as a self-contained tree
// in one op (it is converted to a component, then instanced), so this recurses and
// appends inline rather than threading parents through made[]/IDMAP. Reuses the same
// helpers as the flat path so a master renders identically to inline nodes.
async function buildTemplateNode(tn, parent) {
  let node;
  const k = tn.op;
  if (k === 'text') {
    const fn = await ensureFont(tn.family, tn.style);
    node = figma.createText();
    node.name = tn.name;
    node.fontName = fn;
    node.characters = tn.characters || '';
    if (typeof tn.size === 'number') node.fontSize = tn.size;
    if (tn.lineHeight) { try { node.lineHeight = tn.lineHeight; } catch (e) {} }
    if (tn.letterSpacing) { try { node.letterSpacing = tn.letterSpacing; } catch (e) {} }
    if (tn.fills) await applyFills(node, tn.fills);
    await applyDecorations(node, tn);
    if (parent) parent.appendChild(node);
    // Gap 4a: a wrapped text fills its column and auto-heights (same as doText).
    if (tn.fillH === 'FILL' && parent) {
      try {
        if (parent.layoutMode === 'VERTICAL') { node.layoutAlign = 'STRETCH'; node.textAutoResize = 'HEIGHT'; }
        else if (parent.layoutMode === 'HORIZONTAL') { node.layoutGrow = 1; node.textAutoResize = 'HEIGHT'; }
        else if (typeof tn.w === 'number') { node.resize(Math.max(tn.w, 1), node.height); node.textAutoResize = 'HEIGHT'; }
      } catch (e) {}
    }
    await applyRuns(node, tn);
  } else if (k === 'vector') {
    if (!tn.svg) {
      node = figma.createRectangle(); node.resize(tn.w || 64, tn.h || 64);
      node.fills = [{ type: 'SOLID', color: { r: 0.85, g: 0.85, b: 0.85 } }];
    } else {
      try {
        node = figma.createNodeFromSvg(tn.svg);
        if (typeof tn.w === 'number' && node.width > 0) { try { node.rescale(Math.max(tn.w, 1) / node.width); } catch (e) {} }
      } catch (e) {
        node = figma.createRectangle(); node.resize(tn.w || 64, tn.h || 64);
        node.fills = [{ type: 'SOLID', color: { r: 0.85, g: 0.85, b: 0.85 } }];
      }
    }
    node.name = tn.name;
    await applyDecorations(node, tn);
    if (parent) parent.appendChild(node);
  } else if (k === 'instance') {
    // C2: an INSTANCE_SWAP icon slot — build the master's slot as ONE instance of the
    // default svg component (resolved cross-chunk safe). It must be an INSTANCE so
    // doFrameComponent can bind the mainComponent property to it; each card instance then
    // swaps it to its own svg component via setProperties.
    let scomp = null;
    try { scomp = await resolveNode(tn.component); } catch (e) {}
    if (scomp && typeof scomp.createInstance === 'function') {
      node = scomp.createInstance();
      if (typeof tn.w === 'number' && node.width > 0) { try { node.rescale(Math.max(tn.w, 1) / node.width); } catch (e) {} }
    } else {
      out.flags.push({ feature: 'swap-slot-component-missing', node: tn.name, action: 'placeholder rectangle', needs_human: true });
      node = figma.createRectangle(); node.resize(tn.w || 64, tn.h || 64);
      node.fills = [{ type: 'SOLID', color: { r: 0.85, g: 0.85, b: 0.85 } }];
    }
    node.name = tn.name;
    await applyDecorations(node, tn);
    if (parent) parent.appendChild(node);
  } else if (k === 'image') {
    node = figma.createRectangle();
    node.name = tn.name;
    const S = tn.size || {};
    const w = (typeof S.w === 'number') ? S.w : 64, h = (typeof S.h === 'number') ? S.h : 64;
    try { node.resize(Math.max(w, 0.01), Math.max(h, 0.01)); } catch (e) {}
    node.fills = [{ type: 'SOLID', color: { r: 0.85, g: 0.85, b: 0.85 } }];
    if (tn.fills) await applyFills(node, tn.fills);
    await applyDecorations(node, tn);
    if (parent) parent.appendChild(node);
  } else { // frame / group
    node = figma.createFrame();
    node.name = tn.name;
    applyFrameBox(node, tn);
    if (tn.fills) await applyFills(node, tn.fills);
    else node.fills = []; // WS-A parity: an unfilled master frame is transparent, not Figma's default white
    await applyDecorations(node, tn);
    if (parent) parent.appendChild(node);
    if (tn.children) { for (const c of tn.children) { await buildTemplateNode(c, node); } }
    // Re-assert AUTO after children (WS1 §5a): a HUG axis recomputes to its content
    // once the children exist, the same gotcha the flat path fixes for every container.
    const S = tn.size;
    if (S && (node.layoutMode === 'VERTICAL' || node.layoutMode === 'HORIZONTAL')) {
      try {
        // Same D1 rule as applyFrameBox (frameAxisAuto): re-assert AUTO only where the
        // axis genuinely hugs, so a leaf slot or a captured cross dimension inside a
        // master is not hugged back to Figma's default once its children exist.
        const ax = frameAxisAuto(node.layoutMode, S, !(tn.children && tn.children.length));
        const pA = (node.layoutMode === 'HORIZONTAL') ? ax.wAuto : ax.hAuto;
        const cA = (node.layoutMode === 'HORIZONTAL') ? ax.hAuto : ax.wAuto;
        if (pA) node.primaryAxisSizingMode = 'AUTO';
        if (cA) node.counterAxisSizingMode = 'AUTO';
      } catch (e) {}
    }
  }
  return node;
}
// WS5: one component MASTER. Build the template subtree, convert it to a component,
// declare each TEXT property and reference it from its slot node (navigated by path),
// and persist our prop-id -> Figma property-key map on the node (plugin data) so
// instances resolve it even when they land in a later chunk than the master.
async function doFrameComponent(op) {
  let master;
  try { master = await buildTemplateNode(op.template, null); }
  catch (e) {
    out.errors.push({ key: op.key, field: 'template', error: String(e && e.message || e) });
    master = figma.createFrame(); master.name = op.name;
  }
  let comp;
  try { comp = figma.createComponentFromNode(master); }
  catch (e) {
    out.flags.push({ feature: 'frame-component-failed', node: op.name, action: 'kept as a frame (not a component)', needs_human: true });
    comp = master;
  }
  comp.name = op.name;
  const idToPid = {};
  const slotFonts = [];
  if (typeof comp.addComponentProperty === 'function') {
    for (const p of (op.props || [])) {
      try {
        const ptype = p.type || 'TEXT';
        let target = comp;
        for (const ix of (p.path || [])) { target = (target && target.children) ? target.children[ix] : null; }
        if (ptype === 'INSTANCE_SWAP') {
          // C2: Figma keys an INSTANCE_SWAP property by a component's NODE ID, not our
          // comp_ key — resolve the default svg component first (created earlier; cross-chunk
          // safe via IDMAP). Then bind the master's icon-slot INSTANCE to the property.
          let defNode = null;
          try { defNode = await resolveNode(p.default); } catch (e) {}
          const pid = comp.addComponentProperty(p.name, 'INSTANCE_SWAP', defNode ? defNode.id : '');
          idToPid[p.id] = pid;
          if (target && target.type === 'INSTANCE') {
            const refs = target.componentPropertyReferences || {};
            refs.mainComponent = pid;
            target.componentPropertyReferences = refs;
          } else {
            out.flags.push({ feature: 'component-swap-slot-missing', node: op.name + ' / ' + p.name, action: 'INSTANCE_SWAP property created but no instance slot found at its path', needs_human: true });
          }
        } else {
          const pid = comp.addComponentProperty(p.name, 'TEXT', (p.default == null ? '' : String(p.default)));
          idToPid[p.id] = pid;
          if (target && target.type === 'TEXT') {
            const refs = target.componentPropertyReferences || {};
            refs.characters = pid;
            target.componentPropertyReferences = refs;
            // Record the slot's RESOLVED font so a cross-chunk instance can load it before
            // setProperties rewrites characters. Figma refuses a characters write on an
            // unloaded font; a fresh chunk's session has loaded nothing, so the write would
            // silently throw and the instance keep the master default. target.fontName is the
            // font actually on the node (post-fallback), which is exactly what to reload.
            try { const fn = target.fontName; if (fn && fn.family) slotFonts.push({ family: fn.family, style: fn.style }); } catch (e) {}
          } else {
            out.flags.push({ feature: 'component-prop-slot-missing', node: op.name + ' / ' + p.name, action: 'property created but no TEXT slot found at its path', needs_human: true });
          }
        }
      } catch (e) { out.errors.push({ key: op.key, field: 'prop:' + p.id, error: String(e && e.message || e) }); }
    }
  }
  try { comp.setPluginData('heyhiCompProps', JSON.stringify(idToPid)); } catch (e) {}
  try { comp.setPluginData('heyhiCompFonts', JSON.stringify(slotFonts)); } catch (e) {}
  applyPlacement(comp, op);
  try { const parent = await resolveNode(op.parent); parent.appendChild(comp); } catch (e) {}
  made[op.key] = comp; out.created[op.key] = comp.id;
}
// WS5: one INSTANCE of a master. Resolve the master (made[] or IDMAP, cross-chunk
// safe), create an instance, map our prop ids to Figma property keys via the master's
// stored plugin data, and set this instance's per-card text values.
async function doInstanceComponent(op) {
  let comp = null;
  try { comp = await resolveNode(op.component); } catch (e) {}
  let node;
  if (comp && typeof comp.createInstance === 'function') {
    node = comp.createInstance();
    let idToPid = {};
    try { idToPid = JSON.parse(comp.getPluginData('heyhiCompProps') || '{}'); } catch (e) {}
    const setObj = {};
    const swaps = new Set(op.swaps || []);
    for (const pkey in (op.values || {})) {
      const pid = idToPid[pkey];
      if (!pid) continue;
      if (swaps.has(pkey)) {
        // C2 INSTANCE_SWAP: the value is a comp_ key -> resolve to the swap target's node id
        // (Figma's setProperties keys an INSTANCE_SWAP by component id). Cross-chunk safe.
        let tgt = null;
        try { tgt = await resolveNode(op.values[pkey]); } catch (e) {}
        if (tgt) setObj[pid] = tgt.id;
        else out.flags.push({ feature: 'swap-target-missing', node: op.name, action: 'kept the master default icon', needs_human: true });
      } else {
        setObj[pid] = op.values[pkey];
      }
    }
    if (Object.keys(setObj).length) {
      // Load the slot fonts first: setProperties rewrites `characters`, which Figma refuses
      // on an unloaded font. A same-chunk instance happens to have them loaded (the master
      // just built them in this session); a cross-chunk instance does not, so load explicitly.
      try {
        const fonts = JSON.parse(comp.getPluginData('heyhiCompFonts') || '[]');
        for (const fn of fonts) { try { await ensureFont(fn.family, fn.style); } catch (e) {} }
      } catch (e) {}
      try { node.setProperties(setObj); }
      catch (e) { out.errors.push({ key: op.key, field: 'setProperties', error: String(e && e.message || e) }); }
    }
    if (typeof op.w === 'number' && typeof op.h === 'number') { try { node.resize(Math.max(op.w, 1), Math.max(op.h, 1)); } catch (e) {} }
    else if (typeof op.w === 'number' && node.width > 0) { try { node.rescale(Math.max(op.w, 1) / node.width); } catch (e) {} }
  } else {
    out.flags.push({ feature: 'instance-component-missing', node: op.name, action: 'placeholder rectangle', needs_human: true });
    node = figma.createRectangle(); node.resize(op.w || 64, op.h || 64);
    node.fills = [{ type: 'SOLID', color: { r: 0.85, g: 0.85, b: 0.85 } }];
  }
  node.name = op.name;
  applyPlacement(node, op);
  const parent = await resolveNode(op.parent);
  parent.appendChild(node);
  made[op.key] = node; out.created[op.key] = node.id;
}
// </WS5-COMPONENT-FUNCS>

for (const op of OPS) {
  try {
    if (op.op === 'page') await doPage(op);
    else if (op.op === 'collection') await doCollection(op);
    else if (op.op === 'variable') await doVariable(op);
    else if (op.op === 'frame') await doFrame(op);
    else if (op.op === 'text') await doText(op);
    else if (op.op === 'vector') await doVector(op);
    else if (op.op === 'component') await doComponent(op);
    else if (op.op === 'instance') await doInstance(op);
    else if (op.op === 'frame_component') await doFrameComponent(op); /*WS5*/
    else if (op.op === 'instance_component') await doInstanceComponent(op); /*WS5*/
    else if (op.op === 'image') await doImage(op);
    else out.errors.push({ op: op.op, error: 'unknown op' });
  } catch (e) {
    out.errors.push({ key: op.key || op.op, error: String(e && e.message || e) });
  }
}
return JSON.stringify(out);
"""

WEIGHT_TO_STYLE = {
    100: "Thin", 200: "ExtraLight", 300: "Light", 400: "Regular",
    500: "Medium", 600: "SemiBold", 700: "Bold", 800: "ExtraBold", 900: "Black",
}


def weight_to_style(weight):
    if weight is None:
        return "Regular"
    try:
        w = int(round(float(weight) / 100.0)) * 100
    except (TypeError, ValueError):
        return "Regular"
    w = max(100, min(900, w))
    return WEIGHT_TO_STYLE.get(w, "Regular")


def conv_line_height(lh):
    if lh is None:
        return None
    if isinstance(lh, (int, float)) and lh <= 3:
        return {"value": round(lh * 100, 3), "unit": "PERCENT"}
    if isinstance(lh, (int, float)):
        return {"value": lh, "unit": "PIXELS"}
    return None  # string lineHeight (e.g. "normal") -> leave AUTO


def conv_letter_spacing(ls):
    if ls is None:
        return None
    return {"value": ls, "unit": "PIXELS"}


def line_height_px(lh, size):
    """Pixel line-height for bind mode."""
    if lh is None:
        return None
    if isinstance(lh, (int, float)) and lh <= 3:
        return round(lh * (size or 16), 3)
    if isinstance(lh, (int, float)):
        return lh
    return None


def var_name_from_token(token_path):
    """tokens.color.text.primary -> color/text/primary"""
    p = token_path
    if p.startswith("tokens."):
        p = p[len("tokens."):]
    return p.replace(".", "/")


def type_var_base(token_ref):
    """tokens.typography.scale.h1 -> type/scale/h1"""
    p = token_ref
    for pre in ("tokens.typography.", "tokens.type.", "tokens."):
        if p.startswith(pre):
            p = p[len(pre):]
            break
    return "type/" + p.replace(".", "/")


def collect_color_binds(node, acc):
    for fill in node.get("fills", []) or []:
        b = fill.get("bind")
        if b and b not in acc:
            acc[b] = fill.get("resolved")
    # v0.2: a stroke color binds like a fill (reference.md §2), so its Variable must
    # be created too — otherwise the stroke bind resolves to nothing at write time.
    for st in node.get("strokes", []) or []:
        c = st.get("color") or {}
        b = c.get("bind")
        if b and b not in acc:
            acc[b] = c.get("resolved")
    # Gap 4c (P4): an inline run's colour binds like a fill, so its Variable must be
    # created too — otherwise the run bind resolves to nothing at write time.
    for r in node.get("runs", []) or []:
        rf = r.get("fill") or {}
        b = rf.get("bind")
        if b and b not in acc:
            acc[b] = rf.get("resolved")
    for child in node.get("children", []) or []:
        collect_color_binds(child, acc)


def collect_type_styles(node, acc):
    if node.get("type") == "TEXT":
        ts = node.get("type_style") or {}
        ref = ts.get("token_ref")
        if ref and ref not in acc:
            acc[ref] = {
                "family": ts.get("family", "Inter"),
                "style": weight_to_style(ts.get("weight")),
                "size": ts.get("size"),
                "lineHeight": ts.get("lineHeight"),
                "letterSpacing": ts.get("letterSpacing"),
            }
    for child in node.get("children", []) or []:
        collect_type_styles(child, acc)


def _register_svg(svg_registry, svg, name):
    """Register one svg's bytes as a dedup'd component master (keyed by content hash) and
    return its comp_ key. Shared by build_node_op (top-level SVG dedup) and extract_component
    (C2 INSTANCE_SWAP icon slots) so the same icon content collapses to ONE master whether it
    is a plain page vector or a per-card swap target."""
    h = hashlib.sha1(svg.encode("utf-8")).hexdigest()[:12]
    comp_key = "comp_" + h
    if comp_key not in svg_registry:
        svg_registry[comp_key] = {"key": comp_key, "svg": svg, "name": "SVG source · " + name}
    return comp_key


def build_node_op(node, key, parent_key, ir_dir, type_mode, svg_registry=None):
    t = node.get("type")
    name = node.get("name", t)
    if t == "FRAME" or t == "GROUP":
        op = {"op": "frame", "key": key, "parent": parent_key, "name": name}
        if node.get("layout"):
            op["layout"] = node["layout"]
        if node.get("size"):
            op["size"] = node["size"]
        if node.get("fills"):
            op["fills"] = node["fills"]
        # D1 (plan-design-bridge-geometry-defects): mark a childless frame so the builder
        # FIXES its captured box rather than hugging an empty frame to Figma's 100px
        # default. Emitted only for leaves (keeps the per-op payload lean).
        if not (node.get("children") or []):
            op["leaf"] = True
        return op, []
    if t == "TEXT":
        ts = node.get("type_style") or {}
        family = ts.get("family", "Inter")
        style = weight_to_style(ts.get("weight"))
        op = {
            "op": "text", "key": key, "parent": parent_key, "name": name,
            "characters": node.get("characters", ""),
            "family": family, "style": style,
            "size": ts.get("size"),
            "lineHeight": conv_line_height(ts.get("lineHeight")),
            "letterSpacing": conv_letter_spacing(ts.get("letterSpacing")),
        }
        if node.get("fills"):
            op["fills"] = node["fills"]
        # Gap 4a: a wrapped TEXT (sizing.h == FILL) fills its column and auto-heights.
        _sz = node.get("size") or {}
        if (_sz.get("sizing") or {}).get("h") == "FILL":
            op["fillH"] = "FILL"
        if _sz.get("w") is not None:
            op["w"] = _sz["w"]
        # Gap 4c (P4): forward inline styled runs for setRange* in the interpreter.
        if node.get("runs"):
            op["runs"] = node["runs"]
        if type_mode == "bind" and ts.get("token_ref"):
            base = "var:type:" + ts["token_ref"]
            refs = {
                "fontFamily": base + ":family",
                "fontStyle": base + ":style",
            }
            if ts.get("size") is not None:
                refs["fontSize"] = base + ":size"
            if ts.get("lineHeight") is not None:
                refs["lineHeight"] = base + ":lh"
            if ts.get("letterSpacing") is not None:
                refs["letterSpacing"] = base + ":ls"
            op["bindRefs"] = refs
        return op, []
    if t == "VECTOR":
        svg = None
        flags = []
        ref = node.get("svgRef")
        if ref:
            svg_path = os.path.join(ir_dir, ref)
            if os.path.isfile(svg_path):
                with open(svg_path, "r", encoding="utf-8") as fh:
                    svg = fh.read()
            else:
                flags.append({"feature": "missing-vector-asset", "node": name,
                              "action": "placeholder rectangle", "needs_human": True})
        _sz = node.get("size") or {}
        # SVG dedup (chunk-budget follow-on): register each UNIQUE svg (by content)
        # once as a component master and emit a tiny `instance` op that references it
        # by key. The full svg bytes appear once per page (the component op), not once
        # per use — collapsing an SVG-heavy page's chunk count. A vector with no
        # resolvable svg keeps the placeholder `vector` op (the missing-asset path).
        if svg is not None and svg_registry is not None:
            comp_key = _register_svg(svg_registry, svg, name)
            op = {"op": "instance", "key": key, "parent": parent_key, "name": name,
                  "component": comp_key}
            if _sz.get("w") is not None:
                op["w"] = _sz["w"]
            if _sz.get("h") is not None:
                op["h"] = _sz["h"]
            return op, flags
        op = {"op": "vector", "key": key, "parent": parent_key, "name": name, "svg": svg}
        # Gap 1: an <img>-sourced vector carries its CSS display size so the
        # interpreter can scale the imported svg to the laid-out box.
        if _sz.get("w") is not None:
            op["w"] = _sz["w"]
        if _sz.get("h") is not None:
            op["h"] = _sz["h"]
        return op, flags
    if t == "IMAGE":
        # A raster <img> (or any IMAGE node): emit a real placement op carrying an
        # IMAGE fill (imageRef + scaleMode). The interpreter stages the IMAGE paint
        # and flags the embed; the true figma.createImage(bytes) -> imageHash is the
        # gated live step (P2 plan, Gap 5). An <img> has no background-size, so the
        # scaleMode defaults to FILL (object-fit is not captured by the extractor yet).
        size = node.get("size") or {}
        # P3 (ADR-013): IMAGE is a first-class fill.type now, so the op-fill carries
        # type:"IMAGE" (retiring P2's kind:"IMAGE" stopgap) with imageRef + scaleMode.
        fill = {"type": "IMAGE", "imageRef": node.get("imageRef"),
                "scaleMode": node.get("scaleMode", "FILL"),
                "resolved": node.get("imageRef")}
        op = {"op": "image", "key": key, "parent": parent_key, "name": name,
              "size": size, "fills": [fill]}
        return op, []
    return None, [{"feature": "unknown-node-type", "node": name, "action": "skipped", "needs_human": True}]


def _copy_decor(op, node):
    """Carry v0.2 decoration fields (ADR-010) onto the op for the interpreter:
    cornerRadius, strokes[], effects[], opacity. These set directly; stroke color
    binds like a fill. P3 (ADR-013) also carries node.position -> op.x/op.y so a
    child of a NONE-layout frame is placed at its captured offset, and marks a
    full-bleed (sizing FILL/FILL) placed child so the builder stretches it."""
    for f in ("cornerRadius", "strokes", "effects", "opacity"):
        if node.get(f) is not None:
            op[f] = node[f]
    pos = node.get("position")
    if isinstance(pos, dict):
        if pos.get("x") is not None:
            op["x"] = pos["x"]
        if pos.get("y") is not None:
            op["y"] = pos["y"]
        _sizing = (node.get("size") or {}).get("sizing") or {}
        if _sizing.get("h") == "FILL" and _sizing.get("v") == "FILL":
            op["fillParent"] = True
    return op


_CONTENT_TYPES = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png",
                  ".gif": "image/gif", ".webp": "image/webp"}


def _content_type(path):
    return _CONTENT_TYPES.get(os.path.splitext(path or "")[1].lower(), "application/octet-stream")


_SVGO_STATE = {"warned": False}


def _svgo_minify(svg):
    """Shrink one svg via `npx svgo -p 2 --multipass` (reference.md §F3): ~halves a
    detailed mark with no visible loss. Opt-in (--svgo) and defensive — if npx/svgo
    is absent or the call fails/times out, return the original unchanged (warn once)
    so the builder stays hermetic and never blocks on a missing/networked dependency."""
    if not svg or not shutil.which("npx"):
        if not _SVGO_STATE["warned"]:
            sys.stderr.write("note: --svgo requested but `npx` not found; leaving svgs unminified\n")
            _SVGO_STATE["warned"] = True
        return svg
    try:
        r = subprocess.run(["npx", "--yes", "svgo", "-i", "-", "-o", "-", "-p", "2", "--multipass"],
                           input=svg, capture_output=True, text=True, timeout=60)
        out = (r.stdout or "").strip()
        if r.returncode == 0 and out.startswith("<"):
            return out
    except Exception:
        pass
    if not _SVGO_STATE["warned"]:
        sys.stderr.write("note: --svgo failed; leaving svgs unminified\n")
        _SVGO_STATE["warned"] = True
    return svg


# --- WS5 (components / slots) --------------------------------------------------------
# Detect repeated sibling units (cards, values) and collapse them into one component
# master + N instances. Builder-side, reading the IR node tree — exactly the SVG-dedup
# pattern. The IR stays plain frames; the collapse lives only in the emitted op-plan.
# C0 scope: TEXT-property components for card/value-shaped runs (INSTANCE_SWAP icons C2).

# A "heading-ish" type_style.token_ref — the role-gate, so we componentize content
# cards (title/kicker/summary), not a row of identical spacer divs.
_HEADING_TOKEN_RE = re.compile(
    r"\.(scale|typography)\.(h[1-6]|display|title|lead|heading|subtitle|kicker|eyebrow)\b", re.I)


def _is_heading_token(ref):
    return bool(ref) and bool(_HEADING_TOKEN_RE.search(str(ref)))


def node_signature(node):
    """A canonical string of a node's STRUCTURE, deliberately blind to per-instance
    variation. INCLUDES type, layout mode + wrap, child count, the ordered child
    signatures, fills/strokes presence, a TEXT's token_ref ROLE, an icon slot
    (svgRef-vs-not), corner-radius presence. IGNORES characters, exact sizes, position,
    resolved colour, WHICH svg, exact padding. Two cards with the same shape but
    different titles/icons share a signature; a card with an extra child does not."""
    if not isinstance(node, dict):
        return "?"
    t = node.get("type") or "?"
    parts = [t]
    layout = node.get("layout") or {}
    if layout.get("mode"):
        m = layout.get("mode")
        if layout.get("layoutWrap") == "WRAP":
            m += "+W"
        parts.append("L:" + m)
    fills = node.get("fills") or []
    if fills:
        parts.append("F:" + ",".join(sorted(set((f.get("type") or "SOLID") for f in fills))))
    if node.get("strokes"):
        parts.append("K")
    if node.get("cornerRadius") is not None:
        parts.append("R")
    if t == "TEXT":
        ts = node.get("type_style") or {}
        parts.append("Tr:" + str(ts.get("token_ref") or ""))
    if t == "VECTOR" or node.get("svgRef"):
        parts.append("Ic")
    if t == "IMAGE":
        parts.append("Im")
    kids = node.get("children") or []
    parts.append("n%d" % len(kids))
    parts.append("(" + "|".join(node_signature(k) for k in kids) + ")")
    return ";".join(parts)


def _has_heading_text(node):
    """Does this subtree carry a TEXT with a heading-ish token_ref? The role-gate."""
    if not isinstance(node, dict):
        return False
    if node.get("type") == "TEXT" and _is_heading_token((node.get("type_style") or {}).get("token_ref")):
        return True
    for c in node.get("children") or []:
        if _has_heading_text(c):
            return True
    return False


# C1: control labels (WS4 tags an interactive control's label scale.button) and the
# "pill" shape (chip/tag/button) extend the role-gate beyond heading cards.
_CONTROL_TOKEN_RE = re.compile(r"\.scale\.(button|cta|action)\b", re.I)


def _is_control_token(ref):
    return bool(ref) and bool(_CONTROL_TOKEN_RE.search(str(ref)))


def _has_control_text(node):
    """Does this subtree carry a TEXT tagged as a control/button label? (WS4 tags an
    interactive control's label tokens.typography.scale.button.)"""
    if not isinstance(node, dict):
        return False
    if node.get("type") == "TEXT" and _is_control_token((node.get("type_style") or {}).get("token_ref")):
        return True
    for c in node.get("children") or []:
        if _has_control_text(c):
            return True
    return False


def _is_pill(node):
    """A pill/chip/button shape: a FRAME/GROUP with a VISIBLE BOX (a fill, a stroke, or a
    corner radius) wrapping only leaf content (>=1 TEXT child, no nested FRAME/GROUP). The
    conservative C1 line — it componentizes a labelled chip/tag/button run (and a flat
    card) but NOT a boxless wrapper div (no box), an icon-only row (no TEXT), or a
    multi-section card with nested containers (that path stays heading-gated)."""
    if not isinstance(node, dict) or node.get("type") not in ("FRAME", "GROUP"):
        return False
    has_box = bool(node.get("fills")) or bool(node.get("strokes")) or node.get("cornerRadius") is not None
    if not has_box:
        return False
    kids = node.get("children") or []
    if any(isinstance(k, dict) and k.get("type") in ("FRAME", "GROUP") for k in kids):
        return False
    return any(isinstance(k, dict) and k.get("type") == "TEXT" for k in kids)


def _is_componentizable_unit(node):
    """C1 role-gate: a repeated FRAME/GROUP run componentizes when its member is a content
    card (heading-ish TEXT — C0), an interactive control (a button/cta label), or a pill
    (chip/tag/button shape). A boxless wrapper or a text-less spacer row stays as
    independent frames (conservative — never componentize an anonymous repeat)."""
    return _has_heading_text(node) or _has_control_text(node) or _is_pill(node)


def _text_role_name(node):
    """A property display name for a TEXT slot: 'Title' for a heading, 'Label' for a
    control/button label, else the node's own name (its class, title-cased by build-ir),
    else a generic 'Text'."""
    ts = node.get("type_style") or {}
    if _is_heading_token(ts.get("token_ref")):
        return "Title"
    if _is_control_token(ts.get("token_ref")):
        return "Label"
    return node.get("name") or "Text"


def _icon_role_name(node):
    """A property display name for an INSTANCE_SWAP icon slot (C2): the node's own name
    (its class, title-cased by build-ir), else a generic 'Icon'."""
    return node.get("name") or "Icon"


def detect_component_groups(children, min_size=3):
    """Maximal runs of >= min_size CONSECUTIVE siblings sharing one structural
    signature, gated to componentizable units (member is a FRAME/GROUP that is a content
    card, an interactive control, or a pill/chip — see _is_componentizable_unit). Returns
    [(start, end_exclusive, signature)]. A sibling whose signature differs breaks the run
    and is left to build as an independent frame — never dropped (the varied-card case)."""
    groups = []
    n = len(children)
    i = 0
    while i < n:
        sig = node_signature(children[i])
        j = i + 1
        while j < n and node_signature(children[j]) == sig:
            j += 1
        if (j - i) >= min_size and isinstance(children[i], dict) \
                and children[i].get("type") in ("FRAME", "GROUP") and _is_componentizable_unit(children[i]):
            groups.append((i, j, sig))
        i = j
    return groups


def _template_fields(node, ir_dir, type_mode):
    """The op-shaped fields for ONE template node (no key/parent, no children yet), plus
    any flags build_node_op raised for it (e.g. missing-vector-asset). A master's baked
    content must not silently drop the same review-gate flags the flat-op path raises.
    Reuses build_node_op so a master renders exactly like an inline node would, but
    svg_registry=None bakes an icon inline (C2 promotes it to INSTANCE_SWAP)."""
    op, flags = build_node_op(node, None, None, ir_dir, type_mode, svg_registry=None)
    if op is None:
        return None, flags
    _copy_decor(op, node)
    op.pop("key", None)
    op.pop("parent", None)
    return op, flags


def extract_component(members, ir_dir, type_mode, svg_registry=None):
    """Walk the N member subtrees in lockstep (they share a signature, so positions
    align) and split varying content from baked content. Returns (template, props,
    instance_values, flags, swap_pids): the master template (member 0's structure with
    propId markers), the property list (id/name/type/default/path), each member's
    per-prop values, any flags build_node_op raised while building the template (e.g. a
    missing icon SVG on member 0, whose structure the master is baked from), and the set
    of prop ids that are INSTANCE_SWAP (so instances carry a `swaps` marker).
    At a TEXT position: characters differ across members -> a TEXT property; identical ->
    baked. At an icon (VECTOR/svgRef) position (C2): the svg content differs across members
    AND all resolve -> an INSTANCE_SWAP property whose default + per-instance values are
    dedup'd svg component keys; identical or any-unresolvable -> baked inline (member 0)."""
    props = []
    counter = [0]
    seen_names = {}
    instance_values = [dict() for _ in members]
    all_flags = []
    swap_pids = set()

    def _uniq_name(base):
        # Figma requires unique component-property display names; two slots that resolve to
        # the same role/name (e.g. two headings -> "Title") get a numeric suffix so the second
        # addComponentProperty does not throw and silently drop that slot's per-instance text.
        n = base or "Text"
        seen_names[n] = seen_names.get(n, 0) + 1
        return n if seen_names[n] == 1 else "%s %d" % (n, seen_names[n])

    def rec(aligned, path):
        m0 = aligned[0]
        top, flags = _template_fields(m0, ir_dir, type_mode)
        all_flags.extend(flags)
        if top is None:
            return None
        if m0.get("type") == "TEXT":
            chars = [(m.get("characters") or "") for m in aligned]
            if len(set(chars)) > 1:
                pid = "prop_%d" % counter[0]
                counter[0] += 1
                props.append({"id": pid, "name": _uniq_name(_text_role_name(m0)), "type": "TEXT",
                              "default": chars[0], "path": list(path)})
                top["propId"] = pid
                for idx, m in enumerate(aligned):
                    instance_values[idx][pid] = (m.get("characters") or "")
            # identical across members -> baked; top.characters already == member 0's.
        # C2 icon-swap: an icon (VECTOR/svgRef) slot whose svg CONTENT varies across members
        # becomes an INSTANCE_SWAP property — the master's slot is one instance of the
        # default svg component, and each member's value is its own dedup'd svg component
        # key. Requires every member's svg to resolve (a missing one keeps the baked path so
        # the missing-vector-asset flag still surfaces); identical content stays baked inline.
        elif svg_registry is not None and m0.get("svgRef") and isinstance(top, dict) and top.get("op") == "vector":
            svgs, resolved = [], True
            for m in aligned:
                ref = m.get("svgRef")
                p = os.path.join(ir_dir, ref) if ref else None
                if p and os.path.isfile(p):
                    with open(p, "r", encoding="utf-8") as fh:
                        svgs.append(fh.read())
                else:
                    resolved = False
                    break
            if resolved and len(set(svgs)) > 1:
                comp_keys = [_register_svg(svg_registry, s, m.get("name") or "Icon")
                             for s, m in zip(svgs, aligned)]
                pid = "prop_%d" % counter[0]
                counter[0] += 1
                props.append({"id": pid, "name": _uniq_name(_icon_role_name(m0)),
                              "type": "INSTANCE_SWAP", "default": comp_keys[0], "path": list(path)})
                swap_pids.add(pid)
                # Turn member 0's baked vector op into a swap instance slot (keep name/w/h).
                top.pop("svg", None)
                top["op"] = "instance"
                top["component"] = comp_keys[0]
                top["propId"] = pid
                for idx, ck in enumerate(comp_keys):
                    instance_values[idx][pid] = ck
            # identical / any-unresolvable -> top stays the baked vector op.
        # Recurse children aligned by raw index; `path` counts only BUILT children,
        # matching the interpreter (which appends only built children to the master).
        m0_kids = m0.get("children") or []
        built = []
        bidx = 0
        for ci in range(len(m0_kids)):
            aligned_kids = []
            aligned_ok = True
            for m in aligned:
                mk = m.get("children") or []
                if ci >= len(mk):
                    aligned_ok = False
                    break
                aligned_kids.append(mk[ci])
            if not aligned_ok:
                continue
            tc = rec(aligned_kids, path + [bidx])
            if tc is not None:
                built.append(tc)
                bidx += 1
        if built:
            top["children"] = built
        return top

    template = rec(members, [])
    return template, props, instance_values, all_flags, swap_pids


# ---------------------------------------------------------------------------------
# D-03 (plan-design-bridge-geometry-defects): consume the css-grid + pseudo-element
# "needs human" flags instead of raising them advisory and emitting the defect anyway.
#
#   D4 (CSS grid flattens to one row): the extractor collapses a `display:grid` whose
#     children span grid columns (`grid-column: 1 / -1`) into a single wrapped row and
#     raises a `css-grid` flag. A container is a reconstruction candidate only when it
#     has a full-span child (a child == its content width — the 1/-1 signal). For a
#     candidate whose widths partition cleanly (full-span child -> full-width row;
#     consecutive narrower children summing to the content width -> a shared row) the
#     container is rebuilt as a VERTICAL stack of rows and the flag is marked consumed;
#     a candidate whose widths do NOT partition is marked BLOCKING rather than ship the
#     wrong one-row approximation. An ordinary uniform/non-uniform wrap with no full-span
#     child, and a non-wrap N-column grid, are the extractor's existing behavior and are
#     left untouched (their flag stays advisory).
#
#   D2 (::before/::after never become a layer): the extractor records a pseudo-element
#     as a bare boolean and raises a `pseudo-element` flag; the IR carries no box, no
#     paint, and no per-variant fill for it (verified on the golden — three of its four
#     coverage bars, deep/covered/partial, are byte-identical in the IR because the teal
#     ::before that separates them is absent; only the gap variant differs, and only
#     because it restyles the bar itself, not via the ::before). The builder cannot render
#     "a real layer at the right size and
#     position" from a boolean, so every pseudo-element flag is marked BLOCKING: the
#     build FAILS rather than emit a placeholder that would collapse the four states
#     into one. Consuming a ::before (rendering it as a real layer) needs its box and
#     paint in the IR, which is an extractor change (extract_scene_graph/lib/build-ir.mjs,
#     D-02's owned file — the capture already probes content/color/background but the IR
#     transform drops it to a boolean) and is out of this lane's scope. Until then, a
#     visible ::before/::after refuses the build; `--allow-blocking` is the human override.
#
# A BLOCKING flag makes `main` exit non-zero and stamps `manifest.blocked`, so the flag
# stops being advisory (plan P4: "an advisory flag that still ships is the same class of
# failure as an advisory Exit Gate"). Artifacts are still written first so the plan stays
# measurable, and `--allow-blocking` downgrades the exit for measurement/inspection.

GRID_ROW_TOL = 2.0  # px slack when testing a row's summed width against the content width


def _norm_sel(s):
    """Normalize a node name or a flag's leaf selector to one comparable key
    ('.studio-shell' and 'Studio Shell' both -> 'studioshell')."""
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def _grid_flag_leaf(flag):
    return _norm_sel(str(flag.get("node", "")).split(">")[-1].strip().lstrip("."))


def _content_width(node):
    sz = node.get("size") or {}
    w = sz.get("w")
    if not isinstance(w, (int, float)) or isinstance(w, bool):
        return None
    pad = (node.get("layout") or {}).get("padding") or {}
    return w - (pad.get("l") or 0) - (pad.get("r") or 0)


def _has_full_span(children, content_w):
    """True if any child's captured width == the container content width — the signal
    that the css grid used `grid-column: 1 / -1` (a full-width row) rather than being an
    ordinary uniform/non-uniform wrap. Only a container with a full-span child is a D4
    reconstruction candidate; an ordinary wrap is left as the extractor mapped it."""
    if content_w is None or content_w <= 0:
        return False
    for c in children:
        cw = (c.get("size") or {}).get("w")
        if isinstance(cw, (int, float)) and not isinstance(cw, bool) and abs(cw - content_w) <= GRID_ROW_TOL:
            return True
    return False


def _partition_grid_rows(children, content_w, gap):
    """Group a grid container's children into rows from their captured widths.
    A child whose width == content_w is a full-span (grid-column:1/-1) row; a run of
    narrower children whose widths sum to content_w is one shared row. Returns the list
    of rows (each a list of child nodes), or None when the widths do NOT partition
    cleanly (a dimensionless child, a partial row still open before a full-span child, an
    overflow, or a trailing run that never reaches a full width). The caller invokes this
    only on a container that already has a full-span child (a real 1/-1 grid); a None
    return there means the spanning grid cannot be expressed and the caller BLOCKS rather
    than emit a wrong approximation."""
    if content_w is None or content_w <= 0:
        return None
    rows, cur, cur_w = [], [], 0.0
    for c in children:
        cw = (c.get("size") or {}).get("w")
        if not isinstance(cw, (int, float)) or isinstance(cw, bool):
            return None
        if abs(cw - content_w) <= GRID_ROW_TOL:
            if cur:
                return None            # a partial row was still open -> ambiguous
            rows.append([c])
            continue
        cur.append(c)
        cur_w += cw + (gap if len(cur) > 1 else 0)
        if abs(cur_w - content_w) <= GRID_ROW_TOL:
            rows.append(cur)
            cur, cur_w = [], 0.0
        elif cur_w > content_w + GRID_ROW_TOL:
            return None                # ran past the content width without landing on it
    if cur:
        return None                    # trailing children never summed to a full row
    return rows or None


def _rebuild_grid_container(node, rows, content_w, col_gap, row_gap):
    """Rewrite a css-grid container (mapped to a wrapped single row) into a VERTICAL
    stack: a single full-span child becomes a direct full-width child; a multi-child row
    is wrapped in a synthetic HORIZONTAL row frame. Preserves each child's captured
    geometry — row children are pinned FIXED at their track width so a HORIZONTAL frame
    does not split two FILL children evenly, and full-span children FILL the stack width
    (grid-column:1/-1)."""
    lay = node.get("layout") or {}
    sz = node.get("size") or {}
    align = lay.get("counterAxisAlignItems")
    new_children = []
    for i, row in enumerate(rows):
        if len(row) == 1:
            child = row[0]
            csizing = (child.setdefault("size", {})).setdefault("sizing", {})
            csizing["h"] = "FILL"       # grid-column:1/-1 -> spans the stack width
            new_children.append(child)
        else:
            for c in row:
                csizing = (c.setdefault("size", {})).setdefault("sizing", {})
                csizing["h"] = "FIXED"  # keep the captured track width; no even FILL split
            rowlay = {"mode": "HORIZONTAL"}
            if col_gap:
                rowlay["itemSpacing"] = col_gap
            if align:
                rowlay["counterAxisAlignItems"] = align
            new_children.append({
                "type": "FRAME",
                "name": "%s Row %d" % (node.get("name") or "Grid", i + 1),
                "layout": rowlay,
                "size": {"w": content_w, "h": None, "sizing": {"h": "FILL", "v": "HUG"}},
                "children": row,
            })
    node["children"] = new_children
    newlay = {"mode": "VERTICAL"}
    if lay.get("padding"):
        newlay["padding"] = lay["padding"]
    if row_gap:
        newlay["itemSpacing"] = row_gap
    node["layout"] = newlay
    node["size"] = {"w": sz.get("w"), "h": None,
                    "sizing": {"h": (sz.get("sizing") or {}).get("h", "FIXED"), "v": "HUG"}}


def preprocess_flags(root):
    """D-03 flag-handling pre-pass. Mutates the IR tree and its root `flags` in place:
    consumes the css-grid spanning-row case (rebuilds the container into a vertical stack
    of rows), and marks the unconsumable css-grid and every pseudo-element flag
    `blocking`. Runs before flatten, so the reconstructed tree is what the builder emits,
    measures, and geometry-checks. Fail-closed: if two containers share a normalized name
    and any one cannot be reconstructed, the shared flag is BLOCKING."""
    if not isinstance(root, dict):
        return
    flags = root.get("flags") or []
    # R-1=D (region-scoped structural block, 2026-08-29): build-ir.mjs emits a visible pseudo
    # that it CAN place (a leaf FRAME with a resolvable box) as a needs-human PLACEHOLDER
    # under the informational `pseudo-placeholder` feature — the build ships. A pseudo it
    # CANNOT place (a non-leaf/non-frame host, or an unresolvable in-flow box) keeps the
    # `pseudo-element` feature, which is BLOCKING here: refuse rather than silently ship it.
    # (`pseudo-placeholder` is never blocked; the css-grid partition-fail case below blocks.)
    for f in flags:
        if f.get("feature") == "pseudo-element":
            f["blocking"] = True

    grid_flags = [f for f in flags if f.get("feature") == "css-grid"]
    grid_leaves = {_grid_flag_leaf(f) for f in grid_flags}
    outcomes = {}   # leaf -> {"consumed": n, "blocked": m}

    def visit(node):
        if not isinstance(node, dict):
            return
        lay = node.get("layout") or {}
        leaf = _norm_sel(node.get("name"))
        # A css-grid-flagged container is a grid-column-span (D4) candidate only when the
        # extractor collapsed it to a wrapped row AND it has a full-span child (a
        # grid-column:1/-1 row). A non-wrap grid (a plain N-column row) and an ordinary
        # uniform/non-uniform wrap with no full-span child are already the extractor's
        # existing behavior and are left untouched (their flag stays advisory).
        children = node.get("children") or []
        if (leaf in grid_leaves and lay.get("mode") == "HORIZONTAL"
                and lay.get("layoutWrap") == "WRAP"):
            content_w = _content_width(node)
            if _has_full_span(children, content_w):
                col_gap = lay.get("itemSpacing") or 0
                row_gap = lay.get("counterAxisSpacing") or 0
                rows = _partition_grid_rows(children, content_w, col_gap)
                o = outcomes.setdefault(leaf, {"consumed": 0, "blocked": 0})
                if rows:
                    _rebuild_grid_container(node, rows, content_w, col_gap, row_gap)
                    o["consumed"] += 1
                else:
                    o["blocked"] += 1
        for c in node.get("children") or []:
            visit(c)

    visit(root)

    for f in grid_flags:
        o = outcomes.get(_grid_flag_leaf(f))
        if not o:
            continue    # a non-wrap css-grid (e.g. a plain N-column row) — left advisory
        if o["blocked"]:
            f["blocking"] = True
            f["action"] = ("css grid could not be partitioned into grid-column spans from "
                           "child widths; build refuses to flatten it to one row (needs human "
                           "/ extractor grid-placement capture)")
        else:
            f["needs_human"] = False
            f["blocking"] = False
            f["action"] = "consumed by builder: grid-column spans mapped to rows (grid-column:1/-1 -> full-width rows)"


def flatten(root, ir_dir, type_mode, svg_registry=None, key_prefix="",
            component_registry=None, component_groups=None):
    nodes = []
    extra_flags = []
    assets = []          # upload_assets manifest: raster fills embedded post-write
    counter = [0]

    def _emit_assets(op, key):
        # a raster IMAGE fill on this op is embedded post-write via upload_assets (raw
        # bytes -> cover fill on the node), not inline base64. Resolve the imageRef to
        # an absolute path so the runner can POST the bytes; SVGs are deduped, never raster.
        for f in op.get("fills", []) or []:
            if f.get("type") == "IMAGE" or f.get("kind") == "IMAGE":
                ref = f.get("imageRef")
                if ref:
                    abs_ref = ref if os.path.isabs(ref) else os.path.normpath(os.path.join(ir_dir, ref))
                    assets.append({"key": key, "imageRef": abs_ref,
                                   "scaleMode": f.get("scaleMode", "FILL"),
                                   "content_type": _content_type(abs_ref)})

    def _emit_group(members, parent_key, varied_names):
        # WS5: collapse a confirmed repeat-run into one master (registered once) + N
        # instance ops parented to the same container. Never drops a member.
        template, props, inst_values, comp_flags, swap_pids = extract_component(
            members, ir_dir, type_mode, svg_registry)
        if template is None:                # extraction failed -> build independently
            extra_flags.extend(comp_flags)
            for m in members:
                visit(m, parent_key)
            return
        # Flags build_node_op raised while building the template (e.g. a missing icon
        # SVG on member 0) must surface on the approval ledger exactly as they would on
        # the flat-op path — a componentized card is not exempt from review.
        extra_flags.extend(comp_flags)
        # Key the master by the full template (structure + baked text + prop defaults)
        # so two structurally-identical runs with different baked text get distinct
        # masters, while genuinely-identical runs dedupe — mirrors the SVG content hash.
        h = hashlib.sha1(json.dumps(template, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()[:12]
        comp_key = "%scomp_card_%s" % (key_prefix, h)
        cname = template.get("name") or "Card"
        if component_registry is not None and comp_key not in component_registry:
            component_registry[comp_key] = {"key": comp_key, "name": cname,
                                            "template": template, "props": props}
        if component_groups is not None:
            component_groups.append({"key": comp_key, "name": cname, "count": len(members),
                                     "props": [{"id": p["id"], "name": p["name"],
                                                "type": p.get("type", "TEXT"), "default": p["default"]} for p in props],
                                     "values": inst_values, "excluded": list(varied_names)})
        swaps = sorted(swap_pids)
        for idx, m in enumerate(members):
            ikey = "%snode_%d" % (key_prefix, counter[0])
            counter[0] += 1
            iop = {"op": "instance_component", "key": ikey, "parent": parent_key,
                   "name": (m.get("name") or cname), "component": comp_key,
                   "values": inst_values[idx]}
            # C2: name the INSTANCE_SWAP prop ids so the interpreter resolves each swap
            # value (a comp_ key) to a component node id, and compute_needs threads them.
            if swaps:
                iop["swaps"] = swaps
            msz = m.get("size") or {}
            if msz.get("w") is not None:
                iop["w"] = msz["w"]
            if msz.get("h") is not None:
                iop["h"] = msz["h"]
            nodes.append(iop)

    def visit(node, parent_key):
        key = "%snode_%d" % (key_prefix, counter[0])
        counter[0] += 1
        op, flags = build_node_op(node, key, parent_key, ir_dir, type_mode, svg_registry)
        if op is not None:
            _copy_decor(op, node)
            nodes.append(op)
            _emit_assets(op, key)
        extra_flags.extend(flags)
        children = node.get("children", []) or []
        # WS5: detect repeated card/value runs among THIS node's children; emit a
        # component master + instances for each run, building the rest normally.
        groups = detect_component_groups(children) if component_registry is not None else []
        if not groups:
            for child in children:
                visit(child, key)
            return
        starts = {g[0]: g for g in groups}
        covered = set()
        for (s, e, _sig) in groups:
            covered.update(range(s, e))
        # card-like siblings NOT grouped (the varied card the gate excluded) — reported.
        varied_names = [(children[idx].get("name") or "frame")
                        for idx in range(len(children))
                        if idx not in covered and isinstance(children[idx], dict)
                        and children[idx].get("type") in ("FRAME", "GROUP")
                        and _is_componentizable_unit(children[idx])]
        ci = 0
        while ci < len(children):
            if ci in starts:
                s, e, _sig = starts[ci]
                _emit_group(children[s:e], key, varied_names)
                ci = e
            else:
                visit(children[ci], key)
                ci += 1

    visit(root, "__PAGE__")
    return nodes, extra_flags, assets


def make_text_op(key, parent, name, family, style, size, characters, color_hex,
                 line_height=None, letter_spacing=None, x=None, y=None):
    op = {"op": "text", "key": key, "parent": parent, "name": name,
          "characters": characters, "family": family, "style": style, "size": size,
          "fills": [{"type": "SOLID", "resolved": color_hex}]}
    if line_height is not None:
        op["lineHeight"] = conv_line_height(line_height)
    if letter_spacing is not None:
        op["letterSpacing"] = conv_letter_spacing(letter_spacing)
    if x is not None:
        op["x"] = x
    if y is not None:
        op["y"] = y
    return op


def collapse_flags(flags):
    """Group flags by feature into one counted row each (first-seen order), with an
    example node + action. Plan §4: ~68 identical image-node flags buried the
    substantive ones, so repeated flags collapse to one row '[feature] xN — example'.
    A group is needs_human if any of its flags is."""
    groups, order = {}, []
    for f in flags or []:
        feat = f.get("feature", "?")
        if feat not in groups:
            groups[feat] = {"count": 0, "example": f, "needs_human": False}
            order.append(feat)
        groups[feat]["count"] += 1
        if f.get("needs_human"):
            groups[feat]["needs_human"] = True
    rows = []
    for feat in order:
        g = groups[feat]
        ex = g["example"]
        rows.append({"feature": feat, "count": g["count"], "node": ex.get("node", ""),
                     "action": ex.get("action", ""), "needs_human": g["needs_human"]})
    return rows


def fidelity_forecast(root):
    """A pre-build fidelity forecast (plan §4 'approval-surface blind spot'): what the
    immediate build will and will not render faithfully, surfaced at the approval gate
    (Earn the Room) BEFORE any Figma write. Post Lane-Core: image rasters stage as grey
    placeholders until the gated figma.createImage embed (P2); gradients render as real
    GradientPaints (P2); absolute children are placed at their captured offset in a
    NONE-layout frame (P3)."""
    c = {"img_nodes": 0, "img_fills": 0, "grad_total": 0, "grad_render": 0, "abs_children": 0}

    def walk(n):
        if n.get("type") == "IMAGE":
            c["img_nodes"] += 1
        for f in n.get("fills", []) or []:
            t = f.get("type")
            if t == "IMAGE" or f.get("kind") == "IMAGE":
                c["img_fills"] += 1
            elif t in ("GRADIENT_LINEAR", "GRADIENT_RADIAL"):
                c["grad_total"] += 1
                if f.get("stops"):
                    c["grad_render"] += 1
        if isinstance(n.get("position"), dict):
            c["abs_children"] += 1
        for ch in n.get("children", []) or []:
            walk(ch)

    walk(root)
    img = c["img_nodes"] + c["img_fills"]
    k, m, j = c["grad_total"], c["grad_render"], c["abs_children"]
    lines = []
    lines.append("%d image %s -> placeholder until the Figma MCP upload_assets embed (cover fill, full-res)" % (
        img, "surface" if img == 1 else "surfaces"))
    lines.append("%d of %d gradient%s render as real GradientPaints%s" % (
        m, k, "" if k == 1 else "s", ("; %d unparsed (flagged)" % (k - m)) if k - m else ""))
    lines.append("%d absolute %s placed at the captured offset (NONE-layout frame)" % (
        j, "child" if j == 1 else "children"))
    return lines


def build_doc_ops(ir, type_mode, color_binds, type_styles, all_flags, doc_x, flag_groups=None):
    """A self-describing documentation frame: token + Variable map, type specimen,
    flags ledger, and the bind-type vs set-direct mode note. Uses Inter (always
    present) for doc chrome so doc-frame fonts never pollute the real flag list.

    flag_groups (optional): a list of (label, flags[]) pairs. When given, the flags
    ledger is rendered grouped by label (one section per breakpoint in a merged
    multi-breakpoint doc) instead of as one flat list."""
    ops = []
    DARK = "#1A1A1A"
    GREY = "#555555"
    FONT = "Inter"
    k = [1000]

    def nk():
        k[0] += 1
        return "doc_%d" % k[0]

    doc = nk()
    ops.append({
        "op": "frame", "key": doc, "parent": "__PAGE__", "name": "Documentation — " + ir.get("meta", {}).get("source", "build"),
        "layout": {"mode": "VERTICAL", "primaryAxisAlignItems": "MIN", "counterAxisAlignItems": "MIN",
                   "itemSpacing": 20, "padding": {"t": 40, "r": 40, "b": 40, "l": 40}},
        "size": {"w": 720, "h": None, "sizing": {"h": "FIXED", "v": "HUG"}},
        "fills": [{"type": "SOLID", "resolved": "#FFFFFF"}],
        "x": doc_x, "y": 0,
    })
    ops.append(make_text_op(nk(), doc, "doc-title", FONT, "Bold", 28,
                            "HeyHi Design Bridge — Documentation", DARK))
    ops.append(make_text_op(nk(), doc, "doc-sub", FONT, "Regular", 13,
                            "Generated by heyhi-design-bridge from a reviewed scene-graph IR. "
                            "Color fills are bound to Figma Variables. Typography mode: "
                            + ("BIND (type bound to Variables)" if type_mode == "bind"
                               else "SET-DIRECT (values written directly, token_ref annotated)") + ".", GREY))

    # Mode note (the bind-type vs set-direct explanation, surfaced in-canvas)
    note = nk()
    ops.append({
        "op": "frame", "key": note, "parent": doc, "name": "Type mode note",
        "layout": {"mode": "VERTICAL", "primaryAxisAlignItems": "MIN", "counterAxisAlignItems": "MIN",
                   "itemSpacing": 6, "padding": {"t": 16, "r": 16, "b": 16, "l": 16}},
        "size": {"w": 640, "h": None, "sizing": {"h": "FIXED", "v": "HUG"}},
        "fills": [{"type": "SOLID", "resolved": "#FAFAF5"}],
    })
    ops.append(make_text_op(nk(), note, "note-h", FONT, "Bold", 13, "Why the type mode matters", DARK))
    ops.append(make_text_op(nk(), note, "note-b", FONT, "Regular", 12,
        "set-direct: type values (family, style, size, line-height, letter-spacing) are written "
        "directly onto each text layer and the source token is recorded as token_ref below. The "
        "Figma file carries no typography Variables. Best when the client's library does not model "
        "type as Variables.  bind: the same values are bound to Figma Variables, so changing a type "
        "token in Figma updates every layer. Requires the client's Figma to model typography as "
        "string and float Variables, and couples the build to font availability. Color always binds; "
        "this choice only governs typography.", GREY, line_height=1.5))

    # Token + Variable map
    ops.append(make_text_op(nk(), doc, "map-h", FONT, "Bold", 16, "Token + Variable map", DARK))
    used = ir.get("tokens_used", [])
    seen = set()
    for tu in used:
        tp = tu.get("token_path")
        seen.add(tp)
        bound = " (bound)" if tp in color_binds else ""
        row = "%s  ->  %s  =  %s   [%s %.0f%%]%s" % (
            tu.get("css_var", "?"), tu.get("figma_variable", var_name_from_token(tp or "")),
            tu.get("resolved", "?"), tu.get("source", "?"),
            float(tu.get("match_confidence", 1.0)) * 100, bound)
        ops.append(make_text_op(nk(), doc, "map-row", FONT, "Regular", 12, row,
                                DARK if tu.get("source") == "declared" else "#B26A00"))
    for b, hexv in color_binds.items():
        if b not in seen:
            ops.append(make_text_op(nk(), doc, "map-row", FONT, "Regular", 12,
                       "(bind) %s  ->  %s  =  %s   [bound]" % (b, var_name_from_token(b), hexv), DARK))

    # Type specimen
    ops.append(make_text_op(nk(), doc, "spec-h", FONT, "Bold", 16, "Type specimen", DARK))
    for ref, ts in type_styles.items():
        label = "%s  —  %s %s %spx%s" % (
            ref, ts["family"], ts["style"], ts.get("size", "?"),
            ("  (bound)" if type_mode == "bind" else ""))
        ops.append(make_text_op(nk(), doc, "spec-label", FONT, "Regular", 11, label, GREY))
        ops.append(make_text_op(nk(), doc, "spec-sample", ts["family"], ts["style"],
                                ts.get("size") or 16, "The quick brown fox — 0123", DARK,
                                line_height=ts.get("lineHeight"), letter_spacing=ts.get("letterSpacing")))

    # Flags ledger — collapsed: repeated flags become one counted row with an example
    # (plan §4: ~68 identical image-node flags buried the substantive ones).
    def flag_line(r):
        cnt = (" x%d" % r["count"]) if r.get("count", 1) > 1 else ""
        return "• [%s]%s %s — %s%s" % (
            r.get("feature", "?"), cnt, r.get("node", ""), r.get("action", ""),
            "  (needs human)" if r.get("needs_human") else "")

    total_flags = sum(len(g[1]) for g in flag_groups) if flag_groups else len(all_flags)
    flat = [f for g in flag_groups for f in g[1]] if flag_groups else all_flags
    ops.append(make_text_op(nk(), doc, "flags-h", FONT, "Bold", 16,
               "Flags ledger (%d total, %d distinct)" % (total_flags, len(collapse_flags(flat))), DARK))
    if flag_groups:
        for label, flags in flag_groups:
            rows = collapse_flags(flags)
            ops.append(make_text_op(nk(), doc, "flags-grp", FONT, "Bold", 13,
                       "%s — %d (%d distinct)" % (label, len(flags), len(rows)), DARK))
            if not rows:
                ops.append(make_text_op(nk(), doc, "flags-none", FONT, "Regular", 12, "No flags.", GREY))
            for r in rows:
                ops.append(make_text_op(nk(), doc, "flags-row", FONT, "Regular", 12, flag_line(r), "#B26A00"))
    else:
        rows = collapse_flags(all_flags)
        if not rows:
            ops.append(make_text_op(nk(), doc, "flags-none", FONT, "Regular", 12, "No flags. Clean build.", GREY))
        for r in rows:
            ops.append(make_text_op(nk(), doc, "flags-row", FONT, "Regular", 12, flag_line(r), "#B26A00"))
    return ops, doc


# --- use_figma payload budget (chunk-budget-fix, ADR-013 follow-on) ----------------
# The use_figma `code` argument is hard-capped at 50,000 chars. Each rendered chunk is
# `const IDMAP = <idmap>;\nconst OPS = <ops>;\n` + INTERPRETER_JS. The interpreter is
# fixed per chunk; the idmap is pruned at prep to only this chunk's cross-chunk `needs`
# (run_build.py), so it is small but non-zero. We chunk by projected rendered length so
# every payload clears the cap with margin — count-based chunking blew the cap whenever a
# chunk carried a large inlined SVG (the screenprint logo at ~26.8k chars).
USE_FIGMA_HARD_CAP = 50000
_CHUNK_SCAFFOLD = len("const IDMAP = ;\nconst OPS = ;\n")
_INTERP_OVERHEAD = len(INTERPRETER_JS) + _CHUNK_SCAFFOLD
_IDMAP_RESERVE = 5000     # generous headroom for the pruned per-chunk idmap (real ones run far smaller)
_CHUNK_SAFETY = 500
OPS_BUDGET = USE_FIGMA_HARD_CAP - _INTERP_OVERHEAD - _IDMAP_RESERVE - _CHUNK_SAFETY


def _strip_ws5_components(js):
    """Derive the component-free BASE interpreter: drop the WS5 master/instance handler
    functions and their two dispatch lines (tagged in the JS) so a chunk with no
    frame_component/instance_component op ships the same base interpreter — and the same
    headroom — the deployed builder had. WS5's ~8k of handler JS would otherwise eat the
    margin an SVG-heavy page (a ~21k logo master) needs to clear the 50k cap. Earn the
    Room: a chunk only pays for the handlers it actually uses."""
    a = js.find("// <WS5-COMPONENT-FUNCS>")
    b = js.find("// </WS5-COMPONENT-FUNCS>")
    if a != -1 and b != -1:
        b_eol = js.find("\n", b)
        js = js[:a] + (js[b_eol + 1:] if b_eol != -1 else "")
    return "\n".join(ln for ln in js.split("\n") if not ln.rstrip().endswith("/*WS5*/"))


_BASE_INTERPRETER_JS = _strip_ws5_components(INTERPRETER_JS)
_INTERP_OVERHEAD_BASE = len(_BASE_INTERPRETER_JS) + _CHUNK_SCAFFOLD
# A component-free chunk renders the base interpreter, so it can hold more ops; a chunk
# carrying a component op renders the full interpreter (OPS_BUDGET, the conservative one).
OPS_BUDGET_BASE = USE_FIGMA_HARD_CAP - _INTERP_OVERHEAD_BASE - _IDMAP_RESERVE - _CHUNK_SAFETY
_COMPONENT_OPS = ("frame_component", "instance_component")


def _op_chars(op):
    """Rendered JSON length of one op inside the OPS array (+2 for the comma/space)."""
    return len(json.dumps(op, ensure_ascii=False)) + 2


def _estimate_idmap_chars(needs):
    """Forecast the pruned-idmap JSON length for a chunk: {"<key>":"<~16-char id>",...}."""
    if not needs:
        return len("{}")
    return len("{}") + sum(len(json.dumps(k, ensure_ascii=False)) + 1 + 16 + 1 for k in needs)


def _swap_refs(op):
    """C2: the svg component keys an op resolves via INSTANCE_SWAP — a frame_component
    master's INSTANCE_SWAP prop defaults, and an instance_component's swap values (the
    pkeys named in op['swaps']). The svg masters are created before the card master, so
    these are cross-chunk refs compute_needs must thread or idmap-pruning drops them and the
    live swap silently keeps the default."""
    refs = []
    if op.get("op") == "frame_component":
        for p in op.get("props", []) or []:
            if p.get("type") == "INSTANCE_SWAP" and p.get("default"):
                refs.append(p["default"])
    elif op.get("op") == "instance_component":
        vals = op.get("values") or {}
        for pkey in op.get("swaps", []) or []:
            if vals.get(pkey):
                refs.append(vals[pkey])
    return refs


def _op_refs(op):
    """Keys this op resolves from IDMAP (cross-chunk parents/vars). Mirrors compute_needs,
    used to size a single op's own (small) idmap when it must occupy its own chunk."""
    refs = []
    if op.get("parent"):
        refs.append(op["parent"])
    if op.get("component"):
        refs.append(op["component"])
    refs.extend(_swap_refs(op))
    for fill in op.get("fills", []) or []:
        if fill.get("bind"):
            refs.append("var:" + fill["bind"])
    for r in op.get("runs", []) or []:
        rf = r.get("fill") or {}
        if rf.get("bind"):
            refs.append("var:" + rf["bind"])
    for vk in (op.get("bindRefs") or {}).values():
        refs.append(vk)
    if op.get("op") == "variable" and op.get("collection"):
        refs.append(op["collection"])
    return refs


def chunk_plan(preamble, node_ops, doc_ops, max_nodes, ops_budget=OPS_BUDGET):
    """Chunk ops so each rendered use_figma payload clears the 50,000-char cap. The
    primary split is by projected character length (ops_budget); max_nodes is a secondary
    cap. The preamble (page/collection/variables) seeds chunk 0; documentation ops form
    trailing chunks. A single op larger than ops_budget gets its own chunk. Returns
    (chunks, oversized) where oversized lists ops that cannot fit the hard cap even alone
    (still emitted in their own chunk, but surfaced so the caller can flag them)."""
    chunks = []
    oversized = []

    def _too_big_alone(op, op_len):
        # A solo op gets its own chunk; size its idmap from its OWN refs (a handful of
        # keys), not the worst-case reserve. "Oversized" means it cannot fit even alone.
        # Use the interpreter overhead the op's chunk will actually render: a component op
        # forces the full interpreter, everything else the base (so an SVG master is not
        # falsely flagged oversized by WS5 handler JS its chunk never carries).
        overhead = _INTERP_OVERHEAD if op.get("op") in _COMPONENT_OPS else _INTERP_OVERHEAD_BASE
        solo_idmap = _estimate_idmap_chars(_op_refs(op))
        return overhead + solo_idmap + op_len + _CHUNK_SAFETY > USE_FIGMA_HARD_CAP

    def _pack(ops_seq, seed=None):
        cur = list(seed) if seed else []
        cur_len = sum(_op_chars(o) for o in cur)
        cur_nodes = 0
        cur_has_comp = any(o.get("op") in _COMPONENT_OPS for o in cur)
        for op in ops_seq:
            ol = _op_chars(op)
            is_comp = op.get("op") in _COMPONENT_OPS
            if _too_big_alone(op, ol):
                oversized.append(op)
            # Budget against the interpreter this chunk will actually render: the full
            # (tighter) budget once it carries any component op, the base budget otherwise —
            # so a component-free page chunks exactly as the deployed builder did.
            budget = ops_budget if (cur_has_comp or is_comp) else OPS_BUDGET_BASE
            if cur and (cur_len + ol > budget or cur_nodes >= max_nodes):
                chunks.append(cur)
                cur, cur_len, cur_nodes, cur_has_comp = [], 0, 0, False
            cur.append(op)
            cur_len += ol
            if is_comp:
                cur_has_comp = True
            if op.get("op") in ("frame", "text", "vector", "image", "component", "instance", "frame_component", "instance_component"):
                cur_nodes += 1
        if cur:
            chunks.append(cur)

    _pack(node_ops, seed=preamble)   # chunk 0 leads with the preamble
    if doc_ops:
        _pack(doc_ops)
    return chunks, oversized


def compute_needs(chunks):
    """For each chunk, which referenced keys were created in an earlier chunk."""
    created_so_far = set()
    result = []
    for ops in chunks:
        creates = set()
        for op in ops:
            if op.get("key"):
                creates.add(op["key"])
        needs = set()
        for op in ops:
            refs = []
            if op.get("parent"):
                refs.append(op["parent"])
            if op.get("component"):
                refs.append(op["component"])
            refs.extend(_swap_refs(op))
            for fill in op.get("fills", []) or []:
                if fill.get("bind"):
                    refs.append("var:" + fill["bind"])
            for r in op.get("runs", []) or []:
                rf = r.get("fill") or {}
                if rf.get("bind"):
                    refs.append("var:" + rf["bind"])
            for st in op.get("strokes", []) or []:
                sc = st.get("color") or {}
                if sc.get("bind"):
                    refs.append("var:" + sc["bind"])
            for vk in (op.get("bindRefs") or {}).values():
                refs.append(vk)
            if op.get("op") == "variable" and op.get("collection"):
                refs.append(op["collection"])
            for r in refs:
                if r not in creates and r in created_so_far:
                    needs.add(r)
        created_so_far |= creates
        result.append(sorted(needs))
    return result


def render_chunk_code(ops):
    # A component-free chunk ships the base interpreter (the deployed one); only a chunk
    # that actually carries a frame_component/instance_component op pays for the WS5 handlers.
    interp = INTERPRETER_JS if any(o.get("op") in _COMPONENT_OPS for o in ops) else _BASE_INTERPRETER_JS
    return (
        "const IDMAP = __IDMAP__;\n"
        "const OPS = " + json.dumps(ops, ensure_ascii=False) + ";\n"
        + interp
    )


def count_types(node, acc=None):
    if acc is None:
        acc = {}
    acc[node.get("type", "?")] = acc.get(node.get("type", "?"), 0) + 1
    for c in node.get("children", []) or []:
        count_types(c, acc)
    return acc


# D-04 (plan-design-bridge-geometry-defects, I1): the height Figma's createFrame
# leaves on an auto-layout axis that has no content to size it. The builder never
# writes "100" — this is Figma's own default surviving a hug axis with nothing to hug
# to (the D1 collapse). Named here so the GEOMETRY CHECK can stand in for the Figma
# sizing semantics it was previously blind to.
FIGMA_CREATEFRAME_DEFAULT_PX = 100.0


def predict_frame_axes(layout_mode, size, is_leaf, sizing_semantics="post-d1"):
    """Python port of the JS `frameAxisAuto` (the D1 fix in the interpreter, ~L334):
    predict, per real axis, whether the builder emits it AUTO (content-hug) or FIXED.
    This is what lets the GEOMETRY CHECK reason about *emitted* geometry — "what Figma
    will compute" — rather than only the IR's declared numbers (defect I1).

    Kept verbatim in sync with `frameAxisAuto`; if that JS changes, change this too.

    sizing_semantics selects the builder era, so the check can be shown failing on the
    pre-fix build (batch rule 6) and passing on the post-fix one against the same IR:
      "post-d1" (default) -- the current builder. A declared HUG axis is a genuine
          content-hug only as a non-leaf container's PRIMARY axis, or a dimensionless
          axis; everywhere else the captured dimension is authoritative (FIXED).
      "pre-d1" -- the pre-D1 builder ("never resize a HUG axis"): every declared HUG
          axis, and every dimensionless axis, stays AUTO, so a token-sized leaf keeps
          Figma's createFrame default. This reproduces the D-09 collapse.
    Returns (w_auto, h_auto).
    """
    shug = (size or {}).get("sizing") or {}
    w = (size or {}).get("w")
    h = (size or {}).get("h")
    w_is_primary = (layout_mode == "HORIZONTAL")
    if sizing_semantics == "pre-d1":
        # Honor every declared HUG axis regardless of leaf/content, plus any
        # dimensionless axis — the old "never resize a HUG axis" rule.
        w_auto = (shug.get("h") == "HUG") or (w is None)
        h_auto = (shug.get("v") == "HUG") or (h is None)
    else:
        # frameAxisAuto, verbatim:
        #   wAuto = wIsPrimary ? (shug.h==='HUG' && !isLeaf) : (S.w == null)
        #   hAuto = wIsPrimary ? (S.h == null)              : (shug.v==='HUG' && !isLeaf)
        w_auto = ((shug.get("h") == "HUG") and not is_leaf) if w_is_primary else (w is None)
        h_auto = (h is None) if w_is_primary else ((shug.get("v") == "HUG") and not is_leaf)
    return w_auto, h_auto


def _axis_hits_fallback(is_auto, is_leaf, has_kids, captured):
    """True if a frame axis will land on Figma's createFrame default (the D1 collapse).
    Two ways a resolved value is lost:
      - the axis is AUTO (content-hug) but there is nothing to hug -- a leaf, or a
        container with no children -- so Figma keeps the createFrame default;
      - the axis is FIXED but the IR carried no captured dimension for it (the builder's
        own `unresolved-frame-size` case), so `resize` runs against Figma's default.
    An AUTO axis on a container that actually has children is a genuine hug, not a
    fallback."""
    if is_auto:
        return is_leaf or not has_kids
    return captured is None


def assert_geometry(root, tol=2.0, sizing_semantics="post-d1"):
    """WS2 geometric guard: catch the lost-wrap / over-height-white-space defect
    class on the IR itself, before any Figma write (geometry only, no Figma). Per
    corrections-registry `recurring-defect-needs-root-cause-not-per-site-patch`, a
    plausible-looking single-row overflow must fail a GEOMETRIC assert, not an
    eyeballed thumbnail. Returns a list of {node, kind, detail}:
      overflow   -- a non-wrap HORIZONTAL frame whose children's summed main-axis
                    extent exceeds its fixed width (a wrapping grid/flex lost its wrap).
      whitespace -- an auto-layout frame with a fixed (non-HUG) height greater than
                    its predicted content height (a frame carrying a multi-row bbox h).
      circular   -- (D-04, I1) a `v: FILL` child inside an auto-layout parent whose
                    vertical axis is HUG: the child fills the parent while the parent
                    hugs the child, the circular constraint Figma resolves by collapsing
                    the child (the D-09 root: 1440x143 against a real 2664).
      fallback   -- (D-04, I1) a frame whose emitted height (or width) is Figma's
                    createFrame default rather than a resolved value (the D1 collapse:
                    an 8px bar, a 7px dot landing 100 tall). Predicted from the builder's
                    own axis resolution (predict_frame_axes), so it reflects what Figma
                    will compute, not the IR's declared number.

    sizing_semantics ("post-d1" default | "pre-d1") selects the builder era for the
    emitted-geometry detectors (circular, fallback). The default reflects the current
    builder; "pre-d1" reproduces the pre-fix collapse so the check can be witnessed
    failing on the same golden it later passes (batch rule 6). overflow / whitespace /
    root guards are era-independent and unaffected.
    """
    out = []

    def num(x):
        return x if isinstance(x, (int, float)) and not isinstance(x, bool) else None

    def walk(node):
        if not isinstance(node, dict):
            return
        kids = node.get("children") or []
        layout = node.get("layout") or {}
        size = node.get("size") or {}
        sizing = size.get("sizing") or {}
        mode = layout.get("mode")
        n = len(kids)
        if mode in ("HORIZONTAL", "VERTICAL") and n:
            w = num(size.get("w"))
            h = num(size.get("h"))
            pad = layout.get("padding") or {}
            padL, padR = num(pad.get("l")) or 0, num(pad.get("r")) or 0
            padT, padB = num(pad.get("t")) or 0, num(pad.get("b")) or 0
            gap = num(layout.get("itemSpacing")) or 0
            cw = [num((k.get("size") or {}).get("w")) for k in kids]
            ch = [num((k.get("size") or {}).get("h")) for k in kids]
            child_fill = any(((k.get("size") or {}).get("sizing") or {}).get("h") == "FILL" for k in kids)
            wrap = layout.get("layoutWrap") == "WRAP"
            # overflow: a single-line row laid wider than its fixed frame
            if mode == "HORIZONTAL" and not wrap and w is not None and not child_fill and all(x is not None for x in cw):
                row_w = padL + padR + sum(cw) + gap * (n - 1)
                if row_w > w + tol:
                    out.append({"node": node.get("name", "?"), "kind": "overflow", "severity": "error",
                                "detail": "children span %.0fpx in a %.0fpx single-line frame -- a wrapping grid/flex likely lost its wrap (set layout.layoutWrap=WRAP)" % (row_w, w)})
            # white space: a fixed (non-HUG) height MUCH taller than predicted content.
            # Tuned conservative (excess > 80px AND > 40% over content) so a fixed-height
            # control — a button taller than its label, a banner — is not mistaken for
            # dead space. The real defect class (a section carrying a multi-row grid's
            # height) runs hundreds of px over and clears this easily.
            if h is not None and sizing.get("v") != "HUG":
                valid_h = [x for x in ch if x is not None]
                if valid_h:
                    maxch = max(valid_h)
                    if mode == "VERTICAL":
                        content_h = padT + padB + sum(valid_h) + gap * (n - 1)
                    else:
                        cnt_gap = num(layout.get("counterAxisSpacing")) or 0
                        if wrap and w is not None:
                            widths = [x for x in cw if x is not None]
                            colw = (max(widths) if widths else w) + gap
                            cols = max(1, int((w - padL - padR + gap) // colw)) if colw > 0 else 1
                            rows = (n + cols - 1) // cols
                        else:
                            rows = 1
                        content_h = padT + padB + rows * maxch + cnt_gap * (rows - 1)
                    excess = h - content_h
                    if excess > 80 and excess > 0.4 * content_h:
                        out.append({"node": node.get("name", "?"), "kind": "whitespace", "severity": "error",
                                    "detail": "fixed height %.0fpx exceeds content %.0fpx by %.0fpx (white space); container should HUG height (sizing.v=HUG, h=null)" % (h, content_h, excess)})
        # D-04 (I1): emitted-geometry checks. Reason about what Figma will compute from
        # the builder's own axis resolution (predict_frame_axes), not the IR's declared
        # numbers -- the blind spot that let a collapsed layout pass. Run on every
        # auto-layout frame, leaves included (a leaf is exactly the D1 fallback case).
        if mode in ("HORIZONTAL", "VERTICAL"):
            is_leaf = (n == 0)
            w_auto, h_auto = predict_frame_axes(mode, size, is_leaf, sizing_semantics)
            fb_h = _axis_hits_fallback(h_auto, is_leaf, n > 0, num(size.get("h")))
            fb_w = _axis_hits_fallback(w_auto, is_leaf, n > 0, num(size.get("w")))
            if fb_h or fb_w:
                axes = " & ".join([a for a, f in (("height", fb_h), ("width", fb_w)) if f])
                out.append({"node": node.get("name", "?"), "kind": "fallback", "severity": "error",
                            "detail": "emitted %s takes Figma's createFrame %gpx default, not a resolved value -- a token-sized frame hugging an axis with no content, or a sized axis with no captured dimension (the D1 collapse: an 8px bar landing 100 tall). FIX the axis to its captured value, or give the frame content to hug." % (axes, FIGMA_CREATEFRAME_DEFAULT_PX)})
            # circular constraint: a `v: FILL` child inside a VERTICAL parent whose
            # primary (vertical) axis HUGs -- the child fills the parent while the parent
            # hugs the child. Figma collapses the child (the D-09 root: 1440x143 vs 2664).
            # Restricted to a VERTICAL parent (the primary-axis case the plan cites); a
            # NONE-layout absolute parent (marketing-hero's Hero Scrim) is excluded by the
            # mode gate, and a HORIZONTAL parent's counter-axis stretch is not this defect.
            if mode == "VERTICAL" and h_auto and n:
                for k in kids:
                    if (((k.get("size") or {}).get("sizing") or {}).get("v")) == "FILL":
                        out.append({"node": k.get("name", "?"), "kind": "circular", "severity": "error",
                                    "detail": "vertical FILL inside parent '%s', whose vertical axis HUGs -- the circular constraint Figma resolves by collapsing the child (the D-09 root: 1440x143 vs a real 2664). Give the parent a fixed height, or the child a non-FILL vertical sizing." % node.get("name", "?")})
        for k in kids:
            walk(k)

    # WS-A / WS-B root guards (severity 'warn'): surfaced for human review in --summary,
    # not hard geometric contradictions like overflow/whitespace, and not self-test-fatal
    # (a re-extracted IR complies; a section-rooted fixture legitimately differs). They
    # catch a stale/manual root that floats the footer (root-not-hugging) or renders the
    # page white behind inheriting sections (root-no-background).
    if isinstance(root, dict):
        _rl = root.get("layout") or {}
        _rs = (root.get("size") or {}).get("sizing") or {}
        if _rl.get("mode") != "VERTICAL" or _rs.get("v") != "HUG":
            out.append({"node": root.get("name", "?"), "kind": "root-not-hugging", "severity": "warn",
                        "detail": "document root is not a hugging vertical stack (mode=%s, sizing.v=%s) -- footer/last-section gap risk; force VERTICAL + sizing.v=HUG" % (_rl.get("mode"), _rs.get("v"))})
        if not (root.get("fills") or []):
            out.append({"node": root.get("name", "?"), "kind": "root-no-background", "severity": "warn",
                        "detail": "document root has no resolved background -- inheriting sections render white; set a body/page background fill"})

    walk(root)
    return out


def tree_lines(node, depth=0, out=None, max_lines=80):
    """Container-only frame tree for the approval summary: FRAME/GROUP nodes
    indented, each annotated with a count of its direct leaf children."""
    if out is None:
        out = []
    if len(out) >= max_lines:
        return out
    t = node.get("type")
    if t in ("FRAME", "GROUP"):
        kids = node.get("children", []) or []
        leaf = {}
        for k in kids:
            if k.get("type") not in ("FRAME", "GROUP"):
                leaf[k.get("type")] = leaf.get(k.get("type"), 0) + 1
        leafstr = ("  {" + ", ".join("%sx%d" % (kt, n) for kt, n in leaf.items()) + "}") if leaf else ""
        out.append("  " * depth + "> " + (node.get("name") or t) + " [" + t + "]" + leafstr)
        for k in kids:
            if k.get("type") in ("FRAME", "GROUP"):
                tree_lines(k, depth + 1, out, max_lines)
    return out


def collect_unions(irs):
    """Union color binds, type styles, and tokens_used across all IR roots.
    First value for a given key wins (breakpoints share the same tokens)."""
    color_binds, type_styles, tu_by_path = {}, {}, {}
    for ir, _ in irs:
        collect_color_binds(ir["root"], color_binds)
        collect_type_styles(ir["root"], type_styles)
        for t in ir.get("tokens_used", []) or []:
            tp = t.get("token_path")
            if tp and tp not in tu_by_path:
                tu_by_path[tp] = t
    return color_binds, type_styles, tu_by_path


def build_preamble(page_name, rerun, color_binds, type_styles, tu_by_path, type_mode):
    """Page + token collection + color Variables (+ type Variables in bind mode).
    The collection and variables find-or-create at write time (re-run contract)."""
    preamble = [
        {"op": "page", "key": "__PAGE__", "name": page_name, "rerun": rerun},
        {"op": "collection", "key": "__COL__", "name": "HeyHi Bridge Tokens"},
    ]
    for bind, hexv in color_binds.items():
        tu = tu_by_path.get(bind, {})
        vname = tu.get("figma_variable") or var_name_from_token(bind)
        value = tu.get("resolved") or hexv or "#000000"
        preamble.append({"op": "variable", "key": "var:" + bind, "name": vname,
                         "collection": "__COL__", "vtype": "COLOR", "value": value})
    if type_mode == "bind":
        for ref, ts in type_styles.items():
            base = "var:type:" + ref
            vbase = type_var_base(ref)
            preamble.append({"op": "variable", "key": base + ":family", "name": vbase + "/family",
                             "collection": "__COL__", "vtype": "STRING", "value": ts["family"]})
            preamble.append({"op": "variable", "key": base + ":style", "name": vbase + "/style",
                             "collection": "__COL__", "vtype": "STRING", "value": ts["style"]})
            if ts.get("size") is not None:
                preamble.append({"op": "variable", "key": base + ":size", "name": vbase + "/size",
                                 "collection": "__COL__", "vtype": "FLOAT", "value": ts["size"]})
            if ts.get("lineHeight") is not None:
                preamble.append({"op": "variable", "key": base + ":lh", "name": vbase + "/line-height",
                                 "collection": "__COL__", "vtype": "FLOAT",
                                 "value": line_height_px(ts["lineHeight"], ts.get("size"))})
            if ts.get("letterSpacing") is not None:
                preamble.append({"op": "variable", "key": base + ":ls", "name": vbase + "/letter-spacing",
                                 "collection": "__COL__", "vtype": "FLOAT", "value": ts["letterSpacing"]})
    return preamble


def assemble(irs, args):
    """Assemble the full build plan for one or more IRs. Multiple IRs lay out
    side-by-side on one shared page with one merged documentation frame; a single
    IR reproduces the original page-per-breakpoint behaviour exactly. Returns the
    structures the summary path and the emit path both read, so they never drift."""
    multi = len(irs) > 1
    color_binds, type_styles, tu_by_path = collect_unions(irs)

    first_ir = irs[0][0]
    meta = first_ir.get("meta", {})
    src_stem = os.path.splitext(os.path.basename(meta.get("source", "build")))[0]
    if args.page_name:
        page_name = args.page_name
    elif multi:
        page_name = "HeyHi Bridge · " + src_stem
    else:
        bp = meta.get("breakpoint", "")
        page_name = "HeyHi Bridge · %s%s" % (src_stem, (" · " + bp) if bp else "")

    preamble = build_preamble(page_name, args.rerun, color_binds, type_styles, tu_by_path, args.type_mode)

    # SVG dedup: a registry shared across all breakpoints so a mark used on every
    # page is imported once. flatten emits `instance` ops that reference comp_* keys;
    # the masters are built below and laid out before the node ops.
    svg_registry = {}
    component_registry = {}   # WS5: each detected repeated card/value run -> one master
    component_groups = []     # WS5: per-group report for the --summary approval surface
    node_ops, per_bp, assets = [], [], []
    cursor_x = args.x
    for i, (ir, ir_dir) in enumerate(irs):
        bp = ir.get("meta", {}).get("breakpoint", "bp%d" % i)
        prefix = ("%s:" % bp) if multi else ""
        ops_i, node_flags_i, assets_i = flatten(ir["root"], ir_dir, args.type_mode,
                                                svg_registry, key_prefix=prefix,
                                                component_registry=component_registry,
                                                component_groups=component_groups)
        root_w = (ir["root"].get("size") or {}).get("w") or 1440
        if ops_i:
            ops_i[0]["x"] = cursor_x
            ops_i[0]["y"] = args.y
        flags_i = list(ir["root"].get("flags", []) or []) + node_flags_i
        per_bp.append({"bp": bp, "x": cursor_x, "w": root_w, "flags": flags_i,
                       "counts": count_types(ir["root"])})
        node_ops.extend(ops_i)
        assets.extend(assets_i)
        cursor_x += root_w + args.gap

    vector_uses = sum(1 for o in node_ops if o.get("op") == "instance")

    # Optional SVGO -p2 lever (reference.md §F3): shrink each unique master before it is
    # inlined once. Opt-in (--svgo) and hermetic by default — dedup already collapses
    # the chunk count, so this is a complementary per-mark shrink, not a dependency.
    if getattr(args, "svgo", False):
        for rec in svg_registry.values():
            rec["svg"] = _svgo_minify(rec["svg"])

    # One component master op per unique svg (carries the bytes once), parented to the
    # page off to the left so the masters do not overlap the mockup. Placed BEFORE the
    # node ops so every instance's master is created first; compute_needs threads the
    # comp_* key across chunks when an instance lands in a later chunk than its master.
    component_ops = []
    for j, rec in enumerate(svg_registry.values()):
        component_ops.append({"op": "component", "key": rec["key"], "parent": "__PAGE__",
                              "name": rec["name"], "svg": rec["svg"],
                              "x": float(args.x) - 480.0, "y": float(args.y) + j * 180.0})

    # WS5: one frame_component master op per detected repeat-set, parented off-canvas to
    # the left (like the SVG masters) so it is not laid out inside the grid. Placed BEFORE
    # the node ops so every instance's master is created first; compute_needs threads the
    # comp_card_* key across chunks when an instance lands in a later chunk than its master.
    frame_component_ops = []
    for j, rec in enumerate(component_registry.values()):
        frame_component_ops.append({"op": "frame_component", "key": rec["key"], "parent": "__PAGE__",
                                    "name": rec["name"], "template": rec["template"], "props": rec["props"],
                                    "x": float(args.x) - 980.0, "y": float(args.y) + j * 360.0})
    node_ops = component_ops + frame_component_ops + node_ops

    all_flags = [f for b in per_bp for f in b["flags"]]
    flag_groups = [(b["bp"], b["flags"]) for b in per_bp] if multi else None
    doc_ops, _ = build_doc_ops(first_ir, args.type_mode, color_binds, type_styles,
                               all_flags, cursor_x, flag_groups=flag_groups)

    chunks, oversized = chunk_plan(preamble, node_ops, doc_ops, args.max_nodes)
    needs = compute_needs(chunks)
    return {"multi": multi, "page_name": page_name, "color_binds": color_binds,
            "type_styles": type_styles, "per_bp": per_bp, "all_flags": all_flags,
            "chunks": chunks, "needs": needs, "oversized": oversized,
            "assets": assets, "svg_components": len(component_ops), "vector_uses": vector_uses,
            "component_groups": component_groups, "frame_components": len(frame_component_ops)}


def render_summary(asm, irs, args):
    """The Earn-the-Room approval surface: a scannable text view of what will be
    built, returned BEFORE any Figma write. Frame tree, node counts, token
    provenance, type ramp, chunk plan, and a highlighted flags block."""
    L = []
    meta = irs[0][0].get("meta", {})
    bps = " · ".join("%s (%d)" % (b["bp"], int(b["w"])) for b in asm["per_bp"])
    L.append("HeyHi Design Bridge · Translate preview (approve before any Figma write)")
    L.append("Source: %s    Brand: %s" % (meta.get("source", "?"), meta.get("brand_config", "?")))
    L.append("Breakpoints: %s" % bps)
    L.append("Page: %s    Type mode: %s    Re-run: %s" % (asm["page_name"], args.type_mode, args.rerun))
    L.append("")
    L.append("Node counts:")
    for b in asm["per_bp"]:
        c = b["counts"]
        parts = ["%s %d" % (t, c[t]) for t in ("FRAME", "TEXT", "VECTOR", "IMAGE", "GROUP") if c.get(t)]
        L.append("  %-3s %3d nodes   (%s)" % (b["bp"], sum(c.values()), " · ".join(parts)))
    L.append("")
    rich_ir = irs[-1][0]
    L.append("Frame tree (%s, containers only):" % asm["per_bp"][-1]["bp"])
    L.extend("  " + ln for ln in tree_lines(rich_ir["root"]))
    L.append("")
    prov, low = {}, 0
    for t in (rich_ir.get("tokens_used", []) or []):
        prov[t.get("source", "?")] = prov.get(t.get("source", "?"), 0) + 1
        if t.get("source") == "matched" and float(t.get("match_confidence", 1.0)) < 0.85:
            low += 1
    provstr = ", ".join("%d %s" % (n, s) for s, n in sorted(prov.items()))
    L.append("Tokens to Variables: %d color, created and bound%s." % (
        len(asm["color_binds"]), "" if args.type_mode in ("set-direct", "style") else " (+ type bound)"))
    L.append("  Provenance (%s): %s%s" % (asm["per_bp"][-1]["bp"], provstr,
             ("    %d low-confidence match(es) FLAGGED" % low) if low else ""))
    L.append("")
    _tm_note = {"set-direct": "set directly, token_ref annotated",
                "bind": "bound to Variables",
                "style": "set directly on first paint; FINISH with compose_type.py to land shared Figma Text Styles"}
    L.append("Type styles (%s): %s" % (args.type_mode, _tm_note.get(args.type_mode, "set directly")))
    for ref, ts in asm["type_styles"].items():
        L.append("  %s  ->  %s %s %spx" % (ref, ts["family"], ts["style"], ts.get("size", "?")))
    if args.type_mode == "style":
        L.append("  finish (after the page lands — Earn the Room):")
        L.append("    1) compose_type.py extract <lg.ir.json> -o spec.json    (review / rename roles)")
        L.append("    2) compose_type.py emit spec.json --root-node <built page id> -o out/")
        L.append("    3) issue out/create.js then out/apply.js via use_figma  (Text Styles bind family/style/size; lineHeight set-direct)")
    L.append("")
    if asm.get("vector_uses"):
        L.append("SVG dedup: %d vector use(s) -> %d unique imported once as components, reused by instance." % (
            asm["vector_uses"], asm.get("svg_components", 0)))
    if asm.get("assets"):
        L.append("Rasters: %d embedded full-res via Figma MCP upload_assets (cover fill; raw bytes, no base64)." % len(asm["assets"]))
    if asm.get("vector_uses") or asm.get("assets"):
        L.append("")
    if asm.get("component_groups"):
        L.append("Componentization (WS5 — repeat sets collapsed to a master + instances):")
        for g in asm["component_groups"]:
            props = g["props"]
            text_n = sum(1 for p in props if p.get("type", "TEXT") == "TEXT")
            swap_n = sum(1 for p in props if p.get("type") == "INSTANCE_SWAP")
            kinds = []
            if text_n:
                kinds.append("%d TEXT" % text_n)
            if swap_n:
                kinds.append("%d icon-swap" % swap_n)
            kind_str = " + ".join(kinds) or "no"
            pn = ", ".join(p["name"] for p in props) or "none"
            L.append("  %s · %d instances · %s prop(s): %s" % (g["name"], g["count"], kind_str, pn))
            for p in props:
                vals = [iv.get(p["id"], "") for iv in g["values"]]
                if p.get("type") == "INSTANCE_SWAP":
                    # values are svg component keys; show the distinct-icon count, not the hashes.
                    distinct = len({v for v in vals if v})
                    L.append("      %s = %d distinct icon(s) across %d instances (INSTANCE_SWAP)"
                             % (p["name"], distinct, len(vals)))
                else:
                    shown = ", ".join('"%s"' % v for v in vals[:6])
                    L.append("      %s = %s%s" % (p["name"], shown, " …" if len(vals) > 6 else ""))
            if g.get("excluded"):
                L.append("      excluded (varied sibling kept independent): %s" % ", ".join(g["excluded"]))
        L.append("")
    projected = [len(render_chunk_code(ops)) - len("__IDMAP__") + _estimate_idmap_chars(nd)
                 for ops, nd in zip(asm["chunks"], asm["needs"])]
    maxp = max(projected) if projected else 0
    cap_note = "all under the %d cap" % USE_FIGMA_HARD_CAP if maxp <= USE_FIGMA_HARD_CAP \
        else "OVER the %d cap — triage before write" % USE_FIGMA_HARD_CAP
    L.append("Build plan: %d use_figma call(s), <=%d node ops each, ids threaded across calls." % (
        len(asm["chunks"]), args.max_nodes))
    L.append("  Max projected payload: %d chars (%s)." % (maxp, cap_note))
    if asm.get("oversized"):
        L.append("  WARNING: %d SVG master(s) exceed the cap even alone — run with --svgo (reference.md §F3) to shrink them, or split the mark." % len(asm["oversized"]))
    L.append("Documentation frame: token+Variable map, type specimen, flags ledger (self-describing).")
    L.append("")
    L.append("Fidelity forecast (%s, before the write):" % asm["per_bp"][-1]["bp"])
    for line in fidelity_forecast(rich_ir["root"]):
        L.append("  " + line)
    L.append("")
    geo = assert_geometry(rich_ir["root"])
    L.append("GEOMETRY CHECK (%s) :: overflow + white-space + circular + fallback-size (error) + root hug/paint (warn):" % asm["per_bp"][-1]["bp"])
    _geo_err = [g for g in geo if g.get("severity", "error") == "error"]
    if not geo:
        L.append("  PASS — no overflow, no over-height white space; root hugs + is painted.")
    elif not _geo_err:
        L.append("  PASS (no errors) — %d advisory root warning(s) below for review:" % len(geo))
    for g in geo:
        L.append("  [%s/%s]  %s :: %s" % (g.get("severity", "error"), g["kind"], g.get("node", ""), g["detail"]))
    L.append("")
    # D-03: BLOCKING flags (unconsumable ::before/::after, or a css grid that cannot be
    # partitioned into grid-column spans) refuse the build — surfaced above the advisory
    # flags so an approver cannot miss them. Not counted again in FLAGS below.
    blocking = [f for f in asm["all_flags"] if f.get("blocking")]
    if blocking:
        brows = collapse_flags(blocking)
        L.append("BLOCKING (%d total, %d distinct) :: the build REFUSES to emit — resolve before any Figma write:" % (len(blocking), len(brows)))
        for r in brows:
            cnt = ("  x%d" % r["count"]) if r["count"] > 1 else ""
            L.append("  [%s]%s  %s :: %s" % (r["feature"], cnt, r.get("node", ""), r.get("action", "")))
        L.append("")
    advisory = [f for f in asm["all_flags"] if not f.get("blocking")]
    rows = collapse_flags(advisory)
    L.append("FLAGS (%d total, %d distinct) :: review before approve:" % (len(advisory), len(rows)))
    if not rows:
        L.append("  none. clean build." if not blocking else "  none advisory (see BLOCKING above).")
    for r in rows:
        cnt = ("  x%d" % r["count"]) if r["count"] > 1 else ""
        L.append("  [%s]%s  %s :: %s%s" % (
            r["feature"], cnt, r.get("node", ""), r.get("action", ""),
            "  (needs human)" if r.get("needs_human") else ""))
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="HeyHi Design Bridge Builder (IR -> use_figma chunks)")
    ap.add_argument("ir", nargs="+",
                    help="One or more scene-graph IR JSONs. Multiple IRs (sm/md/lg) build "
                         "side-by-side on one page with one merged documentation frame.")
    ap.add_argument("--type-mode", choices=["set-direct", "bind", "style"], default="set-direct",
                    help="set-direct (default): type written on each layer, token_ref annotated. "
                         "bind: type bound to Variables. style: set-direct on first paint, then finish "
                         "with compose_type.py to land shared Figma Text Styles (the recommended path).")
    ap.add_argument("--rerun", choices=["replace", "version"], default="replace")
    ap.add_argument("--max-nodes", type=int, default=60)
    ap.add_argument("--page-name", default=None)
    ap.add_argument("--x", type=float, default=0.0)
    ap.add_argument("--y", type=float, default=0.0)
    ap.add_argument("--gap", type=float, default=160.0,
                    help="Horizontal gap between breakpoint frame sets and the doc frame.")
    ap.add_argument("--out-dir", default="/tmp/heyhi-bridge-build")
    ap.add_argument("--summary", action="store_true",
                    help="Print the scannable approval summary and exit; write nothing.")
    ap.add_argument("--svgo", action="store_true",
                    help="Shrink each unique SVG master via `npx svgo -p 2 --multipass` "
                         "(reference.md §F3) before inlining. Opt-in, complementary to dedup; "
                         "no-op if npx/svgo is unavailable (builder stays hermetic by default).")
    ap.add_argument("--allow-blocking", action="store_true",
                    help="D-03: record BLOCKING flags (an unconsumable ::before/::after, or a "
                         "css grid that cannot be partitioned into grid-column spans) in the "
                         "manifest and summary but exit 0 instead of failing. For measurement or "
                         "inspection of a blocked build's plan; the default is a hard non-zero FAIL "
                         "so the flag is not advisory.")
    args = ap.parse_args()

    irs = []
    for p in args.ir:
        with open(p, "r", encoding="utf-8") as fh:
            irs.append((json.load(fh), os.path.dirname(os.path.abspath(p))))

    # D-03: consume/refuse the css-grid + pseudo-element "needs human" flags before the
    # tree is flattened, so the reconstructed grid is what the builder emits and measures
    # and the unconsumable flags become BLOCKING rather than advisory.
    for ir, _ in irs:
        preprocess_flags(ir.get("root", {}))

    asm = assemble(irs, args)
    blocking = [f for f in asm["all_flags"] if f.get("blocking")]

    if args.summary:
        print(render_summary(asm, irs, args))
        if blocking and not args.allow_blocking:
            sys.exit(1)
        return

    chunks, needs = asm["chunks"], asm["needs"]
    os.makedirs(args.out_dir, exist_ok=True)
    manifest_chunks, plan_chunks = [], []
    for idx, ops in enumerate(chunks):
        code = render_chunk_code(ops)
        path = os.path.join(args.out_dir, "chunk_%d.js" % idx)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(code)
        node_count = sum(1 for o in ops if o.get("op") in ("frame", "text", "vector", "image", "component", "instance", "frame_component", "instance_component"))
        # Projected rendered length once prep fills __IDMAP__ with this chunk's pruned needs.
        projected = len(code) - len("__IDMAP__") + _estimate_idmap_chars(needs[idx])
        manifest_chunks.append({
            "index": idx,
            "description": ("preamble + " if idx == 0 else "") + ("%d node ops" % node_count),
            "needs": needs[idx],
            "node_count": node_count,
            "op_count": len(ops),
            "projected_chars": projected,
            "code_file": path,
        })
        plan_chunks.append({"index": idx, "ops": ops, "needs": needs[idx], "node_count": node_count})

    max_projected = max((c["projected_chars"] for c in manifest_chunks), default=0)
    cap_ok = max_projected <= USE_FIGMA_HARD_CAP and not asm.get("oversized")
    manifest = {
        "type_mode": args.type_mode,
        "rerun": args.rerun,
        "page_name": asm["page_name"],
        "max_nodes": args.max_nodes,
        "breakpoints": [b["bp"] for b in asm["per_bp"]],
        "chunk_count": len(chunks),
        "out_dir": args.out_dir,
        "color_variables": len(asm["color_binds"]),
        "type_styles": len(asm["type_styles"]),
        "flags": len(asm["all_flags"]),
        "svg_components": asm.get("svg_components", 0),
        "vector_uses": asm.get("vector_uses", 0),
        "frame_components": asm.get("frame_components", 0),
        "component_instances": sum(1 for ch in plan_chunks for o in ch["ops"] if o.get("op") == "instance_component"),
        "hard_cap": USE_FIGMA_HARD_CAP,
        "max_projected_chars": max_projected,
        "cap_ok": cap_ok,
        "oversized_ops": len(asm.get("oversized", [])),
        # D-03: a blocked build must not ship. The plan is still written (so a blocked
        # build stays measurable), but `blocked` is true and `main` exits non-zero.
        "blocked": bool(blocking),
        "blocking_flags": collapse_flags(blocking) if blocking else [],
        "assets": asm.get("assets", []),
        "chunks": manifest_chunks,
    }
    with open(os.path.join(args.out_dir, "manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, ensure_ascii=False)
    with open(os.path.join(args.out_dir, "plan.json"), "w", encoding="utf-8") as fh:
        json.dump({"page_name": asm["page_name"], "type_mode": args.type_mode,
                   "rerun": args.rerun, "max_nodes": args.max_nodes,
                   "assets": asm.get("assets", []), "chunks": plan_chunks},
                  fh, ensure_ascii=False)
    print(json.dumps(manifest, indent=2, ensure_ascii=False))
    if not cap_ok:
        print("WARNING: max projected chunk payload %d > %d-char use_figma cap%s. "
              "Lower --max-nodes, or run with --svgo (reference.md §F3) to shrink oversized SVG masters, "
              "before issuing chunks."
              % (max_projected, USE_FIGMA_HARD_CAP,
                 (" — %d SVG master(s) exceed the cap even alone" % len(asm["oversized"])) if asm.get("oversized") else ""))
    if blocking:
        brows = collapse_flags(blocking)
        print("BUILD BLOCKED: %d blocking flag(s) — this plan must NOT be issued to use_figma:" % len(blocking))
        for r in brows:
            cnt = ("  x%d" % r["count"]) if r["count"] > 1 else ""
            print("  [%s]%s  %s :: %s" % (r["feature"], cnt, r.get("node", ""), r.get("action", "")))
        if args.allow_blocking:
            print("  (--allow-blocking: exiting 0 for measurement/inspection; the plan is still marked blocked.)")
        else:
            sys.exit(1)


if __name__ == "__main__":
    main()
