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
updated: 2026-10-19
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
Every major Markdown tool reads it as the metadata layer:

- [Claude Code][CC] reads purpose, version, and configuration from the YAML frontmatter of `CLAUDE.md` and *[skill][SKILL]* files, without parsing the body ([docs][CC-DOCS]).
- [Obsidian][OBS] built its [Properties][OBS-PROPS] panel on it, and the [Dataview][DATAVIEW] and Tasks plugins query the fields.
- Static-site generators ([Jekyll][JEKYLL], [Hugo][HUGO], Astro, Eleventy) read it as the metadata of a content file.
- GitHub renders it as a table at the top of a Markdown file.

## Decision Drivers

- The Obsidian Properties panel needs YAML frontmatter. Without it the vault has nothing to query
- Claude Code parses frontmatter for [skill][SKILL], *[agent][AGENT]*, and *[rule][RULE]* definitions
- The *[structure schema][STRUCTURESCHEMA]* check (mdschema) validates typed fields, so continuous integration can check them
- Structured MADR, a *[structured architecture decision record][STRUCTUREDARCHITECTUREDECISIONRECORD]* built on the *[Markdown architecture decision record][MARKDOWNARCHITECTUREDECISIONRECORD]* (MADR), depends on a rich frontmatter convention
- Every major Markdown tool expects it

## Considered Options

1. TOML frontmatter between `+++` lines. [Hugo][HUGO] accepts it. A nested structure reads harder, and [Obsidian][OBS] does not read it.
2. JSON frontmatter between `{` and `}`. Some static-site generators accept it. An author writes it by hand with difficulty, and a list reads badly. [Obsidian][OBS] does not read it.
3. YAML frontmatter between `---` lines. Markdown renderers, [Obsidian][OBS], [Claude Code][CC], GitHub, and static-site generators all read it.

## Decision Outcome

Option 3. A Markdown file with metadata MUST keep it as YAML between `---` lines at the top of the file. A [rule][RULE] is a bare *[instruction][INSTRUCTION]* body and may have none. The frontmatter is the metadata a machine reads. The body contains the directions for people and *[models][MODEL]*. The same file works in a git repository, an [Obsidian][OBS] vault, and a [model][MODEL]'s context without conversion.
Frontmatter is YAML and MAY nest. The [Obsidian][OBS] vault is only the viewer and search tool. A Properties panel that cannot show a nested value does not limit the file.
This decision comes before the choice of the MADR format. Frontmatter is the mechanism. Structured MADR is the schema that says which fields a *[decision record][DECISIONRECORD]* has.

### Consequences

- [+] [Dataview][DATAVIEW] queries every file, and the check against the [structure schema][STRUCTURESCHEMA] validates it. A [model][MODEL] reads it without custom logic
- [+] The convention is the dominant one, so nobody migrates a file and nobody writes custom tooling
- [+] Metadata moves with the file
- [-] An author maintains frontmatter beside the prose. Stale metadata is the risk. The continuous integration check and the Properties panel keep it low.
- [-] The Properties panel does not show a nested value. A reader opens the file to see it.

## More Information

- Amended on 2026-10-18: this record drops the flatness constraint, because the vault stopped being the editor. Frontmatter MAY nest.
- Rewritten on 2026-10-19 in the plain spoken register. The decision is unchanged.

[CC]: https://claude.ai/code
[CC-DOCS]: https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview
[OBS-PROPS]: https://help.obsidian.md/properties
[OBS]: https://obsidian.md/
[DATAVIEW]: https://blacksmithgu.github.io/obsidian-dataview/
[JEKYLL]: https://jekyllrb.com/docs/front-matter/
[HUGO]: https://gohugo.io/content-management/front-matter/
[STRUCTURESCHEMA]: ../specs/glossary/structure-schema.md
[STRUCTUREDARCHITECTUREDECISIONRECORD]: ../specs/glossary/structured-architecture-decision-record.md
[MARKDOWNARCHITECTUREDECISIONRECORD]: ../specs/glossary/markdown-architecture-decision-record.md
[SKILL]: ../specs/glossary/skill.md
[AGENT]: ../specs/glossary/agent.md
[RULE]: ../specs/glossary/rule.md
[MODEL]: ../specs/glossary/model.md
[DECISIONRECORD]: ../specs/glossary/decision-record.md
[INSTRUCTION]: ../specs/glossary/instruction.md
