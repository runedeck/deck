## ADDED Requirements

### Requirement: Pushback before scaffold

An intake pass MUST challenge the raw idea against existing specifications, decision records, and advisory memory before any scaffold exists. The pass MUST end in one of three outcomes: a sharpened intent, a merge into an existing change, or a rejection with reasons.

#### Scenario: An idea duplicates an existing capability

- **WHEN** a raw idea restates behavior an existing specification already requires
- **THEN** the intake pass points at the existing capability and scaffolds nothing

#### Scenario: An idea survives pushback

- **WHEN** the challenge pass leaves a sharpened intent standing
- **THEN** the pass creates the change directory and records the intent in its proposal

### Requirement: Blast radius decides depth

The intake pass MUST size the change before scaffolding. A micro-change (prose, one artifact, no machinery) MAY skip the specification. A machinery change MUST carry a specification. A decision with alternatives MUST carry a decision record.

#### Scenario: A one-line rule wording fix arrives

- **WHEN** the idea changes prose in one artifact and no contract
- **THEN** the pass routes it as a direct change without a specification

### Requirement: Any medium, one entry point

The intake pass MUST accept the idea in the form it arrives: a transcript, pasted or linked, a link to a drawing in the owner's vault, or a short written prompt. Every medium is optional and none is required. The pass MUST read each medium through its own reader and MUST continue with one text, so the origin medium changes nothing downstream.

#### Scenario: A voice transcript enters

- **WHEN** a transcript with filler and repetition enters intake
- **THEN** the pushback pass extracts the intent, and the origin medium changes nothing downstream

#### Scenario: A drawing link enters

- **WHEN** a vault link to a drawing enters intake
- **THEN** the pass reads the drawing through the Obsidian CLI, origin on the left, and the record's `upstream` lists the link

#### Scenario: Prompt enters alone

- **WHEN** one short written prompt enters intake with no recording and no drawing
- **THEN** the pass runs the same interview and produces the same change as it would from a recording or a drawing

### Requirement: Interview before the scaffold

After pushback and before any file exists, the intake pass MUST interview the owner about the feature: who it serves, what is different afterwards, what must hold, what must not happen, and how the owner will know it works. The interview MUST stop when the answers state every requirement and its scenarios, and it MUST NOT exceed seven questions in one round.

#### Scenario: Idea arrives without acceptance criteria

- **WHEN** the sharpened intent states an outcome and no way to observe it
- **THEN** the interview asks for the observable result before it writes a scenario

### Requirement: Owner reviews the MUST statements and the scenarios

The intake pass MUST hand the drafted delta specification to the owner for review before the change counts as proposed. The handoff MUST list every MUST statement and every scenario, one line each, and MUST ask for a verdict on each. A change MUST NOT proceed to implementation while a MUST statement or a scenario has no verdict.

#### Scenario: Owner rejects one MUST

- **WHEN** the owner marks one MUST statement wrong in the review
- **THEN** the pass rewrites that requirement and its scenarios and asks again for that one, and the accepted ones stay unchanged
