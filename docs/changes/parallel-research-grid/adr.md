---
title: "Research in parallel tracks with cross-model verification"
description: "The ResearchGrid skill enters the deck as a rewrite of its forge origin, with the rules it must keep."
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
change: parallel-research-grid
---

# Research in parallel tracks with cross-model verification

## Context and Problem Statement

Multi-track research was one of four fan-out shapes. One skill splits a question into tracks, gathers sourced rows, and verifies each row with a different model.

## Considered Options

1. Keep the forge artifact as it is and install it through the forge path.
2. Adopt it through AdoptArtifact with a sealed provenance record.
3. Rewrite it for frontier models inside a deck change.

## Decision Outcome

Option 3. Forge is first-party and retires, so no provenance record is needed. The rewrite keeps the pattern and removes the material that targeted weaker models and other harnesses.

The skill MUST keep these rules:

- ResearchGrid MUST verify each row with a model different from the one that gathered it and MUST quote the supporting excerpt.
- ResearchGrid MUST mark a row rejected when the verifier cannot find the claim in the cited source.
- ResearchGrid MUST mark a load-bearing number unsupported until a second source agrees.

## Consequences

- The skill has one home in the deck and one spec with the rules above.
- A bench case and a behavior proof are deferred tasks. Until they exist the skill carries no verdict.
