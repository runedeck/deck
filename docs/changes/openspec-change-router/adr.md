---
title: "Route each change to its next stage"
description: "The ForgeCycle skill enters the deck as a rewrite of its forge origin, with the rules it must keep."
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
change: openspec-change-router
---

# Route each change to its next stage

## Context and Problem Statement

DECK-0008 names the loop from idea to merge, and the deck holds the stage skills, but no skill routes a change to its next stage. The router is the missing edge.

## Considered Options

1. Keep the forge artifact as it is and install it through the forge path.
2. Adopt it through AdoptArtifact with a sealed provenance record.
3. Rewrite it for frontier models inside a deck change.

## Decision Outcome

Option 3. Forge is first-party and retires, so no provenance record is needed. The rewrite keeps the pattern and removes the material that targeted weaker models and other harnesses.

The skill MUST keep these rules:

- ForgeCycle MUST read the change's task state, name the next stage and the skill that owns it, and end its turn.
- ForgeCycle MUST NOT invoke a workflow tool or a workflow skill itself.
- ForgeCycle MUST return to the implement stage on findings, lint failure, or requested changes, and MUST stop when the owner closes the pull request or the owning skill is absent.

## Consequences

- The skill has one home in the deck and one spec with the rules above.
- A bench case and a behavior proof are deferred tasks. Until they exist the skill carries no verdict.
