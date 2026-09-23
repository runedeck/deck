## ADDED Requirements

### Requirement: Markdown System Language

Every instruction MUST be Markdown with YAML frontmatter, in the dialect the deck accepts: GitHub Flavored Markdown [GFM] plus one YAML frontmatter block, as rumdl checks it. Wikilinks, callouts, and raw HTML blocks are outside the dialect.
Markdown is our plain text format of choice, because it is an LLM-native format and one file serves a git or jj repository, a note-taking vault such as Obsidian, and an LLM harness.

#### Scenario: Instruction arrives in another format

- **WHEN** an instruction is added in a format other than Markdown
- **THEN** validation rejects the file and suggests a transformation

#### Scenario: Markup outside the dialect appears

- **WHEN** an instruction holds a wikilink, a callout, or a raw HTML block
- **THEN** the check reports the construct

### Requirement: Metadata Inside Files

Metadata MUST sit in the frontmatter of the file it describes. The one exception is sealed provenance evidence, which goes into `.provenance/` sidecars because a seal cannot be part of the content it attests.
Frontmatter is the authoritative source. Other stores MAY derive from it.
A deployment manifest records the fingerprints of assembled instances. It describes outputs rather than authored files, so it counts as a derived store.

#### Scenario: Provenance evidence arrives

- **WHEN** an adoption produces provenance evidence for an artifact
- **THEN** the evidence is sealed in a sidecar beside the artifact, not in its frontmatter

#### Scenario: Derived index disagrees with frontmatter

- **WHEN** a derived store and an artifact's frontmatter disagree on one field
- **THEN** frontmatter wins, and the store regenerates

### Requirement: Flat Frontmatter

Frontmatter MUST be flat: scalar values and lists of scalars, no nested objects.
Obsidian's Properties panel does not render nested objects. The one tolerated exception is the Agent Skills `metadata` map in an instruction, which that specification requires.

#### Scenario: Nested object enters frontmatter

- **WHEN** a file has a nested object in its frontmatter
- **THEN** the schema check reports the field

### Requirement: Reference Citations

A citation of an external source MUST be a reference-style link: a named tag inline, and one link definition at the end of the file.
A bare number tells the reader nothing at the point of use.

#### Scenario: Numbered citation appears

- **WHEN** a document cites a source with a bare number
- **THEN** review converts the citation into a named reference link

### Requirement: Defined Terms Cite the Ontology

A term that a document defines MUST be set in italics at first use and cited with a reference tag, `*target* [TARGET]`. The tag's definition at the end of the file gives the term's IRI in the ontology.
Later uses in the same file are plain text.

#### Scenario: Term appears without its tag

- **WHEN** a document sets a term in italics at first use and the tag beside it is missing or names another IRI
- **THEN** validation reports the term and the file

### Requirement: The Ontology Defines Every Term

The ontology MUST be the only definition of a term.
Before writing, the author reads the glossary. A requirement uses an existing term, or the author adds the term to the ontology first.
An italic term in a specification, a record, or a proposal with no ontology entry MUST fail validation.

#### Scenario: Specification uses a term the ontology lacks

- **WHEN** a specification sets a term in italics and `ontology/rune.ttl` has no term with that label
- **THEN** validation reports the term and the ontology file, and the author adds the term there first

#### Scenario: Reference tag names a missing term

- **WHEN** a reference definition under the ontology namespace uses a local name the ontology does not declare
- **THEN** validation fails and reports the file and the tag

### Requirement: Glossary Renders From The Ontology

The glossary MUST be a *render* [RENDER] of the ontology: a check regenerates it and compares the bytes with the committed file. A hand edit to the glossary is drift.
The glossary gives a reader every term's definition one hop from its tag, and the ontology stays the only source.

#### Scenario: Glossary drifts from the ontology

- **WHEN** a term's line in the glossary differs from a fresh rendering of the ontology
- **THEN** the check reports the term, and the ontology is what counts

[GFM]: https://github.github.com/gfm/
[RENDER]: https://runedeck.ai/ns#Render
