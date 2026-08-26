## ADDED Requirements

### Requirement: Pushback before scaffold

An intake pass MUST challenge the raw idea against existing specifications, decision records, and advisory memory before any scaffold exists. The pass MUST end in one of three outcomes: a sharpened intent, a merge into an existing change, or a rejection with reasons.

#### Scenario: An idea duplicates an existing capability

- **WHEN** a raw idea restates behavior an existing specification already requires
- **THEN** the intake pass points at the existing capability and scaffolds nothing

#### Scenario: An idea survives pushback

- **WHEN** the challenge pass leaves a sharpened intent standing
- **THEN** the pass scaffolds a spec change with `rune spec propose` and records the intent in the proposal

### Requirement: Blast radius decides depth

The intake pass MUST size the change before scaffolding. A micro-change (prose, one artifact, no machinery) MAY skip the specification. A machinery change MUST carry a specification. A decision with alternatives MUST carry a decision record.

#### Scenario: A one-line rule wording fix arrives

- **WHEN** the idea changes prose in one artifact and no contract
- **THEN** the pass routes it as a direct change without a specification

### Requirement: Any medium, one entry point

The intake pass MUST accept the idea as text regardless of origin medium. A voice transcript, a sketch description, and written prose enter the same pass unchanged.

#### Scenario: A voice transcript enters

- **WHEN** a transcript with filler and repetition enters intake
- **THEN** the pushback pass extracts the intent, and the origin medium changes nothing downstream
