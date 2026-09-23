## ADDED Requirements

### Requirement: Directories Direct

A directory name MUST tell a tool what to do with the files inside it, and a name no tool recognizes, such as `misc/` or `stuff/`, is forbidden.
`runes/core/skills/` tells assembly to treat its files as skills, `.claude/rules/` tells Claude Code to load its files as rules, and `docs/changes/archive/` tells the validators to skip.
Write `directory` in docs, commit messages, and conversation. Do not write `folder`.

#### Scenario: Content goes into a catch-all directory

- **WHEN** a new directory has a name that no tool recognizes, such as `misc/`
- **THEN** review renames it to a name a tool recognizes, or moves its files into a directory that has one

#### Scenario: Directory name is misspelled

- **WHEN** `.claude/rules/` is written `.claude/rule/`
- **THEN** review corrects the name, because Claude Code loads nothing from the misspelling and reports no error

### Requirement: Catch-All Directories Drain

An inbox, temp, or downloads directory is fine as a queue. It is not a home.
Every item in it MUST either move to a directory a tool recognizes or be deleted. A session that touches the queue leaves it empty.

#### Scenario: Item stays in the queue

- **WHEN** a session ends and an item is still in a catch-all directory
- **THEN** the session reports the item, and the next intake moves or deletes it
