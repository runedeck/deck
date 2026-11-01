---
title: "Adopt Architecture Decision Records"
description: "Each decision with alternatives is one Markdown record with frontmatter, a status lifecycle, and schema validation."
type: adr
category: process
tags:
    - adr
    - process
status: accepted
created: 2026-02-19
updated: 2026-10-19
author: "@N4M3Z"
project: deck
related: []
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5-1@claude"]
informed: []
upstream: []
change: keep-architecture-decision-records
---

# Adopt Architecture Decision Records

## Context and Problem Statement

People decide things in conversations, threads, and commit messages. None of those places gives a decision a structure or keeps it. As a system grows, the reason for a structural choice becomes hard to recover. A person or a *[model][MODEL]* then proposes a *[change][CHANGE]* that contradicts an earlier decision without knowing it. A [model][MODEL] session also loses its reasoning when the context compacts, so a decision must live outside the session.

## Decision Drivers

- A [change][CHANGE] must not contradict an accepted decision silently.
- The decision history must stay readable after a move between repositories and tools. Commit messages are lost in such a move.
- A person, a [model][MODEL], and a note tool must read a record without conversion ([CORE-0001 Markdown as System Language](CORE-0001%20Markdown%20as%20System%20Language.md)).

## Considered Options

1. Commit messages only. A person can search them, and they have no structure and no *[status][STATUS]*.
2. A Decisions section inside each project document. It keeps the context close, and it has no schema and grows without limit.
3. One Markdown file for each decision in `docs/decisions/`, with frontmatter, a [status][STATUS], and a numbered filename.

## Decision Outcome

Option 3. The author MUST write a decision with alternatives as one *[decision record][DECISIONRECORD]* in `docs/decisions/`. A record MUST state a [status][STATUS] that moves from proposed to accepted to superseded. The *[validator][VALIDATOR]* MUST check each record against the directory's *[structure schema][STRUCTURESCHEMA]*.

### Consequences

- [+] One listing of the directory shows every decision.
- [+] A reviewer sees from the [status][STATUS] field when a [change][CHANGE] contradicts an accepted decision.
- [-] Each record costs authoring time. A [change][CHANGE] that weighed no alternative still writes a short record, because the record states what the [change][CHANGE] is for.

## More Information

- [Documenting Architecture Decisions][NYGARD]
- [MADR][MADR]
- Rewritten on 2026-10-19 in the plain spoken register. The decision is unchanged.

[NYGARD]: https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions "Michael Nygard, Documenting Architecture Decisions, 2011"
[MADR]: https://adr.github.io/madr/ "Markdown Architectural Decision Records"
[MODEL]: ../specs/glossary/model.md
[DECISIONRECORD]: ../specs/glossary/decision-record.md
[STATUS]: ../specs/glossary/status.md
[VALIDATOR]: ../specs/glossary/validator.md
[STRUCTURESCHEMA]: ../specs/glossary/structure-schema.md
[CHANGE]: ../specs/glossary/change.md
