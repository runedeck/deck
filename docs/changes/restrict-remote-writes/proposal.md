---
adr: docs/changes/restrict-remote-writes/adr.md
status: proposed
decisions: ["Restrict remote writes", "DECK-0016 Forge Adoption"]
---

# Restrict remote writes

## Why

Prohibitions against merging, commenting, labelling, and pushing were retyped in every session and still leaked. A rule is always on. A three-model review agreed the list cannot live in a skill.

## What Changes

- The RemoteWrites rule at `runes/core/rules/RemoteWrites.md`, rewritten from its forge origin for frontier models.

## Capabilities

- restrict-remote-writes (new)

## Impact

- `runes/core/rules/RemoteWrites.md` (new).
- Split from the forge-adoption change on 2026-09-20. DECK-0016 records the adoption as a whole.
