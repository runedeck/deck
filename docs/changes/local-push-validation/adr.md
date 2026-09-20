---
title: Validate each push locally before publication
description: A push checks only the target it names, in a disposable checkout, before anything reaches the remote.
type: adr
category: architecture
tags:
    - runedeck
    - ceremony
status: proposed
created: 2026-09-20
author: "@N4M3Z"
project: runedeck
related:
    - DECK-0013 Local Checks Before Publication
change: local-push-validation
---

# Validate each push locally before publication

## Context and Problem Statement

The push hook checked every diverged local head. One stale head in any workspace blocked every push from every workspace. The authorship check read `HEAD`, not the outgoing range, so a bad identity failed only in CI and needed a history rewrite to repair.

## Considered Options

1. Keep the full sweep and require a clean estate before any push.
2. Check only the named target, in a disposable checkout that holds exactly that commit.
3. Drop the local hook and rely on CI.

## Decision Outcome

Option 2. The hook MUST run the pre-push checks against the named bookmark, change, or revision only. The bookmark path MUST use a disposable Git checkout so unrelated workspace content never enters validation. The authorship check MUST read the outgoing range. A bare push with no target keeps the full sweep, because that is what `jj git push` sends.

## Consequences

- A stale head in another workspace no longer blocks a push. It is reported by `rune doctor` instead.
- A bad identity fails locally as an amend, not in CI as a rewrite.
- The disposable checkout costs one clone per bookmark push.
