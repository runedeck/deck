## ADDED Requirements

### Requirement: A change with behavior carries a recorded proof

A change that alters user-visible behavior MUST carry one recorded scene per scenario of its delta specification, run end to end against the frozen candidate that the check receipt names. Each THEN clause MUST be asserted with an expectation on the output, and a missed expectation MUST fail the recording. The proof artifact MUST be a GIF recording with its transcript, filed under `docs/proofs/<change>/`. The pull request MUST embed the recording with the commit id it proves and MUST name every scenario without a scene as unproven. A merge check MUST warn, not block, on a scenario without a proof.

#### Scenario: Scenario has no proof at merge

- **WHEN** a pull request reaches merge with a scenario that has no scene under `docs/proofs/<change>/`
- **THEN** the check reports the scenario as unproven with a warning
- **AND** the merge proceeds

#### Scenario: Implementation is finished

- **WHEN** a session finishes an implementation whose delta specification has scenarios
- **THEN** it writes one scene per scenario with an expectation per THEN clause
- **AND** it records the scenes against the candidate that will be published

#### Scenario: Expectation misses

- **WHEN** a scene's expectation does not match the output
- **THEN** the driver exits nonzero and the recording fails
- **AND** the fix goes into the candidate and the recording runs again

#### Scenario: Proof is filed

- **WHEN** the recording passes
- **THEN** the GIF is committed under `docs/proofs/<change>/` and the pull request's Testing section embeds it with the commit id
- **AND** the proof record carries the scenario list, the recording exit status, and the transcript digest

#### Scenario: Change has no behavior

- **WHEN** a change alters only prose or configuration with no user-visible behavior
- **THEN** the pull request states that no behavior proof applies
