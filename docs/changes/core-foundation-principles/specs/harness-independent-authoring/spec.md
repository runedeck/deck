## ADDED Requirements

### Requirement: Author Once

An artifact MUST have one authored source. Provider differences live in companion files, variants, or sidecars, never in forked copies.

#### Scenario: Provider needs different wording

- **WHEN** one provider needs an instruction the others do not
- **THEN** the difference goes to a provider companion or variant and the canonical artifact stays shared

#### Scenario: Divergent copies of one artifact appear

- **WHEN** two provider trees carry different content for one artifact outside the declared variants
- **THEN** the deployment check reports the drift, and reassembly from the canonical source resolves it

### Requirement: Assembled Instances

Assembly MUST resolve each artifact to one instance per provider with recorded provenance.

#### Scenario: Assembly writes a provider instance

- **WHEN** assembly deploys an artifact into a provider tree
- **THEN** the deployment manifest records its fingerprint and the provenance sidecar records its source

### Requirement: Portable Instructions

An instruction MUST use the portable form where one exists. The canonical artifact MUST work where a harness-specific mechanism is absent. Harness-specific content lives in that provider's companion.

#### Scenario: Rune depends on one harness's hook event

- **WHEN** a changed rune requires a mechanism specific to one harness
- **THEN** the requirement moves to that provider's companion and the canonical rune works without it

#### Scenario: New provider joins

- **WHEN** a new provider joins the deployment roster
- **THEN** canonical artifacts deploy without edits and only provider companions are new
