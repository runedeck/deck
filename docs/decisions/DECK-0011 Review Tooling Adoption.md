---
title: Review Tooling Adoption
description: The review funnel adopts five open-source tools for findings, API scripting, labels, status comments, and an open-source reviewer lane, so custom lines shrink to the ceremony itself
type: adr
category: process
tags:
    - process
    - review
    - tooling
status: accepted
created: 2026-09-01
updated: 2026-09-20
author: "@N4M3Z"
project: deck
related:
    - "DECK-0005 Artifact Lifecycle and Evidence Tokens"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5"]
informed: []
upstream: []
change: review-tooling
---

# Review Tooling Adoption

## Context and Problem Statement

The seer review funnel holds every review semantic in bespoke workflow shell and Python. Plumbing that widely used packages already standardize still costs custom lines: posting findings inline, driving the API, provisioning labels, updating a status comment. Every finding in the funnel comes from a hosted vendor or the paid correctness lane. The goal is a small stack. Custom lines cover only the ceremony: instruction pinning, the write and approve identity split, the head-bound verdict. Everything else comes from maintained open source.

## Decision Drivers

- Fewer custom lines: each bespoke segment is a maintenance and audit liability
- Vendor independence: at least one reviewer lane must run on open code against a model the org picks
- Maturity: the candidate ranking uses stars, age, release cadence, and open issues, measured on 2026-09-01 ([candidate table][TABLE])

## Considered Options

1. **Keep the bespoke stack**: no new dependencies, every segment stays hand-written
2. **Hosted vendors only**: Cursor, Macroscope, and CodeRabbit supply findings, and the funnel adjudicates
3. **Adopt the open-source set**: standard packages for plumbing, one open-source reviewer lane, the ceremony stays custom

## Decision Outcome

Option 3. The review funnel MUST use a maintained open-source package for plumbing, and MUST keep custom code only for the ceremony: instruction pinning, the split between the identity that writes and the identity that approves, and the verdict bound to a head. At least one reviewer lane MUST run on open code against a model the organization picks. Five tools, one role each:

- [reviewdog][REVIEWDOG] posts findings as review comments from the rdjsonl the adjudicator writes. Seer PR #35 adopted it.
- [github-script][GHSCRIPT] drives the GitHub API where shell would parse JSON by hand (already adopted).
- [labeler][LABELER] provisions the per-lane label set from the lane table (already adopted for path labels).
- [create-or-update-comment][UPSERT] with [find-comment][FIND] upserts every workflow-authored status comment by header marker.
- [PR-Agent][PRAGENT] runs as the pr-agent lane in command mode from a pinned image: one `review` call per summon, findings posted under the workflow token, adjudicated like every other lane.

PR-Agent runs in command mode, never in its GitHub Action mode. The Action reviews on pull request events, and the ceremony allows a lane to run only on a maintainer's label. The lane needs one org secret, a model API key. When the key is absent, the lane stops with a clear fault.

## Consequences

- The comment publish paths, the lane waits, and the findings posting stop being custom code
- The funnel keeps a reviewer that runs on open code against a model the org chooses
- One more org secret and one more container image to pin and refresh
- The change lives in the skeleton repository as `review-tooling`, so this record names a change that the deck does not hold.
- A fourth lane lengthens the funnel by one model call, and `skip:pr-agent` stands it down

[TABLE]: https://github.com/runedeck/skeleton/blob/main/docs/changes/review-tooling/design.md
[REVIEWDOG]: https://github.com/reviewdog/reviewdog
[GHSCRIPT]: https://github.com/actions/github-script
[LABELER]: https://github.com/actions/labeler
[UPSERT]: https://github.com/peter-evans/create-or-update-comment
[FIND]: https://github.com/peter-evans/find-comment
[PRAGENT]: https://github.com/The-PR-Agent/pr-agent
