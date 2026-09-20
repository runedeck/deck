# Worktree Commit Identity Specification

## Purpose

A workspace gets its model identity before any commit exists, and an explicit-bookmark push validates the exact outgoing history in an isolated checkout. This is the deck's own copy of the push contract. The skeleton's `worktree-identity` specification covers provisioning and cleanup of the checkout itself.

## Requirements

### Requirement: Exact workspace push validation

An explicit-bookmark JJ push MUST validate the selected commit in an isolated Git checkout.
The checkout MUST contain the trusted `origin/main` policy and the exact outgoing history.
The existing pre-push hook MUST pass before publication.
Hook changes to tracked content or new untracked files MUST stop publication.
The push MUST use the validated remote, literal bookmark, and JJ operation.
The wrapper MUST preserve the configured signing mode.

#### Scenario: Workspace uses a bare Git backend

- **WHEN** a JJ workspace has no Git working tree
- **THEN** the hook validates its selected bookmark without reading another workspace

#### Scenario: Another session changes the bookmark

- **WHEN** the selected bookmark changes after validation starts
- **THEN** the push stops or publishes only the validated operation

#### Scenario: A pre-push gate fails

- **WHEN** the existing pre-push hook fails
- **THEN** the remote bookmark remains unchanged

### Requirement: Workspace identity resolution

`make worktree` MUST resolve identity before it changes version-control state.
A known model MUST resolve to one matching author entry.
Within one harness, an exact model ID MUST take precedence over its canonical aliases.
Context normalization MUST remove `[1m]` before this comparison.
Multiple matching harnesses MUST require an explicit harness.
A new model MUST supply an approved harness.
A colocated repository MUST create a Jujutsu workspace.
The target MUST report the resolved author name and address.

#### Scenario: New model has an approved harness

- **WHEN** the caller supplies a valid new model ID and an approved harness
- **THEN** the target resolves a valid identity before it creates the workspace

#### Scenario: Resolution fails

- **WHEN** the identity is ambiguous or its harness is unapproved
- **THEN** the target fails before any version-control command

#### Scenario: Policy contains current and legacy model IDs

- **WHEN** the policy lists both `claude-fable-5` and `claude-fable-51m` for the selected harness
- **THEN** each ID resolves to its exact entry

#### Scenario: Multiple entries use the same model ID and harness

- **WHEN** two author entries have the same model ID and harness
- **THEN** resolution rejects the ambiguous identity
