---
classification: confidential
title: "Module 1.3 — The registry engine and the confidence gate"
track: 1
module: "1.3"
level: foundational
prereqs: ["1.2"]
est_minutes: 30
teaches: keel
opens_files:
  - releases/open-source/keel/skills/registry/README.md
  - releases/open-source/keel/skills/registry/skill-registry.py
  - releases/open-source/keel/skills/registry/skill-registry.template.yaml
---

# Module 1.3 — The registry engine and the confidence gate

## You are here

Module 1.2 left the skills in the searchable class: retrievable from a registry, never pre-loaded. This module opens that registry and shows the mechanism that makes "load only what the task needs" work at forty skills instead of five. Previous: [`module-1-2.md`](module-1-2.md). Next: [`module-1-4.md`](module-1-4.md).

## Learning objectives

After this you can:

- Name the two registry files and what each one does.
- Explain why positive scoring alone cannot separate two similar skills, and what fixes it.
- Name the three confidence labels and the right action for each.
- Run the search against the starter skills and read a confidence verdict.

## Concept

The registry is two files. One is the index, `releases/open-source/keel/skills/registry/skill-registry.template.yaml`: one entry per capability, describing what each skill is for. The other is the search over that index, `releases/open-source/keel/skills/registry/skill-registry.py`: it takes a plain-language query and returns the few capabilities most likely to serve it. You describe the task, the search returns a short list, and only those load. This matters more the more skills you own. Five fit in a session's context without anyone noticing; forty do not, and the failure is the quiet one from module 1.2, the context filling with procedures the task never touches.

Each entry carries a small schema. The fields worth knowing now are `description` and `semantic_tags` (matched against the query), `trigger_patterns` (exact phrases that fire at the highest weight), `dependencies` (files co-loaded when the skill is chosen), `load_cost_tokens` (roughly character count over four), and `not_for`.

`not_for` is the field that earns its keep, and it is subtle enough to teach on its own. Two skills that sound alike collide: an invoice drafter and an invoice auditor share almost all their vocabulary, and positive scoring cannot separate them, because there is nothing to separate on. `not_for` carries negative weight. It says what a skill is not for, and steers a matching query toward the skill the clause names instead. The trap, which the registry README states plainly, is that a `not_for` clause can read as perfectly correct English and do nothing. The penalty fires only under specific matching conditions, and a clause that never meets them looks identical to a working one until you measure it. The lesson generalizes past this one field: correct-looking wording is not evidence a rule fires. You verify by measurement, swapping the clause in and out and reading the scores.

Every number that shapes a routing decision, the scoring weights, the `not_for` penalty, and the confidence thresholds, is a named constant in one `TUNING` block at the top of the search script, and nowhere else. The test suite enforces that the docstrings cite those constants by name rather than restating their values, because a number written into prose goes stale the first time someone re-tunes the code, and it goes stale silently. The values ship as generic starting defaults, not calibrated numbers. The right ones depend on how many skills you have and how you write your triggers, so you tune them against a small set of your own known query-to-skill cases.

The payoff is the confidence gate, and the third of its three answers is the point of the whole mechanism. Ask the search how sure it is, and it classifies the result three ways. **confident**: the top result pulls clearly ahead, so load it and go. **ambiguous**: two candidates are close enough that the search should not be the one choosing, so it surfaces both and asks you. **insufficient**: nothing cleared the floor, so it says so rather than loading the least-bad guess. A registry that answers "insufficient" honestly is more useful than one that always returns something, because the wrong skill loaded confidently is worse than no skill at all: it looks like an answer. That is Earn the Room as a mechanism. A skill earns its way into context by clearing a bar, and when nothing clears it, nothing loads.

## Walkthrough

Open `releases/open-source/keel/skills/registry/README.md`. Read "The two files" and "The per-entry schema" so you know what each entry declares. Then read the section on `not_for` and the paragraph under it about a clause that reads as correct and does nothing: that is the most important passage in the file, and its three-step verification (run the host skill's own triggers back through the search, run the queries the clause should redirect, and never lead the clause with the skill's most common word) is a procedure worth keeping.

Now open `releases/open-source/keel/skills/registry/skill-registry.py` and find the `TUNING` block at the top. Notice that every weight, the penalty, and the three thresholds are named constants in that one place. That single-location discipline is what lets you re-tune routing without hunting through the file. Then open `releases/open-source/keel/skills/registry/skill-registry.template.yaml` and read one entry end to end, so the schema stops being abstract.

## Lab

Run the search against the five starter skills the template ships with. From `releases/open-source/keel/skills/registry/`, after the one-time install the README lists, run a routing query:

```
python3 skill-registry.py --registry skill-registry.template.yaml "draft a proposal"
```

then ask the search how sure it is on a different query:

```
python3 skill-registry.py --registry skill-registry.template.yaml "where are we" --confidence
```

Read both verdicts. The first returns a skill; the second returns a confidence label in front of one. Then reason about the third label: describe a query you would expect to return `insufficient`, and say why returning nothing is the right behavior there.

**Success looks like:** one query that routes to a named skill, one `--confidence` run that reports `confident` in front of a skill, and a one-sentence account of when the gate should answer `insufficient` and why that beats loading the least-bad guess.

## Common misreads

- *"The registry runs the skill."* No. It finds the skill and reports which to load; loading and running happen after. It is a router, not an executor.
- *"A correct-sounding `not_for` clause works."* Not necessarily. The penalty fires only under specific matching conditions, so a clause can be grammatically right and inert. Verify by measurement, not by re-reading.
- *"insufficient is the search failing."* No. It is the search working: nothing cleared the floor, so it declines rather than loading the least-bad guess.
- *"More skills means slower routing."* No. More skills is exactly when routing pays off; the savings compound with the count, which is why the stats report climbs from the starter set upward.

## Self-check

1. What are the two registry files, and what does each do?
2. Why can positive scoring alone fail to separate two similar skills, and what field fixes it?
3. Name the three confidence labels and the right action for each.
4. From the Lab: your `confident` verdict, and one query you would expect to return `insufficient`.

## Go deeper

- `releases/open-source/keel/skills/registry/README.md`: the schema, the `not_for` trap, tuning, and the confidence gate in full.
- `releases/open-source/keel/skills/registry/skill-registry.py`: the `TUNING` block and the search itself.
- `releases/open-source/keel/docs/architecture.md`, figure 3, draws the confidence gate as the routing step of a session.
- The gate is Earn the Room from module 0.3 in mechanism form; corrections in module 1.4 are the other always-loaded, active-only mechanism.

---

*HeyHi Confidential*
