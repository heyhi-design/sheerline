---
classification: confidential
title: "Intent-Journey Map, the pluggable domain-state band"
skill: intent-journey-map
version: "0.1.0"
---

# The pluggable domain-state band

The band spine (intent, journey, system-and-data, UI-and-component, prop-contract, acceptance) is fixed across every engagement. One band is not: the **domain-state band**, which records the state a particular product domain carries that a generic band cannot express. This file gives the slot, two generic illustrative fills, and the rule for writing a new one.

**The domain-state band is a pluggable slot the engagement supplies, not a human-judgment gate.** This template supplies the shape and two worked-generic examples so the fill is fast and honest; it does not decide which band a given engagement needs, and it carries no product-specific state model. Picking the band and its state model is the engagement's work (a small judgment, named in the map header as `Domain band in use: …`); once picked, the band is FILLED at run time, mechanically, from that model, exactly like the other bands. So the domain band never sits blank in the map's ⛔ human-gate section (that section is the research question, the severity calls, and the open decisions); it is filled, or it is skipped. A feature with no special domain state says so and skips the band; do not force a domain lane onto a plain flow.

The band sits between the journey band and the system-and-data band, and it runs at Tier 2 (the tier where a feature is complex or state-bearing enough to earn it). Each cell records only the parts of the state model that **change at that step**, not the whole model every column.

---

## Illustrative fill A, a map-state band (map-centric products)

For a product whose primary surface is a map, the domain state is a tuple of what the map is currently showing. Record only what changes at the step.

| Lane | What it holds |
|---|---|
| Viewport | Center, zoom or scale, rotation. The camera. |
| Basemap and imagery | The active base layer and any imagery overlay. |
| Layer visibility | The set of data layers currently on, and their draw order. |
| Selection | The selected feature or features, and the selection mode. |
| Active tool or mode | Pan, draw, measure, edit; the current interaction mode. |
| Inspector or popup | The open feature inspector or popup and its subject. |
| Filter or query | The active attribute filter or spatial query narrowing what is shown. |
| Edit dirty-state | Whether an in-progress geometry or attribute edit is unsaved. |

Example cell, for a step where the user opens a feature's details: *Selection = the tapped feature; Inspector = open on that feature; Viewport, basemap, layers, tool, filter unchanged.* The band records the delta, not the whole tuple.

This is a generic cartographic-UX state model. A real engagement replaces the lane names and values with its own map platform's terms and its own layer and tool vocabulary.

---

## Illustrative fill B, a document-state band (document and content products)

For a product whose primary surface is an editable document, the domain state is where the document is in its lifecycle and who is acting on it. Record only what changes at the step.

| Lane | What it holds |
|---|---|
| Lifecycle | draft, in-review, published, archived; the document's stage. |
| Revision | The current revision or version, and whether this step creates a new one. |
| Lock and ownership | Whether the document is locked, and by whom; edit versus read access. |
| Presence | Who else is viewing or editing at this step (collaboration state). |
| Dirty-state | Unsaved local changes versus persisted state. |
| Annotation | Open comments, suggestions, or track-changes relevant to the step. |
| Visibility gate | The rule that governs whether this document is publicly visible (a published flag, a scheduled date). |

Example cell, for a step where the author publishes: *Lifecycle = draft → published; Revision = a new immutable revision is written; Visibility gate = the published flag flips true; Presence, lock unchanged.* The band records the transition, not the whole model.

This is a generic document-lifecycle state model. A real engagement replaces the lanes with its own content model's terms (its own review states, its own visibility rules).

---

## Writing a new domain band (the rule)

When neither illustrative fill matches, write a new band from the domain's real state model. Four rules keep it honest and keep it a band rather than a second flow:

1. **One state model, named.** The band records one product domain's state (spatial, document, scheduling, financial-ledger, media-timeline). Name the model in the map header. Do not blend two.
2. **Ground it in the real model.** The lanes come from the application's actual state model, read through `app-recon` and the served context, not from a guess about how the domain "usually" works. A lane the code does not carry is not a lane.
3. **Delta per step, not the whole model per column.** Each cell records only what changes at that step. A band that repeats the full tuple every column is noise.
4. **It is state, not sequence.** The journey band already carries the sequence. The domain band carries the state that sequence moves through. If a lane is really a step, it belongs in the journey band.

A feature that crosses two domains (a document shown on a map) picks the primary domain's band and notes the second domain's state in the system-and-data band, rather than running two domain bands. If the second domain genuinely carries load-bearing state, that is an open decision for the human, not a silent second band.

---

*HeyHi Confidential. `intent-journey-map` domain-band template v0.1.0. The two fills are generic illustrations; every real domain band is engagement knowledge the engagement supplies.*
