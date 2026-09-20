---
title: "Obsidian placement and links as a deck domain"
description: "Vault organization enters the deck as the obsidian domain: inspect through the Obsidian CLI, choose a home from purpose, add meaningful links, verify separately."
type: adr
category: architecture
tags:
    - runedeck
    - domain
    - obsidian
status: accepted
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
change: obsidian-placement-and-links
---

# Obsidian placement and links as a deck domain

## Context and Problem Statement

Vault organization was done by hand and produced duplicate topic names that split navigation. The Euthia audit showed the cost. The procedure has a stable shape and belongs in a skill.

## Considered Options

1. A personal note outside the deck.
2. One skill in core.
3. A separate domain, selected by cast, with the Obsidian skill and its fixtures.

## Decision Outcome

Option 3. The skill MUST inspect the vault through the Obsidian CLI before it proposes a change. It MUST choose a note's home from its purpose and the vault's conventions. It MUST verify file outcomes and graph outcomes separately. It MUST NOT fall back to an unsafe path when application evidence is unavailable.

## Consequences

- A consumer that wants vault work selects the domain by cast. Core pays nothing.
- The skill has no bench verdict and no proof yet. Both are open tasks.
