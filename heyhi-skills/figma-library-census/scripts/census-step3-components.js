// figma-library-census · step 3 · component census, one page (READ-ONLY)
// Verified by probe P-02 (Button page) and P-03 (remaining pages via loadAsync),
// observed on the worked-example scratch library, Figma plan tier Pro,
// 2026-09-07:
// Button page -> COMPONENT_SET "Button" (27 variants; default "Style=primary, Size=sm,
// State=default"; props Label TEXT / Show Icon BOOLEAN / Icon INSTANCE_SWAP /
// Style,Size,State VARIANT). Utilities page -> COMPONENT "Icon/ChevronRight" (no props).
//
// ONE PAGE PER CALL, via page.loadAsync() (NOT setCurrentPageAsync). loadAsync loads a
// page's subtree without switching the editor's current page, so the census stays
// read-only (no view-state change) and N per-page calls run in parallel safely (a single
// message with N tool-use blocks); parallel setCurrentPageAsync calls would race on the
// one global current page. Run step 1 first to get page IDs, then emit one call per page.
//
// OWNER NARROWING: componentPropertyDefinitions throws when read from a variant COMPONENT.
// isRow keeps only COMPONENT_SETs and standalone COMPONENTs (parent not a set), so the
// row node always owns its own definitions; variant children are not rows.
//
// READ-ONLY: reads component metadata only. Adds, mutates, and deletes nothing.

const PAGE_ID = "REPLACE_WITH_PAGE_ID";   // one page id from step 1

const page = await figma.getNodeByIdAsync(PAGE_ID);
await page.loadAsync();   // load this page's subtree; does NOT switch the current page

const all = page.findAllWithCriteria({ types: ["COMPONENT_SET", "COMPONENT"] });
const isRow = n =>
  n.type === "COMPONENT_SET" ||
  (n.type === "COMPONENT" && (!n.parent || n.parent.type !== "COMPONENT_SET"));

const read_errors = [];
const components = all.filter(isRow).map(n => {
  const owner = n;   // a set or a standalone component owns its own definitions
  let properties = [], default_variant = null;
  try {
    const defs = owner.componentPropertyDefinitions;
    properties = Object.entries(defs).map(([k, d]) => ({
      name: k.replace(/#[^#]+$/, ""),
      type: d.type,
      values: d.type === "VARIANT"
        ? (d.variantOptions || [])
        : (d.type === "BOOLEAN" ? ["true", "false"] : [])
    }));
  } catch (e) {
    // Fail loud, but never emit a schema-invalid property row: record the failure
    // out of band so step 4 surfaces it and the emitted map stays valid.
    read_errors.push({ component: n.name, id: n.id, error: String(e) });
  }
  if (n.type === "COMPONENT_SET") {
    try { default_variant = n.defaultVariant ? n.defaultVariant.name : null; } catch (e) { default_variant = null; }
  }
  return {
    name: n.name,
    key: n.key,
    library_key: null,
    type: n.type,
    properties,
    default_variant
  };
});

return { page: page.name, components, read_errors };

// HeyHi Confidential
