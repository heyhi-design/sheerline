# Changelog

Each entry is one export from the canonical monorepo tree. `EXPORT.json` carries the exact
source commit for the current one.

## [0.4.0] - 2026-11-22

Review moves to where the work is reviewed, and gates stop aging silently.

- **Gate fields on every gate** (`os/session-rules.md`): `owner`, `opened`, `max_age_days`,
  `escalate_to` and a signature (`by`, `proxy`, `date`, `where`). A gate's state is derived from
  its fields: only the owner's own signature with `proxy: no` closes it; past its age it reads
  `aged` and goes to `escalate_to` as a question, never a decision. A signature made on the
  owner's behalf records `fired (proxy)`: proof that the work reached a reviewer, never a close.
  The Framing and Entry gates still pass on their own three fields; their signature records who
  filled the block.
- **An `## Uncertain calls` section** on every gated output: the drafts the run itself is least
  sure of, unordered and unscored, or the literal `none`.
- **The drawn-by-default register, opt-in and off by default**
  (`review.drawn_by_default` in `profile/engagement-intake.yaml`). Under deadline a team may let
  a run draw its recommended answer into a register row (the alternative, the cost of changing
  course, who walks it, by when); the gate stays open until the owner walks every row.
- **Figma first as the review surface** (`review.review_surface: figma` by default; `html` and
  `room` remain). `crit-prep-and-capture` 0.2.0 takes Figma comment threads and meeting
  transcripts as capture inputs, turns threads into a revision plan, links each captured item to
  the change that answered it, and adds an uptake audit (counts only).
- **`design-rationale-decision-record` 0.3.0**: `scripts/check_record.py` fails a record that
  reads `accepted` with a blank Decision or Rationale, no owner signature, a proxy signature, or
  an unwalked register row. A record accepted before 0.3.0 has no Owner line or Proxy field, so it
  fails until its owner re-signs.
- **`heyhi-a11y-annotation` 0.2.0**: the Figma annotation handoff (targets, categories, write
  then read back, checked by `scripts/check_annotation_readback.py`) and the reconciliation
  ledger (MATCH, DELTA-FIGMA-WINS, GAP).
- **`heyhi-figjam-mapper` 0.3.0**: target a page or a node of an existing board, with board
  conventions (stamped sections, placed beside existing work, idempotent re-runs).
- **`intent-journey-map` 0.2.0**: a route-down rule (start at the lightest tier and rise only on
  a named trigger), a recorded calibration check every third map, and
  `scripts/validate_contracts.py`, which names a contract missing `schema_version`, `tier` or
  `research_question`.
- **Two new instance slots, shape only**: `interaction.pattern-catalog` (read by
  `interaction-inventory` 0.2.0) and `content.shared-vocabulary` (read by
  `microcopy-states-writer` 0.2.0). Patterns and vocabulary stay with each instance.

## [0.3.0] - 2026-10-27

First public release.

- MIT license, replacing the review-only terms. Material adapted from ui-ux-pro-max-skill (the
  `ui-studio` design-reference data and search engine) is credited in `THIRD-PARTY-NOTICES.md`
  under its own MIT license.
- No file carries an internal classification mark. The README is rewritten for public readers
  and credits the author.
- Sheerline's own docs, diagrams, and seminar describe the public posture: the scaffold ships
  under MIT, the calibrated instance stays with its owner. The conformance-audit rubric ships as
  published method; its calibration record stays instance-only.
- The seminar smoke test no longer requires a `classification` frontmatter key.
- Wheelhouse is served on GitHub Pages; the repository root redirects to it.
- Since 0.2.0: the instance layer (slot registry, resolver, blank-instance defaults, token-name
  scan), a provenance classifier and reference lint, the hardening lanes (provenance, resolver,
  token scan, overlay, lint closure), and `interaction-inventory` v0.1.4.

## [0.2.0] - 2026-10-13

- Instance data out across the tree and every shipped skill: brand defaults and fixtures,
  ratified values, client and engagement history, and owner names are generalized or moved to
  instance files that do not ship. HeyHi remains the named owner.
- HeyHi's own-method skills (voice, pages, decks, workshops) no longer ship and are filtered out
  of this copy's registry.
- `os/project-state.yaml` and `os/decision-log.md` ship as scaffold copies; the Studio snapshot
  is regenerated from the shipped tree.
- History starts here: earlier exports were withdrawn and the repository recreated.

## [0.1.1] - 2026-10-13

- `heyhi-design-bridge` Vectorize ships generic: no palette or accents, and the anchor
  ceilings and fidelity bar are an unratified slot that an instance fills in its own
  `scripts/vectorize/instance_calibration.py` (not included here). Docs and eval 3 describe
  the slot instead of quoting one instance's numbers.
- The Studio dispatch board renders Sheerline's own `os/dispatch/batches/`, seeded with two
  worked examples, instead of an instance's dispatch history. The dispatch ENV CHECK is
  placeholder-generic.
- The Studio snapshot is regenerated against the current registry.

## [0.1.0] - 2026-10-13

- First export (private): the `sheerline/` tree (13 practice areas, the subset registry, the
  seminar, the Studio prototype) plus the 54 skills its registry governs, at their monorepo
  paths.
- The seminar smoke test and the routing battery recognize an exported copy: links back to
  the monorepo are counted as pointers, and cases written against HeyHi's full registry are
  skipped and counted. The maturity meter prints its indirect-evidence column as `n/m` (not
  measured) when the corrections corpus is absent, instead of a zero that reads as "none found".
