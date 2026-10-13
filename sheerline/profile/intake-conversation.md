---
classification: confidential
title: "Sheerline: engagement intake conversation"
adapted_from: releases/open-source/keel/profile/intake-conversation.md
---

# Sheerline: engagement intake conversation

A guided self-interview for scoping a Sheerline engagement. Work through these questions, then transcribe the answers into `profile/engagement-intake.yaml` (or, for a real client, into the instance's gitignored engagement folder, never a tracked file). Adapted from keel's `profile/intake-conversation.md`, design-scoped.

*Hermetic seal: never write a client name into a tracked file. Use a non-identifying label.*

## The engagement

1. What is this engagement, in one line, without naming the client? What stage is it (discovery, audit, build, care)?
2. Is the substrate the practice's own system (substrate `self`) or a client's? If a client's, is the NDA and contract signed, or is every deliverable still a draft held for release?

## The design system

3. Does a design system already exist? Where does it live: Figma, code, a token file, or nothing yet?
4. If tokens exist, what spec are they in, and is the system retrieved through the Design System MCP or pasted? (It should be retrieved.)
5. What is the suspected drift, in one line? (The audit confirms it; do not assume it.)

## The scope

6. Which of the 13 practice areas does this engagement touch? (See `os/foundations/registry.yaml`. Only the in-scope area foundations load conditionally.)
7. What is the accessibility target, and which standard does the jurisdiction name for any conformance claim?
8. Whose voice governs any copy? (For client work it is the client's voice, never HeyHi's.)

## The boundaries

9. Does this engagement touch the retained moat (the evaluator, the populated corpus, calibration)? If so, that work stays in the separate unpublished tree, not in a shipped artifact.
10. What judgment calls stay human on top of the standing don't-automate line?

---

*Schema: `profile/engagement-intake.yaml` · Operating principles: `os/operating-principles.md`*

*HeyHi Confidential*
