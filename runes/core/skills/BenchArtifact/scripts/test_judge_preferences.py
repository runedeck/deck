"""Test independent preference parsing."""

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

import judge_preferences

VERDICT = {
    "clarity": {"winner": "A", "reason": "A is easier to understand."},
    "fluency": {"winner": "B", "reason": "B has smoother prose."},
    "directness": {"winner": "tie", "reason": "Both are equally direct."},
}
ASSERTIONS = [{
    "kind": "required_patterns",
    "text": "The response contains its required marker.",
    "patterns": ["response"],
}]


class PreferenceParserTests(unittest.TestCase):
    def test_parse_keeps_each_dimension_separate(self):
        stdout = json.dumps({"text": json.dumps(VERDICT)})

        self.assertEqual(judge_preferences.parse(stdout), VERDICT)

    def test_parse_accepts_one_complete_json_fence(self):
        verdict = {
            "clarity": {"winner": "A", "reason": "A is clearer."},
            "fluency": {"winner": "B", "reason": "B is smoother."},
            "directness": {"winner": "tie", "reason": "Both are direct."},
        }
        fenced = f"```json\n{json.dumps(verdict)}\n```"

        self.assertEqual(
            judge_preferences.parse(json.dumps({"text": fenced})),
            verdict,
        )

    def test_route_uses_response_kind_and_expanded_environment(self):
        verdict = {
            "clarity": {"winner": "A", "reason": "A is clearer."},
            "fluency": {"winner": "B", "reason": "B is smoother."},
            "directness": {"winner": "tie", "reason": "Both are direct."},
        }
        route = {
            "binary": sys.executable,
            "model": "judge-model",
            "vendor": "judge-vendor",
            "response": "json",
            "env": {"JUDGE_RESULT": "{prompt}"},
            "argv": [
                "-c",
                "import json, os; print(json.dumps({{'final_response': os.environ['JUDGE_RESULT']}}))",
            ],
        }

        result = judge_preferences.invoke("judge", route, json.dumps(verdict), 10)

        self.assertEqual(result["state"], "valid")
        self.assertEqual(
            judge_preferences.parse_verdict(result["response"]),
            verdict,
        )


class PreferenceMainTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.iteration = self.root / "iteration-1"
        self.iteration.mkdir()
        self.manifest = self.iteration / "manifest.json"
        self.routes = self.root / "routes.json"
        self.route = {
            "binary": sys.executable,
            "model": "judge-model",
            "vendor": "judge-vendor",
            "argv": ["-c", "print('unused')"],
            "response": "text",
            "context_canary": "List visible artifact rules.",
            "forbidden_context_markers": ["SECRET_ARTIFACT"],
        }
        self.routes.write_text(
            json.dumps({"routes": {"judge": self.route}}),
            encoding="utf-8",
        )

    def prepare_pairs(self, count: int) -> None:
        evals = []
        for eval_id in range(1, count + 1):
            name = f"case-{eval_id}"
            evals.append({
                "id": eval_id,
                "name": name,
                "prompt": "Rewrite the sample.",
                "files": [],
                "assertions": ASSERTIONS,
            })
            for arm in ("baseline", "with_skill"):
                run = (
                    self.iteration / f"eval-{eval_id}-{name}"
                    / f"{arm}@subject-model" / "run-1"
                )
                outputs = run / "outputs"
                outputs.mkdir(parents=True)
                response = f"The {arm} response is available."
                (run / "result.json").write_text(
                    json.dumps({
                        "schema_version": 2,
                        "state": "valid",
                        "eval_id": eval_id,
                        "eval_name": name,
                        "model": "subject-model",
                        "repeat": 1,
                        "arm": arm,
                        "response": response,
                        "word_count": len(response.split()),
                    }),
                    encoding="utf-8",
                )
                (outputs / "response.md").write_text(
                    response + "\n",
                    encoding="utf-8",
                )
        self.manifest.write_text(
            json.dumps({
                "schema_version": 2,
                "arms": {"baseline": {}, "with_skill": {}},
                "comparisons": [{
                    "id": "skill",
                    "primary": "with_skill",
                    "baseline": "baseline",
                }],
                "evals": evals,
                "run_plan": {
                    "routes": [{
                        "id": "subject",
                        "model": "subject-model",
                        "vendor": "subject-vendor",
                    }],
                    "registry_path": str(self.routes.resolve()),
                    "registry_sha256": (
                        judge_preferences.run_benchmark.artifact_digest(self.routes)
                    ),
                    "repeats": 1,
                },
            }),
            encoding="utf-8",
        )

    def arguments(self, *extra: str) -> list[str]:
        return [
            "--cross-harness",
            "--iteration", str(self.iteration),
            "--manifest", str(self.manifest),
            "--routes", str(self.routes),
            "--judge-route", "judge",
            "--seed", "7",
            *extra,
        ]

    def provider_result(self, prompt: str, resolved_model: str = "judge-model") -> dict:
        if prompt == judge_preferences.run_benchmark.PREFLIGHT_PROMPT:
            response = "OK"
        elif prompt == self.route["context_canary"]:
            response = "No tested marker is visible."
        else:
            response = json.dumps(VERDICT)
        result = {
            "state": "valid",
            "response": response,
            "provider_output": response,
            "returncode": 0,
            "stderr": "",
            "route": {
                "requested_route": "judge",
                "resolved_model": resolved_model,
            },
        }
        return judge_preferences.run_benchmark.validate_resolved_model(
            result, self.route["model"],
        )

    def fake_provider(self, _name, _route, prompt, _artifact, _files, _timeout):
        return self.provider_result(prompt)

    def test_cross_harness_consent_is_required_before_input_access(self):
        arguments = self.arguments()
        arguments.remove("--cross-harness")
        errors = io.StringIO()

        with mock.patch.object(
            judge_preferences.run_benchmark, "invoke",
        ) as provider, redirect_stderr(errors):
            status = judge_preferences.main(arguments)

        self.assertEqual(status, 1)
        self.assertIn("requires --cross-harness", errors.getvalue())
        provider.assert_not_called()

    def test_plan_counts_judgments_and_checks_without_provider_calls(self):
        self.prepare_pairs(1)
        output = io.StringIO()

        with mock.patch.object(
            judge_preferences.run_benchmark, "invoke",
        ) as provider, redirect_stdout(output):
            status = judge_preferences.main(self.arguments("--plan"))

        self.assertEqual(status, 0)
        self.assertIn(
            "1 blinded preference judgments and 2 route checks (3 provider calls)",
            output.getvalue(),
        )
        provider.assert_not_called()
        self.assertFalse((self.iteration / "preferences").exists())

    def test_unknown_model_is_rejected_before_provider_calls(self):
        self.prepare_pairs(1)
        errors = io.StringIO()

        with mock.patch.object(
            judge_preferences.run_benchmark, "invoke",
        ) as provider, redirect_stderr(errors):
            status = judge_preferences.main(
                self.arguments("--plan", "--model", "unknown-model")
            )

        self.assertEqual(status, 1)
        self.assertIn("unknown --model values: unknown-model", errors.getvalue())
        provider.assert_not_called()

    def test_same_vendor_pair_is_rejected_before_provider_calls(self):
        self.prepare_pairs(1)
        manifest = json.loads(self.manifest.read_text(encoding="utf-8"))
        manifest["run_plan"]["routes"][0]["vendor"] = self.route["vendor"]
        self.manifest.write_text(json.dumps(manifest), encoding="utf-8")
        errors = io.StringIO()

        with mock.patch.object(
            judge_preferences.run_benchmark, "invoke",
        ) as provider, redirect_stderr(errors):
            status = judge_preferences.main(self.arguments("--plan"))

        self.assertEqual(status, 1)
        self.assertIn(
            "the judge and subject models have the same vendor: subject-model",
            errors.getvalue(),
        )
        provider.assert_not_called()

    def test_tampered_route_registry_is_rejected_before_provider_calls(self):
        self.prepare_pairs(1)
        self.routes.write_text(
            json.dumps({"routes": {"judge": self.route}}, indent=2),
            encoding="utf-8",
        )
        errors = io.StringIO()

        with mock.patch.object(
            judge_preferences.run_benchmark, "invoke",
        ) as provider, redirect_stderr(errors):
            status = judge_preferences.main(self.arguments("--plan"))

        self.assertEqual(status, 1)
        self.assertIn(
            "the route registry digest does not match the frozen run plan",
            errors.getvalue(),
        )
        provider.assert_not_called()

    def test_approval_counts_judgments_and_route_checks(self):
        self.prepare_pairs(19)
        errors = io.StringIO()

        with mock.patch.object(
            judge_preferences.run_benchmark,
            "invoke",
            side_effect=self.fake_provider,
        ) as provider, redirect_stderr(errors):
            status = judge_preferences.main(self.arguments("--approve", "19"))

        self.assertEqual(status, 1)
        self.assertIn("Pass --approve 21", errors.getvalue())
        provider.assert_not_called()

        with mock.patch.object(
            judge_preferences.run_benchmark,
            "invoke",
            side_effect=self.fake_provider,
        ) as provider:
            status = judge_preferences.main(self.arguments("--approve", "21"))

        self.assertEqual(status, 0)
        self.assertEqual(provider.call_count, 21)
        record = json.loads(next(
            (self.iteration / "preferences").glob("**/run-1.json")
        ).read_text(encoding="utf-8"))
        self.assertEqual(record["judge_vendor"], "judge-vendor")

    def test_resolved_model_mismatch_stops_after_preflight(self):
        self.prepare_pairs(1)

        def mismatch(_name, _route, prompt, _artifact, _files, _timeout):
            return self.provider_result(prompt, resolved_model="other-model")

        with mock.patch.object(
            judge_preferences.run_benchmark, "invoke", side_effect=mismatch,
        ) as provider, redirect_stderr(io.StringIO()):
            status = judge_preferences.main(self.arguments())

        self.assertEqual(status, 1)
        self.assertEqual(provider.call_count, 1)
        self.assertFalse((self.iteration / "preferences").exists())

    def test_context_canary_stops_before_judgments(self):
        self.prepare_pairs(1)

        def leaking(_name, _route, prompt, _artifact, _files, _timeout):
            result = self.provider_result(prompt)
            if prompt == self.route["context_canary"]:
                result["response"] = "SECRET_ARTIFACT is visible."
            return result

        with mock.patch.object(
            judge_preferences.run_benchmark, "invoke", side_effect=leaking,
        ) as provider, redirect_stderr(io.StringIO()):
            status = judge_preferences.main(self.arguments())

        self.assertEqual(status, 1)
        self.assertEqual(provider.call_count, 2)
        self.assertFalse((self.iteration / "preferences").exists())


if __name__ == "__main__":
    unittest.main()
