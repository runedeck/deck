# Behavior proof: proof-page-handover

`record.sh` contains one scene per scenario of the `proof-page-handover` delta specification, in the grammar of
`docs/proofs/driver.sh`. The candidate is the AcceptanceTesting page generator `scripts/proof-page.py`, run on the skeleton's trusted-key-anchor cast. `proof.cast` is its recording on 2026-09-21 through
`docs/proofs/cast.py`, exit 0 (`record-exit=0`). `proof.txt` is the transcript `asciinema convert -f txt` wrote from
it, and `proof.gif` the render.

Transcript digest (`shasum -a 256 proof.txt`): `bca84aa060a2574a56880696655e1023b681458bedf570b6283e68711c117f55`

Scenes, in the order the specification lists them:

- Proof finished
- Owner asks where the proof is
- Cast with five scenes

The generator inlines the player from a checkout of html-tools. The proof passes `CAST_PLAYER` and `FILED_PROOF` for other locations.

Re-record after a change to the scenes or the candidate:

```sh
python3 docs/proofs/cast.py docs/proofs/proof-page-handover/record.sh docs/proofs/proof-page-handover/proof.cast
agg --theme github-dark --font-size 11 --fps-cap 3 --last-frame-duration 3 proof.cast proof.gif
asciinema convert -f txt --overwrite proof.cast proof.txt
```
