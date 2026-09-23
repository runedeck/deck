## ADDED Requirements

### Requirement: Markdown System Language

Every *[instruction][INSTRUCTION]* MUST be Markdown with YAML frontmatter, in the dialect the *[repository][REPOSITORY]* accepts: GitHub Flavored Markdown [GFM] plus one YAML frontmatter block. Wikilinks, callouts, and raw HTML blocks are outside the dialect.
Markdown is our plain text format of choice, because language models are trained on it. One file serves a git or jj repository, a vault such as Obsidian, and a *[harness][HARNESS]*.

#### Scenario: Instruction arrives in another format

- **WHEN** an [instruction][INSTRUCTION] is added in a format other than Markdown
- **THEN** the *[validator][VALIDATOR]* rejects the file and suggests a transformation

#### Scenario: Markup outside the dialect appears

- **WHEN** an [instruction][INSTRUCTION] contains a wikilink, a callout, or a raw HTML block
- **THEN** the [validator][VALIDATOR] reports the construct

### Requirement: Metadata Inside Files

Metadata MUST sit in the frontmatter of the file it describes. Frontmatter is the authoritative source, and other stores MAY derive from it.
The one exception is the *[provenance record][PROVENANCERECORD]*, sealed in a *[sidecar][SIDECAR]*, because a seal cannot be part of the content it attests. *[Basis parameters][BASISPARAMETERS]* beside the *[state file][STATEFILE]* do not break this rule: they describe the build, and nothing about the file.

#### Scenario: Provenance evidence arrives

- **WHEN** an adoption or an assembly produces a [provenance record][PROVENANCERECORD] for an *[artifact][ARTIFACT]*
- **THEN** the *[assembler][ASSEMBLER]* seals the record in a [sidecar][SIDECAR] beside the artifact, and the artifact's frontmatter is untouched

#### Scenario: Derived index disagrees with frontmatter

- **WHEN** a derived store, such as the deployment manifest that records the fingerprints of assembled instances, disagrees with an [artifact][ARTIFACT]'s frontmatter on one field
- **THEN** frontmatter wins, and the *[generator][GENERATOR]* regenerates the store

#### Scenario: Harness field arrives

- **WHEN** a field only one [harness][HARNESS] reads, such as an argument hint or an allowed-tools list, is added for a [state file][STATEFILE]
- **THEN** it goes into that harness's [basis parameters][BASISPARAMETERS] beside the state file. That input tells the [assembler][ASSEMBLER] how to build the *[instance][INSTANCE]* for that harness

### Requirement: Reference Citations

A citation of an external source MUST be a reference-style link. A named tag goes inline, and one link definition goes at the end of the file.
A bare number tells the reader nothing at the point of use. Inserting a source renumbers everything after it. Numbered citations also break when the [assembler][ASSEMBLER] combines or splits files.

#### Scenario: Numbered citation appears

- **WHEN** a document cites a source with a bare number
- **THEN** the [validator][VALIDATOR] reports the citation, and the author rewrites it as a named reference link

### Requirement: Defined Terms Cite the Ontology

A term with a special meaning MUST be marked once per file, at its first use, by an emphasized link to its glossary page. Later uses are plain words, and a later link stays plain. Plain italics mean emphasis only.
The [assembler][ASSEMBLER] strips the links from each [instance][INSTANCE] and adds a definition block for only the terms it uses. An always-on rule tells every *[model][MODEL]* that the [repository][REPOSITORY] has an ontology.

#### Scenario: First use is not emphasized

- **WHEN** the first use of a term in a file is a plain link, or a later use is an emphasized link
- **THEN** the [validator][VALIDATOR] reports the use and the file

#### Scenario: Assembler builds an instance with term links

- **WHEN** the [assembler][ASSEMBLER] builds an [instance][INSTANCE] from a [state file][STATEFILE] that links terms
- **THEN** the instance contains no term links and no reference definition block. A short block built from the ontology defines only the terms the instance uses

#### Scenario: Model meets a word with no entry

- **WHEN** a [model][MODEL] is about to use or introduce a word that seems to have a special meaning
- **THEN** the always-on rule has the model look the word up in the ontology first. The model asks the user when the ontology has no entry for it

### Requirement: The Ontology Defines Every Term

The ontology MUST be the only definition of a term. Before writing, the author reads the glossary and uses an existing term, or adds the term to the ontology first.
A term link whose tag resolves to no ontology entry is a finding. While a *[change][CHANGE]* is active, the *[fixer][FIXER]* adds a draft entry for the term and the [validator][VALIDATOR] warns on every link to a draft. The *[archiver][ARCHIVER]* refuses to archive a change that links to a draft term still without a definition.

#### Scenario: Term link points at no entry

- **WHEN** a term link's tag resolves to no entry in the ontology
- **THEN** the [validator][VALIDATOR] reports the term and the file, and the [fixer][FIXER] adds a draft entry, run by the author or by the commit hook

#### Scenario: Change links to a draft term at archive

- **WHEN** a [change][CHANGE] is archived and one of its files links to a draft term
- **THEN** the [archiver][ARCHIVER] refuses the archive and lists each draft term

### Requirement: Glossary Renders From The Ontology

The glossary MUST be a *[render][RENDER]* of the ontology: one generated page per term and an index. A vault keeps one note per concept in the same way, and term links point at those pages.
The [validator][VALIDATOR] renders every page in memory and compares the bytes with the committed page, so a hand edit is drift. People edit only the ontology, and the [generator][GENERATOR] writes the pages, one hop from every link.

#### Scenario: Glossary page drifts from the ontology

- **WHEN** a committed glossary page differs by one byte from a fresh render of the ontology
- **THEN** the [validator][VALIDATOR] reports the page, and the ontology is what counts

[INSTRUCTION]: ../../../../specs/glossary/instruction.md
[REPOSITORY]: ../../../../specs/glossary/repository.md
[HARNESS]: ../../../../specs/glossary/harness.md
[VALIDATOR]: ../../../../specs/glossary/validator.md
[PROVENANCERECORD]: ../../../../specs/glossary/provenance-record.md
[SIDECAR]: ../../../../specs/glossary/sidecar.md
[BASISPARAMETERS]: ../../../../specs/glossary/basis-parameters.md
[STATEFILE]: ../../../../specs/glossary/state-file.md
[ARTIFACT]: ../../../../specs/glossary/artifact.md
[ASSEMBLER]: ../../../../specs/glossary/assembler.md
[GENERATOR]: ../../../../specs/glossary/generator.md
[INSTANCE]: ../../../../specs/glossary/instance.md
[MODEL]: ../../../../specs/glossary/model.md
[CHANGE]: ../../../../specs/glossary/change.md
[FIXER]: ../../../../specs/glossary/fixer.md
[ARCHIVER]: ../../../../specs/glossary/archiver.md
[RENDER]: ../../../../specs/glossary/render.md
[GFM]: https://github.github.com/gfm/
