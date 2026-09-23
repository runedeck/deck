"""The fallback term scripts accept the valid fixture, report each of the
five findings on the invalid one, and the fixers migrate the legacy tree
and add a draft term, idempotently (CORE-0007). The fixtures under
tests/fixtures/terms/ carry their own ontology and glossary pages, so no
test touches the repository's own tree or delegates to rune."""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FALLBACK = ROOT / "scripts" / "fallback"
FIXTURES = ROOT / "tests" / "fixtures" / "terms"
SPEC = Path("docs") / "changes" / "one-two-three" / "specs" / "thing" / "spec.md"

sys.path.insert(0, str(FALLBACK))
import termlib

DRAFT_PAGE = """---
title: ghost thing
iri: https://runedeck.ai/ns#GhostThing
kind: class
status: draft
---

# ghost thing

Draft term. The fixer added it and nobody has defined it yet. Archive refuses a change that links to it.

Generated from `ontology/rune.ttl`. Edit the ontology, not this page.
"""


def run(script, *args):
    return subprocess.run(["python3", str(FALLBACK / script), *map(str, args)], capture_output=True, text=True, check=False)


def names(output):
    return {line.split("[", 1)[1].split("]", 1)[0] for line in output.splitlines() if line.startswith(("error[", "warning["))}


class TermModel(unittest.TestCase):
    def test_page_names_and_tags(self):
        self.assertEqual(termlib.kebab("Occam's razor"), "occams-razor")
        self.assertEqual(termlib.kebab("analysis tool"), "analysis-tool")
        self.assertEqual(termlib.tag_of("Occam's razor"), "OCCAMSRAZOR")
        self.assertEqual(termlib.camel("ghost thing"), "GhostThing")
        index = termlib.load(FIXTURES / "valid")
        self.assertEqual(index.file_of["Change"], "change.md")
        self.assertEqual(index.file_of["change"], "change-key.md")
        self.assertEqual(index.tag_of["change"], "CHANGE-KEY")
        self.assertEqual(index.by_tag["ANALYSISTOOL"], "AnalysisTool")

    def test_draft_page_bytes(self):
        index = termlib.load(FIXTURES / "invalid")
        self.assertEqual(index.page(index.by_name["GhostThing"]), DRAFT_PAGE)
        self.assertIn("- [ghost thing](ghost-thing.md): Draft term.", index.index())

    def test_defined_page_bytes(self):
        index = termlib.load(FIXTURES / "valid")
        page = index.page(index.by_name["OccamsRazor"])
        self.assertTrue(page.startswith("---\ntitle: Occam's razor\niri: https://runedeck.ai/ns#OccamsRazor\nkind: concept\nstatus: defined\n---\n\n# Occam's razor\n\nOf two"))
        self.assertTrue(page.endswith("wins.\n\nGenerated from `ontology/rune.ttl`. Edit the ontology, not this page.\n"))
        self.assertEqual(index.index().splitlines()[0], "# Glossary")
        self.assertEqual([line[3:].split("]")[0] for line in index.index().splitlines()[4:]], ["Occam's razor", "analysis tool", "change", "change"])


class CheckTerms(unittest.TestCase):
    def test_valid_fixture_passes(self):
        result = run("check-terms", FIXTURES / "valid")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(names(result.stdout), set())

    def test_invalid_fixture_reports_each_finding(self):
        result = run("check-terms", FIXTURES / "invalid")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertEqual(result.stderr, "", "a check that crashes is not a finding")
        self.assertEqual(names(result.stdout), {"term-undefined", "term-draft", "term-first-use", "term-page", "term-legacy"})
        self.assertEqual(result.stdout.count("term-first-use"), 2, result.stdout)
        self.assertIn("analysis-tool.md differs from the ontology", result.stdout)
        self.assertIn("occams-razor.md is missing", result.stdout)
        self.assertIn("warning[term-legacy]", result.stdout)
        self.assertIn("warning[term-draft]", result.stdout)


class GenerateGlossary(unittest.TestCase):
    def test_check_passes_on_current_pages(self):
        result = run("generate-glossary", "--check", FIXTURES / "valid")
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_check_names_the_drifted_and_missing_pages(self):
        result = run("generate-glossary", "--check", FIXTURES / "invalid")
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("analysis-tool.md: differs from the ontology", result.stdout)
        self.assertIn("occams-razor.md: missing", result.stdout)

    def test_write_then_check_round_trips_and_reports_stale(self):
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch) / "deck"
            shutil.copytree(FIXTURES / "legacy", root)
            (root / termlib.SINGLE_FILE).write_text("# Glossary\n")
            (root / termlib.GLOSSARY / "gone.md").write_text("stale\n")
            result = run("generate-glossary", root)
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertIn("stale: docs/specs/glossary.md", result.stdout)
            self.assertIn("stale: docs/specs/glossary/gone.md", result.stdout)
            result = run("generate-glossary", "--check", root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("glossary.md: stale", result.stdout)


class FixTerms(unittest.TestCase):
    def copy(self, scratch):
        root = Path(scratch) / "deck"
        shutil.copytree(FIXTURES / "legacy", root)
        return root

    def test_links_migrates_the_legacy_form_once(self):
        with tempfile.TemporaryDirectory() as scratch:
            root = self.copy(scratch)
            result = run("fix-terms", "--links", root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            text = (root / SPEC).read_text()
            self.assertIn("An *[analysis tool][ANALYSISTOOL]* reads", text)
            self.assertIn("A second [analysis tool][ANALYSISTOOL] citation", text)
            self.assertIn("By *[Occam's razor][OCCAMSRAZOR]*,", text)
            self.assertIn("its *[change][CHANGE-KEY]*.", text)
            self.assertIn("`*analysis tool* [ANALYSISTOOL]`", text, "a code span is never rewritten")
            self.assertIn("[ANALYSISTOOL]: ../../../../specs/glossary/analysis-tool.md", text)
            self.assertIn("[CHANGE-KEY]: ../../../../specs/glossary/change-key.md", text)
            self.assertIn("[GHOST]: https://runedeck.ai/ns#Ghost", text, "an unknown term is left for a person")
            self.assertIn("not a labeled term", result.stdout)
            again = run("fix-terms", "--links", root)
            self.assertEqual((root / SPEC).read_text(), text, again.stdout)
            self.assertIn("links: 0 files rewritten", again.stdout)
            check = run("check-terms", root)
            self.assertNotIn("term-legacy", check.stdout)
            self.assertNotIn("term-first-use", check.stdout)

    def test_terms_adds_a_draft_and_its_page(self):
        with tempfile.TemporaryDirectory() as scratch:
            root = self.copy(scratch)
            result = run("fix-terms", "--terms", root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("terms: added draft rune:GhostThing", result.stdout)
            ontology = (root / termlib.ONTOLOGY).read_text()
            self.assertIn('rune:GhostThing a rdfs:Class ;\n    rdfs:label "ghost thing" ;\n    rune:status "draft" .\n', ontology)
            self.assertEqual(ontology.count("# Draft terms"), 1)
            self.assertEqual((root / termlib.GLOSSARY / "ghost-thing.md").read_text(), DRAFT_PAGE)
            self.assertIn("- [ghost thing](ghost-thing.md): Draft term.", (root / termlib.GLOSSARY / "index.md").read_text())
            check = run("check-terms", root)
            self.assertIn("warning[term-draft]", check.stdout)
            self.assertNotIn("[GHOSTTHING] resolves to no ontology term", check.stdout)
            again = run("fix-terms", "--terms", root)
            self.assertIn("terms: 0 draft terms added", again.stdout)
            self.assertEqual((root / termlib.ONTOLOGY).read_text(), ontology)

    def test_both_fixes_leave_only_the_draft_warning_and_the_unknown_iri(self):
        with tempfile.TemporaryDirectory() as scratch:
            root = self.copy(scratch)
            result = run("fix-terms", root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            check = run("check-terms", root)
            self.assertEqual(names(check.stdout), {"term-draft", "term-undefined"}, check.stdout)
            self.assertIn("[GHOST] resolves to no ontology term", check.stdout)

    def test_unknown_flag_is_a_usage_error(self):
        self.assertEqual(run("fix-terms", "--bogus", FIXTURES / "legacy").returncode, 2)


if __name__ == "__main__":
    unittest.main()
