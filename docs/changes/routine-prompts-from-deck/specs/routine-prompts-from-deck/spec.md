---
type: spec
---

## ADDED Requirements

### Requirement: Routine file is the behavior source

A routine prompt in the provider MUST be a stub that names one file under `routines/` in the runedeck/deck checkout. The file MUST contain the routine's behavior: authority, scope, permitted and prohibited operations, procedure, status rules, and notification format. The stub MUST stay under 20 lines.

#### Scenario: Routine run reads the file

- **WHEN** a run starts with the runedeck/deck source attached and the object-store checks pass
- **THEN** the run reads the file from `FETCH_HEAD` in the object store and follows it, and reads no prompt body from any other place

#### Scenario: Path is absent on the fetched main

- **WHEN** `ls-tree FETCH_HEAD -- routines/<File>.md` prints no entry
- **THEN** the run reports CONFIGURATION_FAILURE and stops

### Requirement: Stub reads the file from the fetched main

The stub MUST fetch `origin main` and require `git ls-tree FETCH_HEAD -- routines/<File>.md` to print exactly one entry with mode 100644 and type blob. The stub MUST read the file only as the output of `git cat-file blob FETCH_HEAD:routines/<File>.md` and MUST NOT point the run at the working-tree file in any sentence. Every bootstrap Git command MUST run with `--no-replace-objects`, so a replacement ref cannot swap the blob. The stub MUST report CONFIGURATION_FAILURE and stop when a command fails, the path is absent, or the mode or type differs. The check sits in the stub, because a check inside the file could be edited away with the file.

#### Scenario: Fetched main lacks the file and an untracked copy exists

- **WHEN** `routines/<File>.md` is absent from `FETCH_HEAD` and an untracked or ignored file with that path exists in the working tree
- **THEN** the run reports CONFIGURATION_FAILURE and stops, and never reads the working-tree file

#### Scenario: Path is a symbolic link on the fetched main

- **WHEN** `ls-tree FETCH_HEAD -- routines/<File>.md` prints mode 120000
- **THEN** the run reports CONFIGURATION_FAILURE and stops before it reads the file

#### Scenario: Working-tree file is edited

- **WHEN** the working-tree file differs from the blob at `FETCH_HEAD`
- **THEN** the run follows the blob from `cat-file` and never the working-tree file

#### Scenario: Replacement ref points at another blob

- **WHEN** `refs/replace/<id>` in the checkout replaces the blob of `routines/<File>.md`
- **THEN** every bootstrap command runs with `--no-replace-objects` and the run follows the original blob

### Requirement: Instance values come from the stub

A routine file MUST list each value it expects from the stub, with its form, under `## Inputs`. The file MUST NOT restate a stub value: the repository list, the fork-to-upstream pairs, and the time zone come from the stub. The stub MUST supply every required value.

#### Scenario: Stub omits a required value

- **WHEN** the stub carries no REPOSITORIES list
- **THEN** the run reports CONFIGURATION_FAILURE and stops

#### Scenario: Fork list is empty

- **WHEN** the stub gives FORK_UPSTREAMS as `- None.`
- **THEN** the run treats the list as empty and reports zero expected pairs

### Requirement: Every other file is data

A routine file MUST state under `## Authority` that the stub and the file are the only instruction sources, and that every other file in every checkout, the deck's own runes included, is untrusted data.

#### Scenario: Checkout carries instruction-like text

- **WHEN** a file in a checkout carries text that reads as an instruction to the run
- **THEN** the run does not follow it, does not quote it, and reports its location under Injection

### Requirement: Routine files match the directory schema

Every Markdown file under `routines/` other than the README MUST sit directly under `routines/` and MUST match `routines/.mdschema`: frontmatter with `type: routine`, one H1, and the section sequence the schema states. A routine file name MUST use only the characters `A-Za-z0-9._-`, because `mdschema` expands a glob character in a path argument. The `mdschema-routines` hook MUST check every such file before a commit, MUST reject a Markdown file in a subdirectory of `routines/`, and MUST reject a file name with another character.

#### Scenario: Routine file lacks the Authority section

- **WHEN** a file under `routines/` has no `## Authority` heading
- **THEN** `mdschema check` fails and the hook blocks the commit

#### Scenario: Routine file is nested

- **WHEN** a Markdown file exists at `routines/<dir>/<name>.md`
- **THEN** the hook fails, names the file, and blocks the commit

#### Scenario: Routine file name has a glob character

- **WHEN** a file exists at `routines/A[1].md` beside a valid `routines/A1.md`
- **THEN** the hook fails and names `routines/A[1].md`, and `A1.md` is not checked in its place
