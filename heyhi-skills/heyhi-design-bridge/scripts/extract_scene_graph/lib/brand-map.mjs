// brand-map.mjs — turn a ui-studio brand-config into the authoritative token
// maps the extractor resolves declared CSS values against.
//
// The CSS-var <-> token-path convention is built FORWARD from the config, exactly
// mirroring heyhi-skills/ui-studio/scripts/cursor-export.py (recurse(color_obj,
// "--color", "tokens.color")). Reverse-parsing var names is wrong because token
// segments contain hyphens (e.g. backgrounds.dark-surface -> --color-backgrounds-
// dark-surface); only a forward build is exact.
//
// STAGED EDIT (skill-updates/, awaiting human review — heyhi-design-bridge is a
// deployed skill). Adds the DTCG-native authoring shim (resolveTokenValue /
// isDtcgToken / isTokenGroup) mirroring heyhi-skills/ui-studio/scripts/tokens.py,
// so every token-value read tolerates BOTH a bare scalar ("#E4572E") and a DTCG
// object ({ "$value": "#E4572E", "$type": "color" }). This is the precondition W5
// Phase B (PR #886) left for the in-place brand-config DTCG migration: without it, a
// migrated leaf makes buildColorTokens recurse INTO the DTCG object and emit
// `--color-accent-primary-$value` instead of `--color-accent-primary`, and the
// numeric builders emit `[object Object]`. Behaviour-preserving for scalar configs
// (every value onboarded today resolves to itself). Source: CLOSE-02 W5 (dispatch-
// prompts-2026-09-13-sheerline-closeout.md); plan-sheerline-dtcg-interop-2026-09-12.md.

import fs from "node:fs";
import { parseColor, toHex, colorDistance, distanceToConfidence } from "./color.mjs";

const REM_PX = 16; // assumes default 1rem = 16px (the prototype does not override html font-size)

// --------------------------------------------------------------------------- //
// DTCG-native authoring shim (semantics-for-semantics with tokens.py:
// is_dtcg_token / resolve_token_value / is_token_group).
// --------------------------------------------------------------------------- //

/** A plain object (a dict), not an array and not null — the JS analogue of Python's isinstance(node, dict). */
function isPlainObject(node) {
  return node != null && typeof node === "object" && !Array.isArray(node);
}

/** True iff `node` is a DTCG token object (a dict carrying `$value`). */
function isDtcgToken(node) {
  return isPlainObject(node) && "$value" in node;
}

/**
 * The concrete value of a token leaf, whatever shape it was authored in:
 *   - bare scalar (string/number/boolean/array) -> returned unchanged (legacy)
 *   - DTCG object { "$value": v, ... }           -> v
 *   - a nested group (a dict WITHOUT $value)      -> null, the recurse/leaf signal
 * The null return is the recurse discriminator: callers descend only when it is null.
 */
function resolveTokenValue(node) {
  if (isDtcgToken(node)) return node["$value"];
  if (isPlainObject(node)) return null; // a group, not a leaf — caller should recurse
  return node; // a bare scalar leaf (legacy)
}

/** True iff `node` is a nested group to recurse into (a dict that is NOT a DTCG token). */
function isTokenGroup(node) {
  return isPlainObject(node) && !isDtcgToken(node);
}

/** token_path (tokens.color.accent.primary) -> figma_variable (color/accent/primary). */
function figmaVarName(tokenPath) {
  return tokenPath.replace(/^tokens\./, "").replace(/\./g, "/");
}

/** rem/px string -> number of px, or null for clamp()/calc()/unresolvable. */
function toPx(value) {
  if (typeof value !== "string") return null;
  const v = value.trim();
  if (/clamp\(|calc\(|var\(|min\(|max\(/.test(v)) return null;
  let m = v.match(/^(-?\d*\.?\d+)px$/);
  if (m) return parseFloat(m[1]);
  m = v.match(/^(-?\d*\.?\d+)rem$/);
  if (m) return parseFloat(m[1]) * REM_PX;
  m = v.match(/^(-?\d*\.?\d+)$/);
  if (m) return parseFloat(m[1]);
  return null;
}

export function loadConfig(configPath) {
  return JSON.parse(fs.readFileSync(configPath, "utf8"));
}

/** Recurse tokens.color exactly like cursor-export.py, keeping only colour leaves. */
function buildColorTokens(config) {
  const out = [];
  const recurse = (obj, cssPrefix, pathPrefix) => {
    for (const [key, value] of Object.entries(obj || {})) {
      const cssVar = `${cssPrefix}-${key}`;
      const tokenPath = `${pathPrefix}.${key}`;
      const resolved = resolveTokenValue(value); // DTCG object -> $value; scalar -> itself; group/array -> null
      if (typeof resolved === "string") {
        const rgb = parseColor(resolved);
        if (!rgb) continue; // skip hierarchy_note / prose leaves — not colours
        out.push({ css_var: cssVar, token_path: tokenPath, figma_variable: figmaVarName(tokenPath), value: toHex(rgb), rgb });
      } else if (value && typeof value === "object" && !isDtcgToken(value)) {
        // A nested group OR an array — descend, exactly like the original
        // cursor-export.py walk (arrays recurse by index, e.g. the
        // tokens.color.prohibited[0].value entry the ui-studio configs carry). NEVER a DTCG
        // token object, which is a leaf already resolved above. This deliberately
        // recurses arrays too (isTokenGroup would exclude them), so a legacy
        // config that recurses an array is behaviour-preserving.
        recurse(value, cssVar, tokenPath);
      }
    }
  };
  recurse(config?.tokens?.color, "--color", "tokens.color");
  return out;
}

/** Spacing vars, mirroring cursor-export.py extract_spacing(). */
function buildSpacingTokens(config) {
  const s = config?.tokens?.spacing || {};
  const out = [];
  // Resolve every value through the DTCG shim so a migrated ($value) leaf and a
  // legacy scalar both store the concrete value (and toPx sees a string, not an object).
  const add = (cssVar, tokenPath, value) => {
    const resolved = resolveTokenValue(value);
    out.push({ css_var: cssVar, token_path: tokenPath, value: resolved, px: toPx(resolved) });
  };
  if (s.base != null) add("--spacing-base", "tokens.spacing.base", s.base);
  for (const [tier, value] of Object.entries(s.tiers || {})) add(`--spacing-${tier}`, `tokens.spacing.tiers.${tier}`, value);
  if (s.content_max_width) add("--content-max-width", "tokens.spacing.content_max_width", s.content_max_width);
  if (s.page_padding) add("--page-padding", "tokens.spacing.page_padding", s.page_padding);
  if (s.grid_gap) add("--grid-gap", "tokens.spacing.grid_gap", s.grid_gap);
  const tt = s["touch-target"];
  // touch-target may be a DTCG leaf (future), a { min } group (current), or a scalar.
  if (tt != null) add("--spacing-touch-target", "tokens.spacing.touch-target", isDtcgToken(tt) ? tt : (isTokenGroup(tt) ? tt.min : tt));
  return out;
}

/** Type-scale vars (--type-{name}) and radius vars. */
function buildScalarTokens(config) {
  const out = [];
  for (const [name, value] of Object.entries(config?.tokens?.typography?.scale || {})) {
    const resolved = resolveTokenValue(value);
    out.push({ css_var: `--type-${name}`, token_path: `tokens.typography.scale.${name}`, value: resolved, px: toPx(resolved) });
  }
  for (const [name, value] of Object.entries(config?.tokens?.radius || {})) {
    const resolved = resolveTokenValue(value);
    out.push({ css_var: `--radius-${name}`, token_path: `tokens.radius.${name}`, value: resolved, px: toPx(resolved) });
  }
  return out;
}

/** Brand font families, lower-cased for matching against computed font-family. */
function buildFontFamilies(config) {
  const fams = config?.tokens?.typography?.families || {};
  return Object.entries(fams).map(([role, def]) => ({
    role, family: def.family, lower: String(def.family || "").toLowerCase(),
    token_path: `tokens.typography.families.${role}`,
  }));
}

export class BrandMap {
  constructor(config, { brandName = "example" } = {}) {
    this.brandName = brandName;
    this.colorTokens = buildColorTokens(config);
    this.spacingTokens = buildSpacingTokens(config);
    this.scalarTokens = buildScalarTokens(config);
    this.fontFamilies = buildFontFamilies(config);
    // Index by css-var for O(1) declared-var lookups.
    this.byCssVar = new Map();
    for (const t of [...this.colorTokens, ...this.spacingTokens, ...this.scalarTokens]) this.byCssVar.set(t.css_var, t);
  }

  /** Exact declared lookup: a bare var(--x) resolves to its token, source "declared". */
  lookupVar(cssVar) {
    return this.byCssVar.get(cssVar) || null;
  }

  /**
   * Nearest colour token to a resolved literal. `preferContains` breaks exact
   * ties by role: a text colour that ties between text.primary and
   * backgrounds.dark (same hex) should bind to the text token, not the bg one.
   * Returns null if the literal is unparseable.
   */
  nearestColor(literal, preferContains = null) {
    const rgb = parseColor(literal);
    if (!rgb) return null;
    let min = Infinity, pool = [];
    for (const t of this.colorTokens) {
      const d = colorDistance(rgb, t.rgb);
      if (d < min - 1e-9) { min = d; pool = [t]; }
      else if (Math.abs(d - min) < 1e-9) pool.push(t);
    }
    if (!pool.length) return null;
    let token = pool[0];
    if (preferContains) { const p = pool.find((t) => t.token_path.includes(preferContains)); if (p) token = p; }
    return { token, distance: min, resolved: toHex(rgb), confidence: distanceToConfidence(min) };
  }

  /** Nearest numeric spacing/radius token to a resolved px value. */
  nearestSpacing(px) {
    if (px == null) return null;
    const pool = [...this.spacingTokens, ...this.scalarTokens].filter((t) => t.px != null);
    let best = null;
    for (const t of pool) {
      const d = Math.abs(px - t.px);
      if (!best || d < best.distance) best = { token: t, distance: d };
    }
    if (!best) return null;
    // Confidence falls off with relative error; exact match -> 1.0.
    const conf = best.token.px === 0 ? (px === 0 ? 1 : 0) : Math.max(0, 1 - best.distance / Math.max(best.token.px, 8));
    return { ...best, confidence: conf };
  }

  /** Is this computed font-family one of the brand families? Returns the match or null. */
  matchFontFamily(computedFamily) {
    const first = String(computedFamily || "").split(",")[0].replace(/['"]/g, "").trim().toLowerCase();
    return this.fontFamilies.find((f) => f.lower === first) || null;
  }

  /** Emit the :root CSS block (colours + type scale + spacing + radius) for the golden prototype. */
  emitRootCss() {
    const lines = [":root {"];
    lines.push("  /* color */");
    for (const t of this.colorTokens) lines.push(`  ${t.css_var}: ${t.value};`);
    lines.push("  /* type scale */");
    for (const t of this.scalarTokens.filter((t) => t.css_var.startsWith("--type-"))) lines.push(`  ${t.css_var}: ${t.value};`);
    lines.push("  /* spacing */");
    for (const t of this.spacingTokens) lines.push(`  ${t.css_var}: ${t.value};`);
    lines.push("  /* radius */");
    for (const t of this.scalarTokens.filter((t) => t.css_var.startsWith("--radius-"))) lines.push(`  ${t.css_var}: ${t.value};`);
    lines.push("}");
    return lines.join("\n");
  }
}
