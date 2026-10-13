# ds-component-author: the code leg (React)

*Loaded before the code write (Step 4). The React emitter: how the same spec that built the Figma component becomes a typed React component whose CSS binds to the served tokens. Includes the worked example's actual typecheck output.*

*classification: HeyHi Confidential*

---

## The emitter, axis by axis

Read one existing component in the target package first and match its idioms. In `@heyhi/components` the idioms are: `React.forwardRef`, a `displayName`, the `heyhi-<name> heyhi-<name>--<variant>` class pattern, prop/variant types centralized in `src/types/tokens.ts`, a per-component `index.ts` barrel, and a `src/index.ts` export block. Derive the props from the axes per the SKILL.md through-line table:

- **VARIANT** to a string-union type in `types/tokens.ts` (`export type ChipTone = 'default' | 'success' | ...`), and one CSS modifier class per value.
- **TEXT** to a `string` prop, rendered as the label text.
- **BOOLEAN** to a `boolean` prop, toggling a region or a class; give it a sensible default.
- **INSTANCE_SWAP** to a `ReactNode` prop (the slotted element).
- **SLOT** to the `children` prop.
- **States** add the interaction affordances: a removable control is a real `<button>` with `onRemove` and an `aria-label`; a disabled state sets the real `disabled` / `aria-disabled`.

## The component template (shape)

```tsx
import React, { ReactNode } from 'react';
import { <Name>Tone, <Name>Size } from '../../types/tokens';
import './<Name>.css';

// Extend the plain HTMLAttributes; do not Omit onClick. The served DS routes an
// interactive label to a Chip WITH onClick, so removing it contradicts the contract.
export interface <Name>Props extends React.HTMLAttributes<HTMLSpanElement> {
  tone?: <Name>Tone;      // VARIANT axis -> union
  size?: <Name>Size;      // VARIANT axis -> union
  label: string;          // TEXT axis
  leadingIcon?: ReactNode; // INSTANCE_SWAP axis
  removable?: boolean;    // BOOLEAN axis
  onRemove?: () => void;  // state affordance (its handler stopPropagation()s so a nested control does not fire a container onClick)
  disabled?: boolean;     // state
  className?: string;
}

export const <Name> = React.forwardRef<HTMLSpanElement, <Name>Props>(
  ({ tone = 'default', size = 'md', label, /* ... */ className = '', ...rest }, ref) => (
    <span ref={ref} className={`heyhi-<name> heyhi-<name>--${tone} heyhi-<name>--${size}${className ? ` ${className}` : ''}`} {...rest}>
      {/* anatomy regions, states as CSS */}
    </span>
  )
);
<Name>.displayName = '<Name>';
```

## The CSS rule (bind every value to a served token)

- Every colour, radius, spacing, and duration is `var(--token)`; **no literals.** One modifier class per VARIANT value.
- Interaction states are real CSS from the spec's `states[]`: `:hover`, `:focus-visible` for the ring (never `:focus`), `:active`, `:disabled`. The focus ring lives in the CSS, bound to the served focus token (`outline: 2px solid var(--accent-primary)`).
- Run `validate_output` (artifact_type `rendered_css`) and act on the findings. A literal where a token exists is a true bypass, fixed by binding the real served var. A finding that names a token the served CSS does not actually emit is a served-surface conflict, surfaced to the human gate, not renamed to a var that breaks the render.

## One story per variant (Storybook not installed)

Emit one CSF3 story file (`<Name>.stories.tsx`) with one story per variant and per interaction state. If the package has no Storybook, use local `Meta`/`StoryObj` type shims so the story still typechecks against the real props, and note that it becomes a live Storybook story by swapping the shims for `@storybook/react` imports. Do not install Storybook.

## Worked example: Chip added to @heyhi/components (proof branch, PR #822)

Files added on `heyhi-design-intelligence-tests/packages/components/` (proof branch, propose-first, not merged):
`src/components/Chip/{Chip.tsx,Chip.css,index.ts,Chip.stories.tsx}`, `src/types/tokens.ts` (`ChipTone`/`ChipSize`), `src/index.ts` (barrel), `code-connect/Chip.figma.ts`.

Chip is the interactive, removable sibling of `Badge` (the served DS routes interactive labels to Chip; the package had only Badge). Its CSS binds every value to a served token, including the two `validate_output` surfaced: `line-height` to `var(--font-line-height-none)` and the transition to `var(--motion-duration-150)`.

### Typecheck output (smoke test 4)

The worked-example component type-checks. The package's own `tsc --noEmit` also surfaces pre-existing errors in files this branch does not touch (Card, Input, Table, present on `origin/main`), so both results are reported honestly.

**Isolated typecheck of the Chip closure** (`src/components/Chip/** + src/types/tokens.ts`, via a temp tsconfig removed after):

```
$ npx tsc --noEmit -p tsconfig.chip-check.json
ISOLATED TYPECHECK EXIT: 0   (the worked-example component is type-clean)
```

**Full-package typecheck** (`npm run typecheck` = `tsc --noEmit`): exit 2, and every error is in a pre-existing file this branch does not modify:

```
src/components/Card/Card.tsx(19,21): error TS2352: Conversion of type 'ForwardRefExoticComponent<...>' to type 'CardComponent' may be a mistake ...
src/components/Card/Card.tsx(22-27): error TS2339: Property 'variant'|'padding'|'as'|'className'|'children'|'onClick' does not exist ...
src/components/Card/Card.tsx(47,6): error TS2339: Property 'displayName' does not exist on type 'CardComponent'.
src/components/Input/Input.tsx(5,18): error TS2430: Interface 'InputProps' incorrectly extends 'InputHTMLAttributes<HTMLInputElement>' (prefix: ReactNode vs string).
src/components/Table/Table.tsx(45,27): error TS2345: Argument of type 'Set<unknown>' is not assignable to 'Set<number>'.
```

`git diff --name-only origin/main` on the proof branch lists only `Chip/`, `code-connect/`, `types/tokens.ts`, and `index.ts`. Card/Input/Table are untouched (Input last changed in the initial commit), so their errors pre-exist and are out of Lane G scope. The skill's rule (SKILL.md Step 4.6): typecheck the new component's closure in isolation and report both results; never claim the whole package is clean when it is not.

---

*HeyHi Confidential. The React code leg of `ds-component-author`. Worked example: the proof record in the instance's engagement folder (gitignored) and proof PR #822. Adapters (Lit, Angular): `references/code-leg-adapters.md`.*
