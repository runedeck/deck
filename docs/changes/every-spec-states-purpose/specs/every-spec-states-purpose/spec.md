## ADDED Requirements

### Requirement: Canonical specs are self-describing

Every canonical specification in the canonical tree MUST open with an H1 of the form `<Directory Name> Specification` in title case and a Purpose paragraph written for that capability. A Purpose MUST NOT be an archive placeholder. A rule MUST appear in one requirement only. A second capability that depends on it MUST point at the first.

#### Scenario: Archive creates a placeholder

- **WHEN** the archiver writes a placeholder purpose into a canonical specification
- **THEN** the archiving change replaces it before the archive commit lands

#### Scenario: Two specs state one rule

- **WHEN** two canonical specs carry the same MUST with the same scenario
- **THEN** one keeps the rule and the other points at it by relative link
