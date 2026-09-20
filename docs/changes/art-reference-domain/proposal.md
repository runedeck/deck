---
adr: docs/changes/art-reference-domain/adr.md
status: proposed
decisions: ["Art reference research as a deck domain"]
---

# Art reference domain

## Why

Visual reference research, painting plans, and attributed art collections were done by hand in each session. The Art skill and the PaletteCritic agent were authored on 2026-09-09 in the primary checkout and never committed.

## What Changes

- The `art` domain at `runes/art/`: the Art skill with seven companions, and the PaletteCritic agent.
- The domain carries its own `module.yaml`, `defaults.yaml`, `LICENSE`, and `README.md`.

## Capabilities

- art-reference-domain (new)

## Impact

- `runes/art/` (new). No other file changes.
- The record in `adr.md` moves to `docs/decisions/` at archive.
