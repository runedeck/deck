## ADDED Requirements

### Requirement: Rule Shape

A core rule MUST state one imperative instruction within 50 words. A rule MAY carry one example pair when the sentence alone misleads.

#### Scenario: A rule exceeds the budget

- **WHEN** a changed rule exceeds 50 words or states a second instruction
- **THEN** the rule-budget gate reports the violation

### Requirement: One Home Per Fact

An instruction MUST live in exactly one artifact. A duplicated sentence outside the declared baseline is a violation.

#### Scenario: A sentence appears in two runes

- **WHEN** a changed rune repeats a sentence another rune already carries, and the baseline does not declare the pair
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

Multi-agent verification MUST use an adversarial reviewer that attempts to refute each finding against the source. A consensus council MUST NOT gate a decision. A finding survives only when the refutation fails.

#### Scenario: A claim needs verification

- **WHEN** a review claim needs a second opinion
- **THEN** an adversarial reviewer attempts to refute it against the source, and the claim survives only when the refutation fails

### Requirement: Gate Ratchet

Every gate in this capability MUST ship at warning severity with a declared-debt baseline and a recorded flip condition.

#### Scenario: A gate would fail existing files

- **WHEN** a new gate fires on files main already contains
- **THEN** the violations enter the baseline and the gate stays at warning
