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
updated: 2026-10-19
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

A *[decision record][DECISIONRECORD]* and a *[change][CHANGE]* proposal cite standards, blog posts, and tool documentation. The first proposals used numbered citations with a numbered Sources list. A bare number tells the reader nothing at the place where the author cites. One insertion renumbers every later reference.

## Decision Drivers

- The reader understands a citation at the place where the author cites, without a jump to the list
- The author adds or removes a source without renumbering the rest
- Plain Markdown that GitHub and Obsidian render
- One convention for [decision records][DECISIONRECORD], proposals, and specifications

## Considered Options

1. Numbered citations: `[1]` markers with a numbered Sources list. The form is compact. A number tells the reader nothing, and one added source renumbers every later marker.
2. Inline URLs: the full URL at each use. The reader finds it readable nowhere, and the author duplicates it everywhere.
3. Reference-style links: `[Obsidian Properties][OBS-PROPS]` inline with one `[OBS-PROPS]: url` definition at the end of the file. The tag identifies the source where the author cites, and the author defines it once.

## Decision Outcome

Option 3. The author MUST cite an external source with a reference-style link. The link is a short tag in upper case at the citation and one link definition at the end of the file. A [change][CHANGE] proposal keeps a Sources section. That section lists each source once with the same tags.

### Consequences

- [+] The reader sees the source of a citation at the place where the author cites
- [+] Sources come and go without renumbering
- [+] Plain Markdown: GitHub, Obsidian, and lychee all read it
- [-] A tag has to stay unique within a file. The reviewer checks that until a checker exists

## More Information

Rewritten on 2026-10-19 in the plain spoken register. The decision is unchanged.

[DECISIONRECORD]: ../specs/glossary/decision-record.md
[CHANGE]: ../specs/glossary/change.md
