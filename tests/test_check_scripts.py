"""Each foundation check accepts its valid fixture and rejects its invalid
one, one rule at a time (CORE-0007). The fixtures under tests/fixtures/ are
the proof inputs the recorded scenes reuse. With REQUIRE_GATES set, a
missing Vale is a failure, never a skip."""
import os
import re
import shutil
import subprocess
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "tests" / "fixtures"
# RUNE_CHECK_OKF points the okf tests at another copy of the script, so a
# proof scene can show that a weakened rule fails the fixture test.
SCRIPTS = {
    "okf": Path(os.environ.get("RUNE_CHECK_OKF", ROOT / "scripts" / "check-okf")),
    "coverage": ROOT / "scripts" / "check-coverage",
    "fixtures": ROOT / "scripts" / "check-fixtures",
    "binary-assets": ROOT / "scripts" / "check-binary-assets",
}
STALE_QUEUE = ROOT / "scripts" / "check-stale-queue"
EXPECTED = {
    "okf": ("type: docs/record.md carries an empty type", "type: runes/core/rules/Rule.md carries an empty metadata.type", "id: docs/record.md carries id 'something-else'", "reserved: log.md carries a frontmatter block", "version: the bundle root index.md"),
    "coverage": ("no coverage row for one-two-three / Thing Is Checked", "names no stated requirement"),
    "fixtures": ("scripts/check-thing: no tests/fixtures/thing",),
    "binary-assets": ("binary: logo.png has no description beside it",),
}


def run(script, root, *extra):
    return subprocess.run(["python3", str(script), str(root), *extra], capture_output=True, text=True, check=False)


class FixtureVerdicts(unittest.TestCase):
    def test_valid_fixtures_pass(self):
        for name, script in SCRIPTS.items():
            with self.subTest(name):
                result = run(script, FIXTURES / name / "valid")
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("0 findings", result.stdout)

    def test_invalid_fixtures_fail_with_each_diagnostic(self):
        for name, script in SCRIPTS.items():
            with self.subTest(name):
                result = run(script, FIXTURES / name / "invalid")
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertEqual(result.stderr, "", "a check that crashes is not a finding")
                for diagnostic in EXPECTED[name]:
                    self.assertIn(diagnostic, result.stdout)

    def test_okf_names_every_rule(self):
        result = run(SCRIPTS["okf"], FIXTURES / "okf" / "invalid")
        for rule in ("type:", "id:", "reserved:", "version:"):
            self.assertIn(rule, result.stdout)

    def test_okf_type_is_optional_and_comes_from_key_or_schema(self):
        """Type On Every File: a key wins, the nearest directory schema that
        fixes one value supplies it otherwise, a schema whose block enum
        allows two values fixes none, and a file with neither is untyped
        and not a finding."""
        result = run(SCRIPTS["okf"], FIXTURES / "okf" / "valid", "--types")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        types = {line.split("\t")[0]: tuple(line.split("\t")[1:]) for line in result.stdout.splitlines()}
        self.assertEqual(types["docs/record.md"], ("adr", "schema"))
        self.assertEqual(types["runes/core/rules/Rule.md"], ("rule", "key"))
        self.assertEqual(types["notes/plain.md"], ("", "untyped"))
        self.assertEqual(types["guides/open.md"], ("", "untyped"))
        self.assertNotIn("index.md", types)

    def test_okf_version_is_a_warning_until_the_generator_lands(self):
        """Bundle Declares Its Version: a missing root index is printed as a
        warning and does not fail the check."""
        with tempfile.TemporaryDirectory() as scratch:
            (Path(scratch) / "note.md").write_text("# Note\n")
            result = run(SCRIPTS["okf"], scratch)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("warning: version: the bundle root index.md is missing", result.stdout)
            self.assertIn("0 findings", result.stdout)

    def test_baseline_hides_known_findings_only(self):
        with tempfile.TemporaryDirectory() as scratch:
            baseline = Path(scratch) / "okf.txt"
            known = run(SCRIPTS["okf"], FIXTURES / "okf" / "invalid").stdout.splitlines()[:-1]
            baseline.write_text("\n".join(known) + "\n")
            result = run(SCRIPTS["okf"], FIXTURES / "okf" / "invalid", "--baseline", str(baseline))
            self.assertEqual(result.returncode, 0, result.stdout)
            baseline.write_text("\n".join(known[1:]) + "\n")
            result = run(SCRIPTS["okf"], FIXTURES / "okf" / "invalid", "--baseline", str(baseline))
            self.assertEqual(result.returncode, 1)

    def test_missing_root_is_a_finding(self):
        result = run(SCRIPTS["binary-assets"], FIXTURES / "binary-assets" / "absent")
        self.assertEqual(result.returncode, 1)


AGE = re.compile(r"^age_days:\s*(\d+)\s*$", re.MULTILINE)


# Hermetic git: the owner's global config signs every commit with a key
# the test must not touch, so the global and system configs are empty.
GIT_ENV = {**os.environ, "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_SYSTEM": os.devnull, "GIT_AUTHOR_NAME": "fixture", "GIT_AUTHOR_EMAIL": "fixture@example.org", "GIT_COMMITTER_NAME": "fixture", "GIT_COMMITTER_EMAIL": "fixture@example.org"}


def git_repo(scratch):
    repo = Path(scratch)
    subprocess.run(["git", "init", "-q", str(repo)], check=True, env=GIT_ENV)
    return repo


def git_dated(repo, days, *args):
    """Run git in the repository with author and committer dates `days` in the past."""
    stamp = f"{int(time.time()) - days * 86400} +0000"
    dated = {**GIT_ENV, "GIT_AUTHOR_DATE": stamp, "GIT_COMMITTER_DATE": stamp}
    subprocess.run(["git", "-C", str(repo), *args], check=True, env=dated, capture_output=True)


def commit_fixture_repo(fixture, scratch, under=""):
    """Build a git repository under scratch from a stale-queue fixture tree,
    placed under the `under` prefix. Each file is committed on its own with
    author and committer dates `age_days` in the past, because
    check-stale-queue reads the age of a queue item from the commit that
    added it at its queue path."""
    repo = git_repo(scratch)
    for source in sorted(p for p in fixture.rglob("*.md") if p.is_file()):
        rel = Path(under) / source.relative_to(fixture)
        target = repo / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        days = int(AGE.search(source.read_text()).group(1))
        git_dated(repo, days, "add", "--", rel.as_posix())
        git_dated(repo, days, "commit", "-q", "--no-verify", "-m", f"add {rel.as_posix()}")
    return repo


class StaleQueue(unittest.TestCase):
    """Catch-All Directories Drain: an item in a queue directory is stale
    from day sixty and an error from day sixty-seven, the unsorted archive
    never ages, a file outside a queue is never aged, and the age counts
    the stay at the queue path."""

    def test_valid_fixture_passes_and_names_the_stale_items(self):
        with tempfile.TemporaryDirectory() as scratch:
            repo = commit_fixture_repo(FIXTURES / "stale-queue" / "valid", scratch)
            result = run(STALE_QUEUE, repo)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(result.stderr, "")
            self.assertIn("stale: downloads/aging.md has waited 62 days", result.stdout)
            self.assertIn("stale: inbox/sixty.md has waited 60 days", result.stdout)
            self.assertNotIn("fresh.md", result.stdout)
            self.assertNotIn("ancient.md", result.stdout)
            self.assertNotIn("note.md", result.stdout)
            self.assertIn("stale-queue: 2 stale, 0 errors", result.stdout)

    def test_invalid_fixture_fails_on_the_old_items(self):
        with tempfile.TemporaryDirectory() as scratch:
            repo = commit_fixture_repo(FIXTURES / "stale-queue" / "invalid", scratch)
            result = run(STALE_QUEUE, repo)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("error: inbox/old.md has waited 70 days (error from day 67)", result.stdout)
            self.assertIn("error: downloads/sixty-seven.md has waited 67 days", result.stdout)
            self.assertIn("stale: temp/aging.md has waited 62 days", result.stdout)
            self.assertIn("stale-queue: 1 stale, 2 errors", result.stdout)

    def test_fixtures_of_the_check_never_age(self):
        """The fixture tree committed under tests/fixtures/ is outside the
        check, so the repository that holds it stays green past day sixty-seven."""
        with tempfile.TemporaryDirectory() as scratch:
            repo = commit_fixture_repo(FIXTURES / "stale-queue" / "invalid", scratch, "tests/fixtures/stale-queue/invalid")
            result = run(STALE_QUEUE, repo)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("stale-queue: 0 stale, 0 errors", result.stdout)

    def test_move_into_a_queue_starts_the_clock(self):
        """An old file moved into inbox yesterday is fresh: the age counts
        the stay at the queue path, not the file's first commit elsewhere."""
        with tempfile.TemporaryDirectory() as scratch:
            repo = git_repo(scratch)
            (repo / "docs").mkdir()
            (repo / "docs" / "moved.md").write_text("# Moved\n")
            git_dated(repo, 100, "add", "--", "docs/moved.md")
            git_dated(repo, 100, "commit", "-q", "--no-verify", "-m", "add docs/moved.md")
            (repo / "inbox").mkdir()
            git_dated(repo, 1, "mv", "docs/moved.md", "inbox/moved.md")
            git_dated(repo, 1, "commit", "-q", "--no-verify", "-m", "move into inbox")
            result = run(STALE_QUEUE, repo)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("stale-queue: 0 stale, 0 errors", result.stdout)

    def test_extra_queue_name_is_aged(self):
        with tempfile.TemporaryDirectory() as scratch:
            repo = commit_fixture_repo(FIXTURES / "stale-queue" / "valid", scratch)
            result = run(STALE_QUEUE, repo, "--queue", "docs")
            self.assertEqual(result.returncode, 1, result.stdout)
            self.assertIn("error: docs/note.md has waited 400 days", result.stdout)

    def test_tree_without_git_history_is_an_error(self):
        with tempfile.TemporaryDirectory() as scratch:
            (Path(scratch) / "inbox").mkdir()
            (Path(scratch) / "inbox" / "x.md").write_text("# x\n")
            result = run(STALE_QUEUE, scratch)
            self.assertEqual(result.returncode, 1)
            self.assertIn("no git history", result.stdout)


def vale_present():
    return shutil.which("vale") is not None


class ValeRules(unittest.TestCase):
    def setUp(self):
        if not vale_present():
            if os.environ.get("REQUIRE_GATES"):
                self.fail("REQUIRE_GATES set and vale is absent")
            self.skipTest("vale is not installed")

    @staticmethod
    def hits(config, *paths):
        result = subprocess.run(["vale", "--no-global", "--config", str(config), "--output=line", "--minAlertLevel", "suggestion", *map(str, paths)], capture_output=True, text=True, check=False)
        found = []
        for line in result.stdout.splitlines():
            parts = line.split(":", 4)
            if len(parts) >= 5 and parts[3].startswith("Core."):
                found.append((Path(parts[0]).name, parts[3]))
        return found

    @staticmethod
    def rule_of(fixture):
        return "Core." + "".join(part.capitalize() for part in fixture.stem.split("-")).replace("Ai", "AI").replace("Emdash", "EmDash")

    def test_each_invalid_fixture_trips_only_its_rule(self):
        config = FIXTURES / "vale" / ".vale.ini"
        for fixture in sorted((FIXTURES / "vale" / "invalid").glob("*.md")):
            with self.subTest(fixture.name):
                rules = {rule for _, rule in self.hits(config, fixture)}
                self.assertIn(self.rule_of(fixture), rules, f"{fixture.name} trips {sorted(rules)}")

    def test_each_valid_fixture_is_clean_for_its_rule(self):
        config = FIXTURES / "vale" / ".vale.ini"
        for fixture in sorted((FIXTURES / "vale" / "valid").glob("*.md")):
            with self.subTest(fixture.name):
                rules = {rule for _, rule in self.hits(config, fixture)}
                self.assertNotIn(self.rule_of(fixture), rules, f"{fixture.name} trips its own rule")

    def test_production_scoping(self):
        """The deck's own .vale.ini decides where a rule applies: instructions
        get the placeholder rules, a companion directory does not, a build
        directory gets nothing, a record gets DeckLinks and Nominalization,
        and BareCommandInProse reads specification files alone, never the
        generated glossary pages."""
        body = "# Specification acceptance\n\nSee [[X]] and ${CLAUDE_PROJECT_DIR} and /Users/martin/x and ${DECK}. Run `rune spec validate`.\n"
        watched = {"Core.DeckLinks", "Core.Nominalization", "Core.HarnessPlaceholder", "Core.UserValue", "Core.BareCommandInProse"}
        with tempfile.TemporaryDirectory() as scratch:
            mirror = Path(scratch)
            shutil.copytree(ROOT / ".vale", mirror / ".vale")
            (mirror / ".vale.ini").write_text(re.sub(r"^StylesPath = .*$", f"StylesPath = {mirror / '.vale' / 'styles'}", (ROOT / ".vale.ini").read_text(), flags=re.MULTILINE))
            places = {
                "docs/decisions/R.md": {"Core.DeckLinks", "Core.Nominalization"},
                "docs/changes/c/specs/cap/spec.md": {"Core.DeckLinks", "Core.Nominalization", "Core.BareCommandInProse"},
                "docs/specs/cap/spec.md": {"Core.DeckLinks", "Core.Nominalization", "Core.BareCommandInProse"},
                "docs/specs/glossary/term.md": {"Core.DeckLinks", "Core.Nominalization"},
                "runes/core/rules/X.md": {"Core.DeckLinks", "Core.Nominalization", "Core.HarnessPlaceholder", "Core.UserValue"},
                "runes/core/skills/S/claude/SKILL.md": {"Core.DeckLinks", "Core.Nominalization", "Core.UserValue"},
                "runes/core/build/claude/skills/S/SKILL.md": {"Core.DeckLinks", "Core.Nominalization"},
            }
            for rel in places:
                (mirror / rel).parent.mkdir(parents=True, exist_ok=True)
                (mirror / rel).write_text(body)
            for rel, expected in places.items():
                with self.subTest(rel):
                    result = subprocess.run(["vale", "--no-global", "--output=line", rel], capture_output=True, text=True, check=False, cwd=mirror)
                    rules = {line.split(":", 4)[3] for line in result.stdout.splitlines() if line.count(":") >= 4}
                    self.assertEqual(rules & watched, expected)


if __name__ == "__main__":
    unittest.main()
