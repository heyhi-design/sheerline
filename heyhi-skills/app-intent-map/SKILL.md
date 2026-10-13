---
name: app-intent-map
description: >-
  Read an application's manifest and write the layer above its surfaces: the
  jobs the product serves, the flows across surfaces, the decisions the product
  already encodes, the vocabulary it uses, and the constraint list any new
  feature must honor. Runs the mechanical work: derive each layer from the
  manifest, evidence-link every job / flow / encoded decision / vocabulary term /
  constraint to a manifest surface id, a file and line, or a JSON pointer (or mark
  it an assumption), and emit a human intent map plus a machine intent-map JSON.
  Produces an Application Intent Map where "what the product is for" (its purpose)
  ships EMPTY behind a named human gate, that is a product judgment, not a
  mechanical one. Triggers: "map the product's intent", "application intent map",
  "app intent map", "what does this product already decide", "what jobs and
  constraints does this product encode", "read the app's intent". NOT for one
  feature's intent and its bound prop-contract (use intent-journey-map). NOT for
  reading the codebase into a manifest (use app-recon; this consumes the
  manifest). NOT for auditing an opportunity tree or JTBD reasoning (use
  strategy-integrity-warden). NOT a taxonomy or information-architecture study
  (taxonomy and labeling audits are `taxonomy-labeling-auditor`, a deployed
  area-2 skill; the structure-design IA skills stay D-3-gated). It writes no prototype, PRD, or story, and it never
  states the product's purpose for the team.
version: "0.1.0"
updated: "2026-09-07"
status: "deployed 2026-09-07 (Sheerline fdde-loop convergence pass 1, DISPATCH-06; promoted from skill-updates/app-intent-map/). Sheerline area 9 (Design Strategy & Product Thinking); serves_areas hints to 1 (User Research) and 2 (Information Architecture), registered nowhere before D-3 (plan § 5 D11). Lane D of the Sheerline forward-deployed loop (plans/plan-sheerline-fdde-loop-2026-09-07.md, DISPATCH-04). The application-level companion to intent-journey-map; the one prior 'intent-map how the product works' exercise (decision-log § 2026-07-16) is the shape it generalizes."
review_by: "2026-09-21"
classification: confidential
---

# Application Intent Map

**Sheerline area 9 (Design Strategy & Product Thinking) · serves areas 1 and 2 · read + structure skill.** Given an application manifest (what surfaces, components, endpoints, and capabilities the app has), this skill writes the layer above those surfaces: the jobs the product serves, the flows that connect its surfaces, the decisions the product already encodes in its own behavior, the vocabulary it speaks, and the constraint list any new feature has to honor. It reads what the application *is*, so the next feature is designed with the product's own logic in hand rather than someone's memory of it. It stops at the point where a human must say what the product is *for*.

**The boundary this skill obeys (Sheerline § 9, absolute).** A structured artifact with explicit empty judgment slots, a named human gate, and provenance labels on anything synthetic. *The product's purpose, "what this product is for," is the empty slot, null by construction.* Deriving the jobs, flows, encoded decisions, vocabulary, and constraints from the manifest, and evidence-linking each, is mechanical. Stating the product's purpose is a product-strategy judgment, and inferring it from the surfaces would launder a machine's read into a mission. A version of this skill that fills `purpose` has exceeded its charter. Every derived row carries evidence (a manifest surface id, a file and line, or a JSON pointer) or is labeled an assumption; nothing is asserted from the shape of the app alone.

> **This skill closes through the Exit Gate (`CLAUDE-SESSION-RULES.md § Exit Gate`).** See the bottom-of-skill bracket.

The one prior "intent-map how the product works" exercise (decision-log § 2026-07-16; `plans/plan-firm-of-one-os-architecture-diagrams-2026-07-15.md` § 2) read a product into its layer-models, its recursions, and the decisions it encoded, and kept honesty guards on every caption. It was never codified. This skill is that codification, generalized to any application with a manifest.

## The five layers at a glance

| Layer | The question it answers | Ships |
|---|---|---|
| Jobs | What does a user come here to get done? | evidence-linked |
| Flows | Which paths across surfaces support those jobs? | evidence-linked |
| Encoded decisions | What has the product already decided, in its behavior? | evidence-linked (the highest-value layer) |
| Vocabulary | What does the product call things, in its own words? | evidence-linked |
| Constraints | What must any new feature honor? | listed, never ranked |
| **Purpose** | **What is the product for?** | **EMPTY, null by construction (the human's)** |

Read the layers top to bottom; the encoded decisions and constraints are the layer a new feature collides with if it is designed without reading the app first.

---

## Routing between sibling skills

| If the task is… | Use |
|---|---|
| "Read the whole product's intent, its jobs, flows, encoded decisions, vocabulary, constraints" | **this skill** |
| One feature's intent, journey, and bound prop-contract | `intent-journey-map` |
| Reading the repository into a grounded `app-manifest.json` | `app-recon` |
| Auditing an opportunity tree / JTBD / prioritization artifact's reasoning | `strategy-integrity-warden` |
| Auditing or structuring a taxonomy, labels, or navigation | `taxonomy-labeling-auditor` (area 2, deployed, for taxonomy/labeling; the structure-design IA skills stay D-3-gated) |
| Stating what the product is *for* (its purpose) | **the human** (this skill's named gate) |

The seam with `intent-journey-map` is altitude: this skill reads the whole application's intent once; the intent-journey map takes one feature down to its bound props. The seam with `app-recon` is direction: recon reads the code into a manifest; this reads the manifest into intent. This skill consumes a manifest; it never produces one.

---

## The evidence rule (the spine of this skill)

Every row this skill writes carries an `evidence` reference, or it is marked an `assumption`. There is no third option, and a claim about what the product does that neither points at the manifest nor admits it is a guess is not written. This is what separates an intent map from a plausible story about the app.

An `evidence` reference is one of four kinds:

- **`surface_id`**, a surface id in the manifest (`surfaces[].id`).
- **`file_line`**, a file and line the manifest already carries (a `copy[]` row's `file` and `line`, a component's provenance).
- **`json_pointer`**, a JSON pointer into the application's OpenAPI, for an endpoint-encoded gate or capability.
- **`assumption`**, the explicit label for a row the sources do not support. An assumption is allowed; an unlabeled guess is not.

The distinction matters most on the encoded-decisions layer: the whole value of naming a decision the product already makes is that a new feature can be checked against it. A decision "read" from the vibe of the app, with no anchor, is worse than no decision at all, because a later feature will trust it. So the rule is strict: anchor it, or label it an assumption, or leave it out.

## Inherited invariants (cited by path, not restated)

This skill sits under the Sheerline area-9 governance manifest (`sheerline/os/foundations/design-strategy/FOUNDATION.md`) and inherits the always-loaded behavioral guardrails authored once in `sheerline/os/operating-principles.md`:

- **What stays human** (`operating-principles.md` § What stays human) names direction selection and the positioning stance; stating the product's purpose is that call, so it is the empty slot here.
- **Scoring is advisory, never a gate** (`operating-principles.md` § the taste-and-critique boundary) is why the constraints are listed, not ranked: an ordering would read as a priority the skill has no charter to set.
- **The empathy boundary** (`operating-principles.md` § The empathy boundary) governs the job layer: a job story is inferred from the surfaces, and an inferred job is labeled as such, never presented as a user's lived account.

This skill is not a taxonomy or information-architecture study skill (that is `taxonomy-labeling-auditor` and the other area-2 skills); it reads intent, it does not author a taxonomy. The routing table and the `not_for` clauses say so.

## Step 0: Improvement hook check

Retrieve any recurring corrections for intent-mapping work (`retrieve_design_corrections`, or the Sheerline `os/corrections/` registry). Fold a match into the pass. Skip silently if none.

## Step 1: Load the manifest

Read the application manifest through `retrieve_application_context(query, scope="manifest")` when the per-system instance serves it, falling back to a passed `app-manifest.json` file path only for the manifest itself. When a prior intent map exists and the instance serves it, load it too (`scope="intent"`) and update rather than restate; when the served context is not present, there is no prior map to load, so skip that read and build fresh. (`retrieve_application_context` is served by the serving lane of this arc; until it lands, the manifest arrives by file path and the prior-map read is skipped.) The manifest is the evidence base: every row this skill writes points back into it (a surface id, a file and line one of its `copy[]` or `components_used[]` rows carries, or an endpoint's JSON pointer). Do not re-read the codebase here; `app-recon` already grounded it, and its `unverified[]` list carries forward.

**How the manifest feeds each layer.** The manifest is not read whole for each layer; each layer draws from a specific part of it. Reading it this way keeps every derived row anchored to a real field.

| Layer | The manifest fields it draws from |
|---|---|
| Jobs | `surfaces[].id`, `surfaces[].route`, and what each surface's `components_used[]` and `copy[]` let a user do |
| Flows | `surfaces[].id` and `surfaces[].route` (the reachable paths), plus `in_flight` for a path still landing |
| Encoded decisions | `capabilities` (auth, roles, writes, offline_sync, feature_flags), `endpoints[].auth` and `entitlement`, and `copy[]` that states a deliberate posture |
| Vocabulary | `surfaces[].copy[]` (the product's own words) and the route and container names |
| Constraints | the `capabilities` and encoded decisions, read as obligations on the next feature |

A field the manifest marks `unverified[]` stays unverified in the map; it is never promoted to evidenced because it reached a second document.

## Step 2: Derive the layers, evidence-linked

Each layer below is derived from the manifest; the full derivation rules for each are in `references/method.md`. Every row carries an `evidence` reference (a manifest surface id, a file and line, or a JSON pointer) or is explicitly marked an `assumption`. A row with neither is not written.

1. **Jobs.** The jobs the product serves, one job story each (*When [situation], I want to [motivation], so I can [outcome]*), each traced to the surfaces that serve it. Derive the job from what the surfaces let a user do, not from a persona goal imagined for them. A job the manifest does not evidence is an assumption, labeled so, not a confident claim. Example: *When I need to check a balance, I want to open the account view, so I can act on the current number* (evidence: the account surface id).
2. **Flows.** The paths that connect surfaces, each naming the manifest surface ids it moves through and the trigger that advances it. A flow is a real path in the app, evidenced by the surfaces and their routes, not a wished-for journey. A flow that requires a surface the manifest does not carry is flagged, not drawn. Example: *sign-in surface, then dashboard, then account detail*, triggered by opening an account row.
3. **Encoded decisions.** The decisions the product already makes in its own behavior. This is the highest-value layer: it is what a new feature will collide with if it is not read first. There are three kinds, and each row names which:
   - **A gate it enforces** (a visibility rule, an auth check, an entitlement). Evidence: the capability or the endpoint `auth` / `entitlement` that enforces it. Example: "an item renders only when its published flag is true."
   - **A default it sets** (an ordering, a pre-selected mode, a fallback). Evidence: the code or copy that sets the default. Example: "the list defaults to newest-first."
   - **A deliberate absence** (a thing it pointedly does not do, evidenced by copy or structure that says so). Evidence: the copy or the missing-by-construction capability. Example: "no lead-capture form; the copy says it is a place to read, not a funnel."
   Each is evidence-linked to the manifest surface, file and line, or capability that encodes it. A decision inferred from behavior with no anchor is marked an assumption, never asserted.
4. **Vocabulary.** The terms the product uses in its own copy and structure, each with the meaning the app gives it (not a dictionary meaning) and the surface it appears on. The product's language, read from its `copy[]` and routes, not renamed to tidier words. A term the product overloads (one word, two meanings across surfaces) is worth its own row: the collision is a real fact about the product. Example: "account" means a login on the sign-in surface and a financial record on the dashboard.
5. **Constraints.** The constraint list any new feature must honor: the rules the encoded decisions and capabilities imply (a visibility gate every content surface obeys, a boundary no write may cross, a platform rule the build enforces). Each traces to the decision or capability that sets it. Where an encoded decision is a fact about what the product does, a constraint is the obligation it puts on the next feature. Example: "any surface that renders an item must obey the visibility gate" traces to the gate decision.

**What stays human.** The product's **purpose** (Step 3, the empty slot). This skill reads what the product does; it does not declare what it is for. A severity or a priority on any constraint, if one is wanted, is also the human's; this skill lists the constraints, it does not rank them.

## Step 3: Produce the Application Intent Map

Output the human map and the paired machine `intent-map.json` (validated against `schemas/intent-map.schema.json`, where `purpose` is `null` by construction). The purpose slot stays empty; the intent review is the named gate.

```
# Application Intent Map: [system]
Source manifest: [app-manifest.json ref]    Mapped: [date]

## ⛔ Purpose (NEEDS HUMAN)
This slot is intentionally empty and null in the machine map. What the product is FOR is a
product-strategy judgment; inferring it from the surfaces would launder a machine read into a
mission. The jobs, flows, decisions, vocabulary, and constraints below are read from the app;
the purpose is the human's to state.
   Purpose: ____________________

## Jobs (each evidence-linked, or marked assumption)
[Job stories, each traced to the surfaces that serve it.]

## Flows (each naming the manifest surface ids it moves through)
[The real paths across surfaces, with the trigger that advances each.]

## Encoded decisions (each evidence-linked to the manifest, or marked assumption)
[The decisions the product already makes in its behavior, a gate, a default, a deliberate absence.
 The layer a new feature collides with if it is not read first.]

## Vocabulary (the product's own terms, from its copy and routes)
[Term, the meaning the app gives it, the surface it appears on.]

## Constraints any new feature must honor (each traced to its decision or capability)
[The rules the encoded decisions and capabilities imply. Listed, not ranked.]

## Named gate
Intent review: ____________________  Date: ______
The purpose stays empty and no constraint is ranked until this line is signed by a human.
```

### A micro-example (calibration only)

A one-surface expense app, mapped from a small manifest, to show the register and the evidence discipline. The full worked example (the instance's own site) is in `references/worked-example.md`.

```
## ⛔ Purpose (NEEDS HUMAN; null in the machine map)

## Jobs
- When I incur a cost, I want to log it against a category, so the total stays current.
  evidence: surface_id = expenses

## Flows
- expenses → add-expense modal → expenses (updated total)   trigger: the add button
  evidence: surface_id = expenses

## Encoded decisions
- gate: an expense must carry a category; an uncategorised expense is rejected.
  evidence: json_pointer = #/components/schemas/Expense/required
- deliberate-absence: no bulk import; the copy says "add them as they happen."
  evidence: file_line = src/features/expenses/EmptyState.tsx:14

## Vocabulary
- category: a fixed bucket an expense is filed under (not a free-text tag).
  evidence: file_line = src/features/expenses/types.ts:8

## Constraints any new feature must honor (listed, not ranked)
- Any surface that creates an expense must require a category.   traces_to: the category gate
- No feature may add a bulk-import path without a product decision.   traces_to: the no-import absence

## Named gate (Intent review): __________  Date: ______
```

Every row points at a real anchor; the purpose is the one thing left blank.

## Step 4: Pre-flight verification

Confirm, before declaring done:

- `purpose` is null in the machine map and empty in the human map; the schema itself rejects a non-null purpose.
- Every job, flow, encoded decision, vocabulary term, and constraint carries an `evidence` reference or is marked `assumption`; no row is asserted from the shape of the app alone.
- No constraint is ranked or scored; the constraints are listed.
- The machine map validates against `schemas/intent-map.schema.json`.
- Prose rules hold: no standalone two-letter model abbreviation, zero em dashes, no banned words, no pricing; the `classification` frontmatter and the footer are present.

## How the map is used downstream

The Application Intent Map is read, not shelved. Three consumers use it, and naming them keeps the map honest about what it is for:

- **`intent-journey-map`** reads this map before mapping any one feature, so the feature's job story specializes a real product job, its journey respects the product's flows, and its prop-contract does not contradict an encoded decision. A per-feature map that violates a constraint here is not a new idea; it is a regression this layer would have caught.
- **`feature-increment`** (the Care unit) checks a proposed feature against the constraint list: a feature that adds a form to a no-form product, or changes a slug with no redirect, is flagged against the constraint it breaks before it is built.
- **The human's intent review** reads the jobs, encoded decisions, and constraints as the evidence base for the one call this skill will not make: what the product is for.

The map is a living artifact. On a later run, load the prior map (`scope="intent"`) and update the layers rather than restating them; a constraint the product has since dropped is retired with a note, not silently deleted.

## Common misreads this skill guards against

The failure modes are all the same shape: reading intent into the app that the app does not actually carry. Each is caught by the evidence rule and the empty purpose slot.

- **A framework default read as a product decision.** Not every default is deliberate; some are the framework's, not the team's. Record the default as observed, and let the human decide whether it was intended. Do not caption an accident as a decision.
- **The vocabulary tidied.** The product's own words are the data, even when they are awkward or overloaded. Renaming "account" to "profile" because it reads better loses the fact that the product calls it "account." Read the term the app uses.
- **A wished-for flow drawn as a real one.** A flow is a path the surfaces actually support. A path that would be nice, but requires a surface the manifest does not carry, is flagged, not drawn.
- **The purpose inferred from the surfaces.** The strongest pull is to look at what the app does and state what it is for. That is the one move this skill does not make; the layers are the evidence a human uses to state the purpose, not the purpose itself.
- **The constraints ranked.** Listing the constraints is the job; ordering them by importance is a priority call the skill has no charter to make.

---

## What is explicitly out of scope

- **Stating the product's purpose.** Null by construction (§ 9). The skill reads what the product does; the human says what it is for.
- **Ranking or scoring the constraints.** The skill lists them; prioritization is the human's.
- **Mapping one feature's journey and prop-contract**: `intent-journey-map`. **Reading the codebase into a manifest**: `app-recon`. **Auditing an opportunity tree**: `strategy-integrity-warden`. **A taxonomy or IA study**: `taxonomy-labeling-auditor` (deployed) and the area-2 IA skills.
- **Writing the prototype, the PRD, or the story.** This skill ends at the map.

---

## Exit Gate Required Headers (bottom-of-skill bracket)

This skill closes through the Exit Gate (`CLAUDE-SESSION-RULES.md § Exit Gate`). Before declaring done, confirm every required header holds real content:

- `## Fixes Applied` (or the delivered Application Intent Map plus its JSON)
- `## Smoke Test` (the Step 4 pre-flight checks, pasted)
- `## Next Session Prompt`

If `purpose` was filled, or any constraint ranked, the gate has **not** been satisfied.

---

*HeyHi Confidential. Sheerline area 9 (Design Strategy & Product Thinking), serves areas 1 and 2. Staged 2026-09-07 (Lane D, `plans/plan-sheerline-fdde-loop-2026-09-07.md`, DISPATCH-04). The application-level companion to `intent-journey-map`; it generalizes the one prior "intent-map how the product works" exercise (decision-log § 2026-07-16; `plans/plan-firm-of-one-os-architecture-diagrams-2026-07-15.md` § 2). Boundary: Sheerline § 9. Skeleton: `heyhi-skills/design-measurability-mapper/SKILL.md`.*
