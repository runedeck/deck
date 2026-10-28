"""Tests for the Claude Code adapter: event decisions, packaging, and probes.

No test starts the real ``claude`` program; process launches are replaced
with fakes.
"""

import io
import json
import os
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path
from typing import ClassVar
from unittest import mock

from scripts.harness import claude

COMMAND = "demo-skill-0a1b2c3d"


def stream_line(inner: dict) -> str:
    return json.dumps({"type": "stream_event", "event": inner})


def tool_start(tool: str) -> str:
    return stream_line(
        {
            "type": "content_block_start",
            "index": 1,
            "content_block": {"type": "tool_use", "id": "toolu_1", "name": tool, "input": {}},
        }
    )


def text_start() -> str:
    return stream_line(
        {"type": "content_block_start", "index": 0, "content_block": {"type": "text", "text": ""}}
    )


def input_delta(text: str) -> str:
    return stream_line(
        {
            "type": "content_block_delta",
            "index": 1,
            "delta": {"type": "input_json_delta", "partial_json": text},
        }
    )


BLOCK_STOP = stream_line({"type": "content_block_stop", "index": 1})
MESSAGE_STOP = stream_line({"type": "message_stop"})
RESULT = json.dumps({"type": "result", "subtype": "success", "is_error": False})


def assistant_line(content: list[dict]) -> str:
    return json.dumps({"type": "assistant", "message": {"role": "assistant", "content": content}})


class CountingLines:
    """Iterable that records how many lines were pulled from it."""

    def __init__(self, lines: list[str]):
        self.lines = lines
        self.consumed = 0

    def __iter__(self):
        for line in self.lines:
            self.consumed += 1
            yield line


class DecideFromEventsTests(unittest.TestCase):
    def test_early_pick_from_partial_deltas(self):
        lines = CountingLines(
            [
                tool_start("Skill"),
                input_delta('{"skill": "' + COMMAND[:6]),
                input_delta(COMMAND[6:] + '"}'),
                BLOCK_STOP,
                RESULT,
            ]
        )
        self.assertTrue(claude.decide_from_events(lines, COMMAND))
        self.assertEqual(lines.consumed, 3)

    def test_early_refusal_on_other_tool(self):
        lines = CountingLines([tool_start("Bash"), input_delta('{"command": "ls"}'), RESULT])
        self.assertFalse(claude.decide_from_events(lines, COMMAND))
        self.assertEqual(lines.consumed, 1)

    def test_block_stop_without_command_name_is_not_picked(self):
        lines = CountingLines(
            [
                tool_start("Read"),
                input_delta('{"file_path": "/repo/README.md"}'),
                BLOCK_STOP,
                RESULT,
            ]
        )
        self.assertFalse(claude.decide_from_events(lines, COMMAND))
        self.assertEqual(lines.consumed, 3)

    def test_read_of_command_file_is_picked(self):
        lines = [
            tool_start("Read"),
            input_delta(f'{{"file_path": "/tmp/proj/.claude/commands/{COMMAND}.md"}}'),
        ]
        self.assertTrue(claude.decide_from_events(lines, COMMAND))

    def test_text_block_then_message_stop_is_not_picked(self):
        lines = CountingLines([text_start(), MESSAGE_STOP, RESULT])
        self.assertFalse(claude.decide_from_events(lines, COMMAND))
        self.assertEqual(lines.consumed, 2)

    def test_assistant_fallback_skill_tool(self):
        lines = [
            assistant_line(
                [{"type": "tool_use", "id": "t", "name": "Skill", "input": {"skill": COMMAND}}]
            )
        ]
        self.assertTrue(claude.decide_from_events(lines, COMMAND))

    def test_assistant_fallback_read_tool(self):
        lines = [
            assistant_line(
                [
                    {"type": "text", "text": "Let me look."},
                    {
                        "type": "tool_use",
                        "id": "t",
                        "name": "Read",
                        "input": {"file_path": f".claude/commands/{COMMAND}.md"},
                    },
                ]
            )
        ]
        self.assertTrue(claude.decide_from_events(lines, COMMAND))

    def test_assistant_fallback_other_tool_or_wrong_name(self):
        other = assistant_line(
            [{"type": "tool_use", "id": "t", "name": "Grep", "input": {"pattern": COMMAND}}]
        )
        self.assertFalse(claude.decide_from_events([other], COMMAND))
        wrong = assistant_line(
            [{"type": "tool_use", "id": "t", "name": "Skill", "input": {"skill": "another"}}]
        )
        self.assertFalse(claude.decide_from_events([wrong], COMMAND))

    def test_assistant_text_only_message_does_not_decide(self):
        lines = CountingLines([assistant_line([{"type": "text", "text": "Hello"}]), RESULT])
        self.assertFalse(claude.decide_from_events(lines, COMMAND))
        self.assertEqual(lines.consumed, 2)

    def test_result_event_is_not_picked(self):
        self.assertFalse(claude.decide_from_events([RESULT], COMMAND))

    def test_non_json_lines_are_ignored(self):
        lines = [
            "",
            "plain text noise",
            "{not json",
            "[1, 2, 3]",
            json.dumps("a string"),
            tool_start("Skill"),
            input_delta(json.dumps({"skill": COMMAND})),
        ]
        self.assertTrue(claude.decide_from_events(lines, COMMAND))

    def test_no_decisive_event_returns_none(self):
        self.assertIsNone(claude.decide_from_events(["noise", ""], COMMAND))
        self.assertIsNone(claude.decide_from_events([], COMMAND))


class PackageTests(unittest.TestCase):
    def setUp(self):
        holder = tempfile.TemporaryDirectory()
        self.addCleanup(holder.cleanup)
        self.root = Path(holder.name)
        self.skill_dir = self.root / "MySkill"
        files = {
            "SKILL.md": "---\nname: my-skill\ndescription: d\n---\n",
            "scripts/run.py": "print('hi')\n",
            "scripts/__pycache__/run.cpython-311.pyc": "bytes",
            "scripts/stale.pyc": "bytes",
            "node_modules/pkg/index.js": "module.exports = 1\n",
            "evals/set.json": "[]",
            ".DS_Store": "x",
            "assets/.DS_Store": "x",
            "assets/page.html": "<p>hi</p>",
            "nested/evals/keep.txt": "kept",
            "deep/node_modules/x.txt": "dropped",
        }
        for relative, text in files.items():
            path = self.skill_dir / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")

    def test_archive_paths_and_exclusions(self):
        output = self.root / "dist" / "nested" / "MySkill.skill"
        returned = claude.package(self.skill_dir, output)
        self.assertEqual(returned, output)
        self.assertTrue(output.is_file())
        with zipfile.ZipFile(output) as archive:
            names = archive.namelist()
            self.assertEqual(
                names,
                sorted(
                    [
                        "MySkill/SKILL.md",
                        "MySkill/scripts/run.py",
                        "MySkill/assets/page.html",
                        "MySkill/nested/evals/keep.txt",
                    ]
                ),
            )
            for name in names:
                self.assertEqual(archive.getinfo(name).compress_type, zipfile.ZIP_DEFLATED)
            self.assertEqual(archive.read("MySkill/nested/evals/keep.txt"), b"kept")

    def test_is_packaged_rules(self):
        self.assertTrue(claude.is_packaged(Path("SKILL.md")))
        self.assertFalse(claude.is_packaged(Path("a/__pycache__/b.py")))
        self.assertFalse(claude.is_packaged(Path("node_modules/x.js")))
        self.assertFalse(claude.is_packaged(Path("evals/x.json")))
        self.assertTrue(claude.is_packaged(Path("docs/evals/x.json")))
        self.assertFalse(claude.is_packaged(Path("sub/.DS_Store")))
        self.assertFalse(claude.is_packaged(Path("sub/mod.pyc")))


class FakePopen:
    """Stands in for subprocess.Popen; emits a script built from the command file."""

    instances: ClassVar[list] = []
    script = staticmethod(lambda command_name: [])

    def __init__(self, command, cwd=None, **kwargs):
        self.command = command
        self.cwd = cwd
        self.kwargs = kwargs
        commands_dir = Path(cwd) / ".claude" / "commands"
        files = list(commands_dir.glob("*.md"))
        self.command_file = files[0] if files else None
        self.command_name = self.command_file.stem if self.command_file else ""
        self.file_text = self.command_file.read_text(encoding="utf-8") if self.command_file else ""
        self.stdout = io.StringIO("\n".join(FakePopen.script(self.command_name)) + "\n")
        self.killed = False
        FakePopen.instances.append(self)

    def poll(self):
        return 0

    def kill(self):
        self.killed = True

    def wait(self, timeout=None):
        return 0


class ProbeTriggerTests(unittest.TestCase):
    def setUp(self):
        holder = tempfile.TemporaryDirectory()
        self.addCleanup(holder.cleanup)
        self.project_root = holder.name
        FakePopen.instances = []
        patcher = mock.patch.object(subprocess, "Popen", FakePopen)
        patcher.start()
        self.addCleanup(patcher.stop)

    def commands_dir(self) -> Path:
        return Path(self.project_root) / ".claude" / "commands"

    def test_picked_when_skill_tool_names_the_command(self):
        FakePopen.script = staticmethod(
            lambda name: [
                tool_start("Skill"),
                input_delta(json.dumps({"skill": name})),
                BLOCK_STOP,
                RESULT,
            ]
        )
        with mock.patch.dict(os.environ, {"CLAUDECODE": "1"}):
            picked = claude.probe_trigger(
                "please help", "demo-skill", 'Line one: "quoted"\nLine two', self.project_root, 30, model="model-x"
            )
        self.assertTrue(picked)
        fake = FakePopen.instances[0]
        self.assertEqual(fake.cwd, self.project_root)
        self.assertEqual(fake.command[:3], ["claude", "-p", "please help"])
        self.assertIn("--output-format", fake.command)
        self.assertIn("stream-json", fake.command)
        self.assertIn("--include-partial-messages", fake.command)
        self.assertIn("--no-session-persistence", fake.command)
        self.assertEqual(fake.command[-2:], ["--model", "model-x"])
        self.assertNotIn("CLAUDECODE", fake.kwargs["env"])
        self.assertTrue(fake.command_name.startswith("demo-skill-"))
        self.assertIn("description: >-", fake.file_text)
        self.assertIn('  Line one: "quoted"\n  Line two\n', fake.file_text)
        self.assertEqual(list(self.commands_dir().glob("*.md")), [])

    def test_not_picked_when_other_tool_runs_first(self):
        FakePopen.script = staticmethod(lambda name: [tool_start("Bash"), RESULT])
        picked = claude.probe_trigger("x", "demo-skill", "d", self.project_root, 30)
        self.assertFalse(picked)
        self.assertNotIn("--model", FakePopen.instances[0].command)
        self.assertEqual(list(self.commands_dir().glob("*.md")), [])

    def test_timeout_means_not_picked_and_file_removed(self):
        FakePopen.script = staticmethod(
            lambda name: [tool_start("Skill"), input_delta(json.dumps({"skill": name}))]
        )
        picked = claude.probe_trigger("x", "demo-skill", "d", self.project_root, 0)
        self.assertFalse(picked)
        self.assertEqual(list(self.commands_dir().glob("*.md")), [])

    def test_command_file_removed_when_launch_fails(self):
        def explode(*args, **kwargs):
            raise OSError("no such program")

        with mock.patch.object(subprocess, "Popen", explode), self.assertRaises(OSError):
            claude.probe_trigger("x", "demo-skill", "d", self.project_root, 30)
        self.assertEqual(list(self.commands_dir().glob("*.md")), [])


class InvokeTests(unittest.TestCase):
    def test_invoke_builds_command_and_returns_stdout(self):
        completed = subprocess.CompletedProcess(args=[], returncode=0, stdout="reply", stderr="")
        with mock.patch.object(subprocess, "run", return_value=completed) as run, mock.patch.dict(
            os.environ, {"CLAUDECODE": "1"}
        ):
            reply = claude.invoke("the prompt", model="model-x", extra_args=["--extra"], timeout=12)
        self.assertEqual(reply, "reply")
        args, kwargs = run.call_args
        self.assertEqual(
            args[0],
            [
                "claude",
                "-p",
                "--output-format",
                "text",
                "--tools",
                "",
                "--no-session-persistence",
                "--model",
                "model-x",
                "--extra",
            ],
        )
        self.assertEqual(kwargs["input"], "the prompt")
        self.assertEqual(kwargs["timeout"], 12)
        self.assertNotIn("CLAUDECODE", kwargs["env"])

    def test_invoke_raises_on_failure(self):
        completed = subprocess.CompletedProcess(args=[], returncode=3, stdout="", stderr="bad things")
        with mock.patch.object(subprocess, "run", return_value=completed), self.assertRaises(RuntimeError) as caught:
            claude.invoke("p")
        self.assertIn("3", str(caught.exception))
        self.assertIn("bad things", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
