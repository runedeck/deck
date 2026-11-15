## ADDED Requirements

### Requirement: Existing Tools Come First

A *[model][MODEL]* MUST use an existing standard tool before it writes a custom script. A project template takes a template tool, and a check on commit or push takes the hook framework that the *[repository][REPOSITORY]* already runs. A custom script MUST stay short and MUST say in its header which tool the author looked for first.

#### Scenario: Task needs a check on every commit

- **WHEN** a task needs a check on every commit, in a repository that already runs a hook framework
- **THEN** the model adds the check to that framework and writes no runner script of its own

### Requirement: Proofs Show The Real App

A *[proof][PROOF]* MUST record the real app doing what the specification describes: the command in a terminal session, the screen in a browser, or the plugin driven inside the *[harness][HARNESS]*. A recording of a test run MUST NOT count as a proof. When a feature has nothing a user sees, the proof records the closest thing a user runs and says so. A different model judges each *[scenario][SCENARIO]* against the recording, and the owner approves last.

#### Scenario: Proof shows only a test run

- **WHEN** the proof for a scenario records only a test run and its output
- **THEN** the reviewing model fails the scenario, and the author records the real app

### Requirement: Bulk Copies Of Data Wait For A Yes

A model MUST ask the owner before it copies, scans, or hands over files or session data in bulk, and MUST wait for a yes. The question MUST say what would move, how much, and where. Reading data in place for the task the owner gave needs no question. Before another session reads an approved copy, the model MUST scan the copy for secrets and report every hit.

#### Scenario: Task would copy session transcripts

- **WHEN** a task would copy session transcripts into a directory that another session reads
- **THEN** the model says what would move, how much, and where, and copies nothing before the owner's yes

### Requirement: Questions Get Answers Before Edits

When the owner asks about the current state of a file, a setting, or a design, a model MUST answer with the facts first. The answer says whether the current state already does what the question hints at. A question or a hint MUST NOT count as a request to edit. The model edits only when the owner asks for a change, or confirms one after the answer.

#### Scenario: Owner asks whether a file says something

- **WHEN** the owner asks whether a file already says a given thing
- **THEN** the model reports what the file says and edits nothing in that turn

[MODEL]: ../../../../specs/glossary/model.md
[REPOSITORY]: ../../../../specs/glossary/repository.md
[PROOF]: ../../../../specs/glossary/proof.md
[HARNESS]: ../../../../specs/glossary/harness.md
[SCENARIO]: ../../../../specs/glossary/scenario.md
