// color.mjs — parse CSS colors and measure perceptual distance for nearest-token
// matching. Kept dependency-free and small; the extractor only needs sRGB hex /
// rgb() values, which is what getComputedStyle returns.

const NAMED = {
  black: "#000000", white: "#ffffff", transparent: "#00000000",
  red: "#ff0000", green: "#008000", blue: "#0000ff", gray: "#808080",
  grey: "#808080", silver: "#c0c0c0",
};

/** Parse a CSS color string into {r,g,b,a} (0–255, a 0–1) or null if unparseable. */
export function parseColor(input) {
  if (!input) return null;
  let s = String(input).trim().toLowerCase();
  if (NAMED[s]) s = NAMED[s];

  // #rgb / #rgba / #rrggbb / #rrggbbaa
  if (s.startsWith("#")) {
    const h = s.slice(1);
    const ex = (a, b) => parseInt(a + b, 16);
    if (h.length === 3) return { r: ex(h[0], h[0]), g: ex(h[1], h[1]), b: ex(h[2], h[2]), a: 1 };
    if (h.length === 4) return { r: ex(h[0], h[0]), g: ex(h[1], h[1]), b: ex(h[2], h[2]), a: ex(h[3], h[3]) / 255 };
    if (h.length === 6) return { r: ex(h[0], h[1]), g: ex(h[2], h[3]), b: ex(h[4], h[5]), a: 1 };
    if (h.length === 8) return { r: ex(h[0], h[1]), g: ex(h[2], h[3]), b: ex(h[4], h[5]), a: ex(h[6], h[7]) / 255 };
    return null;
  }

  // rgb()/rgba(), both comma and space (slash-alpha) syntaxes
  const m = s.match(/^rgba?\(([^)]+)\)$/);
  if (m) {
    const parts = m[1].split(/[\s,/]+/).filter(Boolean);
    if (parts.length < 3) return null;
    const num = (v) => (v.endsWith("%") ? Math.round((parseFloat(v) / 100) * 255) : parseFloat(v));
    const a = parts[3] != null ? (parts[3].endsWith("%") ? parseFloat(parts[3]) / 100 : parseFloat(parts[3])) : 1;
    return { r: num(parts[0]), g: num(parts[1]), b: num(parts[2]), a };
  }
  return null;
}

/** Canonical #RRGGBB (uppercase) from {r,g,b}. Alpha dropped for token compare. */
export function toHex({ r, g, b }) {
  const h = (n) => Math.max(0, Math.min(255, Math.round(n))).toString(16).padStart(2, "0");
  return ("#" + h(r) + h(g) + h(b)).toUpperCase();
}

/**
 * Redmean colour distance — a cheap perceptual approximation that beats raw
 * Euclidean RGB for "is this the same brand colour" decisions.
 * https://en.wikipedia.org/wiki/Color_difference#sRGB
 */
export function colorDistance(c1, c2) {
  const rbar = (c1.r + c2.r) / 2;
  const dr = c1.r - c2.r, dg = c1.g - c2.g, db = c1.b - c2.b;
  return Math.sqrt(
    (2 + rbar / 256) * dr * dr +
    4 * dg * dg +
    (2 + (255 - rbar) / 256) * db * db
  );
}

// Distance between two identical-but-maximally-different colours, used to
// normalise a distance into a 0..1 confidence.
const MAX_DISTANCE = colorDistance({ r: 0, g: 0, b: 0 }, { r: 255, g: 255, b: 255 });

/** Map a redmean distance to a 0..1 confidence (1 = exact). */
export function distanceToConfidence(distance) {
  return Math.max(0, Math.min(1, 1 - distance / MAX_DISTANCE));
}
