## ADDED Requirements

### Requirement: New runes start as registered drafts

A session that starts a new skill, agent, or rule for a consumer MUST register it as a draft and MUST NOT write it by hand into a provider directory. The deployer writes the draft where the harness loads it and records it in the consumer's draft register. The session MUST edit the draft in place and MUST ask the validator to confirm the registration before it decides to promote or drop it.

#### Scenario: Session starts a skill

- **WHEN** a session needs a skill that the deck does not carry
- **THEN** it registers a draft skill at the consumer root and edits the file the deployer reports

#### Scenario: Session finds an unregistered file

- **WHEN** the validator reports a hand-written rune as an orphan
- **THEN** the session moves the file aside, registers a draft of the same kind and name, and puts the body into the registered copy

### Requirement: Promotion opens the change

The session MUST promote a draft that earned its place into a named domain under a change id of at least three lowercase hyphenated words. Promotion moves the draft into the repository and opens the change directory. The session MUST then continue in the repository with BuildSkill for the rune body and with the change's proposal, tasks, and decision record. The session MUST drop a draft that did not earn its place, which removes every provider copy and its register entry.

#### Scenario: Draft is promoted

- **WHEN** the session promotes the draft ReviewSpec into the core domain under the change id review-spec-interaction
- **THEN** the repository holds the ReviewSpec skill under the core domain and a change directory named review-spec-interaction, and the consumer's draft register lists no drafts

#### Scenario: Draft is dropped

- **WHEN** the session drops the draft
- **THEN** every provider copy and the `.drafts` entries are gone and the validator's verification pass reports no findings
