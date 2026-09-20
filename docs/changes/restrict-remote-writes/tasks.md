# Tasks

## 1. Authoring

- [x] 1.1 RemoteWrites rule as a command list, exception for the named review label limited to the invoking agent
- [x] 1.2 VersionControl: one line naming RemoteWrites

## 2. Adversarial review

- [x] 2.1 astra and grok refuted the change documents on 2026-09-16. Dispositions kept for this change: rule as command list (fixed), "MUST load in every session" (fixed, scoped to harnesses with a rules path plus the interim `AGENTS.md`)
- [x] 2.2 astra and grok refuted the authored skills on 2026-09-16. Dispositions kept for this change: child briefs without the RemoteWrites list or the skill path in Report, Table, Settle, Split, Verify (fixed, one contract prefixes every call and the script refuses a relative or missing skill path)
- [x] 2.3 The complete disposition list is in the forge-adoption tasks at deck commit 025ef47f8d28 (`git show 025ef47f8d28:docs/changes/forge-adoption/tasks.md`)

## 3. Verification

- [ ] 3.1 `rune validate`, `rune spec validate restrict-remote-writes`, `mdschema check --schema` on every new document, Vale, rumdl, typos

## 4. Deferred by owner decision

- [ ] 4.1 Bench case with the same prompt and no rule as baseline (BenchArtifact)
- [ ] 4.2 Behavior proof per scenario (DECK-0015)
