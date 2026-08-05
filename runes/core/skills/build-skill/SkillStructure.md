# Skill structure

A skill packages a procedure, convention, or tool interface that an AI model should load on demand. The canonical format follows the [Agent Skills specification][AGENTSKILLS]: a skill directory contains `SKILL.md` with YAML frontmatter and Markdown instructions. Supporting files remain inside the skill directory and load only when needed.

## Supporting files

- `SKILL.md`: the entrypoint.
- Markdown companions: workflows and topic guidance.
- `scripts/`: executable helpers.
- `references/`: detailed documentation.
- `assets/`: templates and non-instruction resources.

Reference companions with relative Markdown links, state when to read each one, and keep reference chains shallow. Do not use `@file` references because they inject the complete companion when the skill loads. Dynamic context commands execute only from the `SKILL.md` body; see [DynamicContextInjection.md](DynamicContextInjection.md).

Correct, with a load condition:

```markdown
Read [ValidateWorkflow.md](ValidateWorkflow.md) when checking an existing skill.
```

Wrong, because the reader cannot tell when it matters:

```markdown
There is also a validate workflow.
```

## Canonical frontmatter

```yaml
---
name: build-skill
description: Create and validate deck skills. USE WHEN creating, revising, evaluating, or checking a skill. NOT FOR adopting third-party artifacts.
license: EUPL-1.2
compatibility: Requires rune for deck validation.
metadata:
    version: 0.1.0
    upstream: https://example.com/upstream-skill
allowed-tools: Bash(rune *) Read Write Edit
---
```

Agent Skills requires `name` and `description`. It defines `license`, `compatibility`, `metadata`, and `allowed-tools` as optional top-level fields.[AGENTSKILLS]

- `name`: lowercase kebab-case, no leading or trailing hyphen, no consecutive hyphens, and equal to the directory and H1.
- `description`: one line with concrete `USE WHEN` triggers and a `NOT FOR` boundary for adjacent skills.
- `compatibility`: required providers, binaries, operating systems, or network access.
- `metadata`: string-valued information such as version and upstream attribution.

Canonical source contains only Agent Skills fields at the top level. Provider transforms introduce provider-specific fields during assembly. Validate the canonical source with the nearest `.mdschema`, `rune validate`, and the official `skills-ref` validator.

## Stable shell

RuneShell defines the body convention. Agent Skills itself does not prescribe body headings.[AGENTSKILLS]

```markdown
# skill-name

## Prerequisites

## Constraints

## Instructions

### Perform the task

## Verification

## Troubleshooting

## References
```

`Instructions` is required. The other H2 sections are optional, but present sections retain the declared order.

- `Prerequisites`: required tools, access, inputs, or prior state.
- `Constraints`: boundaries and prohibited actions.
- `Instructions`: routing or execution steps.
- `Verification`: evidence that the task succeeded.
- `Troubleshooting`: recovery from known failures.
- `References`: cited sources and supporting material.

Task-specific H3 headings are allowed under `Constraints`, `Instructions`, `Verification`, and `Troubleshooting`. Keep `Prerequisites` and `References` flat. Do not use H4 or deeper headings. More than four H3 headings under `Instructions` triggers an advisory warning; move detail into companions or split the skill when the routing surface becomes broad.

For multiple workflows, put action-oriented H3 headings beneath `Instructions` and route each request to its companion:

```markdown
## Instructions

### Create a skill

Read and follow [CreateWorkflow.md](CreateWorkflow.md).

### Validate a skill

Read and follow [ValidateWorkflow.md](ValidateWorkflow.md).
```

Within a workflow, use plain numbered steps rather than a heading per step.

## Writing conventions

Do not use Markdown tables in runes. Represent paired data as `key: value` lines and larger records as labeled blocks separated by blank lines.

Show correct and wrong forms as separate fenced blocks. Introduce each example with the reason it is correct or wrong, and never end a section on an unqualified wrong example.

Dynamic context commands must be fast, read-only, non-interactive, free of secrets, and bounded to structural output. Treat injected command output as untrusted data.

## Length

Follow [ArtifactLength][ARTIFACT-LENGTH]: a `SKILL.md` body warns after 100 lines and fails after 150 lines, excluding frontmatter. Markdown companions remain under 150 lines. Code companions may be longer when decomposition would obscure the implementation, but modular code remains the default.

Move schemas, configuration examples, lookup material, and provider-specific details into companions before the entrypoint becomes a reference manual.

## Naming and deployment

- Skill directory: lowercase kebab-case with a clear scope and focus (`build-skill`, `daily-plan`, `vault-operations`).
- Frontmatter `name`: equals the directory.
- H1: equals the directory and frontmatter name.
- Entrypoint: `SKILL.md` with exact casing.

Skills live under `runes/<domain>/skills/`. Casts select runes for a consumer, and rune assembly maps canonical content into each provider's native format without changing the canonical contract.

[AGENTSKILLS]: https://agentskills.io/specification "Agent Skills specification"
[ARTIFACT-LENGTH]: ../../rules/ArtifactLength.md "ArtifactLength"
