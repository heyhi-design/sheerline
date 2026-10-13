---
title: "heyhi-logo-system — Logo Construction Typology"
classification: HeyHi Confidential
module: A
loads_in: [Concept, Spec]
version: "0.1.0"
created: "2026-06-10"
grounding: ["design-intent-document-template.md:54", "research/visual-language-theory.md (Peirce, Gestalt)", "style-reference-library.md (five clusters)"]
---

# Logo Construction Typology

**HeyHi Confidential**

*On-demand reference module for `heyhi-logo-system`. Loads in **Concept** (to choose a construction direction and name it) and **Spec** (to write the design-intent typology field). Not always-loaded. The seven typologies it names are the canonical set from `ai-services/design-intelligence/design-intent-document-template.md:54`; this module reasons each one. It adds no schema field — typology is non-tokenizable by the skill's own law (see "Token implications").*

---

## Why this module exists: construction is not aesthetic

A logo decision has two independent axes that generic skills routinely conflate:

- **Construction typology** — *how the mark is built.* Is it the name set as type? Initials? A picture of a thing? An abstract symbol? A symbol-plus-name lockup? Type sealed inside a shape? A system of marks? This is the axis below.
- **Aesthetic style** — *how the mark looks and feels.* Bauhaus, Swiss, editorial, warm-humanist, neo-industrial. This axis already has a home: `style-descriptor-vocabulary.md` (the eight descriptor categories) and the five clusters in `style-reference-library.md`.

These are orthogonal. A wordmark can be Swiss or vintage; a pictorial mark can be warm or technical. The external `ckm:logo-design` skill mixes them into one "55 styles" list, which is the category error this module corrects. **In Concept, decide the typology here and the aesthetic from the vocabulary and clusters, then state both.** Do not collapse them into one choice.

A note on signification (from `research/visual-language-theory.md` Part 1, Peirce's trichotomy): every mark communicates as an **icon** (resemblance), an **index** (causal/material connection), or a **symbol** (learned convention) — usually a mix, usually drifting toward symbolic as brand equity accrues. The typology you choose sets the starting point on that spectrum, which is why typology is a meaning decision, not a formatting one.

---

## The seven typologies

Each entry: what it is · how it signifies · when to choose it · what it implies for the tokenizable fields · its characteristic failure modes (full catalog in [`mark-failure-modes.md`](mark-failure-modes.md)) · its cluster affinity.

### 1. Wordmark
**What** — the brand name itself is the mark, set in a distinctive face (Google, Sony; HeyHi's own identity). **Signifies** — symbolic: the letterforms accrue meaning through repetition, while the typeface's connotations (serif authority, geometric-sans precision) do immediate work. **Choose when** — the name is short and worth remembering, and committing to language over symbol is itself a positioning statement. **Token implications** — no separate symbol asset; `min_sizes` is governed by character legibility, not icon recognition; the reduction path (`scale_degradation`) typically drops to a lettermark. **Failure modes** — collapses at favicon scale; generic if the typeface is not distinctive. **Clusters** — A (Clean and Structured), C (Bold and Distinctive, editorial), E (Craft and Studio).

### 2. Lettermark
**What** — initials or a monogram (IBM, HBO, P&G). *ckm's "monogram" is a lettermark subtype, not a separate category — record it as a lettermark.* **Signifies** — symbolic, compact; the initials mean nothing until use makes them mean the brand. **Choose when** — the full name is long or unwieldy, or the mark must hold at very small sizes where a wordmark cannot. **Token implications** — compact, favicon-friendly `min_sizes`; often the reduced form *for* a wordmark or combination mark rather than a standalone. **Failure modes** — low distinctiveness (initials are a crowded space; three-letter marks collide across industries); can read as generic-corporate. **Clusters** — A, D (Sustainable and Infrastructure).

### 3. Pictorial
**What** — a recognizable object or representational image (Apple's apple, Twitter's bird). **Signifies** — iconic: it represents through resemblance, so it is immediately legible — but the more literal, the less distinctive (a camera for a photography brand is instantly understood and instantly shared with every competitor; `visual-language-theory.md:58`). **Choose when** — there is a concrete object that genuinely encodes the brand and the category is not already saturated with it. **Token implications** — a scalable symbol asset separable from the wordmark; supports a combination lockup. **Failure modes** — literalness flattening into low distinctiveness; metaphor over-reach (the object says more, or other, than intended). **Clusters** — B (Warm and Human), C.

### 4. Abstract
**What** — a non-representational symbol (Nike swoosh, Pepsi globe, Chase octagon). **Signifies** — symbolic in the strong sense: the form carries no inherent meaning and earns all of it through sustained, consistent use. High distinctiveness once established; expensive in the early phase (`visual-language-theory.md:66`). **Choose when** — distinctiveness and ownership matter more than immediate legibility, and the brand can invest in establishing the mark. **Token implications** — a pure symbol asset; the cleanest to tokenize as `marks.icon`. **Failure modes** — meaningless or arbitrary early (no equity yet); forgettable if it fails Prägnanz (the perceptual system flattens a fussy abstract form into "some swoosh"; `visual-language-theory.md:188`). **Clusters** — C, D.

### 5. Combination
**What** — a symbol and a wordmark locked together (Adidas, Lacoste, most modern identities). **Signifies** — mixed; the symbol can run iconic or abstract while the wordmark anchors the name. **Choose when** — flexibility matters: the symbol detaches for small or square contexts, the lockup leads everywhere else. The safe, common default. **Token implications** — two assets (`marks.primary` lockup + `marks.icon`); the **mark-to-type relationship is non-tokenizable design intent**, not a field; the reduction path sheds the wordmark to the icon. **Failure modes** — the lockup breaks on mobile when mark-to-type spacing is left to prose (a Medium severity finding by default); two elements to get right instead of one. **Clusters** — any; the most cluster-neutral typology.

### 6. Emblem
**What** — the name is integrated *inside* a contained shape: badge, seal, crest, roundel (Starbucks, Harley-Davidson, most universities and civic bodies). **Signifies** — carries the **code of authority/institutional** and of heritage/craft (`visual-language-theory.md:107`); the containment itself reads as official. **Choose when** — heritage, trust, officialdom, or craft provenance is the point, and the high-trust category rewards gravitas over flexibility. **Token implications** — typically a single integrated asset; the mark and type do not separate, which constrains `scale_degradation` (see below). **Failure modes** — the classic emblem problem: detail-dense, it does not reduce, so it fails at small sizes; mark and type are inseparable, so there is no clean icon form. **Clusters** — E (Craft and Studio), D (civic). **Critique link (R4):** when a *playful* aesthetic is applied to a high-trust category (trade, property, financial, health), the emblem is the form to weight toward — its containment pairs character with the proof-of-seriousness the stakes demand. This is the structural answer to R4's credibility-calibration check.

### 7. Dynamic
**What** — a system of marks or a transforming identity rather than one fixed form (MIT Media Lab, the old Google "dots," Nordkyn). **Signifies** — symbolic and systemic; recognition comes from the *rule*, not a single image. **Choose when** — the brand is a living system, the contexts are genuinely varied, and there is capacity to define and hold a transformation rule. ckm has no equivalent for this typology; it is HeyHi's addition, and it is the one most aligned with "living systems." **Token implications** — the **transformation rules are non-tokenizable** design intent; only the system's bounded parameters (a palette range, a grid, an allowed-variation set) are partly tokenizable. **Failure modes** — incoherence (no rule means chaos, not flexibility); a recognition tax (a moving target is harder to remember; weigh against Prägnanz). **Clusters** — C, D.

---

## Typology → tokenizable-field implications (quick map)

Typology itself is recorded in the **design-intent document** (Section 1, `design-intent-document-template.md:54`) as prose, never as a `logo.*` token field. What each typology *implies* for the fields that *are* tokenizable:

| Typology | `marks` set | `min_sizes` driver | `scale_degradation` reduction target |
|---|---|---|---|
| Wordmark | primary (+ mono) | character legibility | → lettermark / single glyph |
| Lettermark | primary, icon | already compact | usually terminal (it *is* the reduced form) |
| Pictorial | primary, icon | icon recognition | → icon |
| Abstract | icon (+ lockup) | symbol recognition | → icon (already minimal) |
| Combination | primary, icon, secondary | lockup legibility | → icon (shed wordmark) |
| Emblem | primary (+ simplified) | detail survival | → simplified emblem (constrained; see Module D) |
| Dynamic | system + a stable anchor | anchor recognition | → the stable anchor form |

Per-typology reduction paths are specified in [`scale-degradation-matrix.md`](scale-degradation-matrix.md), whose keys match the frozen `logo.scale_degradation` shape.

---

## Working with an existing mark (refresh)

Absorbed from ckm's "Logo Refresh" workflow, which HeyHi otherwise has no explicit entry for. When the engagement is a refresh rather than a new mark, the typology question becomes an **evolution-vs-revolution** question: does the brand keep its current typology and modernize execution (evolution: protect accrued symbolic equity), or change typology (revolution: trade equity for a reset)? Run this as a Concept-mode framing — generate one evolution direction and one revolution alternative — and surface the equity trade explicitly. A mark with deep symbolic equity (a well-known abstract or emblem) pays a high price for revolution; a mark that never earned distinctiveness has little equity to protect, so revolution is cheaper. Name the equity at stake before recommending.

---

## Where ckm's named styles actually land

ckm lists 19 style names under five "categories." Routed onto HeyHi's two axes:

- **Construction (→ this module's typologies):** Monogram → lettermark; Typography-first → wordmark; Pictorial → pictorial; Abstract → abstract; Emblem → emblem; Icon+Text / Badge / Shield → combination or emblem.
- **Aesthetic (→ `style-descriptor-vocabulary.md` + clusters, NOT typology):** Minimal, Bauhaus, Swiss, Constructivist, Slab, Script, Modern, Vintage. These describe *look*, not *construction*; map them through the vocabulary, not here.

This split is the correction ckm's flat list needs, and the reason Concept states a typology *and* a cluster, never one merged "style."

---

*Companion module to `heyhi-logo-system`. Cross-references: [`scale-degradation-matrix.md`](scale-degradation-matrix.md), [`mark-failure-modes.md`](mark-failure-modes.md), [`render-brief-template.md`](render-brief-template.md). Grounding: `ai-services/design-intelligence/design-intent-document-template.md`, `ai-services/design-intelligence/research/visual-language-theory.md`, `ai-services/design-intelligence/style-reference-library.md`.*

*HeyHi Confidential*
