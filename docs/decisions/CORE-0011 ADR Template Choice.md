---
title: "ADR Template Choice"
description: "Records use the structured MADR shape, validated by the directory schema, with accountability and provenance fields added."
type: adr
category: process
tags:
    - adr
    - process
    - structured-madr
status: accepted
created: 2026-02-19
updated: 2026-09-20
author: "@N4M3Z"
project: deck
related:
    - "CORE-0010 Adopt Architecture Decision Records"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5-1"]
informed: []
upstream: []
change: architecture-decision-records
---

# ADR Template Choice

## Context and Problem Statement

[CORE-0010](CORE-0010 Adopt Architecture Decision Records.md) adopts records and leaves the template open. Several formats exist: the original Nygard record, MADR, Y-Statements, and structured MADR. The template must be short enough for a small decision and complete enough for a large one. Its frontmatter must be checked by a machine.

## Decision Drivers

- The considered options must be recorded. The Nygard record omits them.
- Frontmatter must be machine-readable and validated before a commit.
- A record must name who approves the decision.

## Considered Options

1. The Nygard record: context, decision, status, consequences. It has no options list and no frontmatter.
2. Full MADR: adds decision drivers, options with pros and cons, and confirmation. It is thorough and heavy.
3. Y-Statements: one sentence for each decision. A complex decision does not fit.
4. [Structured MADR][SMADR]: the MADR body with machine-readable YAML frontmatter.

## Decision Outcome

Option 4. A record MUST have these sections in order: Context and Problem Statement, Considered Options, Decision Outcome, Consequences. Decision Drivers and More Information are optional. The `docs/decisions/.mdschema` file MUST validate the frontmatter fields and the heading order. [CORE-0012](CORE-0012 MADR Frontmatter Extensions.md) states the added fields.

## Consequences

- The schema rejects a record with a missing field before it reaches review.
- The template is heavier than the Nygard record. A small decision still fills each required section.
- The deck validates with its own schema file, not with the upstream JSON Schema, so an upstream field change does not reach the deck by itself.

## More Information

- [Structured MADR][SMADR]
- [MADR Template Primer][PRIMER]

[SMADR]: https://github.com/zircote/structured-madr "structured-madr, schema and validator"
[PRIMER]: https://www.ozimmer.ch/practices/2022/11/22/MADRTemplatePrimer.html "Olaf Zimmermann, MADR Template Primer, 2022"
