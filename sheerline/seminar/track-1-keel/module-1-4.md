---
classification: confidential
title: "Module 1.4 — Corrections: compounding memory"
track: 1
module: "1.4"
level: foundational
prereqs: ["1.3"]
est_minutes: 30
teaches: keel
opens_files:
  - releases/open-source/keel/os/corrections/LIFECYCLE.md
  - releases/open-source/keel/os/corrections/seed-corrections.yaml
  - releases/open-source/keel/examples/baseline-year/os/corrections/corrections-registry.yaml
---

# Module 1.4 — Corrections: compounding memory

## You are here

Module 1.3 named an always-loaded, active-only mechanism in the abstract. This is that mechanism in full: the corrections registry, the part of keel that turns a repeated mistake into a rule the agent loads before the mistake can happen again. Previous: [`module-1-3.md`](module-1-3.md). Next: [`module-1-5.md`](module-1-5.md).

## Learning objectives

After this you can:

- Read a correction entry and say what each field carries.
- Distinguish a factual correction from a behavioral one, and say why it matters later.
- Name the three statuses, the promotion threshold, and the three close-out steps.
- Trace a real correction from its first fire to a promoted rule.

## Concept

This is the clearest instance of the compounding you met in the harness thesis. A mistake caught once is a note; the same mistake caught a third time is a pattern worth encoding so no future session pays for it again.

A correction is a small structured entry. The fields that carry the weight are `trigger_context` (the situation that should make an agent reach for this correction), `correction` (what to do instead), `pattern` (the failure it prevents), and three bookkeeping fields: `times_fired`, `last_fired`, and `status`. Two classifying fields sit on top. `category` groups the kind of work it touches. `severity` marks whether the pattern is a factual error, a claim you could check and find wrong, or a behavioral one, a way of working that goes wrong. That distinction looks cosmetic here and becomes load-bearing in Track 3, where the two are handled differently: a factual correction is safe to enforce, while a behavioral one is a reminder a human still has to weigh.

A correction is always in exactly one of three statuses. **active**: in force, loaded at session start, honored. **superseded**: a stronger mechanism now covers this pattern, usually a hard rule you promoted, so the entry stays for provenance but no longer loads as guidance and carries a `superseded_by` pointer to the rule that replaced it. **retired**: the pattern no longer applies because the tool or workflow is gone, kept for the record, not loaded. The word not on that list is *promoted*. Promotion is an action, not a status. When a correction fires often enough to earn a permanent rule, you promote it (write the rule into your session rules or operating principles) and then mark the original entry superseded.

Promotion has a threshold worth stating as a default: five or more total fires, or the same pattern across three or more separate sessions. The first is a lifetime count, not a rolling window, so `times_fired` is a floor on how many sessions the pattern has already cost you. When either trigger fires, the soft note is no longer doing its job, so you make it a hard rule, and you close it out in one pass, all three steps together, so the registry never lies: write the new rule into its permanent home, set the original entry's status to superseded with a `superseded_by` pointer, and recompute the registry's `meta` counts. A correction left active after its rule shipped keeps firing on something already enforced, and the signal degrades. A promoted-but-not-superseded entry is the classic source of registry rot.

The last property is the one that keeps the whole thing trustworthy: the registry is curated, not auto-generated. An agent may observe a recurring pattern and propose a correction, but a human decides what enters the registry and what gets promoted. Unreviewed entries never reach agent context, because the registry's value depends entirely on its trustworthiness. The moment it holds noise, agents learn to ignore it, and a registry that gets ignored has no compounding left in it. This is the human-in-the-loop from module 0.3, made operational at the level of the firm's memory.

## Walkthrough

Open `releases/open-source/keel/os/corrections/LIFECYCLE.md`. Read "The three statuses", "Promotion thresholds", and "The close-out protocol". Notice the note that promoted is an action, not a status, and that the close-out is three steps in one pass. Then read "The human standard" at the end: the registry is curated, and unreviewed entries must never reach agent context.

Now open `releases/open-source/keel/os/corrections/seed-corrections.yaml`, the five framework-level patterns a new instance starts with. Read one active entry and one superseded entry, and notice the shape. The superseded ones point at a Verify-Before-Claim rule, meaning they load as history once you adopt that rule and as active guidance until you do. The `meta` block at the top counts three active and two superseded, which is the counting discipline the close-out protocol keeps honest.

## Lab

Trace one correction through its whole life. Open `releases/open-source/keel/examples/baseline-year/os/corrections/corrections-registry.yaml`, the filled registry of the worked instance: four entries, one superseded. Find the superseded entry, `report-drafted-over-untraced-inventory`. Read its `times_fired` count, its `superseded_by` pointer, and the date on it. Then reconstruct the chain the pointer describes: the pattern fired three times, its third fire met the promotion threshold's second trigger (the same pattern across three separate sessions), and on that date its rule was written into the always-loaded constraints and the entry was marked superseded. The other three entries are all still active and below the threshold, which the file's own header calls the normal state.

**Success looks like:** you can name the superseded entry, state its fire count, name the trigger it met, and say where its rule now lives, all read from the entry itself rather than guessed.

## Common misreads

- *"Every mistake becomes a correction."* No. A one-off is a note; a correction earns its entry only after the pattern recurs. The bar the baseline-year header states is at least twice, and a registry that logs every stumble stops being read.
- *"Promoted is a status."* No. Promoted is an action. The status after promotion is superseded, with a `superseded_by` pointer to the rule.
- *"The agent maintains the registry."* No. An agent may propose; a human curates. Unreviewed entries never load, because trust is the registry's whole value.
- *"A superseded entry is dead weight."* No. It stays for provenance: it records that a pattern existed and where its rule went, which is exactly what a future reader needs.

## Self-check

1. What do `trigger_context`, `correction`, and `times_fired` each hold in an entry?
2. Name the three statuses; which word is not a status, and what is it instead?
3. State the promotion threshold and the three close-out steps done in one pass.
4. From the Lab: the superseded baseline-year entry, its fire count, the trigger it met, and where its rule lives.

## Go deeper

- `releases/open-source/keel/os/corrections/LIFECYCLE.md`: statuses, thresholds, the close-out, and the human standard in full.
- `releases/open-source/keel/os/corrections/seed-corrections.yaml`: the five framework seeds a new instance starts from.
- `releases/open-source/keel/docs/architecture.md`, figure 4, draws corrections as one of the three loops that make session ten more reliable than session one.
- The factual-versus-behavioral distinction becomes load-bearing in Track 3, where the two severities are handled differently.

---

*HeyHi Confidential*
