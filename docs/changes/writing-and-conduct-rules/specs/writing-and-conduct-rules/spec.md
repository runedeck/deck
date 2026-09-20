## ADDED Requirements

### Requirement: Deployed rule has a deck source

A rule that the owner runs from a deployed copy MUST have its source in the deck. The deployed text MUST equal the text that `rune install` writes from that source.

#### Scenario: Fresh machine installs the deck

- **WHEN** a fresh machine runs `rune install` with the `core` cast
- **THEN** each of these rules is deployed with the same text the owner runs today

### Requirement: Rule beside a linter stays

A short rule MUST stay in the deck when a linter checks the same property. The rule steers what the model writes, and the linter checks what it wrote.

#### Scenario: Linter already covers the property

- **WHEN** a Vale rule fails on an em-dash and the NoEmDash rule states the same preference
- **THEN** both stay, and the rule is not removed as a duplicate

### Requirement: Rule pays for its tokens

Each rule MUST get one bench run against a baseline with no rule. A rule with no measured effect MUST leave the default casts.

#### Scenario: Bench shows no effect

- **WHEN** a bench run shows the same result with the rule and without it
- **THEN** the rule leaves the `core` cast, and its verdict records the result
