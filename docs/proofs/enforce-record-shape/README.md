# Behavior proof: enforce-record-shape

`record.sh` contains one scene per scenario of the `enforce-record-shape` delta specification, in the grammar of
`docs/proofs/driver.sh`. The candidate is the tightened `docs/decisions/.mdschema` and `scripts/check-decision-shape`,
run on fixture records in a scratch tree and on the real deck. `proof.cast` is its recording on 2026-09-23 through
`docs/proofs/cast.py`, exit 0 (`record-exit=0`). `proof.txt` is the transcript `asciinema convert -f txt` wrote from
it, and `proof.gif` the render.

Transcript digest (`shasum -a 256 proof.txt`): `dc01f222036d550f71b9b2863a46c88313f49ecfea38d76bda62cb5368d14594`

Scenes, in the order the specification lists them:

- Consequences become their own section
- Consequence bullet has no sign
- Consulted entry names a model without a harness
- Consulted entry names an unknown harness
- Upstream names a file that does not exist
- Upstream names a capability requirement
- Record is adopted from forge-core

The last scene copies CORE-0001 from the deck and from the forge-core checkout at `FORGE_CORE` (default
`~/Developer/N4M3Z/forge-core`) into the scratch tree and proves the dates match. No commit-time check reads the source
repository, so that scenario has a proof and no check.

The recording keeps short pauses (`PAUSE_AFTER_COMMENT=0.8`, `PAUSE_AFTER_OUTPUT=1.0`), so the cast runs 26 seconds and a
person can scrub it. A zero-pause recording plays in one second and is unreadable in the player.

Re-record after a change to the scenes or the candidate:

```sh
python3 docs/proofs/cast.py docs/proofs/enforce-record-shape/record.sh docs/proofs/enforce-record-shape/proof.cast
agg --theme github-dark --font-size 11 --fps-cap 3 --last-frame-duration 3 proof.cast proof.gif
asciinema convert -f txt --overwrite proof.cast proof.txt
```
