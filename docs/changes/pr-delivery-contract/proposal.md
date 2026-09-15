---
adr: "docs/decisions/DECK-0008 Idea-to-Merge Flywheel.md"
status: proposed
---

# Pull request delivery contract

## Why

The session required repeated owner intervention to obtain published fixes and accurate merge-ready reports.
VersionControl contains contradictory rebase instructions and lacks bounded recovery and complete delivery evidence.

## What Changes

- Define the delivery contract for the existing babysitting stage.
- Remove contradictory recovery instructions instead of adding another prohibition.
- Derive merge readiness from authoritative requirements and current evidence, including absent checks and skipped reviews.
- Keep task scope, concurrent ownership, and publication state explicit across delegated work and session resumptions.
- Use the trusted attribution contract instead of a model catalog.
- Bound provider recovery and preserve an actionable blocker when a required reviewer cannot complete.
- Amend DECK-0008 with the rationale and the contract reference.

## Capabilities

### New Capabilities

- `pull-request-delivery`: Evidence and recovery requirements for the existing PR babysitting stage.

### Modified Capabilities

None. Existing authorization, attribution, artifact lifecycle, and adversarial-review requirements remain authoritative.

## Impact

- `runes/core/skills/VersionControl/`: follow-up implementation after owner review.
- `docs/changes/pr-delivery-contract/`: proposal, delta specification, design, and tasks.
- `docs/decisions/DECK-0008 Idea-to-Merge Flywheel.md`: proposed amendment.

The separate [authorization PR](https://github.com/runedeck/deck/pull/56) supplies the publication boundary.
This change adds no provider integration, workflow implementation, new model catalog, or routine behavior.

## Pushback

Outcome: a bounded extension of the babysitting stage in `agent-pipeline`, not a replacement pipeline.
That change defines intake and extraction but does not define a complete PR delivery contract.
The current skill already defines merge-ready conditions and publication approval.
This proposal targets contradictory instructions and gaps in obtaining evidence, rather than repeating those definitions.

The council supplies research candidates, not acceptance by agreement.
Each candidate requires a source-based refutation attempt under CORE-0016.
