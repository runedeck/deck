# Benchmark definition

artifact_name: ExampleArtifact
artifact_kind: skill
artifact_source: runes/core/skills/ExampleArtifact
artifact_snapshot: artifact.md
model_policy: current-harness
models:
- current
repeats: 1

## Comparison

primary: with_artifact
baseline: baseline

Only the primary arm receives `artifact.md`.

## Case 1: concise rewrite

Prompt:

Rewrite `draft.md`. Keep every fact. Return only the rewritten text.

Inputs:

- `inputs/case-1/draft.md`

Assertions:

- The response keeps each number from the source.
- The response keeps each scope qualifier from the source.
- The response contains no planning narration.

## Run count

Calculate cases times two arms times models times repeats.

Confirm the cases with the user before execution.
