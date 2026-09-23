## ADDED Requirements

### Requirement: Configuration Defaults

A module MUST include `defaults.yaml` with the full schema and working defaults.
User overrides live in a gitignored `config.yaml` merged recursively.
The config loading exports the merged result as environment variables.

#### Scenario: Module requires user configuration to start

- **WHEN** a module fails without a user `config.yaml`
- **THEN** validation reports the missing default

#### Scenario: Override merges over defaults

- **WHEN** a user `config.yaml` sets one field
- **THEN** the merged configuration contains that value and every other committed default

#### Scenario: Merged configuration exports

- **WHEN** the configuration loads
- **THEN** the merged result exports as environment variables, so instructions reference it by `$NAME`

### Requirement: One Checker Per Concern

Every validation concern MUST have one chosen checker, recorded in the coverage table.
A new concern or a tool change arrives through a decision record.

#### Scenario: Concern has no chosen checker

- **WHEN** a change adds a validation concern that none of the chosen checkers covers
- **THEN** the coverage table records the open gap and a decision record picks the tool

### Requirement: One Validation Path

Every check MUST run through one shared hook configuration locally and in CI.
A check that exists only in CI is a violation.
An environment without the hook runner falls back to the committed hook scripts with the same checks.

#### Scenario: CI-only check appears

- **WHEN** a workflow adds a check absent from the shared hook configuration
- **THEN** review moves the check into the shared configuration

#### Scenario: Runner is absent

- **WHEN** an environment lacks the hook runner
- **THEN** the committed hook scripts run the same checker roster, and a roster difference is a violation
