---
adr: docs/changes/every-spec-states-purpose/adr.md
status: proposed
decisions: ["A canonical spec names its purpose and its decision"]
---

# Canonical spec reconciliation

## Why

The repository's five canonical specifications did not match the work around them. `skills-portable-across-harnesses` carried the archive placeholder `TBD` as its purpose. `record-provenance-for-adoptions` stated the model-identity rule twice with the same scenario. `blocking-scan-on-every-review` held a requirement about the spec-presence check under a security heading. Two H1 titles named a different capability than their directory.

## What Changes

- Rewrite the purpose of `skills-portable-across-harnesses` (DECK-0018) and `record-provenance-for-adoptions`, and fold its two identity requirements into one that points at `model-identity-on-commits`.
- Move `Canonical delta specification` out of `blocking-scan-on-every-review` into a new canonical spec `changes-require-stated-specs`, and write both purposes.
- Set every H1 to `<Directory Name> Specification` in title case: `model-identity-on-commits`, `blocking-scan-on-every-review`, `commits-carry-model-identity`.
- State in `commits-carry-model-identity` how it relates to the skeleton's `worktree-identity`.

## Capabilities

### New Capabilities

- `every-spec-states-purpose`: every canonical spec in `docs/specs/` states a purpose in its own words, one requirement per rule, and an H1 that names its directory.

## Impact

- `docs/specs/` only. No rune, workflow, or decision text changes. The specs still lack a `decisions:` link, because canonical specs carry no frontmatter today. The ADR names the decision each one serves.
