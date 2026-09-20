---
title: YAML Frontmatter for Machine Readability
description: All markdown files carry YAML frontmatter as the metadata format, aligned with Obsidian Properties, Claude Code, and static site generators
type: adr
category: architecture
tags:
    - architecture
    - markdown
    - frontmatter
    - yaml
status: accepted
created: 2026-03-30
updated: 2026-09-20
author: "@N4M3Z"
project: deck
related:
    - "CORE-0001 Markdown as System Language"
    - "CORE-0002 Metadata Inside Files"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5", "gpt-5.6-sol"]
informed: []
upstream: [ObsidianFrontmatter.md]
change: core-foundation-principles
---

# YAML Frontmatter for Machine Readability

## Context and Problem Statement

[CORE-0002](CORE-0002 Metadata Inside Files.md) established that metadata belongs inside the file it describes. This record selects the specific format: YAML frontmatter.

The broader ecosystem has converged on YAML frontmatter as the standard metadata layer for markdown files:

- [**Claude Code**][CC] reads YAML frontmatter in `CLAUDE.md` and skill files to understand file purpose, version, and configuration without parsing the full body ([docs][CC-DOCS]).
- [**Obsidian**][OBS] adopted YAML frontmatter as the basis for its [Properties][OBS-PROPS] system, the native UI for viewing, editing, and querying file metadata. The [Dataview][DATAVIEW] and Tasks plugins query frontmatter fields for dynamic views.
- **Static site generators** ([Jekyll][JEKYLL], [Hugo][HUGO], Astro, Eleventy) all use YAML frontmatter as the standard metadata format for content files.
- **GitHub** renders YAML frontmatter as a formatted table at the top of markdown files in the web UI.

This is not a project-specific convention. It is the de facto standard for markdown metadata across the tools this ecosystem depends on.

## Decision Drivers

- [Obsidian][OBS] Properties requires YAML frontmatter. No frontmatter means no queryable metadata in the vault.
- [Claude Code][CC] parses frontmatter to understand skill definitions, agent configurations, and rule files
- Schema validation through `mdschema` requires typed fields that CI can check
- Structured MADR adoption depends on a rich frontmatter convention
- Every major markdown tool already expects YAML frontmatter

## Considered Options

1. **TOML frontmatter**: delimited by `+++`. [Hugo][HUGO] accepts it as an alternative. Less readable than YAML for nested structures, and [Obsidian][OBS] does not support it natively.
2. **JSON frontmatter**: delimited by `{` and `}`. Valid in some static site generators but hostile to human authoring, with no [Obsidian][OBS] support and poor readability for lists.
3. **YAML frontmatter**: delimited by `---` at the top of the file. Supported by markdown renderers, [Obsidian][OBS], [Claude Code][CC], GitHub, and static site generators.

## Decision Outcome

A Markdown file that carries metadata writes it as YAML frontmatter delimited by `---`. A rule is a bare instruction body and may carry none. Frontmatter holds machine-readable metadata, and the prose body holds human-readable instructions. The same file works in a git repository, an [Obsidian][OBS] vault, and an AI tool's context window without conversion.

Frontmatter stays flat: scalar values and lists of scalars, never nested objects. [Obsidian][OBS]'s Properties panel does not render nested objects.

This decision precedes the MADR template choice because frontmatter is the mechanism. Structured MADR is the schema that standardizes which fields appear in decision-record frontmatter specifically.

Frontmatter MUST be YAML between `---` lines at the top of the file. It MUST stay flat: scalar values and lists of scalars, never nested objects.

## Consequences

- Every file is queryable by [Dataview][DATAVIEW], validatable by `mdschema`, and parseable by AI tools without custom logic
- Aligns with the dominant ecosystem convention: no migration cost, no custom tooling
- Metadata travels with the file across systems, tools, and repositories
- Authors maintain frontmatter beside prose. Stale metadata is a risk, mitigated by CI validation and [Obsidian][OBS]'s Properties UI.

[CC]: https://claude.ai/code
[CC-DOCS]: https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview
[OBS-PROPS]: https://help.obsidian.md/properties
[OBS]: https://obsidian.md/
[DATAVIEW]: https://blacksmithgu.github.io/obsidian-dataview/
[JEKYLL]: https://jekyllrb.com/docs/front-matter/
[HUGO]: https://gohugo.io/content-management/front-matter/
