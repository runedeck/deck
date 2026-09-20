---
title: Markdown as System Language
description: All instructions, skills, agents, and rules are authored as markdown with YAML frontmatter
type: adr
category: architecture
tags:
    - architecture
    - markdown
status: accepted
created: 2026-02-19
updated: 2026-09-20
author: "@N4M3Z"
project: deck
related: []
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5", "gpt-5.6-sol"]
informed: []
upstream: [MarkdownFirst.md]
change: core-foundation-principles
---

# Markdown as System Language

## Context and Problem Statement

The system needs one universal format for skills, agents, rules, documentation, journal templates, and configuration. Humans must read it comfortably, AI tools across providers must consume it, and authors must not need special tooling.

The format must also integrate with PKM tools where content comes first, in particular [Obsidian][OBS]. Obsidian adopted YAML frontmatter in [2020][OBS-FM] and adds `[[wikilinks]]`.

## Decision Drivers

- Multi-provider portability: no vendor lock-in to one AI tool's plugin format
- Zero runtime dependencies: any tool that reads files can consume the content
- Authors iterate by editing prose, not by debugging code
- Content must work in Obsidian vaults, GitHub rendering, and AI tool contexts at the same time

## Considered Options

1. **Code templates**: executable scripts with placeholder substitution. Each provider and artifact type needs a runtime.
2. **JSON or YAML definitions**: structured data with typed fields. Machine-readable but hard to author and review.
3. **Markdown with YAML frontmatter**: prose body for instructions, frontmatter for metadata, validated by mdschema.

## Decision Outcome

Chosen option: **Markdown with YAML frontmatter**. Everything is markdown: skills, agents, rules, decision records, journal templates, and documentation. YAML frontmatter carries machine-readable metadata, and the body stays free-form instruction or content. The same file works in a git repository, an Obsidian vault, and an AI tool's context window.

Every skill, agent, rule, decision record, and document MUST be a Markdown file. A file that carries metadata MUST carry it as YAML frontmatter ([CORE-0003](CORE-0003 YAML Frontmatter for Machine Readability.md)).

## Consequences

- Zero dependencies: any AI tool that reads files can consume the content
- Authors iterate by editing prose, not by debugging code or schemas
- The same files render in Obsidian, GitHub, and AI tool contexts without conversion
- Nothing checks content logic at compile time. Structural checks rely on mdschema, and semantic correctness requires review.
- Free-form markdown checks nothing by itself, so the system needs many linters and validation tools ([CORE-0007](CORE-0007 Unified Module Validation.md))

[OBS]: https://obsidian.md/
[OBS-FM]: https://obsidian.md/changelog/2020-08-21-desktop-v0.8.5/
