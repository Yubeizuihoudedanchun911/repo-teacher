"""Behavior tests: bounded inventory and source-backed artifact references."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "skills/teach-repo/scripts"
FIXTURES = ROOT / "tests/fixtures"
REPO = FIXTURES / "repo"

class ToolBehaviorTests(unittest.TestCase):
    def run_tool(self, name, args, stdin=None):
        script = TOOLS / name
        self.assertTrue(script.is_file(), f"Missing implementation: {script.name}")
        result = subprocess.run([sys.executable, "-B", str(script), *map(str, args)],
                                input=stdin, text=True, capture_output=True, timeout=15)
        return result, json.loads(result.stdout)

    def evidence(self):
        return {
            "schema_version": 1,
            "repository": {"revision": None},
            "claims": [{
                "id": "transform", "statement": "The function increments the input value.",
                "level": "source",
                "sources": [{"path": "src/main.py", "line_start": 1, "line_end": 2,
                             "sha256": hashlib.sha256((REPO / "src/main.py").read_bytes()).hexdigest()}]
            }]
        }

    def check(self, evidence, lesson="lesson.md"):
        return self.run_tool("check_lesson.py",
                             ["--repo", REPO, "--lesson", FIXTURES / lesson, "--evidence", "-"],
                             json.dumps(evidence))

    def test_inventory_excludes_vendor_and_dotenv_files(self):
        result, data = self.run_tool("inspect_repo.py", ["--repo", REPO, "--max-files", 100])
        self.assertEqual(result.returncode, 0)
        paths = [f["path"] for f in data["files"]]
        self.assertEqual(set(paths), {"README.md", "package.json", "src/main.py", "src/worker.py"})
        self.assertTrue(data["inventory_complete"])
        self.assertFalse(data["semantic_coverage_verified"])

    def test_file_budget_marks_inventory_incomplete(self):
        result, data = self.run_tool("inspect_repo.py", ["--repo", REPO, "--max-files", 2])
        self.assertEqual(result.returncode, 0)
        self.assertFalse(data["inventory_complete"])
        self.assertLessEqual(len(data["files"]), 2)
        self.assertIn("file_limit", data["stop_reasons"])

    def test_invalid_scan_limits_do_not_silently_scan_everything(self):
        result, data = self.run_tool("inspect_repo.py", ["--repo", REPO, "--max-files", 0])
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(data["ok"])

    def test_current_reference_and_real_line_range_pass(self):
        result, data = self.check(self.evidence())
        self.assertEqual(result.returncode, 0)
        self.assertTrue(data["ok"])
        self.assertTrue(data["static_validation_only"])

    def test_changed_source_is_detected_by_hash(self):
        evidence = self.evidence()
        evidence["claims"][0]["sources"][0]["sha256"] = "0" * 64
        result, data = self.check(evidence)
        self.assertEqual(result.returncode, 1)
        self.assertIn("source_changed", [x["code"] for x in data["errors"]])

    def test_nonexistent_line_is_rejected(self):
        evidence = self.evidence()
        evidence["claims"][0]["sources"][0]["line_end"] = 99
        result, data = self.check(evidence)
        self.assertEqual(result.returncode, 1)
        self.assertIn("invalid_line_range", [x["code"] for x in data["errors"]])

    def test_source_reference_cannot_escape_repository(self):
        evidence = self.evidence()
        evidence["claims"][0]["sources"][0]["path"] = "../lesson.md"
        result, data = self.check(evidence)
        self.assertEqual(result.returncode, 1)
        self.assertIn("source_outside_repository", [x["code"] for x in data["errors"]])

    def test_broken_lesson_link_is_reported(self):
        result, data = self.check(self.evidence(), "broken-lesson.md")
        self.assertEqual(result.returncode, 1)
        self.assertIn("missing_local_link", [x["code"] for x in data["errors"]])

    def test_codex_style_source_line_link_is_resolved(self):
        result, data = self.check(self.evidence(), "lesson-with-line.md")
        self.assertEqual(result.returncode, 0)
        self.assertTrue(data["ok"])

    def test_basename_line_links_are_not_mistaken_for_url_schemes(self):
        result, data = self.check(self.evidence(), "broken-basename-lines.md")
        self.assertEqual(result.returncode, 1)
        codes = [x["code"] for x in data["errors"]]
        self.assertIn("missing_local_link", codes)
        self.assertIn("invalid_link_line", codes)

    def test_runtime_level_requires_run_metadata(self):
        evidence = self.evidence()
        evidence["claims"][0]["level"] = "runtime"
        result, data = self.check(evidence)
        self.assertEqual(result.returncode, 1)
        self.assertIn("missing_run_metadata", [x["code"] for x in data["errors"]])

if __name__ == "__main__":
    unittest.main()
