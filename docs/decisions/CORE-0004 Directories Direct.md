---
title: Directories Direct
description: Directory names as routing decisions with functional consequences
type: adr
category: architecture
tags:
    - architecture
    - naming
status: accepted
created: 2026-03-19
updated: 2026-10-19
author: "@N4M3Z"
project: deck
related: []
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5@claude", "gpt-5.6-sol@codex"]
informed: []
upstream:
    - "obsidian://open?vault=Atlas&file=Library%2FCanvas%2FPlain%20Text%20Wins"
    - "https://github.com/N4M3Z/forge-core/blob/main/docs/decisions/CORE-0020%20Directories%20Direct.md"
    - "directories-direct-the-tools#directories-direct"
change: plain-text-first-principles
---

# Directories Direct

## Context and Problem Statement

A directory name is how a person and a *[model][MODEL]* find a file. The *[assembler][ASSEMBLER]* reads the same name and acts on it. From the name, the [assembler][ASSEMBLER] picks the *[harness][HARNESS]* that loads the files inside, and the *[variant][VARIANT]* that applies. A directory named `claude/` tells the [assembler][ASSEMBLER] that its content is for Claude. A directory named `misc/` tells it nothing.

## Considered Options

1. Group by kind: `config/`, `docs/`, `scripts/`. The names are familiar. A name says what a thing is. It does not say where the thing goes or what a tool does with it.
2. Name by function: `claude/`, `user/`, `rules/`. Every name is a decision that a tool acts on.

## Decision Outcome

Option 2. A directory name MUST tell the tool that reads it what to do with the files inside. The author MUST NOT add a directory that only groups by kind, such as `misc/`.

- The author names a directory for the place where a person would look first. A taxonomy does not decide the name.
- A well-named directory replaces a document about where things go.
- A name in a qualifier path (`claude/`, `codex/`, `user/`) is configuration, so a typo in that name silently disables the content.
- The author writes `directory` in docs, commit messages, and conversation, never `folder`.

### Consequences

- [+] The tree documents itself
- [+] The owner does not need a separate guide about where to put things
- [+] A qualifier directory name is configuration that a tool acts on

## More Information

- Rewritten on 2026-10-19 in the plain spoken register. The decision is unchanged.

[MODEL]: ../specs/glossary/model.md
[ASSEMBLER]: ../specs/glossary/assembler.md
[HARNESS]: ../specs/glossary/harness.md
[VARIANT]: ../specs/glossary/variant.md
