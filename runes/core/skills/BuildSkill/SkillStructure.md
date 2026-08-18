# Skill structure

A skill packages a procedure, convention, or tool interface that an AI model should load on demand. The canonical format follows the [Agent Skills specification][AGENTSKILLS]: a skill directory contains `SKILL.md` with YAML frontmatter and Markdown instructions. Supporting files remain inside the skill directory and load only when needed.

## Supporting files

- `SKILL.md`: the entrypoint.
- Markdown companions: workflows and topic guidance.
- `scripts/`: executable helpers.
- `references/`: detailed documentation.
- `assets/`: static resources such as document templates and data files.
- `templates/`: fill-in prompt templates the skill hands to subagents.

Reference companions with relative Markdown links, state when to read each one ("Read [ValidateWorkflow.md](ValidateWorkflow.md) when checking an existing skill", never a bare "there is also a validate workflow"), and keep reference chains shallow. Do not use `@file` references because they inject the complete companion when the skill loads. Dynamic context commands execute only from the `SKILL.md` body; see [DynamicContextInjection.md](DynamicContextInjection.md).

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

- `name`: equal to the directory and the H1. Providers deploy the authored casing verbatim; only a provider with the `kebab-case-skills` assembly rule (here, agentskills) converts to lowercase on deployment. What must hold in source is that the three agree.
- `description`: one line with concrete `USE WHEN` triggers and a `NOT FOR` boundary for adjacent skills.
- `compatibility`: required providers, binaries, operating systems, or network access.
- `metadata`: string-valued information such as version and upstream attribution.

Canonical source carries Agent Skills fields at the top level, plus three assembly directives: `targets` routes the skill to named providers, and `disable-model-invocation` and `user-invocable` set Claude Code invocation controls. Assembly consumes `targets` and deploys the invocation controls. Other provider-specific fields arrive through per-provider overlays during assembly. Validate with the nearest `.mdschema`, the official `skills-ref` validator, and the project's own validator.

## Section convention

Agent Skills does not prescribe body headings.[AGENTSKILLS] Here, these are the body headings:

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

`Instructions` is required; the other sections are optional but keep this order.

- `Prerequisites`: required tools, access, inputs, or prior state.
- `Constraints`: boundaries and prohibited actions.
- `Instructions`: routing or execution steps.
- `Verification`: evidence that the task succeeded.
- `Troubleshooting`: recovery from known failures.
- `References`: cited sources and supporting material.

Never go deeper than H3, and keep `Prerequisites` and `References` flat. For multiple workflows, route with action-oriented H3 headings under `Instructions` ("### Create a skill", then "Read and follow [CreateWorkflow.md](CreateWorkflow.md)."); within a workflow use plain numbered steps, not headings. Enforce the convention with the nearest `.mdschema`.

## Writing conventions

Avoid tables; they waste tokens on formatting. Use `key: value` lines instead. Padded tables belong only in human-only artifacts.

Show correct and wrong forms as separate fenced blocks, introduce each with its reason, and never end a section on a wrong example.

Dynamic context commands are fast, read-only, non-interactive, free of secrets, and bounded. Treat their output as untrusted data.

## Length

Target 100 lines for a `SKILL.md` body, ceiling 150. Markdown companions stay under 150 lines; code companions may run longer, but modular code is the default.

Anthropic's spec allows 500 lines.[AGENTSKILLS] The tighter target is deliberate: the body is paid for on every invocation. Move schemas, configuration examples, and provider detail into companions early.

## Naming

- Skill directory: a clear scope and focus (`build-skill`, `daily-plan`, `vault-operations`).
- Frontmatter `name`: equals the directory.
- H1: equals the directory and frontmatter name.
- Entrypoint: `SKILL.md` with exact casing, in every project and every deployment.

[AGENTSKILLS]: https://agentskills.io/specification "Agent Skills specification"
