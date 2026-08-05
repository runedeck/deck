"""Claude Code harness adapter.

Adapter contract — a harness module registered in scripts/harness must expose:

    invoke(prompt, model=None, extra_args=None) -> str
        Run one non-interactive model call and return its stdout text.
        The call must not persist sessions and must not have tool access.

    package(skill_dir, output_path) -> Path
        Build the harness's distributable skill archive at output_path
        and return that path.

A new harness (codex.py, gemini.py) is added by implementing these two
functions in a new module and registering it in scripts/harness/__init__.py.
An adapter may expose extra capabilities beyond the contract (this one adds
probe_trigger for trigger evals); callers must feature-check those with
getattr before relying on them.
"""

import json
import os
import select
import subprocess
import time
import uuid
import zipfile
from pathlib import Path

PACKAGE_EXCLUDE_DIRS = {"__pycache__", "node_modules"}
PACKAGE_EXCLUDE_GLOBS = ("*.pyc",)
PACKAGE_EXCLUDE_FILES = {".DS_Store"}
PACKAGE_ROOT_EXCLUDE_DIRS = {"evals"}


def _subprocess_env() -> dict:
    """Environment for nested `claude -p` calls.

    Removes the CLAUDECODE variable so `claude -p` can run inside a Claude
    Code session. The guard exists for interactive terminal conflicts;
    programmatic subprocess usage is safe.
    """
    return {key: value for key, value in os.environ.items() if key != "CLAUDECODE"}


def invoke(prompt: str, model: str | None = None, extra_args: list[str] | None = None, timeout: int = 300) -> str:
    """Run `claude -p` with the prompt on stdin and return its stdout text.

    The prompt goes over stdin (not argv) because it can embed full skill
    bodies and exceed comfortable argv length. Safety flags disable tool
    access and session persistence.
    """
    command = [
        "claude",
        "-p",
        "--output-format", "text",
        "--tools", "",
        "--no-session-persistence",
    ]
    if model:
        command.extend(["--model", model])
    if extra_args:
        command.extend(extra_args)

    result = subprocess.run(
        command,
        input=prompt,
        capture_output=True,
        text=True,
        env=_subprocess_env(),
        timeout=timeout,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"claude -p exited {result.returncode}\nstderr: {result.stderr}"
        )
    return result.stdout


def _should_exclude_from_package(relative_path: Path) -> bool:
    parts = relative_path.parts
    if any(part in PACKAGE_EXCLUDE_DIRS for part in parts):
        return True
    # relative_path is relative to skill_dir.parent, so parts[0] is the skill
    # directory name and parts[1] (if present) is the first subdirectory.
    if len(parts) > 1 and parts[1] in PACKAGE_ROOT_EXCLUDE_DIRS:
        return True
    name = relative_path.name
    if name in PACKAGE_EXCLUDE_FILES:
        return True
    return any(relative_path.match(pattern) for pattern in PACKAGE_EXCLUDE_GLOBS)


def package(skill_dir: Path, output_path: Path) -> Path:
    """Package a skill directory into a .skill archive (claude.ai upload format).

    The archive is a zip of the skill directory, rooted at the directory name,
    with build artifacts and eval material excluded.
    """
    skill_dir = Path(skill_dir).resolve()
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for file_path in sorted(skill_dir.rglob("*")):
            if not file_path.is_file():
                continue
            archive_name = file_path.relative_to(skill_dir.parent)
            if _should_exclude_from_package(archive_name):
                continue
            archive.write(file_path, archive_name)

    return output_path


def probe_trigger(
    query: str,
    skill_name: str,
    skill_description: str,
    project_root: str,
    timeout: int,
    model: str | None = None,
) -> bool:
    """Run a single query and return whether the skill was triggered.

    Creates a command file in <project_root>/.claude/commands/ so it appears
    in Claude's available_skills list, then runs `claude -p` with the raw
    query. Uses --include-partial-messages to detect triggering early from
    stream events (content_block_start) rather than waiting for the full
    assistant message, which only arrives after tool execution.

    The project_root must be an isolated directory owned by the caller,
    never a real repository.
    """
    unique_id = uuid.uuid4().hex[:8]
    command_name = f"{skill_name}-skill-{unique_id}"
    commands_dir = Path(project_root) / ".claude" / "commands"
    command_file = commands_dir / f"{command_name}.md"

    try:
        commands_dir.mkdir(parents=True, exist_ok=True)
        # Use YAML block scalar to avoid breaking on quotes in description
        indented_description = "\n  ".join(skill_description.split("\n"))
        command_file.write_text(
            f"---\n"
            f"description: |\n"
            f"  {indented_description}\n"
            f"---\n\n"
            f"# {skill_name}\n\n"
            f"This skill handles: {skill_description}\n",
            encoding="utf-8",
        )

        command = [
            "claude",
            "-p", query,
            "--output-format", "stream-json",
            "--verbose",
            "--include-partial-messages",
            "--no-session-persistence",
        ]
        if model:
            command.extend(["--model", model])

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            cwd=project_root,
            env=_subprocess_env(),
        )

        triggered = False
        start_time = time.time()
        buffer = ""
        pending_tool_name = None
        accumulated_json = ""

        try:
            while time.time() - start_time < timeout:
                if process.poll() is not None:
                    remaining = process.stdout.read()
                    if remaining:
                        buffer += remaining.decode("utf-8", errors="replace")
                    break

                ready, _, _ = select.select([process.stdout], [], [], 1.0)
                if not ready:
                    continue

                chunk = os.read(process.stdout.fileno(), 8192)
                if not chunk:
                    break
                buffer += chunk.decode("utf-8", errors="replace")

                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    line = line.strip()
                    if not line:
                        continue

                    try:
                        event = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    # Early detection via stream events
                    if event.get("type") == "stream_event":
                        stream_event = event.get("event", {})
                        stream_event_type = stream_event.get("type", "")

                        if stream_event_type == "content_block_start":
                            content_block = stream_event.get("content_block", {})
                            if content_block.get("type") == "tool_use":
                                tool_name = content_block.get("name", "")
                                if tool_name in ("Skill", "Read"):
                                    pending_tool_name = tool_name
                                    accumulated_json = ""
                                else:
                                    return False

                        elif stream_event_type == "content_block_delta" and pending_tool_name:
                            delta = stream_event.get("delta", {})
                            if delta.get("type") == "input_json_delta":
                                accumulated_json += delta.get("partial_json", "")
                                if command_name in accumulated_json:
                                    return True

                        elif stream_event_type in ("content_block_stop", "message_stop"):
                            if pending_tool_name:
                                return command_name in accumulated_json
                            if stream_event_type == "message_stop":
                                return False

                    # Fallback: full assistant message
                    elif event.get("type") == "assistant":
                        message = event.get("message", {})
                        for content_item in message.get("content", []):
                            if content_item.get("type") != "tool_use":
                                continue
                            tool_name = content_item.get("name", "")
                            tool_input = content_item.get("input", {})
                            skill_triggered = (
                                tool_name == "Skill"
                                and command_name in tool_input.get("skill", "")
                            )
                            read_triggered = (
                                tool_name == "Read"
                                and command_name in tool_input.get("file_path", "")
                            )
                            return skill_triggered or read_triggered

                    elif event.get("type") == "result":
                        return triggered
        finally:
            # Clean up process on any exit path (return, exception, timeout)
            if process.poll() is None:
                process.kill()
                process.wait()

        return triggered
    finally:
        if command_file.exists():
            command_file.unlink()
