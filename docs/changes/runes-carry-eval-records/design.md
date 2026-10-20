# Design

## Coverage table

The table has one row for each *[requirement][REQUIREMENT]* of this change. No hook runs an eval suite, so every behavior of a *[rune][RUNE]* is a *[missed requirement][MISSEDREQUIREMENT]* until a check reads its records. The Commands table below names the program behind each row.

| Capability | Requirement | Check or missed requirement |
|---|---|---|
| rune-cases-can-fail | Cases Run With And Without The Rune | missed requirement: the eval runner builds both runs, and no check proves that the run without the rune lacks the rune |
| rune-cases-can-fail | Every Case Can Fail | missed requirement: no check reads the newest record for a case whose score does not change without the rune |
| rune-cases-can-fail | Graders Give The Same Result | missed requirement: no check rejects a grader type outside the deterministic set |
| rune-cases-can-fail | Suites Pair A Direct Case With A Near Miss | missed requirement: review decides whether a case is a near miss, and no check reads the turn limit or the tool list |
| rune-cases-can-fail | Every Run Leaves A Record | missed requirement: the eval runner writes the record, and no check proves that a run never rewrites an old one |
| rune-cases-can-fail | Recorded Run Shows Both Answers | missed requirement: a reviewing model reads the recording, and no check reads the animated image |
| unattended-work-awaits-owner | Owner Gets Only Questions | missed requirement: the FullSend suite runs on demand, and no hook runs it |
| unattended-work-awaits-owner | Merge Waits For The Owner's Yes | missed requirement: the FullSend suite runs on demand, and only a real pull request shows the merge question |
| unattended-work-awaits-owner | Fix Is Reproduced And Proven | missed requirement: the FullSend suite runs on demand, and no hook runs it |
| unattended-work-awaits-owner | Confidence Rests On The Final Head | missed requirement: the FullSend suite runs on demand, and no check compares the evidence head with the live head |
| unattended-work-awaits-owner | Tests Earn Their Place | missed requirement: the PruneTests suite runs on demand, and no hook runs it |
| unattended-work-awaits-owner | Repairs Are Proven By Mutation | missed requirement: a read-only case cannot break production code, so only a real pull request shows the mutation |
| owner-lessons-become-rules | Existing Tools Come First | missed requirement: the rule has no eval suite yet |
| owner-lessons-become-rules | Proofs Show The Real App | missed requirement: a reviewing model judges each recording, and the rule has no eval suite yet |
| owner-lessons-become-rules | Bulk Copies Of Data Wait For A Yes | missed requirement: the rule has no eval suite yet, and no check scans an approved copy for secrets |
| owner-lessons-become-rules | Questions Get Answers Before Edits | missed requirement: the rule has no eval suite yet |

## Commands

A requirement names a role. This table names the program and flags behind each row. Every row runs on demand, outside the command sandbox, because a run starts full Claude Code sessions. A row that says "not built" is a task in `tasks.md`.

| Requirement | Role | Command and flags |
|---|---|---|
| Cases Run With And Without The Rune | *[assembler][ASSEMBLER]*, eval runner | `scripts/eval-rune <Rune>` copies the rune's domain to a temporary directory and runs `rune assemble --source <copy>`. It copies a skill instance into the plugin's `skills/`, or a rule into `rules/` beside `hooks/hooks.json`, whose `SessionStart` hook prints the rule. Then it runs `rune launch <profile>@claude --direct -- plugin eval <plugin> --runs <n> --no-publish --trust-plugin --keep-temp --model <id> --json <result>` with `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=0` |
| Every Case Can Fail | *[validator][VALIDATOR]* | the record's `cases[].delta`. A check over the newest record of each suite: not built |
| Graders Give The Same Result | validator | the `type` key of each `evals/<Rune>/<case>/graders/*.md`: `regex`, `tool_used`, `tool_order`, or `file_exists`. A check that rejects any other type: not built |
| Suites Pair A Direct Case With A Near Miss | review | `max_turns` and `allowed_tools` in the frontmatter of each `evals/<Rune>/<case>/prompt.md` |
| Every Run Leaves A Record | eval runner | `scripts/eval-rune <Rune> [--profile <name>] [--model <id>] [--runs <n>]` writes `evals/<Rune>/records/<UTC stamp>-<model>.json`. The defaults are profile `main`, model `claude-haiku-4-5-20251001`, and one run. The record also keeps the profile, the passed and total case counts, the cost, and the duration |
| Recorded Run Shows Both Answers | eval runner | `scripts/eval-rune <Rune> --record docs/proofs/runes-carry-eval-records` runs `asciinema rec --headless --window-size 100x30 --idle-time-limit 2 --overwrite --return <dir>/<Rune>.cast`, then `agg --theme github-dark --font-size 18 --last-frame-duration 4 <cast> <gif>`. Inside the recording, `scripts/eval-rune --show <result.json>` prints each case's scores and the first twelve lines of each answer |
| Owner Gets Only Questions, Merge Waits For The Owner's Yes, Fix Is Reproduced And Proven, Confidence Rests On The Final Head | eval runner | `scripts/eval-rune FullSend`. On Claude Code the question tool is `AskUserQuestion`, from the variant `runes/development/skills/FullSend/claude/SKILL.md` |
| Tests Earn Their Place, Repairs Are Proven By Mutation | eval runner | `scripts/eval-rune PruneTests` |
| Existing Tools Come First, Proofs Show The Real App, Bulk Copies Of Data Wait For A Yes, Questions Get Answers Before Edits | eval runner | `scripts/eval-rune <Rule>` after the rule has a suite under `evals/<Rule>/`: not built |

## Proposed terms

The ontology has no entry for these words. The specifications describe each one in plain words. The owner approves or rejects each term before the *[fixer][FIXER]* adds it.

| Term | Definition | Related term |
|---|---|---|
| eval case | One task for a *[model][MODEL]*, with graders that score the answer, run once with a rune and once without it. | *[scenario][SCENARIO]*, because both state a situation and the expected result, and *[fixture][FIXTURE]* |
| eval suite | The eval cases kept for one rune and run together against its *[instance][INSTANCE]*. | [rune][RUNE] |
| eval record | The stored result of one suite run: the instance digest, the model, and each case's score with and without the rune. | *[verdict][VERDICT]*, the judgment a bench draws from such scores |
| eval runner | The role that runs a rune's suite against its instance and writes the eval record. | *[tool role][TOOLROLE]* and *[proof runner][PROOFRUNNER]* |

## Decisions

- The runner wraps the assembled instance in a throwaway plugin. A case then tests what Claude Code loads, and not the *[canon][CANON]*. Each run assembles a private copy of the domain, so parallel runs never share one build directory.
- A plugin cannot hold a rule file. A session-start hook prints the rule instead. Only the run with the plugin gets the hook, and Claude Code's plugin eval makes the run without it by its default with-and-without comparison.
- Graders are deterministic only, because the model judge cannot sign in from the eval's child sessions on this machine. An eval record is therefore not a verdict in the sense of DECK-0003. It holds grader scores with and without the rune, and no assertion on meaning or blind preference.
- The runner launches Claude Code through a rune launch profile, so the profile supplies the model route and its credential. The runner turns off the session's environment scrub, so the child sessions keep that credential.
- A run in which any case fails in the harness writes no record and exits with an error. A broken run never reads as a score.
- Records only accumulate. The file name is the UTC time stamp and the model, so two runs never share a name.
- A *[variant][VARIANT]* earns its place when its record beats the canon's record on the same cases and the same model, as Companions Earn Their Place requires. The runner assembles with the variant. The record for the canon alone needs a run with the variant removed from the private copy. FullSend's Claude Code variant is the first to need it.
- PruneTests gives its pull request to FullSend, so the pull-request loop has one home.
- The rules PreferExistingTools, ProofsShowTheRealApp, and AskBeforeMovingData take their substance from the workshop drafts and their wording from the deck's plain register. AnswerBeforeEditing is new.
- The draft WhenTheUserSignals stays out, because PlainSpokenLanguage already tells a model to stop and explain when the owner does not understand.
- The eval runner is not one of the roles that the record CORE-0023 assigns to rune. The specifications describe it in plain words until the owner decides on the term.

[REQUIREMENT]: ../../specs/glossary/requirement.md
[RUNE]: ../../specs/glossary/rune.md
[MISSEDREQUIREMENT]: ../../specs/glossary/missed-requirement.md
[ASSEMBLER]: ../../specs/glossary/assembler.md
[VALIDATOR]: ../../specs/glossary/validator.md
[FIXER]: ../../specs/glossary/fixer.md
[MODEL]: ../../specs/glossary/model.md
[SCENARIO]: ../../specs/glossary/scenario.md
[FIXTURE]: ../../specs/glossary/fixture.md
[INSTANCE]: ../../specs/glossary/instance.md
[VERDICT]: ../../specs/glossary/verdict.md
[TOOLROLE]: ../../specs/glossary/tool-role.md
[PROOFRUNNER]: ../../specs/glossary/proof-runner.md
[CANON]: ../../specs/glossary/canon.md
[VARIANT]: ../../specs/glossary/variant.md
