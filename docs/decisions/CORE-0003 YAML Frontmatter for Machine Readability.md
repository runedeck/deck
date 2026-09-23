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
updated: 2026-10-18
author: "@N4M3Z"
project: deck
related:
    - "CORE-0001 Markdown as System Language"
    - "CORE-0002 Metadata Inside Files"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5@claude", "gpt-5.6-sol@codex"]
informed: []
upstream:
    - "obsidian://open?vault=Atlas&file=Library%2FCanvas%2FPlain%20Text%20Wins"
    - "https://github.com/N4M3Z/forge-core/blob/main/docs/decisions/CORE-0003%20YAML%20Frontmatter%20for%20Machine%20Readability.md"
change: plain-text-first-principles
---

# YAML Frontmatter for Machine Readability

## Context and Problem Statement

[CORE-0002](CORE-0002%20Metadata%20Inside%20Files.md) puts metadata inside the file. This record picks the format: YAML frontmatter.
The ecosystem has settled on it as the metadata layer for Markdown:

- [Claude Code][CC] reads YAML frontmatter in `CLAUDE.md` and in skill files for purpose, version, and configuration without parsing the body ([docs][CC-DOCS]).
- [Obsidian][OBS] built its [Properties][OBS-PROPS] panel on it, and the [Dataview][DATAVIEW] and Tasks plugins query the fields.
- Static-site generators ([Jekyll][JEKYLL], [Hugo][HUGO], Astro, Eleventy) read it as the metadata of a content file.
- GitHub renders it as a table at the top of a Markdown file.

## Decision Drivers

- Obsidian Properties needs YAML frontmatter, and without it the vault has nothing to query
- Claude Code parses frontmatter for skill, agent, and rule definitions
- mdschema validates typed fields that CI can check
- Structured MADR depends on a rich frontmatter convention
- Every major Markdown tool expects it

## Considered Options

1. TOML frontmatter between `+++` lines. [Hugo][HUGO] accepts it. Harder to read for nested structures, and [Obsidian][OBS] does not read it.
2. JSON frontmatter between `{` and `}`. Some static-site generators accept it. Hostile to hand authoring, poor for lists, and [Obsidian][OBS] does not read it.
3. YAML frontmatter between `---` lines. Markdown renderers, [Obsidian][OBS], [Claude Code][CC], GitHub, and static-site generators all read it.

## Decision Outcome

Option 3. A Markdown file with metadata MUST keep it as YAML between `---` lines at the top of the file. A rule is a bare instruction body and may have none. Frontmatter holds the machine-readable metadata, and the body holds the instruction for people and models. The same file works in a git repository, an [Obsidian][OBS] vault, and a model's context without conversion.
Frontmatter is YAML and MAY nest. The [Obsidian][OBS] vault is only the viewer and search tool. A Properties panel that cannot show a nested value does not limit the file.
This decision comes before the MADR template choice. Frontmatter is the mechanism, and Structured MADR is the schema for which fields a decision record has.

### Consequences

- [+] Every file is queryable by [Dataview][DATAVIEW], checkable by mdschema, and readable by a model without custom logic
- [+] The dominant convention, so no migration and no custom tooling
- [+] Metadata moves with the file
- [-] Authors maintain frontmatter beside prose. Stale metadata is the risk, and CI validation plus the Properties panel keep it low.
- [-] The Properties panel does not show a nested value. A reader opens the file to see it.

## More Information

- Amended on 2026-10-18: the flatness rule is dropped, because the vault stopped being the editor. Frontmatter MAY nest.

[CC]: https://claude.ai/code
[CC-DOCS]: https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview
[OBS-PROPS]: https://help.obsidian.md/properties
[OBS]: https://obsidian.md/
[DATAVIEW]: https://blacksmithgu.github.io/obsidian-dataview/
[JEKYLL]: https://jekyllrb.com/docs/front-matter/
[HUGO]: https://gohugo.io/content-management/front-matter/
