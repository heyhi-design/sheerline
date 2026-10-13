---
classification: confidential
title: "Flattening-lint checklist: the Audit-mode spine"
skill: voice-system-author
loaded_by: "SKILL.md Step 1 (Audit mode)"
---

# Flattening-lint checklist

The four mechanical lint families, how each is run, and how each is reported. Held as read-and-apply reference. On-demand: load when running Audit mode.

*Internal operational reference (staged under `skill-updates/`). Written to its own read-aloud discipline; em dashes kept minimal.*

---

## What the lint is, and what it is not

The lint is **mechanical**. It scans copy for four kinds of flattening and reports where each occurs. It is **advisory**. It never blocks a ship, never approves a ship, and never renders the "this sounds like the client" verdict. That verdict is the human's, and it stays out of every lint output by construction.

The failure this lint exists to catch: copy that has gone off-voice, generic, or overclaiming, drifting toward the "sea of sameness" where a product's words become interchangeable with every competitor's. The lint names *where*. The human decides *what to do about it*.

**One line the lint must never cross.** Flagging that a passage is generic is mechanical. Deciding that the distinct alternative sounds like the client is judgment. The lint flags the first and hands the second to the human. A lint output that says "rewrite this to sound more like you, here is the on-voice version, ship it" has crossed from flagging into deciding.

---

## Family 1: Banned-word / off-voice term flags

Scan for two lists:

1. **The client's own banned list**, if supplied. These are the terms the client's voice definition rules out. Report each hit with its location.
2. **The generic-filler set** the lint carries as a default, for copy that reads as interchangeable product boilerplate:

   leverage, unlock, supercharge, disrupt, seamless, robust, empower, holistic, cutting-edge, next-gen, revolutionary, game-changing, world-class, best-in-class, transformative, innovative, effortless (as a bare claim), delight (as a verb applied to the user), elevate, streamline, one-stop, turnkey, frictionless.

Report format: the term, its location, and why it is flagged (client-banned, or generic filler). This is a scan, not a rewrite. The lint surfaces the term; it does not supply the replacement.

**Standalone-word note.** In HeyHi-authored copy the standalone word "AI" is itself a flag: describe the function instead. When linting a *client's* copy, flag standalone "AI" only if the client's own voice definition bans it; otherwise it is the client's call, not HeyHi's rule to impose. Note the distinction in the report rather than assuming.

---

## Family 2: Claim / SLA-leak flags

Flag every string that asserts an **SLA, guarantee, timeframe, uptime, security posture, compliance status, or performance number**. Each is held with a `NEEDS CLIENT CONFIRMATION` note.

Examples of what to flag:

- timeframes: "within 24 hours," "instant," "same-day"
- guarantees: "guaranteed," "always," "never lose your data"
- security / compliance: "bank-level encryption," "fully compliant," "SOC 2 certified"
- performance: "99.9% uptime," "2x faster," a specific number of anything

The lint does **not** decide whether the claim is true. It surfaces that a claim was made and must be backed by the client before the copy ships. This mirrors the Author-mode claim guardrail: the same discipline, applied to copy already written. A claim caught here is not a defect in the writing; it is an unverified fact that needs an owner.

---

## Family 3: Read-aloud flags

Read the copy aloud, one sentence at a time. Flag every sentence that does not survive it:

- **The stall.** A sentence you have to restart to get through. Usually two ideas jammed into one breath, or a clause order no person would speak.
- **The unsayable.** A sentence no one would say out loud to another person ("Utilize the aforementioned functionality to optimize your workflow").
- **The overlong.** A sentence whose thread you lose before the end. Length alone is not the flag; losing the thread is.

Report the sentence and *why* it stalls. The read-aloud test is the fastest catch for copy that is grammatically fine and humanly wrong. The lint names the stall; the human writes the smoother line, in the client's voice.

---

## Family 4: Distinctiveness / sea-of-sameness / anti-tell flags

Two sub-families, both about copy that has flattened into the generic.

### 4a. Sea-of-sameness

Flag passages that read as interchangeable product boilerplate: copy that could sit on any competitor's page with the logo swapped and no one would notice. Signals:

- opening on the company as subject ("We are a platform that...")
- category claims with nothing picturable ("the modern way to manage your work")
- benefit words with no mechanism ("faster, simpler, smarter")
- a value proposition indistinguishable from three named competitors

The lint names the passage as undifferentiated. It does **not** write the distinctive alternative: that requires the client's confirmed voice, which is the human's.

### 4b. Anti-tell (reads as machine-generated)

Flag the known language-model tells. These read as generated even when grammatically clean:

- **The reframe.** "This is not X. It is Y." / "The problem isn't X, it's Y."
- **The one-sentence reveal.** "That's the difference." dropped after a longer build.
- **The section-ending kicker.** A short punchy sentence performing impact rather than doing work.
- **The tricolon-as-drama.** Three rhythmic fragments ending a section.
- **Naming what just happened.** A sentence that labels the paragraph the reader just read.
- **The hollow transition.** "And then there's..." / "There's a version of this where..."

Report the passage and name the tell. Full catalog with rewrite models: the anti-tell section of `heyhi-skills/heyhi-voice/SKILL.md` and `brand/writing-rules.md`. The lint borrows that machinery to flag the tell in the client's copy. It does not impose HeyHi's voice on the fix.

---

## The report is advisory: how that shows in the output

Every line of the lint output obeys three constraints:

1. **Every flag carries a location and a reason.** No bare "this is off." Where, and why.
2. **No flag reads as an approval or a block.** Not "safe to ship," not "do not ship." Flags describe; they do not decide.
3. **The on-voice judgment is named as the human's.** The report closes with a "what the lint could not check" section that states plainly: whether the flagged passages, once revised, sound like the client is the human's call, and lists anything the lint had no reference to check.

A lint report that ranks copy "on-brand / off-brand," or that hands back finished on-voice rewrites, has stopped being a lint and started being the voice authority. That authority is the human's.

---

*HeyHi Confidential. Reference for `voice-system-author`. Spec source: `sheerline-skill-buildout-research-2026-08-09.md` § 4.1 (the voice-flattening defense: the "sea of sameness" evidence, the anti-tell / read-aloud discipline, provenance and claim guardrails). Anti-tell catalog: `heyhi-voice/SKILL.md`, `brand/writing-rules.md`.*
