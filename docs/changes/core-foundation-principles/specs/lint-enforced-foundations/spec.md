## ADDED Requirements

### Requirement: Analysis Tool Coverage

The *coverage* [COVERAGE] MUST bind every requirement of every foundation capability to the check that enforces it, or to an *missed requirement* [MISSED-REQUIREMENT].
An enforcing check is one run of an *analysis tool* [ANALYSISTOOL] from the shared hook configuration. A new tool starts at warning level with a recorded *analysis baseline* [ANALYSISBASELINE].

#### Scenario: Foundation requirement has no row

- **WHEN** a foundation capability gains a requirement and the coverage table has no row for it
- **THEN** verification fails until a row states the check or the missed requirement

#### Scenario: Missed requirement gains a check

- **WHEN** an analysis tool arrives for a requirement whose row states a missed requirement
- **THEN** the row switches to the tool, and the tool reports at warning level until its baseline is empty

### Requirement: Analysis Tool Has Fixtures

Every analysis tool the deck depends on MUST have one *fixture* [FIXTURE] it accepts and one it rejects, with the expected result asserted. A change to an *analysis rule* [ANALYSISRULE] that alters the asserted result fails the test.
Where fixtures are files, the directory names `valid/` and `invalid/` state the assertion.

#### Scenario: Analysis tool arrives without fixtures

- **WHEN** an analysis tool is added under `scripts/` without a passing and a failing fixture
- **THEN** the coverage table lists the tool as a missed requirement until the fixtures exist

#### Scenario: Analysis rule is weakened

- **WHEN** an analysis rule a tool enforced is removed
- **THEN** the failing fixture passes, and the fixture test fails

### Requirement: Record Cites Its Proofs

An accepted decision record MUST list the *proofs* [PROOF] of the scenarios under the requirements it points at. A record whose scenarios have no proof MUST stay proposed.
The `prove-each-scenario` capability says how a proof is recorded and replayed. This requirement only asks that the record cites it.

#### Scenario: Record is accepted without proof

- **WHEN** a record's status changes to accepted and one scenario under a requirement it points at has no proof
- **THEN** the check refuses the status and lists the scenarios without a proof

[COVERAGE]: https://runedeck.ai/ns#Coverage
[PROOF]: https://runedeck.ai/ns#Proof
[MISSED-REQUIREMENT]: https://runedeck.ai/ns#MissedRequirement
[ANALYSISTOOL]: https://runedeck.ai/ns#AnalysisTool
[ANALYSISRULE]: https://runedeck.ai/ns#AnalysisRule
[ANALYSISBASELINE]: https://runedeck.ai/ns#AnalysisBaseline
[FIXTURE]: https://runedeck.ai/ns#Fixture
