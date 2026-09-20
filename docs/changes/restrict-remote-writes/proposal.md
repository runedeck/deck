---
adr: docs/changes/restrict-remote-writes/adr.md
status: proposed
decisions: ["Restrict remote writes", "DECK-0016 Forge Adoption"]
---

# Restrict remote writes

## Why

Prohibitions against merging, commenting, labelling, and pushing were retyped in every session and still leaked. A rule is always on. A three-model review agreed the list cannot live in a skill.

## What Changes

- The RemoteWrites rule at `runes/core/rules/RemoteWrites.md`, rewritten from its forge origin for frontier models.

## Capabilities

- restrict-remote-writes (new)

## Impact

- `runes/core/rules/RemoteWrites.md` (new).
- Split from the forge-adoption change on 2026-09-20. DECK-0016 records the adoption as a whole.

## Risks

- The prohibitions rule gets stretched, so one named label becomes any label. Guard: command-shaped wording, both exceptions limited to the invoking agent and to the correctness label, and child briefs carry the list without the exceptions.
- pi and codex have no rules path yet. Guard: the pi package `AGENTS.md` carries the same command list until the `AGENTS.md` assembly target exists (task 4.3 in agentic-merge-train).
- No bench and no proof yet, so the only evidence is the adversarial passes on the text. Guard: tasks 4.1 and 4.2 stay open and the record status stays proposed.
