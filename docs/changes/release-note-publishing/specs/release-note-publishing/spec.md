## ADDED Requirements

### Requirement: Release Interval

The compiler MUST read the post-merge `merge_commit_sha` from the [GitHub pull request API](https://docs.github.com/en/rest/pulls/pulls#get-a-pull-request). This SHA is the target-branch incorporation commit.

The compiler MUST select each merged pull request by its target-branch incorporation commit. The previous release commit MUST be the exclusive interval boundary.

The target commit MUST be the inclusive interval boundary. Each selected incorporation commit MUST be reachable from the target commit.

#### Scenario: A later release selects its interval

- **WHEN** a pull request incorporation commit is in the interval after the previous release commit through the target commit
- **THEN** the compiler selects each eligible pull request once
- **AND** the compiler excludes pull requests outside that commit interval

#### Scenario: A squash merge changes the commit identity

- **WHEN** a squash merge adds an incorporation commit that differs from the pull request head
- **THEN** the compiler uses the incorporation commit for interval selection

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

#### Scenario: A selected pull request has invalid release notes

- **WHEN** a selected pull request lacks the `## Release Notes` heading or contains no list item under it
- **THEN** the workflow reports that pull request, fails validation, and leaves the draft unchanged

### Requirement: Historical Transition

The owner MUST select the initial history cutover commit. The first draft MUST compile notes after that commit through the target commit.

The compiled notes MUST come first. The exact `CHANGELOG.md` body at the cutover commit MUST follow without reordered headings or entries.

The draft metadata MUST record the cutover commit. The workflow MUST apply the owner-selected `CHANGELOG.md` state after it creates the draft.

The selected state MUST delete the file or replace its full contents with one heading and one link to the repository Releases page.

Release automation MUST be the only process that generates repository changelog output. Feature pull requests MUST NOT modify `CHANGELOG.md`.

#### Scenario: The first release migrates existing history

- **WHEN** the repository has no earlier release boundary and the owner selects the cutover commit and file state
- **THEN** the first draft contains compiled interval notes followed by the exact changelog body and cutover metadata
- **AND** the workflow applies the selected file state

#### Scenario: A release needs repository changelog output

- **WHEN** the owner selects a release format that includes repository changelog output
- **THEN** the release workflow generates that output from the compiled release body

### Requirement: Changelog Ownership Gate

The changelog ownership gate MUST report each feature pull request that changes `CHANGELOG.md`. The gate MUST ship at warning severity.

The gate MUST seed its declared-debt baseline once. Each entry MUST contain an open pull request number and its current head SHA.

On each evaluation, the gate MUST refresh the SHA only for a seeded pull request that stays open and changes `CHANGELOG.md`.

The gate MUST remove an entry when its pull request closes or stops changing `CHANGELOG.md`. It MUST NOT add or restore debt after seeding.

The gate MUST move to blocking after the baseline is empty. The Skeleton payload MUST omit the file before this move.

Deck MUST also receive the related Copier update before this move.

#### Scenario: An existing feature pull request changes the changelog

- **WHEN** a baseline head changes `CHANGELOG.md` during the warning phase
- **THEN** the gate reports the declared debt at warning severity

#### Scenario: A baseline pull request changes its head

- **WHEN** a seeded pull request receives a new head that still changes `CHANGELOG.md`
- **THEN** the gate refreshes that entry to the new head SHA and reports the declared debt

#### Scenario: The flip condition becomes true

- **WHEN** the baseline is empty, the Skeleton payload omits the file, and Deck contains the Copier update
- **THEN** the gate moves to blocking severity for later feature changes

### Requirement: Ceremony Delivery

The release ceremony MUST satisfy the existing `Governance ships through its own flow` requirement in the artifact-lifecycle specification.

#### Scenario: Deck receives the release ceremony

- **WHEN** the Skeleton release ceremony passes review
- **THEN** Copier delivers the same ceremony files to Deck
