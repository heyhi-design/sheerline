# Sheerline

An agent asked to build a settings page will build one. It will reach for colors that aren't in your system, skip the empty state, write the save button in a voice nobody agreed on, and rank three layouts when the choice was yours to make. Sheerline puts your design system in front of the agent before it starts, and keeps the calls that belong to people (the critique, the positioning, which direction advances) with people.

It is a design-practice operating system: 50 skills and the governed context they run on, across 13 practice areas from user research to service design.

Designed and built by [Cody Clark](https://github.com/codysue) at [HeyHi](https://heyhi.design). MIT licensed.

**[Open Wheelhouse](https://heyhi-design.github.io/sheerline/)**, the prototype workspace over the harness, or start with the [architecture](sheerline/docs/architecture.md).

## Four verbs

Every skill does some part of one loop.

| Verb | What it means here |
|---|---|
| **Retrieve** | Load the system first: tokens, components, the practice area's foundation, the corrections already learned. |
| **Validate** | Check the output against the system before a person sees it. |
| **Grade** | Measure the result over time. Grades inform; they never gate. |
| **Learn** | Turn a recurring correction into a candidate rule a human curates, so the same miss doesn't come back. |

## The 13 practice areas

| # | Area | Skills include |
|---|---|---|
| 1 | User Research | `research-plan-author`, `insight-activation` |
| 2 | Information Architecture | `taxonomy-labeling-auditor` |
| 3 | Content Design / UX Writing | `voice-system-author`, `microcopy-states-writer` |
| 4 | Interaction Design | `interaction-inventory`, `motion-system-author` |
| 5 | Wireframing & Prototyping | `flow-and-lofi-author`, `divergence-guard`, `app-to-figma`, `heyhi-prototype-audit` |
| 6 | Visual Design | `heyhi-style-brief`, `heyhi-logo-system`, `ui-studio` |
| 7 | Design Systems | `heyhi-figma-ds-generator`, `ds-component-author`, `ds-component-change`, `heyhi-drift-repair`, `heyhi-design-intelligence-audit` |
| 8 | Accessibility | `heyhi-a11y-audit`, `heyhi-a11y-annotation` |
| 9 | Design Strategy & Product Thinking | `strategy-integrity-warden`, `design-measurability-mapper`, `intent-journey-map` |
| 10 | Business Acumen | `competitive-teardown-runner`, `design-business-case-drafter`, `experiment-readout-linter` |
| 11 | Collaboration & Facilitation | `crit-prep-and-capture`, `design-rationale-decision-record`, `heyhi-figjam-mapper` |
| 12 | DesignOps | `app-recon`, `feature-increment` |
| 13 | Service Design | `heyhi-service-blueprint` |

Every area is governed (a foundation under `sheerline/os/foundations/`, or for DesignOps an operating invariant), and every governed skill has an eval home. The full map with coverage states is `sheerline/os/foundations/registry.yaml`.

## How it behaves

- **Judgment ships empty.** When a skill reaches a call that belongs to a designer (which alternative advances, whether the copy sounds like the brand, what the product is for), it leaves a labeled slot behind a named human gate. It drafts, flags, and steps back. It does not rank its way into the decision.
- **Your values stay yours.** Anything an organization calibrates (palettes, thresholds, ratified contracts) is an instance slot with a generic default. A blank checkout resolves every slot to its default; your instance fills them without forking the skills. See [`sheerline/os/instance/`](sheerline/os/instance/README.md).
- **The quality loop sits behind a boundary.** Validation runs through a Design System MCP server reached as a tool, never embedded. The skills here call it; the evaluator and its calibration are not part of this repository.
- **Routing is a registry, not a guess.** `sheerline/skills/registry/` scores a request against every skill's trigger patterns and its `not_for` patterns, and says so when it isn't confident.

## Use it

Python 3.9 or newer and PyYAML (`pip install pyyaml`). Work from a clone, so the paths a skill names (`sheerline/os/foundations/...`) resolve.

Route a request to the right skill:

```bash
python3 sheerline/skills/registry/skill-registry.py "which states is this screen missing before we build it" --confidence
```

It names `interaction-inventory` and says it is confident. When two skills score close, it says that instead and shows both.

Make the skills discoverable in Claude Code by linking them into the project's skills folder, from the repository root:

```bash
mkdir -p .claude/skills && for d in heyhi-skills/*/; do [ -f "$d/SKILL.md" ] && ln -s "../../$d" .claude/skills/; done
```

Each skill is a `SKILL.md` with its references beside it, so any agent that reads that format can load one. Some reach the Design System MCP's `validate_output` or the Figma MCP; each `SKILL.md` names what it needs and what it does without it.

To learn the system rather than just run it, the [seminar](sheerline/seminar/README.md) runs five tracks and 21 modules, from orientation to synthesis.

## What's deliberately not here

- The Design System MCP runtime, its evaluator, and the calibration behind it.
- The live corrections corpus. The convention and a generic seed ship in `sheerline/os/corrections/`; the curated corpus does not.
- Any organization's instance data. HeyHi's own instance stays in its own tree, and no client or engagement history is in this repository.
- HeyHi's own-method skills (its voice, pages, decks, and workshops). Their generic equivalents, such as `voice-system-author`, carry the method.

## How this repository is made

Sheerline is maintained in HeyHi's monorepo and exported here one way; `EXPORT.json` names the source commit. Issues and pull requests are welcome: a change made here is folded into the source and comes back on the next export. Some files cite build history (plans, research, decision records) by path. Those links point into the monorepo and don't resolve here, and the checks count them as pointers rather than failures.

The checks CI runs:

```bash
python3 sheerline/seminar/smoke_test.py
python3 sheerline/skills/evals/measure_coverage.py
python3 sheerline/skills/evals/routing-battery/run_battery.py
python3 sheerline/studio/scripts/link-check.py
python3 sheerline/os/instance/resolve.py --check --blank
```

## Lineage

Sheerline is the design-practice sibling of [keel](https://github.com/heyhi-design/keel), the operating layer for a firm of one. It reuses keel's registry engine, loading taxonomy, corrections mechanism, and session lifecycle, and adds the one slot keel lacks: a governed foundation per practice area. [agent-corrections](https://github.com/heyhi-design/agent-corrections) is the corrections registry on its own.

## License

MIT, copyright Bay Design LLC d/b/a HeyHi. The `ui-studio` design-reference data and search engine are adapted from ui-ux-pro-max-skill under its own MIT license; see [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md).
