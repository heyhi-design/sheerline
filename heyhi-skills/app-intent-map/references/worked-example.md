---
classification: confidential
title: "Application Intent Map, worked example (the instance's own site)"
skill: app-intent-map
version: "0.1.0"
substrate: heyhi.design (the instance's own site; no client)
---

# Worked example, heyhi.design (the instance's own site)

Run on HeyHi's own site (`heyhi-website/`), so no client content appears. Built from a hand-written manifest in the `app-manifest.json` shape (§ 3.3), because Lane C (`app-recon`) runs in parallel and its real manifest is not yet available. The point of the example is to show the five layers evidence-linked to real file and line anchors, and the `purpose` slot left empty. Every row below points at a real anchor in the site source; a reader can open each and check it.

Hand-written manifest surfaces used: `home` (`/`), `log-index` (`/log/`), `log-entry` (`/log/$slug`), `lab` (`/lab`), `hermetic-seal` (`/resources/hermetic-seal`). The paired machine map is `worked-example.intent-map.json` beside this reference; it validates against `schemas/intent-map.schema.json`, with `purpose` null.

## ⛔ Purpose, NEEDS HUMAN

Empty by construction, and null in the machine map. The site reads as a writing presence, but whether its purpose is a reading home, a top-of-relationship surface, or a portfolio is a product-strategy call the human states. The layers below read what the site does; they do not declare what it is for.

## Jobs (each evidence-linked)

| Job | Surfaces | Evidence |
|---|---|---|
| *When I hear about HeyHi, I want to read its writing, so I can judge the thinking.* | `log-index`, `log-entry` | surface_id: log-index |
| *When I land on the site, I want to see what HeyHi is, so I can decide if it is for me.* | `home` | surface_id: home |
| *When something resonates, I want to follow new writing, so I do not have to check back.* | `home`, external subscribe | file_line: src/components/Contact.tsx:70 |
| *When I want to see the work, not read about it, I want to explore the interactive lab.* | `lab` | surface_id: lab |

## Flows

| Flow | Surface ids (in order) | Trigger | Evidence |
|---|---|---|---|
| Arrive and read | home → log-index → log-entry | a title on the index | surface_id: log-index |
| Arrive and explore | home → lab | the lab entry point | surface_id: lab |
| Read then follow | log-entry → home (Contact section) → subscribe (external) | the subscribe link in home's Contact section | file_line: src/components/Contact.tsx:70 |

## Encoded decisions (the layer a new feature collides with)

| Decision | Kind | Evidence |
|---|---|---|
| An entry is publicly visible only when its `published` flag is exactly `true`; file existence never equals visibility. | gate | file_line: src/data/logs.ts:29 |
| The gate is strict: any value other than the literal `true` (including the string `"True"`) keeps the entry hidden. | gate | file_line: src/data/logs.ts:27 |
| The site takes no lead capture: a direct email and a subscribe link, no form. It is a place to read, not a funnel. | deliberate-absence | file_line: src/components/Contact.tsx:7 |
| A published slug is stable; changing it requires a 301 redirect in `vercel.json`. | gate | file_line: src/data/logs.ts:6 |
| The frontmatter parser avoids `eval` and `new Function` so the production bundle is CSP-safe. | deliberate-absence | file_line: src/data/logs.ts:38 |

## Vocabulary (the product's own terms)

| Term | Meaning the app gives it | Evidence |
|---|---|---|
| Log | The site's writing index and its entries. | surface_id: log-index |
| Lab | The interactive experiments surface, distinct from the Log. | surface_id: lab |
| entry | A Log post, typed `essay` or `observation`. | file_line: src/data/logs.ts:14 |
| defensibilityTier | An internal `T1`–`T5` tag carried on an entry. | file_line: src/data/logs.ts:19 |
| hermetic seal | A named resource surface on the site. | surface_id: hermetic-seal |

## Constraints any new feature must honor (listed, not ranked)

| Constraint | Traces to | Evidence |
|---|---|---|
| Any surface that lists or renders an entry must obey the `published === true` visibility gate. | the publication gate | file_line: src/data/logs.ts:29 |
| A new feature must not add a lead-capture form to the site; the no-funnel posture is deliberate. | the no-capture decision | file_line: src/components/Contact.tsx:7 |
| A feature that changes a published slug must ship a 301 in `vercel.json`. | the slug-stability default | file_line: src/data/logs.ts:6 |
| No feature may introduce `eval` or `new Function` into the production bundle. | the CSP-safe decision | file_line: src/data/logs.ts:38 |

## Named gate

Intent review: ____________________  Date: ______

The purpose stays empty and no constraint is ranked until this line is signed.

---

*HeyHi Confidential. `app-intent-map` worked example v0.1.0, the instance's own site (heyhi.design). Every row is evidence-linked to a real file:line; the paired machine map validates against `schemas/intent-map.schema.json` with `purpose` null.*
