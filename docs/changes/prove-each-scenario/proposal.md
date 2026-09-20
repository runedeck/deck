---
adr: "docs/decisions/DECK-0015 Behavior Proof per Change.md"
status: proposed
---

# Behavior Proof

## Why

See the linked ADR for the decision rationale. This proposal records the change in scope.

A candidate that passes every check can still do the wrong thing. The specification states the intended behavior as scenarios, and nothing runs them end to end against the built candidate or records the result as evidence.

## What Changes

- The AcceptanceTesting skill in core: one recorded scene per specification scenario, `expect` on every THEN, a failed expectation fails the recording, and the GIF, MP4, and transcript are filed as the `behavior` proof. Companions carry the scene grammar and the recording mechanics. The driver script gains `scenario`, `expect`, and `expect_not`.
- VersionControl carries one constraint: prove the frozen candidate before every push, checks through ContinuousIntegration and, for a change with user-visible behavior, scenarios through AcceptanceTesting, both naming the same commit.
- DECK-0015 records the decision. The terminal-recording proposal (#64) is superseded.

## Capabilities

- prove-each-scenario (new)

## Impact

- `runes/core/skills/AcceptanceTesting/` (new): `SKILL.md`, `Scenes.md`, `Recording.md`, `scripts/record.sh`.
- `runes/core/skills/VersionControl/SKILL.md`: one constraint.
- `docs/decisions/`: DECK-0015.
