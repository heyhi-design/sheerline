# Changelog

Each entry is one export from the canonical monorepo tree. `EXPORT.json` carries the exact
source commit for the current one.

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
