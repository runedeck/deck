# Secure Review Workflows Specification

## Purpose

The repository's review workflows run code from pull requests and hold publication credentials. This specification defines the blocking security scan and the two narrowing rules, one for a scan exception and one for secret scope, that keep that exposure small.

## Requirements

### Requirement: Blocking security scan

The pre-push Semgrep hook MUST disable version checks. It MUST return a nonzero status when it finds a blocking rule match.

#### Scenario: Semgrep scans the repository

- **WHEN** the pre-push hook runs Semgrep
- **THEN** Semgrep does not check for a newer version
- **AND** the scan result depends on the configured rules and repository content

#### Scenario: Semgrep finds a blocking match

- **WHEN** Semgrep reports a blocking rule match
- **THEN** the pre-push hook fails
- **AND** Git does not push the branch

### Requirement: Narrow scan exception

A workflow MUST suppress one Semgrep rule only when a documented control proves that the finding cannot execute untrusted code.

#### Scenario: Trusted base checkout

- **WHEN** a `pull_request_target` job checks out the pull request base SHA
- **THEN** the pull request head does not enter the worktree
- **AND** the job does not execute pull request code
- **AND** the checkout does not persist Git credentials
- **AND** the `nosemgrep` directive names the exact rule

### Requirement: Narrow secret scope

A workflow MUST expose each secret only to the step that consumes it.

#### Scenario: Publication credentials are unavailable

- **WHEN** the credential step cannot read both publication credentials
- **THEN** it emits only `available=false`
- **AND** the artifact step uses that output as a non-secret signal
- **AND** no workflow or job `env` exposes the credentials
