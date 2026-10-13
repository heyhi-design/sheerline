# Worked example — a filled Drift-Repair Run

*HeyHi Confidential. Loaded on demand by `heyhi-drift-repair/SKILL.md` Step 1. A filled run on the synthetic fixtures (`evals/fixtures/`). Read it to calibrate the shape and register of the output — the deviation records, the proposals, the learn candidate. Do not copy its findings. This renders the SKILL.md output structure over the engine's real behavior on the fixtures — the same 9-applied / 3-proposed / 1-learn-candidate split the harness asserts (checks C1, C8, OQ-3). The harness itself (`python3 heyhi-skills/heyhi-drift-repair/evals/run.py`) prints a pass/fail check table, not this report; the `dev-*` ids below are display references, not an engine field.*

The input: 12 located findings against one instance — 9 deterministic call-site drifts in `drifted.css`, one judged contrast finding, one hybrid detached-instance finding, one novel drift with no registered transform. Shown here in **auto-apply mode** (the explicit opt-in) so the applied tier is visible; the default proposal-first mode moves every deterministic row into Proposals with its transform attached and writes nothing.

---

```
# Drift-Repair Run — synthetic-fixture · drifted.css
Mode: auto-apply    Findings in: 12    Run: 2026-09-01

## Applied repairs (deterministic, re-validated)
| Finding | Location | before → after | Re-validated | Provenance | Deviation |
|---------|----------|----------------|--------------|------------|-----------|
| F1 | .btn / color | color: #111827 → color: var(--text-primary) | pass | automated | dev-F1 |
| F2 | .card / padding | padding: 16px → padding: var(--space-4) | pass | automated | dev-F2 |
| F3 | .modal / z-index | z-index: 400 → z-index: var(--z-modal) | pass | automated | dev-F3 |
| F4 | .h1 / font-size | font-size: 16px → font-size: var(--font-size-base) | pass | automated | dev-F4 |
| F5 | .title / font-weight | font-weight: 600 → font-weight: var(--font-weight-semibold) | pass | automated | dev-F5 |
| F6 | .body / line-height | line-height: 1.6 → line-height: var(--font-lineHeight-relaxed) | pass | automated | dev-F6 |
| F7 | .fade / transition-duration | transition-duration: 200ms → var(--motion-duration-200) | pass | automated | dev-F7 |
| F8 | .fade / transition-timing-function | cubic-bezier(0.4, 0, 0.2, 1) → var(--motion-easing-ease-in-out) | pass | automated | dev-F8 |
| F9 | .card / border-width | border-width: 2px → border-width: var(--border-width-thick) | pass | automated | dev-F9 |

## Proposals (human-confirm — NOTHING written)
| Finding | detection | Why propose-only | Ready transform | Provenance | Named gate |
|---------|-----------|------------------|-----------------|------------|------------|
| F10 | judged | contrast "declared safe for this use" is a design decision; at times_fired 6 it is also promotion-eligible — surfaced for the curator, not taken | (none — human call) | [candidate: needs confirmation] | Repair-confirmation sign-off |
| F11 | hybrid | v1 propose-both: no seeded emitted-code structural transform (the detachment lives on json_artifact) | (none in v1) | [candidate: needs confirmation] | Repair-confirmation sign-off |
| F12 | (unmatched) | novel drift — no registered transform; the validator's nearest-token hint is a guess, not a fix | color: #BADA55 → color: var(--accent-primary) | [inferred] | Repair-confirmation sign-off |

## Learn candidates (routed to corrections-intake/, NOT the live registry)
- corrections-intake/2026-09-01-hardcoded-hex-bypasses-token.md — F1 recurred across sessions;
  authored the schema superset (detection: deterministic, known_bad `.btn { color: #111827; }`,
  expected `.btn { color: var(--text-primary); }`); Status: proposed; decide-to-adopt slot EMPTY.

## ⛔ Repair-confirmation — NEEDS HUMAN
Every deviation record above is confirmed: false until this line is signed.
   Confirmed by: ____________________  Date: ______
```

---

## What the example demonstrates (the load-bearing properties)

- **Nine applied, three proposed — and the split is by `detection`, not `severity`.** F10 (contrast) is `severity: factual` yet `detection: judged`, so it is proposed, never applied. Keying on `severity` would have auto-applied a contrast repair — the exact thing the charter forbids.
- **Every applied repair re-validated before it landed** (the "pass" column), and each carries a reversible deviation record with `confirmed: false`. A repair that failed re-validation would appear in Proposals with reason "rolled back," not here.
- **`[inferred]` and `automated` never co-occur.** F12's inferred token-guess is *proposed*, never applied — an inferred value is never auto-written.
- **The aggregate proof:** applying the nine repairs turns `drifted.css` into `clean.css` byte-for-byte, and reverting any one re-fires its finding (the `known_bad`/`expected` discrimination property, `schema.yaml:147-148`).
- **The learn step authored, not filed.** The recurring F1 produced a `corrections-intake/` candidate carrying the design-extension fields the repair loop uniquely knows (`detection`, `known_bad`, `expected`) — a superset of `insight-activation`'s emit — with the decide-to-adopt slot empty behind the human firewall.
- **OQ-4 surfaced, not taken.** The over-threshold contrast seed is flagged promotion-eligible for the curator; the loop never promotes.
