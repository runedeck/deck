#!/usr/bin/env bash
# Create a throwaway agent VM: a linked clone of the template VM at its newest
# snapshot, named after a free Warhammer 40,000 title or office, with the
# purpose in the VM description and the guest hostname synced to the name.
# Usage: new-agent-vm.sh [purpose words...]
# Names never get numbers: when the pool is used up, add names to it. The
# pool leaves out the five Grok Bot agent names (archmagos, administratum,
# seneschal, explorator and enginseer) so a VM never shares an agent's name.
set -euo pipefail
readonly base="STC"
readonly pool="castellan commissar inquisitor interrogator astropath rogue-trader
lexmechanic logis magos fabricator princeps ordinatus techmarine apothecary
chaplain reclusiarch lexicanum codicier epistolary ecclesiarch confessor
palatine canoness celestian dialogus dogmata imagifier arbitrator custodian
tempestor praetor centurion myrmidon thallax servitor cogitator skitarius
vanguard ranger onager dominus manipulus kataphron hospitaller chirurgeon
kastelan navigator"
purpose=${*:-unspecified}

# The snapshot marked with * is the newest one, the base's current state.
snapshot=$(prlctl snapshot-list "$base" | grep -o '\*{[^}]*}' | tr -d '*')
[ -n "$snapshot" ] || { echo "no current snapshot on $base" >&2; exit 1; }

taken=$(prlctl list -a -o name)
free=()
for candidate in $pool; do
    grep -qx "$candidate" <<<"$taken" || free+=("$candidate")
done
if [ "${#free[@]}" -eq 0 ]; then
    echo "every name in the pool is taken; add 40k names to the pool in $0" >&2
    exit 1
fi
name=${free[RANDOM % ${#free[@]}]}

prlctl clone "$base" --name "$name" --linked --id "$snapshot" >/dev/null
prlctl set "$name" --description "Throwaway agent VM. Linked clone of $base at snapshot $snapshot. Created $(date -u +%F). Purpose: $purpose." >/dev/null
prlctl set "$name" --sync-vm-hostname on >/dev/null
echo "$name"
