---
title: "Confirm each stage with an ASCII frame"
description: "The Storyboard skill enters the deck as a rewrite of its forge origin, with the rules it must keep."
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
change: ascii-frame-storyboards
---

# Confirm each stage with an ASCII frame

## Context and Problem Statement

DECK-0008 names no confirmation seam between a plan and the first write. A frame before the first write and a delta frame after the stage give one seam per stage.

## Considered Options

1. Keep the forge artifact as it is and install it through the forge path.
2. Adopt it through AdoptArtifact with a sealed provenance record.
3. Rewrite it for frontier models inside a deck change.

## Decision Outcome

Option 3. Forge is first-party and retires, so no provenance record is needed. The rewrite keeps the pattern and removes the material that targeted weaker models and other harnesses.

The skill MUST keep these rules:

- Storyboard MUST show an ASCII frame and wait for confirmation before the first file write of a stage.
- Storyboard MUST redraw the frame after a correction and MUST show a delta frame when the stage ends.
- Confirmed frames MUST be saved under `docs/changes/<id>/storyboard/` in order.

## Consequences

- The skill has one home in the deck and one spec with the rules above.
- A bench case and a behavior proof are deferred tasks. Until they exist the skill carries no verdict.
