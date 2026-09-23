---
adr: "docs/changes/decision-records-match-template/adr.md"
status: proposed
decisions: ["Record content is checked", "CORE-0011 ADR Template Choice"]
---

# Enforce record shape

## Why

The directory schema checks headings and field presence, and the records drifted anyway. The runeADR template puts `### Consequences` under `## Decision Outcome` with `[+]` and `[-]` bullets. The schema listed `## Consequences` as its own optional section, so 31 of 38 records used that form and dropped the signs, and CORE-0011 codified the drift as a MUST. The adopted forge-core records also lost their `updated` dates, and `upstream` named rule files that do not exist in the repository. Two `related` entries named record titles that were never written. Review did not catch any of it, because nothing read the content.

## What Changes

- The schema requires `### Consequences` under `## Decision Outcome` and rejects `## Consequences`.
- `scripts/check-decision-shape` reads the content: a sign on each consequence, a `consulted` entry as `@handle` or `<model-id>@<harness>` with the harness from `authors.yaml`, and an `upstream` or `related` entry that resolves to a record, a capability, a requirement, or a URL.
- `upstream` gains a stable reference form, `<capability>#<requirement-slug>`, that stays valid after the change that contains the spec archives.
- Every record converts to the template shape. CORE-0001 gets its source dates and its provenance back, and CORE-0011 states the corrected order.
- `authors.yaml` adds the `opencode` harness domain, because Lumo runs through opencode.

## Capabilities

- decision-records-match-template (new). It extends keep-architecture-decision-records, which is not archived yet, so the repository's one-capability rule gives the delta the change id.

## Impact

- `docs/decisions/.mdschema`, every record under `docs/decisions/`, `scripts/check-decision-shape`, `tests/test_check_decision_shape.py`, `.pre-commit-config.yaml`, `authors.yaml`.
- The public format home `runedeck/adr` carries the same schema defect in `adr.mdschema`. Its README and template are already right. The fix there is a copy of this repository's schema, and it is a separate change in that repository.
