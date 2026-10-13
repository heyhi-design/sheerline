// SVGO config for the HeyHi Design Bridge vectorizer.
// Conservative on purpose: cleanup is for coordinate/precision economy, NOT for
// restructuring. Keep the viewBox (landing + fidelity rasterize depend on it) and
// keep per-color paths separate (mergePaths off) so the result stays editable in
// Figma. floatPrecision trims bytes; it does not reduce anchor count.
export default {
  multipass: true,
  plugins: [
    {
      name: 'preset-default',
      params: {
        overrides: {
          removeViewBox: false,
          mergePaths: false,
          removeHiddenElems: false,
          convertShapeToPath: false,
          convertPathData: { floatPrecision: 2, transformPrecision: 2 },
          cleanupNumericValues: { floatPrecision: 2 },
          convertTransform: { floatPrecision: 2 },
        },
      },
    },
  ],
};
