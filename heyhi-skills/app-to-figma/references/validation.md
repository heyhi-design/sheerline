# app-to-figma: validation

*The structural checks and the render-and-look. Loaded on demand. A build is not done until every check here passes on evidence, not assertion. The load-bearing lesson from the 2026-09-04 live proof: a per-node binding audit can report clean while the render is wrong, so the screenshot is not optional.*

*classification: HeyHi Confidential*

---

## 1. The four structural checks (read-only `use_figma`)

Run each against the built wrapper for a surface. Each returns a list of violations; an empty list is a pass. Paste the script and its output into the proof record.

### 1a. Every instance resolves to a library key

Every instance on the surface must trace to a `mainComponent.key` that is present in `figma-library-map.json`. An instance whose key is absent from the map is either an unresolved element that slipped past the gate or a local build that should have been a library instance.

```js
const wrapper = await figma.getNodeByIdAsync("WRAPPER_ID");
const mapKeys = new Set(LIBRARY_MAP_COMPONENT_KEYS); // passed in from figma-library-map.json
const offenders = [];
for (const inst of wrapper.findAllWithCriteria({ types: ["INSTANCE"] })) {
  const mc = inst.mainComponent;
  const cs = mc && mc.parent && mc.parent.type === "COMPONENT_SET" ? mc.parent : mc;
  const key = cs && cs.key;
  if (!key || !mapKeys.has(key)) offenders.push({ id: inst.id, name: inst.name, key: key || null });
}
return { instances: wrapper.findAllWithCriteria({ types: ["INSTANCE"] }).length, offenders };
```

### 1b. Every bound variable is remote (from the library)

Every variable bound to a fill, stroke, spacing, or radius on the surface must be `remote: true`. A `remote: false` binding is a locally-created variable, which the anti-minting invariant forbids.

```js
const wrapper = await figma.getNodeByIdAsync("WRAPPER_ID");
const ids = new Set();
for (const n of wrapper.findAll(() => true)) {
  const bv = n.boundVariables || {};
  for (const b of Object.values(bv)) (Array.isArray(b) ? b : [b]).forEach(x => x && x.id && ids.add(x.id));
}
const vars = await Promise.all([...ids].map(id => figma.variables.getVariableByIdAsync(id)));
const local = vars.filter(v => v && v.remote === false).map(v => ({ name: v.name, id: v.id }));
return { boundVariables: ids.size, localOffenders: local };
```

### 1c. Every text node carries a library text style

Every text node on the surface should carry a `textStyleId` that resolves to a remote (library) style. A bare text node with no style, or a local style, is a miss.

```js
const wrapper = await figma.getNodeByIdAsync("WRAPPER_ID");
const offenders = [];
for (const t of wrapper.findAllWithCriteria({ types: ["TEXT"] })) {
  const sid = t.textStyleId;
  if (!sid) { offenders.push({ id: t.id, reason: "no text style" }); continue; }
  const s = await figma.getStyleByIdAsync(sid);
  if (!s || s.remote === false) offenders.push({ id: t.id, reason: s ? "local style" : "unresolved style" });
}
return { textNodes: wrapper.findAllWithCriteria({ types: ["TEXT"] }).length, offenders };
```

### 1d. Zero local variables and zero local styles were created

The whole-file check. The build must create no local variables and no local styles; every value is imported.

```js
const localVars = await figma.variables.getLocalVariablesAsync();
const localStyles = [
  ...await figma.getLocalPaintStylesAsync(),
  ...await figma.getLocalTextStylesAsync(),
  ...await figma.getLocalEffectStylesAsync(),
];
return { localVariablesCreated: localVars.length, localStylesCreated: localStyles.length };
```

Both counts must be `0`. (A pre-existing local variable that the file already carried is a separate matter recorded at the gate; the invariant is that the build adds none.)

---

## 2. Render-and-look (V9, `sheerline/os/session-rules.md`)

A structural pass is necessary, not sufficient. The 2026-09-04 proof caught two defects that every structural audit passed: a rebound clone that rendered black, and a frame that rendered 1px tall. Both were visible only in the screenshot.

For every built section:

1. `get_screenshot` the section by node ID (not just the full wrapper; a reduced-resolution full shot hides clipped text and placeholder strings).
2. Compare against the source surface (the running dev server, the live site, or the design). Assert, in one line per section:
   - the **font family** matches the product's typefaces (a loaded font is not proof of the correct font);
   - **no clipped text** (line heights or frame sizing cutting off descenders or lines);
   - **no placeholder text** ("Title", "Button", "Heading" left unoverridden);
   - the **theme mode** is the surface's mode.
3. A mismatch is a failed validation; fix it with a targeted `use_figma` call, do not rebuild the section.

---

## 3. The acceptance table (for the proof record)

The proof record carries a table the smoke tests read:

| Row | Target |
|---|---|
| instances resolved to library keys | N of N |
| variables bound remote | N of N |
| local variables created | 0 |
| local styles created | 0 |
| text nodes on a library style | N of N |
| sections screenshotted | N of N |
| deviations ruled by the human | listed |

`grep -c "local variables created: 0"` and `grep -c "local styles created: 0"` over the proof record must each be 1.

---

## 4. The false-clean warning

- A **per-node binding audit** reports a fill as bound when the binding is present in the node's data, even when it renders the base color (the black-rebind trap). Only the screenshot catches it.
- A **`strokeWeight`** binding reads back as `strokeTopWeight` / `strokeBottomWeight` / `strokeLeftWeight` / `strokeRightWeight`; an audit that checks the `strokeWeight` key alone reports a false unbound.
- A **structural pass with zero offenders** is a real pass only when the render-and-look also passes. Report both; a green structural check with no screenshot is an incomplete validation.

---

*HeyHi Confidential. Reference for `app-to-figma` (Sheerline area 5). Live-write lessons: the 2026-09-04 generator proof and `heyhi-skills/heyhi-design-bridge/`. Spec source: `plans/plan-sheerline-fdde-loop-2026-09-07.md` (DISPATCH-02, Lane B).*
