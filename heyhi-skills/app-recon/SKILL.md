---
name: app-recon
description: >-
  Read an application from its own code and emit ground truth before any design,
  Figma, or intent work runs on it. Runs the mechanical read: a tier check with a
  real off-ramp, a read-only in-flight branch scan, a per-surface fan-out with a
  required file:line output shape, endpoints grounded as pointers into the OpenAPI
  and verified against the schema and the handlers, capabilities read from wiring,
  and an app-manifest.json plus a ground-truth brief. Has a delta mode (what changed
  since a baseline commit). Triggers: "read this application", "recon the codebase
  before we design", "what surfaces and endpoints does this app have", "app manifest",
  "ground-truth read of the app", "what does this app actually do". Produces an
  app-manifest.json whose provenance is on every copy and component row, whose
  ungrounded claims live in unverified[], and where which surfaces are in scope, the
  tier when the precedence rule does not decide it, and each unverified[] item ship
  EMPTY behind a named human gate (the brief review). NOT for verifying a finished
  plan against the code it targets (use heyhi-plan-reality-check). NOT for auditing a
  design system's health, token drift, or component-to-code drift (use
  heyhi-design-intelligence-audit). NOT for a Figma component or token library census
  (use figma-library-census). NOT for mapping a product's jobs, journeys, or intent
  (use app-intent-map or intent-journey-map, which read this manifest). NOT for
  writing to Figma, PRDs, stories, or prototypes.
version: "0.1.0"
updated: "2026-09-07"
status: "deployed 2026-09-07 (Sheerline fdde-loop convergence pass 1, DISPATCH-06; promoted from skill-updates/app-recon/). Sheerline forward-deployed loop, read verb (loop stage 1); the codebase-recon method generalized to a HeyHi skill that emits app-manifest.json. Spec: plans/plan-sheerline-fdde-loop-2026-09-07.md 3.1 stage 1 / 3.3 / OWNS Lane C. Buildable-now, proved first on the instance's own application. Registry-entry.yaml drafted, not applied."
review_by: "2026-09-21"
classification: confidential
---

# App Recon

**Sheerline forward-deployed loop, stage 1 (read) · proved first on the instance's own application · a read verb, not an authoring one.** Design and spec work is only as accurate as the ground truth under it. This skill reads the real code before any downstream skill writes anything, so a Figma rebuild, an intent map, or a feature increment targets what is shipped and where the code is heading, not the mockups or memory. It emits two things: a machine `app-manifest.json` (the contract the loop's later stages read) and a ground-truth brief a human reviews. It is read-only against every repository. The method is generalized from the codebase-recon protocol proven once in a sibling engagement (method only; no engagement content crosses).

**The boundary this skill obeys (Sheerline, absolute).** A structured artifact with explicit empty judgment slots, a named human gate, and provenance labels on anything the read could not ground. *Which surfaces are in scope for the artifact, the tier when the precedence rule does not decide it, and every `unverified[]` item are the empty slots.* Reading routes, components, props, copy, endpoints, and capabilities from the code is mechanical; deciding which surfaces to spec, whether an ambiguous change is Tier 1 or Tier 2, and how to resolve an ungrounded claim is the human's. A version of this skill that names an endpoint as real from memory, picks the in-scope surfaces itself, or fills an `unverified[]` item with a guess has exceeded its charter. The read informs; it carries no verdict, score, or pass/fail field.

**Who reads the manifest, and why provenance is not optional.** The manifest is load-bearing for three downstream skills, each of which trusts it as ground truth:

- `app-to-figma` rebuilds each surface in Figma from the client's library and needs the components and props the surface actually uses.
- The intent skills (`app-intent-map`, `intent-journey-map`) read the surfaces, endpoints, and copy to map what the product does and already decides.
- `feature-increment` reads it to size a delta across Figma, the prototype, and the repo.

A component named without a source, or an endpoint named from memory, propagates a wrong build three stages downstream. That is why every copy and component row carries file:line, and why anything the read could not ground is quarantined in `unverified[]` rather than smoothed over. The provenance discipline below is the concrete form of that rule.

> **This skill closes through the Exit Gate (`CLAUDE-SESSION-RULES.md § Exit Gate`).** See the bottom-of-skill bracket.

---

## Inputs and outputs at a glance

| | |
|---|---|
| **Takes** | One or more repositories in scope; an optional running URL; an optional tier hint; the engagement profile (scoping fields); any served prior manifest (as a hypothesis) |
| **Reads** | The running code as ground truth (never a contract, token file, brand config, or DESIGN.md as its spec) |
| **Emits** | `app-manifest.json` (schema version 1.0) and a ground-truth brief a human reviews |
| **Modes** | Full read (stage 1 of the loop); delta read (`--since <commit>`, the read half of Care's monthly recon delta) |
| **Never** | Writes to any repository, the profile, the served context, Figma, or a source of truth; names an endpoint from memory; fills an empty slot |
| **Gate** | The brief review. No downstream skill consumes the manifest until a human signs it. |

---

## Routing: disambiguation with sibling skills

| If the task is… | Use |
|---|---|
| "Read this application / recon the codebase before we design / what surfaces and endpoints does it have" | **this skill** |
| Verify a finished plan against the code it targets (a plan exists; check it) | `heyhi-plan-reality-check` (that checks a plan; this builds ground truth before one) |
| Audit a design system's health, token drift, or component-to-code drift | `heyhi-design-intelligence-audit` (object seam: that measures the design system; this reads the application) |
| Census a Figma component or token library and crosswalk it to code | `figma-library-census` (that reads Figma; this reads code) |
| Map a product's jobs, journeys, encoded decisions, or a feature's intent | `app-intent-map`, `intent-journey-map` (they read this manifest; this produces it) |
| Write the app screens into Figma from the library | `app-to-figma` (it reads this manifest; this produces it) |
| Which surfaces to spec; the ambiguous-tier call; each ungrounded claim | **the human** (this skill's named gate: the brief review) |

The seam with `heyhi-plan-reality-check` is temporal: the reality-check verifies a plan that already exists; this builds the ground truth before the plan. The seam with the design-system audit is object: that audits the system; this reads the application the system dresses. The seam with `figma-library-census` is surface: that reads Figma, this reads code; together they produce the crosswalk, but neither does the other's read.

---

## Step 0: Improvement hook check

Retrieve any recurring corrections for application-read work (`retrieve_design_corrections`, or the Sheerline `os/corrections/` registry). Fold a match into the pass. Skip silently if none.

## Step 1: Load context

1. **The repository or repositories in scope**, plus an optional running URL and a tier hint. The code is the ground truth: this skill reads the running code, never a contract, token file, brand config, or DESIGN.md as its spec (Sheerline § 3.2 / Arc rule 4). If a repository is not available (not mounted or not cloned), it is read doc-only and every claim about it is marked "unverified against code" in `unverified[]`, never guessed.
2. **The engagement profile** (`sheerline/profile/engagement-intake.yaml`, resolved to the filled path at run time). Read, when present, `design_system.component_source` and `component_format` (where the component catalog lives and its shape), `design_system.figma_app_file_key` (the app Figma file, for the downstream build), and the application block `api.spec`, `api.schema`, `api.handlers`, `app.routes`, `app.run_url`. When a field is absent from the profile, ask for it; never infer it. These fields scope the read; they are not its spec.
3. **Any served prior application context** through the instance's `retrieve_application_context` (scope `manifest`), when the instance serves one. Treat a prior manifest as a hypothesis to confirm against the current code, never as truth to trust: a served snapshot goes stale, and the read exists to re-ground it.
4. `references/method.md`: the tier gate, the six moves, the surface fan-out output shape, the OpenAPI-versus-schema-versus-handler verification, and the read-only in-flight and delta commands. THE method spine.
5. `references/worked-example.md`: a filled recon on HeyHi's own site. Read it to calibrate the register and the provenance discipline; do not copy its content.
6. `schemas/app-manifest.schema.json`: the emitted contract's shape (version 1.0). The manifest validates against it before the brief is written.

## Step 2: The tier check (the off-ramp)

Run this first. Most reads are Tier 0 or Tier 1. The tier sets the read's depth and controls token spend at the boundary, not inside a deep run. Deeper grounding costs more tokens now; the return is fewer wrong-output review cycles downstream.

| Tier | When | What runs |
|---|---|---|
| **Tier 0 (skip)** | A single surface, frontend-only, no cross-source dependency, no data or auth behavior change | Skip the full recon; read the file directly. A one-surface manifest, if wanted, is a hand read. |
| **Tier 1 (light)** | One surface, frontend, a design or copy change | Moves 1, 2, 3, 5, 6 (every move except backend grounding, move 4). The fan-out (move 3) is one targeted read or one agent for the single surface. |
| **Tier 2 (full)** | Multiple surfaces, or the change writes data or changes auth or entitlement, or it crosses an architecture boundary | All six moves, including backend grounding (move 4). |

**The precedence rule (binding).** A change that writes data, changes auth or entitlement, or crosses an architecture boundary is **Tier 2 regardless of size**. Surface count never demotes it. When the precedence rule does not fire and the tier is genuinely ambiguous (a one-surface change that might touch a shared data path), the tier is a **human call**: record the candidate tier and the ambiguity in the brief; do not silently pick the cheaper read. The backend grounding move (4) fires only at Tier 2, and only when the change writes data or changes auth or entitlement; a surface that merely reads an endpoint does not trigger it.

The tier does not turn moves on and off arbitrarily. Move 1 (consult) always precedes the rest and move 6 (emit) always closes; the tier gates only two things: whether the fan-out (move 3) is capped to a single surface (Tier 1) or spans several (Tier 2), and whether the backend grounding (move 4) fires at all. That is why Tier 1 still runs move 3: even a one-surface copy change needs that surface's components and copy grounded at file:line.

Worked calls, so the gate is legible:

- A copy tweak on one marketing page: Tier 0. Read the file.
- A restyle of one form, no new fields, no new call: Tier 1. Read the surface and its in-flight branches.
- A one-field addition to a form that posts to a new write endpoint: Tier 2. The precedence rule fires on "writes data" even though it is one surface.
- A whole-application inventory across several surfaces, for the loop's stage 1: Tier 2 by surface count. When the application has no API, the backend move still runs and lands an honest empty `endpoints[]`.

## Step 3: The moves (all read-only)

Each move reads; none mutates a tree. No command in this skill or its references runs a mutating git subcommand (`pull`, `checkout`, `reset`, `stash`), or edits a file in a target repository.

1. **Consult, as hypotheses.** Read what the profile and any served prior manifest record, to scope the read and form hypotheses. Do not use them to skip verifying a load-bearing fact: served snapshots and profiles go stale. Confirm the repositories in scope are available; a missing one yields an "unverified against code" mark, never a guess.
   *Produces:* the candidate surface list and `source_commit`; an `unverified[]` row per unavailable repository.
2. **Scan in-flight branches, read-only.** In each repository in scope: `git fetch`, then `git diff --stat main...origin/<branch>` on active branches, to find migrations or refactors in progress. Record which surfaces are mid-migration and the file the end state lands in (`in_flight.branch`, `in_flight.lands_in`), so a downstream spec targets the destination, not soon-dead code. Never pull or check out a branch.
   *Produces:* the `in_flight` block on any surface mid-migration.
3. **Fan out by surface, capped.** For each in-scope surface, launch one subagent (a general-purpose agent for behavior, an Explore agent for pure location) with three inputs: the exact container directory, the intent or acceptance criteria, and a required file:line-cited output shape (see `references/method.md`). A surface is a product feature-area with its own container directory (a route and its container), not a file. Fold related surfaces into one agent. Cap: one agent per surface; if a surface is too entangled for one agent, record the exception in the brief. Every `components_used` row carries the props actually passed, their defaults, and a `source` with file:line; every `copy` row carries `file` and `line`. The read reuses, by reference, the component-inventory and framework-detection reads in `heyhi-skills/design-system-onboard/SKILL.md` (lines 108-113, 300-308) and the coverage sense in `heyhi-skills/heyhi-design-intelligence-audit/SKILL.md` line 176; it does not restate them.
   *Produces:* `surfaces[].components_used`, `surfaces[].copy`, `surfaces[].route`, `surfaces[].container_dir`, `surfaces[].entry_component`, `surfaces[].breakpoints`, and the per-surface `endpoints[]` call sites.

   The fan-out prompt carries the three inputs and demands the file:line shape back (full version in `references/method.md`):

   ```
   Read the surface at <container_dir>. Intent: <AC or design intent>.
   Return ONLY, with file:line on every row, no prose verdict:
     route, container_dir, entry_component, breakpoints
     components_used[]: name, props_passed, defaults, source (file:line of the call site)
     copy[]: text (verbatim), role, file, line
     endpoints[] called from this surface: method, path, hook
     theme and architecture_target, each with the wiring file:line, or "unresolved"
   Anything you cannot ground from the code: list it, do not guess it.
   ```
4. **Ground the backend (Tier 2, writes or auth or entitlement only).** Read the OpenAPI spec named in the profile (`api.spec`). For each endpoint, record `method`, `path`, and JSON pointers into the spec (`request_pointer`, `response_pointer`), then verify each pointer against the schema (`api.schema`) and the handler (`api.handlers`) and read `auth` and `entitlement` from the handler. **Never name an endpoint as real from memory.** An endpoint with no spec, or a spec repository not available, is not written into `endpoints[]`; it goes to `unverified[]`. Follow `heyhi-plan-reality-check`'s discipline by reference: a claim is real only when a command grounds it.
   *Produces:* the top-level `endpoints[]` registry, each endpoint's `auth` and `entitlement` read from its handler; or, when the application has no API, an honest empty `endpoints[]`. A Tier-2 read may also confirm `capabilities.writes` and `capabilities.roles` against the handlers, but it does not originate the `capabilities` block (move 5 does).
5. **Verify theme and architecture from wiring.** Confirm each surface's `theme` from the theme wiring and its `architecture_target` from the auth and shell wiring. Do not infer either from the surrounding chrome. An unresolved theme or target is an `unverified[]` row, not a best guess.
   *Produces:* `surfaces[].theme`, `surfaces[].architecture_target`, and the whole `capabilities` block (`auth_model`, `roles`, `writes`, `offline_sync`, `feature_flags`), all read from wiring. This is why `capabilities` is populated at every tier, not only Tier 2: it is a wiring read, not a backend read.
6. **Emit, do not integrate.** The manifest and the brief are the output. Durable facts (confirmed themes, real endpoints, corrected docs) are queued in the brief for a separate, human-gated integration step (the instance serves the manifest through Lane E's `retrieve_application_context`; a profile correction is a separate edit). This skill never edits the profile, the served context, or any source of truth mid-recon.
   *Produces:* the validated `app-manifest.json` and the ground-truth brief, with the three empty slots and the gate blank.

**Delta mode (`--since <commit>`).** Given a baseline commit, run `git diff --stat <baseline>..HEAD` (read-only) to find the surfaces that changed, re-recon only those, and emit a manifest with `source_commit` bumped to the new HEAD and the baseline recorded in the brief. This is the read half of Care's monthly recon delta; it never re-reads unchanged surfaces.

### Multiple repositories

An application is often more than one repository: a frontend, a backend or API repository, sometimes a shared package. The read handles several at once.

- One `app-manifest.json` per application (`system_id`), not per repository. The frontend repository supplies most `surfaces[]`; the API repository supplies the `endpoints[]` grounding (move 4).
- The in-flight scan (move 2) runs in every repository in scope, so a migration in the API repository is recorded against the surfaces it lands under, not lost.
- When the frontend is available but the API repository is not, the surfaces read normally and every endpoint the frontend calls goes to `unverified[]` with reason "API repository not available", never grounded from the call site alone. A call site proves the frontend asks for an endpoint; it does not prove the endpoint's shape, auth, or entitlement.
- `source_commit` records the primary repository's HEAD; any secondary repository's commit is noted in the brief.

### Provenance discipline (what counts as grounded)

Every row in the manifest is one of two things: grounded, or in `unverified[]`. There is no third state, and nothing is filled from memory.

| Fact | Grounded when | Otherwise |
|---|---|---|
| A component a surface uses | The import resolves and the call site is read at a file:line | `unverified[]` row for that surface |
| The props a component is passed | Read at the call site, with the component's declared defaults | Passed props omitted; note in `unverified[]` if the call site could not be read |
| A copy string | Quoted verbatim from the source with `file` and `line` | Never included; a remembered string is not copy |
| An endpoint | A pointer resolves in the OpenAPI spec and the handler confirms method, auth, and entitlement | `unverified[]` row; never written to `endpoints[]` |
| A surface's theme or architecture target | Read from the theme, auth, or shell wiring | `unverified[]` row; never inferred from surrounding chrome |
| Anything in a repository that is not available | (cannot be grounded) | `unverified[]` row marked "unverified against code" |

The test for a claim is `heyhi-plan-reality-check`'s test, applied before the plan exists: a fact is real only when a command grounds it. `unverified[]` is not a failure state; a manifest with a full `unverified[]` and honest provenance is more useful than one that looks complete and is wrong.

## Step 4: Emit the manifest and the brief

Emit `app-manifest.json` (validated against `schemas/app-manifest.schema.json`, version 1.0) with the fields in the schema, and a ground-truth brief in this shape. The three empty slots stay empty by construction.

```
# App Recon Brief: [system_id]
Read: [date]   Source commit: [sha]   Tier: [0 | 1 | 2]   Baseline (delta mode): [sha | n/a]
This read informs; it renders no verdict, score, or pass/fail. It carries only ground truth and the claims it could not ground.

## Surfaces read
[One line per surface fanned out: id, route, container_dir, the count of components and copy rows grounded.]

## Candidate surfaces NOT yet in scope
[Surfaces found in the router but not fanned out this pass. These are candidates, not a decision.]

## Endpoints (Tier 2)
[The grounded endpoint registry, or "no API: endpoints[] is empty (verified: no server functions or API routes found)".]

## Capabilities
[auth_model, roles, writes, offline_sync, feature_flags, read from wiring; an honest empty case stated as such.]

## In-flight
[Surfaces mid-migration and where the end state lands, from the read-only branch scan; or "none observed".]

## Durable facts to integrate (queued, not applied)
[Confirmed themes, real endpoints, corrected docs, for a separate human-gated step. This skill applies none of them.]

## ⛔ Which surfaces are in scope: NEEDS HUMAN
This slot is intentionally empty. The read lists the candidate surfaces; which ones the artifact covers is the human's scope call.
   In-scope surfaces: ____________________

## ⛔ The tier, where the precedence rule did not decide it: NEEDS HUMAN
[Empty only when the precedence rule did not fire and the tier is ambiguous; otherwise state the forced tier and why.]
   Confirmed tier: ____________________

## ⛔ Unverified claims: NEEDS HUMAN (one line each)
[Every unverified[] row, verbatim. Each is resolved by the human: confirm it, supply the missing repository or spec, or accept the gap. The skill never fills one.]

## Named gate
Brief reviewer (the engineering or design owner of this read): ____________________  Date: ______
No downstream skill consumes this manifest until this line is signed by a human.
```

**The read is done when** every in-scope surface has a manifest row with file:line provenance on every copy and component, the endpoint registry is grounded or honestly empty, `unverified[]` is present (empty with a one-line reason, or populated), the manifest validates against the schema, and the three ⛔ slots and the gate are blank.

## Step 5: Pre-flight verification

Confirm: the manifest validates against `schemas/app-manifest.schema.json`; every `copy` row and every `components_used` row carries file:line provenance; no endpoint appears in `endpoints[]` without a spec pointer (ungrounded endpoints are in `unverified[]`); no claim about an unavailable repository was guessed; no command in the run mutated a tree (the mutating git subcommands `pull`, `checkout`, `reset`, `stash` never ran); `unverified[]` is present; the three ⛔ slots and the gate are empty; the manifest carries no verdict, score, or pass/fail field, and `tier` is used as a scope selector, not a grade; no client name or file key appears when the hermetic seal is confirmed.

---

## What is explicitly out of scope

- **Which surfaces to spec, the ambiguous-tier call, and each `unverified[]` resolution.** Empty by construction. The read lists candidates, forces the tier where the precedence rule fires, and flags what it could not ground; the human decides.
- **Naming an endpoint from memory.** An endpoint is written to `endpoints[]` only when a spec pointer grounds it and the handler confirms it. Everything else is `unverified[]`.
- **Verifying a finished plan** (`heyhi-plan-reality-check`). **Auditing a design system** (`heyhi-design-intelligence-audit`). **A Figma library census** (`figma-library-census`). **Mapping intent or journeys** (`app-intent-map`, `intent-journey-map`). **Writing to Figma, or producing PRDs, stories, or prototypes** are all out of this skill entirely.
- **Any write.** The skill is read-only against every repository and never edits the profile, the served context, or a source of truth. Durable facts are queued for a separate human-gated step.

---

## Improvement hooks

The read gets sharper with use, and mis-calibration shows up in patterns, not single runs. These are the portable self-checks carried from the source method.

- **Reference case.** Run the skill against `references/worked-example.md` (HeyHi's own site). It must surface the five surfaces, ground the home and log-index copy at file:line, and land an honest empty `endpoints[]` with the no-API reason stated. A miss on any of those is a regression in the skill, not the site.
- **Tier calibration.** After three real reads, check the off-ramp: did the small changes actually stay at Tier 0 and Tier 1? If every read lands at Tier 2, the tiers are mis-calibrated and the gate needs re-drawing, not ignoring.
- **Consult-to-scope.** When consulting the profile and the served prior manifest fails to cut the fan-out (the read has to re-derive everything from scratch), that is a thinness signal in the served context to close, not a reason to skip the consult. Note it in the brief's durable-facts queue.
- **Provenance drift.** If `unverified[]` is empty on a first read of an unfamiliar application, be suspicious: a first read of real code almost always leaves something ungrounded. An empty `unverified[]` is earned by grounding, not by confidence.

---

## Exit Gate Required Headers (bottom-of-skill bracket)

This skill closes through Exit Gate Flavor A (`CLAUDE-SESSION-RULES.md § Exit Gate`). Before declaring done, confirm every required header holds real content:

- `## Fixes Applied` (or the delivered manifest and brief)
- `## Smoke Test` (the Step 5 pre-flight checks, pasted)
- `## Next Session Prompt`

If any ⛔ slot is filled, an endpoint is named without a spec pointer, a verdict or score field exists, or any command mutated a tree, the gate has **not** been satisfied.

---

*HeyHi Confidential. Sheerline forward-deployed loop, stage 1 (read). Staged 2026-09-07 (v0.1.0) in `skill-updates/`, registry-inert until convergence pass 1 promotes it. Spec source: `plans/plan-sheerline-fdde-loop-2026-09-07.md` § 3.1 stage 1 / § 3.3 / OWNS Lane C. Method attribution: the codebase-recon protocol (a sibling engagement, method only). Contract: `app-manifest.json` (schema version 1.0). The advisory-never-gate construction follows `divergence-guard`'s read-informs-not-gates precedent.*
