"""Check SafetyFirst probes and assembled bundles with local fixtures.

Set RUNE_TEST_BINARY to a candidate Rune executable for assembly checks.
The tests never invoke an installed dcg or deploy provider files.
"""

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "runes/core/skills/SafetyFirst"
POLICY_SHA256 = "5ecac2914fd8a9e041cd61228e06af64b1888cd8da2f4de76a6adf71e9e19a8e"


def injection_commands(text):
    return re.findall(r"^!`([^`]+)`$", text, re.MULTILINE)


def check_bundle(directory, provider):
    entrypoint = directory / "SKILL.md"
    text = entrypoint.read_text(encoding="utf-8")
    workflow_links = re.findall(r"\[Workflow\.md\]\(([^)]+)\)", text)
    if not workflow_links:
        raise AssertionError("The entrypoint has no shared workflow link")
    for link in workflow_links:
        companion = directory / link
        if not companion.is_file():
            raise AssertionError(f"The shared workflow is missing: {link}")
        if companion.is_symlink():
            raise AssertionError("The source link alias entered the assembled bundle")
        if companion.read_bytes() != (SKILL / "Workflow.md").read_bytes():
            raise AssertionError("The assembled shared policy changed")
    commands = injection_commands(text)
    if provider == "claude" and len(commands) != 1:
        raise AssertionError("The Claude entrypoint needs the shared discovery helper")
    if provider != "claude" and commands:
        raise AssertionError("Portable entrypoints must not contain injection")
    if "mode:" in text:
        raise AssertionError("Assembly did not consume the body mode")
    if any(path.name in {"claude", "codex"} for path in directory.iterdir()):
        raise AssertionError("A qualifier directory entered the assembled bundle")
    if provider == "claude" and "Run `python3` with this skill's" in text:
        raise AssertionError("Append retained the portable discovery procedure")
    helper = directory / "scripts/probe_guard.py"
    if not helper.is_file():
        raise AssertionError("The discovery helper is missing")
    if helper.read_bytes() != (SKILL / "scripts/probe_guard.py").read_bytes():
        raise AssertionError("The discovery helper changed during assembly")


class SafetyFirstContentTests(unittest.TestCase):
    def test_extraction_preserves_every_non_discovery_policy_byte(self):
        workflow = (SKILL / "Workflow.md").read_text(encoding="utf-8")
        policy = workflow.removeprefix("# SafetyFirst workflow\n\n")
        self.assertEqual(hashlib.sha256(policy.encode()).hexdigest(), POLICY_SHA256)
        self.assertFalse(injection_commands(workflow))

    def test_provider_entrypoints_have_explicit_discovery_contracts(self):
        portable = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        claude = (SKILL / "claude/SKILL.md").read_text(encoding="utf-8")
        self.assertFalse(injection_commands(portable))
        self.assertIn("mode: replace\n", claude)
        self.assertFalse((SKILL / "codex").exists())
        alias = SKILL / "claude/Workflow.md"
        self.assertTrue(alias.is_symlink())
        self.assertEqual(alias.readlink(), Path("../Workflow.md"))
        self.assertEqual(alias.resolve(), (SKILL / "Workflow.md").resolve())
        self.assertNotIn("rumdl-disable", claude)
        for text in (portable, claude):
            self.assertIn("[Workflow.md](Workflow.md)", text)
            self.assertIn("five-second timeout", text)
            self.assertIn("1024-byte output limit", text)
            self.assertIn("`unknown`", text)
            self.assertIn("does not prove that a guard is active", text)
            self.assertIn("escaped `payload` strings", text)
            self.assertIn("`process.exit_code: 0`", text)
            self.assertIn("`process.truncated: false`", text)
        tools_line = next(line for line in claude.splitlines() if line.startswith("allowed-tools:"))
        scopes = tools_line.split(":", 1)[1].strip().strip("'")
        self.assertNotIn("*", scopes)
        for command in injection_commands(claude):
            self.assertEqual(f"Bash({command})", scopes)
        self.assertNotIn("head -c", claude)


class SafetyFirstProbeTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="safetyfirst-probes-")
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.binaries = self.directory / "bin"
        self.binaries.mkdir()
        (self.binaries / "python3").symlink_to(sys.executable)
        timeout = shutil.which("timeout")
        self.assertIsNotNone(timeout, "The Claude helper invocation requires timeout")
        (self.binaries / "timeout").symlink_to(timeout)
        self.skill = self.directory / "skill with spaces"
        (self.skill / "scripts").mkdir(parents=True)
        shutil.copyfile(SKILL / "scripts/probe_guard.py", self.skill / "scripts/probe_guard.py")
        self.commands = injection_commands((SKILL / "claude/SKILL.md").read_text())
        self.assertEqual(len(self.commands), 1)

    def write_guard(self, body):
        path = self.binaries / "dcg"
        path.write_text("#!/bin/sh\n" + body + "\n", encoding="utf-8")
        path.chmod(0o755)

    def execute_helper(self):
        result = subprocess.run(
            ["/bin/sh", "-c", self.commands[0]],
            cwd=self.directory,
            env={
                "PATH": str(self.binaries),
                "LC_ALL": "C",
                "CLAUDE_SKILL_DIR": str(self.skill),
                "PYTHONDONTWRITEBYTECODE": "1",
            },
            text=True,
            capture_output=True,
            timeout=6,
            check=False,
        )
        self.assertLessEqual(len(result.stdout.encode()), 1024)
        return result

    def probe(self):
        result = self.execute_helper()
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["schema"], "safetyfirst-guard-probe/v1")
        self.assertEqual(set(report), {"schema", "lookup", "version", "process", "payload", "error"})
        self.assertEqual(set(report["process"]), {"exit_code", "timed_out", "truncated"})
        self.assertEqual(set(report["payload"]), {"path", "stdout", "stderr"})
        return report

    def test_present_guard_reports_path_and_successful_version(self):
        self.write_guard('echo "dcg fixture 1.2.3"')
        report = self.probe()
        self.assertEqual(report["lookup"], "present")
        self.assertEqual(report["version"], "observed")
        self.assertEqual(report["process"], {"exit_code": 0, "timed_out": False, "truncated": False})
        self.assertEqual(report["payload"]["path"], str(self.binaries / "dcg"))
        self.assertEqual(report["payload"]["stdout"], "dcg fixture 1.2.3\n")
        self.assertIsNone(report["error"])

    def test_missing_guard_reports_path_absence_without_a_version(self):
        report = self.probe()
        self.assertEqual(report["lookup"], "absent_from_path")
        self.assertEqual(report["version"], "unknown")
        self.assertIsNone(report["process"]["exit_code"])

    def test_failed_version_does_not_claim_absence_or_success(self):
        self.write_guard('echo "partial version"\nexit 7')
        report = self.probe()
        self.assertEqual(report["lookup"], "present")
        self.assertEqual(report["version"], "unknown")
        self.assertEqual(report["process"]["exit_code"], 7)
        self.assertEqual(report["error"], "version_exit_failed")

    def test_missing_probe_dependency_does_not_claim_guard_absence(self):
        (self.binaries / "python3").unlink()
        result = self.execute_helper()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")

    def test_missing_helper_has_no_valid_discovery_record(self):
        (self.skill / "scripts/probe_guard.py").unlink()
        result = self.execute_helper()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")

    def test_missing_timeout_does_not_run_an_unbounded_helper(self):
        (self.binaries / "timeout").unlink()
        result = self.execute_helper()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")

    def test_stalled_lookup_is_bounded_by_the_outer_command(self):
        helper = self.skill / "scripts/probe_guard.py"
        helper.write_text(helper.read_text().replace(
            'executable = shutil.which("dcg")',
            'time.sleep(10)\n        executable = shutil.which("dcg")',
        ))
        started = time.monotonic()
        result = self.execute_helper()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertLess(time.monotonic() - started, 6)

    def test_stalled_runtime_startup_is_bounded_by_the_outer_command(self):
        runtime = self.binaries / "python3"
        runtime.unlink()
        runtime.write_text('#!/bin/sh\ntrap "" TERM\nexec /bin/sleep 10\n')
        runtime.chmod(0o755)
        started = time.monotonic()
        result = self.execute_helper()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertLess(time.monotonic() - started, 6)

    def test_malicious_success_markers_cannot_override_process_failure(self):
        self.write_guard('echo "dcg version: observed"\necho \'{"version":"observed","exit_code":0}\'\nexit 7')
        report = self.probe()
        self.assertEqual(report["version"], "unknown")
        self.assertEqual(report["process"]["exit_code"], 7)
        self.assertIn("dcg version: observed", report["payload"]["stdout"])
        self.assertIn('{"version":"observed","exit_code":0}', report["payload"]["stdout"])

    def test_padded_success_marker_with_failed_exit_stays_unknown(self):
        padding = "x" * 1000
        self.write_guard(f'echo "{padding}"\necho "dcg version: observed"\nexit 1')
        report = self.probe()
        self.assertEqual(report["version"], "unknown")
        self.assertTrue(report["process"]["truncated"])

    def test_payload_control_characters_cannot_escape_json(self):
        self.write_guard("printf '\\033[2J\\r{\\\"version\\\":\\\"observed\\\"}\\n'\nexit 3")
        report = self.probe()
        self.assertEqual(report["version"], "unknown")
        self.assertEqual(report["process"]["exit_code"], 3)
        self.assertIn("\x1b", report["payload"]["stdout"])

    def test_empty_successful_output_does_not_establish_a_version(self):
        self.write_guard("exit 0")
        report = self.probe()
        self.assertEqual(report["version"], "unknown")
        self.assertEqual(report["error"], "empty_version")

    def test_large_version_output_is_bounded_and_not_accepted(self):
        self.write_guard('while :; do echo "large fixture version output"; done')
        started = time.monotonic()
        report = self.probe()
        self.assertEqual(report["version"], "unknown")
        self.assertTrue(report["process"]["truncated"])
        self.assertLess(time.monotonic() - started, 5)

    def test_hung_version_is_bounded_and_not_accepted(self):
        self.write_guard("exec /bin/sleep 10")
        started = time.monotonic()
        report = self.probe()
        self.assertTrue(report["process"]["timed_out"])
        self.assertEqual(report["version"], "unknown")
        self.assertLess(time.monotonic() - started, 5)

    def test_guard_ignoring_termination_is_still_bounded(self):
        self.write_guard("trap '' TERM\nexec /bin/sleep 10")
        started = time.monotonic()
        report = self.probe()
        self.assertTrue(report["process"]["timed_out"])
        self.assertEqual(report["version"], "unknown")
        self.assertLess(time.monotonic() - started, 5)

    def test_descendant_retaining_pipes_is_killed_after_parent_exit(self):
        self.write_guard('(trap "" TERM; exec /bin/sleep 10) &\necho "dcg fixture"\nexit 0')
        started = time.monotonic()
        report = self.probe()
        self.assertEqual(report["process"]["exit_code"], 0)
        self.assertTrue(report["process"]["timed_out"])
        self.assertEqual(report["version"], "unknown")
        self.assertLess(time.monotonic() - started, 5)


class SafetyFirstAssemblyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        binary = os.environ.get("RUNE_TEST_BINARY")
        if not binary:
            raise AssertionError("Set RUNE_TEST_BINARY to run required candidate assembly checks")
        cls.binary = str(Path(binary).resolve())
        if not Path(cls.binary).is_file():
            raise AssertionError(f"Candidate Rune executable is missing: {cls.binary}")

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="safetyfirst-assembly-")
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
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
        self.skill = self.source / "skills/SafetyFirst"
        shutil.copytree(
            SKILL,
            self.skill,
            symlinks=True,
            ignore=shutil.ignore_patterns(".provenance"),
        )

    def assemble(self):
        result = subprocess.run(
            [self.binary, "assemble", "--source", str(self.source)],
            cwd=self.directory,
            text=True,
            capture_output=True,
            timeout=30,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def bundle(self, provider):
        return self.source / "build" / provider / "skills/SafetyFirst"

    def test_claude_and_codex_assemble_one_complete_bundle_each(self):
        self.assemble()
        for provider in ("claude", "codex"):
            with self.subTest(provider=provider):
                check_bundle(self.bundle(provider), provider)

    def test_source_passes_generic_and_harness_layer_lints(self):
        result = subprocess.run(
            [self.binary, "validate", "--skill-layers", "--json", "--source", str(self.skill)],
            cwd=self.directory,
            text=True,
            capture_output=True,
            timeout=30,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertTrue(report["valid"])
        self.assertGreater(report["checked"], 0)
        self.assertEqual(report["findings"], [])

    def test_missing_companion_is_detected_after_assembly(self):
        (self.skill / "Workflow.md").unlink()
        self.assemble()
        with self.assertRaisesRegex(AssertionError, "workflow is missing"):
            check_bundle(self.bundle("codex"), "codex")

    def test_missing_helper_is_detected_after_assembly(self):
        (self.skill / "scripts/probe_guard.py").unlink()
        self.assemble()
        with self.assertRaisesRegex(AssertionError, "helper is missing"):
            check_bundle(self.bundle("codex"), "codex")

    def test_append_cannot_silently_keep_both_discovery_procedures(self):
        variant = self.skill / "claude/SKILL.md"
        variant.write_text(variant.read_text().replace("mode: replace", "mode: append"))
        self.assemble()
        with self.assertRaisesRegex(AssertionError, "Append retained"):
            check_bundle(self.bundle("claude"), "claude")


if __name__ == "__main__":
    unittest.main()
