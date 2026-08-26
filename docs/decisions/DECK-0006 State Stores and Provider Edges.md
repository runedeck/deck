---
title: State Stores and Provider Edges
description: Four stores with strict content contracts hold every artifact state, and provider specifics enter only at the Ship and Operate edges
type: adr
category: architecture
tags:
    - architecture
    - state
    - providers
status: proposed
created: 2026-08-19
updated: 2026-08-19
author: "@N4M3Z"
project: deck
related:
    - "DECK-0004 Routine Environment Matrix"
    - "DECK-0005 Artifact Lifecycle and Evidence Tokens"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: []
informed: []
upstream: []
---

# State Stores and Provider Edges

## Context and Problem Statement

Artifact state lives in four places: workshop directories under `~/Agents/<owner>/<project>`, the deck repositories, the consumer checkout with its manifest and rendered private prompts, and the provider accounts. Nothing states what each place may hold, so content leaks across the boundaries: canonical text edited in provider trees, personal values almost committed to repositories, and provider accounts accumulating configuration nobody can rebuild. Providers also differ in what they accept, and every difference tempts a fork of the canonical artifact.

## Decision Drivers

- A fresh machine must be able to rebuild every store below the workshop from repositories alone.
- Personal values and rendered prompts must never enter a repository.
- Canonical artifacts must stay provider-independent, or every provider change multiplies across the deck.
- The environment matrix (DECK-0004) already bounds provider sessions by data sensitivity; the store contract must compose with it.

## Considered Options

1. **One store** — everything in the deck, providers read it directly.
2. **Free placement** — any state anywhere, conventions only.
3. **Four stores with content contracts and two provider edges** — each store has a MUST and a MUST NOT list; providers plug in at Ship and Operate only.

## Decision Outcome

Option 3. The workshop holds anything, and nothing installs from it. The deck holds only reviewed, proven, schema-valid artifacts and their sidecars, and never review transcripts or personal values. The consumer holds the manifest, deploy manifests, and rendered private prompts, and never canonical content. The provider account holds only configuration rendered from shipped templates, and MUST stay reproducible from the deck plus the consumer. Providers enter at two edges: Ship-side through assembly configuration (`targets`, keep-fields, casing rules, overlays) and Operate-side through adapted routine variants under the DECK-0004 matrix. Canonical frontmatter carries Agent Skills fields plus the three assembly directives, and nothing else.

## Consequences

- Removing a provider changes zero canonical artifacts; adding one needs a provider configuration, optional overlays, and routine variants.
- Reproducibility becomes testable: rebuild a provider account from templates and compare.
- The store contracts give the audit routines concrete assertions: canonical content outside the deck, or personal values inside it, are violations, not judgment calls.
- The workshop stays the one free surface, which keeps capture cheap.
