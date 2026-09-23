---
adr: docs/changes/leverage-parallel-agent-teams/adr.md
status: proposed
decisions: ["Implement change tasks in parallel workspaces"]
---

# Implement change tasks in parallel workspaces

## Why

Per-workspace briefs were retyped for every parallel implementation. One skill splits tasks into packages with disjoint file ownership, runs one child per isolated workspace, and integrates on trunk.

## What Changes

- The AgentTeam skill at `runes/development/skills/AgentTeam/`, rewritten from its forge origin for frontier models.
- Deploys only where a workflow tool exists (`targets: [claude, agentskills]`) and stops with one sentence elsewhere.

## Capabilities

- leverage-parallel-agent-teams (new)

## Impact

- `runes/development/skills/AgentTeam/` (new).

## Risks

- A workflow skill reaches a harness with no workflow tool. Guard: `targets`, plus a first line in the body that stops and says so. Task 3.4 verifies the filter.
- Two parallel packages want one file. Guard: the planner merges them or makes one depend on the other.
