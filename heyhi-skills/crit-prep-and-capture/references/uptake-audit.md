# The uptake audit (a grade instrument)

**The question it answers:** of the feedback items a review raised, how many reached the work? A capture pack that records what the room said is a record, not a change. The uptake audit is the instrument that reads the gap between the two: feedback item against work change, over a stated window.

It is one of two named grade instruments for the Figma-first review surface. The other, the reconciliation ledger, compares a Sheerline output against the final Figma frame (`heyhi-a11y-annotation`, `references/figma-annotation-handoff.md`). Both report counts. Neither carries a pass mark.

## Inputs

- A **capture** with one row per item: a Mode B Crit Capture, or a revision plan from the comment-revision method. Each row has a Disposition and an **Answered by** column.
- The **review date** and a **window** in days (the engagement chooses it; for example the next sprint's length). The audit reads the capture as of the window's end. Capture rows carry no dates, so the window is not a filter: run the audit at or after the window's end, and a run before it is reported as a partial, interim reading.

## The count

| Field | What it counts |
|---|---|
| `items` | every row in the capture |
| `answered` | rows whose Answered by links a change (a frame version, a commit, a PR, a prototype build) |
| `deferred` | rows with disposition `deferred` and no link |
| `dropped` | rows with disposition `dropped` and no link |
| `unanswered` | every other row: no link, and neither deferred nor dropped |

The audit reports **both rates**, so no denominator hides: `answered / items`, and `answered / (items - deferred - dropped)`. Run it with `python3 scripts/uptake_count.py <capture.md> --review-date <date> --window-days <n>`; it prints the counts, both rates and the unanswered rows by number.

## The grade series

One row per audit, appended to the engagement's own series file in its gitignored engagement folder (for example `<engagement folder>/grades/uptake-audit.csv`, with `uptake_count.py --append-csv`). The script refuses a path git would track: the series is engagement evidence and never enters a shipped or tracked file. Over time the series shows whether feedback keeps reaching the work, which a single reading cannot.

## What ships and what stays retained

The method ships: the fields, the two rates, the series shape, the script. What a good uptake rate is (a threshold, a target, a comparison across engagements) is calibration. It stays with the instance that earned it and never ships. The audit reports numbers; the owner reads them.

## What it never does

- Decide that an item was answered because a frame changed nearby. Only a link counts.
- Treat a resolved Figma thread as answered. Resolve is data; the link is the evidence.
- Score the review, the reviewers or the designer.

