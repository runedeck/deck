# Tasks

## 1. Authoring

- [x] 1.1 AgentTeam: `SKILL.md`, `workflow.js`, `Split.md` with file ownership for parallel packages, dependent packages from the integrated tree, an Integrate phase, child briefs carry the command list and the absolute skill path

## 2. Adversarial review

- [x] 2.1 astra and grok refuted the change documents on 2026-09-16. Dispositions kept for this change: meta.caps without ceilings (fixed), disjoint ownership for serial packages (fixed)
- [x] 2.2 astra and grok refuted the authored skills on 2026-09-16. Dispositions kept for this change: child briefs without the RemoteWrites list or the skill path in Report, Table, Settle, Split, Verify (fixed, one contract prefixes every call and the script refuses a relative or missing skill path), AgentTeam dependency order not topological and failed predecessors dropped (fixed, topological sort with cycle and unknown-dependency rejection, blocked dependents), file ownership by raw string (fixed, canonical paths, no globs, parallel-only disjointness), integrate on partial or blocking results (fixed, returns integrated false), `.ok` without structured fields treated as clean (fixed, fail closed on missing fields)
- [x] 2.3 The complete disposition list is in the forge-adoption tasks at deck commit 025ef47f8d28 (`git show 025ef47f8d28:docs/changes/forge-adoption/tasks.md`)

## 3. Verification

- [ ] 3.1 `rune validate`, `rune spec validate parallel-agent-teams`, `mdschema check --schema` on every new document, Vale, rumdl, typos
- [ ] 3.2 `node --check` on `workflow.js`, and a static check that every `agent(` result is `.ok`-tested
- [ ] 3.3 One manual run from pi through cliproxyapi, the tool input compared byte for byte with `workflow.js`, transcript kept in the workshop
- [ ] 3.4 Confirm `targets: [claude, agentskills]` filters deployment in `rune assemble`

## 4. Deferred by owner decision

- [ ] 4.1 Bench case with the same prompt and no skill as baseline (BenchArtifact)
- [ ] 4.2 Behavior proof per scenario (DECK-0015)
