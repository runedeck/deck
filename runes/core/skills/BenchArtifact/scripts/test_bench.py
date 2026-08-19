"""Test the public benchmark wrapper paths."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import bench


class BenchWrapperTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.config = {
            "_root": self.root,
            "iteration": 4,
            "manifest": "manifest.json",
            "routes": "routes.json",
            "repeats": 3,
            "seed": 7,
            "comparison": "skill_vs_baseline",
            "approve": 12,
            "artifact_name": "Example",
            "grader": "grade.py",
            "checker": "lint.py",
            "judges": [],
            "quick": {"routes": ["one"], "cases": [1], "iteration": 9},
        }

    def test_report_uses_the_frozen_iteration_manifest(self):
        with patch.object(bench, "run") as run:
            bench.report(self.config)

        aggregate = run.call_args_list[0].args[0]
        manifest_index = aggregate.index("--manifest") + 1
        self.assertEqual(
            aggregate[manifest_index],
            self.root / "iteration-4" / "manifest.json",
        )

    def test_quick_run_forces_one_repeat(self):
        scratch = self.root / "iteration-9"

        def fake_run(argv, **_kwargs):
            if "scripts.aggregate_benchmark" in argv:
                scratch.mkdir(exist_ok=True)
                (scratch / "benchmark.md").write_text("summary\n", encoding="utf-8")

        with patch.object(bench, "run", side_effect=fake_run) as run, patch.object(
            bench, "grade"
        ):
            bench.quick(self.config)

        matrix = run.call_args_list[0].args[0]
        repeats_index = matrix.index("--repeats") + 1
        approve_index = matrix.index("--approve") + 1
        self.assertEqual(matrix[repeats_index], 1)
        self.assertEqual(matrix[approve_index], 2)


if __name__ == "__main__":
    unittest.main()
