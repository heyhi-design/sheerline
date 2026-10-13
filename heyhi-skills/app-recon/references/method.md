---
classification: confidential
title: "app-recon method: the tier gate, the six moves, the fan-out shape, and the verification rules"
skill: app-recon
loaded_by: "SKILL.md Step 1 (the method spine)"
---

# app-recon method

The method spine. SKILL.md is the procedure; this reference carries the operational detail: the tier gate and its precedence rule, the six moves in full, the required surface fan-out output shape, the endpoint verification rules, and the read-only command set. Nothing here mutates a tree.

## The tier gate and the precedence rule

The tier sets the read's depth. Run the check first, on every read.

| Tier | Condition | Moves that run |
|---|---|---|
| 0 (skip) | One surface, frontend-only, no cross-source dependency, no data or auth behavior change | none: read the file directly |
| 1 (light) | One surface, frontend, a design or copy change | 1, 2, 3, 5, 6 (no backend grounding) |
| 2 (full) | Multiple surfaces, or a write, or an auth or entitlement change, or an architecture-boundary crossing | 1 through 6 |

**Precedence rule (binding).** A change that writes data, changes auth or entitlement, or crosses an architecture boundary is Tier 2 regardless of size. Surface count never demotes a Tier 2 to a lighter read. When the precedence rule does not fire and the tier is genuinely ambiguous, the tier is the human's call, recorded in the brief. The backend grounding move (4) fires only at Tier 2, and only for a write, auth, or entitlement change; a surface that merely reads an endpoint does not trigger it.

Token honesty: deeper tiers cost more tokens now (each fanned-out subagent re-ingests context), and the return is fewer wrong-output review cycles downstream. Spend is controlled at the tier boundary and over time (by compounding confirmed facts into the served context), not inside a single deep run.

## The six moves, in full

1. **Consult, as hypotheses.** Read the profile (`sheerline/profile/engagement-intake.yaml`, resolved at run time) and any served prior manifest (`retrieve_application_context`, scope `manifest`). Use them to scope the read and form hypotheses, never to skip verifying a load-bearing fact. Confirm each repository in scope is available. A repository that is not mounted or cloned is read doc-only, and every claim about it is an `unverified[]` row marked "unverified against code".
2. **Scan in-flight branches, read-only.** Per repository: `git fetch`, then `git diff --stat main...origin/<branch>` on each active branch. Record surfaces mid-migration and the file the end state lands in. Never a mutating git subcommand (`pull`, `checkout`, `reset`, `stash`).
3. **Fan out by surface, capped.** One subagent per surface (general-purpose for behavior, Explore for pure location), with the three inputs and the required output shape below. A surface is a feature-area with its own container directory, not a file. Fold related surfaces; cap at one agent per surface; record the exception if a surface is too entangled for one agent.
4. **Ground the backend (Tier 2, write or auth or entitlement only).** Verify every endpoint against the OpenAPI spec, its schema, and its handler (rules below). Never name an endpoint as real from memory.
5. **Verify theme and architecture from wiring.** Read each surface's theme from the theme wiring and its architecture target from the auth and shell wiring. Do not infer either from surrounding chrome. Unresolved reads go to `unverified[]`.
6. **Emit, do not integrate.** Emit the manifest and the brief. Queue durable facts (confirmed themes, real endpoints, corrected docs) in the brief for a separate, human-gated integration step. Never edit the profile, the served context, or any source of truth mid-recon.

## The required surface fan-out output shape

Each surface subagent returns exactly this, with file:line on every row and no prose verdict. The shape maps one-to-one onto the manifest's `surfaces[]` fields.

```
route:                <url path, from the router wiring, file:line>
container_dir:        <the directory that owns the surface>
entry_component:      <the component the route mounts, file:line>
breakpoints:          [<breakpoint tokens read from the layout, file:line>]
theme:                <read from the theme wiring, file:line | "unresolved">
architecture_target:  <read from the auth/shell wiring, file:line | "unresolved">
components_used[]:
  - name:             <component name>
    props_passed:     {<props actually passed at the call site>}
    defaults:         {<defaults the component declares for props not passed>}
    source:           <import path or package, plus file:line of the call site>
copy[]:
  - text:             <the string, verbatim from source>
    role:             <heading | body | label | cta | ...>
    file:             <file>
    line:             <line>
endpoints[]:          # per-surface call sites only; the verified registry is the top-level endpoints[]
  - method:           <verb>
    path:             <path as written at the call site>
    hook:             <the hook or call site issuing the request>
unverified[]:
  - claim:            <anything the agent could not ground from the code>
    reason:           <why it could not be grounded>
```

The rule the shape enforces: a fact is either grounded at a file:line, or it is an `unverified[]` row. There is no third state, and nothing is filled from memory. A component with no readable call site is `unverified[]`, not an omission. A remembered copy string is not copy.

## Endpoint verification: spec, then schema, then handler

At Tier 2, an endpoint earns a row in the top-level `endpoints[]` only when all three hold. Any that fail go to `unverified[]`.

1. **Spec.** The endpoint's `method` and `path` resolve in the OpenAPI spec named in the profile (`api.spec`). Record `request_pointer` and `response_pointer` as JSON pointers into the spec (or `null` when the spec declares none, for example a bodyless GET). A `path` the frontend calls but the spec does not declare is `unverified[]`, reason "not in the OpenAPI spec".
2. **Schema.** Each pointer resolves to a real definition in the schema (`api.schema`). A dangling pointer (the spec references a schema the schema file does not define) is `unverified[]`, reason "pointer does not resolve in the schema".
3. **Handler.** A handler in the code (`api.handlers`) actually serves that method and path, and its `auth` and `entitlement` are read from the handler, not from the spec's prose. An endpoint documented in the spec with no handler is `unverified[]`, reason "no handler found"; the read never trusts a spec over the code.

A frontend call site (move 3) proves the frontend asks for an endpoint. It does not prove the endpoint exists, or its shape, auth, or entitlement. Only the spec-schema-handler chain grounds those. When the API repository is not in scope, every endpoint the frontend calls is `unverified[]`, reason "API repository not available".

## The read-only command set

Every command the skill runs is one of these. None mutates a tree.

| Purpose | Command |
|---|---|
| Refresh remote refs | `git fetch` (read-only; never the mutating pull) |
| Scan an in-flight branch | `git diff --stat main...origin/<branch>` |
| Delta mode: changed surfaces since a baseline | `git diff --stat <baseline>..HEAD` |
| Record the commit read | `git rev-parse HEAD` |
| Inspect a file | Read / Grep only |

Forbidden in this skill and its references: the mutating git subcommands (`pull`, `checkout`, `reset`, `stash`), and any write to a target repository. The read establishes ground truth; it never changes the tree it reads.

## Delta mode

Given `--since <baseline>`: run `git diff --stat <baseline>..HEAD`, take the changed files, map them to surfaces (a file under a surface's `container_dir` marks that surface changed), re-run moves 3 through 5 on only the changed surfaces, and emit a manifest with `source_commit` at the new HEAD and the baseline recorded in the brief. Unchanged surfaces carry forward from the prior manifest untouched. This is the read half of Care's monthly recon delta.

---

*HeyHi Confidential. Method reference for `app-recon` (Sheerline Lane C). Spec source: `plans/plan-sheerline-fdde-loop-2026-09-07.md` § 3.1 stage 1 / § 3.3. Method attribution: the codebase-recon protocol (a sibling engagement, method only; no engagement content crosses).*
