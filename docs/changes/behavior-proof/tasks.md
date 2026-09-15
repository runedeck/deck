# Tasks

## 1. Implementation

- [x] 1.1 Add the AcceptanceTesting skill with the scene grammar, the recording mechanics, and the driver script
- [x] 1.2 Name AcceptanceTesting in the VersionControl constraints
- [x] 1.3 Record DECK-0015

## 2. Verification

- [x] 2.1 `bash -n` and shellcheck on `record.sh`. The driver exits 0 when every expectation matches, 1 on a miss, 1 on a malformed pattern, 1 on an expect before a scene's first run, and state set by one run reaches the next
- [x] 2.2 `rune validate`, Vale, rumdl, typos, and `rune spec validate`
- [x] 2.3 The commit and push stages through the ContinuousIntegration procedure

## 3. Follow-up

- [ ] 3.1 Record the first proof for a cli change and file it under `docs/proofs/`
- [ ] 3.2 Extract filed proofs as `rune:Proof` instances of kind `behavior` once `rune graph export` exists
- [ ] 3.3 Add asciinema, agg, and ffmpeg to `scripts/install-tools` once a Linux runner records proofs in CI
- [ ] 3.4 Close #64 when this change merges
