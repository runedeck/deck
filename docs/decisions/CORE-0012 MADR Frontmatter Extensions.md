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
updated: 2026-10-19
author: "@N4M3Z"
project: deck
related:
    - "CORE-0011 ADR Template Choice"
    - "CORE-0002 Metadata Inside Files"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5-1@claude"]
informed: []
upstream: []
change: keep-architecture-decision-records
---

# MADR Frontmatter Extensions

## Context and Problem Statement

A *[decision record][DECISIONRECORD]* needs facts that *[structured MADR][STRUCTUREDARCHITECTUREDECISIONRECORD]* does not define. MADR is short for *[Markdown Architecture Decision Record][MARKDOWNARCHITECTUREDECISIONRECORD]*. [CORE-0011](CORE-0011%20ADR%20Template%20Choice.md) adopts [structured MADR][STRUCTUREDARCHITECTUREDECISIONRECORD]. Its frontmatter does not say who approves a decision, where an adapted decision came from, or which *[change][CHANGE]* delivered it. [Structured MADR][STRUCTUREDARCHITECTUREDECISIONRECORD] permits an added field when the field has an `x-` prefix. A strict *[validator][VALIDATOR]* of that format rejects an added field without one.

## Considered Options

1. No added fields. The author keeps accountability and provenance in the body as prose, where no check reads them.
2. Prefixed fields only, such as `x-rune-responsible`. A strict [validator][VALIDATOR] accepts them, and every record becomes harder to read.
3. Bare field names only. A record reads well, and a strict [validator][VALIDATOR] of [structured MADR][STRUCTUREDARCHITECTUREDECISIONRECORD] rejects it.
4. Both forms. Each added field has a bare canonical name and a compliant `x-rune-` long form.

## Decision Outcome

Option 4. The bare name is canonical, and the records in the *[repository][REPOSITORY]* use it. The long form exists so that a record can pass a strict [validator][VALIDATOR] of [structured MADR][STRUCTUREDARCHITECTUREDECISIONRECORD] without a mapping step.

| Canonical | Long form | Kind | Meaning |
|---|---|---|---|
| `responsible` | `x-rune-responsible` | list | who does the work |
| `accountable` | `x-rune-accountable` | list | who approves the decision |
| `consulted` | `x-rune-consulted` | list | whose input the author used, people and *[models][MODEL]* |
| `informed` | `x-rune-informed` | list | who hears the outcome |
| `upstream` | `x-rune-upstream` | list | the sources the author adapted the decision from |
| `related` | `x-rune-related` | list | neighbor records by id and title |
| `change` | `x-rune-change` | string or list | the [change][CHANGE] id, or ids, that delivered the decision |

- A record MUST have `responsible`, `accountable`, and `upstream`, each in one form. An empty list is a statement and never an omission.
- A record MUST NOT set both forms of one field.
- `x-rune-` is the only accepted prefix. A field with another `x-` prefix MUST fail the check.
- A record MAY have other fields without an `x-` prefix when they do not conflict with these. A check MUST NOT reject them.
- The frontmatter MUST be enough to rebuild the record's location: `type`, `project`, and the id in the title give the path.

The field check, `scripts/check-decision-fields`, enforces the first three constraints. The *[structure schema][STRUCTURESCHEMA]* of the directory marks the three required fields optional, because a schema cannot state that either form satisfies a field.

### Consequences

- [-] A record written with bare names does not pass a strict [validator][VALIDATOR] of [structured MADR][STRUCTUREDARCHITECTUREDECISIONRECORD]. A record written with the long form does.
- [-] Two forms for one field are two ways to write the same fact. The check rejects a record that sets both, and the [repository][REPOSITORY]'s own records stay on the bare form.
- [+] The `change` field makes the link from a record to its [change][CHANGE] a fact a check can read.
- [-] The public format home states the same constraint in its README, and its JSON Schema still requires the bare names. A long-form record fails that schema until the home revises it.

## More Information

- Rewritten on 2026-10-19 in the plain spoken register. The decision is unchanged.

[DECISIONRECORD]: ../specs/glossary/decision-record.md
[CHANGE]: ../specs/glossary/change.md
[VALIDATOR]: ../specs/glossary/validator.md
[REPOSITORY]: ../specs/glossary/repository.md
[STRUCTURESCHEMA]: ../specs/glossary/structure-schema.md
[MARKDOWNARCHITECTUREDECISIONRECORD]: ../specs/glossary/markdown-architecture-decision-record.md
[STRUCTUREDARCHITECTUREDECISIONRECORD]: ../specs/glossary/structured-architecture-decision-record.md
[MODEL]: ../specs/glossary/model.md
