# Native harness benchmark

Use this procedure unless the user requests cross-harness execution.

## Inputs

- `benchmark.md` records the confirmed human-readable plan.
- `manifest.json` freezes cases, deterministic assertions, models, arms, and repeats.
- `artifact.md` contains the frozen treatment instructions.
- The benchmark definition names one checker and its optional configuration.
- Declared input files contain task data.
- The active harness supplies the runner agents.

## Prepare the iteration

1. Create one new iteration directory.
2. Copy the benchmark definition to `benchmark.md`.
3. Copy the artifact instructions to `artifact.md`.
4. Copy required skill support files without content changes.
5. Record the artifact source path and SHA-256 digest.
6. Write the confirmed plan to `manifest.json` with structured assertions.
7. Add exact model names and the repeat count under `run_plan`.
8. Validate the manifest before you start a runner:

```sh
python3 scripts/grade_iteration.py --manifest <iteration>/manifest.json --validate-only
```

Validation rejects invalid assertions and paths that leave the manifest directory.

9. Check active user and project instructions for the tested artifact.
10. Stop when the baseline context already contains the artifact.

Do not create route registries or provider subprocess commands in native mode.

## Select models

Use only model selectors that the active harness exposes to its agent tool.

Use the current model when the harness does not expose a selector. Record its exact reported name.

Reject unavailable model names before execution. Do not replace a model silently.

## Run the matrix

Create one native runner for each case, arm, model, and repeat.

Use [templates/agents/runner.md](templates/agents/runner.md) as the complete runner instruction template.

Give each runner these inputs:

- the frozen manifest path.
- the case identifier.
- the arm name.
- the model name.
- the repeat number.
- the declared input paths.
- the output directory.
- the artifact path for treatment only.

Do not include the artifact path or text in a baseline runner prompt.

Start all independent runners together when the harness supports concurrent agents.

Print one progress line when each runner starts. Print another line when it finishes or fails.

The output directory has this form:

```text
eval-<ID>-<name>/<arm>@<model>/run-<R>/
```

Percent-encode the model name as one path segment.

The runner writes `outputs/response.md` and `result.json`.

The parent writes `timing.json` from the native completion notification.

Keep unavailable duration and token values as `null`.

## Grade the runs

Run the shared deterministic grader from the BenchArtifact directory:

```sh
python3 scripts/grade_iteration.py --iteration <iteration> \
  --manifest <iteration>/manifest.json --checker <checker.py>
```

Add `--checker-config <rules.json>` when the checker needs a configuration.

The grader rejects any result whose path, identity fields, response text, or word count differs from the frozen plan.

The grader writes assertion results and checker output to each `grading.json` file.

## Judge the pairs

Use [templates/agents/comparator.md](templates/agents/comparator.md) for each matched pair.

Select a judge model from another vendor. If none is available, skip judging and record this limitation.

For each pair:

1. Shuffle the arm labels with the frozen seed, case, model, and repeat.
2. Give the comparator only the task, labeled response paths, judging file, and raw output path.
3. Do not give the comparator the arm names or blind order.
4. Validate every winner and reason in the raw judgment.
5. Add the comparison, pair, judge, seed, and blind-order fields.
6. Map each `A`, `B`, or `tie` winner to its arm field.
7. Percent-encode the model name as one path segment.
8. Write the normalized record under `preferences/<comparison>/eval-<ID>/<model>/run-<R>.json`.

Use the blind preference record in [references/preference-results.md](references/preference-results.md).

## Record limitations

Native harness events may not expose raw provider stdout. Record that limitation instead of inventing raw output.

Native user instructions can affect both arms. Record each visible instruction that the context check does not reject.

Use explicit cross-harness mode when clean harness state or raw provider output is required.
