import base64
import importlib.util
import json
import re
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("build_report.py")
SPEC = importlib.util.spec_from_file_location("build_report", SCRIPT)
REPORT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(REPORT)


class BuildReportTests(unittest.TestCase):
    def embedded_data(self, output: Path) -> dict:
        match = re.search(
            r'atob\("([A-Za-z0-9+/=]+)"\)',
            output.read_text(encoding="utf-8"),
        )
        return json.loads(base64.b64decode(match.group(1)))

    def test_report_data_removes_local_paths_and_provider_diagnostics(self):
        benchmark = {
            "schema_version": 2,
            "metadata": {
                "artifact_path": "/private/artifacts/Rule.md",
                "identities": {
                    "checker": {"path": "/private/bin/lint.py"},
                    "manifest": {"path": "/private/evals/evals.json"},
                },
            },
            "arms": {
                "with_rule": {
                    "artifact_kind": "rule",
                    "artifact_path": "/private/evals/Rule.md",
                    "artifact_source": "/private/source/Rule.md",
                },
                "with_skill": {"artifact_kind": "skill", "artifact_path": "Skill"},
            },
            "comparisons": [],
            "runs": [{"route": {"resolved_binary": "/private/bin/claude"}}],
            "preference_judgments": [{
                "state": "valid", "clarity_winner": "A",
                "clarity_winner_arm": "with_rule",
                "clarity_reason": "Output A is clearer.", "stderr": "secret diagnostic",
            }],
        }
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "benchmark.json"
            output = root / "report.html"
            source.write_text(json.dumps(benchmark), encoding="utf-8")

            REPORT.build_report(source, output)

            data = self.embedded_data(output)
        self.assertEqual(data["metadata"]["artifact_path"], "Rule.md")
        self.assertEqual(data["metadata"]["identities"]["checker"]["path"], "lint.py")
        self.assertNotIn("path_url", data["metadata"]["identities"]["checker"])
        self.assertNotIn("artifact_url", data["arms"]["with_rule"])
        self.assertNotIn("artifact_url", data["arms"]["with_skill"])
        self.assertEqual(data["arms"]["with_rule"]["artifact_path"], "Rule.md")
        self.assertEqual(data["arms"]["with_rule"]["artifact_source"], "Rule.md")
        self.assertEqual(data["runs"][0]["route"]["resolved_binary"], "claude")
        self.assertNotIn("stderr", data["preference_judgments"][0])

    def test_local_links_require_explicit_opt_in(self):
        benchmark = {
            "schema_version": 2,
            "metadata": {
                "identities": {
                    "checker": {"path": "/private/bin/lint.py"},
                    "manifest": {"path": "/private/evals/evals.json"},
                },
            },
            "arms": {
                "with_rule": {"artifact_kind": "rule", "artifact_path": "Rule.md"},
                "with_skill": {"artifact_kind": "skill", "artifact_path": "Skill"},
            },
            "comparisons": [],
        }
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "benchmark.json"
            output = root / "report.html"
            source.write_text(json.dumps(benchmark), encoding="utf-8")

            REPORT.build_report(source, output, local_links=True)

            data = self.embedded_data(output)
        self.assertEqual(data["metadata"]["identities"]["checker"]["path_url"], "file:///private/bin/lint.py")
        self.assertEqual(data["arms"]["with_rule"]["artifact_url"], "file:///private/evals/Rule.md")
        self.assertEqual(data["arms"]["with_skill"]["artifact_url"], "file:///private/evals/Skill/SKILL.md")

    def test_schema_v2_report_backfills_a_missing_verdict(self):
        preference_metrics = {
            f"{dimension}_preference": {"count": 1, "mean": 0.5}
            for dimension in ("clarity", "fluency", "directness")
        }
        benchmark = {
            "schema_version": 2,
            "metadata": {"artifact_name": "Artifact", "models": ["model"]},
            "arms": {"baseline": {}, "with_artifact": {}},
            "comparisons": [{
                "id": "artifact",
                "primary": "with_artifact",
                "baseline": "baseline",
                "models": {"model": {
                    "paired_samples": 1,
                    "planned_pairs": 1,
                    "delta_stats": {
                        "assertion_pass_rate": {"count": 1},
                        "lint_per100w": {"count": 1},
                    },
                    "primary": {"metrics": preference_metrics},
                    "baseline": {"metrics": {}},
                    "paired_corpus": {
                        "primary": {
                            "assertions_passed": 1,
                            "assertions_total": 1,
                            "lint_per100w": 1.0,
                        },
                        "baseline": {"lint_per100w": 2.0},
                        "deltas": {
                            "assertion_pass_rate": 0.0,
                            "lint_per100w": -1.0,
                        },
                    },
                }},
            }],
        }
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "benchmark.json"
            output = root / "report.html"
            source.write_text(json.dumps(benchmark), encoding="utf-8")

            REPORT.build_report(source, output)

            data = self.embedded_data(output)
        verdict = data["comparisons"][0]["models"]["model"]["verdict"]
        self.assertEqual(verdict["status"], "ok")
        self.assertEqual(verdict["label"], "Improves the claimed behavior")
        self.assertIn("across 1 judged pair", " ".join(verdict["parts"]))
        self.assertEqual(
            data["verdict_thresholds"],
            {"trade_off": 0.4, "win": 0.5},
        )


if __name__ == "__main__":
    unittest.main()
