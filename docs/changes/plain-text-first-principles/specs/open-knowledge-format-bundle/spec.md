## ADDED Requirements

### Requirement: Type On Every File

The `type` key MUST be optional in a Markdown file. A file's type comes from the *[structure schema][STRUCTURESCHEMA]* of its nearest directory when that schema fixes the type to one value. An explicit key in the file overrides it. A file with neither is untyped, and the *[validator][VALIDATOR]* reports nothing for it.
The graph export fills the type in. A strict outside reader of the Open Knowledge Format sees a file without the key as untyped, and we accept that.

#### Scenario: Type is derived from the directory

- **WHEN** a file has no `type` key and its directory's [structure schema][STRUCTURESCHEMA] fixes the type to one value
- **THEN** the graph export, a *[projection][PROJECTION]* the *[generator][GENERATOR]* writes, gives the file's node that type

#### Scenario: Explicit key overrides the directory

- **WHEN** a file in a typed directory has its own `type` key
- **THEN** that key is the file's type, in the graph export too

### Requirement: Path Is The Identifier

A file's identifier MUST be its web address: the *[repository][REPOSITORY]*'s base address plus the file's path inside the [repository][REPOSITORY] without the `.md` suffix. The Open Knowledge Format and a vault derive it the same way.
The [repository][REPOSITORY] adds one rule of its own: an `id` key, when present, MUST equal that identifier. Moving a file rewrites every link to it in the same commit, and the [validator][VALIDATOR] reports any link missed.

#### Scenario: Identifier key appears

- **WHEN** a file has an `id` key that differs from its path identifier, such as a random id or a bare file name
- **THEN** the [validator][VALIDATOR] reports the key, and the author removes or corrects it

#### Scenario: File moves

- **WHEN** a file moves to another path
- **THEN** every link to it is rewritten in the same commit, and the [validator][VALIDATOR] reports a link left pointing at the old path

### Requirement: Reserved Names

`index.md` and `log.md` MUST NOT have frontmatter at any level of the [repository][REPOSITORY], except `okf_version` on the root `index.md`. A README stays a README: the reserved names bind only where such a file exists.
Only the root index has the version line. The [generator][GENERATOR] writes the root index, every directory index, and the changelog, and the changelog is a separate file from `log.md`. A directory's authored page is a directory note inside it, named after the directory.

#### Scenario: Reserved name holds frontmatter

- **WHEN** an `index.md` or `log.md` has a frontmatter key, other than `okf_version` on the root `index.md`
- **THEN** the [validator][VALIDATOR] rejects the key, and the content that needs frontmatter moves to a file with another name

#### Scenario: Directory index is edited by hand

- **WHEN** a committed `index.md` differs from what the [generator][GENERATOR] writes: the directory note (Obsidian's `folder note` pattern) included with `![text](relative path)`, then the list of contents
- **THEN** the [validator][VALIDATOR] reports the drift, and the directory note is what counts

### Requirement: Bundle Declares Its Version

The root `index.md` of a [repository][REPOSITORY] read as a bundle MUST declare `okf_version: "0.2"`. The [generator][GENERATOR] writes the declaration into the root index, and the [validator][VALIDATOR] checks it.
The Open Knowledge Format makes the declaration optional. We require it, so a consumer that reads the [repository][REPOSITORY] as a bundle finds the version there.
The check is a warning until the [generator][GENERATOR] exists, and an error after.

#### Scenario: Version declaration is absent

- **WHEN** the root `index.md` has no `okf_version` key
- **THEN** the [validator][VALIDATOR] reports the omission, as a warning until the [generator][GENERATOR] exists and as an error after

[STRUCTURESCHEMA]: ../../../../specs/glossary/structure-schema.md
[VALIDATOR]: ../../../../specs/glossary/validator.md
[PROJECTION]: ../../../../specs/glossary/projection.md
[GENERATOR]: ../../../../specs/glossary/generator.md
[REPOSITORY]: ../../../../specs/glossary/repository.md
