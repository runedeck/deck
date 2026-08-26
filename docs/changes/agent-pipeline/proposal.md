---
adr: "docs/decisions/DECK-0008 Idea-to-Merge Flywheel.md"
status: proposed
---
# Agent Pipeline

## Why

Ideas enter the stack ad hoc, and finished passes leave without teaching anything. The owner's operating model is agents as the primary computer interface, so the path from a raw thought to a merged change and back into context must be one named loop.

## What Changes

- A design document defines the idea-to-merge flywheel: prompt, pushback, specify, isolate, swarm, gates, review, babysit, approve, extract, recycle.
- DECK-0008 records the loop and the placement decisions: memory advisory-only, Obsidian out of the flow, pi as an edge, rift as isolation only, Measure kept in the loop.
- The IntakeIdea skill instantiates the first missing stage: a raw idea becomes a challenged, scaffolded spec change.
- Delta specifications state the intake and extraction contracts as MUST requirements.

## Capabilities

- idea-intake (new)
- artifact-extraction (new)
- declared-constraints (new)

## Impact

- `docs/changes/agent-pipeline/`: proposal, design, delta specifications, tasks.
- `docs/decisions/DECK-0008 Idea-to-Merge Flywheel.md` and `docs/decisions/DECK-0009 Declared Constraints over Proposed Changes.md`.
- `runes/core/skills/IntakeIdea/SKILL.md`: the new intake skill.
- `CHANGELOG.md`.
