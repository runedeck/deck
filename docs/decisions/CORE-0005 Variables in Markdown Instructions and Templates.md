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
updated: 2026-10-19
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

An *[instruction][INSTRUCTION]* (a *[skill][SKILL]*, an *[agent][AGENT]*, or a *[rule][RULE]*) refers to configurable values: paths, directory locations, tool names, and feature flags. A *[template][TEMPLATE]* needs placeholders that the author fills at creation time. A shell tool resolves both kinds of value, and a *[model][MODEL]* reads both.
Placeholders had appeared in three forms: an inline description ("Title, a short noun phrase"), `{{VARIABLE}}` from [Obsidian Templater][TEMPLATER], and `{VARIABLE}` from *[Structured MADR][STRUCTUREDARCHITECTUREDECISIONRECORD]*. A shell resolves none of the three.

## Decision Drivers

- A path written into an [instruction][INSTRUCTION] breaks on the next machine
- A shell command and the prose around it need the same value from one source
- The substitution tool `envsubst` fills a [template][TEMPLATE] without a custom parser
- A placeholder name explains itself
- Obsidian Templater keeps its own `{{VARIABLE}}`, so both patterns have to coexist

## Considered Options

1. `{{VARIABLE}}`, the Templater syntax. It works inside Obsidian. A shell cannot read it. It collides with Templater when the file opens in the vault.
2. `{VARIABLE}`, the [Structured MADR][STRUCTUREDARCHITECTUREDECISIONRECORD] convention. It is not shell syntax, so it needs custom string replacement.
3. `${VARIABLE}` with `%%` comments. A shell expands the placeholder as a standard parameter, and `envsubst` resolves it. An Obsidian `%%` comment documents it inline, and Obsidian hides the comment in preview.

## Decision Outcome

Option 3, as two patterns for two contexts.

An [instruction][INSTRUCTION] MUST refer to a configurable value as `$VARIABLE`. The [model][MODEL] reads the name and resolves it from the environment when it runs a shell command. The pattern needs no build step and no placeholder replacement.

A plain-text [template][TEMPLATE] MUST use `${VARIABLE}` placeholders. The command `envsubst < template.md > output.md` resolves them. A name is `UPPER_SNAKE_CASE`. An end-of-line `%%` comment says what each variable contains, and `|` separates the choices of an enum:

```markdown
status: ${STATUS}                          %% proposed | accepted | deprecated | superseded %%
- ${POSITIVE}                          %% positive outcome, what improves %%
```

An Obsidian Templater [template][TEMPLATE] keeps `{{VARIABLE}}`. The Templater pattern and the shell pattern MUST NOT mix in one file.

### Consequences

- [+] A shell command and an [instruction][INSTRUCTION] share one configuration mechanism
- [+] The author fills a [template][TEMPLATE] with `envsubst` and nothing else
- [+] A `%%` comment is invisible in Obsidian preview and visible in source
- [-] The environment has to contain the values before an [instruction][INSTRUCTION] is useful, so a configuration loading layer is required
- [-] `${VAR}` and `{{VAR}}` coexist. The principle against mixing them in one file keeps them apart

## More Information

- Rewritten on 2026-10-19 in the plain spoken register. The decision is unchanged.

[TEMPLATER]: https://silentvoid13.github.io/Templater/
[INSTRUCTION]: ../specs/glossary/instruction.md
[SKILL]: ../specs/glossary/skill.md
[AGENT]: ../specs/glossary/agent.md
[RULE]: ../specs/glossary/rule.md
[TEMPLATE]: ../specs/glossary/template.md
[MODEL]: ../specs/glossary/model.md
[STRUCTUREDARCHITECTUREDECISIONRECORD]: ../specs/glossary/structured-architecture-decision-record.md
