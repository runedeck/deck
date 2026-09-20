## ADDED Requirements

### Requirement: Change layout

A behavior change MUST live under `docs/changes/<id>/` with a proposal that states Why and What Changes, a task list, and one delta specification for each capability it touches.

#### Scenario: Change arrives without a proposal

- **WHEN** a change directory lacks a proposal or a delta specification
- **THEN** spec validation rejects the change

### Requirement: Testable requirements

A requirement MUST use MUST language and MUST carry at least one scenario with WHEN and THEN.

#### Scenario: Requirement lacks a scenario

- **WHEN** a delta carries a requirement with no WHEN and THEN scenario
- **THEN** spec validation reports the requirement

### Requirement: One canonical tree

Archive MUST merge the delta into `docs/specs/` and MUST move the change directory to `docs/changes/archive/<date>-<id>/`. Every spec CLI MUST operate on the same tree, with no mirror.

#### Scenario: Change completes

- **WHEN** an accepted change archives
- **THEN** the canonical tree carries each of its requirements exactly one time
- **AND** the change directory leaves the active set

### Requirement: Names have three words

A change id and a capability name MUST have at least three words joined by hyphens. A change with one capability MUST name it after the change id. A change with several capabilities MUST give each a name that differs from the change id.

#### Scenario: Change id has two words

- **WHEN** a commit adds `docs/changes/local-checks/`
- **THEN** the name check fails and names the directory

#### Scenario: Several capabilities share the change id

- **WHEN** a change with two capabilities names one of them after the change id
- **THEN** the name check fails and names the capability

### Requirement: Archive is acceptance

Archive MUST be the act that accepts a change. Archive MUST NOT run for a change that has no record.

#### Scenario: Change has no record

- **WHEN** a change with every task checked has no `adr.md` and lists no record in `decisions`
- **THEN** archive refuses and names the missing record

### Requirement: Owner reviews each rule before archive

Before archive, the owner MUST review each MUST statement of the delta through one scenario question with fixed options. A mismatch between the owner's answer and the requirement MUST be settled before archive.

#### Scenario: Owner's answer differs from the requirement

- **WHEN** the owner selects an option that the requirement does not state
- **THEN** the change stays active until the requirement or the answer changes
