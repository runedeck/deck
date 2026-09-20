---
title: "Quality job builds the pinned rune"
description: "The deck's quality job installs rune from the cli at a pinned commit, outside the tree, so the real-graph hook runs under REQUIRE_GATES."
type: adr
category: infrastructure
tags:
    - runedeck
    - ci
    - ontology
status: proposed
created: 2026-09-20
updated: 2026-09-20
author: "@N4M3Z"
project: deck
related:
    - "DECK-0010 Declared World in RDF"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5-1"]
informed: []
upstream: []
change: quality-job-installs-rune
---

# Quality job builds the pinned rune

## Context and Problem Statement

A `REQUIRE_GATES` hook that needs a binary the runner lacks fails the job, by design. The real-graph hook needs `rune`, and the quality job never had it. Two ways to get it: check the cli out into the tree and build it, as the contract job does, or install it outside the tree.

## Considered Options

1. Check out the cli in-tree and build, like the contract job.
2. `cargo install` from the cli at a pinned commit into the runner's cargo bin.
3. Publish a release binary and fetch it by digest, like rudof.

## Decision Outcome

Option 2. An in-tree checkout sits under the all-files hooks (typos, rumdl, vale) and would need an exclusion in every one of them. A release binary does not exist yet. When it does, option 3 replaces this step and the `install-tools.local` pattern applies.

The job MUST keep these rules:

- The cli revision MUST be a full commit id in the workflow, never a branch name.
- The install MUST happen outside the checked-out tree.

## Consequences

- One more slow step in the quality job, a few minutes without a cache. The timeout rises to 30 minutes.
- The pin moves by hand. A deck change that needs a newer `rune graph export` bumps it in the same change.
