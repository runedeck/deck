## ADDED Requirements

### Requirement: New branch checks start at the merge base

The *[validator][VALIDATOR]* MUST select one commit range for every check stage of a push or a pull request. A pull request's range MUST start at its base. A push that carries the earlier head of its branch MUST start there. The first push of a branch, which carries no earlier head, MUST start at the branch's merge base with the default branch. The validator MUST inspect every file only when no start commit exists, as on a push to the default branch with no earlier head.

#### Scenario: New branch arrives without an earlier head

- **WHEN** the first push of a branch other than the default branch arrives
- **THEN** the [validator][VALIDATOR] inspects the files that differ between the branch's merge base with the default branch and its head
- **AND** a hook that needs a desktop tool runs only when the branch changes a file it watches

#### Scenario: Default branch arrives without an earlier head

- **WHEN** a push to the default branch carries no earlier head
- **THEN** the [validator][VALIDATOR] inspects every file

#### Scenario: Later push carries its earlier head

- **WHEN** a later push to a branch carries its earlier head
- **THEN** the [validator][VALIDATOR] inspects the files that differ between that head and the new head

[VALIDATOR]: ../../../../specs/glossary/validator.md
