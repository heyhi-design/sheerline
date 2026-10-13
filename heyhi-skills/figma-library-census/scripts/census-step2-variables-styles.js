// figma-library-census · step 2 · variable + style census (READ-ONLY)
// Verified by probe P-01 (references/probes.md), observed on the worked-example
// scratch library, Figma plan tier Pro, 2026-09-07:
// 4 local collections (Primitives 69 / Color 35 Light,Dark / Spacing 27 / Typography 26),
// 157 variables (every one remote:false, WEB code syntax set, scoped);
// 12 text + 6 effect + 0 paint styles;
// teamLibrary.getAvailableLibraryVariableCollectionsAsync() -> [] from the DEFINING file
// (its own collections are local, not remote), so getVariablesInLibraryCollectionAsync
// has no remote collection key here (confirmed count 0, no throw, against a local key).
//
// TWO PATHS. The variable census has a remote path and a local path:
//   Remote (run from a CONSUMING file that has the library added): teamLibrary returns
//     name/key/resolved_type only (NOT modes, NOT code syntax), see Ground-truth corrections.
//   Local  (run in the DEFINING file, identified by the library's file_key): getLocal*
//     fills modes (from the collection) and code_syntax (per variable).
// The map's modes[] and code_syntax{} always come from the defining-file (local) read.
//
// READ-ONLY: reads collections, variables, and styles. Adds, mutates, and deletes nothing.
// No page switch (variables and styles are document-level).

// --- Remote path (from a consuming file). On the defining file this returns []. ---
let remote_collections = [], remote_note = null;
try {
  const rc = await figma.teamLibrary.getAvailableLibraryVariableCollectionsAsync();
  remote_collections = rc.map(c => ({ name: c.name, key: c.key, libraryName: c.libraryName }));
  if (remote_collections.length === 0) {
    remote_note = "no remote library collections from this file (either the defining file, or no library added)";
  }
} catch (e) { remote_note = "teamLibrary unavailable: " + String(e); }
// For each remote collection, the variables (name/key/resolved_type only):
const remote_variables = {};
for (const rc of remote_collections) {
  const vars = await figma.teamLibrary.getVariablesInLibraryCollectionAsync(rc.key);
  remote_variables[rc.key] = vars.map(v => ({ name: v.name, key: v.key, resolved_type: v.resolvedType }));
}

// --- Local path (the defining file): modes + code syntax + resolved type + scopes. ---
const localCollections = await figma.variables.getLocalVariableCollectionsAsync();
const localVars = await figma.variables.getLocalVariablesAsync();
const varsByColl = {};
for (const v of localVars) (varsByColl[v.variableCollectionId] ||= []).push(v);
const collections = localCollections.map(c => ({
  key: c.key,
  name: c.name,
  library_key: null,
  modes: c.modes.map(m => m.name),
  variables: (varsByColl[c.id] || []).map(v => ({
    name: v.name,
    key: v.key,
    resolved_type: v.resolvedType,
    code_syntax: v.codeSyntax || {},
    remote: v.remote,
    scopes: v.scopes,
    dtcg_token: null   // candidate join filled in step 4 against the served token set
  }))
}));

// --- Styles (text + effect; paint out of scope for v1). ---
const [ts, es] = await Promise.all([
  figma.getLocalTextStylesAsync(),
  figma.getLocalEffectStylesAsync()
]);
const styles = [
  ...ts.map(s => ({ name: s.name, key: s.key, kind: "text" })),
  ...es.map(s => ({ name: s.name, key: s.key, kind: "effect" }))
];

return { remote_collections, remote_variables, remote_note, collections, styles };

// HeyHi Confidential
