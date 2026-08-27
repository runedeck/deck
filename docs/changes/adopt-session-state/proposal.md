---
adr: "docs/decisions/DECK-0002 Temporary Adoption State.md"
status: proposed
---

# Adopt Session State

## Why

Per-block review data is workflow state. Committing it as provenance made large adoptions add thousands of lines without improving deployment integrity.

## What Changes

- AdoptArtifact keeps verdict ledgers in temporary rune sessions.
- Finalized artifacts commit only source-level sidecars with final file digests.
- The deck removes legacy ledgers and rejects future tracked copies.
- Authorship checks treat a trailing `1m` as a context suffix, not a model identity.

## Capabilities

- adoption-session-state (new)

## Impact

- `runes/core/skills/AdoptArtifact/`
- legacy review ledgers under `.provenance/`
- repository validation and authorship checks
