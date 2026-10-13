# HeyHi Design Intelligence Audit: Reference

*Companion to SKILL.md. Pull this before running an audit — it has the templates, interview guides, and report structure you need.*

---

## Pre-Work Request Template

Send this to the client before the audit session.

---

**Before we meet:**

To make the most of our time together, it would help to have access to the following before we start:

- **Figma:** View access to your main design library file (viewer role is fine)
- **Codebase:** Access to your component library or frontend repo — read-only access, GitHub or exported files both work
- **Documentation:** Any existing design system docs — Storybook, Confluence, Notion, or a link to whatever exists
- **15 minutes each:** A brief call with the lead designer and the lead engineer before the audit day — separately if possible

If any of these aren't available or require more setup, let me know and we'll work with what we have.

---

## Interview Question Sets

Run these before or at the start of the audit session. Take notes. The answers shape how you interpret what you find.

### Designer Interview (15 min)

1. When do you reach for the design system vs. build something new? What makes you choose one over the other?
2. What's the last component you had to build outside the system because it didn't exist or wasn't right?
3. When you hand off to engineering, how confident are you that what you've designed matches what will be built?
4. What's one thing about the system you'd change if you could change it tomorrow?
5. Who owns the design system right now? How does that feel?
6. When did the system last feel like it was working well? What was different then?

### Engineer Interview (15 min)

1. How do you find out what components are available? Is the answer reliable?
2. When you look at a Figma file, how much of what you see maps cleanly to something you can build from the component library?
3. When do you use the design system vs. write something custom? What drives that decision?
4. What's the most common disconnect between what's in Figma and what you end up shipping?
5. If you need to add a new component or variant, what's the process?
6. What would make the design system more useful to you specifically?

---

## Audit Session Agenda (Full Day)

**9:00 — 9:15** Pre-audit scan. Run Design Lint on the primary component frames. Scan takes ~10–15 minutes. Document findings by category and count (hardcoded fill/stroke, missing style bindings, etc.). This becomes input to Area 4 (Figma File Health).

**9:15 — 9:30** Kickoff with the team. Scope and goals for the day. What success looks like. Share Design Lint findings from the pre-scan.

**9:30 — 10:30** Token Architecture (Area 1). Work through token layer with designer.

**10:30 — 11:30** Component Coverage (Area 2). Systematic comparison — Figma library vs. codebase.

**11:30 — 12:00** Figma File Health (Area 4). Assess file structure, naming, detached instances. (Note: Design Lint findings already surfaced in kickoff; use them to focus this section.)

**12:00 — 1:00** Break.

**1:00 — 2:00** Documentation and Governance (Area 3). Walk through existing docs. Test knowledge: ask the engineer to find usage guidance for a specific component.

**2:00 — 2:45** Accessibility Baseline (Area 5). Spot-check with tools. Sample key flows.

**2:45 — 3:30** Team Relationship (Area 6). Facilitated conversation. Use interview questions as guide.

**3:30 — 4:00** Synthesis and readout framing. What the report will say. Any clarifying questions before writing.

---

## Half-Day Agenda (Compressed Audit)

**9:00 — 9:10** Pre-audit scan. Run Design Lint on primary components. Document findings by category.

**9:10 — 9:15** Kickoff (brief, given the time constraint)

**9:15 — 10:00** Token Architecture + Component Coverage (Areas 1 & 2, high-level). Use Design Lint findings to focus questions on hardcoded values.

**10:00 — 10:30** Figma File Health + Documentation spot-check (Areas 4 & 3, rapid)

**10:30 — 11:00** Team Relationship (Area 6) — this one is non-negotiable even in compressed audits

**11:00 — 11:30** Accessibility Baseline (Area 5, spot-check only)

**11:30 — 12:00** Synthesis, open questions, path forward conversation

---

## Figma Professional Integration

*Established by Work Block 5, Workstream A (tests T2.1–T2.4, executed 2026-03-16). Source of record: `ai-services/design-intelligence/test-system.md`. This is the capability line for running audits on Professional-plan Figma, which is the majority of the market. The SKILL.md Areas 1, 2, 4, and 7 carry the per-area MCP paths; this section is the cross-area capability line, the linter method, the call budget, and the Code Connect workaround.*

### The capability line: Professional vs. Enterprise

Most clients run Figma Professional, not Enterprise. The audit runs fully on Professional. Be precise about what each tier provides, and never scope a deliverable that depends on a tier the client does not have.

| Capability | Professional | Enterprise (adds) |
|---|---|---|
| Plugin API (read variables in an active session) | ✓ | ✓ |
| Check Designs linter | ✓ | ✓ |
| Figma MCP `get_variable_defs` / `get_design_context` / `search_design_system` | ✓ | ✓ |
| MCP call budget | 200 / day | 600 / day |
| Modes per collection | up to 10 | more |
| Variable export to JSON | community plugin (variables2json, Console MCP bridge) | REST API (headless) |
| Code Connect + its MCP tools (`get_code_connect_map`) | ✗ | ✓ (Org/Enterprise + Dev seat) |
| Extended Variable Collections (multi-brand inheritance) | ✗ | ✓ |
| Library Analytics API | ✗ | ✓ |

The honest version for clients: "We run the full audit on your Professional plan. Two capabilities, headless variable extraction and Code Connect, need Enterprise. Neither blocks the audit, and we have a workaround for each."

### Check Designs as the pre-audit first pass (T2.2)

Figma's native Check Designs, and the community Design Lint plugin, is a read-only linter built into the editor. Run it first (it is already the 9:00 pre-audit scan in both agendas above). It catches the mechanical layer fast, which frees the audit to go where tooling cannot.

On one client test system, Check Designs surfaced 6 errors on the Button CTA, all "Missing fill style #ffffff" in the Focused variants. That is a real but narrow class: unlinked fills. It does not see semantic misuse, missing variants, governance, accessibility intent, or the team's relationship to the system. That gap is the audit.

| Issue category | Check Designs catches | HeyHi audit catches |
|---|---|---|
| Hardcoded fill / stroke / unlinked style | ✓ | ✓ |
| Hardcoded spacing | partial | ✓ |
| Wrong semantic token usage | ✗ | ✓ |
| Token naming quality | ✗ | ✓ |
| Detached instances | partial | ✓ |
| Missing component variants | ✗ | ✓ |
| Cross-file / cross-library consistency | ✗ | ✓ |
| Accessibility violations (contrast, focus, target) | ✗ | ✓ |
| Governance gaps | ✗ | ✓ |
| Team relationship | ✗ | ✓ |

The narrative for clients: "We use Figma's own linter as a first pass for the mechanical issues, then go deeper into the areas it cannot reach: semantics, coverage, governance, and how your team actually uses the system." Practically, Check Designs compresses Area 4 (Figma File Health), which frees time for Areas 1, 2, 3, and 6.

### MCP call budget (T2.3)

`get_variable_defs` on Professional draws against a 200 calls/day limit. A single component selection costs about 1 call; a frame of 10 to 20 components is still about 1 call against the selection. The firm finding from T2.3: **200/day is sufficient for Professional-plan audits of up to about 150 components in a day.** Above that (very large systems, or an automated drift sweep across the whole library), the 200/day limit bites and Enterprise (600/day) is the answer.

Illustrative budget for a typical engagement, derived from the per-frame cost (not a recorded T2.3 figure):

- **Half-day audit:** on the order of 20 to 40 MCP calls. Well inside 200/day.
- **Full-day audit:** on the order of 40 to 80 MCP calls. Inside 200/day.

Practical rule: select frames, not individual components. One `get_variable_defs` call on a frame returns the variables for everything in the selection. Note in the report's methodology section that extraction was automated (a credibility signal with engineering audiences) and which plan tier was used.

### Code Connect: the Professional workaround (T2.4)

Code Connect and its MCP tools (`get_code_connect_map`, `get_code_connect_suggestions`) require an Organization or Enterprise plan with a Dev seat. They are not available on Professional. T2.4 confirmed this and moved Code Connect to the Enterprise tier. Do not let the SKILL.md Area 4 MCP path mislead you here: on Professional, that path is unavailable and the manual fallback applies.

What this means for a Professional-plan audit:

- **Do not promise** Code Connect mapping, stale-mapping detection, or Figma-to-code semantic linking as a deliverable. That is an Enterprise capability HeyHi cannot run on the client's plan.
- **Area 4 fallback:** assess Code Connect status by observation. If it is not configured (the normal case on Professional), flag the absence as a finding framed as "Figma and code are not semantically linked," not as a plan-tier gap to fix inside this engagement.
- **The workaround:** HeyHi's own test system (`heyhi-design-intelligence-tests`) carries the Code Connect reference implementation. It shows the client what good looks like and seeds the setup guide for a future Build engagement, without requiring the client's file to be Enterprise. Use it to demonstrate the target state; do not attempt to write Code Connect into their Professional file.
- If Code Connect is genuinely needed, that is an Enterprise upgrade conversation and a Design System Build deliverable, not part of the Professional-plan audit.

---

## Severity Rubric

### Critical

Active harm being done. The system is failing in ways that are showing up in the product or in the team.

Language examples:
- "The token architecture doesn't exist in code. Designers are using the Figma system; engineers are hardcoding values. The system and the product have already diverged."
- "The component library hasn't been updated in 14 months. Two major product features were built with custom components that don't exist in the library. The system no longer reflects the product."
- "There is no named owner. System decisions are made by whoever asks loudest. This is causing visible inconsistencies across product surfaces."

### High

Significant drift that will compound. Not yet causing visible product failures, but getting expensive to address the longer it waits.

Language examples:
- "Token coverage is partial. About 60% of design decisions are token-backed; the rest are hardcoded. Every month of product development widens this gap."
- "Figma and code cover different component sets. Designers are designing with components that don't exist in code, then negotiating with engineering on every handoff."
- "No contribution process exists. Components get added ad hoc. There are three versions of a date picker across different product areas."

### Medium

Real problems that are manageable now but will require attention before the next major system change.

Language examples:
- "Documentation exists but is acknowledged as out of date by both the design and engineering teams. It covers the original system, not the current one."
- "Figma file uses mostly variables, but roughly 30% of components have hardcoded styles. The drift is not systematic — it's accumulated from individual decisions."
- "Governance is informal but functional. The current approach works because the team is small. It will break when the team grows or when a second designer joins."

### Low

Best-practice gaps. Worth addressing, but not urgent. Good candidates for the first sprint of a Design System Care retainer.

Language examples:
- "Token naming is functional but not semantic. Values are named by appearance ("gray-200") rather than role ("color-border-subtle"). This is workable but will create friction as the system grows."
- "Figma layer naming is inconsistent. This slows handoff but doesn't cause errors."
- "No formal deprecation process. Old components linger in the library but aren't actively causing problems."

---

## Audit Report Template

---

**[Client Name] — Design System Audit**
*HeyHi · [Month Year]*

---

### The Short Version

*3–5 sentences. The overall diagnosis. Written for whoever is reading this first — if that's leadership, write for outcomes; if it's the team, write for specifics. One clear statement of what the audit found and what it means.*

> Example: "The design system has real foundations — the token structure exists, the component coverage is substantial, and the team wants to use it. The problem is the gap between Figma and code has been widening quietly for about eight months, and it's now wide enough that handoffs require negotiation on every feature. That gap is the central finding of this audit. Everything else follows from it."

---

### Findings

*One section per examination area. Not every area will have findings worth reporting — skip or combine if thin.*

---

#### Token Architecture

**What we found:** [Plain language description of what's there and what isn't.]

**Severity:** [Critical / High / Medium / Low]

**Why it matters:** [What this costs the team in concrete terms — time, inconsistency, handoff friction.]

**Next step:** [One specific, concrete action.]

---

#### Component Coverage

**What we found:** [...]

**Severity:** [...]

**Why it matters:** [...]

**Next step:** [...]

---

#### Documentation and Governance

**What we found:** [...]

**Severity:** [...]

**Why it matters:** [...]

**Next step:** [...]

---

#### Figma File Health

**What we found:** [...]

**Severity:** [...]

**Why it matters:** [...]

**Next step:** [...]

---

#### Accessibility Baseline

**What we found:** [...]

**Severity:** [Note: this was a spot-check. Flag if a full audit is recommended.]

**Why it matters:** [...]

**Next step:** [...]

---

#### Team Relationship to the System

**What we found:** [Qualitative summary from interviews and observation.]

**Why it matters:** [Often the most important section. Name what the team dynamic means for any future system work.]

---

#### Agent Interface Readiness *(Include only when `agent_readiness_add_on: true`)*

**ARI Score: [X.XX / 4.0] — Dimension 7: Level [N]**

| Sub-area | Score | Notes |
|----------|-------|-------|
| 7.1 Semantic Token Depth | [1–4] | |
| 7.2 Component Catalog Structure | [1–4] | |
| 7.3 HITL Checkpoint Coverage | [1–4] | |
| 7.4 Layer 0 Signal | [1–4] | |

**[Opening framing paragraph — use the standard framing from the Area 7 block in SKILL.md]**

**[Score-specific framing — match to ARI composite level; all four score bands and the retainer pivot are in SKILL.md § ARI Findings Language]**

**Path to Level [N+1]:** [Specific steps ordered by impact, grounded in the sub-area findings]

**Coverage note:** If Area 7 ran the `get_variable_defs` MCP path for 7.1 or the `search_design_system` path for 7.2, note it in the methodology section: "Agent Interface Readiness token assessment was performed via automated scan of the client's Figma variable definitions." This is a credibility signal with engineering audiences.

---

### The Path Forward

*One paragraph. What the audit recommends as the next engagement and why. Specific to what was found — not a generic upsell.*

*If a Design System Care retainer is appropriate:*
> "The system has good bones. What it needs is consistent attention — monthly component audits, token maintenance as the product evolves, and a standing relationship that keeps the Figma file and the codebase from drifting further apart. That's what a Design System Care retainer provides."

*If a Build engagement is appropriate:*
> "The audit surfaced structural issues that maintenance can't fix. The token architecture needs to be rebuilt with a proper semantic layer, and the component coverage needs to be reconciled against what the product actually requires. That's a Build engagement. The audit gives us the foundation — we know exactly what exists, what's missing, and what needs to change. The build scope comes directly from these findings."

*If Org Consulting is the real next step:*
> "The system's technical issues are real but secondary. The primary problem is ownership and governance — decisions aren't being made, contributions aren't being reviewed, and no one feels accountable for the system's health. Building a better token architecture won't fix that. The right starting point is an Org Consulting engagement focused on how the team structures responsibility for shared infrastructure."

---

*Prepared by HeyHi · [Date]*
*For questions or to discuss next steps: [Auditor contact]*

---

## Findings Language Guide

Technical findings need to be translated for non-technical readers without losing accuracy. The goal is specific and plain — not dumbed down, not jargon-heavy.

| Instead of | Write |
|---|---|
| "The token system lacks a semantic abstraction layer" | "Token names describe what things look like, not what they're for. 'blue-500' instead of 'color-action-primary'. This makes the system harder to maintain when the brand changes." |
| "Component props are not consistent across variants" | "The button component has different prop names in Figma than in code. Designers and engineers are looking at different things when they talk about the same component." |
| "No CI/CD validation for token compliance" | "Nothing checks automatically whether new code is using the design tokens. Violations only get caught if someone notices." |
| "Figma instances are detached from library components" | "Designers have been modifying library components directly in their design files. Those modifications don't update when the library changes, so they're working with a private version of the system." |
| "Governance process is undocumented" | "There's no written process for how new components get added, who approves them, or how old ones get retired. Right now that knowledge lives in a few people's heads." |

---

*Companion to heyhi-design-intelligence-audit/SKILL.md*
*Cross-reference: ai-services/design-intelligence/README.md · ai-services/_core/ai-service-offerings.md*

*HeyHi Confidential*
