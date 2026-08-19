import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("lint.py")
SPEC = importlib.util.spec_from_file_location("ste_lint", SCRIPT)
STE_LINT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(STE_LINT)


class ConfigTests(unittest.TestCase):
    def setUp(self):
        self.config, self.path, self.digest = STE_LINT.load_config()

    def write_config(self, data):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", encoding="utf-8", delete=False
        ) as temporary:
            json.dump(data, temporary)
        self.addCleanup(Path(temporary.name).unlink, missing_ok=True)
        return temporary.name

    def test_default_config_preserves_policy_checks(self):
        result = STE_LINT.lint("Use a seamless system prior to launch.")

        self.assertEqual(result["violations"]["marketing_adjective"], 1)
        self.assertEqual(result["violations"]["banned_word"], 1)
        self.assertEqual(result["config_path"], self.path)
        self.assertEqual(result["config_sha256"], self.digest)

    def test_software_metaphors_are_soft_findings(self):
        result = STE_LINT.lint("Bake the value, gate the merge, and land the change.")

        self.assertEqual(result["violations"]["banned_word"], 3)
        self.assertEqual(result["severity_totals"], {"hard": 0, "soft": 3})

    def test_noun_position_does_not_count_verb_only_words(self):
        for text in (
            "The API surface stays stable.",
            "Travel by ship to the island.",
            "The landing page loads fast.",
        ):
            with self.subTest(text=text):
                result = STE_LINT.lint(text)
                self.assertEqual(result["violations"]["banned_word"], 0)

    def test_jargon_nouns_count_as_banned_words(self):
        for text in ("The release gate is open.", "Turn the knob on the treatment arm."):
            with self.subTest(text=text):
                result = STE_LINT.lint(text)
                self.assertGreaterEqual(result["violations"]["banned_word"], 1)

    def test_verb_position_counts_verb_only_words(self):
        for text in (
            "We ship the fix today.",
            "The team will ship it.",
            "Ship the fix.",
            "Do not ship broken code.",
        ):
            with self.subTest(text=text):
                result = STE_LINT.lint(text)
                self.assertEqual(result["violations"]["banned_word"], 1)

    def test_complete_custom_config_replaces_defaults(self):
        custom = {key: [] for key in STE_LINT.CONFIG_KEYS}
        custom["marketing"] = ["frictionless", "FRICTIONLESS"]
        path = self.write_config(custom)
        config, config_path, digest = STE_LINT.load_config(path)

        result = STE_LINT.lint(
            "A seamless system is frictionless.",
            config=config,
            config_path=config_path,
            config_digest=digest,
        )

        self.assertEqual(config["marketing"], ["frictionless"])
        self.assertEqual(result["violations"]["marketing_adjective"], 1)
        self.assertEqual(result["sample_marketing"], ["frictionless"])
        self.assertNotEqual(result["config_sha256"], self.digest)

    def test_strict_mode_uses_configured_strict_words(self):
        custom = {key: [] for key in STE_LINT.CONFIG_KEYS}
        custom["strictBannedWords"] = ["customword"]
        path = self.write_config(custom)
        config, config_path, digest = STE_LINT.load_config(path)

        result = STE_LINT.lint(
            "Use customword now.",
            strict=True,
            config=config,
            config_path=config_path,
            config_digest=digest,
        )

        self.assertEqual(result["violations"]["strict_banned_word"], 1)

    def test_config_rejects_unknown_and_missing_keys(self):
        with self.subTest("unknown"):
            custom = {key: [] for key in STE_LINT.CONFIG_KEYS}
            custom["unknown"] = []
            with self.assertRaisesRegex(ValueError, "unknown keys: unknown"):
                STE_LINT.load_config(self.write_config(custom))
        with self.subTest("missing"):
            custom = {key: [] for key in STE_LINT.CONFIG_KEYS if key != "marketing"}
            with self.assertRaisesRegex(ValueError, "missing keys: marketing"):
                STE_LINT.load_config(self.write_config(custom))

    def test_config_rejects_invalid_json_and_values(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", encoding="utf-8", delete=False
        ) as invalid:
            invalid.write("{")
        self.addCleanup(Path(invalid.name).unlink, missing_ok=True)
        with self.assertRaisesRegex(ValueError, "invalid JSON"):
            STE_LINT.load_config(invalid.name)

        custom = {key: [] for key in STE_LINT.CONFIG_KEYS}
        custom["marketing"] = [""]
        with self.assertRaisesRegex(ValueError, "non-empty strings"):
            STE_LINT.load_config(self.write_config(custom))

    def test_missing_config_exits_without_traceback(self):
        process = subprocess.run(
            [sys.executable, str(SCRIPT), "--config", "/does/not/exist"],
            input="Use this text.",
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertNotEqual(process.returncode, 0)
        self.assertIn("cannot read config", process.stderr)
        self.assertNotIn("Traceback", process.stderr)

    def test_json_output_carries_config_identity(self):
        process = subprocess.run(
            [sys.executable, str(SCRIPT)],
            input="Use this text.",
            text=True,
            capture_output=True,
            check=True,
        )
        result = json.loads(process.stdout)

        self.assertEqual(result["config_path"], self.path)
        self.assertEqual(result["config_sha256"], self.digest)

    def test_fail_over_uses_configured_score(self):
        custom = {key: [] for key in STE_LINT.CONFIG_KEYS}
        custom["marketing"] = ["customword"]
        path = self.write_config(custom)
        process = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--config",
                path,
                "--fail-over",
                "0",
            ],
            input="Use customword.",
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(process.returncode, 1)

    def test_unmatched_glob_fails_with_threshold(self):
        process = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--fail-over",
                "2.5",
                "/does/not/exist/*.md",
            ],
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertNotEqual(process.returncode, 0)
        self.assertIn("no files matched", process.stderr)

    def test_recursive_glob_lints_nested_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            nested = root / "one" / "two"
            nested.mkdir(parents=True)
            (nested / "draft.md").write_text("Use this text.", encoding="utf-8")
            process = subprocess.run(
                [sys.executable, str(SCRIPT), str(root / "**" / "*.md")],
                text=True,
                capture_output=True,
                check=True,
            )

        self.assertIn("draft.md", process.stdout)

    def test_strict_em_dash_is_only_a_marker(self):
        result = STE_LINT.lint("Use this text — now.", strict=True)

        self.assertEqual(result["em_dash(slop-marker)"], 1)
        self.assertNotIn("em_dash", result["violations"])
        self.assertEqual(result["total"], 0)
        self.assertEqual(result["total_per100w"], 0.0)

    def test_score_version_and_filler_category(self):
        result = STE_LINT.lint("It is important to note that the test failed.")

        self.assertEqual(result["score_version"], 5)
        self.assertEqual(result["violations"]["filler_phrase"], 1)
        self.assertNotIn("modal_hedge", result["violations"])

    def test_semantic_may_is_not_penalized_in_strict_mode(self):
        result = STE_LINT.lint("The request may fail.", strict=True)

        self.assertEqual(result["violations"]["strict_banned_word"], 0)

    def test_modal_perfect_preserves_uncertainty(self):
        for text in (
            "We may have found an edge case.",
            "The service might have failed.",
            "The client could have sent stale data.",
        ):
            with self.subTest(text=text):
                result = STE_LINT.lint(text)
                self.assertEqual(result["violations"]["complex_tense"], 0)

    def test_ordinary_perfect_tense_remains_scored(self):
        result = STE_LINT.lint("We have found an edge case.")

        self.assertEqual(result["violations"]["complex_tense"], 1)

    def test_short_density_is_advisory(self):
        short = STE_LINT.lint("Use this text.")
        long = STE_LINT.lint(" ".join(["word"] * 40) + ".")

        self.assertFalse(short["density_reliable"])
        self.assertEqual(short["density_note"], "Advisory: fewer than 40 words.")
        self.assertTrue(long["density_reliable"])
        self.assertIsNone(long["density_note"])

    def test_markdown_code_frontmatter_and_tables_are_masked(self):
        text = """---
title: Seamless robust platform
---

Use this text.

| Long sentence that must not count as prose | Value |
| --- | --- |
| This is a seamless and robust table value | one |

```text
This is a seamless robust sentence that must not count.
```
"""

        result = STE_LINT.lint(text)

        self.assertEqual(result["violations"]["marketing_adjective"], 0)
        self.assertEqual(result["sentences"], 1)

    def test_markdown_fence_content_is_prose(self):
        text = """```markdown
Use this seamless interface.
```
"""

        result = STE_LINT.lint(text)

        self.assertEqual(result["violations"]["marketing_adjective"], 1)
        self.assertEqual(result["sentences"], 1)

    def test_soft_wrapped_sentence_keeps_one_word_count(self):
        text = "This sentence has ten words across this first soft line\nand eleven more words across the second soft line today for reliable results."

        result = STE_LINT.lint(text)

        self.assertEqual(result["sentences"], 1)
        self.assertEqual(result["violations"]["long_sentence(>20w)"], 1)

    def test_abbreviation_does_not_create_a_sentence_boundary(self):
        result = STE_LINT.lint("Use common formats, e.g. JSON and YAML. Keep both names.")

        self.assertEqual(result["sentences"], 2)

    def test_severity_totals_separate_hard_and_soft_findings(self):
        result = STE_LINT.lint("We have used a seamless system;")

        self.assertGreaterEqual(result["severity_totals"]["hard"], 2)
        self.assertEqual(result["severity_totals"]["soft"], 1)

    def test_context_lints_a_draft_path(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", encoding="utf-8", delete=False
        ) as draft:
            draft.write("Use this text.")
        self.addCleanup(Path(draft.name).unlink, missing_ok=True)
        process = subprocess.run(
            [sys.executable, str(SCRIPT), "--context", draft.name],
            text=True,
            capture_output=True,
            check=True,
        )

        self.assertIn(Path(draft.name).name, process.stdout)

    def test_context_without_a_draft_path_is_advisory(self):
        process = subprocess.run(
            [sys.executable, str(SCRIPT), "--context", "rewrite this sentence"],
            text=True,
            capture_output=True,
            check=True,
        )

        self.assertIn("No readable draft path", process.stdout)

    def test_empty_context_does_not_read_stdin(self):
        process = subprocess.run(
            [sys.executable, str(SCRIPT), "--context", ""],
            input="This input must not be linted.",
            text=True,
            capture_output=True,
            check=True,
        )

        self.assertIn("No readable draft path", process.stdout)
        self.assertNotIn("score_version", process.stdout)

    def test_context_failure_blocks_threshold_callers(self):
        process = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--context",
                "rewrite this sentence",
                "--fail-over",
                "2.5",
            ],
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertNotEqual(process.returncode, 0)
        self.assertIn("No readable draft path", process.stderr)


if __name__ == "__main__":
    unittest.main()
