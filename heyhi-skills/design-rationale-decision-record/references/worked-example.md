---
classification: confidential
title: "Worked example — a Mode B sweep and a Mode A supersede scaffold"
skill: design-rationale-decision-record
loaded_by: "SKILL.md Step 1 (calibration)"
---

# Worked example — decision-record keeper

Two filled goldens on **synthetic, invented** material. No client content; every thread, record, and name below is fabricated for calibration. Read them to anchor register and depth; do not copy their findings.

- **Part 1 — Mode B integrity sweep** exercises the v0.2.0 method: decision-verb heuristics, corpus-scoping, the coverage note, and the open-questions / near-misses surfaces. Every finding is a labeled candidate; nothing is adjudicated.
- **Part 2 — Mode A supersede scaffold** exercises the v0.2.0 variant: it links the predecessor, prompts "what changed," and leaves the new decision and rationale empty (the old "why" is not carried forward).

---

## Part 1 — Mode B integrity sweep (synthetic)

**The input (invented corpus):** a design team's `#design-system` and `#design-crit` Slack channels (Jan–Aug 2026) and an `adr/` folder of 22 records. The human asks: "did we ever actually record the grid decision, and is anything contradicting itself?"

```
# Decision Integrity Sweep — design-team decisions, Jan–Aug 2026 (SYNTHETIC)
Swept: #design-system + #design-crit (Jan–Aug 2026), adr/ folder (ADR-001…022)   Date: 2026-08-23

## Coverage note
Swept fully: the two named Slack channels over Jan–Aug 2026 and all 22 ADRs. NOT swept: Figma
comment threads, DMs, and the #general channel (out of scope for this pass). A "clean" region
below means nothing found in the swept scope — not that nothing exists in the unswept surfaces.

## Unrecorded (discussed, never recorded)
| Where discussed | Apparent decision | Settlement tell | Provenance |
|-----------------|-------------------|-----------------|------------|
| #design-system, Mar 4 | "ok we'll go with the 4-pt grid over 8-pt" | "we'll go with … over" | [candidate — needs confirmation] |
| #design-crit, May 19 | "final call: single-column forms everywhere" | "final call" | [candidate — needs confirmation] |

## Contradicted (recorded, then reversed without a superseding record)
| Record A | Record B / doc | The contradiction |
|----------|----------------|-------------------|
| ADR-012 (accepted, Mar): "primary CTA is filled" | #design-crit, Jun 30: "we're now using outline CTAs everywhere" | The June reversal has no superseding ADR; ADR-012 still reads `accepted`. [candidate — needs confirmation] |

## Stale / dangling
| Record | Issue |
|--------|-------|
| ADR-019 | Stuck in `proposed` since April (4 months); the feature it governs shipped in June. [candidate] |

All rows are agent-surfaced CANDIDATES — see provenance. None asserts what the team decided.

## Open questions for the team (questions, not judgments)
- Was the 4-pt grid actually decided on Mar 4, or was that thread still exploring?
- The Jun 30 outline-CTA message reverses ADR-012 — was that a real decision that needs a
  superseding record, or an in-the-moment comment?
- ADR-019 has been `proposed` since April but its feature shipped — was it accepted and never
  updated, or is it genuinely still open?

## Near-misses and unchecked territory (the sweep journey, made inspectable)
- Considered, not a decision: #design-system Feb 11 "if we killed the tour we'd simplify
  onboarding" — a hypothetical ("if we"), not a settlement. Not surfaced.
- Deduped: the 4-pt grid appears in three threads (Mar 4, Mar 6, Apr 2) — surfaced once, at
  the clearest (Mar 4); the others noted here.
- Not swept: Figma comments and DMs — a decision settled only there would be invisible to
  this pass.

## Named gate
Reviewer confirmation (which candidates are real): ____________________  Date: ______
```

---

## Part 2 — Mode A supersede scaffold (synthetic)

**The input (invented):** "ADR-012 said primary CTAs are filled. An accessibility audit found filled CTAs fail contrast on the new dark theme, so we're revisiting it. Driver: Priya. Approver: the design lead. Contributors: the a11y reviewer and two product designers."

```
# Decision Record — Primary CTA style on the dark theme (SYNTHETIC)
Status: superseding   Date: ______
Supersedes: ADR-012 "Primary CTA is filled" (accepted, Mar 2026) — linked, not rewritten;
            ADR-012 stays in history at status `superseded` once this record is accepted.

## DACI
Driver (owns getting to a decision):  Priya
Approver (makes the call — exactly one): design lead
Contributors (consulted):            a11y reviewer, 2 product designers
Informed (told after):               (to fill)
[DACI-completeness check result: PASS — one Driver, one Approver, Contributors listed]

## Context
[the situation forcing a decision — for the humans to fill]
What changed since the prior decision (ADR-012): [for the humans to fill — e.g. the
accessibility audit finding that surfaced the need to revisit; write it fresh]

## Options considered
1. ____________________
2. ____________________

## ⛔ Decision — NEEDS HUMAN
This slot is intentionally empty. The decision is the Approver's to make and record.
   Decision: ____________________

## ⛔ Rationale — NEEDS HUMAN
This slot is intentionally empty. Articulating *why* is the mechanism; the skill does
not write it for you. On this supersede record, the new "why" is written fresh — ADR-012's
rationale is NOT copied forward (if it still held unchanged, there would be nothing to supersede).
   Why: ____________________

## Consequences
[what this commits the team to — for the humans to fill]

## Open questions for the humans (to complete the record)
- Does this supersede only ADR-012, or also any related component-token decisions the CTA
  change touches?
- Which options were genuinely on the table (keep filled + fix contrast, switch to outline,
  theme-specific variants) versus named for completeness?

## Named gate
Approver sign-off: ____________________   Date: ______
No decision is recorded as accepted until the Approver signs.
```

---

## Why these are good goldens

- **The sweep proposes and steps back.** Every unrecorded/contradicted/stale item is a labeled candidate; the ADR-012-vs-June contradiction is surfaced as a *pair* with no ruling on which CTA style wins.
- **The coverage note earns its clean regions.** It says exactly what was and was not swept, so "nothing in Contradicted beyond this one" reads as "nothing in the swept scope," not "nothing anywhere."
- **The heuristics show their work.** Each unrecorded row cites the settlement tell that surfaced it; the near-misses show a hypothetical ("if we killed the tour…") correctly *not* surfaced, and a three-thread decision deduped to one.
- **The supersede scaffold links, it does not rewrite.** ADR-012 is named and left intact; the new decision, rationale, and "what changed" are empty for the humans, and the note makes explicit that the old rationale is not carried forward.

*HeyHi Confidential. Worked examples for `design-rationale-decision-record` v0.2.0. Fully synthetic; added 2026-08-23 (Wave D) per the 2026-08-22 skills audit § 4 (no worked examples) and § 2.4 / § 5.*
