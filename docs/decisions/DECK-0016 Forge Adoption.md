---
title: "Forge Adoption"
description: "The forge patterns for the agentic loop enter the deck as six condensed skills and one always-on rule, not as a verbatim port and not as pi prompt templates"
type: adr
category: architecture
tags:
    - architecture
    - skills
    - workflows
status: proposed
created: 2026-09-16
updated: 2026-09-16
author: "@N4M3Z"
project: deck
related:
    - "DECK-0008 Idea-to-Merge Flywheel"
    - "CORE-0016 Adversarial Review over Councils"
changes:
    - restrict-remote-writes
    - openspec-change-router
    - ascii-frame-storyboards
    - agentic-merge-train
    - parallel-agent-teams
    - use-adversarial-reviews
    - parallel-research-grid
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5-1", "gpt-6-astra", "grok-4.6", "lumo-max"]
informed: []
upstream:
    - "https://github.com/davis7dotsh/my-pi-setup"
---

# Forge Adoption

## Context and Problem Statement

DECK-0008 names the idea-to-merge loop and leaves its stages to existing skills. The stages
have no router, no confirmation seam, and no reusable fan-out, so the owner writes the same
briefs, prohibitions, and status requests by hand in most sessions. The forge modules hold
working versions of the missing pieces, written for an earlier harness and for weaker models.
pi and Claude Code now both offer a model-authored workflow tool. The question is in what form
these patterns enter the deck.

## Decision Drivers

- Frontier models need contracts and constraints, not tutorials
- Rune deploys skills and rules. It does not deploy pi prompt templates
- A prohibition that only loads with a skill fails in the session that needs it
- A script retyped per run cannot be linted, tested, or versioned
- Nothing here has a bench or a proof yet, so the design must be reviewable as text

## Considered Options

1. **Verbatim port through AdoptArtifact**: forge skills, rules, and agents copied block by block.
   Carries TeamCreate, SendMessage, and AskUserQuestion loops that workflow children cannot run.
2. **pi prompt templates in the pi package**: keeps `$1` arguments, but only pi sees them and rune
   cannot deploy or track them.
3. **Six condensed skills and one rule**: ForgeCycle, Storyboard, MergeTrain, AgentTeam,
   AdversaryReview, ResearchGrid in `runes/development/`, RemoteWrites in `runes/core/rules/`,
   scripts as files beside the skill, deployment limited to harnesses with a workflow tool.

## Decision Outcome

Option 3. Two adversarial passes (astra, grok, lumo on the proposal, then astra and grok on the
change documents, both 2026-09-16) bound these into the change as requirements:

- The prohibitions are an always-on rule written as a command list, so review lanes still run.
- Workflow skills deploy only to `claude` and `agentskills`, stop elsewhere, and the filter is
  verified before merge.
- `workflow.js` is the script, with a 32-agent ceiling and a finite loop ceiling enforced before
  spawning, and no child calls a workflow.
- ForgeCycle names the next DECK-0008 stage and ends its turn. It never invokes a workflow.
- AgentTeam owns files per parallel package, starts dependent packages from the integrated
  tree, and integrates on trunk.
- AdversaryReview applies the CORE-0016 method: a hit ends fixed or rejected with reason.
- ResearchGrid verifies with a different model and an excerpt.
- MergeTrain binds every verdict to the surveyed head SHA and never merges.

This change edits nothing outside the deck. Benches and behavior proofs are deferred by owner
decision, and the status stays proposed until they exist.

## Consequences

- Six skills and one rule replace nine forge sources and four pi prompt templates
- The pi package keeps its interim copies until a later package change removes them, and
  carries the RemoteWrites command list in its `AGENTS.md` until rune can assemble rules there
- One always-on rule costs every session a few lines, which is the price of the deck43 lesson
- Codex, Gemini, and OpenCode receive ForgeCycle, Storyboard, and RemoteWrites, and none of the
  workflow skills, until they have a workflow tool
- Until the bench exists, the only evidence is the adversarial text review
