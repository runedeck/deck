## ADDED Requirements

### Requirement: Verified release installation

The cloud installer MUST download and verify each pinned release asset on every run.
The installer MUST install the verified binary even when a binary with the same name exists.
The installer MUST NOT execute the existing binary to establish trust.

#### Scenario: A tool already exists

- **WHEN** the installer finds an existing pinned tool
- **THEN** it replaces the tool with the verified release binary
- **AND** it leaves the existing binary unexecuted

### Requirement: Failed digest preserves the installation

The cloud installer MUST stop before extraction or installation when an asset digest differs from its declared digest.

#### Scenario: An asset has the wrong digest

- **WHEN** the downloaded asset fails digest verification
- **THEN** the installer returns a nonzero status
- **AND** it preserves the existing installation
- **AND** it leaves a missing binary absent

### Requirement: Standalone schema validator

The cloud installer MUST install the standalone `mdschema` binary through verified release installation.
The schema responsibilities remain in `runes/core/skills/BuildSkill/RuneDeck.md`.

#### Scenario: The image lacks the schema validator

- **WHEN** the cloud installer completes on an image without `mdschema`
- **THEN** `/usr/local/bin/mdschema` contains the verified release binary
- **AND** repository hooks can invoke that binary

### Requirement: Installer regression checks

The existing quality workflow MUST execute the cloud installer regression suite.
The suite MUST use local test assets and isolated installation paths.

#### Scenario: The quality workflow runs

- **WHEN** the quality workflow checks a pull request
- **THEN** it tests verified installation and replacement
- **AND** it tests digest rejection before an installation changes
- **AND** it tests the standalone schema validator archive
- **AND** it fails when an installer regression test fails

### Requirement: Trusted commit attribution

The cloud environment MUST apply the [canonical commit attribution contract](https://github.com/runedeck/deck/blob/269099293e9f8aec8cf801697359c2a733c022dd/docs/specs/commit-attribution/spec.md).
The local checker and identity helper MUST use that contract for outgoing commits.
An explicit-bookmark push MUST validate the selected bookmark through the same contract.

#### Scenario: An approved harness uses a new model

- **WHEN** an outgoing commit declares a model identity that satisfies the trusted policy
- **THEN** local attribution validation accepts it under the canonical contract

#### Scenario: A push starts from a JJ workspace

- **WHEN** the owner pushes one explicit bookmark
- **THEN** the wrapper validates that bookmark in an isolated checkout
- **AND** it preserves the canonical publication and signing constraints
