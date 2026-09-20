## ADDED Requirements

### Requirement: Checks run locally before publication

A session that edits a repository MUST run the repository's commit-stage checks with every tool required after each batch of edits. It MUST run the push-stage checks on the exact head before it asks for a signature or a push. A candidate MUST NOT be reported as validated from a subset of the hooks or from the exit status of a filter.

#### Scenario: Edit batch completes

- **WHEN** a session finishes a batch of edits in a repository with `.pre-commit-config.yaml`
- **THEN** it runs the commit stage with `REQUIRE_GATES` set and fixes every error-level finding before the next batch

#### Scenario: Candidate is frozen

- **WHEN** a session freezes a head for publication
- **THEN** it runs the push-stage checks on that head in a disposable checkout
- **AND** it reports each stage's own exit status with the commit id

#### Scenario: Push hook stops a publication

- **WHEN** the checked push hook fails on a finding
- **THEN** the session fixes the finding, freezes again, and runs both stages before it asks for the key again
