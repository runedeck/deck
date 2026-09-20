# Tasks

## 1. Authoring

- [x] 1.1 DraftArtifact: `SKILL.md` with prerequisites, constraints, the three procedures (start, check, promote or drop), verification, troubleshooting
- [x] 1.2 The skill itself was drafted with `rune draft skill DraftArtifact` and promoted with `rune promote DraftArtifact --domain core --change draft-artifact-skill-adoption` from the cli `4fa850b9` build

## 2. Verification

- [x] 2.1 `rune validate --skill-layers --source runes/core/skills/DraftArtifact`, `rune spec validate draft-artifact-skill-adoption`, and the commit-stage checks
- [ ] 2.2 Bench case: the same "start a new skill" prompt with and without the skill (BenchArtifact), deferred by the owner's rule that a skill carries no verdict until it has one
- [ ] 2.3 Behavior proof: the cli proof at `docs/proofs/draft-runes-before-promotion/` in runedeck/cli covers every command the skill uses. A deck proof is deferred to DECK-0015

## 3. Record

- [ ] 3.1 Archive moves `adr.md` to `docs/decisions/` with the next free DECK number
