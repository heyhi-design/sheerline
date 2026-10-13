# UI Studio

**A design-system-constrained UI build skill for Claude.**

UI Studio takes a brand config (`active-brand.json`) — a structured description of a client's design system — and uses it to generate brand-compliant web interfaces. Every build runs against the config as a constraint layer: colors come from tokens, layout patterns are declared before CSS is written, WCAG AA is enforced, and copy follows the brand's voice rules.

Two skills work together:

| Skill | What it does |
|---|---|
| `ui-studio-onboard` | Extracts a client's design system (Figma, GitHub, npm, or manual) and writes `active-brand.json` |
| `ui-studio` | Reads `active-brand.json` and builds brand-constrained UI (landing pages, product screens, components) |

---

## Prerequisites

**Python 3.10 or later.** The scripts use `str.removeprefix()` and PEP 604 union type hints, both of which require 3.10+. No third-party packages are required — all scripts use the Python standard library only.

```bash
python3 --version  # Must be 3.10+
```

**A Figma MCP connection** (for Figma-based onboarding). If you are using the Designer persona path in ui-studio-onboard, your Claude agent needs the Figma MCP configured and connected to an account with at least "can view" access to the client's design system file. Phase 0 of onboarding verifies this automatically. If you are not extracting from Figma (GitHub, npm, token file, or manual mode), no MCP connection is required.

**Git** (for GitHub or git-clone onboarding modes only). Not needed for manual, token file, or Figma modes.

**npm** (for Enterprise persona / npm package extraction only). Not needed for other onboarding modes.

---

## Directory structure

```
ui-studio/                          ← This skill (builds)
├── SKILL.md                        ← Procedural instructions for the build agent
├── README.md                       ← This file
├── brand-config/
│   ├── schema.json                 ← Full JSON schema for active-brand.json
│   ├── example.json                ← Complete reference config (read this first; the generic default)
│   ├── neo-industrial.json         ← Second worked config (a dark, data-dense style)
│   ├── <name>.json                 ← Your own named configs (an instance's brand configs are instance data)
│   └── active-brand.json           ← Currently loaded config (generated, not committed)
├── scripts/
│   ├── validate.py                 ← Scores a config; enforces gates; handles --promote
│   ├── cursor-export.py            ← Generates .cursor/rules/ui-studio.mdc from active config
│   ├── switch-brand.py             ← Activates a named config as active-brand.json
│   └── search.py                   ← Semantic search over style and layout references
├── references/                     ← Context library (loaded on demand during builds)
├── data/                           ← CSV reference data for style and layout decisions
└── evals/
    └── evals.json                  ← Eval suite for validating skill output quality

ui-studio-onboard/                  ← Companion skill (extracts + writes the config)
├── SKILL.md                        ← Procedural instructions for the onboarding agent
├── .env.example                    ← Environment variables needed for auth-based extraction
├── scripts/
│   ├── setup.py                    ← Extraction script (github / npm / token-file / manual / refresh modes)
│   └── validate.py                 ← Stub — validation runs via ui-studio/scripts/validate.py
└── templates/
    ├── blank-brand-config.json     ← Minimal starter template
    ├── ux-writing-intake.md        ← Guided intake for UX writing patterns (Phase 5)
    └── designer-handoff-artifact.md ← Template for provisional→confirmed designer review
```

---

## Quick start

### 1. Onboard a design system

Run the onboarding skill with your Claude agent, or use setup.py directly for a manual config:

```bash
# Create a starter config manually (fill in values yourself)
cd heyhi-skills/ui-studio-onboard
python3 scripts/setup.py --mode manual --brand-name "Acme" --output ../ui-studio/brand-config/acme.json

# Extract from a GitHub repo
python3 scripts/setup.py --mode github \
  --brand-name "Acme" \
  --github-owner acme-org \
  --github-repo design-system \
  --token-files-path packages/tokens/src \
  --output ../ui-studio/brand-config/acme.json

# Extract from an npm package
python3 scripts/setup.py --mode npm \
  --brand-name "Acme" \
  --npm-package @acme/design-system \
  --output ../ui-studio/brand-config/acme.json
```

For Figma extraction, use the `ui-studio-onboard` SKILL.md with your Claude agent — Figma extraction requires the Figma MCP tool calls that the agent handles interactively.

### 2. Validate the config

```bash
cd heyhi-skills/ui-studio
python3 scripts/validate.py --config brand-config/acme.json --verbose --status
```

This outputs two scores:

- **Completeness score (0–100):** Is the config fully populated? Governs mode unlock.
- **Fidelity score (0–100):** How much has been confirmed against the source? Governs build trustworthiness.

A completeness score of 92 with approximate hex values still produces confidently wrong output. Both scores matter. See the unlock matrix in SKILL.md Phase 9 for the full threshold table.

### 3. Activate the config

```bash
python3 scripts/switch-brand.py --config acme
# (run from heyhi-skills/ui-studio/)
```

This copies `brand-config/acme.json` to `brand-config/active-brand.json` and regenerates the Cursor rules file.

### 4. Generate Cursor rules (optional)

If you use Cursor, the `.cursor/rules/ui-studio.mdc` file gives Cursor brand-aware code suggestions:

```bash
python3 scripts/cursor-export.py --config brand-config/acme.json
```

Regenerate this file any time the active config changes.

### 5. Build

Invoke the `ui-studio` SKILL.md with your Claude agent. The skill reads `active-brand.json` and follows the build process: Layout Declaration → section-by-section build → Quality Gate verification.

---

## The config quality gates

UI Studio uses a gate system to prevent builds from proceeding on incomplete or unconfirmed configs. Two gates are enforced by validate.py:

| Gate | What it checks | Consequence if false |
|---|---|---|
| `direction_lock_confirmed` | Style cluster, temperature, and primary direction have been locked by the designer | Hard stop for Mode A builds |
| `designer_review_complete` | A designer has reviewed extracted token values against the source Figma file | Warning for Mode A; hard stop for `--promote` |

Set these in the config after the relevant confirmation steps:

```json
"gate_status": {
  "direction_lock_confirmed": true,
  "direction_lock_date": "2026-03-01",
  "designer_review_complete": true,
  "designer_review_date": "2026-03-10",
  "designer_reviewer": "Sarah M."
}
```

---

## Version promotion

When a config is production-ready (completeness ≥ 90, fidelity ≥ 80, all gates true, no provisional fields), promote it from `0.x.y` to `1.0.0`:

```bash
python3 scripts/validate.py --config brand-config/acme.json --promote
```

A `0.x.y` version triggers a provisional warning in the generated Cursor rules file. After promotion the warning disappears.

---

## Environment variables

Copy `ui-studio-onboard/.env.example` to `ui-studio-onboard/.env` and populate the variables for the access modes you need. Auth tokens are never stored in the config — only the env var names are stored.

```bash
cp ui-studio-onboard/.env.example ui-studio-onboard/.env
# Edit .env to add your tokens
```

Variables by persona:
- **Designer / Figma:** No env var needed — handled via Figma MCP connection
- **Developer / GitHub:** `GITHUB_TOKEN`
- **Developer / non-GitHub git:** `GIT_TOKEN`
- **Enterprise / npm:** `NPM_TOKEN`
- **Private Storybook:** `STORYBOOK_AUTH_TOKEN`

---

## Reference: example config

`brand-config/example.json` is a complete, valid reference config with all blocks populated, all gates confirmed, and full field provenance. Running validate.py against it should produce completeness 100/100, fidelity 100/100, status FULL. Use it as a model for what a production config looks like. Its token maps are DTCG-native (`{"$value", "$type", "$description"}`), so it is also the default input for `tokens-build/` (`node prep.mjs` with no argument). `python3 scripts/switch-brand.py --config example` activates it.

---

## Reference: config schema

`brand-config/schema.json` documents every field in `active-brand.json`. Field descriptions explain what each value is for, when it applies, and any constraints (WCAG, ISA-101, etc.). Read the schema if you are building or editing a config manually.

---

## Tokens namespace rule

The `tokens.*` namespace in the config is a delivery surface. Never add `_note`, `_rationale`, or similar documentation keys inside `tokens.*` — they will be treated as CSS custom properties by any standard token consumer. Put rationale in `meta.implementation_notes` keyed by field path.

---

## Scripts reference

| Script | Purpose | Key flags |
|---|---|---|
| `validate.py` | Score a config; check gates; run from `ui-studio/` | `--verbose`, `--status`, `--update`, `--promote` |
| `cursor-export.py` | Generate `.mdc` Cursor rules from active config | `--config`, `--output` |
| `switch-brand.py` | Activate a named config | `--config [name]`, `--list` |
| `search.py` | Semantic search over style/layout references | `"<query>" --domain <domain>` |
| `setup.py` | Create or refresh a config (onboard skill) | `--mode [manual\|github\|npm\|token-file\|refresh]` |

All scripts are in the standard library only. No pip install required.

*HeyHi Confidential*
