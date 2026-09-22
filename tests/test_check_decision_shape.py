import importlib.machinery
import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "check-decision-shape"
LOADER = importlib.machinery.SourceFileLoader("check_decision_shape", str(SCRIPT))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
SHAPE = importlib.util.module_from_spec(SPEC)
LOADER.exec_module(SHAPE)

RECORD = """---
title: "Example"
consulted: [{consulted}]
upstream: [{upstream}]
related: []
---

# Example

## Context and Problem Statement

Words.

## Considered Options

1. One

## Decision Outcome

Option 1.

{consequences}
"""


class CheckDecisionShapeTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "docs" / "decisions").mkdir(parents=True)
        spec = self.root / "docs" / "specs" / "example-capability"
        spec.mkdir(parents=True)
        (spec / "spec.md").write_text("### Requirement: Thing Is Checked\n\nBody.\n")
        (self.root / "authors.yaml").write_text(
            "authors:\n    - A <a@b>\nmodel_domains:\n    - claude.noreply.nexus.local\n    - codex.noreply.nexus.local\n"
        )

    def record(self, consulted='"@owner"', upstream="", consequences="### Consequences\n\n- [+] Gain\n- [-] Cost"):
        path = self.root / "docs" / "decisions" / "DECK-0001 Example.md"
        path.write_text(RECORD.format(consulted=consulted, upstream=upstream, consequences=consequences))
        return SHAPE.check(self.root)

    def test_template_shape_passes(self):
        self.assertEqual(self.record(), [])

    def test_unsigned_consequence_is_named(self):
        errors = self.record(consequences="### Consequences\n\n- [+] Gain\n- Cost without a sign")
        self.assertEqual(len(errors), 1)
        self.assertIn("consequence has no sign: `- Cost without a sign`", errors[0])

    def test_own_section_is_reported(self):
        errors = self.record(consequences="## Consequences\n\n- [+] Gain")
        self.assertIn("`## Consequences` is its own section", errors[0])

    def test_bare_model_id_fails(self):
        errors = self.record(consulted='"claude-fable-5-1"')
        self.assertIn("neither `@handle` nor `<model-id>@<harness>`", errors[0])

    def test_unknown_harness_lists_known(self):
        errors = self.record(consulted='"gpt-6-astra@openai"')
        self.assertIn("unknown harness. Known: claude, codex", errors[0])

    def test_model_with_harness_passes(self):
        self.assertEqual(self.record(consulted='"gpt-6-astra@codex", "@owner"'), [])

    def test_dangling_upstream_fails(self):
        errors = self.record(upstream='"MarkdownFirst.md"')
        self.assertIn("upstream `MarkdownFirst.md` matches no record", errors[0])

    def test_requirement_reference_resolves(self):
        self.assertEqual(self.record(upstream='"example-capability#thing-is-checked"'), [])

    def test_unknown_requirement_fails(self):
        errors = self.record(upstream='"example-capability#other-thing"')
        self.assertIn("matches no record, capability, requirement, file, or URL", errors[0])

    def test_repository_file_resolves(self):
        sketch = self.root / "docs" / "ideas" / "DECK-0001.excalidraw.md"
        sketch.parent.mkdir(parents=True)
        sketch.write_text("sketch\n")
        self.assertEqual(self.record(upstream='"docs/ideas/DECK-0001.excalidraw.md"'), [])
        errors = self.record(upstream='"docs/ideas/missing.excalidraw.md"')
        self.assertIn("matches no record, capability, requirement, file, or URL", errors[0])

    def test_record_and_url_resolve(self):
        self.assertEqual(self.record(upstream='"DECK-0001 Example", "https://example.org/x"'), [])


if __name__ == "__main__":
    unittest.main()
