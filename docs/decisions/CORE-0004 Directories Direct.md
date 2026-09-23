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
updated: 2026-03-30
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

Directory names are how people and models find things. In an assembly pipeline they also decide what happens to the files, which harness gets them, and which variant applies. A directory named `claude/` says that its content is for Claude. A directory named `misc/` says nothing.

## Considered Options

1. Group by type: `config/`, `docs/`, `scripts/`. Familiar, and it says what a thing is rather than where it goes or what a tool does with it.
2. Name by function: `claude/`, `user/`, `rules/`. Every name is a decision a tool acts on.

## Decision Outcome

Option 2. A directory name MUST tell a tool what to do with the files inside it. A directory that only groups by type, such as `misc/`, MUST NOT be added.

- Optimize for where someone would look, not for taxonomy
- A well-named directory replaces a document about where things go
- A name in a qualifier path (`claude/`, `codex/`, `user/`) is configuration, so a typo silently disables the content
- Say `directory`, not `folder`, in docs, commit messages, and conversation

### Consequences

- [+] The tree documents itself
- [+] No separate guide about where to put things
- [+] A qualifier directory name is configuration that a tool acts on
