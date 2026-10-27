"""Tests for the SKILL.md frontmatter reader."""

import tempfile
import unittest
from pathlib import Path

from scripts.utils import parse_skill_md


class ParseSkillMdTests(unittest.TestCase):
    def setUp(self):
        holder = tempfile.TemporaryDirectory()
        self.addCleanup(holder.cleanup)
        self.skill_dir = Path(holder.name)

    def write(self, text: str) -> Path:
        (self.skill_dir / "SKILL.md").write_text(text, encoding="utf-8")
        return self.skill_dir

    def test_plain_values(self):
        text = (
            "---\n"
            "name: demo-skill\n"
            "description: Plain text here. USE WHEN asked. NOT FOR other things\n"
            "---\n"
            "# Demo\n"
        )
        self.write(text)
        name, description, content = parse_skill_md(self.skill_dir)
        self.assertEqual(name, "demo-skill")
        self.assertEqual(
            description, "Plain text here. USE WHEN asked. NOT FOR other things"
        )
        self.assertEqual(content, text)

    def test_double_quoted_value_keeps_colons_and_escaped_quotes(self):
        self.write(
            "---\n"
            'name: "demo-skill"\n'
            'description: "Use this: it says \\"hi\\". NOT FOR x"\n'
            "---\n"
        )
        name, description, _ = parse_skill_md(self.skill_dir)
        self.assertEqual(name, "demo-skill")
        self.assertEqual(description, 'Use this: it says "hi". NOT FOR x')

    def test_single_quoted_value(self):
        self.write(
            "---\n"
            "name: 'demo-skill'\n"
            "description: 'It''s quoted: yes'\n"
            "---\n"
        )
        _, description, _ = parse_skill_md(self.skill_dir)
        self.assertEqual(description, "It's quoted: yes")

    def test_folded_block_scalar_joins_lines_with_spaces(self):
        self.write(
            "---\n"
            "name: demo-skill\n"
            "description: >-\n"
            "  First part of the text,\n"
            "  second part: with a colon.\n"
            "  NOT FOR \"quoted\" things\n"
            "license: MIT\n"
            "---\n"
        )
        _, description, _ = parse_skill_md(self.skill_dir)
        self.assertEqual(
            description,
            'First part of the text, second part: with a colon. NOT FOR "quoted" things',
        )

    def test_other_block_indicators(self):
        for indicator in ("|", ">", "|-", ">+"):
            with self.subTest(indicator=indicator):
                self.write(
                    "---\n"
                    f"description: {indicator}\n"
                    "  one\n"
                    "\n"
                    "  two\n"
                    "name: demo-skill\n"
                    "---\n"
                )
                name, description, _ = parse_skill_md(self.skill_dir)
                self.assertEqual(description, "one two")
                self.assertEqual(name, "demo-skill")

    def test_nested_name_under_metadata_is_ignored(self):
        self.write(
            "---\n"
            "metadata:\n"
            "  name: wrong-name\n"
            "  description: wrong description\n"
            "name: right-name\n"
            "description: right description\n"
            "---\n"
        )
        name, description, _ = parse_skill_md(self.skill_dir)
        self.assertEqual(name, "right-name")
        self.assertEqual(description, "right description")

    def test_nested_name_after_top_level_keys_is_ignored(self):
        self.write(
            "---\n"
            "name: right-name\n"
            "description: right description\n"
            "metadata:\n"
            "  name: wrong-name\n"
            "---\n"
        )
        name, _, _ = parse_skill_md(self.skill_dir)
        self.assertEqual(name, "right-name")

    def test_missing_opening_fence(self):
        self.write("name: demo-skill\ndescription: d\n---\n")
        with self.assertRaises(ValueError) as caught:
            parse_skill_md(self.skill_dir)
        self.assertIn("---", str(caught.exception))

    def test_missing_closing_fence(self):
        self.write("---\nname: demo-skill\ndescription: d\n# body\n")
        with self.assertRaises(ValueError) as caught:
            parse_skill_md(self.skill_dir)
        self.assertIn("closes", str(caught.exception))

    def test_missing_name(self):
        self.write("---\ndescription: d\n---\n")
        with self.assertRaises(ValueError) as caught:
            parse_skill_md(self.skill_dir)
        self.assertIn("name", str(caught.exception))

    def test_empty_description(self):
        self.write('---\nname: demo-skill\ndescription: ""\n---\n')
        with self.assertRaises(ValueError) as caught:
            parse_skill_md(self.skill_dir)
        self.assertIn("description", str(caught.exception))

    def test_missing_description(self):
        self.write("---\nname: demo-skill\n---\n")
        with self.assertRaises(ValueError):
            parse_skill_md(self.skill_dir)

    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            parse_skill_md(self.skill_dir)


if __name__ == "__main__":
    unittest.main()
