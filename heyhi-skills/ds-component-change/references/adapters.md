# Framework adapters: Lit and Angular (stubs)

*Reference for `ds-component-change`. Named extension points for the non-React code legs. **Not built for this arc** (plan D5: React only; Lit and Angular are deferred until an engagement pulls them). This file names the shape each would take so the deferral is a known boundary, not a silence. A future lane builds these; do not treat the snippets as shipped code.*

The React leg (`shim-and-codemod-react.md`) is the built reference. The two disciplines carry across every framework: the old surface keeps working through a shim that maps to the new one and warns once in development, and a codemod rewrites downstream call sites. Only the language of the shim and the codemod parser change.

---

## Lit (web components)

**Shim.** A deprecated attribute is reflected and mapped in the property's setter (or in `willUpdate`), warning once via the same `warnDeprecation` pattern.

```ts
// STUB (not built for this arc).
@customElement('hh-button')
export class HhButton extends LitElement {
  @property({ type: Boolean }) block = false;

  /** @deprecated Use `block`. Mapped for now; removed next major. */
  @property({ type: Boolean, attribute: 'full-width' })
  set fullWidth(v: boolean) {
    warnDeprecation('<hh-button>: `full-width` is deprecated; use `block`.');
    this.block = v;
  }
  get fullWidth() { return this.block; }
}
```

**Codemod.** A template-aware transform. HTML template literals and `.html` files hold the attribute (`full-width`), so the parser is an HTML/lit-template AST, not jscodeshift over JSX. The attribute rename is `full-width` to `block`, kebab-cased.

**Migration note and changeset.** Identical shape to React. The changeset bumps the major of the web-component package.

---

## Angular

**Shim.** Angular aliases an input, so the old binding maps to the new field with an alias plus a setter that warns once.

```ts
// STUB (not built for this arc).
@Component({ selector: 'hh-button' })
export class HhButtonComponent {
  @Input() block = false;

  /** @deprecated Use `block`. */
  @Input('fullWidth')
  set fullWidth(v: boolean) {
    warnDeprecation('hh-button: `fullWidth` is deprecated; use `block`.');
    this.block = v;
  }
}
```

**Codemod.** A template transform over Angular HTML templates: the property binding `[fullWidth]` and the attribute `fullWidth` rename to `block` / `[block]`. The parser is the Angular template AST (for example via `@angular/compiler` or a schematic), not jscodeshift.

**Migration note and changeset.** Same shape. An Angular library would ship this as a migration schematic (`ng update`) in addition to, or instead of, a standalone codemod; the schematic is the Angular-idiomatic delivery of the same rewrite.

---

## Why stubs, not builds

Plan D5 (the instance owner, 2026-09-07): build the React leg only; Lit and Angular stay named stubs until an engagement pulls them. The extension points above are the contract a future lane fills. Building them now would be infrastructure ahead of need, which the arc rules forbid. When an engagement brings a Lit or Angular design system, this file is the starting point, and the codemod-parser difference (HTML/template AST rather than JSX) is the one real piece of new work.

---

*HeyHi Confidential. Reference for `ds-component-change` (Sheerline area 7). Adapter stubs; load on demand.*
