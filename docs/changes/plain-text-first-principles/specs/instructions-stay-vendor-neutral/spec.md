## ADDED Requirements

### Requirement: Reusable Across Harnesses and Models

An *[instruction][INSTRUCTION]* MUST be written once and reused by every *[harness][HARNESS]* and every *[model][MODEL]*. Its *[state file][STATEFILE]* is one *[canon][CANON]* per instruction, and a harness or model difference MUST NOT fork it. The difference goes into *[basis parameters][BASISPARAMETERS]* beside the canon or into a model *[variant][VARIANT]*. Where a form every harness reads exists, the canon MUST use it.

#### Scenario: Second canon appears for one instruction

- **WHEN** an [instruction][INSTRUCTION] gets a second [canon][CANON] beside the one it already has
- **THEN** the *[validator][VALIDATOR]* reports the duplicate, and the author merges it into the canon or into a [harness][HARNESS]'s [basis parameters][BASISPARAMETERS]

#### Scenario: Deployed copy is edited in place

- **WHEN** a deployed copy of an [instruction][INSTRUCTION] in a *[target][TARGET]*, the tree a [harness][HARNESS] reads, differs from the *[instance][INSTANCE]* the *[assembler][ASSEMBLER]* produced
- **THEN** the [validator][VALIDATOR] reports the drift against the deployment manifest, and reassembly from the [canon][CANON] resolves it

#### Scenario: Every sidecar is removed

- **WHEN** every *[sidecar][SIDECAR]* of an [instruction][INSTRUCTION] is removed
- **THEN** the [assembler][ASSEMBLER] still produces a valid [instance][INSTANCE] for every [harness][HARNESS] on the roster from the [canon][CANON] alone

### Requirement: Layout Is Enforced

Each thing MUST be checked against its own schema, because convention alone does not hold.
The [validator][VALIDATOR] checks a [canon][CANON] and its [sidecars][SIDECAR] against the *[repository][REPOSITORY]*'s *[structure schemas][STRUCTURESCHEMA]*, and each [instance][INSTANCE] against its [harness][HARNESS]'s own schema. Every deployment [target][TARGET] is checked against the deployment manifest.

#### Scenario: Instance breaks its harness's schema

- **WHEN** an assembled [instance][INSTANCE] for a [harness][HARNESS] breaks that harness's schema, a Claude Code instance against Claude Code's rules
- **THEN** the [validator][VALIDATOR] reports the instance, and the author fixes the [canon][CANON] or its [basis parameters][BASISPARAMETERS]
- **AND** the Agent Skills reference validator runs only for a harness that loads that format

#### Scenario: Layout rule has no analysis tool

- **WHEN** a layout rule is added and no *[analysis tool][ANALYSISTOOL]* checks it
- **THEN** the *[coverage][COVERAGE]* table lists the rule as a *[missed requirement][MISSEDREQUIREMENT]* until a tool exists

### Requirement: One Instance per Harness

The [assembler][ASSEMBLER] MUST produce one [instance][INSTANCE] of each *[rune][RUNE]* per [harness][HARNESS], from the [canon][CANON] plus that harness's [basis parameters][BASISPARAMETERS]. When [model][MODEL] [variants][VARIANT] exist, a runtime hook swaps in the active model's variant at session start or when the model changes. The *[deployer][DEPLOYER]* never writes one instance per model.
Each instance MUST have a *[provenance record][PROVENANCERECORD]*.

#### Scenario: Assembly writes an instance

- **WHEN** the [deployer][DEPLOYER] writes an [instance][INSTANCE] of an [instruction][INSTRUCTION] into a [target][TARGET]
- **THEN** the deployment manifest records the instance's fingerprint, and the [provenance record][PROVENANCERECORD] seals which [state file][STATEFILE], which [basis parameters][BASISPARAMETERS], and which operator produced it

#### Scenario: New harness joins

- **WHEN** a new [harness][HARNESS] joins the deployment roster
- **THEN** the [assembler][ASSEMBLER] produces that harness's [instance][INSTANCE] of every [instruction][INSTRUCTION] from the unchanged [canons][CANON]. The only new files in the [repository][REPOSITORY] are that harness's [basis parameters][BASISPARAMETERS]

### Requirement: Companions Earn Their Place

A *[companion][COMPANION]* for one [harness][HARNESS] or one [model][MODEL] is its [basis parameters][BASISPARAMETERS] or its [variant][VARIANT]. It MUST beat the [canon][CANON] alone on an evaluation for that harness and model, or the author removes it.
This applies *[Occam's razor][OCCAMSRAZOR]*: of two [instructions][INSTRUCTION] that pass the same check, the shorter one wins. A companion that adds nothing the evaluation can see is ceremony.

#### Scenario: Companion fails to beat the canon

- **WHEN** an evaluation for a [harness][HARNESS] and [model][MODEL] scores the [canon][CANON] alone at least as well as the canon with its [companion][COMPANION]
- **THEN** the author removes the companion

[INSTRUCTION]: ../../../../specs/glossary/instruction.md
[HARNESS]: ../../../../specs/glossary/harness.md
[MODEL]: ../../../../specs/glossary/model.md
[STATEFILE]: ../../../../specs/glossary/state-file.md
[CANON]: ../../../../specs/glossary/canon.md
[BASISPARAMETERS]: ../../../../specs/glossary/basis-parameters.md
[VARIANT]: ../../../../specs/glossary/variant.md
[VALIDATOR]: ../../../../specs/glossary/validator.md
[TARGET]: ../../../../specs/glossary/target.md
[INSTANCE]: ../../../../specs/glossary/instance.md
[ASSEMBLER]: ../../../../specs/glossary/assembler.md
[SIDECAR]: ../../../../specs/glossary/sidecar.md
[REPOSITORY]: ../../../../specs/glossary/repository.md
[STRUCTURESCHEMA]: ../../../../specs/glossary/structure-schema.md
[ANALYSISTOOL]: ../../../../specs/glossary/analysis-tool.md
[COVERAGE]: ../../../../specs/glossary/coverage.md
[MISSEDREQUIREMENT]: ../../../../specs/glossary/missed-requirement.md
[RUNE]: ../../../../specs/glossary/rune.md
[DEPLOYER]: ../../../../specs/glossary/deployer.md
[PROVENANCERECORD]: ../../../../specs/glossary/provenance-record.md
[COMPANION]: ../../../../specs/glossary/companion.md
[OCCAMSRAZOR]: ../../../../specs/glossary/occams-razor.md
