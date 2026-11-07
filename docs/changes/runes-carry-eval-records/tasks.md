## 1. Runner

- [x] 1.1 Assemble a rune's Claude Code instance from a private copy and wrap it in a throwaway plugin, with a session-start hook for a rule
- [x] 1.2 Run the cases with the rune and without it through Claude Code's plugin eval, launched through a rune launch profile
- [x] 1.3 Write one record per run beside the suite, and no record when a case fails in the harness
- [x] 1.4 Record a run on request and render an animated image with both answers of every case
- [x] 1.5 Write the suite guide `evals/README.md`
- [ ] 1.6 Add a check that rejects a grader type outside the deterministic set
- [ ] 1.7 Add a check that reports a case whose newest record shows no difference without the rune

## 2. Suites

- [x] 2.1 Write the skill suites: VersionControl, SafetyFirst, SimplifiedTechnicalEnglish, BuildSkill, FullSend, PruneTests
- [x] 2.2 Write the rule suites: RemoteWrites, PreferTrash, OnePurpose, PlainSpokenLanguage, Deslop, VerifyClaims
- [x] 2.3 Run each suite once, and rewrite or drop each case that both runs pass
- [x] 2.4 Fix each rune that fails its own case where the fix is clear: VersionControl's directory flag, FullSend's question fallback and scanner path, and SafetyFirst's Claude Code variant
- [x] 2.5 Record each suite into `docs/proofs/runes-carry-eval-records/` and keep its record
- [x] 2.6 Run FullSend and SafetyFirst with their Claude Code variants and without them. FullSend's variant beats its canon and stays. SafetyFirst's variant scores 0 against 0.44 and is removed
- [ ] 2.7 Decide the weaknesses that need the owner: OnePurpose on chained commands, PlainSpokenLanguage on abbreviations, Deslop on negative parallelism and on cases that pass without it, BuildSkill on triggering and naming, and RemoteWrites on full addresses and thread offers

## 3. Skills and rules

- [x] 3.1 Write the FullSend skill and its Claude Code variant
- [x] 3.2 Write the PruneTests skill, which gives its pull request to FullSend
- [x] 3.3 Write PreferExistingTools, ProofsShowTheRealApp, and AskBeforeMovingData from the workshop drafts
- [x] 3.4 Write AnswerBeforeEditing from the owner's lesson
- [x] 3.5 Leave out the WhenTheUserSignals draft, because PlainSpokenLanguage covers it
- [x] 3.6 Add the changelog entries
- [x] 3.7 Write a suite for AskBeforeMovingData and AnswerBeforeEditing
- [ ] 3.9 Write a suite for PreferExistingTools and ProofsShowTheRealApp
- [ ] 3.8 Remove the drafts from the owner's workshop after the deployer writes the new rules there

## 4. Verification

- [ ] 4.1 Run `openspec validate --all --strict` and `rune spec validate` until both pass
- [ ] 4.2 Have a different model judge each recording against the specifications, scenario by scenario, then ask the owner to approve
- [ ] 4.3 Prove FullSend and PruneTests on a real pull request, because a read-only case cannot show the merge question or a mutation
- [ ] 4.4 Decide on the proposed terms in `design.md`, and add the approved ones to the ontology through the fixer
