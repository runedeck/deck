---
type: proof
change: record-proof-per-scenario
recorded: 2026-09-20
transcript: c1587f64653e0e9534e4201feeba384319b366f56cdab0fd1cde1b69925ad3d7
scenes:
  - scenario: record-proof-per-scenario#proof-is-filed-with-the-pull-request/scenario-has-no-proof-at-merge
    kind: unproven
  - scenario: record-proof-per-scenario#a-change-with-behavior-carries-a-recorded-proof/implementation-is-finished
    kind: check
  - scenario: record-proof-per-scenario#a-change-with-behavior-carries-a-recorded-proof/expectation-misses
    kind: check
  - scenario: record-proof-per-scenario#proof-is-filed-with-the-pull-request/proof-is-filed
    kind: check
  - scenario: record-proof-per-scenario#a-change-with-behavior-carries-a-recorded-proof/change-has-no-behavior
    kind: check
---

# Behavior proof: record-proof-per-scenario

`record.sh` contains one scene per scenario of the `record-proof-per-scenario` delta specification, in the grammar of
`scripts/fallback/prove.sh`. The candidate is the AcceptanceTesting driver grammar, proven on itself: a copied `record.sh` with two scenes, one that passes and one whose expectation misses. `proof.cast` is its recording on 2026-09-21 through
`scripts/fallback/asciinema.py`, exit 0 (`record-exit=0`). `proof.txt` is the transcript `asciinema convert -f txt` wrote from
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
python3 scripts/fallback/asciinema.py docs/proofs/record-proof-per-scenario/record.sh docs/proofs/record-proof-per-scenario/proof.cast
agg --theme github-dark --font-size 11 --fps-cap 3 --last-frame-duration 3 proof.cast proof.gif
asciinema convert -f txt --overwrite proof.cast proof.txt
```
