# Tasks

## 1. Authoring

- [x] 1.1 RemoteWrites rule as a command list, exception for the named review label limited to the invoking agent
- [x] 1.2 Storyboard: `SKILL.md` and the six frame templates, one glyph set, width 78, change map first, delta frame last, frames saved after confirmation
- [x] 1.3 ForgeCycle: `SKILL.md` and `Stages.md` mapping every DECK-0008 stage to one owner or to stop, with the return edges and the owner-closed stop
- [x] 1.4 MergeTrain: `SKILL.md`, `workflow.js` with `meta.caps` enforced, `.ok` on every result, `Triage.md`, `Review.md`, head SHA recorded and every verdict bound to it, child briefs carry the command list and the absolute skill path
- [x] 1.5 AgentTeam: `SKILL.md`, `workflow.js`, `Split.md` with file ownership for parallel packages, dependent packages from the integrated tree, an Integrate phase, child briefs as in 1.4
- [x] 1.6 AdversaryReview: `SKILL.md`, `workflow.js`, `Attack.md`, attacks the original, no rewrite before the attack, every hit fixed or rejected with reason, description cites the CORE-0016 method
- [x] 1.7 ResearchGrid: `SKILL.md`, `workflow.js`, `Track.md`, verifier model differs from gatherer, excerpt per row, rejected rows excluded, single-source numbers marked unsupported
- [x] 1.8 VersionControl: one line naming RemoteWrites and MergeTrain
- [x] 1.9 Record DECK-0016

## 2. Adversarial review of the authoring

- [x] 2.1 astra and grok refuted the change documents on 2026-09-16. Dispositions: rule as command list (fixed), "MUST load in every session" (fixed, scoped to harnesses with a rules path plus the interim `AGENTS.md`), ForgeCycle delegation versus no-workflow (fixed, names the stage and ends the turn), pi package edits leaking into this change (fixed, removed), DECK-0008 stages missing (fixed, Stages.md maps all twelve), meta.caps without ceilings (fixed), disjoint ownership for serial packages (fixed), scenarios without a MUST (fixed or deleted), "accepted with reason" (fixed, removed), rejected versus unsupported rows (fixed, both defined), head SHA as a requirement (fixed), rename AdversaryReview to avoid the CORE-0016 agent (rejected, the owner chose the name and the agent does not exist yet, description cites the method), drop task 3.3 (rejected, pi has the tool and the model passes the file)
- [x] 2.2 astra and grok refuted the authored skills on 2026-09-16. Dispositions: `export const meta` invalid in pi (rejected, pi's tool documents that a script may start with it and a run today used it), child briefs without the RemoteWrites list or the skill path in Report, Table, Settle, Split, Verify (fixed, one contract prefixes every call and the script refuses a relative or missing skill path), AgentTeam dependency order not topological and failed predecessors dropped (fixed, topological sort with cycle and unknown-dependency rejection, blocked dependents), file ownership by raw string (fixed, canonical paths, no globs, parallel-only disjointness), integrate on partial or blocking results (fixed, returns integrated false), MergeTrain readiness by regex and head never re-read (fixed, state enum, remote head read before edit and before verify, stale excluded), `.ok` without structured fields treated as clean (fixed, fail closed on missing fields), ResearchGrid same-model fallback (fixed, both models required and unequal), unverifiable kept in table and secondSource unchecked (fixed, everything but confirmed with excerpt is rejected, second source must differ and agree), AdversaryReview designFlaw optional and no-hit verdict on failed seats (fixed, required, complete flag), hit matching by quote (fixed, ids), fan-out frame mid-workflow (fixed, planOnly run then plan argument), ForgeCycle two owners and ArchitectureDecision naming and closed pull request (fixed), Storyboard delta saved without confirmation (fixed), `targets: [claude, agentskills]` reaches harnesses without the tool (rejected for now, agentskills is the pi path and task 3.4 verifies the filter), ASCII-only glyphs (rejected, the spec says one glyph set, box drawing stays)

## 3. Verification

- [ ] 3.1 `rune validate`, `rune spec validate forge-adoption`, `mdschema check --schema` on every new document, Vale, rumdl, typos
- [ ] 3.2 `node --check` on every `workflow.js`, and a static check that every `agent(` result is `.ok`-tested
- [ ] 3.3 One manual run of each workflow skill from pi through cliproxyapi, the tool input compared byte for byte with `workflow.js`, transcript kept in the workshop
- [ ] 3.4 Confirm `targets: [claude, agentskills]` filters deployment in `rune assemble`. If it does not, the workflow skills do not merge until it does

## 4. Deferred by owner decision

- [ ] 4.1 Bench cases for each skill (BenchArtifact) with the same prompt and no skill as baseline
- [ ] 4.2 Behavior proofs per DECK-0015
- [ ] 4.3 pi package: workflow tool accepts a script path, and the `ask-user` extension is added
- [ ] 4.4 cli: companion existence check in `rune validate`, `rune spec show --schematic`, and an `AGENTS.md` assembly target so rules reach pi and codex
- [ ] 4.5 pi package: remove the prompt templates and skill copies once this change merges and 4.4 lands
