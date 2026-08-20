import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("grade_iteration.py")
SPEC = importlib.util.spec_from_file_location("grade_iteration", SCRIPT)
GRADE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GRADE)


def execution_fixture(root: Path):
    manifest = {
        "schema_version": 2,
        "arms": {"baseline": {}},
        "comparisons": [],
        "evals": [{
            "id": 1,
            "name": "case",
            "prompt": "Review.",
            "assertions": [{
                "kind": "required_patterns",
                "text": "Keep the fact.",
                "patterns": ["fact"],
            }],
        }],
        "run_plan": {"models": ["model"], "repeats": 1},
    }
    case = manifest["evals"][0]
    result_dir = GRADE.run_benchmark.result_dir(root, case, "baseline", "model", 1)
    response = result_dir / "outputs" / "response.md"
    response.parent.mkdir(parents=True)
    response.write_text("Keep the fact.\n", encoding="utf-8")
    execution = {
        "schema_version": 2,
        "eval_id": 1,
        "eval_name": "case",
        "arm": "baseline",
        "model": "model",
        "repeat": 1,
        "state": "valid",
        "response": "Keep the fact.",
        "word_count": 3,
    }
    return manifest, result_dir / "result.json", execution


class GradeIterationTests(unittest.TestCase):
    def test_execution_identity_and_response_match_the_frozen_plan(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            manifest, result_path, execution = execution_fixture(root)
            cases = {1: manifest["evals"][0]}
            run_plan = GRADE.run_benchmark.normalize_run_plan(manifest, required=True)

            case, response, text = GRADE.run_benchmark.validate_execution(
                result_path, execution, root, manifest, cases, run_plan,
            )

            self.assertEqual(case["id"], 1)
            self.assertEqual(response, result_path.parent / "outputs" / "response.md")
            self.assertEqual(text, "Keep the fact.")

    def test_execution_rejects_agent_written_identity_and_response_changes(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            manifest, result_path, execution = execution_fixture(root)
            cases = {1: manifest["evals"][0]}
            run_plan = GRADE.run_benchmark.normalize_run_plan(manifest, required=True)
            changes = {
                "schema_version": 1,
                "state": "unknown",
                "eval_id": 2,
                "eval_name": "other",
                "arm": "other",
                "model": "other",
                "repeat": 2,
                "response": "Different response.",
                "word_count": 99,
            }

            for field, value in changes.items():
                with self.subTest(field=field):
                    changed = copy.deepcopy(execution)
                    changed[field] = value
                    with self.assertRaises((TypeError, ValueError)):
                        GRADE.run_benchmark.validate_execution(
                            result_path, changed, root, manifest, cases, run_plan,
                        )

            wrong_path = root / "eval-1-case" / "wrong@model" / "run-1" / "result.json"
            with self.assertRaisesRegex(ValueError, "identity does not match"):
                GRADE.run_benchmark.validate_execution(
                    wrong_path, execution, root, manifest, cases, run_plan,
                )

    def test_structured_assertions_support_optional_word_bounds(self):
        case = {
            "minimum_words": 3,
            "assertions": [
                {"kind": "word_range", "text": "The response has at least three words."},
                {
                    "kind": "required_patterns",
                    "text": "The response keeps the limit.",
                    "patterns": ["25 jobs"],
                },
            ],
        }

        checks = GRADE.grade_case(case, "Keep the 25 jobs limit.")

        self.assertTrue(all(check["passed"] for check in checks))
        self.assertIn("required at least 3", checks[0]["evidence"])

    def test_plain_string_assertion_reports_the_schema_error(self):
        with self.assertRaisesRegex(TypeError, "assertion must be an object"):
            GRADE.grade_case({"assertions": ["Keep every number."]}, "Keep 25.")

    def test_validate_only_checks_native_manifest_resources(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            manifest = root / "manifest.json"
            manifest.write_text(json.dumps({
                "schema_version": 2,
                "arms": {
                    "baseline": {},
                    "with_rule": {
                        "artifact_kind": "rule",
                        "artifact_path": "../outside.md",
                    },
                },
                "comparisons": [{
                    "id": "rule", "primary": "with_rule", "baseline": "baseline",
                }],
                "evals": [{
                    "id": 1, "name": "case", "prompt": "Review.",
                    "assertions": [{
                        "kind": "required_patterns", "text": "Keep the fact.",
                        "patterns": ["fact"],
                    }],
                }],
                "run_plan": {"models": ["model"], "repeats": 1},
            }), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "escapes the manifest directory"):
                GRADE.main(["--manifest", str(manifest), "--validate-only"])


if __name__ == "__main__":
    unittest.main()
