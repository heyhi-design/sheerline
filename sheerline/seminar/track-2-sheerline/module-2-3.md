---
classification: confidential
title: "Module 2.3 — The foundations slot: reference, never copy"
track: 2
module: "2.3"
level: intermediate
prereqs: ["2.2"]
est_minutes: 30
teaches: sheerline
opens_files:
  - sheerline/os/foundations/visual-design/FOUNDATION.md
  - sheerline/os/foundations/design-systems/FOUNDATION.md
  - ai-services/design-intelligence/style-reference-library.md
---

# Module 2.3 — The foundations slot: reference, never copy

## You are here

The registry told you which areas are deep. This module opens what a deep area actually carries: a foundation, the one net-new structural slot Sheerline adds to keel, and the single rule that keeps it honest. Previous: [`module-2-2.md`](module-2-2.md). Next: [`module-2-4.md`](module-2-4.md).

## Learning objectives

After this you can:

- Say what a foundation is, the two things it does, and the one thing it never does.
- Explain the byte-copy trap and why a referenced corpus beats a copied one.
- Describe how the design-systems subsystem is reached, and which invariant governs that.
- Trace a deep foundation's pointer table to the real corpus file it names.

## Concept

The one structural slot Sheerline adds to keel is `os/foundations/<practice-area>/`. A foundation lives there for each governed area, and it is a *governance manifest*, not new capability. It does two things: it registers the area's existing skills, and it points at HeyHi's existing design corpus. It authors zero net-new skills, and it copies nothing.

That last clause is the whole module. The rule is **reference, never copy.** A foundation is a pointer table plus loading rules. It names the real path of each corpus file and leaves the file where it lives. It does not pull the corpus into `sheerline/`.

The reason is a failure mode worth naming, because it looks harmless. Call it the **byte-copy trap**: a duplicated corpus silently drifts from its source. Suppose a foundation copied the style library into its own folder to be self-contained. The copy reads fine on the day it is made. Then someone updates the real style library, and now there are two authoritative-looking versions that disagree, and nobody notices which one an agent read. A referenced corpus cannot drift, because there is only one of it. The foundation points; the source stays single. This is the same discipline you met as keel's backend-free memory seam in module 1.5 and as "retrieve, do not paste": the value stays at one address, and everything else references that address.

A deep foundation has a recognizable shape. It opens with a pointer table titled roughly "what this foundation references, in place, never copied," listing corpus files by their real repo paths. It carries a second table pointing at the fundamentals reasoning layer, the ratified conflict order and universal design laws, which are likewise referenced and not re-authored. And it states four-class loading rules: nothing loads always, the manifest loads conditionally when the area is the active one, a specific corpus file loads on-demand, and the design system's own data stays searchable through the retrieval boundary.

The Design Systems foundation carries the rule one step further, and it is the sharpest instance. Its subsystem, the Design System MCP with its evaluator and corrections registry, is reached *through the MCP as a boundary tool*: nested and referenced, never embedded as token files inside `sheerline/`. That is the fourth invariant from module 0.3, protocols at boundaries, made concrete. The design system is a thing you retrieve across a boundary, not a pile of files you paste into the tree. Track 3 opens that subsystem; here it matters only as the reference that a foundation points at rather than absorbs.

Briefly, two design terms this module leans on. The *corpus* is HeyHi's existing body of design-intelligence material: the curated style library, the anti-tells that make generated work read as generated, the research on where taste stops being a token. *Tokens* are the design system's named values (a specific color, a spacing step) that emitted output uses instead of a raw hex code. A foundation governs how those are reached; it never becomes a second copy of them.

## Walkthrough

Open `sheerline/os/foundations/visual-design/FOUNDATION.md`. Read the line stating it never byte-copies the corpus into `sheerline/`, and the parenthetical naming the byte-identical-copy trap. Then read the pointer table "what this foundation references (in place, never copied)": six corpus files, each at an `ai-services/design-intelligence/` path, none of them inside the foundation folder.

Now open `sheerline/os/foundations/design-systems/FOUNDATION.md` and read "the nested subsystem, reached through the MCP boundary". Notice the exact claim: the quality loop is referenced, never embedded as token files inside the tree, on the fourth invariant. Both foundations then state the same four-class loading rules, which is the reference rule expressed as when-to-load.

## Lab

Trace one pointer to its source. In `sheerline/os/foundations/visual-design/FOUNDATION.md`, read the "what this foundation references" table and pick one row, for example `ai-services/design-intelligence/style-reference-library.md`. Open that path and confirm the file is real and lives under `ai-services/`, not duplicated inside the foundation folder. Then state, in one sentence, what would go wrong if the foundation held a copy of it instead of a pointer.

**Success looks like:** one corpus path named from the table, confirmed to open at its real `ai-services/` location (and absent from `sheerline/os/foundations/visual-design/`), plus a one-line statement of the drift the byte-copy trap would cause.

## Common misreads

- *"A foundation holds the corpus."* No. It holds pointers to the corpus. The files stay at their real paths; the foundation references them in place.
- *"Copying the corpus in would be safer because it is self-contained."* No. That is the byte-copy trap: the copy drifts from its source, and two authoritative-looking versions are worse than one referenced one.
- *"The design-systems foundation embeds the MCP."* No. The subsystem is reached through the MCP as a boundary tool, nested and referenced, never embedded as token files inside the tree.
- *"A foundation is new capability."* No. It is a governance manifest: it registers existing skills and points at existing corpus, and authors zero net-new skills.

## Self-check

1. What two things does a foundation do, and what does it never do?
2. What is the byte-copy trap, and why is a referenced corpus safer than a copied one?
3. How is the design-systems subsystem reached, and which invariant governs that?
4. From the Lab: one corpus path a foundation points at, and where the file actually lives.

## Go deeper

- `sheerline/os/foundations/visual-design/FOUNDATION.md`: the pointer table and the byte-copy-trap rule.
- `sheerline/os/foundations/design-systems/FOUNDATION.md`: the nested subsystem reached through the MCP boundary.
- Architecture figure 2, [`../../docs/architecture.md`](../../docs/architecture.md), draws the foundations slot sitting between the Configuration layer and the owned line.
- The fundamentals reasoning layer these foundations point at is module 2.4; the design-systems subsystem itself is Track 3.

---

*HeyHi Confidential*
