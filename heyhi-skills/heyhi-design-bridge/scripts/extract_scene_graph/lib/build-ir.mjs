// build-ir.mjs — map the rich browser capture down to the strict v0.1 scene-graph
// IR. The schema is frozen and additionalProperties:false, so every node carries
// only allowed fields; anything that does not fit a slot is surfaced in flags
// (never silently dropped) or, for clean-mapping CSS that v0.1 simply has no slot
// for (radius, shadow, stroke, opacity), aggregated into one schema-gap flag per
// property and reported to the human reviewer (see SCHEMA-GAPS.md) — the schema is NOT changed.

import crypto from "node:crypto";
import { fileURLToPath } from "node:url";
import { isAbsolute as isAbsPath, resolve as resolvePath } from "node:path";
import { parseColor, toHex } from "./color.mjs";

const GENERATED_BY = "heyhi-design-bridge/extract_scene_graph@0.1.0";

// ---------- small value helpers ----------
const round = (n, p = 2) => (n == null ? n : Math.round(n * 10 ** p) / 10 ** p);
function parsePx(v) {
  if (v == null) return null;
  const m = String(v).match(/^(-?\d*\.?\d+)px$/);
  return m ? parseFloat(m[1]) : null;
}
function isBareVar(v) {
  return typeof v === "string" && /^var\(\s*--[\w-]+\s*\)$/.test(v.trim());
}
function varName(v) {
  const m = String(v).match(/^var\(\s*(--[\w-]+)/);
  return m ? m[1] : null;
}
function extractVars(v) {
  return [...String(v || "").matchAll(/var\(\s*(--[\w-]+)/g)].map((m) => m[1]);
}
function hasCalcClamp(v) {
  return /\b(calc|clamp|min|max)\(/.test(String(v || ""));
}
function splitTopLevel(v) {
  const out = [];
  let depth = 0, cur = "";
  for (const ch of String(v || "")) {
    if (ch === "(") depth++;
    if (ch === ")") depth--;
    if (/\s/.test(ch) && depth === 0) { if (cur) { out.push(cur); cur = ""; } }
    else cur += ch;
  }
  if (cur) out.push(cur);
  return out;
}
function isTransparent(color) {
  if (!color || color === "transparent") return true;
  const c = parseColor(color);
  return !c || c.a === 0;
}

// ---------- background-image parsing (gradients + raster url()) ----------
// getComputedStyle returns background-image as a comma-separated STACK of layers
// (gradients and url()s), each itself comma-bearing. The CSS paint order is
// first-layer-on-top; the IR keeps that order so the topmost CSS layer is the
// first fill. parseColor already normalizes the rgb()/rgba() forms computed
// values use, so colour parsing reuses it.

// Split a comma-separated value at the TOP level only, respecting nested parens
// so commas inside rgb()/gradient() args do not split a layer.
function splitTopLevelCommas(v) {
  const out = [];
  let depth = 0, cur = "";
  for (const ch of String(v || "")) {
    if (ch === "(") depth++;
    else if (ch === ")") depth--;
    if (ch === "," && depth === 0) { out.push(cur.trim()); cur = ""; }
    else cur += ch;
  }
  if (cur.trim()) out.push(cur.trim());
  return out;
}

// CSS gradient angle -> degrees. A computed linear-gradient carries either an
// explicit "<n>deg" or a "to <side>" keyword; with neither, CSS defaults to
// "to bottom" (180deg). CSS angles are clockwise from 0deg = up.
const SIDE_ANGLE = {
  "to top": 0, "to right": 90, "to bottom": 180, "to left": 270,
  "to top right": 45, "to right top": 45, "to bottom right": 135, "to right bottom": 135,
  "to bottom left": 225, "to left bottom": 225, "to top left": 315, "to left top": 315,
};
function gradientAngle(prefix) {
  const p = String(prefix || "").trim().toLowerCase();
  const deg = p.match(/(-?\d*\.?\d+)deg/);
  if (deg) return ((parseFloat(deg[1]) % 360) + 360) % 360;
  const rad = p.match(/(-?\d*\.?\d+)rad/);
  if (rad) return (((parseFloat(rad[1]) * 180) / Math.PI % 360) + 360) % 360;
  const side = p.match(/^to\s+[a-z\s]+/);
  if (side && SIDE_ANGLE[side[0].replace(/\s+/g, " ").trim()] != null) {
    return SIDE_ANGLE[side[0].replace(/\s+/g, " ").trim()];
  }
  return 180; // CSS default direction is "to bottom"
}

// Does the first comma-group of a gradient body describe direction/shape rather
// than a colour stop? (a "to .../deg/rad" for linear, a shape/size/"at .." for
// radial). Used to peel the prefix off before reading stops.
function isGradientPrefix(group, radial) {
  const g = group.trim().toLowerCase();
  if (/^to\b/.test(g) || /(-?\d*\.?\d+)(deg|rad|grad|turn)\b/.test(g)) return true;
  if (radial && /^(circle|ellipse|closest|farthest|at\b)/.test(g)) return true;
  return false;
}

// One "<color> [<pos>] [<pos>]" stop group -> {pos|null, color}. Position is read
// as a fraction (0..1) from a %; a px/length position is left null (resolved at
// build time against the box). Two positions (a hard colour band) emit two stops.
function parseStopGroup(group) {
  const g = group.trim();
  const colorMatch = g.match(/^(rgba?\([^)]*\)|#[0-9a-fA-F]+|[a-z]+)/i);
  if (!colorMatch) return [];
  const color = colorMatch[0];
  const rest = g.slice(color.length).trim();
  const positions = (rest.match(/-?\d*\.?\d+%/g) || []).map((p) => parseFloat(p) / 100);
  if (!positions.length) return [{ pos: null, color }];
  return positions.map((pos) => ({ pos, color }));
}

// Parse one CSS gradient layer string into {type, angle?, stops[]}. Linear carries
// an angle; radial carries none (its handle is set from the box at build time).
// Missing stop positions are interpolated evenly (first=0, last=1) per the CSS
// colour-stop rules so the builder always receives explicit positions.
function parseGradientLayer(layer) {
  const s = String(layer || "").trim();
  const radial = /^repeating-radial-gradient|^radial-gradient/i.test(s);
  const open = s.indexOf("(");
  const close = s.lastIndexOf(")");
  if (open < 0 || close < 0) return null;
  const body = s.slice(open + 1, close);
  const groups = splitTopLevelCommas(body);
  let angle = 180;
  let start = 0;
  if (groups.length && isGradientPrefix(groups[0], radial)) {
    if (!radial) angle = gradientAngle(groups[0]);
    start = 1;
  } else if (!radial) {
    angle = 180; // no prefix -> CSS default "to bottom"
  }
  const stops = [];
  for (let i = start; i < groups.length; i++) {
    for (const stop of parseStopGroup(groups[i])) stops.push(stop);
  }
  // Interpolate any null positions (evenly between known anchors; ends pin 0/1).
  const n = stops.length;
  if (n) {
    if (stops[0].pos == null) stops[0].pos = 0;
    if (stops[n - 1].pos == null) stops[n - 1].pos = 1;
    let i = 0;
    while (i < n) {
      if (stops[i].pos == null) {
        let j = i;
        while (j < n && stops[j].pos == null) j++;
        const lo = stops[i - 1].pos, hi = stops[j].pos, span = j - (i - 1);
        for (let k = i; k < j; k++) stops[k].pos = lo + ((hi - lo) * (k - (i - 1))) / span;
        i = j;
      } else i++;
    }
  }
  const type = radial ? "GRADIENT_RADIAL" : "GRADIENT_LINEAR";
  const fill = { type, stops: stops.map((st) => ({ pos: round(st.pos, 4), color: st.color })) };
  if (!radial) fill.angle = round(angle, 2);
  return fill;
}

// Pull the path out of a url(...) layer (computed values quote the URL).
function urlPath(layer) {
  const m = String(layer || "").match(/^url\((['"]?)(.*?)\1\)$/i);
  return m ? m[2] : null;
}
// background-size -> Figma scaleMode. cover -> FILL, contain -> FIT; an explicit
// pair is treated as a placement we approximate to FILL (the closest non-tiling
// mode). Default (auto) reads as FILL so a photo background is not letterboxed.
function scaleModeFromSize(bgSize) {
  const s = String(bgSize || "").trim().toLowerCase();
  if (s.includes("contain")) return "FIT";
  if (s.includes("cover")) return "FILL";
  return "FILL";
}
// Gap 5 (raster-ref): resolve a url()/img src to an imageRef the gated
// figma.createImage embed reads bytes from. A VECTOR's bytes are written into
// prototypes/assets/ and referenced relative to the IR; a RASTER is referenced in
// place, so its ref must point at the real SOURCE asset. The prior code prepended
// the VECTOR convention ("prototypes/") onto the raster path — and a computed
// background-image, which the browser returns already absolute (file://…), then
// became an unreadable "prototypes/file://…" ref. Resolution: file:// -> a real fs
// path; http(s) is kept for a remote fetch; an absolute fs path passes through; a
// relative <img> src resolves against the prototype dir when known (protoDir), else
// is returned cleaned. Never the prototypes/ copy-path (no raster is copied there).
function resolveImageRef(raw, protoDir) {
  if (!raw) return null;
  const s = String(raw).trim().split(/[?#]/)[0];
  if (/^file:\/\//i.test(s)) { try { return fileURLToPath(s); } catch { return s; } }
  if (/^https?:\/\//i.test(s)) return s;
  if (isAbsPath(s)) return s;
  const rel = s.replace(/^\.?\//, "");
  return protoDir ? resolvePath(protoDir, rel) : rel;
}
function isIdentityTransform(t) {
  if (!t || t === "none") return true;
  const s = t.replace(/\s+/g, "");
  return s === "matrix(1,0,0,1,0,0)" || s === "matrix3d(1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1)";
}
// Parse a computed box-shadow into Figma effects. getComputedStyle emits the
// colour as rgba(...) first, then the offsets; multiple shadows are comma-joined
// at the top level. Figma nodes carry multiple effects, so each shadow is one.
function parseShadows(boxShadow) {
  if (!boxShadow || boxShadow === "none") return [];
  const parts = [];
  let depth = 0, cur = "";
  for (const ch of boxShadow) {
    if (ch === "(") depth++;
    else if (ch === ")") depth--;
    if (ch === "," && depth === 0) { parts.push(cur); cur = ""; } else cur += ch;
  }
  if (cur.trim()) parts.push(cur);
  return parts.map((p) => {
    const s = p.trim();
    const inset = /\binset\b/.test(s);
    const colorMatch = s.match(/rgba?\([^)]*\)|#[0-9a-fA-F]+/);
    const color = colorMatch ? colorMatch[0] : null;
    const rest = (colorMatch ? s.replace(colorMatch[0], "") : s).replace(/\binset\b/, "");
    const nums = (rest.match(/-?\d*\.?\d+px/g) || []).map((n) => parseFloat(n));
    const [x = 0, y = 0, blur = 0, spread = 0] = nums;
    return { type: inset ? "INNER_SHADOW" : "DROP_SHADOW", x, y, blur, spread, color };
  });
}

// ---------- naming ----------
function titleCase(s) {
  return s.replace(/[-_]/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}
function nodeName(rich, kind) {
  if (rich.tag === "svg") return rich.classes[0] ? titleCase(rich.classes[0]) : "Vector";
  if (rich.tag === "img") return rich.classes[0] ? titleCase(rich.classes[0]) : "Image";
  if (rich.tag === "body") return "Page";
  if (rich.classes[0]) return titleCase(rich.classes[0]);
  if (rich.id) return titleCase(rich.id);
  if (kind === "TEXT" && rich.text) return rich.text.slice(0, 28);
  return titleCase(rich.tag);
}
function nodePath(rich, parentName) {
  const sel = rich.classes[0] ? `.${rich.classes[0]}` : rich.tag;
  return parentName ? `${parentName} > ${sel}` : sel;
}

// WS4 (C): does a token path name a background / surface / page family? Used to forbid a
// TEXT colour from snapping to a background token (the invisible-label hazard).
function isBackgroundToken(tokenPath) {
  return /(^|[.\/])(backgrounds?|surface|page|canvas)([.\/]|$)/i.test(String(tokenPath || ""));
}
// WS4 (C): WCAG relative luminance of a parsed {r,g,b} (0..255) for the contrast guard.
function relLuminance(rgb) {
  if (!rgb) return null;
  const lin = (v) => { const c = v / 255; return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); };
  return 0.2126 * lin(rgb.r) + 0.7152 * lin(rgb.g) + 0.0722 * lin(rgb.b);
}
// WS4 (B): interactive-control detection (semantic tag / role / btn|cta class).
const CONTROL_CLASS = /(^|[\s])(btn|button|cta)([\s-]|$)/i;
function isInteractiveControl(rich) {
  if (rich.tag === "a" || rich.tag === "button") return true;
  if (rich.role === "button") return true;
  return (rich.classes || []).some((c) => CONTROL_CLASS.test(c));
}
// "button-like" == has a visible box: a non-transparent bg, a real border, or a btn/cta class.
// (A bare link with none of these stays TEXT — nav links never become pills.)
function isButtonLike(rich) {
  if (!isTransparent(rich.computed.backgroundColor)) return true;
  const bw = parsePx(rich.computed.borderTopWidth) || 0;
  if (bw > 0 && rich.computed.borderTopStyle !== "none") return true;
  return (rich.classes || []).some((c) => CONTROL_CLASS.test(c));
}

// D3 (P3): screen-reader-only ("visually hidden" / .sr-only) detection. The universal
// idiom clips the box to ~1px and hides overflow so assistive tech reads the content but
// nothing paints (position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0 0 0 0)).
// Matched on that COMPUTED shape, never on the class name; the class is a convention, the
// clipped 1px box is the contract. Deliberately narrow: the 7px aria-hidden decorative dot has
// a real box and visible overflow, so it is NOT this and survives. clip / clip-path are not in
// the capture, so a variant hiding a full-size box by clip alone is out of reach here (a known
// bound of this shape match); the 1px form is what the golden and the live sheerline/studio use.
const SR_ONLY_MAX_PX = 2;
function isScreenReaderOnly(rich) {
  const c = rich && rich.computed, b = rich && rich.bbox;
  if (!c || !b) return false;
  const clippedTiny = b.w <= SR_ONLY_MAX_PX && b.h <= SR_ONLY_MAX_PX &&
    c.overflowX === "hidden" && c.overflowY === "hidden";
  const positioned = c.position === "absolute" || c.position === "fixed";
  return clippedTiny && positioned;
}

export function buildIR(capture, brandMap, { source, breakpoint, brandConfig, svgAssets = {}, protoDir = null }) {
  const tokensUsed = new Map(); // dedup key -> entry
  const flags = []; // does-not-map flags (per node)
  const missingFonts = new Set();
  const assets = []; // VECTOR svg files to write {file, content}

  function recordToken(entry) {
    const key = `${entry.source}|${entry.token_path}|${entry.resolved || ""}|${entry.css_var || ""}`;
    if (!tokensUsed.has(key)) tokensUsed.set(key, entry);
  }
  function addFlag(feature, node, action, needs_human = true) {
    if (!flags.some((f) => f.feature === feature && f.node === node)) flags.push({ feature, node, action, needs_human });
  }

  // ---- colour token resolution (declared var -> declared; literal -> matched) ----
  // role ('text' | 'bg') breaks exact-hex ties toward the semantically right token.
  function resolveColor(declared, computed, path, role) {
    const resolvedHex = (() => { const c = parseColor(computed); return c ? toHex(c) : computed; })();
    if (isBareVar(declared)) {
      const tok = brandMap.lookupVar(varName(declared));
      if (tok) {
        recordToken({ css_var: tok.css_var, token_path: tok.token_path, figma_variable: tok.figma_variable, resolved: resolvedHex, source: "declared", match_confidence: 1 });
        return { bind: tok.token_path, resolved: resolvedHex };
      }
    }
    // literal / clamp / nested var / inherited -> nearest-token confidence match
    const near = brandMap.nearestColor(computed, role === "text" ? "text" : "background");
    if (near) {
      const conf = round(near.confidence, 3);
      // WS4 (C): anti-snap guard. A TEXT colour that only resolves via the MATCHED path
      // (no declared var — e.g. color:inherit or a JS-set colour) must never bind to a
      // BACKGROUND-family token: that is the "white CTA text matched to backgrounds/surface
      // at 94%" hazard that renders a label invisible. Keep the literal colour UNBOUND and
      // raise link-color-unsnapped instead of snapping it away.
      if (role === "text" && isBackgroundToken(near.token.token_path)) {
        addFlag("link-color-unsnapped", path, `text colour ${resolvedHex} nearest a background token (${near.token.token_path}); kept literal + unbound so the label stays visible`, true);
        return { resolved: resolvedHex };
      }
      recordToken({ token_path: near.token.token_path, figma_variable: near.token.figma_variable, resolved: resolvedHex, source: "matched", match_confidence: conf });
      if (conf < 0.7) addFlag("low-confidence-color-match", path, `nearest token ${near.token.token_path} at confidence ${conf}`, true);
      return { bind: near.token.token_path, resolved: resolvedHex };
    }
    return { resolved: resolvedHex };
  }

  // ---- fills ----
  // A background can stack several layers: any number of gradient and url() raster
  // layers, then the background-color underneath. CSS paints the first layer on
  // top, so fills are emitted in CSS order (topmost first) with the solid colour
  // last. Each gradient layer is parsed into structured {angle, stops}; each
  // url() into an IMAGE fill carrying imageRef + scaleMode. resolved keeps the
  // original layer string for the preview and as a fallback.
  function bgFills(rich, path) {
    const out = [];
    const bgImg = rich.computed.backgroundImage;
    if (bgImg && bgImg !== "none") {
      const layers = splitTopLevelCommas(bgImg);
      const bgSize = rich.computed.backgroundSize;
      for (const layer of layers) {
        if (/gradient/i.test(layer)) {
          const g = parseGradientLayer(layer);
          if (g) out.push({ ...g, resolved: layer });
          else { out.push({ type: /radial/i.test(layer) ? "GRADIENT_RADIAL" : "GRADIENT_LINEAR", resolved: layer });
                 addFlag("gradient-unparsed", path, `could not parse "${layer}" — review manually`, true); }
        } else if (/^url\(/i.test(layer)) {
          // P3 (ADR-013): IMAGE is a first-class fill.type now, with imageRef +
          // scaleMode on the fill — retiring P2's kind:"IMAGE" stopgap (which rode
          // additionalProperties because v0.2's fill.type enum was closed). The
          // builder reads f.type === "IMAGE".
          const ref = resolveImageRef(urlPath(layer), protoDir);
          out.push({ type: "IMAGE", imageRef: ref, scaleMode: scaleModeFromSize(bgSize), resolved: layer });
        } else {
          // a layer we do not model (e.g. element(), cross-fade) — never a silent drop
          addFlag("background-layer-unsupported", path, `"${layer}" not represented`, true);
        }
      }
    }
    if (!isTransparent(rich.computed.backgroundColor)) {
      const r = resolveColor(rich.declared.backgroundColor, rich.computed.backgroundColor, path, "bg");
      out.push({ type: "SOLID", ...(r.bind ? { bind: r.bind } : {}), resolved: r.resolved });
    }
    return out;
  }
  function textFill(rich, path) {
    const r = resolveColor(rich.declared.color, rich.computed.color, path, "text");
    return [{ ...(r.bind ? { bind: r.bind } : {}), resolved: r.resolved }];
  }

  // ---- v0.2 decorations: cornerRadius / strokes / effects / opacity, set directly ----
  function radiusPx(val, rich) {
    const px = parsePx(val);
    if (px != null) return px;
    const m = String(val || "").match(/^(-?\d*\.?\d+)%$/); // e.g. 50% on a square -> circle
    if (m) return (parseFloat(m[1]) / 100) * Math.min(rich.bbox.w, rich.bbox.h);
    return 0;
  }
  function decorations(rich, path) {
    const c = rich.computed;
    const out = {};
    const tl = radiusPx(c.borderTopLeftRadius, rich), tr = radiusPx(c.borderTopRightRadius, rich),
          br = radiusPx(c.borderBottomRightRadius, rich), bl = radiusPx(c.borderBottomLeftRadius, rich);
    if (tl || tr || br || bl) out.cornerRadius = (tl === tr && tr === br && br === bl) ? round(tl) : { tl: round(tl), tr: round(tr), br: round(br), bl: round(bl) };

    const bw = parsePx(c.borderTopWidth) || 0;
    if (bw > 0 && c.borderTopStyle !== "none") {
      const col = resolveColor(rich.declared.borderColor, c.borderTopColor, path, "bg");
      out.strokes = [{ weight: round(bw), color: { type: "SOLID", ...(col.bind ? { bind: col.bind } : {}), resolved: col.resolved } }];
    }

    const shadows = parseShadows(c.boxShadow);
    if (shadows.length) out.effects = shadows.map((s) => ({ type: s.type, x: round(s.x), y: round(s.y), blur: round(s.blur), spread: round(s.spread), ...(s.color ? { color: { resolved: s.color } } : {}) }));

    const op = parseFloat(c.opacity);
    if (!Number.isNaN(op) && op < 1) out.opacity = round(op, 3);
    return out;
  }

  // ---- layout (flex/grid -> auto-layout) ----
  const JUSTIFY = { "flex-start": "MIN", start: "MIN", left: "MIN", center: "CENTER", "flex-end": "MAX", end: "MAX", right: "MAX", "space-between": "SPACE_BETWEEN", "space-around": "SPACE_BETWEEN", "space-evenly": "SPACE_BETWEEN" };
  const ALIGN = { "flex-start": "MIN", start: "MIN", stretch: "MIN", normal: "MIN", center: "CENTER", "flex-end": "MAX", end: "MAX", baseline: "BASELINE" };
  // align-content -> Figma counterAxisAlignContent (WRAP only); only the space-*
  // family maps to SPACE_BETWEEN, everything else stays the AUTO default (unset).
  const ALIGN_CONTENT = { "space-between": "SPACE_BETWEEN", "space-around": "SPACE_BETWEEN", "space-evenly": "SPACE_BETWEEN" };

  // computed gridTemplateColumns is a resolved px track list (e.g. "336px 336px
  // 336px") or "none"; return the numeric track widths so callers can count tracks
  // and test uniformity (repeat(N,1fr) -> N equal tracks -> a faithful WRAP).
  function gridTracks(gtc) {
    if (!gtc || gtc === "none") return [];
    return gtc.split(/\s+/).map((s) => parsePx(s)).filter((v) => v != null && !Number.isNaN(v));
  }

  function spacingProvenance(declaredShorthand, computedSides, path) {
    // Resolve every top-level component: a bare var is a declared lookup; a
    // calc()/clamp()/literal is a confidence-scored match and a clamp flag.
    if (!declaredShorthand) return;
    const comps = splitTopLevel(declaredShorthand);
    comps.forEach((comp, i) => {
      const sidePx = computedSides[Math.min(i, computedSides.length - 1)];
      if (isBareVar(comp)) {
        const tok = brandMap.lookupVar(varName(comp));
        if (tok) recordToken({ css_var: tok.css_var, token_path: tok.token_path, resolved: `${round(sidePx)}px`, source: "declared", match_confidence: 1 });
      } else if (hasCalcClamp(comp)) {
        addFlag("clamp-calc-derived", path, `${comp} — token link is best-effort`, true);
        const near = brandMap.nearestSpacing(sidePx);
        if (near) recordToken({ token_path: near.token.token_path, resolved: `${round(sidePx)}px`, source: "matched", match_confidence: round(near.confidence * 0.7, 3) });
      }
    });
  }

  function mapLayout(rich, type, path) {
    const c = rich.computed;
    const childCount = (rich.children || []).length;
    let mode;
    let wrap = false;          // a wrapping HORIZONTAL container (ADR-014)
    let gridNonUniform = false;
    if (type === "GROUP") { mode = "NONE"; addFlag("absolute-positioning", path, "child is position:absolute — not expressible as auto-layout", true); }
    else if (c.display === "grid" || c.display === "inline-grid") {
      const trackPx = gridTracks(c.gridTemplateColumns);
      const tracks = trackPx.length;
      if (tracks > 1) {
        mode = "HORIZONTAL";
        // a multi-row grid (more items than columns) wraps; a single row that fits
        // its tracks stays a plain HORIZONTAL row (no wrap, no width pin).
        if (childCount > tracks) wrap = true;
        gridNonUniform = (Math.max(...trackPx) - Math.min(...trackPx)) >= 1;
      } else mode = "VERTICAL";
    } else if (c.display === "flex" || c.display === "inline-flex") {
      mode = c.flexDirection.startsWith("column") ? "VERTICAL" : "HORIZONTAL";
      if (c.flexWrap === "wrap" || c.flexWrap === "wrap-reverse") {
        if (mode === "HORIZONTAL" && childCount > 1) wrap = true;
        else if (mode === "VERTICAL") addFlag("flex-wrap-vertical", path, "wrapping column flex has no Figma auto-layout equivalent; review", true);
      }
    } else mode = "VERTICAL"; // block flow stacks vertically

    const layout = { mode };
    if (c.display.includes("flex") || c.display.includes("grid")) {
      if (JUSTIFY[c.justifyContent]) layout.primaryAxisAlignItems = JUSTIFY[c.justifyContent];
      if (ALIGN[c.alignItems]) layout.counterAxisAlignItems = ALIGN[c.alignItems];
    }
    // itemSpacing from the MAIN-axis gap (column-gap for HORIZONTAL incl. wrap, row-gap for VERTICAL)
    const rowGap = parsePx(c.rowGap) || 0, colGap = parsePx(c.columnGap) || 0;
    const spacing = mode === "VERTICAL" ? rowGap : colGap;
    if (spacing) {
      layout.itemSpacing = round(spacing);
      spacingProvenance(rich.declared.gap, [spacing], path);
    }
    // padding
    const pad = { t: round(parsePx(c.paddingTop) || 0), r: round(parsePx(c.paddingRight) || 0), b: round(parsePx(c.paddingBottom) || 0), l: round(parsePx(c.paddingLeft) || 0) };
    if (pad.t || pad.r || pad.b || pad.l) {
      layout.padding = pad;
      spacingProvenance(rich.declared.padding, [pad.t, pad.r, pad.b, pad.l], path);
    }
    // ADR-014: a wrapping horizontal flex / multi-row grid becomes a Figma
    // layoutWrap:WRAP auto-layout (cross-axis gap = row-gap) instead of the old
    // single-line approximation that overflowed off-canvas and only flagged flex-wrap.
    if (wrap && mode === "HORIZONTAL") {
      layout.layoutWrap = "WRAP";
      layout.counterAxisSpacing = round(rowGap);
      const ac = ALIGN_CONTENT[c.alignContent];
      if (ac) layout.counterAxisAlignContent = ac;
    }
    // A uniform grid (repeat(N,1fr) / equal tracks) maps faithfully to WRAP and is
    // not flagged. Only NON-uniform tracks (2fr 1fr / minmax / auto) need review,
    // since Figma wrap columns are equal-width.
    if (gridNonUniform) addFlag("css-grid", path, "non-uniform grid tracks approximated as equal wrap columns; review column widths", true);
    return layout;
  }

  function mapSize(rich, type, layout) {
    const b = rich.bbox;
    const c = rich.computed;
    const sizing = {};
    // Heuristic: a flex/grid item that fills its cross axis -> FILL; text hugs
    // unless it wrapped (Gap 4a), in which case it fills its column and auto-heights.
    if (type === "TEXT") {
      const fpx = parsePx(c.fontSize) || 16;
      const lh = parsePx(c.lineHeight) || fpx * 1.2;
      const wrapped = lh > 0 && b.h > lh * 1.4;
      sizing.h = wrapped ? "FILL" : "HUG";
      sizing.v = "HUG";
      return { w: round(b.w), h: round(b.h), sizing };
    }
    // ADR-014: a wrap container is FIXED width (so Figma wraps at the same column
    // count CSS did) + HUG height (so it auto-heights to the wrapped rows instead
    // of carrying the multi-row bbox height — the white-space root cause). h:null
    // tells the builder not to force a height onto the hug axis.
    if (layout && layout.layoutWrap === "WRAP") {
      sizing.h = "FIXED";
      sizing.v = "HUG";
      return { w: round(b.w), h: null, sizing };
    }
    sizing.h = (c.alignItems === "stretch" || c.display === "block") ? "FILL" : "HUG";
    sizing.v = "HUG";
    return { w: round(b.w), h: round(b.h), sizing };
  }

  // ---- typography (set directly; token_ref for traceability) ----
  const TAG_SCALE = { h1: "h1", h2: "h2", h3: "h3", h4: "h4" };
  function mapTypeStyle(rich, path) {
    const c = rich.computed;
    const ts = {};
    const fam = String(c.fontFamily).split(",")[0].replace(/['"]/g, "").trim();
    if (fam) ts.family = fam;
    const w = parseInt(c.fontWeight, 10);
    if (!Number.isNaN(w)) ts.weight = w;
    const size = parsePx(c.fontSize);
    if (size != null) ts.size = round(size);
    const lh = parsePx(c.lineHeight);
    if (lh != null && size) ts.lineHeight = round(lh / size, 2);
    const ls = parsePx(c.letterSpacing);
    if (ls != null && ls !== 0) ts.letterSpacing = round(ls, 2);

    // token_ref recovery from the declared font-size
    const decl = rich.declared.fontSize;
    if (isBareVar(decl) && varName(decl).startsWith("--type-")) {
      const tok = brandMap.lookupVar(varName(decl));
      if (tok) { ts.token_ref = tok.token_path; recordToken({ css_var: tok.css_var, token_path: tok.token_path, resolved: `${round(size)}px`, source: "declared", match_confidence: 1 }); }
    } else if (hasCalcClamp(decl)) {
      const scaleName = TAG_SCALE[rich.tag] || "body";
      const tp = `tokens.typography.scale.${scaleName}`;
      ts.token_ref = tp;
      addFlag("clamp-calc-derived", path, `font-size ${decl} — token_ref ${tp} inferred from tag`, true);
      recordToken({ token_path: tp, resolved: `${round(size)}px`, source: "matched", match_confidence: 0.5 });
    }
    return ts;
  }

  // ---- inline styled runs (P4, Gap 4c) ----
  // The capture records inline run boundaries (rich.inlineRuns) over the same
  // collapsed `characters`. Map each to a schema run {start, end, fill?, style?},
  // emitting only the fields that DIFFER from the text leaf's base style (a clay
  // accent colour; an <em> italic; a heavier weight). Colour resolves and binds
  // exactly like the leaf fill, so its Variable is created in the preamble.
  function mapRuns(rich, path) {
    const inRuns = rich.inlineRuns;
    if (!inRuns || !inRuns.length) return undefined;
    const base = rich.computed;
    const baseWeight = parseInt(base.fontWeight, 10);
    const baseFam = String(base.fontFamily || "").split(",")[0].replace(/['"]/g, "").trim();
    const baseItalic = /italic|oblique/.test(base.fontStyle || "");
    const out = [];
    for (const r of inRuns) {
      const c = r.computed || {};
      const run = { start: r.start, end: r.end };
      if (c.color && c.color !== base.color) {
        const rc = resolveColor(r.declaredColor, c.color, path, "text");
        run.fill = { ...(rc.bind ? { bind: rc.bind } : {}), resolved: rc.resolved };
      }
      const style = {};
      if (/italic|oblique/.test(c.fontStyle || "") && !baseItalic) style.italic = true;
      const rw = parseInt(c.fontWeight, 10);
      if (!Number.isNaN(rw) && rw !== baseWeight) style.weight = rw;
      const rfam = c.fontFamily ? String(c.fontFamily).split(",")[0].replace(/['"]/g, "").trim() : null;
      if (rfam && rfam !== baseFam) style.family = rfam;
      if (Object.keys(style).length) run.style = style;
      if (run.fill || run.style) out.push(run);
    }
    if (out.length) addFlag("inline-run", path, `${out.length} inline styled run(s) preserved; applied via setRange in the builder`, false);
    return out.length ? out : undefined;
  }

  // ---- per-node CSS feature flags (does-not-map + schema-gap aggregation) ----
  function collectFlags(rich, path) {
    const c = rich.computed;
    if (c.position === "sticky") addFlag("position-sticky", path, "flattened to static; sticky has no Figma equivalent", true);
    if (c.position === "fixed") addFlag("position-fixed", path, "flattened to static; fixed has no Figma equivalent", true);
    // R-1=D: the pseudo flag is raised by handlePseudo (after the node is built), because
    // whether it is a non-blocking placeholder or a blocking refusal depends on the built node
    // (resolvable box -> a placeholder, flipping a leaf host or wrapping a non-leaf one; a
    // box-less content-text marker -> an inline placeholder; only a truly unplaceable pseudo
    // refuses — do not silent-ship).
    if (!isIdentityTransform(c.transform)) addFlag("transform", path, `transform ${c.transform} not represented; review manually`, true);
    if (c.overflowX === "scroll" || c.overflowY === "scroll" || c.overflowX === "auto" || c.overflowY === "auto") addFlag("overflow-scroll", path, "scroll container flattened; content may clip", true);
    const animDeclared = rich.declared.animation && !/^(none|initial|inherit)\b/.test(rich.declared.animation.trim());
    if (animDeclared || (c.animationName && c.animationName !== "none")) {
      const animName = rich.declared.animation ? rich.declared.animation.trim().split(/\s+/).find((t) => !/^\d|^(ease|linear|infinite|alternate|both|forwards|backwards|normal|reverse|s|ms)/.test(t)) || c.animationName : c.animationName;
      addFlag("animation", path, `@keyframes ${animName} not represented (static frame)`, true);
    }
    // box-shadow (single or stacked) maps to effects[] in v0.2 (ADR-010); no flag.
    // missing font: not a brand family and not a generic keyword
    if (rich.text && !rich.font.brand && !rich.font.generic) {
      missingFonts.add(rich.font.family);
      addFlag("missing-font", path, `"${rich.font.family}" is not a brand family; the workspace will likely lack it`, true);
    }
    // corner-radius / borders / box-shadow / opacity now have node slots (v0.2, ADR-010);
    // they are emitted by decorations() rather than flagged as schema gaps.
  }

  // ---- P3 (Gap 3 / ADR-013): place a child inside a NONE-layout container ----
  // A Figma frame with no auto-layout positions every child by x/y, so each child
  // of such a container carries its offset from the parent frame's top-left
  // (child.bbox - parent.bbox). A full-bleed child (inset:0 — its box matches the
  // parent's) is modelled as fill-parent (sizing FILL/FILL at the origin) so it
  // tracks the parent if resized, rather than a fixed box pinned at one size.
  function placeInParent(rich, parentRich, path) {
    const b = rich.bbox, pb = parentRich.bbox;
    const x = round(b.x - pb.x), y = round(b.y - pb.y);
    const fullBleed =
      Math.abs(b.x - pb.x) < 0.5 && Math.abs(b.y - pb.y) < 0.5 &&
      Math.abs(b.w - pb.w) < 0.5 && Math.abs(b.h - pb.h) < 0.5;
    const abs = rich.computed.position === "absolute" || rich.computed.position === "fixed";
    if (abs) addFlag("absolute-positioning", path, `placed at x:${fullBleed ? 0 : x} y:${fullBleed ? 0 : y} in the NONE-layout parent (was collapsing to origin)`, false);
    return { position: { x: fullBleed ? 0 : x, y: fullBleed ? 0 : y }, fullBleed };
  }

  // ---- R-1=D (region-scoped structural block) + the non-leaf / box-null follow-up: emit a
  // visible ::before/::after as a needs-human PLACEHOLDER, never a whole-build halt (D-03) and
  // never a silent drop. Three shapes, in descending fidelity:
  //   1. Resolvable box + CHILDLESS FRAME/GROUP host -> flip the host to NONE-layout IN PLACE
  //      and add the placeholder child (the coverage-bar / progress-fill leaf pattern; the host
  //      has no layout to protect, so an in-place flip is safe).
  //   2. Resolvable box + any OTHER host (a host with children, or a non-frame TEXT/CHIP host)
  //      -> WRAP the host in a NONE-layout container [host, placeholder] so the host keeps its
  //      own layout and the positioned placeholder is still honoured (the interpreter honours a
  //      positioned child only under a NONE parent, ADR-013). A leaf flip would corrupt an
  //      existing auto-layout; the wrapper never does. (non-leaf follow-up.)
  //   3. NO resolvable box but visible CONTENT text (an in-flow `position:static` marker such as
  //      content:"▸ ", whose getComputedStyle width is `auto`) -> WRAP the host in a HORIZONTAL
  //      auto-layout [placeholder, host] so the marker ships as an inline needs-human slot where
  //      it renders. No captured box, so a nominal ~1em square stands in. (box-null follow-up.)
  // Only a box-less pseudo with NO content (an empty in-flow static ::before) or an incoherent
  // box+inline mix on one host still REFUSES (a blocking `pseudo-element` flag). The placeholder
  // is intentionally NOT the faithful paint: a neutral fill + outline + a sentence-case ⚠ marker
  // so the region reads as unresolved and a human confirms it. handlePseudo returns the node to
  // emit — the mutated host, or a wrapper around it — and mapNode uses that return value. ----
  const PSEUDO_PLACEHOLDER_FILL = { type: "SOLID", resolved: "#EDEAE3" };
  const PSEUDO_PLACEHOLDER_STROKE = { weight: 1, align: "INSIDE", color: { type: "SOLID", resolved: "#B0A99A" } };
  // A pseudo carries visible TEXT even with no resolvable box: a quoted non-empty content string
  // (content:"▸ ") or a generated-content function (counter()/attr()). An empty content:"" is the
  // decorative-box idiom (always paired with a resolvable box) and is NOT content text.
  function pseudoHasContentText(p) {
    if (!p || !p.content) return false;
    if (String(p.content).replace(/^\s*["']|["']\s*$/g, "").trim().length) return true;
    return /\b(counter|counters|attr)\s*\(/.test(p.content);
  }
  // A placeholder FRAME at a resolvable box, offset inside a NONE-layout container whose origin is
  // `originBbox` (viewport coords). Shared by the leaf-flip (shape 1) and the box-wrap (shape 2).
  const pseudoPlaceholderBox = (which, box, originBbox) => ({
    type: "FRAME", name: `⚠ ${which} (needs human)`,
    size: { w: round(box.w), h: round(box.h), sizing: { h: "FIXED", v: "FIXED" } },
    position: { x: round(box.x - originBbox.x), y: round(box.y - originBbox.y) },
    fills: [PSEUDO_PLACEHOLDER_FILL], strokes: [PSEUDO_PLACEHOLDER_STROKE], opacity: 0.9,
  });
  // A placeholder FRAME for an inline content-text pseudo with no resolvable box: a nominal ~1em
  // square placed by auto-layout (no position), sized from the host font. (shape 3.)
  const pseudoPlaceholderInline = (which, fpx) => {
    const s = round(Math.max(fpx, 6));
    return { type: "FRAME", name: `⚠ ${which} (needs human)`,
      size: { w: s, h: s, sizing: { h: "FIXED", v: "FIXED" } },
      fills: [PSEUDO_PLACEHOLDER_FILL], strokes: [PSEUDO_PLACEHOLDER_STROKE], opacity: 0.9 };
  };
  function handlePseudo(node, rich, path) {
    if (!rich.pseudo || (!rich.pseudo.before && !rich.pseudo.after)) return node;
    const present = [["::before", rich.pseudo.before], ["::after", rich.pseudo.after]].filter(([, p]) => p);
    const which = present.map(([w]) => w).join(" / ");
    const boxed = present.filter(([, p]) => p.box);
    const inline = present.filter(([, p]) => !p.box && pseudoHasContentText(p));
    const dead = present.filter(([, p]) => !p.box && !pseudoHasContentText(p));
    const isFrameHost = node.type === "FRAME" || node.type === "GROUP";
    const childless = !(node.children && node.children.length);

    // Shape 1 + 2: every present pseudo resolves to a box.
    if (boxed.length && !inline.length && !dead.length) {
      const placeholders = boxed.map(([w, p]) => pseudoPlaceholderBox(w, p.box, rich.bbox));
      if (isFrameHost && childless) {
        node.layout = { mode: "NONE" };
        node.children = placeholders;
        addFlag("pseudo-placeholder", path,
          `${which} emitted as a needs-human placeholder at its captured box; confirm/apply the real paint`, true);
        return node;
      }
      // Shape 2: a non-leaf / non-frame host -> wrap so the host's own layout is preserved.
      addFlag("pseudo-placeholder", path,
        `${which} emitted as a needs-human placeholder at its captured box (host wrapped in a NONE-layout container so its own layout is preserved); confirm/apply the real paint`, true);
      return {
        type: "FRAME", name: node.name, layout: { mode: "NONE" },
        size: { w: round(rich.bbox.w), h: round(rich.bbox.h), sizing: { h: "FIXED", v: "FIXED" } },
        children: [{ ...node, position: { x: 0, y: 0 } }, ...placeholders],
      };
    }

    // Shape 3: a content-text pseudo with no resolvable box (an in-flow static marker) -> wrap in
    // a HORIZONTAL row so the marked slot ships inline before/after the host content.
    if (inline.length && !boxed.length && !dead.length) {
      const fpx = parsePx(rich.computed.fontSize) || 16;
      const before = inline.filter(([w]) => w === "::before").map(([w]) => pseudoPlaceholderInline(w, fpx));
      const after = inline.filter(([w]) => w === "::after").map(([w]) => pseudoPlaceholderInline(w, fpx));
      addFlag("pseudo-placeholder", path,
        `${which} is in-flow content with no resolvable box; host wrapped so the marker ships as a needs-human inline placeholder — confirm/apply the real content`, true);
      return {
        type: "FRAME", name: node.name,
        layout: { mode: "HORIZONTAL", primaryAxisAlignItems: "MIN", counterAxisAlignItems: "CENTER", itemSpacing: round(fpx * 0.3) },
        // Both axes HUG the [placeholder, host] content, so the wrapper size is null/null (NOT the
        // host bbox — a smaller fixed width there would read as its own content overflowing and
        // false-trip assert_geometry's lost-wrap check; a fixed height shorter than a tall marker
        // would clip it). The builder's frameAxisAuto keys HUG on a null axis, not the sizing tag.
        size: { w: null, h: null, sizing: { h: "HUG", v: "HUG" } },
        children: [...before, { ...node }, ...after],
      };
    }

    // Anything else (a box-less pseudo with no visible content, or an incoherent box+inline mix on
    // one host) -> REFUSE rather than silently ship. build_figma.preprocess_flags marks
    // `pseudo-element` blocking, so the build exits non-zero; --allow-blocking is the override.
    const reason = dead.length && !boxed.length && !inline.length
      ? "no resolvable box and no visible content (an empty in-flow/static pseudo)"
      : "the host's ::before/::after need incompatible placement (a positioned box vs an inline marker, or one is unplaceable) and cannot be wrapped coherently";
    addFlag("pseudo-element", path,
      `${which} could not be emitted as a placeholder (${reason}); the build refuses to ship it silently`, true);
    return node;
  }

  // ---- WS4 (B): interactive controls -> a deterministic styled control FRAME ----
  // A non-transparent bg paints as fills; a transparent-bg control WITH a border paints the
  // border as a real stroke (decorations() already emits it) so a ghost/secondary button is
  // an OUTLINE, never bare text. The text label is tagged with the UI/Button token_ref so the
  // WS3 style mode binds it to the shared Button text style. Children (icon + label) are kept.
  function nearInvisibleLabel(fills, children, path) {
    const solid = (fills || []).find((f) => f.type === "SOLID" && f.resolved);
    const label = (children || []).find((c) => c.type === "TEXT" && c.fills && c.fills[0] && c.fills[0].resolved);
    if (!solid || !label) return;
    const lb = relLuminance(parseColor(label.fills[0].resolved));
    const bg = relLuminance(parseColor(solid.resolved));
    if (lb == null || bg == null) return;
    const ratio = (Math.max(lb, bg) + 0.05) / (Math.min(lb, bg) + 0.05);
    if (ratio < 1.6) addFlag("near-invisible-label", path, `label vs control fill contrast ${round(ratio, 2)}:1 — likely unreadable; pick a visible label colour`, true);
  }
  function mapControl(rich, path) {
    const layout = mapLayout(rich, "FRAME", path);
    if (!layout.mode || layout.mode === "NONE") layout.mode = "HORIZONTAL";
    const deco = decorations(rich, path);   // cornerRadius + strokes(border) + effects
    const fills = bgFills(rich, path);       // [] when the control bg is transparent
    const name = nodeName(rich, "FRAME");
    let children;
    if (rich.children && rich.children.length) {
      children = rich.children.map((ch) => mapNode(ch, name, rich));
    } else if (rich.text) {
      const runs = mapRuns(rich, path);
      children = [{ type: "TEXT", name: `${name} Label`, characters: rich.text,
                    type_style: mapTypeStyle(rich, path), fills: textFill(rich, path), ...(runs ? { runs } : {}) }];
    } else {
      children = [];
    }
    // bind the (first) text label to the shared UI/Button style via the WS3 token_ref naming
    for (const ch of children) {
      if (ch.type === "TEXT") { ch.type_style = { ...(ch.type_style || {}), token_ref: "tokens.typography.scale.button" }; break; }
    }
    nearInvisibleLabel(fills, children, path);
    return { type: "FRAME", name, layout, size: mapSize(rich, "FRAME", layout),
             ...(fills.length ? { fills } : {}), ...deco, children };
  }

  // ---- D3 (P3): drop screen-reader-only children before they map ----
  // sr-only content must never render as a visible layer. Filtering here (before the type
  // and children decisions in mapNodeInner) keeps both the control path and the general path
  // clean. hasAbsChild is recomputed from the survivors: an sr-only node is position:absolute,
  // so a parent whose ONLY absolute child was sr-only would otherwise stay a positioned GROUP
  // after the drop, so the recompute lets it revert to a clean auto-layout FRAME. Recorded, not
  // silent (needs_human:false), per the extractor's no-silent-drop contract.
  function dropScreenReaderOnly(rich) {
    if (!rich.children || !rich.children.length) return;
    const selfName = nodeName(rich, "FRAME");
    const kept = [];
    for (const ch of rich.children) {
      if (isScreenReaderOnly(ch)) {
        addFlag("screen-reader-only", nodePath(ch, selfName),
          "screen-reader-only content (clipped to ~1px, overflow hidden) omitted; assistive-only text must not render as a visible layer", false);
      } else kept.push(ch);
    }
    if (kept.length !== rich.children.length) {
      rich.children = kept;
      // Mirror browser-capture's hasAbsChild predicate exactly (position:absolute), so this
      // is a faithful recompute over the survivors, not a new rule about what forces a GROUP.
      rich.hasAbsChild = kept.some((c) => c.computed && c.computed.position === "absolute");
    }
  }

  // ---- the recursive node mapper ----
  // The wrapper attaches P3 placement; mapNodeInner builds the node body unchanged
  // from the auto-layout path. A child of a NONE-layout container
  // (parentRich.hasAbsChild) is placed by x/y in Figma, so it carries position{x,y}.
  function mapNode(rich, parentName, parentRich) {
    let node = mapNodeInner(rich, parentName);
    node = handlePseudo(node, rich, nodePath(rich, parentName)) || node;   // R-1=D: placehold in place, wrap, or refuse
    if (parentRich && parentRich.hasAbsChild) {
      const { position, fullBleed } = placeInParent(rich, parentRich, nodePath(rich, parentName));
      node.position = position;
      if (fullBleed && node.size && node.size.sizing) { node.size.sizing.h = "FILL"; node.size.sizing.v = "FILL"; }
    }
    return node;
  }

  function mapNodeInner(rich, parentName) {
    const path = nodePath(rich, parentName);
    dropScreenReaderOnly(rich); // D3: strip sr-only children before type/children decisions
    collectFlags(rich, path);

    // WS4 (B): an interactive control with a visible box (bg, border, or .btn/.cta) becomes a
    // deterministic control FRAME so secondary/ghost buttons render as a real outline and never
    // collapse to bare text. svg/img are media, never controls; a bare link (no box) falls
    // through to TEXT, where resolveColor's anti-snap guard keeps its colour visible.
    if (rich.tag !== "svg" && rich.tag !== "img" && isInteractiveControl(rich) && isButtonLike(rich)) {
      return mapControl(rich, path);
    }

    // node type
    let type;
    let svgContent = null;
    if (rich.tag === "svg") { type = "VECTOR"; svgContent = rich.svgOuter; }
    else if (rich.tag === "img") {
      // Gap 1: an <img> pointing at an .svg is a VECTOR, not a raster. The builder
      // already imports SVG to editable vectors (createNodeFromSvg); the bug was
      // the misclassification that routed these to the grey-placeholder path. A
      // raster <img> (jpg/png/webp) or an unreadable svg still falls through to IMAGE.
      const src = rich.imgSrc || "";
      const content = /\.svg(\?|#|$)/i.test(src) ? svgAssets[src] : null;
      if (content) { type = "VECTOR"; svgContent = content; }
      else type = "IMAGE";
    }
    else if (rich.children.length > 0) type = rich.hasAbsChild ? "GROUP" : "FRAME";
    else if (rich.text && !isTransparent(rich.computed.backgroundColor)) type = "CHIP"; // FRAME wrapping a synthetic TEXT
    else if (rich.text) type = "TEXT";
    else type = "FRAME";

    const name = nodeName(rich, type === "CHIP" ? "FRAME" : type);
    const deco = decorations(rich, path); // cornerRadius / strokes / effects / opacity

    if (type === "VECTOR") {
      const hash = crypto.createHash("sha1").update(svgContent).digest("hex").slice(0, 8);
      const file = `prototypes/assets/vec-${hash}.svg`;
      assets.push({ file, content: svgContent });
      // an <img>-sourced vector carries its CSS display size so the builder can
      // scale the imported svg to the laid-out box (Gap 1).
      const sized = rich.tag === "img" ? { size: mapSize(rich, "IMAGE") } : {};
      return { type: "VECTOR", name, svgRef: file, ...sized, ...deco };
    }
    if (type === "IMAGE") {
      const ref = resolveImageRef(rich.imgSrc, protoDir);
      return { type: "IMAGE", name, imageRef: ref, size: mapSize(rich, "IMAGE"), ...deco };
    }
    if (type === "TEXT") {
      // Gap 4a: TEXT carries size so a wrapped block fills its column. Gap 4c
      // (P4): TEXT carries runs[] for its inline styled ranges (accent / emphasis).
      const runs = mapRuns(rich, path);
      return { type: "TEXT", name, characters: rich.text, type_style: mapTypeStyle(rich, path), fills: textFill(rich, path), size: mapSize(rich, "TEXT"), ...(runs ? { runs } : {}), ...deco };
    }
    if (type === "CHIP") {
      // a leaf with both text and a background: FRAME (bg + padding) wrapping one TEXT.
      // decorations (radius/border/shadow) belong on the box, not the inner text.
      const chipRuns = mapRuns(rich, path);
      const label = { type: "TEXT", name: `${name} Label`, characters: rich.text, type_style: mapTypeStyle(rich, path), fills: textFill(rich, path), ...(chipRuns ? { runs: chipRuns } : {}) };
      const chipLayout = mapLayout(rich, "FRAME", path);
      return {
        type: "FRAME", name,
        layout: chipLayout,
        size: mapSize(rich, "FRAME", chipLayout),
        fills: bgFills(rich, path),
        ...deco,
        children: [label],
      };
    }

    // FRAME / GROUP
    const layout = mapLayout(rich, type, path);
    const node = { type, name, layout, size: mapSize(rich, type, layout) };
    const fills = bgFills(rich, path);
    if (fills.length) node.fills = fills;
    Object.assign(node, deco);
    if (rich.children.length) node.children = rich.children.map((ch) => mapNode(ch, name, rich));
    return node;
  }

  const root = mapNode(capture.root, null, null);

  // WS-B (page-hug): the document body is always a hugging vertical stack. If the body
  // falls to NONE (an absolutely-positioned descendant -> GROUP) or carries a fixed
  // height, the footer floats below a stale box — the footer/last-section gap. Force
  // VERTICAL + HUG height at the document root; absolute positioning is modelled inside
  // sections (ADR-013), never by collapsing the body. Gated to tag==='body' so a fixture
  // rooted at a section/grid is unaffected.
  if (capture.root && capture.root.tag === "body") {
    if (root.type === "GROUP") root.type = "FRAME";
    root.layout = root.layout || {};
    root.layout.mode = "VERTICAL";
    if (root.size) { root.size.sizing = root.size.sizing || {}; root.size.sizing.v = "HUG"; root.size.h = null; }
    // WS-A (backgrounds): the page must be painted, or every section that inherits the
    // body background renders white on bare canvas (a transparent section frame shows the
    // document root behind it). Flag an unpainted body for review.
    if (!root.fills || !root.fills.length) {
      addFlag("root-background-unresolved", root.name || "Page",
        "document root has no resolved background; inheriting sections render white — set a body/page background", true);
    }
  }

  if (flags.length) root.flags = flags;

  const ir = {
    $schema: "heyhi-scene-graph/v0.4",
    meta: { source, breakpoint, brand_config: brandConfig, generated_by: GENERATED_BY },
    tokens_used: [...tokensUsed.values()],
    root,
  };

  // dedupe assets by file (the same VECTOR appears at every breakpoint)
  const assetByFile = new Map();
  for (const a of assets) if (!assetByFile.has(a.file)) assetByFile.set(a.file, a);

  return { ir, assets: [...assetByFile.values()], missingFonts: [...missingFonts] };
}
