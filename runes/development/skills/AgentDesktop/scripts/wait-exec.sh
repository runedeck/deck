#!/usr/bin/env bash
# Retry prlctl exec until it answers, then print the guest machine id and address.
# Usage: wait-exec.sh <vm> <max-seconds>
set -uo pipefail
readonly vm=$1 limit=$2
start=$SECONDS
until prlctl exec "$vm" /usr/bin/true >/dev/null 2>&1; do
    [ $((SECONDS - start)) -lt "$limit" ] || { echo "$vm: exec still failing after $limit s"; exit 1; }
    sleep 5
done
echo "$vm: exec answered after $((SECONDS - start)) s more"
prlctl exec "$vm" "cat /etc/machine-id; ip -4 -o addr show scope global | cut -c1-40"
