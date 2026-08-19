"""Test independent preference parsing."""

import json
import sys
import unittest

import judge_preferences


class PreferenceParserTests(unittest.TestCase):
    def test_parse_keeps_each_dimension_separate(self):
        verdict = {
            "clarity": {"winner": "A", "reason": "A is easier to understand."},
            "fluency": {"winner": "B", "reason": "B has smoother prose."},
            "directness": {"winner": "tie", "reason": "Both are equally direct."},
        }
        stdout = json.dumps({"text": json.dumps(verdict)})

        self.assertEqual(judge_preferences.parse(stdout), verdict)

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
            "response": "json",
            "env": {"JUDGE_RESULT": "{prompt}"},
            "argv": [
                "-c",
                "import json, os; print(json.dumps({{'final_response': os.environ['JUDGE_RESULT']}}))",
            ],
        }

        process = judge_preferences.invoke(route, json.dumps(verdict), 10)

        self.assertEqual(process.returncode, 0)
        self.assertEqual(
            judge_preferences.parse(process.stdout, response_kind=route["response"]),
            verdict,
        )


if __name__ == "__main__":
    unittest.main()
