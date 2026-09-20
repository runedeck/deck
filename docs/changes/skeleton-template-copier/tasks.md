## 1. Implementation

- [x] 1.1 Copier update from the recorded pin to the current skeleton commit
- [x] 1.2 Re-add the deck hooks, Makefile targets, lint excludes, and Quality steps on the template base
- [x] 1.3 Correct semicolons and contractions at the reported positions and reseal the touched sidecars
- [x] 1.4 Path-scoped Vale override for the Simplified Technical English samples
- [x] 1.5 Record DECK-0012 and this change

## 2. Verification

- [x] 2.1 `rune adopt doctor --root runes/core` and `scripts/check-provenance` report no stale sidecar
- [x] 2.2 `vale`, `rumdl`, `typos`, `lychee --offline`, `actionlint`, and `zizmor` pass under the merged configs
- [ ] 2.3 First Quality run on main is green and the first weekly parity run reports no deck drift
