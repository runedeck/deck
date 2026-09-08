---
title: Retirement Path
description: Retirement removes an artifact from every store through the same review ceremony that admitted it and keeps every evidence record
type: adr
category: architecture
tags:
    - architecture
    - lifecycle
    - retirement
status: proposed
created: 2026-08-19
updated: 2026-08-19
author: "@N4M3Z"
project: deck
related:
    - "DECK-0004 Temporary Adoption State"
    - "DECK-0005 Artifact Lifecycle and Evidence Tokens"
    - "DECK-0006 State Stores and Provider Edges"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: []
informed: []
upstream: []
---

# Retirement Path

## Context and Problem Statement

The stack defines how artifacts arrive and nothing about how they leave. The first first-party module teardown is live, and it exposed three loose ends. Deck removal, consumer manifest cleanup, and provider teardown are separate manual acts. Nobody has stated what happens to the retired artifact's evidence. And first-party provenance sidecars raised the question of what provenance is for at all.

## Decision Drivers

- An artifact that leaves must leave everywhere, or stale copies keep loading context.
- Evidence has historical value after the artifact is gone: verdicts and reviews explain past behavior.
- Provenance sidecars cost maintenance (the check-provenance hook now enforces digest freshness), so they must earn that cost.
- Deletion must be as reviewable as addition, because a quiet removal is a governance hole.

## Considered Options

1. **Ad-hoc deletion** — remove files where noticed, keep no rule.
2. **Tombstones everywhere** — keep a marker for every removed artifact in every store.
3. **Reviewed reverse path with evidence retention** — removal follows the review ceremony, evidence stays, provenance is scoped to ownership boundaries.

## Decision Outcome

Option 3. Retirement runs the flow in reverse, per store. The provider account drops its rendered configuration. The consumer drops the manifest entry, and pruning removes the deployed files the deploy manifest tracks. The deck removes the artifact and its sidecar in a reviewed change that records the reason. The workshop ledger captures the retirement decision. Evidence records (bench verdicts, review history, decision records) stay. The teardown also sets the provenance principle: sidecars exist to import trust across an ownership boundary. First-party artifacts carry their trust in the authorship ceremony, so removing first-party sidecars is a correction, not a loss.

## Consequences

- Retirement becomes auditable: a reviewed change per removal, and drift routines can flag artifacts present in one store and absent upstream.
- The provenance rule shrinks the sidecar population to adopted artifacts, which shrinks the check-provenance surface.
- A future `rune retire` command has a defined transaction to implement: one artifact, three stores, one review.
- Evidence retention means benchmarks of retired artifacts remain citable when a successor claims the same behavior.
