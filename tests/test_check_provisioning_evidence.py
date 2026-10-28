"""scripts/check-provisioning-evidence refuses a provisioning rune without
a comparison record on two models that shows a changed answer
(provisioning-joins-the-deck, A Provisioning Rune Shows That It Helps)."""
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "check-provisioning-evidence"
SKILL = "---\nname: Alpha\ndescription: An example skill.\n---\n\n# Alpha\n\nBody.\n"
CHANGED = {"with": "pass", "without": "fail"}
SAME = {"with": "pass", "without": "pass"}
EXCLUDED = {"with": "excluded", "without": "excluded"}


def run(root):
    return subprocess.run(["python3", str(SCRIPT), str(root)], capture_output=True, text=True, check=False)


def skill(root, name="Alpha"):
    path = Path(root) / "runes" / "provisioning" / "skills" / name
    path.mkdir(parents=True)
    (path / "SKILL.md").write_text(SKILL)


def rule(root, name):
    path = Path(root) / "runes" / "provisioning" / "rules"
    path.mkdir(parents=True, exist_ok=True)
    (path / f"{name}.md").write_text(f"# {name}\n\nBody.\n")


def raw_record(root, name, text, change="some-change"):
    path = Path(root) / "docs" / "changes" / change / "comparisons" / f"{name}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def record(root, name, *cases, change="some-change"):
    models = sorted({model for case in cases for model in case})
    body = {
        "rune": name,
        "models": models,
        "cases": [{"id": str(number), "name": f"case-{number}", "results": case} for number, case in enumerate(cases, 1)],
        "sources": [],
    }
    raw_record(root, name, json.dumps(body, indent=2, sort_keys=True), change=change)


class ComparisonEvidence(unittest.TestCase):
    def test_rune_without_record_fails_and_is_named(self):
        with tempfile.TemporaryDirectory() as scratch:
            skill(scratch)
            result = run(scratch)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertEqual(result.stderr, "", "a check that crashes is not a finding")
            self.assertEqual(result.stdout, "runes/provisioning/skills/Alpha: no comparison record\n")

    def test_rule_without_record_fails(self):
        with tempfile.TemporaryDirectory() as scratch:
            rule(scratch, "Boundary")
            result = run(scratch)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(result.stdout, "runes/provisioning/rules/Boundary.md: no comparison record\n")

    def test_passing_record_passes(self):
        with tempfile.TemporaryDirectory() as scratch:
            skill(scratch)
            record(scratch, "Alpha", {"model-a": CHANGED, "model-b": SAME}, {"model-a": SAME, "model-b": EXCLUDED})
            result = run(scratch)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(result.stdout, "")

    def test_archived_record_passes(self):
        with tempfile.TemporaryDirectory() as scratch:
            skill(scratch)
            record(scratch, "Alpha", {"model-a": CHANGED, "model-b": SAME}, change="archive/2026-01-01-old-change")
            self.assertEqual(run(scratch).returncode, 0)

    def test_one_model_fails(self):
        with tempfile.TemporaryDirectory() as scratch:
            skill(scratch)
            record(scratch, "Alpha", {"model-a": CHANGED}, {"model-a": SAME})
            result = run(scratch)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(
                result.stdout,
                "runes/provisioning/skills/Alpha: fewer than two models (docs/changes/some-change/comparisons/Alpha.json)\n",
            )

    def test_excluded_arm_does_not_count_as_a_model(self):
        with tempfile.TemporaryDirectory() as scratch:
            skill(scratch)
            record(scratch, "Alpha", {"model-a": CHANGED, "model-b": {"with": "pass", "without": "excluded"}})
            result = run(scratch)
            self.assertEqual(result.returncode, 1)
            self.assertIn("fewer than two models", result.stdout)

    def test_no_changed_answer_fails(self):
        with tempfile.TemporaryDirectory() as scratch:
            skill(scratch)
            record(scratch, "Alpha", {"model-a": SAME, "model-b": SAME}, {"model-a": {"with": "fail", "without": "pass"}, "model-b": SAME})
            result = run(scratch)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(
                result.stdout,
                "runes/provisioning/skills/Alpha: no changed answer (docs/changes/some-change/comparisons/Alpha.json)\n",
            )

    def test_malformed_record_is_a_finding_and_the_later_rune_is_still_checked(self):
        malformed = {
            "not an object": "[]",
            "cases not a list": '{"cases": {}}',
            "case not an object": '{"cases": ["x"]}',
            "results a string": '{"cases": [{"id": "1", "name": "x", "results": "pass"}]}',
            "result a string": '{"cases": [{"id": "1", "name": "x", "results": {"m": "pass"}}]}',
            "unknown verdict": '{"cases": [{"id": "1", "name": "x", "results": {"m": {"with": "yes", "without": "fail"}}}]}',
            "list verdict": '{"cases": [{"id": "1", "name": "x", "results": {"m": {"with": [], "without": "fail"}}}]}',
            "object verdict": '{"cases": [{"id": "1", "name": "x", "results": {"m": {"with": "pass", "without": {}}}}]}',
            "null verdict": '{"cases": [{"id": "1", "name": "x", "results": {"m": {"with": null, "without": "fail"}}}]}',
        }
        for label, text in malformed.items():
            with self.subTest(label), tempfile.TemporaryDirectory() as scratch:
                skill(scratch, "Alpha")
                skill(scratch, "Beta")
                raw_record(scratch, "Alpha", text)
                result = run(scratch)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertEqual(result.stderr, "", "a check that crashes is not a finding")
                self.assertRegex(
                    result.stdout,
                    r"^runes/provisioning/skills/Alpha: malformed record: .+ \(docs/changes/some-change/comparisons/Alpha\.json\)\n"
                    r"runes/provisioning/skills/Beta: no comparison record\n$",
                )

    def test_record_without_rune_is_ignored(self):
        with tempfile.TemporaryDirectory() as scratch:
            skill(scratch)
            record(scratch, "Alpha", {"model-a": CHANGED, "model-b": SAME})
            record(scratch, "Gone", {"model-a": SAME})
            self.assertEqual(run(scratch).returncode, 0)

    def test_absent_module_passes(self):
        with tempfile.TemporaryDirectory() as scratch:
            (Path(scratch) / "runes" / "core").mkdir(parents=True)
            self.assertEqual(run(scratch).returncode, 0)


if __name__ == "__main__":
    unittest.main()
