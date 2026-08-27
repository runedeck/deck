---
name: BuildTask
description: "Build one copy-ready recurring task for Claude Code Routines or ChatGPT Scheduled tasks. USE WHEN creating, rendering, or reviewing a provider task prompt and its schedule, permissions, notification, and canary settings. NOT FOR running a task, changing provider state, or designing a domain-specific scanner."
license: EUPL-1.2
metadata:
    version: 0.1.0
---

# BuildTask

Build one provider task from a complete task definition.
Return a manual setup package.

## Prerequisites

The task definition must contain these values:

- task name
- provider interface
- model and reasoning level
- fallback policy
- schedule and time zone
- prompt template
- approved placeholder values
- placeholder schema
- repository, network, browser, and tool permissions
- notification destination and size limit
- task-specific canary checks and fixture specification

Ask for a missing value when the caller does not supply it.

## Constraints

- Build only one task during each invocation.
- Never run the task.
- Never create or change provider state.
- Never write a rendered prompt to a local file.

- Never use account memory as a placeholder source.
- Never infer a missing identity value.
- Never weaken a permission to make the task succeed.
- Never claim that a prompt enforces a security boundary.
- Never claim that Rune configured the provider.
- Use the minimum approved public data.
- State that the provider stores the rendered prompt and its approved values.

## Instructions

### Validate the definition

Accept these provider interfaces:

- Claude Code Routine
- ChatGPT Work standalone Scheduled task

Reject an unknown provider interface.
Reject `current` or `latest` as a model identifier.
Reject a task that has no explicit write policy.
Reject a task that has no fallback policy.
Reject a task that has no notification limit.
Reject a task that requests a private placeholder value.
Reject a task that has no typed placeholder schema.

### Select the provider guide

Read [ClaudeCode.md](references/ClaudeCode.md) for a Claude Code Routine.
Read [ChatGPTWork.md](references/ChatGPTWork.md) for a ChatGPT Scheduled task.
Read [CanaryChecks.md](references/CanaryChecks.md) for all tasks.
Read only the selected provider guide.
Read [PlaceholderValues.md](references/PlaceholderValues.md).

### Render the prompt

Validate each value against its typed schema.
Reject each unsafe value before rendering.
Replace each template placeholder with an approved literal value.
Use `- None.` for an approved empty optional list.
Keep all other template text unchanged.
Keep each list item on a separate line.
Do not include an unresolved placeholder.
Do not add a value from memory, prior chats, browser history, or local files.

### Return the setup package

Return these sections:

1. Task identity
2. Provider settings
3. Schedule
4. Permissions
5. Complete prompt
6. Canary checks

Put the complete prompt in one copy-ready code block.
State that the provider setup remains manual.
Tell the user to run the manual canary before schedule activation.

## Verification

- Confirm that no placeholder remains.
- Confirm that the result contains no unapproved private value.
- Confirm that each value passed its typed schema.
- Confirm that the write policy is explicit.
- Confirm that the fallback policy is explicit.

- Confirm that the prompt requires redaction when the task handles sensitive data.
- Confirm that the prompt reports coverage limits.
- Confirm that the prompt sends only the permitted notifications.
