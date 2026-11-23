---
title: "Shared vocabulary (the area-3 slot)"
status: unratified
ratified_by: null
version: "0.0.0"
effective_date: null
---

# Shared vocabulary

> **Slot `content.shared-vocabulary`: the shape only.** No terms ship. An instance fills this slot with the product's ruled terms, in the shape below, and ratifies it in this file's frontmatter. Until then the resolver reports `ratified: false` and readers treat every term as a candidate.

One vocabulary for the whole product: the words the interface, the docs and the team use for the same things, so a "workspace" on one screen is not a "project" on the next. It is **versioned**: a term is added, changed or retired only by the owner's ruling, and every ruling bumps the version. Readers: `microcopy-states-writer` checks its candidate glossary against it (a conflict with a ruled term is a flag, never a silent swap), `voice-system-author` cites it in a voice block, `taxonomy-labeling-auditor` reads it as the controlled vocabulary, and the pattern catalog slot (`interaction.pattern-catalog`) names copy slots in its terms.

## Term shape

| Term | Definition | Use for | Do not use (variants seen) | Ruled by | Since | Status |
|---|---|---|---|---|---|---|

- **Term**: the one word or phrase the product uses.
- **Definition**: what it means here, in one sentence.
- **Use for** / **Do not use**: the things it names, and the variants it replaces.
- **Ruled by**: the person who ruled the term in. Blank means it is still a candidate.
- **Since**: the vocabulary version that added or last changed the term.
- **Status**: `candidate` · `ruled` · `retired` (kept in the table, so an old link still resolves).

## Versioning

Every ruling bumps the frontmatter `version` and sets the term's `Since`. A run never rules a term in, never edits a ruled term, and never bumps the version; it proposes candidates from its own glossary for the owner to rule on.

## Terms

None in the default.

