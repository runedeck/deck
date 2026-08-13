---
title: "Temporary Adoption State"
description: "Keep block verdicts in temporary rune sessions and commit only source-level provenance sidecars"
type: adr
category: "architecture"
tags: ["adoption", "provenance", "review"]
status: proposed
created: 2026-08-13
updated: 2026-08-13
author: "Martin Zeman"
project: "deck"
related: []
responsible: []
accountable: []
consulted: []
informed: []
upstream:
    - "https://github.com/runedeck/cli/issues/21"
---

# Temporary Adoption State

## Context and Problem Statement

AdoptArtifact reviews imported content block by block. The first CLI implementation stored every block, verdict, note, and timestamp in a tracked review ledger. Large imports produced thousands of provenance lines even though deployment already relies on each adopted file's source pin and final digest.

## Decision Drivers

- Every imported block must receive a verdict before finalization.
- Workflow details must survive interrupted CLI sessions.
- Published deck artifacts need source attribution and final integrity, not a review transcript.
- A repository must not need local ignore rules to use the CLI safely.

## Considered Options

- Commit the complete review ledger beside each artifact.
- Compress the ledger but keep it as permanent provenance.
- Keep the ledger as temporary CLI state and commit only source-level sidecars.

## Decision Outcome

Keep block text, verdicts, notes, flags, and timestamps in temporary CLI session state. Finalization enforces the complete session, updates each adopt sidecar with its final file digest and reviewed state, then removes the session. The deck commits the artifact and those sidecars only.

The repository rejects tracked `.provenance/review.yaml` and `.provenance/*.review.yaml` files. Existing ledgers are removed after their ordinary provenance sidecars are verified. The rune CLI owns session placement, crash recovery, doctor checks, and reseal behavior under runedeck/cli#21.

## Consequences

- Git history stays concise while block review remains mandatory.
- Source URLs, upstream digests, transforms, reviewed state, and final file digests remain durable.
- Review notes are process data and do not become a second provenance authority.
- Legacy ledgers require removal, but their reviewed sidecars remain valid.
