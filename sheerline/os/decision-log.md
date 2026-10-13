---
classification: confidential
title: "Sheerline Decision Log"
adapted_from: keel os/decision-log.template.md
---

# Sheerline Decision Log

**Append-only. The permanent record of this instance's significant decisions.**

This is the scaffold copy. An instance keeps its own log here: the decisions that change the direction of its practice, newest first. The instance that maintains Sheerline keeps its build history in its own copy; it does not ship.

## The rules

1. **Append-only.** Never edit an existing entry. The one exception is a security redaction (a leaked secret or client name), which is edited in place and recorded in a new appended entry so the edit is never silent.
2. **Newest-first.** Prepend new entries directly under `## Entries`.
3. **Read before you write.** Read the last few entries before appending, to check for overlap or supersession.
4. **Log decisions, not activity.** An entry earns its place when it changes the direction of the work.

## Entry shape

```
## YYYY-MM-DD - [area or scope] One-line decision

**Type:** ... · **Criticality:** ... · **Contributor:** ...

### What We Had
### What Changed
### What We Decided
### Documents Affected
```

---

## Entries

<!-- Prepend new entries directly below this line, newest first. -->

## YYYY-MM-DD - [sheerline] Instance stood up from the scaffold

**Type:** founding · **Criticality:** high · **Contributor:** the instance owner

### What We Had
The Sheerline scaffold: the 13-area foundations registry, the design-scoped skill registry, the seminar, and the Studio prototype, with no instance data.

### What Changed
The instance filled its engagement intake (`profile/engagement-intake.yaml`), chose its practice areas in scope, and recorded its own calibrations in the instance files its skills read.

### What We Decided
Replace this entry with the instance's founding decision.

### Documents Affected
`profile/engagement-intake.yaml`, this log.

---

*Session rules: `os/session-rules.md`*

*HeyHi Confidential*
