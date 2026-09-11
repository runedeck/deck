"""Emit bounded guard discovery evidence without executing a shell."""

import json
import os
import selectors
import shutil
import signal
import subprocess
import time

SCHEMA = "safetyfirst-guard-probe/v1"
DEADLINE_SECONDS = 4.5
CAPTURE_BYTES = 512
OUTPUT_BYTES = 1024


def bounded_text(raw, limit):
    """Keep an escaped JSON string within its assigned byte budget."""
    text = raw.decode("utf-8", errors="replace")
    original = text
    while len(json.dumps(text, ensure_ascii=True).encode("ascii")) > limit:
        text = text[:-1]
    return text, text != original


def stop_group(process):
    """Kill the probe group, including descendants that retain its pipes."""
    process.poll()
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass


def capture_version(executable, deadline):
    output = {"stdout": bytearray(), "stderr": bytearray()}
    outcome = {"exit_code": None, "timed_out": False, "truncated": False}
    cleanup_failed = False
    process = subprocess.Popen(
        [executable, "--version"],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        start_new_session=True,
    )
    try:
        with selectors.DefaultSelector() as selector:
            for name, stream in (("stdout", process.stdout), ("stderr", process.stderr)):
                os.set_blocking(stream.fileno(), False)
                selector.register(stream, selectors.EVENT_READ, name)
            while selector.get_map():
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    outcome["timed_out"] = True
                    break
                for key, _ in selector.select(remaining):
                    data = os.read(key.fileobj.fileno(), CAPTURE_BYTES + 1)
                    if not data:
                        selector.unregister(key.fileobj)
                        continue
                    room = CAPTURE_BYTES - sum(map(len, output.values()))
                    output[key.data].extend(data[:room])
                    if len(data) > room:
                        outcome["truncated"] = True
                        break
                if outcome["truncated"]:
                    break
            if not outcome["timed_out"] and not outcome["truncated"]:
                try:
                    process.wait(timeout=max(0, deadline - time.monotonic()))
                except subprocess.TimeoutExpired:
                    outcome["timed_out"] = True
    finally:
        try:
            stop_group(process)
        except OSError:
            cleanup_failed = True
        process.stdout.close()
        process.stderr.close()
        try:
            process.wait(timeout=0.2)
        except subprocess.TimeoutExpired:
            outcome["timed_out"] = True
        outcome["exit_code"] = process.returncode
    return outcome, output, cleanup_failed


def probe():
    started = time.monotonic()
    report = {
        "schema": SCHEMA,
        "lookup": "unknown",
        "version": "unknown",
        "process": {"exit_code": None, "timed_out": False, "truncated": False},
        "payload": {"path": "", "stdout": "", "stderr": ""},
        "error": None,
    }
    if os.name != "posix":
        report["error"] = "unsupported_process_boundary"
        return report
    try:
        executable = shutil.which("dcg")
    except (OSError, ValueError):
        report["error"] = "lookup_failed"
        return report
    if executable is None:
        report["lookup"] = "absent_from_path"
        return report
    report["lookup"] = "present"
    report["payload"]["path"], path_truncated = bounded_text(os.fsencode(executable), 192)
    if path_truncated:
        report["lookup"] = "unknown"
        report["process"]["truncated"] = True
        report["error"] = "path_limit"
        return report
    if time.monotonic() - started >= DEADLINE_SECONDS:
        report["process"]["timed_out"] = True
        report["error"] = "deadline"
        return report
    try:
        outcome, output, cleanup_failed = capture_version(executable, started + DEADLINE_SECONDS)
    except (OSError, ValueError, subprocess.SubprocessError):
        report["error"] = "version_probe_failed"
        return report
    report["process"] = outcome
    for name, budget in (("stdout", 256), ("stderr", 128)):
        text, truncated = bounded_text(output[name], budget)
        report["payload"][name] = text
        outcome["truncated"] = outcome["truncated"] or truncated
    if cleanup_failed:
        report["error"] = "cleanup_failed"
    elif outcome["timed_out"]:
        report["error"] = "deadline"
    elif outcome["truncated"]:
        report["error"] = "output_limit"
    elif outcome["exit_code"] != 0:
        report["error"] = "version_exit_failed"
    elif not report["payload"]["stdout"].strip():
        report["error"] = "empty_version"
    else:
        report["version"] = "observed"
    return report


def main():
    encoded = json.dumps(probe(), ensure_ascii=True, separators=(",", ":")) + "\n"
    if len(encoded.encode("ascii")) > OUTPUT_BYTES:
        encoded = json.dumps({"schema": SCHEMA, "error": "envelope_limit"}) + "\n"
    print(encoded, end="")


if __name__ == "__main__":
    main()
