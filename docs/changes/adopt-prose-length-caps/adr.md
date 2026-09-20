---
title: "Deck prose keeps the cli caps"
description: "Deck requirement statements, scenario steps, and changelog lines stay under the caps rune enforces, and the quality job runs a rune that carries them."
type: adr
category: process
tags:
    - runedeck
    - specs
    - changelog
status: proposed
created: 2026-09-20
updated: 2026-09-20
author: "@N4M3Z"
project: deck
related:
    - "DECK-0013 Local Checks Before Publication"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5-1"]
informed: []
upstream: []
change: adopt-prose-length-caps
---

# Deck prose keeps the cli caps

## Context and Problem Statement

The cli now refuses a requirement statement over 100 words and a changelog line over 200 characters. The deck had both kinds of wall. A rule that lives in the binary is only as strong as the binary CI runs, and the quality job pins its rune by commit.

## Considered Options

1. Keep the deck text as it is and let the pin stay behind the rule.
2. Rewrite the text now, and move the pin when the cli change is on `main`.
3. Rewrite the text and copy the rule into a deck script, so the pin does not matter.

## Decision Outcome

Option 2. One rule, one home, one binary. The rewrite lands first because it is correct on its own, and the pin moves in the same change as soon as the cli commit exists on `main`.

The deck MUST keep these rules:

- A requirement statement MUST stay at or under 100 words, a step at or under 30 words, a changelog line at or under 200 characters.
- The quality job's `RUNE_CLI_REV` MUST point at a cli commit that carries both checks.

## Consequences

- Splitting a requirement multiplies headings. The `pull-request-delivery-contract` delta crosses the 150-line warning, and that capability wants its own split.
- Until the pin moves, the caps hold locally for anyone with a current rune and in CI only through the older checks.
