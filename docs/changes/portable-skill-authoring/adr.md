---
title: "Keep shared skill procedures independent of harness syntax"
description: "Align shared skill instructions and rules with layered validation."
type: adr
category: deck
tags: [skills, portability, authoring]
status: proposed
created: 2026-09-11
updated: 2026-09-11
author: "@N4M3Z"
project: runedeck
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["gpt-6-astra"]
informed: []
upstream: []
---

# Keep shared skill procedures independent of harness syntax

## Context and Problem Statement

The generic layer cannot provide consistent instructions when it requires tools from a particular harness.
The authoring guide must enforce the same boundary that the validator checks.

This ADR remains an unnumbered proposal pending maintainer review.

## Considered Options

1. Treating native commands as harmless text leaves their execution meaning unclear.
2. Suppressing their findings would preserve the contradiction between the authoring guide and the validator.
3. Duplicating all workflow text would create multiple places to maintain the same procedure.

## Decision Outcome

Use portable capability instructions in generic entrypoints and companions.
Keep native scopes and procedures in explicit harness entrypoint variants.
Require the layer gate before declaring authoring compliance.
Preserve native evidence as a separate acceptance condition.

## Consequences

- Shared instructions remain usable without a fixed harness tool catalog.
- Provider-specific metadata stays with its provider.
- The change requires no new assembly mechanism and grants no deployment or approval authority.
