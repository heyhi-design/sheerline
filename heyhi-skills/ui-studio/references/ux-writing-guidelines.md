# UX Writing Guidelines Reference

**`ui-studio/references` · Load when writing component-level copy · March 2026**

*How to apply the ux_writing config block, slot lookup, gap handling, and source attribution.*

---

## The Copy Hierarchy

When writing any visible interface text in a ui-studio build, apply rules in this order:

1. **`ux_writing` slot** — if the config has a populated slot for this copy type, follow its pattern exactly
2. **`voice` rules** — if no ux_writing slot, apply `voice.tone`, `voice.prohibited_words`, `voice.cta_style`
3. **Universal copy quality** — applies to all brands regardless of what the config contains

If neither exists (missing ux_writing block and missing voice block): write clean, professional copy and flag: *"No voice or UX writing guidelines in this config. Copy has been written to universal quality standards. Establish guidelines via ui-studio-onboard Phase 5."*

---

## Slot Lookup

The `ux_writing` block has eight standard slots. For each piece of copy you write, identify the slot it belongs to:

| Slot | What it covers |
|---|---|
| `empty_states` | Screens with no content yet — empty lists, zero results, first-time states |
| `error_messages` | System errors, validation failures, connection problems |
| `tooltips` | Hover/focus contextual help text |
| `buttons_ctas` | Button labels, primary CTAs, link text that triggers actions |
| `form_labels` | Field labels, helper text, placeholder text, field validation messages |
| `notifications` | Success, error, warning, and info toast/banner messages |
| `loading_states` | In-progress messages during async operations |
| `onboarding` | First-time user flows, setup steps, guided tours |
| `custom` | Any brand-specific slot defined in `ux_writing.custom.*` |

---

## Applying a Slot

When you have the slot, read its fields before writing:

**For `empty_states`:**
- `pattern` tells you the structural approach (e.g., "State what's missing + one concrete action")
- Write copy that follows the pattern. Don't invent a different structure.

**For `error_messages`:**
- `pattern` = overall approach
- `tone` = how it should sound (e.g., "calm and practical")
- `structure` = the sentence-level format (e.g., "[What failed]. [Why, if known]. [Next step].")
- Write the error message to match all three fields.

**For `tooltips`:**
- `max_length` = enforce this. Count characters.
- `tone` = how it should sound
- `avoid` = list of patterns not to use — check your draft against each

**For `buttons_ctas`:**
- `verb_preference` = the verb style to use
- `examples` = reference these; derive new CTAs from the same pattern
- Never invent a CTA that contradicts the examples in direction or tone.

**For `form_labels`:**
- `case` = apply exactly (sentence case, title case, ALL CAPS, etc.)
- `helper_text_style` = format guidance only vs. instructional vs. none
- `placeholder_policy` = how/whether to use placeholder text

**For `notifications`:**
- Four distinct tones for success, error, warning, info — apply each to its context
- Do not use a success tone for a warning, or an error tone for info

**For `loading_states`:**
- `pattern` = the general approach
- `examples` = use as direct models. Derive new loading messages by substituting the action.

**For `onboarding`:**
- `tone` = how it should sound across the entire onboarding flow
- `structure` = the flow-level approach (e.g., "One task per step, clear progress indicator")

---

## Gap Handling

When the config has a `ux_writing` block but a specific slot is missing or empty:

1. **Check `voice` rules** — apply those to fill the gap
2. **Apply universal copy quality** (below)
3. **Flag the gap** in your output: *"No [slot name] guidelines in config. Used voice rules + universal standards. Fill this slot via ui-studio-onboard Phase 5 when available."*
4. **Document the source** in your copy comments: `/* source: voice rules + universal standards — no ux_writing.[slot] in config */`

Do not silently fill gaps. The flag keeps the config debt visible.

---

## Source Attribution

Every piece of interface copy should have a source attribution comment in the HTML or template:

```html
<!-- copy source: ux_writing.buttons_ctas (config v1.2.0) -->
<button type="submit">Deploy to production</button>

<!-- copy source: voice rules + universal standards (no ux_writing.empty_states in config) -->
<p class="empty-state">No deployments yet. Connect a repository to start.</p>
```

In the developer handoff document, include a copy provenance table:

| Component | Copy | Source | Last verified |
|---|---|---|---|
| Submit button | "Deploy to production" | ux_writing.buttons_ctas | [config last_verified date] |
| Empty state | "No deployments yet. Connect a repository to start." | voice rules + universal | N/A (derived) |

---

## Universal Copy Quality

Apply to all brands, regardless of config completeness:

**CTAs:** Specific and human. "Start a conversation" over "Get started." "Connect your repository" over "Click here." The CTA describes the outcome, not the navigation.

**Labels:** Concise. Utility text must be scannable. Every word earns its place.

**Empty states:** Never "Nothing to see here" or "No data." State what's missing and one concrete action. Make the empty state feel like an invitation, not an absence.

**Error messages:** Never blame the user. Never use "Oops." State what happened, why if known, and what to do next. Calm and practical.

**Loading states:** Action-specific over generic. "Saving changes..." not "Loading..." "Connecting to GitHub..." not "Please wait."

**Notifications:** Success confirms the action (past tense). Error gives a path forward. Warning describes what might go wrong. Info is context only — no action required.

**No filler patterns:** Remove "Please note that...", "It seems that...", "Unfortunately...", "We're sorry to inform you..." Cut to the substance.

**Prohibited patterns (all brands unless config explicitly permits):**
- Exclamation points (except in marketing content if voice rules permit)
- Ellipsis to suggest incompleteness or playfulness ("Loading..." is fine; "We're checking on things..." is not)
- "Easy" or "simple" — these are promises the interface may not keep
- Passive voice for user actions ("Your file was uploaded" → "File uploaded")

---

## Mode C Copy Notes

In Mode C, the concept narrative language applies. Brand prohibited words may be used if the concept demands it — with documentation in the concept narrative. Standard UX writing quality still applies: even speculative interfaces need clear, human copy.

When writing Mode C interface copy:
- State in the concept narrative which prohibited words were used and why the concept required them
- Apply universal copy quality as the floor
- The ux_writing slot patterns are departure points in Mode C, not hard rules

---

*HeyHi Internal Use Only. Created March 25, 2026.*
