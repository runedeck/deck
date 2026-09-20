## ADDED Requirements

### Requirement: Markdown System Language

Every instruction artifact MUST be in Markdown, optionally with YAML frontmatter. Markdown is the chosen representation of plain text. The same format serves a git or jj repository, a PKM vault, and an LLM harness.

#### Scenario: Artifact arrives in another format

- **WHEN** a change adds an instruction artifact that is not Markdown
- **THEN** validation rejects the artifact and suggests a transformation

### Requirement: Metadata Inside Files

Metadata MUST live in the frontmatter of the file it describes, with one recorded exception: sealed provenance evidence lives in `.provenance/` sidecars, and its details arrive in a later change. Frontmatter stays the authoritative source, and other stores MAY derive from it.

#### Scenario: Provenance evidence arrives

- **WHEN** an adoption produces provenance evidence for an artifact
- **THEN** the evidence is sealed in a sidecar beside the artifact, never in its frontmatter

#### Scenario: Derived index disagrees with frontmatter

- **WHEN** a derived store and an artifact's frontmatter state different values for one field
- **THEN** frontmatter wins and the store regenerates

### Requirement: Flat Frontmatter

Frontmatter MUST stay flat: scalar values and lists of scalars, never nested objects. Obsidian's Properties panel does not render nested objects.

#### Scenario: Nested object enters frontmatter

- **WHEN** a changed file carries a nested object in frontmatter
- **THEN** the schema check reports the field

### Requirement: Directories Direct

A directory name MUST state routing, never categorization. A qualifier directory name is configuration, and a typo silently disables its content. The term is directory, never folder, in docs, commit messages, and conversation.

#### Scenario: Content goes into a catch-all directory

- **WHEN** a change adds a directory whose name states no routing decision
- **THEN** review renames the directory or relocates the content

### Requirement: Runtime Variables

A runtime instruction MUST reference configuration by `$NAME` environment variables.

#### Scenario: Instruction embeds a configurable value

- **WHEN** a changed instruction hardcodes a value the configuration owns
- **THEN** review replaces the value with its `$NAME` reference

### Requirement: Template Placeholders

A template MUST use `${NAME}` placeholders with end-of-line `%%` comments, instantiable with `envsubst`.

#### Scenario: Template invents placeholder syntax

- **WHEN** a changed template uses a placeholder form other than `${NAME}`
- **THEN** review converts the template to the convention

### Requirement: Configuration Defaults

A module MUST include `defaults.yaml` with the full schema and working defaults. User overrides live in a gitignored `config.yaml` merged recursively. The config loading exports the merged result as environment variables.

#### Scenario: Module requires user configuration to start

- **WHEN** a module fails without a user `config.yaml`
- **THEN** validation reports the missing default

#### Scenario: Override merges over defaults

- **WHEN** a user `config.yaml` sets one field
- **THEN** the merged configuration carries that value and every other committed default

#### Scenario: Merged configuration exports

- **WHEN** the configuration loads
- **THEN** the merged result exports as environment variables, so instructions reference it by `$NAME`

### Requirement: One Checker Per Concern

Every validation concern MUST have one chosen checker, recorded in the checker map. A new concern or a tool change arrives through a decision record.

#### Scenario: Concern has no chosen checker

- **WHEN** a change adds a validation concern no chosen checker covers
- **THEN** the checker map records the gap and a decision record picks the tool

### Requirement: One Validation Path

Every check MUST run through one shared configuration locally and in CI. A check that exists only in CI is a violation. An environment without the runner falls back to the committed hook path with the same checks.

#### Scenario: CI-only check appears

- **WHEN** a workflow adds a check absent from the shared configuration
- **THEN** review moves the check into the shared configuration

#### Scenario: Runner is absent

- **WHEN** an environment lacks the runner
- **THEN** the committed hook path runs the same checker roster, and a roster difference is a violation

### Requirement: Reference Citations

A document MUST cite an external source with a reference-style link: a named tag inline and one link definition at the end of the file. A numbered citation carries no meaning at the point of use.

#### Scenario: Numbered citation appears

- **WHEN** a changed document cites a source with a bare number
- **THEN** review converts the citation to a named reference link
