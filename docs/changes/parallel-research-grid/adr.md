---
title: Research in parallel tracks with cross-model verification
description: The ResearchGrid skill enters the deck as a condensed rewrite of its forge origin.
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
change: parallel-research-grid
---

# Research in parallel tracks with cross-model verification

## Context and Problem Statement

Multi-track research was one of four fan-out shapes. One skill splits a question into tracks, gathers sourced rows per track, and verifies each row with a different model against its cited page.

## Considered Options

1. Keep the forge artifact as it is and install it through the forge path.
2. Adopt it through AdoptArtifact with a sealed record.
3. Rewrite it for frontier models inside a deck change.

## Decision Outcome

Option 3. Forge is first-party and retires, so no provenance record is needed. The rewrite keeps the pattern and drops the guidance that only weaker models needed.

## Consequences

- The skill has one home in the deck and one spec with MUST statements.
- Bench cases and behavior proofs are deferred tasks. Until they exist the skill carries no verdict.
