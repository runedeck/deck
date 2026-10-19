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

One format has to serve the *[instructions][INSTRUCTION]* (*[skills][SKILL]*, *[agents][AGENT]*, *[rules][RULE]*), records, *[templates][TEMPLATE]*, and configuration. A person reads the file in an editor. A *[model][MODEL]* reads it through any *[harness][HARNESS]*. An author edits it without special tooling.
The format also has to work in a note-taking tool where content comes first, above all [Obsidian][OBS]. Obsidian adopted YAML frontmatter in [2020][OBS-FM] and adds `[[wikilinks]]` on top.

## Decision Drivers

- The owner wants no lock-in to one AI tool's plugin format.
- Any tool that reads files can read the content. The *[repository][REPOSITORY]* needs no runtime dependency.
- An author improves a file by editing prose. Nobody debugs code to improve it.
- One file works in an Obsidian vault, on GitHub, and in a [model][MODEL]'s context window.

## Considered Options

1. Code [templates][TEMPLATE]: an executable script fills placeholders. Each [harness][HARNESS] and each kind of file then needs its own runtime.
2. JSON or YAML definitions: structured data with typed fields. A machine reads it well. A person authors and reviews it badly.
3. Markdown with YAML frontmatter: the body is the [instruction][INSTRUCTION] as prose, and the frontmatter is the metadata. The *[validator][VALIDATOR]*, the program `mdschema`, checks the file against the *[structure schema][STRUCTURESCHEMA]* of its directory.

## Decision Outcome

Option 3. The author writes every [skill][SKILL], [agent][AGENT], [rule][RULE], *[decision record][DECISIONRECORD]*, [template][TEMPLATE], and document as Markdown. The YAML frontmatter stores the metadata a machine reads. The body is the [instruction][INSTRUCTION] or the content as free prose. One file works in a git [repository][REPOSITORY], an Obsidian vault, and a [model][MODEL]'s context window.
The author MUST write every [skill][SKILL], [agent][AGENT], [rule][RULE], [decision record][DECISIONRECORD], and document as a Markdown file. When a file has metadata, the author MUST keep it as YAML frontmatter ([CORE-0003](CORE-0003%20YAML%20Frontmatter%20for%20Machine%20Readability.md)).

### Consequences

- [+] Any AI tool that reads files can read the content. The [repository][REPOSITORY] needs no dependency.
- [+] An author improves a file by editing prose.
- [+] The same file renders in Obsidian, on GitHub, and in a [model][MODEL]'s context without conversion.
- [-] Nothing checks the logic of the content at compile time. The [validator][VALIDATOR] checks structure against the [structure schema][STRUCTURESCHEMA], and a reviewer checks meaning.
- [-] Free-form Markdown checks nothing on its own, so the [repository][REPOSITORY] needs *[linters][LINTER]* and [validators][VALIDATOR] to check it ([CORE-0021](CORE-0021%20Unified%20Module%20Validation.md)).

## More Information

- Rewritten on 2026-10-19 in the plain spoken register. The decision is unchanged.

[OBS]: https://obsidian.md/
[OBS-FM]: https://obsidian.md/changelog/2020-08-21-desktop-v0.8.5/
[INSTRUCTION]: ../specs/glossary/instruction.md
[REPOSITORY]: ../specs/glossary/repository.md
[SKILL]: ../specs/glossary/skill.md
[AGENT]: ../specs/glossary/agent.md
[RULE]: ../specs/glossary/rule.md
[DECISIONRECORD]: ../specs/glossary/decision-record.md
[MODEL]: ../specs/glossary/model.md
[HARNESS]: ../specs/glossary/harness.md
[VALIDATOR]: ../specs/glossary/validator.md
[STRUCTURESCHEMA]: ../specs/glossary/structure-schema.md
[TEMPLATE]: ../specs/glossary/template.md
[LINTER]: ../specs/glossary/linter.md
