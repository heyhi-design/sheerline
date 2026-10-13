---
name: motion-system-author
description: >-
  Author a client motion-token system and its component motion specs, or translate a Figma
  Motion / Rive export into a token-mapped handoff spec. Two modes over one motion model.
  Author assembles springs (spatial and effects, across three speeds) with a duration-plus-
  easing fallback, stagger tokens, and a mandatory prefers-reduced-motion variant, from a
  motion personality the human states, and documents the DTCG motion standards gap in every
  output. Translate ingests a Figma Motion timeline (via get_motion_context or an exported
  CSS/JSON/React file) or a Rive export, lints off-system values, and produces the token-
  mapped spec. Triggers: "author a motion system", "build motion tokens", "spring token
  system", "motion spec for handoff", "translate this Figma Motion export to motion tokens".
  The motion personality, the restraint call, and the "does it feel right" verdict stay human
  (empty slots behind a named gate). NOT for building an interface or prototype (use
  heyhi-ui-ux for HeyHi pages, ui-studio for client UI); this authors the motion-token SYSTEM,
  not the screens that consume it. NOT for translating a whole prototype or raster into a Figma
  design file (use heyhi-design-bridge; this is motion-specific and shares only the Translate
  mechanic). NOT for auditing whether a built prototype's interactions are complete (use
  heyhi-prototype-audit). Sheerline area 4 (Interaction Design).
version: "0.1.1"
updated: "2026-09-05"
status: "Deployed — heyhi-skills/motion-system-author/; registered in the main + Sheerline subset registries (Sheerline Wave G-4, 2026-08-28). Net-new, effectively (no heyhi-motion-system-author candidate exists in the tree). Sheerline area 4 (Interaction Design), P3. Spec: sheerline-skill-buildout-research-2026-08-09.md § 4.2. Boundary: § 9."
classification: HeyHi Confidential
---

# Motion System Author

**Sheerline area 4 (Interaction Design) · P3 · dual-mode generate + translate.** A client needs a motion-token system: the springs, durations, easings, stagger, and reduced-motion behavior that make interface motion consistent, plus the per-component specs that say how each element moves. Or a designer has already animated something in Figma Motion or Rive and needs it turned into a token-mapped handoff a developer can build against. This skill does both, over one shared motion model. It assembles and lints the plumbing; the human keeps the personality, the restraint, and the read of whether it feels right.

**The boundary this skill obeys (Sheerline § 9, absolute).** A structured artifact with explicit empty judgment slots, a named human gate, and provenance labels on anything synthetic. *The motion personality, the restraint call, and the "does it feel right" verdict are the empty slots.* Assembling the token model from a stated personality, drafting candidate spring parameters, generating the mandatory reduced-motion variant, and linting an export for off-system values are mechanical. Deciding what the motion should feel like, how much of it to spend, where to hold back, and whether the result lands is judgment. A version of this skill that invents the motion personality, or auto-approves "it feels right," has exceeded its charter. Grades never gates; mechanics never taste.

> **This skill closes through the Exit Gate (`CLAUDE-SESSION-RULES.md § Exit Gate`).** See the bottom-of-skill bracket.

---

## Routing: disambiguation with sibling skills

| If the task is… | Use |
|---|---|
| "Author a motion-token system / build motion tokens / spring token system / motion spec for handoff" | **this skill (Author)** |
| "Translate this Figma Motion (or Rive) export into motion tokens" | **this skill (Translate)** |
| Build a HeyHi page or component that *consumes* motion | `heyhi-ui-ux` |
| Build a client interface or prototype that *consumes* motion | `ui-studio` |
| Translate a whole HTML prototype or a raster into a Figma design file | `heyhi-design-bridge` (shares only the Translate mechanic; keep the seam clean) |
| Audit whether a built prototype's interactions are complete | `heyhi-prototype-audit` |
| Decide the motion personality, the restraint, or whether it feels right | **the human** (this skill's named gate) |

The seam with `heyhi-design-bridge` is scope: design-bridge translates a whole prototype or raster into a Figma design file; this skill translates the *motion layer only*, into tokens. The seam with `heyhi-ui-ux` / `ui-studio` is object: they build the screens; this authors the motion-token system those screens reference. The seam with `heyhi-prototype-audit` is direction: it audits a built artifact for completeness; this authors the system upstream of the build.

---

## Foundation note (area 4, governed)

Area 4's foundation is `governance` in `sheerline/os/foundations/registry.yaml`: `sheerline/os/foundations/interaction-design/FOUNDATION.md` (authored 2026-09-05, the P3 fill) registers this skill under area 4. Load it before Step 1 (Route to a mode) as the governed context, alongside the corrections hook in Step 0; it points at the **control-state contract** (default / hover / focus-visible / active / disabled / loading / error + success / selected), adopted as Increment A A.3 (`ai-services/design-intelligence/research/design-fundamentals-decision-research-2026-08-12.md`) and served as `design-system://fundamentals`. Component motion specs (Mode A, Step A4) key off that state set; do not re-derive it here. The spec source stays `ai-services/design-intelligence/research/sheerline-skill-buildout-research-2026-08-09.md` § 4.2. The structural inventory of *which* states and transitions an element has is `interaction-inventory`'s (this skill gives the transition its motion; that one names it).

---

## The motion model (both modes share it)

The model has four token groups plus a mandatory variant. Full schema, value examples, and the DTCG note are in `references/motion-token-schema.md`; the summary:

1. **Springs (the primary model, not duration+easing).** Two spring *categories* across three speeds each (M3 Expressive):
   - **Spatial springs**: motion that changes an element's position or size. May overshoot slightly (a small bounce reads as physical).
   - **Effects springs**: motion for color, opacity, and other non-spatial properties. No overshoot (overshoot on opacity reads as a flicker).
   - Three speeds per category (fast / default / slow), each expressed as spring parameters (stiffness, damping, mass), not a duration.
2. **Duration + easing fallback.** The classic token pair (duration scale + named easing curves) for any consumer that cannot express a spring: a CSS transition, a platform without a spring primitive, a documentation table. Every spring token carries a fallback so the system degrades honestly rather than silently dropping motion.
3. **Stagger tokens.** Sequenced entrance delays for lists, grids, and grouped reveals (tight / default / loose).
4. **Reduced-motion variant (MANDATORY).** Every emitted set includes a `prefers-reduced-motion` behavior. See the mandate below.

---

## The reduced-motion mandate (non-negotiable)

**No motion set ships without its `prefers-reduced-motion` fallback.** For each token group and each component spec, the emitted artifact states what happens when the user (or the OS) requests reduced motion: typically a cross-fade or an instant transition in place of spatial movement, spatial springs collapsed to an opacity change, stagger removed, parallax and large-travel motion disabled. This is not an accessibility nice-to-have layered on later; it is part of the token by construction. Author-mode output with a spring token but no reduced-motion counterpart is incomplete and fails the smoke test. Translate-mode output must flag any animation in the export that has no reduced-motion path.

---

## Step 0: Improvement hook check

Retrieve any recurring corrections for motion / interaction work (`retrieve_design_corrections` or the Sheerline `os/corrections/` registry). Fold a match into the pass. Skip silently if none.

## Step 1: Route to a mode

- **Author**: assemble a motion-token system from a stated personality. Triggers: "author a motion system", "build motion tokens", "spring token system", "motion spec for handoff".
- **Translate**: turn a Figma Motion or Rive export into a token-mapped spec. Triggers: "translate this Figma Motion export", "turn this Rive animation into tokens", "map these animations to our motion system".

If both are wanted (author the system, then map an existing export onto it), run Author first so Translate has a system to lint against.

---

## Mode A: Author

Input: a **stated motion personality** (the human's words for how motion should feel, for example "calm and deliberate, motion earns its place"; "quick and confident"; "playful, with a little bounce on entrances"). Output: a motion-token artifact (the four groups + reduced-motion), component motion specs, and the DTCG-gap note, with the judgment slots empty.

### Step A1: Take the personality as input, never invent it

The motion personality is a **human input**, not an agent decision (§ 9). Read it from what the human stated (a style brief's motion line, a direct instruction, an approved direction). If no personality is stated, **do not choose one**. Surface the empty slot and ask the human to state it in one or two phrases, then proceed. Record the personality verbatim in the artifact as the human-owned input it is. This skill takes a stated personality; it does not read a HeyHi `motion_personality` field or any other system's fixed pair. It is client-agnostic by construction.

### Step A2: Assemble the token model, mechanically

From the stated personality, draft the four token groups (schema in `references/motion-token-schema.md`). Each value is a **candidate**, labeled so:

1. **Springs**: spatial and effects categories, three speeds each, as spring parameters. Let the stated personality bias the parameters (a "calm" personality drafts higher damping and slower speeds; a "playful" one drafts lower damping on the *spatial* springs so entrances carry a little overshoot, effects springs staying critically damped regardless). The mapping from personality-words to parameter ranges is drafting, not deciding: it widens the human's starting point, it does not lock the feel.
2. **Duration + easing fallback**: a duration scale and named easing curves, each spring token cross-referenced to its fallback.
3. **Stagger**: tight / default / loose.
4. **Reduced-motion variant**: the mandatory counterpart for every group (see the mandate).

Every drafted value carries a provenance label (`candidate (agent-drafted)`). Nothing here is the final feel.

### Step A3: Document the DTCG standards gap in the output

The output must state the standards gap plainly, because a reader will assume "design tokens" means a ratified format and motion has none. Include this in the artifact (wording in `references/motion-token-schema.md § DTCG gap`): the stable DTCG spec (2025.10) defines **no first-class motion types** (springs, keyframes, and transitions are unspecified), so mature systems hand-roll their own motion tokens (M3, Carbon, Polaris each define bespoke shapes). This system therefore emits a **documented house schema**, not standard DTCG motion tokens, and says so. Silence here is a defect: an undocumented house schema reads as if it were a standard, and it is not.

### Step A4: Component motion specs

For each interactive component the engagement covers, specify how it moves, keyed to the control-state contract (default / hover / focus-visible / active / disabled / loading / error + success / selected, the A.3 set named in the foundation note). Map each state transition and each entrance/exit to a token from Step A2, and state the reduced-motion behavior for each. Worked component table (button, card, modal, list load, page transition, toast) in `references/motion-token-schema.md § Component specs`. Which components are in scope, and which transitions actually matter, is a human read. Draft the full set and let the human prune.

### Step A5: Produce the artifact

Output this structure. The personality is the human's stated input; the restraint and feel slots stay empty by construction.

```
# Motion System: [engagement label]
Personality (HUMAN-STATED INPUT): "[verbatim]"      Authored: [date]

## Standards note
[The DTCG motion-gap paragraph: this is a documented house schema, not standard DTCG motion tokens.]

## Tokens
### Springs (spatial / effects × fast / default / slow)   [all values: candidate (agent-drafted)]
### Duration + easing fallback                             [candidate (agent-drafted)]
### Stagger                                                [candidate (agent-drafted)]
### Reduced-motion variant (MANDATORY, one per group)     [candidate (agent-drafted)]

## Component motion specs
[table: component × state/transition → token, + reduced-motion behavior per row]

## Restraint notes (candidate observations, not verdicts)
[Where the system offers more motion than a surface may need; questions, not cuts.
 e.g. "The stagger-loose token exists; whether the results list should stagger at all
 is a restraint call for you."]

## ⛔ Motion personality: HUMAN-OWNED
The personality above is the human's stated input, recorded verbatim. If it was
not stated, this slot is blank and the system is NOT authored until it is filled.
   Stated personality: ____________________

## ⛔ Restraint + "does it feel right": NEEDS HUMAN
These slots are intentionally empty. How much motion to spend, where to hold back,
and whether the assembled system lands are human reads, made in motion, not on paper.
   Restraint decisions (what to cut / hold): ____________________
   Feel sign-off (prototype reviewed in motion): ____________________

## Named gate
Sign-off owner (design lead / motion owner): ____________________  Date: ______
No motion system is adopted until this line is signed by a human who has seen it move.
```

**Author output is done when** every token group has candidate values, every group and every component row has a reduced-motion counterpart, the DTCG note is present, every value is provenance-labeled, and the personality/restraint/feel slots are handled per the rules above (personality recorded or flagged blank; restraint + feel empty).

---

## Mode B: Translate

Input: a **Figma Motion export** or a **Rive export**. Output: a token-mapped handoff spec: each animation resolved to a token where it maps, off-system values flagged, and a reduced-motion gap list. Mapping details and the export formats are in `references/translate-mapping.md`.

### Step B1: Ingest the export

- **Figma Motion.** The read path is the Figma MCP `get_motion_context` tool against the file/frame, or a developer-supplied export (Figma Motion is Dev-Mode-inspectable and exports CSS / JSON / React). Aug-2026 substrate: Figma Motion is a timeline model, Dev-Mode-inspectable, with a CSS/JSON/React export and MCP passthrough. Confirm the connection (`whoami`) before a live read; if only an exported file is provided, parse that.
- **Rive.** Parse the Rive export (state machines; the Rive Editor MCP is in early access per the Aug-2026 spec, so a file export is the reliable path). Read the state machine's transitions and their timing.

Do not write to Figma in this mode. Translate reads the motion and emits a spec; it does not modify the source.

### Step B2: Lint off-system values

Compare every animated value in the export against the target motion system (the Author-mode system if one exists, or the token model's expected shape). Flag, with provenance:

- A duration that is not on the duration scale (a bespoke 237ms where the scale has 250ms).
- An easing curve that is not a named token (an ad-hoc cubic-bezier).
- A spring whose parameters match no spring token, or a spring used where the category is wrong (a spatial-style overshoot applied to opacity).
- An animation with **no reduced-motion path** (the mandate applied to translation).
- Any value the export carries that the token model cannot express (flag it, never drop it silently).

Each finding is `off-system` with the source value and the nearest token, so the human can decide: snap to the token, or extend the system. The skill flags; it does not silently rewrite the designer's motion.

### Step B3: Generate the token-mapped handoff spec

Produce the spec: each animation → its resolved token (or `off-system` flag), the fallback duration/easing for consumers that cannot express the spring, the reduced-motion behavior (or a gap flag), and a provenance label on every row (`from-export` for values read from the source, `agent-derived` for anything the mapping inferred). Close with the same empty judgment slots and named gate. Whether an off-system value is a bug to snap or an intentional flourish to keep is the human's restraint-and-feel call.

```
# Motion Translate: [engagement label]
Source: [Figma Motion frame / Rive file]      Translated: [date]

## Standards note
[The same DTCG motion-gap paragraph: the emitted tokens are a documented house schema.]

## Animation → token map
| Animation | Source value (from-export) | Resolved token | Fallback (dur+easing) | Reduced-motion | Provenance |
|---|---|---|---|---|---|
| card entrance | spring s240 d26 | spring.spatial.default | 250ms / emphasized-decelerate | cross-fade | from-export |
| … | … | off-system (flagged) | … | GAP: none in export | from-export |

## Off-system findings (flag, do not rewrite)
[each: source value, nearest token, why it is off-system]

## Reduced-motion gaps
[animations in the export with no reduced-motion path: the mandate applied to the source]

## ⛔ Snap vs keep: NEEDS HUMAN
Each off-system value is either a bug to snap to the system or an intentional flourish to
keep and add to the system. That is a restraint-and-feel call.
   Decisions: ____________________

## Named gate
Sign-off owner: ____________________  Date: ______
```

**Translate output is done when** every animation has a resolved token or an `off-system` flag, every row has a fallback and a reduced-motion cell (or a gap flag), every row is provenance-labeled, off-system values are flagged rather than rewritten, and the snap-vs-keep slot and gate are empty.

---

## Step 2 (both modes): Pre-flight verification

Confirm before delivering:

- **Reduced-motion present everywhere.** Every token group (Author) or every animation row (Translate) has a reduced-motion counterpart or an explicit gap flag. This is the mandate; a missing one is a hard fail.
- **Springs, not just duration+easing.** Author output carries spatial and effects springs across three speeds, with duration+easing as the *fallback*, not the primary model.
- **DTCG gap documented.** The standards note is present and states there is no first-class DTCG motion type; the output does not present its tokens as standard DTCG.
- **Personality not invented.** Author mode recorded a human-stated personality or flagged the slot blank; it did not choose one.
- **Judgment slots empty.** Restraint, feel, and (Translate) snap-vs-keep are unfilled; the named gate is present and unsigned.
- **Provenance on everything synthetic.** Candidate values labeled `candidate (agent-drafted)`; export-read values `from-export`; inferred values `agent-derived`.
- **Off-system flagged, not rewritten** (Translate). The skill did not silently normalize the designer's motion.

---

## What is explicitly out of scope

- **Choosing the motion personality.** A human input, never an agent decision (§ 9). Recorded or flagged blank; never invented.
- **The restraint call and the "does it feel right" verdict.** Empty by construction. Motion is judged in motion, by a human who has seen it run, not signed off on paper.
- **Building the screens that consume the motion.** `heyhi-ui-ux` (HeyHi pages) / `ui-studio` (client UI). This authors the system, not the interface.
- **Translating a whole prototype or a raster into a Figma design file.** `heyhi-design-bridge`. This is motion-specific.
- **Auditing a built prototype's interaction completeness.** `heyhi-prototype-audit`.
- **Writing to the Figma canvas in Translate mode.** Translate reads motion and emits a spec; it does not modify the source file.

---

## Exit Gate Required Headers (bottom-of-skill bracket)

This skill closes through Exit Gate Flavor A (`CLAUDE-SESSION-RULES.md § Exit Gate`). Before declaring done, confirm every required header holds real content:

- `## Fixes Applied` (or the delivered Motion System / Motion Translate artifact)
- `## Smoke Test` (the Step 2 pre-flight checks, pasted)
- `## Next Session Prompt`

If any motion set lacks its reduced-motion counterpart, if the DTCG note is missing, or if the personality/restraint/feel slots are filled by the agent, the gate has **not** been satisfied.

---

*HeyHi Confidential. Sheerline area 4 (Interaction Design), P3. Effectively net-new (no `heyhi-motion-system-author` candidate exists in the tree; built from the § 4.2 spec). Deployed in `heyhi-skills/motion-system-author/`; registered in the main + Sheerline subset registries (Wave G-4, 2026-08-28). Spec source: `ai-services/design-intelligence/research/sheerline-skill-buildout-research-2026-08-09.md` § 4.2; DTCG gap § 4 (~line 160). Boundary: § 9. Foundation: `sheerline/os/foundations/interaction-design/FOUNDATION.md` (registered 2026-09-05). Substrate pointer: control-state contract A.3, `design-fundamentals-decision-research-2026-08-12.md`, served as `design-system://fundamentals`.*
