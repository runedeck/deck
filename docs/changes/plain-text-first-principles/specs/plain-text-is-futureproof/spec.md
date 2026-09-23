## ADDED Requirements

### Requirement: Plain Text Representation

Every *[artifact][ARTIFACT]* MUST have one authoritative *[representation][REPRESENTATION]* in plain text: the file itself when the file is text, and a description beside it otherwise.
A *[model][MODEL]* reads that plain text. An encoding wrapper such as base64 is not plain text.
Other stores MAY keep other [representations][REPRESENTATION], and every one of them derives from the plain text.

#### Scenario: Database is rebuilt from plain text

- **WHEN** a database is deleted and rebuilt from plain text
- **THEN** nothing is missing from it, because the plain text stored every fact the database held

### Requirement: UTF-8 Encoding

A text [artifact][ARTIFACT] MUST be valid UTF-8 without a byte order mark.
UTF-8 is the encoding the editors, *[harnesses][HARNESS]*, git hosts, and Markdown parsers on our roster read without configuration.
The WHATWG Encoding Standard requires it for every new format [ENCODING], and JSON requires it for interchange and forbids the byte order mark [RFC8259].

#### Scenario: Text file fails to decode as UTF-8

- **WHEN** a text [artifact][ARTIFACT] holds bytes that are not valid UTF-8, or starts with a byte order mark
- **THEN** the *[validator][VALIDATOR]* reports the file

### Requirement: Binary Assets Carry a Description

An [artifact][ARTIFACT] with no plain-text [representation][REPRESENTATION], that is a file git labels binary [GITATTR], MUST have a plain-text description beside it. The description is a sibling `<name>.md`, or a README that names the file, and it says what the file is and where it is used.
A [model][MODEL] cannot use an image, a font, or an archive without that description, and a diff cannot show what changed in one.

#### Scenario: Binary asset enters the repository

- **WHEN** a file that git labels binary is added to the *[repository][REPOSITORY]*
- **THEN** a plain-text description sits beside it, or the [validator][VALIDATOR] reports the file

### Requirement: Lossless Renders

A committed *[render][RENDER]* of a *[state file][STATEFILE]* MUST regenerate from that file byte for byte. The *[generator][GENERATOR]* that writes the render is kept in the [repository][REPOSITORY], so the [validator][VALIDATOR] can rerun it and compare. A render nobody can rerun is a second home for the same facts, and the two drift apart.
An assembled *[instance][INSTANCE]* is not a render: instructions-stay-vendor-neutral covers it.

#### Scenario: Render drifts from its state file

- **WHEN** a committed [render][RENDER] differs by one byte from a fresh regeneration from its [state file][STATEFILE]
- **THEN** the [validator][VALIDATOR] reports the drift, and the state file is what counts

### Requirement: Projections Are Never Authoritative

A *[projection][PROJECTION]* is a representation that drops information from its *[source state][SOURCESTATE]*. A projection operator in quantum mechanics does the same: it keeps one component of a state and discards the rest.
A projection MUST NOT replace the source state it was taken from. A search index is never committed. A snapshot of something outside the [repository][REPOSITORY] is committed only with a *[provenance record][PROVENANCERECORD]* that says where it came from.

#### Scenario: Committed file is generated from a projection

- **WHEN** a committed file is generated from a [projection][PROJECTION] instead of from its [source state][SOURCESTATE]
- **THEN** the [validator][VALIDATOR] reports the file

#### Scenario: Snapshot arrives without a provenance record

- **WHEN** a snapshot of something outside the [repository][REPOSITORY] is committed with no [provenance record][PROVENANCERECORD]
- **THEN** the [validator][VALIDATOR] reports the snapshot

[ARTIFACT]: ../../../../specs/glossary/artifact.md
[REPRESENTATION]: ../../../../specs/glossary/representation.md
[MODEL]: ../../../../specs/glossary/model.md
[HARNESS]: ../../../../specs/glossary/harness.md
[VALIDATOR]: ../../../../specs/glossary/validator.md
[REPOSITORY]: ../../../../specs/glossary/repository.md
[RENDER]: ../../../../specs/glossary/render.md
[STATEFILE]: ../../../../specs/glossary/state-file.md
[GENERATOR]: ../../../../specs/glossary/generator.md
[INSTANCE]: ../../../../specs/glossary/instance.md
[PROJECTION]: ../../../../specs/glossary/projection.md
[SOURCESTATE]: ../../../../specs/glossary/source-state.md
[PROVENANCERECORD]: ../../../../specs/glossary/provenance-record.md
[GITATTR]: https://git-scm.com/docs/gitattributes
[ENCODING]: https://encoding.spec.whatwg.org/#preface
[RFC8259]: https://www.rfc-editor.org/rfc/rfc8259.html#section-8.1
