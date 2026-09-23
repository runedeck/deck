## ADDED Requirements

### Requirement: Directories Direct

A directory name MUST tell a tool what to do with its files. A skills directory tells the *[assembler][ASSEMBLER]* to treat them as skills, and a rules directory tells a *[harness][HARNESS]* to load rules. An archive directory tells the *[validator][VALIDATOR]* to skip it. A name no tool recognizes, such as a miscellaneous directory, MUST NOT appear.
Review enforces the judgment, a *[missed requirement][MISSEDREQUIREMENT]* in the *[coverage][COVERAGE]* table until a tool exists.

#### Scenario: Content goes into a catch-all directory

- **WHEN** a new directory has a name that no tool recognizes, such as a miscellaneous directory
- **THEN** review renames it to a name a tool recognizes, or moves its files into a directory that has one

#### Scenario: Wrong word for directory appears

- **WHEN** a doc or a commit message says `folder`
- **THEN** the [validator][VALIDATOR] reports the word, and the author writes `directory`

### Requirement: Qualifier Directory Names Are Checked

One narrow check MUST cover the directory names a [harness][HARNESS] acts on, such as its rules directory. A typo there silently disables content, and the harness reports no error. The [validator][VALIDATOR] reports a name the harness does not document.
The routing judgment itself stays with review. A wrong name elsewhere costs little, and a general check would force every directory onto an allowlist, which the owner rejected.

#### Scenario: Qualifier directory name is misspelled

- **WHEN** a directory name a [harness][HARNESS] acts on, such as its rules directory, is misspelled
- **THEN** the [validator][VALIDATOR] reports the name, because the harness loads nothing from the misspelling and reports no error

### Requirement: Catch-All Directories Drain

An inbox, temp, or downloads directory is a queue. It is not a home, and every item in it MUST move to a directory a tool recognizes, or be deleted.
A queue drains by age, copied from GitHub's stale bot. Sixty days after an item's first commit, the [validator][VALIDATOR] reports it as stale. Sixty-seven days after, the item is an error that blocks until it moves or is deleted. The escape hatch is an unsorted archive directory: an item moved there never ages.

#### Scenario: Item ages in the queue

- **WHEN** an item has been in a queue directory for sixty days after its first commit
- **THEN** the [validator][VALIDATOR] reports it as stale, and from sixty-seven days as an error

#### Scenario: Item moves to the unsorted archive

- **WHEN** an item moves from a queue directory to the unsorted archive
- **THEN** the [validator][VALIDATOR] stops aging it, and the item waits there until someone comes back to it

[ASSEMBLER]: ../../../../specs/glossary/assembler.md
[HARNESS]: ../../../../specs/glossary/harness.md
[MISSEDREQUIREMENT]: ../../../../specs/glossary/missed-requirement.md
[COVERAGE]: ../../../../specs/glossary/coverage.md
[VALIDATOR]: ../../../../specs/glossary/validator.md
