---
adr: "docs/decisions/DECK-0013 Local Checks Before Publication.md"
status: proposed
---

# Local checks

## Why

Every repository declares its checks in `.pre-commit-config.yaml`, and CI runs that file. Sessions ran hand-picked lints instead, reported them as clean, and met the full set only inside the checked push hook, while the owner waited at the signing key. A `typos` finding and a broken base change stopped two pushes that way on 2026-09-14. The checks exist. Nothing said when to run them.

## What Changes

- The ContinuousIntegration skill in core: run the commit stage with every tool required after each edit batch, run the push stage on the frozen head before publication, record each stage's own exit status, and never bypass a finding.
- VersionControl names ContinuousIntegration as the step before every push.

## Capabilities

### New Capabilities

- `enforce-local-checks`: a session runs the repository's own check stages locally and repeatedly before it asks for a push or a signature.

## Impact

- `runes/core/skills/ContinuousIntegration/` and one constraint in `runes/core/skills/VersionControl/SKILL.md`.
- No hook, workflow, or tool pin changes. The next step is a core rule and the same mandate in the cli and skeleton specifications.
