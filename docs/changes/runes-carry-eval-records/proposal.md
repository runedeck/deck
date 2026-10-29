---
adr: "docs/decisions/DECK-0001 Artifact Benchmarking Skill.md"
status: proposed
---

# Runes carry eval records

## Why

The foundations decide what stays in an *[instruction][INSTRUCTION]*: a *[requirement][REQUIREMENT]* states a check that can fail, and the shortest instruction that passes the check wins. These are *[falsifiability][FALSIFIABILITY]* and *[Occam's razor][OCCAMSRAZOR]*, and the foundations cite an evaluation score as the measure ([foundations][FOUNDATIONS]). The foundations also say that a *[variant][VARIANT]* for one *[harness][HARNESS]* or *[model][MODEL]* must beat the *[canon][CANON]* alone on an evaluation, or the author removes it. That is the requirement Companions Earn Their Place ([vendor-neutral instructions][NEUTRAL]).

Until now no *[rune][RUNE]* in the *[deck][DECK]* had a case that could fail inside the *[repository][REPOSITORY]*. The *[coverage][COVERAGE]* table of the foundations lists Companions Earn Their Place as a *[missed requirement][MISSEDREQUIREMENT]* for that reason. The record DECK-0001 already asks for the same evidence for a skill, a rule, and an agent alike: behavior with the rune against behavior without it ([DECK-0001][DECK0001]).

An evaluation case, an eval case for short, gives a model one task. Checks called graders score the answer, and each grader gives the same result every time for the same answer. The case runs twice, once with the rune loaded and once without it. The difference between the two scores is what the rune does. When both runs pass a case, the case shows nothing about the rune, and the author rewrites it or drops it.

Two more needs come with this change. The owner asks for a task taken to a merge-ready pull request while nobody reads the output, with one question at the end. And lessons the owner gave sit as drafts in the owner's workshop under machine-made names, outside the deck where no check reads them.

## What Changes

- A runner for one rune's eval suite. It builds the rune's Claude Code *[instance][INSTANCE]* through the *[assembler][ASSEMBLER]* and wraps it in a throwaway plugin. A *[rule][RULE]* loads through a session-start hook, because a plugin cannot hold a rule file. The runner runs the cases with the rune and without it through Claude Code's own plugin eval command, launched through a rune launch profile. Each run writes a JSON record beside the suite. With a record directory, the runner also records the run and renders an animated image that shows both answers of every case.
- The graders are deterministic only. The model judge cannot sign in from the eval's child sessions on this machine ([evals guide][EVALS]).
- Eval suites for the *[skills][SKILL]* VersionControl, SafetyFirst, SimplifiedTechnicalEnglish, BuildSkill, FullSend, and PruneTests, and for the rules RemoteWrites, PreferTrash, OnePurpose, PlainSpokenLanguage, Deslop, and VerifyClaims. The recordings go into the *[proof][PROOF]* directory of this change.
- When a rune fails its own case, this change fixes the rune or the case and says which.
- FullSend, a new skill in the development domain. It takes one task to a merge-ready pull request while the owner reads nothing, then asks once to merge. It never merges without the owner's yes.
- PruneTests, a new skill in the development domain. It deletes tests that no plausible bug can fail and repairs weak ones. A recorded mutation proves each repair, and FullSend takes the pull request from there.
- The core rules PreferExistingTools, ProofsShowTheRealApp, and AskBeforeMovingData, which this change rewrites from the workshop drafts.
- The core rule AnswerBeforeEditing, new, from a lesson the owner gave.
- This change drops the draft WhenTheUserSignals, because PlainSpokenLanguage already says it.

## Capabilities

### New Capabilities

- `rune-cases-can-fail`: a rune's eval cases run with the rune and without it on the same model and instance. Every case can fail, and a grader gives one result for one answer. Every run leaves a record, and a new run never rewrites an old one.
- `unattended-work-awaits-owner`: FullSend asks the owner only through the question tool and proves the fix on the final head. It never merges before the owner's yes. PruneTests deletes tests no plausible bug can fail and proves each repair with a mutation.
- `owner-lessons-become-rules`: an existing tool comes before a custom script, and a proof records the real app. A bulk copy of data waits for the owner's yes. A question gets an answer before any edit.

## Impact

- `scripts/eval-rune` and the suite guide `evals/README.md`.
- One directory per rune under `evals/`, each with its cases and a `records/` directory that runs fill.
- The recordings under `docs/proofs/runes-carry-eval-records/`.
- `runes/development/skills/FullSend/` with a Claude Code variant, and `runes/development/skills/PruneTests/`.
- The new rule files under `runes/core/rules/`.
- Changelog entries under Unreleased.
- A run starts full Claude Code sessions on the launch profile's credential. It runs outside the command sandbox and uses model calls for each case and each run.

## Risks

- A record speaks for one model and one harness. The runner defaults to a small model ([runner][RUNNER]), and a rune that a larger model does not need can still score on it.
- A pattern grader reads the words of an answer. It never sees the result on disk, and a right answer in an unexpected form fails a required pattern. The records hold grader scores only. A three-metric verdict in the sense of DECK-0003 also needs assertions on meaning and blind preference ([DECK-0003][DECK0003]).
- Cases use read-only tools and four turns or fewer ([evals guide][EVALS]). A case shows what a model says and plans. It cannot show FullSend open a real pull request or PruneTests break production code. The recordings prove the runner and the answers, and a real pull request must prove those two skills.
- The new rules PreferExistingTools, ProofsShowTheRealApp, AskBeforeMovingData, and AnswerBeforeEditing have no eval suite yet. They have not shown that they can fail. FullSend's Claude Code variant has no record against the canon alone.
- The runner turns off the session's environment scrub. The eval's child sessions then get the profile's credential.

## Sources

- [The foundations][FOUNDATIONS], the change `plain-text-first-principles`
- [DECK-0001 Artifact Benchmarking Skill][DECK0001] and [DECK-0003 Three-Metric Verdict and Cross-Vendor Judging][DECK0003]
- [The evals guide][EVALS] and [the runner][RUNNER]

[FOUNDATIONS]: ../plain-text-first-principles/proposal.md
[NEUTRAL]: ../plain-text-first-principles/specs/instructions-stay-vendor-neutral/spec.md
[DECK0001]: ../../decisions/DECK-0001%20Artifact%20Benchmarking%20Skill.md
[DECK0003]: ../../decisions/DECK-0003%20Three-Metric%20Verdict%20and%20Cross-Vendor%20Judging.md
[EVALS]: ../../../evals/README.md
[RUNNER]: ../../../scripts/eval-rune
[INSTRUCTION]: ../../specs/glossary/instruction.md
[REQUIREMENT]: ../../specs/glossary/requirement.md
[FALSIFIABILITY]: ../../specs/glossary/falsifiability.md
[OCCAMSRAZOR]: ../../specs/glossary/occams-razor.md
[VARIANT]: ../../specs/glossary/variant.md
[HARNESS]: ../../specs/glossary/harness.md
[MODEL]: ../../specs/glossary/model.md
[CANON]: ../../specs/glossary/canon.md
[RUNE]: ../../specs/glossary/rune.md
[DECK]: ../../specs/glossary/deck.md
[REPOSITORY]: ../../specs/glossary/repository.md
[COVERAGE]: ../../specs/glossary/coverage.md
[MISSEDREQUIREMENT]: ../../specs/glossary/missed-requirement.md
[INSTANCE]: ../../specs/glossary/instance.md
[ASSEMBLER]: ../../specs/glossary/assembler.md
[RULE]: ../../specs/glossary/rule.md
[SKILL]: ../../specs/glossary/skill.md
[PROOF]: ../../specs/glossary/proof.md
