import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("aggregate_benchmark.py")
SPEC = importlib.util.spec_from_file_location("aggregate_benchmark", SCRIPT)
AGG = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AGG)


class AggregateTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def write_run(
        self, arm, run, state="valid", tokens=None, lint=2, cache_tokens=None,
        words=50, checker_words=None, passed=1, assertions=1,
        density_reliable=True,
    ):
        checker_words = words if checker_words is None else checker_words
        path = self.root / "eval-1-case" / f"{arm}@model" / f"run-{run}"
        path.mkdir(parents=True)
        (path / "result.json").write_text(json.dumps({
            "state": state, "model": "model", "duration_seconds": 1.5,
            "word_count": words, "usage": {
                "cache_creation_input_tokens": cache_tokens,
                "total_tokens": tokens,
            },
            "error": "provider failed" if state != "valid" else None,
        }), encoding="utf-8")
        if state == "valid":
            (path / "grading.json").write_text(json.dumps({
                "summary": {
                    "passed": passed, "failed": assertions - passed,
                    "total": assertions, "pass_rate": passed / assertions,
                },
                "lint": {
                    "total": lint, "total_per100w": lint * 100.0 / checker_words,
                    "words": checker_words, "density_reliable": density_reliable,
                },
            }), encoding="utf-8")

    def test_agent_rule_and_skill_arms_use_explicit_comparisons(self):
        for arm in ("baseline", "with_agent", "with_rule", "with_skill"):
            self.write_run(arm, 1, tokens=None)
        manifest = self.root / "evals.json"
        manifest.write_text(json.dumps({
            "artifact_name": "STE",
            "arms": {"baseline": {}, "with_agent": {}, "with_rule": {}, "with_skill": {}},
            "comparisons": [
                {"id": "agent", "label": "Agent", "primary": "with_agent", "baseline": "baseline"},
                {"id": "rule", "label": "Rule", "primary": "with_rule", "baseline": "baseline"},
                {"id": "skill", "label": "Skill", "primary": "with_skill", "baseline": "baseline"},
            ],
        }), encoding="utf-8")

        data = AGG.generate(self.root, manifest, "", "")

        self.assertEqual(data["schema_version"], 2)
        self.assertEqual(len(data["comparisons"]), 3)
        self.assertEqual(data["comparisons"][0]["models"]["model"]["baseline"]["valid_samples"], 1)
        self.assertIsNone(data["summaries"]["model"]["baseline"]["metrics"]["total_tokens"]["mean"])

    def test_dimension_preferences_remain_separate(self):
        self.write_run("baseline", 1)
        self.write_run("with_rule", 1)
        preferences = self.root / "preferences" / "rule" / "eval-1" / "model"
        preferences.mkdir(parents=True)
        (preferences / "run-1.json").write_text(json.dumps({
            "state": "valid", "comparison": "rule", "model": "model",
            "clarity_winner_arm": "with_rule",
            "fluency_winner_arm": "baseline",
            "directness_winner_arm": "tie",
        }), encoding="utf-8")
        manifest = self.root / "evals.json"
        manifest.write_text(json.dumps({
            "arms": {"baseline": {}, "with_rule": {}},
            "comparisons": [{"id": "rule", "primary": "with_rule", "baseline": "baseline"}],
        }), encoding="utf-8")

        result = AGG.generate(self.root, manifest, "STE", "")["comparisons"][0]["models"]["model"]

        self.assertEqual(result["primary"]["metrics"]["clarity_preference"]["mean"], 1.0)
        self.assertEqual(result["primary"]["metrics"]["fluency_preference"]["mean"], 0.0)
        self.assertEqual(result["primary"]["metrics"]["directness_preference"]["mean"], 0.5)

    def test_paired_corpus_uses_raw_totals(self):
        self.write_run("baseline", 1, lint=1, words=100, checker_words=25, passed=1, assertions=2)
        self.write_run("baseline", 2, lint=9, words=100, checker_words=75, passed=2, assertions=2)
        self.write_run("with_rule", 1, lint=0, words=100, checker_words=25, passed=2, assertions=2)
        self.write_run("with_rule", 2, lint=6, words=100, checker_words=75, passed=2, assertions=2)
        manifest = self.root / "evals.json"
        manifest.write_text(json.dumps({
            "arms": {"baseline": {}, "with_rule": {}},
            "comparisons": [{"id": "rule", "primary": "with_rule", "baseline": "baseline"}],
        }), encoding="utf-8")

        result = AGG.generate(self.root, manifest, "STE", "")["comparisons"][0]["models"]["model"]

        self.assertEqual(result["paired_corpus"]["baseline"]["lint_per100w"], 10.0)
        self.assertEqual(result["paired_corpus"]["primary"]["lint_per100w"], 6.0)
        self.assertEqual(result["paired_corpus"]["baseline"]["word_count"], 100)
        self.assertEqual(result["paired_corpus"]["primary"]["word_count"], 100)
        self.assertEqual(result["deltas"]["lint_per100w"], -4.0)
        self.assertEqual(result["paired_corpus"]["baseline"]["assertion_pass_rate"], 0.75)
        self.assertEqual(result["paired_corpus"]["primary"]["assertion_pass_rate"], 1.0)

    def test_unreliable_checker_density_is_excluded(self):
        self.write_run("baseline", 1, lint=4, checker_words=1, density_reliable=False)
        self.write_run("with_rule", 1, lint=0, checker_words=50)
        manifest = self.root / "evals.json"
        manifest.write_text(json.dumps({
            "arms": {"baseline": {}, "with_rule": {}},
            "comparisons": [{"id": "rule", "primary": "with_rule", "baseline": "baseline"}],
        }), encoding="utf-8")

        result = AGG.generate(self.root, manifest, "STE", "")["comparisons"][0]["models"]["model"]

        self.assertIsNone(result["baseline"]["metrics"]["lint_per100w"]["mean"])
        self.assertIsNone(result["paired_corpus"]["baseline"]["lint_per100w"])

    def test_rune_cache_usage_field_is_aggregated(self):
        self.write_run("baseline", 1, cache_tokens=17)
        manifest = self.root / "evals.json"
        manifest.write_text(json.dumps({
            "arms": {"baseline": {}},
            "comparisons": [],
        }), encoding="utf-8")

        data = AGG.generate(self.root, manifest, "STE", "")

        metric = data["summaries"]["model"]["baseline"]["metrics"]["cache_creation_input_tokens"]
        self.assertEqual(metric["mean"], 17.0)

    def test_encoded_model_directory_round_trips(self):
        self.assertEqual(
            AGG.split_arm("baseline@proton-lumo%2Flumo-max"),
            ("baseline", "proton-lumo/lumo-max"),
        )

    def test_generate_does_not_mutate_manifest_identities(self):
        self.write_run("baseline", 1)
        manifest = self.root / "evals.json"
        manifest.write_text(json.dumps({
            "arms": {"baseline": {}},
            "comparisons": [],
            "identities": {"checker": {"sha256": "abc"}},
        }), encoding="utf-8")
        original = AGG.read_json(manifest)

        AGG.generate(self.root, manifest, "STE", "")

        self.assertEqual(original["identities"], {"checker": {"sha256": "abc"}})

    def test_iteration_manifest_is_used_by_default(self):
        self.write_run("baseline", 1)
        self.write_run("with_skill", 1)
        (self.root / "manifest.json").write_text(json.dumps({
            "artifact_name": "Skill",
            "arms": {"baseline": {}, "with_skill": {}},
            "comparisons": [
                {"id": "skill", "primary": "with_skill", "baseline": "baseline"},
            ],
        }), encoding="utf-8")

        data = AGG.generate(self.root, None, "", "")

        self.assertEqual(data["metadata"]["artifact_name"], "Skill")
        self.assertEqual(data["comparisons"][0]["id"], "skill")
        self.assertEqual(data["metadata"]["identities"]["manifest"]["path"], str((self.root / "manifest.json").resolve()))

    def test_frozen_run_plan_adds_absent_planned_runs(self):
        self.write_run("baseline", 1)
        self.write_run("with_skill", 1)
        manifest = self.root / "manifest.json"
        manifest.write_text(json.dumps({
            "arms": {"baseline": {}, "with_skill": {}},
            "comparisons": [
                {"id": "skill", "primary": "with_skill", "baseline": "baseline"},
            ],
            "evals": [
                {"id": 1, "name": "case"},
                {"id": 2, "name": "second"},
            ],
            "run_plan": {
                "routes": [{"id": "fake", "model": "model"}],
                "repeats": 2,
                "seed": 1,
                "timeout_seconds": 300,
                "jobs": 1,
            },
        }), encoding="utf-8")

        data = AGG.generate(self.root, manifest, "Skill", "")
        result = data["comparisons"][0]["models"]["model"]

        self.assertEqual(data["metadata"]["run_counts"]["total"], 8)
        self.assertEqual(result["paired_samples"], 1)
        self.assertEqual(result["planned_pairs"], 4)
        self.assertEqual(result["primary"]["exclusion_reasons"], {"missing_execution": 3})
        self.assertEqual(result["baseline"]["exclusion_reasons"], {"missing_execution": 3})

    def test_structured_provider_error_becomes_safe_reason(self):
        path = self.root / "eval-1-case" / "baseline@model" / "run-1"
        path.mkdir(parents=True)
        (path / "result.json").write_text(json.dumps({
            "state": "provider_failure", "model": "model",
            "error": {"message": "quota", "code": 429},
        }), encoding="utf-8")
        manifest = self.root / "evals.json"
        manifest.write_text(json.dumps({"arms": {"baseline": {}}, "comparisons": []}), encoding="utf-8")

        data = AGG.generate(self.root, manifest, "STE", "")

        reasons = data["summaries"]["model"]["baseline"]["exclusion_reasons"]
        self.assertEqual(reasons["provider_failure (code 429)"], 1)
        self.assertNotIn("quota", reasons)

    def test_unpaired_runs_do_not_produce_delta(self):
        self.write_run("baseline", 1, lint=4)
        self.write_run("with_rule", 2, lint=1)
        manifest = self.root / "evals.json"
        manifest.write_text(json.dumps({
            "arms": {"baseline": {}, "with_rule": {}},
            "comparisons": [{"id": "rule", "primary": "with_rule", "baseline": "baseline"}],
        }), encoding="utf-8")

        data = AGG.generate(self.root, manifest, "STE", "")
        result = data["comparisons"][0]["models"]["model"]

        self.assertEqual(result["paired_samples"], 0)
        self.assertIsNone(result["deltas"]["lint_violations"])

    def test_default_comparison_keeps_baseline_on_right(self):
        self.write_run("baseline", 1)
        self.write_run("with_rule", 1)
        manifest = self.root / "evals.json"
        manifest.write_text(json.dumps({
            "arms": {"baseline": {}, "with_rule": {}},
            "comparisons": [],
        }), encoding="utf-8")

        data = AGG.generate(self.root, manifest, "STE", "")

        self.assertEqual(data["comparisons"][0]["primary"], "with_rule")
        self.assertEqual(data["comparisons"][0]["baseline"], "baseline")

    def test_missing_grading_uses_missing_grading_reason(self):
        path = self.root / "eval-1-case" / "baseline@model" / "run-1"
        path.mkdir(parents=True)
        (path / "result.json").write_text(json.dumps({
            "state": "valid", "model": "model",
        }), encoding="utf-8")
        manifest = self.root / "evals.json"
        manifest.write_text(json.dumps({
            "arms": {"baseline": {}}, "comparisons": [],
        }), encoding="utf-8")

        data = AGG.generate(self.root, manifest, "STE", "")
        summary = data["summaries"]["model"]["baseline"]

        self.assertEqual(summary["exclusion_reasons"], {"missing_grading": 1})

    def test_exclusions_remain_visible(self):
        self.write_run("baseline", 1, state="provider_failure")
        self.write_run("with_rule", 1)
        manifest = self.root / "evals.json"
        manifest.write_text(json.dumps({
            "arms": {"baseline": {}, "with_rule": {}},
            "comparisons": [{"id": "rule", "primary": "with_rule", "baseline": "baseline"}],
        }), encoding="utf-8")

        data = AGG.generate(self.root, manifest, "STE", "")
        baseline = data["comparisons"][0]["models"]["model"]["baseline"]

        self.assertEqual(baseline["valid_samples"], 0)
        self.assertEqual(baseline["exclusions"], 1)
        self.assertEqual(baseline["exclusion_reasons"]["provider_failure"], 1)


if __name__ == "__main__":
    unittest.main()
