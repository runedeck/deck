---
title: Adversarial Review over Councils
description: Refutation against the source replaces consensus panels as the verification gate, and cross-provider fan-out stays a research instrument
type: adr
category: architecture
tags:
    - architecture
    - review
    - agents
status: proposed
created: 2026-08-27
updated: 2026-08-27
author: "@N4M3Z"
project: deck
related:
    - "CORE-0014 No Performance Personas"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: []
informed: []
---

# Adversarial Review over Councils

## Context and Problem Statement

The council pattern fans one question to several providers and synthesizes by agreement. A consensus panel averages independent guesses and rewards fluent agreement, so a plausible but wrong finding can survive on style. Verification needs a mechanism that kills wrong findings on evidence.

## Considered Options

1. Keep councils as the verification mechanism.
2. Replace councils with an adversarial reviewer that attempts to refute each finding.

## Decision Outcome

Chosen option: adversarial review.

- An adversarial reviewer attacks one claim against the source.
- The reviewer accepts the claim only after a completed review finds no counterexample.
- A timeout, crash, cancellation, or missing result is a reviewer fault. A reviewer fault never accepts the claim.
- A consensus council never gates a decision.
- Cross-provider fan-out stays available for research questions that want breadth.
- The AdversarialReviewer agent owns refutation.

### Consequences

- [+] Plausible but wrong findings die on evidence instead of surviving on agreement.
- [+] Verification cost concentrates on claims that matter.
- [-] A single reviewer can miss a failure mode a diverse panel would catch, so hard claims may get several adversarial lenses, never a vote.
