---
title: Metadata Inside Files
description: Metadata belongs inside the file it describes, with sealed provenance sidecars as the one exception
type: adr
category: architecture
tags:
    - architecture
    - metadata
    - portability
status: accepted
created: 2026-03-30
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
    - "obsidian://open?vault=Atlas&file=Library%2FCanvas%2FPlain%20Text%20Wins"
    - "https://github.com/N4M3Z/forge-core/blob/main/docs/decisions/CORE-0002%20Metadata%20Inside%20Files.md"
change: plain-text-first-principles
---

# Metadata Inside Files

## Context and Problem Statement

Every Markdown file has metadata, and this record says where the author stores it. [CORE-0001](CORE-0001%20Markdown%20as%20System%20Language.md) makes Markdown the system language. The metadata of a file is its status, its author, its tags, its relationships, and its dates.
Knowledge tools store that metadata in one of two places. One tool keeps the metadata in a database beside the files. Another tool keeps it inside each file.

## Decision Drivers

- The owner moves files between git repositories, Obsidian vaults, *[model][MODEL]* contexts, continuous integration (CI) pipelines, and shared drives
- Metadata that does not move with its file is invisible to the reader, and the owner loses it in the end
- Obsidian, Claude Code, GitHub, shell scripts, and CI validators all read the same metadata
- No tool is the keeper of the metadata. The file is the source of truth.

## Considered Options

1. An external database. [Evernote][EVERNOTE], [DEVONthink][DEVON], [TheBrain][BRAIN], and [Bear][BEAR] keep metadata in a proprietary database outside the files. Queries are fast. Git, a text editor, and a [model][MODEL] cannot see the metadata. A file that the owner moves loses its metadata. The database is one point of failure, and it locks the owner in.
2. *[Sidecar][SIDECAR]* files. The author writes a `.yaml` or `.json` beside each `.md`. The data stays in the filesystem. The number of files doubles. A rename or a move orphans the [sidecar][SIDECAR], and no tool warns.
3. Metadata inside the file. The metadata moves with the file. Every tool that reads the file gets the metadata, and there is nothing to synchronize.

## Decision Outcome

Option 3. The author MUST keep metadata inside the file it describes. A database, a [sidecar][SIDECAR], or a separate tracking system MUST NOT hold it.
The one exception is the sealed *[provenance record][PROVENANCERECORD]*. It goes into a [sidecar][SIDECAR] under `.provenance/` beside each deployed *[artifact][ARTIFACT]*. A seal attests a file at a point in time, so the seal cannot be part of the content it attests.
[Obsidian][OBS] keeps frontmatter in each file and rebuilds its metadata cache from the files. A vault of thousands of notes moves through git with nothing but the files ([Obsidian Properties][OBS-PROPS]).
The author writes the metadata as YAML frontmatter ([CORE-0003](CORE-0003%20YAML%20Frontmatter%20for%20Machine%20Readability.md)).

### Consequences

- [+] A file describes itself, and the owner moves it to any system that reads text
- [+] The metadata depends on nothing outside the file
- [+] A whole class of bugs disappears: orphaned metadata, stale [sidecars][SIDECAR], and failed synchronization
- [-] A file grows slightly. Compact frontmatter limits the growth.

## More Information

- Rewritten on 2026-10-19 in the plain spoken register. The decision is unchanged.

[EVERNOTE]: https://evernote.com/
[DEVON]: https://www.devontechnologies.com/apps/devonthink
[BRAIN]: https://thebrain.com/
[BEAR]: https://bear.app/
[OBS]: https://obsidian.md/
[OBS-PROPS]: https://help.obsidian.md/properties
[MODEL]: ../specs/glossary/model.md
[PROVENANCERECORD]: ../specs/glossary/provenance-record.md
[SIDECAR]: ../specs/glossary/sidecar.md
[ARTIFACT]: ../specs/glossary/artifact.md
