# Tasks

## 1. Authoring

- [x] 1.1 AdversaryReview: `SKILL.md`, `workflow.js`, `Attack.md`, attacks the original, no rewrite before the attack, every hit fixed or rejected with reason, description cites the CORE-0016 method

## 2. Adversarial review

- [x] 2.1 astra and grok refuted the change documents on 2026-09-16. Dispositions kept for this change: meta.caps without ceilings (fixed), "accepted with reason" (fixed, removed), rename AdversaryReview to avoid the CORE-0016 agent (rejected, the owner chose the name and the agent does not exist yet, description cites the method)
- [x] 2.2 astra and grok refuted the authored skills on 2026-09-16. Dispositions kept for this change: child briefs without the RemoteWrites list or the skill path in Report, Table, Settle, Split, Verify (fixed, one contract prefixes every call and the script refuses a relative or missing skill path), `.ok` without structured fields treated as clean (fixed, fail closed on missing fields), AdversaryReview designFlaw optional and no-hit verdict on failed seats (fixed, required, complete flag), hit matching by quote (fixed, ids)
- [x] 2.3 The complete disposition list is in the forge-adoption tasks at deck commit 025ef47f8d28 (`git show 025ef47f8d28:docs/changes/forge-adoption/tasks.md`)

## 3. Verification

- [ ] 3.1 `rune validate`, `rune spec validate use-adversarial-reviews`, `mdschema check --schema` on every new document, Vale, rumdl, typos
- [ ] 3.2 `node --check` on `workflow.js`, and a static check that every `agent(` result is `.ok`-tested
- [ ] 3.3 One manual run from pi through cliproxyapi, the tool input compared byte for byte with `workflow.js`, transcript kept in the workshop
- [ ] 3.4 Confirm `targets: [claude, agentskills]` filters deployment in `rune assemble`

## 4. Deferred by owner decision

- [ ] 4.1 Bench case with the same prompt and no skill as baseline (BenchArtifact)
- [ ] 4.2 Behavior proof per scenario (DECK-0015)
