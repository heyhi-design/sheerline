# Component Analysis Reference

How to perform deep analysis of a client's component library. This reference guides the skill's full component analysis mode — scanning not just token variables but the actual component implementations to understand props, variants, composition patterns, and architectural decisions.

---

## When to Run Component Analysis

- **First-time brand onboarding:** Building the component inventory for the brand config
- **Before building a new component:** Checking if something similar already exists
- **Before extending a component:** Understanding the current implementation before modifying
- **During design system audits:** Evaluating library health, drift, and consistency

---

## Analysis Depth Levels

### Level 1: Inventory Scan

Quick pass to build the component list. Answers: "What exists?"

**Process:**
1. Scan the component repository for component directories/files
2. Extract component names from file names, exports, or directory structure
3. Build a flat inventory: `[{ name, path, type }]`

**File patterns to scan:**
```
src/components/**/*.{tsx,jsx,vue,svelte}
src/lib/**/*.{tsx,jsx,vue,svelte}
packages/*/src/**/*.{tsx,jsx,vue,svelte}
```

**What to capture:**
- Component name (from filename, export, or displayName)
- File path
- Component type (primitive, composite, layout, utility, page-level)
- Framework (React, Vue, Svelte, Web Components)

### Level 2: Props & Variants

Deeper pass to understand each component's API. Answers: "What can each component do?"

**Process:**
1. Read each component file
2. Extract prop/type definitions
3. Identify variant patterns (props that switch between predefined styles)
4. Note slot/children patterns (composition API)

**What to capture per component:**
```json
{
  "name": "Button",
  "path": "src/components/Button/Button.tsx",
  "props": [
    { "name": "variant", "type": "primary | secondary | ghost | danger", "default": "primary" },
    { "name": "size", "type": "sm | md | lg", "default": "md" },
    { "name": "disabled", "type": "boolean", "default": false },
    { "name": "loading", "type": "boolean", "default": false },
    { "name": "icon", "type": "ReactNode", "required": false },
    { "name": "children", "type": "ReactNode", "required": true }
  ],
  "variants": ["primary", "secondary", "ghost", "danger"],
  "sizes": ["sm", "md", "lg"],
  "composition": "Accepts children. Optional icon slot.",
  "token_usage": ["--color-primary", "--radius-md", "--spacing-2", "--font-body"]
}
```

**Framework-specific extraction:**

| Framework | Where to find props | Where to find types |
|-----------|-------------------|-------------------|
| React (TS) | Interface/type definition, often `ComponentProps` or `ComponentNameProps` | Same file or `.types.ts` |
| React (JS) | `propTypes` object, or destructured params | `.propTypes` definition |
| Vue | `defineProps()` or `props` option | Same, or `.d.ts` file |
| Svelte | `export let` declarations | `<script lang="ts">` section |
| Web Components | `static get observedAttributes` | Custom elements manifest |

### Level 3: Implementation Patterns

Deepest pass to understand how components are built. Answers: "What patterns and conventions does this library follow?"

**Process:**
1. Sample 5-10 representative components across different types
2. Analyze code structure, styling approach, state management patterns
3. Extract the implicit conventions

**What to capture:**

**Styling approach:**
- CSS Modules, styled-components, Tailwind, vanilla CSS, CSS-in-JS
- How tokens are consumed (CSS variables? Theme object? Utility classes?)
- How variants are implemented (className switching? style objects? data attributes?)

**State management:**
- How internal state is handled (useState, useReducer, stores)
- How external state is consumed (context, props, stores)
- Event handling patterns (callback props? custom events? event bus?)

**Composition patterns:**
- Compound components (e.g., `<Select><Select.Option>`)
- Render props or slot patterns
- Higher-order components or hooks
- Forward ref patterns

**Naming conventions:**
- File naming (PascalCase? kebab-case? index files?)
- Export patterns (default? named? barrel files?)
- CSS class naming (BEM? camelCase? utility-first?)
- Prop naming (boolean prefixes like `is`/`has`? callback prefixes like `on`?)

**Testing patterns:**
- Test file location (co-located? `__tests__` directory?)
- Testing library (Jest, Vitest, Testing Library, Cypress)
- Test structure (unit? integration? snapshot?)

---

## Component Relationship Mapping

Beyond individual components, understand how they compose:

### Dependency Graph

Which components use other components? Build a simple dependency map:

```
Page
  └── Layout
       ├── Header
       │    ├── Nav
       │    │    └── NavLink
       │    └── Logo
       ├── Main
       │    ├── Hero
       │    │    ├── Heading
       │    │    └── Button
       │    └── Section
       │         ├── Card
       │         └── Grid
       └── Footer
            ├── FooterNav
            └── SocialLinks
```

### Token Flow

How do design tokens flow through the component hierarchy?

- **Direct:** Component reads CSS variables from `:root`
- **Theme provider:** Component reads from a context/provider (e.g., ThemeProvider, CSS custom property scope)
- **Props:** Parent passes token values as props
- **Mixed:** Some values from tokens, some from props

Document the pattern so new components follow it.

---

## Drift Detection

When analyzing an existing library, check for drift — places where implementation has diverged from the design system's intent:

### Token Drift
- Components using raw values instead of tokens
- Components using the wrong semantic token (e.g., using `--color-primary` for text instead of `--color-text-primary`)
- Inconsistent token naming within the codebase

### Pattern Drift
- Components that implement the same pattern differently (e.g., two different loading state approaches)
- Variant naming inconsistencies (e.g., `size="small"` in one component, `size="sm"` in another)
- Composition pattern inconsistencies (some components use slots, others use render props for the same purpose)

### API Drift
- Prop naming inconsistencies across similar components
- Different approaches to the same concern (e.g., some components accept `className`, others don't)
- Inconsistent default values for common props

### Drift Remediation Procedure

Detecting drift is not the goal. The goal is deciding what to do about it during a build session. Use this procedure when drift is found:

**Step 1 — Classify the drift by severity:**

| Severity | Definition | Example |
|---|---|---|
| **Breaking** | Drift that produces incorrect output or accessibility failures | Component uses raw hex that fails WCAG contrast; two components use conflicting `--color-primary` token for different semantic roles |
| **Structural** | Drift that creates inconsistency visible to users or engineers | One component uses `size="small"`, another uses `size="sm"` for the same intent; slot patterns differ between equivalent components |
| **Cosmetic** | Drift that creates technical debt but doesn't affect visible output | Magic number padding value that matches the token value but doesn't use the variable; comment style inconsistency |

**Step 2 — Decide action based on severity and your current task:**

| Severity | In-scope (you're working on this component) | Out-of-scope (you noticed it while working on something else) |
|---|---|---|
| Breaking | Fix it now, before building on top of it | Flag in a `## Drift Findings` section of the session output. Do not fix out-of-scope breaking drift silently — it may have intentional reasons. |
| Structural | Fix it now if the fix is bounded (renaming a variant value, updating a prop name). Escalate if the fix touches other components. | Flag with component name, drift type, and recommended fix. |
| Cosmetic | Note it in the config's `drift.token_drift` or `drift.pattern_drift` array for future cleanup. Do not fix during a build session. | Same — add to the drift array, defer fixing. |

**Step 3 — Document the finding regardless of action:**

Add to the component entry in the `components.drift` object under the appropriate category (`token_drift`, `pattern_drift`, or `api_drift`):

```json
{
  "component": "Button",
  "type": "token_drift",
  "severity": "breaking",
  "description": "Uses hardcoded #0066CC instead of var(--color-accent-primary) for background",
  "found_during": "Level 1 scan / build session [date]",
  "action": "fixed in-session | flagged for repair | deferred cosmetic"
}
```

**Step 4 — If you fixed breaking or structural drift in-session:**

Note the fix in your build session output under `## Drift Resolved`. Include: component name, what was wrong, what you changed, and whether the fix requires a design system PR or is isolated to this prototype.

**The principle:** Drift found and undocumented is drift that will cause confusion in the next session. The bar for documenting is lower than the bar for fixing.

---

## Output Format

Component analysis results are stored in the brand config under `components`:

```json
{
  "components": {
    "source": "git@github.com:org/design-system.git",
    "framework": "React + TypeScript",
    "styling": "CSS Modules with CSS custom properties",
    "inventory": [
      {
        "name": "Button",
        "path": "src/components/Button/Button.tsx",
        "category": "primitive",
        "props": [...],
        "variants": [...],
        "tokens_used": [...],
        "dependencies": ["Icon"],
        "notes": ""
      }
    ],
    "conventions": {
      "naming": "PascalCase files, co-located CSS modules, barrel exports via index.ts",
      "props": "Boolean props use 'is' prefix. Callbacks use 'on' prefix. Size uses 'sm|md|lg'.",
      "variants": "String union types. Default variant is always first in union.",
      "composition": "Compound components for complex UI. forwardRef on all primitives.",
      "styling": "CSS Modules. Tokens consumed via CSS custom properties. Variants via data-attributes.",
      "testing": "Co-located .test.tsx files. React Testing Library. No snapshots."
    },
    "drift": {
      "token_drift": [],
      "pattern_drift": [],
      "api_drift": []
    }
  }
}
```

---

## Using Analysis Results During Builds

When the skill runs Step 5 (Build) and Step 6 (Component Library Check), it references this analysis:

1. **Search before building:** Query the inventory for components matching the current task
2. **Match props:** If using an existing component, verify prop usage matches the documented API
3. **Follow conventions:** New components adopt the naming, prop, and variant conventions captured in the analysis
4. **Respect styling patterns:** Use the same token consumption approach (CSS variables? Theme object?)
5. **Flag drift:** If building something that necessarily diverges from conventions, document why

---

## Supernova MCP Integration

When connected to Supernova, component analysis can be enriched with:

- **Component documentation** from Supernova's component pages
- **Design specs** showing intended usage, spacing, and states
- **Token mappings** showing which tokens each component should use
- **Figma links** connecting code components to their design source

Query the Supernova MCP for component metadata to cross-reference against the code analysis. Gaps between Supernova documentation and code implementation are drift signals.

---

## Git Repository Integration

When connected to a git-hosted token/component repository:

1. **Clone/pull** the repository to get current state
2. **Read component source** for implementation analysis
3. **Read token definitions** for the source-of-truth token set
4. **Check git history** for recent changes that might affect component status
5. **Read CI/CD config** for build and test patterns

Store the repository URL in `repository.component_repo` and `repository.token_repo` in the brand config for future reference.

---

*Reference for ui-studio skill. Originally authored for design-system-ux, March 2026.*

*HeyHi Confidential*
