---
title: "Consumer Ceremony Synchronization"
description: "Consumers of the skeleton template synchronize through Copier from a real recorded commit, keep only declared additions, and reseal sealed prose after mechanical corrections"
type: adr
category: process
tags:
    - ceremony
    - template
    - provenance
status: proposed
created: 2026-09-11
updated: 2026-09-11
author: "@N4M3Z"
project: deck
related:
    - "DECK-0005 Artifact Lifecycle and Evidence Tokens"
    - "DECK-0010 Declared World in RDF"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5"]
informed: []
upstream: []
---

# Consumer Ceremony Synchronization

## Context and Problem Statement

The deck adopted six prose and workflow linters and the jj push check before the skeleton template carried them. Its checks and the template disagreed in every shared file, its `answers.yaml` pinned a skeleton commit two months old, and the weekly ceremony audit reported the same intentional rows each week (deck#45). The cli pinned a tag that never existed on skeleton, so Copier could not update it at all. Skeleton now carries the linters, the push check, the divergence register, and seed-once files, so the consumers can converge. The open question was how to bring a diverged consumer back under the template without losing what it added.

## Decision Drivers

- Copier must do the merge, so the next update has a real baseline to diff from.
- Deck-only checks (mdschema skills, Stable shell schemas, ontology shapes, openspec, provenance digests) must survive the merge.
- Sealed adoption sidecars must stay valid after prose corrections, through the reviewed reseal path and never a regex rewrite.

## Considered Options

1. Trust `copier update` alone from the recorded pin and hand-resolve its conflicts.
2. Recover a historical baseline for each consumer and replay its additions.
3. Reset the recorded reference, compare a fresh render, and reconcile by hand.

## Decision Outcome

Chosen option: option 1 for the deck, whose `482ea1f` pin is a real skeleton commit, and option 1 for the cli after rewriting its phantom `v0.5.0` pin to the same baseline. Copier merges from the baseline to the new skeleton commit. Every file with both template and consumer edits is resolved by taking the template side and re-adding the consumer's own hooks, targets, excludes, and workflow steps on top. Files the template seeds once (`CHANGELOG.md`, `AGENTS.md`, `CONTRIBUTING.md`, `INSTALL.md`, `CODEOWNERS`, `.gitignore`) stay the consumer's. The result records the new full skeleton commit in `answers.yaml`.

Prose the generated Vale style rejects is corrected at the reported position, and every sealed file the corrections touch is resealed with `rune adopt reseal`, which preserves the source and review facts and rewrites only the subject digest. The Simplified Technical English example and reference files keep their deliberate errors through a path-scoped rule override in `.vale.ini`, not through edits.

Option 2 has no baseline to recover: the deck's additions arrived across dozens of commits. Option 3 leaves Copier with two equal references and applies nothing, so the next update would conflict on every line again.

## Consequences

- Copier updates from the recorded commit again, and the weekly parity audit compares against a real baseline.
- Deck-only checks live as additions on top of the template's hook list. A future template change to a shared hook merges cleanly. A change to a deck-only hook is the deck's to make.
- Every prose edit in a sealed file cost a reseal. The sidecars record the new digests with the original review facts intact.
- The `.vale.ini` path overrides are deck-specific and will conflict on the next template change to that file. The divergence register does not cover it yet, because the register only approves whole-file differences.
