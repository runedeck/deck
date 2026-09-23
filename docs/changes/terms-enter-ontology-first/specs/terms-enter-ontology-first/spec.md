## ADDED Requirements

### Requirement: Terms enter the ontology before prose

A term that names a concept MUST exist in `ontology/rune.ttl` before a spec, a decision record, or a skill uses it. A minted class MUST declare a superclass from an established vocabulary, and a minted scheme MUST use SKOS. A new class MUST be recorded in a decision record.

#### Scenario: New concept appears in a change

- **WHEN** a change needs a name for a concept the ontology does not hold
- **THEN** the change adds the term to `ontology/rune.ttl` with a label, a comment, and a superclass
- **AND** it adds a shape at Warning severity and a seeded smoke instance the shape reports

#### Scenario: Established term fits

- **WHEN** an established vocabulary already defines the concept
- **THEN** the change reuses that IRI and mints nothing

### Requirement: Artifacts are named from the lifecycle

A skill name MUST be the verb of the lifecycle stage it serves, or an established discipline noun, plus the entity the stage consumes. A name MUST NOT name a category instead of an act, and MUST NOT start with a marketing adjective.

#### Scenario: Skill is named

- **WHEN** a new skill is proposed
- **THEN** its name is derived from the stage table and recorded there

### Requirement: The prove stage produces a proof

A `rune:Proof` MUST name the candidate commit it covers and exactly one kind of proof. A candidate is proven when a proof exists for its commit, which MUST be computed as a query and MUST NOT be stored as a state.

#### Scenario: Proof lacks a commit or a kind

- **WHEN** the shapes validate a proof without `rune:proves` or without one `rune:proofKind`
- **THEN** the report carries one Warning per missing property

### Requirement: Drift is audited and retired

The corpus MUST be auditable for synonyms of a label and for labels of a word, reported as a density with the target one. A retired term MUST be deprecated with its label kept as an alternative label for one release before removal.

#### Scenario: Two words name one concept

- **WHEN** the audit finds two terms for one concept
- **THEN** one label survives, every use of the other is replaced in one change, and the other is deprecated
