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
updated: 2026-10-19
author: "@N4M3Z"
project: deck
related:
    - "DECK-0012 Consumer Ceremony Synchronization"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5-1@claude"]
informed: []
upstream: []
change: all-checks-before-push
---

# Local Checks Before Publication

## Context and Problem Statement

Every runedeck *[repository][REPOSITORY]* declares its checks in `.pre-commit-config.yaml`. Continuous integration runs that file with every tool required. The checked push hook replays the file in an isolated checkout before `jj git push`. A session ran a hand-picked subset by hand, reported it as clean, and met the full set only at push time. On 2026-09-14 two pushes stopped while the owner waited at the signing key. One stopped on a `typos` finding in an adopted *[decision record][DECISIONRECORD]*, the other on a base *[change][CHANGE]* with no proposal. The checks were right. The procedure ran them last instead of first.

## Decision Drivers

- The [repository][REPOSITORY] declares the check set once. A second, hand-picked list drifts from it.
- The owner's presence at the key is the scarce step. Nothing that can fail belongs after that step starts.
- A skipped tool has to fail instead of passing silently.

## Considered Options

1. A *[skill][SKILL]* that mandates the commit stage after each edit batch, the push stage on the frozen head, and a receipt for each stage. The same mandate then becomes a *[rule][RULE]* and a specification *[requirement][REQUIREMENT]* in the cli and the skeleton.
2. Rely on the push hook and continuous integration alone.
3. Run the checks only at push time, as today, and tolerate the wait.

## Decision Outcome

Option 1: the [skill][SKILL] now, with the [rule][RULE] and the specifications to come later.

The ContinuousIntegration [skill][SKILL] runs `REQUIRE_GATES=1 make validate` after every edit batch. It runs `REQUIRE_GATES=1 bash .githooks/jj-push -b <bookmark> --dry-run` on the frozen head. Both commands use the [repository][REPOSITORY]'s configuration and require every tool. Each stage writes one log that ends with the check's own exit status, beside the id of the candidate commit. The session fixes a finding and restarts the sequence. The signing step comes last.

Option 2 finds the same defects, one push later, with the owner waiting. Option 3 is the state this decision replaces.

### Consequences

- [-] A session spends a few minutes per edit batch on checks it would otherwise meet once at the end. In return, the push arrives at the key without a validation stop.
- [+] The [skill][SKILL] names `make validate` and the checked push hook. In a [repository][REPOSITORY] without either, the session calls `prek` directly, and the [skill][SKILL] gives those calls too.
- [-] The mandate lives only in the [skill][SKILL] until the [rule][RULE] and the cli and skeleton specifications state it.

## More Information

- Rewritten on 2026-10-19 in the plain spoken register. The decision is unchanged.

[REPOSITORY]: ../specs/glossary/repository.md
[DECISIONRECORD]: ../specs/glossary/decision-record.md
[CHANGE]: ../specs/glossary/change.md
[SKILL]: ../specs/glossary/skill.md
[RULE]: ../specs/glossary/rule.md
[REQUIREMENT]: ../specs/glossary/requirement.md
