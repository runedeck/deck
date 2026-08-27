# Workflow Security Specification

## Purpose

This specification defines blocking security scans for repository workflows.

## Requirements

### Requirement: Blocking security scan

The pre-push Semgrep hook SHALL disable version checks. It SHALL return a nonzero status when it finds a blocking rule match.

#### Scenario: Semgrep scans the repository

- **WHEN** the pre-push hook runs Semgrep
- **THEN** Semgrep does not check for a newer version
- **AND** the scan result depends on the configured rules and repository content

#### Scenario: Semgrep finds a blocking match

- **WHEN** Semgrep reports a blocking rule match
- **THEN** the pre-push hook fails
- **AND** Git does not push the branch

### Requirement: Narrow scan exception

A workflow SHALL suppress one Semgrep rule only when a documented control proves that the finding cannot execute untrusted code.

#### Scenario: Trusted base checkout

- **WHEN** a `pull_request_target` job checks out the pull request base SHA
- **THEN** the pull request head does not enter the worktree
- **AND** the job does not execute pull request code
- **AND** the checkout does not persist Git credentials
- **AND** the `nosemgrep` directive names the exact rule

### Requirement: Narrow secret scope

A workflow SHALL expose each secret only to the step that consumes it.

#### Scenario: Publication credentials are unavailable

- **WHEN** the credential step cannot read both publication credentials
- **THEN** it emits only `available=false`
- **AND** the artifact step uses that output as a non-secret signal
- **AND** no workflow or job `env` exposes the credentials

### Requirement: Canonical delta specification

The spec gate SHALL accept canonical delta specifications under `docs/changes/<change>/specs/`.

#### Scenario: A protected change includes a delta specification

- **WHEN** a pull request changes a protected path
- **AND** it changes a file under `docs/changes/<change>/specs/`
- **THEN** the spec gate accepts the specification
