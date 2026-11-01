---
title: YAML Configuration Files
description: Modules ship defaults.yaml merged with gitignored config.yaml via recursive deep merge
type: adr
category: architecture
tags:
    - architecture
    - config
status: accepted
created: 2026-02-19
updated: 2026-10-19
author: "@N4M3Z"
project: deck
related:
    - "CORE-0005 Variables in Markdown Instructions and Templates"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5@claude", "gpt-5.6-sol@codex"]
informed: []
upstream:
    - "https://github.com/N4M3Z/forge-core/blob/main/docs/decisions/CORE-0009%20YAML%20Configuration%20Files.md"
    - "one-domain-one-plugin#configuration-defaults"
change: one-domain-one-plugin
---

# YAML Configuration Files

## Context and Problem Statement

An environment variable in a Markdown *[instruction][INSTRUCTION]* ([CORE-0005](CORE-0005%20Variables%20in%20Markdown%20Instructions%20and%20Templates.md)) needs a source. Each *[module][MODULE]* has configurable values (paths, feature flags, *[skill][SKILL]* rosters) that differ between the default setup and a user's own setup. The configuration system must hold committed defaults and accept user overrides. It must also export the environment variables, so that the user manages no shell profile.

## Decision Drivers

- The author commits the defaults to version control. The [module][MODULE] then works without setup
- The user keeps an override in a git-ignored file, so a personal path or preference stays out of the *[repository][REPOSITORY]*
- A user overrides one field, such as one path, and keeps the rest of the configuration
- The configuration loader exports the environment variables without a manual step. `yq` can read individual values, but the export of a whole configuration subtree as prefixed environment variables needs a multi-step pipeline

## Considered Options

1. **Flat ENV files**: a `.env` file with `KEY=VALUE` pairs. A flat file cannot nest, cannot merge, and has no defaults mechanism.
2. **JSON config**: a structured file that merges. A person finds it hard to author by hand, and the format has no comment syntax.
3. **YAML with deep merge**: the loader merges a committed `defaults.yaml` with a git-ignored `config.yaml` recursively. A user overrides only the fields they need.

## Decision Outcome

Chosen option: **YAML with deep merge**. Each [module][MODULE] includes a `defaults.yaml` with the full schema and working defaults. A user creates a git-ignored `config.yaml` with only the fields they override. The configuration loader exports the merged result as environment variables with a configurable prefix.

A [module][MODULE] MUST include a committed `defaults.yaml` that works without user input. A user override MUST live in a git-ignored `config.yaml` and MUST merge over the defaults field by field.

### Consequences

- [+] The [module][MODULE] works before the user configures anything
- [+] A user overrides one field without knowing the full schema
- [+] The configuration loader turns the configuration into environment variables for [skills][SKILL] and shell commands
- [-] Deep merge can surprise a user on two questions: whether an array replaces or appends, and whether null differs from missing

## More Information

- Rewritten on 2026-10-19 in the plain spoken register. The decision is unchanged.

[INSTRUCTION]: ../specs/glossary/instruction.md
[MODULE]: ../specs/glossary/module.md
[SKILL]: ../specs/glossary/skill.md
[REPOSITORY]: ../specs/glossary/repository.md
