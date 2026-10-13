---
classification: confidential
title: "Module 1.5 — The memory contract"
track: 1
module: "1.5"
level: foundational
prereqs: ["1.4"]
est_minutes: 30
teaches: keel
opens_files:
  - releases/open-source/keel/docs/memory.md
  - releases/open-source/keel/memory/base.py
  - releases/open-source/keel/memory/README.md
---

# Module 1.5 — The memory contract

## You are here

Corrections and the decision log are memory, but not the kind you search by meaning. This module opens the recall-by-meaning layer: a fixed twelve-tool contract over a backend you can swap without touching a single skill. Previous: [`module-1-4.md`](module-1-4.md). Next: [`module-1-6.md`](module-1-6.md).

## Learning objectives

After this you can:

- Say what "memory" means here and how it differs from the corrections registry.
- Name the twelve memory tools by their four categories.
- Name the three storage tiers and when you climb from one to the next.
- Explain why the tool names stay backend-free, and what the seam buys you.

## Concept

"Memory" in keel means one specific thing: a way for your agent to recall things from past sessions without you re-explaining them, searchable by meaning rather than by exact file and line. It is a separate concern from the corrections registry and the decision log, which are memory too, just not searchable-by-meaning memory. You do not need any of this to run keel. Reach for it when you notice yourself wishing you could search past sessions by what they were about rather than by remembering which file they live in.

The design has two halves worth holding apart: a contract that never changes, and a backend that can. The contract is twelve tools, grouped four ways. **Entries** are the durable notes: `memory_write`, `memory_search`, `memory_get`, `memory_list`, `memory_update`, `memory_delete`. **Diary** is the per-agent session log: `memory_diary_write` and `memory_diary_read`. **Relations** are a small knowledge graph of subject-predicate-object edges: `memory_add_relation` and `memory_query_relations`. And two more: `memory_link` and `memory_status`. Entries are filed by `wing` (a top namespace) and `room` (a category inside it), so recall can be scoped rather than global. A skill or workflow written against these twelve does not change when anything behind them changes.

Behind the contract sit three tiers, and you climb them only when the one below genuinely runs out. **Tier 1 is file-based, the default, no setup.** Your corrections registry and decision log are already durable memory: plain files, version-controlled, readable by you and the agent without a database. For a solo practice this is often enough, and the instruction is blunt: do not add infrastructure you do not need yet. **Tier 2 is a lightweight local backend for searchable recall**, a single-file SQLite store using built-in full-text keyword search, no server and nothing to install beyond Python. Recall by meaning is an optional follow-on on top of it, off by default, added by injecting an embedding model at a seam; when it is absent the store degrades cleanly back to keyword search rather than failing. **Tier 3 is a server-backed database, Postgres with pgvector, for scale**, handling more concurrent writers and more data than a single local file holds comfortably. Most solo practices never need it.

The point of the whole shape is the seam between the contract and the backend. It is Layer 1 of the three-layer model from module 1.1, applied one level down. Nothing that calls the memory tools names a specific backend, so moving from SQLite to Postgres later is a configuration change, not a rewrite. The interface that makes this true is one small abstract class, `MemoryAdapter`: every backend is one adapter implementing the same twelve methods, and swapping backends means writing one new adapter and pointing an environment variable at it. The skills never change. The tool names stay backend-free on purpose: `memory_write`, never `memory_write_sqlite`.

Two disciplines ride along. First, two write-time guards run before anything is stored, in shared modules so any future backend enforces them by construction: a noise filter that refuses obvious junk (a semantic store's quality depends on corpus quality), and a closed predicate vocabulary that rejects off-vocabulary or over-long relation edges rather than silently folding them, so the graph stays queryable. Second, a relations rule you will meet again: attach a status-like fact to the finest-grained named thing it is actually about, a specific project or task, not a broad, frequently-reused subject like your company name or yourself. Tools that group relations by subject to detect supersession will otherwise lump unrelated facts together just because they share that subject, and may discard real information as if it had been replaced.

## Walkthrough

Open `releases/open-source/keel/docs/memory.md`. Read the three tier sections and "The contract that stays the same across all three", with its four-category table of twelve tools. Notice the relations tip about attaching a fact to the finest-grained named thing, and the closing line that this is Layer 1 of the three-layer model applied one level down.

Now open `releases/open-source/keel/memory/base.py`, the interface itself. It is short on purpose. Read the class `MemoryAdapter` and count the abstract methods: six for entries, two for diary, two for relations, and `link` and `status`, the same twelve the contract names. Notice the argument names are clean and function-named with no backend detail, and the docstring's one claim: swapping backends is writing one new adapter and pointing `MEMORY_BACKEND` at it, and the callers never change. Then open `releases/open-source/keel/memory/README.md` and find the embedder-injection seam and the two write-time guards, so you see how the optional semantic leg attaches without the contract moving.

## Lab

Read the adapter interface and reconstruct the contract from it. Open `releases/open-source/keel/memory/base.py` and list the twelve methods by category (entries, diary, relations, and the two others). For one of them, `write`, read its parameters and note that `wing`, `room`, and `content` are required while the rest are optional. Then answer the design question the file is built to make obvious: why must the twelve tool names stay backend-free, and what specifically breaks if a skill calls a tool named for its backend instead?

**Success looks like:** the twelve methods listed by category, the required arguments of `write` named, and a one-sentence reason that a backend-named tool would force every skill to change when the backend does, which is exactly what the seam exists to prevent.

## Common misreads

- *"Memory is the corrections registry."* No. The registry and the decision log are memory, but not searchable-by-meaning memory. This module is the recall-by-meaning layer, a separate concern.
- *"You need a database to use keel."* No. Tier 1 is files, the default, and for many solo practices it is enough. You climb tiers only when the one below runs out.
- *"Semantic recall is required for Tier 2."* No. Tier 2's default is keyword search with nothing to install; recall by meaning is an optional follow-on that degrades cleanly back to keyword when absent.
- *"Swapping backends means rewriting the skills."* No. That is the one thing the `MemoryAdapter` seam prevents: one new adapter, one environment variable, and the callers stay put.

## Self-check

1. What does "memory" mean here, and how is it different from the corrections registry?
2. Name the twelve tools by their four categories.
3. What are the three tiers, and when do you climb from one to the next?
4. From the Lab: why must the tool names stay backend-free, and what breaks otherwise?

## Go deeper

- `releases/open-source/keel/docs/memory.md`: the three tiers and the twelve-tool contract in full.
- `releases/open-source/keel/memory/base.py`: the `MemoryAdapter` interface, the whole contract in one short file.
- `releases/open-source/keel/memory/README.md`: the embedder-injection seam and the two write-time guards.
- This is the three-layer model from module 1.1 applied one level down; the backend-free seam is the same owned-versus-rented discipline.

---

*HeyHi Confidential*
