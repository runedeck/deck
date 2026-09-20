---
adr: docs/changes/parallel-agent-teams/adr.md
status: proposed
decisions:
    - DECK-0016 Forge Adoption
---

# Implement change tasks in parallel workspaces

## Why

Per-workspace briefs were retyped for every parallel implementation. One skill splits tasks into packages with disjoint file ownership, runs one child per isolated workspace, and integrates on trunk.

## What Changes

- The AgentTeam skill at `runes/development/skills/AgentTeam/`, condensed from forge for frontier models.
- Deploys only where a workflow tool exists (`targets: [claude, agentskills]`) and stops with one sentence elsewhere.

## Capabilities

- parallel-agent-teams (new)

## Impact

- `runes/development/skills/AgentTeam/` (new).
- Split from the forge-adoption change on 2026-09-20. DECK-0016 records the adoption as a whole.
