---
classification: confidential
title: "Module 3.1 — RETRIEVE: the Design System MCP"
track: 3
module: "3.1"
level: advanced
prereqs: ["2.4"]
est_minutes: 30
teaches: sheerline
opens_files:
  - heyhi-mcp/heyhi_mcp/server.py
  - heyhi-mcp/heyhi_mcp/resources/summary.py
  - sheerline/os/foundations/design-systems/FOUNDATION.md
---

# Module 3.1 — RETRIEVE: the Design System MCP

## You are here

Track 2 placed Sheerline as a keel instance, walked its thirteen-area registry, and settled the two-axis conflict order. Track 3 opens the one module that is actually built end to end: the Design-Systems quality loop, area 7, the most-built area and not the whole practice. The loop runs four verbs, and this module is the first. The question it answers: how does an agent get a design system into a session without pasting it in? Previous: [module 2.4 in Track 2](../track-2-sheerline/module-2-4.md). Next: [`module-3-2.md`](module-3-2.md).

## Learning objectives

After this you can:

- Name the two always-loaded resources and the five tools of the Design System MCP, and say what each returns.
- Explain "retrieve, never paste" as Earn the Room's searchable load class made into a mechanism.
- Say why the design system is reached through the MCP as a boundary tool rather than embedded in `sheerline/`.
- Place RETRIEVE in the four-verb loop and name what it hands to the next verb.

## Concept

You met the four load classes in Track 1.2 and the reference-not-copy discipline in 2.3. RETRIEVE is where both become a running mechanism. A design system is the token, component, and pattern vocabulary a team designs against, and it is exactly the content Earn the Room files under **searchable, never pre-loaded**: too large to sit in every session, relevant one slice at a time. So the agent pulls the slice it needs at the moment it needs it, across a tool boundary, instead of carrying the whole system in context.

That boundary is the point, and it is the fourth invariant made concrete for the first time. Protocols at boundaries, not inside them: the design system is reached *through* the Design System MCP, a boundary tool, and never byte-copied into `sheerline/`. This is 2.3's byte-copy trap one level up. The corpus lives in one place; the MCP retrieves from it; nothing is duplicated. The foundation for area 7 says it plainly: the design system is retrieved, not pasted.

The MCP surface has two always-loaded resources and five tools. The resources are the standing context every design session opens with. `design-system://summary` is the meaning layer over the token and component set, and it carries the active corrections fold you will meet in 3.4. `design-system://fundamentals` is the universal reasoning layer: the conflict order you learned in 2.4, the binding interaction laws, and the control-state contract. Read the summary first for the token and component vocabulary, the fundamentals second for the structural principles that fill what the design system leaves silent.

The five tools are the on-request surface. `retrieve_design_context` runs a vector search over the indexed design-system documentation and returns token values, component specs, and patterns for a query. `validate_output` checks an emitted artifact against the system and returns findings, which is the next verb, so it lives on this surface but belongs to 3.2. `retrieve_design_relationships` walks the token-to-component graph for impact and dependency questions. `retrieve_design_examples` returns curated worked examples, distinct from documentation retrieval. `retrieve_design_corrections` answers "what have we been told about this?", which is the learn verb, 3.4. The published scaffold of this server is one resource and four tools; the live internal subsystem adds the fundamentals resource and the corrections tool, so its counts run ahead of the public document, a gap that returns as the moat in Track 4.

Hold the loop in view. RETRIEVE hands the retrieved system to VALIDATE, which grades emitted output against it; GRADE scores that over time; LEARN folds a correction back into the summary, so the next retrieval already carries what the last session learned. The verb you are reading is the one that makes the other three possible.

## Walkthrough

Open `heyhi-mcp/heyhi_mcp/server.py`. Read the module docstring first: it maps every resource and tool to the file that implements it and states that this file "holds no business logic of its own", the boundary wired to its implementations. Read the `FastMCP` instructions block and notice the ordering rule it hands every client: read the summary first, then the fundamentals. Now read the five `@mcp.tool()` signatures and their docstrings. Each returns a `dict`; note that `validate_output` advertises "runs outside the model, no token cost", which is the seam into 3.2.

Open `heyhi-mcp/heyhi_mcp/resources/summary.py` and find `get_summary_bundle`: the served resource is the summary file plus the active-corrections fold. Read `_neutralize` and notice the bound on a folded correction, so an injected line cannot restructure the always-loaded bundle. Then open `sheerline/os/foundations/design-systems/FOUNDATION.md` and read "reached through the MCP boundary": the subsystem is referenced, never embedded, and the retrieval tools are "searchable, never pre-loaded" realized.

## Lab

Open `heyhi-mcp/heyhi_mcp/server.py` and read the five `@mcp.tool()` signatures top to bottom. For each tool, write its name, what it returns, and its one-line job. Then, from the same file's resource definitions, write the one sentence that says why the design system is retrieved through this server rather than pasted into the session.

**Success looks like:** five tools named with their return type and purpose (for example, `retrieve_design_context` returns markdown token and spec chunks for a query), plus a sentence naming both reasons the system is retrieved rather than pasted: it is Earn the Room's searchable class, and the MCP is the boundary tool of invariant 4.

## Common misreads

- *"The MCP is the design system."* No. It is the boundary tool that retrieves it. The system is the token and component corpus, referenced in place, one copy.
- *"Read the summary to get token values."* The summary is the meaning layer. Concrete values come from `retrieve_design_context`, the searchable tool, not the always-loaded bundle.
- *"Five tools, five kinds of retrieval."* No. `validate_output` is the validate verb and `retrieve_design_corrections` is the learn verb. The surface spans the whole loop, not just RETRIEVE.
- *"Both resources are conveniences you can skip."* No. Both are always-loaded, and the fundamentals resource is the second standing surface, read right after the summary.

## Self-check

1. Name the two resources and the five tools, and say what each tool returns.
2. Why is the design system retrieved through the MCP rather than embedded in `sheerline/`?
3. Which load class is the token and component data, and why that one?
4. From the Lab: your five-tool inventory and the one-sentence retrieve-not-paste answer.

## Go deeper

- `heyhi-mcp/heyhi_mcp/server.py`: the whole MCP surface, two resources and five tools, wired to their implementations.
- `sheerline/os/foundations/design-systems/FOUNDATION.md`: the nested subsystem reached through the boundary, and its loading rules.
- Architecture figure 4, [`../../docs/architecture.md`](../../docs/architecture.md), draws the four-verb loop this track walks.
- Protocols at boundaries is the fourth invariant from module [0.3](../track-0-orientation/module-0-3.md); VALIDATE is 3.2, GRADE is 3.3, LEARN is 3.4.

---

*HeyHi Confidential*
