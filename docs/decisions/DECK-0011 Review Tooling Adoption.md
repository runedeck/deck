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
updated: 2026-10-19
author: "@N4M3Z"
project: deck
related:
    - "DECK-0005 Artifact Lifecycle and Evidence Tokens"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5@claude"]
informed: []
upstream: []
change: review-tooling
---

# Review Tooling Adoption

## Context and Problem Statement

Seer, the review bot, keeps every review semantic in bespoke workflow shell and Python. Plumbing that widely used packages already standardize still costs custom lines. That plumbing posts findings inline, drives the API (application programming interface), provisions labels, and updates a status comment. Every finding in the *[review funnel][REVIEWFUNNEL]* comes from a hosted vendor or from the paid correctness *[agentic review lane][AGENTICREVIEWLANE]*.
The goal is a small stack. Custom lines cover only the ceremony. The ceremony pins the instructions, splits the identity that writes from the identity that approves, and binds the verdict to a head. Everything else comes from maintained open source.

## Decision Drivers

- Fewer custom lines: each bespoke segment is a maintenance and audit liability
- Vendor independence: at least one [agentic review lane][AGENTICREVIEWLANE] must run on open code against a *[model][MODEL]* the organization picks
- Maturity: the candidate ranking uses stars, age, release cadence, and open issues, measured on 2026-09-01 ([candidate table][TABLE])

## Considered Options

1. **Keep the bespoke stack**: no new dependency, and every segment remains hand-written
2. **Hosted vendors only**: Cursor, Macroscope, and CodeRabbit supply findings, and the funnel adjudicates
3. **Adopt the open-source set**: standard packages do the plumbing, one lane runs on open code, and the ceremony remains custom

## Decision Outcome

Option 3. The [review funnel][REVIEWFUNNEL] MUST use a maintained open-source package for plumbing. It MUST keep custom code only for the ceremony. The ceremony pins the instructions, splits the identity that writes from the identity that approves, and binds the verdict to a head. At least one lane MUST run on open code against a [model][MODEL] the organization picks. Five tools follow, and each has one role:

- [reviewdog][REVIEWDOG] posts findings as review comments from the rdjsonl file the adjudicator writes. Seer pull request #35 adopted it.
- [github-script][GHSCRIPT] drives the GitHub API where shell would parse JSON by hand (already adopted).
- [labeler][LABELER] provisions one label per lane from the *[lane table][LANETABLE]* (already adopted for path labels).
- [create-or-update-comment][UPSERT] with [find-comment][FIND] updates or creates every workflow-authored status comment by its header marker.
- [PR-Agent][PRAGENT] runs as the pr-agent lane in command mode from a pinned image. Each summon makes one `review` call. The findings post under the workflow token, and the adjudicator treats them like every other lane's.

PR-Agent runs in command mode and never in its GitHub Action mode. The Action reviews on pull request events, and the ceremony allows a lane to run only on a maintainer's label. The pr-agent lane needs one organization secret, a [model][MODEL] API key. When the key is absent, it stops with a clear fault.

### Consequences

- [+] The comment publish paths, the lane waits, and the findings posting are no longer custom code
- [+] The funnel keeps a reviewer that runs on open code against a [model][MODEL] the organization chooses
- [-] One more organization secret and one more container image to pin and refresh
- [-] The *[change][CHANGE]* is in the skeleton *[repository][REPOSITORY]* as `review-tooling`, so this record cites a [change][CHANGE] that this [repository][REPOSITORY] does not contain.
- [-] A fourth lane lengthens the funnel by one [model][MODEL] call, and `skip:pr-agent` stands it down

## More Information

- Rewritten on 2026-10-19 in the plain spoken register. The decision is unchanged.

[TABLE]: https://github.com/runedeck/skeleton/blob/main/docs/changes/review-tooling/design.md
[REVIEWDOG]: https://github.com/reviewdog/reviewdog
[GHSCRIPT]: https://github.com/actions/github-script
[LABELER]: https://github.com/actions/labeler
[UPSERT]: https://github.com/peter-evans/create-or-update-comment
[FIND]: https://github.com/peter-evans/find-comment
[PRAGENT]: https://github.com/The-PR-Agent/pr-agent
[REVIEWFUNNEL]: ../specs/glossary/review-funnel.md
[AGENTICREVIEWLANE]: ../specs/glossary/agentic-review-lane.md
[MODEL]: ../specs/glossary/model.md
[LANETABLE]: ../specs/glossary/lane-table.md
[CHANGE]: ../specs/glossary/change.md
[REPOSITORY]: ../specs/glossary/repository.md
