---
title: "Sealed Review Ceremony"
description: "The owner's key enters at open and merge, not only at tags; a controller-owned ledger disposes every thread; paid review is triaged and budgeted; no vendor lane is required"
type: adr
category: architecture
tags:
    - architecture
    - review
    - signing
status: accepted
created: 2026-09-19
updated: 2026-10-19
author: "@N4M3Z"
project: deck
related:
    - "DECK-0008 Idea-to-Merge Flywheel"
    - "DECK-0011 Review Tooling Adoption"
    - "CORE-0016 Adversarial Review over Councils"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5-1@claude", "gpt-6-astra@codex", "grok-4.6@grok", "lumo-max@opencode"]
informed: []
upstream:
    - "https://github.com/runedeck/skeleton/tree/main/docs/specs/review-ceremony"
---

# Sealed Review Ceremony

## Context and Problem Statement

The skeleton's review ceremony said that the owner's hardware key enters at tags and not at merges. It also said that merging demands no signature ritual beyond the platform's own. The cli's `rune sign` proposal cites a "CORE-0013 Attribution Signing and Merge Ceremony" for that policy. No decision of that title exists in the *[repository][REPOSITORY]*, so only the skeleton specification recorded the choice.

A read of 21 pull requests across the [repository][REPOSITORY] and the cli clone on 2026-09-19 found the loop open at both ends. Findings from a free *[agentic review lane][AGENTICREVIEWLANE]* sat unanswered under clean adjudicator verdicts. Three pull requests merged with the loop open, one before any [lane][AGENTICREVIEWLANE] reported. Paid rounds had no bound. The owner's stored login was the only thing between a *[harness][HARNESS]* and a pull request in the owner's name.

## Decision Drivers

- A pull request in the owner's name is a statement by the owner, and such a statement needs the key
- Every finding from every lane must end in a recorded disposition, or the verdict is a fault
- Paid review must have a bound per *[work item][WORKITEM]*, and a [harness][HARNESS] must never start it
- A vendor can switch off its lane on any day, so no lane may be load-bearing
- The ruleset, not habit, must make merging with the loop open impossible

## Considered Options

1. **Keep the tag-only key and the owner click.** It is the cheapest. It leaves impersonation through the stored login open, and only habit closes the loop.
2. **One *[merge seal][MERGESEAL]* only.** It closes the merge. Opening a pull request in the owner's name stays unattested.
3. **Two seals and a controller ledger**, where a draft opens under the app identity on the first accepted push. The *[signer][SIGNER]* (`rune sign open`) signs an *[open seal][OPENSEAL]* bound to the [repository][REPOSITORY], the base, the tree, and a single-use nonce. The [signer][SIGNER] then flips the draft to ready, which invites the triage of the *[review controller][REVIEWCONTROLLER]*. The paid lane judges a pinned `(reviewed_sha, generation)` under three rounds per [work item][WORKITEM], and it must dispose of every ledger thread. The [signer][SIGNER] (`rune sign next`) signs a [merge seal][MERGESEAL] as an empty child of `reviewed_sha`. The ruleset requires both seals and the controller's check.

## Decision Outcome

Option 3, as three adversarial passes bound it. The *[models][MODEL]* astra, grok, and lumo attacked the first draft. The [models][MODEL] astra and grok attacked the documents of the *[change][CHANGE]*. Three [harness][HARNESS] sessions attacked the final design on trust boundaries, rollout, and provider behavior.

The skeleton specifications `review-ceremony`, `review-requests`, `review-lanes`, and `release-ceremony` now state it, edited in place. The glossary defines `ledger`, `open-seal`, `merge-seal`, `controller`, and `work item`. The owner instructed a rewrite of the specification history. This record is the trail.

The design binds these points, and they are now requirements:

- The [open seal][OPENSEAL] binds one pull request through a nonce.
- The [merge seal][MERGESEAL] never moves `reviewed_sha`.
- The ledger belongs to the controller. The controller builds it from the API (application programming interface) by lane login. It records a state for each expected lane and a generation that any update increments.
- `KEYS`, the verifier, and the *[lane table][LANETABLE]* come from the protected branch.
- A [harness][HARNESS] pushes a branch after the prek pipeline. It never opens, readies, closes, merges, labels, resolves, or comments.
- The [harness][HARNESS] session that the owner works in may invoke `rune sign`. The touch is the owner's.
- `free lanes only` is a recorded coverage state and a valid queue entry.
- An outside pull request enters through `rune sign adopt`.

### Consequences

- [+] The owner touches the key twice per pull request, and each touch authorizes a displayed action
- [+] The stored owner login can open a pull request, and that pull request cannot merge
- [+] A lane that vanishes leaves a recorded state instead of a hole
- [-] `rune sign open`, `adopt`, `owner-seal`, the controller ledger, and the triage do not exist yet. Until they do, the *[rules][RULE]* of the *[deck][DECK]* describe a ceremony the tooling cannot enforce
- [-] The rune-sign proposal's citation of a CORE-0013 signing decision is stale and points here

## More Information

- Rewritten on 2026-10-19 in the plain spoken register. The decision is unchanged.

## Audit

- 2026-09-19: the author created this record, which supersedes the tag-only policy in the skeleton `release-ceremony` specification. The route to enforcement is the workshop's `docs/specs/2026-09-19-review-loop-plan.md`.
- 2026-09-19: the author fixed the ledger's carrier. The full ledger is a workflow artifact. Its public record is a check run named `ledger` on `reviewed_sha` under the reviewing app, which has the `checks: write` permission for it. The first line of that check run names the artifact, its sha256, the generation, and the pull request. Only the creating app can edit a check run, so the line is the controller's word without a comment or a commit. The [merge seal][MERGESEAL] binds the digest, so a rebuilt ledger at the same generation unseals.
- 2026-09-23: the owner accepted the record. The decision stands while the tooling is pending. A record under `docs/decisions/` is never proposed.

[REPOSITORY]: ../specs/glossary/repository.md
[AGENTICREVIEWLANE]: ../specs/glossary/agentic-review-lane.md
[SIGNER]: ../specs/glossary/signer.md
[REVIEWCONTROLLER]: ../specs/glossary/review-controller.md
[LANETABLE]: ../specs/glossary/lane-table.md
[DECK]: ../specs/glossary/deck.md
[WORKITEM]: ../specs/glossary/work-item.md
[MERGESEAL]: ../specs/glossary/merge-seal.md
[OPENSEAL]: ../specs/glossary/open-seal.md
[HARNESS]: ../specs/glossary/harness.md
[MODEL]: ../specs/glossary/model.md
[CHANGE]: ../specs/glossary/change.md
[RULE]: ../specs/glossary/rule.md
