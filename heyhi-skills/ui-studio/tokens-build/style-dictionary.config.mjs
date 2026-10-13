// Style Dictionary v5 config — DTCG-native token -> CSS custom properties (W5 / audit G7).
//
// The point of this file: a DTCG-native brand config is a valid Style Dictionary input
// with NO adapter. Style Dictionary v5 parses $value/$type natively and resolves DTCG
// {alias} references, then runs the built-in `css/variables` format. `prep.mjs` produces
// the clean DTCG source (build/tokens.dtcg.json) from the ui-studio config's token subtree.
//
// Names: the default CSS transform derives each custom-property name from the token's
// path (e.g. color.accent.primary -> --color-accent-primary). The canonical name per
// role for any specific TARGET (e.g. a site's shorter --color-accent) is a recorded
// human decision, not fixed here.
//
// Native Swift/Kotlin transforms (ios-swift / android formats) are available once a DTCG
// source exists, but are out of this cut — no current native consumer (parent plan B2).

// Transform set is deliberately minimal and value-preserving: `name/kebab` for the
// custom-property name, `attribute/cti` for categorisation. We do NOT use the default
// `css` transformGroup, because its `size/rem` transform rejects CSS `clamp()`
// dimensions (the responsive type scale) and its `color/css` transform lowercases hex —
// both mutate the authored value. Emitting values verbatim keeps the transform a
// faithful projection of the DTCG source (the fidelity the G7 proof needs); brand
// value normalisation is a target-specific choice, not forced by the transform.
export default {
  source: ['build/tokens.dtcg.json'],
  platforms: {
    css: {
      transforms: ['attribute/cti', 'name/kebab'],
      buildPath: 'build/',
      files: [
        {
          destination: 'tokens.css',
          format: 'css/variables',
          options: { outputReferences: true },
        },
      ],
    },
  },
};
