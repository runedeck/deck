#!/usr/bin/env bash
# Copy a script into the guest and run it as root, logging inside the guest.
# Usage: run-in-guest.sh <vm> <host-script> <guest-log>
set -uo pipefail
readonly vm=$1 script=$2 log=$3
name=$(basename "$script")
readonly name

# prlctl exec fails now and then with "PrlJob_GetResult: Invalid argument"
# or "Unable to open new session". Retry each call; every call is idempotent.
guest() {
    local attempt
    for attempt in 1 2 3 4 5; do
        prlctl exec "$vm" "$1" && return 0
        echo "exec attempt $attempt failed, retrying" >&2
        sleep 3
    done
    return 1
}

# prlctl exec joins its arguments into one guest shell command line, and a
# long line fails, so the script travels as base64 in numbered chunks.
encoded=$(base64 < "$script" | tr -d '\n')
guest "install -d -m 0700 /root/$name.parts" || exit 1
part=0
for ((offset = 0; offset < ${#encoded}; offset += 900)); do
    guest "printf %s ${encoded:offset:900} > /root/$name.parts/$(printf %04d "$part")" || exit 1
    part=$((part + 1))
done
guest "cat /root/$name.parts/* | base64 -d > /root/$name && chmod 0700 /root/$name && sha256sum /root/$name" || exit 1
shasum -a 256 "$script"

status=0
prlctl exec "$vm" "bash /root/$name > $log 2>&1" || status=$?
guest "tail -n 25 $log"
echo "exit $status"
exit "$status"
