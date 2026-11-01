---
title: "Spec-Driven Change Lifecycle"
description: "Behavior enters the deck through the OpenSpec lifecycle: a proposal, delta specifications, and an archive into one canonical tree."
type: adr
category: architecture
tags:
    - architecture
    - specifications
    - openspec
status: accepted
created: 2026-08-27
updated: 2026-10-19
author: "@N4M3Z"
project: deck
related:
    - "CORE-0010 Adopt Architecture Decision Records"
    - "CORE-0013 Context Economy"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5-1@claude", "gpt-6-astra@codex"]
informed: []
upstream:
    - "https://github.com/Fission-AI/OpenSpec"
change: lifecycle-of-a-change
---

# Spec-Driven Change Lifecycle

## Context and Problem Statement

The *[repository][REPOSITORY]* needs one *[change][CHANGE]* *[lifecycle][LIFECYCLE]*. In it, an author states each *[requirement][REQUIREMENT]*, a check validates it, and an archive merges it into one canonical tree. *[Decision records][DECISIONRECORD]* capture why a choice stands, and nothing captured what must hold. Behavior sat in prose, drifted with it, and review had nothing to test.

## Considered Options

1. A free-form design document for each [change][CHANGE].
2. The [OpenSpec][OPENSPEC] [lifecycle][LIFECYCLE]: a proposal with the `Why` and `What Changes` sections, a *[delta specification][DELTASPECIFICATION]* for each *[capability][CAPABILITY]*, and an archive into one canonical spec tree.

## Decision Outcome

Option 2.

- A [change][CHANGE] MUST live under `docs/changes/<id>/` with a proposal, a task list, and a [delta specification][DELTASPECIFICATION] for each [capability][CAPABILITY].
- A [requirement][REQUIREMENT] MUST use MUST language with at least one WHEN and THEN *[scenario][SCENARIO]*.
- Archive MUST merge the delta into `docs/specs/` and MUST move the [change][CHANGE] directory to `docs/changes/archive/`. The canonical tree is the only authoritative specification.
- Archive is the act that accepts a [change][CHANGE]. OpenSpec has no *[status][STATUS]* field and no accepted state, and the [repository][REPOSITORY] adds none. Archive MUST NOT run for a [change][CHANGE] without a record.
- `rune spec` is the native implementation over `docs/`, and the OpenSpec CLI operates on the same tree. One tree serves both, with no mirror.
- Validation has layers: the spec grammar through the spec tooling, the document frame through mdschema, and the prose through the chosen *[linters][LINTER]*.

### Consequences

- [+] Review has a [requirement][REQUIREMENT] it can test, and each [requirement][REQUIREMENT] can state the check that enforces it.
- [-] A small [change][CHANGE] needs the full ceremony: a proposal, a delta, and a record. The owner chose that cost, because a record states the intent of the [change][CHANGE].
- [-] The `status` field in a proposal is a note for readers. The tools read task checkboxes and the archive location, so the field can disagree with them.
- [-] `rune spec archive` matches [requirement][REQUIREMENT] headings by exact text. A canonical heading that someone recased by hand duplicates on the next archive. It also does not move a record or assign an id. Both are open tasks in the cli clone.

## More Information

- Rewritten on 2026-10-19 in the plain spoken register. The decision is unchanged.

[OPENSPEC]: https://github.com/Fission-AI/OpenSpec "OpenSpec, the spec-driven change lifecycle"
[REPOSITORY]: ../specs/glossary/repository.md
[CHANGE]: ../specs/glossary/change.md
[LIFECYCLE]: ../specs/glossary/lifecycle.md
[REQUIREMENT]: ../specs/glossary/requirement.md
[DECISIONRECORD]: ../specs/glossary/decision-record.md
[DELTASPECIFICATION]: ../specs/glossary/delta-specification.md
[CAPABILITY]: ../specs/glossary/capability.md
[SCENARIO]: ../specs/glossary/scenario.md
[STATUS]: ../specs/glossary/status.md
[LINTER]: ../specs/glossary/linter.md
