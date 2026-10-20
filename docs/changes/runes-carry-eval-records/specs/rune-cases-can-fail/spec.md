## ADDED Requirements

### Requirement: Cases Run With And Without The Rune

An evaluation case, an eval case for short, gives a *[model][MODEL]* one task and scores the answer. The eval runner is the role that runs the cases of one *[rune][RUNE]*. It MUST run each case twice, on the same model and the same *[instance][INSTANCE]* that the *[assembler][ASSEMBLER]* builds for one *[harness][HARNESS]*: once with the rune loaded and once without it. A *[rule][RULE]* MUST load as always-on context in the run with the rune only.

#### Scenario: Eval runner runs a case of a rule

- **WHEN** the eval runner runs a case of a rule
- **THEN** the run with the rule starts with the rule's text in context, the run without it has none, and the same graders score both answers

### Requirement: Every Case Can Fail

An eval case MUST be able to fail. On the model it is recorded for, the run without the rune MUST score lower than the run with it. When a rune fails its own case, the author decides whether the rune is weak or the case is wrong, and says which in the *[change][CHANGE]* that fixes it. A rune MUST NOT gain text whose only purpose is to pass its own case.

#### Scenario: Both runs pass a case

- **WHEN** the run with the rune and the run without it both pass a case on the recorded model
- **THEN** the author rewrites the case until the run without the rune scores lower, or drops the case

### Requirement: Graders Give The Same Result

A grader is a check that scores one property of an answer. Each grader MUST give the same result every time it reads the same answer: a text pattern, a check of which tools ran and in which order, or a check that a file exists. A grader that asks a model for a judgment MUST NOT score a case. A pattern for a forbidden action MUST match the action as a model uses it, such as a command at the start of a line.

#### Scenario: Answer quotes a forbidden command

- **WHEN** an answer names a forbidden command only to explain why it does not use it
- **THEN** the grader for that forbidden action finds no use, and the case keeps its score

### Requirement: Suites Pair A Direct Case With A Near Miss

An eval suite is the set of cases for one rune. A suite MUST hold two or three cases. One case MUST ask for the behavior directly. One case MUST be a near miss: a task that does not mention the behavior, where the rune must still hold. Each case MUST stay within four turns and use read-only tools, so it tests what the model says and plans and leaves the disk alone.

#### Scenario: Suite holds only direct cases

- **WHEN** every case in a suite names the behavior that its rune requires
- **THEN** review asks for a near-miss case before the suite counts as evidence

### Requirement: Every Run Leaves A Record

The eval runner MUST write one record for each run of a suite. The record MUST name the rune and its kind, the digest of the instance, the model, the run count, the time, the harness version, the overall score, the mean difference the rune makes, and each case's score with and without the rune. A new run MUST add a record and MUST NOT rewrite an old one. A run in which the harness fails a case MUST NOT write a record.

#### Scenario: Suite run finishes cleanly

- **WHEN** the eval runner finishes a run in which every case ran with the rune and without it
- **THEN** a new record names the instance digest and the model, and every older record of the suite is unchanged

### Requirement: Recorded Run Shows Both Answers

When the author asks for a recording, the eval runner MUST record the terminal session of the run and render it as an animated image. For each case, the image MUST show both scores and the answers with and without the rune, so a reader sees what the rune changed without opening the record. The recording MUST go into the *[proof][PROOF]* directory of the change that adds or changes the suite.

#### Scenario: Eval runner records a suite run

- **WHEN** the eval runner records a run of a suite
- **THEN** the animated image shows, for each case, both scores and the first lines of both answers

[MODEL]: ../../../../specs/glossary/model.md
[RUNE]: ../../../../specs/glossary/rune.md
[INSTANCE]: ../../../../specs/glossary/instance.md
[ASSEMBLER]: ../../../../specs/glossary/assembler.md
[HARNESS]: ../../../../specs/glossary/harness.md
[RULE]: ../../../../specs/glossary/rule.md
[CHANGE]: ../../../../specs/glossary/change.md
[PROOF]: ../../../../specs/glossary/proof.md
