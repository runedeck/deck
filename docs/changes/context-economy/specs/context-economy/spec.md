## ADDED Requirements

### Requirement: Rule Shape

A core rule MUST state one imperative instruction within 50 words. A rule MAY carry one example pair when the sentence alone misleads.

#### Scenario: A rule exceeds the budget

- **WHEN** a changed rule does not contain exactly one imperative instruction or exceeds 50 words
- **THEN** the rule-budget gate reports the violation

### Requirement: One Home Per Fact

An instruction in the canonical Rune tree MUST live in exactly one rune. The duplication sweep MUST inspect Markdown files under `runes/`.

A duplicated sentence outside the declared baseline is a violation.

#### Scenario: A rule repeats a skill instruction

- **WHEN** a changed rule repeats a sentence from a skill, and the baseline does not declare the pair
- **THEN** the duplication sweep reports both locations

### Requirement: No Performance Personas

A rune MUST NOT frame capability through a persona. Voice guidance for outward-facing text is permitted and MUST NOT claim expertise as capability.

#### Scenario: A skill adds an expert persona

- **WHEN** a changed rune matches a persona pattern
- **THEN** the persona lint reports the violation with the study citation

### Requirement: Positive Instruction

An instruction MUST state the wanted behavior. Negation is permitted only for a true prohibition.

#### Scenario: Negation density rises

- **WHEN** a changed rune exceeds the negation-density threshold
- **THEN** the negation lint reports the count at warning severity

### Requirement: Adversarial Review

Multi-agent verification MUST use an adversarial reviewer that attempts to refute each finding against the source. A consensus council MUST NOT gate a decision.

The reviewer MUST accept a finding only after a completed review finds no counterexample. A reviewer fault MUST return a non-accepting result.

#### Scenario: A claim needs verification

- **WHEN** a review claim needs a second opinion
- **THEN** an adversarial reviewer attempts to refute it against the source and accepts it only after a completed review finds no counterexample

#### Scenario: The reviewer does not complete

- **WHEN** the reviewer times out, crashes, receives cancellation, or returns no result
- **THEN** verification reports a reviewer fault and does not accept the finding

### Requirement: Gate Ratchet

Every gate in this capability MUST ship at warning severity with a declared-debt baseline and a recorded flip condition.

#### Scenario: A gate would fail existing files

- **WHEN** a new gate fires on files main already contains
- **THEN** the violations enter the baseline and the gate stays at warning
