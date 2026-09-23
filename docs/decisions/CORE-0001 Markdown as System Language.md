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
    - "https://github.com/N4M3Z/forge-core/blob/main/docs/decisions/CORE-0001%20Markdown%20as%20System%20Language.md"
    - "https://github.com/N4M3Z/forge-core/blob/main/rules/MarkdownFirst.md"
    - "plain-text-is-futureproof#plain-text-representation"
    - "markdown-with-yaml-frontmatter#markdown-system-language"
    - "markdown-with-yaml-frontmatter#metadata-inside-files"
    - "instructions-stay-vendor-neutral#reusable-across-harnesses-and-models"
    - "instructions-stay-vendor-neutral#reusable-across-harnesses-and-models"
    - "lint-enforced-foundation-requirements#analysis-tool-coverage"
change: plain-text-first-principles
---

# Markdown as System Language

## Context and Problem Statement

One format has to serve skills, agents, rules, records, templates, and configuration. A person reads it in an editor, a model reads it through any harness, and an author edits it without special tooling.
The format also has to work in a note-taking tool where content comes first, above all [Obsidian][OBS]. Obsidian adopted YAML frontmatter in [2020][OBS-FM] and adds `[[wikilinks]]` on top.

## Decision Drivers

- No lock-in to one AI tool's plugin format
- No runtime dependency: any tool that reads files can read the content
- Authors iterate by editing prose, not by debugging code
- The same file works in an Obsidian vault, on GitHub, and in a model's context

## Considered Options

1. Code templates: executable scripts with placeholder substitution. Each provider and each kind of file needs its own runtime.
2. JSON or YAML definitions: structured data with typed fields. A machine reads it well, and a person authors and reviews it badly.
3. Markdown with YAML frontmatter: a prose body for the instruction, frontmatter for the metadata, validated by mdschema.

## Decision Outcome

Option 3. Everything is Markdown: skills, agents, rules, decision records, templates, and documentation. YAML frontmatter holds the machine-readable metadata, and the body is free-form instruction or content. The same file works in a git repository, an Obsidian vault, and a model's context window.
Every skill, agent, rule, decision record, and document MUST be a Markdown file. A file with metadata MUST keep it as YAML frontmatter ([CORE-0003](CORE-0003%20YAML%20Frontmatter%20for%20Machine%20Readability.md)).

### Consequences

- [+] No dependency: any AI tool that reads files can read the content
- [+] Authors iterate by editing prose
- [+] The same files render in Obsidian, on GitHub, and in a model's context without conversion
- [-] Nothing checks content logic at compile time. mdschema checks structure, and review checks meaning.
- [-] Free-form Markdown checks nothing on its own, so the system needs linters and validators ([CORE-0021](CORE-0021%20Unified%20Module%20Validation.md))

[OBS]: https://obsidian.md/
[OBS-FM]: https://obsidian.md/changelog/2020-08-21-desktop-v0.8.5/
