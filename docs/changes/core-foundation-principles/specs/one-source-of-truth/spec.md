## ADDED Requirements

### Requirement: Code Is Truth

When code and prose disagree, the code is authoritative, because the code is what runs.
A comment MUST NOT repeat what the code beside it says. When the code changes, the comment is what gets left behind.
A comment says what the code cannot: why, under which constraint, or from which source.

#### Scenario: Comment restates the code

- **WHEN** a line has a comment that repeats the statement below it
- **THEN** review removes the comment

### Requirement: One Home Per Fact

A fact MUST be stated in one file. Every other file links there.
Two copies of one fact drift apart as soon as one of them changes.

#### Scenario: Fact appears in a second file

- **WHEN** a statement is copied into a second file
- **THEN** review replaces the copy with a link
