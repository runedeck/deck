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
updated: 2026-10-19
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

The *[repository][REPOSITORY]* is a directory of Markdown files. A person reads it in an editor or a vault. A *[model][MODEL]* reads it through a *[harness][HARNESS]*. A tool reads it to build a graph or an index.
Either each file says what it is and what it links to, or the reader has to guess.
Three link forms compete. The [repository][REPOSITORY] uses Markdown links, the vault uses wikilinks, and a [harness][HARNESS] uses `@path` references.
The [repository][REPOSITORY] needs one contract for the file structure and the link form, one that a machine can read as a graph. The files alone have to be enough to rebuild the graph (frame 04 of the canvas).

## Decision Drivers

- The contract has one optional key, so a file without the key takes its *[type][TYPE]* from the *[structure schema][STRUCTURESCHEMA]* of its directory. A *[rune][RUNE]* may still carry the key under the Agent Skills `metadata` map.
- Links are standard Markdown, so GitHub, the link checker lychee, the Markdown *[linter][LINTER]* rumdl, and a plain parser resolve them.
- The format does not keep a central registry of [types][TYPE], so a [repository][REPOSITORY] adds a kind without asking anyone.
- Another organization publishes and maintains the specification.

## Considered Options

1. Bespoke frontmatter: the [repository][REPOSITORY] keeps the fields each file kind grew. Nobody writes the contract down, and a graph tool learns each kind by hand.
2. [MIF][MIF], the Modeled Information Format: typed relationships, a JSON-LD (JSON for Linked Data) projection, and bi-temporal fields. It also uses W3C PROV, the provenance standard of the World Wide Web Consortium. It fits provenance and records, and it asks every file for more than a [type][TYPE]. The owner defers this option and does not reject it. The `modeled-information-format-alignment` *[change][CHANGE]* decides that alignment.
3. [Open Knowledge Format 0.2][OKF]: a bundle is a directory of Markdown files with YAML frontmatter. The format requires one key, `type`. The file path is the identifier. Links are standard Markdown. The format reserves the names `index.md` and `log.md`. A consumer tolerates unknown keys and [types][TYPE].

## Decision Outcome

Option 3. The [repository][REPOSITORY] MUST be a conformant Open Knowledge Format 0.2 bundle. A file takes its [type][TYPE] from the [structure schema][STRUCTURESCHEMA] of its nearest directory. An explicit key in the file overrides that [type][TYPE]. A [rune][RUNE] may keep its `type` under the Agent Skills `metadata` map. The graph export fills in the [type][TYPE] for every file.
The author MUST give every Markdown file outside the reserved names a `type`.
A record, a specification, or a proposal MUST link to another file in the [repository][REPOSITORY] with a relative Markdown link. It MUST NOT use a wikilink or an `@path` reference for that.
An *[instruction][INSTRUCTION]* body MAY use the `@path` form where its [harness][HARNESS] reads it, because the [harness][HARNESS] loads that text.
The author MUST declare `okf_version: "0.2"` in the [repository][REPOSITORY] root `index.md`.
MIF alignment continues where the Open Knowledge Format is silent: provenance, typed relationships, and the stages a record passes through.

### Consequences

- [+] A directory of files reads as a graph. A database over it is an index the owner can rebuild. It is never a second home for the facts.
- [+] Every link in the [repository][REPOSITORY] resolves in GitHub and in the link checker, lychee. Obsidian resolves relative Markdown links too. Renderers differ on fragment conventions, so the link checker with fragments on is the [repository][REPOSITORY]'s arbiter.
- [-] The [repository][REPOSITORY] keeps wikilinks out, so whoever copies a note from the vault rewrites its links at the boundary. The Obsidian compatibility *[capability][CAPABILITY]* specifies that rewrite.
- [-] A strict outside reader of the format sees a file without the key as untyped. The reader does so because the [type][TYPE] lives in the directory's [structure schema][STRUCTURESCHEMA] and the graph export. The owner accepts that.

## More Information

- Amended on 2026-10-18: the [type][TYPE] key is optional and derived from the directory's [structure schema][STRUCTURESCHEMA], so the `metadata` map is no longer an exception.
- Amended on 2026-10-18: the record says [repository][REPOSITORY] where it meant the container. It does so because the Open Knowledge Format bundle is the [repository][REPOSITORY] and the marker file marks a *[deck][DECK]*.
- Rewritten on 2026-10-19 in the plain spoken register. The decision is unchanged.

[MIF]: https://github.com/modeled-information-format/MIF
[OKF]: https://github.com/GoogleCloudPlatform/open-knowledge-format-bundle/blob/main/SPEC.md
[REPOSITORY]: ../specs/glossary/repository.md
[MODEL]: ../specs/glossary/model.md
[HARNESS]: ../specs/glossary/harness.md
[STRUCTURESCHEMA]: ../specs/glossary/structure-schema.md
[RUNE]: ../specs/glossary/rune.md
[INSTRUCTION]: ../specs/glossary/instruction.md
[CHANGE]: ../specs/glossary/change.md
[CAPABILITY]: ../specs/glossary/capability.md
[DECK]: ../specs/glossary/deck.md
[TYPE]: ../specs/glossary/type.md
[LINTER]: ../specs/glossary/linter.md
