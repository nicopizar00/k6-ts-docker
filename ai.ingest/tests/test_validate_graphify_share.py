#!/usr/bin/env python3
"""Regression suite for ai.ingest/validate_graphify_share.py."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

VALIDATE_PATH = Path(__file__).resolve().parent.parent / "validate_graphify_share.py"
_spec = importlib.util.spec_from_file_location("validate_graphify_share", VALIDATE_PATH)
guard = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(guard)


class GraphifyPathViolations(unittest.TestCase):
    def test_allows_only_root_shared_artifacts(self):
        paths = [
            "graphify-out/graph.json",
            "graphify-out/GRAPH_REPORT.md",
        ]
        self.assertEqual(guard.graphify_path_violations(paths), [])

    def test_rejects_extra_root_output(self):
        paths = ["graphify-out/graph.html"]
        self.assertEqual(guard.graphify_path_violations(paths), ["graphify-out/graph.html"])

    def test_rejects_nested_output_folder(self):
        paths = ["docs/graphify-out/graph.json"]
        self.assertEqual(
            guard.graphify_path_violations(paths),
            ["docs/graphify-out/graph.json"],
        )

    def test_rejects_renamed_output_folder(self):
        paths = ["graphify-out-copy/graph.json", "tmp/graphify-out_backup/graph.json"]
        self.assertEqual(
            guard.graphify_path_violations(paths),
            ["graphify-out-copy/graph.json", "tmp/graphify-out_backup/graph.json"],
        )


class ArtifactContentChecks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_graph_json_rejects_invalid_json(self):
        graph = self.root / "graph.json"
        graph.write_text("{", encoding="utf-8")
        errors = guard.check_graph_json(graph)
        self.assertEqual(len(errors), 1)
        self.assertIn("invalid JSON", errors[0])

    def test_graph_json_rejects_absolute_node_ids(self):
        graph = self.root / "graph.json"
        graph.write_text('{"nodes":[{"id":"/Users/me/repo/file.py"}]}', encoding="utf-8")
        errors = guard.check_graph_json(graph)
        self.assertEqual(len(errors), 1)
        self.assertIn("absolute node IDs", errors[0])

    def test_text_rejects_local_paths_and_raw_cost_keys(self):
        text = "/Users/me/repo\ninput_tokens\n"
        errors = guard.check_text_patterns(self.root / "report.md", text)
        self.assertEqual(len(errors), 2)
        self.assertTrue(any("absolute path" in err for err in errors))
        self.assertTrue(any("raw cost/token key" in err for err in errors))


if __name__ == "__main__":
    unittest.main()
