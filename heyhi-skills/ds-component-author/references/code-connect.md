# ds-component-author: the Code Connect leg

*Loaded before the template write (Step 5). The parserless Code Connect template joins the Figma component to the code component. It is always emitted; it is published only on an Organization or Enterprise plan. Follow Figma's own `figma-code-connect` served skill for the API; this file is the component-author overlay.*

*classification: HeyHi Confidential*

---

## The one hard rule

Write a **`Component.figma.ts`** file whose default export is a parserless template using a `` figma.code`...` `` tagged template. Never a `.figma.tsx` file, and never the parser-based connect form (the `.figma.tsx` / connect-function style is a different artifact, published a different way, and is rejected here). If a capable model reaches for the more familiar `.figma.tsx` pattern from memory, that is the wrong output; the correct output is always `.figma.ts` plus `figma.code`.

## Template shape

```ts
// url=https://www.figma.com/design/<FILE_KEY_REDACTED>/<name>?node-id=<NODE_ID_REDACTED>
// source=<path to the code component>
// component=<code component name>
import figma from 'figma';
const instance = figma.selectedInstance;

// one extraction per property, per the through-line table:
const label = instance.getString('Label');
const tone = instance.getEnum('Tone', { default: 'default', success: 'success', warning: 'warning', error: 'error', info: 'info' });
const size = instance.getEnum('Size', { md: 'md', sm: 'sm' });
const removable = instance.getBoolean('Removable');
const showIcon = instance.getBoolean('Show Icon');
const leadingIcon = showIcon ? instance.getInstanceSwap('Leading Icon') : null;
let iconCode;
if (leadingIcon && leadingIcon.type === 'INSTANCE') {
  iconCode = leadingIcon.executeTemplate().example;
}

export default {
  example: figma.code`
    <Chip
      tone="${tone}"
      size="${size}"
      label="${label}"
      ${removable ? 'removable' : ''}
      ${iconCode ? figma.code`leadingIcon={${iconCode}}` : ''}
    />
  `,
  imports: ['import { Chip } from "@heyhi/components"'],
  id: 'chip',
  metadata: { nestable: true },
};
```

## The mapping rules (per Figma property type)

| Figma property | Method | Rule |
|---|---|---|
| VARIANT | `instance.getEnum('Name', { figmaVal: 'codeVal', ... })` | **Exhaustive**: map every value the property returns. An unmapped value renders `undefined`. |
| TEXT | `instance.getString('Name')` | Interpolate in quotes: `label="${label}"`. |
| BOOLEAN | `instance.getBoolean('Name')` | Interpolate as a conditional bare prop: `${removable ? 'removable' : ''}`. |
| INSTANCE_SWAP | `instance.getInstanceSwap('Name')` | Resolve dynamically: check `type === 'INSTANCE'`, then `executeTemplate().example`; interpolate in braces. Never hardcode the swapped child. |
| SLOT | `instance.getSlot('Name')` | Interpolate the returned sections directly inside the tagged template. Only for a property whose Figma type is `SLOT`. |

Emit only props that exist on the code component's interface; where a Figma property has no code prop, omit it rather than invent one. Interpolation: strings in quotes, instance/slot sections in braces or inline, booleans as conditionals.

## The publish gate (plan-gated, recorded)

- **Emit always.** The `.figma.ts` file is written to the repo regardless of the plan; the spec's `code_connect.emit` defaults true.
- **Publish only on Organization or Enterprise.** Call `add_code_connect_map` only when `whoami` shows an Organization or Enterprise plan AND the spec's `code_connect.publish` is true. Code Connect is not available on Free or Professional plans. **Record the `whoami` result** in the proof.
- **On the proof run**, `whoami` showed Pro (no Organization or Enterprise), so `add_code_connect_map` was NOT called; the template was emitted only. Publishing later also needs the `@figma/code-connect` package, a `figma.config.json`, and `@figma/code-connect/figma-types` in the tsconfig `types` for the `.figma.ts` to type-check.

## Where the file goes, and the hermetic seal

- Place the template alongside the component's Code Connect files, outside the package's typecheck `include` (e.g. a `code-connect/` directory), so the special `figma` import does not break the library `tsc --noEmit`.
- **Redact the Figma file key and node id** in the tracked template (`<FILE_KEY_REDACTED>` / `<NODE_ID_REDACTED>`); a template is a reusable artifact, so the redaction costs nothing. The real url lives in the gitignored proof record; fill it before publishing.

## Verify

Read the file back: it is `.figma.ts` (not `.figma.tsx`); the default export is a `figma.code` template; every Figma property is accounted for; every VARIANT mapping is exhaustive; no child is hardcoded. A grep of the skill folder for the parser-based connect form returns nothing.

---

*HeyHi Confidential. The Code Connect leg of `ds-component-author`. API: Figma's `figma-code-connect` served skill. Worked example: `code-connect/Chip.figma.ts` on proof PR #822 (redacted url) + the real url in the gitignored proof record.*
