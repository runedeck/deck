## ADDED Requirements

### Requirement: Consumer Reference Recovery

The deck SHALL record in `answers.yaml` a skeleton commit that resolves on the skeleton repository, and each Copier update SHALL move from that commit to the new one.

#### Scenario: Consumer pin names the new skeleton commit

- **WHEN** a Copier update from the recorded commit completes
- **THEN** `answers.yaml` records the new skeleton commit and the parity audit resolves it

### Requirement: Consumer Additions

The deck SHALL carry its own checks as additions on top of the template's hook list, Makefile targets, lint excludes, and Quality steps, and a Copier update SHALL preserve them.

#### Scenario: Copier update preserves declared additions

- **WHEN** a template change touches a file that carries a deck addition
- **THEN** the merged file keeps the template change and the addition

### Requirement: Provenance Test Execution

Quality SHALL run the provenance digest tests beside the attribution and push check tests.

#### Scenario: Quality runs provenance tests

- **WHEN** Quality runs on a push or pull request
- **THEN** the provenance digest tests run before the commit-stage checks
