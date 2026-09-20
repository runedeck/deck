## ADDED Requirements

### Requirement: Staged lifecycle with evidence tokens

Every artifact MUST advance through the flow stages in order: Capture, Author, Prove, Measure, Review, Ship, Operate. Each stage MUST issue its evidence token before the next stage consumes the artifact. Evidence MUST be append-only.

#### Scenario: A rule reaches a provider tree

- **WHEN** a rule is installed into a provider tree
- **THEN** the rule carries a schema-validation pass, a provenance identity, a bench verdict, and a merge from a clean review round
- **AND** the consumer's deploy manifest records the deployed digest

#### Scenario: A stage input lacks the previous token

- **WHEN** an artifact reaches a stage without the previous stage's evidence token
- **THEN** the stage refuses the artifact and names the missing token

### Requirement: Provenance by ownership boundary

A third-party artifact MUST carry a sealed block-review record and an in-toto sidecar with a source pin and a subject digest. A first-party artifact MUST carry its trust in the authorship ceremony and MUST NOT require a provenance sidecar.

#### Scenario: An upstream skill is adopted

- **WHEN** an upstream skill enters the deck
- **THEN** every imported block has a recorded verdict, the review record is sealed, and the sidecar pins the source and the final digest

#### Scenario: A first-party module retires its sidecars

- **WHEN** a first-party module removes its provenance sidecars
- **THEN** the removal is a correction, and the authorship ceremony remains the module's trust anchor

### Requirement: State store contracts

The workshop, the deck, the consumer, and the provider account MUST hold only the state their store contract permits. A provider account MUST stay reproducible from the deck and the consumer alone.

#### Scenario: A provider account is rebuilt

- **WHEN** a provider account is recreated from nothing
- **THEN** rendering the shipped templates with the consumer's private values restores every routine and setting

### Requirement: Provider edge containment

Provider specifics MUST enter only at the Ship edge, through assembly configuration and overlays, and at the Operate edge, through adapted routine variants. Canonical artifacts MUST carry only Agent Skills fields plus the three assembly directives.

#### Scenario: A provider is removed

- **WHEN** a provider is dropped from the fleet
- **THEN** no canonical artifact changes

### Requirement: Governance ships through its own flow

Ceremony changes MUST land in the skeleton first, in both the repository root and the template payload, and MUST reach consumers through Copier updates. Skeleton-to-consumer drift MUST be watched by an audit routine.

#### Scenario: A ceremony check changes

- **WHEN** a ceremony workflow changes in the skeleton
- **THEN** consumers receive the change through a Copier update, and the next audit reports zero drift for that file

### Requirement: Retirement is a reviewed reverse path

Retiring an artifact MUST remove it from every store through the same review ceremony that admitted it, and MUST keep its evidence records.

#### Scenario: An artifact is retired

- **WHEN** an artifact is removed from the deck
- **THEN** a reviewed change records the reason, consumer manifests drop the entry, deployed files are pruned by manifest, and bench verdicts, review history, and decision records remain
