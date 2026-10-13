---
classification: confidential
title: "Decision-record canon — the method spine"
skill: design-rationale-decision-record
loaded_by: "SKILL.md Step 1"
---

# Decision-record canon

The record structures and the integrity-sweep method, held as reference. On-demand — load when running the keeper.

*Internal operational reference (deployed under `heyhi-skills/`): em-dash limit exempt per `OPERATING_PRINCIPLES.md`.*

---

## ADR — the record structure

An Architecture (or design) Decision Record captures one decision. The fields, all of which the *humans* fill except structure:

- **Title** — a short noun phrase naming the decision.
- **Status** — `proposed` → `accepted` → (later) `superseded`. A record that supersedes another names it, so history stays traceable rather than overwritten. (This mirrors HeyHi's own append-only decision-log discipline: never edit a past decision, add a new one that supersedes it.)
- **Context** — the situation forcing the decision.
- **Options considered** — the alternatives, as headers to fill.
- **Decision** — the choice made. *Empty slot* — the Approver's to make.
- **Rationale / Why** — the reasoning. *Empty slot* — see below.
- **Consequences** — what the decision commits the team to.

## The supersede-record variant (v0.2.0)

Supersession is the core discipline the canon names, but a team has to *remember* to write a new record instead of editing the old one — the moment they edit in place, the history is lost. This variant makes the discipline a one-step scaffold:

- **Status `superseding`** and a **`Supersedes:` line** naming the predecessor record (its id or title). The predecessor is **linked, never rewritten** — it stays in the history at status `superseded`, and the new record points back at it.
- A **"What changed since the prior decision"** context prompt — the reason a settled decision is being reopened (new evidence, a changed constraint, a failed bet). This is what a bare edit would erase.
- The new **Decision and Rationale are still empty slots.** Critically, the new "why" is written *fresh* — a supersede record must not copy the predecessor's rationale forward as if the reasoning still holds unchanged; if it held unchanged, there would be nothing to supersede. Carrying the old rationale forward is the exact failure the variant exists to prevent.
- The scaffold links the predecessor; it does not judge whether superseding is correct (that is the Approver's call, recorded by signing).

This is the append-only / superseded-not-overwritten discipline turned into a form, so the team's decision history stays a traceable chain instead of a series of silent overwrites.

## DACI vs RACI — role frameworks

**DACI is for the decision; RACI is for the work.** Do not confuse them.

- **DACI** — *Driver* (owns getting to a decision by a date), *Approver* (makes the call — exactly one, the accountable owner), *Contributors* (consulted for input), *Informed* (told after). The DACI-completeness check: exactly one Approver, a named Driver, listed Contributors and Informed. **A decision with no Approver has no accountable owner — that is the failure DACI exists to prevent, and the most important flag the skill raises.** Two Approvers is the second-most-common failure (nobody can actually decide).
- **RACI** — *Responsible*, *Accountable*, *Consulted*, *Informed* — governs *executing* the work after the decision. The keeper checks DACI on the decision; RACI is out of scope unless the team explicitly asks to map the follow-on work.

## Why the rationale ships empty (the load-bearing constraint)

It is tempting to have the skill draft the "why." It must not. **The struggle of articulating the rationale is the mechanism** — writing down why forces the team to confront whether the reasoning actually holds, and a pre-written rationale robs them of exactly that. A rationale the agent authored reads as settled thinking that was never actually thought. The skill structures the slot and leaves it blank. Same for the decision: the Approver decides; the skill records.

This is the § 9 boundary in its purest form for this area — the record is the structured artifact, the decision and rationale are the empty judgment slots, the Approver sign-off is the named gate.

## The integrity sweep (Mode B) — method at scale (v0.2.0)

Scanning a body of docs/threads/records for decision hygiene. The v0.1.0 skill named the three findings but not *how to find them across a large corpus*. The method:

### Decision-verb / settlement-phrase heuristics

A settled decision leaves linguistic tells. Scan for them as **candidate-surfacing signals** (never as proof):

- **Settlement phrases** — "we'll go with", "let's ship / drop / kill / cut", "decided to", "final call", "the call is", "agreed", "we're going with X (over Y)", "approved", "sign-off", "locked".
- **Past-tense settlements** — "we ended up", "we went with", "we settled on", "in the end we".
- **Reversal / supersession tells** (for contradictions) — "actually, let's not", "changing course", "we're now", "instead of", "scrap that", "on second thought".

Each hit is a *candidate location*, not a decision. A settlement phrase inside a hypothetical ("if we went with X, then…"), a quote, or a question ("should we go with X?") is a **near-miss**, not a finding — record it in near-misses, do not surface it as a candidate.

### Corpus-scoping (make a large sweep tractable and honest)

- **Bound it first.** Name the doc/channel set and the date range before sweeping. An unbounded "sweep everything" is neither runnable nor verifiable.
- **Prioritize high-signal surfaces.** Meeting notes, decision-tagged threads, RFC/spec docs, PR/MR descriptions, and design-review docs carry decisions; general chatter mostly does not. Sweep the high-signal set first.
- **Dedup.** One decision discussed across several threads is *one* candidate — collapse duplicates, cite the clearest location, and note the others in near-misses.
- **Sample deliberately, and say so.** On a corpus too large to read fully, sample the high-signal surfaces and state that the sweep was a sample. Never present a sampled sweep as exhaustive.

### The coverage note (the honesty discipline)

Every sweep states **what was swept and what was not**, and whether the pass was exhaustive over the named corpus or a sample. This exists because *absence of findings is only a finding if the instrument ran over the whole corpus* — a silent clean result reads as "there are no unrecorded decisions," which a partial sweep has not earned. (This is the decision-hygiene instance of the verification-harness-false-clean discipline: a "0 candidates" result must distinguish "swept fully, genuinely nothing" from "sampled a slice.")

### The three findings

Each surfaced as a `[candidate — needs confirmation]`, never asserted:

- **Unrecorded** — a decision discussed and apparently settled in a thread or doc but never written into a record. The sweep proposes "this looks decided"; a human confirms it was.
- **Contradicted** — a recorded decision that a later record or doc reverses *without* a superseding record. Surface the pair; do not decide which is right (that is a human call, resolved by writing a superseding record — the supersede variant above is the tool for it).
- **Stale / dangling** — records stuck in `proposed` long past the decision, or citing context that has since been superseded.

The sweep's whole value is that it *proposes and steps back*. An integrity sweep that declares "the team decided X" has manufactured a decision record out of an inference — the exact laundering the boundary forbids.

## The two curiosity surfaces (open questions, near-misses) — why they are not verdicts (v0.2.0)

- **Open questions** (both modes) — in Mode A, the questions the record still needs answered to be complete (is there a predecessor? which options were genuinely considered?); in Mode B, the questions that would confirm each candidate ("was the tabbed-nav drop actually decided, or is it still open?"). Never an assertion; always a question.
- **Near-misses and unchecked territory** (Mode B — the sweep has a journey to trace) — settlement phrases that turned out to be hypotheticals, candidates deduped to one, corpus regions left unswept. It renders the sweep inspectable so the next reader sees where coverage is thin. No verdict.

## Provenance discipline for this skill

Anything the sweep surfaces is agent-inferred from the source material and labeled `[candidate — needs confirmation]`. It never reads as an established decision. If the keeper drafts placeholder text inside a record scaffold (e.g. a candidate option pulled from a thread), that text is labeled as a candidate too, so a scaffold can never be mistaken for a filled, human-owned record.

## Kinship, not collision, with HeyHi's own log

HeyHi runs exactly this discipline on itself: an append-only `decision-log.md`, never edited, superseded-not-overwritten, read-the-last-5 before appending. This skill generalizes that discipline into a tool a *client* design team can run on its own decisions. It is precedent — the proof the discipline works — not a tool for maintaining HeyHi's log (that stays a direct edit of `ai-services/_core/decision-log.md`).

*HeyHi Confidential. Reference for `design-rationale-decision-record`. Spec source: `sheerline-skill-buildout-research-2026-08-09.md` § 6.3; supersede variant + sweep method + coverage note added v0.2.0 per the 2026-08-22 skills audit § 2.4.*
