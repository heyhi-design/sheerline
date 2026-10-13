---
classification: confidential
title: "Module 2.2 — The 13-area practice registry"
track: 2
module: "2.2"
level: intermediate
prereqs: ["2.1"]
est_minutes: 30
teaches: sheerline
opens_files:
  - sheerline/os/foundations/registry.yaml
  - sheerline/os/agent-context.md
---

# Module 2.2 — The 13-area practice registry

## You are here

You know Sheerline is a keel instance with one net-new slot. This module opens the map that slot organizes: the thirteen-area practice registry, how each area carries a coverage state, and why a tracked gap beats an invisible one. Previous: [`module-2-1.md`](module-2-1.md). Next: [`module-2-3.md`](module-2-3.md).

## Learning objectives

After this you can:

- Name the four coverage states and how many areas sit in each.
- Explain why the registry is flat and tagged rather than a two-tier tree.
- Say what "a gap is a tracked state" means and why it beats a silence.
- Classify one real area on all its tags and defend the coverage call.

## Concept

The design discipline is wider than any one practice is strong at. Sheerline names it as thirteen areas and holds them in a single flat, tagged registry, not a two-tier tree. Flat matters: every area is a peer, and the structure lives in the tags, not in a hierarchy that would imply some areas are sub-parts of others.

Each area carries three tags that decide how it behaves. **nature** is one of craft, operating, or conditional: eight craft areas (the making), four operating areas (strategy, business, facilitation, operations), and one conditional area (service design, relevant only to certain engagements). **coverage** is one of deep, covered, partial, or gap, and it measures design-practice capability, not the keel three layers. **phase** is the phase that governs or fills the area, so a thin area has a scheduled home rather than an open question.

Here is the governance thesis in one line: a gap is a *tracked state*, not an invisible absence. HeyHi's capability is deep but lopsided, strong in Visual and Design Systems and thin upstream in research and information architecture. Left unnamed, that lopsidedness is a silence a client discovers the hard way. Named with a coverage tag and a phase, it becomes a thing you can see and schedule. The registry converts an absence into an entry.

The Phase 1 coverage distribution is exact, and it is worth holding the numbers:

- **deep (2):** Visual Design (area 6) and Design Systems (area 7). Both carry a governed foundation and a strong skill cluster.
- **covered (1):** Wireframing and Prototyping (area 5), under governance and strong at high fidelity.
- **partial (6):** Content Design (3), Interaction Design (4), Accessibility (8), Design Strategy (9), Collaboration and Facilitation (11), and DesignOps (12). Each has some capability and a named shortfall.
- **gap (4):** User Research (1), Information Architecture (2), Business Acumen (10), and Service Design (13). Registered, phased, and honestly empty for now.

Two deep, one covered, six partial, four gap: thirteen areas, every one placed. Five of them ship in Phase 1 as first-class tracked-state stubs (User Research, Information Architecture, Accessibility, Business Acumen, Service Design), four of those flagged gap and Accessibility flagged partial-and-elevated because its mechanical floor is already enforced while its judged half is the tracked shortfall.

Two mechanisms fall out of the tags. Conditional loading: only active, governed areas ever enter a session, so the thirteen maintain routing and coverage-tracking rather than sitting in context. And the naming caution from module 0.2 gets its sharpest test here: Design Systems is area 7, one of thirteen, the most-built one. It is not Sheerline. Track 3 opens that area's quality loop; this module keeps it in its row.

Where the deep areas carry a foundation, that foundation is the subject of module 2.3. Where areas disagree about a value, the conflict order that resolves them is module 2.4.

## Walkthrough

Open `sheerline/os/foundations/registry.yaml`. Read the header comment defining the tag vocabulary (nature, coverage, elevated, phase, foundation, build_gate), then the `meta` block: thirteen areas, eight craft, four operating, one conditional, two deep manifests, one governance foundation, five stubs. Now read a single area entry end to end, say area 8 (Accessibility): notice it carries `coverage: partial`, `elevated: true`, a `phase`, a `foundation_path`, a `build_gate`, and a `grounding` line that defends the tag in prose.

Now open `sheerline/os/agent-context.md` and find the Craft / Operating / Conditional table. It is the same thirteen areas in a reading layout: the registry is the machine surface, the table is the human one.

## Lab

Classify one area and defend it. In `sheerline/os/foundations/registry.yaml`, pick any area and write its four facts: nature, coverage, phase, and whether it carries a foundation. Then defend the coverage tag by quoting its `grounding` line. Area 8 (Accessibility) is a good one to reason about: it is tagged partial and elevated, and its grounding explains why (the mechanical conformance floor is deep and enforced, but the judged half, does it work for an assistive-technology user, is the tracked shortfall).

**Success looks like:** one area stated on all four tags, with the coverage call defended by its own `grounding` line rather than by guess, and a sentence on why that area is not simply "done" or "missing."

## Common misreads

- *"The thirteen areas are a hierarchy."* No. It is a flat, tagged registry, not a two-tier tree. Every area is a peer; the tags carry the structure.
- *"A gap means the area is ignored."* No. A gap is a tracked state with a phase and a build gate. Governance makes the absence visible and scheduled instead of silent.
- *"Design Systems is the biggest area, so it is Sheerline."* No. It is area 7, one of thirteen, the most-built one. The naming caution holds hardest here.
- *"Coverage measures keel layers."* No. Coverage is design-practice depth (deep, covered, partial, gap), a different axis from the keel three-layer model.

## Self-check

1. Name the four coverage states and how many areas are in each.
2. Why flat-and-tagged rather than a two-tier tree?
3. What does "a gap is a tracked state" mean, and why does it beat a silence?
4. From the Lab: your area, its four tags, and the grounding that defends its coverage.

## Go deeper

- `sheerline/os/foundations/registry.yaml`: the thirteen areas with nature, coverage, phase, and foundation in full.
- `sheerline/os/agent-context.md`: the Craft / Operating / Conditional reading table.
- Architecture figure 3, [`../../docs/architecture.md`](../../docs/architecture.md), draws the registry with a coverage bar on every area.
- The foundations the deep areas carry are module 2.3; the conflict order that resolves disagreements between areas is module 2.4.

---

*HeyHi Confidential*
