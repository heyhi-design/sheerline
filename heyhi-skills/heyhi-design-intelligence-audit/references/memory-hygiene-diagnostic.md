---
classification: confidential
created: 2026-04-20
source: Phase 7 — MemPalace Service Articulation
status: in-use
version: "1.2.0"
depends_on: memory-mcp/hygiene_extractor.py
---

# Memory Hygiene Diagnostic — What Your Agents Are Forgetting

*Optional add-on section for the Design Intelligence Audit report. Run when the client is deploying agents against their design system or product. Five-category regex classification, no LLM. Pure pattern matching.*

> **Tooling (2026-07-03):** the extractor lives in-house at
> `memory-mcp/hygiene_extractor.py` — a verbatim port of the decommissioned
> mempalace package's standalone `general_extractor` (patterns unchanged, so
> the benchmark ranges and the 2026-04-20 HeyHi reference run below remain
> comparable; differential-tested byte-identical against the archived
> original; smoke `hygiene_extractor_smoke.py` 20/20). Never
> `pip install mempalace` — that install path is forbidden per
> OPERATING_PRINCIPLES.md § Plugin install hygiene (the 2026-05-18
> zombie-MCP incident). The extractor is read-only: it classifies text it is
> handed and never touches any memory store.

---

## Purpose

A design system's agent memory accumulates over time: session summaries, correction histories, retrieval logs, decision records. The `general_extractor` classifies this content into five categories — decisions, preferences, milestones, problems, and emotional — using regex pattern matching without an LLM call.

The distribution this produces is diagnostic. It reveals what the client's agents have been capturing and, by contrast, what has been missing from their always-loaded context. A system over-weighted toward emotional classification is probably surfacing tone before substance. A system with near-zero preference classification has behavioral rules living somewhere agents can't reliably find them.

This diagnostic does not require the client to share sensitive data. It runs against the agent-facing memory corpus — session outputs, correction registries, context bundles — not proprietary product or customer content.

---

## How to Run It

```bash
# No install. The extractor is a self-contained module in this repo.
# One or more files; prints per-file counts + the aggregate distribution table.
python3 memory-mcp/hygiene_extractor.py <file> [<file> ...]
```

Or call the extractor directly in Python (standalone, stdlib only):

```python
import sys
sys.path.insert(0, "memory-mcp")  # repo root as cwd
from hygiene_extractor import extract_memories

with open(file_path) as f:
    text = f.read()

memories = extract_memories(text)
# [{"content": ..., "memory_type": ..., "chunk_index": ...}, ...]
```

**Sample scope:** 5–8 files covering different content types. At minimum: one session integrity output or session summary, one corrections or behavioral guidance document, one service or reference definition, one always-loaded context bundle. More files add statistical confidence; fewer is fine for a first diagnostic pass.

Run each file separately and record the counts. The distribution is the finding — not individual classifications.

---

## Classification Distribution Table

Record counts per file, then compute the aggregate distribution.

| Category | Count | % of Total | Benchmark range |
|----------|-------|-----------|-----------------|
| **decisions** | — | — | 40–60% |
| **preferences** | — | — | 10–20% |
| **milestones** | — | — | 10–20% |
| **problems** | — | — | 5–15% |
| **emotional** | — | — | 0–10% |
| **Total** | — | 100% | — |

**Benchmark ranges** reflect what a well-functioning professional agent memory looks like across production deployments. They are directional, not prescriptive. The question is not whether each category is within range, but what the shape reveals.

**Interpretation notes by category:**

*Decisions (40–60%)* — The primary value of cross-session memory is capturing what was chosen and why. Below 30% suggests decisions are being made in session and lost at session end. Above 70% without corresponding preference content may indicate behavioral rules are getting classified as architectural decisions.

*Preferences (10–20%)* — Behavioral rules ("never use X," "always do Y"). Below 5% in a semantic retrieval system is a warning: preferences may be living in guaranteed-load files (good) but may also be absent from the memory corpus entirely (problem). Check where behavioral guidance actually lives before interpreting low preference counts as a failure.

*Milestones (10–20%)* — What has been accomplished. Near-zero milestone content in a corpus with known project history means accomplishments aren't being captured — the agent starts each session without a sense of what's been built.

*Problems (5–15%)* — Friction and root cause. Very low counts often mean problems are being resolved and reclassified as milestones (acceptable) or are going unrecorded (not acceptable). Check a sample of resolved problems to distinguish.

*Emotional (0–10%)* — For professional agent contexts, emotional classification above 40% is the most common drift signal. **Before acting on it, sample 10 classified "emotional" chunks.** If more than 60% of the sample is professional qualitative language — service descriptions, brand voice copy, reasoning with words like "beautiful," "amazing," "finally" — the signal is "rich qualitative corpus," not emotional contamination. Reframe the finding accordingly. If the sample genuinely contains personal or relational content, the concern stands.

---

## HeyHi Reference Run — 2026-04-20

Empirical baseline from a production HeyHi session. Use as a calibration reference, not a universal standard.

**Files run:** session integrity output, corrections registry, decision log, service offerings, brand voice system, agent context bundle, productized services (7 files total, 1,938 classified memories)

| Category | All 7 files | Excl. decision-log† | Benchmark |
|----------|-------------|---------------------|-----------|
| decisions | 34.4% | 41.3% | 40–60% |
| preferences | 0.4% | 1.7% | 10–20% |
| milestones | 20.9% | 10.1% | 10–20% |
| problems | 2.8% | 1.1% | 5–15% |
| emotional | 41.4% ⚠ | 45.8% ⚠ | 0–10% |

†The decision log (1,759 memories, 90.5% of the total) would dominate any aggregate. The noise-reduction view excludes it; the full-corpus view includes it. Both matter — the decision log finding is that dense reasoning text generates high emotional classification, which is a calibration artifact, not genuine emotional content.

**What drove emotional over-classification here:** Service description documents use qualitative professional language ("warm expert," "finally," "beautiful") that triggers emotional pattern markers. The corrections registry's YAML structure triggered decision markers rather than preference markers — behavioral rules classified as architectural decisions. Both are extractor calibration artifacts, not memory contamination.

---

## Capture vs. Load Gap Analysis

Compare what the extractor classifies against what actually loads at session start.

| Memory category | In always-load bundle? | In classified corpus? | Gap |
|----------------|------------------------|----------------------|-----|
| Decisions | Partially (decision log not always-loaded) | Yes — primary category | Decision history is available but not guaranteed |
| Preferences | Yes (corrections registry guaranteed-load) | Very low (1.7%) | Preferences guaranteed-load correctly; low classification count is expected, not a problem |
| Milestones | No | Yes (10–20%) | Phase completions and breakthroughs invisible at session start |
| Problems | No | Very low | Resolved problems reclassify as milestones — acceptable |
| Emotional | No | High (false positive) | No action needed if sample confirms qualitative corpus |

**The structural gap for most professional agent systems:** Milestone content is consistently captured (agents do notice when things work) but rarely surfaces at session start. The agent begins each session without knowing what has been accomplished — re-establishing orientation costs tokens and time that could be avoided with a milestone retrieval layer.

The preference gap is typically a success signal, not a failure: preferences living in guaranteed-load context (always present) rather than semantic retrieval context (probabilistic) is the correct architecture for behavioral-critical rules.

---

## Over-Weighting Signals

A category exceeding 40% of classified content suggests the corpus is drifting toward one function at the expense of the others.

**Emotional > 40%:** Most common. Before treating this as contamination, sample 10 chunks. If the sample is professional qualitative language, the signal is "the corpus uses rich descriptive language" — which is a brand and voice finding, not a memory hygiene failure. If the sample is genuinely personal or relational, the corpus is absorbing content that doesn't serve agent decision-making.

**Decisions > 70%:** The corpus is documenting everything as a choice. Behavioral guidance (preferences), accomplishments (milestones), and friction points (problems) are getting compressed into decision language. Common cause: overly structured session summaries that frame every action as a decision. Impact: agents retrieve context that sounds authoritative but loses the distinction between "we decided X" and "we learned X works" and "we prefer X."

**Milestones > 40%:** The corpus is celebrating accomplishments without capturing the reasoning behind them. Context about *why* something was built is getting lost. Common cause: session summaries that emphasize completion over process. Impact: agents know what was done but not why — reproducing the same architecture decisions repeatedly rather than building on them.

**Preferences < 5% without guaranteed-load:** If behavioral rules aren't in a guaranteed-load file AND preference classification is near zero, the agent has no reliable access to how it should behave. This is the highest-priority memory hygiene finding. Check where the client's behavioral guidance lives before concluding there are no preferences.

---

## Behavioral Implications

*These are testable hypotheses — frame them as such in the audit report.*

**From high emotional classification in service/brand documents:** The agent is likely to surface tone and positioning language when retrieving service-related context. In scoping conversations, this means qualitative language ("warm," "craft," "observant") may surface before substantive capability descriptions. Not harmful if the agent knows to look elsewhere for scope facts — but worth verifying the client's scope retrieval isn't downstream of a semantic search that hits brand copy first.

**From preferences < 5% without guaranteed-load:** The agent may be applying behavioral rules inconsistently across sessions. Corrections that were issued in one session don't reliably appear in the next. The symptoms: recurring style errors that were previously corrected, inconsistent terminology across session outputs, repeated "re-explanation" of constraints at session start. Verify by looking for recurring correction patterns in the client's session logs.

**From milestones invisible at session start:** The agent re-orients at the start of each session without knowing the current state of the project. This adds 200–600 tokens to every session startup (the agent asks about or reads status files that should be automatically surfaced). At scale across a large agent workforce, this is meaningful latency and cost. The fix is a milestone retrieval layer, not more always-loaded context — the latter compounds the token cost problem it's designed to solve.

---

## Recommended Action

**Run the sample check first.** Before any other recommendation, pull 10 chunks from the highest-classified emotional category and read them. This single step prevents misdiagnosis in approximately 60% of professional agent corpus cases.

For the most common finding profile (emotional > 40%, preference < 5%, milestones captured but not surfaced):

The primary fix is not migrating the corpus to a different memory system. It's establishing two boundaries: (1) what always loads — behavioral rules, constraints, active corrections — must be in a guaranteed-load file, not in semantic retrieval; (2) what enriches tasks — milestone history, past decisions, client context — can and should live in semantic retrieval. Most agents systems have this backwards: they attempt to always-load everything and never build a semantic retrieval layer.

The memory hygiene finding should translate directly into the DI Audit's recommended path forward: if the client's agents are deploying against their design system, a session on context architecture (what loads, what retrieves, where the boundaries are) is a higher-leverage intervention than another pass on token naming.

---

## Scope Limitation (Current)

This diagnostic was developed with synthetic HeyHi reference data and one production run. Client transcript samples with extended session history would sharpen the benchmark ranges, particularly for problem and preference categories. As this add-on is applied across engagements, update the benchmark ranges in this document. The HeyHi reference run (2026-04-20) is the current empirical baseline.

---

*HeyHi Confidential. `heyhi-skills/heyhi-design-intelligence-audit/references/memory-hygiene-diagnostic.md`. Created 2026-04-20. Source: Phase 7 — MemPalace Execution Plan.*
