---
classification: confidential
title: "Lo-fi method — the ceiling, the divergence axes, the inventory schema, the Mermaid hand-off"
skill: flow-and-lofi-author
loaded_by: "SKILL.md Step 1 (also pointed at by divergence-guard/references/fidelity-ladder.md for the axes)"
---

# Lo-fi method

The method knowledge `flow-and-lofi-author` loads to draft a Lo-fi Pack. Two of its four parts are craft canon adopted 2026-09-05 (spec § 10 D8): the **structure** of the ceiling table and the divergence axes is the adopted recommendation; **the specific values come from design practice, not from a cited source**, and are a starting point to adjust as real runs accumulate. The always-loaded behavioral invariants this skill obeys live in `sheerline/os/operating-principles.md` and are cited, not restated.

*Internal operational reference: em-dash limit exempt per `OPERATING_PRINCIPLES.md`.*

---

## 1. The fidelity ceiling (inherited, not invented)

The ceiling is the lo-fi phase as `OPERATING_PRINCIPLES.md` § Design and visual work protocol defines it: **"wireframe-level structure, layout, component placement, interaction logic — no visual polish."** That sentence is the rule; this table is its operational form.

| Allowed in a lo-fi skeleton | Over the ceiling (belongs to a hi-fi builder) |
|---|---|
| Regions, boxes, reading order, hierarchy by position and size | Color of any kind; any hex; any token reference |
| Functional labels ("Primary action", "Filter", "Order summary") and *provisional* label text marked `[provisional]` | Final copy, voice-tuned microcopy (`voice-system-author` / `microcopy-states-writer`) |
| Component *placement* by generic name ("a table", "a stepper") | Component *selection* from a design system, variants, sizes |
| Interaction logic: what a control does, where it leads, state names | Motion, easing, transitions (`motion-system-author`); state behavior specs (`interaction-inventory`) |
| Grayscale, monospace or system type, no imagery | Typography choices, imagery, illustration, brand marks |
| Annotations and open questions | Anything read from `active-brand.json` |

Why the skill runs without a config: `ui-studio`'s no-config hard stop exists because a hi-fi build without tokens produces generic defaults. A lo-fi has no tokens to default; **the ceiling is the config.** The self-check in Step 2.5 sweeps every skeleton for the right-hand column before emit and lists what it removed.

## 2. The divergence axes (authored once, here)

Alternatives are "structurally distinct" when they differ on at least one axis. The axes make overlap **measurable** (shared tags) without a taste judgment. `divergence-guard` compares on these same axes and points here rather than carrying a second copy.

| Axis | Values (examples, not a closed list) |
|---|---|
| Navigation model | linear / wizard · hub-and-spoke · tabbed · single-page with disclosure · conversational |
| Task decomposition | one screen · stepped · split by user role · split by object |
| Information hierarchy | what is primary on the first screen: the object · the action · the status · the choice |
| Entry point | where the task starts: a list · a detail · a prompt · an empty state · deep-linked |
| Disclosure strategy | everything visible · progressive · on-demand · defaults-first with override |
| Input model | form · direct manipulation · selection from candidates · guided / conversational |

**The overlap rule.** Two alternatives sharing every tag are one alternative rearranged. The default N (3; minimum 2) only means something with this check underneath it; without it, N is a count the skill could satisfy by shuffling boxes. When a pair shares every axis, the skill names the pair as a rearrangement and regenerates or asks; it never ships the fake N.

## 3. The screen-inventory schema

| Field | What goes in it |
|---|---|
| `id` | S1, S2, … stable within the pack |
| Screen | a functional name, not a page title |
| Purpose | one line: what the person is doing here |
| Entry from | the screens or triggers that lead here |
| Exits to | where the person goes next, including error and cancel paths |
| Data needed | what must be present for the screen to work |
| State placeholders | `loading · empty · error · success` as **names only**; behavior is `interaction-inventory`'s (area 4), copy is `microcopy-states-writer`'s (area 3) |
| Provenance | `[from-input]` (read from what the human brought) or `[inferred]` (added to complete the structure) |

The area-4 spec names this inventory as `interaction-inventory`'s natural pre-build input, not a dependency: the inventory row is the hand-off. A missing screen is an open question, never a silently inferred row.

## 4. The flow-map hand-off (Mermaid, unchanged)

The flow is emitted as a Mermaid **`flowchart`** in the constraints `heyhi-figjam-mapper` renders through `generate_diagram`: camelCase or short alphanumeric node ids, any special characters quoted, no emojis, no `\n`, no HTML, supported types only. Decision nodes as `{…}`, terminal states named, error paths and dead ends drawn, not omitted. This makes the seam a hand-off (the mapper draws the pack's flow verbatim) and not a re-draw. Any edge the skill supplied to connect the structure is listed as `[inferred]` under the map; any step the inputs do not account for is listed as a gap, not drawn.

## 5. The skeleton, per screen

For each alternative, each screen gets a wire description in this order: the regions in reading order; the primary action (one); the secondary actions; the content blocks as labeled boxes; the interaction logic between regions (what a control does and where it leads). Labels are functional, or provisional text marked `[provisional]`. Grayscale, unstyled, no imagery. A monochrome HTML skeleton behind a flag is a v1.1 option (spec § 10 D3); v1 is markdown-first because the HTML path is where the ceiling is hardest to hold (a stylesheet is a token waiting to happen).

## 6. Provenance labels

`[from-input]` and `[inferred]` on inventory rows and edges; `[provisional]` on any label text that is not purely functional; `[stimulus — not a recommendation]` is `divergence-guard`'s label, not this skill's. Anything modeled for illustration is `synthetic`.

---

*HeyHi Confidential. Reference for `flow-and-lofi-author`; the divergence axes are authored here and pointed at from `divergence-guard/references/fidelity-ladder.md`. Spec source: `plans/plan-sheerline-p3-prototyping-lofi-2026-09-05.md` § 2.3–§ 2.5, § 6.2. Canon adopted 2026-09-05 (§ 10 D8): structure recommended, values from design practice.*
