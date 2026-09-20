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
updated: 2026-09-20
author: "@N4M3Z"
project: deck
related: []
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5-1"]
informed: []
upstream: []
change: architecture-decision-records
---

# Adopt Architecture Decision Records

## Context and Problem Statement

Decisions are made in conversations, threads, and commit messages. None of those is structured or durable. As a system grows, the reason for a structural choice becomes hard to recover. People and models then propose changes that contradict an earlier decision without knowing it. A model session also loses its reasoning at context compaction, so a decision must live outside the session.

## Decision Drivers

- An accepted decision must not be contradicted silently.
- Decision history must survive a move between repositories and tools, which commit messages do not.
- A record must be readable by a person, a model, and a note tool without conversion (CORE-0001 Markdown as System Language).

## Considered Options

1. Commit messages only. They are searchable, and they have no structure and no status.
2. A Decisions section inside project documents. It keeps context close, and it has no schema and grows without limit.
3. One Markdown file for each decision in `docs/decisions/`, with frontmatter, a status, and a numbered filename.

## Decision Outcome

Option 3. A decision with alternatives MUST be one record in `docs/decisions/`. A record MUST carry a status from proposed to accepted to superseded. The directory schema MUST validate the record shape.

## Consequences

- One directory listing shows every decision.
- The status field makes a contradiction of an accepted decision visible at review.
- Each record costs authoring time. A change that weighed no alternative still writes a short record, because the record states what the change wants.

## More Information

- [Documenting Architecture Decisions][NYGARD]
- [MADR][MADR]

[NYGARD]: https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions "Michael Nygard, Documenting Architecture Decisions, 2011"
[MADR]: https://adr.github.io/madr/ "Markdown Architectural Decision Records"
