## ADDED Requirements

### Requirement: ForgeCycle routes one stage per turn

ForgeCycle MUST read the change's task state, print the stage strip, name the next DECK-0008 stage and the skill that owns it, and end its turn. It MUST NOT invoke a workflow tool or a workflow skill itself. It MUST return to the implement stage on adversary findings, lint failure, or requested changes, to the decision stage on a design flaw, and MUST stop and report when the owner closes the pull request or the owning skill is absent in the harness.

#### Scenario: Adversary reports a design flaw

- **WHEN** AdversaryReview marks a fatal hit as a design flaw
- **THEN** ForgeCycle names ArchitectureDecision as the next stage, not implementation

#### Scenario: Owner closes the pull request

- **WHEN** the pull request is closed without merge
- **THEN** ForgeCycle stops and reports, and does not name an implementation stage

#### Scenario: Owning skill is absent

- **WHEN** the next stage's skill is not installed in the harness
- **THEN** ForgeCycle reports the missing skill and ends the turn
