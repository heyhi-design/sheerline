---
classification: confidential
title: "Sheerline Skills"
---

# Sheerline Skills

Sheerline reuses keel's skill mechanism (the registry engine, the SKILL.md / reference split, the eval-case scaffold) and points it at HeyHi's deployed design skills. In Phase 1 it authors **zero net-new skills**: it governs the design-practice skills HeyHi already has, and tracks the gaps as states.

- **`registry/`**: the reused keel registry engine (`skill-registry.py`, R2) plus the design-scoped `skill-registry.yaml` that indexes the 13 areas and the deployed design-practice skills. Honest abstention is built in: the confidence gate returns `insufficient` on an out-of-scope query.
- **`templates/`**: **pointers** to HeyHi's existing design skills in `heyhi-skills/` (referenced, never copied). Not filled skill templates.
- **`evals/`**: the per-skill eval-case scaffold (the R4 pattern): a `cases.yaml` per governed capability, run by hand or by the agent, judged against `pass_criteria`.

## Routing

Before loading any skill, run the registry:

```bash
cd skills/registry && python3 skill-registry.py "<the task>" --confidence
```

Load only the top skill when the gate reports `confident`. When it reports `ambiguous`, surface both candidates to the human. When it reports `insufficient`, abstain: no capability clearly matches.

## When a net-new skill earns existence (P1.5 onward)

Phase 1 authors none. From P1.5, a net-new skill earns its place only when it does mechanical work a designer genuinely offloads (structure, capture, audit, hygiene), never when it restructures a judgment the designer must make. Every net-new skill obeys the boundary spec (`os/operating-principles.md`): a structured artifact with explicit empty judgment slots, a named human gate, and provenance labels on anything synthetic. A capability that fills its own judgment slot has exceeded its charter.

---

*Registry: `skills/registry/README.md` · Area map: `os/foundations/registry.yaml`*

*HeyHi Confidential*
