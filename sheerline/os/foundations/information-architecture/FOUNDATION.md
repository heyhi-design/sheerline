---
classification: confidential
title: "Foundation: Information Architecture (area 2, COVERED / filled / governed practice)"
area: 2
nature: craft
coverage: covered
phase: P3
kind: governance
status: filled
---

# Foundation: Information Architecture (area 2)

**Coverage: COVERED. Filled (P3 foundation fill, after the User Research foundation in dependency order) and now carrying a deployed skill.** Information Architecture presupposes User Research: labels and taxonomy are sourced from *real user vocabulary*, which research supplies. This foundation is second in the spine and points at the UR foundation; an IA skill that invents labels without the UR vocabulary source has skipped the spine. Coverage moved `gap → partial` at the fill, then `partial → covered` when the D-3 offering opened on a client-engagement pull and `taxonomy-labeling-auditor` (the most durable IA value; the `heyhi-aeo` machine-readability schema seam) was built and deployed. The other three IA skills (`ia-study-designer`, `findability-audit`, `intent-taxonomist`) stay held / unbuilt (they build on an engagement pull).

IA's buyer is the least like the practice's proven buyer, which is exactly why the remaining skills are gated on a real engagement pull; a deep capability gap is not a market gap.

## What already exists (do not re-stub as absent)

- `ui-studio` touches layout **without IA discipline** — the gap this foundation fills, not a duplicate. IA is not the layout it produces; it is the structure underneath.
- `heyhi-aeo` owns the **answer-engine optimization** the foundation's machine-readability layer *hands off to*, not duplicates. The seam is bounded below (§ the answer-engine-era layer) and enforced by `taxonomy-labeling-auditor`'s `not_for`: this area authors and audits the taxonomy and its schema layer; `heyhi-aeo` optimizes for citation.

## Points at the invariant, does not restate it

Cited by path, re-derived nowhere ([`os/operating-principles.md`](../../operating-principles.md)):

- **What stays human** (`operating-principles.md` § What stays human) — the final structure, taxonomy and label decisions, the restructure verdict. The canonical list lives there.
- **The cross-quality conflict-resolution order** (`operating-principles.md` § The cross-quality conflict-resolution order, which points at A.1) — how a structure decision resolves against accessibility and the design system when they disagree.
- **The empathy boundary** (`operating-principles.md` § The empathy boundary) — where IA leans on UR synthesis for the user vocabulary its labels come from, the same boundary applies: inferred user language is inferred, labeled as such.
- **Scoring is advisory, never a gate** (`operating-principles.md` § the taste-and-critique boundary) — a findability severity informs; it never blocks.

## The judged layer (what stays human)

Empty slots behind a named gate on every IA skill:

- the final **structure**;
- **resolving dendrogram conflicts** (card-sort clusters routinely contain practical conflicts only design resolves — the read is judgment, not output);
- **label choices** and **granularity**;
- the **restructure decision**;
- the **severity** of a findability defect.

## The knowledge canon (authored here)

| Topic | The canon (authored here) |
|---|---|
| **The three IA models** | IA ≠ navigation; the organization schemes (LATCH and kin — Location, Alphabet, Time, Category, Hierarchy). Structure is not the nav bar. |
| **Card-sorting standards** | The binding rule: **dendrogram interpretation is judgment**, not output — clusters carry practical conflicts only design resolves. Open / closed / hybrid sort selection is scaffolded; the read stays human. |
| **Tree-testing** | Card sort *designs* the structure; tree test *validates* it. The pairing, and when each applies. |
| **Labeling + taxonomy from real user vocabulary** | The **User Research dependency** made concrete: labels come from participant language, not designer coinage. Polyhierarchy, metadata, information scent. |
| **The answer-engine-era layer** | Searchable → machine-ready: structured content as the source answer engines cite. The **`heyhi-aeo` seam**, named and bounded — this area authors and audits the taxonomy and its schema layer; `heyhi-aeo` optimizes for citation. |
| **Intent modeling** | Search and agentic intent taxonomies; routing, disambiguation, fallback. (Self-referential: Sheerline's own routing *is* an intent taxonomy.) |
| **Findability heuristics** | Orphan / dead-end / weak scent; first-click; depth vs. breadth. **Every claim evidence-linked** — a findability finding names the node and the path, never a vibe. |

## Registered skills (area 2)

**`taxonomy-labeling-auditor` is DEPLOYED** (D-3 open on a client-engagement pull); the other three stay held on an engagement pull. Gate tiers: [`plans/plan-sheerline-p3-ur-ia-foundations-2026-08-29.md`](../../../../plans/plan-sheerline-p3-ur-ia-foundations-2026-08-29.md) § 1.2.

| Skill | Class | Gate tier | Judgment that stays human |
|---|---|---|---|
| `taxonomy-labeling-auditor` | N (most durable IA value) | **DEPLOYED** (`heyhi-skills/taxonomy-labeling-auditor/`, v0.1.0, D-3 open); the `heyhi-aeo` schema seam is the differentiator | label choices; granularity; stakes |
| `ia-study-designer` | N | Tier 3 — held on pull | final structure; resolve dendrogram conflicts; restructure verdict |
| `findability-audit` | X (audit family) | Tier 3 — held on pull (highest-collision — do not build first) | severity; restructure decision |
| `intent-taxonomist` | N (optional — a bet) | Tier 3 — D-3 (the deferrable first-mover bet) | what is a distinct intent; granularity; routing stakes |

`heyhi-figjam-mapper` (area 11) already serves this area's diagram generation (IA sitemaps) from the facilitation layer; it is not an IA study skill and does not register here.

---

*Area map: [`os/foundations/registry.yaml`](../registry.yaml) · Depends on: [`os/foundations/user-research/FOUNDATION.md`](../user-research/FOUNDATION.md) (the vocabulary source) · Always-loaded invariants: [`os/operating-principles.md`](../../operating-principles.md) · Spec source: [`plans/plan-sheerline-p3-ur-ia-foundations-2026-08-29.md`](../../../../plans/plan-sheerline-p3-ur-ia-foundations-2026-08-29.md) · Research of record: `ai-services/design-intelligence/research/sheerline-skill-buildout-research-2026-08-09.md` § 3.2 / § 7b*

*HeyHi Confidential*
