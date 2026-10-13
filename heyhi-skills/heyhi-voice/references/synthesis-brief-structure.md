---
classification: internal
title: Synthesis-Brief Structure
purpose: Three-level structure for synthesis briefs that close campaigns, audits, or multi-session investigations. The shape that lets a reader open one document and see where things stand.
created: 2026-05-21
last_reviewed: 2026-05-21
loaded_by: heyhi-voice
companion_to: brand/essay-craft-guide.md
worked_examples:
  - ai-services/_core/service-readiness-brief-2026-05-21.md
  - ai-services/_core/integrity-mechanism-fix-spec-2026-05-21.md
---

# Synthesis-Brief Structure

Reference for `heyhi-voice` when the task is a closing artifact for a campaign, audit, multi-session investigation, or any work that needs to be readable by someone who was not in the room. Load this when the user asks for a brief, a readiness assessment, a state-of-the-X document, an audit summary, or a fix specification.

This reference governs structure. It does not replace the voice rules in `heyhi-voice/SKILL.md` — those still apply. Voice rules tell you *how to sound*; this document tells you *how to be readable*.

---

## What a synthesis brief is

A document the reader opens to see where one named thing stands, today. The reader is making a decision or building on the work; they did not run the campaign that produced it. The brief is the bridge.

Three properties define one:

- **Single subject.** One topic, named in the title. Not a status update across many initiatives.
- **Single moment.** One date in the frontmatter. The brief is a snapshot, not a living document. It will be superseded by the next pass, and that is fine.
- **Cited.** Every non-obvious claim points to a source the reader could open: a ledger row, a finding ID, a downstream file, a session output. No claim without evidence.

If the document the user is asking for fails any of these three, it is not a synthesis brief. It is a plan (multi-subject, forward-looking), a decision log (multi-moment, append-only), or an essay (cited only by argument structure). Push back and clarify before drafting.

---

## The three-level structure

Every synthesis brief has three levels, in this order. Each level serves a distinct reader posture.

### Level 1: Headline

**Reader posture:** "I have 60 seconds. Tell me where this stands."

**What it is:** One paragraph or one short table that fits on one screen and answers the document's central question. If the brief is a readiness assessment, the headline names the counts in each readiness category. If the brief is a fix specification, the headline names the hypotheses confirmed and the parts of the fix that close them. If the brief is a status review, the headline names what is finished, in progress, and left to do.

**Form:**

- Lead with the number, the verdict, or the named state. Not the methodology, not the background.
- Add 3–6 supporting bullets that decompose the headline into its parts.
- End the level when a reader could close the document and walk away with a defensible summary.

**Anti-form:** Do not open with "This document...". Do not narrate the campaign. Do not list what the brief covers before the brief says anything. The headline is the answer; the reader earns the methodology by reading further.

### Level 2: Per-layer detail

**Reader posture:** "The headline says X. Show me the breakdown by the dimensions that matter."

**What it is:** The headline decomposed along the natural categories of the work. For a service readiness brief: per service layer (Consult / Build / Sustain / Products / Workshops). For a fix spec: per part of the fix (Part A / B / C / D). For an audit: per area or per finding cluster. For a status review: per workstream.

**Form:**

- Use tables, not prose paragraphs, for any breakdown with three or more rows. A table is a propagation surface; the next reader greps it.
- Each row carries the same fields. Pick the fields once; do not let columns drift between sections. (A common drift: "Backing" in one section, "Evidence" in the next.)
- Group rows by the highest-impact dimension. For readiness, that is *sellable today / sellable with caveats / not yet*. For a fix spec, that is *what / where / why / how verified / scope discipline*.
- Subsections within a layer get a third heading level (`###`) only when the layer contains genuinely different shapes of information (e.g., "sellable today" vs. "sellable with caveats" vs. "not yet").

**Anti-form:** Do not write per-layer detail as paragraphs interrupted by occasional bullets. The reader is scanning at this level. Paragraphs at level 2 push the reader back to level 1 or skip them to level 3, which means level 2 did not do its job.

### Level 3: Cited evidence

**Reader posture:** "I am going to act on this. Show me the source."

**What it is:** Every claim in levels 1 and 2 is backed by an identifier the reader can resolve. The brief does not contain the evidence itself — the evidence lives in the ledger, the finding catalog, the downstream surface, the session output. The brief points at it.

**Form:**

- Inline citations: `(deployed/done)`, `area_id`, `(DF-2)`, `(PL-14)`, `(CBD-1)`, `H3`, `Session 9` — short codes that resolve to a known location in the project.
- File-path citations: `offerings §Strategy Audit`, `synthesis.md`, `capability-audit-ledger.yaml#follow_on_artifacts`, `plans/plan-session-integrity-backward-reconciliation-2026-05-21.md`. Always relative to the project root; never bare filenames.
- Closing pointer: the brief ends with a "what 'today' means" or "carry-forward" section that names what is dated about this snapshot, what produced it, and what the next brief should re-verify.

**Anti-form:** Do not write evidence as "according to recent findings" or "the audit showed". Either you can cite a specific source by ID or path, or the claim is not earned and should be removed.

---

## What goes where: a decision table

| Information type | Level | Form |
|---|---|---|
| Total counts (how many sellable today, how many hypotheses confirmed) | 1 | Sentence with the number first |
| The verdict on the brief's central question | 1 | One paragraph |
| The 3–6 things that compose the headline | 1 | Bulleted list |
| Per-category breakdown of items | 2 | Table |
| Per-row evidence and gate | 2 | Table columns |
| Sub-shapes within a category (e.g., today / with caveats / not yet) | 2 | `###` subsections, each with its own table |
| Reasoning that does not fit a row | 2 | One paragraph between tables, never inside |
| Source identifiers for any claim | 3 | Inline parenthetical, code-formatted |
| Cross-references to other documents | 3 | Relative path, italic or backtick |
| The methodology that produced the brief | 3 | "What 'today' means" closing section |
| The deferred work that justifies caveats | 3 | "Carry-forward" closing section |

The most common drift is information bleeding up — methodology in the headline, evidence in level 2, level-3 detail crowding out the per-layer breakdown. The fix is to ask: *what is the reader doing right now?* Headline reader is deciding. Level-2 reader is scanning. Level-3 reader is acting. Match the form to the posture.

---

## Worked example 1: readiness brief

**Document:** `ai-services/_core/service-readiness-brief-2026-05-21.md` (Session 10 of the ai-services Audit Campaign).

**Central question:** Where does HeyHi stand on shipping agentic services for clients, today?

**Level 1 — Headline.** Three-bucket count: "Sellable today: 24. Sellable with caveats: 8. Not yet: 11." Followed by a five-bullet decomposition (Consult: 7, Build: 3, Sustain: 5, Products: 0, Workshops: 9). One paragraph naming the strongest service surfaces (design-intelligence and the consult layer) and the two highest-impact gaps (Signal Reader as agentic service, bidirectional canvas loop on Care+). Reader who stops here knows: 24 sellable today, two named gaps, plans in flight for both.

**Level 2 — Per-layer detail.** Six sections by service layer: `## Layer 01: Consult`, `## Layer 02: Build`, `## Layer 03: Sustain`, `## Layer 04: Products`, `## Workshops`, `## IP Buckets`. Each layer contains up to three subsections (`### Sellable today`, `### Sellable with caveats`, `### Not yet`), each with a table. Tables use the same column shape: Service · Backing area_ids · Downstream surface (or: Service · Backing · Caveat | Gate). The reader scans by layer, then by readiness state, and lands on a row.

**Level 3 — Cited evidence.** Every row cites at least one `area_id` from `capability-audit-ledger.yaml` and one downstream surface in `ai-service-offerings.md` or related files. Finding IDs (`DF-1`, `CBD-1`, `PL-5`) appear inline. The closing section "What 'today' means" names the brief's date (2026-05-21), the source it inherits from (the campaign ledger), and the structural fix that will keep it honest (Session 11's `state-sync.py capability_readiness` staleness check). A "Finished / In Progress / Left to Do" recap at level 2.5 (between full level-2 detail and the closing) gives one more flat enumeration for readers who want the totals back, broken down.

**Why this works:** The brief is offerable. A new agent or a new reader can open it cold and walk out with a defensible answer to "what can HeyHi sell today?" within 60 seconds. Drilling further does not change the answer; it grounds it.

---

## Worked example 2: fix specification

**Document:** `ai-services/_core/integrity-mechanism-fix-spec-2026-05-21.md` (Session 11 of the ai-services Audit Campaign).

**Central question:** What is the structural fix to the integrity mechanism, and what does the campaign's evidence say it must close?

**Level 1 — Headline.** A seven-row table: the seven hypotheses confirmed across Sessions 1, 9, and 10. Each row has the hypothesis ID (H1–H7), one-line statement, Session 1 verdict, new evidence summary, and final-campaign verdict. The headline paragraph after the table names the high-impact hypotheses ("H1, H2, and H5 are load-bearing"). Reader who stops here knows: seven hypotheses confirmed, three load-bearing, four-part fix follows.

**Level 2 — Per-layer detail.** Four `###` sections, one per part of the fix (Part A: Backward Reconciliation Pass, Part B: Deterministic Mandatory Propagation Checklist, Part C: state-sync.py Staleness Check, Part D: Targeted Hard-Rule and Correction-Registry Updates). Each part uses the same five-field shape: What it does · Where it lives · Why it works · How it gets verified · Scope discipline. The verification field always names a runnable test, not a claim that the part is correct.

**Level 3 — Cited evidence.** Every hypothesis cites the session(s) that confirmed it, the finding IDs (`DF-1` through `DF-11`, `CBD-1` through `CBD-6`), and the file(s) the evidence lives in (`capability-audit-ledger.yaml#integrity_pre_diagnosis`, `corrections-registry.yaml`). Each Part B rule cites the finding it addresses (`DF-2`, `CBD-1`). Closing sections: "Implementation order and ownership" (a table of who owns each part and where it lands), "What this fix is not" (the negative space — what the spec does *not* claim to do), and "Carry-forward" (what the next session inherits).

**Why this works:** The spec is buildable from the document alone. An engineer or a reviewer can open it cold and know which part to build next, what file changes, and what test confirms it works. The negative-space section prevents scope creep on the next pass.

---

## Two patterns the structure deliberately rejects

**The narrative campaign retrospective.** The temptation, at the end of a long campaign, is to tell the story of the campaign — what was found in Session 1, what shifted in Session 5, where the team got stuck in Session 8. Reject this. The reader of a synthesis brief does not need the narrative; they need the state. The campaign's narrative belongs in the decision-log entry that closes the campaign, not in the brief that summarizes it.

**The methodology-first explainer.** The other temptation is to lead with how the brief was produced — "this brief draws on the 60-area capability audit conducted across 11 sessions...". The methodology earns its place at the bottom, in "What 'today' means," not at the top. Headlines that begin with methodology are headlines the reader skips.

---

## Voice rules that still apply

The brief follows everything in `heyhi-voice/SKILL.md`:

- No em dashes beyond the document's exempt ceiling (the readiness brief and the fix spec are internal operational documents — exempt under the rationale in `OPERATING_PRINCIPLES.md`; the rule still applies for any client-facing or unclassified synthesis brief).
- No "AI" as a standalone word. Describe the function or the system.
- No banned vocabulary (no "leverage," no "unlock," no "synergy").
- Active voice. One idea per sentence in the prose paragraphs that bridge tables.
- Cite, do not summarize: when the source is a finding ID, write the finding ID; when the source is a file, write the relative path.

The structure is the propagation surface; the voice is the carrier. Both must hold for the brief to land.

---

## When *not* to use this structure

- **Plans.** A plan is forward-looking and covers multiple subjects (sessions, workstreams, deliverables). Synthesis briefs are backward-looking and cover one. If the document needs a "session detail" section per upcoming session, it is a plan; load `plans/README.md` instead.
- **Essays.** Long-form thought leadership earns its readers by argument, not by structured fields. Load `brand/essay-craft-guide.md`.
- **Status updates inside a session.** A status update is part of a working session, not a closing artifact. Use the Exit Gate's `## Findings Integration` or `## Smoke Test` slots in the handoff; do not produce a synthesis brief mid-session.
- **Single-table reports.** If the entire document fits in one table, write one table with a one-paragraph headline above it. The three-level structure is only justified when the brief is genuinely a brief — multi-table, multi-section, cite-dense.

---

## Quick checklist before declaring a synthesis brief done

- [ ] Title names a single subject and (usually) a date.
- [ ] Frontmatter includes `classification:`, `created:`, and the linked source artifact (campaign plan, ledger, audit report) the brief draws from.
- [ ] Level 1 (headline) fits on one screen. Lead is a number or a verdict, not a sentence about the document.
- [ ] Level 2 (per-layer detail) uses tables with stable column shapes.
- [ ] Level 3 (cited evidence) has no uncited claims. Every short code (`DF-N`, `PL-N`, `area_id`) resolves to a known location.
- [ ] Closing section names what the brief inherits, what it does not yet close, and what the next brief should re-verify.
- [ ] Voice gate passed: em-dash scan, banned-word scan, "AI" standalone scan.
- [ ] If the brief is one of two patterns deliberately rejected above, restructure before publishing.

---

*HeyHi Internal Use Only. Loaded by `heyhi-voice/SKILL.md` when a synthesis brief is the task.*
