"""The default deployment leaves the provisioning module out
(provisioning-joins-the-deck, The Default Deployment Omits the Module).

The test builds a deck with a core module and a provisioning module, one
skill each, and the real casts/all.yaml of this repository. A consumer that
selects every module through the `all` cast receives no provisioning rune
in any harness tree. A consumer that names the module receives it. rune
runs with HOME and XDG_CONFIG_HOME inside the scratch directory, so the test
never reads or writes ~/.config/rune/. It skips when rune is absent and
fails instead when REQUIRE_GATES is set, the convention of the deck hooks."""
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ALL_CAST = ROOT / "casts" / "all.yaml"
DECK = "schema: 1\nname: deck\nversion: 0.1.0\ndescription: A test deck.\nproviders:\n    - claude\n    - codex\n    - gemini\n    - opencode\n"
SKILL = "---\nname: {name}\ndescription: The {name} skill.\n---\n\n# {name}\n\nBody.\n"
CONSUMER = "version: 1\nsources:\n  deck:\n    local: {deck}\nrunes:\n  deck:\n    {selection}\n"


def module(deck, name, skill):
    root = deck / "runes" / name
    (root / "skills" / skill).mkdir(parents=True)
    (root / "module.yaml").write_text(f"name: {name}\nversion: 0.1.0\ndescription: The {name} module.\nevents: []\n")
    (root / "defaults.yaml").write_text("")
    (root / "README.md").write_text(f"# {name}\n")
    (root / "LICENSE").write_text("EUPL-1.2\n")
    (root / "skills" / skill / "SKILL.md").write_text(SKILL.format(name=skill))


def deck(scratch):
    root = scratch / "deck"
    (root / "casts").mkdir(parents=True)
    (root / "deck.yaml").write_text(DECK)
    shutil.copyfile(ALL_CAST, root / "casts" / "all.yaml")
    module(root, "core", "CoreSkill")
    module(root, "provisioning", "ProvisioningSkill")
    return root


class DefaultSelection(unittest.TestCase):
    def setUp(self):
        self.rune = shutil.which("rune")
        if self.rune is None:
            if os.environ.get("REQUIRE_GATES"):
                self.fail("REQUIRE_GATES set and rune is absent")
            self.skipTest("rune is not installed")
        self.scratch = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.scratch, ignore_errors=True)
        home = self.scratch / "home"
        (home / ".config").mkdir(parents=True)
        self.env = {**os.environ, "HOME": str(home), "XDG_CONFIG_HOME": str(home / ".config")}
        self.deck = deck(self.scratch)

    def install(self, label, selection):
        """Deployed SKILL.md paths, relative to the consumer, for one selection."""
        consumer = self.scratch / label
        consumer.mkdir()
        (consumer / ".rune").write_text(CONSUMER.format(deck=self.deck, selection=selection))
        result = subprocess.run(
            [self.rune, "install", "--no-color"], cwd=consumer, env=self.env, capture_output=True, text=True, check=False
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return sorted(path.relative_to(consumer).as_posix() for path in consumer.rglob("SKILL.md"))

    def test_selecting_every_module_leaves_provisioning_out(self):
        deployed = self.install("every-module", "casts: [all]")
        self.assertIn(".claude/skills/CoreSkill/SKILL.md", deployed)
        self.assertEqual([path for path in deployed if "ProvisioningSkill" in path], [])

    def test_naming_the_module_deploys_it(self):
        deployed = self.install("named-module", "include: [provisioning]")
        self.assertIn(".claude/skills/ProvisioningSkill/SKILL.md", deployed)
        self.assertEqual([path for path in deployed if "CoreSkill" in path], [])


if __name__ == "__main__":
    unittest.main()
