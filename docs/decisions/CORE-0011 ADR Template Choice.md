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
updated: 2026-10-19
author: "@N4M3Z"
project: deck
related:
    - "CORE-0010 Adopt Architecture Decision Records"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5-1@claude"]
informed: []
upstream: []
change: ["keep-architecture-decision-records", "decision-records-match-template"]
---

# ADR Template Choice

## Context and Problem Statement

[CORE-0010](CORE-0010%20Adopt%20Architecture%20Decision%20Records.md) adopts *[decision records][DECISIONRECORD]* and leaves the template open. Several formats exist: the original Nygard *[architecture decision record][ARCHITECTUREDECISIONRECORD]*, MADR (the *[markdown architecture decision record][MARKDOWNARCHITECTUREDECISIONRECORD]*), Y-Statements, and structured MADR. The template has to be short enough for a small decision and complete enough for a large one. A machine has to check its frontmatter.

## Decision Drivers

- The author must record the considered options. The Nygard record omits them.
- A machine must read the frontmatter, and the *[validator][VALIDATOR]* must check it before a commit.
- A record must name who approves the decision.

## Considered Options

1. The Nygard record: context, decision, status, consequences. It has no options list and no frontmatter.
2. Full MADR: it adds decision drivers and a confirmation section, and each option lists its pros and cons. It is thorough and heavy.
3. Y-Statements: one sentence for each decision. A complex decision does not fit.
4. [Structured MADR][SMADR]: the *[structured architecture decision record][STRUCTUREDARCHITECTUREDECISIONRECORD]*, the MADR body with YAML frontmatter that a machine reads.

## Decision Outcome

Option 4. A record MUST have these sections in this order: Context and Problem Statement, Considered Options, and Decision Outcome. Consequences is a subsection of Decision Outcome. Decision Drivers and More Information are optional. The [validator][VALIDATOR] MUST check the frontmatter fields and the heading order against the *[structure schema][STRUCTURESCHEMA]* at `docs/decisions/.mdschema`. [CORE-0012](CORE-0012%20MADR%20Frontmatter%20Extensions.md) states the added fields.

### Consequences

- [+] The [validator][VALIDATOR] rejects a record with a missing field before the record reaches review.
- [-] The template is heavier than the Nygard record. The author of a small decision still fills each required section.
- [-] The [validator][VALIDATOR] reads the repository's own schema file instead of the upstream JSON Schema. An upstream field change does not reach the repository by itself.

## More Information

- [Structured MADR][SMADR]
- [MADR Template Primer][PRIMER]
- 2026-09-22: the outcome listed Consequences as a fourth top-level section. The runeADR template puts it under Decision Outcome. Thirty-one records had matched the wrong sentence. The decision-records-match-template change corrected the sentence and the records.
- Rewritten on 2026-10-19 in the plain spoken register. The decision is unchanged.

[SMADR]: https://github.com/zircote/structured-madr "structured-madr, schema and validator"
[PRIMER]: https://www.ozimmer.ch/practices/2022/11/22/MADRTemplatePrimer.html "Olaf Zimmermann, MADR Template Primer, 2022"
[DECISIONRECORD]: ../specs/glossary/decision-record.md
[ARCHITECTUREDECISIONRECORD]: ../specs/glossary/architecture-decision-record.md
[MARKDOWNARCHITECTUREDECISIONRECORD]: ../specs/glossary/markdown-architecture-decision-record.md
[STRUCTUREDARCHITECTUREDECISIONRECORD]: ../specs/glossary/structured-architecture-decision-record.md
[VALIDATOR]: ../specs/glossary/validator.md
[STRUCTURESCHEMA]: ../specs/glossary/structure-schema.md
