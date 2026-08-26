import unittest
from pathlib import Path

TEMPLATES = Path(__file__).resolve().parents[1] / "templates" / "chatgpt"


class SourceAccountingTests(unittest.TestCase):
    def test_expected_sources_require_destination_controls(self):
        expectations = {
            "PublicWebMentions.md": (
                "Count a selected source as expected only after its initial URL "
                "passes the pre-navigation destination controls."
            ),
            "SocialPIIExposure.md": (
                "Count a discovered source as expected only after its initial URL "
                "passes the pre-navigation destination controls."
            ),
        }

        for name, expected_accounting in expectations.items():
            with self.subTest(template=name):
                template = (TEMPLATES / name).read_text(encoding="utf-8")
                controls = template.index("## Destination controls")
                accounting = template.index(expected_accounting)
                inspection = template.index("Inspect each expected source")

                self.assertLess(controls, accounting)
                self.assertLess(accounting, inspection)


if __name__ == "__main__":
    unittest.main()
