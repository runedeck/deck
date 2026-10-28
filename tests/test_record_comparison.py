"""scripts/record-comparison turns a BenchArtifact workspace into one
comparison record per rune: a grading file per run, the later iteration
wins for a model, a run without a grading file is excluded, and the record
carries no absolute path (provisioning-joins-the-deck, A Provisioning Rune
Shows That It Helps)."""
import hashlib
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "record-comparison"
PASS = {"text": "Names the fix.", "passed": True, "evidence": "Missing: none."}
FAIL = {"text": "Names the fix.", "passed": False, "evidence": "Missing: the fix."}
WORDS = {"text": "The answer has 3 to 250 words.", "passed": True, "evidence": "40 words."}


def grading(workspace, iteration, case, arm, model, run, *expectations):
    path = workspace / f"iteration-{iteration}" / case / f"{arm}@{model}" / f"run-{run}" / "grading.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"grader_version": 1, "expectations": list(expectations)}))
    return path


def benchmark(workspace, iteration, models, digest):
    path = workspace / f"iteration-{iteration}" / "benchmark.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "metadata": {"artifact_name": "Alpha", "models": models, "arms": ["with_artifact", "baseline"]},
        "arms": {"with_artifact": {"artifact_name": "Alpha", "artifact_sha256": digest}, "baseline": {}},
        "runs": [],
    }
    path.write_text(json.dumps(data))
    return path


def workspace_fixture(root):
    """Two iterations. Iteration 1 covers model-a, iteration 2 covers model-a
    again and model-b, so iteration 2 wins for model-a."""
    workspace = root / "bench" / "Alpha"
    benchmark(workspace, 1, ["model-a"], "1" * 64)
    grading(workspace, 1, "eval-1-first", "with_artifact", "model-a", 1, PASS, WORDS)
    grading(workspace, 1, "eval-1-first", "baseline", "model-a", 1, FAIL, WORDS)
    grading(workspace, 1, "eval-2-second", "with_artifact", "model-a", 1, PASS, WORDS)
    grading(workspace, 1, "eval-2-second", "baseline", "model-a", 1, PASS, WORDS)
    benchmark(workspace, 2, ["model-a", "model-b"], "2" * 64)
    grading(workspace, 2, "eval-1-first", "with_artifact", "model-a", 1, PASS, WORDS)
    grading(workspace, 2, "eval-1-first", "baseline", "model-a", 1, PASS, WORDS)
    grading(workspace, 2, "eval-2-second", "with_artifact", "model-a", 1, PASS, WORDS)
    grading(workspace, 2, "eval-2-second", "with_artifact", "model-a", 2, PASS, FAIL)
    (workspace / "iteration-2" / "eval-2-second" / "baseline@model-a" / "run-1").mkdir(parents=True)
    grading(workspace, 2, "eval-1-first", "with_artifact", "model-b", 1, PASS, WORDS)
    grading(workspace, 2, "eval-1-first", "baseline", "model-b", 1, FAIL, WORDS)
    grading(workspace, 2, "eval-2-second", "with_artifact", "model-b", 1, PASS, WORDS)
    grading(workspace, 2, "eval-2-second", "baseline", "model-b", 1, PASS, WORDS)
    return workspace


class RecordComparison(unittest.TestCase):
    def setUp(self):
        self.scratch = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: subprocess.run(["rm", "-rf", str(self.scratch)], check=False))
        self.workspace = workspace_fixture(self.scratch)
        self.repo = self.scratch / "repo"
        (self.repo / "docs" / "changes" / "test-change").mkdir(parents=True)
        self.env = {**os.environ, "ROOT_BENCHMARK": str(self.scratch)}

    def run_script(self, *extra):
        return subprocess.run(
            ["python3", str(SCRIPT), str(self.workspace), "--change", "test-change", "--root", str(self.repo), *extra],
            capture_output=True, text=True, check=False, env=self.env,
        )

    def record(self, name="Alpha"):
        return json.loads((self.repo / "docs" / "changes" / "test-change" / "comparisons" / f"{name}.json").read_text())

    def test_record_shape_later_iteration_and_excluded_run(self):
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stdout, "docs/changes/test-change/comparisons/Alpha.json\n")
        record = self.record()
        self.assertEqual(record["rune"], "Alpha")
        self.assertEqual(record["models"], ["model-a", "model-b"])
        self.assertEqual(
            record["cases"],
            [
                {
                    "id": "1",
                    "name": "first",
                    "results": {
                        "model-a": {"with": "pass", "without": "pass"},
                        "model-b": {"with": "pass", "without": "fail"},
                    },
                },
                {
                    "id": "2",
                    "name": "second",
                    "results": {
                        "model-a": {"with": "fail", "without": "excluded"},
                        "model-b": {"with": "pass", "without": "pass"},
                    },
                },
            ],
        )
        self.assertEqual(
            record["iterations"],
            [
                {"number": 1, "models": ["model-a"], "artifact_sha256": "1" * 64},
                {"number": 2, "models": ["model-a", "model-b"], "artifact_sha256": "2" * 64},
            ],
        )

    def test_sources_are_relative_to_the_benchmark_root_with_digests(self):
        self.run_script()
        sources = self.record()["sources"]
        paths = [source["path"] for source in sources]
        self.assertEqual(paths, sorted(paths))
        self.assertIn("bench/Alpha/iteration-1/benchmark.json", paths)
        self.assertIn("bench/Alpha/iteration-2/eval-1-first/baseline@model-b/run-1/grading.json", paths)
        self.assertNotIn("bench/Alpha/iteration-2/eval-2-second/baseline@model-a/run-1/grading.json", paths)
        for source in sources:
            self.assertFalse(source["path"].startswith("/"), source["path"])
            digest = hashlib.sha256((self.scratch / source["path"]).read_bytes()).hexdigest()
            self.assertEqual(source["sha256"], digest)
        text = json.dumps(self.record())
        self.assertNotIn(str(self.scratch), text)

    def test_grading_file_without_an_expectation_is_excluded(self):
        """A baseline run with no graded expectation is not a fail, so it
        cannot count as a changed answer."""
        path = self.workspace / "iteration-2" / "eval-1-first" / "baseline@model-b" / "run-1" / "grading.json"
        bodies = {"empty": {"expectations": []}, "null": {"expectations": None}, "absent": {"grader_version": 1}}
        for label, body in bodies.items():
            with self.subTest(label):
                path.write_text(json.dumps(body))
                result = self.run_script()
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual(self.record()["cases"][0]["results"]["model-b"], {"with": "pass", "without": "excluded"})

    def test_output_is_deterministic(self):
        self.run_script()
        first = (self.repo / "docs" / "changes" / "test-change" / "comparisons" / "Alpha.json").read_bytes()
        self.run_script()
        second = (self.repo / "docs" / "changes" / "test-change" / "comparisons" / "Alpha.json").read_bytes()
        self.assertEqual(first, second)

    def test_rune_flag_names_the_record(self):
        result = self.run_script("--rune", "Beta")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.record("Beta")["rune"], "Beta")

    def test_workspace_outside_the_root_is_relative_to_its_parent(self):
        self.env["ROOT_BENCHMARK"] = str(self.scratch / "elsewhere")
        self.run_script()
        paths = [source["path"] for source in self.record()["sources"]]
        self.assertIn("Alpha/iteration-1/benchmark.json", paths)

    def test_missing_change_fails(self):
        result = subprocess.run(
            ["python3", str(SCRIPT), str(self.workspace), "--change", "absent", "--root", str(self.repo)],
            capture_output=True, text=True, check=False, env=self.env,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("no change at", result.stderr)


if __name__ == "__main__":
    unittest.main()
