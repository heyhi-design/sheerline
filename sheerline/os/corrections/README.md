---
classification: confidential
title: "Sheerline corrections: the convention slot"
---

# Sheerline corrections: the convention slot

This directory is the **convention** for how corrections work in Sheerline: the lifecycle (`LIFECYCLE.md`) and a generic-factual seed template (`seed-corrections.yaml`). It is modeled on `releases/open-source/keel/os/corrections/`.

**The runtime lives elsewhere. Build no runtime here.** The design-corrections *runtime* (the "learn" verb: the vendored `agent-corrections` mechanism, the schema extension, the readers, the conformance-lane enforcement, and the populated registry) lands in the internal **`heyhi-mcp`** in **Phase 2 (DISPATCH-02)**, not in `sheerline/`. This slot is the convention and the seed template; it references that runtime by name. The populated per-design-system corrections corpus and its promotion judgment are the retained moat (`os/operating-principles.md` § IP boundary) and are never bundled here.

**The two hard automation tightenings** (carried by the runtime, stated here as the convention's boundary): only `factual` corrections are injected or enforced; `behavioral` corrections surface to the human as a reminder to decide and are **never** promotable to an auto-enforced rule. A taste correction hardening into an enforced check is the boundary collapsing.

**Retrieval is instrumented (the measurement seam).** The runtime is wired to log every Step-0 corrections retrieval to `.claude/hooks-audit/corrections-retrieval.jsonl` (the probe in `heyhi-mcp`, `corrections.py`), so the "gets better from use" claim can carry a probe rather than an assertion: which correction was retrieved, for which task, becomes a recorded fact the next harvest can read. Like the rest of the runtime, the probe is a Layer-1 instrument reached through the `heyhi-mcp` boundary, not built here; this slot only names it. That retrieval record is the evidence base for the learn and grade verbs the moat rests on.

---

*Lifecycle: `os/corrections/LIFECYCLE.md` · Seed template: `os/corrections/seed-corrections.yaml` · Runtime: the internal `heyhi-mcp` (Phase 2 / DISPATCH-02).*

*HeyHi Confidential*
