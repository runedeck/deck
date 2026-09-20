---
adr: "docs/decisions/CORE-0019 Spec-Driven Change Lifecycle.md"
status: accepted
decisions:
    - "CORE-0019 Spec-Driven Change Lifecycle"
---

# Spec change lifecycle

## Why

Decision records state why a choice stands. Nothing stated what must hold. Behavior lived in prose, drifted with it, and review had no target to test. The core foundations require that each behavior becomes a specification requirement, and they leave the lifecycle open.

The 2026-09-20 alignment with the owner added rules that no document carried: what marks a change accepted, how a change is named, and what the owner reviews before an archive.

## What Changes

- A spec-change-lifecycle capability: the change layout, the testable requirement grammar, one canonical tree, and the rules for names, acceptance, and review.
- `scripts/check-spec-names` enforces the name rules. It already runs as a prek hook.

## Capabilities

- spec-change-lifecycle (new)

## Impact

- `docs/changes/spec-change-lifecycle/`, `docs/decisions/CORE-0019 Spec-Driven Change Lifecycle.md`.
- Two defects in `rune spec archive` are recorded as tasks for the cli repository.
