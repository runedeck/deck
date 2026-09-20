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

# Metadata Inside Files

## Context and Problem Statement

[CORE-0001](CORE-0001 Markdown as System Language.md) established markdown as the universal format. Every markdown file needs metadata: status, author, tags, relationships, dates. Where does that metadata live?

Knowledge management tools take two approaches. One stores metadata in an external database beside the files. The other embeds metadata inside each file.

## Decision Drivers

- Files move between systems: git repositories, Obsidian vaults, AI tool contexts, CI pipelines, shared drives
- When a file moves, its metadata must move with it. Orphaned metadata is invisible and eventually disappears.
- Multiple tools must read the same metadata: Obsidian, Claude Code, GitHub, shell scripts, CI validators
- No single tool is the gatekeeper of metadata. The file itself is the source of truth.

## Considered Options

1. **External database**: tools such as [Evernote][EVERNOTE], [DEVONThink][DEVON], [TheBrain][BRAIN], and [Bear][BEAR] store metadata in a proprietary database outside the files. Queries are fast, but git, text editors, and AI tools cannot see the metadata. Files that move between systems lose their metadata. The database becomes a single point of failure and a source of vendor lock-in.

2. **Separate sidecar files**: `.yaml` or `.json` files beside each `.md` file. The data stays in the filesystem, but the file count doubles and sidecars drift from canonical content. A rename or move silently orphans the sidecar.

3. **Metadata inside the file**: embed the metadata in a standard format. When a file moves, its metadata moves with it. Every tool that reads the file gets its metadata. No external dependency, no drift, no orphaning.

## Decision Outcome

Metadata belongs inside the file it describes: not in an external database, not in a sidecar, not in a separate tracking system.

The deck records one exception: sealed provenance evidence lives in `.provenance/` sidecars beside deployed artifacts. A provenance seal attests a file at a point in time, so it cannot live in the frontmatter it attests.

When a file moves, its metadata moves with it. When you read a file, you get its metadata. When you delete a file, its metadata goes with it. There is no synchronization problem because there is nothing to synchronize.

[Obsidian][OBS] proved this at scale: a vault of thousands of markdown files with embedded frontmatter, portable across machines through git. Dataview queries it, and Properties searches it. No database server, no sync service, no proprietary format.

The mechanism for embedded metadata in markdown files is YAML frontmatter.

Metadata MUST live inside the file it describes. A sealed provenance sidecar under `.provenance/` is the one exception, because a seal cannot live in the content it attests.

## Consequences

- Files are self-describing and portable across any system that can read text
- No external dependency for metadata: no database, no service, no proprietary format
- Removes an entire class of bugs: orphaned metadata, stale sidecars, sync failures
- File size increases slightly. Compact YAML frontmatter keeps the cost small.

[EVERNOTE]: https://evernote.com/
[DEVON]: https://www.devontechnologies.com/apps/devonthink
[BRAIN]: https://thebrain.com/
[BEAR]: https://bear.app/
[OBS]: https://obsidian.md/
