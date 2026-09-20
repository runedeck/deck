---
title: "Restrict remote writes"
description: "The RemoteWrites rule enters the deck as a rewrite of its forge origin, with the rules it must keep."
type: adr
category: architecture
tags:
    - runedeck
    - rule
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
change: restrict-remote-writes
---

# Restrict remote writes

## Context and Problem Statement

Prohibitions against merging, commenting, labelling, and pushing were retyped in every session and still leaked. A rule is always on. A three-model review agreed the list cannot live in a skill.

## Considered Options

1. Keep the forge artifact as it is and install it through the forge path.
2. Adopt it through AdoptArtifact with a sealed provenance record.
3. Rewrite it for frontier models inside a deck change.

## Decision Outcome

Option 3. Forge is first-party and retires, so no provenance record is needed. The rewrite keeps the pattern and removes the material that targeted weaker models and other harnesses.

The rule MUST keep these rules:

- An agent MUST NOT merge, close, comment on, review, or relabel a pull request or issue, and MUST NOT push to a remote, except through the repository's guarded push on a branch it created.
- The invoking agent MAY apply the one review label the prompt names, and MAY apply the correctness review label once per green head on a pull request it opened or babysits.
- A child agent MUST NOT use either exception.

## Consequences

- The rule has one home in the deck and one spec with the rules above.
- A bench case and a behavior proof are deferred tasks. Until they exist the rule carries no verdict.
