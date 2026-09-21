#!/usr/bin/env bash
# Driver for a recorded acceptance proof of the proof-page-handover
# specification: the AcceptanceTesting page generator, run on a real cast.
# shellcheck source=../driver.sh
. "$(dirname "$0")/../driver.sh"

printf '\033[2J\033[H'

ROOT=$(cd "$(dirname "$0")/../../.." && pwd) || exit 1
RUNE=${RUNE:-rune}
export RUNE
PLAYER=${CAST_PLAYER:-/Users/N4M3Z/Developer/N4M3Z/html-tools/runtime/cast-player.js}
FILED=${FILED_PROOF:-/Users/N4M3Z/Developer/runedeck/skeleton/docs/proofs/trusted-key-anchor}
PROOF_HOME=$(mktemp -d "${TMPDIR:-/tmp}/proof-page-handover.XXXXXX")
trap 'command rm -rf "$PROOF_HOME"' EXIT
cd "$PROOF_HOME" || exit 1
mkdir -p docs/proofs/trusted-key-anchor vendor
rsync -a "$FILED/proof.cast" docs/proofs/trusted-key-anchor/proof.cast
rsync -a "$PLAYER" vendor/cast-player.js
GEN="$ROOT/runes/core/skills/AcceptanceTesting/scripts/proof-page.py"
export TYPE_DELAY=0 PAUSE_AFTER_COMMENT=0 PAUSE_AFTER_OUTPUT=0

scenario "Proof finished"
comment "After the recording and the transcript check, the generator builds the page; the handover is its path."
run "python3 proof-page.py --title 'Pinned Signers' --player vendor/cast-player.js --cast trusted-key-anchor=docs/proofs/trusted-key-anchor/proof.cast --caption trusted-key-anchor='KEYS pins a signer by fingerprint' --meta trusted-key-anchor='skeleton 2b5762ef' --out proof-set.html" \
    "python3 '$GEN' --title 'Pinned Signers' --player vendor/cast-player.js --cast trusted-key-anchor=docs/proofs/trusted-key-anchor/proof.cast --caption trusted-key-anchor='KEYS pins a signer by fingerprint' --meta trusted-key-anchor='skeleton 2b5762ef' --out proof-set.html"
expect "proof-set.html \(1 casts\)"
run "grep -c 'CastPlayer.attach(document' proof-set.html"
expect "^1$"

scenario "Owner asks where the proof is"
comment "The skill's answer is the page path, never the GIF alone."
run "grep -o 'A message that names the GIF alone is an unfinished handover' $ROOT/runes/core/skills/AcceptanceTesting/SKILL.md"
expect "unfinished handover"

scenario "Cast with five scenes"
comment "The scene list comes from the cast's own Scenario lines, in playback order."
run "grep -o '<li>[^<]*' proof-set.html | sed 's/<li>//'"
expect "^KEYS names signers by fingerprint$"
expect "^verify-seal builds its keyring through the resolver$"
run "grep -o '<li>' proof-set.html | wc -l | tr -d ' '"
expect "^5$"
