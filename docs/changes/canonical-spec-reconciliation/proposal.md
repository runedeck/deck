---
adr: docs/changes/canonical-spec-reconciliation/adr.md
status: proposed
decisions: ["A canonical spec names its purpose and its decision"]
---

# Canonical spec reconciliation

## Why

The deck's five canonical specifications did not match the work around them. `portable-skill-authoring` carried the archive placeholder `TBD` as its purpose. `adoption-session-state` stated the model-identity rule twice with the same scenario. `secure-review-workflows` held a requirement about the spec-presence check under a security heading. Two H1 titles named a different capability than their directory.

## What Changes

- Rewrite the purpose of `portable-skill-authoring` (DECK-0018) and `adoption-session-state`, and fold its two identity requirements into one that points at `model-commit-attribution`.
- Move `Canonical delta specification` out of `secure-review-workflows` into a new canonical spec `spec-presence-attestation`, and write both purposes.
- Set every H1 to `<Directory Name> Specification` in title case: `model-commit-attribution`, `secure-review-workflows`, `worktree-commit-identity`.
- State in `worktree-commit-identity` how it relates to the skeleton's `worktree-identity`.

## Capabilities

### New Capabilities

- `canonical-spec-reconciliation`: every canonical spec in `docs/specs/` states a purpose in its own words, one requirement per rule, and an H1 that names its directory.

## Impact

- `docs/specs/` only. No rune, workflow, or decision text changes. The specs still lack a `decisions:` link, because canonical specs carry no frontmatter today. The ADR names the decision each one serves.
