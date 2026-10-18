## ADDED Requirements

### Requirement: Code Is Truth

When code and prose disagree, the code is authoritative, because the code is what runs.
A comment MUST NOT repeat what the code beside it says. When the code changes, the comment is what gets left behind.
Anything derived MUST regenerate from its *[source state][SOURCESTATE]* on demand, or it does not exist. A *[validator][VALIDATOR]* only checks that a thing is present and correct, and a *[generator][GENERATOR]* writes every derived file.

#### Scenario: Comment restates the code

- **WHEN** a line has a comment that repeats the statement below it
- **THEN** review removes the comment. A comment says what the code cannot: why, under which constraint, or from which source

#### Scenario: Derived file has no generator

- **WHEN** a committed file is derived and no [generator][GENERATOR] in the *[repository][REPOSITORY]* regenerates it from its [source state][SOURCESTATE]
- **THEN** the [validator][VALIDATOR] reports the file, and the author deletes the file or writes its [generator][GENERATOR]
- **AND** the root index, the directory indexes, the glossary pages, and the changelog each have one

### Requirement: One Home Per Fact

A fact MUST be stated in one file. Every other file links there.
Two copies of one fact drift apart as soon as one of them changes.

#### Scenario: Fact appears in a second file

- **WHEN** a statement is copied into a second file
- **THEN** review replaces the copy with a link

[SOURCESTATE]: ../../../../specs/glossary/source-state.md
[VALIDATOR]: ../../../../specs/glossary/validator.md
[GENERATOR]: ../../../../specs/glossary/generator.md
[REPOSITORY]: ../../../../specs/glossary/repository.md
