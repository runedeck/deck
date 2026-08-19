# Native harness benchmark

Use this procedure unless the user requests cross-harness execution.

## Inputs

- `benchmark.md` defines cases, assertions, models, and repeats.
- `artifact.md` contains the frozen treatment instructions.
- Declared input files contain task data.
- The active harness supplies the runner agents.

## Prepare the iteration

1. Create one new iteration directory.
2. Copy the benchmark definition to `benchmark.md`.
3. Copy the artifact instructions to `artifact.md`.
4. Copy required skill support files without content changes.
5. Record the artifact source path and SHA-256 digest.
6. Check active user and project instructions for the tested artifact.
7. Stop when the baseline context already contains the artifact.

Do not create route registries or provider subprocess commands in native mode.

## Select models

Use only model selectors that the active harness exposes to its agent tool.

Use the current model when the harness does not expose a selector. Record its exact reported name.

Reject unavailable model names before execution. Do not replace a model silently.

## Run the matrix

Create one native runner for each case, arm, model, and repeat.

Use [templates/agents/runner.md](templates/agents/runner.md) as the complete runner instruction template.

Give each runner these inputs:

- the benchmark definition path.
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

The runner writes `outputs/response.md` and `result.json`.

The parent writes `timing.json` from the native completion notification.

Keep unavailable duration and token values as `null`.

## Grade the runs

Start one grader for each valid run. Give it the frozen assertions and the response path.

The grader writes `grading.json` beside `result.json`.

Use a program for assertions that a program can verify. Do not ask a model to count exact tokens or strings.

## Record limitations

Native harness events may not expose raw provider stdout. Record that limitation instead of inventing raw output.

Native user instructions can affect both arms. Record each visible instruction that the context check does not reject.

Use explicit cross-harness mode when clean harness state or raw provider output is required.
