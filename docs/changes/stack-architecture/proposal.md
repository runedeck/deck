---
adr: "docs/decisions/DECK-0005 Artifact Lifecycle and Evidence Tokens.md"
status: proposed
---
# Stack Architecture

## Why

The stack grew as tools: build skills, an adoption state machine, a bench harness, review lanes, an installer, and provider routines. No document names the system they form. The live drift report (issue #45) shows the cost: seams between tools fail silently because no contract says who owns them.

## What Changes

- One design document names the three planes, the seven flow stages, their evidence tokens, the four state stores, the two provider edges, and the retirement path.
- Three decision records fix the load-bearing choices: DECK-0005 (lifecycle and evidence tokens), DECK-0006 (state stores and provider edges), DECK-0007 (retirement path).
- A gap register records every known divergence between the abstraction and today's tooling. This change fixes none of them.
- The delta specification states the lifecycle contracts as MUST requirements for future enforcement work.

## Capabilities

- artifact-lifecycle (new)

## Impact

- `docs/changes/stack-architecture/`: this proposal, the design document, the delta specification, and the follow-up tasks.
- `docs/decisions/`: DECK-0005, DECK-0006, DECK-0007.
- No rune, cast, command, workflow, or consumer behavior changes.
