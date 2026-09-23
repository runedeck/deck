## ADDED Requirements

### Requirement: Type On Every File

Every Markdown file in the deck, other than the reserved names, MUST have a `type` key with a nonempty value as required by the Open Knowledge Format 0.2.
An instruction keeps it under the Agent Skills `metadata` map, because that specification reserves no other place for a foreign key. That map is the one nested object Flat Frontmatter tolerates, and a top-level `type` waits for a harness matrix that shows every harness accepts it.

#### Scenario: File without a type appears

- **WHEN** a Markdown file outside the reserved names has no non-empty `type`, in its frontmatter or, for an instruction, under `metadata`
- **THEN** validation reports the file, and the author adds the key

### Requirement: Path Is The Identifier

A file's identifier MUST be its path inside the deck without the `.md` suffix, the way the Open Knowledge Format derives it.
The deck adds one rule of its own: an `id` key, when present, MUST equal that identifier.

#### Scenario: Identifier key appears

- **WHEN** a file has an `id` key that differs from its path identifier
- **THEN** validation reports the key, and the author removes or corrects it

### Requirement: Reserved Names

`index.md` and `log.md` MUST NOT have frontmatter at any level of the deck. The one exception is `okf_version` on the bundle root `index.md`.
The check accepts `okf_version` on the bundle root `index.md` and rejects every other frontmatter key on a reserved file.
`index.md` lists a directory. `log.md` is a newest-first history under `YYYY-MM-DD` date headings, as sections 8 and 9 of the format describe.

#### Scenario: Reserved name holds frontmatter

- **WHEN** an `index.md` or `log.md` has a frontmatter key, other than `okf_version` on the bundle root `index.md`
- **THEN** validation rejects the key, and the content that needs frontmatter moves to a file with another name

### Requirement: Bundle Declares Its Version

The `index.md` at the root of a repository that is a bundle MUST declare `okf_version: "0.2"`. The deck is one such repository, and so is any other repository we read as a bundle.
The format makes the declaration optional. We require it, so a consumer that reads the repository as a bundle finds the version there.

#### Scenario: Version declaration is absent

- **WHEN** the repository root `index.md` has no `okf_version` key
- **THEN** validation reports the omission
