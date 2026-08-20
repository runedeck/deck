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

### Requirement: Execution Ladder

BenchArtifact SHALL offer ordered execution setups that share one manifest, one grading path, and one verdict rule: a native in-harness procedure as the default, a direct Claude and Codex invocation for a fast first table, and a cross-harness matrix behind an explicit `--cross-harness` flag. A scratch run SHALL label its output as low confidence.

#### Scenario: Cross-harness requires the flag

- **WHEN** the orchestrator is invoked without `--cross-harness`
- **THEN** it refuses to start external harness processes

### Requirement: Frozen Iterations

The cross-harness orchestrator SHALL freeze the evaluation manifest into the iteration directory before any provider call, SHALL refuse to run into an iteration that already contains benchmark runs or a different frozen manifest, and SHALL retain raw provider stdout beside each parsed response.

#### Scenario: Second invocation into one iteration

- **WHEN** a second matrix invocation targets an iteration that contains runs
- **THEN** the orchestrator exits with an error and writes nothing

### Requirement: Three-Metric Verdict

The report SHALL state one verdict per model from three signals read together: assertion pass rate, checker density per 100 checker words, and blind pairwise preferences for clarity, fluency, and directness. Blind judging SHALL be cross-vendor so no judge grades output from its own model. The report SHALL withhold a verdict when fewer than half of the planned pairs are valid.

#### Scenario: Judge assignment

- **WHEN** the judged pairs include the judge model's own output
- **THEN** a judge from another vendor covers those pairs

### Requirement: Reviewable Pairs

The report SHALL provide a pair browser over every matched pair: the baseline and treatment responses side by side with their per-run metrics, and the blind judgment with its recorded reasons beside each pair.

#### Scenario: Reviewer inspects a degraded model

- **WHEN** a reviewer selects a model and a case in the report
- **THEN** both responses, their metrics, and the pair's judgment render without network access

### Requirement: Pull Request Table

Aggregation SHALL write one compact markdown table per executed comparison: one row per model with pairs, assertion movement, checker density movement, and the three preference deltas. Comparisons without executed pairs SHALL NOT appear.

#### Scenario: Table accompanies an artifact pull request

- **WHEN** a pull request adds or changes a skill, rule, or agent
- **THEN** its body carries the benchmark table for the latest iteration
