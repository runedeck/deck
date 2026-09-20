---
title: "Refute a draft before accepting it"
description: "The AdversaryReview skill enters the deck as a rewrite of its forge origin, with the rules it must keep."
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
change: use-adversarial-reviews
---

# Refute a draft before accepting it

## Context and Problem Statement

Hostile prose rounds were run by hand. One skill attacks the original from three disjoint angles and settles every hit (CORE-0016 method).

## Considered Options

1. Keep the forge artifact as it is and install it through the forge path.
2. Adopt it through AdoptArtifact with a sealed provenance record.
3. Rewrite it for frontier models inside a deck change.

## Decision Outcome

Option 3. Forge is first-party and retires, so no provenance record is needed. The rewrite keeps the pattern and removes the material that targeted weaker models and other harnesses.

The skill MUST keep these rules:

- AdversaryReview MUST attack the original text and MUST NOT rewrite it before the attack.
- AdversaryReview MUST bind each hit to a quoted line.
- AdversaryReview MUST record a disposition of fixed or rejected with a stated reason for every hit.

## Consequences

- The skill has one home in the deck and one spec with the rules above.
- A bench case and a behavior proof are deferred tasks. Until they exist the skill carries no verdict.
