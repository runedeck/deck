---
title: "Writing and conduct rules in core"
description: "The rules the owner runs from a deployed copy enter the deck as first-party content with the deployed text, and each stays until a bench run shows no effect."
type: adr
category: process
tags:
    - runedeck
    - rules
status: proposed
created: 2026-09-20
updated: 2026-09-20
author: "@N4M3Z"
project: deck
related:
    - "CORE-0013 Context Economy"
    - "DECK-0003 Three-Metric Verdict and Cross-Vendor Judging"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5-1", "gpt-6-astra"]
informed: []
upstream: []
change: writing-and-conduct-rules
---

# Writing and conduct rules in core

## Context and Problem Statement

The owner runs a set of short rules in every session: how to cite, how much to say, how to draw, how to name a scenario, how to scope one action. The deployed copies were the only complete source. The deck could not rebuild them on a fresh machine.

A review proposed to drop the rule against em-dashes, because a Vale rule already fails on them.

## Considered Options

1. Rewrite each rule before it enters the deck.
2. Enter each rule with the deployed text, and measure it afterwards.
3. Drop each rule that a linter already covers.

## Decision Outcome

Option 2. A rule that the owner runs MUST have its source in the deck with the deployed text. A short rule MUST stay when a linter checks the same property, because the rule steers the input and the linter checks the output. Each rule MUST get one bench run, and a rule with no measured effect MUST leave the default casts.

## Consequences

- The deployment is reproducible from the deck.
- Every session pays the tokens of rules that no bench has measured yet. The RuleShape warning stays on each until its verdict exists.
- A rule and a linter state one preference in two places. When the preference changes, both need the edit.
