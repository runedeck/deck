---
title: "Local Checks Before Publication"
description: "A session runs the repository's own commit and push check stages locally and repeatedly, with every tool required, before it asks for a signature or a push"
type: adr
category: process
tags:
    - ceremony
    - checks
    - publication
status: accepted
created: 2026-09-14
updated: 2026-09-14
author: "@N4M3Z"
project: deck
related:
    - "DECK-0012 Consumer Ceremony Synchronization"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5-1"]
informed: []
upstream: []
change: enforce-local-checks
---

# Local Checks Before Publication

## Context and Problem Statement

Every runedeck repository declares its checks in `.pre-commit-config.yaml`. CI runs that file with every tool required, and the checked push hook replays it in an isolated checkout before `jj git push`. Sessions ran a hand-picked subset by hand, reported it as clean, and met the full set only at push time. On 2026-09-14 a `typos` finding in an adopted decision record and a base change with no proposal stopped two pushes while the owner waited at the signing key. The checks were right. The procedure ran them last instead of first.

## Decision Drivers

- The check set is declared once. A second, hand-picked list drifts from it.
- The owner's presence at the key is the scarce step. Nothing that can fail should run after it starts.
- A skipped tool must fail, not pass silently.

## Considered Options

1. A skill that mandates the commit stage after each edit batch, the push stage on the frozen head, and a receipt per stage. The same mandate follows as a rule and as a specification requirement in the cli and skeleton.
2. Rely on the push hook and CI alone.
3. Run the checks only at push time, as today, and tolerate the wait.

## Decision Outcome

Chosen option: the skill, with the rule and the specifications to follow.

ContinuousIntegration runs `REQUIRE_GATES=1 make validate` after every edit batch and `REQUIRE_GATES=1 bash .githooks/jj-push -b <bookmark> --dry-run` on the frozen head. Both use the repository's configuration and require every tool. Each stage writes one log that ends with the check's own exit status, beside the candidate commit id. A finding is fixed and the sequence restarts. The signing step comes last.

Option 2 finds the same defects, one push later, with the owner waiting. Option 3 is the state this decision replaces.

## Consequences

- A session spends a few minutes per edit batch on checks it would otherwise meet once at the end, and the push reaches the key without a validation stop.
- The skill names `make validate` and the checked push hook. A repository without either falls back to direct `prek` invocations, which the skill also gives.
- The mandate is skill-level until the rule and the cli and skeleton specifications carry it.
