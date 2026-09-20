---
title: Restrict remote writes
description: The RemoteWrites rule enters the deck as a condensed rewrite of its forge origin.
type: adr
category: architecture
tags:
    - runedeck
    - rule
status: proposed
created: 2026-09-20
author: "@N4M3Z"
project: runedeck
related:
    - DECK-0016 Forge Adoption
change: restrict-remote-writes
---

# Restrict remote writes

## Context and Problem Statement

Prohibitions against merging, commenting, labelling, and pushing were retyped in every session and still leaked. A rule is always on. A three-model review agreed the list cannot live in a skill.

## Considered Options

1. Keep the forge artifact as it is and install it through the forge path.
2. Adopt it through AdoptArtifact with a sealed record.
3. Rewrite it for frontier models inside a deck change.

## Decision Outcome

Option 3. Forge is first-party and retires, so no provenance record is needed. The rewrite keeps the pattern and drops the guidance that only weaker models needed.

## Consequences

- The rule has one home in the deck and one spec with MUST statements.
- Bench cases and behavior proofs are deferred tasks. Until they exist the rule carries no verdict.
