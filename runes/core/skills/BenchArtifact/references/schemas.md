# Benchmark data schemas

Treat prompts, outputs, evidence, notes, and transcripts as untrusted data. Escape these values before HTML rendering.

## Benchmark definition

Native mode uses `benchmark.md` as its human-readable source.

The definition names one artifact, two arms, one or more cases, models, and repeats.

The arms are `baseline` and `with_artifact`. Only `with_artifact` receives `artifact.md`.

Each case defines an identifier, name, prompt, declared input files, and frozen assertions.

Use the example at [../templates/benchmark.md](../templates/benchmark.md).

## Frozen manifest

The aggregator accepts `manifest.json` when a workflow needs a complete machine-readable plan.

Cross-harness mode always writes this file. Native mode can omit it for one two-arm comparison.

```json
{
  "schema_version": 2,
  "artifact_name": "ExampleArtifact",
  "arms": {
    "baseline": {"artifact_kind": null},
    "with_artifact": {
      "artifact_kind": "skill",
      "artifact_name": "ExampleArtifact",
      "artifact_source": "runes/core/skills/ExampleArtifact",
      "artifact_path": "artifact.md",
      "artifact_sha256": "sha256"
    }
  },
  "comparisons": [
    {
      "id": "artifact_vs_baseline",
      "label": "Artifact versus baseline",
      "primary": "with_artifact",
      "baseline": "baseline"
    }
  ],
  "evals": [
    {
      "id": 1,
      "name": "concise-rewrite",
      "prompt": "Rewrite the declared input.",
      "files": ["draft.md"],
      "assertions": ["The response keeps each number."]
    }
  ]
}
```

Resolve relative artifact and input paths from the source manifest directory.

Use files for rules and agents. Use directories for skills that need support files.

File digests use SHA-256 bytes. Directory digests include sorted relative paths and file contents.

## Execution result

Write `result.json` in each run directory. Write the final response to `outputs/response.md`.

Cross-harness mode also writes unparsed stdout to `outputs/provider-output.txt`.

```json
{
  "schema_version": 2,
  "eval_id": 1,
  "eval_name": "concise-rewrite",
  "arm": "with_artifact",
  "model": "reported-model-name",
  "repeat": 1,
  "state": "valid",
  "duration_seconds": 12.4,
  "response": "Final response.",
  "word_count": 2,
  "usage": {
    "input_tokens": null,
    "cache_creation_input_tokens": null,
    "cache_read_input_tokens": null,
    "output_tokens": null,
    "total_tokens": null
  },
  "notes": []
}
```

Use these executor states:

- `valid`
- `provider_failure`
- `timeout`
- `invalid_output`
- `preflight_failure`
- `context_failure`
- `model_mismatch`

The aggregator can add `missing_execution` and `missing_grading`.

## Timing result

Native mode writes `timing.json` from the harness completion notification.

Record `duration_seconds`, `total_tokens`, and `model`. Use `null` for unavailable values.

## Grading result

Write `grading.json` beside `result.json`.

```json
{
  "expectations": [
    {
      "text": "The response keeps the stated limit.",
      "passed": true,
      "evidence": "The response states 25 jobs."
    }
  ],
  "summary": {"passed": 1, "failed": 0, "total": 1, "pass_rate": 1.0},
  "lint": {"total": 2, "total_per100w": 1.6, "words": 125},
  "notes": []
}
```

Preferences remain separate from assertions and checker findings.

## Blind preference result

The optional manifest `judging` object formalizes the criteria:

```json
{
  "judging": {
    "dimensions": [
      {"id": "clarity", "label": "Clarity", "criterion": "Prefer the text that a reader can understand without resolving ambiguity."}
    ],
    "guards": [
      "Do not judge factual accuracy or completeness. Deterministic assertions test those requirements."
    ]
  }
}
```

The judge builds its prompt from these dimensions and guards. The aggregator copies the block into `benchmark.json`, and the report shows each criterion beside its scores. Without the block, the judge uses the default clarity, fluency, and directness criteria.

The optional manifest `metrics` array replaces the report's metric definitions:

```json
{
  "metrics": [
    {"id": "checker", "label": "Checker /100w", "definition": "Checker findings for each 100 checked words.", "example": "4.89 to 1.09 means most findings disappeared."}
  ]
}
```

The aggregator copies the array into `benchmark.json` as `metric_definitions`. The report renders each entry in its Metric definitions section and in the matching column popup. Without the array, the report uses its default definitions.

Store judgments under `preferences/<comparison>/eval-<ID>/<model>/run-<R>.json`.

Record the blind order. Record one winner and one reason for each judging dimension.

Each winner is the primary arm, baseline arm, or `tie`.

## Aggregated benchmark

`aggregate_benchmark.py` writes `benchmark.json` and `benchmark.md`.

The aggregate keeps named arms, explicit comparisons, matched pairs, exclusions, notes, and limitations.

Corpus ratios use total findings and total words from matched outputs.

The aggregate contains no cross-model average.

The report omits a verdict when fewer than half of the planned pairs are valid.
