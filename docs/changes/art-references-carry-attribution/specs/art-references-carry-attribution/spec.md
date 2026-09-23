## ADDED Requirements

### Requirement: Art references carry attribution

The Art skill MUST record the source and the artist of every reference it collects. A collection entry without attribution MUST be marked incomplete.

#### Scenario: Reference enters a collection

- **WHEN** the skill adds a reference to a collection
- **THEN** the entry names the source URL and the artist, or is marked incomplete

### Requirement: Palette critique is independent

The PaletteCritic agent MUST review a proposed palette against the references, the material behavior, and the stated constraints. It MUST NOT propose a palette of its own.

#### Scenario: Palette is handed over

- **WHEN** the Art skill hands a palette to PaletteCritic
- **THEN** the critic returns findings against the references and constraints, and proposes no replacement palette
