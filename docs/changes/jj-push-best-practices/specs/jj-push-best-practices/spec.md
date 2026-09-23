## ADDED Requirements

### Requirement: Exact bookmark validation

The push hook MUST route a push that names one bookmark through a bookmark helper.
The helper MUST run the existing pre-push checks against the selected commit in an isolated Git checkout.
The helper MUST publish only the validated bookmark, remote, and JJ operation.
The helper MUST preserve the configured signing mode.

#### Scenario: Unrelated changes exist in another workspace

- **WHEN** the caller pushes one explicit bookmark from a JJ workspace
- **THEN** the checks inspect that bookmark's tree and outgoing history
- **AND** unrelated workspace content stays outside the validation checkout

#### Scenario: Validation fails or changes the checkout

- **WHEN** a pre-push check fails or changes tracked content or adds an untracked file
- **THEN** the helper stops before publication

#### Scenario: The remote bookmark changes during validation

- **WHEN** another session changes the remote bookmark before publication
- **THEN** the helper stops and requests reconciliation

### Requirement: Outgoing authorship validation

The authorship check MUST validate the outgoing commit range against the trusted policy.
The check MUST select its target in this order: the explicit target option, the pre-commit target variable, the gitleaks push target variable, then the current head.
The checker MUST inspect the complete reachable history of an orphan target.

#### Scenario: The outgoing target differs from the current checkout

- **WHEN** the push hook supplies an orphan target through the gitleaks push target variable
- **THEN** the checker validates every commit reachable from that target against the trusted policy as published on the remote main branch

### Requirement: Future model attribution

The identity checker MUST accept formatted model identities under domains that the trusted policy approves.
The identity checker MUST apply the identity and contributor constraints in the [commit attribution specification](https://github.com/runedeck/deck/blob/0dd75051f4d47f3ca86dbb41cd555e46072a7e9d/docs/specs/commit-attribution/spec.md).

#### Scenario: A new version uses an approved harness

- **WHEN** a formatted identity uses `claude-fable-5.2` under an approved Claude domain
- **THEN** the checker accepts the identity without a new model entry

#### Scenario: A model identity uses an unapproved domain

- **WHEN** a formatted model identity uses a domain absent from the trusted policy
- **THEN** the checker rejects that identity
