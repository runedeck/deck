## ADDED Requirements

### Requirement: Remote writes belong to the owner

An agent MUST NOT run `gh pr merge`, `gh pr close`, `gh pr comment`, `gh pr review`, `gh pr edit --add-label`, `gh pr edit --remove-label`, `gh issue comment`, `gh issue close`, `git push`, `jj git push`, or a review-thread resolution call, and MUST NOT reach the same effects through the API. The one exception is the single review label the invoking prompt names, and it belongs to the invoking agent only, never to a child. The rule MUST load in every harness where rune installs core rules. Where rune has no rules path yet, the harness's `AGENTS.md` MUST carry the same list until the assembly target exists.

#### Scenario: Routine session finishes a fix

- **WHEN** a session with no workflow skill loaded finishes a code fix
- **THEN** it runs none of the listed commands and reports what the owner can push

#### Scenario: Prompt names a review label

- **WHEN** the prompt says to summon a reviewer with a named label
- **THEN** the invoking agent adds exactly that label and touches no other label

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

### Requirement: Storyboard frames precede writes

Before the first file write of a stage, Storyboard MUST show an ASCII frame and wait for the owner's confirmation. When a change directory exists, the first frame MUST be the change map with the current stage marked. A correction from the owner MUST produce a redrawn frame before any write. Each stage MUST end with a frame of what changed. Confirmed frames MUST be saved under `docs/changes/<id>/storyboard/` in order, after confirmation, and MUST use one glyph set at 78 columns or less. The question uses the harness's question tool when one exists and a plain question otherwise.

#### Scenario: Change directory exists

- **WHEN** a session starts work inside a change
- **THEN** the first frame is the change map with the current stage marked, and the session waits for confirmation

#### Scenario: Owner edits a box

- **WHEN** the owner answers with a correction to the frame
- **THEN** the frame is redrawn and shown again before any write

#### Scenario: Stage ends

- **WHEN** a stage finishes
- **THEN** a delta frame is shown and saved as the next numbered file
