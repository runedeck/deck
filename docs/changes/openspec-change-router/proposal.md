---
adr: docs/changes/openspec-change-router/adr.md
status: proposed
decisions: ["Route each change to its next stage"]
---

# Route each change to its next stage

## Why

DECK-0008 names the loop from idea to merge but no skill routed a change to its next stage. The router is the missing edge.

## What Changes

- The ForgeCycle skill at `runes/development/skills/ForgeCycle/`, rewritten from its forge origin for frontier models.

## Capabilities

- openspec-change-router (new)

## Impact

- `runes/development/skills/ForgeCycle/` (new).
