---
name: BenchArtifact
description: "Benchmark one skill, rule, or agent against a baseline. Use native harness agents by default, or select explicit cross-harness execution. USE WHEN evaluating an artifact, comparing model behavior, or measuring context cost. NOT FOR authoring artifacts or reviewing imports."
compatibility: "Native mode requires a harness with agent support. Cross-harness mode requires Python 3.11 and Rune."
metadata:
    version: 0.3.0
allowed-tools: Bash(python3 *), Bash(mkdir *), Bash(cp *), Read, Write, Edit, Grep, Glob, Agent
---

# BenchArtifact

Measure how one artifact changes model behavior. Compare the treatment and baseline only within one model.

Store results in `$ROOT_BENCHMARK/<deck>/<artifact-name>/iteration-<N>/`. The root defaults to `~/Data/Benchmarks`.

## Prerequisites

- Read [NativeBench.md](NativeBench.md) for the default native procedure.
- Read [RuneBench.md](RuneBench.md) only when the user requests cross-harness execution.
- Snapshot the artifact before execution.
- Confirm two or three realistic cases with the user.

## Constraints

- Change only the artifact between paired runs.
- Keep prompts, files, assertions, models, and repeat counts identical.
- Use only models that the active harness exposes in native mode.
- Do not start another harness in native mode.
- Stop native execution when the baseline already contains the tested artifact.
- Keep provider failures, timeouts, invalid outputs, and exclusions separate.
- Keep missing numbers as `null`. Do not estimate token counts.
- Compute deltas from matched case and repeat pairs only.
- Do not average results across models.
- Generate each report from `benchmark.json`.

## Instructions

### Define the benchmark

Copy [templates/benchmark.md](templates/benchmark.md) to the iteration directory as `benchmark.md`.

Freeze the treatment instructions as `artifact.md`. Keep source files beside it when a skill needs support files.

Define one `baseline` arm and one `with_artifact` arm. Use a separate native comparison for another artifact.

State the run count before execution. The count is cases times arms times models times repeats.

Get explicit approval when the count exceeds 20 runs.

### Execute the benchmark

Use the native procedure unless the user requests cross-harness execution.

Use the active harness agent tool with [templates/agents/runner.md](templates/agents/runner.md).

Give `artifact.md` only to treatment runners. Never give it to baseline runners.

Report each case, arm, model, completion, and failure while the matrix runs.

### Grade and compare

Grade each valid run against the frozen assertions. Use [templates/agents/grader.md](templates/agents/grader.md).

An artifact with a measurable claim names its checker. An artifact without a dedicated checker uses [scripts/lint.py](scripts/lint.py) with a small patterns JSON. No artifact ships its own checker script for simple pattern claims.

Use [templates/agents/comparator.md](templates/agents/comparator.md) for blind clarity, fluency, and directness judgments.

Aggregate the normalized results:

```sh
python3 -m scripts.aggregate_benchmark <workspace>/iteration-<N> --artifact-name <name>
```

Render the report:

```sh
python3 -m scripts.build_report <workspace>/iteration-<N>/benchmark.json
```

### Review the result

Read the paired outputs and the aggregate metrics. Assertions protect required meaning.

Checker density measures the claimed behavior. Blind judgments measure prose quality.

Show the generated report to the user. Record sample gaps and failure causes.

## Verification

- Each pair uses one model, prompt, file set, assertion set, and repeat number.
- Each treatment run receives the frozen artifact. Each baseline run does not.
- Every planned run has a result or an explicit exclusion.
- `benchmark.json` contains no cross-model aggregate.
- The report renders without network access.
- The report gives no verdict when fewer than half of the planned pairs are valid.

## Troubleshooting

- If native context contains the artifact, use an isolated project or explicit cross-harness mode.
- If the harness cannot create agents, run one case at a time and record this limitation.
- If a model is unavailable, remove it from `benchmark.md` before any run.
- If aggregation reports a missing pair, execute that exact case, arm, model, and repeat.

## References

- [references/schemas.md](references/schemas.md) defines normalized records and report data.
