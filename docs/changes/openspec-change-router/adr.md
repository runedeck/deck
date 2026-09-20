---
title: Route each change to its next stage
description: The ForgeCycle skill enters the deck as a condensed rewrite of its forge origin.
type: adr
category: architecture
tags:
    - runedeck
    - skill
status: proposed
created: 2026-09-20
author: "@N4M3Z"
project: runedeck
related:
    - DECK-0016 Forge Adoption
change: openspec-change-router
---

# Route each change to its next stage

## Context and Problem Statement

DECK-0008 names the loop from idea to merge but no skill routed a change to its next stage. Sessions guessed the stage and skipped the owner of it.

## Considered Options

1. Keep the forge artifact as it is and install it through the forge path.
2. Adopt it through AdoptArtifact with a sealed record.
3. Rewrite it for frontier models inside a deck change.

## Decision Outcome

Option 3. Forge is first-party and retires, so no provenance record is needed. The rewrite keeps the pattern and drops the guidance that only weaker models needed.

## Consequences

- The skill has one home in the deck and one spec with MUST statements.
- Bench cases and behavior proofs are deferred tasks. Until they exist the skill carries no verdict.
