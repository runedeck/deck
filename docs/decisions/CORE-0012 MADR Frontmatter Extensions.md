---
title: "MADR Frontmatter Extensions"
description: "Records add accountability, provenance, and change-link fields to the structured MADR frontmatter, written as bare field names."
type: adr
category: process
tags:
    - adr
    - process
    - frontmatter
status: accepted
created: 2026-03-30
updated: 2026-09-20
author: "@N4M3Z"
project: deck
related:
    - "CORE-0011 ADR Template Choice"
    - "CORE-0002 Metadata Inside Files"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5-1"]
informed: []
upstream: []
change: architecture-decision-records
---

# MADR Frontmatter Extensions

## Context and Problem Statement

[CORE-0011](CORE-0011 ADR Template Choice.md) adopts structured MADR. Its frontmatter does not say who approves a decision, where an adapted decision came from, or which change delivered it. Structured MADR permits added fields with an `x-` prefix.

## Considered Options

1. No added fields. Accountability and provenance stay in the body as prose, where no check reads them.
2. Prefixed fields such as `x-responsible`. Upstream validators accept them, and every record becomes harder to read.
3. Bare field names, validated by the deck's own schema.

## Decision Outcome

Option 3. A record MUST carry these fields, and an empty list is a statement, never an omission:

| Field | Type | Meaning |
|---|---|---|
| `responsible` | list | who does the work |
| `accountable` | list | who approves the decision |
| `consulted` | list | whose input was used, people and models |
| `informed` | list | who is told the outcome |
| `upstream` | list | sources the decision was adapted from |
| `related` | list | neighbor records by id and title |
| `change` | string or list | the change id, or ids, that delivered the decision |

A record MAY carry more fields when they do not conflict with these. A check MUST NOT reject an unknown field. The frontmatter MUST be enough to rebuild the record's location: `type`, `project`, and the id in the title give the path.

## Consequences

- The deck's records do not validate against the upstream structured MADR schema without a mapping, because the names have no prefix.
- One schema file in the deck owns the field list, so a field change is one edit.
- The `change` field makes the link from a record to its change a fact a check can read.
