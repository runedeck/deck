## ADDED Requirements

### Requirement: Plain Text Representation

Every *artifact* [ARTIFACT] MUST have one authoritative *representation* [REPRESENTATION] in plain text: the file itself when the file is text, and a description beside it otherwise.
A model reads that plain text. An encoding wrapper such as base64 does not qualify as plain text.
Other stores MAY keep other representations, and every one of them derives from the plain text.

#### Scenario: Database is rebuilt from plain text

- **WHEN** a database is deleted and rebuilt from plain text
- **THEN** nothing is missing from it, because the plain text stored every fact the database held

### Requirement: UTF-8 Encoding

A text artifact MUST be valid UTF-8 without a byte order mark.
UTF-8 is the encoding the editors, harnesses, git hosts, and Markdown parsers on our roster read without configuration.
The WHATWG Encoding Standard requires it for every new format [ENCODING], and JSON requires it for interchange and forbids the byte order mark [RFC8259].

#### Scenario: Text file fails to decode as UTF-8

- **WHEN** a text artifact holds bytes that are not valid UTF-8, or starts with a byte order mark
- **THEN** the check reports the file

### Requirement: Binary Assets Carry a Description

An artifact with no plain-text representation, i.e. a file that git labels binary [GITATTR], MUST have a plain-text description beside it: a sibling `<name>.md`, or a README that names the file, saying what the file is and where it is used.
A model cannot use an image, a font, or an archive without that description, and a diff cannot show what changed in one.

#### Scenario: Binary asset enters the repository

- **WHEN** a file that git labels binary is added to the repository
- **THEN** a plain-text description sits beside it, or the check reports the file

### Requirement: Lossless Renders

A committed *render* [RENDER] of a plain-text source MUST regenerate from that source byte for byte through a command in the repository, so a check can rerun it. A render nobody can rerun is a second source of the same facts, and the two drift apart.
An assembled instance is not a render: harness-independent-authoring covers it.

#### Scenario: Render drifts from its source

- **WHEN** a committed render differs by one byte from a fresh regeneration from its source
- **THEN** a check reports the drift, and the source is what counts

### Requirement: Projections Are Never a Source

A representation that drops information is a *projection* [PROJECTION], and a projection MUST NOT stand in for its source: a search index stays uncommitted, and a snapshot of a source outside the repository is committed only with a provenance sidecar that names its upstream.

#### Scenario: Snapshot arrives without a sidecar

- **WHEN** a snapshot of a source outside the repository is committed with no provenance sidecar
- **THEN** the check reports the snapshot

[ARTIFACT]: https://runedeck.ai/ns#Artifact
[REPRESENTATION]: https://runedeck.ai/ns#Representation
[RENDER]: https://runedeck.ai/ns#Render
[PROJECTION]: https://runedeck.ai/ns#Projection
[GITATTR]: https://git-scm.com/docs/gitattributes
[ENCODING]: https://encoding.spec.whatwg.org/#preface
[RFC8259]: https://www.rfc-editor.org/rfc/rfc8259.html#section-8.1
