---
title: "Scanner routines run a deterministic detector from the deck"
description: "A scanner routine streams versioned detection code from the deck object store, takes its findings, ids, and status as printed, and reports finding status apart from scan health. The GitHub Exposure routine is retired."
type: adr
category: architecture
tags:
    - routine
    - security
    - deck
status: proposed
created: 2026-10-02
updated: 2026-10-02
author: "@N4M3Z"
project: deck
related:
    - "DECK-0006 State Stores and Provider Edges"
    - "Routine prompts are read from the deck"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5-1@claude", "gpt-6-astra@codex", "lumo-max@opencode"]
informed: []
upstream:
    - "scanner-routines-from-deck#detector-decides-findings-and-status-in-code"
    - "scanner-routines-from-deck#finding-identity-hides-the-value"
    - "scanner-routines-from-deck#finding-status-is-separate-from-scan-health"
    - "scanner-routines-from-deck#acknowledgement-binds-to-a-commit"
    - "scanner-routines-from-deck#scanner-routines-stream-the-detector-from-the-deck"
    - "scanner-routines-from-deck#stub-reads-the-ref-in-policy-ref"
    - "scanner-routines-from-deck#github-exposure-routine-is-retired"
change: scanner-routines-from-deck
---

# Scanner routines run a deterministic detector from the deck

## Context and Problem Statement

Three scanner routines ran daily on the provider with full prompts that asked a model to enumerate every Git object, classify what it saw, and pick one status from a five-way list. The reports changed severity on unchanged evidence, every run was INCOMPLETE because the platform clone is shallow, and no report named a path, a line, or a commit to fix. The GitHub Exposure routine could not reach its subject at all: the provider proxy refuses GitHub paths outside an attached source. A council of two models reviewed the three prompts on 2026-10-02 and agreed on rework for the two scanners with a subject and retirement for the third. The question is what decides a finding and its status, and where that logic lives.

## Considered Options

1. Keep the prompts and ask the model to be consistent. Identical evidence still produces different ids and classifications, because no instruction makes a model deterministic.
2. Move the prompts to deck files under the routine stub model, and keep detection in the model. The prompt gains review and history, and the status still varies.
3. Option 2 plus a deterministic, versioned detector in the deck that the run streams from the object store. The detector decides findings, ids, and status. The model reviews, adds located items, and writes the report.
4. Option 3 with a pinned detector digest in the stub, and a runner that removes the GitHub write tools an attached source adds.

## Decision Outcome

Option 3, with option 4 deferred.

- A scanner routine MUST take every finding, id, count, finding status, and scan health from `routines/scripts/exposure_scan.py`, streamed from the deck `FETCH_HEAD` after an `ls-tree` mode check, and MUST NOT change them.
- A finding id MUST be the rule code plus ten hex digits of the SHA-256 of the value. The value MUST NOT leave the detector: a matching path segment and the context line are redacted in the detector. KNOWN_FINDINGS in the private stub MUST be `<id> <commit>` pairs: an occurrence is known only when its object is reachable from the acknowledged commit, and the same value in any other object is new. Known means acknowledged, not fixed.
- The run MUST stream the detector into `python3 -I -` from a directory outside every checkout, so a tracked module cannot shadow the standard library, and MUST NOT read repository content by another means.
- Finding status and scan health MUST be separate values. The Dotfiles Scanner MUST fetch the whole history of the branch, and a scanned history that stops at a shallow boundary MUST make health INCOMPLETE.
- The stub MUST fetch the ref in POLICY_REF, default `main`, so the owner can test a branch before merge.
- Online Mentions MUST run weekly with identity-qualified queries and owner-reviewed exclusions.
- The GitHub Exposure routine is retired.

### Consequences

- [+] The same repository state yields the same ids and the same status on every run, and an acknowledgement suppresses a repeat alarm without hiding a replacement secret in the same file or the same secret in a new file.
- [-] The owner must re-acknowledge after each change that touches an acknowledged object, because the acknowledgement binds to the objects reachable from one commit.
- [+] A rule change is a deck pull request with tests, and the rules version in every report says which rules ran.
- [+] The owner gets a path, a line, a commit, and a blob id for each finding in the session, and a notification whose first line says whether to act.
- [-] Each run downloads the whole history of the scanned branch, so a repository with a long history makes the run slower.
- [-] The rules are regular expressions with placeholder filters. They miss a secret with no known format and flag some fixtures, and the model's review items are the only cover for personal data the rules cannot see.
- [-] A finding id is a plain digest prefix. An attacker with the private stub and a candidate value can confirm the value, so the stub stays private and the ids never enter the deck.
- [-] The stub still trusts `main` at run time, and an attached source adds GitHub write tools that the prompt alone forbids. Pinning and a runner that removes those tools are deferred.
- [-] Two conventions coexist until the ConfigureScanners overlap is resolved: the deck routine file and the older template under `runes/security/`.
