"""The fallback term scripts accept the valid fixture, report each of the
five findings on the invalid one, and the fixers migrate the legacy tree
and add a draft term, idempotently (CORE-0007). The fixtures under
tests/fixtures/terms/ carry their own ontology and glossary pages, so no
test touches the repository's own tree or delegates to rune."""
import re
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


LINKED_ONTOLOGY = "@prefix rune: <https://runedeck.ai/ns#> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n\n" + "".join(
    f'rune:{name} a rdfs:Class ;\n    rdfs:label "{label}" ;\n    rdfs:comment "The {label}." .\n\n'
    for name, label in (("Harness", "harness"), ("Rule", "rule"), ("Requirement", "requirement"), ("MissedRequirement", "missed requirement"), ("RedReview", "red review"), ("ReviewLane", "review lane"), ("Capability", "capability"))
)
PAGE = {"HARNESS": "harness", "RULE": "rule", "REQUIREMENT": "requirement", "MISSEDREQUIREMENT": "missed-requirement", "REDREVIEW": "red-review", "REVIEWLANE": "review-lane", "CAPABILITY": "capability"}


def definitions(*tags):
    return "\n" + "".join(f"[{tag}]: ../specs/glossary/{PAGE[tag]}.md\n" for tag in tags)


FIRST = "*[harness][HARNESS]* first.\n\n"
HARNESS = definitions("HARNESS")
# One file per case: the body, and the plain words the checker reports in it.
UNLINKED = {
    "line-edges": (FIRST + "harness works.\nThe harness\n" + HARNESS, ["harness", "harness"]),
    "es-plural": (FIRST + "Two harnesses work.\n" + HARNESS, ["harnesses"]),
    "ies-plural": ("A *[capability][CAPABILITY]* here. Two capabilities, no capabilitys.\n\n[CAPABILITY]: ../specs/glossary/capability.md\n", ["capabilities"]),
    "bare-url": (FIRST + "See https://example.com/harness and <https://x/harness> and <a href=\"harness\">x</a>, then a harness.\n" + HARNESS, ["harness"]),
    # An emphasized word is a run-in label (`**Change ceremony.**`) and stays plain, as in rune.
    "italic-word": (FIRST + "A later *harness* here.\n" + HARNESS, []),
    "legacy-citation": (FIRST + "A *harness* [HARNESS] cite.\n" + HARNESS, []),
    "fences": (FIRST + "~~~md\nThe harness works.\n~~~~\n\n  ```\n  The harness works.\n  ```\n" + HARNESS, []),
    "unclosed-fence": (HARNESS + "\n" + FIRST + "```\nThe harness works.\n", []),
    "code-spans": (FIRST + "Use ``the harness`` and ``a `harness` b`` here.\n" + HARNESS, []),
    "destinations": (FIRST + "See [record](path(foo)harness) and [record](a]harness) now.\n" + HARNESS, []),
    "setext-heading": (FIRST + "The harness guide\n=================\n" + HARNESS, []),
    "definition-label": (FIRST + "[MORE INFO]: ./harness.md\n" + HARNESS, []),
    "titled-definition": (FIRST + "A plain harness.\n\n[HARNESS]: ../specs/glossary/harness.md \"title\"\n", ["harness"]),
    "definition-only": ("The harness works.\n" + HARNESS, []),
    "legacy-definition-only": ("The harness works.\n\n[HARNESS]: https://runedeck.ai/ns#Harness\n", []),
    "longer-term": ("*[requirement][REQUIREMENT]* and *[missed requirement][MISSEDREQUIREMENT]*.\n\nA missed requirement remains.\n" + definitions("REQUIREMENT", "MISSEDREQUIREMENT"), ["missed requirement"]),
}
OWN_TAG = "\n[OTHER]: ../specs/glossary/harness.md\n[HARNESS]: ../specs/glossary/harness.md\n"
LANES = definitions("REDREVIEW", "REVIEWLANE")
RULE = definitions("RULE")
# One file per case: the body, and the text after `fix-terms --links`.
FIXED = {
    "dotted-capital": (FIRST + "The İ harness works.\n" + HARNESS, FIRST + "The İ [harness][HARNESS] works.\n" + HARNESS),
    "own-tag": (FIRST + "A plain harness.\n" + OWN_TAG, FIRST + "A plain [harness][HARNESS].\n" + OWN_TAG),
    "later-longer-term": ("*[red review][REDREVIEW]* and *[review lane][REVIEWLANE]*.\n\nThe red review lane runs.\n" + LANES, "*[red review][REDREVIEW]* and *[review lane][REVIEWLANE]*.\n\nThe red [review lane][REVIEWLANE] runs.\n" + LANES),
    "first-use-moves": ("A rule governs. Then *[rule][RULE]* follows.\n" + RULE, "A *[rule][RULE]* governs. Then [rule][RULE] follows.\n" + RULE),
    "italic-later-use": (FIRST + "A later *harness* here.\n" + HARNESS, FIRST + "A later *harness* here.\n" + HARNESS),
}
UNLINKED_LINE = re.compile(r"^error\[term-unlinked\]: docs/notes/([^:]+)\.md:\d+: '([^']*)'", re.MULTILINE)


def unlinked_words(output, name):
    return [word for file, word in UNLINKED_LINE.findall(output) if file == name]


class LinkedTermOccurrences(unittest.TestCase):
    """Every plain occurrence of a term a file links is a link. The checker
    finds one at a line edge, as an `es` plural, and in italics, and never
    in code, a heading, a definition, a legacy citation, or a link
    destination. The fixer links the longer term first and keeps the
    emphasis on the first use. Each case is one file of a scratch deck."""

    @staticmethod
    def deck(scratch, cases, missing=()):
        root = Path(scratch) / "deck"
        (root / "ontology").mkdir(parents=True)
        (root / termlib.ONTOLOGY).write_text(LINKED_ONTOLOGY)
        glossary = root / termlib.GLOSSARY
        glossary.mkdir(parents=True)
        for name, text in termlib.load(root).render().items():
            if name not in missing:
                (glossary / name).write_text(text)
        notes = root / "docs" / "notes"
        notes.mkdir(parents=True)
        for name, body in cases.items():
            (notes / f"{name}.md").write_text(body)
        return root, notes

    def test_checker_reports_each_plain_occurrence_once(self):
        with tempfile.TemporaryDirectory() as scratch:
            root, _ = self.deck(scratch, {name: body for name, (body, _) in UNLINKED.items()})
            result = run("check-terms", root)
            self.assertEqual(result.stderr, "", "a check that crashes is not a finding")
            for name, (_, words) in UNLINKED.items():
                with self.subTest(name):
                    self.assertEqual(unlinked_words(result.stdout, name), words, result.stdout)

    def test_checker_suggests_the_tag_the_file_uses(self):
        with tempfile.TemporaryDirectory() as scratch:
            root, _ = self.deck(scratch, {"own-tag": FIXED["own-tag"][0]})
            result = run("check-terms", root)
            self.assertIn("write `[harness][HARNESS]`", result.stdout)

    def test_fixer_links_once_and_moves_the_emphasis(self):
        cases = {name: body for name, (body, _) in {**UNLINKED, **FIXED}.items()}
        with tempfile.TemporaryDirectory() as scratch:
            root, notes = self.deck(scratch, cases)
            result = run("fix-terms", "--links", root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            for name, (_, expected) in FIXED.items():
                with self.subTest(name):
                    self.assertEqual((notes / f"{name}.md").read_text(), expected)
            for name, (body, words) in UNLINKED.items():
                if not words and name != "legacy-definition-only":
                    with self.subTest(name):
                        self.assertEqual((notes / f"{name}.md").read_text(), body, "nothing to link, so nothing changes")
            check = run("check-terms", root)
            self.assertNotIn("term-unlinked", check.stdout)
            self.assertNotIn("term-first-use", check.stdout)
            again = run("fix-terms", "--links", root)
            self.assertIn("links: 0 files rewritten", again.stdout)

    def test_a_migrated_link_to_a_missing_page_keeps_its_term(self):
        body = "A *rule* [CUSTOM] governs. Another rule follows.\n\n[CUSTOM]: https://runedeck.ai/ns#Rule\n"
        with tempfile.TemporaryDirectory() as scratch:
            root, notes = self.deck(scratch, {"custom-tag": body}, missing={"rule.md"})
            result = run("fix-terms", "--links", root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual((notes / "custom-tag.md").read_text(), "A *[rule][CUSTOM]* governs. Another [rule][CUSTOM] follows.\n\n[CUSTOM]: ../specs/glossary/rule.md\n")


if __name__ == "__main__":
    unittest.main()
