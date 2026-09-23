import importlib.machinery
import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "sync-idea"
LOADER = importlib.machinery.SourceFileLoader("sync_idea", str(SCRIPT))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
SYNC = importlib.util.module_from_spec(SPEC)
LOADER.exec_module(SYNC)


class ParseLinkTests(unittest.TestCase):
    def test_vault_and_file_with_encoded_space(self):
        self.assertEqual(
            SYNC.parse_link("obsidian://open?vault=Atlas&file=Library%2FCanvas%2FMarkdown%20First"),
            ("Atlas", "Library/Canvas/Markdown First.md"),
        )

    def test_explicit_extension_is_kept(self):
        self.assertEqual(SYNC.parse_link("obsidian://open?vault=Atlas&file=Inbox/Note.md"), ("Atlas", "Inbox/Note.md"))

    def test_other_scheme_is_refused(self):
        with self.assertRaises(ValueError):
            SYNC.parse_link("https://vault.martinzeman.net/Library/Canvas/Markdown+First")

    def test_link_without_file_is_refused(self):
        with self.assertRaises(ValueError):
            SYNC.parse_link("obsidian://open?vault=Atlas")

    def test_sidecar_records_link_and_digest(self):
        text = SYNC.sidecar_text("Markdown First.svg", "obsidian://open?vault=Atlas&file=Library/Canvas/Markdown%20First", "ab" * 32, "cd" * 32)
        self.assertEqual(SYNC.field(text, "upstream_url"), "obsidian://open?vault=Atlas&file=Library/Canvas/Markdown%20First")
        self.assertEqual(SYNC.field(text, "sha256"), "ab" * 32)
        self.assertEqual(SYNC.field(text, "sha256", after="resolvedDependencies"), "cd" * 32)
        self.assertIn("name: docs/ideas/Markdown First.svg", text)


if __name__ == "__main__":
    unittest.main()
