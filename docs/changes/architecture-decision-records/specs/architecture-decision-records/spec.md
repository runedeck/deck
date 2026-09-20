## ADDED Requirements

### Requirement: Record Per Decision

An architectural decision with alternatives MUST become a dated record in `docs/decisions/` with a status lifecycle from proposed to accepted to superseded.

#### Scenario: Machinery change arrives without a record

- **WHEN** a change picks between architectural alternatives and adds no decision record
- **THEN** review requests the record before the merge

### Requirement: Record Shape

A record MUST follow the structured-madr shape: a context and problem statement, considered options, and a decision outcome. The directory schema validates the shape.

#### Scenario: Record misses its outcome

- **WHEN** a record lacks the Decision Outcome section
- **THEN** the schema check reports the record

### Requirement: Accountability Fields

A record MUST carry the RACI fields: responsible, accountable, consulted, and informed. Accountable names who approves the decision.

#### Scenario: Record omits accountability

- **WHEN** a changed record carries no accountable entry
- **THEN** the schema check reports the missing field

### Requirement: Provenance Fields

A record MUST carry an upstream list for its sources and a related list for its neighbor records. An empty list is a statement, never an omission.

#### Scenario: Record adopts an external practice

- **WHEN** a record's decision follows an external source
- **THEN** the upstream list names the source

### Requirement: Record states its rules

A record MUST state what its change wants as MUST statements in the Decision Outcome. A change that adds one skill still writes a record.

#### Scenario: Change adds one skill

- **WHEN** a change adds a skill and weighs no architectural alternative
- **THEN** the change still carries a record, and the record names the rules the skill must keep

### Requirement: Record lives in its change until archive

A draft record MUST live in the change directory as `adr.md`. Archive MUST move it to `docs/decisions/` and MUST assign its id at that moment.

#### Scenario: Change archives

- **WHEN** an accepted change archives
- **THEN** its `adr.md` becomes `docs/decisions/<FAMILY>-<NNNN> <Title>.md` and the change directory holds no record

### Requirement: Change and record link both ways

A proposal MUST list its records in the `decisions` frontmatter field. A record MUST name its change in the `change` field. A check MUST fail when one side is missing.

#### Scenario: Record names no change

- **WHEN** a record in `docs/decisions/` has no `change` field and its change exists
- **THEN** the link check reports the record

### Requirement: Record ids are never reused

A new record MUST take the lowest unused number in its family. A deleted record MUST leave a gap. A check MUST fail when two records share an id.

#### Scenario: Two sessions take one number

- **WHEN** two branches each add a record with the same id and both reach one tree
- **THEN** `scripts/check-decision-numbers` fails and names both files

### Requirement: Unknown frontmatter is kept

A check MUST NOT reject a frontmatter field it does not know. The frontmatter MUST be enough to rebuild the location of the file.

#### Scenario: Record carries an extra field

- **WHEN** a record carries a field that the schema does not list
- **THEN** validation passes and the field stays
