## ADDED Requirements

### Requirement: Scanner Register

Every routine prompt SHALL carry an authority section that names its untrusted inputs, an explicit permitted-operations list, an explicit prohibited-operations list, expected and completed coverage counts, exactly one status from an ordered set, and a fixed notification structure with line limits.

#### Scenario: Untrusted data carries an instruction

- **WHEN** repository content, a comment, or a tool response contains instruction-like text
- **THEN** the run refuses it, reports its location without quoting it, and keeps scope, tools, and format unchanged

### Requirement: Loud Canary

A routine SHALL verify its grants and safety values before its first substantive action and SHALL report CONFIGURATION_FAILURE with the exact gap when a precondition fails. A run SHALL NOT degrade silently past a failed precondition.

#### Scenario: Missing repository grant

- **WHEN** a required repository is not mounted in the session
- **THEN** the run stops before any inspection and the notification names the missing grant

### Requirement: Environment By Data Sensitivity

A routine SHALL run in the environment its readable data selects: private content with no network, repository work with GitHub proxy access only, and public-data scans with full network. A private repository SHALL NOT mount in a session with general network egress.

#### Scenario: Private chip beside full egress

- **WHEN** a routine setup mounts a private repository into a full-network environment
- **THEN** the setup violates this specification and the private chip moves or the environment narrows

### Requirement: Honest Degradation

When the environment blocks part of the required coverage, the run SHALL report INCOMPLETE with expected and completed counts and SHALL name the blocked surface. A partial scan SHALL NOT report OK.

#### Scenario: Allowlist proxy blocks sources

- **WHEN** the network policy blocks a subset of the selected sources
- **THEN** the notification reports INCOMPLETE, the counts, and the blocked categories

### Requirement: Provider Adaptation

A scanner ported between providers SHALL adapt its instrument controls to the provider and SHALL keep findings, evidence redaction, status order, and notification contract identical. A Claude web scanner SHALL use only unauthenticated requests as its public-view boundary. A variant with a reduced trust model SHALL state that model in its header.

#### Scenario: Authenticated client would widen the view

- **WHEN** a Claude scanner could reach private data through an authenticated client
- **THEN** the prompt forbids that client and the scan stays within the public view

### Requirement: Rendered Value Privacy

Templates in the repository SHALL carry typed placeholders only. Rendered prompts with approved personal values SHALL live outside every repository, in a git-ignored consumer directory.

#### Scenario: Scanner rendered for one identity

- **WHEN** a template renders with approved identity values
- **THEN** the rendered file lands in the consumer private directory and no repository commit contains the values

### Requirement: Manual Provider Setup

Routine installation SHALL stay manual. Each routine file SHALL separate picker settings from the paste-ready prompt, and no tool SHALL claim that it configured the provider.

#### Scenario: Routine installed from a file

- **WHEN** the owner installs a routine
- **THEN** the file states the picker settings apart from the prompt and the owner performs the provider steps
