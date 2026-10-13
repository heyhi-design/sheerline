// prep.mjs — extract a clean DTCG document from a ui-studio brand config's `tokens`
// subtree (W5 / audit G7 B2).
//
// A ui-studio config after `dtcg-codemod.py` mixes DTCG token objects ({"$value",...})
// with non-token metadata that shares the tokens namespace: prose ("use", "rhythm",
// "principles", "hierarchy_note"), arrays ("prohibited", "contrast_notes", font
// "weights"), and booleans ("variable"). Style Dictionary consumes DTCG tokens, so this
// prunes everything that is NOT a token object (or a group that leads to one), producing
// a source Style Dictionary accepts with no adapter — the interop point of G7.
//
// Input:  ../brand-config/<config>  (default: the instance's default-config.txt, else example.json,
//         DTCG-native in place; override via argv[2], e.g. `node prep.mjs acme.json`).
//         Any config whose `tokens` subtree is DTCG-native (scalars converted to
//         {"$value",...}) is read directly with no sibling file, the single-source intent
//         of the in-place migration. A legacy scalar config yields zero tokens and fails.
// Output: build/tokens.dtcg.json

import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

// The default config is an instance setting: an instance names its own brand config in
// ../brand-config/default-config.txt (instance-only, never shipped in a scaffold export).
// Without it, the generic reference config is used.
const DEFAULT_FILE = new URL('../brand-config/default-config.txt', import.meta.url);
const instanceDefault = existsSync(DEFAULT_FILE) ? readFileSync(DEFAULT_FILE, 'utf8').trim() : '';
const configName = process.argv[2] ?? (instanceDefault || 'example.json');
const SRC = new URL(`../brand-config/${configName}`, import.meta.url);
const OUT_DIR = new URL('./build/', import.meta.url);
const OUT = new URL('./build/tokens.dtcg.json', import.meta.url);

const isToken = (n) =>
  n && typeof n === 'object' && !Array.isArray(n) && Object.prototype.hasOwnProperty.call(n, '$value');

// Keep DTCG tokens whole; keep groups only if they still contain a token after pruning;
// drop bare scalars and arrays (config metadata that is not a design token).
function prune(node) {
  if (isToken(node)) return node;
  if (node && typeof node === 'object' && !Array.isArray(node)) {
    const out = {};
    for (const [k, v] of Object.entries(node)) {
      const p = prune(v);
      if (isToken(p) || (p && typeof p === 'object' && !Array.isArray(p) && Object.keys(p).length)) {
        out[k] = p;
      }
    }
    return out;
  }
  return undefined;
}

let config;
try {
  config = JSON.parse(readFileSync(SRC, 'utf8'));
} catch (err) {
  console.error(
    `prep: cannot read ${fileURLToPath(SRC)}.\n` +
      `Pass a config name that exists in ../brand-config/ (default: example.json).\n` +
      `For a legacy (scalar) config, convert it in place first:\n` +
      `  python3 ../scripts/dtcg-codemod.py --config ../brand-config/<config>.json --in-place`,
  );
  process.exit(1);
}

const tokens = prune(config.tokens ?? {});
const count = JSON.stringify(tokens).match(/"\$value"/g)?.length ?? 0;
if (count === 0) {
  // A legacy scalar config prunes to nothing. Fail loudly rather than write an empty
  // source that Style Dictionary would "build" into an empty tokens.css.
  console.error(
    `prep: ${configName} has no DTCG tokens (a legacy scalar config).\n` +
      `Convert it in place first:\n` +
      `  python3 ../scripts/dtcg-codemod.py --config ../brand-config/${configName} --in-place --yes`,
  );
  process.exit(1);
}
mkdirSync(OUT_DIR, { recursive: true });
writeFileSync(OUT, JSON.stringify(tokens, null, 2) + '\n');
console.log(`prep: wrote ${count} DTCG tokens -> ${fileURLToPath(OUT)}`);
