---
title: "Art reference research as a deck domain"
description: "Visual reference research, painting plans, and attributed collections enter the deck as the art domain with one skill and one critic agent."
type: adr
category: architecture
tags:
    - runedeck
    - domain
    - art
status: proposed
created: 2026-09-20
updated: 2026-09-20
author: "@N4M3Z"
project: deck
related: []
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5-1"]
informed: []
upstream: []
change: art-reference-domain
---

# Art reference research as a deck domain

## Context and Problem Statement

Reference research and palette planning for painting were repeated by hand. The work has a stable shape: find references, attribute them, plan the palette, get an independent critique.

## Considered Options

1. Keep the procedure in a personal note outside the deck.
2. One skill in core.
3. A separate domain with the skill and a critic agent, so consumers select it by cast.

## Decision Outcome

Option 3. The domain MUST stay out of the `core` cast. The Art skill MUST attribute every reference. The PaletteCritic agent MUST review and MUST NOT author a palette, so the critique stays independent.

## Consequences

- A consumer that wants the domain selects it by cast. Core consumers pay nothing for it.
- The skill has no bench verdict and no proof yet. Both are open tasks.
