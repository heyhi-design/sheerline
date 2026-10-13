---
classification: confidential
created: "2026-08-22"
status: ready-for-review
lane: DISPATCH-02 (LOFI-FIGMA)
source: plans/plan-sheerline-studio-ui-2026-08-21.md
---

# Wheelhouse lo-fi wireframes (G-A review)

> **Note (2026-10-13):** this is the lo-fi record as reviewed. The built dispatch board (S-10) now renders Sheerline's own `os/dispatch/batches/` (two worked examples plus an instance's own batches), not the monorepo's batch files described below.

Grayscale wireframes of all twelve Studio screens plus the three router result states, built in Figma for the instance owner's review at gate **G-A**. Boxes and labels only. The information architecture made visible, with no visual design applied.

## Where to review

**Figma page:** [Lo-fi · G-A review Opus 5](https://www.figma.com/design/gjxbSE2CP4wD4Ow60K1A41/Sheerline-Studio-%E2%80%94-lo-fi--G-A-review-?node-id=19-149)

The page sits in the existing lo-fi file (key `gjxbSE2CP4wD4Ow60K1A41`) alongside the earlier page, which is untouched. Frames are laid out in reading order, left to right and top to bottom: Home, the three router states, the session pair, the quality trio, the library screens, then the operating screens.

## Fidelity

Grayscale, per the plan's § 9 Q-5 default. The Resolution cell was still unanswered when this lane ran, so the stated default applied and is recorded here. Taste enters at D-03, not in these frames.

One color exception: every human-gate and empty-judgment slot carries a crimson dashed outline and the literal label `YOURS TO FILL`, so law L4 reads even at wireframe fidelity. Crimson appears nowhere else. S-1 opens with a lo-fi key that decodes the coverage ramp and the crimson slot, so the page can be read without this file.

Every screen frame carries its name and a one-line purpose above the chrome, so the canvas is legible without the layers panel.

Labels are real. Area names, coverage tags, phase tags, correction ids, dispatch batch filenames and their verbatim frontmatter status strings, seminar track titles and module names, and the intake schema keys all come from the live tree. Invented content is marked `sim`. No calibrated value, threshold, or populated-corpus entry appears in any frame.

## The frames

| Frame | What it shows | Laws it demonstrates |
|---|---|---|
| `S-1 · Home` | Lo-fi key legend, router bar, 13 coverage-styled area chips, 3 example prompts, the practice map grouped Craft / Operating / Conditional, recent sessions, real phase states, corrections pulse | L1, L2, L8 |
| `S-1 · Router state — routed` | One skill card, co-loads, summed load cost | L1, L6 |
| `S-1 · Router state — close-call` | Two cards side by side, "the call is yours", crimson choose slot | L1, L4, L8 |
| `S-1 · Router state — abstained` | Confidence insufficient, nearest areas, the capability-gap link | L1, L2 |
| `S-2 · Artifacts` | Kind filter chips, provenance-chip cards over real repo paths, an honest empty-kind state | L2, L7 |
| `S-3 · Areas` | Faceted filters, the 13-item list with `#area-<key>` anchors, two details side by side (a gap area and a deep area) with build gate and grounding verbatim, crimson tracked-gap callout | L2, L7, L8 |
| `S-4 · Skills` | Scope tabs with the real derived counts, search filter, cards on verbatim registry fields (description, triggers, `not_for`, load cost) including one reference-type card, `#cap-<id>` anchors | L1, L2, L7 |
| `S-5 · Session workspace` | Lifecycle stepper, three panes plus dock. In the room, artifact canvas with the rendered button set, run rail with the four verbs made concrete (MCP call, diff, checks, series), gate cards, crimson verdict slot, per-verb gate chips, inert composer | L3, L4, L5, L6, L7, L8 |
| `S-6 · Exit Gate` | Three filled Flavor A header slots with the human line inside Smoke Test, collapsed Flavor B, an empty-header error state that blocks emit, a handoff block that emits with the human line still open | L4, L5 |
| `S-7 · Validate` | Severity axis legend in verbatim order, rule-hit table with failing values and token-source suggestions, an above-the-floor card naming what the validator cannot answer | L3, L7, L8 |
| `S-8 · Grade` | The six real evaluator dimensions split floor / judge panel, sparklines over 8 simulated runs, direction table, no aggregate and no threshold line, crimson next-check slot | L3, L4, L8 |
| `S-9 · Learn` | Factual and behavioral columns with the seed `trigger_context` and `correction` text expanded verbatim, lifecycle as a progression, inert file-a-correction form on the real schema, moat card | L3, L4, L7 |
| `S-10 · Dispatch board` | Four columns, one swimlane per real batch file with its verbatim frontmatter status, this batch rendering its own nine prompts with wave and OWNS, batch-detail drawer, snapshot honesty line | L2, L6 |
| `S-11 · Seminar` | The 8-part module anatomy legend on the real template headers, five track rows with level, module count and build state, module cards with teaches badges, the separability line naming the C-1 and D-3 gates | L2, L7 |
| `S-12 · Intake` | Crimson hermetic-seal boundary card, seven read-only sections with blank value cells and comments as help text, the one substrate carve-out, illustrative area chips | L6, L8 |

## Review at gate G-A

Two things unblock D-03:

1. Review the Figma page above and say whether the structure holds.
2. Answer Q-1 through Q-4 in [`plans/plan-sheerline-studio-ui-2026-08-21.md`](../../../plans/plan-sheerline-studio-ui-2026-08-21.md) § 9 in one sitting, then flip the plan's frontmatter `status:` to `in-progress` and commit.

D-03 reads all five resolutions before it builds, so a partial answer holds the wave.

## Deviations from the lane spec

- The prompt specifies a new Figma file. The instance owner directed this run to add a new page to the existing lo-fi file instead, as the Opus 5 side of a model comparison against the page already there. The earlier page was not read or modified.
- Frame names carry the em dashes the prompt's naming spec uses. Authored copy inside the frames carries none. The single em dash inside a frame is part of a dispatch frontmatter status string quoted verbatim on the board, which is data rather than authored copy.

## Gate G-A: passed 2026-08-22

All five Decision Register rows in [plan § 9](../../../plans/plan-sheerline-studio-ui-2026-08-21.md) carry a resolution and the plan frontmatter is `in-progress`. What the review decided:

| Q | Resolution |
|---|---|
| Q-1 Name | **Wheelhouse.** Applied to these frames already: the wordmark reads `WHEELHOUSE` on all 12 screen frames, and the S-6 verdict line names Wheelhouse. File paths keep the `sheerline/studio/` slug, and the `ui-studio` skill names are unrelated and untouched. Decided before D-03 rather than at D-08 because the wordmark lives in the shell snippet that D-03 freezes. |
| Q-2 Screen cuts | **Keep all 12.** No lane skips a file. |
| Q-3 Visual direction | **§ 5 confirmed as written**, crimson budget not relaxed. These frames are the evidence: across all 15, crimson landed only on the three L8 uses. |
| Q-4 Capture scope | **S-1 + S-5 only** for the D-09 hi-fi capture. |
| Q-5 Lo-fi fidelity | **Grayscale**, by the row's own stated default, recorded rather than decided. |

D-03 is unblocked.

## Cross-model review (2026-08-22)

This page is the Opus 5 side of a model comparison. After it was committed, the Opus 4.8 page in the same file was reviewed frame by frame and its findings folded back in. Everything adopted was verified against the live tree first, not copied on sight.

**Corrected here because the other page was right and this one had invented:**

| Fix | Verified against |
|---|---|
| Frame names `S-7 · Validate`, `S-8 · Grade`, `S-9 · Learn` (this page had `S-N · Quality — Title`) | the lane prompt's own OUTPUT SPEC title list |
| The 8-part module anatomy is You are here / Learning objectives / Concept / Walkthrough / Lab / Common misreads / Self-check / Go deeper | `seminar/_module-template.md` § The eight sections |
| Phase states are complete / complete / active / not-started / not-started, D-3 gated to 2026-10-09 | `os/project-state.yaml` `phases:` |
| S-4 load costs, descriptions and `not_for` strings are the registry's own; scope tab shows 42 = 29 skills + 13 references | `skills/registry/skill-registry.yaml` |
| S-10 prompt cards carry wave and OWNS | plan § 4.2 S-10 spec |

**Adopted as better ideas, not corrections:** the lo-fi key legend on S-1; a title and purpose line on every frame; the session lifecycle stepper (scope, route, load, run, gate); concrete verb cards on S-5 (the named MCP call, a real diff, the check list, zero-token cost); per-verb gate chips in the dock including `grade · awaiting human`; the human slot moved inside `## Smoke Test` on S-6, which is where the plan actually places L4; the `blocks emit` consequence chip; a handoff block that emits with `[human observation]` still open; the above-the-floor card on S-7; expanded correction text on S-9; a second area detail on S-3 so a deep area sits beside a gap area; an actionable abstention on S-1.

**Kept as built, deliberately:** the artifact list at per-file granularity (the § 6.2 data contract globs individual paths, and the other page's eval-cases path does not exist); all four real dispatch batches with verbatim status strings rather than a generic prior-batch lane; the crimson hermetic-seal card at the top of S-12, which plan § 4.2 requires; the rail carrying target filenames; the discrete four-step coverage ramp; the full validator table including the no-hit Brand and Code rows; 760-wide state frames, which the prompt asks to be smaller.

**Corrected beyond both pages:** S-8 now uses the real evaluator dimensions, split by instrument. Dimensions 1, 2, 3 and 6 are the deterministic floor (token conformance, component reuse, accessibility, silent-drift surface) from `eval_harness_i1.py`; dimensions 4 and 5 are the judge panel (intent fidelity, compositional coherence) from `seminar/track-3-quality-loop/module-3-3.md`. Both pages had invented dimension names.

---

*HeyHi Confidential*

---

## Hi-fi capture (G-B)

**Figma page:** [Hi-Fi · G-B review](https://www.figma.com/design/gjxbSE2CP4wD4Ow60K1A41/Sheerline-Studio-%E2%80%94-lo-fi--G-A-review-?node-id=64-2)

Captured **2026-08-24** by DISPATCH-09. Two frames, both desktop 1440, on a third page of the same file alongside the two lo-fi pages:

| Frame | Size | What it carries |
|---|---|---|
| `S-1 · Home` | 1440 × 2647 | Router bar with the three real gate verdicts, 13 area chips on the four-state coverage ramp, the practice map grouped Craft / Operating / Conditional, phase progress, corrections pulse |
| `S-5 · Session workspace` | 1440 × 2101 | Lifecycle stepper, three panes (In the room / artifact canvas / run rail), the four verbs with provenance and action logs, the Grade card, bottom dock |

Scope is S-1 + S-5 per plan § 9 Q-4. Layers are real text and real frames on token-true fills, not flattened screenshots.

### Token fidelity

Twelve values were read back out of Figma and compared against `shared/studio.css`; all twelve match:
`--field` #FAFAF5 · `--teal` #0B6E75 · `--crimson-bright` #FF3B30 · wordmark Sora Bold 15.2/ls1.82 · rail label Sora 14.72 · h1 Sora SemiBold 32 · `--topbar-h` 60 · `--sp-5` 24 · `--sp-4` 16 · `--r-2` 10 · `.cov__bar` 52×8 · `--rail-w` 220.

### Deviations from the lane spec

- **Same file, not a new one.** The prompt specifies a new Figma file; plan § 8 specifies a third page in the existing lo-fi file, and the instance owner directed this run to the page already made for it. The plan and the direction agree, so the capture is a page here. The two lo-fi pages were not read or modified.
- **Authored, not mechanically translated.** The `heyhi-design-bridge` Translate pipeline ran end to end (extract, validate, build, plugin transport, headless mock PASS) and its output was rejected on quality. Its builder gives any zero- or auto-height DOM element a default 100px, which turned every coverage bar, status dot and flex spacer into a large empty rounded rectangle; `::before` pseudo-elements never became layers, so the coverage ramp rendered hollow; `.sr-only` text rendered visibly; and the CSS grid flattened into a single horizontal row. The frames were therefore authored directly against `studio.css` and the snapshot data, using the extracted IR as the measurement reference for type, colour and copy. The IR, build plan and plugins remain in the instance's engagement folder if the mechanical path is ever revisited. Those plugins have been **neutralised**: their page op now targets a scratch page name, their `rerun` is `none` so they clear nothing, and their manifests are prefixed `[REJECTED BUILD]`. As shipped they targeted this review page with `rerun: replace`, so one stray Run would have deleted the capture.
- **Sora Medium is unavailable in Figma.** `studio.css` imports Sora 500 and the browser renders true Medium, but Figma offers Sora in Thin/ExtraLight/Light/Regular/SemiBold/Bold/ExtraBold only. The 34 affected layers (rail labels, button labels, tabs, card titles) are captured as Sora **SemiBold**, the instance owner's call at gate G-B, accepting that it collapses the 500/600 weight distinction so that nothing renders lighter than the browser does. Size still carries the hierarchy. Everything else resolves to its exact weight.
- **The skip link is omitted.** `.skip-link` is `position:absolute; top:-60px`, so it sits off-screen until keyboard focus. Including it added a stray visible button and 43px to the frame.

### Review at gate G-B

1. Review the Figma page above, and open `sheerline/studio/index.html` and `session.html` locally for the interactive read.
2. Record the next-step decision as a dated line appended to [`plans/plan-sheerline-studio-ui-2026-08-21.md`](../../../plans/plan-sheerline-studio-ui-2026-08-21.md) § 11, and flip that plan's frontmatter `status:` (`done` if the exercise closes here; `in-progress` or `blocked` if a follow-on is chosen). Commit both.

*HeyHi Confidential.*

### Adversarial pass (2026-08-24, post-capture)

A fresh pass over the finished capture found twelve defects, all since fixed. Recorded because most were mine, not the pipeline's, and the pattern is worth keeping.

**One live hazard.** The two build plugins were still importable and targeted this page with `rerun: replace`, which clears every child. A stray Run would have replaced the capture with the rejected mechanical output. The Desktop copies are deleted and the retained copies retargeted; if the plugins still appear under Plugins → Development in Figma, remove them.

**Two fabricated or invented values.** The phase meter's `active` fill was set to 55% by eye; the real rule is `pf(status) = complete ? 100 : (active ? 60 : 0)`, so it is now 60%. The coverage-key gate swatch was built 52×14; the source is 18×12.

**One repeated defect.** The router card carried a visible `DESCRIBE A DESIGN TASK` label. That string is a `.sr-only` element, invisible in the browser, so rendering it was the same screen-reader-leak defect the mechanical builder was rejected for. Removed. The visible string there is the input's own placeholder, `Describe a design task, then Route`, which had been replaced with invented copy.

**Eight casing and colour drifts**, from setting case by eye rather than from `text-transform` in the stylesheet. Wrong in both directions: `Or jump to an area`, `Try the router` and `Gate status` had been uppercased when their classes carry no transform; `human's to fill`, the button-set column headers, `promoted to a session` and the composer tag had been left lowercase when their classes do uppercase. The action-log summaries were faint uppercase without a marker; `.actions > summary` is teal, sentence case, with a `▸` disclosure marker. `promoted to a session` was also indigo rather than the specified teal.

Re-verified after the fixes: all token spot-checks unchanged, zero verdict-shaped strings (L3 holds), zero banned words, zero screen-reader leaks. The single em dash remaining is inside verbatim snapshot grounding text, which the prototype itself renders; editing it would make the capture misreport the data.
