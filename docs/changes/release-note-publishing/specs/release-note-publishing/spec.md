## ADDED Requirements

### Requirement: Release Interval

The compiler MUST select pull requests merged after the previous release commit. Each selected pull request MUST be reachable from the target commit.

#### Scenario: A later release selects its interval

- **WHEN** the target commit contains pull requests merged after the previous release commit
- **THEN** the compiler selects each eligible pull request once
- **AND** the compiler excludes pull requests outside that commit interval

### Requirement: Curated Note Extraction

The compiler MUST read only the `## Release Notes` list from each selected pull request. It MUST omit an exact `- N/A` entry.

The compiler MUST keep each other list item and add its pull request link. One recorded body snapshot policy MUST apply to the full run.

#### Scenario: A pull request contains release notes

- **WHEN** a selected pull request contains two release-note list items
- **THEN** the compiler emits both items with one link to that pull request

#### Scenario: A pull request has no release effect

- **WHEN** a selected pull request contains the exact `- N/A` entry
- **THEN** the compiler emits no release entry for that pull request

### Requirement: Owner-Reviewed Release Draft

The release workflow MUST create or update one draft GitHub Release for the target version. The owner MUST publish the draft.

The workflow MUST stop before publication. A repeat run for the same target MUST update the same draft without duplicate entries.

#### Scenario: A release run completes

- **WHEN** the compiler returns a complete release body for the target version
- **THEN** the workflow stores that body in one draft GitHub Release
- **AND** the workflow leaves the draft unpublished

#### Scenario: The owner repeats a release run

- **WHEN** a draft already exists for the same target version and commit
- **THEN** the workflow updates that draft without adding duplicate entries

### Requirement: Complete Input Before Draft Mutation

The workflow MUST validate the selected interval before it changes a draft. The validation MUST cover pagination and required release-note sections.

#### Scenario: GitHub returns an incomplete page set

- **WHEN** the workflow cannot verify that it received every page in the selected interval
- **THEN** the workflow reports the incomplete input and leaves the draft unchanged

### Requirement: Historical Transition

The first release draft MUST preserve every entry from the current `CHANGELOG.md`. It MUST record the commit that ends the imported history.

Release automation MUST be the only process that generates repository changelog output. Feature pull requests MUST NOT modify `CHANGELOG.md`.

#### Scenario: The first release migrates existing history

- **WHEN** the repository has no earlier release boundary
- **THEN** the first draft contains the current changelog history and its cutover commit

#### Scenario: A release needs repository changelog output

- **WHEN** the owner selects a release format that includes repository changelog output
- **THEN** the release workflow generates that output from the compiled release body

### Requirement: Changelog Ownership Gate

The changelog ownership gate MUST report each feature pull request that changes `CHANGELOG.md`. The gate MUST ship at warning severity.

Its declared-debt baseline MUST list each open pull request head that contains an existing change. The baseline MUST shrink as those heads close.

The gate MUST move to blocking after the baseline is empty. The Skeleton payload MUST omit the file before this move.

Deck MUST also receive the related Copier update before this move.

#### Scenario: An existing feature pull request changes the changelog

- **WHEN** a baseline head changes `CHANGELOG.md` during the warning phase
- **THEN** the gate reports the declared debt at warning severity

#### Scenario: The flip condition becomes true

- **WHEN** the baseline is empty, the Skeleton payload omits the file, and Deck contains the Copier update
- **THEN** the gate moves to blocking severity for later feature changes

### Requirement: Ceremony Delivery

The release ceremony MUST satisfy the existing `Governance ships through its own flow` requirement in the artifact-lifecycle specification.

#### Scenario: Deck receives the release ceremony

- **WHEN** the Skeleton release ceremony passes review
- **THEN** Copier delivers the same ceremony files to Deck
