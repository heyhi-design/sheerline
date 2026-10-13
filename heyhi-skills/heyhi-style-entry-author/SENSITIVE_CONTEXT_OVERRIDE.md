# Sensitive Context Motion Override Pattern

**`heyhi-skills/heyhi-style-entry-author` · Reference · March 24, 2026**

*HeyHi Internal Use Only*

This pattern applies when a style entry will serve users under heightened cognitive load or in emotionally sensitive contexts. It is invoked per-entry, not globally — use it when the entry's `industry_fit.natural` includes any of the scope conditions below.

---

## When to Invoke This Pattern

Apply this override when a style entry's natural industry fit includes any of the following **cognitive load conditions:**

- Mental health, therapy, or trauma-informed applications
- Crisis support, suicide prevention, or 988-adjacent services
- Addiction recovery or substance use treatment platforms
- Grief, loss, or bereavement support tools
- Applications explicitly designed for neurodivergent users (ADHD, autism)
- High-stakes decision contexts (medical, legal, financial decisions under stress)
- Applications serving elderly users with reduced attention or processing speed
- Cognitive accessibility-first platforms (literacy-sensitive, stress-sensitive)

**Unifying principle:** These contexts share one condition — users are operating under reduced cognitive capacity or heightened emotional activation. Motion adds processing cost. When a user cannot afford that cost, motion becomes a harm, not an affordance.

---

## The Override

### Default (from entry)
Whatever `motion_personality` the entry carries (minimal / purposeful / expressive) is appropriate for the entry's general use case.

### Sensitive Context Modification
When serving any scope condition above:

| Token | Default (entry value) | Sensitive Context Override |
|-------|-----------------------|---------------------------|
| `motion_personality` | any | `minimal` |
| `motion_duration` | per personality tier | 0–75ms (essential feedback only) |
| `motion_easing` | cubic-bezier or spring | `linear` |
| Entrance animations | present | Remove entirely |
| Scale/translate transforms | allowed | Remove — opacity only |
| Parallax / auto-play | allowed | Remove entirely |
| Spring-physics easing | allowed in expressive | Remove |

### Implementation Checklist

Before delivering any sensitive-context build:

- [ ] Entrance animations removed from baseline component set
- [ ] Only opacity transitions present (no translate, scale, rotate)
- [ ] Duration ≤ 75ms for essential state-change feedback
- [ ] No parallax or auto-play motion present
- [ ] `@media (prefers-reduced-motion: reduce)` resets all durations to 0ms at CSS root
- [ ] Application provides a "Calm Mode" or "Accessibility Mode" toggle (optional but recommended)
- [ ] Design review approval gate: "No decorative motion present in baseline. All motion communicates critical feedback only."
- [ ] QA verifies prefers-reduced-motion implementation

### Approval Gate Statement
Before finalizing any sensitive-context component: *"This motion communicates critical information or feedback. Removing it would degrade the user's ability to complete the task. It cannot trigger vestibular responses or trauma-related reactions."* If this statement cannot be made, remove the motion.

---

## Authorities

This pattern is grounded in:

- **SAMHSA Trauma-Informed Approach** — Safety and Empowerment principles require predictability and user control. Unpredictable or uncontrolled motion violates both. (SAMHSA SMA14-4884)
- **WCAG 2.2 Success Criterion 2.3.3** — Animation from Interactions (AAA): motion triggered by user interaction must be disableable unless essential.
- **Mind Motion Toolkit & Guidelines** (UK Mind charity) — Published standard for motion in mental health interfaces, reviewed by people with lived mental health experience.
- **Vestibular disorder research** — ~28% of the general population has motion sensitivity. In mental health, trauma, and neurodivergent populations, the rate is significantly higher.
- **Cognitive load under stress** — Psychologically distressed users face heightened anxiety, reduced attention span, and impaired working memory. Motion adds processing cost; for users at capacity, this cost is material.

---

## Entry-Level Documentation

When adding this pattern to a style entry, insert the following block in `industry_fit:`, after the `natural:` list and before `stretch:`:

```yaml
  motion_override:
    sensitive_contexts:
      - [List the specific scope conditions that apply from the master list above]
    principle: >
      [One sentence stating why this entry's natural industry fit includes contexts where
      motion should default to minimal.]
    override:
      motion_personality: minimal
      motion_approach: >
        Color fades and opacity changes only. No scale transforms, no entrance animations,
        no spring-physics easing. Duration capped at 75ms for essential state-change feedback.
      easing: linear
    authority:
      - "SAMHSA Trauma-Informed Care: Safety + Empowerment principles require predictability"
      - "WCAG 2.2 SC 2.3.3: Animation from interactions must be disableable (AAA)"
      - "Mind Motion Toolkit: Published standard for mental health interface motion"
    implementation:
      - "Design base component set without entrance animations"
      - "Use opacity transitions only (no translate/scale)"
      - "Provide Calm Mode toggle in application settings"
      - "Implement @media (prefers-reduced-motion: reduce) at CSS root level"
      - "Design review approval gate: confirm no decorative motion in baseline"
    upgrade_path: >
      This prose pattern will be promoted to a Tier 2 token set override once HeyHi's token
      pipeline supports multi-variant aliasing. At that point, a sensitive-context-motion-set
      token set replaces this prose checklist. No style entry rewrites required.
```

---

## Current Entries with This Pattern Applied

| Entry | Industry Context | Override Applied |
|-------|-----------------|-----------------|
| Entry 8 — Community Platform | Mental health and mental wellness | Yes — see entry's `motion_override` block |

---

## Upgrade Path

**Current (Phase 0 — implemented March 2026):** Structured prose checklist in this file + per-entry `motion_override` YAML block.

**Phase 1 (Q3 2026, when token pipeline supports multi-variant aliasing):**
```
Tier 2 semantic tokens:
  sensitive-context-motion-entrance:  { duration: 0ms, easing: none }
  sensitive-context-motion-transition: { duration: 75ms, easing: linear }

style entry update: motion_sensitivity_profile: standard | sensitive
component update: reads profile from token set, not prose checklist
```
No style entry rewrites required — entries shift from prose checklist to token set selection.

---

## Research Notes for Future Sessions

**Parallel token set architecture for dark mode** (related concern): The `default_scheme: dark` style property signals dark-native entries, but the full token set architecture for expressing light/dark modes in W3C DTCG format warrants a dedicated session. W3C DTCG v2025.10 supports multi-mode token sets natively; Tokens Studio, Figma Variables, and Style Dictionary all implement this. Recommend: Session I or a parallel research session before first dark-native client engagement.

**Motion sensitivity profile expansion** (future): A binary standard/sensitive profile may expand to three tiers (full motion / reduced motion / no motion) as the library grows into accessibility-first and high-stakes-decision-making contexts. The current structure is compatible with this expansion — add a `minimal_strict` override tier without rewriting the pattern.

---

*HeyHi Internal Use Only · Classification: Internal Use Only · Last updated: March 24, 2026*
