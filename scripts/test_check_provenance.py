import hashlib
import importlib.machinery
import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("check-provenance")
LOADER = importlib.machinery.SourceFileLoader(
    "check_provenance",
    str(SCRIPT),
)
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
CHECK_PROVENANCE = importlib.util.module_from_spec(SPEC)
LOADER.exec_module(CHECK_PROVENANCE)


class CheckProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.source = Path(self.temporary.name) / "Example.md"
        self.source.write_text("example\n", encoding="utf-8")
        self.sidecar = self.source.parent / ".provenance" / "Example.md.yaml"
        self.sidecar.parent.mkdir()
        self.sidecar.write_text(
            "provenance:\n"
            "  subject:\n"
            "  - name: skills/Example.md\n"
            "    digest:\n"
            f"      sha256: {'0' * 64}\n"
            "  predicate:\n"
            "    dependency_sha256: "
            f"{'1' * 64}\n",
            encoding="utf-8",
        )

    def test_sidecar_path_checks_its_source(self):
        self.assertEqual(CHECK_PROVENANCE.check([str(self.sidecar)]), 1)

    def test_sidecar_path_fixes_only_the_subject_digest(self):
        self.assertEqual(
            CHECK_PROVENANCE.check([str(self.sidecar)], fix=True),
            0,
        )

        text = self.sidecar.read_text(encoding="utf-8")
        digest = hashlib.sha256(self.source.read_bytes()).hexdigest()
        self.assertIn(f"sha256: {digest}", text)
        self.assertIn(f"dependency_sha256: {'1' * 64}", text)

    def test_missing_subject_digest_does_not_rewrite_dependency(self):
        self.sidecar.write_text(
            "provenance:\n"
            "  subject:\n"
            "  - name: skills/Example.md\n"
            "  predicate:\n"
            "    resolvedDependencies:\n"
            "    - uri: git+https://example.invalid/upstream\n"
            "      digest:\n"
            f"        sha256: {'1' * 64}\n",
            encoding="utf-8",
        )
        original = self.sidecar.read_text(encoding="utf-8")

        self.assertEqual(
            CHECK_PROVENANCE.check([str(self.sidecar)], fix=True),
            1,
        )
        self.assertEqual(self.sidecar.read_text(encoding="utf-8"), original)


if __name__ == "__main__":
    unittest.main()
