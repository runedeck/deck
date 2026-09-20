---
adr: docs/changes/agentic-merge-train/adr.md
status: proposed
decisions:
    - DECK-0016 Forge Adoption
---

# Clear the pull request queue in one pass

## Why

Merge polling was one of four fan-out shapes that consumed the owner's sessions. One pass surveys every open pull request, repairs what an agent can repair in isolation, and reports with full URLs. It never merges.

## What Changes

- The MergeTrain skill at `runes/development/skills/MergeTrain/`, condensed from forge for frontier models.
- Deploys only where a workflow tool exists (`targets: [claude, agentskills]`) and stops with one sentence elsewhere.

## Capabilities

- agentic-merge-train (new)

## Impact

- `runes/development/skills/MergeTrain/` (new).
- Split from the forge-adoption change on 2026-09-20. DECK-0016 records the adoption as a whole.
