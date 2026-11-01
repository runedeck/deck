---
title: "Consumer Ceremony Synchronization"
description: "Consumers of the skeleton template synchronize through Copier from a real recorded commit, keep only declared additions, and reseal sealed prose after mechanical corrections"
type: adr
category: process
tags:
    - ceremony
    - template
    - provenance
status: accepted
created: 2026-09-11
updated: 2026-10-19
author: "@N4M3Z"
project: deck
related:
    - "DECK-0005 Artifact Lifecycle and Evidence Tokens"
    - "DECK-0010 Declared World in RDF"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5@claude"]
informed: []
upstream: []
change: use-single-repository-skeleton
---

# Consumer Ceremony Synchronization

## Context and Problem Statement

The deck *[repository][REPOSITORY]* adopted six prose and workflow *[linters][LINTER]* and the push check for `jj` before the skeleton *[template][TEMPLATE]* had them. The [repository][REPOSITORY]'s checks and the [template][TEMPLATE] disagreed in every shared file. Its `answers.yaml` pinned a skeleton commit two months old. The weekly ceremony audit reported the same intentional rows each week (deck#45).

The cli clone pinned a tag that never existed on skeleton, so Copier could not update the cli clone at all. Skeleton now has the [linters][LINTER], the push check, the divergence register, and seed-once files, so the consumers can converge on it. The open question was how the owner brings a diverged consumer back under the [template][TEMPLATE] without losing what the consumer added.

## Decision Drivers

- Copier must do the merge, so the next update has a real baseline to diff from.
- The merge must keep the deck [repository][REPOSITORY]'s own checks (mdschema skills, Stable shell schemas, ontology shapes, openspec, provenance digests).
- A sealed adoption *[sidecar][SIDECAR]* must remain valid after a prose correction. The author must reseal it through the reviewed reseal path and never through a regex rewrite.

## Considered Options

1. The owner trusts `copier update` alone from the recorded pin and resolves its conflicts by hand.
2. The owner recovers a historical baseline for each consumer and replays its additions.
3. The owner resets the recorded reference and compares a fresh render. The owner then reconciles by hand.

## Decision Outcome

The owner chose option 1 for both consumers. The deck [repository][REPOSITORY]'s `482ea1f` pin is a real skeleton commit. The cli clone gets option 1 after the owner rewrites its phantom `v0.5.0` pin to the same baseline.

Copier merges from the baseline to the new skeleton commit. For every file with both [template][TEMPLATE] and consumer edits, the owner takes the [template][TEMPLATE] side. The owner then re-adds the consumer's own hooks, targets, excludes, and workflow steps on top. Files the [template][TEMPLATE] seeds once (`CHANGELOG.md`, `AGENTS.md`, `CONTRIBUTING.md`, `INSTALL.md`, `CODEOWNERS`, `.gitignore`) remain the consumer's. The result records the new full skeleton commit in `answers.yaml`.

The author corrects prose that the generated Vale style rejects at the reported position. The author reseals every sealed file the corrections touch with the reseal step, `rune adopt reseal`. The reseal preserves the source and review facts and rewrites only the subject digest. The Simplified Technical English example and reference files keep their deliberate errors. A path-scoped Vale override in `.vale.ini` protects them, and the author does not edit them.

Option 2 has no baseline to recover: the deck [repository][REPOSITORY]'s additions arrived across dozens of commits. Option 3 leaves Copier with two equal references and applies nothing, so the next update would conflict on every line again.

### Consequences

- [+] Copier updates from the recorded commit again. The weekly parity audit compares against a real baseline.
- [+] The checks that only the deck [repository][REPOSITORY] runs sit as additions on top of the [template][TEMPLATE]'s hook list. A future [template][TEMPLATE] edit of a shared hook merges cleanly. An edit of one of those additions is the deck [repository][REPOSITORY]'s to make.
- [-] Every prose edit in a sealed file cost a reseal. The [sidecars][SIDECAR] record the new digests with the original review facts intact.
- [-] The `.vale.ini` path overrides belong to the deck [repository][REPOSITORY] alone, and they will conflict on the next [template][TEMPLATE] edit of that file. The divergence register does not cover them yet, because the register only approves whole-file differences.

## More Information

- Rewritten on 2026-10-19 in the plain spoken register. The decision is unchanged.

[REPOSITORY]: ../specs/glossary/repository.md
[LINTER]: ../specs/glossary/linter.md
[TEMPLATE]: ../specs/glossary/template.md
[SIDECAR]: ../specs/glossary/sidecar.md
