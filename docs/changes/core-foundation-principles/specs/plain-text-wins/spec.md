## ADDED Requirements

### Requirement: Plain Text Representation

Every artifact a model reads MUST have an authoritative UTF-8 plain-text representation that carries its meaning directly. An encoding wrapper such as base64 does not qualify. Other stores MAY hold derived forms, and the model-facing representation stays plain text.

#### Scenario: External store appears

- **WHEN** a change introduces a database or an index over artifact content
- **THEN** the store derives from the plain-text source, and everything the model reads stays plain text

### Requirement: Lossless Derived Forms

A committed derived form of a plain-text source MUST regenerate from that source without loss. A derived form nothing regenerates is a second home for the facts and a drift risk.

#### Scenario: Derived form drifts from its source

- **WHEN** a committed derived form no longer matches a regeneration from its source
- **THEN** a check reports the drift, and the source wins
