# Tasks

## 1. Authoring

- [x] 1.1 MergeTrain: `SKILL.md`, `workflow.js` with `meta.caps` enforced, `.ok` on every result, `Triage.md`, `Review.md`, head SHA recorded and every verdict bound to it, child briefs carry the command list and the absolute skill path
- [x] 1.2 VersionControl: one line naming MergeTrain

## 2. Adversarial review

- [x] 2.1 astra and grok refuted the change documents on 2026-09-16. Dispositions kept for this change: meta.caps without ceilings (fixed), head SHA as a requirement (fixed)
- [x] 2.2 astra and grok refuted the authored skills on 2026-09-16. Dispositions kept for this change: child briefs without the RemoteWrites list or the skill path in Report, Table, Settle, Split, Verify (fixed, one contract prefixes every call and the script refuses a relative or missing skill path), MergeTrain readiness by regex and head never re-read (fixed, state enum, remote head read before edit and before verify, stale excluded), `.ok` without structured fields treated as clean (fixed, fail closed on missing fields)
- [x] 2.3 The complete disposition list is in the forge-adoption tasks at deck commit 025ef47f8d28 (`git show 025ef47f8d28:docs/changes/forge-adoption/tasks.md`)

## 3. Verification

- [ ] 3.1 `rune validate`, `rune spec validate agentic-merge-train`, `mdschema check --schema` on every new document, Vale, rumdl, typos
- [ ] 3.2 `node --check` on `workflow.js`, and a static check that every `agent(` result is `.ok`-tested
- [ ] 3.3 One manual run from pi through cliproxyapi, the tool input compared byte for byte with `workflow.js`, transcript kept in the workshop
- [ ] 3.4 Confirm `targets: [claude, agentskills]` filters deployment in `rune assemble`

## 4. Deferred by owner decision

- [ ] 4.1 Bench case with the same prompt and no skill as baseline (BenchArtifact)
- [ ] 4.2 Behavior proof per scenario (DECK-0015)
- [ ] 4.3 pi package: workflow tool accepts a script path, and the `ask-user` extension is added
- [ ] 4.4 cli: companion existence check in `rune validate`, `rune spec show --schematic`, and an `AGENTS.md` assembly target so rules reach pi and codex
- [ ] 4.5 pi package: remove the prompt templates and skill copies once this change merges and the cli support is released
