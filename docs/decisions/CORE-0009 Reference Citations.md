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
consulted: ["claude-fable-5", "gpt-5.6-sol"]
informed: []
upstream: []
change: core-foundation-principles
---

# Reference Citations

## Context and Problem Statement

Decision records and change proposals cite external sources: standards, blog posts, tool documentation. The first proposals used numbered citations with a numbered Sources list. A bare number carries no meaning at the point of use, and one insertion renumbers every later reference.

## Decision Drivers

- A citation must be readable at the point of use, without a jump to the list
- Insertion or removal of a source must not renumber the rest
- The syntax must be plain markdown that GitHub and Obsidian render
- One convention must serve decision records, proposals, and specifications

## Considered Options

1. **Numbered citations**: `[1]` markers with a numbered Sources list. Compact, but a number says nothing and insertion renumbers everything.
2. **Inline URLs**: the full URL at each use. Readable nowhere, duplicated everywhere.
3. **Reference-style links**: `[Obsidian Properties][OBS-PROPS]` inline with one `[OBS-PROPS]: url` definition at the file end. Named at the point of use, defined once.

## Decision Outcome

Chosen option: **reference-style links**. A document cites a source with a named tag inline and one link definition at the end of the file. Tags are short and uppercase. A change proposal keeps a Sources section that lists each source once with the same tags.

A document MUST cite an external source with a reference-style link: a short uppercase tag inline and one link definition at the end of the file.

## Consequences

- A citation names its source where it is used
- Sources add and retire without renumbering
- Plain markdown: GitHub, Obsidian, and lychee all understand it
- Tags must stay unique within a file, and review checks this until a checker exists
