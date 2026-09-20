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
updated: 2026-09-20
author: "@N4M3Z"
project: deck
related:
    - "CORE-0003 YAML Frontmatter for Machine Readability"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5", "gpt-5.6-sol"]
informed: []
upstream: [PlaintextTemplateVariables.md]
change: core-foundation-principles
---

# Variables in Markdown Instructions and Templates

## Context and Problem Statement

Markdown instructions (skills, agents, rules) reference configurable values: file paths, directory locations, tool names, feature flags. Templates need placeholder values filled at creation time. Shell tools must resolve both, and AI must read both.

Three placeholder patterns had emerged organically: inline descriptions ("Title, a short noun phrase"), `{{VARIABLE}}` ([Obsidian Templater][TEMPLATER] syntax), and `{VARIABLE}` (the Structured MADR convention). None of these is shell-resolvable.

## Decision Drivers

- Hardcoded paths break across environments
- Shell commands and AI prose need the same values from the same source
- Templates must be instantiable with `envsubst`, with no custom parsers
- Placeholder names must be self-documenting
- Obsidian Templater keeps its own `{{VARIABLE}}` pattern, so coexistence is required

## Considered Options

1. **`{{VARIABLE}}`**: Obsidian Templater syntax. Works inside Obsidian but shell tools cannot resolve it. Collides with Templater when files open in the vault.
2. **`{VARIABLE}`**: the Structured MADR convention. Not standard shell syntax, requires custom string replacement.
3. **`${VARIABLE}` with `%%` comments**: standard shell parameter expansion, resolvable by `envsubst`. Obsidian `%%` comments give inline documentation hidden in preview mode.

## Decision Outcome

Two complementary patterns for two contexts:

**Runtime instructions**: skills and rules reference `$VARIABLE` environment variables by name. The AI reads the variable name and resolves it from the environment. Shell commands use the `$VAR` syntax directly. No build step, no placeholder replacement: configuration resolves at runtime.

**Templates**: plaintext templates use `${VARIABLE}` placeholders, instantiable with `envsubst < template.md > output.md`. Variable names are UPPER_SNAKE_CASE and self-documenting. End-of-line `%%` comments describe what each variable holds, with enum choices separated by `|`:

```markdown
status: ${STATUS}                          %% proposed | accepted | deprecated | superseded %%
- ${POSITIVE}                          %% positive outcome, what improves %%
```

Obsidian Templater templates continue to use `{{VARIABLE}}`. The two patterns never mix within a single file.

An instruction MUST name a configurable value as `$VARIABLE`. A plain-text template MUST use `${VARIABLE}` placeholders that `envsubst` resolves. The two patterns MUST NOT mix in one file with the Templater `{{VARIABLE}}` pattern.

## Consequences

- Shell commands and AI instructions share the same configuration mechanism
- Templates are instantiable with `envsubst`, with zero custom tooling
- `%%` comments are invisible in Obsidian preview and visible in source: guidance without noise
- The environment must hold the values before the instruction is useful, so a config loading layer is required
- Two patterns coexist (`${VAR}` and `{{VAR}}`), mitigated by the rule that they never mix in one file

[TEMPLATER]: https://silentvoid13.github.io/Templater/
