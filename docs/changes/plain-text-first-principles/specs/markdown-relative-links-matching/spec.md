## ADDED Requirements

### Requirement: Markdown Links Between Files

A *[repository][REPOSITORY]* file MUST link to another with a relative Markdown link. A vault note or a web page is linked by its address.
A wikilink MUST NOT appear: a graph tool sees no edge in it, and a vault resolves relative links natively.
A *[state file][STATEFILE]* includes another file with `![text](relative path)`, and the *[assembler][ASSEMBLER]* translates the include for each *[harness][HARNESS]*. The at-sign form MUST NOT appear in a shared *[instruction][INSTRUCTION]*.

#### Scenario: Wikilink enters a repository file

- **WHEN** a [repository][REPOSITORY] file contains a name between `[[` and `]]`
- **THEN** the *[validator][VALIDATOR]* reports the wikilink, and the author rewrites it as a relative Markdown link

#### Scenario: At-sign reference enters a state file

- **WHEN** a [state file][STATEFILE] refers to a file with the at-sign form
- **THEN** the [validator][VALIDATOR] reports the reference, and the author rewrites it as an include

#### Scenario: Include is assembled per harness

- **WHEN** a [state file][STATEFILE] includes another file
- **THEN** the Claude Code and Gemini *[instances][INSTANCE]* get the at-sign file reference. A [harness][HARNESS] with no include of its own gets the file's content inlined

### Requirement: Link Targets Resolve

Every internal link in a [repository][REPOSITORY] file MUST resolve. A relative link points at a file, a fragment at a heading in that file, and a term link at a generated glossary page. The [validator][VALIDATOR] checks every link offline, excludes nothing, and only reports.
The *[fixer][FIXER]* repairs a link to a term the ontology lacks by adding a draft entry. A commit hook may run the fixer before the validator. An external link never blocks a commit.

#### Scenario: Link target moves

- **WHEN** a linked file is renamed and a link still points at the old path
- **THEN** the [validator][VALIDATOR] reports the link, and the author fixes it before commit

#### Scenario: Term link points at no page

- **WHEN** a term link points at a glossary page that does not exist
- **THEN** the [fixer][FIXER] adds a draft entry to the ontology and the *[generator][GENERATOR]* writes the page. The link resolves, and the [validator][VALIDATOR] warns on the draft

#### Scenario: External link is dead

- **WHEN** a changed file links to a web page that does not answer
- **THEN** the push reports the link as a warning and does not stop the push
- **AND** a weekly online job reports dead links across the [repository][REPOSITORY]

[REPOSITORY]: ../../../../specs/glossary/repository.md
[STATEFILE]: ../../../../specs/glossary/state-file.md
[ASSEMBLER]: ../../../../specs/glossary/assembler.md
[HARNESS]: ../../../../specs/glossary/harness.md
[INSTRUCTION]: ../../../../specs/glossary/instruction.md
[VALIDATOR]: ../../../../specs/glossary/validator.md
[INSTANCE]: ../../../../specs/glossary/instance.md
[FIXER]: ../../../../specs/glossary/fixer.md
[GENERATOR]: ../../../../specs/glossary/generator.md
