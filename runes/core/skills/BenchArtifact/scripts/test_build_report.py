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
    def test_report_data_removes_local_paths_and_provider_diagnostics(self):
        benchmark = {
            "schema_version": 2,
            "metadata": {
                "artifact_path": "/private/artifacts/Rule.md",
                "identities": {
                    "checker": {"path": "/private/bin/ste-lint.py"},
                    "manifest": {"path": "/private/evals/evals.json"},
                },
            },
            "arms": {
                "with_rule": {"artifact_kind": "rule", "artifact_path": "Rule.md"},
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

            match = re.search(r'atob\("([A-Za-z0-9+/=]+)"\)', output.read_text(encoding="utf-8"))
            data = json.loads(base64.b64decode(match.group(1)))
        self.assertEqual(data["metadata"]["artifact_path"], "Rule.md")
        self.assertEqual(data["metadata"]["identities"]["checker"]["path"], "ste-lint.py")
        self.assertEqual(
            data["metadata"]["identities"]["checker"]["path_url"],
            "file:///private/bin/ste-lint.py",
        )
        self.assertEqual(
            data["arms"]["with_rule"]["artifact_url"],
            "file:///private/evals/Rule.md",
        )
        self.assertEqual(
            data["arms"]["with_skill"]["artifact_url"],
            "file:///private/evals/Skill/SKILL.md",
        )
        self.assertEqual(data["runs"][0]["route"]["resolved_binary"], "claude")
        self.assertNotIn("stderr", data["preference_judgments"][0])

    def test_template_keeps_generic_metrics_and_guards_small_samples(self):
        template = REPORT.TEMPLATE_PATH.read_text(encoding="utf-8")

        self.assertIn("paired * 2 < planned", template)
        self.assertIn("Checker findings", template)
        self.assertIn('pairedMetric(data, "primary", name)', template)
        self.assertIn('label: "Improves controlled English"', template)
        self.assertIn('label: "No meaning data"', template)
        self.assertIn('Required meaning data is unavailable.', template)
        self.assertNotIn("proseRejected", template)
        self.assertIn(".filter(([name])", template)
        self.assertNotIn("controlled-language violations", template)
        self.assertLess(template.index('id="summary"'), template.index('id="verdict-rows"'))
        self.assertIn("nav.side ul { display: flex", template)
        self.assertIn("grid-template-columns: minmax(0, 1fr)", template)
        self.assertIn("overflow-wrap: anywhere", template)
        self.assertIn("flex: 1 0 100%", template)
        self.assertIn("No run records are available for this comparison.", template)
        self.assertIn("#1e1e2e", template)
        self.assertIn("#cdd6f4", template)
        self.assertIn('role="radiogroup" aria-label="Theme"', template)
        self.assertIn('document.documentElement.removeAttribute("data-theme")', template)
        self.assertIn('localStorage.setItem("bench-theme", value)', template)
        self.assertIn('link.href = href', template)
        self.assertIn('link.href = pathUrl || value', template)
        self.assertIn('"syntax-key"', template)
        self.assertIn('row.dataset.verdict = summary.cls.replace', template)
        self.assertIn('role="tablist" aria-label="Verdict comparison"', template)
        self.assertIn('new Intl.ListFormat("en"', template)
        self.assertIn('"Checker findings did not change."', template)
        self.assertIn("setVerdictComparison(comparisonList[0].id)", template)
        self.assertIn('button.dataset.kind = kind || "artifact"', template)
        self.assertIn('event.key === "ArrowRight"', template)
        self.assertIn("button.tabIndex = selected ? 0 : -1", template)
        self.assertIn('[hidden] { display: none !important; }', template)
        self.assertIn('row.setAttribute("aria-hidden", String(hidden))', template)
        self.assertIn('class="verdict-grid"', template)
        self.assertIn('id="pair-view"', template)
        self.assertIn("const renderPair = () => {", template)
        self.assertIn("Blind judgment for this pair", template)
        self.assertEqual(template.count("Every matched pair shows the same task answered"), 1)
        self.assertNotIn("p { max-width: 76ch; }", template)
        self.assertNotIn("nav.side { display: none; }", template)


if __name__ == "__main__":
    unittest.main()
