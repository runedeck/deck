## ADDED Requirements

### Requirement: Prose Seal Renewal

A mechanical prose correction to a sealed file SHALL be followed by `rune adopt reseal` for that artifact, and the reseal SHALL preserve the source and review facts while rewriting the subject digest.

#### Scenario: Sealed file changes after prose correction

- **WHEN** a sealed file's bytes change through a punctuation or contraction correction
- **THEN** its sidecar records the new subject digest with the original review state and the adoption doctor reports no error

#### Scenario: Deliberate prose samples stay untouched

- **WHEN** a file holds deliberate before-and-after prose errors
- **THEN** the Vale configuration exempts that path from the sentence rules instead of the file being edited
