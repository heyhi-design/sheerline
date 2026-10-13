---
classification: confidential
title: "feature-increment: repo adapters (React built; Lit and Angular stubbed)"
---

# Repo adapters

The repo leg (SKILL.md Step 5) scaffolds the feature typed from the contract, in the frontend framework the profile names. This arc builds the **React** adapter (plan § 5 D5, override: React only for now). **Lit** (web components) and **Angular** are named extension points with a stub shape, deferred until an engagement pulls them. This reference gives the React adapter in full and the two stubs enough shape to be filled later without re-deciding the seam.

The adapter is a shape, not a generator: it says what files the increment produces and how each maps to a contract row. The skill applies it; a human reviews the propose-first PR.

## The contract-to-scaffold mapping (framework-agnostic)

Every adapter maps the same contract rows to the same concepts; only the syntax differs.

| Contract row | Scaffold artifact |
|---|---|
| a component + its props | a typed component whose prop type is the contract's prop list (name, type, required, enum) |
| a variant axis | a variant prop (a union type) and, where the repo has a story harness, one story per variant |
| a data prop bound to an endpoint | a hook stub typed to the endpoint's request/response pointer |
| a route the feature adds | a route registration stub |
| an unbindable prop (the contract flagged it) | a typed placeholder with a `// contract: unbound` marker, never a fabricated value |
| a component the ds-map says exists in the package | an import from the design-system package, not a re-implementation |
| a component the ds-map says the package lacks | a local pattern in the repo, named from the ds-map, with a ledger row |

## React adapter (built)

The one this arc runs. Files the increment produces for a NEW component:

```
src/components/<Feature>/<Component>.tsx        // the typed component
src/components/<Feature>/<Component>.stories.tsx // one story per variant (only if the repo has Storybook)
src/hooks/use<Feature>.ts                        // a hook stub, typed to the endpoint pointer (only if the feature reads data)
src/routes/<route>.tsx                           // a route stub (only if the feature adds a route)
```

Rules specific to React:

- **Props are the contract.** The `Props` type is the contract's prop rows verbatim: `type Props = { categories: string[]; selected: string; onSelect: (c: string) => void }`. A required prop is non-optional; an enum prop is a union type.
- **Imports over re-implementation.** A ds-map `both` / `code-only` row imports the component from the package (`import { Chip } from "<package>"`), never redraws it. The worked example's `heyhi-website` has no separate design-system package, so the crosswalk resolves against the repo's own `src/components/ui/` and its design tokens: where an existing component matches, the increment imports it; where none does (the chip has no match in `ui/`, which holds only `responsive-image`), the increment builds a local component from the repo's own token classes (`text-*` / `bg-accent` / `border-annotation`) rather than raw values. The finding notes the absent package.
- **State is local unless the contract says otherwise.** A client-only feature (the category filter) uses `useState`; a data-bound feature uses the hook stub. The skill never invents a fetch the contract does not carry.
- **Typecheck with the repo's command.** For `heyhi-website`: `eslint . && tsc --noEmit`. A failure is a finding on the increment, fixed toward the contract.
- **Stories are conditional on the harness.** `heyhi-website` has no Storybook; the story file is a named gap with a finding id, not an invented harness. When the repo has Storybook, one story per variant renders the variant matrix for the reviewer.

## Lit adapter (named stub, not built)

Deferred to an engagement pull (plan D5). The shape, so it can be filled without re-deciding the seam:

```
src/components/<component>.ts     // a LitElement with @property() decorators typed from the contract
src/components/<component>.stories.ts
```

The mapping is the same: `@property()` fields are the contract's props; a variant axis is a reflected attribute; the ds-map decides import vs local. The open question a builder must answer: how the design-system package publishes web components (custom-element registration vs a wrapped export), which is engagement-specific. Do not build this until an engagement names a Lit repo.

## Angular adapter (named stub, not built)

Deferred to an engagement pull (plan D5). The shape:

```
src/app/<feature>/<component>.component.ts   // @Input() fields typed from the contract
src/app/<feature>/<component>.component.html
src/app/<feature>/<component>.stories.ts
```

The mapping is the same: `@Input()` fields are the contract's props; a variant axis is an input union; the ds-map decides import vs local. The open question: whether the engagement uses standalone components or NgModules, which changes the route and import shape. Do not build this until an engagement names an Angular repo.

## The deviation record (all adapters)

The repo leg's conformance read (`validate_output` on the increment's CSS) writes findings into a reversible deviation record, reusing `heyhi-drift-repair`'s shape:

```json
{
  "finding": "<what validate_output flagged>",
  "matched_correction": null,
  "before": "<the value in the increment>",
  "after": "<the conformant value, or null if the human must decide>",
  "surface": "<the component / route>",
  "location": "<file:line>",
  "timestamp": "<iso>",
  "provenance": "automated",
  "confirmed": false
}
```

The shape is `heyhi-drift-repair`'s deviation record verbatim. `matched_correction` is `null` here by construction: a raw `validate_output` conformance finding has no corrections-registry match (that field is set only when a finding resolves against the corrections module, which is drift-repair's own machinery, not the repo leg's). The repo leg is propose-first: the record is the human-confirmation queue, `confirmed` flips only on a human's review, and the PR is never merged by the skill. This is the seam with `heyhi-drift-repair`: that skill owns applied and proposed repairs across a whole system, matching findings to corrections and setting `matched_correction`; this skill reuses the record shape for one feature's increment and hands genuine drift to it.

*HeyHi Confidential. `skill-updates/feature-increment/references/`. React adapter built (plan D5); Lit and Angular stubbed. Deviation-record shape reused from `heyhi-drift-repair`.*
