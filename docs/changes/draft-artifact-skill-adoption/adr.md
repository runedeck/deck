---
title: "Draft a rune where the harness loads it"
description: "A new skill, agent, or rule starts as a registered draft in the consumer and enters the deck through rune promote."
type: adr
category: process
tags:
    - runedeck
    - skill
    - lifecycle
status: proposed
created: 2026-09-20
updated: 2026-09-20
author: "@N4M3Z"
project: deck
related:
    - "DECK-0015 Recorded Behavior Proofs"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5-1", "gpt-6-astra"]
informed: []
upstream: []
change: draft-artifact-skill-adoption
---

# Draft a rune where the harness loads it

## Context and Problem Statement

A rune is useful only where a harness loads it, and the deck is not that place until `rune install` runs. Sessions that wanted to try a skill wrote it into `.claude/skills/` by hand, where the manifest guard treats it as an orphan. The alternative, a deck change for every idea, front-loads the record before the idea has run once.

## Considered Options

1. Keep hand-written files and teach doctor an allowlist.
2. Write every idea into the deck first and deploy to try it.
3. A registered draft in the consumer (`rune draft`, `.drafts`), promoted into the deck when it earns its place (`rune promote`), with one skill that says so.

## Decision Outcome

Option 3, decided with the owner on 2026-09-20. `.drafts` sits beside `.manifest` and is the only thing that separates a draft from an orphan. Promotion writes the deck side first and opens the change with `spec propose`, so the record starts at the moment the rune becomes deck content.

The skill MUST keep these rules:

- DraftArtifact MUST route every new rune through `rune draft` and MUST NOT describe a hand-written provider file as acceptable.
- DraftArtifact MUST name `rune promote` as the only path from a draft into the deck and MUST hand the body to BuildSkill after promotion.
- DraftArtifact MUST tell the session that a draft is local and uncommitted.

## Consequences

- One more skill in core, and one more command pair the session must know. The cli owns the behavior. The skill owns the habit.
- The bench case and a deck-side proof are deferred. Until they exist the skill carries no verdict, as with the other adoptions this month.
