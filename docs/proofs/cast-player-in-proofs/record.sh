#!/usr/bin/env bash
# Driver for a recorded acceptance proof of the cast-player-in-proofs
# specification. The player is html-tools runtime/cast-player.js; its
# parse, scenes, sceneAt, and controller run under node without a
# browser, which is how the page behavior is proven here.
# shellcheck source=../driver.sh
. "$(dirname "$0")/../driver.sh"

printf '\033[2J\033[H'

ROOT=$(cd "$(dirname "$0")/../../.." && pwd) || exit 1
RUNE=${RUNE:-rune}
export RUNE
PLAYER=${CAST_PLAYER:-/Users/N4M3Z/Developer/N4M3Z/html-tools/runtime/cast-player.js}
FILED=${FILED_PROOF:-/Users/N4M3Z/Developer/runedeck/skeleton/docs/proofs/trusted-key-anchor}
PROOF_HOME=$(mktemp -d "${TMPDIR:-/tmp}/cast-player-in-proofs.XXXXXX")
trap 'command rm -rf "$PROOF_HOME"' EXIT
cd "$PROOF_HOME" || exit 1
rsync -a "$PLAYER" cast-player.js
rsync -a "$FILED/proof.cast" proof.cast
cat > pause.js <<'EOF'
// Load the player the way the page does, then press Space mid-scene.
const fs = require("fs");
const CastPlayer = require("./cast-player.js");
const cast = CastPlayer.parse(fs.readFileSync("proof.cast", "utf8"));
const list = CastPlayer.scenes(cast);
const player = CastPlayer.controller(cast, () => {});
player.play(0);
const mid = (list[1].time + list[2].time) / 2;
player.seek(mid, 0);
player.toggle(0); // Space
const index = CastPlayer.sceneAt(list, player.time);
// A plain string: under FORCE_COLOR node would colour a bare boolean.
console.log("playing: " + String(player.playing));
console.log("Scene " + (index + 1) + " of " + list.length + ": " + list[index].title);
EOF
export TYPE_DELAY=0 PAUSE_AFTER_COMMENT=0 PAUSE_AFTER_OUTPUT=0

scenario "Reader pauses a proof"
comment "Space during the second scene stops playback, and the page names that scene by number and title."
run "node pause.js"
expect "^playing: false$"
expect "^Scene 2 of 5: The pin admits the key that carries it$"

scenario "Pull request shows the proof"
comment "A pull request body renders images only, so it embeds the GIF that stays committed beside the cast."
run "ls docs/proofs/trusted-key-anchor | grep -E 'proof\.(gif|cast)'" "ls $FILED | grep -E 'proof\.(gif|cast)'"
expect "proof.gif"
expect "proof.cast"
run "grep -o 'Keep the GIF for surfaces that render images only, such as a pull request body' $ROOT/runes/core/skills/AcceptanceTesting/Recording.md"
expect "pull request body"
