## ADDED Requirements

### Requirement: Quality job carries the rune binary

The quality job MUST install the `rune` binary that the real-graph hook runs, built from the cli at a pinned full commit id, outside the checked-out tree, before the commit-stage checks run under `REQUIRE_GATES`.

#### Scenario: Quality job runs the real-graph hook

- **WHEN** the quality job reaches the commit-stage checks
- **THEN** `rune` is on the path at the pinned cli commit and the `ontology-graph` hook runs instead of failing on an absent binary

#### Scenario: Pin is a branch name

- **WHEN** a change sets the cli revision to a branch name instead of a full commit id
- **THEN** review refuses the change, because the build would move without a deck change
