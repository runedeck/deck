---
adr: docs/changes/obsidian-placement-and-links/adr.md
status: accepted
decisions: ["Obsidian placement and links as a deck domain"]
---

# Obsidian placement and links

## Why

Vault organization needs clear folder placement for people and meaningful links between notes.
The Euthia audit found duplicate topic names that split navigation despite valid files and readable content.

## What Changes

- Add an organization workflow to Deck's planned Obsidian module.
- Inspect note types, folders, aliases, resolved links, backlinks, and relevant Base filters through Obsidian CLI before proposing changes.
- Choose each note's home from its purpose and the vault's current conventions.
- Add meaningful topic, project, resource, collection, and source links as that purpose becomes clear.
- Distinguish the physical location of a note from its roles in the graph.
- Detect duplicate names and verify each intended link destination before renaming, merging, or moving notes.
- Separate project work from reusable resources while linking both to existing topics.
- Normalize affected frontmatter using current conventions while preserving semantic fields and view dependencies.
- Validate saved notes, resolved relationships, and affected views as separate checks.
- Use the Euthia painting graph as a review case without applying a vault migration in this change proposal.

## Capabilities

### New Capabilities

- `obsidian-placement-and-links`: Organize notes through human-readable placement, meaningful relationships, and application-backed validation.

### Modified Capabilities

None.

## Impact

- Planned implementation home: `runes/obsidian/`. This module does not exist in the inspected checkout.
- Existing Art collection workflows should refer to the shared Obsidian workflow when it becomes available.
- Tests use disposable vault fixtures for duplicate names, direct-link views, note roles, and move preservation.
- No new hierarchy field, universal folder tree, automatic all-to-all linking, or background service is required.
- This proposal does not modify Atlas notes, deploy skills, or change the existing Art work in progress.
