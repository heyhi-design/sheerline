// resolved-slot.mjs: the Node side of the Sheerline slot resolver.
//
// Node consumers do not re-implement resolution. They read the resolver's output,
// <instance root>/resolved-slots.json (written by `python3 sheerline/os/instance/resolve.py
// --write`), from the same instance the Python consumer path (resolve.py consumer_slot) picks:
//   1. $SHEERLINE_INSTANCE (the value `none` means a blank instance). The one selector
//      consumers honor; resolve.py's --instance flag is resolve-only and never reaches here;
//   2. the checkout's default-instance pointer, when it carries one;
//   3. none: the caller uses the slot's generic default.
// An instance path is read as Python reads it: `~` or `~/...` is the home directory, a
// relative path is relative to the repo root (never the current directory), `~name` is refused.
//
//   import { resolvedSlot } from "<repo>/sheerline/os/instance/resolved-slot.mjs";
//   const rec = resolvedSlot("ui-studio.default-brand", { repoRoot });
//   // null (no instance selected), or { source, path (absolute), ratified?, ... }
//
// Throws, never falls back: a selected instance with no resolved-slots.json; a file written
// for another instance (its id or root differ from the selected instance's instance.yaml);
// a selected root that breaks resolve.py's placement rules (checkPlacement: a client root
// under .claude/worktrees/, enclosing the checkout or a registered instance, or inside the
// checkout outside a declared client root; `kind: self` or pointer mode outside the
// registered instances folder); a slot recorded with an error. A missing or borrowed value
// must never silently become the generic default or another instance's value.

import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
export const DEFAULT_REPO_ROOT = path.resolve(HERE, "..", "..", "..");
export const DEFAULT_POINTER = "releases/private/sheerline/default-instance";
export const RESOLVED_FILE = "resolved-slots.json";
export const RESOLVED_SCHEMA = "sheerline-resolved-slots/1";
export const ENV_VAR = "SHEERLINE_INSTANCE";
export const BLANK_VALUE = "none";

const real = (p) => (fs.existsSync(p) ? fs.realpathSync(p) : path.resolve(p));

// Same rule as resolve.py instance_path().
export function instancePath(value, repoRoot = DEFAULT_REPO_ROOT) {
  let v = String(value).trim();
  if (v.startsWith("~")) {
    if (v !== "~" && !v.startsWith("~/")) {
      throw new Error(`instance path ${JSON.stringify(value)}: \`~name\` is not supported ` +
        "(use ~/..., an absolute path, or a repo-relative path)");
    }
    v = os.homedir() + v.slice(1);
  }
  return real(path.isAbsolute(v) ? v : path.resolve(repoRoot, v));
}

export function selectInstance({ repoRoot = DEFAULT_REPO_ROOT, env = process.env } = {}) {
  const fromEnv = (env[ENV_VAR] || "").trim();
  if (fromEnv === BLANK_VALUE) return null;
  if (fromEnv) return instancePath(fromEnv, repoRoot);
  const ptr = path.join(repoRoot, DEFAULT_POINTER);
  if (!fs.existsSync(ptr)) return null;
  const line = fs.readFileSync(ptr, "utf8").split("\n").map((l) => l.trim())
    .find((l) => l && !l.startsWith("#"));
  return line ? instancePath(line, repoRoot) : null;
}

// Built from parts, as in resolve.py: the practice's registered instances sit one level below.
export const INSTANCES_DIR = ["releases", "private", "sheerline", "instances"].join("/");

const unquote = (s) => s.replace(/^(['"])(.*)\1$/, "$2");

// The `instance:` block of an instance.yaml: id, kind, mode, and client_roots (flow or block
// list), read the way resolve.py's loader reads them for this manifest grammar.
export function readManifest(instanceRoot) {
  const mf = path.join(instanceRoot, "instance.yaml");
  if (!fs.existsSync(mf)) throw new Error(`instance root has no instance.yaml: ${instanceRoot}`);
  const out = { file: mf, client_roots: null };
  let inBlock = false;
  let listKey = null;
  for (const raw of fs.readFileSync(mf, "utf8").split("\n")) {
    const line = raw.replace(/\s+#.*$/, "").replace(/^#.*$/, "").replace(/\s+$/, "");
    if (!line.trim()) continue;
    if (/^\S/.test(line)) { inBlock = /^instance:$/.test(line); listKey = null; continue; }
    if (!inBlock) continue;
    const item = line.match(/^ +- (.*)$/);
    if (item && listKey) { out[listKey].push(unquote(item[1].trim())); continue; }
    const kv = line.match(/^ {2}([A-Za-z_]+):\s*(.*)$/);
    if (!kv) continue;
    listKey = null;
    const [, key, value] = kv;
    if (key === "client_roots") {
      if (value === "") { out.client_roots = []; listKey = "client_roots"; }
      else if (/^\[.*\]$/.test(value)) {
        out.client_roots = value.slice(1, -1).split(",").map((s) => unquote(s.trim())).filter(Boolean);
      } else {
        out.client_roots = value; // a scalar: refused below, as resolve.py refuses it
      }
    } else if (["id", "kind", "mode"].includes(key)) {
      out[key] = value;
    }
  }
  if (out.id === undefined || /^-?\d+$/.test(out.id) || !unquote(out.id).trim()) {
    throw new Error(`${mf}: instance.id must be a non-empty string (quote a numeric id), got ${out.id}`);
  }
  out.id = unquote(out.id);
  out.kind = out.kind === undefined ? undefined : unquote(out.kind);
  out.mode = out.mode === undefined ? undefined : unquote(out.mode);
  return out;
}

export function instanceId(instanceRoot) {
  return readManifest(instanceRoot).id;
}

const within = (p, base) => {
  const rel = path.relative(base, p);
  return rel === "" || (!rel.startsWith("..") && !path.isAbsolute(rel));
};

function registeredInstances(repoRoot) {
  const d = real(path.join(repoRoot, INSTANCES_DIR));
  if (!fs.existsSync(d)) return [];
  return fs.readdirSync(d).map((n) => path.join(d, n))
    .filter((p) => fs.existsSync(path.join(p, "instance.yaml"))).map(real);
}

function practiceClientRoots(repoRoot) {
  const roots = new Set();
  for (const inst of registeredInstances(repoRoot)) {
    const m = readManifest(inst);
    if (m.kind !== "self" || m.client_roots === null) continue;
    if (!Array.isArray(m.client_roots)) {
      throw new Error(`${m.file}: instance.client_roots must be a list of folders`);
    }
    for (const c of m.client_roots) {
      const n = path.posix.normalize(c.replace(/\\/g, "/"));
      if (!n || n === "." || n.startsWith("/") || n.startsWith("..")) {
        throw new Error(`${m.file}: client root ${c} must be a folder inside the checkout`);
      }
      roots.add(n.replace(/\/+$/, "") + "/");
    }
  }
  return [...roots];
}

// The placement rules resolve.py load_instance() enforces, applied to the selected root.
export function checkPlacement(root, manifest, repoRoot) {
  const r = real(root);
  const repo = real(repoRoot);
  const registered = registeredInstances(repoRoot).includes(r);
  const mf = manifest.file;
  if (manifest.kind === "client" && manifest.mode === "pointer") {
    throw new Error(`${mf}: a client instance is rooted; pointer mode is for the practice's own instance`);
  }
  if ((manifest.kind === "self" || manifest.mode === "pointer") && !registered) {
    throw new Error(`${mf}: \`kind: self\` and pointer mode are allowed only for an instance ` +
      `registered in ${INSTANCES_DIR}/<id>/ of the checkout ${repo}`);
  }
  if (manifest.kind !== "client") return;
  if (registered) throw new Error(`${mf}: a client instance root never sits in the tracked ${INSTANCES_DIR}/ folder`);
  if ((r + "/").toLowerCase().includes("/.claude/worktrees/")) {
    throw new Error(`refusing a client instance root under a .claude/worktrees/ checkout: ${r}`);
  }
  if (within(repo, r)) throw new Error(`${mf}: a client instance root may not be the checkout or enclose it`);
  if (registeredInstances(repoRoot).some((reg) => within(reg, r))) {
    throw new Error(`${mf}: a client instance root may not enclose the practice's registered instance`);
  }
  if (within(r, repo)) {
    const rel = path.relative(repo, r).split(path.sep).join("/").toLowerCase() + "/";
    if (!practiceClientRoots(repoRoot).some((c) => rel.startsWith(c.toLowerCase()))) {
      throw new Error(`${mf}: a client instance root inside the checkout must sit in a client root ` +
        "the practice declares");
    }
  }
}

export function resolvedSlot(slotId, { repoRoot = DEFAULT_REPO_ROOT, env = process.env } = {}) {
  const root = selectInstance({ repoRoot, env });
  if (root === null) return null;
  const file = path.join(root, RESOLVED_FILE);
  if (!fs.existsSync(file)) {
    throw new Error(`${file} is missing: run python3 sheerline/os/instance/resolve.py --write ` +
      `with ${ENV_VAR} set to the instance at ${root}`);
  }
  const body = JSON.parse(fs.readFileSync(file, "utf8"));
  if (body.schema !== RESOLVED_SCHEMA) {
    throw new Error(`${file}: schema must be ${RESOLVED_SCHEMA}; rerun resolve.py --write`);
  }
  const manifest = readManifest(root);
  checkPlacement(root, manifest, repoRoot);
  const id = manifest.id;
  if (typeof body.instance !== "string" || body.instance !== id) {
    throw new Error(`${file} was written for instance ${JSON.stringify(body.instance)}, but the ` +
      `selected instance is ${JSON.stringify(id)}: rerun resolve.py --write for this instance`);
  }
  if (!body.instance_root || instancePath(body.instance_root, repoRoot) !== real(root)) {
    throw new Error(`${file} was written for the instance root ${JSON.stringify(body.instance_root)}, ` +
      `not ${real(root)}: rerun resolve.py --write for this instance`);
  }
  const rec = (body.slots || {})[slotId];
  if (!rec) throw new Error(`slot ${slotId} is not in ${file}; rerun resolve.py --write`);
  if (rec.error) throw new Error(`slot ${slotId}: ${rec.error}`);
  const abs = (p) => (path.isAbsolute(p) ? p : path.resolve(repoRoot, p));
  return {
    ...rec,
    instance: id,
    path: rec.path ? abs(rec.path) : null,
    paths: rec.paths ? rec.paths.map(abs) : undefined,
  };
}

// CLI for checks: node resolved-slot.mjs <slot-id>  -> JSON (or "null")
if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    console.log(JSON.stringify(resolvedSlot(process.argv[2])));
  } catch (err) {
    console.error(`resolved-slot: ${err.message}`);
    process.exit(2);
  }
}
