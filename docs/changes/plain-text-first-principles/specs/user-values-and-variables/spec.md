## ADDED Requirements

### Requirement: Variables Are $NAME

A shared *[instruction][INSTRUCTION]* MUST NOT contain a value that belongs to one user or one machine. Personal paths and account names leak into [instructions][INSTRUCTION] easily.

#### Scenario: Instruction embeds a configurable value

- **WHEN** an [instruction][INSTRUCTION] contains a hardcoded path, account, or host that belongs to one user or machine
- **THEN** the *[validator][VALIDATOR]* reports the value, and the author replaces it with a variable reference and explains the variable in one sentence

### Requirement: Both Shell Forms Resolve In The Shell

It MUST refer to the value as a shell variable, `$NAME`, or `${NAME}` when text follows the name directly, and no *[harness][HARNESS]* syntax is needed. A name ends at the first character that is not a letter, a digit, or an underscore. The shell default form, `${NAME:-fallback}`, supplies a value when nothing sets the variable.

#### Scenario: Assembler meets a user variable

- **WHEN** the *[assembler][ASSEMBLER]* builds an *[instance][INSTANCE]* from a *[state file][STATEFILE]* that refers to `$NAME`
- **THEN** the [instance][INSTANCE] keeps the reference as written, because the [assembler][ASSEMBLER] substitutes no user variable
- **AND** the value resolves in the shell when the *[model][MODEL]* runs a command, because every [harness][HARNESS] has a shell

### Requirement: Canon Stays Vendor-Neutral

Some things only one [harness][HARNESS] understands: its own placeholders, such as Claude Code's `$ARGUMENTS`, and wording or mechanisms only that [harness][HARNESS] needs. These MUST be in that [harness][HARNESS]'s *[basis parameters][BASISPARAMETERS]* beside the *[canon][CANON]*, and the [canon][CANON] MUST NOT contain them.

#### Scenario: Harness placeholder enters the canon

- **WHEN** a [canon][CANON] uses a placeholder form that one [harness][HARNESS] documents and the others do not
- **THEN** the [validator][VALIDATOR] reports the line, and the author moves it into that [harness][HARNESS]'s [basis parameters][BASISPARAMETERS] and keeps the `$NAME` form in the [canon][CANON]

#### Scenario: Harness needs different wording

- **WHEN** one [harness][HARNESS] needs wording the others do not
- **THEN** the wording goes into that [harness][HARNESS]'s [basis parameters][BASISPARAMETERS], and the [canon][CANON] does not change
- **AND** the [basis parameters][BASISPARAMETERS] file names its [harness][HARNESS] and adds to the [canon][CANON] without replacing it

### Requirement: Assembly Projects Out One Harness

The *[source state][SOURCESTATE]* is the superposition of the [canon][CANON] and its [basis parameters][BASISPARAMETERS], and the [assembler][ASSEMBLER] MUST project out one [harness][HARNESS] from it. The [canon][CANON] alone MUST stay readable and neutral.

#### Scenario: Instruction depends on one harness's hook event

- **WHEN** an [instruction][INSTRUCTION] depends on a mechanism that only one [harness][HARNESS] has
- **THEN** the dependency moves into that [harness][HARNESS]'s [basis parameters][BASISPARAMETERS], and the [canon][CANON] works without it

[INSTRUCTION]: ../../../../specs/glossary/instruction.md
[HARNESS]: ../../../../specs/glossary/harness.md
[VALIDATOR]: ../../../../specs/glossary/validator.md
[ASSEMBLER]: ../../../../specs/glossary/assembler.md
[INSTANCE]: ../../../../specs/glossary/instance.md
[STATEFILE]: ../../../../specs/glossary/state-file.md
[MODEL]: ../../../../specs/glossary/model.md
[BASISPARAMETERS]: ../../../../specs/glossary/basis-parameters.md
[CANON]: ../../../../specs/glossary/canon.md
[SOURCESTATE]: ../../../../specs/glossary/source-state.md
