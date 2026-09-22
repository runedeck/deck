---
title: "Record content is checked"
description: "A check reads what the schema cannot: the sign on each consequence, the harness on each consulted model, and the target of each provenance entry."
type: adr
category: process
tags:
    - adr
    - process
    - checks
status: proposed
created: 2026-09-22
updated: 2026-09-22
author: "@N4M3Z"
project: deck
related:
    - "CORE-0011 ADR Template Choice"
    - "CORE-0012 MADR Frontmatter Extensions"
    - "CORE-0018 Fixture-Based Canary Testing"
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5-1@claude"]
informed: []
upstream:
    - "https://github.com/runedeck/adr"
    - "enforce-record-shape#consequences-carry-a-sign"
    - "enforce-record-shape#consulted-entries-name-the-harness"
    - "enforce-record-shape#provenance-entries-resolve"
    - "enforce-record-shape#adopted-record-keeps-its-source-dates"
change: enforce-record-shape
---

# Record content is checked

## Context and Problem Statement

The directory schema validates headings and field presence, and nothing reads what a record says. The runeADR template puts `### Consequences` under `## Decision Outcome` with `[+]` and `[-]` bullets, and the schema at the public home lists `## Consequences` as its own optional section. The deck copied the schema, 31 of 38 records followed it, the signs disappeared, and CORE-0011 wrote the drift into a MUST. The adopted forge-core records lost their `updated` dates, `upstream` named files that exist in no deck, and two `related` entries named records that were never written. Review passed all of it. The question is which of these facts a check can read, and which stay with review.

## Considered Options

1. Keep the schema and rely on review. Review passed every case above.
2. Tighten the schema and add a content check for what a schema cannot express: the shape of a list item, the form of a field value, and whether a reference resolves.
3. Validate through the upstream Structured MADR JSON Schema and action. It checks frontmatter as data, not the body, and it rejects the bare field names CORE-0012 made canonical.

## Decision Outcome

Option 2.

- A record MUST place its consequences under `### Consequences` inside `## Decision Outcome`, one list item each, starting with `[+]` or `[-]`.
- A `consulted` entry MUST be `@handle` or `<model-id>@<harness>`, and the harness MUST be a domain label in `authors.yaml`.
- An `upstream` or `related` entry MUST resolve: a record stem, a draft record title, a capability, `<capability>#<requirement-slug>`, or a URL.
- An adopted record MUST keep the `created` and `updated` of its source and MUST name the source in `upstream`. A later deck edit moves `updated` and states itself under More Information.
- `scripts/check-decision-shape` MUST enforce the first three rules on every record before a commit and in CI. The fourth stays with review, because no check reads the source repository.

### Consequences

- [+] A drafted record that does not follow the template fails before review reads it.
- [+] A provenance entry is a fact a check can follow, and the capability form stays valid after the change that contains the spec archives.
- [-] Every consequence needs a sign, and a mixed effect must be split into two items or given the sign of its larger part.
- [-] The harness suffix on seven adopted records is inferred, not recorded. Task 3.2 holds the question.
- [-] The public format home keeps the old schema until its own change is merged. A record that passes the deck fails the home's schema on the Consequences heading, and the reverse.
