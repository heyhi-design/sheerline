---
classification: confidential
title: "Worked example: harvest a finished engagement into candidate corrections"
status: pending
example: true
---

# Worked example batch 02: harvest an engagement (pending)

**A worked example of the dispatch convention, not a real batch.** A single-wave batch: two read-only harvest lanes in parallel, then the human curates. Shows a pending batch and a lane whose output stops at a human gate.

---

## DISPATCH-01: Harvest audit findings

**OWNS:** one harvest note in the instance's gitignored engagement folder.

**MISSION.** Read the engagement's audit reports and list every finding that recurred, each with its evidence, as candidate corrections for the human to curate.

**CONTEXT LOAD.** (1) The engagement's audit reports. (2) `os/corrections/LIFECYCLE.md`: what makes a finding a correction, factual vs behavioral. Before declaring any cited path missing, glob it.

**OUTPUT SPEC.** One note: finding, evidence, candidate correction text, factual or behavioral.

**CRITICAL CONSTRAINTS.** Read-only against the engagement. Client-identifying detail stays in the gitignored folder. Never write the live corrections registry: candidates go to intake, and a human promotes them.

**SMOKE TESTS.** Every candidate cites evidence. None is written to the live registry. The confidentiality check returns zero hits in tracked files.

**QUALITY GATE.** A curated-ready list; nothing promoted by the agent.

---

## DISPATCH-02: Harvest what the skills missed

**OWNS:** a second note in the same folder.

**MISSION.** List the places a human overrode or completed a skill's output during the engagement, as candidate skill improvements.

**SMOKE TESTS.** Each item names the skill, the override, and the evidence. Day-0 re-read.

**QUALITY GATE.** A list a human can accept or reject item by item.

*HeyHi Confidential*
