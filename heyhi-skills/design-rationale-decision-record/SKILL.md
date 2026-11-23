---
name: design-rationale-decision-record
description: >-
  Scaffold a design decision record and keep the team's decision history honest.
  Runs the mechanical work: build the ADR / DACI record structure with the
  rationale and the decision left as empty slots (including a supersede-record
  variant that links the predecessor), check DACI completeness (is a Driver and
  an Approver named, are Contributors and Informed listed), and sweep a body of
  docs or threads for decisions that were discussed but never recorded, or
  recorded in one place and contradicted in another. Triggers: "record this
  design decision", "write the ADR", "scaffold the rationale", "who's the
  approver on this", "did we ever decide", "find unrecorded decisions", "decision
  log for the design team". Produces a decision record whose rationale and
  decision ship EMPTY behind a named human gate — the decision is the human's.
  NOT for auditing an opportunity / JTBD / strategy artifact's reasoning (use
  strategy-integrity-warden). NOT for maintaining HeyHi's own append-only
  decision-log (that is the firm's ai-services/_core/decision-log.md, not a
  client design-team tool). NOT for running or capturing a live critique.
version: "0.3.0"
updated: "2026-11-22"
status: "deployed — heyhi-skills/; v0.2.0 promoted 2026-08-23 (Gate G-C, plans/plan-sheerline-skills-upgrade-2026-08-22.md) — adds Mode B sweep method (decision-verb/settlement-phrase heuristics + corpus-scoping + a coverage note), a Mode A supersede-record scaffold variant, open-questions + near-misses surfaces, a worked example, 2 eval cases (5→7). v0.1.0 promoted 2026-08-15 (DISPATCH-D). Sheerline area 11 (Collaboration & Facilitation), P1.5. Registered in skill-registry.yaml v2.35.0. v0.3.0 promoted 2026-11-22 by keel-sheerline-next CV1.2 after the owner's G-F-1 review (#1017, #1018; drafted by LF, #1008)."
---

# Design Rationale & Decision-Record Keeper

**Sheerline area 11 (Collaboration, Communication & Facilitation) · P1.5 · pure validate/audit skill.** Design teams decide things in meetings and lose the reasoning by the next sprint; the same question gets re-litigated because nobody wrote down why it was settled, or two docs quietly contradict each other. This skill does the mechanical half: it structures the record, checks that the decision-making roles are named, and sweeps for decisions that went unrecorded or drifted out of agreement. It leaves the *rationale content and the decision itself* to the people who own them. It generalizes HeyHi's own append-only decision-log discipline as a tool a client design team can use — precedent, not a copy of HeyHi's log.

**The boundary this skill obeys (Sheerline § 9, absolute).** A structured artifact with explicit empty judgment slots, a named human gate, and provenance labels on anything synthetic. *The rationale content and the decision are the empty slots.* Building the ADR frame (including the supersede-record variant) and checking DACI completeness is mechanical; deciding, and articulating *why*, is the human's — and the articulation struggle is itself the mechanism, so the skill must not do it for them. A version that writes the rationale or picks the option has exceeded its charter. The Mode B sweep *proposes* candidates and steps back; it never asserts what was decided. Grades never gates; mechanics never taste.

> **This skill closes through the Exit Gate (`CLAUDE-SESSION-RULES.md § Exit Gate`).** See the bottom-of-skill bracket.

---

## Routing — disambiguation with sibling skills

| If the task is… | Use |
|---|---|
| Scaffold a design decision record, check DACI roles, sweep for unrecorded/contradicted decisions | **this skill** |
| Audit an opportunity / JTBD / prioritization artifact's *reasoning integrity* | `strategy-integrity-warden` |
| Maintain **HeyHi's own** append-only decision-log | edit `ai-services/_core/decision-log.md` directly (the firm's log, not a skill) |
| Sweep **HeyHi's own** project for propagation gaps / integrity | `heyhi-session-integrity` |
| Prepare or capture a live design critique | `crit-prep-and-capture` (area 11; capture emits into this skill's Mode A scaffold) |
| Write the rationale, or make the decision | **the human** (this skill's named gate) |

The kinship with HeyHi's decision-log is precedent, not collision: this skill *is* that discipline, generalized for a client design team's own decisions. It never edits HeyHi's log.

---

## Step 0: Improvement hook check

Retrieve any recurring corrections for decision-record / rationale work (`retrieve_design_corrections` or the Sheerline `os/corrections/` registry). Fold a match in. Skip silently if none.

## Step 1: Load context

1. The **material**: for a *record* task, the decision the human wants captured (plus who was involved, and whether it supersedes a prior decision). For a *sweep* task, the body of docs / threads / decision-log the human points at, and the scope bound (which docs, what date range).
2. `references/decision-record-canon.md` — the ADR structure, the supersede-record variant, DACI vs RACI, the integrity-sweep method with its decision-verb heuristics and corpus-scoping guidance, and why the rationale ships empty. THE method spine.
3. `references/worked-example.md` — a filled Mode B sweep and a Mode A supersede scaffold on synthetic input. Read it to calibrate register and depth; do not copy its findings.
4. The Sheerline area-11 governed context (`sheerline/os/foundations/registry.yaml` area-collaboration-facilitation; the area-11 foundation is deferred to P3, manifest-grade foundation under consideration in Wave G). Register under it; do not author it.
5. The gate rules in `sheerline/os/session-rules.md` § Gate fields (owner, age, escalation, a proxy-aware signature, the Uncertain calls section, the drawn-by-default register) and the engagement intake's `review` block (`review_surface`, `drawn_by_default`, `gate_max_age_days`, `gate_escalate_to`). Copy the intake's gate defaults into the scaffold's Named gate; leave a field blank when the intake has no default.

## Step 2: Do the mechanical work

Two modes, one boundary.

**Mode A — Scaffold a record.** Build the ADR/DACI frame with the reasoning slots empty:
- **Structure** the record: title, status, context, options considered (as headers to fill, not filled), decision (empty), consequences (empty).
- **DACI-completeness check:** is exactly one **Driver** named? one **Approver**? are **Contributors** and **Informed** listed? Flag a record with no Approver, two Approvers, or an unnamed Driver — a decision with no accountable owner is the failure mode DACI exists to prevent.
- **Supersede-record variant (v0.2.0).** When the decision revisits a prior one, scaffold it as a *superseding* record rather than an edit of the old one (append-only discipline): set status `superseding`, add a `Supersedes:` line naming the predecessor record, and add a "What changed since the prior decision" context prompt. The predecessor is **linked, not rewritten**; the new decision and rationale stay empty slots. The point of the variant is to make "never overwrite a past decision, write a new one that supersedes it" a one-step scaffold instead of a discipline the team has to remember.
- **Gate fields and uncertain calls (v0.3.0).** The Named gate carries the owner (the Approver), the day it opened, its max age, who it escalates to, and a signature with a Proxy field that ships blank (`sheerline/os/session-rules.md` § Gate fields). Only the owner's own signature with `Proxy: no` closes it. A proxy signature records `fired (proxy)`: proof the record reached a reviewer, never a close, so it never moves the record to `accepted`. The Uncertain calls section lists the scaffold's own least-sure drafts (a DACI role read from a thread, a paraphrased option name, an inferred supersede link), unordered and unscored, or the literal `none`. A record accepted before v0.3.0 carries no Owner line or Proxy field, so it fails DR-07 and DR-09 until its owner re-signs with `Proxy: no`; the check never re-signs it.
- **Drawn-by-default, opt-in only (v0.3.0).** Only when the engagement intake sets `review.drawn_by_default: true` may the scaffold draw a recommended Decision, and only into a register row (drawn, alternative, redraw cost, walked by, walk by). The Decision slot itself stays empty until the Approver walks the row and writes it. The Rationale is never drawn, even with the opt-in on: writing the why is the mechanism this skill protects. With the opt-in off (the default) there is no register.
- The record is handed over with the reasoning blank for the humans to fill.

**Mode B — Integrity sweep.** Scan the pointed-at body for decisions that are unrecorded, contradicted, or stale — at scale, using the method:
- **Decision-verb / settlement-phrase heuristics.** A decision leaves linguistic tells. Scan for settlement phrases — "we'll go with", "let's ship / drop / kill", "decided to", "final call", "agreed", "going with X over Y", "approved", "sign-off", and past-tense settlements ("we ended up", "we went with"). For contradictions and supersessions, scan for reversal tells — "actually, let's not", "changing course", "we're now", "instead of". These are *candidate-surfacing* heuristics, not proof: a settlement phrase in a hypothetical ("if we went with X…") is a near-miss, not a decision.
- **Corpus-scoping.** Bound the sweep before running it: name the doc/channel set and the date range, prioritize high-signal surfaces (meeting notes, decision-tagged threads, RFC/spec docs, PR descriptions) over low-signal chatter, and **dedup** — one decision discussed across three threads is one candidate. On a large corpus, sample deliberately and say so; never present a sampled sweep as exhaustive.
- **The coverage note (honesty).** State what was swept and what was not. A sweep that surfaces nothing must distinguish "swept fully, found nothing" from "sampled a slice" — a silent clean result reads as "there is nothing there," which a partial sweep has not earned. (Pairs with the verification-harness-false-clean discipline: absence of findings is only a finding if the instrument actually ran over the whole corpus.)
- **The three findings**, each surfaced as a `[candidate — needs confirmation]` (see provenance): **unrecorded** (settled in a thread, never written into a record), **contradicted** (recorded, then reversed with no superseding record — surface the pair, do not adjudicate), **stale / dangling** (stuck `proposed`, or citing superseded context).

## Step 3: Produce the output

**Mode A — the record scaffold** (base, or the supersede variant):

```
# Decision Record — [title]
Status: [ proposed | accepted | superseding | superseded ]   Date: ______
Supersedes: [predecessor record id/title — ONLY on the supersede variant; the predecessor is
             linked, never rewritten]

## DACI
Driver (owns getting to a decision):  ____________________
Approver (makes the call — exactly one): ____________________
Contributors (consulted):            ____________________
Informed (told after):               ____________________
[DACI-completeness check result: PASS / FLAG — reason]

## Context
[the situation forcing a decision — for the humans to fill]
[supersede variant adds: What changed since the prior decision — for the humans to fill]

## Options considered
1. ____________________
2. ____________________

## ⛔ Decision — NEEDS HUMAN
This slot is intentionally empty. The decision is the Approver's to make and record.
   Decision: ____________________

## ⛔ Rationale — NEEDS HUMAN
This slot is intentionally empty. Articulating *why* is the mechanism; the skill does
not write it for you. (On a supersede record: the new "why" is written fresh, not copied
forward from the predecessor.)
   Why: ____________________

## Consequences
[what this commits the team to — for the humans to fill]

## Open questions for the humans (to complete the record)
[Questions the record still needs answered — not the rationale itself. E.g. "Is this the
 first decision on this topic, or does it supersede a prior record?" "Which of the listed
 options were genuinely considered vs. named for completeness?"]

## Uncertain calls
[The scaffold's own least-sure drafts, unordered and unscored: a DACI role read from a thread,
 an option name paraphrased, a supersede link inferred. Write `none` when there are none.]

## Drawn-by-default register (ONLY when the engagement intake sets review.drawn_by_default: true)
| Slot | Drawn | Alternative | Redraw cost | Walked by | Walk by |
|------|-------|-------------|-------------|-----------|---------|
[Absent when the opt-in is off (the default). Never a Rationale row.]

## Named gate
Owner (the Approver above): ____________   Opened: ______   Max age (days): ______   Escalate to: ____________
Approver sign-off: ____________________   Date: ______   Proxy: ____   Where: ______
No decision is recorded as accepted until the Owner signs in person and states no in the Proxy
field. Someone signing on the Owner's behalf states yes there, which records `fired (proxy)`:
proof the record reached a reviewer, never a close. Proxy ships blank; the person who signs states it.
Before marking accepted: python3 scripts/check_record.py <this record>
```

**Mode B — the integrity-sweep report:**

```
# Decision Integrity Sweep — [scope]
Swept: [what was scanned]        Date: ______

## Coverage note
[What was swept (doc/channel set, date range) and what was NOT. Exhaustive over the named
 corpus, or a sample? A clean result means "nothing found in the swept scope", not "nothing
 exists" — say which.]

## Unrecorded (discussed, never recorded)
| Where discussed | Apparent decision | Settlement tell | Provenance |
|-----------------|-------------------|-----------------|------------|
| #design-thread  | "we'll drop the tabbed nav" | "we'll drop" | [candidate — needs confirmation] |

## Contradicted (recorded, then reversed without a superseding record)
| Record A | Record B / doc | The contradiction |
|----------|----------------|-------------------|

## Stale / dangling
| Record | Issue (stuck 'proposed', superseded context, …) |

All rows are agent-surfaced CANDIDATES — see provenance. None asserts what the team decided.

## Open questions for the team (questions, not judgments)
[What the sweep would ask to confirm the candidates. Each a question — "Was the tabbed-nav
 drop actually decided, or is it still open?" — never an assertion that it was.]

## Near-misses and unchecked territory (the sweep journey, made inspectable)
[Phrases that looked like decisions but were hypotheticals; candidates deduped to one; corpus
 regions not swept. Traces, no verdicts.]
- Considered, not a decision: [e.g. "'if we killed the tour…' in #ideas — a hypothetical, not a settlement."]
- Deduped: [e.g. "the 4-pt grid appears in 3 threads — surfaced once."]
- Not swept: [e.g. "the Figma comment threads were out of scope for this pass."]

## Uncertain calls
[The sweep's own least-sure candidates, unordered and unscored: a settlement phrase that may be
 a hypothetical, a dedup that may have merged two decisions. Write `none` when there are none.]

## Named gate
Owner: ____________   Opened: ______   Max age (days): ______   Escalate to: ____________
Reviewer confirmation (which candidates are real): ____________________  Date: ______   Proxy: ____   Where: ______
```

**Done when:** Mode A hands over a structured record (base or supersede variant) with the decision and rationale slots blank, a DACI-completeness result, and — on a supersede record — the predecessor linked but not rewritten; Mode B surfaces candidates without adjudicating any, carries a coverage note, and populates the open-questions and near-misses surfaces as questions/traces. Both carry the gate fields and an Uncertain calls section (or `none`); a register appears only when the intake opted in.

## Step 4: Pre-flight verification

Confirm: the decision and rationale slots are empty (Mode A); on a supersede record, the predecessor is linked and the new decision/rationale/why are NOT copied forward from it; every swept candidate is labeled `[candidate — needs confirmation]` and none is asserted as fact (Mode B); the DACI check flags rather than fills a missing Approver; the skill has not adjudicated any contradiction; no HeyHi-internal decision-log file was edited. New in v0.2.0: confirm the Mode B report carries a coverage note that distinguishes "swept fully" from "sampled"; confirm every open question is a question and every near-miss is a trace. New in v0.3.0: confirm the Named gate carries all four gate fields and a Proxy field; confirm the Uncertain calls section is present (or reads `none`); confirm a register exists only when the intake opted in and holds no Rationale row; and run `python3 scripts/check_record.py <record>` on any record a human is about to mark `accepted`. It fails an accepted record with a blank or placeholder Decision or Rationale, no signature, a proxy signature, a signature that is not the Owner's, a blank or unclear Proxy field, two statuses, an unwalked or proxy-walked register row, or a Rationale register row, and it warns on an aged gate. It fails closed: only the Owner's own signature with `Proxy: no` closes the gate. It is read-only and never fills a slot.

---

## What is explicitly out of scope

- **Writing the rationale or making the decision.** Empty by construction (§ 9). The articulation struggle is the human's mechanism; the skill must not shortcut it — including on a supersede record, where the new "why" is written fresh, never carried over.
- **Adjudicating a contradiction.** Mode B surfaces the pair; which record wins is a human call recorded via a superseding record.
- **Signing, escalating or closing a gate.** The check reads gate state; it never signs, never counts a proxy signature as a close, and never decides what an aged gate's escalation owner decides.
- **Claiming exhaustive coverage on a sampled sweep.** The coverage note is honest about scope; a partial sweep never presents its clean regions as proof nothing exists.
- **HeyHi's own decision-log.** `ai-services/_core/decision-log.md` is the firm's append-only log, edited directly, not through this skill. **HeyHi's own integrity sweep** — `heyhi-session-integrity`.
- **Opportunity / strategy reasoning** — `strategy-integrity-warden`. **Live critique** — `crit-prep-and-capture` (area 11; it feeds this skill).

---

## Exit Gate Required Headers (bottom-of-skill bracket)

This skill closes through Exit Gate Flavor A (`CLAUDE-SESSION-RULES.md § Exit Gate`). Before declaring done, confirm every required header holds real content:

- `## Fixes Applied` (or the delivered record scaffold / sweep report)
- `## Smoke Test` (the Step 4 pre-flight checks, pasted)
- `## Next Session Prompt`

If the decision or rationale slot is filled, a swept candidate is asserted as fact, a supersede record rewrites its predecessor, a sampled sweep claims exhaustive coverage, a proxy signature is counted as a close, or a record reads `accepted` while `scripts/check_record.py` fails it, the gate has **not** been satisfied.

---

*Sheerline area 11 (Collaboration, Communication & Facilitation), P1.5 net-new. v0.1.0 deployed 2026-08-15 (DISPATCH-D); registered in `skill-registry.yaml` v2.32.0. v0.2.0 staged 2026-08-23 (Wave D, `plans/plan-sheerline-skills-upgrade-2026-08-22.md`). v0.3.0 staged 2026-11-22 (gate hygiene: the gate fields, the Uncertain calls section, the opt-in drawn-by-default register, `scripts/check_record.py`; `plans/plan-keel-sheerline-next-versions-2026-11-21.md` LF.1 to LF.3). Spec source: `ai-services/design-intelligence/research/sheerline-skill-buildout-research-2026-08-09.md` § 6.3 / § 8; sweep method, supersede scaffold, and curiosity surfaces from the 2026-08-22 skills audit § 2.4 / § 5. Boundary: § 9.*
