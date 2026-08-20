## ADDED Requirements

### Requirement: Temporary Review State

AdoptArtifact SHALL record block text, verdicts, notes, flags, and timestamps only in temporary rune session state. The deck SHALL NOT commit `review.yaml` or `*.review.yaml` files under `.provenance`.

#### Scenario: Adoption finalizes

- **WHEN** every imported block has a verdict and finalization succeeds
- **THEN** the temporary session is removed and no block-review ledger appears in the staged diff

### Requirement: Durable Source Provenance

A finalized adoption SHALL commit a source-level provenance sidecar for each adopted file. Each sidecar SHALL retain the upstream source and digest, reviewed state, and final file digest.

#### Scenario: Reviewed artifact is staged

- **WHEN** a maintainer stages a finalized adoption
- **THEN** the staged files contain the artifact and its source-level sidecars without a review transcript

### Requirement: Ledger Guard

Repository validation SHALL fail when a tracked `.provenance/review.yaml` or `.provenance/*.review.yaml` file exists.

#### Scenario: Legacy ledger remains tracked

- **WHEN** a tracked review ledger exists in the repository
- **THEN** the review-ledger hook fails and identifies its path

### Requirement: Context Suffix Normalization

Authorship validation SHALL ignore a trailing `1m` context suffix after a model version digit in display model IDs and email local parts.

#### Scenario: One-million-context identity

- **WHEN** a commit uses `claude-opus-51m` or `claude-fable-51m`
- **THEN** authorship validation compares it as `claude-opus-5` or `claude-fable-5`
