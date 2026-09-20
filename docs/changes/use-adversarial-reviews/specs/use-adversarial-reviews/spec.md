## ADDED Requirements

### Requirement: Workflow script is a file

A workflow skill MUST keep its script in `workflow.js` beside `SKILL.md`. The script MUST declare `meta.caps` with a total agent ceiling of 32 or less and a finite loop ceiling, MUST refuse to spawn past either, MUST NOT call a workflow tool from a child, and MUST check `.ok` on every agent result. The model MUST pass the file verbatim to the workflow tool, with `args` carrying the change id when one exists.

#### Scenario: Skill is invoked

- **WHEN** a workflow skill fires
- **THEN** the script passed to the tool is byte-identical to `workflow.js` and `args` carries the change id when one exists

#### Scenario: Cap is reached

- **WHEN** the next `agent()` call would exceed `meta.caps`
- **THEN** the script stops the phase and reports the cap in its result

### Requirement: Workflow skills stop without a workflow tool

A workflow skill MUST deploy only to harnesses with a workflow tool, and the deployment filter MUST be verified before the change merges. The skill MUST stop with one sentence when the tool is absent.

#### Scenario: Skill reaches a harness without the tool

- **WHEN** the skill body is loaded in a harness with no workflow tool
- **THEN** the model reports that the skill needs a workflow tool and makes no attempt to simulate the run

### Requirement: Children inherit the prohibitions

Every child brief MUST restate the RemoteWrites command list without the label exception, and MUST name the absolute path of the skill directory for companions.

#### Scenario: Repair child finishes

- **WHEN** a MergeTrain repair child clears a blocker
- **THEN** it stops with the workspace path and the changed files, and no remote state has changed

### Requirement: AdversaryReview refutes the original

AdversaryReview MUST attack the original text, MUST NOT rewrite before the attack, and MUST record for every hit a disposition of fixed or rejected with a stated reason. A hit that is neither fixed nor refuted MUST remain open in the report.

#### Scenario: Non-fatal hit

- **WHEN** an attack child marks a hit non-fatal
- **THEN** the settle step still records fixed or rejected with reason for it
