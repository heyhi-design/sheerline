# React shim and codemod: templates and the worked example

*Reference for `ds-component-change`. The React code leg for a breaking change: the deprecation shim, the codemod, the ESLint entry, the migration note, and the changeset, as reusable templates and as the actual artifacts from the worked example (Button `fullWidth` to `block`). Load on demand. React is the only built leg for this arc (plan D5); Lit and Angular are in `adapters.md`.*

The worked-example artifacts live on the proof branch `ds-component-change-proof-2026-09-07` (propose-first, not merged) under `heyhi-design-intelligence-tests/packages/components/`. Paths below are relative to that package.

---

## 1. The deprecation shim

**Template.** The old prop stays in the interface with an `@deprecated` JSDoc naming the replacement and the codemod. In the body, the old value maps to the new one (new wins when both are set) and a one-time development-only warning fires when the old prop is used.

```tsx
export interface XProps {
  /** The new prop. */
  next?: T;
  /**
   * @deprecated Use `next` instead. `old` is still accepted and maps to
   * `next` (with a development-only warning); removed in the next major.
   * Codemod: `npx jscodeshift -t codemods/x-old-to-next.cjs <path>`.
   */
  old?: T;
}

// in the component body
if (old !== undefined) {
  warnDeprecation('[pkg] X: `old` is deprecated; use `next`. Codemod: ...');
}
const value = next ?? old ?? DEFAULT;
```

**The one-time warn helper** (`src/internal/warnDeprecation.ts`). One place so every shim warns identically and never in production. The `process` ambient is declared locally so it typechecks without `@types/node`, and the `typeof` guard keeps it safe in a browser where `process` is not defined.

```ts
declare const process: { env?: { NODE_ENV?: string } } | undefined;
const warned = new Set<string>();

export function warnDeprecation(message: string): void {
  const isProduction =
    typeof process !== 'undefined' && process?.env?.NODE_ENV === 'production';
  if (isProduction || warned.has(message)) return;
  warned.add(message);
  if (typeof console !== 'undefined' && typeof console.warn === 'function') {
    console.warn(message);
  }
}
```

**Worked example** (`src/components/Button/Button.tsx`). `fullWidth` becomes `block`; the internal `heyhi-button-wrapper--full-width` class is unchanged, so the rendered markup does not change. This is a pure API-surface rename.

```tsx
export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  // ...
  /** Stretch the button to fill the width of its container. */
  block?: boolean;
  /**
   * @deprecated Use `block` instead. `fullWidth` is still accepted and is
   * mapped to `block` (with a development-only warning); it will be removed in
   * the next major version. Codemod:
   * `npx jscodeshift -t codemods/button-fullWidth-to-block.cjs <path>`.
   */
  fullWidth?: boolean;
}

// body:
if (fullWidth !== undefined) {
  warnDeprecation(
    '[@heyhi/components] Button: the `fullWidth` prop is deprecated and will ' +
      'be removed in the next major version. Use `block` instead. Codemod: ' +
      'npx jscodeshift -t codemods/button-fullWidth-to-block.cjs <path>'
  );
}
const isBlock = block ?? fullWidth ?? false;
```

Neither `block` nor `fullWidth` reaches the DOM (both are destructured out of `...rest`).

## 2. The ESLint entry

Pair the linter with the JSDoc so enforcement and documentation agree. Pick the rule by what is deprecated:

- a deprecated **prop**: `no-restricted-syntax` on the JSX attribute (below);
- a deprecated **import** (a whole component): `no-restricted-imports` (the DI-audit gate's named rule);
- any `@deprecated` symbol: `eslint-plugin-deprecation`'s `deprecation/deprecation` reads the JSDoc directly (needs the plugin and TypeScript parser services).

**Worked example** (`.eslintrc.deprecations.cjs`):

```cjs
module.exports = {
  rules: {
    'no-restricted-syntax': ['warn', {
      selector:
        "JSXOpeningElement[name.name='Button'] > JSXAttribute[name.name='fullWidth']",
      message:
        'Button `fullWidth` is deprecated; use `block`. Codemod: npx jscodeshift -t node_modules/@heyhi/components/codemods/button-fullWidth-to-block.cjs <path>',
    }],
  },
};
```

## 3. The codemod

A jscodeshift transform, runnable with no added dependency (`npx jscodeshift -t <file> <path> --parser=tsx`), like the Material UI codemod package. Two disciplines make it safe:

- **Alias-aware scoping.** Resolve the local name(s) the target is imported as from the matching import (`@heyhi/components` or a local `./Button`). Rewrite only elements with that name, so a same-named symbol from elsewhere is left alone. When no matching import is found, fall back to the literal name (a human should confirm any file that was changed on the name alone).
- **Idempotence and precision.** If an element already carries the new prop, drop the redundant old one rather than duplicate it. Return `null` (no write) for files with no change, so a repo-wide run touches only the files that use the deprecated prop.

**Worked example** (`codemods/button-fullWidth-to-block.cjs`, abridged; full file on the proof branch):

```js
module.exports = function transform(file, api) {
  const j = api.jscodeshift;
  const root = j(file.source);
  const isNamedAttr = (name) => (a) =>
    a.type === 'JSXAttribute' && a.name?.type === 'JSXIdentifier' && a.name.name === name;

  // resolve the local name(s) Button is imported as (alias-aware)
  const names = new Set();
  root.find(j.ImportDeclaration)
    .filter((p) => {
      const s = p.node.source && p.node.source.value;
      return typeof s === 'string' && (s === '@heyhi/components' || /(^|\/)Button$/.test(s));
    })
    .forEach((p) => (p.node.specifiers || []).forEach((sp) => {
      if (sp.type === 'ImportSpecifier' && sp.imported?.name === 'Button')
        names.add(sp.local ? sp.local.name : 'Button');
    }));
  if (names.size === 0) names.add('Button'); // fallback: match by name

  let changed = 0;
  root.find(j.JSXOpeningElement)
    .filter((p) => p.node.name.type === 'JSXIdentifier' && names.has(p.node.name.name))
    .forEach((p) => {
      const attrs = p.node.attributes || [];
      const hasBlock = attrs.some(isNamedAttr('block'));
      p.node.attributes = attrs.filter((a) => {
        if (isNamedAttr('fullWidth')(a)) {
          if (hasBlock) { changed++; return false; }   // drop redundant
          a.name.name = 'block'; changed++;             // rename
        }
        return true;
      });
    });
  return changed ? root.toSource() : null;
};
```

### The fixture and the run

`codemods/__testfixtures__/button-fullWidth.input.tsx` has three Button call sites (shorthand, `={true}`, expression) and one decoy `<Hero fullWidth>` that is not a package Button. Running the transform produces `.output.tsx`. Actual run:

```
$ npx jscodeshift -t codemods/button-fullWidth-to-block.cjs \
    codemods/__testfixtures__/button-fullWidth.output.tsx --extensions=tsx --parser=tsx
Results: 0 errors, 0 unmodified, 0 skipped, 1 ok

$ diff button-fullWidth.input.tsx button-fullWidth.output.tsx
15c15
<       <Button variant="primary" fullWidth>
---
>       <Button variant="primary" block>
19c19
<       <Button variant="secondary" fullWidth={true}>
---
>       <Button variant="secondary" block={true}>
23c23
<       <Button variant="ghost" fullWidth={wide}>
---
>       <Button variant="ghost" block={wide}>
```

All three call sites rewritten across all three forms; the `<Hero fullWidth>` decoy (line 27) untouched. None missed, none over-reached.

## 4. The migration note

`MIGRATIONS/2026-09-07-button-fullWidth-to-block.md` on the proof branch. It states the change, the human's reason, the backward-compatibility behavior, the deprecation window (accepted through the current major, removed in the next: the owner's call), the `npx jscodeshift` command, and that there is no runtime or visual change. Written for the consumer, it names the exact command and the exact removal version.

## 5. The changeset

`.changeset/button-fullwidth-to-block.md`, bumping the **major**:

```md
---
"@heyhi/components": major
---

Button: rename the `fullWidth` prop to `block`.

`fullWidth` is still accepted and maps to `block` with a development-only
deprecation warning; it will be removed in the next major version. Migrate with
the codemod: `npx jscodeshift -t ...codemods/button-fullWidth-to-block.cjs <path>`.
```

The changeset frontmatter is parsed as package-to-bump by Changesets, so no `classification:` key is added there; the classification mark rides in a trailing HTML comment that does not render in the generated changelog. In a repo whose Changesets config is at the monorepo root, this file belongs at the root `.changeset/`; it sits under the package in the worked example to keep the proof inside its own write tree.

## 6. typecheck

`npm run typecheck` on the changed files is clean. The changed files (`Button.tsx`, `src/internal/warnDeprecation.ts`) introduce **zero** type errors, verified with a scoped `tsc --noEmit -p` over just those files (exit 0). The package's full typecheck reports ten **pre-existing** errors (eight in `Card.tsx`, one each in `Input.tsx` and `Table.tsx`), which are byte-identical to `origin/main` and untouched by this change; they are flagged out of scope in the proof and the handoff, not fixed here (a Button prop rename should not touch three unrelated components). The rule the skill enforces: **the changed files introduce no new type error**, proven by a scoped typecheck, not by fixing pre-existing package debt.

---

*HeyHi Confidential. Reference for `ds-component-change` (Sheerline area 7). React code leg; load on demand.*
