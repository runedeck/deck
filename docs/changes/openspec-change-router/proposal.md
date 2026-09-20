---
adr: docs/changes/openspec-change-router/adr.md
status: proposed
decisions:
    - DECK-0016 Forge Adoption
---

# Route each change to its next stage

## Why

DECK-0008 names the loop from idea to merge but no skill routed a change to its next stage. Sessions guessed the stage and skipped the owner of it.

## What Changes

- The ForgeCycle skill at `runes/development/skills/ForgeCycle/`, condensed from forge for frontier models.

## Capabilities

- openspec-change-router (new)

## Impact

- `runes/development/skills/ForgeCycle/` (new).
- Split from the forge-adoption change on 2026-09-20. DECK-0016 records the adoption as a whole.
