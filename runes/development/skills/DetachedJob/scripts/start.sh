#!/bin/sh
# Start a long command detached from the caller; run as:
#   start.sh <name> -- <command> [args...]
# The job gets its own session and process group (perl setsid: macOS
# ships no setsid binary), stdin from /dev/null, and stdout+stderr in
# $STATE/<name>.log. When it ends, $STATE/<name>.rc holds the exit
# code. No harness tool timeout, terminal close, or session exit can
# reach it: those kill the caller's process group, and the job left it.
# Companion: wait.sh <name> blocks on the rc file; log.sh <name>
# tails the log.
# STATE defaults to ${XDG_STATE_HOME:-~/.local/state}/detached-job; JOB_STATE
# overrides it (tests, scripting).
set -u
name="${1:?usage: start.sh <name> -- <command> [args...]}"
shift
[ "${1:-}" = "--" ] && shift
[ $# -gt 0 ] || { echo 'start.sh: no command given' >&2; exit 2; }
case "$name" in
    */*|.*|'') echo "start.sh: bad job name '$name'" >&2; exit 2 ;;
esac
state="${JOB_STATE:-${XDG_STATE_HOME:-$HOME/.local/state}/detached-job}"
mkdir -p "$state" || exit 1
log="$state/$name.log"
rc="$state/$name.rc"
pidf="$state/$name.pid"
# A live job of the same name is refused. Only a definite "no such
# process" clears the way: a sandboxed caller may be refused the signal
# and the process table for a job outside the sandbox.
alive() {
    kill -0 "$1" 2>/dev/null && return 0
    ps -p "$1" >/dev/null 2>&1
    r=$?
    [ "$r" -eq 0 ] && return 0
    [ "$r" -eq 1 ] && return 1
    [ -f "$rc" ] && return 1
    return 0
}
# The liveness check and the state files must move as one step, or two
# concurrent starts of the same name both pass the check and share one
# log, pid, and rc. mkdir is atomic on every filesystem; the directory is
# the lock and lives as long as the job's state files do.
lock="$state/$name.lock"
if ! mkdir "$lock" 2>/dev/null; then
    if [ -f "$pidf" ] && alive "$(cat "$pidf")"; then
        echo "start.sh: '$name' is still running (pid $(cat "$pidf"))" >&2
        exit 1
    fi
    # A stale lock from a finished or dead job. Take it over.
    rmdir "$lock" 2>/dev/null
    mkdir "$lock" 2>/dev/null || { echo "start.sh: '$name' is being started by another caller" >&2; exit 1; }
fi
if [ -f "$pidf" ] && alive "$(cat "$pidf")"; then
    echo "start.sh: '$name' is still running (pid $(cat "$pidf"))" >&2
    exit 1
fi
rm -f "$rc"
: > "$log"
# The wrapper runs the command, records its exit code, and exits. perl
# calls setsid before exec so the wrapper is the leader of a new session.
# The rc file is written under a temporary name and renamed, so a reader
# never sees a partial file, and the lock directory goes with it.
perl -e 'use POSIX qw(setsid); setsid() or die "setsid: $!"; exec @ARGV or die "exec: $!"' -- \
    /bin/sh -c 'cmd_rc="$1"; cmd_lock="$2"; shift 2; "$@"; r=$?; echo "$r" > "$cmd_rc.tmp" && mv -f "$cmd_rc.tmp" "$cmd_rc"; rmdir "$cmd_lock" 2>/dev/null' _ "$rc" "$lock" "$@" \
    < /dev/null >> "$log" 2>&1 &
echo $! > "$pidf"
printf 'started %s (pid %s)\nlog: %s\n' "$name" "$!" "$log"
exit 0
