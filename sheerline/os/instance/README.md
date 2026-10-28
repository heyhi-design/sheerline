---
title: "Sheerline instance layer"
---

# Sheerline instance layer

Sheerline is a scaffold: skills, slots with generic defaults, templates, and stages. An
**instance** is one practice's values: its design-system contract, brand configs, palettes,
ratified thresholds, and its own build history. This folder is the seam between the two.

| File | What it is |
|---|---|
| `slots.yaml` | The slot registry: every place a scaffold skill reads an instance's value, with its generic default, kind, ratification rule, and the in-tree path class an instance may keep the value at. |
| `instance.schema.json` | The schema of an instance manifest (`instance.yaml`). |
| `resolve.py` | The resolver (standard library only). A skill asks for a slot and gets the instance's value or the generic default; with neither it fails loudly, naming the slot and the `instance.yaml` key that fills it. |
| `defaults/` | Generic defaults for slots whose owning skill has no generic copy of its own yet. |
| `tests/` | The resolver's tests (`python3 -m pytest sheerline/os/instance/tests -q`). |

The blank manifest is `sheerline/profile/instance.template.yaml`.

## The instance root

```
<instance-root>/
├── instance.yaml   manifest: id, kind (self | client), slot fills, contract + MCP pointers
├── intake/         the filled engagement-intake.yaml
├── contract/       the DS-MCP data contract onboarding writes (app/ holds application context)
├── mcp/            build record: image ref, SBOM, tool-surface pin, component schedule
├── slots/          values for scaffold slots
└── history/        the instance's decision log, project state, plans, dispatch batches
```

A client instance root lives in the practice's gitignored engagement folder, never inside a
`.claude/worktrees/` checkout (the resolver refuses one there, because the worktree and the
data with it are reaped). It is passed by path, never discovered by scanning.

## Which instance the resolver reads

1. `--instance <root>` (or `instance=` from Python): **resolve-only.** It applies to that one
   `resolve.py` run (for example `--write` for a named instance) and never reaches a consumer;
2. `$SHEERLINE_INSTANCE` (`none` means a blank instance): **the one selector consumers
   honor.** A skill's Python code calls `consumer_slot()`; Node code reads through
   `resolved-slot.mjs`. To point a skill at an instance, export this variable;
3. the checkout's default-instance pointer, when it carries one (the practice's own monorepo
   does, so its sessions resolve its own values with no flag);
4. otherwise none, and every slot resolves to its generic default.

A relative instance path is relative to the repo root, never the current directory; `~` and
`~/...` are the home directory (Python and Node alike); `~name` is refused.

The resolver never reads one instance's value on behalf of another, and it takes these rules
from the practice's own registered instances, never from the manifest being read:

- `kind: self` and `mode: pointer` are allowed only for an instance registered in the
  practice's instances folder (a direct child folder holding `instance.yaml`); a client
  instance is `kind: client`, `mode: rooted`, and never sits in that folder;
- a client root never is or encloses the checkout or a registered instance, and inside the
  checkout it sits in a client root the practice declares;
- a rooted instance's fills sit under its own root;
- no fill sits under any other folder that holds an `instance.yaml`, registered or not;
- a pointer fill never sits under a client root the practice declares (the union of every
  registered self instance's `client_roots`); with none declared, pointer fills are refused;
- `resolved-slots.json` records the instance id and root it was written for; a consumer that
  finds one written for another instance stops, rather than reading it.

## Commands

```
python3 sheerline/os/instance/resolve.py --list                 # where every slot resolves
python3 sheerline/os/instance/resolve.py --slot <id>            # one slot's record, as JSON
python3 sheerline/os/instance/resolve.py --write                # resolved-slots.json for Node readers
python3 sheerline/os/instance/resolve.py --check --blank        # a blank instance gets only generic defaults
python3 sheerline/os/instance/resolve.py --check --expect <fixture.json>
```

`--write` emits `resolved-slots.json` into the instance root; Node consumers read the paths
from it. Rerun it after any slot fill changes. `--list` exits 1 when any required slot is in
ERROR.

## Adding a slot

Declare it in `slots.yaml` with a generic default (or `default: null` plus `optional: true`),
name its `in_tree` path class if an instance keeps the value inside a shipped root, and have
the consuming skill resolve it instead of reading a file by name. Each instance fills it in its
own `instance.yaml`. Nothing is added to an exclusion list by hand: an export derives its
exclusions from the registry and the registered instances' fills.
