# Style Direction Brief — Reference

Companion to `heyhi-style-brief/SKILL.md`. Holds the brief template, the descriptor → plain-language translation guide, and the field-mapping table from the upstream selection output. Loaded on demand during a brief write.

*Classification: internal*

---

## 1. The brief template

A direction brief is short — one to two pages of readable prose. A client should be able to read it in five minutes and know whether it is them. Resist the urge to be exhaustive; the token build carries the detail. The brief carries the decision.

### Suggested structure

**[Client] — Design Direction**

**The direction.** One sentence. The `agent_context_snippet` from the style entry, rewritten so a non-designer feels it. This is the line they repeat to a colleague.

**What it will feel like.** Two to four sentences on mood, tied to what the client said they wanted. Lead with the feeling. If the client said "we want to feel trustworthy without feeling corporate," answer that sentence directly.

**Color.** Two to three sentences. The temperature and character — warm, grounded, calm, confident. What the palette does for the experience (e.g., "an accent color with personality, used deliberately, so the few things that should draw the eye actually do"). No hex codes, no token names. If color is asset-derived, say the palette comes from their own photography; if pending, say it will.

**Typography.** Two to three sentences on what the type will *do*: read clearly, feel warm, carry quiet authority. Not its classification. If named typefaces are not yet chosen, say so here and make it a decision in the closing section.

**Imagery and photography.** Two to four sentences. Translate the Category 8 register into what to expect and, where useful, what to start gathering. "Documentary photography of real people in real settings — unposed, warmly lit" reads; "imagery_approach: documentary" does not.

**Why this fits you.** Two to four sentences. The sector intersection in client terms. Natural fit: confirm cleanly and say why. Stretch: name honestly what adapts and why it still holds. This is where the brief earns trust — it shows the direction was chosen for them, not pulled off a shelf.

**What we're not doing.** One or two sentences. The road not taken, in plain language ("We're not going cool and minimal — that would read as distant, and you asked for warmth"). Naming it sharpens the yes.

**What happens when you approve.** Two to three sentences. The next step (the team builds the design system tokens and components against this direction), and the specific decisions this approval locks — plus any open questions the client answers here (typeface choice, imagery sourcing, a sector adaptation).

---

## 2. Descriptor → plain-language translation guide

The brief never uses the left column in client-facing copy. Translate to the right.

| Technical / vocabulary term | Plain client language |
|---|---|
| `color_temperature: warm` | warm, grounded, inviting |
| `color_temperature: cool` | calm, clear, composed |
| `color_temperature: cool-neutral` | quiet and neutral, with a cool edge |
| accessible accent color | one color with personality, used deliberately |
| `type_personality: humanist` | clear and approachable; type that feels human, not mechanical |
| `type_personality: geometric` | clean and modern; precise without feeling cold |
| `type_personality: grotesque` | confident and contemporary |
| `type_personality: serif` / transitional | considered and credible; a touch of editorial authority |
| `type_scale_ratio: Major Third 1.25x` | a clear, comfortable size hierarchy (omit the ratio) |
| `spacing_density: spacious` | open and unhurried, with room to breathe |
| `spacing_density: balanced` | organized but not crowded |
| `spacing_density: dense` | efficient and information-rich |
| `border_radius_range: rounded` | soft, approachable edges |
| `border_radius_range: sharp` | crisp, precise edges |
| `shadow_depth: subtle` | a gentle sense of depth; surfaces feel tactile |
| `shadow_depth: flat` | clean and flat, no decoration for its own sake |
| `motion_personality: purposeful` | motion that responds with care, never showy |
| `motion_personality: expressive` | lively, with motion that has personality |
| imagery `documentary` / `reportage` | real people in real settings, unposed |
| imagery `editorial` / `constructed` | composed, art-directed imagery with a point of view |
| imagery `spatial` | wide shots that establish place and scale |
| imagery `data-visual` / `diagrammatic` | clear charts and diagrams that do real explaining |
| imagery `geometric-illustration` | simple, friendly illustration for explanations and empty states |
| `industry_fit: natural` | this style is a natural home for your kind of work |
| `industry_fit: stretch` | not the obvious choice for your sector — here's what we adapt and why it works |

The rule: a client approves an experience. Describe the experience. Keep the mechanism in the build.

---

## 3. Field-mapping from the upstream selection output

When the input is a **Mode B `style_pre_classification` YAML**, each field maps to a brief section:

| Mode B field | Brief section |
|---|---|
| `matched_style` + `cluster` | The direction (one line) |
| `match_evidence.mood_alignment` | What it will feel like |
| `token_implications.color_temperature` (+ `color_*_hex` if asset-derived) | Color |
| `token_implications.type_personality` (+ `type_*_face` if confirmed) | Typography |
| `match_evidence.imagery_register` | Imagery and photography |
| `sector_fit` + `sector_note` | Why this fits you |
| (the matched entry's `anti_mood`) | What we're not doing |
| `designer_confirmation_needed[]` | Open decisions in "what happens when you approve" |
| `color_palette_source`, unresolved typography, provisional imagery | Approval checkpoints (Step 5) |

When the input is a **Mode A package**, the five components already carry most of this — the work is register and tone, plus pulling the `designer_confirmation_needed` equivalents (Mode A's "what this enables next" caveats) into explicit approval checkpoints.

---

## 4. Voice notes specific to direction briefs

- The brief persuades by showing attention, not by selling. It should read like it was written by someone who was in the room and heard what the client said.
- Avoid the reveal-and-label pattern ("That's the difference." / "This isn't decoration. It's direction."). Per `writing-rules.md`, these read as machine-generated. State the thing; trust the reader.
- One or two em dashes across the brief, allocated deliberately. A comma or a period almost always serves.
- No banned words. "We build it in" and "what fits your team" are in-voice; "leverage," "seamless," "elevate the experience" are not.

---

*HeyHi Internal Use Only. Bay Design LLC. June 2026.*
