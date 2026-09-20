# Tasks

## 1. Authoring

- [x] 1.1 AdversaryReview: `SKILL.md`, `workflow.js`, `Attack.md`, attacks the original, no rewrite before the attack, every hit fixed or rejected with reason, description cites the CORE-0016 method

## 2. Adversarial review

- [x] 2.1 astra and grok refuted the change documents and the authored artifact on 2026-09-16. Dispositions are recorded in the forge-adoption change history.

## 3. Verification

- [ ] 3.1 `rune validate`, `rune spec validate use-adversarial-reviews`, `mdschema check --schema` on every new document, Vale, rumdl, typos
- [ ] 3.2 `node --check` on `workflow.js`, and a static check that every `agent(` result is `.ok`-tested
- [ ] 3.3 One manual run from pi through cliproxyapi, the tool input compared byte for byte with `workflow.js`, transcript kept in the workshop
- [ ] 3.4 Confirm `targets: [claude, agentskills]` filters deployment in `rune assemble`

## 4. Deferred by owner decision

- [ ] 4.1 Bench case with the same prompt and no skill as baseline (BenchArtifact)
- [ ] 4.2 Behavior proof per scenario (DECK-0015)
