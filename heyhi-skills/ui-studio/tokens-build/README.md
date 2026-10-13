# tokens-build — DTCG-native → CSS transform (Style Dictionary)

**HeyHi Internal Use Only.** Sheerline W5 / audit G7 (Phase B2).

Proves the interop half of audit G7 the design harness was missing: a ui-studio brand config
authored **DTCG-native** (via `../scripts/dtcg-codemod.py`) is a valid **Style Dictionary**
input with no adapter, emitting CSS custom properties. This closes "reads/validates DTCG
but authors proprietary, web-only emit" — DTCG is now the shared interchange the config
projects *out* through, not just a format it reads *in*.

## Run

```bash
cd heyhi-skills/ui-studio/tokens-build
npm install
npm run build          # -> build/tokens.css (and build/tokens.dtcg.json, the clean source)
node prep.mjs acme.json && npx style-dictionary build --config style-dictionary.config.mjs
                       # same, for another config in ../brand-config/
```

`npm run build` runs two steps:

1. `prep.mjs` reads `../brand-config/<config>`. The default is the config an instance names
   in `../brand-config/default-config.txt` (an instance file, not shipped in a scaffold
   export); without it, `example.json`, the generic reference config, DTCG-native in place. A legacy scalar config yields zero
   tokens and fails loudly; convert it first with
   `python3 ../scripts/dtcg-codemod.py --config ../brand-config/<config>.json --in-place --yes`
   (or review the sibling `<config>.dtcg.json` the codemod writes without `--in-place`).
   It extracts a **clean DTCG document** from its `tokens` subtree — pruning the non-token
   metadata a ui-studio config carries in that namespace (prose `use`/`rhythm`/`principles`,
   arrays like `prohibited`, booleans). Style Dictionary consumes DTCG tokens, not metadata.
2. `style-dictionary build` emits `build/tokens.css` from that source.

Both `node_modules/` and `build/` are gitignored — the durable artifacts are the config,
`prep.mjs`, and the lockfile.

## Version note

The parent plan referenced Style Dictionary **v4**; the current stable major is **v5**
(`^5.5.3` at authoring). v5 is likewise DTCG-first-class (parses `$value`/`$type`, resolves
`{alias}` references). This build pins v5.

## Transforms

Deliberately minimal and value-preserving: `attribute/cti` + `name/kebab`. The default `css`
transformGroup is **not** used — its `size/rem` transform rejects CSS `clamp()` dimensions
(the responsive type scale) and `color/css` lowercases hex. Emitting values verbatim keeps
the transform a faithful projection of the source (the fidelity a token projection needs). Value
normalisation, and the canonical custom-property name per role for a specific target, are
target decisions recorded by a human, not forced here.

Names default to the token path: `color.accent.primary` → `--color-accent-primary`.

## Scope (this cut) and one finding

- **Native platforms (Swift/Kotlin) are deferred.** Style Dictionary ships `ios-swift` /
  `android` formats once a DTCG source exists, but there is no current native consumer —
  building it now is infrastructure ahead of need (parent plan B2).
- **This does NOT replace a site's existing hand-authored theme.** Read the target's theme
  first-hand before assuming it is a projection of the brand config. In the instance's own
  first proof run, the site's Tailwind v4 `@theme` block turned out to be a **separately
  hand-curated set**: only the accent and the font families matched the config, while the
  background, text, and muted colors differed and one theme color had no source token at all.
  Collapsing such a theme into a build output of this transform is a **value migration** (it
  changes rendered colors), not a mechanical no-op. The migration is a deliberate, reviewed
  human decision, not part of this build.
