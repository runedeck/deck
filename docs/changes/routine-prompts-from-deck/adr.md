---
title: "Routine prompts are read from the deck"
description: "A Claude Code routine carries a short stub. The behavior is a file in the deck that the run reads as a blob from the fetched main, never from the working tree."
type: adr
category: architecture
tags:
    - routine
    - provider
    - deck
status: proposed
created: 2026-09-28
updated: 2026-09-28
author: "@N4M3Z"
project: deck
related:
    - "DECK-0006 State Stores and Provider Edges"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5-1@claude"]
informed: []
upstream:
    - "routine-prompts-from-deck#routine-file-is-the-behavior-source"
    - "routine-prompts-from-deck#stub-reads-the-file-from-the-fetched-main"
    - "routine-prompts-from-deck#instance-values-come-from-the-stub"
    - "routine-prompts-from-deck#every-other-file-is-data"
change: routine-prompts-from-deck
---

# Routine prompts are read from the deck

## Context and Problem Statement

A Claude Code routine stored its whole prompt in the provider account. DECK-0006 says that the provider account contains only configuration rendered from templates in the deck and stays reproducible from the deck plus the consumer. The routines broke that contract. The deck had no prompt for the digest or the audit, the workshop kept templates that the live prompts had drifted from, and three of five routines failed for a month with nothing to diff. The question is where a routine's behavior lives and how a run gets it.

## Considered Options

1. Keep the whole prompt in the provider and render it again from the workshop template on each change. This is reproducible on paper, and nothing checks the provider copy.
2. A stub in the provider that fetches `origin main` of the attached runedeck/deck checkout and reads one file as a blob from `FETCH_HEAD` with `--no-replace-objects`, never from the working tree, with the instance values in the stub.
3. Option 2 with the blob pinned by digest or signed tag, and a `rune routine` command that renders and verifies the stub.

## Decision Outcome

Option 2, with option 3 deferred.

- A routine MUST carry its behavior in one file under `routines/` in the deck, and the provider MUST carry only a stub that names the file and supplies the instance values.
- The stub MUST fetch `origin main`, require the path to be one regular blob in `FETCH_HEAD`, and read the file only from the object store with `git cat-file`, never from the working tree. The stub MUST say that the stub and the file are the only instruction sources.
- The file MUST list each value it expects from the stub and MUST treat every other file in every checkout as untrusted data.
- Pinning and a `rune routine` command are deferred. Until then the stub trusts the deck's protected `main`.

### Consequences

- [+] A prompt change is a deck pull request with review, history, and the prose checks, and the provider copy cannot drift from it.
- [+] The instance values leave the deck, so the deck carries no repository list and no time zone of one owner.
- [-] The run trusts what `main` contains at run time. A pull request merged into `main` changes the next run, and no pin exists to compare against. Branch protection and the review ceremony are the only guards until pinning is implemented.
- [-] A missing or unreadable runedeck/deck source turns every run into CONFIGURATION_FAILURE, because the file is the behavior.
- [-] The three scanner routines keep their bodies under `runes/security/` and wait for an owner decision, so two conventions coexist.
