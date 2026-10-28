"""Tests for the optimization loop, with evaluation and improvement patched out."""

import argparse
import random
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import run_loop as loop_module
from scripts.run_loop import holdout_fraction, run_loop, split_eval_set

D0 = "Zero. USE WHEN a. NOT FOR b"
D1 = "One. USE WHEN a. NOT FOR b"
D2 = "Two. USE WHEN a. NOT FOR b"
RUNS = 3
SHOULD = ["s1", "s2", "s3"]
SHOULD_NOT = ["n1", "n2", "n3"]
EVAL_SET = [{"query": q, "should_trigger": True} for q in SHOULD] + [
    {"query": q, "should_trigger": False} for q in SHOULD_NOT
]


def fake_run_eval_for(picks_by_description: dict[str, dict[str, int]]):
    """Build a run_eval stand-in whose picks per query depend on the description."""

    def fake_run_eval(
        eval_set,
        skill_name,
        description,
        num_workers,
        timeout,
        runs_per_query=1,
        trigger_threshold=0.5,
        model=None,
        harness_name="claude",
    ):
        picks = picks_by_description[description]
        results = []
        for entry in eval_set:
            triggers = picks.get(entry["query"], 0)
            rate = triggers / runs_per_query
            if entry["should_trigger"]:
                passed = rate >= trigger_threshold
            else:
                passed = rate < trigger_threshold
            results.append(
                {
                    "query": entry["query"],
                    "should_trigger": entry["should_trigger"],
                    "trigger_rate": rate,
                    "triggers": triggers,
                    "runs": runs_per_query,
                    "pass": passed,
                }
            )
        passed_count = sum(1 for r in results if r["pass"])
        return {
            "skill_name": skill_name,
            "description": description,
            "results": results,
            "summary": {
                "total": len(results),
                "passed": passed_count,
                "failed": len(results) - passed_count,
            },
        }

    return fake_run_eval


def all_should_picked(**overrides: int) -> dict[str, int]:
    """Picks where every should-trigger query is picked and no other, then overrides."""
    picks = {q: RUNS for q in SHOULD}
    picks.update(overrides)
    return picks


class SplitEvalSetTests(unittest.TestCase):
    def test_same_seed_gives_same_split(self):
        first = split_eval_set(EVAL_SET, 0.4, seed=7)
        second = split_eval_set(EVAL_SET, 0.4, seed=7)
        self.assertEqual(first, second)

    def test_global_random_state_untouched(self):
        random.seed(1234)
        expected = random.random()
        random.seed(1234)
        split_eval_set(EVAL_SET, 0.4)
        self.assertEqual(random.random(), expected)

    def test_sizes_per_group(self):
        big = [{"query": f"s{i}", "should_trigger": True} for i in range(10)] + [
            {"query": f"n{i}", "should_trigger": False} for i in range(10)
        ]
        train, test = split_eval_set(big, 0.4)
        self.assertEqual(len(test), 8)
        self.assertEqual(len(train), 12)
        self.assertEqual(sum(1 for e in test if e["should_trigger"]), 4)
        self.assertEqual(sum(1 for e in train if e["should_trigger"]), 6)
        self.assertEqual(sorted(e["query"] for e in train + test), sorted(e["query"] for e in big))

    def test_one_item_group_stays_in_train(self):
        eval_set = [{"query": q, "should_trigger": True} for q in SHOULD] + [
            {"query": "lonely", "should_trigger": False}
        ]
        train, test = split_eval_set(eval_set, 0.4)
        self.assertEqual([e["query"] for e in test if not e["should_trigger"]], [])
        self.assertIn({"query": "lonely", "should_trigger": False}, train)
        self.assertEqual(len(test), 1)

    def test_single_item_set_and_empty_set(self):
        train, test = split_eval_set([{"query": "only", "should_trigger": True}], 0.5)
        self.assertEqual(len(train), 1)
        self.assertEqual(test, [])
        self.assertEqual(split_eval_set([], 0.5), ([], []))

    def test_train_never_empty_for_two_item_group(self):
        two = [{"query": "a", "should_trigger": True}, {"query": "b", "should_trigger": True}]
        train, test = split_eval_set(two, 0.9)
        self.assertEqual(len(train), 1)
        self.assertEqual(len(test), 1)


class RunLoopTests(unittest.TestCase):
    def setUp(self):
        holder = tempfile.TemporaryDirectory()
        self.addCleanup(holder.cleanup)
        self.work = Path(holder.name)
        self.skill_dir = self.work / "demo"
        self.skill_dir.mkdir()
        (self.skill_dir / "SKILL.md").write_text(
            f"---\nname: demo-skill\ndescription: {D0}\n---\n# Demo\n", encoding="utf-8"
        )
        train, test = split_eval_set(EVAL_SET, 0.4)
        self.train_should = [e["query"] for e in train if e["should_trigger"]]
        self.test_should = next(e["query"] for e in test if e["should_trigger"])
        self.test_should_not = next(e["query"] for e in test if not e["should_trigger"])

    def run_with(self, picks, improvements, holdout=0.4, max_iterations=3, **extra):
        improve_calls = []
        proposals = list(improvements)

        def fake_improve(
            skill_name,
            skill_content,
            current_description,
            eval_results,
            history,
            model,
            test_results=None,
            log_dir=None,
            iteration=None,
            harness_name="claude",
        ):
            improve_calls.append(
                {
                    "current": current_description,
                    "eval_results": eval_results,
                    "history": history,
                    "iteration": iteration,
                    "log_dir": log_dir,
                    "test_results": test_results,
                }
            )
            return proposals.pop(0)

        with mock.patch.object(loop_module, "run_eval", fake_run_eval_for(picks)), mock.patch.object(
            loop_module, "improve_description", fake_improve
        ):
            result = run_loop(
                EVAL_SET,
                self.skill_dir,
                None,
                num_workers=1,
                timeout=5,
                max_iterations=max_iterations,
                runs_per_query=RUNS,
                trigger_threshold=0.5,
                holdout=holdout,
                model="model-x",
                verbose=False,
                **extra,
            )
        return result, improve_calls

    def test_stops_when_all_train_queries_pass(self):
        result, calls = self.run_with({D0: all_should_picked()}, [])
        self.assertEqual(result["exit_reason"], "all_passed (iteration 1)")
        self.assertEqual(calls, [])
        self.assertEqual(result["iterations_run"], 1)
        self.assertEqual(result["original_description"], D0)
        self.assertEqual(result["best_description"], D0)
        self.assertEqual(result["final_description"], D0)
        self.assertEqual(result["best_score"], "2/2")
        self.assertEqual(result["best_train_score"], "4/4")
        self.assertEqual(result["best_test_score"], "2/2")
        self.assertEqual((result["train_size"], result["test_size"]), (4, 2))
        self.assertAlmostEqual(result["holdout"], 0.4)
        entry = result["history"][0]
        self.assertEqual(entry["iteration"], 1)
        self.assertEqual((entry["train_passed"], entry["train_failed"], entry["train_total"]), (4, 0, 4))
        self.assertEqual((entry["test_passed"], entry["test_failed"], entry["test_total"]), (2, 0, 2))
        self.assertEqual((entry["passed"], entry["failed"], entry["total"]), (4, 0, 4))
        self.assertEqual(entry["results"], entry["train_results"])
        self.assertEqual(len(entry["test_results"]), 2)

    def test_stops_at_iteration_limit(self):
        failing = all_should_picked(**{self.train_should[0]: 0})
        result, calls = self.run_with({D0: failing, D1: failing}, [D1], max_iterations=2)
        self.assertEqual(result["exit_reason"], "max_iterations (2)")
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0]["iteration"], 1)
        self.assertEqual(calls[0]["current"], D0)
        self.assertEqual(result["iterations_run"], 2)
        self.assertEqual(result["final_description"], D1)
        self.assertEqual([e["description"] for e in result["history"]], [D0, D1])

    def test_best_iteration_by_test_score(self):
        broken_train = {self.train_should[0]: 0}
        picks = {
            D0: all_should_picked(**broken_train, **{self.test_should: 0}),
            D1: all_should_picked(**broken_train),
            D2: all_should_picked(**broken_train, **{self.test_should: 0, self.test_should_not: RUNS}),
        }
        result, _ = self.run_with(picks, [D1, D2])
        self.assertEqual(result["exit_reason"], "max_iterations (3)")
        self.assertEqual(result["best_description"], D1)
        self.assertEqual(result["best_score"], "2/2")
        self.assertEqual(result["best_test_score"], "2/2")
        self.assertEqual(result["best_train_score"], "3/4")
        self.assertEqual(result["final_description"], D2)

    def test_best_iteration_tie_goes_to_earliest(self):
        broken_train = {self.train_should[0]: 0}
        picks = {
            D0: all_should_picked(**broken_train),
            D1: all_should_picked(**broken_train),
            D2: all_should_picked(**broken_train, **{self.test_should: 0}),
        }
        result, _ = self.run_with(picks, [D1, D2])
        self.assertEqual(result["best_description"], D0)
        self.assertEqual(result["best_score"], "2/2")

    def test_without_holdout_best_is_by_train_score(self):
        picks = {
            D0: all_should_picked(s1=0, n1=RUNS),
            D1: all_should_picked(s1=0),
        }
        result, calls = self.run_with(picks, [D1], holdout=0, max_iterations=2)
        self.assertEqual((result["train_size"], result["test_size"]), (6, 0))
        self.assertEqual(result["best_description"], D1)
        self.assertEqual(result["best_score"], "5/6")
        self.assertEqual(result["best_train_score"], "5/6")
        self.assertIsNone(result["best_test_score"])
        entry = result["history"][0]
        self.assertEqual(entry["train_passed"], 4)
        self.assertIsNone(entry["test_passed"])
        self.assertIsNone(entry["test_total"])
        self.assertIsNone(entry["test_results"])
        self.assertEqual(len(calls), 1)

    def test_history_given_to_improver_is_blinded(self):
        broken_train = {self.train_should[0]: 0}
        picks = {
            D0: all_should_picked(**broken_train),
            D1: all_should_picked(**broken_train),
            D2: all_should_picked(**broken_train),
        }
        result, calls = self.run_with(picks, [D1, D2], max_iterations=3)
        self.assertEqual(len(calls), 2)
        blinded = calls[1]["history"]
        self.assertEqual(len(blinded), 2)
        for entry in blinded:
            self.assertFalse([k for k in entry if k.startswith("test_")], entry.keys())
            self.assertIn("train_passed", entry)
            self.assertIn("results", entry)
        self.assertIsNone(calls[1]["test_results"])
        train_queries = {r["query"] for r in calls[1]["eval_results"]["results"]}
        self.assertNotIn(self.test_should, train_queries)
        self.assertNotIn(self.test_should_not, train_queries)
        self.assertEqual(calls[1]["eval_results"]["summary"]["total"], 4)
        # The real history still carries the held-out results.
        self.assertEqual(result["history"][0]["test_total"], 2)

    def test_live_report_and_log_dir_are_passed_through(self):
        report = self.work / "live.html"
        log_dir = self.work / "logs"
        picks = {D0: all_should_picked(**{self.train_should[0]: 0})}
        result, calls = self.run_with(
            {**picks, D1: all_should_picked()},
            [D1],
            live_report_path=report,
            log_dir=log_dir,
        )
        self.assertEqual(result["exit_reason"], "all_passed (iteration 2)")
        page = report.read_text(encoding="utf-8")
        self.assertIn('http-equiv="refresh"', page)
        self.assertIn("demo-skill", page)
        self.assertEqual(calls[0]["log_dir"], log_dir)

    def test_description_override_is_the_starting_point(self):
        with mock.patch.object(loop_module, "run_eval", fake_run_eval_for({D1: all_should_picked()})):
            result = run_loop(
                EVAL_SET,
                self.skill_dir,
                D1,
                num_workers=1,
                timeout=5,
                max_iterations=1,
                runs_per_query=RUNS,
                trigger_threshold=0.5,
                holdout=0.4,
                model="model-x",
                verbose=False,
            )
        self.assertEqual(result["original_description"], D1)


class HoldoutArgumentTests(unittest.TestCase):
    def test_accepts_zero_and_open_interval(self):
        self.assertEqual(holdout_fraction("0"), 0.0)
        self.assertAlmostEqual(holdout_fraction("0.4"), 0.4)
        self.assertAlmostEqual(holdout_fraction("0.999"), 0.999)

    def test_rejects_other_values(self):
        for bad in ("1", "1.5", "-0.1", "abc"):
            with self.subTest(value=bad), self.assertRaises(argparse.ArgumentTypeError):
                holdout_fraction(bad)


if __name__ == "__main__":
    unittest.main()
