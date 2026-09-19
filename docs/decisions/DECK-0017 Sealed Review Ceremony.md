---
title: "Sealed Review Ceremony"
description: "The owner's key enters at open and merge, not only at tags; a controller-owned ledger disposes every thread; paid review is triaged and budgeted; no vendor lane is required"
type: adr
category: architecture
tags:
    - architecture
    - review
    - signing
status: proposed
created: 2026-09-19
updated: 2026-09-19
author: "@N4M3Z"
project: deck
related:
    - "DECK-0008 Idea-to-Merge Flywheel"
    - "DECK-0011 Review Tooling Adoption"
    - "CORE-0016 Adversarial Review over Councils"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5-1", "gpt-6-astra", "grok-4.6", "lumo-max"]
informed: []
upstream:
    - "https://github.com/runedeck/skeleton/tree/main/docs/specs/review-ceremony"
---

# Sealed Review Ceremony

## Context and Problem Statement

The skeleton's review ceremony held that the owner's hardware key enters at tags, not merges, and
that merging demands no signature ritual beyond the platform's own. The cli's `rune sign`
proposal cites a "CORE-0013 Attribution Signing and Merge Ceremony" for that rule. No decision of
that title exists in the deck, so the choice was recorded only in the skeleton spec. A read of
21 pull requests across deck and cli on 2026-09-19 found the loop open at both ends: free-lane
findings sat unanswered under clean adjudicator verdicts, three pull requests merged with the
loop open, one before any lane reported, paid rounds had no bound, and the owner's stored login
was the only thing standing between an agent and a pull request in the owner's name.

## Decision Drivers

- A pull request in the owner's name is an attestation, and an attestation needs the key
- Every finding from every lane must end in a recorded disposition, or the verdict is a fault
- Paid review must be bounded per work item and never started by an agent
- Every vendor lane can be switched off on any day, so none may be load-bearing
- Merging with the loop open must be impossible by ruleset, not by habit

## Considered Options

1. **Keep the tag-only key and the owner click.** Cheapest. Leaves impersonation through the
   stored login open and leaves the loop closable by habit only.
2. **One merge-seal only.** Closes the merge, leaves opening a pull request in the owner's name
   unattested.
3. **Two seals and a controller ledger.** A draft opens under the app identity on the first
   accepted push. `rune sign open` signs an open-seal bound to repository, base, tree, and a
   single-use nonce and flips the draft ready. Ready invites the controller's triage. The paid
   lane judges a pinned `(reviewed_sha, generation)` under three rounds per work item and must
   dispose of every ledger thread. `rune sign next` signs a merge-seal as an empty child of
   `reviewed_sha`. The ruleset requires both seals and the controller's check.

## Decision Outcome

Option 3, as three adversarial passes bound it: astra, grok, and lumo on the first draft, astra
and grok on the change documents, and three agents on trust boundaries, rollout, and provider
behavior on the final design. The skeleton specs `review-ceremony`, `review-requests`, `review-lanes`, and
`release-ceremony` are edited in place to state it. The glossary carries `ledger`,
`open-seal`, `merge-seal`, `controller`, and `work item`. The spec history is rewritten at the
owner's instruction. This record is the trail.

Bound into the design and now requirements:

- The open-seal binds one pull request through a nonce.
- The merge-seal never moves `reviewed_sha`.
- The ledger is the controller's, built from the API by lane login, with a status per expected
  lane and a generation that any change increments.
- `KEYS`, the verifier, and the lane table come from the protected branch.
- Agents push branches after the prek pipeline and never open, ready, close, merge, label,
  resolve, or comment.
- The session agent may invoke `rune sign`. The touch is the owner's.
- `free lanes only` is a recorded coverage state and a valid queue entry.
- Outside pull requests enter through `rune sign adopt`.

## Consequences

- Two key touches per pull request, each authorizing a displayed action
- The stored owner login can open a pull request, and that pull request cannot merge
- A lane that vanishes leaves a recorded status, not a hole
- `rune sign open`, `adopt`, `owner-seal`, the controller ledger, and the triage do not exist
  yet. Until they do, the deck's rules describe a ceremony the tooling cannot enforce, and this
  record stays proposed
- The rune-sign proposal's citation of a CORE-0013 signing decision is stale and points here

## Audit

- 2026-09-19: created, superseding the tag-only rule in the skeleton `release-ceremony` spec.
  The route to enforcement is the workshop's `docs/specs/2026-09-19-review-loop-plan.md`.
- 2026-09-19: the ledger's carrier fixed. The full ledger is a workflow artifact. Its public
  record is a check run named `ledger` on `reviewed_sha` under the reviewing app, whose first
  line names the artifact, its sha256, the generation, and the pull request. Only the creating
  app can edit a check run, so the line is the controller's word without a comment or a commit.
  The merge-seal binds the digest, so a rebuilt ledger at the same generation unseals. The
  reviewing app carries `checks: write` for it.
