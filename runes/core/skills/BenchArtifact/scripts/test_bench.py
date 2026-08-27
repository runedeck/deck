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

    def test_matrix_leaves_approval_with_the_runner(self):
        with mock.patch.object(BENCH, "run") as run:
            BENCH.matrix(self.config)

        self.assertNotIn("--approve", run.call_args.args[0])

    def test_matrix_passes_an_explicit_approval(self):
        self.config["approve"] = 19
        with mock.patch.object(BENCH, "run") as run:
            BENCH.matrix(self.config)

        argv = run.call_args.args[0]
        self.assertEqual(argv[argv.index("--approve") + 1], 19)

    def test_quick_matrix_keeps_filters_without_approval(self):
        argv = BENCH.quick_matrix_argv(self.config, ["first"], ["1"])

        self.assertNotIn("--approve", argv)
        self.assertEqual(argv[argv.index("--route") + 1], "first")
        self.assertEqual(argv[argv.index("--case") + 1], "1")

    def test_quick_matrix_passes_an_explicit_approval(self):
        argv = BENCH.quick_matrix_argv(
            self.config,
            ["first"],
            ["1"],
            6,
        )

        self.assertEqual(argv[argv.index("--approve") + 1], 6)

    def test_quick_requires_route_and_case_filters(self):
        for quick in ({}, {"routes": ["first"]}, {"cases": [1]}):
            self.config["quick"] = quick
            with (
                self.subTest(quick=quick),
                self.assertRaisesRegex(ValueError, "must each select"),
            ):
                BENCH.quick(self.config)

    def test_quick_rejects_non_integer_iteration_before_delete(self):
        scratch = self.root / "iteration-invalid"
        scratch.mkdir()
        self.config["quick"] = {
            "routes": ["first"],
            "cases": [1],
            "iteration": "invalid",
        }

        with (
            mock.patch.object(BENCH.shutil, "rmtree") as remove,
            self.assertRaisesRegex(TypeError, "must be an integer"),
        ):
            BENCH.quick(self.config)

        remove.assert_not_called()

    def test_snapshot_records_a_manifest_relative_artifact_path(self):
        artifact = self.root / "artifact"
        artifact.mkdir()
        (artifact / "SKILL.md").write_text("example\n", encoding="utf-8")
        manifest = self.root / "manifests" / "manifest.json"
        manifest.parent.mkdir()
        (manifest.parent / "snapshots").mkdir()
        manifest.write_text(
            json.dumps({"arms": {"with_skill": {}}}),
            encoding="utf-8",
        )
        self.config.update({
            "artifact_source": "artifact",
            "snapshot": "manifests/snapshots/artifact",
            "manifest": "manifests/manifest.json",
            "treatment_arm": "with_skill",
        })

        BENCH.snapshot(self.config)

        written = json.loads(manifest.read_text(encoding="utf-8"))
        self.assertEqual(
            written["arms"]["with_skill"]["artifact_path"],
            "snapshots/artifact",
        )

    def test_snapshot_rejects_manifest_directory_before_delete(self):
        source = self.root / "source"
        source.mkdir()
        manifest = self.root / "definition" / "manifest.json"
        manifest.parent.mkdir()
        config = {
            "_root": self.root,
            "artifact_source": "source",
            "manifest": "definition/manifest.json",
            "snapshot": "definition",
        }

        with (
            mock.patch.object(BENCH.shutil, "rmtree") as remove,
            self.assertRaisesRegex(ValueError, "below the manifest directory"),
        ):
            BENCH.snapshot(config)

        remove.assert_not_called()

    def test_snapshot_rejects_missing_source_before_delete(self):
        target = self.root / "definition" / "snapshots" / "artifact"
        target.mkdir(parents=True)
        config = {
            "_root": self.root,
            "artifact_source": "missing",
            "manifest": "definition/manifest.json",
            "snapshot": "definition/snapshots/artifact",
        }

        with (
            mock.patch.object(BENCH.shutil, "rmtree") as remove,
            self.assertRaisesRegex(ValueError, "must be an existing directory"),
        ):
            BENCH.snapshot(config)

        remove.assert_not_called()

    def test_snapshot_rejects_source_target_overlap_before_delete(self):
        source = self.root / "definition" / "snapshots" / "artifact"
        source.mkdir(parents=True)
        config = {
            "_root": self.root,
            "artifact_source": "definition/snapshots/artifact",
            "manifest": "definition/manifest.json",
            "snapshot": "definition/snapshots/artifact",
        }

        with (
            mock.patch.object(BENCH.shutil, "rmtree") as remove,
            self.assertRaisesRegex(ValueError, "must be separate directories"),
        ):
            BENCH.snapshot(config)

        remove.assert_not_called()

    def test_snapshot_rejects_missing_manifest_arm_before_delete(self):
        source = self.root / "source"
        source.mkdir()
        target = self.root / "definition" / "snapshots" / "artifact"
        target.mkdir(parents=True)
        manifest = self.root / "definition" / "manifest.json"
        manifest.write_text(
            json.dumps({"arms": {}}),
            encoding="utf-8",
        )
        config = {
            "_root": self.root,
            "artifact_source": "source",
            "manifest": "definition/manifest.json",
            "snapshot": "definition/snapshots/artifact",
            "treatment_arm": "with_artifact",
        }

        with (
            mock.patch.object(BENCH.shutil, "rmtree") as remove,
            self.assertRaises(KeyError),
        ):
            BENCH.snapshot(config)

        remove.assert_not_called()


if __name__ == "__main__":
    unittest.main()
