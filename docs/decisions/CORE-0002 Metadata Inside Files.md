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
updated: 2026-03-30
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
change: core-foundation-principles
---

# Metadata Inside Files

## Context and Problem Statement

[CORE-0001](CORE-0001%20Markdown%20as%20System%20Language.md) makes Markdown the system language. Every Markdown file has metadata: status, author, tags, relationships, dates. The question is where that metadata lives.
Knowledge tools answer it in two ways. One keeps the metadata in a database beside the files. The other keeps it inside each file.

## Decision Drivers

- Files move between git repositories, Obsidian vaults, model contexts, CI pipelines, and shared drives
- Metadata that does not move with its file is invisible and eventually lost
- Obsidian, Claude Code, GitHub, shell scripts, and CI validators all read the same metadata
- No single tool is the keeper of the metadata. The file is the source of truth.

## Considered Options

1. An external database: [Evernote][EVERNOTE], [DEVONthink][DEVON], [TheBrain][BRAIN], and [Bear][BEAR] keep metadata in a proprietary database outside the files. Queries are fast, and git, text editors, and models cannot see the metadata. A file that moves loses it, and the database is a single point of failure and a lock-in.
2. Sidecar files: a `.yaml` or `.json` beside each `.md`. The data stays in the filesystem, the file count doubles, and a rename or move silently orphans the sidecar.
3. Metadata inside the file: the metadata moves with the file, every tool that reads the file gets it, and there is nothing to synchronize.

## Decision Outcome

Option 3. Metadata MUST live inside the file it describes, not in a database, a sidecar, or a separate tracking system.
The one exception is sealed provenance evidence, which goes into `.provenance/` sidecars beside deployed artifacts, because a seal attests a file at a point in time and cannot be part of the content it attests.
[Obsidian][OBS] keeps frontmatter in each file and rebuilds its metadata cache from the files, so a vault of thousands of notes moves through git with nothing but the files ([Obsidian Properties][OBS-PROPS]).
The mechanism is YAML frontmatter ([CORE-0003](CORE-0003%20YAML%20Frontmatter%20for%20Machine%20Readability.md)).

### Consequences

- [+] Files describe themselves and move to any system that reads text
- [+] No external dependency for metadata
- [+] A whole class of bugs disappears: orphaned metadata, stale sidecars, sync failures
- [-] Files grow slightly. Compact frontmatter keeps the cost small.

[EVERNOTE]: https://evernote.com/
[DEVON]: https://www.devontechnologies.com/apps/devonthink
[BRAIN]: https://thebrain.com/
[BEAR]: https://bear.app/
[OBS]: https://obsidian.md/
[OBS-PROPS]: https://help.obsidian.md/properties
