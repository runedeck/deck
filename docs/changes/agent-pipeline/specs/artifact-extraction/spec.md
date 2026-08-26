## ADDED Requirements

### Requirement: Every pass ends with an extraction question

A pipeline pass MUST answer "what did this pass teach" before it closes. The answer is an extracted artifact, a captured note, or an explicit "nothing". Silence is not an outcome.

#### Scenario: A pass surfaces a repeated correction

- **WHEN** the same correction appears twice in one pass
- **THEN** the pass extracts it through the leverage ladder: architecture change, then lint, then rule or skill, then review guidance

#### Scenario: A pass teaches nothing

- **WHEN** the pass ends with no repeated correction and no new procedure
- **THEN** the extraction outcome is an explicit "nothing", recorded where the pass reports

### Requirement: Extracted artifacts rejoin the lifecycle

An extracted skill, rule, or agent MUST enter the standard lifecycle: authored to schema, proven, measured, reviewed, and shipped. An extracted rule MUST carry a bench verdict before it ships, because rules cost context on every turn.

#### Scenario: An extracted rule ships

- **WHEN** an extraction produces a rule
- **THEN** the rule reaches provider trees only after a BenchArtifact verdict and a clean review round

### Requirement: Extraction feeds the next prompt

A shipped extracted artifact MUST be present in the context of later pipeline passes through the normal install path. The loop closes through deployment, not through manual recall.

#### Scenario: The next pass benefits

- **WHEN** a later idea enters intake after an extraction shipped
- **THEN** the pushback pass runs with the extracted artifact in context
