# Tasks

## 1. Authoring

- [x] 1.1 ForgeCycle: `SKILL.md` and `Stages.md` mapping every DECK-0008 stage to one owner or to stop, with the return edges and the owner-closed stop

## 2. Adversarial review

- [x] 2.1 astra and grok refuted the change documents on 2026-09-16. Dispositions kept for this change: ForgeCycle delegation versus no-workflow (fixed, names the stage and ends the turn), DECK-0008 stages missing (fixed, Stages.md maps all twelve)
- [x] 2.2 astra and grok refuted the authored skills on 2026-09-16. Dispositions kept for this change: ForgeCycle two owners and ArchitectureDecision naming and closed pull request (fixed)
- [x] 2.3 The complete disposition list is in the forge-adoption tasks at deck commit 025ef47f8d28 (`git show 025ef47f8d28:docs/changes/forge-adoption/tasks.md`)

## 3. Verification

- [ ] 3.1 `rune validate`, `rune spec validate openspec-change-router`, `mdschema check --schema` on every new document, Vale, rumdl, typos

## 4. Deferred by owner decision

- [ ] 4.1 Bench case with the same prompt and no skill as baseline (BenchArtifact)
- [ ] 4.2 Behavior proof per scenario (DECK-0015)
