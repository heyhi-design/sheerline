# Cluster Crosswalk — ui-reasoning.csv to HeyHi A–E clusters

*Reference for ui-studio-onboard. Translates ui-ux-pro-max's `Style_Priority` taxonomy (in `data/ui-reasoning.csv`) into HeyHi's A–E style cluster system. The two are different systems; this table is the translation layer.*

*HeyHi Internal Use Only*

## Why this exists

`data/ui-reasoning.csv` maps product type to recommended styles using ui-ux-pro-max's style names ("Glassmorphism + Flat Design," "Neumorphism," "Brutalism + Motion-Driven"). HeyHi uses the A–E cluster taxonomy (A Minimal/Refined, B Warm/Human, C Bold/Distinctive, D Technical/Precision, E Organic/Natural). The CSV cannot populate `brand.style_cluster` directly: a translation is required. Treat this as a first-pass signal, not a deterministic mapping.

## Crosswalk

| ui-reasoning Style_Priority | HeyHi Cluster | Notes |
|---|---|---|
| Minimalism / Swiss Style | A, Minimal/Refined | Direct match |
| Trust & Authority + Minimalism | A, Minimal/Refined | Restraint, precision |
| Accessible & Ethical + Minimalism | A, Minimal/Refined | Clarity first |
| Flat Design + Micro-interactions | A, Minimal/Refined | Clean, functional |
| AI-Native UI + Minimalism | A or D | A if content-first; D if data-dense |
| Motion-Driven + Minimalism | A or B | A if editorial; B if warm and breathing |
| Neumorphism + Accessible & Ethical | B, Warm/Human | Soft, organic UI feel |
| Claymorphism + Micro-interactions | B, Warm/Human | Friendly, approachable |
| Glassmorphism + Flat Design | C, Bold/Distinctive | Frosted glass reads as contrast-forward |
| Motion-Driven + Vibrant & Block | C, Bold/Distinctive | High energy, graphic |
| Vibrant & Block-based | C, Bold/Distinctive | Decisiveness over subtlety |
| Liquid Glass + Glassmorphism | C, Bold/Distinctive | Premium visual drama |
| Brutalism + Motion-Driven | C, Bold/Distinctive | Raw contrast, architectural type |
| 3D & Hyperrealism + Retro-Futurism | C, Bold/Distinctive | Immersive and expressive |
| Cyberpunk UI + Glassmorphism | C, Bold/Distinctive | Neon, high-contrast |
| Dark Mode (OLED) + Data-Dense | D, Technical/Precision | Grid as system, density hierarchy |
| Data-Dense + Heat Map | D, Technical/Precision | Functional clarity dominates |
| Organic / Natural / Earthy | E, Organic/Natural | Textural depth, material honesty |

## Ambiguous mappings — confirm with the practitioner

- **Glassmorphism**: A or C depending on color treatment
- **Motion-Driven + Minimalism**: A or B depending on warmth
- **AI-Native UI**: A or D depending on data density

When the product type lands on one of these, surface the ambiguity and ask rather than auto-assigning.

## How to use in onboarding (Phase 3)

1. Read `data/ui-reasoning.csv` directly (no search command, this skill is procedural).
2. Find the row whose `UI_Category` best matches the client's product type.
3. Read its `Style_Priority` and look it up above to get the suggested HeyHi cluster.
4. Surface: "Based on this product type, the closest HeyHi cluster is [X]. Does that match your read of their brand?"
5. On confirmation, write the cluster to `brand.style_cluster`.

Do not automate cluster assignment from this crosswalk without confirmation.

---

*HeyHi Internal Use Only. Authored 2026-06-18 from ui-ux-pro-max-improvement-plan.md Item 5.*
