---
adr: docs/changes/use-adversarial-reviews/adr.md
status: proposed
decisions: ["Refute a draft before accepting it", "DECK-0016 Forge Adoption"]
---

# Refute a draft before accepting it

## Why

Hostile prose rounds were run by hand. One skill attacks the original from three disjoint angles and binds each hit to a quoted line. It settles every hit as fixed or rejected with reason (CORE-0016 method).

## What Changes

- The AdversaryReview skill at `runes/development/skills/AdversaryReview/`, rewritten from its forge origin for frontier models.
- Deploys only where a workflow tool exists (`targets: [claude, agentskills]`) and stops with one sentence elsewhere.

## Capabilities

- use-adversarial-reviews (new)

## Impact

- `runes/development/skills/AdversaryReview/` (new).
- Split from the forge-adoption change on 2026-09-20. DECK-0016 records the adoption as a whole.
