---
classification: confidential
title: "Application Intent Map, method reference"
skill: app-intent-map
version: "0.1.0"
---

# Application Intent Map, method reference

The method the SKILL.md routes to. It reads an application manifest and derives five layers above the surfaces, each evidence-linked, leaving one slot (`purpose`) empty for the human. The SKILL.md names the boundary; this reference is the derivation.

The shape generalizes the one prior "intent-map how the product works" exercise (`plans/plan-firm-of-one-os-architecture-diagrams-2026-07-15.md` § 2, decision-log § 2026-07-16): read what the product is, name the layer-models it runs on, name the recursions and the decisions it encodes, and keep the honesty guards on every caption. That exercise was never codified; this is the codification.

---

## The evidence rule (the spine of the method)

Every row this skill writes carries an `evidence` reference, or it is marked an `assumption`. There is no third option. A claim about what the product does that neither points at the manifest nor admits it is a guess is not written.

An `evidence` reference is one of:

- **`surface_id`**, a surface id in the manifest (`surfaces[].id`).
- **`file_line`**, a file and line the manifest already carries (a `copy[]` row's `file` and `line`, a `components_used[]` provenance).
- **`json_pointer`**, a JSON pointer into the application's OpenAPI (for an endpoint-encoded decision or capability).
- **`assumption`**, the explicit label for a row the sources do not support. An assumption is allowed; an unlabeled guess is not.

The manifest's own `unverified[]` list carries forward: a claim the recon could not ground stays `unverified` here, never promoted to evidenced because it reached a second document.

---

## The five layers

### 1. Jobs

The jobs the product serves, one job story each: *When [situation], I want to [motivation], so I can [outcome].* Each job traces to the surfaces that serve it (`surface_id` evidence). Derive jobs from what the surfaces let a user do, not from a persona goal imagined for them. A job with no surface that serves it is either an assumption (label it) or not a real job of this product.

### 2. Flows

The paths that connect surfaces. Each flow names the manifest `surface_id`s it moves through, in order, and the trigger that advances each step. A flow is a real path the app supports (evidenced by the surfaces and their routes), not a wished-for journey. A flow that requires a surface the manifest does not carry is flagged, not drawn.

### 3. Encoded decisions

The highest-value layer: the decisions the product already makes in its own behavior. Three kinds:

- **A gate it enforces** (a visibility rule, an auth check, an entitlement).
- **A default it sets** (an ordering, a pre-selected mode, a fallback).
- **A deliberate absence** (a thing it pointedly does not do, evidenced by copy or structure that says so).

Each is evidence-linked to the surface, file and line, or capability that encodes it. This is the layer a new feature collides with if it is not read first: a feature that violates an encoded decision is not a new idea, it is a regression the intent map would have caught.

### 4. Vocabulary

The terms the product uses in its own copy and structure, each with the meaning the app gives it (not a dictionary meaning) and the surface it appears on. Read the vocabulary from the manifest's `copy[]` and routes; do not rename the product's terms to tidier ones. A term the product overloads (one word, two meanings across surfaces) is worth flagging as its own row.

### 5. Constraints any new feature must honor

The rules the encoded decisions and capabilities imply. Where an encoded decision is a fact about what the product does, a constraint is the obligation it puts on the next feature: *every content surface obeys the visibility gate; no write may cross this boundary; the build enforces this platform rule.* Each constraint traces to the decision or capability that sets it. The constraints are **listed, not ranked**: which matters most is a human judgment, and a ranked list would read as a priority the skill has no charter to set.

---

## The purpose boundary (the empty slot)

`purpose` is null by construction, in the machine map and empty in the human map. The five layers read what the product *does*; the purpose is what it is *for*, and stating it is a product-strategy judgment. Inferring it from the surfaces would launder a machine's read of the app into a mission statement the team never wrote. The schema enforces this: a non-null `purpose` fails validation. Name the slot, hand it to the human at the intent-review gate, and stop.

The honesty guards from the prior exercise apply to every caption: staged is not shipped; a design property is not a realized capability; portability rests on cross-deployment evidence, not on one worked example. Where the map reads a decision that is aspirational rather than enforced, it says so.

---

## Reuses (owned elsewhere; not restated here)

- **The manifest:** `app-recon` produces it; this skill consumes it through `retrieve_application_context` (or a passed file path for the manifest itself). This skill does not re-read the codebase.
- **A prior intent map:** loaded through `retrieve_application_context(scope="intent")` when the instance serves it, and updated rather than restated; skipped when the served context is not present (there is nothing to update against). The tool is served by this arc's serving lane; until it lands, the manifest arrives by file path and this read is skipped.
- **The served design system:** component and token names come through the per-system instance, never a disk file.

---

*HeyHi Confidential. `app-intent-map` method reference v0.1.0. Reads the manifest, derives five evidence-linked layers, leaves `purpose` for the human.*
