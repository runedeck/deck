---
title: "MADR Frontmatter Extensions"
description: "Records add accountability, provenance, and change-link fields to the structured MADR frontmatter. Each field has a bare canonical name and a compliant x-rune- long form."
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

[CORE-0011](CORE-0011 ADR Template Choice.md) adopts structured MADR. Its frontmatter does not say who approves a decision, where an adapted decision came from, or which change delivered it. Structured MADR permits added fields when they carry an `x-` prefix, and a strict validator rejects an added field without one.

## Considered Options

1. No added fields. Accountability and provenance stay in the body as prose, where no check reads them.
2. Prefixed fields only, such as `x-rune-responsible`. A strict validator accepts them, and every record becomes harder to read.
3. Bare field names only. Records read well, and a strict structured MADR validator rejects them.
4. Both forms: a bare canonical name and a compliant `x-rune-` long form for each added field.

## Decision Outcome

Option 4. The bare name is canonical, and records in the deck use it. The long form exists so that a record can pass a strict structured MADR validator without a mapping step.

| Canonical | Long form | Type | Meaning |
|---|---|---|---|
| `responsible` | `x-rune-responsible` | list | who does the work |
| `accountable` | `x-rune-accountable` | list | who approves the decision |
| `consulted` | `x-rune-consulted` | list | whose input was used, people and models |
| `informed` | `x-rune-informed` | list | who is told the outcome |
| `upstream` | `x-rune-upstream` | list | sources the decision was adapted from |
| `related` | `x-rune-related` | list | neighbor records by id and title |
| `change` | `x-rune-change` | string or list | the change id, or ids, that delivered the decision |

- A record MUST carry `responsible`, `accountable`, and `upstream`, each in one form. An empty list is a statement, never an omission.
- A record MUST NOT set both forms of one field.
- `x-rune-` is the only accepted prefix. A field with another `x-` prefix MUST fail the check.
- A record MAY carry other fields without an `x-` prefix when they do not conflict with these. A check MUST NOT reject them.
- The frontmatter MUST be enough to rebuild the record's location: `type`, `project`, and the id in the title give the path.

`scripts/check-decision-fields` enforces the first three rules. The directory schema marks the three required fields optional, because a schema cannot state that either form satisfies a field.

## Consequences

- A record written with bare names does not pass a strict structured MADR validator. A record written with the long form does.
- Two forms for one field are two ways to write the same fact. The check forbids both at once, and the deck's own records stay on the bare form.
- The `change` field makes the link from a record to its change a fact a check can read.
- The public format home states the same rule in its README, and its JSON Schema still requires the bare names. A long-form record fails that schema until the home changes it.
