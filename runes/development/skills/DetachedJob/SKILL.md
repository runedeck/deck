---
name: DetachedJob
description: "Run a long command as a detached job that no harness tool timeout, sandbox kill, terminal close, or session exit can stop, and collect its log and exit code afterwards. USE WHEN a build, test suite, download, or install runs longer than the shell tool allows, a background command was killed when the session ended, or a command must survive a timeout. NOT FOR quick commands, interactive programs, or services that must stay up after the work ends (use launchd or systemd)."
license: EUPL-1.2
compatibility: "POSIX sh plus perl (for setsid). Tested on macOS; Linux works the same."
metadata:
    version: 0.1.0
---

# DetachedJob

A harness shell tool kills its child process group when a timeout fires or the session ends. A job that leaves that process group survives both. This skill starts the job in its own session, keeps the log and exit code in files, and waits on the exit-code file instead of the process.

## Prerequisites

- `perl` on PATH. The start script calls `setsid` through perl, because macOS has no `setsid` binary.
- A writable state directory. Default: `${XDG_STATE_HOME:-~/.local/state}/detached-job`. Set `JOB_STATE` to move it.
- The absolute path of this skill's `scripts/` directory.

## Constraints

- One name per job. A second `start` with a live job of the same name is refused.
- The command must not need a terminal. stdin is `/dev/null`.
- A sandboxed caller cannot signal a job that runs outside the sandbox. Liveness comes from `ps`, never from `kill -0`.
- The scripts never delete a log. Old logs are the caller's to remove.
- A job that must outlive a reboot is a service, not a job.

## Instructions

### Start

```sh
sh scripts/start.sh <name> -- <command> [args...]
```

Prints the pid and the log path. The wrapper records the command's exit code in `<state>/<name>.rc` when it ends.

If the command needs to run outside a sandbox (it links, signs, or downloads through paths the sandbox denies), start it with the harness's unsandboxed option. The start returns at once, so the unsandboxed window is the start call alone.

### Wait

```sh
sh scripts/wait.sh <name> [lines]
```

Blocks until the rc file exists, prints the last `lines` of the log (default 20), and exits with the job's own code. When the tool timeout cuts the wait short, call it again: nothing is lost, the job kept running.

For a harness that offers a file monitor, watch the log for phase markers and the rc file for the end instead of blocking:

```sh
tail -f <state>/<name>.log | grep --line-buffered -E '^==>|error|Finished'
```

### Read

```sh
sh scripts/log.sh <name>        # whole log
sh scripts/log.sh <name> -f     # follow until the job ends
```

## Verification

Run the smoke test. It starts a two-second job that exits 3, waits, and checks that `wait.sh` returns 3 and prints both lines.

```sh
JOB_STATE=$(mktemp -d) sh scripts/start.sh smoke -- sh -c 'echo hi; sleep 2; echo bye; exit 3'
```

Then `wait.sh smoke` in the same `JOB_STATE`. Expected: `hi`, `bye`, `[smoke exited 3]`, exit status 3.

## Troubleshooting

- `died without an exit code`: the process is gone and wrote no rc. Something outside killed it, or the machine rebooted. Read the log, then start again.
- `is still running`: a job with that name is live. Pick another name or wait for it.
- `setsid: Operation not permitted`: the caller made the start script a process group leader. Run it through `sh scripts/start.sh`, not through `exec`.
- The job cannot write its state: the state directory is read-only or sandbox-denied. Set `JOB_STATE` to a writable path.

## References

- Personal deployment: the dotfiles `sd job start|wait|log` commands are these scripts under the `sd` dispatcher.
- POSIX `setsid(2)`: a new session detaches the process from the caller's controlling terminal and process group.
