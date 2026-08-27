## ADDED Requirements

### Requirement: Draft in the shared register

A drafted change MUST use Simplified Technical English and the repository's markdown schemas. The draft MUST define each term of art on first use or link the definition.

#### Scenario: A draft leaves the register

- **WHEN** a drafted document violates the STE style or its mdschema
- **THEN** the write-time lint reports the violation before any commit

### Requirement: Deterministic pass precedes review

Every deterministic check MUST run and pass before a human reads the draft. The owner reviews content, never formatting, spelling, schema, or link health.

#### Scenario: A draft reaches the owner

- **WHEN** a draft is presented for owner review
- **THEN** the write-time lints, `rune spec validate`, and the commit-stage hooks have already passed on it

### Requirement: Review points by blast radius

A decision-bearing or xlarge change MUST get a draft review before its pull request. A smaller change MAY go straight to the pull request, where the ceremony provides the review.

#### Scenario: A decision-bearing change is drafted

- **WHEN** a change carries a decision record or an xlarge label
- **THEN** the owner reviews the draft before any push, and the pull request review sees final form with the adversarial verdict beside it
