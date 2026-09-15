"""Check portable skill sources and their rendered provider bundles.

Set RUNE_TEST_BINARY to the candidate Rune executable. These checks use
temporary modules. They do not deploy skills or invoke a model.
"""

import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "runes/core/skills"
NAMES = (
    "AdoptArtifact",
    "BenchArtifact",
    "BuildAvatar",
    "BuildSkill",
    "SimplifiedTechnicalEnglish",
)
CLAUDE_SCOPES = {
    "AdoptArtifact": "Bash(rune *), Bash(git add *), Bash(git status *), Bash(git diff *), Bash(rm *), Read, Edit, Write, Grep, Glob",
    "BenchArtifact": "Bash(python3 *), Bash(mkdir *), Bash(cp *), Read, Write, Edit, Grep, Glob, Agent",
    "SimplifiedTechnicalEnglish": "Bash(python3 *), Bash(git diff *), Read, Write, Edit, Grep, Glob",
}


def body(text):
    return text.split("\n---\n", 1)[1].strip()


def field(text, key):
    header = text.split("\n---\n", 1)[0]
    match = re.search(rf"^{re.escape(key)}: (.*)$", header, re.MULTILINE)
    return match.group(1) if match else None


def content_paths(root):
    return {
        path.relative_to(root)
        for path in root.rglob("*")
        if path.is_file()
        and ".provenance" not in path.relative_to(root).parts
        and path.relative_to(root).parts[0] != "claude"
    }


class PortableSkillContentTests(unittest.TestCase):
    def test_create_and_validate_route_to_the_bounded_loop_companion(self):
        skill = SKILLS / "BuildSkill"
        for name in ("SKILL.md", "CreateWorkflow.md", "ValidateWorkflow.md"):
            text = (skill / name).read_text()
            self.assertIn("[ImplementationLoop.md](ImplementationLoop.md)", text)
        loop = (skill / "ImplementationLoop.md").read_text()
        self.assertIn("cli/blob/main/docs/artifact-implementation-loop.md", loop)
        self.assertLess(len(loop.splitlines()), 150)
        self.assertLess(len(body((skill / "SKILL.md").read_text()).splitlines()), 100)

    def test_authoring_rules_use_the_same_variant_paths(self):
        rules = ROOT / "runes/core/rules"
        for name in ("ArtifactLength", "SkillLayout"):
            with self.subTest(rule=name):
                text = (rules / f"{name}.md").read_text()
                self.assertIn("<provider>/<exact-model-id>/SKILL.md", text)
                self.assertIn("configured model registry", text)
        layout = (rules / "SkillLayout.md").read_text()
        self.assertIn("<provider>/SKILL.md", layout)
        self.assertIn("not separate canonical skills", layout)
        self.assertIn("explicit body mode", layout)
        efficient = (rules / "UseEfficientCLI.md").read_text()
        self.assertIn("available file-reading tool", efficient)
        self.assertIn("bounded shell read", efficient)
        self.assertNotIn("harness Read tool", efficient)

    def test_existing_claude_scopes_are_preserved_in_metadata_only_variants(self):
        for name, expected in CLAUDE_SCOPES.items():
            with self.subTest(skill=name):
                canonical = (SKILLS / name / "SKILL.md").read_text()
                variant = (SKILLS / name / "claude/SKILL.md").read_text()
                self.assertIsNone(field(canonical, "allowed-tools"))
                self.assertEqual(field(variant, "allowed-tools"), expected)
                self.assertEqual(field(variant, "mode"), "append")
                self.assertEqual(body(variant), "")

    def test_interview_bank_preserves_all_eight_sections_and_depth(self):
        text = (SKILLS / "BuildAvatar/Interview.md").read_text()
        sections = re.findall(r"^### (\d+)\. (.+)$", text, re.MULTILINE)
        self.assertEqual([number for number, _ in sections], list("12345678"))
        questions = text.split("## Rounds\n", 1)[1].split("## After the rounds", 1)[0]
        count = len(re.findall(r"^- ", questions, re.MULTILINE))
        self.assertGreaterEqual(count, 20)
        self.assertLessEqual(count, 30)
        for path in ("BuildAvatar/SKILL.md", "BuildAvatar/Interview.md"):
            instructions = (SKILLS / path).read_text()
            self.assertIn("20 to 30 questions", instructions)
            self.assertIn("one question in each message", instructions)
            self.assertNotIn("four questions", instructions)
            self.assertNotIn("five to eight", instructions)

    def test_all_existing_source_subject_digests_match_their_content(self):
        for name in NAMES:
            for sidecar in (SKILLS / name).rglob(".provenance/*.yaml"):
                source = sidecar.parent.parent / sidecar.name.removesuffix(".yaml")
                if not source.is_file():
                    continue
                with self.subTest(source=source.relative_to(ROOT)):
                    statement = sidecar.read_text()
                    subject = statement.split("subject:", 1)[1].split("\npredicate:", 1)[0]
                    expected = re.search(r"sha256: ([0-9a-f]{64})", subject).group(1)
                    self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), expected)


class PortableSkillAssemblyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        binary = os.environ.get("RUNE_TEST_BINARY")
        if not binary:
            raise AssertionError("Set RUNE_TEST_BINARY for the required candidate checks")
        cls.binary = str(Path(binary).resolve())
        if not Path(cls.binary).is_file():
            raise AssertionError(f"Candidate Rune executable is missing: {cls.binary}")

    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="portable-skills-")
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        self.source = self.directory / "source"
        self.source.mkdir()
        (self.source / "module.yaml").write_text("name: fixture\nversion: 0.1.0\n")
        (self.source / "config.yaml").write_text(
            "providers:\n"
            "    claude:\n        enabled: true\n"
            "    codex:\n        enabled: true\n"
            "    gemini:\n        enabled: false\n"
            "    opencode:\n        enabled: false\n"
            "    agentskills:\n        enabled: false\n"
        )
        for name in NAMES:
            shutil.copytree(
                SKILLS / name,
                self.source / "skills" / name,
                symlinks=True,
                ignore=shutil.ignore_patterns(".provenance", "__pycache__"),
            )

    def run_rune(self, *arguments):
        return subprocess.run(
            [self.binary, *arguments, "--source", str(self.source)],
            cwd=self.directory,
            text=True,
            capture_output=True,
            timeout=60,
            check=False,
        )

    def test_all_five_skills_pass_source_layers(self):
        result = self.run_rune("validate", "--skill-layers", "--json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertTrue(report["valid"])
        self.assertGreaterEqual(report["checked"], len(NAMES))
        self.assertEqual(report["findings"], [])

    def test_claude_scopes_preserve_procedures_and_do_not_enter_codex(self):
        result = self.run_rune("assemble")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        rendered = {}
        for name, expected in CLAUDE_SCOPES.items():
            for provider in ("claude", "codex"):
                with self.subTest(skill=name, provider=provider):
                    text = (self.source / "build" / provider / "skills" / name / "SKILL.md").read_text()
                    rendered[(name, provider)] = text
                    self.assertEqual(field(text, "allowed-tools"), expected if provider == "claude" else None)
                    self.assertIsNone(field(text, "mode"))
        claude_adopt = (self.source / "build/claude/skills/AdoptArtifact/SKILL.md").read_text()
        self.assertEqual(
            field(claude_adopt, "argument-hint"),
            field((SKILLS / "AdoptArtifact/claude/SKILL.md").read_text(), "argument-hint"),
        )
        for name in CLAUDE_SCOPES:
            (self.source / "skills" / name / "claude/SKILL.md").unlink()
        result = self.run_rune("assemble")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for (name, provider), text in rendered.items():
            with self.subTest(baseline=name, provider=provider):
                baseline = (self.source / "build" / provider / "skills" / name / "SKILL.md").read_text()
                self.assertEqual(body(text), body(baseline))

    def test_both_providers_receive_every_shared_companion(self):
        result = self.run_rune("assemble")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for name in NAMES:
            source = self.source / "skills" / name
            for provider in ("claude", "codex"):
                with self.subTest(skill=name, provider=provider):
                    bundle = self.source / "build" / provider / "skills" / name
                    self.assertEqual(content_paths(bundle), content_paths(source))
                    self.assertFalse((bundle / "claude").exists())
                    for path in content_paths(source):
                        if path.parts[0] in {"scripts", "assets", "config"}:
                            self.assertEqual((bundle / path).read_bytes(), (source / path).read_bytes())

    def test_shared_reference_cannot_reintroduce_quoted_native_syntax(self):
        path = self.source / "skills/BuildSkill/ClaudeSkill.md"
        with path.open("a") as handle:
            handle.write("\nA forbidden quoted example: `AskUserQuestion`.\n")
        result = self.run_rune("validate", "--skill-layers", "--json")
        self.assertNotEqual(result.returncode, 0)
        report = json.loads(result.stdout)
        self.assertFalse(report["valid"])
        self.assertTrue(any(
            finding["code"] == "CSI007_HARNESS_LEAKAGE"
            and Path(finding["path"]).resolve() == path.resolve()
            and finding.get("token") == "AskUserQuestion"
            for finding in report["findings"]
        ), report["findings"])


if __name__ == "__main__":
    unittest.main()
