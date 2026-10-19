---
title: "Temporary Adoption State"
description: "Keep block verdicts in temporary rune sessions and commit only source-level provenance sidecars"
type: adr
category: "architecture"
tags: ["adoption", "provenance", "review"]
status: accepted
created: 2026-08-13
updated: 2026-10-19
author: "Martin Zeman"
project: "deck"
related: []
change: record-provenance-for-adoptions
responsible: []
accountable: []
consulted: []
informed: []
upstream:
    - "https://github.com/runedeck/cli/issues/21"
---

# Temporary Adoption State

## Context and Problem Statement

The AdoptArtifact *[skill][SKILL]* reviews imported content block by block. The first version of the rune command-line interface (CLI) stored every block, verdict, note, and timestamp in a tracked review ledger. A large import produced thousands of provenance lines, even though deployment already relies on each adopted file's source pin and final digest.

## Decision Drivers

- Every imported block must have a verdict before the *[importer][IMPORTER]* seals the adoption.
- Workflow details must survive an interrupted CLI session.
- A published *[artifact][ARTIFACT]* in the *[repository][REPOSITORY]* needs its source attribution and its final digest. It does not need a review transcript.
- A [repository][REPOSITORY] must not need local ignore rules to use the CLI safely.

## Considered Options

- The [importer][IMPORTER] commits the complete review ledger beside each [artifact][ARTIFACT].
- The [importer][IMPORTER] compresses the ledger and keeps it as permanent provenance.
- The CLI keeps the ledger as temporary state, and the [importer][IMPORTER] commits only source-level *[sidecars][SIDECAR]*.

## Decision Outcome

The CLI keeps block text, verdicts, notes, flags, and timestamps in temporary session state. At finalization, the [importer][IMPORTER] checks that the session is complete. It then writes the final file digest and the reviewed state into each adoption [sidecar][SIDECAR], and removes the session. The author commits only the [artifact][ARTIFACT] and those [sidecars][SIDECAR] to the [repository][REPOSITORY].

The [repository][REPOSITORY] rejects a tracked `.provenance/review.yaml` or `.provenance/*.review.yaml` file. The author removes an existing ledger after the *[validator][VALIDATOR]* verifies its ordinary provenance [sidecars][SIDECAR]. The rune CLI owns session placement, crash recovery, doctor checks, and reseal behavior under runedeck/cli#21.

### Consequences

- [+] The git history contains no ledger, and block review remains mandatory.
- [+] Each [sidecar][SIDECAR] keeps the source URL (its Uniform Resource Locator), the upstream digest, the transforms, the reviewed state, and the final file digest.
- [+] Review notes are process data. They never become a second provenance authority.
- [-] The author has to remove each legacy ledger. The reviewed [sidecars][SIDECAR] beside it remain valid.

## More Information

- Rewritten on 2026-10-19 in the plain spoken register. The decision is unchanged.

[SKILL]: ../specs/glossary/skill.md
[IMPORTER]: ../specs/glossary/importer.md
[ARTIFACT]: ../specs/glossary/artifact.md
[SIDECAR]: ../specs/glossary/sidecar.md
[REPOSITORY]: ../specs/glossary/repository.md
[VALIDATOR]: ../specs/glossary/validator.md
