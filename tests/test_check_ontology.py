import importlib.machinery
import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "check-ontology"
LOADER = importlib.machinery.SourceFileLoader("check_ontology", str(SCRIPT))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
CHECK = importlib.util.module_from_spec(SPEC)
LOADER.exec_module(CHECK)

SH = "http://www.w3.org/ns/shacl#"
REPORT = f"""_:1 <{SH}conforms> "false"^^<http://www.w3.org/2001/XMLSchema#boolean> .
_:2 <{SH}focusNode> <https://runedeck.ai/id/DECK-0002> .
_:2 <{SH}resultSeverity> <{SH}Violation> .
_:2 <{SH}resultPath> <http://purl.org/dc/terms/title> .
_:2 <{SH}resultMessage> "Two records share one identifier." .
_:2 <{SH}sourceConstraintComponent> <{SH}MaxCountConstraintComponent> .
_:3 <{SH}resultSeverity> <{SH}Warning> .
_:3 <{SH}focusNode> <https://runedeck.ai/id/UseEfficientCLI> .
_:3 <{SH}resultPath> <https://runedeck.ai/ns#verdict> .
_:3 <{SH}resultMessage> "A rule carries no bench verdict pointer. Run \\"BenchArtifact\\"." .
_:3 <{SH}sourceConstraintComponent> <{SH}MinCountConstraintComponent> .
"""


class ParseTests(unittest.TestCase):
    def test_findings_are_named_and_sorted(self):
        found = CHECK.parse(REPORT)
        self.assertEqual(
            [tuple(f) for f in found],
            [
                ("Violation", "DECK-0002", "title", "MaxCount", "Two records share one identifier."),
                ("Warning", "UseEfficientCLI", "verdict", "MinCount",
                 'A rule carries no bench verdict pointer. Run \\"BenchArtifact\\".'),
            ],
        )

    def test_report_without_results_is_empty(self):
        self.assertEqual(CHECK.parse(REPORT.splitlines()[0]), [])

    def test_short_takes_the_local_name(self):
        self.assertEqual(CHECK.short("https://runedeck.ai/ns#status"), "status")
        self.assertEqual(CHECK.short("https://runedeck.ai/id/DECK-0001"), "DECK-0001")
        self.assertEqual(CHECK.short(""), "-")


if __name__ == "__main__":
    unittest.main()
