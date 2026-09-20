---
title: "Implement change tasks in parallel workspaces"
description: "The AgentTeam skill enters the deck as a rewrite of its forge origin, with the rules it must keep."
type: adr
category: architecture
tags:
    - runedeck
    - skill
    - forge
status: proposed
created: 2026-09-20
updated: 2026-09-20
author: "@N4M3Z"
project: deck
related:
    - "DECK-0016 Forge Adoption"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5-1", "gpt-6-astra"]
informed: []
upstream: []
change: parallel-agent-teams
---

# Implement change tasks in parallel workspaces

## Context and Problem Statement

Per-workspace briefs were retyped for every parallel implementation. One skill splits tasks into packages with disjoint file ownership and integrates on trunk.

## Considered Options

1. Keep the forge artifact as it is and install it through the forge path.
2. Adopt it through AdoptArtifact with a sealed provenance record.
3. Rewrite it for frontier models inside a deck change.

## Decision Outcome

Option 3. Forge is first-party and retires, so no provenance record is needed. The rewrite keeps the pattern and removes the material that targeted weaker models and other harnesses.

The skill MUST keep these rules:

- AgentTeam MUST give packages that run in parallel disjoint file ownership.
- AgentTeam MUST run one child per isolated workspace and MUST start a dependent package from the integrated tree of its predecessors.
- AgentTeam MUST apply the packages onto trunk in order and MUST run the suite on the combined tree before it reports.

## Consequences

- The skill has one home in the deck and one spec with the rules above.
- A bench case and a behavior proof are deferred tasks. Until they exist the skill carries no verdict.
