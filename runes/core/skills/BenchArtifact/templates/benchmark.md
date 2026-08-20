# Benchmark definition

artifact_name: ExampleArtifact
artifact_kind: skill
artifact_source: runes/core/skills/ExampleArtifact
artifact_snapshot: artifact.md
checker: scripts/lint.py
checker_config: config/rules.sample.json
model_policy: current-harness
models:
- current
repeats: 1

## Comparison

primary: with_artifact
baseline: baseline

Only the primary arm receives `artifact.md`.

## Case 1: concise rewrite

minimum_words: 20
maximum_words: 100

Prompt:

Rewrite `draft.md`. Keep every fact. Return only the rewritten text.

Inputs:

- `inputs/case-1/draft.md`

Assertions:

- kind: required_patterns
  text: The response keeps the stated limit.
  patterns: ["25 jobs", "up to"]
- kind: forbidden_patterns
  text: The response contains no planning narration.
  patterns: ["I will", "my plan"]
- kind: word_range
  text: The response contains 20 to 100 words.

## Run count

Calculate cases times two arms times models times repeats.

Confirm the cases with the user before execution.
