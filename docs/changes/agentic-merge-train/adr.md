---
title: Clear the pull request queue in one pass
description: The MergeTrain skill enters the deck as a condensed rewrite of its forge origin.
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
change: agentic-merge-train
---

# Clear the pull request queue in one pass

## Context and Problem Statement

Merge polling was one of four fan-out shapes that consumed the owner's sessions. One pass surveys every open pull request, repairs what an agent can repair in isolation, and reports with full URLs. It never merges.

## Considered Options

1. Keep the forge artifact as it is and install it through the forge path.
2. Adopt it through AdoptArtifact with a sealed record.
3. Rewrite it for frontier models inside a deck change.

## Decision Outcome

Option 3. Forge is first-party and retires, so no provenance record is needed. The rewrite keeps the pattern and drops the guidance that only weaker models needed.

## Consequences

- The skill has one home in the deck and one spec with MUST statements.
- Bench cases and behavior proofs are deferred tasks. Until they exist the skill carries no verdict.
