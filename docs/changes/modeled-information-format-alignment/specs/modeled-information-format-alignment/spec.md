## ADDED Requirements

### Requirement: Vocabulary reuse before a new term

The deck ontology MUST map a new term to the MIF ontology corpus before minting one. A minted term MUST record the reason no corpus term fits.

#### Scenario: Change mints a term the corpus already defines

- **WHEN** a change adds an ontology term that a MIF corpus term already covers
- **THEN** review replaces the minted term with the mapped corpus term

### Requirement: Scoped adoption with a verdict

A MIF component MUST enter through the adoption review with provenance and a maturity note. Deck machinery MUST NOT depend on a pre-1.0 implementation.

#### Scenario: Pre-1.0 dependency is proposed

- **WHEN** a change adds a dependency on a MIF implementation below version 1.0
- **THEN** review rejects the dependency and records the maturity condition

### Requirement: Shapes decide

SHACL validation over the extracted graph MUST stay the only pass-or-fail authority. A JSON-LD projection MUST NOT decide a pass or a fail.

#### Scenario: Projection is proposed as a check

- **WHEN** a change proposes a JSON-LD document as a pass-or-fail authority
- **THEN** review routes the constraint into a SHACL shape
