# Behavior proof: cast-player-in-proofs

`record.sh` contains one scene per scenario of the `cast-player-in-proofs` delta specification, in the grammar of
`docs/proofs/driver.sh`. The candidate is the html-tools cast player (`runtime/cast-player.js`), driven under node without a browser: parse, scenes, controller, and sceneAt on the skeleton's trusted-key-anchor cast. `proof.cast` is its recording on 2026-09-21 through
`docs/proofs/cast.py`, exit 0 (`record-exit=0`). `proof.txt` is the transcript `asciinema convert -f txt` wrote from
it, and `proof.gif` the render.

Transcript digest (`shasum -a 256 proof.txt`): `e2938094b328e897e61b25d19e79472839d3f9c6bbb35a11afc78f6dd930b00c`

Scenes, in the order the specification lists them:

- Reader pauses a proof
- Pull request shows the proof

The page behavior (Space pauses, the label states the scene) is proven through the same functions the page calls. The DOM wiring itself is not exercised here.

Re-record after a change to the scenes or the candidate:

```sh
python3 docs/proofs/cast.py docs/proofs/cast-player-in-proofs/record.sh docs/proofs/cast-player-in-proofs/proof.cast
agg --theme github-dark --font-size 11 --fps-cap 3 --last-frame-duration 3 proof.cast proof.gif
asciinema convert -f txt --overwrite proof.cast proof.txt
```
