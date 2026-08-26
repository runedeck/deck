import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPT = Path(__file__).with_name("bench.py")
SPEC = importlib.util.spec_from_file_location("bench", SCRIPT)
BENCH = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BENCH)


class BenchTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.manifest = self.root / "manifest.json"
        self.routes = self.root / "routes.json"
        self.manifest.write_text(json.dumps({
            "comparisons": [{
                "id": "skill",
                "primary": "with_skill",
                "baseline": "baseline",
            }],
            "evals": [{"id": 1}, {"id": 2}, {"id": 3}],
        }), encoding="utf-8")
        self.routes.write_text(json.dumps({
            "routes": {"first": {}, "second": {}},
        }), encoding="utf-8")
        self.config = {
            "_root": self.root,
            "manifest": self.manifest.name,
            "routes": self.routes.name,
            "comparison": "skill",
            "repeats": 2,
            "iteration": 1,
            "judge_script": "judge.py",
            "seed": 7,
            "judges": [{"route": "judge", "models": ["model"]}],
        }

    def test_judge_passes_cross_harness_consent(self):
        self.config["judges"][0]["approve"] = 23
        with mock.patch.object(BENCH, "run") as run:
            BENCH.judge(self.config)

        argv = run.call_args.args[0]
        self.assertLess(argv.index("--cross-harness"), argv.index("--iteration"))
        self.assertEqual(argv[argv.index("--approve") + 1], 23)

    def test_judge_does_not_reuse_matrix_approval(self):
        self.config["approve"] = 99
        with mock.patch.object(BENCH, "run") as run:
            BENCH.judge(self.config)

        self.assertNotIn("--approve", run.call_args.args[0])

    def test_repeat_summary_reports_configured_repeats(self):
        self.assertEqual(BENCH.repeat_summary(self.config), "2 repeats")
        self.assertEqual(BENCH.repeat_summary({}), "1 repeat")

    def test_quick_approval_matches_runner_selection(self):
        self.assertEqual(BENCH.quick_approval(self.config, [], []), 28)
        self.assertEqual(
            BENCH.quick_approval(
                self.config,
                ["first", "first"],
                ["1", "1"],
            ),
            6,
        )

    def test_quick_approval_rejects_an_unknown_filter(self):
        with self.assertRaisesRegex(ValueError, "filter values not found: missing"):
            BENCH.quick_approval(self.config, ["missing"], ["1"])


if __name__ == "__main__":
    unittest.main()
