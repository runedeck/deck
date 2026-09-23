## ADDED Requirements

### Requirement: Reusable Across Harnesses and Models

An *instruction* [INSTRUCTION] MUST be written once and reused by every *harness* [HARNESS] and every *model* [MODEL].
The source is one file per instruction, and a harness or model difference MUST NOT fork it.

#### Scenario: Second source appears for one instruction

- **WHEN** an instruction gets a second source file beside the one it already has
- **THEN** `rune validate` reports the duplicate, and the author merges it into the source or into a harness-specific file

#### Scenario: Deployed copy is edited in place

- **WHEN** a deployed copy of an instruction in a *target* [TARGET], the tree a harness reads such as `.claude/`, differs from the instance assembly produced
- **THEN** the deployment check reports the drift, and reassembly from the source resolves it

### Requirement: Layout Is Enforced

Analysis tools MUST enforce the layout, because convention alone does not hold.
`rune validate` checks that each instruction under `runes/<domain>/` has one entrypoint with its harness-specific files beside it. mdschema checks the structure of the entrypoint. The deployment check reports a deployed copy that differs from the instance assembly produced.
Conformance with the Agent Skills reference validator is a missed requirement, listed in the coverage table.

#### Scenario: Layout rule has no analysis tool

- **WHEN** a layout rule is added and no analysis tool checks it
- **THEN** the coverage table lists the rule as a missed requirement until a tool exists

### Requirement: Harness Specifics Stay Beside the Source

Wording and quirks that only one harness needs MUST go into a separate file beside the shared instruction, in the place the layout reserves for that harness.
The file MUST say which harness it is for. It adds to the source and never replaces it.

#### Scenario: Harness needs different wording

- **WHEN** one harness needs wording the others do not
- **THEN** the wording goes into that harness's companion file beside the source, and the source itself does not change

#### Scenario: Instruction depends on one harness's hook event

- **WHEN** an instruction depends on a mechanism that only one harness has
- **THEN** the dependency moves into that harness's file, and the source works without it

### Requirement: One Instance per Harness

*Assembly* [ASSEMBLY] MUST produce one *instance* [INSTANCE] of each rune per harness, from the source plus that harness's files.
An instance per model is deferred, because no harness tells assembly which model runs.
Each instance MUST record its *provenance* [PROVENANCE]. The deployment manifest stores the instance's fingerprint, and the *sidecar* [SIDECAR] stores the sealed statement of where it came from.

#### Scenario: Assembly writes an instance

- **WHEN** assembly deploys an instruction into a target
- **THEN** the manifest records the instance's fingerprint and the sidecar records its source

#### Scenario: New harness joins

- **WHEN** a new harness joins the deployment roster
- **THEN** assembly produces that harness's instance of every instruction from the unchanged sources, and the only new files in the deck are the ones specific to that harness

### Requirement: Portable Instructions

The portable form of an instruction is the one every harness on the roster reads. Where a portable form exists, an instruction MUST use it.
The source MUST assemble and pass validation for every harness on the roster with no harness-specific file present.

#### Scenario: Harness lacks a mechanism

- **WHEN** a harness on the roster has no equivalent of a mechanism an instruction uses
- **THEN** the source still assembles and validates for that harness, and the wording that needs the mechanism is in another harness's file

[INSTRUCTION]: https://runedeck.ai/ns#Instruction
[HARNESS]: https://runedeck.ai/ns#Harness
[MODEL]: https://runedeck.ai/ns#Model
[TARGET]: https://runedeck.ai/ns#Target
[ASSEMBLY]: https://runedeck.ai/ns#Assembly
[SIDECAR]: https://runedeck.ai/ns#Sidecar
[PROVENANCE]: https://runedeck.ai/ns#Provenance
[INSTANCE]: https://runedeck.ai/ns#Instance
