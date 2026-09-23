## ADDED Requirements

### Requirement: Markdown Links Between Files

A deck file MUST link to another deck file with a relative Markdown link.
A file outside the deck, a vault note or a web page, is linked by its URL or URI.
A wikilink MUST NOT appear in a deck file. Wikilinks are the vault's form, and the `obsidian-placement-and-links` change decides where that boundary sits.
A harness reads `@path` as a file reference. That form belongs in the instruction that uses it, never in a record or a specification.

#### Scenario: Wikilink enters a deck file

- **WHEN** a record, specification, or proposal contains a name between `[[` and `]]`
- **THEN** the check reports the wikilink, and the author rewrites it as a relative Markdown link

#### Scenario: Harness reference enters a record

- **WHEN** a record or specification refers to a file as `@path`
- **THEN** the check reports the reference, and the author rewrites it as a relative Markdown link

### Requirement: Link Targets Resolve

Every relative Markdown link in a deck file MUST point at a file in the repository, and a fragment MUST point at a heading in that file.

#### Scenario: Link target moves

- **WHEN** a linked file is renamed and a link still points at the old path
- **THEN** the offline link check reports the link, and the author fixes it before commit
