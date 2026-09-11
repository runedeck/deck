## ADDED Requirements

### Requirement: Shared instructions use portable capabilities

Generic skill entrypoints and shared companions MUST avoid foreign harness literals forbidden by the source-layer policy.
They MUST prescribe a portable fallback when a required capability is unavailable.

#### Scenario: A structured question tool is unavailable

- **WHEN** the harness has no structured question tool
- **THEN** the workflow uses its prescribed plain-text fallback
- **AND** it preserves the question content and required evidence

### Requirement: Native tool scopes remain in their harness layer

Claude tool scopes MUST live in explicit Claude variants.
A metadata-only variant MUST use an additive mode and preserve the complete base procedure.

#### Scenario: A Claude metadata variant is selected

- **WHEN** assembly selects the metadata-only Claude variant
- **THEN** its native scope metadata is retained for Claude
- **AND** the portable base procedure remains intact
- **AND** the Codex bundle contains no Claude invocation literals

### Requirement: Interview capacity follows the available tool

BuildAvatar MUST retain its 20-to-30-question interview scope.
Each structured round MUST respect the available tool's actual capacity.

#### Scenario: The harness accepts fewer questions per call

- **WHEN** the tool's question capacity is below the previous round size
- **THEN** the workflow uses additional rounds
- **AND** it preserves the complete interview scope

### Requirement: Authoring compliance requires the layer gate

The authoring procedure MUST require the source-layer lint for each new or changed skill.
It MUST distinguish schema validation, rendered compatibility, and native acceptance.

#### Scenario: A new skill contains a forbidden native call

- **WHEN** the layer gate reports the forbidden call
- **THEN** the author cannot declare the skill compliant
- **AND** the report identifies the source path and finding

### Requirement: Shared rules agree with variant resolution

SkillLayout and ArtifactLength MUST describe model variants under the owning provider and exact configured model ID.
A provider or model entrypoint MUST NOT count as a second canonical skill.
UseEfficientCLI MUST prescribe the available file-reading capability without requiring a particular harness tool name.

#### Scenario: An author adds guidance for one model

- **WHEN** the author follows the shared rules to add model-specific guidance
- **THEN** the variant uses `<provider>/<exact-model-id>/SKILL.md`
- **AND** the canonical identity remains unchanged

### Requirement: Skill implementation uses the repeatable artifact loop

BuildSkill creation and validation MUST route through one implementation-loop companion.
The procedure MUST freeze requirements, worker scope, independent reviewer roles, and expected checks.
It MUST require executable evidence and return material failures to implementation or contract review.
It MUST keep missing native evidence and approval status separate from local check success.

#### Scenario: A worker reports success without current evidence

- **WHEN** the required receipt is absent, stale, or bound to another candidate
- **THEN** the author cannot declare the implementation verified
- **AND** the procedure repeats the required checks against the current candidate
