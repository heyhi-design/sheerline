# Figma MCP Integration Reference

**`ui-studio/references` · Load when Figma output is requested · March 2026 · Capability notes updated July 2026 (post-Config)**

*Figma MCP calls, frame tagging by mode, multi-library extraction routing, and token-to-variable mapping.*

---

## When to Use This Reference

Load this file when:
- The user requests Figma output alongside the prototype
- You're extracting design tokens from a Figma file during a build session
- You need to tag or document frames in a Figma file
- You're cross-referencing component variables to a token library

---

## Figma MCP Tools Available

The following tools are accessible via the Figma MCP connection (tool names prefixed `mcp__cc3b9073-81e0-44b0-90d3-a098646cb9e6__`):

| Tool | Purpose |
|---|---|
| `whoami` | Verify account access before any extraction |
| `get_metadata` | Get file metadata: name, last modified, file key |
| `search_design_system` | Search for components, styles, and variables by keyword |
| `get_design_context` | Extract design decisions, properties, and layout from specific frames |
| `get_variable_defs` | Get all variable definitions from a file (token library extraction) |
| `get_screenshot` | Capture a screenshot of a specific frame |
| `get_figjam` | Access FigJam file content |
| `generate_diagram` | Generate a diagram from structured data |
| `create_new_file` | Create a new Figma file |
| `create_design_system_rules` | Generate design system rule content (supplementary context only — not the .mdc generator) |
| `get_code_connect_map` | Get Code Connect mappings |
| `get_code_connect_suggestions` | Get Code Connect mapping suggestions |
| `add_code_connect_map` | Add Code Connect mappings |
| `send_code_connect_mappings` | Send Code Connect mappings to Figma |
| `use_figma` | General Figma operation |

**Config 2026 update (June 2026; noted July 2026).** The tool surface above remains available. Additions from Config 2026 that touch this reference, each with its availability tier:

- `use_figma` is moving toward Plugin-API parity, starting with image support and custom fonts (open beta, free during the beta; all MCP clients including Claude Code).
- **Figma Motion** makes animated components a published, versioned design-system primitive, and the exact motion spec (keyframes, easing, timing) is readable over MCP via Dev Mode's Motion tab — relevant when extracting `tokens.motion.*`. Open beta since June 2026; core motion tools on all plans; publishing animated components, agent-generated motion, and hi-res export require a Full seat on a paid plan.
- **Shader fills/effects** are convertible to code and exportable over MCP (open beta; paid plans, Full seats; excluded from Starter/Education/Government plans).
- **Figma agent Skills** (markdown, slash-command instructions for Figma's in-canvas agent, with a live Community registry) are open beta on paid plans with Full seats. They shape in-canvas agent behavior; this reference governs code-side extraction and delivery, and is unchanged by them.

---

## Access Verification

Run before any extraction:

```
whoami() → confirms the connected Figma account
search_design_system(query="test") → confirms library access
```

If access fails: **Stop.** Say: *"Account [email] cannot access this file. Share the file with that account before continuing."*

---

## Multi-Library Extraction Routing

Most design systems have separate files for tokens and components. Extract from the right file for each data type.

### Library Classification

When `search_design_system` returns multiple connected libraries, classify each:

| Library type | Extraction method |
|---|---|
| `token_foundation` | `get_variable_defs(file_key=TOKEN_FILE_KEY)` |
| `atomic` | `search_design_system` + `get_design_context` on component frames |
| `molecular` | `search_design_system` + `get_design_context` on complex component frames |
| `layout_template` | `search_design_system` + `get_design_context` on layout frames |
| `icon` | `search_design_system` for icon set inventory |
| `documentation` | `get_design_context` on documentation frames (text extraction) |

**Critical rule:** Call `get_variable_defs` against the **token library file_key**, not the component library file_key. Calling it against the wrong library returns an empty or incomplete variable set. Always confirm which file is the token foundation before extracting.

### Confirming the Right File

Ask: "Which file is the primary design system file — the component library master or the token foundation?" If unclear, call `get_metadata` on both candidates and check which was last modified and which has variable collections.

---

## Token Extraction: `get_variable_defs`

```
get_variable_defs(file_key="[TOKEN_LIBRARY_FILE_KEY]")
```

Returns all variable collections with their modes and values. Map to `active-brand.json` structure:

| Figma variable collection | active-brand.json target |
|---|---|
| Colors → Primitives, Semantic | `tokens.color.*` |
| Typography → Font families, sizes, weights | `tokens.typography.*` |
| Spacing → Base, tiers | `tokens.spacing.*` |
| Motion → Easing, durations | `tokens.motion.*` |
| Radius | `tokens.radius.*` |
| Elevation / Shadow | `tokens.elevation.*` |

**Variable collection names to record:** Store in `repository.figma.token_library.variable_collection_names` for future refresh operations.

**Unresolved references:** If a component's variable references a token not found in the token library file, add to `meta.provisional_fields` with reason `unresolved_variable_reference`. Do not null out the component — mark it provisional with the unresolved path.

---

## Frame Tagging by Mode

When delivering Figma frames alongside a build, tag frames consistently:

| Mode | Tag format | Figma page |
|---|---|---|
| Mode A | `[production]` | Main/Production page |
| Mode B | `[exploratory]` | Explorations page |
| Mode C | `[speculative]` | Concept page |

**Frame naming convention:** `[client-name] · [page-name] · [mode-tag] · [date]`

Example: `Acme · Homepage · [production] · 2026-03-25`

To get a screenshot of a frame for documentation: `get_screenshot(frame_id="[FRAME_ID]")`

---

## Token-to-Variable Mapping

When generating CSS custom properties from a config, document the Figma variable → CSS property mapping for the developer handoff:

```
Figma variable: Colors/Background/Page → CSS: --color-bg-page
Figma variable: Typography/Scale/H1 → CSS: --type-h1
Figma variable: Spacing/Base → CSS: --spacing-base
```

This mapping lets engineers use the Figma variable names and the CSS custom property names as interchangeable references during implementation.

**For dark-native configs (meta.default_scheme = 'dark'):** The variable collection will have modes (Dark, Light). Map each mode's values to the corresponding `tokens.color.schemes.dark.*` and `tokens.color.schemes.light.*` paths in active-brand.json.

---

## Storybook Integration

When a Storybook URL is available (`repository.storybook.url`), fetch the component inventory:

```
GET {storybook_url}/stories.json
```

This provides a Level 1 component inventory (names, story types, category groupings) without requiring git access. Parse the response to populate `components.inventory` with component names and categories. Props and variants require Level 2 analysis (source code access).

---

## Code Connect

If the design system uses Figma Code Connect, retrieve mappings after component extraction:

```
get_code_connect_map(file_key="[COMPONENT_LIBRARY_FILE_KEY]")
```

Store the mappings for reference during the build. When generating implementation code, prefer Code Connect component names over generic HTML when the framework matches.

---

*HeyHi Internal Use Only. Created March 25, 2026.*
