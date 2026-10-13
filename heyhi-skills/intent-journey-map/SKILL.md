---
name: intent-journey-map
description: >-
  Map a feature's intent and journey BEFORE a prototype exists, and carry that
  map forward as a bound contract so the prototype translates into real
  components whose props match the application's own API schema. Runs the
  mechanical work: a three-tier cost gate with a real off-ramp, a fixed band
  spine (intent; journey; system and data; UI and component; a 14-column
  prop-contract bound by JSON pointer to the application's OpenAPI; Given / When
  / Then acceptance), one pluggable domain-state band per engagement, a
  bind-do-not-guess rule that FLAGS any prop whose schema field is absent, and a
  mandatory adversarial over-claim pass at Tier 2. Produces a human Intent-Journey
  Map and a paired machine contract. Triggers: "map the intent of this feature",
  "intent and journey map", "intent-journey map", "map this feature before the
  prototype", "build the prop contract for this feature", "bind these props to
  the API". The research question behind the feature, the theme and severity
  calls, and every named-owner open decision ship EMPTY behind a named human
  gate; the domain-state band is a pluggable slot the engagement supplies (its
  choice and state model), filled mechanically at run time like the other bands.
  NOT for planning a user study or a usability
  test (use research-plan-author). NOT for auditing an opportunity tree, JTBD, or
  prioritization artifact (use strategy-integrity-warden). NOT for the
  product-level jobs/flows/decisions layer above surfaces (use app-intent-map).
  NOT a taxonomy or information-architecture study (taxonomy and labeling audits are `taxonomy-labeling-auditor`, a deployed area-2 skill; the structure-design IA skills stay D-3-gated). NOT
  for reading the codebase into a manifest (use app-recon), and it writes no
  prototype, PRD, or story.
version: "0.1.0"
updated: "2026-09-07"
status: "deployed 2026-09-07 (Sheerline fdde-loop convergence pass 1, DISPATCH-06; promoted from skill-updates/intent-journey-map/). Sheerline area 9 (Design Strategy & Product Thinking); serves_areas hints to 1 (User Research) and 2 (Information Architecture), registered nowhere before D-3 (plan § 5 D11). Lane D of the Sheerline forward-deployed loop (plans/plan-sheerline-fdde-loop-2026-09-07.md, DISPATCH-04). Method ported from a proven-once next-door protocol (method only, no engagement data); the fixed spine plus one pluggable domain band is the generalization."
review_by: "2026-09-21"
classification: confidential
---

# Intent-Journey Map

**Sheerline area 9 (Design Strategy & Product Thinking) · serves areas 1 and 2 · read + structure skill.** A team is about to design a feature. Before a prototype exists, this skill frames the feature's intent, walks its journey, and records for each screen state the component that renders it, the props it takes, and the API schema field each data prop binds to. It closes two gaps that a prototype alone leaves open: the design-to-code gap (a mockup that never says which reusable component renders each state) and the design-to-API gap (a mockup that invents data shapes the API does not serve). The output is one artifact, the Intent-Journey Map, plus its paired machine contract, which the prototype and the engineering story are then built against.

**The boundary this skill obeys (Sheerline § 9, absolute).** A structured artifact with explicit empty judgment slots, a named human gate, and provenance labels on anything synthetic. *The research question behind the feature, the theme and severity calls, and every named-owner open decision are the empty judgment slots.* (The domain-state band is a different thing: a pluggable slot the engagement supplies and the run fills mechanically, not a ruling withheld from the map. See Step 3a.) Laying out the bands, binding each data prop to the schema, and flagging a prop whose field is absent is mechanical. Deciding what the feature is for, whether a pattern is real, how much a friction matters, and which open question resolves which way is judgment. A version of this skill that answers its own open decisions, sets a severity, or asserts a field is real when the sources do not support it has exceeded its charter. Binding is not guessing: a field the spec does not carry is flagged, never invented.

> **This skill closes through the Exit Gate (`CLAUDE-SESSION-RULES.md § Exit Gate`).** See the bottom-of-skill bracket.

---

## Routing between sibling skills

| If the task is… | Use |
|---|---|
| "Map the intent and journey of this feature, and bind its props to the API" (per feature, before the build) | **this skill** |
| The product-level layer above surfaces (jobs, flows, the decisions the product already encodes, vocabulary, constraints) | `app-intent-map` |
| Reading the repository into a grounded `app-manifest.json` (surfaces, components, endpoints, capabilities) | `app-recon` |
| Planning a user study, a usability test, or a sample size | `research-plan-author` |
| Auditing an opportunity tree / JTBD / prioritization artifact's reasoning | `strategy-integrity-warden` |
| Auditing or structuring a taxonomy, labels, or navigation | `taxonomy-labeling-auditor` (area 2, deployed, for taxonomy/labeling; the structure-design IA skills stay D-3-gated) |
| Answering "what is this feature for," setting a severity, or resolving an open decision | **the human** (this skill's named gate) |

The seam with `app-intent-map` is altitude: that skill reads the whole application's intent once; this skill maps one feature down to its bound props. The seam with `app-recon` is direction: recon reads the code into a manifest; this reads the manifest into intent and a contract. This skill consumes a manifest; it never produces one.

## Inherited invariants (cited by path, not restated)

This skill sits under the Sheerline area-9 governance manifest (`sheerline/os/foundations/design-strategy/FOUNDATION.md`) and inherits the always-loaded guardrails authored once in `sheerline/os/operating-principles.md`:

- **What stays human** (`operating-principles.md` § What stays human) names direction selection and severity-as-truth; the research question and the theme-and-severity calls are those, so they are the empty slots here.
- **Scoring is advisory, never a gate** (`operating-principles.md` § the taste-and-critique boundary): a friction observation informs; the map never sets a severity that blocks.
- **The empathy boundary** (`operating-principles.md` § The empathy boundary) governs the intent band: a job story is inferred, and an inferred motivation is labeled as such, never presented as a user's lived account.

This skill is not a taxonomy or information-architecture study skill (that is `taxonomy-labeling-auditor` and the other area-2 skills); it maps a feature's intent and contract, it does not author a taxonomy. The routing table and the `not_for` clauses say so.

---

## Step 0: Improvement hook check

Retrieve any recurring corrections for intent-mapping or contract work (`retrieve_design_corrections`, or the Sheerline `os/corrections/` registry). Fold a match into the pass. Skip silently if none.

## Step 1: The tier check (the off-ramp), run this first

Most changes do not need this protocol. Choose the tier deliberately: deeper maps cost more now and save wrong-prototype and wrong-prop review cycles later.

| Tier | When | What runs |
|---|---|---|
| **Tier 0 (skip)** | A single control or a copy change on one existing state, with no data write, no auth or entitlement change, and no cross-surface boundary crossing (a button label, one tooltip, one empty-state line) | Skip this protocol. Make the change directly, or route the copy to the states-writer. No map. |
| **Tier 1 (light)** | One job, one surface, no data write, no boundary crossing (a settings reflow, a single-view edit form) | The intent, journey, UI-and-component, and acceptance bands only. Skip the system-and-data, prop-contract, and domain bands unless a load-bearing decision needs one. Ground through `app-recon` at its light tier. |
| **Tier 2 (full)** | Multiple steps, or the change writes data, or it crosses a persona or surface boundary, or it introduces a new reusable component | All bands. Build the prop-contract. Ground the system-and-data and component bands through `app-recon` at its full tier. Run the adversarial pass (Step 5). |

**The precedence rule (binding).** A change that writes data, changes auth or entitlement, or crosses an architecture boundary is Tier 2 regardless of how few controls it touches. Size never demotes a data-writing change. The prop-contract band and the schema grounding fire only at Tier 2.

**The tier is a candidate the human confirms.** State the tier and the one-line reason. When the precedence rule does not settle it (a borderline single-write, an ambiguous boundary), name it as an open decision and leave the choice to the human rather than picking silently. `⛔ Tier when the precedence rule does not decide it (NEEDS HUMAN).`

Worked tier calls: renaming a button label is Tier 0 (skip). A settings panel that reflows existing controls and writes nothing is Tier 1. A one-field form that saves a note is Tier 2 (it writes data; control count does not demote it). A multi-step wizard that only reads is Tier 2 by its step count. A single toggle that flips an entitlement is Tier 2 by the precedence rule, not its one control.

## Step 2: Load context

1. **The feature brief** the human brought (a one-pager, a ticket, a definition note). This is what gets mapped. The **research question behind it** (what are we actually trying to learn or serve) is an empty slot the human fills; this skill records the brief's stated framing, it does not invent the question.
2. **The application manifest**, through `retrieve_application_context(query, scope="manifest")` when the per-system instance serves it, falling back to a passed `app-manifest.json` file path only for the manifest itself. Read the surfaces, the components used with their props, the endpoints as OpenAPI pointers, and the capabilities. Do not re-read the codebase here; `app-recon` already did.
3. **The served design-system context**, through `retrieve_design_context` and `retrieve_design_relationships` for component names, atomic levels, token names, and the `uses_component` / `contains_component` relations. Never load a token file, a brand config, or a component manifest from disk as the spec; the instance is the boundary (plan § 3.2).
4. **The application's OpenAPI**, as the binding target for the prop-contract, resolved by the JSON pointers the manifest's endpoints carry. This is the application's own contract, read as a pointer target, never as this skill's design spec. Where the application carries no OpenAPI, Step 4 handles it honestly (a typed data module or an external endpoint is bound by source, and the absence is recorded, never papered over).

## Step 3: Walk the bands (the fixed spine)

Columns are journey steps in narrative order, each headed by a job story. The spine is fixed; one domain band is pluggable (Step 3a). Not every band runs at every tier (Step 1).

1. **Frame the job or jobs as job stories.** One line each: *When [situation], I want to [motivation], so I can [outcome].* The situation carries the real context the feature runs in. Specialize the job to the engagement; the job-story starter set is engagement knowledge that lives in the domain band template, not here. Do not invent a persona goal where a concrete job fits.
2. **Lay the backbone.** Put the journey steps in narrative order; each step becomes a column. The walking skeleton is the thinnest path that completes the job.
3. **Intent band (why).** Per step: the job story, and the persona-and-surface note (which user, which surface, which viewport).
4. **Journey band (sequence).** Per step: the stage label, the one concrete user action (a single task-analysis leaf), and the emotion / friction / opportunity note. **The severity of a friction and whether an opportunity is real are theme-and-severity calls that stay human** (`⛔`); record the observation, not the ruling.
5. **System-and-data band (Tier 2; the backend bridge).** Per step where the user action crosses the line of visibility: the service or endpoint that fires, the entities and fields read or written, and a frontstage / backstage marker so the front-end and back-end handoff is explicit. Ground every name through `app-recon`; a name not in the manifest is marked `unverified`, never asserted.
6. **UI-and-component band (on-glass; feeds the prototype).** Per step: the specific screen or component and its state (empty, loading, filled, success, error), the served-library component that renders it plus its atomic level (or `NEW:` with a proposed name when nothing existing fits), and the layer (container, meaning data-connected, or presentational).
7. **Acceptance band (verify; all tiers, the Tier 1 minimum's last band).** Per step: the Given/When/Then, the checkable pre-state, trigger, and post-state. These become the engineering acceptance criteria and the prototype and story assertions, so no step is complete without them. A step whose post-state cannot be stated as a checkable assertion is a step whose intent is not yet settled: surface that, do not paper over it.

### Step 3a: The pluggable domain-state band

Between the journey band and the system band sits **one** domain-state band, chosen per engagement, that records the state a particular product domain carries and a generic band cannot. A map-centric product carries a viewport-and-layers state; a document product carries a draft-and-revision state; a scheduling product carries a calendar-and-availability state. The band is a slot, not a fixed lane: pick the one the engagement needs, fill it from that domain's real state model, and say so in the map header. **The domain-state band is a pluggable slot the engagement supplies**, not one of the human-judgment gates below: the skill ships its shape and two illustrative fills, the engagement supplies which band and its real state model, and the band is then filled at run time (mechanically, grounded through `app-recon`, exactly like the other bands). What is the engagement's here is the pluggability (which band, whose state model), not a ruling withheld from the map. Two generic illustrative fills (a map-state band and a document-state band), and the rule for writing a new one, live in `references/domain-band-template.md`.

Choosing the band is a small judgment, and it is the engagement's, not this skill's. The test is simple: what state does the sequence in the journey band move *through* that a generic loading / filled / error state does not capture? That is the domain. Ground its lanes in the application's real state model, read through `app-recon` and the served context, not a guess about how the domain "usually" works. Record only the delta at each step, not the whole state tuple in every column. A feature with no special domain state says so and skips the band; do not force a domain lane onto a plain flow, and a feature that spans two domains picks the primary one and notes the second in the system-and-data band rather than running two domain bands.

## Step 4: Build the prop-contract (Tier 2): bind, do not guess

The prop-contract is the machine half of the map: one row per data prop, the 14 columns of `references/method.md` (§ The prop-contract), emitted as the paired `*-ijm-contract.json` validated against `schemas/ijm-contract.schema.json`. The enforceable core is the binding: each data prop's schema-field column is a JSON pointer into the application's OpenAPI, resolved and checked.

- **Bind each data prop to the real contract.** Resolve the `json_pointer` against the supplied OpenAPI. A pointer that resolves sets `binding_status: bound` and carries the schema's `required`, `enum`, and type across.
- **Flag, never invent.** A pointer that does not resolve (a field the spec does not carry) sets `binding_status: flagged-absent` and is surfaced as a finding, never silently kept and never filled with a guessed shape. A field the human asserts but the sources do not support is `assumption`, labeled as such.
- **Honest handling when there is no owned spec.** An application with no OpenAPI binds each data prop to its real source instead (a typed data module by file and symbol, or a named external endpoint) and sets `binding_status: no-spec`, recording that no owned contract exists to bind against. This is the truthful state, not a gap to hide.
- **Enum equals the token or variant set.** Where a prop's enum drives a design-token role or a component variant set, the contract asserts the enum equals that set; a divergence is a finding for the human.

A feature is design-complete when every step has the intent, journey, UI-and-component, and acceptance bands, and every data prop in the contract has a source and a schema field that is either bound or explicitly flagged.

## Step 5: The adversarial over-claim pass (Tier 2, mandatory)

Before the map is final, one adversarial reading checks the map and the contract against the manifest and the OpenAPI for any over-claim: a field, endpoint, component, or capability asserted as real that the sources do not support. The full checklist lives in `references/method.md` (§ The adversarial over-claim pass); the six checks in brief:

1. Every endpoint named in band 3 or the contract resolves in the manifest or the OpenAPI, else `unverified`.
2. Every `binding_status: bound` row actually resolves at its `json_pointer` (re-resolve each; a stale pointer is re-flagged).
3. Every component named is a served-library component or explicitly `NEW:`, else `unverified`.
4. Every implied capability (a write, a role gate, an offline path) traces to the manifest's `capabilities`, else `assumption`.
5. Every enum-equality claim is checked against both sides; a divergence is a finding, not a silent match.
6. No screen state claims to be shown that the sources do not evidence; an inferred state is labeled inferred.

Every over-claim is corrected to the source or re-labeled `unverified` / `assumption`, and the pass produces a short note of what was checked and corrected. **This pass finds over-claims; it does not decide whether the feature is worth building.** That judgment is the human's.

## Step 6: Produce the Intent-Journey Map

Output the human map (the bands as a lane model, columns as steps) and the paired machine contract. The judgment slots stay empty by construction; the open-decisions block carries questions with a named owner each, never answers.

```
# Intent-Journey Map: [feature name]
Source: [brief]    Mapped: [date]    Tier: [0 / 1 / 2, with the one-line reason]
Architecture target: [as stated in the brief or the manifest]
Domain band in use: [the chosen band, or "none, plain flow"]

## The lane model
[Columns are journey steps in narrative order. Rows are the bands from Step 3 (+ 3a at Tier 2):
 intent · journey · domain-state (if any) · system-and-data (Tier 2) · UI-and-component · acceptance.
 Each UI-and-component cell names the served-library component + atomic level, or NEW: name.]

## Given / When / Then acceptance (per step)
[The checkable pre-state, trigger, and post-state for each step. These become the engineering
 acceptance criteria and the prototype and story assertions.]

## Prop-contract  →  [feature]-ijm-contract.json
[One row per data prop, the 14 columns. Every data prop bound (json_pointer resolves) or flagged.
 Emitted as the paired machine contract; validated against schemas/ijm-contract.schema.json.]

## Opportunities and observed friction (observations, not rulings)
[The friction and opportunity notes from the journey band, as observations. Severity is not set here.]

## ⛔ Research question behind the feature (NEEDS HUMAN)
This slot is intentionally empty. What the team is actually trying to learn or serve is a
product judgment, not a mechanical one. The brief's stated framing is recorded above; the
question is the human's to lock.
   Research question: ____________________

## ⛔ Theme and severity calls (NEEDS HUMAN)
   Which observed frictions are real, and how much each matters: ____________________

## ⛔ Open decisions (NEEDS HUMAN, each carries a named owner)
[Every decision the map surfaced and could not settle, one per line, with the owner named.
 The tier when the precedence rule did not decide it belongs here.]
   - [decision], owner: ____________________

## Named gate
Contract review by the engineering owner: ____________________  Date: ______
The prop-contract is a proposal until this line is signed. No open decision is resolved,
no severity is set, and no unverified field is promoted to real, by this skill.
```

**The two outputs, and why both.** The human map is the lane model a designer and an engineer read together to agree on what the feature is and does. The machine contract is the subset a codegen or a contract test can enforce: it is what makes "bind, do not guess" checkable rather than aspirational. The map without the contract drifts from the API; the contract without the map loses the intent the props serve. Both ship, or neither is done.

### A micro-example (calibration only)

One step of a Tier 2 feature, to show the band shape and one contract row. The full worked example (the instance's own site) is in `references/worked-example.md`.

```
Step: "Save a note"
  Intent:      When I finish a thought, I want to save it, so it is not lost.  (user, desktop, editor surface)
  Journey:     stage: commit · action: press Save · friction: is a slow save legible? (observation, severity is the human's)
  System/data: POST /notes  ·  writes Note{id, body}  ·  backstage
  UI/component: NoteEditor (container), states: filled → loading → success / error
  Acceptance:  Given a non-empty body, When Save is pressed, Then the note persists and a success state shows;
               Given an empty body, Then Save is disabled.

Contract row (one of several):
  prop: body · role: data · type: string · source: {hook: useCreateNote, endpoint: POST /notes}
  json_pointer: #/components/schemas/Note/properties/body · binding_status: bound
  required: true · empty_or_error_state: "inline 'note not saved' on failure; the draft is kept"
```

The `binding_status: bound` says the pointer resolved; a `body` the schema did not carry would read `flagged-absent` and become a finding, never a guessed type.

## Step 7: Pre-flight verification

Confirm, before declaring done:

- The tier is stated with its reason; a borderline tier is an open decision, not a silent pick.
- Every system-and-data name traces to the manifest or is marked `unverified`; nothing is asserted from memory.
- Every data prop in the contract is `bound`, `flagged-absent`, `no-spec`, or `assumption`, never a silent guess; the machine contract validates against `schemas/ijm-contract.schema.json`.
- At Tier 2, the adversarial pass ran and every over-claim was corrected or re-labeled.
- The research-question, theme-and-severity, and open-decisions slots are empty; the named gate is unsigned; each open decision carries an owner.
- Prose rules hold: no standalone two-letter model abbreviation, zero em dashes, no banned words, no pricing; the `classification` frontmatter and the footer are present.

## How the map feeds downstream

The Intent-Journey Map is built to be consumed, not filed. Three consumers read it, and naming them keeps the map honest about its job:

- **The prototype build** (`ui-studio` for client work, `heyhi-ui-ux` for HeyHi) reads the UI-and-component band and the acceptance band: the states to build and the assertions each must satisfy. A prototype that renders a state the map did not name, or skips one it did, has drifted from the agreed intent.
- **`feature-increment`** (the Care unit) reads the whole map and its contract as the single source for a three-way build (Figma, prototype, repo) and a coverage table: every contract row must appear in all three, or it is a finding. The map is what makes that coverage checkable.
- **The engineering owner's contract review** (the named gate) reads the prop-contract to confirm every binding is real before code is written against it.

The map is a living artifact. When the feature changes, update the affected bands and re-resolve the contract rather than restating the whole map; a binding the API has since changed is re-flagged, not left stale.

Because all three consumers read the same map, the map is where a disagreement surfaces early and cheaply: an engineer who reads a `flagged-absent` binding, a designer who reads a `NEW:` component the library lacks, and a reviewer who reads an unsigned open decision are all looking at the same artifact, before any code is written. That is the return the tier-2 cost buys.

---

## What is explicitly out of scope

- **Answering the open decisions, setting a severity, or locking the research question.** Empty by construction (§ 9). The map surfaces the decisions and their owners; the humans decide.
- **Inventing a schema field.** Bind or flag; never guess. A field the spec does not carry is a finding.
- **Writing the prototype, the PRD, or the engineering story.** This skill ends at the map plus its contract; those consume it. Building the prototype is `ui-studio` (client) or `heyhi-ui-ux` (HeyHi); the story is downstream.
- **Reading the codebase into a manifest**: `app-recon`. **The product-level intent layer**: `app-intent-map`. **Planning a study**: `research-plan-author`. **Auditing an opportunity tree**: `strategy-integrity-warden`. **A taxonomy or IA study**: `taxonomy-labeling-auditor` (deployed) and the area-2 IA skills.

---

## Exit Gate Required Headers (bottom-of-skill bracket)

This skill closes through the Exit Gate (`CLAUDE-SESSION-RULES.md § Exit Gate`). Before declaring done, confirm every required header holds real content:

- `## Fixes Applied` (or the delivered Intent-Journey Map plus its contract)
- `## Smoke Test` (the Step 7 pre-flight checks, pasted)
- `## Next Session Prompt`

If any open decision was answered, any severity set, or any unverified field promoted to real, the gate has **not** been satisfied.

---

*HeyHi Confidential. Sheerline area 9 (Design Strategy & Product Thinking), serves areas 1 and 2. Staged 2026-09-07 (Lane D, `plans/plan-sheerline-fdde-loop-2026-09-07.md`, DISPATCH-04). Method ported from a proven-once next-door intent-and-journey-mapping protocol as portable methodology only (the fixed spine, the tier gate, bind-do-not-guess, the paired output, the named-owner decisions, the adversarial pass); the domain band, the job-story set, and every stack binding are engagement knowledge the engagement fills. Boundary: Sheerline § 9. Skeleton: `heyhi-skills/design-measurability-mapper/SKILL.md`.*
