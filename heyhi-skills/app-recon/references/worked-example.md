---
classification: confidential
title: "Worked example: an app-recon of HeyHi's own site"
skill: app-recon
loaded_by: "SKILL.md Step 1 (calibration)"
---

# Worked example: an app-recon of heyhi-website

**The instance's own site, read from real code. No client content.** This is a genuine recon of `heyhi-website/`, run to calibrate the register and prove the provenance discipline. The machine output is `worked-example.manifest.json` beside this file (it validates against the schema); this narrative is the brief a human reviews. Read it for the discipline, not to copy its content: your application's surfaces, copy, and endpoints are its own.

**The application.** `heyhi-website/` is a TanStack Start site (React 19, TanStack Router), prerendered and served static. Five surfaces, no API, no auth, no writes. That last fact is the point of this example: an honest empty capabilities block is a finding, not a gap.

**Tier.** Tier 2, by surface count (five surfaces). The backend grounding move (4) still ran and confirmed there is no API to ground, so `endpoints[]` is honestly empty rather than omitted. This is the "the backend move fires and finds nothing" case.

---

## The brief (as a human would review it)

```
# App Recon Brief: heyhi-website
Read: 2026-09-07   Source commit: 216566a   Tier: 2   Baseline (delta mode): n/a
This read informs; it renders no verdict, score, or pass/fail. It carries only ground truth and the claims it could not ground.

## Surfaces read
- home (/): src/routes, entry HomePage: 5 components, 1 copy row grounded
- log-index (/log/): src/routes/log, entry createLazyFileRoute("/log/"): 2 components, 2 copy rows grounded

## Candidate surfaces NOT yet in scope
- log-entry (/log/$slug): src/routes/log/$slug.lazy.tsx
- lab (/lab): src/routes/lab.lazy.tsx
- resources-hermetic-seal (/resources/hermetic-seal): src/routes/resources/hermetic-seal.lazy.tsx
  (These three are found in the router but not fanned out this pass. Candidates, not a decision.)

## Endpoints (Tier 2)
no API: endpoints[] is empty (verified: no createServerFn / createAPIFileRoute / defineEventHandler found in src/).
The content is compile-time (src/data/logs.ts:62 uses import.meta.glob over src/content/logs/*.md, eager); there is no runtime data path.

## Capabilities
auth_model: none   roles: []   writes: []   offline_sync: false   feature_flags: []
Read from wiring: static prerendered site, no auth boundary, no server functions, no write paths.

## In-flight
None recorded for this pass (the branch scan is available; not run exhaustively for this calibration example).

## Durable facts to integrate (queued, not applied)
- The site is single-theme (no ThemeProvider or data-theme wiring found in src/). Worth confirming and recording in the served context.
- Content is file-based (src/content/logs/*.md), compiled in. If the served context claims a runtime API, correct it.

## ⛔ Which surfaces are in scope: NEEDS HUMAN
This slot is intentionally empty. Two surfaces were fanned out (home, log-index); three are candidates.
   In-scope surfaces: ____________________

## ⛔ The tier, where the precedence rule did not decide it: NEEDS HUMAN
The precedence rule did not fire (no writes, no auth). The tier is 2 by surface count, which is unambiguous, so this slot is stated, not blank: Tier 2, whole-site inventory.
   Confirmed tier: ____________________

## ⛔ Unverified claims: NEEDS HUMAN (one line each)
- log-entry: components_used and copy: not fanned out this pass; candidate surface, selection pending.
- lab: components_used and copy: not fanned out this pass; candidate surface, selection pending.
- resources-hermetic-seal: components_used and copy: not fanned out this pass; candidate surface, selection pending.
- global: feature_flags: no flag wiring observed in the two surfaces read; not exhaustively searched.
- home: the full breakpoint token set: md and lg observed in Hero.tsx; not confirmed as the site-wide scale.

## Named gate
Brief reviewer (the engineering or design owner of this read): ____________________  Date: ______
No downstream skill consumes this manifest until this line is signed by a human.
```

---

## The provenance, spelled out

Two surfaces were fanned out fully, with real file:line on every row (see `worked-example.manifest.json`):

- **home (`/`)** mounts `HomePage` at `src/routes/index.lazy.tsx:12`, which composes `Hero`, `Problem`, `Approach`, `Founder`, `Contact` (call sites at `src/routes/index.lazy.tsx:15` through `:19`). Its one grounded copy row is the display heading "designing how your team's work, works" at `src/components/Hero.tsx:117`.
- **log-index (`/log/`)** is defined at `src/routes/log/index.lazy.tsx`, uses `Link` (`@tanstack/react-router`, imported at line 1) and `motion` (`motion/react`, line 2), and reads the compile-time `logs` array. Its grounded copy: the heading "The Log" at `src/routes/log/index.lazy.tsx:20` and the intro "Observations on living systems, intelligent infrastructure, and the organizations that build them." at line 23 (line 22 is the `<p>` tag; the string starts on 23).

The three other surfaces were not fanned out, so their components and copy are **not** invented. Each is a candidate row plus an `unverified[]` entry. That is the whole discipline: the read grounds what it read and quarantines what it did not, rather than filling the gap from the router names.

## What to notice

- **The empty capabilities block is a real finding.** `auth_model: none`, `writes: []`, `endpoints: []` were confirmed from wiring (no server functions, no API routes), not assumed. An application with no backend gets an honest empty block, which is exactly what a downstream `app-to-figma` build needs to know.
- **The "which surfaces are in scope" slot stayed empty.** The read found five surfaces and fanned out two; it did not decide the artifact covers all five, or only the Log index. That is the human's scope call.
- **The tier slot is stated, not blank, because the precedence rule was unambiguous here.** Tier 2 by surface count. The slot exists for the ambiguous case; when the answer is forced, the brief says so.
- **`unverified[]` is non-empty and honest.** Five rows, each a real gap (three deferred surfaces, one un-searched capability, one under-confirmed breakpoint set). A first read that produced an empty `unverified[]` would be the suspicious one.
- **No verdict anywhere.** There is no score, no pass/fail, no readiness call. The brief carries ground truth and the gaps in it, and hands the decisions to the reviewer at the gate.

*HeyHi Confidential. Worked example for `app-recon` (the instance's own site). Machine output: `worked-example.manifest.json`. Spec source: `plans/plan-sheerline-fdde-loop-2026-09-07.md` § 3.3.*
