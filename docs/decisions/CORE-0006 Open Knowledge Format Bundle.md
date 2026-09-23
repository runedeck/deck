---
title: Open Knowledge Format Bundle
description: The deck is a conformant Open Knowledge Format 0.2 bundle, so a directory of Markdown files with a type and Markdown links reads as a graph without a database
type: adr
category: architecture
tags:
    - architecture
    - markdown
    - linking
status: proposed
created: 2026-09-23
updated: 2026-09-23
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
    - "https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md"
    - "linked-markdown-notes#markdown-links-between-files"
    - "linked-markdown-notes#link-targets-resolve"
    - "open-knowledge-format#type-on-every-file"
    - "open-knowledge-format#path-is-the-identifier"
    - "open-knowledge-format#reserved-names"
    - "open-knowledge-format#bundle-declares-its-version"
change: core-foundation-principles
---

# Open Knowledge Format Bundle

## Context and Problem Statement

A deck is a directory of Markdown files. Its readers are a person in an editor or a vault, a model through a harness, and a tool that builds a graph or an index.
Either each file says what it is and what it links to, or the reader has to guess.
Three link forms compete: Markdown links in the deck, wikilinks in the vault, and `@path` references in a harness.
The deck needs one contract for the file structure and the link form, one a machine can read as a graph, and the graph has to be rebuildable from the files alone (frame 04 of the canvas).

## Decision Drivers

- One required key, so a file with Agent Skills frontmatter needs one addition, and the Agent Skills `metadata` map is the place that specification reserves for it
- Standard Markdown links, so GitHub, lychee, rumdl, and a plain parser resolve them
- No central registry of types, so a deck adds a kind without asking anyone
- A published specification another organization maintains

## Considered Options

1. Bespoke frontmatter: keep the fields each file kind grew. The contract is then written down nowhere, and a graph tool learns each kind by hand.
2. [MIF][MIF]: typed relationships, a JSON-LD projection, bi-temporal fields, W3C PROV. It fits provenance and records, and it asks every file for more than a type. Deferred rather than rejected: the `modeled-information-format-alignment` change decides that alignment.
3. [Open Knowledge Format 0.2][OKF]: a bundle is a directory of Markdown files with YAML frontmatter. `type` is the only required key, the identifier is the file path, links are standard Markdown, `index.md` and `log.md` are reserved, consumers tolerate unknown keys and types.

## Decision Outcome

Option 3. The deck MUST be a conformant Open Knowledge Format 0.2 bundle, with one exception: a rune keeps its `type` under the Agent Skills `metadata` map until a harness matrix shows that every harness accepts a top-level key.
Every Markdown file outside the reserved names MUST have a `type`.
A record, a specification, or a proposal MUST link to another deck file with a relative Markdown link, never a wikilink or an `@path` reference.
An instruction body MAY use the `@path` form where its harness reads it, because that text is what the harness loads.
The deck root `index.md` MUST declare `okf_version: "0.2"`.
MIF alignment continues where OKF is silent: provenance, typed relationships, and the record lifecycle.

### Consequences

- [+] A directory of files reads as a graph, and a database over it is a rebuildable index, never a second home for the facts.
- [+] Every deck link resolves in GitHub and in the lychee check, and Obsidian resolves relative Markdown links. Fragment conventions differ by renderer, so lychee with fragments is the deck's arbiter.
- [-] Wikilinks are kept out of the deck, so a note copied from the vault gets rewritten at the boundary. The Obsidian compatibility capability specifies that rewrite.
- [-] A rune has its `type` under the Agent Skills `metadata` map rather than at the top level, so a strict OKF consumer reads a rune as untyped until a harness matrix shows a top-level key is tolerated. That is a known non-conformance.

[MIF]: https://github.com/modeled-information-format/MIF
[OKF]: https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md
