---
adr: docs/changes/agentic-merge-train/adr.md
status: proposed
decisions: ["Survey the queue and repair eligible blockers", "DECK-0016 Forge Adoption"]
---

# Survey the queue and repair eligible blockers

## Why

Merge polling was one of four fan-out shapes that consumed the owner's sessions. One pass surveys every open pull request, repairs what an agent can repair in isolation, and reports with full URLs. It never merges.

## What Changes

- The MergeTrain skill at `runes/development/skills/MergeTrain/`, rewritten from its forge origin for frontier models.
- Deploys only where a workflow tool exists (`targets: [claude, agentskills]`) and stops with one sentence elsewhere.

## Capabilities

- agentic-merge-train (new)

## Impact

- `runes/development/skills/MergeTrain/` (new).
- Split from the forge-adoption change on 2026-09-20. DECK-0016 records the adoption as a whole.

## Risks

- A workflow skill reaches a harness with no workflow tool. Guard: `targets`, plus a first line in the body that stops and says so. Task 3.4 verifies the filter and blocks the merge if it does not hold.
- Companion paths resolve against the child's cwd instead of the skill. Guard: the absolute skill path in every child brief. A `rune validate` check is task 4.4.
