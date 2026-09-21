# Behavior proof: prove-each-scenario

`record.sh` contains one scene per scenario of the `prove-each-scenario` delta specification, in the grammar of
`docs/proofs/driver.sh`. The candidate is the AcceptanceTesting driver grammar, proven on itself: a copied `record.sh` with two scenes, one that passes and one whose expectation misses. `proof.cast` is its recording on 2026-09-21 through
`docs/proofs/cast.py`, exit 0 (`record-exit=0`). `proof.txt` is the transcript `asciinema convert -f txt` wrote from
it, and `proof.gif` the render.

Transcript digest (`shasum -a 256 proof.txt`): `c1587f64653e0e9534e4201feeba384319b366f56cdab0fd1cde1b69925ad3d7`

Scenes, in the order the specification lists them:

- Implementation is finished
- Expectation misses
- Proof is filed
- Change has no behavior
- Scenario has no proof at merge

The scene `Scenario has no proof at merge` records a gap: the warning merge check is task 3.5 of the change and does not exist, so that scenario is unproven and the scene shows the absence.

Re-record after a change to the scenes or the candidate:

```sh
python3 docs/proofs/cast.py docs/proofs/prove-each-scenario/record.sh docs/proofs/prove-each-scenario/proof.cast
agg --theme github-dark --font-size 11 --fps-cap 3 --last-frame-duration 3 proof.cast proof.gif
asciinema convert -f txt --overwrite proof.cast proof.txt
```
