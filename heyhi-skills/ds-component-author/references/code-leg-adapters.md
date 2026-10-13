# ds-component-author: the code-leg adapters (Lit and Angular)

*Named stubs, not built. Decision D5 (plan § 5): React only for this arc; Lit and Angular are deferred until an engagement pulls them. This file is the contract each stub will implement, so the next author has a mapping and not a blank page. The through-line table in the SKILL.md is framework-neutral; only the emitter differs.*

*classification: HeyHi Confidential*

---

## Status

- **React**: built and proved (`references/code-leg-react.md`, proof PR #822).
- **Lit (web components)**: STUB. Contract below. Not emitted by v1.
- **Angular**: STUB. Contract below. Not emitted by v1.

A request for Lit or Angular today stops at the stub and reports; the skill does not half-emit an untested framework.

## Lit (web components): the mapping this stub will implement

The same axes drive the emitter; the idioms change.

| Spec axis | Lit |
|---|---|
| VARIANT | a reflected attribute (`@property({ reflect: true }) tone = 'default'`), styled by `:host([tone="success"])` |
| TEXT | a `@property()` string, rendered in the template |
| BOOLEAN | a boolean attribute (`@property({ type: Boolean, reflect: true }) removable = false`) |
| INSTANCE_SWAP | a named `<slot name="leading-icon">` (web components have no node prop) |
| SLOT | the default `<slot>` |
| states | `:host(:focus-visible)`, `:host([disabled])`, and a nested `<button>` for the remove control |

Tokens bind the same way: the component's CSS (in the shadow root or a shared sheet) references `var(--token)`. Notes the stub must resolve: shadow-DOM token inheritance (CSS custom properties pierce the shadow boundary, so the served tokens reach the component), and the reflected-attribute naming (kebab attributes vs the camel spec axis names).

## Angular: the mapping this stub will implement

| Spec axis | Angular |
|---|---|
| VARIANT | an `@Input()` with a union type; a host binding (`[class.heyhi-chip--success]="tone === 'success'"`) or `[ngClass]` |
| TEXT | an `@Input()` string |
| BOOLEAN | an `@Input()` boolean |
| INSTANCE_SWAP | content projection: `<ng-content select="[leadingIcon]">` |
| SLOT | `<ng-content>` |
| states | `:host(:focus-visible)`, `[disabled]`, an `@Output() remove` for the remove control |

Notes the stub must resolve: `ChangeDetectionStrategy.OnPush` for a presentational component, and whether the union `@Input()` types live in a shared types file mirroring `types/tokens.ts`.

## What is shared across all three

- One spec, one property model (the through-line table). A change to the model changes every emitter's input, not just React's.
- CSS binds to the same served tokens via `var(--token)`; no framework mints its own tokens.
- The Code Connect template maps the Figma component to whichever code component is the client's target; the `component=` and `source=` lines and the `imports` change per framework, the property mapping does not.
- Every framework leg honors the same states and the same accessibility contract (SKILL.md Accessibility section).

---

*HeyHi Confidential. Adapter stubs for `ds-component-author`. Build order fixed by D5. React leg: `references/code-leg-react.md`.*
