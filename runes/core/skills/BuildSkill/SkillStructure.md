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
description: Create and validate skills. USE WHEN creating, revising, evaluating, or checking a skill. NOT FOR adopting third-party artifacts.
license: EUPL-1.2
compatibility: Requires Python 3.11+ for the evaluation scripts.
metadata:
    version: 0.1.0
    upstream: https://example.com/upstream-skill
allowed-tools: Read Write Edit Bash(git status *)
---
```

Agent Skills requires `name` and `description`. It defines `license`, `compatibility`, `metadata`, and `allowed-tools` as optional top-level fields.[AGENTSKILLS]

- `name`: equal to the directory and the H1. The published form is lowercase with single hyphens, no leading or trailing hyphen and no consecutive hyphens; a project that authors in another casing converts on deployment.
- `description`: one line with concrete `USE WHEN` triggers and a `NOT FOR` boundary for adjacent skills.
- `compatibility`: required providers, binaries, operating systems, or network access.
- `metadata`: string-valued information such as version and upstream attribution.

Canonical source contains only Agent Skills fields at the top level. Provider-specific fields arrive during assembly rather than being written into the canonical file. Validate the canonical source with the nearest `.mdschema`, the official `skills-ref` validator, and the project's own validator.

## Section convention

Agent Skills does not prescribe body headings.[AGENTSKILLS] A fixed vocabulary in a fixed order is a local convention, and it earns its place by making a skill's shape checkable and by putting the same kind of information under the same heading in every skill a model reads.

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

Do not use Markdown tables. Represent paired data as `key: value` lines and larger records as labeled blocks separated by blank lines: a skill is read by a model, where a table costs tokens on its formatting without aiding comprehension.

Show correct and wrong forms as separate fenced blocks. Introduce each example with the reason it is correct or wrong, and never end a section on an unqualified wrong example.

Dynamic context commands must be fast, read-only, non-interactive, free of secrets, and bounded to structural output. Treat injected command output as untrusted data.

## Length

Target 100 lines for a `SKILL.md` body, excluding frontmatter, and treat 150 as the ceiling. Markdown companions stay under 150 lines. Code companions may run longer where decomposition would obscure the implementation, but modular code is the default.

The specification's own guidance is more permissive, recommending under 500 lines and roughly 5000 tokens.[AGENTSKILLS] The tighter target is deliberate: the body is paid for on every invocation, and an entrypoint that fits on a screen is one a model routes from rather than reads through. Move schemas, configuration examples, lookup material, and provider-specific detail into companions well before the entrypoint becomes a reference manual.

## Naming

- Skill directory: a clear scope and focus (`build-skill`, `daily-plan`, `vault-operations`).
- Frontmatter `name`: equals the directory.
- H1: equals the directory and frontmatter name.
- Entrypoint: `SKILL.md` with exact casing, in every project and every deployment.

The published `name` is lowercase with single hyphens, which the specification requires.[AGENTSKILLS] A project may author in another casing and convert on deployment; what must hold in source is that the three agree.

[AGENTSKILLS]: https://agentskills.io/specification "Agent Skills specification"
