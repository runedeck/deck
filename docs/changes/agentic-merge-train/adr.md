---
title: "Survey the queue and repair eligible blockers"
description: "The MergeTrain skill enters the deck as a rewrite of its forge origin, with the rules it must keep."
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
change: agentic-merge-train
---

# Survey the queue and repair eligible blockers

## Context and Problem Statement

Merge polling was one of four fan-out shapes that consumed the owner's sessions. One pass surveys every open pull request, repairs what an agent can repair in isolation, and reports with full URLs.

## Considered Options

1. Keep the forge artifact as it is and install it through the forge path.
2. Adopt it through AdoptArtifact with a sealed provenance record.
3. Rewrite it for frontier models inside a deck change.

## Decision Outcome

Option 3. Forge is first-party and retires, so no provenance record is needed. The rewrite keeps the pattern and removes the material that targeted weaker models and other harnesses.

The skill MUST keep these rules:

- MergeTrain MUST record the head SHA of each pull request at survey time and MUST bind every verdict to that SHA.
- MergeTrain MUST report a verdict as stale when the head has moved and MUST NOT merge.
- Every child brief MUST restate the RemoteWrites command list and MUST name the absolute skill path.

## Consequences

- The skill has one home in the deck and one spec with the rules above.
- A bench case and a behavior proof are deferred tasks. Until they exist the skill carries no verdict.
