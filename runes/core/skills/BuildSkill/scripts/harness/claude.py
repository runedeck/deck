"""Harness adapter for Claude Code.

A harness adapter exposes three functions:

- ``invoke`` runs the agent on a prompt with every tool switched off and
  returns the reply text.
- ``package`` zips a skill directory for distribution.
- ``probe_trigger`` checks whether one user request makes the agent pick a
  skill that is exposed only through its name and description.

The probe exposes the skill as a project command file, streams the agent's
events, and stops at the first event that settles the answer.
"""

import json
import os
import queue
import secrets
import subprocess
import threading
import time
import zipfile
from collections.abc import Iterable, Iterator
from pathlib import Path

CLI = "claude"

# Tools whose invocation can mean "the agent opened the skill".
SKILL_OPENING_TOOLS = frozenset({"Skill", "Read"})

_SKIPPED_DIR_PARTS = frozenset({"__pycache__", "node_modules"})
_SKIPPED_FILE_NAMES = frozenset({".DS_Store"})
_SKIPPED_SUFFIXES = frozenset({".pyc"})
_TOP_LEVEL_SKIPPED_DIRS = frozenset({"evals"})


def _child_environment() -> dict[str, str]:
    """Copy the environment without the marker that blocks nested runs."""
    env = dict(os.environ)
    env.pop("CLAUDECODE", None)
    return env


def invoke(
    prompt: str,
    model: str | None = None,
    extra_args: list[str] | None = None,
    timeout: int = 300,
) -> str:
    """Run the agent on ``prompt`` with no tools and return its reply."""
    command = [
        CLI,
        "-p",
        "--output-format",
        "text",
        "--tools",
        "",
        "--no-session-persistence",
    ]
    if model:
        command.extend(["--model", model])
    if extra_args:
        command.extend(extra_args)

    completed = subprocess.run(
        command,
        input=prompt,
        capture_output=True,
        text=True,
        timeout=timeout,
        env=_child_environment(),
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"{CLI} exited with code {completed.returncode}: "
            f"{completed.stderr.strip()}"
        )
    return completed.stdout


def is_packaged(relative_path: Path) -> bool:
    """Tell whether a path inside the skill directory belongs in the archive."""
    parts = relative_path.parts
    if any(part in _SKIPPED_DIR_PARTS for part in parts):
        return False
    if len(parts) > 1 and parts[0] in _TOP_LEVEL_SKIPPED_DIRS:
        return False
    if relative_path.name in _SKIPPED_FILE_NAMES:
        return False
    return relative_path.suffix not in _SKIPPED_SUFFIXES


def package(skill_dir: Path, output_path: Path) -> Path:
    """Write a deflate-compressed zip of ``skill_dir`` to ``output_path``."""
    skill_dir = Path(skill_dir)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_resolved = output_path.resolve()

    files = sorted(
        (path for path in skill_dir.rglob("*") if path.is_file()),
        key=lambda path: path.relative_to(skill_dir).as_posix(),
    )
    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            if path.resolve() == output_resolved:
                continue
            relative = path.relative_to(skill_dir)
            if not is_packaged(relative):
                continue
            archive.write(path, arcname=(Path(skill_dir.name) / relative).as_posix())
    return output_path


def _command_file_text(skill_name: str, description: str) -> str:
    """Build a project command file whose frontmatter carries the description.

    A folded block scalar keeps quotes and colons in the description from
    breaking the frontmatter.
    """
    description_lines = description.splitlines() or [""]
    folded = "\n".join(f"  {line}" for line in description_lines)
    return (
        "---\n"
        "description: >-\n"
        f"{folded}\n"
        "---\n"
        f"Apply the {skill_name} skill to the request above.\n"
    )


def _parse_event(line: str) -> dict | None:
    """Decode one stream line; anything that is not a JSON object is ignored."""
    stripped = line.strip()
    if not stripped:
        return None
    try:
        event = json.loads(stripped)
    except json.JSONDecodeError:
        return None
    return event if isinstance(event, dict) else None


def _assistant_message_verdict(event: dict, command_name: str) -> bool | None:
    """Judge a whole assistant message by its first tool call, if any."""
    message = event.get("message") or {}
    for item in message.get("content") or []:
        if not isinstance(item, dict) or item.get("type") != "tool_use":
            continue
        tool_input = item.get("input") or {}
        if not isinstance(tool_input, dict):
            tool_input = {}
        tool = item.get("name")
        if tool == "Skill":
            return command_name in str(tool_input.get("skill", ""))
        if tool == "Read":
            return command_name in str(tool_input.get("file_path", ""))
        return False
    return None


def decide_from_events(lines: Iterable[str], command_name: str) -> bool | None:
    """Decide from stream-json lines whether the agent opened the command.

    Returns True or False at the first line that settles the question, and
    None when the lines run out before anything settles it. The function has
    no side effects, so tests can feed it canned lines.
    """
    watching_tool = False
    collected_input = ""

    for line in lines:
        event = _parse_event(line)
        if event is None:
            continue
        kind = event.get("type")

        if kind == "stream_event":
            inner = event.get("event") or {}
            inner_type = inner.get("type")

            if inner_type == "content_block_start":
                block = inner.get("content_block") or {}
                if block.get("type") != "tool_use":
                    continue
                if block.get("name") in SKILL_OPENING_TOOLS:
                    watching_tool = True
                    collected_input = ""
                    continue
                return False

            if inner_type == "content_block_delta" and watching_tool:
                delta = inner.get("delta") or {}
                if delta.get("type") == "input_json_delta":
                    collected_input += str(delta.get("partial_json") or "")
                    if command_name in collected_input:
                        return True
                continue

            if inner_type == "content_block_stop" and watching_tool:
                return command_name in collected_input

            if inner_type == "message_stop" and not watching_tool:
                return False

        elif kind == "assistant":
            verdict = _assistant_message_verdict(event, command_name)
            if verdict is not None:
                return verdict

        elif kind == "result":
            return False

    return None


def _lines_until(proc: subprocess.Popen, deadline: float) -> Iterator[str]:
    """Yield stdout lines until the stream ends or the deadline passes.

    A helper thread does the blocking reads so the caller never waits past
    the deadline on a quiet pipe.
    """
    stream = proc.stdout
    if stream is None:
        return
    pending: queue.Queue[str | None] = queue.Queue()

    def pump() -> None:
        try:
            for line in stream:
                pending.put(line)
        except (OSError, ValueError):
            pass
        finally:
            pending.put(None)

    threading.Thread(target=pump, daemon=True).start()
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return
        try:
            line = pending.get(timeout=remaining)
        except queue.Empty:
            return
        if line is None:
            return
        yield line


def _stop_process(proc: subprocess.Popen) -> None:
    if proc.poll() is not None:
        return
    proc.kill()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        pass


def probe_trigger(
    query: str,
    skill_name: str,
    skill_description: str,
    project_root: str,
    timeout: int,
    model: str | None = None,
) -> bool:
    """Return True when the agent opens the skill for ``query``.

    ``project_root`` is a throwaway directory owned by the caller. The skill
    is exposed there as a command file under a unique name so that a pick is
    unambiguous; the file is removed again on every exit path.
    """
    command_name = f"{skill_name}-{secrets.token_hex(4)}"
    commands_dir = Path(project_root) / ".claude" / "commands"
    commands_dir.mkdir(parents=True, exist_ok=True)
    command_file = commands_dir / f"{command_name}.md"
    command_file.write_text(
        _command_file_text(skill_name, skill_description), encoding="utf-8"
    )

    command = [
        CLI,
        "-p",
        query,
        "--output-format",
        "stream-json",
        "--verbose",
        "--include-partial-messages",
        "--no-session-persistence",
    ]
    if model:
        command.extend(["--model", model])

    proc: subprocess.Popen | None = None
    try:
        proc = subprocess.Popen(
            command,
            cwd=str(project_root),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=_child_environment(),
        )
        deadline = time.monotonic() + timeout
        verdict = decide_from_events(_lines_until(proc, deadline), command_name)
        return bool(verdict)
    finally:
        if proc is not None:
            _stop_process(proc)
        command_file.unlink(missing_ok=True)
