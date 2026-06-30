#!/usr/bin/env python3
"""Regression suite for ai.ingest/compare.py (stdlib unittest only).

Run: python3 -m unittest discover -s ai.ingest/tests

`compare.py` lives in a dotted dir (`ai.ingest/`) that is not an importable
package, so it is loaded by absolute path.
"""
import contextlib
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path

CMP_PATH = Path(__file__).resolve().parent.parent / "compare.py"
_spec = importlib.util.spec_from_file_location("compare", CMP_PATH)
cmp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cmp)


class DiffAxis(unittest.TestCase):
    def test_four_core_verdicts(self):
        self.assertEqual(dict(cmp.diff_axis({"a": "sha256:1"}, {"a": "sha256:2"}))["a"], "changed")
        self.assertEqual(dict(cmp.diff_axis({"a": "sha256:1"}, {"a": "sha256:1"}))["a"], "unchanged")
        self.assertEqual(dict(cmp.diff_axis({}, {"a": "sha256:1"}))["a"], "added")
        self.assertEqual(dict(cmp.diff_axis({"a": "sha256:1"}, {}))["a"], "removed")

    def test_null_baseline_is_not_drift(self):
        self.assertEqual(dict(cmp.diff_axis({"a": None}, {"a": "sha256:1"}))["a"], "baseline-not-recorded")

    def test_intentional_absent_suppressed(self):
        rows = dict(cmp.diff_axis({"x.md": "sha256:1"}, {}, suppress_absent={"x.md"}))
        self.assertEqual(rows["x.md"], "intentional-absent")

    def test_skip_names_dropped_both_sides(self):
        # marker recorded in baseline + present live → not reported at all
        rows = dict(cmp.diff_axis({"m": None, "a": None}, {"m": "sha256:1", "a": "sha256:1"},
                                  skip_names={"m"}))
        self.assertNotIn("m", rows)
        self.assertIn("a", rows)


class LiveAssets(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "SKILL.md").write_text("hi", encoding="utf-8")
        (self.root / "references").mkdir()
        (self.root / "references" / "q.md").write_text("q", encoding="utf-8")
        (self.root / ".graphify_version").write_text("0.8.41", encoding="utf-8")
        (self.root / "graphify-out").mkdir()
        (self.root / "graphify-out" / "graph.json").write_text("{}", encoding="utf-8")
        self.globs = ["SKILL.md", "references/**/*.md", ".graphify_version", "graphify-out/*.json"]

    def tearDown(self):
        self.tmp.cleanup()

    def test_excludes_outputs_and_marker(self):
        live = cmp.live_assets(self.root, self.globs,
                               self.root / "graphify-out", skip_names={".graphify_version"})
        self.assertIn("SKILL.md", live)
        self.assertIn("references/q.md", live)
        self.assertNotIn(".graphify_version", live)           # marker skipped
        self.assertFalse(any("graphify-out" in k for k in live))  # outputs excluded

    def test_hashes_are_sha256_prefixed(self):
        live = cmp.live_assets(self.root, ["SKILL.md"], self.root / "graphify-out")
        self.assertTrue(live["SKILL.md"].startswith("sha256:"))


class ProbeAndVersion(unittest.TestCase):
    def test_absent_binary(self):
        self.assertIsNone(cmp.probe_version(["__no_such_bin__", "--version"]))

    def test_nonzero_returncode(self):
        self.assertIsNone(cmp.probe_version(["sh", "-c", "echo 9.9.9 >&2; exit 1"]))

    def test_parses_version_on_success(self):
        self.assertEqual(cmp.probe_version(["sh", "-c", "echo tool 1.2.3"]), "1.2.3")

    def test_axis_version_states(self):
        desc_ok = {"verify": {"version_probe": ["sh", "-c", "echo 0.8.41"]}}
        desc_bad = {"verify": {"version_probe": ["sh", "-c", "echo 0.9.0"]}}
        desc_absent = {"verify": {"version_probe": ["__no_such_bin__"]}}
        skill = {"adopted_version": {"package_version": "0.8.41"}}
        self.assertEqual(cmp.axis_version(skill, desc_ok)[0], "match")
        self.assertEqual(cmp.axis_version(skill, desc_bad)[0], "version-drift")
        self.assertEqual(cmp.axis_version(skill, desc_absent)[0], "not-installed")


class EndToEnd(unittest.TestCase):
    def test_main_against_seed_is_readonly_and_complete(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = cmp.main(["graphify"])
        out = buf.getvalue()
        self.assertEqual(rc, 0)
        self.assertIn("[1] version drift", out)
        self.assertIn("[2] upstream-asset drift", out)
        self.assertIn("[3] adaptation drift", out)
        self.assertIn("summary:", out)
        # seed has null baselines → incomplete, never false 'drift detected'
        self.assertIn("baseline-not-recorded", out)
        self.assertNotIn("drift detected", out)


if __name__ == "__main__":
    unittest.main()
