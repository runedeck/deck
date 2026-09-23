---
title: Open Knowledge Format Bundle
description: The repository is a conformant Open Knowledge Format 0.2 bundle, so a directory of Markdown files with a type and Markdown links reads as a graph without a database
type: adr
category: architecture
tags:
    - architecture
    - markdown
    - linking
status: proposed
created: 2026-09-23
updated: 2026-10-18
author: "@N4M3Z"
project: deck
related:
    - "CORE-0001 Markdown as System Language"
    - "CORE-0002 Metadata Inside Files"
    - "CORE-0009 Reference Citations"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5-1@claude"]
informed: []
upstream:
    - "obsidian://open?vault=Atlas&file=Library%2FCanvas%2FPlain%20Text%20Wins"
    - "https://github.com/GoogleCloudPlatform/open-knowledge-format-bundle/blob/main/SPEC.md"
    - "markdown-relative-links-matching#markdown-links-between-files"
    - "markdown-relative-links-matching#link-targets-resolve"
    - "open-knowledge-format-bundle#type-on-every-file"
    - "open-knowledge-format-bundle#path-is-the-identifier"
    - "open-knowledge-format-bundle#reserved-names"
    - "open-knowledge-format-bundle#bundle-declares-its-version"
change: plain-text-first-principles
---

# Open Knowledge Format Bundle

## Context and Problem Statement

The repository is a directory of Markdown files. Its readers are a person in an editor or a vault, a model through a harness, and a tool that builds a graph or an index.
Either each file says what it is and what it links to, or the reader has to guess.
Three link forms compete: Markdown links in the repository, wikilinks in the vault, and `@path` references in a harness.
The repository needs one contract for the file structure and the link form, one a machine can read as a graph, and the graph has to be rebuildable from the files alone (frame 04 of the canvas).

## Decision Drivers

- One optional key, so a file without it takes its type from the structure schema of its directory, and a rune may still carry it under the Agent Skills `metadata` map
- Standard Markdown links, so GitHub, lychee, rumdl, and a plain parser resolve them
- No central registry of types, so a repository adds a kind without asking anyone
- A published specification another organization maintains

## Considered Options

1. Bespoke frontmatter: keep the fields each file kind grew. The contract is then written down nowhere, and a graph tool learns each kind by hand.
2. [MIF][MIF]: typed relationships, a JSON-LD projection, bi-temporal fields, W3C PROV. It fits provenance and records, and it asks every file for more than a type. Deferred rather than rejected: the `modeled-information-format-alignment` change decides that alignment.
3. [Open Knowledge Format 0.2][OKF]: a bundle is a directory of Markdown files with YAML frontmatter. `type` is the only required key, the identifier is the file path, links are standard Markdown, `index.md` and `log.md` are reserved, consumers tolerate unknown keys and types.

## Decision Outcome

Option 3. The repository MUST be a conformant Open Knowledge Format 0.2 bundle. A file's type comes from the structure schema of its nearest directory, and an explicit key in the file overrides it. A rune may keep its `type` under the Agent Skills `metadata` map, and the graph export fills the type in for every file.
Every Markdown file outside the reserved names MUST have a `type`.
A record, a specification, or a proposal MUST link to another file in the repository with a relative Markdown link, never a wikilink or an `@path` reference.
An instruction body MAY use the `@path` form where its harness reads it, because that text is what the harness loads.
The repository root `index.md` MUST declare `okf_version: "0.2"`.
MIF alignment continues where OKF is silent: provenance, typed relationships, and the record lifecycle.

### Consequences

- [+] A directory of files reads as a graph, and a database over it is a rebuildable index, never a second home for the facts.
- [+] Every link in the repository resolves in GitHub and in the lychee check, and Obsidian resolves relative Markdown links. Fragment conventions differ by renderer, so lychee with fragments is the repository's arbiter.
- [-] Wikilinks are kept out of the repository, so a note copied from the vault gets rewritten at the boundary. The Obsidian compatibility capability specifies that rewrite.
- [-] A strict outside reader of the format sees a file without the key as untyped, because the type lives in the directory schema and the graph export. We accept that.

## More Information

- Amended on 2026-10-18: the type key is optional and derived from the directory schema, so the `metadata` map is no longer an exception.
- Amended on 2026-10-18: the record says repository where it meant the container, because the Open Knowledge Format bundle is the repository and the marker file marks a deck.

[MIF]: https://github.com/modeled-information-format/MIF
[OKF]: https://github.com/GoogleCloudPlatform/open-knowledge-format-bundle/blob/main/SPEC.md
