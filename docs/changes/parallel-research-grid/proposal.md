---
adr: docs/changes/parallel-research-grid/adr.md
status: proposed
decisions: ["Research in parallel tracks with cross-model verification", "DECK-0016 Forge Adoption"]
---

# Research in parallel tracks with cross-model verification

## Why

Multi-track research was one of four fan-out shapes. One skill splits a question into tracks, gathers sourced rows per track, and verifies each row with a different model against its cited page.

## What Changes

- The ResearchGrid skill at `runes/development/skills/ResearchGrid/`, rewritten from its forge origin for frontier models.
- Deploys only where a workflow tool exists (`targets: [claude, agentskills]`) and stops with one sentence elsewhere.

## Capabilities

- parallel-research-grid (new)

## Impact

- `runes/development/skills/ResearchGrid/` (new).
- Split from the forge-adoption change on 2026-09-20. DECK-0016 records the adoption as a whole.
