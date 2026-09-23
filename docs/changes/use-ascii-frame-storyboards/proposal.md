---
adr: docs/changes/use-ascii-frame-storyboards/adr.md
status: proposed
decisions: ["Confirm each stage with an ASCII frame"]
---

# Confirm each stage with an ASCII frame

## Why

A frame before the first write and a delta frame after the stage give one confirmation seam per stage.

## What Changes

- The Storyboard skill at `runes/development/skills/Storyboard/`, rewritten from its forge origin for frontier models.

## Capabilities

- use-ascii-frame-storyboards (new)

## Impact

- `runes/development/skills/Storyboard/` (new).

## Risks

- The question tool differs per harness. Guard: AskUserQuestion in Claude Code, a plain question elsewhere, `ask-user` in pi as a later package change.
