## ADDED Requirements

### Requirement: Variables Are $NAME

Personal paths, account names, and other user-specific values leak into instructions easily.
A shared instruction MUST NOT contain a value that belongs to one user or one machine.
It MUST refer to the value as an environment variable, `$NAME`. The model reads the variable through the shell, and every harness has one.
A name ends at the first character that is not a letter, a digit, or an underscore.

#### Scenario: Instruction embeds a configurable value

- **WHEN** an instruction contains a hardcoded path, account, or host that belongs to one user or machine
- **THEN** review replaces the value with a `$NAME` reference and explains the variable in one sentence

#### Scenario: Braced form appears

- **WHEN** an instruction writes a variable as `${NAME}`
- **THEN** review rewrites it as `$NAME`

### Requirement: The Shell Resolves the Variable

An instruction that refers to a variable MUST say when the model reads it, because the value resolves when the model runs a shell command and never when the harness loads the file.
No harness expands an environment variable inside an instruction file it loads ([Claude Code][CC-MEMORY], [Codex][CODEX-AGENTS], [Gemini CLI][GEMINI-MD], [OpenCode][OPENCODE-RULES]). Claude Code's own placeholders such as `$ARGUMENTS` are the next requirement's subject.

#### Scenario: Instruction names a variable and never reads it

- **WHEN** an instruction refers to `$NAME` and no step reads the variable through the shell
- **THEN** review adds the step, or the instruction states the value's meaning without a variable

### Requirement: Harness Placeholders Stay in the Harness File

A placeholder that only one harness expands, such as `${CLAUDE_PROJECT_DIR}` or `$ARGUMENTS` in a Claude Code skill body, MUST NOT appear in a shared source.
It goes into that harness's file beside the source, and the shared source refers to the same value as `$NAME`.

#### Scenario: Harness placeholder enters a shared source

- **WHEN** a shared source uses a placeholder form that one harness documents and the others do not
- **THEN** review moves the line into that harness's file, and the source keeps the `$NAME` form

[CC-MEMORY]: https://code.claude.com/docs/en/memory
[CODEX-AGENTS]: https://learn.chatgpt.com/docs/agent-configuration/agents-md
[GEMINI-MD]: https://geminicli.com/docs/cli/gemini-md/
[OPENCODE-RULES]: https://opencode.ai/docs/rules/
