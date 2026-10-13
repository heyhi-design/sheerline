// figma-library-census · step 1 · page discovery (READ-ONLY)
// Verified by probe P-03 (references/probes.md), observed on the worked-example
// scratch library, Figma plan tier Pro, 2026-09-07:
// returned 7 pages (Cover, Getting Started, Foundations, ---, Button, ---, Utilities).
//
// Step 1 has two halves. The library-availability half is the get_libraries MCP tool
// (not use_figma): get_libraries({ fileKey }), paginating libraries_available_to_add
// via libraries_available_to_add_next_offset, recording added vs available. This file
// is the other half: the cheap page list that precedes the per-page component fan-out
// in step 3. Run this ALONE first, then emit one step-3 call per content page.
//
// READ-ONLY: this snippet reads the page list only. It adds, mutates, and deletes nothing.
// Only id and name are read (the step-3 fan-out consumes only those). Do NOT read
// p.children here: a non-loaded page's children can throw on a dynamic-page client file,
// and a child count is not needed to fan out.

const pages = figma.root.children.map((p, i) => ({
  index: i,
  id: p.id,
  name: p.name
}));
return { pages };

// HeyHi Confidential
