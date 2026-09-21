#!/bin/sh
# Block until a detached job ends; run as: wait.sh <name> [lines]
# Polls for $STATE/<name>.rc (written by start.sh when the command
# exits), then prints the last <lines> of the log (default 20) and exits
# with the job's own exit code. A caller with its own timeout can call
# this repeatedly: each call resumes the same wait, nothing is lost.
set -u
name="${1:?usage: wait.sh <name> [lines]}"
lines="${2:-20}"
state="${JOB_STATE:-${XDG_STATE_HOME:-$HOME/.local/state}/detached-job}"
rc="$state/$name.rc"
log="$state/$name.log"
pidf="$state/$name.pid"
[ -f "$log" ] || { echo "wait.sh: no job '$name'" >&2; exit 2; }
# Liveness is best effort. A sandboxed caller may be refused both the
# signal (kill -0) and the process table (ps) for a job outside the
# sandbox; only a definite "no such process" counts as dead.
alive() {
    kill -0 "$1" 2>/dev/null && return 0
    ps -p "$1" >/dev/null 2>&1
    r=$?
    [ "$r" -eq 0 ] && return 0
    [ "$r" -eq 1 ] && return 1
    return 0
}
while [ ! -f "$rc" ]; do
    if [ -f "$pidf" ] && ! alive "$(cat "$pidf")"; then
        # Process is gone but wrote no rc: killed from outside.
        echo "wait.sh: '$name' died without an exit code" >&2
        tail -n "$lines" "$log"
        exit 137
    fi
    sleep 5
done
tail -n "$lines" "$log"
code=$(cat "$rc")
printf '[%s exited %s]\n' "$name" "$code"
exit "$code"
