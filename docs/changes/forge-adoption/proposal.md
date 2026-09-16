---
adr: "docs/decisions/DECK-0016 Forge Adoption.md"
status: proposed
---

# Forge Adoption

## Why

See the linked ADR for the decision rationale. This proposal records the change in scope.

DECK-0008 names the loop from idea to merge and says every middle stage already exists. It does not: the stages exist as separate skills with no router, no confirmation seam, and no reusable fan-out. A 45-day review of the owner's sessions found the cost concentrated in four fan-out-verify-report shapes (merge polling, per-workspace briefs, hostile prose rounds, multi-track research) and in prohibitions retyped every session. The forge modules hold mature versions of these patterns, written for weaker models and for a harness the deck no longer uses.

## What Changes

- Six skills in `runes/development/`, condensed from forge-core, forge-dev, and forge-council for frontier models: ForgeCycle (the DECK-0008 stage router, one edge per turn), Storyboard (ASCII frames with a confirmation checkpoint per stage), MergeTrain, AgentTeam, AdversaryReview, ResearchGrid (workflow skills whose script is a file beside `SKILL.md`).
- One rule in `runes/core/rules/`, RemoteWrites: a command list, never `gh pr merge|close|comment|review|edit --add-label|--remove-label`, `gh issue comment|close`, `git push`, `jj git push`, or a thread resolution, with one exception for the review label the prompt names. Always on. A three-model review was unanimous that this cannot live in a skill.
- The four workflow skills deploy only where a workflow tool exists (`targets: [claude, agentskills]`), stop with one sentence elsewhere, and the filter is verified before merge.
- Deferred by owner decision, each a task under Follow-up: bench cases (BenchArtifact), behavior proofs (DECK-0015), the pi package changes these skills would benefit from (script path for the workflow tool, `ask-user`), the cli support they want (companion check in `rune validate`, `rune spec show --schematic`, an `AGENTS.md` assembly target), and the removal of the interim copies from the pi package. This change edits nothing outside the deck.

## Capabilities

- agentic-loop (new): the ForgeCycle and Storyboard skills, and the RemoteWrites core rule
- workflow-skills (new): MergeTrain, AgentTeam, AdversaryReview, ResearchGrid

## Impact

- `runes/development/skills/{ForgeCycle,Storyboard,MergeTrain,AgentTeam,AdversaryReview,ResearchGrid}/` (new).
- `runes/core/rules/RemoteWrites.md` (new).
- `runes/core/skills/VersionControl/SKILL.md`: one line pointing at RemoteWrites and MergeTrain.
- `docs/decisions/`: DECK-0016.
- No file outside the deck. The pi package keeps its interim copies until a later package change removes them.
