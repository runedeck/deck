---
adr: "docs/decisions/CORE-0010 Adopt Architecture Decision Records.md"
status: accepted
decisions: ["CORE-0010 Adopt Architecture Decision Records", "CORE-0011 ADR Template Choice", "CORE-0012 MADR Frontmatter Extensions"]
---

# Architecture Decision Records

## Why

Core foundations requires that each decision becomes a record and delegates the format. The format needs its own capability: the record shape, the accountability fields, and the provenance fields, each enforceable by a check. The format also needs a public home under the runedeck organization, so consumers adopt it without adopting the whole deck.

## What Changes

- An architecture-decision-records capability: the record shape, the status lifecycle, the accountability fields, and the provenance fields.
- The record rules from the 2026-09-20 alignment: a record for every change, the record inside its change until archive, a link both ways, ids never reused, unknown frontmatter kept.
- The public format home is under the runedeck organization, and records use bare field names.

## Capabilities

- architecture-decision-records

## Impact

- `docs/changes/architecture-decision-records/`, `docs/decisions/.mdschema`, later the public format repository.
