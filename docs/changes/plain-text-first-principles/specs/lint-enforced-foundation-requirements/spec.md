## ADDED Requirements

### Requirement: Analysis Tool Coverage

The *[coverage][COVERAGE]* MUST bind every requirement of every foundation capability to the check that enforces it, or to a *[missed requirement][MISSEDREQUIREMENT]*.
An enforcing check is one run of an *[analysis tool][ANALYSISTOOL]* from the shared hook configuration. A new tool starts at warning level with a recorded *[analysis baseline][ANALYSISBASELINE]*.

#### Scenario: Foundation requirement has no row

- **WHEN** a foundation capability gains a requirement and the [coverage][COVERAGE] table has no row for it
- **THEN** verification fails until a row states the check or the [missed requirement][MISSEDREQUIREMENT]

#### Scenario: Missed requirement gains a check

- **WHEN** an [analysis tool][ANALYSISTOOL] arrives for a requirement whose row states a [missed requirement][MISSEDREQUIREMENT]
- **THEN** the row switches to the tool, and the tool reports at warning level until its baseline is empty

### Requirement: Analysis Tool Has Fixtures

Every [analysis tool][ANALYSISTOOL] the *[repository][REPOSITORY]* depends on MUST have one *[fixture][FIXTURE]* it accepts and one it rejects, with the expected result asserted. A change to an *[analysis rule][ANALYSISRULE]* that alters the asserted result fails the test.
Where [fixtures][FIXTURE] are files, the directory name states the assertion: one directory holds the accepted [fixtures][FIXTURE] and one the rejected ones.

#### Scenario: Analysis tool arrives without fixtures

- **WHEN** an [analysis tool][ANALYSISTOOL] is added to the [repository][REPOSITORY] without a passing and a failing [fixture][FIXTURE]
- **THEN** the [coverage][COVERAGE] table lists the tool as a [missed requirement][MISSEDREQUIREMENT] until the [fixtures][FIXTURE] exist

#### Scenario: Analysis rule is weakened

- **WHEN** an [analysis rule][ANALYSISRULE] a tool enforced is removed
- **THEN** the failing [fixture][FIXTURE] passes, and the [fixture][FIXTURE] test fails

### Requirement: Record Cites Its Proofs

An accepted decision record MUST list the *[proofs][PROOF]* of the scenarios under the requirements it points at. A record whose scenarios have no [proof][PROOF] MUST stay proposed.
The `record-proof-per-scenario` capability says how a [proof][PROOF] is recorded and replayed. This requirement only asks that the record cites it.

#### Scenario: Record is accepted without proof

- **WHEN** a record's status changes to accepted and one scenario under a requirement it points at has no [proof][PROOF]
- **THEN** the check refuses the status and lists the scenarios without a [proof][PROOF]

[COVERAGE]: ../../../../specs/glossary/coverage.md
[MISSEDREQUIREMENT]: ../../../../specs/glossary/missed-requirement.md
[ANALYSISTOOL]: ../../../../specs/glossary/analysis-tool.md
[ANALYSISBASELINE]: ../../../../specs/glossary/analysis-baseline.md
[REPOSITORY]: ../../../../specs/glossary/repository.md
[FIXTURE]: ../../../../specs/glossary/fixture.md
[ANALYSISRULE]: ../../../../specs/glossary/analysis-rule.md
[PROOF]: ../../../../specs/glossary/proof.md
