---
classification: confidential
title: "Reference: the motion-token schema (springs + fallback + stagger + reduced-motion)"
skill: motion-system-author
mode: Author
---

# Motion-token schema

**HeyHi Confidential.** The house schema Author mode assembles. Load this when building or reviewing the token model. Every value the skill drafts is a candidate the human tunes; this reference gives the shape and sane starting ranges, not the final feel.

---

## DTCG gap (put this in every output)

The stable DTCG (Design Tokens Community Group) spec, 2025.10, defines **no first-class motion types**. Springs, keyframes, and transitions are unspecified. There is a `duration` type and a `cubicBezier` type, and a `transition` composite exists only in draft form; there is nothing for springs, staggers, or reduced-motion. So every mature system hand-rolls its own motion tokens: Material 3, Carbon, and Polaris each define a bespoke motion-token shape, and none of them is portable to another.

Consequence for this skill: the tokens below are a **documented house schema, not standard DTCG motion tokens.** Every artifact this skill emits must say so in a standards note, in plain words, near the top. A reader who sees "design tokens" will assume a ratified format; motion has none, and presenting a house schema as if it were standard is a defect. State the gap, name the schema as HeyHi's, and note that the duration and cubic-bezier fallback values *do* map to the DTCG types that exist (which is why the fallback matters for portability).

*[Fact source: `sheerline-skill-buildout-research-2026-08-09.md` § 4 (~line 160), marked verified 2-source in the spec. Do not re-verify online; use the stated fact and flag if a future DTCG release adds motion types.]*

---

## Group 1: Springs (the primary model)

Springs, not duration+easing, are the primary model (M3 Expressive). Two categories, three speeds each, expressed as physical parameters, not a time.

- **Spatial springs**: motion that changes an element's **position or size** (a card sliding in, a sheet expanding, a thumb moving on a switch). May carry a small overshoot; a little bounce reads as physical and intentional.
- **Effects springs**: motion for **color, opacity, and other non-spatial** properties (a fade, a tint change, a shadow deepening). **No overshoot**: overshoot on opacity reads as a flicker, so effects springs stay critically damped regardless of personality.

Parameters: `stiffness`, `damping`, `mass` (the standard spring triple; a renderer converts these to its own units). Starting ranges (candidates, tune to the stated personality):

```yaml
spring:
  spatial:            # may overshoot
    fast:    { stiffness: 700, damping: 30, mass: 1 }   # snappy, small travel (toggles, chips)
    default: { stiffness: 450, damping: 32, mass: 1 }   # standard entrances, cards
    slow:    { stiffness: 260, damping: 34, mass: 1 }   # large surfaces, sheets, dialogs
  effects:            # never overshoots (critically damped)
    fast:    { stiffness: 700, damping: 42, mass: 1 }   # quick fades, hover tint
    default: { stiffness: 450, damping: 44, mass: 1 }   # standard opacity/color
    slow:    { stiffness: 260, damping: 46, mass: 1 }   # slow reveals, scrims
```

**Personality biases the parameters, it does not pick the feel.** A "calm / deliberate" personality drafts higher damping and slower speeds; a "quick / confident" one drafts higher stiffness on the fast/default spatial springs; a "playful" one lowers spatial damping so entrances overshoot a little (effects damping stays high, playful never means flickering opacity). The mapping is a starting point that widens the human's options; the human tunes and signs off on the feel.

---

## Group 2: Duration + easing fallback

Every spring token cross-references a duration+easing pair for any consumer that cannot express a spring: a CSS `transition`, a platform without a spring primitive, a static documentation table, a reduced-motion path. These are the values that *do* map to the DTCG types that exist.

```yaml
fallback:
  duration:           # a small, named scale, do not free-set arbitrary ms
    instant: 0ms
    fast:    150ms
    default: 250ms
    slow:    400ms
    deliberate: 600ms
  easing:             # named cubic-bezier curves (map to DTCG cubicBezier)
    standard:            cubic-bezier(0.2, 0.0, 0.0, 1.0)   # general in+out
    emphasized-decelerate: cubic-bezier(0.05, 0.7, 0.1, 1.0) # entrances (from off-screen)
    emphasized-accelerate: cubic-bezier(0.3, 0.0, 0.8, 0.15) # exits (to off-screen)
    standard-decelerate: cubic-bezier(0.0, 0.0, 0.0, 1.0)
    standard-accelerate: cubic-bezier(0.3, 0.0, 1.0, 1.0)
```

Rule: **every spring token names its fallback.** A spring with no fallback degrades to "no motion" on a consumer that cannot render it, silently. Naming the fallback is how the system degrades honestly.

---

## Group 3: Stagger

Sequenced delay for lists, grids, and grouped reveals. A single small scale.

```yaml
stagger:
  tight:   20ms   # dense lists
  default: 40ms   # standard grid / list entrance
  loose:   80ms   # a few large cards
```

Whether a given surface should stagger *at all* is a restraint call, not a token default. The token exists; using it is the human's decision (surface it in the Author artifact's restraint notes).

---

## Group 4: Reduced-motion variant (MANDATORY)

Every group above and every component spec below carries a `prefers-reduced-motion` counterpart. This is part of the token by construction, not a later accessibility pass. The default strategies:

```yaml
reduced_motion:
  spatial:  cross-fade      # replace position/size travel with an opacity change
  effects:  keep-short      # opacity/color changes are usually fine; cap at fast duration
  stagger:  none            # remove sequenced delay; reveal together
  large_travel_or_parallax: disable   # no large-distance or parallax motion
  overshoot: none           # collapse any bounce to a settle
```

A spatial spring's reduced-motion path is a cross-fade at the `fast` fallback duration; effects springs shorten to `fast` and drop any easing flourish; stagger goes to zero; parallax, large-travel, and overshoot are removed. An emitted set with a spring token but no reduced-motion counterpart is **incomplete** and fails the smoke test.

---

## Component specs

Component motion keys off the control-state contract (default / hover / focus-visible / active / disabled / loading / error + success / selected, the A.3 set, `design-fundamentals-decision-research-2026-08-12.md`). Draft the full table and let the human prune which components and which transitions matter.

| Component | Transition | Spring token | Fallback | Reduced-motion |
|---|---|---|---|---|
| Button | default → hover | effects.fast | 150ms / standard | keep-short |
| Button | hover → active (press) | spatial.fast | 150ms / standard | cross-fade (no scale travel) |
| Button | → loading | effects.default | 250ms / standard | keep-short |
| Card | entrance | spatial.default | 250ms / emphasized-decelerate | cross-fade |
| Card | list load (staggered) | spatial.default + stagger.default | 250ms / emphasized-decelerate | cross-fade, stagger none |
| Modal / sheet | open | spatial.slow | 400ms / emphasized-decelerate | cross-fade |
| Modal / sheet | close | spatial.slow | 400ms / emphasized-accelerate | cross-fade |
| Toast | enter / exit | spatial.default | 250ms / emphasized | cross-fade |
| Page | route transition | spatial.slow | 400ms / standard | cross-fade, no travel |
| Field | → error / success | effects.default | 250ms / standard | keep-short, no shake |

`focus-visible` never depends on motion to be perceivable (the state must be legible with motion fully off); `disabled` has no entrance motion. Note both in the artifact.

---

## Provenance and the empty slots

- Every drafted value is `candidate (agent-drafted)`. The schema widens the human's starting point; it does not set the feel.
- The **personality** is a human-stated input recorded verbatim, never invented.
- The **restraint** call (how much motion, where to hold back) and the **feel** sign-off (reviewed in motion) are empty slots behind the named gate.

---

*HeyHi Confidential. Reference for `motion-system-author` (Author mode). Spec: `sheerline-skill-buildout-research-2026-08-09.md` § 4.2; DTCG gap § 4.*
