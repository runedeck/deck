---
title: Retirement Path
description: Retirement removes an artifact from every store through the same review ceremony that admitted it and keeps every evidence record
type: adr
category: architecture
tags:
    - architecture
    - lifecycle
    - retirement
status: accepted
created: 2026-08-19
updated: 2026-10-19
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
change: lifecycle-stages-and-evidence
---

# Retirement Path

## Context and Problem Statement

The stack defines how *[artifacts][ARTIFACT]* arrive and nothing about how they leave. The first first-party *[module][MODULE]* teardown is live, and it exposed three loose ends. *[Deck][DECK]* removal, consumer manifest cleanup, and provider teardown are separate manual acts. Nobody has stated what happens to the evidence of the retired [artifact][ARTIFACT]. First-party provenance *[sidecars][SIDECAR]* raised the question of what provenance is for at all.

## Decision Drivers

- An [artifact][ARTIFACT] that leaves must leave everywhere, or stale copies keep loading context.
- Evidence has historical value after the [artifact][ARTIFACT] leaves: *[verdicts][VERDICT]* and reviews explain past behavior.
- Provenance [sidecars][SIDECAR] cost maintenance (the check-provenance hook now enforces digest freshness), so they must justify that cost.
- Deletion must be as reviewable as addition, because a quiet removal is a governance hole.

## Considered Options

1. **Ad-hoc deletion**: remove files where someone notices them, with no stated principle.
2. **Tombstones everywhere**: keep a marker for every removed [artifact][ARTIFACT] in every store.
3. **Reviewed reverse path with evidence retention**: removal goes through the review ceremony, evidence stays, and provenance is scoped to ownership boundaries.

## Decision Outcome

Option 3. Retirement runs the flow in reverse, per store. The provider account drops its rendered configuration. The consumer drops the manifest entry, and pruning removes the deployed files that the deploy manifest tracks.

The [deck][DECK] removes the [artifact][ARTIFACT] and its [sidecar][SIDECAR] in a reviewed *[change][CHANGE]* that records the reason. The workshop ledger captures the retirement decision. Evidence records (bench [verdicts][VERDICT], review history, *[decision records][DECISIONRECORD]*) stay.

The teardown also sets the provenance principle: [sidecars][SIDECAR] exist to import trust across an ownership boundary. First-party [artifacts][ARTIFACT] hold their trust in the authorship ceremony, so removing first-party [sidecars][SIDECAR] corrects a mistake and loses nothing.

### Consequences

- [+] Retirement becomes auditable: each removal is a reviewed [change][CHANGE], and drift *[routines][ROUTINE]* can flag [artifacts][ARTIFACT] present in one store and absent upstream.
- [+] The provenance principle shrinks the [sidecar][SIDECAR] population to adopted [artifacts][ARTIFACT], which shrinks what the check-provenance hook has to check.
- [+] A future `rune retire` command has a defined transaction to implement: one [artifact][ARTIFACT], three stores, one review.
- [+] Evidence retention means that benchmarks of retired [artifacts][ARTIFACT] remain citable when a successor claims the same behavior.

## More Information

- Rewritten on 2026-10-19 in the plain spoken register. The decision is unchanged.

[ARTIFACT]: ../specs/glossary/artifact.md
[MODULE]: ../specs/glossary/module.md
[DECK]: ../specs/glossary/deck.md
[SIDECAR]: ../specs/glossary/sidecar.md
[VERDICT]: ../specs/glossary/verdict.md
[CHANGE]: ../specs/glossary/change.md
[DECISIONRECORD]: ../specs/glossary/decision-record.md
[ROUTINE]: ../specs/glossary/routine.md
