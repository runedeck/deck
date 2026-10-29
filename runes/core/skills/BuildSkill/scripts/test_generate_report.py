"""Tests for the HTML report renderer."""

import unittest

from scripts.generate_report import best_iteration_index, generate_html


def query_result(query: str, should_trigger: bool, triggers: int, runs: int = 3) -> dict:
    rate = triggers / runs
    passed = rate >= 0.5 if should_trigger else rate < 0.5
    return {
        "query": query,
        "should_trigger": should_trigger,
        "trigger_rate": rate,
        "triggers": triggers,
        "runs": runs,
        "pass": passed,
    }


def entry(iteration: int, description: str, train: list[dict], test: list[dict] | None = None) -> dict:
    train_passed = sum(1 for r in train if r["pass"])
    data = {
        "iteration": iteration,
        "description": description,
        "train_passed": train_passed,
        "train_failed": len(train) - train_passed,
        "train_total": len(train),
        "train_results": train,
        "test_passed": None,
        "test_failed": None,
        "test_total": None,
        "test_results": None,
        "passed": train_passed,
        "failed": len(train) - train_passed,
        "total": len(train),
        "results": train,
    }
    if test is not None:
        test_passed = sum(1 for r in test if r["pass"])
        data.update(
            {
                "test_passed": test_passed,
                "test_failed": len(test) - test_passed,
                "test_total": len(test),
                "test_results": test,
            }
        )
    return data


def best_row(page: str) -> str:
    start = page.index('<tr class="iteration best">')
    return page[start : page.index("</tr>", start)]


class GenerateHtmlTests(unittest.TestCase):
    def test_escapes_every_data_value(self):
        hostile_description = "<script>alert('x')</script>"
        hostile_query = '<img src=x onerror="steal()">'
        data = {
            "original_description": "a & b <i>",
            "best_description": hostile_description,
            "best_score": "1/1",
            "iterations_run": 1,
            "train_size": 1,
            "test_size": 0,
            "history": [
                entry(1, hostile_description, [query_result(hostile_query, True, 3)])
            ],
        }
        page = generate_html(data, skill_name="<b>name</b>")
        self.assertNotIn(hostile_description, page)
        self.assertNotIn(hostile_query, page)
        self.assertNotIn("<b>name</b>", page)
        self.assertIn("&lt;script&gt;", page)
        self.assertIn("&lt;img src=x", page)
        self.assertIn("a &amp; b &lt;i&gt;", page)
        self.assertIn("&lt;b&gt;name&lt;/b&gt;", page)

    def test_best_row_highlight_by_test_score(self):
        train = [query_result("t1", True, 3)]
        history = [
            entry(1, "first description", train, [query_result("h1", True, 3), query_result("h2", False, 3)]),
            entry(2, "second description", train, [query_result("h1", True, 3), query_result("h2", False, 0)]),
        ]
        page = generate_html({"history": history, "best_score": "2/2", "test_size": 2, "train_size": 1})
        self.assertEqual(page.count('<tr class="iteration best">'), 1)
        self.assertIn("second description", best_row(page))
        self.assertEqual(best_iteration_index(history), 1)
        self.assertIn("Best score (test)", page)

    def test_best_row_tie_goes_to_earliest_and_train_rule_without_test(self):
        history = [
            entry(1, "first description", [query_result("t1", True, 3), query_result("t2", False, 3)]),
            entry(2, "second description", [query_result("t1", True, 3), query_result("t2", False, 3)]),
            entry(3, "third description", [query_result("t1", True, 0), query_result("t2", False, 3)]),
        ]
        page = generate_html({"history": history, "test_size": 0, "train_size": 2})
        self.assertEqual(page.count('<tr class="iteration best">'), 1)
        self.assertIn("first description", best_row(page))
        self.assertEqual(best_iteration_index(history), 0)
        self.assertIn("Best score (train)", page)

    def test_older_history_keys_are_accepted(self):
        history = [
            {
                "iteration": 1,
                "description": "legacy entry",
                "passed": 1,
                "total": 2,
                "results": [
                    query_result("legacy query one", True, 2),
                    query_result("legacy query two", False, 1),
                ],
            }
        ]
        page = generate_html({"history": history})
        self.assertIn("legacy entry", page)
        self.assertIn("legacy query one", page)
        self.assertIn("4/6", page)
        self.assertIn('<tr class="iteration best">', page)
        self.assertEqual(best_iteration_index(history), 0)

    def test_auto_refresh_and_title(self):
        data = {"history": []}
        with_refresh = generate_html(data, auto_refresh=True, skill_name="demo-skill")
        self.assertIn('<meta http-equiv="refresh" content="5">', with_refresh)
        self.assertIn("<title>Trigger optimization report: demo-skill</title>", with_refresh)
        without = generate_html(data, auto_refresh=False)
        self.assertNotIn('http-equiv="refresh"', without)
        self.assertNotIn("<script", without.lower())
        self.assertNotIn("http://", without)
        self.assertNotIn("https://", without)

    def test_score_grades_and_query_headers(self):
        history = [
            entry(
                1,
                "d",
                [query_result("yes-q", True, 3), query_result("no-q", False, 0)],
                [query_result("held", True, 1)],
            )
        ]
        page = generate_html({"history": history, "test_size": 1, "train_size": 2})
        self.assertIn('class="score good"', page)
        self.assertIn('class="score poor"', page)
        self.assertIn("should NOT trigger", page)
        self.assertIn('class="query test', page)
        self.assertIn('class="query train', page)
        self.assertIn("✓ 3/3", page)
        self.assertIn("✗ 1/3", page)


if __name__ == "__main__":
    unittest.main()
