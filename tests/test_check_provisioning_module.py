"""scripts/check-provisioning-module reports a file in the provisioning
module that has an execute permission bit or an interpreter line
(provisioning-joins-the-deck, The Validator Rejects Executable Files in the
Module)."""
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "check-provisioning-module"
SKILL = "---\nname: Example\ndescription: An example skill.\n---\n\n# Example\n\nBody.\n"


def run(root):
    return subprocess.run(["python3", str(SCRIPT), str(root)], capture_output=True, text=True, check=False)


def module(root):
    skill = Path(root) / "runes" / "provisioning" / "skills" / "Example"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(SKILL)
    return skill


class ExecutableFiles(unittest.TestCase):
    def test_clean_module_passes(self):
        with tempfile.TemporaryDirectory() as scratch:
            module(scratch)
            result = run(scratch)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(result.stdout, "")

    def test_absent_module_passes(self):
        with tempfile.TemporaryDirectory() as scratch:
            (Path(scratch) / "runes" / "core").mkdir(parents=True)
            result = run(scratch)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_execute_permission_fails(self):
        with tempfile.TemporaryDirectory() as scratch:
            script = module(scratch) / "install.sh"
            script.write_text("echo installed\n")
            script.chmod(0o755)
            result = run(scratch)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertEqual(result.stderr, "", "a check that crashes is not a finding")
            self.assertEqual(
                result.stdout,
                "runes/provisioning/skills/Example/install.sh: execute permission\n",
            )

    def test_interpreter_line_fails(self):
        with tempfile.TemporaryDirectory() as scratch:
            script = module(scratch) / "scripts" / "install"
            script.parent.mkdir()
            script.write_text("#!/bin/sh\necho installed\n")
            script.chmod(0o644)
            result = run(scratch)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertEqual(
                result.stdout,
                "runes/provisioning/skills/Example/scripts/install: interpreter line\n",
            )

    def test_one_line_names_both_reasons(self):
        with tempfile.TemporaryDirectory() as scratch:
            script = module(scratch) / "install.sh"
            script.write_text("#!/bin/sh\necho installed\n")
            script.chmod(0o755)
            result = run(scratch)
            self.assertEqual(
                result.stdout,
                "runes/provisioning/skills/Example/install.sh: execute permission and interpreter line\n",
            )


if __name__ == "__main__":
    unittest.main()
