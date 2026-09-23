---
title: Reference Citations
description: Documents cite external sources with reference-style links, a named tag inline and one link definition at the file end
type: adr
category: architecture
tags:
    - architecture
    - documentation
    - citations
status: accepted
created: 2026-08-28
updated: 2026-09-20
author: "@N4M3Z"
project: deck
related:
    - "CORE-0001 Markdown as System Language"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5@claude", "gpt-5.6-sol@codex"]
informed: []
upstream:
    - "markdown-with-yaml-frontmatter#reference-citations"
change: plain-text-first-principles
---

# Reference Citations

## Context and Problem Statement

Decision records and change proposals cite standards, blog posts, and tool documentation. The first proposals used numbered citations with a numbered Sources list. A bare number says nothing where it is used, and one insertion renumbers every later reference.

## Decision Drivers

- A citation is readable where it is used, without a jump to the list
- Adding or removing a source renumbers nothing
- Plain Markdown that GitHub and Obsidian render
- One convention for decision records, proposals, and specifications

## Considered Options

1. Numbered citations: `[1]` markers with a numbered Sources list. Compact, and a number says nothing, and an insertion renumbers everything.
2. Inline URLs: the full URL at each use. Readable nowhere, duplicated everywhere.
3. Reference-style links: `[Obsidian Properties][OBS-PROPS]` inline with one `[OBS-PROPS]: url` definition at the end of the file. Named where it is used, defined once.

## Decision Outcome

Option 3. A document MUST cite an external source with a reference-style link: a short uppercase tag inline and one link definition at the end of the file. A change proposal keeps a Sources section that lists each source once with the same tags.

### Consequences

- [+] A citation names its source where it is used
- [+] Sources come and go without renumbering
- [+] Plain Markdown: GitHub, Obsidian, and lychee all read it
- [-] Tags have to stay unique within a file, and review checks that until a checker exists
