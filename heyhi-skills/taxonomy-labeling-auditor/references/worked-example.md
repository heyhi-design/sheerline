---
classification: confidential
title: "Worked example — Taxonomy Audit (synthetic: an online learning platform)"
version: "0.1.1"
updated: "2026-10-07"
note: "SYNTHETIC input. No client content. Calibration only — read for register and depth of the free-prose surfaces; do not copy the findings."
---

# Worked example (synthetic) — "Learnly", an online learning platform

**Synthetic engagement. Invented product, no client content.** Read this to calibrate register and the depth of the open-questions and near-misses surfaces, and to see the vocabulary-provenance discipline in action. Do not copy its findings.

**The taxonomy the human brought (synthetic):** a top nav — `Courses`, `Resources`, `Community`, `Pricing`, `Settings` — where `Courses` is a single-parent tree by subject, `Resources` mixes docs + blog + templates + webinars, and account controls appear under both `Settings` and a separate `Preferences` panel. **User-vocabulary source provided:** a set of 40 support-ticket subject lines and 3 months of on-site search terms.

---

# Taxonomy Audit — Learnly top nav + course tree · audited [date]
Source: top nav (5 items) + Courses tree (subject-only) + account controls     User-vocabulary source: 40 support tickets + on-site search logs (cover every audited surface)     Owner: ____ (a content / IA owner — NOT YET NAMED)

## Label-consistency findings (each evidence-linked: label + location)

| Label | Location (node / path) | Finding | Vocabulary provenance |
|-------|------------------------|---------|-----------------------|
| "Settings" vs "Preferences" | top nav > Settings; account > Preferences | two labels for one concept (account controls split across both) | `user-vocab-sourced` — tickets say "settings" 9×, "preferences" 0× (prefer "Settings") |
| "Resources" | top nav > Resources | one label over four content types (docs, blog, templates, webinars) | `designer-coinage` — appears in 0 tickets / 0 searches |
| "Community" | top nav > Community | consistent, single concept | `user-vocab-sourced` — searched 14× |
| "Courses" | top nav > Courses | consistent | `user-vocab-sourced` — the top search term |

## Information-scent findings (node + path linked, never a vibe)

- **`Resources` (top nav) — weak scent.** Destination is a mixed bag (docs + blog + templates + webinars). A user searching for a template cannot predict it lives here; on-site search for "template" (22×) rarely clicks `Resources` first. First-click ambiguity with `Courses` (webinars read as courses).
- **`Courses` tree is subject-only — ambiguous scent for skill-level seekers.** Tickets show users ask for "beginner" courses (11×); the tree offers no difficulty facet, so scent for "where are the beginner courses" is absent.
- **`Settings` / `Preferences` split — misleading scent.** A user who changed a setting under one panel and looks for it under the other (support tickets: 6 "can't find where I changed X").

## Polyhierarchy + metadata review

- **Courses need polyhierarchy.** A "Python for Data Analysis" course belongs under both `Programming` and `Data` — the single-parent subject tree forces one home, and search logs show users reaching it from both. Fix is a **facet model** (subject + difficulty + format), not a deeper tree.
- **`Resources` is a metadata problem, not a nav item.** Its four content types want a `type` facet (doc / blog / template / webinar), reachable from context, rather than one weak-scent bucket.

## Draft machine-readability schema layer (CANDIDATE — answer-engine optimization is a separate pass, not part of this audit)

- Candidate content types: `Course` (fields: title, subject[], difficulty, format, instructor), `Article`, `Template`, `Webinar`, each a schema.org-shaped type; relationships: `Course —teaches→ Subject`, `Course —hasLevel→ Difficulty`. Labeled a candidate; hands to a separate answer-engine-optimization pass and to engineering for the JSON-LD implementation.

## Open questions for the team (questions, not label decisions)

- Is `Resources` one concept the team wants to keep, or four content types that belong in context? (Determines whether this is a scent fix or a nav removal.)
- Should the Courses facets be subject + difficulty + format, or is format ("webinar") really a separate content type? (Changes the schema above.)
- Do "Settings" and "Preferences" map to two real surfaces the team maintains separately, or one that drifted into two labels?

## Near-misses and unchecked territory (the audit journey, made inspectable)

- Considered, left: `Community` vs `Forum` read like a possible inconsistency, but tickets and search both use "community" — left as consistent, not a finding.
- Almost flagged: `Pricing` scent looked weak until search logs showed a direct, high-intent path to it — pulled back; the scent is fine for its audience.
- Could not check: whether "template" is how users say it in-product (the tickets use it; the in-app label was not in the artifact provided).

## ⛔ Label choices — NEEDS HUMAN
This slot is intentionally empty. The audit shows `Resources` is designer-coinage and `Settings` beats
`Preferences` in user vocabulary — but which word ships, and whether `Resources` is renamed or removed,
is a taxonomy decision the owner makes from the vocabulary evidence, not the skill.

## ⛔ Granularity — NEEDS HUMAN
   How deep the Courses tree goes, how many facets, whether webinars are a type or a format: ____________

## ⛔ Restructure stakes — NEEDS HUMAN
   Whether the `Resources` finding is worth a restructure or a small scent fix, and the severity: ____________

## Named gate
Taxonomy owner sign-off: ____________________  Date: ______
No label is chosen, no granularity set, and no restructure ordered until this line is signed.

---

*HeyHi Confidential. Synthetic worked example for `taxonomy-labeling-auditor`. No client content. Method canon: `sheerline/os/foundations/information-architecture/FOUNDATION.md`; recipe: `references/taxonomy-canon.md`.*
