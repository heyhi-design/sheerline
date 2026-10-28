"""Tests for the Sheerline slot resolver (sheerline/os/instance/resolve.py).

Runs under pytest or the standard library alone:

    python3 -m pytest sheerline/os/instance/tests -q
    python3 -m unittest discover -s sheerline/os/instance/tests -p 'test_*.py'

Tests that need the practice's own instance (instance 0) or the monorepo's export overlay skip
in a checkout that does not carry them (an export).
"""
from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
RESOLVE = ROOT / "sheerline/os/instance/resolve.py"
SLOTS = ROOT / "sheerline/os/instance/slots.yaml"
TEMPLATE = ROOT / "sheerline/profile/instance.template.yaml"
SCHEMA = ROOT / "sheerline/os/instance/instance.schema.json"
OVERLAY_CONTRACT = (ROOT / "releases/private/sheerline/overlay/heyhi-skills/design-system-care-monthly"
                    / "references/adoption-definitions-contract.md")

_spec = importlib.util.spec_from_file_location("sheerline_resolve_under_test", RESOLVE)
R = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(R)

# Built from the resolver's own constant, so this shipped file cites no instance-root path and
# the provenance lint needs no instance-class exemption for it.
INSTANCE0 = ROOT / R.INSTANCES_DIR / "heyhi"
FIXTURE = INSTANCE0 / "tests/instance0-pre-w1.json"

try:
    import yaml  # noqa: F401
    HAVE_YAML = True
except ImportError:
    HAVE_YAML = False

try:
    import jsonschema  # noqa: F401
    HAVE_JSONSCHEMA = True
except ImportError:
    HAVE_JSONSCHEMA = False


class _Env:
    """Run a block with $SHEERLINE_INSTANCE set to a value or removed."""

    def __init__(self, value):
        self.value = value

    def __enter__(self):
        self.old = os.environ.get(R.ENV_VAR)
        if self.value is None:
            os.environ.pop(R.ENV_VAR, None)
        else:
            os.environ[R.ENV_VAR] = str(self.value)

    def __exit__(self, *exc):
        if self.old is None:
            os.environ.pop(R.ENV_VAR, None)
        else:
            os.environ[R.ENV_VAR] = self.old


MINI_SLOTS = """\
schema: sheerline-slots/1
slots:
  - id: demo.with-default
    owner: sheerline
    kind: brand
    format: json
    requires_ratification: false
    consumers: [python]
    default: defaults/demo.json
    optional: false
    in_tree: [tree/demo-instance.json]
    values: [name]
  - id: demo.no-default
    owner: sheerline
    kind: calibration
    format: markdown
    requires_ratification: true
    consumers: [markdown]
    default: null
    optional: false
    in_tree: []
    values: [status]
"""


def make_root(tmp: Path) -> Path:
    """A scratch repo root carrying a two-slot registry and a generic default."""
    (tmp / "sheerline/os/instance").mkdir(parents=True)
    (tmp / "sheerline/os/instance/slots.yaml").write_text(MINI_SLOTS)
    (tmp / "defaults").mkdir()
    (tmp / "defaults/demo.json").write_text(json.dumps({"name": "generic"}))
    return tmp


def make_instance(base: Path, kind="client", mode="rooted", fills="", iid="demo",
                  client_roots=None) -> Path:
    base.mkdir(parents=True, exist_ok=True)
    roots = f"  client_roots: [{', '.join(client_roots)}]\n" if client_roots else ""
    (base / "instance.yaml").write_text(
        "schema: sheerline-instance/1\n"
        f"instance:\n  id: {iid}\n  kind: {kind}\n  mode: {mode}\n  owner: someone\n{roots}"
        f"slots:\n{fills or '  {}'}\n".replace("slots:\n  {}", "slots: {}"))
    return base


class MiniYaml(unittest.TestCase):
    @unittest.skipUnless(HAVE_YAML, "PyYAML not installed")
    def test_agrees_with_pyyaml_on_every_instance_file(self):
        import yaml
        files = [SLOTS, TEMPLATE] + ([INSTANCE0 / "instance.yaml"] if INSTANCE0.is_dir() else [])
        for f in files:
            text = f.read_text(encoding="utf-8")
            self.assertEqual(R.load_yaml(text), yaml.safe_load(text), f)

    def test_rejects_unsupported_syntax(self):
        with self.assertRaises(ValueError):
            R.load_yaml("a: &anchor 1\nb: *anchor\n")
        with self.assertRaises(ValueError):
            R.load_yaml("a: 1\na: 2\n")


class NoInstancePathCited(unittest.TestCase):
    def test_shipped_instance_layer_files_cite_no_instance_root(self):
        # H2 item 7: the shipped resolver files named the instances folder literally, so the
        # export's provenance lint (an `instance`-class reference) needed an exemption for them.
        # Only the default-instance pointer (a declared exemption) may be named.
        needle = "/".join(("releases", "private", "sheerline", "instances"))
        base = ROOT / "sheerline/os/instance"
        kept_home = R.instance_paths(ROOT)  # instance history here (MIGRATION.md) never ships
        offenders = [p.relative_to(ROOT).as_posix() for p in sorted(base.rglob("*"))
                     if p.is_file() and "__pycache__" not in p.parts
                     and not R._matches(p.relative_to(ROOT).as_posix(), kept_home)
                     and needle in p.read_text(encoding="utf-8", errors="replace")]
        self.assertEqual(offenders, [])


class Registry(unittest.TestCase):
    def test_every_slot_is_well_formed(self):
        slots = R.load_slots(ROOT)
        self.assertTrue(slots)
        for sid, s in slots.items():
            self.assertRegex(sid, r"^[a-z0-9-]+\.[a-z0-9-]+$")
            owner = s["owner"]
            self.assertTrue(owner == "sheerline" or (ROOT / "heyhi-skills" / owner).is_dir(), sid)
            if s.get("default"):
                self.assertTrue((ROOT / s["default"]).exists(), f"{sid} default missing")
            else:
                self.assertTrue(s.get("optional") or s.get("derived_from"),
                                f"{sid}: no default, so it must be optional or derived")
            for p in s["in_tree"]:
                self.assertFalse(p.startswith(("sheerline/os/instance/", "releases/")), p)


class Blank(unittest.TestCase):
    def test_blank_check_is_clean(self):
        self.assertEqual(R.check_blank(ROOT), [])

    def test_blank_resolves_generic_defaults_and_reports_unratified(self):
        res = R.resolve_all(ROOT, blank=True)
        self.assertIsNone(res["instance"])
        rec = res["slots"]["care.adoption-contract"]
        self.assertEqual(rec["source"], "default")
        self.assertIs(rec["ratified"], False)
        vec = res["slots"]["vectorize.calibration"]
        self.assertIs(vec["ratified"], False)
        self.assertIsNone(vec["values"]["PALETTE"])
        derived = res["slots"]["ui-studio.cursor-rules"]
        self.assertEqual(derived["source"], "derived")
        self.assertEqual(derived["path"], res["slots"]["ui-studio.default-brand"]["path"])
        for sid in ("history.decision-log", "history.project-state"):
            self.assertIn("error", res["slots"][sid])
            self.assertTrue(res["slots"][sid]["optional"])

    def test_cli_blank_check_exit_zero(self):
        r = subprocess.run([sys.executable, str(RESOLVE), "--check", "--blank"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


@unittest.skipUnless(FIXTURE.is_file(), "instance 0 is not in this checkout (an export)")
class InstanceZero(unittest.TestCase):
    def test_no_flag_reproduces_the_pre_w1_fixture(self):
        with _Env(None):
            fixture = json.loads(FIXTURE.read_text())
            self.assertEqual(R.check_expect(fixture, ROOT), [])
            r = subprocess.run([sys.executable, str(RESOLVE), "--check", "--expect", str(FIXTURE)],
                               capture_output=True, text=True, env={k: v for k, v in os.environ.items()
                                                                   if k != R.ENV_VAR})
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_expect_check_catches_a_changed_value(self):
        fixture = json.loads(FIXTURE.read_text())
        fixture["slots"]["vectorize.calibration"]["values"]["PALETTE"][0] = "#000001"
        with _Env(None):
            problems = R.check_expect(fixture, ROOT)
        self.assertTrue(any("vectorize.calibration.values" in p for p in problems), problems)

    def test_expect_check_fails_with_no_instance(self):
        fixture = json.loads(FIXTURE.read_text())
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            shutil.copytree(ROOT / "sheerline/os/instance", root / "sheerline/os/instance",
                            ignore=shutil.ignore_patterns("tests", "__pycache__"))
            problems = R.check_expect(fixture, root)
        self.assertTrue(any("no instance selected" in p for p in problems), problems)

    def test_ratification_is_reported(self):
        with _Env(None):
            res = R.resolve_all(ROOT)
        self.assertEqual(res["instance"], "heyhi")
        self.assertIs(res["slots"]["care.adoption-contract"]["ratified"], True)
        self.assertIs(res["slots"]["vectorize.calibration"]["ratified"], True)

    def test_committed_resolved_slots_json_is_current(self):
        committed = (INSTANCE0 / R.RESOLVED_FILE).read_text()
        with _Env(None):
            inst_root, fresh = R.resolved_text(ROOT)
        self.assertEqual(inst_root.resolve(), INSTANCE0.resolve())
        self.assertEqual(fresh, committed,
                         "resolved-slots.json is stale: run resolve.py --write and commit it")

    def test_instance_zero_validates_against_the_schema(self):
        if not HAVE_YAML or not HAVE_JSONSCHEMA:
            self.skipTest("PyYAML or jsonschema not installed")
        import jsonschema
        import yaml
        schema = json.loads(SCHEMA.read_text())
        jsonschema.validate(yaml.safe_load((INSTANCE0 / "instance.yaml").read_text()), schema)


class Selection(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.root = make_root(self.tmp / "repo")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _rooted(self, name="client-a", value="slots/demo.json"):
        inst = make_instance(self.tmp / name,
                             fills=f"  demo.with-default:\n    value: {value}")
        (inst / "slots").mkdir(exist_ok=True)
        (inst / "slots/demo.json").write_text(json.dumps({"name": name}))
        return inst

    def test_env_selects_an_instance_and_flag_overrides_env(self):
        a, b = self._rooted("client-a"), self._rooted("client-b")
        with _Env(a):
            self.assertEqual(R.resolve_slot("demo.with-default", self.root)["values"]["name"], "client-a")
            self.assertEqual(R.resolve_slot("demo.with-default", self.root, instance=str(b))["values"]["name"],
                             "client-b")
        with _Env(None):
            rec = R.resolve_slot("demo.with-default", self.root)
            self.assertEqual((rec["source"], rec["values"]["name"]), ("default", "generic"))

    def test_default_pointer_is_used_when_present(self):
        inst = self._rooted("pointed")
        ptr = self.root / R.DEFAULT_POINTER
        ptr.parent.mkdir(parents=True)
        ptr.write_text(f"# comment\n{inst}\n")
        with _Env(None):
            self.assertEqual(R.select_instance(self.root)[1], R.DEFAULT_POINTER)
            self.assertEqual(R.resolve_slot("demo.with-default", self.root)["values"]["name"], "pointed")
            self.assertEqual(R.resolve_slot("demo.with-default", self.root, blank=True)["source"], "default")
        with _Env(R.BLANK_VALUE):
            self.assertIsNone(R.select_instance(self.root)[0])
            self.assertEqual(R.resolve_slot("demo.with-default", self.root)["source"], "default")

    def test_no_default_and_no_value_fails_loudly(self):
        with _Env(None):
            with self.assertRaises(R.SlotError) as cm:
                R.resolve_slot("demo.no-default", self.root)
        msg = str(cm.exception)
        self.assertIn("demo.no-default", msg)
        self.assertIn("slots.demo.no-default.value", msg)
        inst = self._rooted()
        with self.assertRaises(R.SlotError) as cm:
            R.resolve_slot("demo.no-default", self.root, instance=str(inst))
        self.assertIn("slots.demo.no-default.value", str(cm.exception))
        self.assertIn(str(inst / "instance.yaml"), str(cm.exception))

    def test_cli_names_the_slot_and_key_with_a_nonzero_exit(self):
        r = subprocess.run([sys.executable, str(RESOLVE), "--root", str(self.root), "--blank",
                            "--slot", "demo.no-default"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)
        self.assertIn("demo.no-default", r.stderr)
        self.assertIn("slots.demo.no-default.value", r.stderr)

    def test_unknown_slot_fails(self):
        with self.assertRaises(R.SlotError):
            R.resolve_slot("demo.nope", self.root, blank=True)

    def test_client_root_under_worktrees_is_refused(self):
        inst = make_instance(self.tmp / "ws/.claude/worktrees/some-tree/engagements/x/sheerline-instance")
        with self.assertRaises(R.InstanceError) as cm:
            R.resolve_slot("demo.with-default", self.root, instance=str(inst))
        self.assertIn(".claude/worktrees", str(cm.exception))
        r = subprocess.run([sys.executable, str(RESOLVE), "--root", str(self.root),
                            "--instance", str(inst), "--list"], capture_output=True, text=True)
        self.assertNotEqual(r.returncode, 0)

    def test_practice_own_instance_under_worktrees_is_allowed(self):
        # The practice's own instance is registered in the checkout's instances folder; the
        # checkout itself may be a .claude/worktrees/ tree.
        wt_root = make_root(self.tmp / "ws/.claude/worktrees/some-tree")
        inst = make_instance(wt_root / R.INSTANCES_DIR / "self", kind="self", mode="rooted")
        self.assertEqual(R.resolve_slot("demo.with-default", wt_root, instance=str(inst))["source"],
                         "default")

    def test_self_relabeled_client_root_under_worktrees_is_refused(self):
        # H2 item 4 / review case 1: relabeling a client root `kind: self` used to skip the
        # worktree refusal. `kind: self` is allowed only for a registered instance now.
        inst = make_instance(self.tmp / "ws/.claude/worktrees/t/engagements/acme/sheerline-inst",
                             kind="self", mode="rooted",
                             fills="  demo.with-default:\n    value: slots/v.json")
        (inst / "slots").mkdir()
        (inst / "slots/v.json").write_text(json.dumps({"name": "acme"}))
        with self.assertRaises(R.InstanceError) as cm:
            R.resolve_slot("demo.with-default", self.root, instance=str(inst))
        self.assertIn("allowed only for an instance registered", str(cm.exception))

    def test_pointer_mode_outside_the_instances_folder_is_refused(self):
        # H2 item 4 / review case 3: a pointer-mode manifest outside the instances folder.
        inst = make_instance(self.tmp / "loose", kind="self", mode="pointer",
                             fills="  demo.with-default:\n    value: defaults/demo.json",
                             client_roots=["engagements/"])
        with self.assertRaises(R.InstanceError) as cm:
            R.resolve_slot("demo.with-default", self.root, instance=str(inst))
        self.assertIn("allowed only for an instance registered", str(cm.exception))

    def test_client_instance_in_the_instances_folder_is_refused(self):
        inst = make_instance(self.root / R.INSTANCES_DIR / "acme", kind="client", mode="rooted")
        with self.assertRaises(R.InstanceError) as cm:
            R.resolve_slot("demo.with-default", self.root, instance=str(inst))
        self.assertIn("never sits in the tracked", str(cm.exception))

    def test_client_pointer_mode_is_refused(self):
        inst = make_instance(self.tmp / "c", kind="client", mode="pointer")
        with self.assertRaises(R.InstanceError):
            R.resolve_slot("demo.with-default", self.root, instance=str(inst))

    def test_rooted_fill_outside_its_root_is_refused(self):
        other = self._rooted("client-other")
        inst = make_instance(self.tmp / "client-thief",
                             fills=f"  demo.with-default:\n    value: {other / 'slots/demo.json'}")
        with self.assertRaises(R.SlotError) as cm:
            R.resolve_slot("demo.with-default", self.root, instance=str(inst))
        self.assertIn("outside its instance root", str(cm.exception))
        inst2 = make_instance(self.tmp / "client-dots",
                              fills="  demo.with-default:\n    value: ../client-other/slots/demo.json")
        with self.assertRaises(R.SlotError):
            R.resolve_slot("demo.with-default", self.root, instance=str(inst2))

    def _practice(self, roots=("engagements/",)):
        """Register the practice's own instance (instance 0 stand-in) declaring client roots."""
        return make_instance(self.root / R.INSTANCES_DIR / "practice", kind="self", mode="pointer",
                             iid="practice", client_roots=list(roots))

    def test_pointer_fill_under_another_registered_instance_is_refused(self):
        self._practice()
        reg = self.root / R.INSTANCES_DIR
        donor = make_instance(reg / "donor", kind="self", mode="pointer")
        (donor / "value.json").write_text(json.dumps({"name": "donor"}))
        taker = make_instance(reg / "taker", kind="self", mode="pointer",
                              fills=f"  demo.with-default:\n    value: {R.INSTANCES_DIR}/donor/value.json",
                              iid="taker")
        with self.assertRaises(R.SlotError) as cm:
            R.resolve_slot("demo.with-default", self.root, instance=str(taker))
        self.assertIn("another instance root", str(cm.exception))

    def test_pointer_fill_in_a_client_root_is_refused(self):
        (self.root / "engagements/x").mkdir(parents=True)
        (self.root / "engagements/x/v.json").write_text("{}")
        inst = make_instance(self.root / R.INSTANCES_DIR / "self-ptr", kind="self", mode="pointer",
                             fills="  demo.with-default:\n    value: engagements/x/v.json",
                             client_roots=["engagements/"])
        with self.assertRaises(R.SlotError) as cm:
            R.resolve_slot("demo.with-default", self.root, instance=str(inst))
        self.assertIn("client root", str(cm.exception))
        # case-insensitive: a differently cased spelling of the client root is the same folder
        # on a case-insensitive filesystem
        inst2 = make_instance(self.root / R.INSTANCES_DIR / "self-case", kind="self", mode="pointer",
                              fills="  demo.with-default:\n    value: Engagements/x/v.json", iid="c2")
        with self.assertRaises(R.SlotError):
            R.resolve_slot("demo.with-default", self.root, instance=str(inst2))
        outside = make_instance(self.root / R.INSTANCES_DIR / "self-out", kind="self", mode="pointer",
                                fills=f"  demo.with-default:\n    value: {self.tmp / 'stray.json'}",
                                iid="out")
        (self.tmp / "stray.json").write_text("{}")
        with self.assertRaises(R.SlotError) as cm:
            R.resolve_slot("demo.with-default", self.root, instance=str(outside))
        self.assertIn("outside the checkout", str(cm.exception))

    def test_empty_client_roots_cannot_open_a_client_folder(self):
        # H2 item 4 / review case 2: the guard read client_roots from the manifest being
        # checked, so `client_roots: []` switched it off. They come from the practice now.
        (self.root / "engagements/acme").mkdir(parents=True)
        (self.root / "engagements/acme/v.json").write_text(json.dumps({"name": "acme"}))
        fill = "  demo.with-default:\n    value: engagements/acme/v.json"
        evil = make_instance(self.root / R.INSTANCES_DIR / "evil", kind="self", mode="pointer",
                             fills=fill, iid="evil", client_roots=[])
        # no practice instance declares any client root: fail closed
        with self.assertRaises(R.SlotError) as cm:
            R.resolve_slot("demo.with-default", self.root, instance=str(evil))
        self.assertIn("declares instance.client_roots", str(cm.exception))
        # the practice declares engagements/: the empty list in `evil` changes nothing
        self._practice()
        with self.assertRaises(R.SlotError) as cm:
            R.resolve_slot("demo.with-default", self.root, instance=str(evil))
        self.assertIn("client root engagements/", str(cm.exception))

    def test_any_folder_holding_an_instance_yaml_is_an_instance_root(self):
        # H2 item 4: an unregistered client root inside the checkout is still an instance root.
        self._practice()
        other = make_instance(self.root / "work/other/inst", iid="other")
        (other / "v.json").write_text(json.dumps({"name": "other"}))
        taker = make_instance(self.root / R.INSTANCES_DIR / "taker", kind="self", mode="pointer",
                              fills="  demo.with-default:\n    value: work/other/inst/v.json", iid="taker")
        with self.assertRaises(R.SlotError) as cm:
            R.resolve_slot("demo.with-default", self.root, instance=str(taker))
        self.assertIn("holds an instance.yaml", str(cm.exception))
        # rooted: a nested instance inside the reading root is another instance's root
        outer = make_instance(self.tmp / "outer", fills="  demo.with-default:\n    value: nested/v.json")
        nested = make_instance(outer / "nested", iid="nested")
        (nested / "v.json").write_text(json.dumps({"name": "nested"}))
        with self.assertRaises(R.SlotError) as cm:
            R.resolve_slot("demo.with-default", self.root, instance=str(outer))
        self.assertIn("holds an instance.yaml", str(cm.exception))

    def test_client_root_may_not_enclose_the_checkout_or_sit_in_a_shipped_folder(self):
        # H2 rule-H review D2: a client root at the repo root (or its parent, or a skill folder)
        # could fill its slots with the practice's own files.
        self._practice(roots=("engagements/",))
        (self.root / "tree").mkdir()
        (self.root / "tree/practice.json").write_text(json.dumps({"name": "practice"}))
        fill = "  demo.with-default:\n    value: tree/practice.json"
        at_root = make_instance(self.root, iid="acme", fills=fill)
        with self.assertRaises(R.InstanceError) as cm:
            R.resolve_slot("demo.with-default", self.root, instance=str(at_root))
        self.assertIn("enclose it", str(cm.exception))
        (self.root / "instance.yaml").unlink()
        parent = make_instance(self.tmp, iid="acme", fills="  demo.with-default:\n    value: repo/tree/practice.json")
        with self.assertRaises(R.InstanceError):
            R.resolve_slot("demo.with-default", self.root, instance=str(parent))
        (self.tmp / "instance.yaml").unlink()
        in_tree = make_instance(self.root / "tree", iid="acme",
                                fills="  demo.with-default:\n    value: practice.json")
        with self.assertRaises(R.InstanceError) as cm:
            R.resolve_slot("demo.with-default", self.root, instance=str(in_tree))
        self.assertIn("must sit in a client root", str(cm.exception))
        # inside the checkout, under a declared client root: allowed
        ok = make_instance(self.root / "engagements/acme/inst", iid="acme",
                           fills="  demo.with-default:\n    value: v.json")
        (ok / "v.json").write_text(json.dumps({"name": "acme"}))
        self.assertEqual(R.resolve_slot("demo.with-default", self.root, instance=str(ok))["values"]["name"],
                         "acme")

    def test_client_roots_must_be_a_list_and_are_normalized(self):
        # H2 rule-H review D3: `client_roots: clients/` iterated character by character, and
        # `./clients/` never matched.
        (self.root / "engagements/acme").mkdir(parents=True)
        (self.root / "engagements/acme/v.json").write_text("{}")
        reg = self.root / R.INSTANCES_DIR / "practice"
        reg.mkdir(parents=True)
        (reg / "instance.yaml").write_text(
            "schema: sheerline-instance/1\ninstance:\n  id: practice\n  kind: self\n  mode: pointer\n"
            "  owner: x\n  client_roots: engagements/\n"
            "slots:\n  demo.with-default:\n    value: engagements/acme/v.json\n")
        with self.assertRaises(R.InstanceError) as cm:
            R.resolve_slot("demo.with-default", self.root, instance=str(reg))
        self.assertIn("must be a list", str(cm.exception))
        (reg / "instance.yaml").write_text((reg / "instance.yaml").read_text().replace(
            "client_roots: engagements/", "client_roots: [./engagements/]"))
        with self.assertRaises(R.SlotError) as cm:
            R.resolve_slot("demo.with-default", self.root, instance=str(reg))
        self.assertIn("client root engagements/", str(cm.exception))

    def test_numeric_instance_id_is_refused(self):
        # H2 rule-H review note 9: `id: 007` is int 7 here and "007" in Node.
        inst = make_instance(self.tmp / "num", iid="007")
        with self.assertRaises(R.InstanceError) as cm:
            R.resolve_slot("demo.with-default", self.root, instance=str(inst))
        self.assertIn("instance.id must be", str(cm.exception))
        quoted = make_instance(self.tmp / "numq", iid='"007"')
        self.assertEqual(R.resolve_slot("demo.with-default", self.root, instance=str(quoted))["source"],
                         "default")

    def test_worktree_refusal_ignores_case(self):
        # H2 rule-H review note 7 (APFS is case-insensitive)
        inst = make_instance(self.tmp / "ws/.CLAUDE/Worktrees/t/acme")
        with self.assertRaises(R.InstanceError) as cm:
            R.resolve_slot("demo.with-default", self.root, instance=str(inst))
        self.assertIn(".claude/worktrees", str(cm.exception))

    def test_resolved_file_root_is_absolute_unless_registered(self):
        # H2 rule-H review D5: a repo-relative root made the file depend on the checkout that
        # wrote it (main workspace vs a worktree).
        a = self._rooted("client-a")
        R.write_resolved(self.root, str(a))
        body = json.loads((a / R.RESOLVED_FILE).read_text())
        self.assertEqual(body["instance_root"], a.resolve().as_posix())
        self._practice()
        inside = make_instance(self.root / "engagements/acme/inst", iid="acme")
        R.write_resolved(self.root, str(inside))
        body = json.loads((inside / R.RESOLVED_FILE).read_text())
        self.assertTrue(Path(body["instance_root"]).is_absolute(), body["instance_root"])
        # a second checkout of the same repo (a worktree) reads the main checkout's client file
        other_checkout = make_root(self.tmp / "other-checkout")
        with _Env(inside):
            R.check_resolved_file(inside, "acme", other_checkout)
        reg = self.root / R.INSTANCES_DIR / "practice"
        R.write_resolved(self.root, str(reg))
        self.assertEqual(json.loads((reg / R.RESOLVED_FILE).read_text())["instance_root"],
                         f"{R.INSTANCES_DIR}/practice")

    def test_write_exits_nonzero_when_a_required_slot_errors(self):
        # H2 rule-H review note 11: --write wrote ERROR slots and exited 0.
        a = self._rooted("client-a")
        env = {k: v for k, v in os.environ.items() if k != R.ENV_VAR}
        r = subprocess.run([sys.executable, str(RESOLVE), "--root", str(self.root), "--instance", str(a),
                            "--write"], capture_output=True, text=True, env=env)
        self.assertEqual(r.returncode, 1, r.stderr)
        self.assertIn("demo.no-default", r.stderr)
        self.assertTrue((a / R.RESOLVED_FILE).is_file())

    def test_relative_instance_paths_resolve_against_the_repo_root(self):
        # H2 item 3: a relative --instance or $SHEERLINE_INSTANCE used to resolve against the
        # current directory, so the same value picked different instances from different cwds.
        self._practice(roots=("insts/",))
        inst = make_instance(self.root / "insts/client-r", iid="client-r",
                             fills="  demo.with-default:\n    value: v.json")
        (inst / "v.json").write_text(json.dumps({"name": "client-r"}))
        cwd = os.getcwd()
        os.chdir(self.tmp)
        try:
            self.assertEqual(R.resolve_slot("demo.with-default", self.root,
                                            instance="insts/client-r")["values"]["name"], "client-r")
            with _Env("insts/client-r"):
                self.assertEqual(R.select_instance(self.root)[0], inst.resolve())
        finally:
            os.chdir(cwd)

    def test_tilde_is_home_and_tilde_name_is_refused(self):
        self.assertEqual(R.instance_path("~/x/y", self.root), (Path.home() / "x/y").resolve())
        self.assertEqual(R.instance_path("~", self.root), Path.home().resolve())
        with self.assertRaises(R.InstanceError):
            R.instance_path("~someone/x", self.root)

    def test_consumer_slot_selects_by_env_and_refuses_a_stale_resolved_file(self):
        a = self._rooted("client-a")
        R.write_resolved(self.root, str(a))
        with _Env(a):
            self.assertEqual(R.consumer_slot("demo.with-default", self.root)["values"]["name"], "client-a")
        # copy client-a's folder to client-s and give it its own id: its resolved-slots.json
        # still names client-a and must be refused, by Python and by Node alike
        s = self.tmp / "client-s"
        shutil.copytree(a, s)
        (s / "instance.yaml").write_text((s / "instance.yaml").read_text().replace("id: demo", "id: client-s"))
        with _Env(s):
            with self.assertRaises(R.InstanceError) as cm:
                R.consumer_slot("demo.with-default", self.root)
        self.assertIn("written for instance", str(cm.exception))
        # same id, different folder: the recorded root differs
        t = self.tmp / "client-t"
        shutil.copytree(a, t)
        with _Env(t):
            with self.assertRaises(R.InstanceError) as cm:
                R.consumer_slot("demo.with-default", self.root)
        self.assertIn("instance root", str(cm.exception))
        # no resolved file at all is fine for Python (it resolves directly)
        (t / R.RESOLVED_FILE).unlink()
        with _Env(t):
            self.assertEqual(R.consumer_slot("demo.with-default", self.root)["values"]["name"], "client-a")

    def test_list_exits_nonzero_when_it_prints_an_error(self):
        # H2 item 8
        r = subprocess.run([sys.executable, str(RESOLVE), "--root", str(self.root), "--blank", "--list"],
                           capture_output=True, text=True)
        self.assertIn("ERROR", r.stdout)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)

    def test_instance_flag_is_resolve_only_and_says_so(self):
        a = self._rooted("client-a")
        env = {k: v for k, v in os.environ.items() if k != R.ENV_VAR}
        r = subprocess.run([sys.executable, str(RESOLVE), "--root", str(self.root), "--instance", str(a),
                            "--list"], capture_output=True, text=True, env=env)
        self.assertIn(f"export {R.ENV_VAR}=", r.stderr)

    def test_stale_fill_fails(self):
        inst = make_instance(self.tmp / "stale", fills="  demo.with-default:\n    value: slots/gone.json")
        with self.assertRaises(R.SlotError) as cm:
            R.resolve_slot("demo.with-default", self.root, instance=str(inst))
        self.assertIn("does not exist", str(cm.exception))

    def test_write_emits_resolved_slots_into_the_instance_root(self):
        inst = self._rooted("client-w")
        out = R.write_resolved(self.root, str(inst))
        self.assertEqual(out.resolve(), (inst / R.RESOLVED_FILE).resolve())
        body = json.loads(out.read_text())
        self.assertEqual(body["slots"]["demo.with-default"]["source"], "instance")
        self.assertTrue(Path(body["slots"]["demo.with-default"]["path"]).is_absolute())
        self.assertIn("error", body["slots"]["demo.no-default"])
        with self.assertRaises(R.InstanceError):
            with _Env(None):
                R.write_resolved(self.root)

    def test_blank_check_flags_a_default_that_is_an_instance_path(self):
        slots = (self.root / "sheerline/os/instance/slots.yaml")
        slots.write_text(MINI_SLOTS.replace("in_tree: [tree/demo-instance.json]",
                                            "in_tree: [defaults/demo.json]"))
        problems = R.check_blank(self.root)
        self.assertTrue(any("is an instance path" in p for p in problems), problems)
        self.assertTrue(any("demo.no-default" in p for p in problems), problems)


class Template(unittest.TestCase):
    def test_every_identifying_field_is_blank(self):
        data = R.load_yaml(TEMPLATE.read_text())
        self.assertEqual(data["schema"], R.SCHEMA)
        for k in ("id", "kind", "mode", "owner"):
            self.assertEqual(data["instance"][k], "", k)
        for sect in ("contract", "mcp"):
            for k, v in data[sect].items():
                self.assertEqual(v, "", f"{sect}.{k}")
        self.assertEqual(data["intake"], "")
        self.assertEqual(data["slots"], {})

    def test_template_is_not_loadable_until_filled(self):
        with tempfile.TemporaryDirectory() as t:
            shutil.copy(TEMPLATE, Path(t) / "instance.yaml")
            with self.assertRaises(R.InstanceError):
                R.load_instance(Path(t), ROOT)

    @unittest.skipUnless(HAVE_YAML and HAVE_JSONSCHEMA, "PyYAML or jsonschema not installed")
    def test_template_validates_against_the_schema(self):
        import jsonschema
        import yaml
        jsonschema.validate(yaml.safe_load(TEMPLATE.read_text()), json.loads(SCHEMA.read_text()))


NODE = shutil.which("node")
NODE_HELPER = ROOT / "sheerline/os/instance/resolved-slot.mjs"


@unittest.skipUnless(NODE, "node is not installed")
class NodeParity(unittest.TestCase):
    """The Node reader picks the same instance and the same value as the Python resolver."""

    def _node(self, slot_id, env_value):
        env = {k: v for k, v in os.environ.items() if k != R.ENV_VAR}
        if env_value is not None:
            env[R.ENV_VAR] = str(env_value)
        r = subprocess.run([NODE, str(NODE_HELPER), slot_id], capture_output=True, text=True, env=env)
        return r.returncode, (json.loads(r.stdout) if r.returncode == 0 else r.stderr)

    def _node_eval(self, expr, repo, env_value, cwd, home=None):
        env = {k: v for k, v in os.environ.items() if k != R.ENV_VAR}
        if env_value is not None:
            env[R.ENV_VAR] = str(env_value)
        if home is not None:
            env["HOME"] = str(home)
        code = (f"import({json.dumps(NODE_HELPER.as_uri())}).then(m => "
                f"console.log(JSON.stringify({expr.replace('REPO', json.dumps(str(repo)))})))"
                ".catch(e => { console.error(e.message); process.exit(2); })")
        r = subprocess.run([NODE, "-e", code], capture_output=True, text=True, env=env, cwd=str(cwd))
        return r.returncode, (json.loads(r.stdout) if r.returncode == 0 else r.stderr)

    def test_relative_env_resolves_against_the_repo_root_and_tilde_is_home(self):
        # H2 item 3: Node used path.resolve(env), i.e. the cwd, and left `~` unexpanded.
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            root = make_root(t / "repo")
            make_instance(root / R.INSTANCES_DIR / "practice", kind="self", mode="pointer",
                          iid="practice", client_roots=["insts/"])
            inst = make_instance(root / "insts/client-r", iid="client-r",
                                 fills="  demo.with-default:\n    value: v.json")
            (inst / "v.json").write_text(json.dumps({"name": "client-r"}))
            R.write_resolved(root, str(inst))
            rc, rec = self._node_eval("m.resolvedSlot('demo.with-default', {repoRoot: REPO})", root,
                                      "insts/client-r", cwd=t)
            self.assertEqual(rc, 0, rec)
            self.assertEqual(Path(rec["path"]).resolve(), (inst / "v.json").resolve())
            self.assertEqual(rec["instance"], "client-r")
            home = t / "home"
            (home / "insts").mkdir(parents=True)
            rc, picked = self._node_eval("m.selectInstance({repoRoot: REPO})", root, "~/insts", cwd=t,
                                         home=home)
            self.assertEqual(rc, 0, picked)
            self.assertEqual(Path(picked).resolve(), (home / "insts").resolve())
            rc, err = self._node_eval("m.selectInstance({repoRoot: REPO})", root, "~bob/x", cwd=t)
            self.assertEqual(rc, 2)
            self.assertIn("~name", err)

    def test_a_resolved_file_written_for_another_instance_errors(self):
        # H2 item 3: copying an instance folder (or a stray resolved-slots.json) used to hand
        # the copy the other instance's values.
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            root = make_root(t / "repo")
            a = make_instance(t / "client-a", iid="client-a",
                              fills="  demo.with-default:\n    value: v.json")
            (a / "v.json").write_text(json.dumps({"name": "a"}))
            R.write_resolved(root, str(a))
            s = t / "client-s"
            shutil.copytree(a, s)
            (s / "instance.yaml").write_text((s / "instance.yaml").read_text().replace("client-a", "client-s"))
            rc, err = self._node_eval("m.resolvedSlot('demo.with-default', {repoRoot: REPO})", root, s, cwd=t)
            self.assertEqual(rc, 2, err)
            self.assertIn("written for instance", err)
            same_id = t / "client-a-copy"
            shutil.copytree(a, same_id)
            rc, err = self._node_eval("m.resolvedSlot('demo.with-default', {repoRoot: REPO})", root,
                                      same_id, cwd=t)
            self.assertEqual(rc, 2, err)
            self.assertIn("instance root", err)

    def test_node_applies_the_placement_rules(self):
        # H2 rule-H review D6: Node read any root's resolved-slots.json, so a client folder
        # copied into a .claude/worktrees/ checkout (with its file) was read there while Python
        # refused it. Also notes 7 and 9 (case, numeric ids), and D2 inside the checkout.
        resolved = "m.resolvedSlot('demo.with-default', {repoRoot: REPO})"
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            root = make_root(t / "repo")
            a = make_instance(t / "client-a", iid="client-a", fills="  demo.with-default:\n    value: v.json")
            (a / "v.json").write_text(json.dumps({"name": "a"}))
            R.write_resolved(root, str(a))
            for wt in ("ws/.claude/worktrees/x/acme1", "ws2/.Claude/WORKTREES/x/acme2"):
                copy = t / wt
                shutil.copytree(a, copy)
                body = json.loads((copy / R.RESOLVED_FILE).read_text())
                body["instance_root"] = copy.resolve().as_posix()  # even a "fixed-up" copy
                (copy / R.RESOLVED_FILE).write_text(json.dumps(body))
                rc, err = self._node_eval(resolved, root, copy, cwd=t)
                self.assertEqual(rc, 2, (wt, err))
                self.assertIn(".claude/worktrees", err)
            selfish = make_instance(t / "selfish", kind="self", mode="rooted", iid="selfish")
            (selfish / R.RESOLVED_FILE).write_text(json.dumps({
                "schema": R.RESOLVED_SCHEMA, "instance": "selfish",
                "instance_root": selfish.resolve().as_posix(), "slots": {}}))
            rc, err = self._node_eval(resolved, root, selfish, cwd=t)
            self.assertEqual(rc, 2, err)
            self.assertIn("allowed only for an instance registered", err)
            num = make_instance(t / "num", iid="007")
            (num / R.RESOLVED_FILE).write_text(json.dumps({
                "schema": R.RESOLVED_SCHEMA, "instance": "007",
                "instance_root": num.resolve().as_posix(), "slots": {}}))
            rc, err = self._node_eval(resolved, root, num, cwd=t)
            self.assertEqual(rc, 2, err)
            self.assertIn("instance.id must be", err)
            make_instance(root / R.INSTANCES_DIR / "practice", kind="self", mode="pointer",
                          iid="practice", client_roots=["engagements/"])
            stray = make_instance(root / "tree/acme", iid="acme")
            (stray / R.RESOLVED_FILE).write_text(json.dumps({
                "schema": R.RESOLVED_SCHEMA, "instance": "acme",
                "instance_root": stray.resolve().as_posix(), "slots": {}}))
            rc, err = self._node_eval(resolved, root, stray, cwd=t)
            self.assertEqual(rc, 2, err)
            self.assertIn("must sit in a client root", err)
            ok = make_instance(root / "engagements/acme/inst", iid="acme",
                               fills="  demo.with-default:\n    value: v.json")
            (ok / "v.json").write_text(json.dumps({"name": "acme"}))
            R.write_resolved(root, str(ok))
            rc, rec = self._node_eval(resolved, root, ok, cwd=t)
            self.assertEqual(rc, 0, rec)
            self.assertEqual(Path(rec["path"]).resolve(), (ok / "v.json").resolve())

    def test_blank_is_null(self):
        self.assertEqual(self._node("ui-studio.default-brand", R.BLANK_VALUE), (0, None))

    @unittest.skipUnless(FIXTURE.is_file(), "instance 0 is not in this checkout (an export)")
    def test_default_pointer_matches_python(self):
        rc, rec = self._node("ui-studio.default-brand", None)
        self.assertEqual(rc, 0, rec)
        with _Env(None):
            py = R.resolve_slot("ui-studio.default-brand", ROOT)
        self.assertEqual(rec["source"], py["source"])
        self.assertEqual(Path(rec["path"]).resolve(), (ROOT / py["path"]).resolve())

    def test_rooted_instance_matches_python_and_missing_output_fails(self):
        with tempfile.TemporaryDirectory() as t:
            root = make_root(Path(t) / "repo")
            inst = make_instance(Path(t) / "client-n", fills="  demo.with-default:\n    value: slots/demo.json")
            (inst / "slots").mkdir()
            (inst / "slots/demo.json").write_text(json.dumps({"name": "n"}))
            rc, err = self._node("demo.with-default", inst)
            self.assertEqual(rc, 2)
            self.assertIn("resolve.py --write", err)
            R.write_resolved(root, str(inst))
            rc, rec = self._node("demo.with-default", inst)
            self.assertEqual(rc, 0, rec)
            self.assertEqual(Path(rec["path"]).resolve(), (inst / "slots/demo.json").resolve())
            rc, err = self._node("demo.no-default", inst)
            self.assertEqual(rc, 2)
            self.assertIn("demo.no-default", err)


@unittest.skipUnless(OVERLAY_CONTRACT.is_file(), "the export overlay is not in this checkout")
class DefaultParity(unittest.TestCase):
    def test_adoption_default_matches_the_overlay_copy(self):
        # Same text as the overlay's unratified copy, with its spaced em dashes written as
        # colons (the slot default keeps to the house em-dash limit). Any other edit to
        # either copy alone fails here.
        default = ROOT / R.load_slots(ROOT)["care.adoption-contract"]["default"]
        overlay = OVERLAY_CONTRACT.read_text(encoding="utf-8").replace(" — ", ": ")
        self.assertEqual(default.read_text(encoding="utf-8"), overlay,
                         "the slot default and the export overlay's unratified copy drifted")


if __name__ == "__main__":
    unittest.main()
