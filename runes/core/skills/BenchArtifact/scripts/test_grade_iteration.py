import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("grade_iteration.py")
SPEC = importlib.util.spec_from_file_location("grade_iteration", SCRIPT)
GRADE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GRADE)


class GradeIterationTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
