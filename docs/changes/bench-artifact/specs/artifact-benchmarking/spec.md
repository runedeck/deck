## ADDED Requirements

### Requirement: Any Artifact Kind

BenchArtifact SHALL benchmark a skill, a rule, or an agent by running the same test cases in a with-artifact configuration and a baseline configuration defined per kind: a skill runs with the skill loaded against no skill, a rule runs with the rule text in context against no rule, and an agent runs the agent definition against a general-purpose baseline. Improving an existing artifact SHALL use the prior version as the baseline.

#### Scenario: Rule benchmark

- **WHEN** BenchArtifact is invoked on a rule
- **THEN** each test case runs once with the rule text in the runner's context and once without it, and both runs are graded against the same assertions

### Requirement: Per-Model Breakdown

Every run SHALL record the model that produced it. When more than one model is requested, every configuration SHALL run on every requested model, and aggregation SHALL report each configuration-model pair separately. Aggregates SHALL NOT average across models.

#### Scenario: Two models requested

- **WHEN** a benchmark requests two models
- **THEN** the aggregate output contains one row per configuration and model, and the with-artifact delta is computed within each model only

### Requirement: Self-Contained Comparison Report

The benchmark SHALL produce a single self-contained HTML report that renders the configuration-by-model matrix with pass rates, deltas, timing, and token counts, inlining its structured data and styles so the file makes no external requests.

#### Scenario: Report opened offline

- **WHEN** the report file is opened with no network access
- **THEN** the full comparison renders, including per-model breakdown and per-case grading detail

### Requirement: BuildSkill Delegation

BuildSkill SHALL NOT carry its own copy of the evaluation loop. Its authoring workflow SHALL reference BenchArtifact for measurement, and the extracted scripts, agent templates, and viewer SHALL live only under BenchArtifact.

#### Scenario: Skill evaluation after extraction

- **WHEN** BuildSkill's workflow reaches its evaluation step
- **THEN** it directs the session to BenchArtifact, and no evaluation script remains under BuildSkill
