---
type: proof
change: convenient-proof-page-viewer
recorded: 2026-09-21
transcript: bca84aa060a2574a56880696655e1023b681458bedf570b6283e68711c117f55
scenes:
  - scenario: convenient-proof-page-viewer#a-proof-is-handed-over-as-a-page/proof-finished
    kind: check
  - scenario: convenient-proof-page-viewer#a-proof-is-handed-over-as-a-page/owner-asks-where-the-proof-is
    kind: check
  - scenario: convenient-proof-page-viewer#the-page-builds-from-the-casts-alone/cast-with-five-scenes
    kind: check
---

# Behavior proof: convenient-proof-page-viewer

`record.sh` contains one scene per scenario of the `convenient-proof-page-viewer` delta specification, in the grammar of
`scripts/fallback/prove.sh`. The candidate is the AcceptanceTesting page generator `scripts/proof-page.py`, run on the skeleton's trusted-key-anchor cast. `proof.cast` is its recording on 2026-09-21 through
`scripts/fallback/asciinema.py`, exit 0 (`record-exit=0`). `proof.txt` is the transcript `asciinema convert -f txt` wrote from
it, and `proof.gif` the render.

Transcript digest (`shasum -a 256 proof.txt`): `bca84aa060a2574a56880696655e1023b681458bedf570b6283e68711c117f55`

Scenes, in the order the specification lists them:

- Proof finished
- Owner asks where the proof is
- Cast with five scenes

The generator inlines the player from a checkout of html-tools. The proof passes `CAST_PLAYER` and `FILED_PROOF` for other locations.

Re-record after a change to the scenes or the candidate:

```sh
python3 scripts/fallback/asciinema.py docs/proofs/convenient-proof-page-viewer/record.sh docs/proofs/convenient-proof-page-viewer/proof.cast
agg --theme github-dark --font-size 11 --fps-cap 3 --last-frame-duration 3 proof.cast proof.gif
asciinema convert -f txt --overwrite proof.cast proof.txt
```
