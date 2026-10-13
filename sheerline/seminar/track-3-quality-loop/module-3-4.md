---
classification: confidential
title: "Module 3.4 — LEARN: the corrections registry"
track: 3
module: "3.4"
level: advanced
prereqs: ["3.3"]
est_minutes: 30
teaches: sheerline
opens_files:
  - heyhi-mcp/heyhi_mcp/corrections/__init__.py
  - heyhi-mcp/heyhi_mcp/corrections/predicates.py
  - heyhi-mcp/heyhi_mcp/corrections/schema.yaml
  - heyhi-mcp/heyhi_mcp/tools/corrections.py
---

# Module 3.4 — LEARN: the corrections registry

## You are here

The loop so far runs forward: retrieve the system, validate the output, grade it over time. LEARN closes it. This module opens the design corrections registry, the part that turns a caught mistake into something all three earlier verbs read, so the next session starts ahead of the last. It closes Track 3. Previous: [`module-3-3.md`](module-3-3.md). Next: Track 4, which takes a learner to subject-matter expert (authored in the seminar's dispatch batch).

## Learning objectives

After this you can:

- Name the one registry and its four readers, and the slice each one pulls.
- Distinguish a factual correction from a behavioral one, and say what each is allowed to do.
- Explain how a correction becomes a deterministic validation rule and a graded sub-check.
- Say why the registry is vendored, and where the live one resolves versus the bundled seeds.

## Concept

You met corrections at the keel level in module [1.4](../track-1-keel/module-1-4.md): a repeated mistake encoded once so no future session pays for it again, carrying a factual-versus-behavioral distinction that looked cosmetic there. This is where that distinction becomes load-bearing, exactly as 1.4 promised. The design corrections registry is one curated file read by four consumers, each pulling only the slice it can act on, and that is the whole idea: a correction captured once is read by every verb of the loop.

The four readers serve the loop's three earlier verbs, with the grade fed by two of them. **Retrieval:** active corrections fold into the always-loaded summary, and the fifth tool answers the query-time question, what have we been told about this token or component. **Validation:** a correction that carries a machine-checkable predicate becomes a rule, so an emitted-CSS predicate runs through the conformance lane from 3.2, a class-present or class-absent predicate runs in `heyhi-mcp/heyhi_mcp/corrections/predicates.py` against the markup, and a manifest predicate checks the self-reported artifact through `validate_output`. **Grading:** a recurring drift becomes a weighted sub-check in the evaluator series from 3.3. **Eval-seeding:** each correction ships a known-bad and expected pair, join-ready for the graded known-bad set, a real observed drift rather than a synthetic one.

Now the line that governs all four, and the reason 1.4 pointed forward to here. Only factual corrections are injected or enforced. A behavioral correction, a judgment about how the agent should work, is captured and surfaced to a human as a reminder to decide; it is never injected as a directive and never promotable to an auto-enforced rule. The reader layer honors this at every surface: the always-loaded fold lists factual corrections as apply-these and behavioral ones as a-human-decides, the query tool tags each returned correction with its enforceability, and the predicate evaluator refuses to run any correction whose severity is not factual. A taste correction hardening into an enforced check is the automation boundary collapsing, the same don't-automate line from module [0.3](../track-0-orientation/module-0-3.md) and the grades-inform-never-gate rule from 3.3, now defended at the level of the firm's memory.

Two more properties keep the mechanism honest. The registry is vendored, neither reimplemented nor depended on as a package: it reuses HeyHi's already-public corrections tool, several hundred lines of hard-won edge-case handling, instead of growing a second copy that could drift. And it resolves in one of two places. The live per-design-system registry sits beside the token file in the operator's data dir and is never bundled; the default install and the tests fall back to the bundled generic seeds, the practice running the loop on its own harness. A design correction adds five optional fields over a base entry, a detection axis (deterministic, judged, or hybrid), a scoring dimension, the token or component it is about, the predicate, and the known-bad and expected pair, and each of those fields is the hook a different reader pulls on. A correction carrying none of them is still a valid plain entry.

This is the compounding from the harness thesis in module 0.1, specialized to design and wired into the whole loop. Session ten is more reliable than session one because a correction it would have needed is already folded into the retrieval it opens with.

## Walkthrough

Open `heyhi-mcp/heyhi_mcp/corrections/__init__.py` and read the module docstring: one registry, four readers, each pulling its slice, and the resolution rule (live beside the tokens, otherwise the bundled seeds). Read `active_corrections` and `enforceable_corrections` and notice that enforceable is factual-only. Open `heyhi-mcp/heyhi_mcp/corrections/predicates.py`: a class-present or class-absent correction becomes a deterministic rule by dispatching to `check_class` in the conformance lane, and the evaluator returns nothing for any correction whose severity is not factual. Open `heyhi-mcp/heyhi_mcp/corrections/schema.yaml` and read the design-extension section: the five optional fields, and the note that the severity enum is not extended while the design taxonomy lives in the free-text `category`. Finally open `heyhi-mcp/heyhi_mcp/tools/corrections.py` and see the query-time reader tag each returned correction with its enforceability.

## Lab

Open `heyhi-mcp/heyhi_mcp/corrections/__init__.py` and read the four-reader docstring. Take one factual correction that carries a predicate and a known-bad and expected pair, and trace it through all four readers, naming the slice each pulls. Then take a behavioral correction and say where it stops.

**Success looks like:** for the factual correction you can name reader (a) folding it into the summary and answering the query tool, (b) running its predicate as a rule through the conformance lane or the class evaluator, (c) turning the recurring drift into a weighted eval sub-check, and (d) shipping its known-bad and expected pair to the graded known-bad set; and you can state that a behavioral correction reaches only reader (a), as a human reminder, and is never enforced or promoted.

## Common misreads

- *"Every correction can become an enforced rule."* No. Only factual corrections inject or enforce. A behavioral one is a human reminder, never promotable.
- *"The four readers are four registries."* No. One curated registry, four consumers, each reading the slice it can act on.
- *"The corrections engine was built here."* No. It is vendored from HeyHi's public corrections tool, neither reimplemented nor depended on as a package.
- *"The bundled seeds are HeyHi's real corpus."* No. The seeds are generic, brand-free, and publishable; the live per-design-system registry is a separate file beside the tokens, never bundled.

## Self-check

1. Name the one registry and its four readers, and the slice each pulls.
2. What is a factual correction allowed to do that a behavioral one is not?
3. How does a correction become a deterministic validation rule, and how does it seed the grade?
4. From the Lab: your factual correction traced through all four readers, and where the behavioral one stops.

## Go deeper

- `heyhi-mcp/heyhi_mcp/corrections/__init__.py`: one registry, four readers, and the resolution rule.
- `heyhi-mcp/heyhi_mcp/corrections/predicates.py`: how a class predicate becomes a deterministic rule.
- `heyhi-mcp/heyhi_mcp/corrections/schema.yaml`: the design-extension fields the four readers pull on.
- `heyhi-mcp/heyhi_mcp/tools/corrections.py`: the query-time reader and its enforceability tag.
- Architecture figure 4, [`../../docs/architecture.md`](../../docs/architecture.md), draws LEARN folding back into the next retrieval.
- Corrections at the keel level are module [1.4](../track-1-keel/module-1-4.md); the factual-versus-behavioral line the base tool lacks is the design layer's addition. The retained moat, the populated corpus itself, is Track 4.1.

---

*HeyHi Confidential*
