"""Tests for run_eval, using a fake harness adapter registered in the registry."""

import contextlib
import io
import json
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

import scripts.harness
from scripts import run_eval as run_eval_module
from scripts.run_eval import run_eval, validate_skill_name

FAKE_MODULE = "scripts.harness.fake_probe_adapter"
BARE_MODULE = "scripts.harness.fake_bare_adapter"


def item(query: str, should_trigger: bool = True) -> dict:
    return {"query": query, "should_trigger": should_trigger}


class FakeHarnessCase(unittest.TestCase):
    """Registers a fake adapter whose probe outcomes are scripted per query."""

    def setUp(self):
        self.outcomes: dict[str, list] = {}
        self.calls: list[dict] = []
        case = self

        def probe_trigger(query, skill_name, skill_description, project_root, timeout, model=None):
            case.calls.append(
                {
                    "query": query,
                    "skill_name": skill_name,
                    "description": skill_description,
                    "project_root": project_root,
                    "timeout": timeout,
                    "model": model,
                    "commands_dir_present": (Path(project_root) / ".claude" / "commands").is_dir(),
                }
            )
            outcome = case.outcomes[query].pop(0)
            if isinstance(outcome, Exception):
                raise outcome
            return outcome

        fake = types.ModuleType(FAKE_MODULE)
        fake.probe_trigger = probe_trigger
        bare = types.ModuleType(BARE_MODULE)

        for patcher in (
            mock.patch.dict(sys.modules, {FAKE_MODULE: fake, BARE_MODULE: bare}),
            mock.patch.dict(
                scripts.harness._HARNESS_MODULES, {"fake": FAKE_MODULE, "bare": BARE_MODULE}
            ),
        ):
            patcher.start()
            self.addCleanup(patcher.stop)

    def evaluate(self, eval_set, **overrides):
        kwargs = {
            "skill_name": "demo-skill",
            "description": "the description",
            "num_workers": 1,
            "timeout": 7,
            "runs_per_query": 2,
            "trigger_threshold": 0.5,
            "harness_name": "fake",
        }
        kwargs.update(overrides)
        return run_eval(eval_set, **kwargs)


class RunEvalTests(FakeHarnessCase):
    def test_should_trigger_passes_at_threshold(self):
        self.outcomes = {"q": [True, False]}
        result = self.evaluate([item("q")])
        entry = result["results"][0]
        self.assertEqual(entry["triggers"], 1)
        self.assertEqual(entry["runs"], 2)
        self.assertAlmostEqual(entry["trigger_rate"], 0.5)
        self.assertTrue(entry["pass"])
        self.assertEqual(result["summary"], {"total": 1, "passed": 1, "failed": 0})

    def test_should_trigger_fails_below_threshold(self):
        self.outcomes = {"q": [False, False]}
        result = self.evaluate([item("q")])
        self.assertFalse(result["results"][0]["pass"])
        self.assertEqual(result["summary"], {"total": 1, "passed": 0, "failed": 1})

    def test_should_not_trigger_fails_at_threshold(self):
        self.outcomes = {"q": [True, False]}
        result = self.evaluate([item("q", should_trigger=False)])
        entry = result["results"][0]
        self.assertAlmostEqual(entry["trigger_rate"], 0.5)
        self.assertFalse(entry["pass"])

    def test_should_not_trigger_passes_below_threshold(self):
        self.outcomes = {"q": [True, False, False]}
        result = self.evaluate([item("q", should_trigger=False)], runs_per_query=3)
        entry = result["results"][0]
        self.assertEqual(entry["triggers"], 1)
        self.assertAlmostEqual(entry["trigger_rate"], 1 / 3)
        self.assertTrue(entry["pass"])

    def test_results_keep_eval_set_order_and_metadata(self):
        self.outcomes = {"b": [True, True], "a": [False, False], "c": [True, True]}
        result = self.evaluate(
            [item("b"), item("a", should_trigger=False), item("c", should_trigger=False)],
            model="model-x",
        )
        self.assertEqual([r["query"] for r in result["results"]], ["b", "a", "c"])
        self.assertEqual([r["pass"] for r in result["results"]], [True, True, False])
        self.assertEqual(result["skill_name"], "demo-skill")
        self.assertEqual(result["description"], "the description")
        self.assertEqual(result["summary"], {"total": 3, "passed": 2, "failed": 1})
        self.assertEqual(len(self.calls), 6)
        self.assertEqual(self.calls[0]["model"], "model-x")
        self.assertEqual(self.calls[0]["timeout"], 7)
        self.assertEqual(self.calls[0]["description"], "the description")

    def test_probe_exception_counts_as_not_picked_with_warning(self):
        self.outcomes = {"q": [RuntimeError("probe broke"), True]}
        captured = io.StringIO()
        with contextlib.redirect_stderr(captured):
            result = self.evaluate([item("q")])
        entry = result["results"][0]
        self.assertEqual(entry["triggers"], 1)
        self.assertTrue(entry["pass"])
        self.assertIn("warning", captured.getvalue().lower())
        self.assertIn("probe broke", captured.getvalue())

    def test_duplicate_query_raises(self):
        with self.assertRaises(ValueError) as caught:
            self.evaluate([item("same"), item("same", should_trigger=False)])
        self.assertIn("duplicate", str(caught.exception).lower())
        self.assertEqual(self.calls, [])

    def test_invalid_skill_names_raise(self):
        for bad in ("has space", "double--dash", "-leading", "trailing_", "dot.name", "", "a" * 65):
            with self.subTest(name=bad), self.assertRaises(ValueError):
                self.evaluate([item("q")], skill_name=bad)

    def test_valid_skill_names_accepted(self):
        for good in ("a", "my-skill", "my_skill-2", "A1-b2_C3", "x" * 64):
            with self.subTest(name=good):
                validate_skill_name(good)

    def test_harness_without_probe_trigger_raises(self):
        with self.assertRaises(ValueError) as caught:
            self.evaluate([item("q")], harness_name="bare")
        self.assertIn("probe", str(caught.exception).lower())

    def test_unknown_harness_raises(self):
        with self.assertRaises(ValueError):
            self.evaluate([item("q")], harness_name="nope")

    def test_temporary_project_dir_exists_during_probes_and_is_removed(self):
        self.outcomes = {"q": [True, True]}
        self.evaluate([item("q")])
        roots = {call["project_root"] for call in self.calls}
        self.assertEqual(len(roots), 1)
        root = roots.pop()
        self.assertTrue(all(call["commands_dir_present"] for call in self.calls))
        self.assertFalse(Path(root).exists())

    def test_temporary_project_dir_removed_when_worker_raises(self):
        roots = []

        def exploding(job):
            roots.append(job.project_root)
            raise RuntimeError("worker crashed")

        with mock.patch.object(run_eval_module, "run_probe", exploding), self.assertRaises(RuntimeError):
            self.evaluate([item("q")])
        self.assertEqual(len(roots), 1)
        self.assertFalse(Path(roots[0]).exists())


class CommandLineTests(FakeHarnessCase):
    def setUp(self):
        super().setUp()
        holder = tempfile.TemporaryDirectory()
        self.addCleanup(holder.cleanup)
        self.work = Path(holder.name)
        self.skill_dir = self.work / "demo"
        self.skill_dir.mkdir()
        (self.skill_dir / "SKILL.md").write_text(
            "---\nname: demo-skill\ndescription: Frontmatter description\n---\n",
            encoding="utf-8",
        )
        self.eval_path = self.work / "evals.json"
        self.eval_path.write_text(
            json.dumps([item("one"), item("two", should_trigger=False)]), encoding="utf-8"
        )

    def run_main(self, *extra: str) -> tuple[str, str, int | None]:
        out, err = io.StringIO(), io.StringIO()
        code = None
        args = [
            "--eval-set", str(self.eval_path),
            "--skill-path", str(self.skill_dir),
            "--harness", "fake",
            "--num-workers", "1",
            "--runs-per-query", "1",
            *extra,
        ]
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                run_eval_module.main(args)
            except SystemExit as stop:
                code = stop.code
        return out.getvalue(), err.getvalue(), code

    def test_main_prints_json_with_frontmatter_description(self):
        self.outcomes = {"one": [True], "two": [False]}
        out, _, code = self.run_main()
        self.assertIsNone(code)
        data = json.loads(out)
        self.assertEqual(data["description"], "Frontmatter description")
        self.assertEqual(data["summary"], {"total": 2, "passed": 2, "failed": 0})
        self.assertIn("\n  ", out)

    def test_main_description_override_and_verbose(self):
        self.outcomes = {"one": [False], "two": [True]}
        out, err, _ = self.run_main("--description", "Override text", "--verbose")
        data = json.loads(out)
        self.assertEqual(data["description"], "Override text")
        self.assertIn("Override text", err)
        self.assertIn("Passed 0/2", err)
        self.assertIn("FAIL", err)
        self.assertIn("one", err)

    def test_main_missing_skill_md_exits_one(self):
        (self.skill_dir / "SKILL.md").unlink()
        _, err, code = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("SKILL.md", err)

    def test_main_value_error_exits_one(self):
        self.eval_path.write_text(json.dumps([item("dup"), item("dup")]), encoding="utf-8")
        _, err, code = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("duplicate", err.lower())


if __name__ == "__main__":
    unittest.main()
