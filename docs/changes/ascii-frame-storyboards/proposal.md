---
adr: docs/changes/ascii-frame-storyboards/adr.md
status: proposed
decisions: ["Confirm each stage with an ASCII frame", "DECK-0016 Forge Adoption"]
---

# Confirm each stage with an ASCII frame

## Why

A frame before the first write and a delta frame after the stage give one confirmation seam per stage.

## What Changes

- The Storyboard skill at `runes/development/skills/Storyboard/`, rewritten from its forge origin for frontier models.

## Capabilities

- ascii-frame-storyboards (new)

## Impact

- `runes/development/skills/Storyboard/` (new).
- Split from the forge-adoption change on 2026-09-20. DECK-0016 records the adoption as a whole.

## Risks

- The question tool differs per harness. Guard: AskUserQuestion in Claude Code, a plain question elsewhere, `ask-user` in pi as a later package change.
