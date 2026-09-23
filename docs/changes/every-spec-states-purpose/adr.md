---
title: "A canonical spec names its purpose and its decision"
description: "Every canonical specification under docs/specs/ opens with its own purpose and an H1 that names its directory, states each rule once, and points at the decision it serves."
type: adr
category: process
tags:
    - runedeck
    - specs
status: proposed
created: 2026-09-20
updated: 2026-09-20
author: "@N4M3Z"
project: deck
related:
    - "DECK-0018 Keep Shared Skill Procedures Independent of Harness Syntax"
    - "DECK-0013 Local Checks Before Publication"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5-1"]
informed: []
upstream: []
change: every-spec-states-purpose
---

# A canonical spec names its purpose and its decision

## Context and Problem Statement

Canonical specs arrive by archive, by migration from an openspec tree, or by copy from the skeleton. Three of the repository's five had no purpose of their own, one repeated a rule, and one hid a check rule under a security heading. A reader cannot tell what a spec is for or which decision put it there.

## Considered Options

1. Leave them, because the deltas carry the real content.
2. Rewrite the five now and add the rule that a canonical spec is self-describing.
3. Delete the three with no decision behind them.

## Decision Outcome

Option 2. The three without a decision describe real behavior the repository runs (push validation, review workflow scans, adoption state), so they stay, with a purpose that says so. Which decision each serves: `record-provenance-for-adoptions` and `skills-portable-across-harnesses` come from their archived changes (DECK-0018 for the second), `model-identity-on-commits` and `commits-carry-model-identity` from the skeleton's authorship contract (DECK-0013 names the local checks), `blocking-scan-on-every-review` and `changes-require-stated-specs` from the review workflow security work that predates records.

The repository MUST keep these rules:

- A canonical spec's H1 MUST be `<Directory Name> Specification` and its Purpose MUST be written for that capability.
- A rule MUST live in one canonical spec, and another spec MUST point at it.

## Consequences

- `rune spec archive` still writes `TBD` as a purpose. Until the cli writes one from the proposal, the archiving change replaces it by hand.
- Canonical specs carry no frontmatter, so the decision link lives in this record and in the ADRs that name them. The spec file holds no link.
