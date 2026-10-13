---
classification: confidential
title: "Sheerline insights: the convention slot"
---

# Sheerline insights: the convention slot

This directory is the **convention** for how research INSIGHTS (nuggets) work in Sheerline — the ResearchOps half of the "learn" verb (`retrieve -> validate -> grade -> learn`). It is the sibling of `os/corrections/`: that slot governs failure-CORRECTIONS (a recurring mistake to stop repeating); this slot governs INSIGHTS (a recurring, opinion-free observation about a user, domain, or product). Placed here, mirroring `os/corrections/`, rather than under `os/foundations/`, so the two "learn" conventions sit side by side.

**The runtime lives elsewhere. Build no runtime here.** The insight *runtime* — the nugget schema, the three-tier registry resolution (live per-engagement `design-insights.yaml` / bundled `seed-insights.yaml` / always-loaded `practice-insights.yaml`), the bespoke validator and scorer, and the `retrieve_design_insights` reader — lands in the internal **`heyhi-mcp`** (`heyhi_mcp/corrections/insight_store.py`, `heyhi_mcp/tools/insights.py`), alongside the corrections runtime whose primitives it reuses. This slot is the convention pointer; it names that runtime and holds no runtime of its own. The populated per-engagement insight corpus and its curation judgment are the retained moat (`os/operating-principles.md` § IP boundary) and are never bundled here.

**An insight is not a correction (the hard boundary).** A correction is a validated RULE about our own process, prescriptive and (when factual) enforceable. An insight is provisional EVIDENCE about the world — descriptive, opinion-free, and **never enforced or auto-injected**. It informs a human or a downstream skill's judgment, full stop. The nugget schema deliberately carries no severity, no trigger condition, no correction rule, and no predicate; the insight reader tags every result `informational_only`. A version that enforced an insight, or let one auto-change generation, has collapsed the boundary this slot exists to hold.

**Retrieval is instrumented (the measurement seam), with the relevance fix built in.** Every `retrieve_design_insights` call logs one line to `.claude/hooks-audit/insights-retrieval.jsonl` (the probe in `heyhi-mcp`, `tools/insights.py`), each hit carrying `id` / `registry` / **`score`** — the relevance signal the corrections probe still lacks (it logs only `id` / `registry`). So "did a curated insight reach a later run, and how relevant was it?" is a recorded fact, not an assertion.

**The firewall (unchanged).** No agent writes any insight registry. An agent may OBSERVE a recurring finding and, via the `insight-activation` skill, file a CANDIDATE to `corrections-intake/` (an `insight-` filename prefix) — never here, never to a live registry. Only the instance owner promotes. See `corrections-intake/README.md` § Promoting an insight, and `plans/decision-register-sheerline-insight-registry-2026-09-13.md`.

**Cross-store links, not a shared file.** Corrections and insights share a search ENGINE's primitives, never a registry FILE. A nugget's `corroborated_by` / `contradicted_by` may reference ids in the corrections and method registries via a shared addressing convention — separation of governance, federation of retrieval.

---

*Runtime: the internal `heyhi-mcp` (`heyhi_mcp/corrections/insight_store.py`, `heyhi_mcp/tools/insights.py`, `heyhi_mcp/corrections/insight-schema.yaml`). Sibling convention: `os/corrections/`. Schema decision: `plans/decision-register-sheerline-insight-registry-2026-09-13.md`. Build spec: `plans/plan-sheerline-insight-registry-2026-09-12.md`.*

*HeyHi Confidential*
