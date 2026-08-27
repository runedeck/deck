import unittest
from pathlib import Path

TEMPLATES = Path(__file__).resolve().parents[1] / "templates" / "chatgpt"


class SourceAccountingTests(unittest.TestCase):
    def test_expected_sources_require_destination_controls(self):
        expectations = {
            "PublicWebMentions.md": (
                (
                    "Count a selected source as expected only after its initial URL "
                    "passes the pre-navigation destination controls."
                ),
                (
                    "Record a selected source that fails its initial destination "
                    "controls as a policy exclusion in Limits."
                ),
            ),
            "SocialPIIExposure.md": (
                (
                    "Count a discovered source as expected only after its initial URL "
                    "passes the pre-navigation destination controls."
                ),
                (
                    "Record a discovered source that fails its initial destination "
                    "controls as a policy exclusion in Limits."
                ),
            ),
        }

        for name, (expected_accounting, policy_exclusion) in expectations.items():
            with self.subTest(template=name):
                template = (TEMPLATES / name).read_text(encoding="utf-8")
                controls = template.index("## Destination controls")
                exclusion = template.index(policy_exclusion)
                redirect_failure = template.index(
                    "If a redirect destination fails a control for an expected "
                    "source, stop that source and report INCOMPLETE."
                )
                accounting = template.index(expected_accounting)
                inspection = template.index("Inspect each expected source")

                self.assertLess(controls, exclusion)
                self.assertLess(exclusion, accounting)
                self.assertLess(controls, redirect_failure)
                self.assertLess(controls, accounting)
                self.assertLess(accounting, inspection)

                self.assertIn(
                    "A source policy exclusion before expected-source accounting "
                    "does not cause INCOMPLETE.",
                    template,
                )
                self.assertIn(
                    "A redirect failure for an expected source causes INCOMPLETE.",
                    template,
                )
                self.assertNotIn(
                    "Report each blocked destination as INCOMPLETE.", template
                )
                self.assertNotIn(
                    "A stated policy exclusion does not cause INCOMPLETE.", template
                )


if __name__ == "__main__":
    unittest.main()
