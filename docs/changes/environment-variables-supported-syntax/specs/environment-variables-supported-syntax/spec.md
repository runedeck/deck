## ADDED Requirements

### Requirement: Value Sources Have One Order

A configurable value in an *[instruction][INSTRUCTION]* MUST come from the first of these sources that sets it:

1. an argument given at invocation
2. the user's own configuration file, which git ignores
3. the defaults file that comes with the [instruction][INSTRUCTION]'s domain
4. the fallback written in the *[state file][STATEFILE]* with the shell's default form

An earlier source always wins. The user sets a value once, and an argument still wins for one run.

#### Scenario: User configuration sets a value the defaults also set

- **WHEN** the domain's defaults file and the user's configuration file set the same name
- **THEN** the loader exports the user's value, and an argument given at invocation replaces it for that run

### Requirement: The Loader Exports Environment Variables

A loader MUST merge the sources in that order and export the result as environment variables. It runs before the first step of the [instruction][INSTRUCTION] reads one. The [instruction][INSTRUCTION] refers to a value only as a shell variable, so the same text works in every *[harness][HARNESS]*. The [instruction][INSTRUCTION] text holds no value that belongs to one user or one machine.

#### Scenario: Instruction step reads a value through the shell

- **WHEN** a step reads `$NAME` after the loader ran
- **THEN** the shell returns the merged value, and the [instruction][INSTRUCTION] text holds no value of its own

### Requirement: The Shell Resolves the Variable

An [instruction][INSTRUCTION] that refers to a variable MUST say when the *[model][MODEL]* reads it. The value resolves when the [model][MODEL] runs a shell command and never when the [harness][HARNESS] loads the file. No [harness][HARNESS] expands an environment variable inside an [instruction][INSTRUCTION] file it loads ([Claude Code][CC-MEMORY], [Codex][CODEX-AGENTS], [Gemini CLI][GEMINI-MD], [OpenCode][OPENCODE-RULES]).

#### Scenario: Instruction names a variable and never reads it

- **WHEN** an [instruction][INSTRUCTION] refers to `$NAME` and no step reads the variable through the shell
- **THEN** review adds the step, or the [instruction][INSTRUCTION] states the value's meaning without a variable

### Requirement: Each Harness Runs the Loader

The *[assembler][ASSEMBLER]* MUST give each [harness][HARNESS] *[instance][INSTANCE]* its own way to run the loader before the first step. For Claude Code, the *[basis parameters][BASISPARAMETERS]* add an argument hint for the value. They also add one dynamic context line that runs the loader when the *[skill][SKILL]* loads. Codex and OpenCode inject nothing, so their [instance][INSTANCE] opens with a step that runs the loader in the shell. The [state file][STATEFILE] holds neither form.

#### Scenario: Harness has no context injection

- **WHEN** the [assembler][ASSEMBLER] builds the [instance][INSTANCE] for a [harness][HARNESS] that cannot run a command while a [skill][SKILL] loads
- **THEN** the [instance][INSTANCE] opens with a step that runs the loader in the shell, and the [state file][STATEFILE] is unchanged

#### Scenario: Harness injects context when a skill loads

- **WHEN** the [assembler][ASSEMBLER] builds the Claude Code [instance][INSTANCE]
- **THEN** the [instance][INSTANCE] carries an argument hint and a dynamic context line that runs the loader, both from the [basis parameters][BASISPARAMETERS]

### Requirement: Provenance Shows the Parameters

The *[provenance record][PROVENANCERECORD]* of each [instance][INSTANCE] MUST name the [basis parameters][BASISPARAMETERS] that produced it. A reader then sees why one [instance][INSTANCE] runs the loader as a first step and another through context injection.

#### Scenario: Two instances load the value in different ways

- **WHEN** two [instances][INSTANCE] of one [instruction][INSTRUCTION] differ in how they run the loader
- **THEN** each [provenance record][PROVENANCERECORD] names the [basis parameters][BASISPARAMETERS] that produced that [instance][INSTANCE]

[INSTRUCTION]: ../../../../specs/glossary/instruction.md
[STATEFILE]: ../../../../specs/glossary/state-file.md
[HARNESS]: ../../../../specs/glossary/harness.md
[MODEL]: ../../../../specs/glossary/model.md
[ASSEMBLER]: ../../../../specs/glossary/assembler.md
[INSTANCE]: ../../../../specs/glossary/instance.md
[BASISPARAMETERS]: ../../../../specs/glossary/basis-parameters.md
[SKILL]: ../../../../specs/glossary/skill.md
[PROVENANCERECORD]: ../../../../specs/glossary/provenance-record.md
[CC-MEMORY]: https://code.claude.com/docs/en/memory
[CODEX-AGENTS]: https://learn.chatgpt.com/docs/agent-configuration/agents-md
[GEMINI-MD]: https://geminicli.com/docs/cli/gemini-md/
[OPENCODE-RULES]: https://opencode.ai/docs/rules/
