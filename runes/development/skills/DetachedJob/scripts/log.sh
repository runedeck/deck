#!/bin/sh
# Show a detached job's log; run as: log.sh <name> [-f]
# -f follows the log until the job's rc file appears, or until the job
# is gone without one (killed from outside), or until the follower is
# interrupted. The background tail is reaped on every exit.
set -u
name="${1:?usage: log.sh <name> [-f]}"
state="${JOB_STATE:-${XDG_STATE_HOME:-$HOME/.local/state}/detached-job}"
log="$state/$name.log"
rc="$state/$name.rc"
pidf="$state/$name.pid"
[ -f "$log" ] || { echo "log.sh: no job '$name'" >&2; exit 2; }
# Same liveness rule as wait.sh: only a definite "no such process"
# counts as dead, a sandboxed caller may be refused the process table.
alive() {
    kill -0 "$1" 2>/dev/null && return 0
    ps -p "$1" >/dev/null 2>&1
    r=$?
    [ "$r" -eq 0 ] && return 0
    [ "$r" -eq 1 ] && return 1
    return 0
}
if [ "${2:-}" = "-f" ]; then
    tail -n 20 -f "$log" &
    t=$!
    trap 'kill "$t" 2>/dev/null; wait "$t" 2>/dev/null; exit 130' INT TERM HUP
    while [ ! -f "$rc" ]; do
        if [ -f "$pidf" ] && ! alive "$(cat "$pidf")"; then
            kill "$t" 2>/dev/null; wait "$t" 2>/dev/null
            echo "log.sh: '$name' died without an exit code" >&2
            exit 137
        fi
        sleep 2
    done
    sleep 1
    kill "$t" 2>/dev/null; wait "$t" 2>/dev/null
    printf '[%s exited %s]\n' "$name" "$(cat "$rc")"
    exit 0
fi
cat "$log"
