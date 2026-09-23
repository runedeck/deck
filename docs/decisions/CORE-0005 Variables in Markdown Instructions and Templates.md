---
title: Variables in Markdown Instructions and Templates
description: Runtime ENV vars for instructions, ${VARIABLE} with envsubst for templates, %% comments for inline guidance
type: adr
category: architecture
tags:
    - architecture
    - config
    - skills
    - templates
status: accepted
created: 2026-02-19
updated: 2026-03-30
author: "@N4M3Z"
project: deck
related:
    - "CORE-0003 YAML Frontmatter for Machine Readability"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5@claude", "gpt-5.6-sol@codex"]
informed: []
upstream:
    - "https://github.com/N4M3Z/forge-core/blob/main/docs/decisions/CORE-0022%20Variables%20in%20Markdown%20Instructions%20and%20Templates.md"
    - "https://github.com/N4M3Z/forge-core/blob/main/rules/PlaintextTemplateVariables.md"
    - "user-values-and-variables#variables-are-name"
    - "user-values-and-variables#canon-stays-vendor-neutral"
    - "obsidian://open?vault=Atlas&file=Library%2FCanvas%2FPlain%20Text%20Wins"
change: plain-text-first-principles
---

# Variables in Markdown Instructions and Templates

## Context and Problem Statement

Skills, agents, and rules refer to configurable values: paths, directory locations, tool names, feature flags. Templates need placeholders filled at creation time. Shell tools resolve both, and a model reads both.
Three placeholder patterns had grown on their own: inline descriptions ("Title, a short noun phrase"), `{{VARIABLE}}` from [Obsidian Templater][TEMPLATER], and `{VARIABLE}` from Structured MADR. A shell resolves none of them.

## Decision Drivers

- A hardcoded path breaks on the next machine
- Shell commands and prose need the same value from the same source
- A template instantiates with `envsubst` and no custom parser
- A placeholder name explains itself
- Obsidian Templater keeps its own `{{VARIABLE}}`, so the two have to coexist

## Considered Options

1. `{{VARIABLE}}`, the Templater syntax. Works inside Obsidian, unreadable to a shell, and collides with Templater when the file opens in the vault.
2. `{VARIABLE}`, the Structured MADR convention. Not shell syntax, so it needs custom string replacement.
3. `${VARIABLE}` with `%%` comments: standard shell parameter expansion that `envsubst` resolves, with Obsidian `%%` comments as inline documentation hidden in preview.

## Decision Outcome

Option 3, as two patterns for two contexts.
An instruction MUST refer to a configurable value as `$VARIABLE`. The model reads the name and resolves it from the environment when it runs a shell command, with no build step and no placeholder replacement.
A plain-text template MUST use `${VARIABLE}` placeholders that `envsubst < template.md > output.md` resolves. Names are UPPER_SNAKE_CASE, and an end-of-line `%%` comment says what each variable holds, with enum choices separated by `|`:

```markdown
status: ${STATUS}                          %% proposed | accepted | deprecated | superseded %%
- ${POSITIVE}                          %% positive outcome, what improves %%
```

Obsidian Templater templates keep `{{VARIABLE}}`. The two patterns MUST NOT mix in one file.

### Consequences

- [+] Shell commands and instructions share one configuration mechanism
- [+] Templates instantiate with `envsubst` and nothing else
- [+] `%%` comments are invisible in Obsidian preview and visible in source
- [-] The environment has to hold the values before the instruction is useful, so a configuration loading layer is required
- [-] `${VAR}` and `{{VAR}}` coexist, kept apart by the rule that they never mix in one file

[TEMPLATER]: https://silentvoid13.github.io/Templater/
