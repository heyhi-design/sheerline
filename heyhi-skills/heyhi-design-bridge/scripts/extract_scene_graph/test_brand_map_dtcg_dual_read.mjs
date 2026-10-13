// Dual-read test for brand-map.mjs — proves the DTCG-native authoring shim.
//
// STAGED (skill-updates/, awaiting human review). BrandMap must build IDENTICAL
// token maps whether the ui-studio brand-config is authored in the legacy
// bare-scalar shape or migrated to DTCG objects ({ "$value": ... }). Without the
// shim a migrated colour leaf makes buildColorTokens recurse into the DTCG object
// and emit `--color-accent-primary-$value`, and the numeric builders emit
// `[object Object]`. Fixtures are a matched pair: fixtures/brand-dtcg.json is
// fixtures/brand-scalar.json run through the real dtcg-codemod.py.
//
// NOTE ON RUNNING: this imports ./lib/brand-map.mjs, which imports ./lib/color.mjs.
// After the staged brand-map.mjs is promoted into the deployed skill, run this
// from the deployed extract_scene_graph/ dir (where color.mjs sits alongside):
//   node test_brand_map_dtcg_dual_read.mjs
// It was proven in-session (CLOSE-02) against the deployed color.mjs via a temp harness.
// Run: exit 0 = pass, non-zero = fail.

import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { BrandMap, loadConfig } from "./lib/brand-map.mjs";

const here = dirname(fileURLToPath(import.meta.url));
const SCALAR = resolve(here, "fixtures/brand-scalar.json");
const DTCG = resolve(here, "fixtures/brand-dtcg.json");

// --- Anti-false-clean control: the DTCG fixture must REALLY be DTCG-shaped. ---
const dtcgRaw = JSON.parse(readFileSync(DTCG, "utf8"));
const accent = dtcgRaw.tokens.color.accent.primary;
assert.ok(
  accent && typeof accent === "object" && "$value" in accent,
  "control FAILED: fixtures/brand-dtcg.json accent.primary is not a DTCG object — the test would be vacuous",
);

const scalar = new BrandMap(loadConfig(SCALAR));
const dtcg = new BrandMap(loadConfig(DTCG));

// --- The core claim: identical token maps + identical emitted :root CSS. ---
const serialize = (bm) => JSON.stringify({
  color: bm.colorTokens,
  spacing: bm.spacingTokens,
  scalar: bm.scalarTokens,
  fonts: bm.fontFamilies,
}, null, 2);

assert.equal(serialize(dtcg), serialize(scalar), "DTCG token maps differ from scalar token maps");
assert.equal(dtcg.emitRootCss(), scalar.emitRootCss(), "DTCG :root CSS differs from scalar :root CSS");

// --- No leakage of the DTCG wrapper into token paths or emitted values. ---
const css = dtcg.emitRootCss();
assert.ok(!css.includes("[object Object]"), "emitted CSS contains [object Object] — a DTCG object leaked unresolved");
assert.ok(!css.includes("$value"), "emitted CSS contains $value — a DTCG object leaked unresolved");
assert.ok(!dtcg.colorTokens.some((t) => t.css_var.includes("$value") || t.token_path.includes("$value")),
  "a colour token leaked a -$value segment — the recurse descended into a DTCG leaf");
// --- Array recursion must be preserved (the ui-studio configs carry tokens.color.prohibited[],
// an array the original walk descends into; the shim must NOT skip arrays). ---
assert.ok(dtcg.colorTokens.some((t) => t.token_path === "tokens.color.prohibited.0.value"),
  "expected the array-nested tokens.color.prohibited.0.value colour token — the recurse must descend into arrays, not just plain groups");
// --- Positive assertions that values actually resolved from the DTCG leaves. ---
assert.ok(css.includes("--color-accent-primary: #E4572E;"), "expected --color-accent-primary to resolve to #E4572E");
assert.ok(css.includes("--type-h1: 2.5rem;"), "expected --type-h1 to resolve to 2.5rem from the DTCG dimension leaf");
assert.ok(css.includes("--radius-sm: 4px;"), "expected --radius-sm to resolve to 4px from the DTCG dimension leaf");
assert.ok(css.includes("--spacing-md: 1rem;"), "expected --spacing-md to resolve to 1rem from the DTCG dimension leaf");

console.log("PASS — brand-map.mjs dual-read: scalar and DTCG configs build identical token maps + :root CSS.");
console.log(`  colour tokens: ${dtcg.colorTokens.length}, scalar tokens: ${dtcg.scalarTokens.length}, spacing tokens: ${dtcg.spacingTokens.length}; no wrapper leakage.`);
