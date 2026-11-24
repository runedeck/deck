---
title: Adversarial Review over Councils
description: Refutation against the source replaces consensus panels as the verification check, and cross-provider fan-out stays a research instrument
type: adr
category: architecture
tags:
    - architecture
    - review
    - agents
status: accepted
created: 2026-08-27
updated: 2026-10-19
author: "@N4M3Z"
project: deck
related:
    - "CORE-0014 No Performance Personas"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: []
informed: []
upstream: []
change: economy-measure-context-efficiency
---

# Adversarial Review over Councils

## Context and Problem Statement

The council pattern sends one question to several providers and combines the answers by agreement. A consensus panel averages independent guesses and rewards fluent agreement, so a plausible but wrong finding can survive on style. Verification needs a mechanism that kills a wrong finding on evidence.

## Considered Options

1. The owner keeps councils as the verification mechanism.
2. The owner replaces councils with an adversarial reviewer that tries to refute each finding.

## Decision Outcome

Chosen option: adversarial review.

- An adversarial reviewer attacks one claim against the source.
- The reviewer accepts the claim only after it completes the review and fails to find a counterexample.
- A timeout, a crash, a cancellation, or a missing result is a reviewer fault. A reviewer fault never accepts the claim.
- A consensus council never admits or refuses a decision.
- The owner keeps cross-provider fan-out for a research question that wants breadth.
- The AdversarialReviewer *[agent][AGENT]* owns refutation.

### Consequences

- [+] A plausible but wrong finding dies on evidence instead of surviving on agreement.
- [+] The reviewer spends its effort on the claims that matter.
- [-] One reviewer can miss a failure mode that a diverse panel would catch, so a hard claim may get several adversarial reviewers with different angles. It never gets a vote.

## More Information

- Rewritten on 2026-10-19 in the plain spoken register. The decision is unchanged.

[AGENT]: ../specs/glossary/agent.md
